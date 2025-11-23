#!/usr/bin/env python3
"""
JQL Query Builder - Jira Query Language Generator

Generates optimized JQL queries for common Jira use cases. Supports advanced filters,
sprint queries, custom field searches, and complex boolean logic.
"""

import argparse
import json
import sys
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class JQLQueryBuilder:
    """Builds and validates JQL queries for Jira"""

    COMMON_FIELDS = [
        'project', 'status', 'assignee', 'reporter', 'priority',
        'type', 'created', 'updated', 'resolved', 'sprint',
        'labels', 'component', 'fixVersion', 'duedate'
    ]

    OPERATORS = ['=', '!=', '>', '<', '>=', '<=', '~', '!~', 'IN', 'NOT IN', 'IS', 'IS NOT']

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.query_parts = []
        self.order_by = []

    def build_sprint_query(self, sprint_name: str, project: str = None) -> str:
        """Build query for specific sprint"""
        parts = [f'sprint = "{sprint_name}"']
        if project:
            parts.append(f'project = {project}')
        return ' AND '.join(parts)

    def build_active_sprint_query(self, project: str) -> str:
        """Build query for active sprint"""
        return f'project = {project} AND sprint in openSprints()'

    def build_unresolved_bugs_query(self, project: str, priority: Optional[str] = None) -> str:
        """Build query for unresolved bugs"""
        parts = [
            f'project = {project}',
            'type = Bug',
            'status != Done',
            'status != Closed'
        ]
        if priority:
            parts.append(f'priority = {priority}')
        return ' AND '.join(parts)

    def build_overdue_tasks_query(self, project: str = None, assignee: str = None) -> str:
        """Build query for overdue tasks"""
        parts = ['duedate < now()', 'status != Done']
        if project:
            parts.append(f'project = {project}')
        if assignee:
            parts.append(f'assignee = {assignee}')
        return ' AND '.join(parts) + ' ORDER BY duedate ASC'

    def build_recently_updated_query(self, project: str, days: int = 7) -> str:
        """Build query for recently updated issues"""
        return f'project = {project} AND updated >= -{days}d ORDER BY updated DESC'

    def build_custom_query(self, conditions: List[Dict]) -> str:
        """Build custom query from conditions list"""
        parts = []
        for condition in conditions:
            field = condition.get('field')
            operator = condition.get('operator', '=')
            value = condition.get('value')

            if not field or value is None:
                continue

            # Quote string values
            if isinstance(value, str) and operator not in ['IN', 'NOT IN']:
                if ' ' in value or operator in ['~', '!~']:
                    value = f'"{value}"'

            parts.append(f'{field} {operator} {value}')

        return ' AND '.join(parts) if parts else ''

    def build_velocity_query(self, project: str, completed_sprints: int = 5) -> str:
        """Build query for velocity calculation"""
        return f'project = {project} AND sprint in closedSprints() AND status = Done ORDER BY resolutiondate DESC'

    def build_blocked_issues_query(self, project: str = None) -> str:
        """Build query for blocked issues"""
        parts = [
            'status != Done',
            '(labels = blocked OR statusCategory = "To Do")'
        ]
        if project:
            parts.insert(0, f'project = {project}')
        return ' AND '.join(parts)

    def build_epic_progress_query(self, epic_key: str) -> str:
        """Build query for issues in epic"""
        return f'"Epic Link" = {epic_key} ORDER BY status, priority DESC'

    def validate_query(self, query: str) -> Dict:
        """Validate JQL query syntax"""
        validation = {
            'valid': True,
            'warnings': [],
            'suggestions': []
        }

        # Check for common issues
        if not query:
            validation['valid'] = False
            validation['warnings'].append("Query is empty")
            return validation

        # Check for unquoted values with spaces
        if ' = ' in query:
            parts = query.split(' = ')
            for i in range(1, len(parts)):
                value = parts[i].split()[0] if parts[i] else ''
                if ' ' in value and not (value.startswith('"') or value.endswith('"')):
                    validation['warnings'].append(
                        f"Value '{value}' contains spaces but is not quoted"
                    )

        # Check for performance
        if 'ORDER BY' not in query.upper():
            validation['suggestions'].append(
                "Consider adding ORDER BY clause for better result organization"
            )

        if query.count('OR') > 5:
            validation['warnings'].append(
                "Query has many OR conditions which may impact performance"
            )

        return validation

    def format_query(self, query: str, pretty: bool = False) -> str:
        """Format JQL query for readability"""
        if not pretty:
            return query

        # Add newlines for readability
        formatted = query.replace(' AND ', '\n  AND ')
        formatted = formatted.replace(' OR ', '\n   OR ')
        return formatted

def main():
    parser = argparse.ArgumentParser(
        description="Build and optimize JQL queries for Jira",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Query Templates:
  sprint        - Issues in specific sprint
  active        - Issues in active sprint
  bugs          - Unresolved bugs
  overdue       - Overdue tasks
  recent        - Recently updated issues
  blocked       - Blocked issues
  epic          - Issues in epic
  velocity      - Velocity calculation

Examples:
  # Generate sprint query
  %(prog)s --template sprint --project PROJ --sprint "Sprint 23"

  # Find overdue tasks
  %(prog)s --template overdue --project PROJ

  # Custom query
  %(prog)s --custom '{"field":"status","value":"In Progress"}'

  # Validate existing query
  %(prog)s --validate "project = PROJ AND type = Bug"
        """
    )

    parser.add_argument(
        '--template',
        choices=['sprint', 'active', 'bugs', 'overdue', 'recent', 'blocked', 'epic', 'velocity'],
        help='Query template to use'
    )
    parser.add_argument(
        '--project',
        help='Jira project key'
    )
    parser.add_argument(
        '--sprint',
        help='Sprint name (for sprint template)'
    )
    parser.add_argument(
        '--epic',
        help='Epic key (for epic template)'
    )
    parser.add_argument(
        '--priority',
        choices=['Highest', 'High', 'Medium', 'Low', 'Lowest'],
        help='Issue priority'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days for date filters (default: 7)'
    )
    parser.add_argument(
        '--custom',
        help='Custom conditions as JSON array'
    )
    parser.add_argument(
        '--validate',
        help='Validate existing JQL query'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty print query with formatting'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    builder = JQLQueryBuilder(verbose=args.verbose)

    # Handle validation
    if args.validate:
        result = builder.validate_query(args.validate)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Query: {args.validate}\n")
            print(f"Valid: {'✅' if result['valid'] else '❌'}")
            if result['warnings']:
                print(f"\n⚠️  Warnings:")
                for w in result['warnings']:
                    print(f"  - {w}")
            if result['suggestions']:
                print(f"\n💡 Suggestions:")
                for s in result['suggestions']:
                    print(f"  - {s}")
        return

    # Generate query based on template
    query = None

    if args.template == 'sprint':
        if not args.sprint:
            print("Error: --sprint required for sprint template", file=sys.stderr)
            sys.exit(1)
        query = builder.build_sprint_query(args.sprint, args.project)

    elif args.template == 'active':
        if not args.project:
            print("Error: --project required for active template", file=sys.stderr)
            sys.exit(1)
        query = builder.build_active_sprint_query(args.project)

    elif args.template == 'bugs':
        if not args.project:
            print("Error: --project required for bugs template", file=sys.stderr)
            sys.exit(1)
        query = builder.build_unresolved_bugs_query(args.project, args.priority)

    elif args.template == 'overdue':
        query = builder.build_overdue_tasks_query(args.project)

    elif args.template == 'recent':
        if not args.project:
            print("Error: --project required for recent template", file=sys.stderr)
            sys.exit(1)
        query = builder.build_recently_updated_query(args.project, args.days)

    elif args.template == 'blocked':
        query = builder.build_blocked_issues_query(args.project)

    elif args.template == 'epic':
        if not args.epic:
            print("Error: --epic required for epic template", file=sys.stderr)
            sys.exit(1)
        query = builder.build_epic_progress_query(args.epic)

    elif args.template == 'velocity':
        if not args.project:
            print("Error: --project required for velocity template", file=sys.stderr)
            sys.exit(1)
        query = builder.build_velocity_query(args.project)

    elif args.custom:
        try:
            conditions = json.loads(args.custom)
            if not isinstance(conditions, list):
                conditions = [conditions]
            query = builder.build_custom_query(conditions)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(0)

    if query:
        formatted_query = builder.format_query(query, args.pretty)

        if args.json:
            output = {
                'query': query,
                'formatted': formatted_query,
                'validation': builder.validate_query(query)
            }
            print(json.dumps(output, indent=2))
        else:
            print(formatted_query)

            if args.verbose:
                print(f"\n📋 Copy this query to Jira:")
                print(f"   {query}")

if __name__ == "__main__":
    main()
