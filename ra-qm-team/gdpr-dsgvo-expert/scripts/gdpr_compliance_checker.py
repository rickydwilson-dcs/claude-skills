#!/usr/bin/env python3
"""
GDPR/DSGVO Compliance Checker
Comprehensive assessment of data processing activities against GDPR requirements.

This script analyzes data processing inventories and controls to assess GDPR
compliance across key areas: lawful basis, data subject rights, DPIAs, breach
readiness, and data protection by design. Generates risk-based assessments with
compliance scores and identifies high-risk gaps requiring immediate attention.

Usage:
    python gdpr_compliance_checker.py processing_inventory.json
    python gdpr_compliance_checker.py data.json --output json
    python gdpr_compliance_checker.py data.json -o csv -f compliance_report.csv
    python gdpr_compliance_checker.py data.json -o json --verbose

Author: GDPR/DSGVO Expert Team
Version: 1.0.0
Last Updated: 2025-11-05
"""

import argparse
import json
import sys
import csv
from io import StringIO
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime


class LawfulBasis(Enum):
    """Article 6 GDPR lawful basis for processing"""
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    VITAL_INTERESTS = "vital_interests"
    PUBLIC_TASK = "public_task"
    LEGITIMATE_INTERESTS = "legitimate_interests"
    NOT_SPECIFIED = "not_specified"


class DataCategory(Enum):
    """Data categories including special category data (Article 9)"""
    BASIC_PERSONAL = "basic_personal"  # Name, address, email
    IDENTIFICATION = "identification"  # ID numbers, biometric
    FINANCIAL = "financial"
    HEALTH = "health"  # Special category
    GENETIC = "genetic"  # Special category
    BIOMETRIC = "biometric"  # Special category
    RACIAL_ETHNIC = "racial_ethnic"  # Special category
    POLITICAL = "political"  # Special category
    RELIGIOUS = "religious"  # Special category
    TRADE_UNION = "trade_union"  # Special category
    SEX_LIFE = "sex_life"  # Special category
    CRIMINAL = "criminal"  # Article 10


class RiskLevel(Enum):
    """Risk levels for GDPR compliance assessment"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DataSubjectRights:
    """Implementation status of data subject rights (Articles 12-23)"""
    right_to_access: bool = False  # Article 15
    right_to_rectification: bool = False  # Article 16
    right_to_erasure: bool = False  # Article 17
    right_to_restriction: bool = False  # Article 18
    right_to_portability: bool = False  # Article 20
    right_to_object: bool = False  # Article 21
    automated_decision_making_safeguards: bool = False  # Article 22

    def compliance_score(self) -> float:
        """Calculate compliance score for data subject rights"""
        implemented = sum([
            self.right_to_access,
            self.right_to_rectification,
            self.right_to_erasure,
            self.right_to_restriction,
            self.right_to_portability,
            self.right_to_object,
            self.automated_decision_making_safeguards
        ])
        return (implemented / 7) * 100


@dataclass
class TechnicalOrganizationalMeasures:
    """Technical and organizational measures (Articles 25, 32)"""
    pseudonymization: bool = False
    encryption: bool = False
    access_controls: bool = False
    data_minimization: bool = False
    regular_testing: bool = False
    incident_response_plan: bool = False
    staff_training: bool = False

    def compliance_score(self) -> float:
        """Calculate compliance score for technical/organizational measures"""
        implemented = sum([
            self.pseudonymization,
            self.encryption,
            self.access_controls,
            self.data_minimization,
            self.regular_testing,
            self.incident_response_plan,
            self.staff_training
        ])
        return (implemented / 7) * 100


@dataclass
class InternationalTransfer:
    """International data transfer details (Chapter V)"""
    has_transfers: bool = False
    transfer_mechanism: str = ""  # adequacy, SCC, BCR, derogation
    countries: List[str] = field(default_factory=list)
    transfer_assessment_completed: bool = False
    supplementary_measures: bool = False


@dataclass
class ProcessingActivity:
    """Data processing activity with GDPR compliance details"""
    activity_id: str
    activity_name: str
    purpose: str
    data_categories: List[DataCategory]
    lawful_basis: LawfulBasis
    data_subjects: str  # customers, employees, patients, etc.
    retention_period: str

    # Compliance elements
    has_privacy_notice: bool = False
    records_of_processing: bool = False  # Article 30
    dpia_required: bool = False
    dpia_completed: bool = False
    data_subject_rights: DataSubjectRights = field(default_factory=DataSubjectRights)
    technical_measures: TechnicalOrganizationalMeasures = field(default_factory=TechnicalOrganizationalMeasures)
    international_transfer: InternationalTransfer = field(default_factory=InternationalTransfer)

    # Breach preparedness
    breach_notification_procedures: bool = False
    breach_response_tested: bool = False

    # Additional context
    data_processors: List[str] = field(default_factory=list)
    processor_agreements: bool = False
    last_review_date: Optional[str] = None
    notes: str = ""


class GDPRComplianceChecker:
    """GDPR compliance assessment engine"""

    def __init__(self, data: Dict[str, Any]):
        self.processing_activities: List[ProcessingActivity] = []
        self.load_processing_activities(data)
        self.assessment_results: Dict[str, Any] = {}

    def load_processing_activities(self, data: Dict[str, Any]) -> None:
        """Load and validate processing activities from input data"""
        activities_data = data.get('processing_activities', [])

        for activity_data in activities_data:
            try:
                # Convert enum strings to enum values
                if 'data_categories' in activity_data:
                    activity_data['data_categories'] = [
                        DataCategory(cat) for cat in activity_data['data_categories']
                    ]

                if 'lawful_basis' in activity_data:
                    activity_data['lawful_basis'] = LawfulBasis(activity_data['lawful_basis'])

                # Convert nested dictionaries to dataclass instances
                if 'data_subject_rights' in activity_data:
                    activity_data['data_subject_rights'] = DataSubjectRights(
                        **activity_data['data_subject_rights']
                    )

                if 'technical_measures' in activity_data:
                    activity_data['technical_measures'] = TechnicalOrganizationalMeasures(
                        **activity_data['technical_measures']
                    )

                if 'international_transfer' in activity_data:
                    activity_data['international_transfer'] = InternationalTransfer(
                        **activity_data['international_transfer']
                    )

                activity = ProcessingActivity(**activity_data)
                self.processing_activities.append(activity)

            except (TypeError, ValueError) as e:
                print(f"Warning: Skipping invalid activity: {e}", file=sys.stderr)

    def assess_lawful_basis(self, activity: ProcessingActivity) -> Dict[str, Any]:
        """Assess lawful basis compliance (Article 6)"""
        issues = []
        risk = RiskLevel.LOW

        # Risk priority mapping for comparisons
        risk_priority = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }

        if activity.lawful_basis == LawfulBasis.NOT_SPECIFIED:
            issues.append("No lawful basis specified - CRITICAL")
            risk = RiskLevel.CRITICAL

        # Check special category data (Article 9)
        special_categories = [
            DataCategory.HEALTH, DataCategory.GENETIC, DataCategory.BIOMETRIC,
            DataCategory.RACIAL_ETHNIC, DataCategory.POLITICAL, DataCategory.RELIGIOUS,
            DataCategory.TRADE_UNION, DataCategory.SEX_LIFE
        ]

        has_special_data = any(cat in special_categories for cat in activity.data_categories)

        if has_special_data:
            if activity.lawful_basis == LawfulBasis.LEGITIMATE_INTERESTS:
                issues.append("Legitimate interests cannot be used for special category data")
                risk = RiskLevel.CRITICAL
            elif activity.lawful_basis != LawfulBasis.CONSENT:
                issues.append("Special category data requires explicit consent or specific Article 9 condition")
                if risk_priority[risk.value] < risk_priority[RiskLevel.HIGH.value]:
                    risk = RiskLevel.HIGH

        # Check criminal conviction data (Article 10)
        if DataCategory.CRIMINAL in activity.data_categories:
            issues.append("Criminal conviction data requires official authority or specific law")
            if risk_priority[risk.value] < risk_priority[RiskLevel.HIGH.value]:
                risk = RiskLevel.HIGH

        # Check consent management
        if activity.lawful_basis == LawfulBasis.CONSENT and not activity.has_privacy_notice:
            issues.append("Consent requires clear privacy notice")
            if risk_priority[risk.value] < risk_priority[RiskLevel.MEDIUM.value]:
                risk = RiskLevel.MEDIUM

        compliant = len(issues) == 0 and activity.lawful_basis != LawfulBasis.NOT_SPECIFIED

        return {
            "compliant": compliant,
            "risk_level": risk.value,
            "lawful_basis": activity.lawful_basis.value,
            "has_special_category_data": has_special_data,
            "issues": issues
        }

    def assess_data_subject_rights(self, activity: ProcessingActivity) -> Dict[str, Any]:
        """Assess data subject rights implementation (Articles 12-23)"""
        rights = activity.data_subject_rights
        score = rights.compliance_score()
        issues = []

        if not rights.right_to_access:
            issues.append("Right to access (Art. 15) not implemented")
        if not rights.right_to_rectification:
            issues.append("Right to rectification (Art. 16) not implemented")
        if not rights.right_to_erasure:
            issues.append("Right to erasure (Art. 17) not implemented")
        if not rights.right_to_restriction:
            issues.append("Right to restriction (Art. 18) not implemented")
        if not rights.right_to_portability:
            issues.append("Right to portability (Art. 20) not implemented")
        if not rights.right_to_object:
            issues.append("Right to object (Art. 21) not implemented")

        # Determine risk level
        if score < 40:
            risk = RiskLevel.CRITICAL
        elif score < 60:
            risk = RiskLevel.HIGH
        elif score < 80:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.LOW

        return {
            "compliance_score": round(score, 1),
            "risk_level": risk.value,
            "issues": issues,
            "implemented_rights": {
                "access": rights.right_to_access,
                "rectification": rights.right_to_rectification,
                "erasure": rights.right_to_erasure,
                "restriction": rights.right_to_restriction,
                "portability": rights.right_to_portability,
                "object": rights.right_to_object,
                "automated_decision_safeguards": rights.automated_decision_making_safeguards
            }
        }

    def assess_dpia_requirement(self, activity: ProcessingActivity) -> Dict[str, Any]:
        """Assess DPIA requirement and completion (Article 35)"""
        issues = []
        risk = RiskLevel.LOW

        # DPIA triggers (Article 35.3)
        dpia_triggers = []

        # Systematic and extensive automated processing
        if activity.data_subject_rights.automated_decision_making_safeguards:
            dpia_triggers.append("Automated decision-making with legal/significant effects")

        # Large-scale processing of special categories
        special_categories = [
            DataCategory.HEALTH, DataCategory.GENETIC, DataCategory.BIOMETRIC,
            DataCategory.RACIAL_ETHNIC, DataCategory.POLITICAL, DataCategory.RELIGIOUS,
            DataCategory.TRADE_UNION, DataCategory.SEX_LIFE
        ]
        has_special = any(cat in special_categories for cat in activity.data_categories)

        if has_special:
            dpia_triggers.append("Processing special category data")

        # Systematic monitoring
        if "monitoring" in activity.purpose.lower() or "tracking" in activity.purpose.lower():
            dpia_triggers.append("Systematic monitoring of publicly accessible areas")

        dpia_required = len(dpia_triggers) > 0 or activity.dpia_required

        if dpia_required and not activity.dpia_completed:
            issues.append("DPIA required but not completed")
            risk = RiskLevel.HIGH

        if not dpia_required and activity.dpia_completed:
            issues.append("DPIA completed (good practice even if not required)")

        return {
            "dpia_required": dpia_required,
            "dpia_completed": activity.dpia_completed,
            "compliant": not dpia_required or activity.dpia_completed,
            "risk_level": risk.value,
            "triggers": dpia_triggers,
            "issues": issues
        }

    def assess_breach_readiness(self, activity: ProcessingActivity) -> Dict[str, Any]:
        """Assess breach notification preparedness (Articles 33-34)"""
        issues = []

        if not activity.breach_notification_procedures:
            issues.append("No breach notification procedures documented")

        if not activity.breach_response_tested:
            issues.append("Breach response procedures not tested")

        # High-risk activities need robust breach preparedness
        special_categories = [DataCategory.HEALTH, DataCategory.GENETIC, DataCategory.BIOMETRIC]
        has_high_risk_data = any(cat in special_categories for cat in activity.data_categories)

        score = sum([
            activity.breach_notification_procedures,
            activity.breach_response_tested
        ]) / 2 * 100

        if has_high_risk_data and score < 100:
            risk = RiskLevel.HIGH
        elif score < 50:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.LOW

        return {
            "compliance_score": round(score, 1),
            "risk_level": risk.value,
            "procedures_documented": activity.breach_notification_procedures,
            "procedures_tested": activity.breach_response_tested,
            "issues": issues
        }

    def assess_technical_measures(self, activity: ProcessingActivity) -> Dict[str, Any]:
        """Assess data protection by design and default (Articles 25, 32)"""
        measures = activity.technical_measures
        score = measures.compliance_score()
        issues = []

        # Critical measures
        if not measures.encryption:
            issues.append("Encryption not implemented for data at rest/in transit")
        if not measures.access_controls:
            issues.append("Access controls not implemented")

        # Important measures
        if not measures.pseudonymization:
            issues.append("Pseudonymization not implemented (recommended)")
        if not measures.data_minimization:
            issues.append("Data minimization principles not documented")
        if not measures.regular_testing:
            issues.append("Regular security testing not performed")
        if not measures.incident_response_plan:
            issues.append("No incident response plan")
        if not measures.staff_training:
            issues.append("Staff training on data protection not conducted")

        # Risk assessment
        if score < 50:
            risk = RiskLevel.CRITICAL
        elif score < 70:
            risk = RiskLevel.HIGH
        elif score < 85:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.LOW

        return {
            "compliance_score": round(score, 1),
            "risk_level": risk.value,
            "issues": issues,
            "implemented_measures": {
                "pseudonymization": measures.pseudonymization,
                "encryption": measures.encryption,
                "access_controls": measures.access_controls,
                "data_minimization": measures.data_minimization,
                "regular_testing": measures.regular_testing,
                "incident_response": measures.incident_response_plan,
                "staff_training": measures.staff_training
            }
        }

    def assess_international_transfers(self, activity: ProcessingActivity) -> Dict[str, Any]:
        """Assess international data transfer compliance (Chapter V)"""
        transfer = activity.international_transfer
        issues = []
        risk = RiskLevel.LOW

        if not transfer.has_transfers:
            return {
                "has_transfers": False,
                "compliant": True,
                "risk_level": risk.value,
                "issues": []
            }

        if not transfer.transfer_mechanism:
            issues.append("International transfers without documented mechanism")
            risk = RiskLevel.CRITICAL
        elif transfer.transfer_mechanism not in ["adequacy", "SCC", "BCR", "derogation"]:
            issues.append(f"Invalid transfer mechanism: {transfer.transfer_mechanism}")
            risk = RiskLevel.HIGH

        if not transfer.transfer_assessment_completed:
            issues.append("Transfer risk assessment not completed (post-Schrems II requirement)")
            risk_priority = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            if risk_priority[risk.value] < risk_priority[RiskLevel.HIGH.value]:
                risk = RiskLevel.HIGH

        if transfer.transfer_mechanism == "SCC" and not transfer.supplementary_measures:
            issues.append("SCCs may require supplementary measures (case-by-case assessment)")
            risk_priority = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            if risk_priority[risk.value] < risk_priority[RiskLevel.MEDIUM.value]:
                risk = RiskLevel.MEDIUM

        return {
            "has_transfers": True,
            "compliant": len(issues) == 0,
            "risk_level": risk.value,
            "transfer_mechanism": transfer.transfer_mechanism,
            "countries": transfer.countries,
            "assessment_completed": transfer.transfer_assessment_completed,
            "supplementary_measures": transfer.supplementary_measures,
            "issues": issues
        }

    def assess_documentation_gaps(self, activity: ProcessingActivity) -> Dict[str, Any]:
        """Assess documentation and accountability gaps"""
        issues = []

        if not activity.has_privacy_notice:
            issues.append("Privacy notice missing (Art. 13-14)")
        if not activity.records_of_processing:
            issues.append("Records of processing activities missing (Art. 30)")
        if activity.data_processors and not activity.processor_agreements:
            issues.append("Processor agreements missing (Art. 28)")
        if not activity.last_review_date:
            issues.append("No documented review date for processing activity")

        gaps = len(issues)

        if gaps >= 3:
            risk = RiskLevel.HIGH
        elif gaps >= 2:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.LOW

        return {
            "documentation_gaps": gaps,
            "risk_level": risk.value,
            "issues": issues,
            "has_privacy_notice": activity.has_privacy_notice,
            "has_records_of_processing": activity.records_of_processing,
            "has_processor_agreements": activity.processor_agreements,
            "last_review_date": activity.last_review_date
        }

    def assess_activity(self, activity: ProcessingActivity) -> Dict[str, Any]:
        """Comprehensive assessment of single processing activity"""
        assessment = {
            "activity_id": activity.activity_id,
            "activity_name": activity.activity_name,
            "purpose": activity.purpose,
            "data_subjects": activity.data_subjects,
            "assessments": {
                "lawful_basis": self.assess_lawful_basis(activity),
                "data_subject_rights": self.assess_data_subject_rights(activity),
                "dpia": self.assess_dpia_requirement(activity),
                "breach_readiness": self.assess_breach_readiness(activity),
                "technical_measures": self.assess_technical_measures(activity),
                "international_transfers": self.assess_international_transfers(activity),
                "documentation": self.assess_documentation_gaps(activity)
            }
        }

        # Calculate overall risk level for activity
        risk_levels = [
            assessment["assessments"]["lawful_basis"]["risk_level"],
            assessment["assessments"]["data_subject_rights"]["risk_level"],
            assessment["assessments"]["dpia"]["risk_level"],
            assessment["assessments"]["breach_readiness"]["risk_level"],
            assessment["assessments"]["technical_measures"]["risk_level"],
            assessment["assessments"]["international_transfers"]["risk_level"],
            assessment["assessments"]["documentation"]["risk_level"]
        ]

        risk_priority = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }

        overall_risk = max(risk_levels, key=lambda x: risk_priority.get(x, 0))
        assessment["overall_risk"] = overall_risk

        # Calculate overall compliance score
        scores = [
            assessment["assessments"]["data_subject_rights"]["compliance_score"],
            assessment["assessments"]["breach_readiness"]["compliance_score"],
            assessment["assessments"]["technical_measures"]["compliance_score"]
        ]
        assessment["compliance_score"] = round(sum(scores) / len(scores), 1)

        return assessment

    def run_assessment(self) -> Dict[str, Any]:
        """Run comprehensive GDPR compliance assessment"""
        activity_assessments = []

        for activity in self.processing_activities:
            assessment = self.assess_activity(activity)
            activity_assessments.append(assessment)

        # Generate summary statistics
        total_activities = len(activity_assessments)
        critical_issues = sum(1 for a in activity_assessments if a["overall_risk"] == "critical")
        high_risk = sum(1 for a in activity_assessments if a["overall_risk"] == "high")
        medium_risk = sum(1 for a in activity_assessments if a["overall_risk"] == "medium")
        low_risk = sum(1 for a in activity_assessments if a["overall_risk"] == "low")

        avg_compliance = (
            sum(a["compliance_score"] for a in activity_assessments) / total_activities
            if total_activities > 0 else 0
        )

        # Identify high-priority gaps
        high_priority_gaps = []
        for assessment in activity_assessments:
            if assessment["overall_risk"] in ["critical", "high"]:
                for area, details in assessment["assessments"].items():
                    if details.get("issues"):
                        for issue in details["issues"]:
                            high_priority_gaps.append({
                                "activity": assessment["activity_name"],
                                "area": area,
                                "issue": issue,
                                "risk": assessment["overall_risk"]
                            })

        self.assessment_results = {
            "summary": {
                "total_activities": total_activities,
                "overall_compliance_score": round(avg_compliance, 1),
                "risk_distribution": {
                    "critical": critical_issues,
                    "high": high_risk,
                    "medium": medium_risk,
                    "low": low_risk
                }
            },
            "high_priority_gaps": high_priority_gaps[:10],  # Top 10 gaps
            "activity_assessments": activity_assessments
        }

        return self.assessment_results


def format_text_output(results: Dict[str, Any], verbose: bool = False) -> str:
    """Format assessment results as human-readable text"""
    output = []

    output.append("=" * 70)
    output.append("GDPR/DSGVO COMPLIANCE ASSESSMENT REPORT")
    output.append("=" * 70)
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    output.append("")

    # Summary
    summary = results["summary"]
    output.append("EXECUTIVE SUMMARY")
    output.append("-" * 70)
    output.append(f"Total Processing Activities: {summary['total_activities']}")
    output.append(f"Overall Compliance Score: {summary['overall_compliance_score']}%")
    output.append("")
    output.append("Risk Distribution:")
    risk_dist = summary["risk_distribution"]
    output.append(f"  Critical Issues: {risk_dist['critical']}")
    output.append(f"  High Risk:       {risk_dist['high']}")
    output.append(f"  Medium Risk:     {risk_dist['medium']}")
    output.append(f"  Low Risk:        {risk_dist['low']}")
    output.append("")

    # High-priority gaps
    if results["high_priority_gaps"]:
        output.append("HIGH-PRIORITY GAPS REQUIRING IMMEDIATE ATTENTION")
        output.append("-" * 70)
        for i, gap in enumerate(results["high_priority_gaps"], 1):
            output.append(f"{i}. [{gap['risk'].upper()}] {gap['activity']}")
            output.append(f"   Area: {gap['area']}")
            output.append(f"   Issue: {gap['issue']}")
            output.append("")

    # Individual activity assessments
    if verbose:
        output.append("")
        output.append("DETAILED ACTIVITY ASSESSMENTS")
        output.append("=" * 70)

        for assessment in results["activity_assessments"]:
            output.append("")
            output.append(f"Activity: {assessment['activity_name']}")
            output.append(f"ID: {assessment['activity_id']}")
            output.append(f"Purpose: {assessment['purpose']}")
            output.append(f"Overall Risk: {assessment['overall_risk'].upper()}")
            output.append(f"Compliance Score: {assessment['compliance_score']}%")
            output.append("")

            for area, details in assessment["assessments"].items():
                if details.get("issues"):
                    output.append(f"  {area.replace('_', ' ').title()}:")
                    for issue in details["issues"]:
                        output.append(f"    - {issue}")
            output.append("-" * 70)

    return "\n".join(output)


def format_json_output(results: Dict[str, Any]) -> str:
    """Format assessment results as JSON"""
    output = {
        "metadata": {
            "tool": "gdpr_compliance_checker.py",
            "version": "1.0.0",
            "timestamp": datetime.now().astimezone().isoformat(),
            "assessment_date": datetime.now().strftime('%Y-%m-%d')
        },
        "results": results
    }

    return json.dumps(output, indent=2)


def format_csv_output(results: Dict[str, Any]) -> str:
    """Format assessment results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "Activity ID",
        "Activity Name",
        "Overall Risk",
        "Compliance Score",
        "Lawful Basis Status",
        "Data Subject Rights Score",
        "DPIA Required",
        "DPIA Completed",
        "Technical Measures Score",
        "High Priority Issues"
    ])

    # Data rows
    for assessment in results["activity_assessments"]:
        issues_count = sum(
            len(details.get("issues", []))
            for details in assessment["assessments"].values()
        )

        writer.writerow([
            assessment["activity_id"],
            assessment["activity_name"],
            assessment["overall_risk"].upper(),
            assessment["compliance_score"],
            "Pass" if assessment["assessments"]["lawful_basis"]["compliant"] else "Fail",
            assessment["assessments"]["data_subject_rights"]["compliance_score"],
            "Yes" if assessment["assessments"]["dpia"]["dpia_required"] else "No",
            "Yes" if assessment["assessments"]["dpia"]["dpia_completed"] else "No",
            assessment["assessments"]["technical_measures"]["compliance_score"],
            issues_count
        ])

    return output.getvalue()


def main():
    """
    Main entry point with standardized argument parsing.

    Parses command-line arguments, loads processing inventory, performs
    comprehensive GDPR compliance assessment, and generates detailed reports.
    """
    parser = argparse.ArgumentParser(
        description='Assess GDPR/DSGVO compliance for data processing activities with risk-based analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic text assessment
  %(prog)s processing_inventory.json

  # Detailed JSON report for compliance dashboard
  %(prog)s processing_inventory.json --output json --verbose

  # CSV export for spreadsheet analysis
  %(prog)s processing_inventory.json -o csv -f compliance_report.csv

  # Verbose text report with all activity details
  %(prog)s processing_inventory.json -v

Input JSON Format:
  {
    "processing_activities": [
      {
        "activity_id": "PA-001",
        "activity_name": "Customer database",
        "purpose": "Customer relationship management",
        "data_categories": ["basic_personal", "financial"],
        "lawful_basis": "contract",
        "data_subjects": "customers",
        "retention_period": "7 years",
        "has_privacy_notice": true,
        "records_of_processing": true,
        "dpia_required": false,
        "dpia_completed": false,
        "data_subject_rights": {
          "right_to_access": true,
          "right_to_rectification": true,
          "right_to_erasure": true,
          "right_to_restriction": false,
          "right_to_portability": true,
          "right_to_object": false,
          "automated_decision_making_safeguards": false
        },
        "technical_measures": {
          "pseudonymization": false,
          "encryption": true,
          "access_controls": true,
          "data_minimization": true,
          "regular_testing": true,
          "incident_response_plan": true,
          "staff_training": true
        },
        "international_transfer": {
          "has_transfers": false
        },
        "breach_notification_procedures": true,
        "breach_response_tested": false,
        "data_processors": ["CRM Vendor"],
        "processor_agreements": true,
        "last_review_date": "2025-01-15"
      }
    ]
  }

For more information, see:
ra-qm-team/gdpr-dsgvo-expert/SKILL.md
        """
    )

    # Positional arguments
    parser.add_argument(
        'input',
        help='JSON file containing data processing inventory and controls'
    )

    # Optional arguments
    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format: text (default), json, or csv'
    )

    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Include detailed activity assessments in output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        # Validate input file
        input_path = Path(args.input)

        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        if not input_path.is_file():
            print(f"Error: Path is not a file: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Load input data
        if args.verbose:
            print(f"Loading processing inventory from: {args.input}", file=sys.stderr)

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}", file=sys.stderr)
            sys.exit(3)

        # Initialize compliance checker
        checker = GDPRComplianceChecker(data)

        if args.verbose:
            print(f"Assessing {len(checker.processing_activities)} processing activities...", file=sys.stderr)

        # Run assessment
        results = checker.run_assessment()

        # Format output
        if args.output == 'json':
            output = format_json_output(results)
        elif args.output == 'csv':
            output = format_csv_output(results)
        else:  # text (default)
            output = format_text_output(results, verbose=args.verbose)

        # Write output
        if args.file:
            try:
                output_path = Path(args.file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output)

                if args.verbose:
                    print(f"Assessment report written to: {args.file}", file=sys.stderr)
                else:
                    print(f"Report saved to: {args.file}")

            except PermissionError:
                print(f"Error: Permission denied writing to: {args.file}", file=sys.stderr)
                sys.exit(4)
            except Exception as e:
                print(f"Error writing output file: {e}", file=sys.stderr)
                sys.exit(4)
        else:
            print(output)

        # Exit with appropriate code based on assessment
        if results["summary"]["risk_distribution"]["critical"] > 0:
            sys.exit(3)  # Critical issues found

        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)

    except PermissionError as e:
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"Error: Invalid input data: {e}", file=sys.stderr)
        sys.exit(3)

    except KeyboardInterrupt:
        print("\nAssessment cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
