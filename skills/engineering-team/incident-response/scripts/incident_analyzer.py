#!/usr/bin/env python3
"""
Incident Analyzer - Root Cause Analysis and Impact Assessment Tool

Root cause analysis, impact assessment, and post-incident report generation
for security incident response.

Features:
- Attack vector and entry point identification
- Dwell time calculation and lateral movement mapping
- Business impact quantification (systems, users, data, cost)
- MTTD/MTTR metrics calculation
- Markdown and HTML report generation
- Lessons learned documentation

Usage:
    python incident_analyzer.py --incident INC-001 --rca
    python incident_analyzer.py --incident INC-001 --impact
    python incident_analyzer.py --incident INC-001 --report --output markdown

Author: Claude Skills Team
Version: 1.0.0
License: MIT
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

__version__ = "1.0.0"


# =============================================================================
# ENUMS AND DATA CLASSES
# =============================================================================

class AttackVector(Enum):
    """Classification of attack vectors."""
    PHISHING = "phishing"
    VULNERABILITY_EXPLOITATION = "vulnerability_exploitation"
    CREDENTIAL_THEFT = "credential_theft"
    MISCONFIGURATION = "misconfiguration"
    INSIDER_THREAT = "insider_threat"
    SUPPLY_CHAIN = "supply_chain"
    SOCIAL_ENGINEERING = "social_engineering"
    BRUTE_FORCE = "brute_force"
    ZERO_DAY = "zero_day"
    PHYSICAL_ACCESS = "physical_access"
    UNKNOWN = "unknown"


class DataClassification(Enum):
    """Classification of data sensitivity levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    PII = "pii"
    PHI = "phi"
    PCI = "pci"
    TRADE_SECRET = "trade_secret"


class ImpactCategory(Enum):
    """Categories of business impact."""
    DATA_CONFIDENTIALITY = "data_confidentiality"
    DATA_INTEGRITY = "data_integrity"
    SYSTEM_AVAILABILITY = "system_availability"
    FINANCIAL = "financial"
    REGULATORY = "regulatory"
    REPUTATIONAL = "reputational"
    OPERATIONAL = "operational"


class RemediationPriority(Enum):
    """Priority levels for remediation actions."""
    IMMEDIATE = "immediate"  # Within 24 hours
    SHORT_TERM = "short_term"  # Within 30 days
    MEDIUM_TERM = "medium_term"  # Within 90 days
    LONG_TERM = "long_term"  # Within 12 months


@dataclass
class RootCauseAnalysis:
    """Root cause analysis results."""
    incident_id: str
    attack_vector: AttackVector
    entry_point: str
    vulnerability_exploited: Optional[str] = None
    cve_id: Optional[str] = None
    initial_compromise_time: str = ""
    detection_time: str = ""
    dwell_time_hours: float = 0.0
    lateral_movement_path: List[str] = field(default_factory=list)
    persistence_mechanisms: List[str] = field(default_factory=list)
    data_accessed: List[str] = field(default_factory=list)
    tools_used_by_attacker: List[str] = field(default_factory=list)
    ttps_identified: List[str] = field(default_factory=list)
    confidence_level: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "incident_id": self.incident_id,
            "attack_vector": self.attack_vector.value,
            "entry_point": self.entry_point,
            "vulnerability_exploited": self.vulnerability_exploited,
            "cve_id": self.cve_id,
            "initial_compromise_time": self.initial_compromise_time,
            "detection_time": self.detection_time,
            "dwell_time_hours": self.dwell_time_hours,
            "lateral_movement_path": self.lateral_movement_path,
            "persistence_mechanisms": self.persistence_mechanisms,
            "data_accessed": self.data_accessed,
            "tools_used_by_attacker": self.tools_used_by_attacker,
            "ttps_identified": self.ttps_identified,
            "confidence_level": self.confidence_level
        }


@dataclass
class DataExposure:
    """Information about exposed data."""
    data_type: DataClassification
    record_count: int
    affected_systems: List[str]
    exposure_confirmed: bool
    exfiltration_confirmed: bool

    def to_dict(self) -> Dict:
        return {
            "data_type": self.data_type.value,
            "record_count": self.record_count,
            "affected_systems": self.affected_systems,
            "exposure_confirmed": self.exposure_confirmed,
            "exfiltration_confirmed": self.exfiltration_confirmed
        }


@dataclass
class ImpactAssessment:
    """Business impact assessment results."""
    incident_id: str
    affected_systems: List[str] = field(default_factory=list)
    affected_users: int = 0
    affected_customers: int = 0
    data_exposure: List[DataExposure] = field(default_factory=list)
    downtime_hours: float = 0.0
    estimated_financial_impact: float = 0.0
    regulatory_implications: List[str] = field(default_factory=list)
    notification_requirements: List[str] = field(default_factory=list)
    impact_score: float = 0.0  # 0-10 scale
    impact_categories: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "incident_id": self.incident_id,
            "affected_systems": self.affected_systems,
            "affected_users": self.affected_users,
            "affected_customers": self.affected_customers,
            "data_exposure": [d.to_dict() for d in self.data_exposure],
            "downtime_hours": self.downtime_hours,
            "estimated_financial_impact": self.estimated_financial_impact,
            "regulatory_implications": self.regulatory_implications,
            "notification_requirements": self.notification_requirements,
            "impact_score": self.impact_score,
            "impact_categories": self.impact_categories
        }


@dataclass
class RemediationAction:
    """A single remediation action item."""
    action_id: str
    description: str
    priority: RemediationPriority
    owner: str = "Security Team"
    due_date: str = ""
    status: str = "open"
    effort_hours: float = 0.0
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "action_id": self.action_id,
            "description": self.description,
            "priority": self.priority.value,
            "owner": self.owner,
            "due_date": self.due_date,
            "status": self.status,
            "effort_hours": self.effort_hours,
            "dependencies": self.dependencies
        }


@dataclass
class RemediationPlan:
    """Complete remediation plan."""
    incident_id: str
    immediate_actions: List[RemediationAction] = field(default_factory=list)
    short_term_fixes: List[RemediationAction] = field(default_factory=list)
    medium_term_improvements: List[RemediationAction] = field(default_factory=list)
    long_term_initiatives: List[RemediationAction] = field(default_factory=list)
    preventive_controls: List[str] = field(default_factory=list)
    detection_improvements: List[str] = field(default_factory=list)
    total_effort_hours: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "incident_id": self.incident_id,
            "immediate_actions": [a.to_dict() for a in self.immediate_actions],
            "short_term_fixes": [a.to_dict() for a in self.short_term_fixes],
            "medium_term_improvements": [a.to_dict() for a in self.medium_term_improvements],
            "long_term_initiatives": [a.to_dict() for a in self.long_term_initiatives],
            "preventive_controls": self.preventive_controls,
            "detection_improvements": self.detection_improvements,
            "total_effort_hours": self.total_effort_hours
        }


@dataclass
class IncidentMetrics:
    """Incident response metrics."""
    incident_id: str
    mttd_hours: float = 0.0  # Mean Time to Detect
    mttr_hours: float = 0.0  # Mean Time to Respond
    mttc_hours: float = 0.0  # Mean Time to Contain
    mtte_hours: float = 0.0  # Mean Time to Eradicate
    mttrec_hours: float = 0.0  # Mean Time to Recover
    containment_effectiveness: float = 0.0  # 0-100%
    evidence_completeness: float = 0.0  # 0-100%
    communication_timeliness: float = 0.0  # 0-100%

    def to_dict(self) -> Dict:
        return {
            "incident_id": self.incident_id,
            "mttd_hours": self.mttd_hours,
            "mttr_hours": self.mttr_hours,
            "mttc_hours": self.mttc_hours,
            "mtte_hours": self.mtte_hours,
            "mttrec_hours": self.mttrec_hours,
            "containment_effectiveness": self.containment_effectiveness,
            "evidence_completeness": self.evidence_completeness,
            "communication_timeliness": self.communication_timeliness
        }


@dataclass
class LessonLearned:
    """A single lesson learned from the incident."""
    category: str
    observation: str
    recommendation: str
    priority: str

    def to_dict(self) -> Dict:
        return {
            "category": self.category,
            "observation": self.observation,
            "recommendation": self.recommendation,
            "priority": self.priority
        }


# =============================================================================
# COST ESTIMATION FACTORS
# =============================================================================

COST_FACTORS = {
    "per_pii_record": 180,  # Average cost per PII record breach (IBM report)
    "per_phi_record": 500,  # Healthcare records
    "per_pci_record": 150,  # Payment card data
    "downtime_per_hour": 5000,  # Average cost per hour of downtime
    "forensic_investigation": 50000,  # Base forensic investigation cost
    "legal_fees": 75000,  # Base legal consultation
    "notification_per_person": 5,  # Cost to notify each affected person
    "credit_monitoring_per_person": 100,  # Credit monitoring services
    "pr_crisis_management": 25000,  # PR crisis management
    "regulatory_fine_base": 100000,  # Base regulatory fine
}

# Regulatory notification requirements
REGULATORY_REQUIREMENTS = {
    DataClassification.PII: [
        "GDPR: Notify authority within 72 hours",
        "CCPA: Notify affected consumers without unreasonable delay",
        "State breach notification laws may apply"
    ],
    DataClassification.PHI: [
        "HIPAA: Notify HHS within 60 days",
        "HIPAA: Notify affected individuals within 60 days",
        "If >500 records: Notify media"
    ],
    DataClassification.PCI: [
        "PCI DSS: Notify payment card brands immediately",
        "Notify acquiring bank",
        "Forensic investigation by PCI QSA may be required"
    ],
}


# =============================================================================
# INCIDENT ANALYZER
# =============================================================================

class IncidentAnalyzer:
    """Main incident analysis engine."""

    def __init__(self, incident_id: str, evidence_dir: Optional[str] = None):
        self.incident_id = incident_id
        self.evidence_dir = Path(evidence_dir) if evidence_dir else None
        self.rca: Optional[RootCauseAnalysis] = None
        self.impact: Optional[ImpactAssessment] = None
        self.remediation: Optional[RemediationPlan] = None
        self.metrics: Optional[IncidentMetrics] = None
        self.lessons_learned: List[LessonLearned] = []
        self.action_counter = 0

        # Load incident data if available
        self._load_incident_data()

    def _load_incident_data(self):
        """Load incident data from evidence directory."""
        if self.evidence_dir and self.evidence_dir.exists():
            manifest_path = self.evidence_dir / f"{self.incident_id}_evidence_manifest.json"
            if manifest_path.exists():
                with open(manifest_path, 'r') as f:
                    self.evidence_manifest = json.load(f)
            else:
                self.evidence_manifest = {}
        else:
            self.evidence_manifest = {}

    def _generate_action_id(self) -> str:
        """Generate unique action ID."""
        self.action_counter += 1
        return f"REM-{self.incident_id}-{self.action_counter:03d}"

    def perform_rca(self, attack_vector: Optional[AttackVector] = None,
                   entry_point: str = "",
                   compromise_time: str = "",
                   detection_time: str = "") -> RootCauseAnalysis:
        """Perform root cause analysis."""

        # Default values if not provided
        if not attack_vector:
            attack_vector = AttackVector.UNKNOWN

        if not compromise_time:
            compromise_time = (datetime.now() - timedelta(hours=24)).isoformat()

        if not detection_time:
            detection_time = datetime.now().isoformat()

        # Calculate dwell time
        try:
            comp_dt = datetime.fromisoformat(compromise_time.replace('Z', '+00:00'))
            det_dt = datetime.fromisoformat(detection_time.replace('Z', '+00:00'))
            dwell_time = (det_dt - comp_dt).total_seconds() / 3600
        except:
            dwell_time = 24.0  # Default assumption

        # Build RCA based on attack vector
        lateral_movement = self._infer_lateral_movement(attack_vector)
        persistence = self._infer_persistence_mechanisms(attack_vector)
        ttps = self._map_attack_ttps(attack_vector)

        self.rca = RootCauseAnalysis(
            incident_id=self.incident_id,
            attack_vector=attack_vector,
            entry_point=entry_point or self._infer_entry_point(attack_vector),
            vulnerability_exploited=self._identify_vulnerability(attack_vector),
            initial_compromise_time=compromise_time,
            detection_time=detection_time,
            dwell_time_hours=dwell_time,
            lateral_movement_path=lateral_movement,
            persistence_mechanisms=persistence,
            data_accessed=self._identify_data_accessed(),
            tools_used_by_attacker=self._identify_attacker_tools(attack_vector),
            ttps_identified=ttps,
            confidence_level=0.75  # Default confidence
        )

        return self.rca

    def _infer_entry_point(self, attack_vector: AttackVector) -> str:
        """Infer likely entry point based on attack vector."""
        entry_points = {
            AttackVector.PHISHING: "Email attachment or malicious link",
            AttackVector.VULNERABILITY_EXPLOITATION: "Unpatched public-facing service",
            AttackVector.CREDENTIAL_THEFT: "Compromised user credentials",
            AttackVector.MISCONFIGURATION: "Misconfigured cloud resource",
            AttackVector.INSIDER_THREAT: "Authorized user access",
            AttackVector.SUPPLY_CHAIN: "Third-party software or service",
            AttackVector.BRUTE_FORCE: "Authentication endpoint",
            AttackVector.SOCIAL_ENGINEERING: "Human manipulation",
        }
        return entry_points.get(attack_vector, "Unknown entry point")

    def _infer_lateral_movement(self, attack_vector: AttackVector) -> List[str]:
        """Infer lateral movement based on attack vector."""
        if attack_vector in [AttackVector.PHISHING, AttackVector.CREDENTIAL_THEFT]:
            return [
                "Initial workstation compromise",
                "Credential harvesting from memory",
                "Internal reconnaissance",
                "Pivot to file server",
                "Access to database server"
            ]
        elif attack_vector == AttackVector.VULNERABILITY_EXPLOITATION:
            return [
                "Initial server compromise",
                "Privilege escalation",
                "Network scanning",
                "Lateral movement via SMB",
                "Domain controller access"
            ]
        return ["Unknown movement pattern"]

    def _infer_persistence_mechanisms(self, attack_vector: AttackVector) -> List[str]:
        """Infer persistence mechanisms based on attack vector."""
        mechanisms = []
        if attack_vector in [AttackVector.PHISHING, AttackVector.CREDENTIAL_THEFT]:
            mechanisms = [
                "Scheduled tasks",
                "Registry run keys",
                "Web shell on compromised server"
            ]
        elif attack_vector == AttackVector.VULNERABILITY_EXPLOITATION:
            mechanisms = [
                "Backdoor user account",
                "Modified system service",
                "Cron job"
            ]
        return mechanisms or ["No persistence identified"]

    def _identify_vulnerability(self, attack_vector: AttackVector) -> Optional[str]:
        """Identify exploited vulnerability."""
        if attack_vector == AttackVector.VULNERABILITY_EXPLOITATION:
            return "CVE-XXXX-XXXX (requires specific identification)"
        return None

    def _identify_attacker_tools(self, attack_vector: AttackVector) -> List[str]:
        """Identify tools likely used by attacker."""
        tools = {
            AttackVector.PHISHING: ["Malicious macro", "Credential harvester"],
            AttackVector.VULNERABILITY_EXPLOITATION: ["Exploit framework", "Reverse shell"],
            AttackVector.CREDENTIAL_THEFT: ["Mimikatz", "Pass-the-hash tools"],
            AttackVector.BRUTE_FORCE: ["Hydra", "Medusa", "Custom script"],
        }
        return tools.get(attack_vector, ["Unknown tools"])

    def _map_attack_ttps(self, attack_vector: AttackVector) -> List[str]:
        """Map attack to MITRE ATT&CK TTPs."""
        ttps = {
            AttackVector.PHISHING: [
                "T1566 - Phishing",
                "T1204 - User Execution",
                "T1078 - Valid Accounts"
            ],
            AttackVector.CREDENTIAL_THEFT: [
                "T1003 - OS Credential Dumping",
                "T1550 - Use Alternate Authentication Material",
                "T1021 - Remote Services"
            ],
            AttackVector.VULNERABILITY_EXPLOITATION: [
                "T1190 - Exploit Public-Facing Application",
                "T1068 - Exploitation for Privilege Escalation"
            ],
        }
        return ttps.get(attack_vector, ["Unknown TTPs"])

    def _identify_data_accessed(self) -> List[str]:
        """Identify data potentially accessed during incident."""
        return [
            "User credentials database",
            "Customer PII records",
            "Financial transaction logs",
            "Internal documentation"
        ]

    def assess_impact(self, affected_systems: Optional[List[str]] = None,
                     affected_users: int = 0,
                     data_types_exposed: Optional[List[DataClassification]] = None,
                     record_counts: Optional[Dict[str, int]] = None,
                     downtime_hours: float = 0.0) -> ImpactAssessment:
        """Assess business impact of the incident."""

        # Default values
        if not affected_systems:
            affected_systems = ["Production server", "Database server"]

        if not data_types_exposed:
            data_types_exposed = [DataClassification.INTERNAL]

        if not record_counts:
            record_counts = {}

        # Build data exposure list
        data_exposure = []
        for data_type in data_types_exposed:
            count = record_counts.get(data_type.value, 0)
            exposure = DataExposure(
                data_type=data_type,
                record_count=count,
                affected_systems=affected_systems[:2],
                exposure_confirmed=True,
                exfiltration_confirmed=False
            )
            data_exposure.append(exposure)

        # Calculate financial impact
        financial_impact = self._calculate_financial_impact(
            data_exposure, downtime_hours, affected_users
        )

        # Determine regulatory implications
        regulatory = self._determine_regulatory_implications(data_types_exposed)
        notifications = self._determine_notification_requirements(data_types_exposed)

        # Calculate impact score
        impact_score = self._calculate_impact_score(
            data_exposure, affected_users, downtime_hours, len(affected_systems)
        )

        # Categorize impacts
        impact_categories = self._categorize_impacts(data_exposure, downtime_hours)

        self.impact = ImpactAssessment(
            incident_id=self.incident_id,
            affected_systems=affected_systems,
            affected_users=affected_users,
            affected_customers=affected_users // 2,  # Estimate
            data_exposure=data_exposure,
            downtime_hours=downtime_hours,
            estimated_financial_impact=financial_impact,
            regulatory_implications=regulatory,
            notification_requirements=notifications,
            impact_score=impact_score,
            impact_categories=impact_categories
        )

        return self.impact

    def _calculate_financial_impact(self, data_exposure: List[DataExposure],
                                   downtime_hours: float,
                                   affected_users: int) -> float:
        """Calculate estimated financial impact."""
        total = 0.0

        # Data breach costs
        for exposure in data_exposure:
            if exposure.data_type == DataClassification.PII:
                total += exposure.record_count * COST_FACTORS["per_pii_record"]
            elif exposure.data_type == DataClassification.PHI:
                total += exposure.record_count * COST_FACTORS["per_phi_record"]
            elif exposure.data_type == DataClassification.PCI:
                total += exposure.record_count * COST_FACTORS["per_pci_record"]

        # Downtime costs
        total += downtime_hours * COST_FACTORS["downtime_per_hour"]

        # Fixed costs
        total += COST_FACTORS["forensic_investigation"]
        total += COST_FACTORS["legal_fees"]

        # Notification costs
        if affected_users > 0:
            total += affected_users * COST_FACTORS["notification_per_person"]
            total += affected_users * COST_FACTORS["credit_monitoring_per_person"]

        return round(total, 2)

    def _determine_regulatory_implications(self,
                                          data_types: List[DataClassification]) -> List[str]:
        """Determine regulatory implications based on data types."""
        implications = []
        for data_type in data_types:
            if data_type in REGULATORY_REQUIREMENTS:
                implications.extend(REGULATORY_REQUIREMENTS[data_type])
        return list(set(implications))

    def _determine_notification_requirements(self,
                                            data_types: List[DataClassification]) -> List[str]:
        """Determine notification requirements."""
        requirements = []
        for data_type in data_types:
            if data_type == DataClassification.PII:
                requirements.append("Notify affected individuals")
                requirements.append("Notify state attorney general (if required by state law)")
            if data_type == DataClassification.PHI:
                requirements.append("Notify HHS")
                requirements.append("Notify affected individuals")
            if data_type == DataClassification.PCI:
                requirements.append("Notify payment card brands")
                requirements.append("Notify acquiring bank")
        return list(set(requirements))

    def _calculate_impact_score(self, data_exposure: List[DataExposure],
                               affected_users: int,
                               downtime_hours: float,
                               affected_systems: int) -> float:
        """Calculate overall impact score (0-10)."""
        score = 0.0

        # Data sensitivity (0-4 points)
        for exposure in data_exposure:
            if exposure.data_type in [DataClassification.PHI, DataClassification.PCI]:
                score += 2
            elif exposure.data_type in [DataClassification.PII, DataClassification.RESTRICTED]:
                score += 1.5
            elif exposure.data_type == DataClassification.CONFIDENTIAL:
                score += 1

        # Affected users (0-2 points)
        if affected_users > 10000:
            score += 2
        elif affected_users > 1000:
            score += 1.5
        elif affected_users > 100:
            score += 1

        # Downtime (0-2 points)
        if downtime_hours > 24:
            score += 2
        elif downtime_hours > 8:
            score += 1.5
        elif downtime_hours > 4:
            score += 1

        # Systems affected (0-2 points)
        if affected_systems > 10:
            score += 2
        elif affected_systems > 5:
            score += 1

        return min(round(score, 1), 10.0)

    def _categorize_impacts(self, data_exposure: List[DataExposure],
                           downtime_hours: float) -> Dict[str, str]:
        """Categorize impacts by area."""
        categories = {}

        # Data confidentiality
        sensitive_exposure = any(
            e.data_type in [DataClassification.PII, DataClassification.PHI, DataClassification.PCI]
            for e in data_exposure
        )
        categories["data_confidentiality"] = "high" if sensitive_exposure else "low"

        # System availability
        if downtime_hours > 8:
            categories["system_availability"] = "high"
        elif downtime_hours > 2:
            categories["system_availability"] = "medium"
        else:
            categories["system_availability"] = "low"

        # Regulatory
        regulated_data = any(
            e.data_type in REGULATORY_REQUIREMENTS for e in data_exposure
        )
        categories["regulatory"] = "high" if regulated_data else "low"

        return categories

    def generate_remediation_plan(self) -> RemediationPlan:
        """Generate remediation plan based on RCA and impact assessment."""

        plan = RemediationPlan(incident_id=self.incident_id)

        # Immediate actions (24 hours)
        immediate = [
            RemediationAction(
                action_id=self._generate_action_id(),
                description="Reset all compromised credentials",
                priority=RemediationPriority.IMMEDIATE,
                owner="Identity Team",
                effort_hours=4
            ),
            RemediationAction(
                action_id=self._generate_action_id(),
                description="Patch exploited vulnerability (if applicable)",
                priority=RemediationPriority.IMMEDIATE,
                owner="Security Team",
                effort_hours=8
            ),
            RemediationAction(
                action_id=self._generate_action_id(),
                description="Verify backup integrity and availability",
                priority=RemediationPriority.IMMEDIATE,
                owner="Infrastructure Team",
                effort_hours=4
            ),
        ]
        plan.immediate_actions = immediate

        # Short-term fixes (30 days)
        short_term = [
            RemediationAction(
                action_id=self._generate_action_id(),
                description="Implement enhanced monitoring for affected systems",
                priority=RemediationPriority.SHORT_TERM,
                owner="SOC Team",
                effort_hours=16
            ),
            RemediationAction(
                action_id=self._generate_action_id(),
                description="Conduct security awareness training for affected users",
                priority=RemediationPriority.SHORT_TERM,
                owner="Security Team",
                effort_hours=8
            ),
            RemediationAction(
                action_id=self._generate_action_id(),
                description="Review and update access controls",
                priority=RemediationPriority.SHORT_TERM,
                owner="Identity Team",
                effort_hours=24
            ),
        ]
        plan.short_term_fixes = short_term

        # Medium-term improvements (90 days)
        medium_term = [
            RemediationAction(
                action_id=self._generate_action_id(),
                description="Implement additional network segmentation",
                priority=RemediationPriority.MEDIUM_TERM,
                owner="Network Team",
                effort_hours=40
            ),
            RemediationAction(
                action_id=self._generate_action_id(),
                description="Deploy EDR solution on all endpoints",
                priority=RemediationPriority.MEDIUM_TERM,
                owner="Security Team",
                effort_hours=80
            ),
        ]
        plan.medium_term_improvements = medium_term

        # Long-term initiatives (12 months)
        long_term = [
            RemediationAction(
                action_id=self._generate_action_id(),
                description="Implement zero trust architecture",
                priority=RemediationPriority.LONG_TERM,
                owner="Architecture Team",
                effort_hours=400
            ),
        ]
        plan.long_term_initiatives = long_term

        # Preventive controls
        plan.preventive_controls = [
            "Implement MFA for all users",
            "Deploy email security gateway",
            "Enable least privilege access model",
            "Implement DLP controls"
        ]

        # Detection improvements
        plan.detection_improvements = [
            "Add detection rules for identified TTPs",
            "Implement user behavior analytics",
            "Enhance logging coverage",
            "Deploy deception technologies"
        ]

        # Calculate total effort
        all_actions = (
            plan.immediate_actions +
            plan.short_term_fixes +
            plan.medium_term_improvements +
            plan.long_term_initiatives
        )
        plan.total_effort_hours = sum(a.effort_hours for a in all_actions)

        self.remediation = plan
        return plan

    def calculate_metrics(self, detection_time: str = "",
                         containment_time: str = "",
                         eradication_time: str = "",
                         recovery_time: str = "") -> IncidentMetrics:
        """Calculate incident response metrics."""

        now = datetime.now()
        metrics = IncidentMetrics(incident_id=self.incident_id)

        # Use RCA data if available
        if self.rca:
            # MTTD = Time from compromise to detection
            if self.rca.initial_compromise_time and self.rca.detection_time:
                try:
                    comp = datetime.fromisoformat(self.rca.initial_compromise_time.replace('Z', '+00:00'))
                    det = datetime.fromisoformat(self.rca.detection_time.replace('Z', '+00:00'))
                    metrics.mttd_hours = (det - comp).total_seconds() / 3600
                except:
                    metrics.mttd_hours = self.rca.dwell_time_hours

        # MTTR = Time from detection to containment
        if detection_time and containment_time:
            try:
                det = datetime.fromisoformat(detection_time.replace('Z', '+00:00'))
                cont = datetime.fromisoformat(containment_time.replace('Z', '+00:00'))
                metrics.mttr_hours = (cont - det).total_seconds() / 3600
                metrics.mttc_hours = metrics.mttr_hours
            except:
                pass

        # MTTE = Time from containment to eradication
        if containment_time and eradication_time:
            try:
                cont = datetime.fromisoformat(containment_time.replace('Z', '+00:00'))
                erad = datetime.fromisoformat(eradication_time.replace('Z', '+00:00'))
                metrics.mtte_hours = (erad - cont).total_seconds() / 3600
            except:
                pass

        # MTTRec = Time from eradication to recovery
        if eradication_time and recovery_time:
            try:
                erad = datetime.fromisoformat(eradication_time.replace('Z', '+00:00'))
                rec = datetime.fromisoformat(recovery_time.replace('Z', '+00:00'))
                metrics.mttrec_hours = (rec - erad).total_seconds() / 3600
            except:
                pass

        # Effectiveness scores (would be calculated from actual data)
        metrics.containment_effectiveness = 95.0
        metrics.evidence_completeness = 85.0
        metrics.communication_timeliness = 90.0

        self.metrics = metrics
        return metrics

    def generate_lessons_learned(self) -> List[LessonLearned]:
        """Generate lessons learned from the incident."""
        lessons = []

        # Based on attack vector
        if self.rca:
            if self.rca.attack_vector == AttackVector.PHISHING:
                lessons.append(LessonLearned(
                    category="Prevention",
                    observation="Phishing email bypassed existing email filters",
                    recommendation="Implement AI-based email filtering with link rewriting",
                    priority="high"
                ))
                lessons.append(LessonLearned(
                    category="Training",
                    observation="User clicked on malicious link",
                    recommendation="Increase frequency of phishing simulations and training",
                    priority="medium"
                ))

        # Based on detection
        if self.metrics and self.metrics.mttd_hours > 24:
            lessons.append(LessonLearned(
                category="Detection",
                observation=f"Dwell time was {self.metrics.mttd_hours:.1f} hours before detection",
                recommendation="Implement enhanced detection rules for initial access techniques",
                priority="high"
            ))

        # Based on impact
        if self.impact:
            if self.impact.impact_score > 7:
                lessons.append(LessonLearned(
                    category="Response",
                    observation="High impact incident with significant data exposure",
                    recommendation="Conduct tabletop exercises quarterly for high-impact scenarios",
                    priority="high"
                ))

        # Standard lessons
        lessons.extend([
            LessonLearned(
                category="Process",
                observation="Incident response plan was effective but could be improved",
                recommendation="Update runbooks with specific steps identified during response",
                priority="medium"
            ),
            LessonLearned(
                category="Communication",
                observation="Stakeholder communication could be more streamlined",
                recommendation="Pre-define communication templates and escalation paths",
                priority="medium"
            ),
        ])

        self.lessons_learned = lessons
        return lessons

    def generate_report(self, format: str = "markdown") -> str:
        """Generate comprehensive incident report."""

        # Ensure all analyses are complete
        if not self.rca:
            self.perform_rca()
        if not self.impact:
            self.assess_impact()
        if not self.remediation:
            self.generate_remediation_plan()
        if not self.metrics:
            self.calculate_metrics()
        if not self.lessons_learned:
            self.generate_lessons_learned()

        if format == "markdown":
            return self._generate_markdown_report()
        elif format == "html":
            return self._generate_html_report()
        else:
            return self._generate_text_report()

    def _generate_markdown_report(self) -> str:
        """Generate markdown format report."""
        lines = []

        lines.append(f"# Incident Report: {self.incident_id}")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Executive Summary
        lines.append("## Executive Summary")
        lines.append("")
        if self.rca:
            lines.append(f"On {self.rca.initial_compromise_time[:10]}, a security incident was detected involving "
                        f"**{self.rca.attack_vector.value}** attack. The initial entry point was: "
                        f"*{self.rca.entry_point}*.")
            lines.append("")
            lines.append(f"The attacker maintained access for approximately **{self.rca.dwell_time_hours:.1f} hours** "
                        f"before detection.")
        if self.impact:
            lines.append("")
            lines.append(f"**Impact Assessment:**")
            lines.append(f"- Affected Systems: {len(self.impact.affected_systems)}")
            lines.append(f"- Affected Users: {self.impact.affected_users}")
            lines.append(f"- Impact Score: {self.impact.impact_score}/10")
            lines.append(f"- Estimated Financial Impact: ${self.impact.estimated_financial_impact:,.2f}")
        lines.append("")

        # Incident Details
        lines.append("## Incident Details")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.append(f"| Incident ID | {self.incident_id} |")
        if self.rca:
            lines.append(f"| Attack Vector | {self.rca.attack_vector.value} |")
            lines.append(f"| Entry Point | {self.rca.entry_point} |")
            lines.append(f"| Initial Compromise | {self.rca.initial_compromise_time} |")
            lines.append(f"| Detection Time | {self.rca.detection_time} |")
            lines.append(f"| Dwell Time | {self.rca.dwell_time_hours:.1f} hours |")
        lines.append("")

        # Root Cause Analysis
        lines.append("## Root Cause Analysis")
        lines.append("")
        if self.rca:
            lines.append("### Attack Path")
            lines.append("")
            for i, step in enumerate(self.rca.lateral_movement_path, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

            lines.append("### MITRE ATT&CK TTPs")
            lines.append("")
            for ttp in self.rca.ttps_identified:
                lines.append(f"- {ttp}")
            lines.append("")

        # Impact Assessment
        lines.append("## Impact Assessment")
        lines.append("")
        if self.impact:
            lines.append("### Affected Systems")
            lines.append("")
            for system in self.impact.affected_systems:
                lines.append(f"- {system}")
            lines.append("")

            if self.impact.data_exposure:
                lines.append("### Data Exposure")
                lines.append("")
                lines.append("| Data Type | Records | Exfiltration Confirmed |")
                lines.append("|-----------|---------|------------------------|")
                for exp in self.impact.data_exposure:
                    lines.append(f"| {exp.data_type.value} | {exp.record_count:,} | {exp.exfiltration_confirmed} |")
                lines.append("")

            if self.impact.regulatory_implications:
                lines.append("### Regulatory Implications")
                lines.append("")
                for reg in self.impact.regulatory_implications:
                    lines.append(f"- {reg}")
                lines.append("")

        # Metrics
        lines.append("## Response Metrics")
        lines.append("")
        if self.metrics:
            lines.append("| Metric | Value |")
            lines.append("|--------|-------|")
            lines.append(f"| Mean Time to Detect (MTTD) | {self.metrics.mttd_hours:.1f} hours |")
            lines.append(f"| Mean Time to Respond (MTTR) | {self.metrics.mttr_hours:.1f} hours |")
            lines.append(f"| Containment Effectiveness | {self.metrics.containment_effectiveness}% |")
        lines.append("")

        # Remediation Plan
        lines.append("## Remediation Plan")
        lines.append("")
        if self.remediation:
            lines.append("### Immediate Actions (24 hours)")
            lines.append("")
            for action in self.remediation.immediate_actions:
                lines.append(f"- [ ] {action.description} ({action.owner})")
            lines.append("")

            lines.append("### Short-Term Fixes (30 days)")
            lines.append("")
            for action in self.remediation.short_term_fixes:
                lines.append(f"- [ ] {action.description} ({action.owner})")
            lines.append("")

            lines.append(f"**Total Estimated Effort:** {self.remediation.total_effort_hours} hours")
            lines.append("")

        # Lessons Learned
        lines.append("## Lessons Learned")
        lines.append("")
        if self.lessons_learned:
            lines.append("| Category | Observation | Recommendation | Priority |")
            lines.append("|----------|-------------|----------------|----------|")
            for lesson in self.lessons_learned:
                lines.append(f"| {lesson.category} | {lesson.observation[:50]}... | {lesson.recommendation[:50]}... | {lesson.priority} |")
        lines.append("")

        # Footer
        lines.append("---")
        lines.append(f"*Report generated by incident_analyzer.py v{__version__}*")

        return "\n".join(lines)

    def _generate_html_report(self) -> str:
        """Generate HTML format report."""
        md_report = self._generate_markdown_report()
        # Simple HTML wrapper - in production would use proper HTML generation
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Incident Report: {self.incident_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; border-bottom: 1px solid #ccc; }}
        pre {{ background-color: #f5f5f5; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
<pre>{md_report}</pre>
</body>
</html>"""

    def _generate_text_report(self) -> str:
        """Generate plain text report."""
        # Use markdown report and strip markdown syntax
        md = self._generate_markdown_report()
        # Simple cleanup
        text = md.replace('# ', '').replace('## ', '').replace('### ', '')
        text = text.replace('**', '').replace('*', '').replace('`', '')
        return text

    def run(self, perform_rca: bool = False,
           assess_impact: bool = False,
           generate_report: bool = False,
           attack_vector: Optional[str] = None,
           output_format: str = "text") -> Dict:
        """Run the incident analysis workflow."""

        results = {
            "status": "completed",
            "incident_id": self.incident_id,
            "timestamp": datetime.now().isoformat()
        }

        # Perform RCA if requested
        if perform_rca:
            av = AttackVector(attack_vector) if attack_vector else None
            rca = self.perform_rca(attack_vector=av)
            results["root_cause_analysis"] = rca.to_dict()

        # Assess impact if requested
        if assess_impact:
            impact = self.assess_impact()
            results["impact_assessment"] = impact.to_dict()

        # Generate metrics
        metrics = self.calculate_metrics()
        results["metrics"] = metrics.to_dict()

        # Generate full report if requested
        if generate_report:
            self.generate_remediation_plan()
            self.generate_lessons_learned()
            report = self.generate_report(format=output_format)
            results["report"] = report
            results["lessons_learned"] = [l.to_dict() for l in self.lessons_learned]
            results["remediation_plan"] = self.remediation.to_dict() if self.remediation else None

        return results


# =============================================================================
# OUTPUT FORMATTERS
# =============================================================================

def format_text_output(results: Dict) -> str:
    """Format results as human-readable text."""
    lines = []
    lines.append("=" * 70)
    lines.append("INCIDENT ANALYSIS REPORT")
    lines.append("=" * 70)
    lines.append(f"Incident ID: {results['incident_id']}")
    lines.append(f"Timestamp: {results['timestamp']}")
    lines.append("")

    # RCA Summary
    if 'root_cause_analysis' in results:
        rca = results['root_cause_analysis']
        lines.append("ROOT CAUSE ANALYSIS")
        lines.append("-" * 40)
        lines.append(f"  Attack Vector:     {rca['attack_vector']}")
        lines.append(f"  Entry Point:       {rca['entry_point']}")
        lines.append(f"  Dwell Time:        {rca['dwell_time_hours']:.1f} hours")
        lines.append(f"  Confidence:        {rca['confidence_level']*100:.0f}%")
        lines.append("")

    # Impact Summary
    if 'impact_assessment' in results:
        impact = results['impact_assessment']
        lines.append("IMPACT ASSESSMENT")
        lines.append("-" * 40)
        lines.append(f"  Systems Affected:  {len(impact['affected_systems'])}")
        lines.append(f"  Users Affected:    {impact['affected_users']}")
        lines.append(f"  Downtime:          {impact['downtime_hours']} hours")
        lines.append(f"  Financial Impact:  ${impact['estimated_financial_impact']:,.2f}")
        lines.append(f"  Impact Score:      {impact['impact_score']}/10")
        lines.append("")

    # Metrics
    if 'metrics' in results:
        metrics = results['metrics']
        lines.append("RESPONSE METRICS")
        lines.append("-" * 40)
        lines.append(f"  MTTD:              {metrics['mttd_hours']:.1f} hours")
        lines.append(f"  MTTR:              {metrics['mttr_hours']:.1f} hours")
        lines.append(f"  Containment:       {metrics['containment_effectiveness']}%")
        lines.append("")

    # Report
    if 'report' in results:
        lines.append("FULL REPORT")
        lines.append("-" * 40)
        lines.append(results['report'])

    lines.append("=" * 70)

    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='incident_analyzer',
        description="""
Incident Analyzer - Root Cause Analysis and Impact Assessment

Root cause analysis, impact assessment, and post-incident report generation
for security incident response.

Features:
  - Attack vector and entry point identification
  - Dwell time calculation and lateral movement mapping
  - Business impact quantification
  - MTTD/MTTR metrics calculation
  - Markdown and HTML report generation

Examples:
  %(prog)s --incident INC-001 --rca
  %(prog)s --incident INC-001 --impact
  %(prog)s --incident INC-001 --report --output markdown
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--incident', '-i',
        required=True,
        help='Incident identifier'
    )

    parser.add_argument(
        '--evidence-dir', '-e',
        help='Path to evidence directory'
    )

    parser.add_argument(
        '--rca',
        action='store_true',
        help='Perform root cause analysis'
    )

    parser.add_argument(
        '--attack-vector', '-a',
        choices=[av.value for av in AttackVector],
        help='Known attack vector (for RCA)'
    )

    parser.add_argument(
        '--impact',
        action='store_true',
        help='Perform impact assessment'
    )

    parser.add_argument(
        '--report', '-r',
        action='store_true',
        help='Generate full incident report'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'markdown', 'html'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Initialize analyzer
    analyzer = IncidentAnalyzer(
        incident_id=args.incident,
        evidence_dir=args.evidence_dir
    )

    if args.verbose:
        print(f"Analyzing incident: {args.incident}", file=sys.stderr)

    # Determine report format for markdown/html
    report_format = "markdown" if args.output == "markdown" else args.output

    # Run analysis
    results = analyzer.run(
        perform_rca=args.rca or args.report,
        assess_impact=args.impact or args.report,
        generate_report=args.report,
        attack_vector=args.attack_vector,
        output_format=report_format
    )

    # Format output
    if args.output == 'json':
        output = json.dumps(results, indent=2)
    elif args.output in ['markdown', 'html'] and 'report' in results:
        output = results['report']
    else:
        output = format_text_output(results)

    # Write output
    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        if args.verbose:
            print(f"Results written to: {args.file}", file=sys.stderr)
    else:
        print(output)

    sys.exit(0)


if __name__ == '__main__':
    main()
