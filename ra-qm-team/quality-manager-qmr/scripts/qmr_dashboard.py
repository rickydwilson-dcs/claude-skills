#!/usr/bin/env python3
"""
Quality Management Review (QMR) Dashboard
Generates comprehensive QMR reports with compliance KPIs and CAPA trending.

This script produces management review meeting reports with quality metrics,
CAPA trends, audit findings, and compliance status tracking. Supports both
text (human-readable) and JSON output for dashboard integration.

Usage:
    python qmr_dashboard.py qmr_data.json
    python qmr_dashboard.py data.json --output json
    python qmr_dashboard.py data.json -o json -f qmr_report.json
    python qmr_dashboard.py data.json -o text -v

Author: Quality Management Team
Version: 1.0.0
Last Updated: 2025-11-05
"""

import argparse
import json
import sys
import csv
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

class TrendStatus(Enum):
    IMPROVING = "IMPROVING"
    STABLE = "STABLE"
    DECLINING = "DECLINING"
    CRITICAL = "CRITICAL"

class ComplianceStatus(Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    UNDER_REVIEW = "UNDER_REVIEW"
    ACTION_REQUIRED = "ACTION_REQUIRED"

@dataclass
class QualityKPI:
    kpi_name: str
    current_value: float
    target_value: float
    unit: str
    trend: TrendStatus
    period: str
    description: str = ""

@dataclass
class CAPARecord:
    capa_id: str
    issue_description: str
    root_cause: str
    corrective_action: str
    preventive_action: str
    status: str
    priority: str
    opened_date: str
    target_date: str
    closed_date: Optional[str] = None
    effectiveness_verified: bool = False

@dataclass
class AuditFinding:
    finding_id: str
    audit_type: str
    severity: str
    area: str
    description: str
    identified_date: str
    capa_reference: Optional[str] = None
    status: str = "OPEN"

@dataclass
class ComplianceMetric:
    standard: str
    status: ComplianceStatus
    last_audit_date: str
    next_audit_date: str
    open_findings: int
    critical_issues: int
    notes: str = ""

class QMRDashboard:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.kpis: List[QualityKPI] = []
        self.capas: List[CAPARecord] = []
        self.audit_findings: List[AuditFinding] = []
        self.compliance_metrics: List[ComplianceMetric] = []
        self.metadata: Dict[str, Any] = {}
        self.load_data()

    def load_data(self):
        """Load QMR data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)

                # Load metadata
                self.metadata = data.get('metadata', {})

                # Load KPIs
                for kpi_data in data.get('kpis', []):
                    kpi_data['trend'] = TrendStatus(kpi_data['trend'])
                    self.kpis.append(QualityKPI(**kpi_data))

                # Load CAPAs
                for capa_data in data.get('capas', []):
                    self.capas.append(CAPARecord(**capa_data))

                # Load audit findings
                for finding_data in data.get('audit_findings', []):
                    self.audit_findings.append(AuditFinding(**finding_data))

                # Load compliance metrics
                for comp_data in data.get('compliance_metrics', []):
                    comp_data['status'] = ComplianceStatus(comp_data['status'])
                    self.compliance_metrics.append(ComplianceMetric(**comp_data))

        except FileNotFoundError:
            print(f"Error: Data file not found: {self.data_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}", file=sys.stderr)
            sys.exit(3)
        except Exception as e:
            print(f"Error loading data: {e}", file=sys.stderr)
            sys.exit(1)

    def calculate_kpi_performance(self) -> Dict[str, Any]:
        """Calculate overall KPI performance metrics"""
        if not self.kpis:
            return {"total": 0, "on_target": 0, "below_target": 0, "performance_rate": 0}

        on_target = sum(1 for kpi in self.kpis if kpi.current_value >= kpi.target_value)
        below_target = len(self.kpis) - on_target
        performance_rate = (on_target / len(self.kpis)) * 100

        return {
            "total": len(self.kpis),
            "on_target": on_target,
            "below_target": below_target,
            "performance_rate": round(performance_rate, 1)
        }

    def analyze_capa_trends(self) -> Dict[str, Any]:
        """Analyze CAPA trends and patterns"""
        if not self.capas:
            return {
                "total_capas": 0,
                "open_capas": 0,
                "closed_capas": 0,
                "overdue_capas": 0,
                "closure_rate": 0,
                "effectiveness_verified": 0
            }

        today = datetime.date.today().strftime('%Y-%m-%d')
        open_capas = [c for c in self.capas if c.status.upper() in ['OPEN', 'IN_PROGRESS']]
        closed_capas = [c for c in self.capas if c.status.upper() == 'CLOSED']
        overdue_capas = [c for c in open_capas if c.target_date < today]
        verified = [c for c in closed_capas if c.effectiveness_verified]

        closure_rate = (len(closed_capas) / len(self.capas)) * 100 if self.capas else 0

        return {
            "total_capas": len(self.capas),
            "open_capas": len(open_capas),
            "closed_capas": len(closed_capas),
            "overdue_capas": len(overdue_capas),
            "closure_rate": round(closure_rate, 1),
            "effectiveness_verified": len(verified),
            "priority_breakdown": self._count_by_priority()
        }

    def _count_by_priority(self) -> Dict[str, int]:
        """Count CAPAs by priority level"""
        priority_count = {}
        for capa in self.capas:
            priority = capa.priority.upper()
            priority_count[priority] = priority_count.get(priority, 0) + 1
        return priority_count

    def summarize_audit_findings(self) -> Dict[str, Any]:
        """Summarize audit findings by severity and status"""
        if not self.audit_findings:
            return {
                "total_findings": 0,
                "open_findings": 0,
                "closed_findings": 0,
                "by_severity": {},
                "by_type": {}
            }

        open_findings = [f for f in self.audit_findings if f.status.upper() == 'OPEN']
        closed_findings = [f for f in self.audit_findings if f.status.upper() == 'CLOSED']

        by_severity = {}
        by_type = {}
        for finding in self.audit_findings:
            severity = finding.severity.upper()
            audit_type = finding.audit_type
            by_severity[severity] = by_severity.get(severity, 0) + 1
            by_type[audit_type] = by_type.get(audit_type, 0) + 1

        return {
            "total_findings": len(self.audit_findings),
            "open_findings": len(open_findings),
            "closed_findings": len(closed_findings),
            "by_severity": by_severity,
            "by_type": by_type
        }

    def assess_compliance_status(self) -> Dict[str, Any]:
        """Assess overall compliance status across standards"""
        if not self.compliance_metrics:
            return {
                "total_standards": 0,
                "compliant": 0,
                "non_compliant": 0,
                "action_required": 0,
                "compliance_rate": 0
            }

        compliant = [c for c in self.compliance_metrics if c.status == ComplianceStatus.COMPLIANT]
        non_compliant = [c for c in self.compliance_metrics if c.status == ComplianceStatus.NON_COMPLIANT]
        action_required = [c for c in self.compliance_metrics if c.status == ComplianceStatus.ACTION_REQUIRED]

        compliance_rate = (len(compliant) / len(self.compliance_metrics)) * 100

        return {
            "total_standards": len(self.compliance_metrics),
            "compliant": len(compliant),
            "non_compliant": len(non_compliant),
            "action_required": len(action_required),
            "compliance_rate": round(compliance_rate, 1)
        }

    def generate_text_report(self, verbose: bool = False) -> str:
        """Generate comprehensive text report"""
        report = []
        report.append("=" * 70)
        report.append("QUALITY MANAGEMENT REVIEW (QMR) DASHBOARD")
        report.append("=" * 70)
        report.append(f"Report Generated: {datetime.date.today()}")
        report.append(f"Reporting Period: {self.metadata.get('period', 'Not specified')}")
        report.append(f"Organization: {self.metadata.get('organization', 'Not specified')}")
        report.append("")

        # KPI Performance Section
        report.append("--- KEY PERFORMANCE INDICATORS (KPIs) ---")
        kpi_perf = self.calculate_kpi_performance()
        report.append(f"Total KPIs Tracked: {kpi_perf['total']}")
        report.append(f"On Target: {kpi_perf['on_target']} ({kpi_perf['performance_rate']}%)")
        report.append(f"Below Target: {kpi_perf['below_target']}")
        report.append("")

        if verbose and self.kpis:
            report.append("KPI Details:")
            for kpi in self.kpis:
                achievement = (kpi.current_value / kpi.target_value * 100) if kpi.target_value > 0 else 0
                report.append(f"  • {kpi.kpi_name}: {kpi.current_value}{kpi.unit} / {kpi.target_value}{kpi.unit} ({achievement:.1f}%)")
                report.append(f"    Trend: {kpi.trend.value}, Period: {kpi.period}")
            report.append("")

        # CAPA Trending Section
        report.append("--- CAPA (CORRECTIVE & PREVENTIVE ACTION) TRENDING ---")
        capa_trends = self.analyze_capa_trends()
        report.append(f"Total CAPAs: {capa_trends['total_capas']}")
        report.append(f"Open: {capa_trends['open_capas']} | Closed: {capa_trends['closed_capas']}")
        report.append(f"Overdue: {capa_trends['overdue_capas']}")
        report.append(f"Closure Rate: {capa_trends['closure_rate']}%")
        report.append(f"Effectiveness Verified: {capa_trends['effectiveness_verified']}")

        if capa_trends['priority_breakdown']:
            report.append("Priority Breakdown:")
            for priority, count in capa_trends['priority_breakdown'].items():
                report.append(f"  • {priority}: {count}")
        report.append("")

        # Audit Findings Section
        report.append("--- AUDIT FINDINGS SUMMARY ---")
        audit_summary = self.summarize_audit_findings()
        report.append(f"Total Findings: {audit_summary['total_findings']}")
        report.append(f"Open: {audit_summary['open_findings']} | Closed: {audit_summary['closed_findings']}")

        if audit_summary['by_severity']:
            report.append("By Severity:")
            for severity, count in audit_summary['by_severity'].items():
                report.append(f"  • {severity}: {count}")

        if verbose and audit_summary['by_type']:
            report.append("By Audit Type:")
            for audit_type, count in audit_summary['by_type'].items():
                report.append(f"  • {audit_type}: {count}")
        report.append("")

        # Compliance Status Section
        report.append("--- COMPLIANCE STATUS ---")
        compliance = self.assess_compliance_status()
        report.append(f"Standards Tracked: {compliance['total_standards']}")
        report.append(f"Compliant: {compliance['compliant']} ({compliance['compliance_rate']}%)")
        report.append(f"Non-Compliant: {compliance['non_compliant']}")
        report.append(f"Action Required: {compliance['action_required']}")
        report.append("")

        if verbose and self.compliance_metrics:
            report.append("Compliance Details:")
            for metric in self.compliance_metrics:
                report.append(f"  • {metric.standard}: {metric.status.value}")
                report.append(f"    Last Audit: {metric.last_audit_date} | Next: {metric.next_audit_date}")
                report.append(f"    Open Findings: {metric.open_findings} | Critical: {metric.critical_issues}")
            report.append("")

        # Management Actions Required
        report.append("--- MANAGEMENT ACTIONS REQUIRED ---")
        actions_needed = []

        if kpi_perf['below_target'] > 0:
            actions_needed.append(f"• Review {kpi_perf['below_target']} KPIs below target")

        if capa_trends['overdue_capas'] > 0:
            actions_needed.append(f"• Address {capa_trends['overdue_capas']} overdue CAPAs")

        if compliance['non_compliant'] > 0:
            actions_needed.append(f"• Remediate {compliance['non_compliant']} non-compliant standards")

        if audit_summary['open_findings'] > 0:
            actions_needed.append(f"• Close {audit_summary['open_findings']} open audit findings")

        if actions_needed:
            for action in actions_needed:
                report.append(action)
        else:
            report.append("• No immediate actions required - Quality system performing well")

        report.append("")
        report.append("=" * 70)

        return "\n".join(report)

    def generate_json_report(self, verbose: bool = False) -> Dict[str, Any]:
        """Generate comprehensive JSON report"""
        report = {
            "metadata": {
                "tool": "qmr_dashboard.py",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "generated_date": datetime.date.today().strftime('%Y-%m-%d'),
                "reporting_period": self.metadata.get('period', 'Not specified'),
                "organization": self.metadata.get('organization', 'Not specified')
            },
            "summary": {
                "kpi_performance": self.calculate_kpi_performance(),
                "capa_trends": self.analyze_capa_trends(),
                "audit_findings": self.summarize_audit_findings(),
                "compliance_status": self.assess_compliance_status()
            }
        }

        if verbose:
            report["detailed_data"] = {
                "kpis": [asdict(kpi) for kpi in self.kpis],
                "capas": [asdict(capa) for capa in self.capas],
                "audit_findings": [asdict(finding) for finding in self.audit_findings],
                "compliance_metrics": [asdict(metric) for metric in self.compliance_metrics]
            }

            # Convert enums to strings
            for kpi in report["detailed_data"]["kpis"]:
                kpi['trend'] = kpi['trend'].value if hasattr(kpi['trend'], 'value') else str(kpi['trend'])

            for metric in report["detailed_data"]["compliance_metrics"]:
                metric['status'] = metric['status'].value if hasattr(metric['status'], 'value') else str(metric['status'])

        return report

    def generate_csv_report(self) -> str:
        """Generate CSV report with KPI and CAPA summary"""
        output = []

        # KPIs section
        output.append("KPI Summary")
        output.append("KPI Name,Current Value,Target Value,Unit,Trend,Period,Achievement %")

        for kpi in self.kpis:
            achievement = (kpi.current_value / kpi.target_value * 100) if kpi.target_value > 0 else 0
            output.append(f"{kpi.kpi_name},{kpi.current_value},{kpi.target_value},{kpi.unit},{kpi.trend.value},{kpi.period},{achievement:.1f}")

        output.append("")

        # CAPAs section
        output.append("CAPA Summary")
        output.append("CAPA ID,Issue,Status,Priority,Opened Date,Target Date,Effectiveness Verified")

        for capa in self.capas:
            output.append(f"{capa.capa_id},{capa.issue_description},{capa.status},{capa.priority},{capa.opened_date},{capa.target_date},{capa.effectiveness_verified}")

        output.append("")

        # Compliance section
        output.append("Compliance Summary")
        output.append("Standard,Status,Last Audit,Next Audit,Open Findings,Critical Issues")

        for metric in self.compliance_metrics:
            output.append(f"{metric.standard},{metric.status.value},{metric.last_audit_date},{metric.next_audit_date},{metric.open_findings},{metric.critical_issues}")

        return "\n".join(output)

def main():
    """
    Main entry point with standardized argument parsing.
    """
    parser = argparse.ArgumentParser(
        description='Generate Quality Management Review (QMR) dashboard with compliance KPIs and CAPA trending',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate text report (default)
  %(prog)s qmr_data.json

  # Generate JSON report for dashboard integration
  %(prog)s qmr_data.json --output json

  # Save detailed report to file
  %(prog)s qmr_data.json -o json -f qmr_report.json -v

  # Generate CSV export for management
  %(prog)s qmr_data.json --output csv

For more information, see:
ra-qm-team/quality-manager-qmr/SKILL.md
        """
    )

    parser.add_argument(
        'input',
        help='QMR data file (JSON format with KPIs, CAPAs, audit findings, compliance metrics)'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format: text (default), json for dashboards, csv for spreadsheets'
    )

    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Include detailed KPI, CAPA, and compliance information'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

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

        # Load QMR dashboard
        if args.verbose:
            print(f"Loading QMR data from: {args.input}", file=sys.stderr)

        dashboard = QMRDashboard(str(input_path))

        if args.verbose:
            print(f"Loaded: {len(dashboard.kpis)} KPIs, {len(dashboard.capas)} CAPAs, "
                  f"{len(dashboard.audit_findings)} findings, {len(dashboard.compliance_metrics)} standards",
                  file=sys.stderr)

        # Generate report based on output format
        if args.output == 'json':
            report_data = dashboard.generate_json_report(verbose=args.verbose)
            output = json.dumps(report_data, indent=2)
        elif args.output == 'csv':
            output = dashboard.generate_csv_report()
        else:  # text (default)
            output = dashboard.generate_text_report(verbose=args.verbose)

        # Write output to file or stdout
        if args.file:
            try:
                output_path = Path(args.file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output)

                if args.verbose:
                    print(f"QMR report written to: {args.file}", file=sys.stderr)
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
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
