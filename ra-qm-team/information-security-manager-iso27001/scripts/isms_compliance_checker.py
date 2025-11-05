#!/usr/bin/env python3
"""
ISMS Compliance Checker - ISO 27001:2022 Assessment Tool
Evaluates ISO 27001:2022 Annex A controls implementation and security posture.

This script assesses the implementation status of all 93 ISO 27001:2022 Annex A controls
across four control themes (Organizational, People, Physical, Technological) and generates
comprehensive compliance reports with gap analysis and remediation priorities.

Usage:
    python isms_compliance_checker.py assessment.json
    python isms_compliance_checker.py assessment.json --output json
    python isms_compliance_checker.py assessment.json -o csv -f compliance_report.csv

Author: Information Security Manager - ISO 27001
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

class ControlStatus(Enum):
    """Control implementation status"""
    IMPLEMENTED = "IMPLEMENTED"
    PARTIALLY_IMPLEMENTED = "PARTIALLY_IMPLEMENTED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    PLANNED = "PLANNED"

class ControlTheme(Enum):
    """ISO 27001:2022 control themes"""
    ORGANIZATIONAL = "ORGANIZATIONAL"
    PEOPLE = "PEOPLE"
    PHYSICAL = "PHYSICAL"
    TECHNOLOGICAL = "TECHNOLOGICAL"

class EffectivenessRating(Enum):
    """Control effectiveness ratings"""
    EFFECTIVE = "EFFECTIVE"
    PARTIALLY_EFFECTIVE = "PARTIALLY_EFFECTIVE"
    INEFFECTIVE = "INEFFECTIVE"
    NOT_TESTED = "NOT_TESTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class Priority(Enum):
    """Remediation priority levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class SecurityControl:
    """ISO 27001:2022 Annex A security control"""
    control_id: str
    control_name: str
    theme: ControlTheme
    status: ControlStatus
    effectiveness: EffectivenessRating
    implementation_date: Optional[str] = None
    evidence: str = ""
    gaps: str = ""
    remediation_plan: str = ""
    remediation_priority: Optional[Priority] = None
    responsible_person: str = ""
    target_date: Optional[str] = None
    notes: str = ""

class ISMSComplianceChecker:
    """ISO 27001:2022 compliance assessment and reporting"""

    # ISO 27001:2022 Annex A control counts
    CONTROL_COUNTS = {
        ControlTheme.ORGANIZATIONAL: 37,
        ControlTheme.PEOPLE: 8,
        ControlTheme.PHYSICAL: 14,
        ControlTheme.TECHNOLOGICAL: 34
    }

    def __init__(self, assessment_file: str):
        self.assessment_file = assessment_file
        self.controls: List[SecurityControl] = []
        self.metadata: Dict[str, Any] = {}
        self.load_assessment()

    def load_assessment(self):
        """Load ISO 27001 assessment data from JSON file"""
        try:
            with open(self.assessment_file, 'r') as f:
                data = json.load(f)

                self.metadata = data.get('metadata', {})

                for control_data in data.get('controls', []):
                    control_data['theme'] = ControlTheme(control_data['theme'])
                    control_data['status'] = ControlStatus(control_data['status'])
                    control_data['effectiveness'] = EffectivenessRating(control_data['effectiveness'])
                    if control_data.get('remediation_priority'):
                        control_data['remediation_priority'] = Priority(control_data['remediation_priority'])
                    self.controls.append(SecurityControl(**control_data))

        except FileNotFoundError:
            print(f"Error: Assessment file not found: {self.assessment_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}", file=sys.stderr)
            sys.exit(3)
        except Exception as e:
            print(f"Error loading assessment data: {e}", file=sys.stderr)
            sys.exit(1)

    def calculate_theme_compliance(self, theme: ControlTheme) -> Dict[str, Any]:
        """Calculate compliance percentage for a specific theme"""
        theme_controls = [c for c in self.controls if c.theme == theme]
        total = len(theme_controls)

        if total == 0:
            return {
                "total_controls": 0,
                "implemented": 0,
                "partially_implemented": 0,
                "not_implemented": 0,
                "not_applicable": 0,
                "planned": 0,
                "compliance_percentage": 0.0,
                "effective_controls": 0,
                "effectiveness_rate": 0.0
            }

        implemented = len([c for c in theme_controls if c.status == ControlStatus.IMPLEMENTED])
        partially = len([c for c in theme_controls if c.status == ControlStatus.PARTIALLY_IMPLEMENTED])
        not_implemented = len([c for c in theme_controls if c.status == ControlStatus.NOT_IMPLEMENTED])
        not_applicable = len([c for c in theme_controls if c.status == ControlStatus.NOT_APPLICABLE])
        planned = len([c for c in theme_controls if c.status == ControlStatus.PLANNED])

        # Calculate compliance (excluding not applicable)
        applicable = total - not_applicable
        if applicable > 0:
            compliance_percentage = ((implemented + (partially * 0.5)) / applicable) * 100
        else:
            compliance_percentage = 100.0

        # Calculate effectiveness
        testable = [c for c in theme_controls if c.status == ControlStatus.IMPLEMENTED]
        effective = len([c for c in testable if c.effectiveness == EffectivenessRating.EFFECTIVE])
        effectiveness_rate = (effective / len(testable) * 100) if testable else 0.0

        return {
            "total_controls": total,
            "implemented": implemented,
            "partially_implemented": partially,
            "not_implemented": not_implemented,
            "not_applicable": not_applicable,
            "planned": planned,
            "compliance_percentage": round(compliance_percentage, 1),
            "effective_controls": effective,
            "effectiveness_rate": round(effectiveness_rate, 1)
        }

    def calculate_overall_compliance(self) -> Dict[str, Any]:
        """Calculate overall ISMS compliance metrics"""
        total = len(self.controls)
        if total == 0:
            return {
                "total_controls": 0,
                "compliance_percentage": 0.0,
                "maturity_level": "NONE"
            }

        implemented = len([c for c in self.controls if c.status == ControlStatus.IMPLEMENTED])
        partially = len([c for c in self.controls if c.status == ControlStatus.PARTIALLY_IMPLEMENTED])
        not_applicable = len([c for c in self.controls if c.status == ControlStatus.NOT_APPLICABLE])

        # Calculate overall compliance
        applicable = total - not_applicable
        if applicable > 0:
            compliance = ((implemented + (partially * 0.5)) / applicable) * 100
        else:
            compliance = 100.0

        # Determine maturity level
        if compliance >= 95:
            maturity = "OPTIMIZED"
        elif compliance >= 85:
            maturity = "MANAGED"
        elif compliance >= 70:
            maturity = "DEFINED"
        elif compliance >= 50:
            maturity = "DEVELOPING"
        else:
            maturity = "INITIAL"

        return {
            "total_controls": total,
            "applicable_controls": applicable,
            "implemented": implemented,
            "partially_implemented": partially,
            "not_implemented": len([c for c in self.controls if c.status == ControlStatus.NOT_IMPLEMENTED]),
            "compliance_percentage": round(compliance, 1),
            "maturity_level": maturity
        }

    def identify_critical_gaps(self) -> List[SecurityControl]:
        """Identify critical gaps requiring immediate attention"""
        critical_gaps = []

        for control in self.controls:
            # Critical if not implemented or ineffective high-priority controls
            is_gap = (
                control.status == ControlStatus.NOT_IMPLEMENTED or
                control.status == ControlStatus.PLANNED or
                (control.status == ControlStatus.PARTIALLY_IMPLEMENTED and
                 control.remediation_priority == Priority.CRITICAL) or
                (control.effectiveness == EffectivenessRating.INEFFECTIVE)
            )

            if is_gap and control.status != ControlStatus.NOT_APPLICABLE:
                critical_gaps.append(control)

        # Sort by priority
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
            None: 4
        }
        critical_gaps.sort(key=lambda c: priority_order.get(c.remediation_priority, 4))

        return critical_gaps

    def generate_remediation_roadmap(self) -> Dict[str, List[SecurityControl]]:
        """Generate prioritized remediation roadmap"""
        gaps = self.identify_critical_gaps()

        roadmap = {
            "immediate": [],      # Critical priority
            "short_term": [],     # High priority
            "medium_term": [],    # Medium priority
            "long_term": []       # Low priority
        }

        for gap in gaps:
            if gap.remediation_priority == Priority.CRITICAL:
                roadmap["immediate"].append(gap)
            elif gap.remediation_priority == Priority.HIGH:
                roadmap["short_term"].append(gap)
            elif gap.remediation_priority == Priority.MEDIUM:
                roadmap["medium_term"].append(gap)
            else:
                roadmap["long_term"].append(gap)

        return roadmap

    def calculate_risk_exposure(self) -> Dict[str, Any]:
        """Calculate security risk exposure based on control gaps"""
        gaps = self.identify_critical_gaps()

        # Count high-risk areas
        critical_count = len([g for g in gaps if g.remediation_priority == Priority.CRITICAL])
        high_count = len([g for g in gaps if g.remediation_priority == Priority.HIGH])

        # Determine overall risk level
        if critical_count > 10 or high_count > 20:
            risk_level = "CRITICAL"
        elif critical_count > 5 or high_count > 10:
            risk_level = "HIGH"
        elif critical_count > 0 or high_count > 5:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "risk_level": risk_level,
            "critical_gaps": critical_count,
            "high_gaps": high_count,
            "total_gaps": len(gaps),
            "risk_score": min(100, critical_count * 10 + high_count * 5)
        }

    def generate_text_report(self, verbose: bool = False) -> str:
        """Generate comprehensive text compliance report"""
        report = []
        report.append("=" * 80)
        report.append("ISO 27001:2022 INFORMATION SECURITY MANAGEMENT SYSTEM")
        report.append("COMPLIANCE ASSESSMENT REPORT")
        report.append("=" * 80)
        report.append(f"Assessment Date: {datetime.date.today()}")
        report.append(f"Organization: {self.metadata.get('organization', 'Not specified')}")
        report.append(f"Scope: {self.metadata.get('scope', 'Not specified')}")
        report.append("")

        # Executive Summary
        report.append("--- EXECUTIVE SUMMARY ---")
        overall = self.calculate_overall_compliance()
        risk = self.calculate_risk_exposure()
        report.append(f"Overall Compliance: {overall['compliance_percentage']}%")
        report.append(f"Maturity Level: {overall['maturity_level']}")
        report.append(f"Risk Level: {risk['risk_level']}")
        report.append(f"Total Controls Assessed: {overall['total_controls']}")
        report.append(f"Critical Gaps: {risk['critical_gaps']}")
        report.append("")

        # Compliance by Theme
        report.append("--- COMPLIANCE BY CONTROL THEME ---")
        for theme in ControlTheme:
            metrics = self.calculate_theme_compliance(theme)
            report.append(f"\n{theme.value} Controls (Expected: {self.CONTROL_COUNTS[theme]})")
            report.append(f"  Total Assessed: {metrics['total_controls']}")
            report.append(f"  Compliance: {metrics['compliance_percentage']}%")
            report.append(f"  Implemented: {metrics['implemented']}")
            report.append(f"  Partially Implemented: {metrics['partially_implemented']}")
            report.append(f"  Not Implemented: {metrics['not_implemented']}")
            report.append(f"  Effectiveness Rate: {metrics['effectiveness_rate']}%")
        report.append("")

        # Critical Gaps
        gaps = self.identify_critical_gaps()
        if gaps:
            report.append(f"--- CRITICAL GAPS IDENTIFIED: {len(gaps)} ---")
            for gap in gaps[:10]:  # Show top 10
                priority = gap.remediation_priority.value if gap.remediation_priority else "UNDEFINED"
                report.append(f"\n  [{priority}] {gap.control_id}: {gap.control_name}")
                report.append(f"  Status: {gap.status.value}")
                report.append(f"  Theme: {gap.theme.value}")
                if gap.gaps:
                    report.append(f"  Gap: {gap.gaps}")
                if gap.remediation_plan:
                    report.append(f"  Remediation: {gap.remediation_plan}")
                if gap.target_date:
                    report.append(f"  Target: {gap.target_date}")

            if len(gaps) > 10:
                report.append(f"\n  ... and {len(gaps) - 10} more gaps")
            report.append("")

        # Remediation Roadmap
        report.append("--- REMEDIATION ROADMAP ---")
        roadmap = self.generate_remediation_roadmap()
        report.append(f"Immediate Action Required (Critical): {len(roadmap['immediate'])} controls")
        report.append(f"Short-term (0-3 months): {len(roadmap['short_term'])} controls")
        report.append(f"Medium-term (3-6 months): {len(roadmap['medium_term'])} controls")
        report.append(f"Long-term (6-12 months): {len(roadmap['long_term'])} controls")
        report.append("")

        # Risk Assessment
        report.append("--- SECURITY RISK ASSESSMENT ---")
        report.append(f"Overall Risk Level: {risk['risk_level']}")
        report.append(f"Risk Score: {risk['risk_score']}/100")
        report.append(f"Controls with Critical Priority: {risk['critical_gaps']}")
        report.append(f"Controls with High Priority: {risk['high_gaps']}")
        report.append("")

        # Recommendations
        report.append("--- KEY RECOMMENDATIONS ---")
        if risk['risk_level'] in ['CRITICAL', 'HIGH']:
            report.append("  1. Address all critical priority gaps immediately")
            report.append("  2. Establish incident response procedures for high-risk areas")
            report.append("  3. Conduct security awareness training for all personnel")

        if overall['compliance_percentage'] < 70:
            report.append("  4. Develop comprehensive control implementation plan")
            report.append("  5. Allocate resources for security control deployment")

        report.append("  6. Schedule regular compliance reviews and audits")
        report.append("  7. Implement continuous monitoring for critical controls")
        report.append("")

        # Detailed Control List (verbose mode)
        if verbose:
            report.append("--- DETAILED CONTROL ASSESSMENT ---")
            by_theme = {}
            for control in self.controls:
                if control.theme not in by_theme:
                    by_theme[control.theme] = []
                by_theme[control.theme].append(control)

            for theme in ControlTheme:
                if theme in by_theme:
                    report.append(f"\n{theme.value} CONTROLS:")
                    for control in by_theme[theme]:
                        report.append(f"\n  {control.control_id}: {control.control_name}")
                        report.append(f"  Status: {control.status.value}")
                        report.append(f"  Effectiveness: {control.effectiveness.value}")
                        if control.evidence:
                            report.append(f"  Evidence: {control.evidence}")
                        if control.gaps:
                            report.append(f"  Gaps: {control.gaps}")
                        if control.responsible_person:
                            report.append(f"  Responsible: {control.responsible_person}")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)

    def generate_json_report(self, verbose: bool = False) -> Dict[str, Any]:
        """Generate comprehensive JSON compliance report"""
        report = {
            "metadata": {
                "tool": "isms_compliance_checker.py",
                "version": "1.0.0",
                "standard": "ISO 27001:2022",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "assessment_date": datetime.date.today().strftime('%Y-%m-%d'),
                "organization": self.metadata.get('organization', 'Not specified'),
                "scope": self.metadata.get('scope', 'Not specified')
            },
            "executive_summary": {
                "overall_compliance": self.calculate_overall_compliance(),
                "risk_assessment": self.calculate_risk_exposure()
            },
            "compliance_by_theme": {},
            "critical_gaps_count": len(self.identify_critical_gaps()),
            "remediation_roadmap": {}
        }

        # Theme compliance
        for theme in ControlTheme:
            report["compliance_by_theme"][theme.value] = self.calculate_theme_compliance(theme)

        # Remediation roadmap summary
        roadmap = self.generate_remediation_roadmap()
        report["remediation_roadmap"] = {
            "immediate": len(roadmap["immediate"]),
            "short_term": len(roadmap["short_term"]),
            "medium_term": len(roadmap["medium_term"]),
            "long_term": len(roadmap["long_term"])
        }

        # Detailed data (verbose mode)
        if verbose:
            gaps = self.identify_critical_gaps()
            report["detailed_data"] = {
                "critical_gaps": [asdict(gap) for gap in gaps],
                "all_controls": [asdict(control) for control in self.controls],
                "roadmap_details": {
                    "immediate": [asdict(c) for c in roadmap["immediate"]],
                    "short_term": [asdict(c) for c in roadmap["short_term"]],
                    "medium_term": [asdict(c) for c in roadmap["medium_term"]],
                    "long_term": [asdict(c) for c in roadmap["long_term"]]
                }
            }

            # Convert enums to strings
            for control in report["detailed_data"]["all_controls"]:
                control['theme'] = control['theme'].value
                control['status'] = control['status'].value
                control['effectiveness'] = control['effectiveness'].value
                if control['remediation_priority']:
                    control['remediation_priority'] = control['remediation_priority'].value

            for gap in report["detailed_data"]["critical_gaps"]:
                gap['theme'] = gap['theme'].value
                gap['status'] = gap['status'].value
                gap['effectiveness'] = gap['effectiveness'].value
                if gap['remediation_priority']:
                    gap['remediation_priority'] = gap['remediation_priority'].value

            for phase in ['immediate', 'short_term', 'medium_term', 'long_term']:
                for control in report["detailed_data"]["roadmap_details"][phase]:
                    control['theme'] = control['theme'].value
                    control['status'] = control['status'].value
                    control['effectiveness'] = control['effectiveness'].value
                    if control['remediation_priority']:
                        control['remediation_priority'] = control['remediation_priority'].value

        return report

    def generate_csv_report(self) -> str:
        """Generate CSV compliance report"""
        output = []
        output.append("Control ID,Control Name,Theme,Status,Effectiveness,Priority,Gaps,Target Date,Responsible")

        for control in self.controls:
            priority = control.remediation_priority.value if control.remediation_priority else ""
            output.append(
                f'"{control.control_id}","{control.control_name}",{control.theme.value},'
                f'{control.status.value},{control.effectiveness.value},{priority},'
                f'"{control.gaps}",{control.target_date or ""},"{control.responsible_person}"'
            )

        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Assess ISO 27001:2022 Annex A controls implementation and security posture',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s assessment.json
  %(prog)s assessment.json --output json
  %(prog)s assessment.json -o csv -f compliance_report.csv -v

For more information:
ra-qm-team/information-security-manager-iso27001/SKILL.md
        """
    )

    parser.add_argument('input', help='ISO 27001 assessment data file (JSON format)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'],
                       default='text', help='Output format (default: text)')
    parser.add_argument('--file', '-f', help='Write output to file instead of stdout')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Include detailed control information')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        if not input_path.is_file():
            print(f"Error: Path is not a file: {args.input}", file=sys.stderr)
            sys.exit(1)

        checker = ISMSComplianceChecker(str(input_path))

        if args.output == 'json':
            output = json.dumps(checker.generate_json_report(verbose=args.verbose), indent=2)
        elif args.output == 'csv':
            output = checker.generate_csv_report()
        else:
            output = checker.generate_text_report(verbose=args.verbose)

        if args.file:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Compliance report saved to: {args.file}")
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
