#!/usr/bin/env python3
"""
Sprint Backlog Optimizer - RICE-Integrated Sprint Planning

Combines RICE prioritization scores with sprint-specific factors to optimize
backlog allocation for upcoming sprints. Integrates with velocity data from
sprint_metrics_calculator.py and RICE scores from rice_prioritizer.py.

Sprint Priority = RICE_Score * Goal_Alignment * (1 - Dependency_Risk) * Expertise_Match
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Dict, List, Optional


class SprintBacklogOptimizer:
    """Optimize backlog for sprint planning with RICE integration"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def calculate_sprint_priority(self, item: Dict, sprint_goal: str = "") -> float:
        """
        Calculate sprint-specific priority combining RICE with sprint factors.

        Formula: Sprint Priority = RICE * Goal_Alignment * (1 - Dep_Risk) * Expertise

        Args:
            item: Backlog item with rice_score and sprint factors
            sprint_goal: Current sprint goal for alignment scoring

        Returns:
            Sprint priority score (0-100+ scale)
        """
        # Get RICE score (default to 50 if not present)
        rice_score = item.get('rice_score', item.get('priority_score', 50))

        # Goal alignment (0.5-1.0): How well item aligns with sprint goal
        goal_alignment = item.get('goal_alignment', 0.8)
        goal_alignment = max(0.5, min(1.0, goal_alignment))

        # Dependency risk (0.0-1.0): Risk from blocking dependencies
        dep_risk = item.get('dependency_risk', 0.0)
        dep_risk = max(0.0, min(1.0, dep_risk))
        dep_factor = 1 - dep_risk

        # Team expertise match (0.5-1.0): Does team have skills for this?
        expertise = item.get('expertise_match', 0.9)
        expertise = max(0.5, min(1.0, expertise))

        # Calculate sprint priority
        sprint_priority = rice_score * goal_alignment * dep_factor * expertise

        return round(sprint_priority, 2)

    def optimize_backlog(self, items: List[Dict], sprint_goal: str = "") -> List[Dict]:
        """
        Calculate sprint priorities and rank items for sprint planning.

        Args:
            items: List of backlog items (with optional rice_score)
            sprint_goal: Current sprint goal

        Returns:
            Sorted list with sprint_priority added
        """
        for item in items:
            item['sprint_priority'] = self.calculate_sprint_priority(item, sprint_goal)

        # Sort by sprint priority descending
        return sorted(items, key=lambda x: x['sprint_priority'], reverse=True)

    def recommend_sprint_backlog(self, items: List[Dict],
                                  velocity: int,
                                  buffer_percent: float = 0.15) -> Dict:
        """
        Recommend items for sprint based on team velocity.

        Args:
            items: Optimized backlog items
            velocity: Average team velocity in story points
            buffer_percent: Safety buffer (default: 15%)

        Returns:
            Sprint recommendation with committed and stretch items
        """
        target_capacity = int(velocity * (1 - buffer_percent))
        max_capacity = velocity

        committed_items = []
        stretch_items = []
        committed_points = 0
        stretch_points = 0

        for item in items:
            points = item.get('story_points', item.get('effort', 0))

            if committed_points + points <= target_capacity:
                committed_items.append(item)
                committed_points += points
            elif committed_points + points <= max_capacity:
                stretch_items.append(item)
                stretch_points += points

        return {
            'committed_items': committed_items,
            'committed_points': committed_points,
            'committed_count': len(committed_items),
            'stretch_items': stretch_items,
            'stretch_points': stretch_points,
            'stretch_count': len(stretch_items),
            'velocity': velocity,
            'target_capacity': target_capacity,
            'buffer_points': velocity - target_capacity,
            'utilization': round(committed_points / velocity * 100, 1) if velocity > 0 else 0
        }

    def assess_risks(self, items: List[Dict]) -> List[Dict]:
        """
        Identify and assess risks in recommended sprint backlog.

        Args:
            items: Sprint items to assess

        Returns:
            List of risk assessments
        """
        risks = []

        # Check for dependency risks
        dep_items = [i for i in items if i.get('dependency_risk', 0) > 0.3]
        if dep_items:
            risks.append({
                'type': 'dependency',
                'severity': 'high' if any(i.get('dependency_risk', 0) > 0.6 for i in dep_items) else 'medium',
                'items': [i.get('id', i.get('name', 'Unknown')) for i in dep_items],
                'mitigation': 'Resolve dependencies before sprint start or coordinate with dependent teams'
            })

        # Check for expertise gaps
        expertise_gaps = [i for i in items if i.get('expertise_match', 1) < 0.7]
        if expertise_gaps:
            risks.append({
                'type': 'expertise_gap',
                'severity': 'medium',
                'items': [i.get('id', i.get('name', 'Unknown')) for i in expertise_gaps],
                'mitigation': 'Consider pair programming or knowledge transfer sessions'
            })

        # Check for large items
        large_items = [i for i in items if i.get('story_points', 0) > 8]
        if large_items:
            risks.append({
                'type': 'large_stories',
                'severity': 'medium',
                'items': [i.get('id', i.get('name', 'Unknown')) for i in large_items],
                'mitigation': 'Break down stories larger than 8 points before sprint start'
            })

        # Check for low goal alignment
        low_alignment = [i for i in items if i.get('goal_alignment', 1) < 0.6]
        if low_alignment:
            risks.append({
                'type': 'goal_misalignment',
                'severity': 'low',
                'items': [i.get('id', i.get('name', 'Unknown')) for i in low_alignment],
                'mitigation': 'Discuss with Product Owner - consider deferring to future sprint'
            })

        return risks

    def generate_mcp_commands(self, sprint_name: str, items: List[Dict],
                               board_key: str = "TEAM") -> List[str]:
        """
        Generate MCP commands for Jira sprint creation.

        Args:
            sprint_name: Name for the new sprint
            items: Items to add to sprint
            board_key: Jira board key

        Returns:
            List of MCP command strings
        """
        commands = []

        # Create sprint command
        commands.append(f'# Create new sprint in Jira')
        commands.append(f'mcp__atlassian__create_sprint board="{board_key}" name="{sprint_name}"')

        # Move issues command
        if items:
            issue_ids = [i.get('id', '') for i in items if i.get('id')]
            if issue_ids:
                ids_str = ','.join(issue_ids)
                commands.append(f'\n# Add items to sprint')
                commands.append(f'mcp__atlassian__move_issues sprint="{sprint_name}" issues="{ids_str}"')

        return commands


def load_from_json(filepath: str) -> List[Dict]:
    """Load backlog items from JSON file (supports RICE output format)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

        # Handle RICE prioritizer output format
        if isinstance(data, dict):
            if 'features' in data:
                return data['features']
            elif 'items' in data:
                return data['items']
            elif 'prioritized_items' in data:
                return data['prioritized_items']

        # Direct array format
        if isinstance(data, list):
            return data

        raise ValueError("Unrecognized JSON format")


def load_from_csv(filepath: str) -> List[Dict]:
    """Load backlog items from CSV file"""
    items = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = {
                'id': row.get('id', row.get('key', '')),
                'name': row.get('name', row.get('title', '')),
                'story_points': int(row.get('story_points', row.get('effort', row.get('points', 0)))),
                'rice_score': float(row.get('rice_score', row.get('priority_score', 50))),
                'goal_alignment': float(row.get('goal_alignment', 0.8)),
                'dependency_risk': float(row.get('dependency_risk', 0)),
                'expertise_match': float(row.get('expertise_match', 0.9))
            }
            items.append(item)
    return items


def detect_and_load(filepath: str) -> List[Dict]:
    """Detect file format and load accordingly"""
    path = Path(filepath)
    suffix = path.suffix.lower()

    if suffix == '.json':
        return load_from_json(filepath)
    elif suffix == '.csv':
        return load_from_csv(filepath)
    else:
        # Try JSON first
        try:
            return load_from_json(filepath)
        except (json.JSONDecodeError, ValueError):
            return load_from_csv(filepath)


def format_text_output(recommendation: Dict, risks: List[Dict],
                        mcp_commands: Optional[List[str]] = None,
                        sprint_goal: str = "") -> str:
    """Format results as human-readable text"""
    output = []
    output.append("=" * 60)
    output.append("SPRINT BACKLOG OPTIMIZATION")
    output.append("=" * 60)

    if sprint_goal:
        output.append(f"\nSprint Goal: {sprint_goal}")

    output.append(f"\n📊 CAPACITY PLANNING")
    output.append("-" * 60)
    output.append(f"Team Velocity: {recommendation['velocity']} points")
    output.append(f"Target Capacity (85%): {recommendation['target_capacity']} points")
    output.append(f"Buffer: {recommendation['buffer_points']} points")
    output.append(f"Utilization: {recommendation['utilization']}%")

    # Committed items
    output.append(f"\n✅ COMMITTED ITEMS ({recommendation['committed_count']} items, {recommendation['committed_points']} points)")
    output.append("-" * 60)
    for item in recommendation['committed_items']:
        name = item.get('name', item.get('title', 'Unnamed'))[:30]
        points = item.get('story_points', item.get('effort', 0))
        priority = item.get('sprint_priority', 0)
        output.append(f"  [{points} pts] {item.get('id', '-')}: {name} (Priority: {priority})")

    # Stretch items
    if recommendation['stretch_items']:
        output.append(f"\n🎯 STRETCH ITEMS ({recommendation['stretch_count']} items, {recommendation['stretch_points']} points)")
        output.append("-" * 60)
        for item in recommendation['stretch_items']:
            name = item.get('name', item.get('title', 'Unnamed'))[:30]
            points = item.get('story_points', item.get('effort', 0))
            output.append(f"  [{points} pts] {item.get('id', '-')}: {name}")

    # Risks
    if risks:
        output.append(f"\n⚠️  RISK ASSESSMENT ({len(risks)} risks identified)")
        output.append("-" * 60)
        for risk in risks:
            output.append(f"  [{risk['severity'].upper()}] {risk['type'].replace('_', ' ').title()}")
            output.append(f"    Items: {', '.join(risk['items'][:3])}")
            output.append(f"    Mitigation: {risk['mitigation']}")

    # MCP commands
    if mcp_commands:
        output.append(f"\n🔧 MCP COMMANDS (Copy to execute)")
        output.append("-" * 60)
        for cmd in mcp_commands:
            output.append(cmd)

    output.append("")
    output.append("=" * 60)
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Optimize backlog for sprint planning with RICE integration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic optimization with velocity
  %(prog)s backlog.json --velocity 30

  # With sprint goal for alignment scoring
  %(prog)s rice_output.json --velocity 25 --sprint-goal "Improve authentication"

  # Generate MCP commands for Jira
  %(prog)s backlog.json --velocity 30 --sprint-name "Sprint 24" --board TEAM

  # JSON output for integration
  %(prog)s backlog.json --velocity 30 --json

  # Use velocity history (calculates average)
  %(prog)s backlog.json --velocity-history 28 30 25 27

Input Formats Supported:
  - RICE prioritizer JSON output (from rice_prioritizer.py)
  - prioritize_backlog.py JSON output
  - CSV with columns: id, name, story_points, rice_score, goal_alignment, dependency_risk, expertise_match

Sprint Priority Formula:
  Sprint_Priority = RICE_Score * Goal_Alignment * (1 - Dependency_Risk) * Expertise_Match
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='JSON or CSV file with backlog items (supports RICE output)'
    )
    parser.add_argument(
        '--velocity',
        type=int,
        help='Team velocity in story points'
    )
    parser.add_argument(
        '--velocity-history',
        nargs='+',
        type=int,
        help='Historical velocity values (calculates average)'
    )
    parser.add_argument(
        '--sprint-goal',
        type=str,
        default='',
        help='Sprint goal for alignment scoring'
    )
    parser.add_argument(
        '--sprint-name',
        type=str,
        help='Sprint name for MCP commands'
    )
    parser.add_argument(
        '--board',
        type=str,
        default='TEAM',
        help='Jira board key (default: TEAM)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--output', '-o',
        help='Write output to file'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Determine velocity
    velocity = args.velocity
    if args.velocity_history:
        velocity = int(mean(args.velocity_history))
        if args.verbose:
            print(f"Calculated average velocity: {velocity} from history", file=sys.stderr)

    if not velocity:
        velocity = 30  # Default velocity
        if args.verbose:
            print(f"Using default velocity: {velocity}", file=sys.stderr)

    # Load data
    if not args.input:
        if args.verbose:
            print("No input file specified, using sample data", file=sys.stderr)
        items = [
            {'id': 'PROJ-101', 'name': 'User Authentication', 'story_points': 8, 'rice_score': 120, 'goal_alignment': 0.9, 'dependency_risk': 0.1, 'expertise_match': 0.9},
            {'id': 'PROJ-102', 'name': 'Password Reset Flow', 'story_points': 3, 'rice_score': 80, 'goal_alignment': 0.8, 'dependency_risk': 0.0, 'expertise_match': 1.0},
            {'id': 'PROJ-103', 'name': 'OAuth Integration', 'story_points': 5, 'rice_score': 100, 'goal_alignment': 0.95, 'dependency_risk': 0.2, 'expertise_match': 0.7},
            {'id': 'PROJ-104', 'name': 'Session Management', 'story_points': 5, 'rice_score': 90, 'goal_alignment': 0.85, 'dependency_risk': 0.3, 'expertise_match': 0.8},
            {'id': 'PROJ-105', 'name': 'Audit Logging', 'story_points': 3, 'rice_score': 60, 'goal_alignment': 0.5, 'dependency_risk': 0.0, 'expertise_match': 1.0},
            {'id': 'PROJ-106', 'name': 'Real-time Notifications', 'story_points': 13, 'rice_score': 70, 'goal_alignment': 0.4, 'dependency_risk': 0.5, 'expertise_match': 0.6},
            {'id': 'PROJ-107', 'name': 'Rate Limiting', 'story_points': 2, 'rice_score': 50, 'goal_alignment': 0.7, 'dependency_risk': 0.0, 'expertise_match': 0.95},
        ]
    else:
        if args.verbose:
            print(f"Loading backlog from: {args.input}", file=sys.stderr)
        try:
            items = detect_and_load(args.input)
        except FileNotFoundError:
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error loading file: {e}", file=sys.stderr)
            sys.exit(1)

    # Optimize
    optimizer = SprintBacklogOptimizer(verbose=args.verbose)

    if args.verbose:
        print(f"Optimizing {len(items)} items for velocity {velocity}...", file=sys.stderr)

    optimized = optimizer.optimize_backlog(items, args.sprint_goal)
    recommendation = optimizer.recommend_sprint_backlog(optimized, velocity)
    risks = optimizer.assess_risks(recommendation['committed_items'])

    # Generate MCP commands if sprint name provided
    mcp_commands = None
    if args.sprint_name:
        mcp_commands = optimizer.generate_mcp_commands(
            args.sprint_name,
            recommendation['committed_items'],
            args.board
        )

    # Format output
    if args.json:
        result = {
            'metadata': {
                'tool': 'sprint_backlog_optimizer',
                'version': '1.0.0',
                'generated_at': datetime.now().isoformat(),
                'velocity': velocity,
                'sprint_goal': args.sprint_goal,
                'formula': 'Sprint_Priority = RICE * Goal_Alignment * (1 - Dep_Risk) * Expertise'
            },
            'recommendation': recommendation,
            'risks': risks,
            'optimized_backlog': optimized
        }
        if mcp_commands:
            result['mcp_commands'] = mcp_commands

        output = json.dumps(result, indent=2)
    else:
        output = format_text_output(recommendation, risks, mcp_commands, args.sprint_goal)

    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Output saved to: {args.output}")
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()
