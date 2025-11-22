#!/usr/bin/env python3
"""
Gap Analyzer - Identify missing elements in process documentation

Analyzes process documentation to identify gaps, missing elements, and improvement
opportunities using deterministic algorithms.

Usage:
    python gap_analyzer.py --input process.json
    python gap_analyzer.py --input process.json --severity-threshold high
    python gap_analyzer.py --input process.json --output json
    python gap_analyzer.py --stdin --format human

Categories:
    - Missing owners (RACI gaps)
    - Missing decision criteria
    - Missing inputs/outputs
    - Exception handling gaps
    - Missing success/failure paths
    - Bottlenecks and inefficiencies

Author: Claude Skills - Business Analyst Toolkit
Version: 1.0.0
License: MIT
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 1
EXIT_PARSE_ERROR = 2
EXIT_ANALYSIS_ERROR = 3

# Schema version
SCHEMA_VERSION = "1.0"

# Severity levels and thresholds
SEVERITY_LEVELS = {
    'critical': 4,
    'high': 3,
    'medium': 2,
    'low': 1
}


class GapAnalyzer:
    """Analyzes process documentation for missing elements and gaps."""

    def __init__(self, severity_threshold: str = 'low', verbose: bool = False):
        """
        Initialize gap analyzer.

        Args:
            severity_threshold: Minimum severity to report (critical|high|medium|low)
            verbose: Enable verbose logging
        """
        self.severity_threshold = severity_threshold.lower()
        self.verbose = verbose
        self.gaps = []

        if self.severity_threshold not in SEVERITY_LEVELS:
            raise ValueError(f"Invalid severity threshold: {severity_threshold}")

    def analyze(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main analysis logic.

        Args:
            process_data: Process JSON data

        Returns:
            Analysis result with identified gaps
        """
        self._log("Starting gap analysis")

        # Validate schema
        self._validate_schema(process_data)

        # Reset gaps list
        self.gaps = []

        # Run all gap detection methods
        self._identify_missing_owners(process_data)
        self._identify_decision_criteria_gaps(process_data)
        self._identify_input_output_gaps(process_data)
        self._identify_exception_handling_gaps(process_data)
        self._identify_bottlenecks(process_data)
        self._identify_documentation_gaps(process_data)
        self._identify_validation_gaps(process_data)

        # Filter by severity threshold
        filtered_gaps = self._filter_by_severity(self.gaps)

        # Calculate completeness score
        completeness_score = self._calculate_completeness(process_data, self.gaps)

        # Count gaps by severity
        gaps_by_severity = self._count_by_severity(filtered_gaps)

        # Generate recommendations
        recommendations = self._generate_recommendations(filtered_gaps, process_data)

        # Build result
        result = {
            'schema_version': SCHEMA_VERSION,
            'analyzed_at': datetime.utcnow().isoformat() + 'Z',
            'process_id': process_data.get('process_id', 'unknown'),
            'process_name': process_data.get('process_name', 'Unknown Process'),
            'completeness_score': round(completeness_score, 2),
            'total_gaps': len(filtered_gaps),
            'gaps_by_severity': gaps_by_severity,
            'gaps': filtered_gaps,
            'recommendations': recommendations,
            'analysis_summary': self._generate_summary(
                completeness_score,
                filtered_gaps,
                process_data
            )
        }

        self._log(f"Analysis complete. Found {len(filtered_gaps)} gaps")

        return result

    def _validate_schema(self, data: Dict[str, Any]) -> None:
        """
        Validate process JSON schema.

        Args:
            data: Process data to validate

        Raises:
            ValueError: If schema invalid
        """
        required_fields = ['process_name', 'steps']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data['steps'], list):
            raise ValueError("Field 'steps' must be an array")

        if len(data['steps']) == 0:
            raise ValueError("Process must have at least one step")

    def _identify_missing_owners(self, process_data: Dict[str, Any]) -> None:
        """Identify steps without clear role/owner assignments."""
        steps = process_data.get('steps', [])

        for i, step in enumerate(steps):
            step_id = step.get('id', f'step_{i+1:03d}')
            step_name = step.get('name', f'Step {i+1}')

            # Check for missing role
            if not step.get('role'):
                self.gaps.append({
                    'id': f'GAP-{len(self.gaps)+1:03d}',
                    'severity': 'critical',
                    'category': 'missing_owner',
                    'element': f"Step {i+1}: {step_name}",
                    'step_id': step_id,
                    'description': 'No role/owner assigned to step',
                    'impact': 'Unclear accountability, potential delays in execution',
                    'recommendation': 'Assign RACI responsible role (R) for this step'
                })

            # Check for ambiguous roles
            elif isinstance(step.get('role'), list) and len(step['role']) > 1:
                self.gaps.append({
                    'id': f'GAP-{len(self.gaps)+1:03d}',
                    'severity': 'high',
                    'category': 'ambiguous_owner',
                    'element': f"Step {i+1}: {step_name}",
                    'step_id': step_id,
                    'description': f"Multiple roles assigned: {', '.join(step['role'])}",
                    'impact': 'Unclear primary responsibility, potential confusion',
                    'recommendation': 'Designate single responsible (R) role, others as consulted (C) or informed (I)'
                })

    def _identify_decision_criteria_gaps(self, process_data: Dict[str, Any]) -> None:
        """Identify decision points without clear criteria."""
        steps = process_data.get('steps', [])

        for i, step in enumerate(steps):
            step_id = step.get('id', f'step_{i+1:03d}')
            step_name = step.get('name', f'Step {i+1}')
            decisions = step.get('decisions', [])

            # Check if step has decision points
            if decisions:
                for j, decision in enumerate(decisions):
                    # Missing criteria
                    if not decision.get('criteria'):
                        self.gaps.append({
                            'id': f'GAP-{len(self.gaps)+1:03d}',
                            'severity': 'high',
                            'category': 'missing_decision_criteria',
                            'element': f"Step {i+1}: {step_name} - Decision {j+1}",
                            'step_id': step_id,
                            'description': f"Decision point '{decision.get('question', 'Unknown')}' has no defined criteria",
                            'impact': 'Inconsistent decision-making, subjective judgments',
                            'recommendation': 'Define specific, measurable criteria for this decision'
                        })

                    # Missing options
                    if not decision.get('options') or len(decision.get('options', [])) < 2:
                        self.gaps.append({
                            'id': f'GAP-{len(self.gaps)+1:03d}',
                            'severity': 'medium',
                            'category': 'incomplete_decision',
                            'element': f"Step {i+1}: {step_name} - Decision {j+1}",
                            'step_id': step_id,
                            'description': 'Decision point has fewer than 2 options',
                            'impact': 'Unclear process flow, missing alternative paths',
                            'recommendation': 'Document all possible decision outcomes'
                        })

            # Check for implicit decisions (keywords in step name)
            decision_keywords = ['approve', 'review', 'validate', 'check', 'verify', 'assess']
            if any(keyword in step_name.lower() for keyword in decision_keywords):
                if not decisions:
                    self.gaps.append({
                        'id': f'GAP-{len(self.gaps)+1:03d}',
                        'severity': 'medium',
                        'category': 'implicit_decision',
                        'element': f"Step {i+1}: {step_name}",
                        'step_id': step_id,
                        'description': 'Step implies decision but has no decision points documented',
                        'impact': 'Hidden decision logic, lack of transparency',
                        'recommendation': 'Add explicit decision point with criteria and options'
                    })

    def _identify_input_output_gaps(self, process_data: Dict[str, Any]) -> None:
        """Identify missing inputs, outputs, or broken dependencies."""
        steps = process_data.get('steps', [])

        # Track all outputs
        available_outputs = set()

        for i, step in enumerate(steps):
            step_id = step.get('id', f'step_{i+1:03d}')
            step_name = step.get('name', f'Step {i+1}')
            inputs = step.get('inputs', [])
            outputs = step.get('outputs', [])

            # Check for missing inputs
            if not inputs or len(inputs) == 0:
                self.gaps.append({
                    'id': f'GAP-{len(self.gaps)+1:03d}',
                    'severity': 'medium',
                    'category': 'missing_inputs',
                    'element': f"Step {i+1}: {step_name}",
                    'step_id': step_id,
                    'description': 'No inputs defined for this step',
                    'impact': 'Unclear what information/materials are needed',
                    'recommendation': 'Document required inputs (data, documents, approvals)'
                })

            # Check for missing outputs
            if not outputs or len(outputs) == 0:
                self.gaps.append({
                    'id': f'GAP-{len(self.gaps)+1:03d}',
                    'severity': 'medium',
                    'category': 'missing_outputs',
                    'element': f"Step {i+1}: {step_name}",
                    'step_id': step_id,
                    'description': 'No outputs defined for this step',
                    'impact': 'Unclear what this step produces or delivers',
                    'recommendation': 'Document outputs (deliverables, decisions, data)'
                })

            # Add outputs to available set for dependency checking
            available_outputs.update(outputs)

        # Check for orphaned inputs (inputs with no source)
        for i, step in enumerate(steps):
            step_id = step.get('id', f'step_{i+1:03d}')
            step_name = step.get('name', f'Step {i+1}')
            inputs = step.get('inputs', [])

            for input_item in inputs:
                # Check if this input is produced by any previous step
                if input_item not in available_outputs and i > 0:
                    self.gaps.append({
                        'id': f'GAP-{len(self.gaps)+1:03d}',
                        'severity': 'low',
                        'category': 'orphaned_input',
                        'element': f"Step {i+1}: {step_name}",
                        'step_id': step_id,
                        'description': f"Input '{input_item}' has no clear source from previous steps",
                        'impact': 'Unclear where this input comes from',
                        'recommendation': 'Identify source step that produces this input'
                    })

    def _identify_exception_handling_gaps(self, process_data: Dict[str, Any]) -> None:
        """Identify missing exception handling and error paths."""
        steps = process_data.get('steps', [])

        # Check for overall error handling
        has_error_handling = False

        for i, step in enumerate(steps):
            step_id = step.get('id', f'step_{i+1:03d}')
            step_name = step.get('name', f'Step {i+1}')

            # Check for error handling keywords
            error_keywords = ['error', 'exception', 'failure', 'reject', 'escalate']
            if any(keyword in step_name.lower() for keyword in error_keywords):
                has_error_handling = True

            # Check decisions for failure paths
            decisions = step.get('decisions', [])
            for decision in decisions:
                options = decision.get('options', [])
                if any('reject' in opt.lower() or 'fail' in opt.lower() or 'error' in opt.lower()
                       for opt in options):
                    has_error_handling = True

            # Check for high-risk steps without error handling
            risk_keywords = ['payment', 'transfer', 'delete', 'approve', 'authorize', 'execute']
            if any(keyword in step_name.lower() for keyword in risk_keywords):
                if not decisions:
                    self.gaps.append({
                        'id': f'GAP-{len(self.gaps)+1:03d}',
                        'severity': 'high',
                        'category': 'missing_error_handling',
                        'element': f"Step {i+1}: {step_name}",
                        'step_id': step_id,
                        'description': 'High-risk step has no error handling or validation',
                        'impact': 'Process failure risk, no recovery path',
                        'recommendation': 'Add decision point for success/failure with appropriate handling'
                    })

        # If process has no error handling at all
        if not has_error_handling and len(steps) > 3:
            self.gaps.append({
                'id': f'GAP-{len(self.gaps)+1:03d}',
                'severity': 'critical',
                'category': 'no_error_handling',
                'element': 'Overall Process',
                'step_id': None,
                'description': 'Process has no documented error handling or exception paths',
                'impact': 'No recovery mechanism for failures, unclear escalation',
                'recommendation': 'Add error handling steps and exception paths throughout process'
            })

    def _identify_bottlenecks(self, process_data: Dict[str, Any]) -> None:
        """Identify potential bottlenecks and efficiency issues."""
        steps = process_data.get('steps', [])

        # Calculate total duration if available
        total_duration = 0
        max_duration = 0
        max_duration_step = None

        for i, step in enumerate(steps):
            step_id = step.get('id', f'step_{i+1:03d}')
            step_name = step.get('name', f'Step {i+1}')
            duration = step.get('duration_minutes', 0)
            effort = step.get('effort_hours', 0)

            # Track maximum duration step
            if duration > max_duration:
                max_duration = duration
                max_duration_step = (i, step_name, step_id)

            total_duration += duration

            # Check for long duration steps
            if duration > 480:  # More than 8 hours
                self.gaps.append({
                    'id': f'GAP-{len(self.gaps)+1:03d}',
                    'severity': 'medium',
                    'category': 'bottleneck_duration',
                    'element': f"Step {i+1}: {step_name}",
                    'step_id': step_id,
                    'description': f"Step has long duration: {duration} minutes ({duration/60:.1f} hours)",
                    'impact': 'Process delay, potential bottleneck',
                    'recommendation': 'Review step for automation or parallelization opportunities'
                })

            # Check for high effort steps
            if effort > 4:  # More than 4 hours of work
                self.gaps.append({
                    'id': f'GAP-{len(self.gaps)+1:03d}',
                    'severity': 'low',
                    'category': 'high_effort',
                    'element': f"Step {i+1}: {step_name}",
                    'step_id': step_id,
                    'description': f"Step requires significant effort: {effort} hours",
                    'impact': 'Resource-intensive, potential for errors',
                    'recommendation': 'Consider breaking into smaller steps or automation'
                })

            # Check for manual steps that could be automated
            manual_keywords = ['manually', 'copy', 'paste', 'type', 'enter', 'fill']
            if any(keyword in step_name.lower() or keyword in step.get('description', '').lower()
                   for keyword in manual_keywords):
                self.gaps.append({
                    'id': f'GAP-{len(self.gaps)+1:03d}',
                    'severity': 'low',
                    'category': 'automation_opportunity',
                    'element': f"Step {i+1}: {step_name}",
                    'step_id': step_id,
                    'description': 'Manual step may be automatable',
                    'impact': 'Time-consuming, error-prone, inefficient',
                    'recommendation': 'Evaluate automation feasibility (RPA, API integration, workflow tool)'
                })

        # Check if the longest step dominates the process
        if max_duration_step and total_duration > 0:
            if max_duration / total_duration > 0.5:  # More than 50% of total time
                i, step_name, step_id = max_duration_step
                self.gaps.append({
                    'id': f'GAP-{len(self.gaps)+1:03d}',
                    'severity': 'high',
                    'category': 'dominant_bottleneck',
                    'element': f"Step {i+1}: {step_name}",
                    'step_id': step_id,
                    'description': f"Step accounts for {(max_duration/total_duration*100):.0f}% of total process time",
                    'impact': 'Major bottleneck limiting overall process speed',
                    'recommendation': 'Prioritize optimization or parallelization of this step'
                })

    def _identify_documentation_gaps(self, process_data: Dict[str, Any]) -> None:
        """Identify incomplete documentation."""

        # Check for missing process owner
        if not process_data.get('process_owner'):
            self.gaps.append({
                'id': f'GAP-{len(self.gaps)+1:03d}',
                'severity': 'high',
                'category': 'missing_process_owner',
                'element': 'Process Metadata',
                'step_id': None,
                'description': 'No process owner assigned',
                'impact': 'Unclear who is accountable for process performance',
                'recommendation': 'Assign process owner with clear accountability'
            })

        # Check for missing process description
        if not process_data.get('process_description'):
            self.gaps.append({
                'id': f'GAP-{len(self.gaps)+1:03d}',
                'severity': 'medium',
                'category': 'missing_description',
                'element': 'Process Metadata',
                'step_id': None,
                'description': 'No process description provided',
                'impact': 'Unclear purpose and scope of process',
                'recommendation': 'Add clear description of process purpose and objectives'
            })

        # Check step-level documentation
        steps = process_data.get('steps', [])
        for i, step in enumerate(steps):
            step_id = step.get('id', f'step_{i+1:03d}')
            step_name = step.get('name', f'Step {i+1}')

            # Check for missing description
            if not step.get('description'):
                self.gaps.append({
                    'id': f'GAP-{len(self.gaps)+1:03d}',
                    'severity': 'low',
                    'category': 'missing_step_description',
                    'element': f"Step {i+1}: {step_name}",
                    'step_id': step_id,
                    'description': 'No detailed description for step',
                    'impact': 'Unclear what needs to be done',
                    'recommendation': 'Add clear description of step activities and expected outcomes'
                })

    def _identify_validation_gaps(self, process_data: Dict[str, Any]) -> None:
        """Identify missing quality checks and validation points."""
        steps = process_data.get('steps', [])

        has_validation = False

        for i, step in enumerate(steps):
            step_id = step.get('id', f'step_{i+1:03d}')
            step_name = step.get('name', f'Step {i+1}')

            # Check for validation keywords
            validation_keywords = ['review', 'verify', 'validate', 'check', 'inspect', 'audit']
            if any(keyword in step_name.lower() for keyword in validation_keywords):
                has_validation = True

        # If process has no validation steps
        if not has_validation and len(steps) > 3:
            self.gaps.append({
                'id': f'GAP-{len(self.gaps)+1:03d}',
                'severity': 'high',
                'category': 'no_validation',
                'element': 'Overall Process',
                'step_id': None,
                'description': 'Process has no quality checks or validation steps',
                'impact': 'No quality assurance, potential for errors',
                'recommendation': 'Add validation checkpoints at critical stages'
            })

    def _calculate_completeness(self, process_data: Dict[str, Any], gaps: List[Dict]) -> float:
        """
        Calculate process completeness score.

        Args:
            process_data: Process data
            gaps: List of identified gaps

        Returns:
            Completeness score (0.0-1.0)
        """
        steps = process_data.get('steps', [])
        total_elements = 0
        complete_elements = 0

        # Count completeness of required elements
        for step in steps:
            # Role assignment (weight: 2)
            total_elements += 2
            if step.get('role'):
                complete_elements += 2

            # Inputs (weight: 1)
            total_elements += 1
            if step.get('inputs') and len(step['inputs']) > 0:
                complete_elements += 1

            # Outputs (weight: 1)
            total_elements += 1
            if step.get('outputs') and len(step['outputs']) > 0:
                complete_elements += 1

            # Description (weight: 1)
            total_elements += 1
            if step.get('description'):
                complete_elements += 1

            # Duration (weight: 0.5)
            total_elements += 0.5
            if step.get('duration_minutes'):
                complete_elements += 0.5

            # Decisions with criteria (weight: 1)
            if step.get('decisions'):
                for decision in step['decisions']:
                    total_elements += 1
                    if decision.get('criteria') and decision.get('options'):
                        complete_elements += 1

        # Process-level elements
        total_elements += 3
        if process_data.get('process_owner'):
            complete_elements += 1
        if process_data.get('process_description'):
            complete_elements += 1
        if process_data.get('roles'):
            complete_elements += 1

        # Calculate score
        if total_elements == 0:
            return 0.0

        base_score = complete_elements / total_elements

        # Penalty for critical gaps
        critical_gaps = sum(1 for gap in gaps if gap['severity'] == 'critical')
        penalty = min(0.3, critical_gaps * 0.1)

        return max(0.0, base_score - penalty)

    def _filter_by_severity(self, gaps: List[Dict]) -> List[Dict]:
        """
        Filter gaps by severity threshold.

        Args:
            gaps: All identified gaps

        Returns:
            Filtered gaps meeting threshold
        """
        threshold_value = SEVERITY_LEVELS[self.severity_threshold]
        return [
            gap for gap in gaps
            if SEVERITY_LEVELS[gap['severity']] >= threshold_value
        ]

    def _count_by_severity(self, gaps: List[Dict]) -> Dict[str, int]:
        """Count gaps by severity level."""
        counts = {level: 0 for level in SEVERITY_LEVELS.keys()}
        for gap in gaps:
            counts[gap['severity']] += 1
        return counts

    def _generate_recommendations(self, gaps: List[Dict], process_data: Dict) -> List[str]:
        """
        Generate high-level recommendations.

        Args:
            gaps: Identified gaps
            process_data: Process data

        Returns:
            List of prioritized recommendations
        """
        recommendations = []

        # Critical gaps first
        critical_gaps = [g for g in gaps if g['severity'] == 'critical']
        if critical_gaps:
            recommendations.append(
                f"Address {len(critical_gaps)} critical gap(s) immediately - "
                f"these represent significant process risks"
            )

        # Category-based recommendations
        categories = {}
        for gap in gaps:
            category = gap['category']
            categories[category] = categories.get(category, 0) + 1

        # Prioritize by frequency
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

        for category, count in sorted_categories[:3]:
            if category == 'missing_owner':
                recommendations.append(
                    f"Create RACI matrix to assign clear roles and responsibilities ({count} gaps)"
                )
            elif category == 'missing_decision_criteria':
                recommendations.append(
                    f"Document decision criteria for all approval/review steps ({count} gaps)"
                )
            elif category == 'missing_inputs' or category == 'missing_outputs':
                recommendations.append(
                    f"Map inputs and outputs for all process steps ({count} gaps)"
                )
            elif category == 'no_error_handling':
                recommendations.append(
                    "Implement error handling and exception paths throughout process"
                )
            elif category == 'bottleneck_duration':
                recommendations.append(
                    f"Review process timing and identify optimization opportunities ({count} gaps)"
                )
            elif category == 'automation_opportunity':
                recommendations.append(
                    f"Evaluate automation feasibility for manual steps ({count} gaps)"
                )

        # Completeness-based recommendation
        steps = process_data.get('steps', [])
        if len(steps) > 5 and not process_data.get('roles'):
            recommendations.append("Define process roles and stakeholders for better governance")

        return recommendations

    def _generate_summary(self, completeness: float, gaps: List[Dict],
                         process_data: Dict) -> Dict[str, Any]:
        """Generate analysis summary."""
        steps = process_data.get('steps', [])

        # Determine health status
        if completeness >= 0.85:
            health = 'green'
            status = 'Excellent'
        elif completeness >= 0.70:
            health = 'amber'
            status = 'Good'
        elif completeness >= 0.50:
            health = 'amber'
            status = 'Needs Improvement'
        else:
            health = 'red'
            status = 'Poor'

        # Count critical issues
        critical_count = sum(1 for gap in gaps if gap['severity'] == 'critical')
        high_count = sum(1 for gap in gaps if gap['severity'] == 'high')

        return {
            'health_status': health,
            'status_label': status,
            'total_steps': len(steps),
            'critical_issues': critical_count,
            'high_priority_issues': high_count,
            'key_findings': self._extract_key_findings(gaps)[:5]
        }

    def _extract_key_findings(self, gaps: List[Dict]) -> List[str]:
        """Extract key findings from gaps."""
        findings = []

        # Critical and high severity gaps
        priority_gaps = [g for g in gaps if g['severity'] in ['critical', 'high']]

        for gap in priority_gaps[:5]:
            findings.append(f"{gap['category'].replace('_', ' ').title()}: {gap['description']}")

        return findings

    def _log(self, message: str, level: str = 'INFO') -> None:
        """Log message if verbose enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] {level}: {message}", file=sys.stderr)


def validate_filepath(filepath: str, must_exist: bool = True) -> str:
    """
    Validate file path for security.

    Args:
        filepath: User-provided file path
        must_exist: Require file to exist

    Returns:
        Validated absolute path

    Raises:
        ValueError: If path invalid
    """
    if not filepath or not filepath.strip():
        raise ValueError("File path cannot be empty")

    if '..' in filepath:
        raise ValueError("Path traversal not allowed")

    path = Path(filepath).resolve()

    if must_exist and not path.exists():
        raise ValueError(f"File not found: {filepath}")

    if must_exist and not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    return str(path)


def read_json_file(filepath: str) -> Dict:
    """
    Read and parse JSON file safely.

    Args:
        filepath: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        ValueError: If file invalid or parse error
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    except Exception as e:
        raise ValueError(f"Failed to read file: {e}")


def format_human_readable(data: Dict) -> str:
    """
    Format analysis results for human-readable output.

    Args:
        data: Analysis result data

    Returns:
        Formatted string
    """
    output = []

    # Header
    output.append("=" * 80)
    output.append(f"GAP ANALYSIS REPORT: {data.get('process_name', 'Unknown Process')}")
    output.append("=" * 80)
    output.append("")

    # Summary
    summary = data.get('analysis_summary', {})
    output.append("SUMMARY")
    output.append("-" * 80)
    output.append(f"Completeness Score:  {data.get('completeness_score', 0):.1%}")
    output.append(f"Health Status:       {summary.get('status_label', 'Unknown')} "
                 f"({summary.get('health_status', 'unknown').upper()})")
    output.append(f"Total Steps:         {summary.get('total_steps', 0)}")
    output.append(f"Total Gaps Found:    {data.get('total_gaps', 0)}")
    output.append("")

    # Gaps by severity
    gaps_by_severity = data.get('gaps_by_severity', {})
    output.append("GAPS BY SEVERITY")
    output.append("-" * 80)
    output.append(f"  Critical:  {gaps_by_severity.get('critical', 0)}")
    output.append(f"  High:      {gaps_by_severity.get('high', 0)}")
    output.append(f"  Medium:    {gaps_by_severity.get('medium', 0)}")
    output.append(f"  Low:       {gaps_by_severity.get('low', 0)}")
    output.append("")

    # Key findings
    key_findings = summary.get('key_findings', [])
    if key_findings:
        output.append("KEY FINDINGS")
        output.append("-" * 80)
        for i, finding in enumerate(key_findings, 1):
            output.append(f"{i}. {finding}")
        output.append("")

    # Detailed gaps
    gaps = data.get('gaps', [])
    if gaps:
        output.append("DETAILED GAPS")
        output.append("-" * 80)

        for gap in gaps:
            output.append(f"\n[{gap['id']}] {gap['element']}")
            output.append(f"  Severity:    {gap['severity'].upper()}")
            output.append(f"  Category:    {gap['category'].replace('_', ' ').title()}")
            output.append(f"  Description: {gap['description']}")
            output.append(f"  Impact:      {gap['impact']}")
            output.append(f"  Recommendation: {gap['recommendation']}")
        output.append("")

    # Recommendations
    recommendations = data.get('recommendations', [])
    if recommendations:
        output.append("\nRECOMMENDATIONS")
        output.append("-" * 80)
        for i, rec in enumerate(recommendations, 1):
            output.append(f"{i}. {rec}")
        output.append("")

    # Footer
    output.append("=" * 80)
    output.append(f"Analysis completed: {data.get('analyzed_at', 'Unknown')}")
    output.append("=" * 80)

    return '\n'.join(output)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Gap Analyzer - Identify missing elements in process documentation',
        epilog='Examples:\n'
               '  python gap_analyzer.py --input process.json\n'
               '  python gap_analyzer.py --input process.json --severity-threshold high\n'
               '  python gap_analyzer.py --input process.json --output gaps.json\n'
               '  python gap_analyzer.py --stdin --format human\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Input arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', type=str,
                            help='Input process JSON file path')
    input_group.add_argument('--stdin', action='store_true',
                            help='Read process JSON from stdin')

    # Output arguments
    parser.add_argument('--output', type=str,
                       help='Output file path (default: stdout)')
    parser.add_argument('--format', type=str, default='json',
                       choices=['json', 'human'],
                       help='Output format (default: json)')

    # Analysis options
    parser.add_argument('--severity-threshold', type=str, default='low',
                       choices=['critical', 'high', 'medium', 'low'],
                       help='Minimum severity level to report (default: low)')

    # Flags
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing output file')

    args = parser.parse_args()

    try:
        # Read input
        if args.stdin:
            input_data = json.load(sys.stdin)
        else:
            input_path = validate_filepath(args.input, must_exist=True)
            input_data = read_json_file(input_path)

        # Analyze
        analyzer = GapAnalyzer(
            severity_threshold=args.severity_threshold,
            verbose=args.verbose
        )
        result = analyzer.analyze(input_data)

        # Format output
        if args.format == 'json':
            output_text = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output_text = format_human_readable(result)

        # Write output
        if args.output:
            output_path = validate_filepath(args.output, must_exist=False)
            path = Path(output_path)

            if path.exists() and not args.overwrite:
                print(f"Error: File exists (use --overwrite): {args.output}",
                     file=sys.stderr)
                return EXIT_VALIDATION_ERROR

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_text)

            if args.verbose:
                print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(output_text)

        return EXIT_SUCCESS

    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return EXIT_VALIDATION_ERROR

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return EXIT_PARSE_ERROR

    except Exception as e:
        print(f"Analysis error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return EXIT_ANALYSIS_ERROR


if __name__ == '__main__':
    sys.exit(main())
