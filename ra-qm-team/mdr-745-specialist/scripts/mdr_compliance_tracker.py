#!/usr/bin/env python3
"""
MDR Compliance Tracker - EU MDR 2017/745 Compliance Management
Tracks EU MDR compliance requirements, gap analysis, and certification readiness.

This script implements comprehensive MDR compliance tracking including General Safety
and Performance Requirements (GSPR) Annex I, Technical Documentation Annex II/III,
Clinical Evaluation Article 61, Post-Market Surveillance Articles 83-92, and UDI
system compliance.

Usage:
    python mdr_compliance_tracker.py mdr_requirements.json
    python mdr_compliance_tracker.py data.json --output json
    python mdr_compliance_tracker.py data.json -o csv -f mdr_report.csv

Author: MDR 2017/745 Specialist Team
Version: 1.0.0
Last Updated: 2025-11-05
"""

import argparse
import json
import sys
import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path


class MDRAnnex(Enum):
    """MDR Annexes and Articles"""
    ANNEX_I = "ANNEX_I_GSPR"  # General Safety and Performance Requirements
    ANNEX_II = "ANNEX_II_TECH_DOC"  # Technical Documentation
    ANNEX_III = "ANNEX_III_TECH_DOC_CLASS_III"  # Technical Documentation Class III
    ANNEX_XIV = "ANNEX_XIV_CLINICAL"  # Clinical Evaluation
    ARTICLE_61 = "ARTICLE_61_CLINICAL_EVAL"  # Clinical Evaluation
    ARTICLE_83_92 = "ARTICLE_83_92_PMS"  # Post-Market Surveillance
    ARTICLE_27 = "ARTICLE_27_UDI"  # UDI System


class ComplianceStatus(Enum):
    """Compliance status levels"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    COMPLIANT = "COMPLIANT"
    VERIFIED = "VERIFIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Priority(Enum):
    """Priority levels for requirements"""
    BLOCKING = "BLOCKING"  # Must be complete for CE marking
    HIGH = "HIGH"  # Critical for submission
    MEDIUM = "MEDIUM"  # Important but not blocking
    LOW = "LOW"  # Nice to have or future consideration


class DeviceClass(Enum):
    """Medical device classification"""
    CLASS_I = "CLASS_I"
    CLASS_IIA = "CLASS_IIA"
    CLASS_IIB = "CLASS_IIB"
    CLASS_III = "CLASS_III"


@dataclass
class MDRRequirement:
    """Individual MDR requirement"""
    requirement_id: str
    annex_article: MDRAnnex
    title: str
    description: str
    priority: Priority
    status: ComplianceStatus
    device_class_applicable: List[str]
    responsible_person: str
    target_date: str
    completion_date: Optional[str] = None
    evidence_location: str = ""
    gap_description: str = ""
    mitigation_plan: str = ""
    verification_method: str = ""
    estimated_effort_hours: int = 0
    blocking_for_ce_mark: bool = False
    notes: str = ""


@dataclass
class PMCFCommitment:
    """Post-Market Clinical Follow-up commitments"""
    pmcf_id: str
    study_title: str
    objective: str
    start_date: str
    target_completion: str
    status: str
    data_sources: List[str]
    responsible_person: str
    milestones: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class UDIRequirement:
    """UDI System compliance tracking"""
    udi_di_assigned: bool
    eudamed_registration_complete: bool
    eudamed_target_date: str
    udi_on_device_label: bool
    udi_on_packaging: bool
    basic_udi_di_assigned: bool
    responsible_person: str
    status: str
    notes: str = ""


class MDRComplianceTracker:
    """Main MDR compliance tracking system"""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.requirements: List[MDRRequirement] = []
        self.pmcf_commitments: List[PMCFCommitment] = []
        self.udi_status: Optional[UDIRequirement] = None
        self.metadata: Dict[str, Any] = {}
        self.load_data()

    def load_data(self):
        """Load MDR compliance data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                self.metadata = data.get('metadata', {})

                # Load requirements
                for req_data in data.get('requirements', []):
                    req_data['annex_article'] = MDRAnnex(req_data['annex_article'])
                    req_data['priority'] = Priority(req_data['priority'])
                    req_data['status'] = ComplianceStatus(req_data['status'])
                    self.requirements.append(MDRRequirement(**req_data))

                # Load PMCF commitments
                for pmcf_data in data.get('pmcf_commitments', []):
                    self.pmcf_commitments.append(PMCFCommitment(**pmcf_data))

                # Load UDI status
                if 'udi_status' in data:
                    self.udi_status = UDIRequirement(**data['udi_status'])

        except FileNotFoundError:
            print(f"Error: Data file not found: {self.data_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}", file=sys.stderr)
            sys.exit(3)
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error: Invalid data format: {e}", file=sys.stderr)
            sys.exit(3)
        except Exception as e:
            print(f"Error loading data: {e}", file=sys.stderr)
            sys.exit(1)

    def calculate_readiness_percentage(self) -> float:
        """Calculate overall MDR compliance readiness"""
        if not self.requirements:
            return 0.0

        status_weights = {
            ComplianceStatus.NOT_STARTED: 0.0,
            ComplianceStatus.IN_PROGRESS: 0.3,
            ComplianceStatus.PARTIALLY_COMPLIANT: 0.6,
            ComplianceStatus.COMPLIANT: 0.9,
            ComplianceStatus.VERIFIED: 1.0,
            ComplianceStatus.NOT_APPLICABLE: 1.0
        }

        total_score = 0.0
        for req in self.requirements:
            total_score += status_weights.get(req.status, 0.0)

        return round((total_score / len(self.requirements)) * 100, 1)

    def get_blocking_gaps(self) -> List[MDRRequirement]:
        """Identify blocking gaps that prevent CE marking"""
        return [
            req for req in self.requirements
            if req.blocking_for_ce_mark and req.status not in [
                ComplianceStatus.COMPLIANT,
                ComplianceStatus.VERIFIED,
                ComplianceStatus.NOT_APPLICABLE
            ]
        ]

    def get_overdue_requirements(self) -> List[MDRRequirement]:
        """Get overdue requirements"""
        today = datetime.date.today().strftime('%Y-%m-%d')
        return [
            req for req in self.requirements
            if req.target_date < today and req.status not in [
                ComplianceStatus.COMPLIANT,
                ComplianceStatus.VERIFIED,
                ComplianceStatus.NOT_APPLICABLE
            ]
        ]

    def calculate_estimated_effort(self) -> Dict[str, int]:
        """Calculate remaining effort by status"""
        not_started = sum(
            req.estimated_effort_hours for req in self.requirements
            if req.status == ComplianceStatus.NOT_STARTED
        )
        in_progress = sum(
            req.estimated_effort_hours for req in self.requirements
            if req.status == ComplianceStatus.IN_PROGRESS
        )
        total_remaining = sum(
            req.estimated_effort_hours for req in self.requirements
            if req.status not in [
                ComplianceStatus.COMPLIANT,
                ComplianceStatus.VERIFIED,
                ComplianceStatus.NOT_APPLICABLE
            ]
        )

        return {
            "not_started_hours": not_started,
            "in_progress_hours": in_progress,
            "total_remaining_hours": total_remaining,
            "estimated_weeks": round(total_remaining / 40, 1) if total_remaining > 0 else 0
        }

    def analyze_by_annex(self) -> Dict[str, Dict[str, Any]]:
        """Analyze compliance by MDR Annex/Article"""
        by_annex = {}

        for req in self.requirements:
            annex = req.annex_article.value
            if annex not in by_annex:
                by_annex[annex] = {
                    "total": 0,
                    "compliant": 0,
                    "in_progress": 0,
                    "not_started": 0,
                    "blocking": 0
                }

            by_annex[annex]["total"] += 1

            if req.status in [ComplianceStatus.COMPLIANT, ComplianceStatus.VERIFIED]:
                by_annex[annex]["compliant"] += 1
            elif req.status == ComplianceStatus.IN_PROGRESS:
                by_annex[annex]["in_progress"] += 1
            elif req.status == ComplianceStatus.NOT_STARTED:
                by_annex[annex]["not_started"] += 1

            if req.blocking_for_ce_mark:
                by_annex[annex]["blocking"] += 1

        # Calculate completion percentage for each annex
        for annex in by_annex:
            total = by_annex[annex]["total"]
            compliant = by_annex[annex]["compliant"]
            by_annex[annex]["completion_pct"] = round((compliant / total * 100), 1) if total > 0 else 0

        return by_annex

    def generate_submission_timeline(self) -> List[Dict[str, str]]:
        """Generate timeline for regulatory submission"""
        milestones = []

        # Sort requirements by target date
        sorted_reqs = sorted(
            [r for r in self.requirements if r.status not in [
                ComplianceStatus.COMPLIANT,
                ComplianceStatus.VERIFIED,
                ComplianceStatus.NOT_APPLICABLE
            ]],
            key=lambda x: x.target_date
        )

        # Group by month
        by_month = {}
        for req in sorted_reqs:
            month_key = req.target_date[:7]  # YYYY-MM
            if month_key not in by_month:
                by_month[month_key] = []
            by_month[month_key].append(req)

        # Create timeline entries
        for month, reqs in sorted(by_month.items()):
            blocking_count = sum(1 for r in reqs if r.blocking_for_ce_mark)
            milestones.append({
                "month": month,
                "total_requirements": len(reqs),
                "blocking_requirements": blocking_count,
                "key_deliverables": ", ".join([r.title[:50] for r in reqs[:3]])
            })

        return milestones

    def assess_ce_marking_readiness(self) -> Dict[str, Any]:
        """Assess readiness for CE marking submission"""
        blocking_gaps = self.get_blocking_gaps()

        # Check critical areas
        gspr_complete = all(
            req.status in [ComplianceStatus.COMPLIANT, ComplianceStatus.VERIFIED]
            for req in self.requirements
            if req.annex_article == MDRAnnex.ANNEX_I and req.blocking_for_ce_mark
        )

        tech_doc_complete = all(
            req.status in [ComplianceStatus.COMPLIANT, ComplianceStatus.VERIFIED]
            for req in self.requirements
            if req.annex_article in [MDRAnnex.ANNEX_II, MDRAnnex.ANNEX_III] and req.blocking_for_ce_mark
        )

        clinical_eval_complete = all(
            req.status in [ComplianceStatus.COMPLIANT, ComplianceStatus.VERIFIED]
            for req in self.requirements
            if req.annex_article in [MDRAnnex.ANNEX_XIV, MDRAnnex.ARTICLE_61] and req.blocking_for_ce_mark
        )

        pms_system_complete = all(
            req.status in [ComplianceStatus.COMPLIANT, ComplianceStatus.VERIFIED]
            for req in self.requirements
            if req.annex_article == MDRAnnex.ARTICLE_83_92 and req.blocking_for_ce_mark
        )

        udi_complete = (
            self.udi_status.udi_di_assigned and
            self.udi_status.udi_on_device_label and
            self.udi_status.udi_on_packaging
        ) if self.udi_status else False

        all_blocking_complete = len(blocking_gaps) == 0

        readiness_status = "READY" if all_blocking_complete else "NOT_READY"
        if all_blocking_complete and not gspr_complete:
            readiness_status = "NEAR_READY"

        return {
            "readiness_status": readiness_status,
            "blocking_gaps_count": len(blocking_gaps),
            "gspr_complete": gspr_complete,
            "technical_documentation_complete": tech_doc_complete,
            "clinical_evaluation_complete": clinical_eval_complete,
            "pms_system_complete": pms_system_complete,
            "udi_system_complete": udi_complete,
            "blocking_gaps": [req.requirement_id for req in blocking_gaps]
        }

    def generate_text_report(self, verbose: bool = False) -> str:
        """Generate comprehensive text report"""
        report = []
        report.append("=" * 80)
        report.append("EU MDR 2017/745 COMPLIANCE TRACKING DASHBOARD")
        report.append("=" * 80)
        report.append(f"Report Generated: {datetime.date.today()}")
        report.append(f"Device: {self.metadata.get('device_name', 'Not specified')}")
        report.append(f"Device Class: {self.metadata.get('device_class', 'Not specified')}")
        report.append(f"Manufacturer: {self.metadata.get('manufacturer', 'Not specified')}")
        report.append("")

        # Overall readiness
        readiness = self.calculate_readiness_percentage()
        report.append("--- OVERALL MDR COMPLIANCE READINESS ---")
        report.append(f"Compliance Score: {readiness}%")
        report.append("")

        # CE Marking readiness
        ce_readiness = self.assess_ce_marking_readiness()
        report.append("--- CE MARKING READINESS ASSESSMENT ---")
        report.append(f"Status: {ce_readiness['readiness_status']}")
        report.append(f"Blocking Gaps: {ce_readiness['blocking_gaps_count']}")
        report.append("")
        report.append("Critical Requirements Status:")
        report.append(f"  • GSPR (Annex I): {'✓ Complete' if ce_readiness['gspr_complete'] else '✗ Incomplete'}")
        report.append(f"  • Technical Documentation: {'✓ Complete' if ce_readiness['technical_documentation_complete'] else '✗ Incomplete'}")
        report.append(f"  • Clinical Evaluation: {'✓ Complete' if ce_readiness['clinical_evaluation_complete'] else '✗ Incomplete'}")
        report.append(f"  • Post-Market Surveillance: {'✓ Complete' if ce_readiness['pms_system_complete'] else '✗ Incomplete'}")
        report.append(f"  • UDI System: {'✓ Complete' if ce_readiness['udi_system_complete'] else '✗ Incomplete'}")
        report.append("")

        # Blocking gaps
        blocking_gaps = self.get_blocking_gaps()
        if blocking_gaps:
            report.append(f"--- BLOCKING GAPS (CE MARKING CRITICAL): {len(blocking_gaps)} ---")
            for gap in blocking_gaps:
                report.append(f"  • {gap.requirement_id}: {gap.title}")
                report.append(f"    Annex/Article: {gap.annex_article.value}")
                report.append(f"    Status: {gap.status.value} | Target: {gap.target_date}")
                report.append(f"    Responsible: {gap.responsible_person}")
                if gap.gap_description:
                    report.append(f"    Gap: {gap.gap_description}")
            report.append("")

        # Compliance by Annex
        report.append("--- COMPLIANCE BY MDR ANNEX/ARTICLE ---")
        by_annex = self.analyze_by_annex()
        for annex, stats in sorted(by_annex.items()):
            report.append(f"\n{annex}:")
            report.append(f"  Total Requirements: {stats['total']}")
            report.append(f"  Compliant: {stats['compliant']} ({stats['completion_pct']}%)")
            report.append(f"  In Progress: {stats['in_progress']}")
            report.append(f"  Not Started: {stats['not_started']}")
            report.append(f"  Blocking Requirements: {stats['blocking']}")
        report.append("")

        # Effort estimation
        effort = self.calculate_estimated_effort()
        report.append("--- ESTIMATED REMAINING EFFORT ---")
        report.append(f"Not Started: {effort['not_started_hours']} hours")
        report.append(f"In Progress: {effort['in_progress_hours']} hours")
        report.append(f"Total Remaining: {effort['total_remaining_hours']} hours (~{effort['estimated_weeks']} weeks)")
        report.append("")

        # Submission timeline
        timeline = self.generate_submission_timeline()
        if timeline:
            report.append("--- SUBMISSION TIMELINE (NEXT 6 MONTHS) ---")
            for milestone in timeline[:6]:
                report.append(f"\n{milestone['month']}:")
                report.append(f"  Requirements Due: {milestone['total_requirements']}")
                report.append(f"  Blocking: {milestone['blocking_requirements']}")
                report.append(f"  Key Deliverables: {milestone['key_deliverables']}")
            report.append("")

        # UDI Status
        if self.udi_status:
            report.append("--- UDI SYSTEM COMPLIANCE ---")
            report.append(f"UDI-DI Assigned: {'Yes' if self.udi_status.udi_di_assigned else 'No'}")
            report.append(f"EUDAMED Registration: {'Complete' if self.udi_status.eudamed_registration_complete else 'Pending'}")
            report.append(f"EUDAMED Target: {self.udi_status.eudamed_target_date}")
            report.append(f"UDI on Device Label: {'Yes' if self.udi_status.udi_on_device_label else 'No'}")
            report.append(f"UDI on Packaging: {'Yes' if self.udi_status.udi_on_packaging else 'No'}")
            report.append(f"Responsible: {self.udi_status.responsible_person}")
            report.append("")

        # PMCF Commitments
        if self.pmcf_commitments:
            report.append(f"--- POST-MARKET CLINICAL FOLLOW-UP: {len(self.pmcf_commitments)} Studies ---")
            for pmcf in self.pmcf_commitments:
                report.append(f"\n{pmcf.pmcf_id}: {pmcf.study_title}")
                report.append(f"  Objective: {pmcf.objective}")
                report.append(f"  Timeline: {pmcf.start_date} to {pmcf.target_completion}")
                report.append(f"  Status: {pmcf.status}")
                report.append(f"  Responsible: {pmcf.responsible_person}")
            report.append("")

        # Overdue requirements
        overdue = self.get_overdue_requirements()
        if overdue:
            report.append(f"--- OVERDUE REQUIREMENTS: {len(overdue)} ---")
            for req in overdue[:10]:
                days_overdue = (datetime.date.today() - datetime.datetime.strptime(req.target_date, '%Y-%m-%d').date()).days
                report.append(f"  • {req.requirement_id}: {req.title} ({days_overdue} days overdue)")
            report.append("")

        # Detailed requirements list (verbose mode)
        if verbose:
            report.append("--- DETAILED REQUIREMENTS LIST ---")
            for req in self.requirements:
                report.append(f"\n{req.requirement_id}: {req.title}")
                report.append(f"  Annex/Article: {req.annex_article.value}")
                report.append(f"  Status: {req.status.value} | Priority: {req.priority.value}")
                report.append(f"  Blocking: {'Yes' if req.blocking_for_ce_mark else 'No'}")
                report.append(f"  Target Date: {req.target_date}")
                report.append(f"  Responsible: {req.responsible_person}")
                report.append(f"  Estimated Effort: {req.estimated_effort_hours} hours")
                if req.gap_description:
                    report.append(f"  Gap: {req.gap_description}")
                if req.mitigation_plan:
                    report.append(f"  Mitigation: {req.mitigation_plan}")
                if req.evidence_location:
                    report.append(f"  Evidence: {req.evidence_location}")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)

    def generate_json_report(self, verbose: bool = False) -> Dict[str, Any]:
        """Generate comprehensive JSON report"""
        report = {
            "metadata": {
                "tool": "mdr_compliance_tracker.py",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "generated_date": datetime.date.today().strftime('%Y-%m-%d'),
                "device_name": self.metadata.get('device_name', 'Not specified'),
                "device_class": self.metadata.get('device_class', 'Not specified'),
                "manufacturer": self.metadata.get('manufacturer', 'Not specified')
            },
            "summary": {
                "overall_readiness_pct": self.calculate_readiness_percentage(),
                "ce_marking_readiness": self.assess_ce_marking_readiness(),
                "by_annex": self.analyze_by_annex(),
                "estimated_effort": self.calculate_estimated_effort(),
                "blocking_gaps_count": len(self.get_blocking_gaps()),
                "overdue_count": len(self.get_overdue_requirements()),
                "total_requirements": len(self.requirements),
                "pmcf_studies_count": len(self.pmcf_commitments)
            },
            "submission_timeline": self.generate_submission_timeline()
        }

        if self.udi_status:
            report["udi_compliance"] = asdict(self.udi_status)

        if verbose:
            report["detailed_data"] = {
                "all_requirements": [self._requirement_to_dict(req) for req in self.requirements],
                "blocking_gaps": [self._requirement_to_dict(req) for req in self.get_blocking_gaps()],
                "overdue_requirements": [self._requirement_to_dict(req) for req in self.get_overdue_requirements()],
                "pmcf_commitments": [asdict(pmcf) for pmcf in self.pmcf_commitments]
            }

        return report

    def _requirement_to_dict(self, req: MDRRequirement) -> Dict[str, Any]:
        """Convert requirement to dictionary with enum values as strings"""
        req_dict = asdict(req)
        req_dict['annex_article'] = req_dict['annex_article'].value
        req_dict['priority'] = req_dict['priority'].value
        req_dict['status'] = req_dict['status'].value
        return req_dict

    def generate_csv_report(self) -> str:
        """Generate CSV report"""
        output = []
        output.append("Requirement ID,Annex/Article,Title,Status,Priority,Blocking,Target Date,Responsible,Effort Hours,Gap Description")

        for req in self.requirements:
            output.append(
                f'"{req.requirement_id}","{req.annex_article.value}","{req.title}",'
                f'{req.status.value},{req.priority.value},{req.blocking_for_ce_mark},'
                f'{req.target_date},"{req.responsible_person}",{req.estimated_effort_hours},'
                f'"{req.gap_description}"'
            )

        return "\n".join(output)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Track EU MDR 2017/745 compliance, gap analysis, and CE marking readiness',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s mdr_requirements.json
  %(prog)s mdr_requirements.json --output json
  %(prog)s mdr_requirements.json -o csv -f mdr_compliance.csv -v

MDR Coverage:
  • Annex I - General Safety and Performance Requirements (GSPR)
  • Annex II/III - Technical Documentation
  • Annex XIV / Article 61 - Clinical Evaluation
  • Article 83-92 - Post-Market Surveillance
  • Article 27 - UDI System

For more information:
ra-qm-team/mdr-745-specialist/SKILL.md
        """
    )

    parser.add_argument('input', help='MDR requirements data file (JSON format)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'],
                       default='text', help='Output format (default: text)')
    parser.add_argument('--file', '-f', help='Write output to file instead of stdout')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Include detailed requirement information')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

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

        # Create tracker and generate report
        tracker = MDRComplianceTracker(str(input_path))

        if args.output == 'json':
            output = json.dumps(tracker.generate_json_report(verbose=args.verbose), indent=2)
        elif args.output == 'csv':
            output = tracker.generate_csv_report()
        else:
            output = tracker.generate_text_report(verbose=args.verbose)

        # Write output
        if args.file:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"MDR compliance report saved to: {args.file}")
        else:
            print(output)

        sys.exit(0)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
