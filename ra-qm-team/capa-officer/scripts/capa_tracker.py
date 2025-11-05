#!/usr/bin/env python3
"""
CAPA Tracker - Corrective and Preventive Action Management
Tracks CAPA creation, root cause analysis workflow, and effectiveness verification.

This script manages the complete CAPA lifecycle including issue identification,
root cause analysis, corrective/preventive actions, and effectiveness checks.

Usage:
    python capa_tracker.py capa_data.json
    python capa_tracker.py data.json --output json
    python capa_tracker.py data.json -o csv -f capa_report.csv

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

class CAPAStatus(Enum):
    INITIATED = "INITIATED"
    INVESTIGATING = "INVESTIGATING"
    ACTION_PLAN = "ACTION_PLAN"
    IMPLEMENTING = "IMPLEMENTING"
    VERIFICATION = "VERIFICATION"
    EFFECTIVENESS_CHECK = "EFFECTIVENESS_CHECK"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class Priority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class RCAMethod(Enum):
    FIVE_WHY = "5_WHY"
    FISHBONE = "FISHBONE"
    FAULT_TREE = "FAULT_TREE"
    FMEA = "FMEA"
    BARRIER_ANALYSIS = "BARRIER_ANALYSIS"

@dataclass
class CAPARecord:
    capa_id: str
    title: str
    source: str
    issue_description: str
    priority: Priority
    status: CAPAStatus
    initiated_by: str
    initiated_date: str
    target_completion: str
    root_cause: Optional[str] = None
    rca_method: Optional[RCAMethod] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    responsible_person: Optional[str] = None
    actual_completion: Optional[str] = None
    effectiveness_verified: bool = False
    effectiveness_date: Optional[str] = None
    cost_impact: float = 0.0
    notes: str = ""

class CAPATracker:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.capas: List[CAPARecord] = []
        self.metadata: Dict[str, Any] = {}
        self.load_data()

    def load_data(self):
        """Load CAPA data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)

                self.metadata = data.get('metadata', {})

                for capa_data in data.get('capas', []):
                    capa_data['priority'] = Priority(capa_data['priority'])
                    capa_data['status'] = CAPAStatus(capa_data['status'])
                    if capa_data.get('rca_method'):
                        capa_data['rca_method'] = RCAMethod(capa_data['rca_method'])
                    self.capas.append(CAPARecord(**capa_data))

        except FileNotFoundError:
            print(f"Error: Data file not found: {self.data_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}", file=sys.stderr)
            sys.exit(3)
        except Exception as e:
            print(f"Error loading data: {e}", file=sys.stderr)
            sys.exit(1)

    def get_open_capas(self) -> List[CAPARecord]:
        """Get all open CAPAs"""
        return [c for c in self.capas if c.status != CAPAStatus.CLOSED and c.status != CAPAStatus.CANCELLED]

    def get_overdue_capas(self) -> List[CAPARecord]:
        """Get overdue CAPAs"""
        today = datetime.date.today().strftime('%Y-%m-%d')
        return [c for c in self.get_open_capas() if c.target_completion < today]

    def get_critical_capas(self) -> List[CAPARecord]:
        """Get critical priority CAPAs"""
        return [c for c in self.get_open_capas() if c.priority == Priority.CRITICAL]

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate CAPA metrics"""
        total = len(self.capas)
        if total == 0:
            return {
                "total": 0,
                "open": 0,
                "closed": 0,
                "overdue": 0,
                "closure_rate": 0,
                "avg_closure_days": 0,
                "effectiveness_verified": 0
            }

        open_capas = self.get_open_capas()
        closed_capas = [c for c in self.capas if c.status == CAPAStatus.CLOSED]
        overdue = self.get_overdue_capas()
        verified = [c for c in closed_capas if c.effectiveness_verified]

        closure_rate = (len(closed_capas) / total) * 100

        # Calculate average closure time
        total_days = 0
        count = 0
        for capa in closed_capas:
            if capa.actual_completion:
                start = datetime.datetime.strptime(capa.initiated_date, '%Y-%m-%d')
                end = datetime.datetime.strptime(capa.actual_completion, '%Y-%m-%d')
                total_days += (end - start).days
                count += 1

        avg_closure_days = total_days / count if count > 0 else 0

        return {
            "total": total,
            "open": len(open_capas),
            "closed": len(closed_capas),
            "overdue": len(overdue),
            "closure_rate": round(closure_rate, 1),
            "avg_closure_days": round(avg_closure_days, 1),
            "effectiveness_verified": len(verified)
        }

    def analyze_by_source(self) -> Dict[str, int]:
        """Analyze CAPAs by source"""
        by_source = {}
        for capa in self.capas:
            source = capa.source
            by_source[source] = by_source.get(source, 0) + 1
        return by_source

    def analyze_by_priority(self) -> Dict[str, int]:
        """Analyze CAPAs by priority"""
        by_priority = {}
        for capa in self.capas:
            priority = capa.priority.value
            by_priority[priority] = by_priority.get(priority, 0) + 1
        return by_priority

    def analyze_by_rca_method(self) -> Dict[str, int]:
        """Analyze root cause analysis methods used"""
        by_method = {}
        for capa in self.capas:
            if capa.rca_method:
                method = capa.rca_method.value
                by_method[method] = by_method.get(method, 0) + 1
        return by_method

    def calculate_cost_impact(self) -> Dict[str, float]:
        """Calculate total cost impact"""
        total_cost = sum(capa.cost_impact for capa in self.capas)
        open_cost = sum(capa.cost_impact for capa in self.get_open_capas())
        closed_cost = sum(capa.cost_impact for capa in self.capas if capa.status == CAPAStatus.CLOSED)

        return {
            "total_cost": round(total_cost, 2),
            "open_cost": round(open_cost, 2),
            "closed_cost": round(closed_cost, 2)
        }

    def generate_text_report(self, verbose: bool = False) -> str:
        """Generate comprehensive text report"""
        report = []
        report.append("=" * 70)
        report.append("CAPA (CORRECTIVE & PREVENTIVE ACTION) TRACKING REPORT")
        report.append("=" * 70)
        report.append(f"Report Generated: {datetime.date.today()}")
        report.append(f"Organization: {self.metadata.get('organization', 'Not specified')}")
        report.append("")

        # Overall Metrics
        report.append("--- CAPA METRICS OVERVIEW ---")
        metrics = self.calculate_metrics()
        report.append(f"Total CAPAs: {metrics['total']}")
        report.append(f"Open: {metrics['open']} | Closed: {metrics['closed']}")
        report.append(f"Overdue: {metrics['overdue']}")
        report.append(f"Closure Rate: {metrics['closure_rate']}%")
        report.append(f"Avg Closure Time: {metrics['avg_closure_days']} days")
        report.append(f"Effectiveness Verified: {metrics['effectiveness_verified']}")
        report.append("")

        # Critical CAPAs
        critical = self.get_critical_capas()
        if critical:
            report.append(f"--- CRITICAL PRIORITY CAPAs: {len(critical)} ---")
            for capa in critical:
                report.append(f"  • {capa.capa_id}: {capa.title}")
                report.append(f"    Status: {capa.status.value} | Target: {capa.target_completion}")
            report.append("")

        # Overdue CAPAs
        overdue = self.get_overdue_capas()
        if overdue:
            report.append(f"--- OVERDUE CAPAs: {len(overdue)} ---")
            for capa in overdue:
                days_overdue = (datetime.date.today() - datetime.datetime.strptime(capa.target_completion, '%Y-%m-%d').date()).days
                report.append(f"  • {capa.capa_id}: {capa.title} ({days_overdue} days overdue)")
                report.append(f"    Priority: {capa.priority.value} | Responsible: {capa.responsible_person}")
            report.append("")

        # Analysis by Source
        report.append("--- CAPA SOURCE ANALYSIS ---")
        by_source = self.analyze_by_source()
        for source, count in sorted(by_source.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  • {source}: {count}")
        report.append("")

        # Analysis by Priority
        report.append("--- PRIORITY DISTRIBUTION ---")
        by_priority = self.analyze_by_priority()
        for priority, count in by_priority.items():
            report.append(f"  • {priority}: {count}")
        report.append("")

        # RCA Method Analysis
        report.append("--- ROOT CAUSE ANALYSIS METHODS ---")
        by_method = self.analyze_by_rca_method()
        if by_method:
            for method, count in by_method.items():
                report.append(f"  • {method}: {count}")
        else:
            report.append("  • No RCA methods recorded")
        report.append("")

        # Cost Impact
        report.append("--- COST IMPACT ANALYSIS ---")
        costs = self.calculate_cost_impact()
        report.append(f"Total Cost Impact: ${costs['total_cost']:,.2f}")
        report.append(f"Open CAPAs: ${costs['open_cost']:,.2f}")
        report.append(f"Closed CAPAs: ${costs['closed_cost']:,.2f}")
        report.append("")

        # Detailed CAPA List (verbose mode)
        if verbose:
            report.append("--- DETAILED CAPA LIST ---")
            for capa in self.capas:
                report.append(f"\n{capa.capa_id}: {capa.title}")
                report.append(f"  Status: {capa.status.value} | Priority: {capa.priority.value}")
                report.append(f"  Source: {capa.source}")
                report.append(f"  Initiated: {capa.initiated_date} by {capa.initiated_by}")
                report.append(f"  Target: {capa.target_completion}")
                if capa.root_cause:
                    report.append(f"  Root Cause: {capa.root_cause}")
                if capa.corrective_action:
                    report.append(f"  Corrective Action: {capa.corrective_action}")
                if capa.preventive_action:
                    report.append(f"  Preventive Action: {capa.preventive_action}")
                if capa.effectiveness_verified:
                    report.append(f"  Effectiveness Verified: {capa.effectiveness_date}")
            report.append("")

        report.append("=" * 70)

        return "\n".join(report)

    def generate_json_report(self, verbose: bool = False) -> Dict[str, Any]:
        """Generate comprehensive JSON report"""
        report = {
            "metadata": {
                "tool": "capa_tracker.py",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "generated_date": datetime.date.today().strftime('%Y-%m-%d'),
                "organization": self.metadata.get('organization', 'Not specified')
            },
            "summary": {
                "metrics": self.calculate_metrics(),
                "by_source": self.analyze_by_source(),
                "by_priority": self.analyze_by_priority(),
                "by_rca_method": self.analyze_by_rca_method(),
                "cost_impact": self.calculate_cost_impact(),
                "critical_count": len(self.get_critical_capas()),
                "overdue_count": len(self.get_overdue_capas())
            }
        }

        if verbose:
            report["detailed_data"] = {
                "all_capas": [asdict(capa) for capa in self.capas],
                "critical_capas": [asdict(capa) for capa in self.get_critical_capas()],
                "overdue_capas": [asdict(capa) for capa in self.get_overdue_capas()]
            }

            # Convert enums to strings
            for capa in report["detailed_data"]["all_capas"]:
                capa['priority'] = capa['priority'].value
                capa['status'] = capa['status'].value
                if capa['rca_method']:
                    capa['rca_method'] = capa['rca_method'].value

            for capa in report["detailed_data"]["critical_capas"]:
                capa['priority'] = capa['priority'].value
                capa['status'] = capa['status'].value
                if capa['rca_method']:
                    capa['rca_method'] = capa['rca_method'].value

            for capa in report["detailed_data"]["overdue_capas"]:
                capa['priority'] = capa['priority'].value
                capa['status'] = capa['status'].value
                if capa['rca_method']:
                    capa['rca_method'] = capa['rca_method'].value

        return report

    def generate_csv_report(self) -> str:
        """Generate CSV report"""
        output = []
        output.append("CAPA ID,Title,Source,Priority,Status,Initiated Date,Target Completion,Responsible,Root Cause,Effectiveness Verified,Cost Impact")

        for capa in self.capas:
            output.append(f'"{capa.capa_id}","{capa.title}","{capa.source}",{capa.priority.value},{capa.status.value},'
                         f'{capa.initiated_date},{capa.target_completion},"{capa.responsible_person}",'
                         f'"{capa.root_cause or ""}",{capa.effectiveness_verified},{capa.cost_impact}')

        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Track CAPA lifecycle including root cause analysis and effectiveness verification',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s capa_data.json
  %(prog)s capa_data.json --output json
  %(prog)s capa_data.json -o csv -f capa_report.csv -v

For more information:
ra-qm-team/capa-officer/SKILL.md
        """
    )

    parser.add_argument('input', help='CAPA data file (JSON format)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text')
    parser.add_argument('--file', '-f', help='Write output to file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Include detailed CAPA information')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        tracker = CAPATracker(str(input_path))

        if args.output == 'json':
            output = json.dumps(tracker.generate_json_report(verbose=args.verbose), indent=2)
        elif args.output == 'csv':
            output = tracker.generate_csv_report()
        else:
            output = tracker.generate_text_report(verbose=args.verbose)

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
