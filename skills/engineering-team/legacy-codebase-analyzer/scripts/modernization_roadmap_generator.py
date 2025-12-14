#!/usr/bin/env python3
"""
Modernization Roadmap Generator

Generates comprehensive, phased modernization roadmap with timeline, milestones,
and success metrics for legacy codebases.

Usage:
    python modernization_roadmap_generator.py --input analysis_dir/
    python modernization_roadmap_generator.py -i debt_score.json --output markdown
    python modernization_roadmap_generator.py -i analysis/ --team-size 8 --timeline-months 18
    python modernization_roadmap_generator.py -i debt_score.json -o json -f roadmap.json
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import argparse
import json
import logging
import sys


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Priority(Enum):
    """Work item priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class WorkItemType(Enum):
    """Types of work items"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    CODE_QUALITY = "code_quality"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    TECHNICAL_DEBT = "technical_debt"


@dataclass
class WorkItem:
    """Individual work item in roadmap"""
    id: str
    title: str
    description: str
    type: str
    priority: str
    effort_points: int
    dependencies: List[str] = field(default_factory=list)
    impact: str = "medium"
    risk: str = "medium"

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Milestone:
    """Project milestone"""
    name: str
    description: str
    target_date: str
    success_criteria: List[str]
    deliverables: List[str]
    metrics: Dict[str, str]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class RoadmapPhase:
    """Phase in modernization roadmap"""
    phase_number: int
    name: str
    description: str
    duration_weeks: int
    start_week: int
    work_items: List[WorkItem]
    expected_outcomes: List[str]
    success_metrics: List[Dict[str, str]]
    risks: List[Dict[str, str]]
    effort_points: int = 0
    person_months: float = 0.0

    def to_dict(self) -> Dict:
        return {
            'phase_number': self.phase_number,
            'name': self.name,
            'description': self.description,
            'duration_weeks': self.duration_weeks,
            'start_week': self.start_week,
            'work_items': [item.to_dict() for item in self.work_items],
            'expected_outcomes': self.expected_outcomes,
            'success_metrics': self.success_metrics,
            'risks': self.risks,
            'effort_points': self.effort_points,
            'person_months': self.person_months
        }


@dataclass
class ROIEstimate:
    """Return on investment estimate"""
    investment_person_months: float
    investment_cost: float
    expected_savings_annual: float
    productivity_gain_percent: float
    payback_period_months: float
    net_benefit_3yr: float
    assumptions: List[str]

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ModernizationRoadmap:
    """Complete modernization roadmap"""
    generated_at: str
    project_name: str
    timeline_months: int
    team_size: int
    phases: List[RoadmapPhase]
    milestones: List[Milestone]
    roi_estimate: ROIEstimate
    gantt_diagram: str
    summary: Dict[str, any]

    def to_dict(self) -> Dict:
        return {
            'generated_at': self.generated_at,
            'project_name': self.project_name,
            'timeline_months': self.timeline_months,
            'team_size': self.team_size,
            'phases': [phase.to_dict() for phase in self.phases],
            'milestones': [milestone.to_dict() for milestone in self.milestones],
            'roi_estimate': self.roi_estimate.to_dict(),
            'gantt_diagram': self.gantt_diagram,
            'summary': self.summary
        }


class RoadmapGenerator:
    """Generates modernization roadmap from analysis data"""

    def __init__(self, team_size: int = 5, timeline_months: int = 12,
                 num_phases: int = 4, verbose: bool = False):
        self.team_size = team_size
        self.timeline_months = timeline_months
        self.num_phases = num_phases
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("ModernizationRoadmapGenerator initialized")

        # Effort calculation constants
        self.POINTS_PER_PERSON_WEEK = 8  # Story points per person per week
        self.WEEKS_PER_MONTH = 4.33
        self.AVG_DEVELOPER_COST_MONTHLY = 12000  # USD

    def log(self, message: str):
        """Log message if verbose mode enabled"""
        if self.verbose:
            print(f"[INFO] {message}", file=sys.stderr)

    def load_analysis_data(self, input_path: Path) -> Dict:
        """Load analysis data from file or directory"""
        self.log(f"Loading analysis data from: {input_path}")

        if input_path.is_file():
            with open(input_path, 'r') as f:
                data = json.load(f)
                self.log(f"Loaded data from single file")
                return data

        elif input_path.is_dir():
            # Load all JSON files from directory
            data = {
                'security': None,
                'performance': None,
                'architecture': None,
                'code_quality': None,
                'debt_score': None
            }

            for json_file in input_path.glob('*.json'):
                filename = json_file.stem.lower()
                with open(json_file, 'r') as f:
                    file_data = json.load(f)

                    if 'security' in filename or 'vulnerability' in filename:
                        data['security'] = file_data
                    elif 'performance' in filename or 'bottleneck' in filename:
                        data['performance'] = file_data
                    elif 'architecture' in filename:
                        data['architecture'] = file_data
                    elif 'quality' in filename:
                        data['code_quality'] = file_data
                    elif 'debt' in filename:
                        data['debt_score'] = file_data

            self.log(f"Loaded {sum(1 for v in data.values() if v)} analysis files")
            return data

        else:
            raise ValueError(f"Input path does not exist: {input_path}")

    def extract_work_items(self, data: Dict) -> List[WorkItem]:
        """Extract work items from analysis data"""
        self.log("Extracting work items from analysis data")
        work_items = []
        item_id = 1

        # Security vulnerabilities
        if data.get('security'):
            security_data = data['security']
            if 'vulnerabilities' in security_data:
                for vuln in security_data['vulnerabilities'][:20]:  # Limit to top 20
                    severity = vuln.get('severity', 'medium').lower()
                    priority = self._severity_to_priority(severity)

                    work_items.append(WorkItem(
                        id=f"SEC-{item_id:03d}",
                        title=f"Fix {severity} security issue: {vuln.get('type', 'Unknown')}",
                        description=vuln.get('description', 'Security vulnerability'),
                        type=WorkItemType.SECURITY.value,
                        priority=priority.value,
                        effort_points=self._estimate_security_effort(severity),
                        impact="high" if priority in [Priority.CRITICAL, Priority.HIGH] else "medium",
                        risk="high"
                    ))
                    item_id += 1

        # Performance bottlenecks
        if data.get('performance'):
            perf_data = data['performance']
            if 'bottlenecks' in perf_data:
                for bottleneck in perf_data['bottlenecks'][:15]:
                    severity = bottleneck.get('severity', 'medium').lower()

                    work_items.append(WorkItem(
                        id=f"PERF-{item_id:03d}",
                        title=f"Optimize {bottleneck.get('type', 'performance issue')}",
                        description=bottleneck.get('description', 'Performance optimization'),
                        type=WorkItemType.PERFORMANCE.value,
                        priority=Priority.HIGH.value if severity == 'high' else Priority.MEDIUM.value,
                        effort_points=self._estimate_performance_effort(severity),
                        impact="high",
                        risk="medium"
                    ))
                    item_id += 1

        # Architecture issues
        if data.get('architecture'):
            arch_data = data['architecture']
            if 'issues' in arch_data:
                for issue in arch_data['issues'][:15]:
                    work_items.append(WorkItem(
                        id=f"ARCH-{item_id:03d}",
                        title=f"Refactor: {issue.get('title', 'Architecture improvement')}",
                        description=issue.get('description', 'Architectural refactoring'),
                        type=WorkItemType.ARCHITECTURE.value,
                        priority=Priority.MEDIUM.value,
                        effort_points=self._estimate_architecture_effort(issue),
                        impact="high",
                        risk="medium"
                    ))
                    item_id += 1

        # Code quality issues
        if data.get('code_quality'):
            quality_data = data['code_quality']
            if 'issues' in quality_data:
                for issue in quality_data['issues'][:20]:
                    severity = issue.get('severity', 'medium').lower()

                    work_items.append(WorkItem(
                        id=f"QUAL-{item_id:03d}",
                        title=f"Improve code quality: {issue.get('type', 'Quality issue')}",
                        description=issue.get('description', 'Code quality improvement'),
                        type=WorkItemType.CODE_QUALITY.value,
                        priority=Priority.MEDIUM.value if severity == 'high' else Priority.LOW.value,
                        effort_points=self._estimate_quality_effort(severity),
                        impact="medium",
                        risk="low"
                    ))
                    item_id += 1

        # Add baseline work items if no analysis data
        if not work_items:
            work_items = self._generate_baseline_work_items()

        self.log(f"Extracted {len(work_items)} work items")
        return work_items

    def _severity_to_priority(self, severity: str) -> Priority:
        """Convert severity string to priority enum"""
        severity_map = {
            'critical': Priority.CRITICAL,
            'high': Priority.HIGH,
            'medium': Priority.MEDIUM,
            'low': Priority.LOW
        }
        return severity_map.get(severity.lower(), Priority.MEDIUM)

    def _estimate_security_effort(self, severity: str) -> int:
        """Estimate effort points for security fix"""
        effort_map = {
            'critical': 13,
            'high': 8,
            'medium': 5,
            'low': 3
        }
        return effort_map.get(severity.lower(), 5)

    def _estimate_performance_effort(self, severity: str) -> int:
        """Estimate effort points for performance optimization"""
        effort_map = {
            'critical': 13,
            'high': 8,
            'medium': 5,
            'low': 3
        }
        return effort_map.get(severity.lower(), 5)

    def _estimate_architecture_effort(self, issue: Dict) -> int:
        """Estimate effort points for architecture work"""
        # Base effort on complexity indicators
        complexity = issue.get('complexity', 'medium').lower()
        effort_map = {
            'high': 21,
            'medium': 13,
            'low': 8
        }
        return effort_map.get(complexity, 13)

    def _estimate_quality_effort(self, severity: str) -> int:
        """Estimate effort points for quality improvements"""
        effort_map = {
            'critical': 8,
            'high': 5,
            'medium': 3,
            'low': 2
        }
        return effort_map.get(severity.lower(), 3)

    def _generate_baseline_work_items(self) -> List[WorkItem]:
        """Generate baseline work items when no analysis data available"""
        self.log("Generating baseline work items")
        return [
            WorkItem(
                id="BASE-001",
                title="Security audit and vulnerability fixes",
                description="Comprehensive security review and critical vulnerability remediation",
                type=WorkItemType.SECURITY.value,
                priority=Priority.CRITICAL.value,
                effort_points=21,
                impact="high",
                risk="high"
            ),
            WorkItem(
                id="BASE-002",
                title="Performance profiling and optimization",
                description="Identify and fix performance bottlenecks",
                type=WorkItemType.PERFORMANCE.value,
                priority=Priority.HIGH.value,
                effort_points=13,
                impact="high",
                risk="medium"
            ),
            WorkItem(
                id="BASE-003",
                title="Architecture assessment and planning",
                description="Evaluate current architecture and plan improvements",
                type=WorkItemType.ARCHITECTURE.value,
                priority=Priority.HIGH.value,
                effort_points=13,
                impact="high",
                risk="medium"
            ),
            WorkItem(
                id="BASE-004",
                title="Code quality baseline establishment",
                description="Set up linting, formatting, and quality gates",
                type=WorkItemType.CODE_QUALITY.value,
                priority=Priority.MEDIUM.value,
                effort_points=8,
                impact="medium",
                risk="low"
            ),
            WorkItem(
                id="BASE-005",
                title="Test coverage improvement",
                description="Increase test coverage to 70%+ with unit and integration tests",
                type=WorkItemType.TESTING.value,
                priority=Priority.MEDIUM.value,
                effort_points=21,
                impact="high",
                risk="medium"
            ),
            WorkItem(
                id="BASE-006",
                title="Documentation update",
                description="Update technical documentation and API docs",
                type=WorkItemType.DOCUMENTATION.value,
                priority=Priority.MEDIUM.value,
                effort_points=8,
                impact="medium",
                risk="low"
            )
        ]

    def create_phases(self, work_items: List[WorkItem]) -> List[RoadmapPhase]:
        """Organize work items into phases"""
        self.log(f"Creating {self.num_phases} phases")

        # Sort work items by priority and type
        sorted_items = sorted(
            work_items,
            key=lambda x: (
                ['critical', 'high', 'medium', 'low'].index(x.priority),
                ['security', 'performance', 'architecture', 'code_quality',
                 'testing', 'documentation', 'technical_debt'].index(x.type)
            )
        )

        # Calculate total effort capacity
        total_weeks = int(self.timeline_months * self.WEEKS_PER_MONTH)
        weeks_per_phase = total_weeks // self.num_phases

        phases = []

        # Phase 1: Foundation (Security & Critical Issues)
        phase1_items = [
            item for item in sorted_items
            if item.priority in [Priority.CRITICAL.value, Priority.HIGH.value]
            and item.type in [WorkItemType.SECURITY.value, WorkItemType.PERFORMANCE.value]
        ][:10]

        phases.append(RoadmapPhase(
            phase_number=1,
            name="Foundation & Security",
            description="Address critical security vulnerabilities and establish baseline stability",
            duration_weeks=weeks_per_phase,
            start_week=0,
            work_items=phase1_items,
            expected_outcomes=[
                "All critical security vulnerabilities resolved",
                "Performance baseline established",
                "Production stability improved",
                "Security scanning integrated into CI/CD"
            ],
            success_metrics=[
                {"metric": "Critical vulnerabilities", "target": "0"},
                {"metric": "High vulnerabilities", "target": "< 5"},
                {"metric": "Security scan coverage", "target": "100%"},
                {"metric": "Production incidents", "target": "< 2/month"}
            ],
            risks=[
                {"risk": "Unknown dependencies may surface", "mitigation": "Thorough testing and staged rollout"},
                {"risk": "Business impact from changes", "mitigation": "Feature flags and rollback plan"}
            ]
        ))

        # Phase 2: Stabilization (Quality & Testing)
        phase2_items = [
            item for item in sorted_items
            if item.type in [WorkItemType.CODE_QUALITY.value, WorkItemType.TESTING.value]
        ][:12]

        phases.append(RoadmapPhase(
            phase_number=2,
            name="Stabilization & Quality",
            description="Improve code quality, increase test coverage, and establish quality gates",
            duration_weeks=weeks_per_phase,
            start_week=weeks_per_phase,
            work_items=phase2_items,
            expected_outcomes=[
                "Test coverage increased to 70%+",
                "Code quality metrics improved by 40%",
                "CI/CD pipeline with quality gates",
                "Automated testing suite operational"
            ],
            success_metrics=[
                {"metric": "Test coverage", "target": "> 70%"},
                {"metric": "Code quality score", "target": "> 7.0/10"},
                {"metric": "Technical debt ratio", "target": "< 10%"},
                {"metric": "Build success rate", "target": "> 95%"}
            ],
            risks=[
                {"risk": "Legacy code difficult to test", "mitigation": "Refactor in small increments"},
                {"risk": "Team learning curve", "mitigation": "Training and pair programming"}
            ]
        ))

        # Phase 3: Modernization (Architecture)
        phase3_items = [
            item for item in sorted_items
            if item.type in [WorkItemType.ARCHITECTURE.value, WorkItemType.TECHNICAL_DEBT.value]
        ][:10]

        phases.append(RoadmapPhase(
            phase_number=3,
            name="Architecture Modernization",
            description="Refactor architecture, reduce technical debt, implement modern patterns",
            duration_weeks=weeks_per_phase,
            start_week=weeks_per_phase * 2,
            work_items=phase3_items,
            expected_outcomes=[
                "Modern architecture patterns implemented",
                "Technical debt reduced by 50%",
                "Scalability improved",
                "Microservices or modular architecture in place"
            ],
            success_metrics=[
                {"metric": "Coupling score", "target": "< 0.3"},
                {"metric": "Cyclomatic complexity", "target": "< 10 avg"},
                {"metric": "Module cohesion", "target": "> 0.7"},
                {"metric": "Deployment frequency", "target": "Weekly"}
            ],
            risks=[
                {"risk": "Large refactoring scope", "mitigation": "Strangler pattern approach"},
                {"risk": "Breaking changes", "mitigation": "Comprehensive integration tests"}
            ]
        ))

        # Phase 4: Optimization (Polish & Performance)
        phase4_items = [
            item for item in sorted_items
            if item not in phase1_items + phase2_items + phase3_items
        ][:10]

        phases.append(RoadmapPhase(
            phase_number=4,
            name="Optimization & Enhancement",
            description="Performance tuning, documentation, and final improvements",
            duration_weeks=weeks_per_phase,
            start_week=weeks_per_phase * 3,
            work_items=phase4_items,
            expected_outcomes=[
                "Performance optimized for production scale",
                "Comprehensive documentation complete",
                "Monitoring and observability implemented",
                "Team fully trained on new architecture"
            ],
            success_metrics=[
                {"metric": "API response time", "target": "< 200ms p95"},
                {"metric": "Documentation coverage", "target": "100%"},
                {"metric": "Monitoring coverage", "target": "100%"},
                {"metric": "Team satisfaction", "target": "> 8/10"}
            ],
            risks=[
                {"risk": "Optimization complexity", "mitigation": "Data-driven decisions"},
                {"risk": "Documentation drift", "mitigation": "Automated doc generation"}
            ]
        ))

        # Calculate effort and duration for each phase
        for phase in phases:
            phase.effort_points = sum(item.effort_points for item in phase.work_items)
            capacity_per_phase = self.team_size * phase.duration_weeks * self.POINTS_PER_PERSON_WEEK
            phase.person_months = phase.effort_points / (self.POINTS_PER_PERSON_WEEK * self.WEEKS_PER_MONTH)

            self.log(f"Phase {phase.phase_number}: {len(phase.work_items)} items, "
                    f"{phase.effort_points} points, {phase.person_months:.1f} person-months")

        return phases

    def create_milestones(self, phases: List[RoadmapPhase]) -> List[Milestone]:
        """Create milestones based on phases"""
        self.log("Creating milestones")
        milestones = []
        start_date = datetime.now()

        for phase in phases:
            milestone_date = start_date + timedelta(weeks=phase.start_week + phase.duration_weeks)

            milestones.append(Milestone(
                name=f"{phase.name} Complete",
                description=f"Completion of {phase.name} phase",
                target_date=milestone_date.strftime("%Y-%m-%d"),
                success_criteria=[metric['metric'] + ': ' + metric['target']
                                for metric in phase.success_metrics],
                deliverables=[outcome for outcome in phase.expected_outcomes],
                metrics={
                    "work_items_completed": str(len(phase.work_items)),
                    "effort_points": str(phase.effort_points),
                    "phase_duration": f"{phase.duration_weeks} weeks"
                }
            ))

        return milestones

    def calculate_roi(self, phases: List[RoadmapPhase]) -> ROIEstimate:
        """Calculate return on investment estimate"""
        self.log("Calculating ROI estimate")

        # Calculate total investment
        total_person_months = sum(phase.person_months for phase in phases)
        total_cost = total_person_months * self.AVG_DEVELOPER_COST_MONTHLY

        # Estimate savings (based on typical modernization benefits)
        # These are conservative estimates based on industry averages
        productivity_gain_percent = 35.0  # 30-40% typical
        reduced_incidents_savings = total_cost * 0.15  # 15% of cost
        faster_features_value = total_cost * 0.25  # 25% of cost
        reduced_maintenance = total_cost * 0.20  # 20% of cost

        expected_annual_savings = (
            reduced_incidents_savings +
            faster_features_value +
            reduced_maintenance
        )

        # Calculate payback period
        if expected_annual_savings > 0:
            payback_months = total_cost / (expected_annual_savings / 12)
        else:
            payback_months = float('inf')

        # 3-year net benefit
        net_benefit_3yr = (expected_annual_savings * 3) - total_cost

        return ROIEstimate(
            investment_person_months=round(total_person_months, 1),
            investment_cost=round(total_cost, 2),
            expected_savings_annual=round(expected_annual_savings, 2),
            productivity_gain_percent=productivity_gain_percent,
            payback_period_months=round(payback_months, 1),
            net_benefit_3yr=round(net_benefit_3yr, 2),
            assumptions=[
                f"Team size: {self.team_size} developers",
                f"Average developer cost: ${self.AVG_DEVELOPER_COST_MONTHLY}/month",
                f"Timeline: {self.timeline_months} months",
                f"Productivity gain: {productivity_gain_percent}%",
                "Reduced incident response costs",
                "Faster feature delivery",
                "Lower maintenance overhead",
                "Assumes successful execution and adoption"
            ]
        )

    def generate_gantt_diagram(self, phases: List[RoadmapPhase]) -> str:
        """Generate Mermaid Gantt chart"""
        self.log("Generating Gantt diagram")

        lines = [
            "gantt",
            "    title Modernization Roadmap Timeline",
            "    dateFormat YYYY-MM-DD",
            "    section Phases"
        ]

        start_date = datetime.now()

        for phase in phases:
            phase_start = start_date + timedelta(weeks=phase.start_week)
            phase_end = phase_start + timedelta(weeks=phase.duration_weeks)

            lines.append(
                f"    {phase.name} :{phase_start.strftime('%Y-%m-%d')}, "
                f"{phase.duration_weeks}w"
            )

        lines.append("    section Milestones")

        for phase in phases:
            milestone_date = start_date + timedelta(weeks=phase.start_week + phase.duration_weeks)
            lines.append(
                f"    {phase.name} Done :milestone, "
                f"{milestone_date.strftime('%Y-%m-%d')}, 0d"
            )

        return "\n".join(lines)

    def generate_roadmap(self, input_path: Path, project_name: str = "Legacy Modernization") -> ModernizationRoadmap:
        """Generate complete modernization roadmap"""
        self.log(f"Generating roadmap for: {project_name}")

        # Load analysis data
        data = self.load_analysis_data(input_path)

        # Extract work items
        work_items = self.extract_work_items(data)

        # Create phases
        phases = self.create_phases(work_items)

        # Create milestones
        milestones = self.create_milestones(phases)

        # Calculate ROI
        roi_estimate = self.calculate_roi(phases)

        # Generate Gantt diagram
        gantt_diagram = self.generate_gantt_diagram(phases)

        # Create summary
        total_work_items = sum(len(phase.work_items) for phase in phases)
        total_effort = sum(phase.effort_points for phase in phases)

        summary = {
            "total_phases": len(phases),
            "total_work_items": total_work_items,
            "total_effort_points": total_effort,
            "total_person_months": round(sum(phase.person_months for phase in phases), 1),
            "timeline_weeks": int(self.timeline_months * self.WEEKS_PER_MONTH),
            "team_size": self.team_size,
            "estimated_cost": roi_estimate.investment_cost,
            "expected_roi": f"{((roi_estimate.net_benefit_3yr / roi_estimate.investment_cost) * 100):.1f}%",
            "payback_period": f"{roi_estimate.payback_period_months:.1f} months"
        }

        roadmap = ModernizationRoadmap(
            generated_at=datetime.now().isoformat(),
            project_name=project_name,
            timeline_months=self.timeline_months,
            team_size=self.team_size,
            phases=phases,
            milestones=milestones,
            roi_estimate=roi_estimate,
            gantt_diagram=gantt_diagram,
            summary=summary
        )

        self.log("Roadmap generation complete")
        return roadmap


class OutputFormatter:
    """Format roadmap output in different formats"""

    @staticmethod
    def format_json(roadmap: ModernizationRoadmap) -> str:
        """Format as JSON"""
        return json.dumps(roadmap.to_dict(), indent=2)

    @staticmethod
    def format_text(roadmap: ModernizationRoadmap) -> str:
        """Format as plain text"""
        lines = [
            "=" * 80,
            f"MODERNIZATION ROADMAP: {roadmap.project_name}",
            "=" * 80,
            "",
            f"Generated: {roadmap.generated_at}",
            f"Timeline: {roadmap.timeline_months} months ({roadmap.summary['timeline_weeks']} weeks)",
            f"Team Size: {roadmap.team_size} developers",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 80,
            f"Total Phases: {roadmap.summary['total_phases']}",
            f"Total Work Items: {roadmap.summary['total_work_items']}",
            f"Total Effort: {roadmap.summary['total_effort_points']} story points "
            f"({roadmap.summary['total_person_months']} person-months)",
            f"Estimated Investment: ${roadmap.summary['estimated_cost']:,.2f}",
            f"Expected 3-Year ROI: {roadmap.summary['expected_roi']}",
            f"Payback Period: {roadmap.summary['payback_period']}",
            "",
        ]

        # Phases
        for phase in roadmap.phases:
            lines.extend([
                "",
                f"PHASE {phase.phase_number}: {phase.name}",
                "-" * 80,
                f"Duration: {phase.duration_weeks} weeks (Week {phase.start_week + 1} - "
                f"Week {phase.start_week + phase.duration_weeks})",
                f"Effort: {phase.effort_points} story points ({phase.person_months:.1f} person-months)",
                "",
                f"Description: {phase.description}",
                "",
                f"Work Items ({len(phase.work_items)}):",
            ])

            for item in phase.work_items[:5]:  # Show first 5
                lines.append(f"  [{item.priority.upper()}] {item.id}: {item.title} ({item.effort_points} pts)")

            if len(phase.work_items) > 5:
                lines.append(f"  ... and {len(phase.work_items) - 5} more items")

            lines.extend([
                "",
                "Expected Outcomes:",
            ])
            for outcome in phase.expected_outcomes:
                lines.append(f"  - {outcome}")

            lines.extend([
                "",
                "Success Metrics:",
            ])
            for metric in phase.success_metrics:
                lines.append(f"  - {metric['metric']}: {metric['target']}")

        # Milestones
        lines.extend([
            "",
            "",
            "KEY MILESTONES",
            "-" * 80,
        ])

        for milestone in roadmap.milestones:
            lines.extend([
                f"\n{milestone.name} - {milestone.target_date}",
                f"  {milestone.description}",
                "  Success Criteria:",
            ])
            for criteria in milestone.success_criteria[:3]:
                lines.append(f"    - {criteria}")

        # ROI
        roi = roadmap.roi_estimate
        lines.extend([
            "",
            "",
            "ROI ESTIMATE",
            "-" * 80,
            f"Investment: ${roi.investment_cost:,.2f} ({roi.investment_person_months} person-months)",
            f"Expected Annual Savings: ${roi.expected_savings_annual:,.2f}",
            f"Productivity Gain: {roi.productivity_gain_percent}%",
            f"Payback Period: {roi.payback_period_months:.1f} months",
            f"3-Year Net Benefit: ${roi.net_benefit_3yr:,.2f}",
            "",
            "Assumptions:",
        ])

        for assumption in roi.assumptions:
            lines.append(f"  - {assumption}")

        lines.extend([
            "",
            "=" * 80,
        ])

        return "\n".join(lines)

    @staticmethod
    def format_markdown(roadmap: ModernizationRoadmap) -> str:
        """Format as Markdown"""
        lines = [
            f"# Modernization Roadmap: {roadmap.project_name}",
            "",
            f"**Generated:** {roadmap.generated_at}  ",
            f"**Timeline:** {roadmap.timeline_months} months ({roadmap.summary['timeline_weeks']} weeks)  ",
            f"**Team Size:** {roadmap.team_size} developers",
            "",
            "## Executive Summary",
            "",
            f"- **Total Phases:** {roadmap.summary['total_phases']}",
            f"- **Total Work Items:** {roadmap.summary['total_work_items']}",
            f"- **Total Effort:** {roadmap.summary['total_effort_points']} story points "
            f"({roadmap.summary['total_person_months']} person-months)",
            f"- **Estimated Investment:** ${roadmap.summary['estimated_cost']:,.2f}",
            f"- **Expected 3-Year ROI:** {roadmap.summary['expected_roi']}",
            f"- **Payback Period:** {roadmap.summary['payback_period']}",
            "",
            "## Timeline Visualization",
            "",
            "```mermaid",
            roadmap.gantt_diagram,
            "```",
            "",
            "## Phases",
            "",
        ]

        # Phases
        for phase in roadmap.phases:
            lines.extend([
                f"### Phase {phase.phase_number}: {phase.name}",
                "",
                f"**Duration:** {phase.duration_weeks} weeks (Week {phase.start_week + 1} - "
                f"Week {phase.start_week + phase.duration_weeks})  ",
                f"**Effort:** {phase.effort_points} story points ({phase.person_months:.1f} person-months)",
                "",
                f"**Description:** {phase.description}",
                "",
                f"#### Work Items ({len(phase.work_items)})",
                "",
            ])

            for item in phase.work_items:
                lines.append(
                    f"- **[{item.priority.upper()}]** `{item.id}`: {item.title} "
                    f"({item.effort_points} pts)"
                )

            lines.extend([
                "",
                "#### Expected Outcomes",
                "",
            ])
            for outcome in phase.expected_outcomes:
                lines.append(f"- {outcome}")

            lines.extend([
                "",
                "#### Success Metrics",
                "",
                "| Metric | Target |",
                "|--------|--------|",
            ])
            for metric in phase.success_metrics:
                lines.append(f"| {metric['metric']} | {metric['target']} |")

            lines.extend([
                "",
                "#### Risks & Mitigation",
                "",
            ])
            for risk in phase.risks:
                lines.append(f"- **Risk:** {risk['risk']}")
                lines.append(f"  - **Mitigation:** {risk['mitigation']}")

            lines.append("")

        # Milestones
        lines.extend([
            "## Key Milestones",
            "",
        ])

        for milestone in roadmap.milestones:
            lines.extend([
                f"### {milestone.name}",
                f"**Target Date:** {milestone.target_date}",
                "",
                f"{milestone.description}",
                "",
                "**Success Criteria:**",
            ])
            for criteria in milestone.success_criteria:
                lines.append(f"- {criteria}")
            lines.append("")

        # ROI
        roi = roadmap.roi_estimate
        lines.extend([
            "## ROI Estimate",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Investment | ${roi.investment_cost:,.2f} ({roi.investment_person_months} person-months) |",
            f"| Expected Annual Savings | ${roi.expected_savings_annual:,.2f} |",
            f"| Productivity Gain | {roi.productivity_gain_percent}% |",
            f"| Payback Period | {roi.payback_period_months:.1f} months |",
            f"| 3-Year Net Benefit | ${roi.net_benefit_3yr:,.2f} |",
            "",
            "### Assumptions",
            "",
        ])

        for assumption in roi.assumptions:
            lines.append(f"- {assumption}")

        lines.extend([
            "",
            "---",
            "",
            f"*This roadmap was generated on {roadmap.generated_at}*",
        ])

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive modernization roadmap with timeline and ROI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from analysis directory
  python modernization_roadmap_generator.py --input analysis_results/

  # Generate with custom team size and timeline
  python modernization_roadmap_generator.py -i debt_score.json --team-size 8 --timeline-months 18

  # Generate markdown report
  python modernization_roadmap_generator.py -i analysis/ -o markdown -f roadmap.md

  # Generate with verbose output
  python modernization_roadmap_generator.py -i analysis/ -v
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        type=Path,
        help='Input directory with analysis files or debt_score.json file'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        type=Path,
        help='Output file path (optional, prints to stdout if not specified)'
    )

    parser.add_argument(
        '--team-size',
        type=int,
        default=5,
        help='Team size in developers (default: 5)'
    )

    parser.add_argument(
        '--timeline-months',
        type=int,
        default=12,
        help='Timeline in months (default: 12)'
    )

    parser.add_argument(
        '--phases',
        type=int,
        default=4,
        help='Number of phases (default: 4)'
    )

    parser.add_argument(
        '--project-name',
        default='Legacy Modernization',
        help='Project name for roadmap (default: "Legacy Modernization")'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Validate input
    if not args.input.exists():
        print(f"Error: Input path does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        # Generate roadmap
        generator = RoadmapGenerator(
            team_size=args.team_size,
            timeline_months=args.timeline_months,
            num_phases=args.phases,
            verbose=args.verbose
        )

        roadmap = generator.generate_roadmap(args.input, args.project_name)

        # Format output
        formatter = OutputFormatter()

        if args.output == 'json':
            output = formatter.format_json(roadmap)
        elif args.output == 'markdown':
            output = formatter.format_markdown(roadmap)
        else:  # text
            output = formatter.format_text(roadmap)

        # Write or print output
        if args.file:
            args.file.parent.mkdir(parents=True, exist_ok=True)
            with open(args.file, 'w') as f:
                f.write(output)
            print(f"Roadmap generated: {args.file}", file=sys.stderr)
        else:
            print(output)

        if args.verbose:
            print(f"\n[SUCCESS] Generated roadmap with {roadmap.summary['total_phases']} phases, "
                  f"{roadmap.summary['total_work_items']} work items", file=sys.stderr)

    except Exception as e:
        print(f"Error generating roadmap: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
