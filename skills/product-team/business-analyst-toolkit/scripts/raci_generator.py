#!/usr/bin/env python3
"""
RACI Generator - Create RACI matrices from process documentation

Generates RACI (Responsible, Accountable, Consulted, Informed) matrices from
process documentation and role definitions. Supports multiple input formats and
validates RACI best practices.

Usage:
    python raci_generator.py process.json --output markdown
    python raci_generator.py process.md --template raci-template.csv
    python raci_generator.py process.json --validate-only
    python raci_generator.py --input process.json --output csv --verbose

Author: Claude Skills - Business Analyst Toolkit
Version: 1.0.0
License: MIT
"""

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 1
EXIT_PARSE_ERROR = 2
EXIT_GENERATION_ERROR = 3

# RACI codes
VALID_RACI_CODES = {'R', 'A', 'C', 'I'}

# Role keywords for automatic assignment
ROLE_KEYWORDS = {
    'A': [  # Accountable (approver, decision maker)
        'manager', 'director', 'owner', 'lead', 'head', 'chief',
        'approver', 'sponsor', 'executive', 'vp', 'ceo', 'cto', 'cfo'
    ],
    'R': [  # Responsible (doer)
        'analyst', 'engineer', 'developer', 'coordinator', 'specialist',
        'associate', 'administrator', 'assistant', 'operator', 'technician'
    ],
    'C': [  # Consulted (advisor)
        'consultant', 'advisor', 'expert', 'architect', 'strategist',
        'subject matter expert', 'sme', 'reviewer'
    ],
    'I': [  # Informed (stakeholder)
        'stakeholder', 'team', 'department', 'group', 'board',
        'committee', 'observer'
    ]
}

# Action verbs for role inference
ACTION_VERBS = {
    'R': [  # Responsible (action verbs)
        'create', 'build', 'develop', 'implement', 'execute', 'perform',
        'draft', 'prepare', 'conduct', 'analyze', 'process', 'handle',
        'complete', 'prepare', 'generate', 'produce', 'deliver'
    ],
    'A': [  # Accountable (approval verbs)
        'approve', 'authorize', 'sign-off', 'accept', 'validate',
        'finalize', 'endorse', 'ratify', 'certify', 'sanction'
    ],
    'C': [  # Consulted (advisory verbs)
        'review', 'advise', 'consult', 'recommend', 'provide input',
        'evaluate', 'assess', 'examine', 'guide', 'counsel'
    ],
    'I': [  # Informed (notification verbs)
        'notify', 'inform', 'update', 'communicate', 'report to',
        'distribute', 'share', 'brief', 'alert', 'announce'
    ]
}


class RACIGenerator:
    """Generates RACI matrices from process documentation"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.valid_raci_codes = VALID_RACI_CODES

    def generate(self, process_data: Dict[str, any], template: Optional[Dict] = None) -> Dict[str, any]:
        """Generate RACI matrix from process data"""
        if self.verbose:
            print("🔄 Generating RACI matrix...")

        # Extract or use provided roles
        if template and 'roles' in template:
            roles = template['roles']
        else:
            roles = self._extract_roles(process_data)

        if not roles:
            raise ValueError("No roles found in process data or template")

        # Extract activities
        activities = self._extract_activities(process_data)

        if not activities:
            raise ValueError("No activities found in process data")

        # Build RACI matrix
        raci_matrix = []
        for activity in activities:
            raci_entry = self._generate_raci_assignment(activity, roles, template)
            raci_matrix.append(raci_entry)

        # Build result
        result = {
            'process_name': process_data.get('process_name', 'Untitled Process'),
            'process_description': process_data.get('process_description', ''),
            'generated_at': datetime.now().isoformat(),
            'raci_matrix': raci_matrix,
            'roles': roles,
            'role_summary': self._calculate_role_summary(raci_matrix, roles),
            'validation_issues': []
        }

        # Add metadata if available
        if 'process_id' in process_data:
            result['process_id'] = process_data['process_id']

        if self.verbose:
            print(f"✅ Generated RACI matrix: {len(activities)} activities × {len(roles)} roles")

        return result

    def _extract_roles(self, process_data: Dict[str, any]) -> List[str]:
        """Extract unique roles from process data"""
        roles = set()

        # From top-level roles list
        if 'roles' in process_data:
            roles.update(process_data['roles'])

        # From process steps
        if 'steps' in process_data:
            for step in process_data['steps']:
                if 'role' in step:
                    roles.add(step['role'])

        # From RACI template if present
        if 'raci' in process_data:
            for entry in process_data['raci']:
                if 'roles' in entry:
                    roles.update(entry['roles'].keys())

        return sorted(list(roles))

    def _extract_activities(self, process_data: Dict[str, any]) -> List[Dict[str, any]]:
        """Extract activities from process data"""
        activities = []

        # From process steps
        if 'steps' in process_data:
            for step in process_data['steps']:
                activity = {
                    'id': step.get('id', f"activity_{len(activities) + 1}"),
                    'name': step.get('name', step.get('description', 'Unnamed Activity')),
                    'description': step.get('description', ''),
                    'sequence': step.get('sequence', len(activities) + 1),
                    'role': step.get('role'),  # Primary role if specified
                    'decisions': step.get('decisions', [])
                }

                # Extract additional context
                if 'inputs' in step:
                    activity['inputs'] = step['inputs']
                if 'outputs' in step:
                    activity['outputs'] = step['outputs']

                activities.append(activity)

        # From explicit activities list
        elif 'activities' in process_data:
            for act in process_data['activities']:
                activities.append(act)

        return activities

    def _generate_raci_assignment(
        self,
        activity: Dict[str, any],
        roles: List[str],
        template: Optional[Dict] = None
    ) -> Dict[str, any]:
        """Generate RACI assignments for an activity"""

        # Start with template assignments if available
        if template and 'assignments' in template:
            assignments = template['assignments'].get(activity['id'], {})
        else:
            assignments = {}

        # Fill in missing assignments using heuristics
        activity_name = activity.get('name', '').lower()
        activity_desc = activity.get('description', '').lower()
        activity_text = f"{activity_name} {activity_desc}"

        for role in roles:
            if role not in assignments:
                # Use primary role from step if available
                if activity.get('role') == role:
                    # Primary role is typically Responsible
                    assignments[role] = 'R'
                else:
                    # Use heuristics to assign RACI code
                    raci_code = self._infer_raci_code(role, activity_text, activity)
                    if raci_code:
                        assignments[role] = raci_code

        # Ensure RACI rules are followed
        assignments = self._enforce_raci_rules(assignments, activity_name)

        return {
            'activity_id': activity.get('id'),
            'activity': activity.get('name'),
            'description': activity.get('description', ''),
            'roles': assignments
        }

    def _infer_raci_code(self, role: str, activity_text: str, activity: Dict) -> Optional[str]:
        """Infer RACI code based on role name and activity description"""
        role_lower = role.lower()

        # Check role keywords
        for raci_code, keywords in ROLE_KEYWORDS.items():
            if any(keyword in role_lower for keyword in keywords):
                # Found role type, now check activity context

                # For Accountable roles (managers, directors)
                if raci_code == 'A':
                    # They're A if it's an approval/decision activity
                    if any(verb in activity_text for verb in ACTION_VERBS['A']):
                        return 'A'
                    # Otherwise consulted
                    return 'C'

                # For Responsible roles (doers)
                elif raci_code == 'R':
                    # They're R if they're performing the work
                    if any(verb in activity_text for verb in ACTION_VERBS['R']):
                        return 'R'
                    # Might be informed
                    return 'I'

                # For Consulted roles (advisors)
                elif raci_code == 'C':
                    if any(verb in activity_text for verb in ACTION_VERBS['C']):
                        return 'C'
                    return 'I'

                # For Informed roles (stakeholders)
                elif raci_code == 'I':
                    return 'I'

        # Check action verbs in activity description
        for raci_code, verbs in ACTION_VERBS.items():
            if any(verb in activity_text for verb in verbs):
                # If role seems to match the action
                if raci_code == 'R':
                    return 'R'
                elif raci_code == 'A':
                    # Only assign A if role looks managerial
                    if any(kw in role_lower for kw in ROLE_KEYWORDS['A']):
                        return 'A'
                elif raci_code == 'C':
                    return 'C'

        # Default: Informed (better to over-inform than miss someone)
        return 'I'

    def _enforce_raci_rules(self, assignments: Dict[str, str], activity_name: str) -> Dict[str, str]:
        """Enforce RACI matrix rules"""

        # Rule 1: Exactly one Accountable
        accountable_roles = [role for role, code in assignments.items() if code == 'A']

        if len(accountable_roles) == 0:
            # No A - assign to highest-level role
            for role, code in sorted(assignments.items()):
                role_lower = role.lower()
                if any(kw in role_lower for kw in ROLE_KEYWORDS['A']):
                    assignments[role] = 'A'
                    break
            else:
                # Still no A - make first R into A
                for role, code in assignments.items():
                    if code == 'R':
                        assignments[role] = 'A'
                        break

        elif len(accountable_roles) > 1:
            # Multiple A - keep first, convert others to C
            for i, role in enumerate(accountable_roles):
                if i > 0:
                    assignments[role] = 'C'

        # Rule 2: At least one Responsible
        responsible_roles = [role for role, code in assignments.items() if code == 'R']

        if len(responsible_roles) == 0:
            # Find the A and make them also R (A/R pattern)
            for role, code in assignments.items():
                if code == 'A':
                    # Keep A, but note they're also doing the work
                    # We can't show A/R in single code, so we keep A
                    # This will be flagged in validation if needed
                    break
            else:
                # No R and no A - assign first role as R
                first_role = list(assignments.keys())[0]
                assignments[first_role] = 'R'

        # Rule 3: No role should be both R and A (unless small team)
        # This is more of a warning than a strict rule

        return assignments

    def _calculate_role_summary(self, raci_matrix: List[Dict], roles: List[str]) -> Dict[str, Dict[str, int]]:
        """Calculate summary statistics for each role"""
        summary = {role: {'R': 0, 'A': 0, 'C': 0, 'I': 0, 'total': 0} for role in roles}

        for entry in raci_matrix:
            for role, code in entry['roles'].items():
                if code in VALID_RACI_CODES:
                    summary[role][code] += 1
                    summary[role]['total'] += 1

        return summary

    def validate_raci(self, raci_result: Dict[str, any]) -> List[str]:
        """Validate RACI matrix against best practices"""
        issues = []
        raci_matrix = raci_result['raci_matrix']
        role_summary = raci_result['role_summary']

        # Rule 1: Each activity must have exactly one Accountable
        for entry in raci_matrix:
            activity = entry['activity']
            accountable_count = sum(1 for code in entry['roles'].values() if code == 'A')

            if accountable_count == 0:
                issues.append({
                    'severity': 'critical',
                    'activity': activity,
                    'issue': 'No Accountable role assigned',
                    'recommendation': 'Assign exactly one Accountable role'
                })
            elif accountable_count > 1:
                issues.append({
                    'severity': 'critical',
                    'activity': activity,
                    'issue': f'Multiple Accountable roles ({accountable_count})',
                    'recommendation': 'Keep only one Accountable role per activity'
                })

        # Rule 2: Each activity must have at least one Responsible
        for entry in raci_matrix:
            activity = entry['activity']
            responsible_count = sum(1 for code in entry['roles'].values() if code == 'R')

            if responsible_count == 0:
                issues.append({
                    'severity': 'high',
                    'activity': activity,
                    'issue': 'No Responsible role assigned',
                    'recommendation': 'Assign at least one Responsible role'
                })

        # Rule 3: Check for role overload
        total_activities = len(raci_matrix)
        for role, stats in role_summary.items():
            # Too many Accountable assignments
            if stats['A'] > total_activities * 0.5:
                issues.append({
                    'severity': 'medium',
                    'role': role,
                    'issue': f"Role is Accountable for {stats['A']} activities ({stats['A']/total_activities*100:.0f}%)",
                    'recommendation': 'Consider distributing accountability across more roles'
                })

            # Too many Responsible assignments
            if stats['R'] > total_activities * 0.7:
                issues.append({
                    'severity': 'medium',
                    'role': role,
                    'issue': f"Role is Responsible for {stats['R']} activities ({stats['R']/total_activities*100:.0f}%)",
                    'recommendation': 'Consider distributing work across more roles'
                })

            # Too many Consulted assignments (consultation overload)
            if stats['C'] > total_activities * 0.6:
                issues.append({
                    'severity': 'low',
                    'role': role,
                    'issue': f"Role is Consulted on {stats['C']} activities ({stats['C']/total_activities*100:.0f}%)",
                    'recommendation': 'Reduce consultation to critical activities only'
                })

            # Role has no assignments
            if stats['total'] == 0:
                issues.append({
                    'severity': 'low',
                    'role': role,
                    'issue': 'Role has no RACI assignments',
                    'recommendation': 'Remove unused role or assign responsibilities'
                })

        # Rule 4: Check for missing role combinations
        for entry in raci_matrix:
            roles_assigned = set(entry['roles'].values())

            # Activity with only Informed roles (no work is being done)
            if roles_assigned == {'I'}:
                issues.append({
                    'severity': 'high',
                    'activity': entry['activity'],
                    'issue': 'Activity has only Informed roles',
                    'recommendation': 'Assign Responsible and Accountable roles'
                })

        return issues

    def format_markdown(self, raci_result: Dict[str, any]) -> str:
        """Format RACI matrix as markdown table"""
        lines = []

        # Header
        lines.append(f"# RACI Matrix: {raci_result['process_name']}\n")

        if raci_result.get('process_description'):
            lines.append(f"**Description:** {raci_result['process_description']}\n")

        lines.append(f"**Generated:** {raci_result['generated_at']}\n")
        lines.append("---\n")

        # Legend
        lines.append("## RACI Legend\n")
        lines.append("- **R (Responsible):** Does the work to complete the task")
        lines.append("- **A (Accountable):** Ultimately answerable for the task (only ONE per task)")
        lines.append("- **C (Consulted):** Provides input and expertise (two-way communication)")
        lines.append("- **I (Informed):** Kept up-to-date on progress (one-way communication)\n")
        lines.append("---\n")

        # RACI Matrix Table
        lines.append("## RACI Matrix\n")

        roles = raci_result['roles']
        raci_matrix = raci_result['raci_matrix']

        # Table header
        header = "| Activity |"
        for role in roles:
            header += f" {role} |"
        lines.append(header)

        # Table separator
        separator = "|" + "---|" * (len(roles) + 1)
        lines.append(separator)

        # Table rows
        for entry in raci_matrix:
            row = f"| {entry['activity']} |"
            for role in roles:
                code = entry['roles'].get(role, '-')
                row += f" {code} |"
            lines.append(row)

        lines.append("")

        # Role Summary
        lines.append("---\n")
        lines.append("## Role Summary\n")
        lines.append("| Role | Responsible | Accountable | Consulted | Informed | Total |")
        lines.append("|------|-------------|-------------|-----------|----------|-------|")

        for role in roles:
            stats = raci_result['role_summary'][role]
            lines.append(
                f"| {role} | {stats['R']} | {stats['A']} | "
                f"{stats['C']} | {stats['I']} | {stats['total']} |"
            )

        lines.append("")

        # Validation Issues
        if raci_result.get('validation_issues'):
            lines.append("---\n")
            lines.append("## Validation Issues\n")

            critical = [i for i in raci_result['validation_issues'] if i['severity'] == 'critical']
            high = [i for i in raci_result['validation_issues'] if i['severity'] == 'high']
            medium = [i for i in raci_result['validation_issues'] if i['severity'] == 'medium']
            low = [i for i in raci_result['validation_issues'] if i['severity'] == 'low']

            for severity, issues_list in [('Critical', critical), ('High', high), ('Medium', medium), ('Low', low)]:
                if issues_list:
                    lines.append(f"### {severity} Priority\n")
                    for issue in issues_list:
                        activity = issue.get('activity', issue.get('role', 'General'))
                        lines.append(f"- **{activity}**: {issue['issue']}")
                        lines.append(f"  - *Recommendation:* {issue['recommendation']}\n")

        return "\n".join(lines)

    def format_csv(self, raci_result: Dict[str, any]) -> str:
        """Format RACI matrix as CSV"""
        import io

        output = io.StringIO()
        roles = raci_result['roles']
        raci_matrix = raci_result['raci_matrix']

        writer = csv.writer(output)

        # Header row
        header = ['Activity'] + roles
        writer.writerow(header)

        # Data rows
        for entry in raci_matrix:
            row = [entry['activity']]
            for role in roles:
                code = entry['roles'].get(role, '')
                row.append(code)
            writer.writerow(row)

        return output.getvalue()

    def format_html(self, raci_result: Dict[str, any]) -> str:
        """Format RACI matrix as HTML table"""
        lines = []

        lines.append("<!DOCTYPE html>")
        lines.append("<html lang='en'>")
        lines.append("<head>")
        lines.append("<meta charset='UTF-8'>")
        lines.append(f"<title>RACI Matrix: {raci_result['process_name']}</title>")
        lines.append("<style>")
        lines.append("body { font-family: Arial, sans-serif; margin: 20px; }")
        lines.append("h1 { color: #333; }")
        lines.append("table { border-collapse: collapse; width: 100%; margin: 20px 0; }")
        lines.append("th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }")
        lines.append("th { background-color: #4CAF50; color: white; }")
        lines.append("tr:nth-child(even) { background-color: #f2f2f2; }")
        lines.append(".legend { margin: 20px 0; padding: 10px; background: #f9f9f9; border-left: 4px solid #4CAF50; }")
        lines.append(".R { background-color: #4CAF50; color: white; font-weight: bold; }")
        lines.append(".A { background-color: #2196F3; color: white; font-weight: bold; }")
        lines.append(".C { background-color: #FF9800; color: white; font-weight: bold; }")
        lines.append(".I { background-color: #9E9E9E; color: white; font-weight: bold; }")
        lines.append("</style>")
        lines.append("</head>")
        lines.append("<body>")

        lines.append(f"<h1>RACI Matrix: {raci_result['process_name']}</h1>")

        if raci_result.get('process_description'):
            lines.append(f"<p><strong>Description:</strong> {raci_result['process_description']}</p>")

        lines.append(f"<p><strong>Generated:</strong> {raci_result['generated_at']}</p>")

        # Legend
        lines.append("<div class='legend'>")
        lines.append("<h3>RACI Legend</h3>")
        lines.append("<ul>")
        lines.append("<li><strong>R (Responsible):</strong> Does the work to complete the task</li>")
        lines.append("<li><strong>A (Accountable):</strong> Ultimately answerable for the task (only ONE per task)</li>")
        lines.append("<li><strong>C (Consulted):</strong> Provides input and expertise (two-way communication)</li>")
        lines.append("<li><strong>I (Informed):</strong> Kept up-to-date on progress (one-way communication)</li>")
        lines.append("</ul>")
        lines.append("</div>")

        # RACI Table
        roles = raci_result['roles']
        raci_matrix = raci_result['raci_matrix']

        lines.append("<table>")

        # Header
        lines.append("<thead><tr>")
        lines.append("<th>Activity</th>")
        for role in roles:
            lines.append(f"<th>{role}</th>")
        lines.append("</tr></thead>")

        # Body
        lines.append("<tbody>")
        for entry in raci_matrix:
            lines.append("<tr>")
            lines.append(f"<td style='text-align: left;'>{entry['activity']}</td>")
            for role in roles:
                code = entry['roles'].get(role, '-')
                css_class = code if code in VALID_RACI_CODES else ''
                lines.append(f"<td class='{css_class}'>{code}</td>")
            lines.append("</tr>")
        lines.append("</tbody>")
        lines.append("</table>")

        lines.append("</body>")
        lines.append("</html>")

        return "\n".join(lines)


def load_input(input_path: str) -> Dict[str, any]:
    """Load process data from file"""
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # JSON format (from process_parser.py output)
    if path.suffix.lower() == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # CSV format (simple activity list)
    elif path.suffix.lower() == '.csv':
        activities = []
        roles = set()

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                activity = {
                    'id': f"activity_{i}",
                    'name': row.get('activity', row.get('name', f'Activity {i}')),
                    'description': row.get('description', ''),
                    'sequence': i
                }

                # Extract role if present
                if 'role' in row:
                    activity['role'] = row['role']
                    roles.add(row['role'])

                activities.append(activity)

        # Add any additional role columns
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for field in reader.fieldnames:
                if field not in ['activity', 'name', 'description', 'role', 'sequence']:
                    roles.add(field)

        return {
            'process_name': path.stem.replace('_', ' ').replace('-', ' ').title(),
            'activities': activities,
            'roles': sorted(list(roles)) if roles else []
        }

    # Markdown format (simple parsing)
    elif path.suffix.lower() in ['.md', '.markdown', '.txt']:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract process name from first heading
        name_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        process_name = name_match.group(1) if name_match else path.stem

        # Extract activities from numbered or bulleted lists
        activities = []

        # Try numbered lists first
        pattern = r'^\s*\d+\.\s+(.+)$'
        matches = re.findall(pattern, content, re.MULTILINE)

        if not matches:
            # Try bullet lists
            pattern = r'^\s*[-*]\s+(.+)$'
            matches = re.findall(pattern, content, re.MULTILINE)

        for i, match in enumerate(matches, 1):
            activities.append({
                'id': f"activity_{i}",
                'name': match.strip(),
                'description': match.strip(),
                'sequence': i
            })

        return {
            'process_name': process_name,
            'activities': activities,
            'roles': []
        }

    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def load_template(template_path: str) -> Dict[str, any]:
    """Load RACI template from file"""
    path = Path(template_path)

    if not path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    if path.suffix.lower() == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    elif path.suffix.lower() == '.csv':
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # First row contains role names
            roles = [col for col in reader.fieldnames if col != 'activity']

            # Read assignments
            assignments = {}
            for row in reader:
                activity_id = row['activity']
                assignments[activity_id] = {
                    role: row[role] for role in roles if row.get(role)
                }

        return {
            'roles': roles,
            'assignments': assignments
        }

    else:
        raise ValueError(f"Unsupported template format: {path.suffix}")


def main():
    parser = argparse.ArgumentParser(
        description='RACI Generator - Create RACI matrices from process documentation',
        epilog='Examples:\n'
               '  python raci_generator.py process.json --output markdown\n'
               '  python raci_generator.py process.csv --template raci-template.csv\n'
               '  python raci_generator.py process.json --validate-only\n'
               '  python raci_generator.py process.json --output json --verbose\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input', type=str, help='Input process file (JSON, CSV, or Markdown)')
    parser.add_argument('--output', '-o', type=str, default='markdown',
                        choices=['json', 'csv', 'markdown', 'html'],
                        help='Output format (default: markdown)')
    parser.add_argument('--template', '-t', type=str,
                        help='RACI template file with predefined assignments')
    parser.add_argument('--validate-only', action='store_true',
                        help='Only validate RACI matrix, do not generate output')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    parser.add_argument('--output-file', '-f', type=str,
                        help='Write output to file instead of stdout')

    args = parser.parse_args()

    try:
        # Load input
        if args.verbose:
            print(f"📥 Loading input: {args.input}")

        process_data = load_input(args.input)

        # Load template if provided
        template = None
        if args.template:
            if args.verbose:
                print(f"📋 Loading template: {args.template}")
            template = load_template(args.template)

        # Generate RACI matrix
        generator = RACIGenerator(verbose=args.verbose)
        raci_result = generator.generate(process_data, template)

        # Validate
        if args.verbose:
            print("✅ Validating RACI matrix...")

        validation_issues = generator.validate_raci(raci_result)
        raci_result['validation_issues'] = validation_issues

        # Print validation summary
        if validation_issues:
            critical = sum(1 for i in validation_issues if i['severity'] == 'critical')
            high = sum(1 for i in validation_issues if i['severity'] == 'high')
            medium = sum(1 for i in validation_issues if i['severity'] == 'medium')
            low = sum(1 for i in validation_issues if i['severity'] == 'low')

            print(f"⚠️  {len(validation_issues)} validation issues found:", file=sys.stderr)
            if critical:
                print(f"   • {critical} critical", file=sys.stderr)
            if high:
                print(f"   • {high} high", file=sys.stderr)
            if medium:
                print(f"   • {medium} medium", file=sys.stderr)
            if low:
                print(f"   • {low} low", file=sys.stderr)

            if critical > 0:
                print("❌ Critical issues must be resolved", file=sys.stderr)
                if not args.validate_only:
                    sys.exit(EXIT_VALIDATION_ERROR)
        else:
            print("✨ No validation issues found", file=sys.stderr)

        # If validate-only, stop here
        if args.validate_only:
            if critical > 0:
                sys.exit(EXIT_VALIDATION_ERROR)
            else:
                sys.exit(EXIT_SUCCESS)

        # Format output
        if args.output == 'json':
            output = json.dumps(raci_result, indent=2, ensure_ascii=False)
        elif args.output == 'csv':
            output = generator.format_csv(raci_result)
        elif args.output == 'markdown':
            output = generator.format_markdown(raci_result)
        elif args.output == 'html':
            output = generator.format_html(raci_result)
        else:
            output = json.dumps(raci_result, indent=2, ensure_ascii=False)

        # Write output
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"💾 Saved to: {args.output_file}", file=sys.stderr)
        else:
            print(output)

        # Exit with validation error if critical issues exist
        if critical > 0:
            sys.exit(EXIT_VALIDATION_ERROR)
        else:
            sys.exit(EXIT_SUCCESS)

    except FileNotFoundError as e:
        print(f"❌ File not found: {e}", file=sys.stderr)
        sys.exit(EXIT_PARSE_ERROR)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}", file=sys.stderr)
        sys.exit(EXIT_PARSE_ERROR)
    except ValueError as e:
        print(f"❌ Validation error: {e}", file=sys.stderr)
        sys.exit(EXIT_VALIDATION_ERROR)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(EXIT_GENERATION_ERROR)


if __name__ == '__main__':
    main()
