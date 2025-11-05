#!/usr/bin/env python3
"""
QMS Audit Scheduler - ISO 13485 Compliance
Manages internal audit scheduling, tracking, and ISO 13485 compliance monitoring.

This script automates audit scheduling, tracks audit findings, monitors
compliance status, and generates audit reports for ISO 13485 certification.

Usage:
    python qms_audit_scheduler.py audit_data.json
    python qms_audit_scheduler.py data.json --output json
    python qms_audit_scheduler.py data.json -o csv -f audit_schedule.csv

Author: Quality Management Team
Version: 1.0.0
Last Updated: 2025-11-05
"""

import argparse
import json
import sys
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

class AuditType(Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    SURVEILLANCE = "SURVEILLANCE"
    RECERTIFICATION = "RECERTIFICATION"
    SUPPLIER = "SUPPLIER"

class AuditStatus(Enum):
    PLANNED = "PLANNED"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class FindingSeverity(Enum):
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    OBSERVATION = "OBSERVATION"
    OPPORTUNITY = "OPPORTUNITY"

@dataclass
class AuditSchedule:
    audit_id: str
    audit_type: AuditType
    scope: str
    iso_clause: str
    auditor: str
    auditee: str
    planned_date: str
    actual_date: Optional[str] = None
    status: AuditStatus = AuditStatus.PLANNED
    duration_hours: float = 4.0
    findings_count: int = 0
    notes: str = ""

@dataclass
class AuditFinding:
    finding_id: str
    audit_id: str
    severity: FindingSeverity
    iso_clause: str
    description: str
    evidence: str
    requirement: str
    identified_date: str
    due_date: str
    status: str = "OPEN"
    capa_id: Optional[str] = None

@dataclass
class ComplianceClause:
    clause_number: str
    clause_title: str
    last_audit_date: Optional[str]
    next_audit_date: str
    findings_count: int
    compliance_status: str
    risk_level: str

class QMSAuditScheduler:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.audits: List[AuditSchedule] = []
        self.findings: List[AuditFinding] = []
        self.clauses: List[ComplianceClause] = []
        self.metadata: Dict[str, Any] = {}
        self.load_data()

    def load_data(self):
        """Load audit data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)

                self.metadata = data.get('metadata', {})

                for audit_data in data.get('audits', []):
                    audit_data['audit_type'] = AuditType(audit_data['audit_type'])
                    audit_data['status'] = AuditStatus(audit_data['status'])
                    self.audits.append(AuditSchedule(**audit_data))

                for finding_data in data.get('findings', []):
                    finding_data['severity'] = FindingSeverity(finding_data['severity'])
                    self.findings.append(AuditFinding(**finding_data))

                for clause_data in data.get('clauses', []):
                    self.clauses.append(ComplianceClause(**clause_data))

        except FileNotFoundError:
            print(f"Error: Data file not found: {self.data_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}", file=sys.stderr)
            sys.exit(3)
        except Exception as e:
            print(f"Error loading data: {e}", file=sys.stderr)
            sys.exit(1)

    def get_upcoming_audits(self, days: int = 30) -> List[AuditSchedule]:
        """Get audits scheduled within next N days"""
        today = datetime.date.today()
        cutoff = today + datetime.timedelta(days=days)

        upcoming = []
        for audit in self.audits:
            if audit.status in [AuditStatus.PLANNED, AuditStatus.SCHEDULED]:
                audit_date = datetime.datetime.strptime(audit.planned_date, '%Y-%m-%d').date()
                if today <= audit_date <= cutoff:
                    upcoming.append(audit)

        return sorted(upcoming, key=lambda x: x.planned_date)

    def get_overdue_audits(self) -> List[AuditSchedule]:
        """Get audits that are overdue"""
        today = datetime.date.today()
        overdue = []

        for audit in self.audits:
            if audit.status in [AuditStatus.PLANNED, AuditStatus.SCHEDULED]:
                audit_date = datetime.datetime.strptime(audit.planned_date, '%Y-%m-%d').date()
                if audit_date < today:
                    overdue.append(audit)

        return sorted(overdue, key=lambda x: x.planned_date)

    def analyze_findings(self) -> Dict[str, Any]:
        """Analyze audit findings by severity and status"""
        total = len(self.findings)
        if total == 0:
            return {
                "total": 0,
                "open": 0,
                "closed": 0,
                "by_severity": {},
                "major_open": 0
            }

        open_findings = [f for f in self.findings if f.status.upper() == 'OPEN']
        closed_findings = [f for f in self.findings if f.status.upper() == 'CLOSED']

        by_severity = {}
        for finding in self.findings:
            severity = finding.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1

        major_open = len([f for f in open_findings if f.severity == FindingSeverity.MAJOR])

        return {
            "total": total,
            "open": len(open_findings),
            "closed": len(closed_findings),
            "by_severity": by_severity,
            "major_open": major_open
        }

    def calculate_compliance_coverage(self) -> Dict[str, Any]:
        """Calculate ISO 13485 clause coverage"""
        total_clauses = len(self.clauses)
        if total_clauses == 0:
            return {
                "total_clauses": 0,
                "compliant": 0,
                "non_compliant": 0,
                "coverage_rate": 0
            }

        compliant = [c for c in self.clauses if c.compliance_status.upper() == 'COMPLIANT']
        non_compliant = [c for c in self.clauses if c.compliance_status.upper() == 'NON_COMPLIANT']

        coverage_rate = (len(compliant) / total_clauses) * 100

        return {
            "total_clauses": total_clauses,
            "compliant": len(compliant),
            "non_compliant": len(non_compliant),
            "coverage_rate": round(coverage_rate, 1)
        }

    def generate_text_report(self, verbose: bool = False) -> str:
        """Generate comprehensive text report"""
        report = []
        report.append("=" * 70)
        report.append("QMS AUDIT SCHEDULE & COMPLIANCE REPORT - ISO 13485")
        report.append("=" * 70)
        report.append(f"Report Generated: {datetime.date.today()}")
        report.append(f"Organization: {self.metadata.get('organization', 'Not specified')}")
        report.append("")

        # Audit Schedule Overview
        report.append("--- AUDIT SCHEDULE OVERVIEW ---")
        report.append(f"Total Audits Scheduled: {len(self.audits)}")

        by_status = {}
        for audit in self.audits:
            status = audit.status.value
            by_status[status] = by_status.get(status, 0) + 1

        for status, count in by_status.items():
            report.append(f"  {status}: {count}")
        report.append("")

        # Upcoming Audits
        upcoming = self.get_upcoming_audits(30)
        if upcoming:
            report.append(f"--- UPCOMING AUDITS (Next 30 Days: {len(upcoming)}) ---")
            for audit in upcoming:
                report.append(f"  • {audit.planned_date}: {audit.scope} ({audit.audit_type.value})")
                report.append(f"    Auditor: {audit.auditor} | Auditee: {audit.auditee}")
            report.append("")

        # Overdue Audits
        overdue = self.get_overdue_audits()
        if overdue:
            report.append(f"--- OVERDUE AUDITS: {len(overdue)} ---")
            for audit in overdue:
                days_overdue = (datetime.date.today() - datetime.datetime.strptime(audit.planned_date, '%Y-%m-%d').date()).days
                report.append(f"  • {audit.audit_id}: {audit.scope} ({days_overdue} days overdue)")
            report.append("")

        # Findings Analysis
        report.append("--- AUDIT FINDINGS ANALYSIS ---")
        findings = self.analyze_findings()
        report.append(f"Total Findings: {findings['total']}")
        report.append(f"Open: {findings['open']} | Closed: {findings['closed']}")
        report.append(f"Major Findings (Open): {findings['major_open']}")

        if findings['by_severity']:
            report.append("By Severity:")
            for severity, count in findings['by_severity'].items():
                report.append(f"  • {severity}: {count}")
        report.append("")

        # ISO 13485 Compliance Coverage
        report.append("--- ISO 13485 COMPLIANCE COVERAGE ---")
        coverage = self.calculate_compliance_coverage()
        report.append(f"Total Clauses: {coverage['total_clauses']}")
        report.append(f"Compliant: {coverage['compliant']} ({coverage['coverage_rate']}%)")
        report.append(f"Non-Compliant: {coverage['non_compliant']}")
        report.append("")

        if verbose and self.clauses:
            report.append("Clause Details:")
            for clause in self.clauses:
                report.append(f"  • {clause.clause_number}: {clause.clause_title}")
                report.append(f"    Status: {clause.compliance_status} | Risk: {clause.risk_level}")
                report.append(f"    Last Audit: {clause.last_audit_date} | Next: {clause.next_audit_date}")
            report.append("")

        # Action Items
        report.append("--- ACTION ITEMS REQUIRED ---")
        if overdue:
            report.append(f"• Reschedule {len(overdue)} overdue audits")
        if findings['major_open'] > 0:
            report.append(f"• Address {findings['major_open']} open major findings")
        if coverage['non_compliant'] > 0:
            report.append(f"• Remediate {coverage['non_compliant']} non-compliant clauses")
        if not (overdue or findings['major_open'] or coverage['non_compliant']):
            report.append("• No critical actions required - QMS performing well")
        report.append("")

        report.append("=" * 70)

        return "\n".join(report)

    def generate_json_report(self, verbose: bool = False) -> Dict[str, Any]:
        """Generate comprehensive JSON report"""
        report = {
            "metadata": {
                "tool": "qms_audit_scheduler.py",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "generated_date": datetime.date.today().strftime('%Y-%m-%d'),
                "organization": self.metadata.get('organization', 'Not specified')
            },
            "summary": {
                "total_audits": len(self.audits),
                "upcoming_audits": len(self.get_upcoming_audits(30)),
                "overdue_audits": len(self.get_overdue_audits()),
                "findings_analysis": self.analyze_findings(),
                "compliance_coverage": self.calculate_compliance_coverage()
            }
        }

        if verbose:
            report["detailed_data"] = {
                "audits": [asdict(audit) for audit in self.audits],
                "findings": [asdict(finding) for finding in self.findings],
                "clauses": [asdict(clause) for clause in self.clauses],
                "upcoming": [asdict(audit) for audit in self.get_upcoming_audits(30)],
                "overdue": [asdict(audit) for audit in self.get_overdue_audits()]
            }

            # Convert enums to strings
            for audit in report["detailed_data"]["audits"]:
                audit['audit_type'] = audit['audit_type'].value
                audit['status'] = audit['status'].value

            for finding in report["detailed_data"]["findings"]:
                finding['severity'] = finding['severity'].value

            for audit in report["detailed_data"]["upcoming"]:
                audit['audit_type'] = audit['audit_type'].value
                audit['status'] = audit['status'].value

            for audit in report["detailed_data"]["overdue"]:
                audit['audit_type'] = audit['audit_type'].value
                audit['status'] = audit['status'].value

        return report

    def generate_csv_report(self) -> str:
        """Generate CSV report with audit schedule"""
        output = []

        output.append("Audit Schedule")
        output.append("Audit ID,Type,Scope,ISO Clause,Auditor,Auditee,Planned Date,Status,Findings")

        for audit in self.audits:
            output.append(f"{audit.audit_id},{audit.audit_type.value},{audit.scope},{audit.iso_clause},"
                         f"{audit.auditor},{audit.auditee},{audit.planned_date},{audit.status.value},{audit.findings_count}")

        output.append("")
        output.append("Compliance Coverage")
        output.append("Clause,Title,Last Audit,Next Audit,Findings,Status,Risk Level")

        for clause in self.clauses:
            output.append(f"{clause.clause_number},{clause.clause_title},{clause.last_audit_date},"
                         f"{clause.next_audit_date},{clause.findings_count},{clause.compliance_status},{clause.risk_level}")

        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Manage ISO 13485 internal audit scheduling, tracking, and compliance monitoring',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audit_data.json
  %(prog)s audit_data.json --output json
  %(prog)s audit_data.json -o csv -f audit_schedule.csv -v

For more information:
ra-qm-team/quality-manager-qms-iso13485/SKILL.md
        """
    )

    parser.add_argument('input', help='Audit data file (JSON format)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text',
                       help='Output format')
    parser.add_argument('--file', '-f', help='Write output to file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Include detailed audit and compliance information')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        scheduler = QMSAuditScheduler(str(input_path))

        if args.output == 'json':
            output = json.dumps(scheduler.generate_json_report(verbose=args.verbose), indent=2)
        elif args.output == 'csv':
            output = scheduler.generate_csv_report()
        else:
            output = scheduler.generate_text_report(verbose=args.verbose)

        if args.file:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Report saved to: {args.file}")
        else:
            print(output)

        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
