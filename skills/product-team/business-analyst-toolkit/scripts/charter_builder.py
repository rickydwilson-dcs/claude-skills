#!/usr/bin/env python3
"""
Charter Builder - Generate process improvement charters

Purpose:
    Generate comprehensive process improvement charters from process analysis data,
    combining scope, objectives, success metrics, and stakeholder information.

Usage:
    # Basic charter generation
    python charter_builder.py --process "Customer Onboarding" --objectives "Reduce cycle time"

    # With gap analysis and stakeholder data
    python charter_builder.py --process process.json --gaps gaps.json --stakeholders stakeholders.json

    # Custom template with HTML output
    python charter_builder.py --process "Onboarding" --objectives obj.txt --template charter.md --output html

    # JSON export for integration
    python charter_builder.py --process process.json --output json

Features:
    - Parse process analysis results (gap_analyzer.py, process_parser.py)
    - Import stakeholder data (stakeholder_mapper.py)
    - Generate formatted charters (markdown, HTML, JSON, PDF)
    - Validate charter completeness
    - Cross-reference with templates

Exit Codes:
    0 - Success
    1 - Validation error (missing required sections)
    2 - Parse error (invalid input format)
    3 - Generation error (charter creation failed)

Author: Claude Skills - Business Analyst Toolkit
Version: 1.0.0
"""

import argparse
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 1
EXIT_PARSE_ERROR = 2
EXIT_GENERATION_ERROR = 3


class CharterBuilder:
    """Generates process improvement charters"""

    def __init__(self, template_path: Optional[str] = None, verbose: bool = False):
        """
        Initialize charter builder

        Args:
            template_path: Path to custom charter template
            verbose: Enable verbose output
        """
        self.template_path = template_path
        self.verbose = verbose
        self.required_sections = [
            'process_info',
            'executive_summary',
            'current_state',
            'objectives',
            'scope',
            'success_metrics',
            'stakeholders',
            'timeline',
            'resources',
            'risks'
        ]

        # Default strategy templates
        self.strategy_templates = {
            'efficiency': {
                'focus': 'Reduce cycle time and eliminate waste',
                'metrics': ['Cycle Time', 'Cost per Transaction', 'Error Rate']
            },
            'quality': {
                'focus': 'Improve process quality and reduce defects',
                'metrics': ['Defect Rate', 'First-Time Quality', 'Customer Satisfaction']
            },
            'capacity': {
                'focus': 'Increase throughput and capacity',
                'metrics': ['Throughput', 'Capacity Utilization', 'Lead Time']
            },
            'experience': {
                'focus': 'Enhance customer/user experience',
                'metrics': ['CSAT Score', 'NPS', 'Time to Value']
            }
        }

    def log(self, message: str, level: str = 'INFO'):
        """Log message if verbose mode enabled"""
        if self.verbose:
            print(f"[{level}] {message}", file=sys.stderr)

    def parse_input_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse input file (JSON, TXT, CSV)

        Args:
            file_path: Path to input file

        Returns:
            Parsed data dictionary

        Raises:
            ValueError: If file format is unsupported or parsing fails
        """
        path = Path(file_path)
        if not path.exists():
            raise ValueError(f"File not found: {file_path}")

        self.log(f"Parsing input file: {file_path}")

        # Try JSON first
        if path.suffix.lower() == '.json':
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                self.log(f"Parsed JSON with {len(data)} top-level keys")
                return data
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON: {e}")

        # Try text file
        elif path.suffix.lower() in ['.txt', '.md']:
            with open(path, 'r') as f:
                content = f.read()
            return {'content': content, 'source': str(path)}

        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

    def parse_process_data(self, process_input: str) -> Dict[str, Any]:
        """
        Parse process information from string or file

        Args:
            process_input: Process name or path to process file

        Returns:
            Process data dictionary
        """
        # Check if it's a file path
        if Path(process_input).exists():
            data = self.parse_input_file(process_input)

            # If it's already structured data
            if isinstance(data, dict) and 'process_name' in data:
                return data

            # If it's plain text, create basic structure
            return {
                'process_name': Path(process_input).stem.replace('_', ' ').title(),
                'description': data.get('content', ''),
                'source': process_input
            }

        # Otherwise, treat as process name
        return {
            'process_name': process_input,
            'description': f"Process improvement initiative for {process_input}",
            'source': 'user_input'
        }

    def parse_objectives(self, objectives_input: str) -> List[Dict[str, Any]]:
        """
        Parse objectives from string or file

        Args:
            objectives_input: Objectives text or file path

        Returns:
            List of objective dictionaries
        """
        # Check if it's a file
        if Path(objectives_input).exists():
            data = self.parse_input_file(objectives_input)

            # If it's structured JSON
            if isinstance(data, dict) and 'objectives' in data:
                return data['objectives']

            # If it's plain text
            content = data.get('content', objectives_input)
        else:
            content = objectives_input

        # Parse objectives from text
        objectives = []
        lines = content.strip().split('\n')

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Remove bullet points, numbers
            clean_line = re.sub(r'^[\d\.\-\*\+]+\s*', '', line)

            if clean_line:
                objectives.append({
                    'id': f"OBJ-{i:03d}",
                    'description': clean_line,
                    'priority': 'High' if i <= 3 else 'Medium',
                    'measurable': self._is_measurable(clean_line)
                })

        return objectives

    def _is_measurable(self, objective: str) -> bool:
        """Check if objective contains measurable elements"""
        measurable_patterns = [
            r'\d+%',  # Percentages
            r'\d+\s*(days?|hours?|minutes?|weeks?|months?)',  # Time units
            r'(reduce|increase|improve|decrease)\s+\w+\s+by',  # Improvement language
            r'from\s+[\d\.]+\s+to\s+[\d\.]+',  # From X to Y
            r'<|>|≤|≥',  # Comparison operators
        ]

        return any(re.search(pattern, objective.lower()) for pattern in measurable_patterns)

    def generate_charter_id(self, process_name: str) -> str:
        """
        Generate unique charter ID

        Args:
            process_name: Name of the process

        Returns:
            Charter ID (e.g., PIC-2025-001)
        """
        year = datetime.now().year
        # Use hash of process name for uniqueness
        hash_val = abs(hash(process_name)) % 1000
        return f"PIC-{year}-{hash_val:03d}"

    def extract_current_state(self, gaps_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract current state metrics from gap analysis data

        Args:
            gaps_data: Gap analysis results

        Returns:
            Current state summary
        """
        if not gaps_data:
            return {
                'completeness': 'Unknown',
                'critical_gaps': 0,
                'cycle_time': 'Not specified',
                'error_rate': 'Not specified',
                'summary': 'Current state analysis pending'
            }

        # Extract from gap_analyzer.py output
        summary = gaps_data.get('summary', {})

        return {
            'completeness': f"{summary.get('process_completeness', 0)}%",
            'critical_gaps': summary.get('critical_gaps', 0),
            'cycle_time': summary.get('cycle_time', 'Unknown'),
            'error_rate': summary.get('error_rate', 'Unknown'),
            'summary': summary.get('overall_assessment', 'Current state requires improvement'),
            'gaps': gaps_data.get('gaps', [])[:5]  # Top 5 gaps
        }

    def generate_scope(self, objectives: List[Dict[str, Any]],
                       gaps_data: Optional[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Generate scope section (in scope / out of scope)

        Args:
            objectives: List of objectives
            gaps_data: Gap analysis data

        Returns:
            Dictionary with 'in_scope' and 'out_of_scope' lists
        """
        in_scope = []
        out_of_scope = []

        # Extract scope from objectives
        for obj in objectives:
            desc = obj['description']

            # Items typically in scope
            if any(keyword in desc.lower() for keyword in
                   ['improve', 'reduce', 'eliminate', 'automate', 'streamline', 'optimize']):
                in_scope.append(desc)

        # If we have gaps data, add gap-related scope
        if gaps_data and 'gaps' in gaps_data:
            for gap in gaps_data['gaps'][:3]:  # Top 3 gaps
                if gap.get('severity') in ['Critical', 'High']:
                    in_scope.append(f"Address: {gap.get('description', 'Unknown gap')}")

        # Default scope items if nothing specific
        if not in_scope:
            in_scope = [
                'Process steps identified in current state analysis',
                'Key stakeholder roles and responsibilities',
                'Existing systems and tools',
                'Measurable process metrics'
            ]

        # Common out-of-scope items
        out_of_scope = [
            'Changes to organizational structure',
            'Major system replacements (require separate IT project)',
            'Processes outside defined boundaries',
            'Items requiring executive-level approval'
        ]

        return {
            'in_scope': in_scope[:6],  # Max 6 items
            'out_of_scope': out_of_scope[:4]  # Max 4 items
        }

    def generate_success_metrics(self, objectives: List[Dict[str, Any]],
                                  current_state: Dict[str, Any],
                                  strategy: str = 'efficiency') -> List[Dict[str, Any]]:
        """
        Generate success metrics table

        Args:
            objectives: List of objectives
            current_state: Current state data
            strategy: Improvement strategy type

        Returns:
            List of metric dictionaries
        """
        metrics = []

        # Get strategy-specific metrics
        strategy_metrics = self.strategy_templates.get(strategy, {}).get('metrics', [])

        # Common metrics with current/target values
        metric_templates = {
            'Cycle Time': {
                'current': current_state.get('cycle_time', 'X days'),
                'target': 'Y days (50% reduction)',
                'measurement': 'Process tracking system'
            },
            'Error Rate': {
                'current': current_state.get('error_rate', 'X%'),
                'target': '<5%',
                'measurement': 'Quality audit'
            },
            'Cost per Transaction': {
                'current': '$X',
                'target': '$Y (30% reduction)',
                'measurement': 'Financial system'
            },
            'Customer Satisfaction': {
                'current': 'X/10',
                'target': 'Y/10 (>8.0)',
                'measurement': 'Post-process survey'
            },
            'Throughput': {
                'current': 'X units/day',
                'target': 'Y units/day (25% increase)',
                'measurement': 'Production tracking'
            },
            'Defect Rate': {
                'current': 'X%',
                'target': '<2%',
                'measurement': 'Quality control system'
            },
            'Lead Time': {
                'current': 'X hours',
                'target': 'Y hours (40% reduction)',
                'measurement': 'Time tracking'
            }
        }

        # Add strategy-specific metrics
        for metric_name in strategy_metrics:
            if metric_name in metric_templates:
                metric = metric_templates[metric_name].copy()
                metric['name'] = metric_name
                metrics.append(metric)

        # Add 2-3 default metrics if list is short
        if len(metrics) < 3:
            defaults = ['Cycle Time', 'Error Rate', 'Customer Satisfaction']
            for metric_name in defaults:
                if metric_name not in [m['name'] for m in metrics]:
                    metric = metric_templates[metric_name].copy()
                    metric['name'] = metric_name
                    metrics.append(metric)

        return metrics[:5]  # Max 5 metrics

    def extract_stakeholders(self, stakeholder_data: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract stakeholder information

        Args:
            stakeholder_data: Stakeholder mapping data

        Returns:
            List of stakeholder dictionaries
        """
        if not stakeholder_data:
            return [
                {
                    'name': 'Process Owner',
                    'role': 'Director/Manager',
                    'raci': 'A',
                    'engagement': 'Manage Closely'
                },
                {
                    'name': 'Executive Sponsor',
                    'role': 'VP/C-Level',
                    'raci': 'A',
                    'engagement': 'Keep Satisfied'
                },
                {
                    'name': 'Team Members',
                    'role': 'Individual Contributors',
                    'raci': 'R',
                    'engagement': 'Keep Informed'
                }
            ]

        # Extract from stakeholder_mapper.py output
        stakeholders = []

        # Check for RACI matrix format
        if 'raci_matrix' in stakeholder_data:
            for role, data in stakeholder_data['raci_matrix'].items():
                stakeholders.append({
                    'name': data.get('name', role),
                    'role': role,
                    'raci': data.get('primary_raci', 'I'),
                    'engagement': data.get('engagement_strategy', 'Keep Informed')
                })

        # Check for stakeholder list format
        elif 'stakeholders' in stakeholder_data:
            for sh in stakeholder_data['stakeholders']:
                stakeholders.append({
                    'name': sh.get('name', 'Unknown'),
                    'role': sh.get('role', 'Stakeholder'),
                    'raci': sh.get('raci', 'I'),
                    'engagement': sh.get('engagement', 'Keep Informed')
                })

        return stakeholders[:8]  # Max 8 stakeholders

    def generate_timeline(self, objectives: List[Dict[str, Any]],
                          duration_weeks: int = 12) -> List[Dict[str, Any]]:
        """
        Generate project timeline with milestones

        Args:
            objectives: List of objectives
            duration_weeks: Total project duration in weeks

        Returns:
            List of milestone dictionaries
        """
        start_date = datetime.now()

        # Standard timeline phases
        phases = [
            {'name': 'Kickoff', 'week': 1, 'deliverable': 'Charter approved, team assembled'},
            {'name': 'Analysis Complete', 'week': duration_weeks // 4,
             'deliverable': 'Current state mapped, root causes identified'},
            {'name': 'Solution Design', 'week': duration_weeks // 3,
             'deliverable': 'Future state designed, solutions prioritized'},
            {'name': 'Implementation', 'week': int(duration_weeks * 0.6),
             'deliverable': 'Changes implemented, training completed'},
            {'name': 'Testing', 'week': int(duration_weeks * 0.8),
             'deliverable': 'Pilot tested, issues resolved'},
            {'name': 'Launch', 'week': duration_weeks,
             'deliverable': 'Full rollout, monitoring established'}
        ]

        milestones = []
        for phase in phases:
            milestone_date = start_date + timedelta(weeks=phase['week'] - 1)
            milestones.append({
                'name': phase['name'],
                'week': phase['week'],
                'date': milestone_date.strftime('%Y-%m-%d'),
                'deliverable': phase['deliverable']
            })

        return milestones

    def estimate_resources(self, objectives: List[Dict[str, Any]],
                           complexity: str = 'medium') -> Dict[str, Any]:
        """
        Estimate resource requirements

        Args:
            objectives: List of objectives
            complexity: Project complexity (low, medium, high)

        Returns:
            Resource estimates dictionary
        """
        # Base hours by role and complexity
        base_hours = {
            'low': {'analyst': 40, 'owner': 20, 'development': 0, 'budget': 10000},
            'medium': {'analyst': 80, 'owner': 40, 'development': 80, 'budget': 50000},
            'high': {'analyst': 160, 'owner': 80, 'development': 240, 'budget': 150000}
        }

        hours = base_hours.get(complexity, base_hours['medium'])

        # Adjust based on number of objectives
        multiplier = min(len(objectives) / 3.0, 2.0)  # Max 2x multiplier

        return {
            'business_analyst': int(hours['analyst'] * multiplier),
            'process_owner': int(hours['owner'] * multiplier),
            'development_team': int(hours['development'] * multiplier),
            'budget': int(hours['budget'] * multiplier),
            'complexity': complexity
        }

    def generate_risks(self, objectives: List[Dict[str, Any]],
                       stakeholders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate risk assessment

        Args:
            objectives: List of objectives
            stakeholders: List of stakeholders

        Returns:
            List of risk dictionaries
        """
        # Common risks by category
        common_risks = [
            {
                'risk': 'Stakeholder resistance to change',
                'mitigation': 'Early engagement, clear communication, visible sponsorship',
                'probability': 'Medium',
                'impact': 'High'
            },
            {
                'risk': 'Resource availability constraints',
                'mitigation': 'Secure commitments upfront, build buffer into timeline',
                'probability': 'Medium',
                'impact': 'Medium'
            },
            {
                'risk': 'Technical complexity underestimated',
                'mitigation': 'Phased rollout, pilot testing, technical review gates',
                'probability': 'Low',
                'impact': 'High'
            },
            {
                'risk': 'Scope creep beyond initial charter',
                'mitigation': 'Clear scope documentation, change control process',
                'probability': 'High',
                'impact': 'Medium'
            },
            {
                'risk': 'Insufficient data for baseline metrics',
                'mitigation': 'Early data collection plan, proxy metrics if needed',
                'probability': 'Medium',
                'impact': 'Medium'
            }
        ]

        # Return 3-5 risks
        return common_risks[:min(len(objectives) + 2, 5)]

    def build_charter(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate charter from input data

        Args:
            data: Input data dictionary containing:
                - process: Process information
                - objectives: List of objectives
                - gaps: Optional gap analysis data
                - stakeholders: Optional stakeholder data
                - strategy: Optional improvement strategy
                - timeline_weeks: Optional duration

        Returns:
            Complete charter dictionary
        """
        self.log("Building charter from input data")

        # Extract components
        process_data = data.get('process', {})
        objectives = data.get('objectives', [])
        gaps_data = data.get('gaps')
        stakeholder_data = data.get('stakeholders')
        strategy = data.get('strategy', 'efficiency')
        timeline_weeks = data.get('timeline_weeks', 12)
        complexity = data.get('complexity', 'medium')

        # Generate charter components
        charter_id = self.generate_charter_id(process_data.get('process_name', 'Unknown'))
        current_state = self.extract_current_state(gaps_data)
        scope = self.generate_scope(objectives, gaps_data)
        metrics = self.generate_success_metrics(objectives, current_state, strategy)
        stakeholders = self.extract_stakeholders(stakeholder_data)
        timeline = self.generate_timeline(objectives, timeline_weeks)
        resources = self.estimate_resources(objectives, complexity)
        risks = self.generate_risks(objectives, stakeholders)

        # Build charter
        charter = {
            'process_info': {
                'process_name': process_data.get('process_name', 'Unknown Process'),
                'process_owner': process_data.get('owner', 'TBD'),
                'charter_date': datetime.now().strftime('%Y-%m-%d'),
                'charter_id': charter_id
            },
            'executive_summary': self._generate_executive_summary(
                process_data, objectives, current_state
            ),
            'current_state': current_state,
            'objectives': objectives,
            'scope': scope,
            'success_metrics': metrics,
            'stakeholders': stakeholders,
            'timeline': timeline,
            'resources': resources,
            'risks': risks,
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'strategy': strategy,
                'version': '1.0'
            }
        }

        self.log(f"Charter generated: {charter_id}")
        return charter

    def _generate_executive_summary(self, process_data: Dict[str, Any],
                                     objectives: List[Dict[str, Any]],
                                     current_state: Dict[str, Any]) -> str:
        """Generate executive summary paragraph"""
        process_name = process_data.get('process_name', 'the process')
        num_objectives = len(objectives)

        summary = (
            f"This charter outlines a process improvement initiative for {process_name}. "
            f"The project aims to achieve {num_objectives} primary objectives focused on "
            f"improving process efficiency, quality, and stakeholder satisfaction. "
        )

        if current_state.get('critical_gaps', 0) > 0:
            summary += (
                f"Current state analysis has identified {current_state['critical_gaps']} "
                f"critical gaps requiring immediate attention. "
            )

        summary += (
            "Expected outcomes include measurable improvements in cycle time, error rates, "
            "and customer satisfaction, with clear success metrics defined for tracking progress."
        )

        return summary

    def validate_charter(self, charter: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate charter completeness

        Args:
            charter: Charter dictionary

        Returns:
            Tuple of (is_valid, list of issues)
        """
        self.log("Validating charter completeness")
        issues = []

        # Check required sections exist
        for section in self.required_sections:
            if section not in charter:
                issues.append(f"Missing required section: {section}")
            elif not charter[section]:
                issues.append(f"Empty section: {section}")

        # Validate specific sections
        if 'objectives' in charter and len(charter['objectives']) < 1:
            issues.append("Charter must have at least one objective")

        if 'success_metrics' in charter and len(charter['success_metrics']) < 2:
            issues.append("Charter must have at least two success metrics")

        if 'stakeholders' in charter and len(charter['stakeholders']) < 2:
            issues.append("Charter must identify at least two stakeholders")

        if 'timeline' in charter and len(charter['timeline']) < 4:
            issues.append("Timeline must have at least four milestones")

        is_valid = len(issues) == 0
        if is_valid:
            self.log("Charter validation passed")
        else:
            self.log(f"Charter validation failed: {len(issues)} issues", "WARNING")

        return is_valid, issues

    def format_markdown(self, charter: Dict[str, Any]) -> str:
        """
        Format charter as markdown

        Args:
            charter: Charter dictionary

        Returns:
            Markdown-formatted charter
        """
        self.log("Formatting charter as markdown")

        md = []
        md.append("# Process Improvement Charter")
        md.append("")

        # Process Information
        md.append("## Process Information")
        info = charter['process_info']
        md.append(f"- **Process Name**: {info['process_name']}")
        md.append(f"- **Process Owner**: {info['process_owner']}")
        md.append(f"- **Charter Date**: {info['charter_date']}")
        md.append(f"- **Charter ID**: {info['charter_id']}")
        md.append("")

        # Executive Summary
        md.append("## Executive Summary")
        md.append(charter['executive_summary'])
        md.append("")

        # Current State
        md.append("## Current State")
        cs = charter['current_state']
        md.append(f"- **Process Completeness**: {cs['completeness']}")
        md.append(f"- **Critical Gaps**: {cs['critical_gaps']}")
        md.append(f"- **Cycle Time**: {cs['cycle_time']}")
        md.append(f"- **Error Rate**: {cs['error_rate']}")
        md.append("")
        md.append(f"**Summary**: {cs['summary']}")
        md.append("")

        # Objectives
        md.append("## Objectives")
        for i, obj in enumerate(charter['objectives'], 1):
            measurable_flag = " [SMART]" if obj.get('measurable') else ""
            md.append(f"{i}. {obj['description']}{measurable_flag}")
        md.append("")

        # Scope
        md.append("## Scope")
        md.append("### In Scope")
        for item in charter['scope']['in_scope']:
            md.append(f"- {item}")
        md.append("")
        md.append("### Out of Scope")
        for item in charter['scope']['out_of_scope']:
            md.append(f"- {item}")
        md.append("")

        # Success Metrics
        md.append("## Success Metrics")
        md.append("| Metric | Current | Target | Measurement Method |")
        md.append("|--------|---------|--------|-------------------|")
        for metric in charter['success_metrics']:
            md.append(f"| {metric['name']} | {metric['current']} | "
                      f"{metric['target']} | {metric['measurement']} |")
        md.append("")

        # Stakeholders
        md.append("## Stakeholders")
        md.append("| Name | Role | RACI | Engagement Strategy |")
        md.append("|------|------|------|---------------------|")
        for sh in charter['stakeholders']:
            md.append(f"| {sh['name']} | {sh['role']} | {sh['raci']} | {sh['engagement']} |")
        md.append("")

        # Timeline
        md.append("## Timeline")
        for milestone in charter['timeline']:
            md.append(f"- **{milestone['name']}** (Week {milestone['week']}, {milestone['date']})")
            md.append(f"  - {milestone['deliverable']}")
        md.append("")

        # Resources Required
        md.append("## Resources Required")
        res = charter['resources']
        md.append(f"- **Business Analyst**: {res['business_analyst']} hours")
        md.append(f"- **Process Owner**: {res['process_owner']} hours")
        if res['development_team'] > 0:
            md.append(f"- **Development Team**: {res['development_team']} hours")
        md.append(f"- **Estimated Budget**: ${res['budget']:,}")
        md.append(f"- **Project Complexity**: {res['complexity'].title()}")
        md.append("")

        # Risks and Mitigation
        md.append("## Risks and Mitigation")
        for i, risk in enumerate(charter['risks'], 1):
            md.append(f"{i}. **Risk**: {risk['risk']}")
            md.append(f"   - **Probability**: {risk['probability']} | **Impact**: {risk['impact']}")
            md.append(f"   - **Mitigation**: {risk['mitigation']}")
        md.append("")

        # Approval Section
        md.append("## Approval")
        md.append("| Role | Name | Signature | Date |")
        md.append("|------|------|-----------|------|")
        md.append("| Process Owner | _________________ | _________________ | _______ |")
        md.append("| Executive Sponsor | _________________ | _________________ | _______ |")
        md.append("| Business Lead | _________________ | _________________ | _______ |")
        md.append("")

        md.append("---")
        md.append(f"*Generated by Charter Builder v1.0 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return '\n'.join(md)

    def format_html(self, charter: Dict[str, Any]) -> str:
        """
        Format charter as HTML

        Args:
            charter: Charter dictionary

        Returns:
            HTML-formatted charter
        """
        self.log("Formatting charter as HTML")

        # Convert markdown to basic HTML
        markdown = self.format_markdown(charter)

        html = ['<!DOCTYPE html>']
        html.append('<html>')
        html.append('<head>')
        html.append('  <meta charset="UTF-8">')
        html.append('  <title>Process Improvement Charter</title>')
        html.append('  <style>')
        html.append('    body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; }')
        html.append('    h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }')
        html.append('    h2 { color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; margin-top: 30px; }')
        html.append('    h3 { color: #7f8c8d; }')
        html.append('    table { border-collapse: collapse; width: 100%; margin: 15px 0; }')
        html.append('    th, td { border: 1px solid #bdc3c7; padding: 10px; text-align: left; }')
        html.append('    th { background-color: #ecf0f1; font-weight: bold; }')
        html.append('    ul, ol { margin: 10px 0; }')
        html.append('    li { margin: 5px 0; }')
        html.append('    .metadata { color: #95a5a6; font-size: 0.9em; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1; }')
        html.append('  </style>')
        html.append('</head>')
        html.append('<body>')

        # Convert markdown to HTML (simple conversion)
        lines = markdown.split('\n')
        in_table = False

        for line in lines:
            if not line.strip():
                continue

            # Headers
            if line.startswith('# '):
                html.append(f'  <h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html.append(f'  <h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html.append(f'  <h3>{line[4:]}</h3>')

            # Tables
            elif line.startswith('|'):
                if not in_table:
                    html.append('  <table>')
                    in_table = True

                if '---' in line:
                    continue  # Skip separator row

                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                if line.startswith('| Metric') or line.startswith('| Name') or line.startswith('| Role'):
                    html.append('    <tr>')
                    for cell in cells:
                        html.append(f'      <th>{cell}</th>')
                    html.append('    </tr>')
                else:
                    html.append('    <tr>')
                    for cell in cells:
                        html.append(f'      <td>{cell}</td>')
                    html.append('    </tr>')

            else:
                if in_table:
                    html.append('  </table>')
                    in_table = False

                # Lists
                if line.strip().startswith('- '):
                    html.append(f'  <li>{line.strip()[2:]}</li>')
                elif re.match(r'^\d+\.', line.strip()):
                    html.append(f'  <li>{re.sub(r"^\d+\.\s*", "", line.strip())}</li>')
                # Paragraphs
                elif line.strip().startswith('*'):
                    html.append(f'  <p class="metadata">{line.strip()}</p>')
                else:
                    html.append(f'  <p>{line.strip()}</p>')

        if in_table:
            html.append('  </table>')

        html.append('</body>')
        html.append('</html>')

        return '\n'.join(html)

    def format_json(self, charter: Dict[str, Any]) -> str:
        """
        Format charter as JSON

        Args:
            charter: Charter dictionary

        Returns:
            JSON-formatted charter
        """
        self.log("Formatting charter as JSON")
        return json.dumps(charter, indent=2, default=str)


def main():
    parser = argparse.ArgumentParser(
        description='Generate process improvement charters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic charter
  python charter_builder.py --process "Customer Onboarding" --objectives "Reduce cycle time by 50%"

  # With gap analysis
  python charter_builder.py --process process.json --gaps gaps.json --objectives objectives.txt

  # With stakeholder data
  python charter_builder.py --process "Billing" --objectives obj.txt --stakeholders stakeholders.json

  # HTML output
  python charter_builder.py --process process.json --output html > charter.html

  # JSON for integration
  python charter_builder.py --process process.json --output json > charter.json

Input Formats:
  - Process: String or JSON file with process data
  - Objectives: Text file (one per line) or JSON array
  - Gaps: JSON from gap_analyzer.py
  - Stakeholders: JSON from stakeholder_mapper.py
        """
    )

    parser.add_argument('--process', required=True,
                        help='Process name or path to process file (JSON)')
    parser.add_argument('--objectives', required=True,
                        help='Objectives text or path to objectives file')
    parser.add_argument('--gaps',
                        help='Path to gap analysis JSON file (from gap_analyzer.py)')
    parser.add_argument('--stakeholders',
                        help='Path to stakeholder mapping JSON (from stakeholder_mapper.py)')
    parser.add_argument('--template',
                        help='Path to custom charter template (markdown)')
    parser.add_argument('--strategy', default='efficiency',
                        choices=['efficiency', 'quality', 'capacity', 'experience'],
                        help='Improvement strategy type (default: efficiency)')
    parser.add_argument('--timeline', type=int, default=12, metavar='WEEKS',
                        help='Project timeline in weeks (default: 12)')
    parser.add_argument('--complexity', default='medium',
                        choices=['low', 'medium', 'high'],
                        help='Project complexity level (default: medium)')
    parser.add_argument('--output', default='markdown',
                        choices=['markdown', 'html', 'json'],
                        help='Output format (default: markdown)')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    try:
        # Initialize builder
        builder = CharterBuilder(template_path=args.template, verbose=args.verbose)

        # Parse inputs
        process_data = builder.parse_process_data(args.process)
        objectives = builder.parse_objectives(args.objectives)

        # Parse optional inputs
        gaps_data = None
        if args.gaps:
            gaps_data = builder.parse_input_file(args.gaps)

        stakeholder_data = None
        if args.stakeholders:
            stakeholder_data = builder.parse_input_file(args.stakeholders)

        # Build charter data
        charter_input = {
            'process': process_data,
            'objectives': objectives,
            'gaps': gaps_data,
            'stakeholders': stakeholder_data,
            'strategy': args.strategy,
            'timeline_weeks': args.timeline,
            'complexity': args.complexity
        }

        # Generate charter
        charter = builder.build_charter(charter_input)

        # Validate charter
        is_valid, issues = builder.validate_charter(charter)
        if not is_valid:
            print("Charter validation failed:", file=sys.stderr)
            for issue in issues:
                print(f"  - {issue}", file=sys.stderr)
            sys.exit(EXIT_VALIDATION_ERROR)

        # Format output
        if args.output == 'markdown':
            output = builder.format_markdown(charter)
        elif args.output == 'html':
            output = builder.format_html(charter)
        elif args.output == 'json':
            output = builder.format_json(charter)
        else:
            print(f"Unsupported output format: {args.output}", file=sys.stderr)
            sys.exit(EXIT_GENERATION_ERROR)

        # Print result
        print(output)

        if args.verbose:
            print(f"\nCharter generated successfully: {charter['process_info']['charter_id']}",
                  file=sys.stderr)
            print(f"Objectives: {len(charter['objectives'])}", file=sys.stderr)
            print(f"Metrics: {len(charter['success_metrics'])}", file=sys.stderr)
            print(f"Stakeholders: {len(charter['stakeholders'])}", file=sys.stderr)
            print(f"Timeline: {len(charter['timeline'])} milestones", file=sys.stderr)

        sys.exit(EXIT_SUCCESS)

    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(EXIT_VALIDATION_ERROR)

    except (IOError, OSError) as e:
        print(f"File error: {e}", file=sys.stderr)
        sys.exit(EXIT_PARSE_ERROR)

    except Exception as e:
        print(f"Generation error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(EXIT_GENERATION_ERROR)


if __name__ == '__main__':
    main()
