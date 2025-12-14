#!/usr/bin/env python3
"""
Improvement Planner - Generate process improvement plans from gap analysis

Creates detailed, phased improvement plans with prioritized actions, timelines,
resource allocation, and expected impact based on gap analysis results.

Usage:
    python improvement_planner.py --gaps gaps.json [--timeline 12] [--output json]
    python improvement_planner.py --gaps gaps.json --process process.json --resources resources.json
    python improvement_planner.py --gaps gaps.json --output gantt > plan.md
    python improvement_planner.py --gaps gaps.json --output markdown --verbose

Author: Claude Skills - Business Analyst Toolkit
Version: 1.0.0
License: MIT
"""

import argparse
import json
import logging
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 1
EXIT_PARSE_ERROR = 2
EXIT_PLANNING_ERROR = 3


class ImprovementPlanner:
    """Generates comprehensive process improvement plans from gap analysis"""

    def __init__(self, timeline_weeks: int = 12, verbose: bool = False):
        """
        Initialize the improvement planner

        Args:
            timeline_weeks: Target timeline in weeks for improvements
            verbose: Enable verbose output
        """
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("ImprovementPlanner initialized")
        self.timeline_weeks = timeline_weeks
        self.verbose = verbose

        # Effort estimation map (hours) by gap type
        self.effort_estimates = {
            'missing_owner': 8,
            'undefined_role': 8,
            'missing_criteria': 16,
            'missing_input': 12,
            'missing_output': 12,
            'missing_exception': 24,
            'exception_handling': 24,
            'missing_decision': 20,
            'unclear_dependency': 16,
            'missing_info': 12,
            'process_inefficiency': 40,
            'compliance_risk': 32,
            'quality_issue': 24,
            'automation_opportunity': 60,
            'default': 16
        }

        # Severity to phase mapping
        self.severity_phases = {
            'critical': 1,
            'high': 2,
            'medium': 3,
            'low': 4
        }

        # Phase names and durations (as percentage of total timeline)
        self.phase_config = {
            1: {'name': 'Critical Fixes', 'duration_pct': 0.15},
            2: {'name': 'High Priority Improvements', 'duration_pct': 0.35},
            3: {'name': 'Medium Priority Enhancements', 'duration_pct': 0.35},
            4: {'name': 'Continuous Improvements', 'duration_pct': 0.15}
        }

        # Impact estimation by gap type (% improvement)
        self.impact_estimates = {
            'missing_owner': {'cycle_time': 10, 'error_rate': 5, 'cost': 5},
            'undefined_role': {'cycle_time': 10, 'error_rate': 5, 'cost': 5},
            'missing_criteria': {'cycle_time': 15, 'error_rate': 20, 'cost': 10},
            'missing_exception': {'cycle_time': 5, 'error_rate': 30, 'cost': 15},
            'exception_handling': {'cycle_time': 5, 'error_rate': 30, 'cost': 15},
            'missing_decision': {'cycle_time': 20, 'error_rate': 15, 'cost': 10},
            'process_inefficiency': {'cycle_time': 30, 'error_rate': 10, 'cost': 20},
            'automation_opportunity': {'cycle_time': 50, 'error_rate': 25, 'cost': 30},
            'compliance_risk': {'cycle_time': 0, 'error_rate': 10, 'cost': 5},
            'quality_issue': {'cycle_time': 10, 'error_rate': 25, 'cost': 15},
            'default': {'cycle_time': 10, 'error_rate': 10, 'cost': 5}
        }

    def create_plan(self, gaps_data: Dict[str, Any], process_data: Optional[Dict] = None,
                   resources: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate comprehensive improvement plan from gap analysis

        Args:
            gaps_data: Gap analysis results (from gap_analyzer.py)
            process_data: Optional process data for context
            resources: Optional resource constraints

        Returns:
            Comprehensive improvement plan dictionary
        """
        logger.debug("create_plan method called")
        if not gaps_data:
            logger.warning("Empty gaps_data provided")
        if self.verbose:
            print(f"📋 Creating improvement plan for: {gaps_data.get('process_name', 'Unknown Process')}")

        # Extract gaps from input
        gaps = self._extract_gaps(gaps_data)

        if not gaps:
            if self.verbose:
                print("✅ No gaps found - no improvements needed")
            return self._create_empty_plan(gaps_data.get('process_name', 'Unknown Process'))

        # Organize gaps into phases by severity
        phased_gaps = self._prioritize_improvements(gaps)

        # Generate improvement actions for each gap
        improvements = self._generate_improvements(phased_gaps)

        # Calculate total effort and timeline
        total_effort = sum(imp['effort_hours'] for phase in improvements.values() for imp in phase)

        # Calculate expected impact
        expected_impact = self._calculate_impact(gaps)

        # Generate milestones
        milestones = self._generate_milestones(improvements)

        # Allocate resources
        resource_allocation = self._allocate_resources(improvements, resources)

        # Identify risks
        risks = self._identify_risks(improvements, total_effort)

        # Build the plan
        plan = {
            'process_name': gaps_data.get('process_name', 'Unknown Process'),
            'plan_metadata': {
                'created_at': datetime.utcnow().isoformat() + 'Z',
                'version': '1.0',
                'schema_version': '1.0',
                'timeline_weeks': self.timeline_weeks
            },
            'improvement_plan': {
                'total_improvements': len(gaps),
                'total_effort_hours': total_effort,
                'expected_timeline_weeks': self.timeline_weeks,
                'expected_impact': expected_impact
            },
            'phases': self._format_phases(improvements),
            'milestones': milestones,
            'resource_allocation': resource_allocation,
            'risks': risks,
            'recommendations': self._generate_recommendations(gaps, total_effort)
        }

        if self.verbose:
            self._print_summary(plan)

        return plan

    def _extract_gaps(self, gaps_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract gaps list from various input formats"""
        logger.debug("_extract_gaps called")
        if not gaps_data:
            logger.warning("No gaps_data provided to _extract_gaps")
        # Handle different input structures
        if 'gaps' in gaps_data:
            return gaps_data['gaps']
        elif 'gap_analysis' in gaps_data and 'gaps' in gaps_data['gap_analysis']:
            return gaps_data['gap_analysis']['gaps']
        elif isinstance(gaps_data, list):
            return gaps_data
        else:
            # Try to find gaps in any nested structure
            for key, value in gaps_data.items():
                if isinstance(value, list) and value and 'severity' in value[0]:
                    return value

        return []

    def _create_empty_plan(self, process_name: str) -> Dict[str, Any]:
        """Create empty plan when no gaps found"""
        return {
            'process_name': process_name,
            'plan_metadata': {
                'created_at': datetime.utcnow().isoformat() + 'Z',
                'version': '1.0'
            },
            'improvement_plan': {
                'total_improvements': 0,
                'total_effort_hours': 0,
                'expected_timeline_weeks': 0,
                'expected_impact': {
                    'cycle_time_reduction': '0%',
                    'error_rate_reduction': '0%',
                    'cost_savings': '$0/year'
                }
            },
            'phases': [],
            'milestones': [],
            'resource_allocation': {},
            'risks': [],
            'recommendations': ['Process is well-defined with no significant gaps identified.']
        }

    def _prioritize_improvements(self, gaps: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
        """
        Organize gaps into phases based on severity

        Returns:
            Dictionary mapping phase number to list of gaps
        """
        phased = {1: [], 2: [], 3: [], 4: []}

        for gap in gaps:
            severity = gap.get('severity', 'medium')
            phase = self.severity_phases.get(severity, 3)
            phased[phase].append(gap)

        return phased

    def _generate_improvements(self, phased_gaps: Dict[int, List[Dict[str, Any]]]) -> Dict[int, List[Dict[str, Any]]]:
        """
        Generate detailed improvement actions for each gap

        Args:
            phased_gaps: Gaps organized by phase

        Returns:
            Dictionary mapping phase to list of improvements
        """
        improvements = {1: [], 2: [], 3: [], 4: []}
        improvement_counter = 1

        for phase, gaps in phased_gaps.items():
            for gap in gaps:
                improvement = self._create_improvement(gap, improvement_counter)
                improvements[phase].append(improvement)
                improvement_counter += 1

        return improvements

    def _create_improvement(self, gap: Dict[str, Any], imp_id: int) -> Dict[str, Any]:
        """Create improvement action from gap"""
        gap_type = gap.get('type', 'default')
        severity = gap.get('severity', 'medium')
        description = gap.get('description', 'Unspecified gap')

        # Estimate effort
        effort_hours = self.effort_estimates.get(gap_type, self.effort_estimates['default'])

        # Adjust effort by severity
        effort_multiplier = {'critical': 1.5, 'high': 1.2, 'medium': 1.0, 'low': 0.8}
        effort_hours = int(effort_hours * effort_multiplier.get(severity, 1.0))

        # Generate title and action items
        title = self._generate_title(gap)
        action_items = self._generate_action_items(gap)
        success_criteria = self._generate_success_criteria(gap)
        expected_impact = self._generate_expected_impact(gap)

        # Determine owner
        owner = self._assign_owner(gap)

        # Identify dependencies
        dependencies = gap.get('dependencies', [])

        improvement = {
            'id': f"IMP-{imp_id:03d}",
            'gap_id': gap.get('id', f"GAP-{imp_id:03d}"),
            'severity': severity,
            'gap_type': gap_type,
            'title': title,
            'description': description,
            'action_items': action_items,
            'owner': owner,
            'effort_hours': effort_hours,
            'dependencies': dependencies,
            'success_criteria': success_criteria,
            'expected_impact': expected_impact
        }

        return improvement

    def _generate_title(self, gap: Dict[str, Any]) -> str:
        """Generate improvement title from gap"""
        gap_type = gap.get('type', 'default')
        step_name = gap.get('step_name', 'process step')

        title_templates = {
            'missing_owner': f"Assign ownership to {step_name}",
            'undefined_role': f"Define role for {step_name}",
            'missing_criteria': f"Define decision criteria for {step_name}",
            'missing_input': f"Document required inputs for {step_name}",
            'missing_output': f"Document expected outputs for {step_name}",
            'missing_exception': f"Add exception handling to {step_name}",
            'exception_handling': f"Improve exception handling in {step_name}",
            'missing_decision': f"Clarify decision logic in {step_name}",
            'process_inefficiency': f"Optimize {step_name}",
            'automation_opportunity': f"Automate {step_name}",
            'compliance_risk': f"Address compliance issues in {step_name}",
            'quality_issue': f"Improve quality controls for {step_name}",
            'default': f"Address gap in {step_name}"
        }

        return title_templates.get(gap_type, title_templates['default'])

    def _generate_action_items(self, gap: Dict[str, Any]) -> List[str]:
        """Generate specific action items for gap"""
        gap_type = gap.get('type', 'default')

        action_templates = {
            'missing_owner': [
                'Identify appropriate role or individual',
                'Update RACI matrix with responsibility assignment',
                'Communicate ownership to team',
                'Update process documentation'
            ],
            'undefined_role': [
                'Define role responsibilities',
                'Update RACI matrix',
                'Document role in process definition',
                'Train team on role expectations'
            ],
            'missing_criteria': [
                'Gather requirements from stakeholders',
                'Define measurable decision criteria',
                'Document criteria in process guide',
                'Train team on applying criteria consistently'
            ],
            'missing_input': [
                'Identify all required inputs',
                'Document input specifications',
                'Update process documentation',
                'Validate with process users'
            ],
            'missing_output': [
                'Define expected output deliverables',
                'Document output specifications',
                'Update process documentation',
                'Create output templates if needed'
            ],
            'missing_exception': [
                'Identify potential exceptions',
                'Design exception handling procedure',
                'Document escalation path',
                'Update process documentation',
                'Train team on exception handling'
            ],
            'missing_decision': [
                'Map decision logic',
                'Define decision criteria',
                'Document decision tree',
                'Train decision-makers'
            ],
            'process_inefficiency': [
                'Analyze current state bottlenecks',
                'Design improved workflow',
                'Pilot new approach',
                'Implement and monitor improvements'
            ],
            'automation_opportunity': [
                'Document automation requirements',
                'Evaluate automation tools',
                'Design automated workflow',
                'Implement and test automation',
                'Train users on new system'
            ],
            'compliance_risk': [
                'Review compliance requirements',
                'Design compliant process',
                'Document compliance controls',
                'Implement monitoring',
                'Audit and validate'
            ],
            'quality_issue': [
                'Define quality standards',
                'Implement quality checks',
                'Document quality procedures',
                'Train team on quality requirements'
            ]
        }

        return action_templates.get(gap_type, [
            'Analyze gap details',
            'Design solution',
            'Implement changes',
            'Validate improvements'
        ])

    def _generate_success_criteria(self, gap: Dict[str, Any]) -> str:
        """Generate success criteria for improvement"""
        gap_type = gap.get('type', 'default')

        criteria_templates = {
            'missing_owner': 'All process steps have assigned owners in RACI matrix',
            'undefined_role': 'All roles clearly defined with documented responsibilities',
            'missing_criteria': 'Decision criteria documented and consistently applied',
            'missing_input': 'All inputs documented with clear specifications',
            'missing_output': 'All outputs defined with quality standards',
            'missing_exception': 'Exception handling procedures documented and tested',
            'missing_decision': 'Decision logic documented with clear criteria',
            'process_inefficiency': 'Measurable reduction in cycle time or cost',
            'automation_opportunity': 'Manual steps automated with <5% error rate',
            'compliance_risk': '100% compliance in next audit',
            'quality_issue': 'Error rate reduced to target threshold',
            'default': 'Gap resolved and validated by stakeholders'
        }

        return criteria_templates.get(gap_type, criteria_templates['default'])

    def _generate_expected_impact(self, gap: Dict[str, Any]) -> str:
        """Generate expected impact description"""
        gap_type = gap.get('type', 'default')
        severity = gap.get('severity', 'medium')

        impact_map = self.impact_estimates.get(gap_type, self.impact_estimates['default'])

        # Adjust impact by severity
        severity_multiplier = {'critical': 1.5, 'high': 1.2, 'medium': 1.0, 'low': 0.7}
        multiplier = severity_multiplier.get(severity, 1.0)

        cycle_time = int(impact_map['cycle_time'] * multiplier)
        error_rate = int(impact_map['error_rate'] * multiplier)

        impacts = []
        if cycle_time > 0:
            impacts.append(f"Reduce cycle time by ~{cycle_time}%")
        if error_rate > 0:
            impacts.append(f"Reduce errors by ~{error_rate}%")

        return ', '.join(impacts) if impacts else 'Improve process quality'

    def _assign_owner(self, gap: Dict[str, Any]) -> str:
        """Assign owner role for improvement"""
        gap_type = gap.get('type', 'default')

        owner_map = {
            'missing_owner': 'Process Manager',
            'undefined_role': 'Process Manager',
            'missing_criteria': 'Business Analyst',
            'missing_input': 'Business Analyst',
            'missing_output': 'Business Analyst',
            'missing_exception': 'Process Owner',
            'exception_handling': 'Process Owner',
            'missing_decision': 'Process Owner',
            'process_inefficiency': 'Process Improvement Lead',
            'automation_opportunity': 'Technical Lead',
            'compliance_risk': 'Compliance Manager',
            'quality_issue': 'Quality Manager',
            'default': 'Process Owner'
        }

        return owner_map.get(gap_type, owner_map['default'])

    def _calculate_impact(self, gaps: List[Dict[str, Any]]) -> Dict[str, str]:
        """Calculate overall expected impact from all improvements"""
        total_cycle_time = 0
        total_error_rate = 0
        total_cost = 0

        for gap in gaps:
            gap_type = gap.get('type', 'default')
            severity = gap.get('severity', 'medium')

            impact_map = self.impact_estimates.get(gap_type, self.impact_estimates['default'])
            severity_multiplier = {'critical': 1.5, 'high': 1.2, 'medium': 1.0, 'low': 0.7}
            multiplier = severity_multiplier.get(severity, 1.0)

            total_cycle_time += impact_map['cycle_time'] * multiplier
            total_error_rate += impact_map['error_rate'] * multiplier
            total_cost += impact_map['cost'] * multiplier

        # Cap improvements at reasonable maximums
        cycle_time_reduction = min(int(total_cycle_time), 70)
        error_rate_reduction = min(int(total_error_rate), 80)

        # Estimate cost savings (simplified calculation)
        annual_savings = int(total_cost * 1000)  # Placeholder formula

        return {
            'cycle_time_reduction': f"{cycle_time_reduction}%",
            'error_rate_reduction': f"{error_rate_reduction}%",
            'cost_savings': f"${annual_savings:,}/year"
        }

    def _format_phases(self, improvements: Dict[int, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Format improvements into phase structure"""
        phases = []

        for phase_num in sorted(improvements.keys()):
            if not improvements[phase_num]:
                continue

            config = self.phase_config[phase_num]
            duration_weeks = int(self.timeline_weeks * config['duration_pct'])

            phase = {
                'phase': phase_num,
                'name': config['name'],
                'duration_weeks': max(duration_weeks, 1),
                'improvements': improvements[phase_num],
                'total_effort_hours': sum(imp['effort_hours'] for imp in improvements[phase_num])
            }

            phases.append(phase)

        return phases

    def _generate_milestones(self, improvements: Dict[int, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Generate milestone tracking points"""
        milestones = []
        weeks_elapsed = 0

        for phase_num in sorted(improvements.keys()):
            if not improvements[phase_num]:
                continue

            config = self.phase_config[phase_num]
            duration_weeks = int(self.timeline_weeks * config['duration_pct'])
            weeks_elapsed += max(duration_weeks, 1)

            # Key deliverables for this phase
            deliverables = []
            gap_types = set(imp['gap_type'] for imp in improvements[phase_num])

            if 'missing_owner' in gap_types or 'undefined_role' in gap_types:
                deliverables.append('Updated RACI matrix')
            if 'missing_criteria' in gap_types or 'missing_decision' in gap_types:
                deliverables.append('Decision criteria documentation')
            if 'missing_exception' in gap_types:
                deliverables.append('Exception handling procedures')
            if 'automation_opportunity' in gap_types:
                deliverables.append('Automation implementation')

            if not deliverables:
                deliverables.append('Process documentation updates')

            milestone = {
                'week': weeks_elapsed,
                'milestone': f"Phase {phase_num} Complete - {config['name']}",
                'deliverables': deliverables
            }

            milestones.append(milestone)

        return milestones

    def _allocate_resources(self, improvements: Dict[int, List[Dict[str, Any]]],
                          resources: Optional[Dict] = None) -> Dict[str, int]:
        """Allocate resource hours by role"""
        allocation = defaultdict(int)

        for phase_improvements in improvements.values():
            for imp in phase_improvements:
                owner = imp['owner']
                effort = imp['effort_hours']
                allocation[owner] += effort

        return dict(allocation)

    def _identify_risks(self, improvements: Dict[int, List[Dict[str, Any]]],
                       total_effort: int) -> List[Dict[str, str]]:
        """Identify implementation risks"""
        risks = []

        # Resource availability risk
        if total_effort > 500:
            risks.append({
                'risk': 'Resource availability',
                'impact': 'high',
                'mitigation': 'Secure dedicated resources and prioritize critical improvements first'
            })
        elif total_effort > 200:
            risks.append({
                'risk': 'Resource availability',
                'impact': 'medium',
                'mitigation': 'Schedule work during lower-demand periods'
            })

        # Change management risk
        total_improvements = sum(len(imps) for imps in improvements.values())
        if total_improvements > 15:
            risks.append({
                'risk': 'Change fatigue',
                'impact': 'medium',
                'mitigation': 'Implement strong change management and communication plan'
            })

        # Technical complexity risk
        automation_count = sum(
            1 for phase in improvements.values()
            for imp in phase
            if imp['gap_type'] == 'automation_opportunity'
        )
        if automation_count > 0:
            risks.append({
                'risk': 'Technical implementation complexity',
                'impact': 'medium',
                'mitigation': 'Conduct proof of concept before full implementation'
            })

        # Timeline risk
        if self.timeline_weeks < 8:
            risks.append({
                'risk': 'Aggressive timeline',
                'impact': 'medium',
                'mitigation': 'Build in buffer time and use agile approach with frequent reviews'
            })

        return risks

    def _generate_recommendations(self, gaps: List[Dict[str, Any]], total_effort: int) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []

        # Critical gaps
        critical_count = sum(1 for g in gaps if g.get('severity') == 'critical')
        if critical_count > 0:
            recommendations.append(
                f"Address {critical_count} critical gap(s) immediately to prevent process failures"
            )

        # Effort guidance
        if total_effort > 500:
            recommendations.append(
                "Consider phased implementation with pilot testing before full rollout"
            )

        # Automation opportunities
        automation_gaps = [g for g in gaps if g.get('type') == 'automation_opportunity']
        if automation_gaps:
            recommendations.append(
                f"Prioritize {len(automation_gaps)} automation opportunity(ies) for long-term efficiency gains"
            )

        # Quick wins
        quick_wins = [g for g in gaps if g.get('severity') == 'low']
        if quick_wins:
            recommendations.append(
                f"Implement {len(quick_wins)} quick win(s) early to build momentum"
            )

        # General advice
        recommendations.append("Establish regular review checkpoints to track progress and adjust plan")
        recommendations.append("Engage stakeholders early and maintain clear communication throughout")

        return recommendations

    def _print_summary(self, plan: Dict[str, Any]):
        """Print plan summary for verbose mode"""
        imp_plan = plan['improvement_plan']

        print(f"\n📊 Improvement Plan Summary")
        print(f"   Process: {plan['process_name']}")
        print(f"   Total Improvements: {imp_plan['total_improvements']}")
        print(f"   Total Effort: {imp_plan['total_effort_hours']} hours")
        print(f"   Timeline: {imp_plan['expected_timeline_weeks']} weeks")
        print(f"\n📈 Expected Impact:")
        print(f"   Cycle Time Reduction: {imp_plan['expected_impact']['cycle_time_reduction']}")
        print(f"   Error Rate Reduction: {imp_plan['expected_impact']['error_rate_reduction']}")
        print(f"   Cost Savings: {imp_plan['expected_impact']['cost_savings']}")
        print(f"\n✅ Plan generated successfully")


def format_markdown_output(plan: Dict[str, Any]) -> str:
    """Format plan as detailed markdown"""
    lines = []

    lines.append(f"# Process Improvement Plan: {plan['process_name']}")
    lines.append("")
    lines.append(f"**Generated:** {plan['plan_metadata']['created_at'][:10]}")
    lines.append(f"**Timeline:** {plan['improvement_plan']['expected_timeline_weeks']} weeks")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    imp_plan = plan['improvement_plan']
    lines.append(f"- **Total Improvements:** {imp_plan['total_improvements']}")
    lines.append(f"- **Total Effort:** {imp_plan['total_effort_hours']} hours")
    lines.append(f"- **Expected Timeline:** {imp_plan['expected_timeline_weeks']} weeks")
    lines.append("")

    lines.append("### Expected Impact")
    impact = imp_plan['expected_impact']
    lines.append(f"- **Cycle Time Reduction:** {impact['cycle_time_reduction']}")
    lines.append(f"- **Error Rate Reduction:** {impact['error_rate_reduction']}")
    lines.append(f"- **Cost Savings:** {impact['cost_savings']}")
    lines.append("")

    # Phases
    for phase in plan['phases']:
        lines.append(f"## Phase {phase['phase']}: {phase['name']} (Weeks 1-{phase['duration_weeks']})")
        lines.append("")
        lines.append(f"**Duration:** {phase['duration_weeks']} weeks | **Total Effort:** {phase['total_effort_hours']} hours")
        lines.append("")

        for imp in phase['improvements']:
            lines.append(f"### {imp['id']}: {imp['title']}")
            lines.append("")
            lines.append(f"- **Severity:** {imp['severity'].capitalize()}")
            lines.append(f"- **Owner:** {imp['owner']}")
            lines.append(f"- **Effort:** {imp['effort_hours']} hours")
            lines.append(f"- **Expected Impact:** {imp['expected_impact']}")
            lines.append("")

            lines.append("**Action Items:**")
            for action in imp['action_items']:
                lines.append(f"- {action}")
            lines.append("")

            lines.append(f"**Success Criteria:** {imp['success_criteria']}")
            lines.append("")

            if imp.get('dependencies'):
                lines.append(f"**Dependencies:** {', '.join(imp['dependencies'])}")
                lines.append("")

    # Milestones
    lines.append("## Milestones")
    lines.append("")
    for milestone in plan['milestones']:
        lines.append(f"### Week {milestone['week']}: {milestone['milestone']}")
        lines.append("")
        lines.append("**Deliverables:**")
        for deliverable in milestone['deliverables']:
            lines.append(f"- {deliverable}")
        lines.append("")

    # Resource Allocation
    lines.append("## Resource Allocation")
    lines.append("")
    lines.append("| Role | Total Hours |")
    lines.append("|------|-------------|")
    for role, hours in sorted(plan['resource_allocation'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {role} | {hours} |")
    lines.append("")

    # Risks
    lines.append("## Risks and Mitigation")
    lines.append("")
    for risk in plan['risks']:
        lines.append(f"### {risk['risk']}")
        lines.append(f"- **Impact:** {risk['impact'].capitalize()}")
        lines.append(f"- **Mitigation:** {risk['mitigation']}")
        lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    for i, rec in enumerate(plan['recommendations'], 1):
        lines.append(f"{i}. {rec}")
    lines.append("")

    return '\n'.join(lines)


def format_gantt_output(plan: Dict[str, Any]) -> str:
    """Format plan as markdown with Gantt chart"""
    lines = []

    lines.append(f"# Process Improvement Plan: {plan['process_name']}")
    lines.append("")

    # Timeline Overview
    lines.append("## Timeline Overview")
    imp_plan = plan['improvement_plan']
    lines.append(f"- **Total Duration:** {imp_plan['expected_timeline_weeks']} weeks")
    lines.append(f"- **Total Effort:** {imp_plan['total_effort_hours']} hours")
    lines.append(f"- **Expected Impact:** {imp_plan['expected_impact']['cycle_time_reduction']} cycle time reduction")
    lines.append("")

    # Gantt Chart
    lines.append("## Gantt Chart")
    lines.append("```mermaid")
    lines.append("gantt")
    lines.append("    title Process Improvement Timeline")
    lines.append("    dateFormat YYYY-MM-DD")

    # Calculate start date (today)
    start_date = datetime.now()

    for phase in plan['phases']:
        lines.append(f"    section Phase {phase['phase']}")
        phase_name = phase['name']
        duration = phase['duration_weeks']
        lines.append(f"    {phase_name}           :{start_date.strftime('%Y-%m-%d')}, {duration}w")
        start_date += timedelta(weeks=duration)

    lines.append("```")
    lines.append("")

    # Add detailed phase information
    lines.append("## Implementation Phases")
    lines.append("")

    for phase in plan['phases']:
        lines.append(f"### Phase {phase['phase']}: {phase['name']} ({phase['duration_weeks']} weeks)")
        lines.append("")
        lines.append(f"**Total Effort:** {phase['total_effort_hours']} hours")
        lines.append("")

        lines.append("**Key Improvements:**")
        for imp in phase['improvements'][:5]:  # Limit to top 5
            lines.append(f"- **{imp['id']}:** {imp['title']} ({imp['effort_hours']}h)")

        if len(phase['improvements']) > 5:
            lines.append(f"- ... and {len(phase['improvements']) - 5} more")

        lines.append("")

    # Add impact summary
    lines.append("## Expected Benefits")
    lines.append("")
    impact = imp_plan['expected_impact']
    lines.append(f"- Cycle time reduction: **{impact['cycle_time_reduction']}**")
    lines.append(f"- Error rate reduction: **{impact['error_rate_reduction']}**")
    lines.append(f"- Annual cost savings: **{impact['cost_savings']}**")
    lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Improvement Planner - Generate process improvement plans from gap analysis',
        epilog='Examples:\n'
               '  python improvement_planner.py --gaps gaps.json\n'
               '  python improvement_planner.py --gaps gaps.json --timeline 12 --output json\n'
               '  python improvement_planner.py --gaps gaps.json --output gantt\n'
               '  python improvement_planner.py --gaps gaps.json --process process.json --resources resources.json\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--gaps', type=str, required=True,
                       help='Gap analysis results file (JSON)')
    parser.add_argument('--process', type=str,
                       help='Optional process data file (JSON)')
    parser.add_argument('--resources', type=str,
                       help='Optional resource constraints file (JSON)')
    parser.add_argument('--timeline', type=int, default=12,
                       help='Target timeline in weeks (default: 12)')
    parser.add_argument('--output', type=str, default='json',
                       choices=['json', 'markdown', 'gantt'],
                       help='Output format (default: json)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    try:
        # Load gap analysis data
        if args.verbose:
            print(f"📂 Loading gap analysis: {args.gaps}")

        gaps_file = Path(args.gaps)
        if not gaps_file.exists():
            print(f"❌ Error: Gap analysis file not found: {args.gaps}", file=sys.stderr)
            sys.exit(EXIT_VALIDATION_ERROR)

        try:
            with open(gaps_file, 'r', encoding='utf-8') as f:
                gaps_data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in gaps file: {e}")
            print(f"❌ Error: Invalid JSON in gaps file: {e}", file=sys.stderr)
            sys.exit(EXIT_PARSE_ERROR)

        # Load optional process data
        process_data = None
        if args.process:
            if args.verbose:
                print(f"📂 Loading process data: {args.process}")

            process_file = Path(args.process)
            if process_file.exists():
                try:
                    with open(process_file, 'r', encoding='utf-8') as f:
                        process_data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"⚠️  Warning: Invalid JSON in process file: {e}", file=sys.stderr)

        # Load optional resources
        resources = None
        if args.resources:
            if args.verbose:
                print(f"📂 Loading resource constraints: {args.resources}")

            resources_file = Path(args.resources)
            if resources_file.exists():
                try:
                    with open(resources_file, 'r', encoding='utf-8') as f:
                        resources = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"⚠️  Warning: Invalid JSON in resources file: {e}", file=sys.stderr)

        # Create improvement plan
        planner = ImprovementPlanner(timeline_weeks=args.timeline, verbose=args.verbose)
        plan = planner.create_plan(gaps_data, process_data, resources)

        # Format output
        if args.output == 'json':
            output = json.dumps(plan, indent=2, ensure_ascii=False)
        elif args.output == 'markdown':
            output = format_markdown_output(plan)
        elif args.output == 'gantt':
            output = format_gantt_output(plan)
        else:
            output = json.dumps(plan, indent=2, ensure_ascii=False)

        # Print output
        print(output)

        sys.exit(EXIT_SUCCESS)

    except FileNotFoundError as e:
        print(f"❌ Error: File not found: {e}", file=sys.stderr)
        sys.exit(EXIT_VALIDATION_ERROR)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(EXIT_PLANNING_ERROR)


if __name__ == '__main__':
    main()
