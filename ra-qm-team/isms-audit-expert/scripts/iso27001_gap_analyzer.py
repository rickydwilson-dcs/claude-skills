#!/usr/bin/env python3
"""
ISO 27001 Gap Analyzer - ISMS Audit Gap Analysis Tool
Performs comprehensive gap analysis between current state and ISO 27001:2022 requirements.

This script assesses security control implementation maturity across all 93 Annex A controls,
calculates gaps, prioritizes remediation efforts, and generates certification readiness reports.

Usage:
    python iso27001_gap_analyzer.py controls_assessment.json
    python iso27001_gap_analyzer.py data.json --output json
    python iso27001_gap_analyzer.py data.json -o csv -f gap_report.csv -v

Author: ISMS Audit Expert Team
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

class MaturityLevel(Enum):
    """ISO 27001 Control Maturity Levels"""
    NOT_IMPLEMENTED = 0  # Control does not exist
    AD_HOC = 1          # Reactive, informal processes
    DEFINED = 2         # Documented process exists
    CONSISTENT = 3      # Process consistently implemented
    MEASURED = 4        # Process measured and monitored
    OPTIMIZED = 5       # Continuous improvement in place

class GapSeverity(Enum):
    """Gap severity classification"""
    CRITICAL = "CRITICAL"      # Blocks certification
    HIGH = "HIGH"              # Major compliance issue
    MEDIUM = "MEDIUM"          # Moderate improvement needed
    LOW = "LOW"                # Minor enhancement
    NONE = "NONE"              # No gap

class ControlTheme(Enum):
    """ISO 27001:2022 Annex A Control Themes"""
    ORGANIZATIONAL = "Organizational"
    PEOPLE = "People"
    PHYSICAL = "Physical"
    TECHNOLOGICAL = "Technological"

@dataclass
class ControlAssessment:
    """Individual control assessment"""
    control_id: str
    control_name: str
    theme: ControlTheme
    description: str
    current_maturity: MaturityLevel
    target_maturity: MaturityLevel
    is_applicable: bool = True
    implementation_notes: str = ""
    evidence: List[str] = None
    responsible_person: str = ""

    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []

@dataclass
class GapAnalysis:
    """Gap analysis result for a control"""
    control_id: str
    control_name: str
    theme: str
    current_maturity: int
    target_maturity: int
    gap_score: int
    severity: GapSeverity
    certification_blocker: bool
    estimated_effort_hours: int
    remediation_priority: int
    recommendations: List[str]

class ISO27001GapAnalyzer:
    """ISO 27001:2022 Gap Analysis Engine"""

    # ISO 27001:2022 Annex A Control Framework (93 controls)
    CONTROL_FRAMEWORK = {
        "Organizational": [
            ("5.1", "Policies for information security", True),
            ("5.2", "Information security roles and responsibilities", True),
            ("5.3", "Segregation of duties", True),
            ("5.4", "Management responsibilities", True),
            ("5.5", "Contact with authorities", True),
            ("5.6", "Contact with special interest groups", True),
            ("5.7", "Threat intelligence", True),
            ("5.8", "Information security in project management", True),
            ("5.9", "Inventory of information and other associated assets", True),
            ("5.10", "Acceptable use of information and other associated assets", True),
            ("5.11", "Return of assets", True),
            ("5.12", "Classification of information", True),
            ("5.13", "Labelling of information", True),
            ("5.14", "Information transfer", True),
            ("5.15", "Access control", True),
            ("5.16", "Identity management", True),
            ("5.17", "Authentication information", True),
            ("5.18", "Access rights", True),
            ("5.19", "Information security in supplier relationships", True),
            ("5.20", "Addressing information security within supplier agreements", True),
            ("5.21", "Managing information security in the ICT supply chain", True),
            ("5.22", "Monitoring, review and change management of supplier services", True),
            ("5.23", "Information security for use of cloud services", True),
            ("5.24", "Information security incident management planning and preparation", True),
            ("5.25", "Assessment and decision on information security events", True),
            ("5.26", "Response to information security incidents", True),
            ("5.27", "Learning from information security incidents", True),
            ("5.28", "Collection of evidence", True),
            ("5.29", "Information security during disruption", True),
            ("5.30", "ICT readiness for business continuity", True),
            ("5.31", "Legal, statutory, regulatory and contractual requirements", True),
            ("5.32", "Intellectual property rights", False),
            ("5.33", "Protection of records", True),
            ("5.34", "Privacy and protection of PII", True),
            ("5.35", "Independent review of information security", True),
            ("5.36", "Compliance with policies, rules and standards for information security", True),
            ("5.37", "Documented operating procedures", True),
        ],
        "People": [
            ("6.1", "Screening", True),
            ("6.2", "Terms and conditions of employment", True),
            ("6.3", "Information security awareness, education and training", True),
            ("6.4", "Disciplinary process", True),
            ("6.5", "Responsibilities after termination or change of employment", True),
            ("6.6", "Confidentiality or non-disclosure agreements", True),
            ("6.7", "Remote working", True),
            ("6.8", "Information security event reporting", True),
        ],
        "Physical": [
            ("7.1", "Physical security perimeters", True),
            ("7.2", "Physical entry", True),
            ("7.3", "Securing offices, rooms and facilities", True),
            ("7.4", "Physical security monitoring", True),
            ("7.5", "Protecting against physical and environmental threats", True),
            ("7.6", "Working in secure areas", True),
            ("7.7", "Clear desk and clear screen", True),
            ("7.8", "Equipment siting and protection", True),
            ("7.9", "Security of assets off-premises", True),
            ("7.10", "Storage media", True),
            ("7.11", "Supporting utilities", True),
            ("7.12", "Cabling security", True),
            ("7.13", "Equipment maintenance", True),
            ("7.14", "Secure disposal or re-use of equipment", True),
        ],
        "Technological": [
            ("8.1", "User endpoint devices", True),
            ("8.2", "Privileged access rights", True),
            ("8.3", "Information access restriction", True),
            ("8.4", "Access to source code", True),
            ("8.5", "Secure authentication", True),
            ("8.6", "Capacity management", True),
            ("8.7", "Protection against malware", True),
            ("8.8", "Management of technical vulnerabilities", True),
            ("8.9", "Configuration management", True),
            ("8.10", "Information deletion", True),
            ("8.11", "Data masking", True),
            ("8.12", "Data leakage prevention", True),
            ("8.13", "Information backup", True),
            ("8.14", "Redundancy of information processing facilities", True),
            ("8.15", "Logging", True),
            ("8.16", "Monitoring activities", True),
            ("8.17", "Clock synchronization", True),
            ("8.18", "Use of privileged utility programs", True),
            ("8.19", "Installation of software on operational systems", True),
            ("8.20", "Networks security", True),
            ("8.21", "Security of network services", True),
            ("8.22", "Segregation of networks", True),
            ("8.23", "Web filtering", True),
            ("8.24", "Use of cryptography", True),
            ("8.25", "Secure development life cycle", True),
            ("8.26", "Application security requirements", True),
            ("8.27", "Secure system architecture and engineering principles", True),
            ("8.28", "Secure coding", True),
            ("8.29", "Security testing in development and acceptance", True),
            ("8.30", "Outsourced development", True),
            ("8.31", "Separation of development, test and production environments", True),
            ("8.32", "Change management", True),
            ("8.33", "Test information", True),
            ("8.34", "Protection of information systems during audit testing", True),
        ]
    }

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.assessments: List[ControlAssessment] = []
        self.metadata: Dict[str, Any] = {}
        self.load_data()

    def load_data(self):
        """Load control assessment data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)

                self.metadata = data.get('metadata', {})

                for assessment_data in data.get('controls', []):
                    # Convert string values to enums
                    assessment_data['theme'] = ControlTheme(assessment_data['theme'])
                    assessment_data['current_maturity'] = MaturityLevel(assessment_data['current_maturity'])
                    assessment_data['target_maturity'] = MaturityLevel(assessment_data['target_maturity'])

                    self.assessments.append(ControlAssessment(**assessment_data))

        except FileNotFoundError:
            print(f"Error: Input file not found: {self.data_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format: {e}", file=sys.stderr)
            sys.exit(3)
        except KeyError as e:
            print(f"Error: Missing required field in data: {e}", file=sys.stderr)
            sys.exit(3)
        except Exception as e:
            print(f"Error loading data: {e}", file=sys.stderr)
            sys.exit(1)

    def calculate_gap_severity(self, gap_score: int, control_id: str) -> GapSeverity:
        """Determine gap severity based on gap score and control criticality"""
        critical_controls = [
            "5.1", "5.2", "5.15", "5.16", "5.17", "5.18", "5.24", "5.25", "5.26",
            "6.3", "8.2", "8.5", "8.7", "8.8", "8.15", "8.16", "8.24"
        ]

        if gap_score == 0:
            return GapSeverity.NONE
        elif gap_score >= 4 or (gap_score >= 3 and control_id in critical_controls):
            return GapSeverity.CRITICAL
        elif gap_score >= 3:
            return GapSeverity.HIGH
        elif gap_score >= 2:
            return GapSeverity.MEDIUM
        else:
            return GapSeverity.LOW

    def estimate_remediation_effort(self, gap_score: int, theme: str) -> int:
        """Estimate effort in hours to close the gap"""
        base_hours = {
            "Organizational": 40,
            "People": 30,
            "Physical": 50,
            "Technological": 60
        }

        multiplier = {
            0: 0,
            1: 0.5,
            2: 1.0,
            3: 1.5,
            4: 2.5,
            5: 3.5
        }

        return int(base_hours.get(theme, 40) * multiplier.get(gap_score, 1.0))

    def generate_recommendations(self, assessment: ControlAssessment, gap_score: int) -> List[str]:
        """Generate remediation recommendations based on gap analysis"""
        recommendations = []
        current = assessment.current_maturity.value
        target = assessment.target_maturity.value

        if current == 0:
            recommendations.append(f"Implement {assessment.control_name} from scratch")
            recommendations.append("Document control procedures and assign ownership")
            recommendations.append("Establish baseline metrics for future monitoring")
        elif current == 1:
            recommendations.append("Formalize and document existing ad-hoc processes")
            recommendations.append("Define clear roles and responsibilities")
            recommendations.append("Create standard operating procedures")
        elif current == 2:
            recommendations.append("Train personnel on documented procedures")
            recommendations.append("Establish consistency in implementation across organization")
            recommendations.append("Implement control verification mechanisms")
        elif current == 3:
            recommendations.append("Establish KPIs and monitoring mechanisms")
            recommendations.append("Implement regular control effectiveness reviews")
            recommendations.append("Create dashboards for control performance tracking")
        elif current == 4:
            recommendations.append("Analyze control performance data for optimization opportunities")
            recommendations.append("Implement automation where possible")
            recommendations.append("Establish continuous improvement feedback loops")

        if gap_score >= 3:
            recommendations.append("PRIORITY: Address this gap before certification audit")

        return recommendations

    def analyze_control(self, assessment: ControlAssessment) -> GapAnalysis:
        """Perform gap analysis for a single control"""
        gap_score = assessment.target_maturity.value - assessment.current_maturity.value
        severity = self.calculate_gap_severity(gap_score, assessment.control_id)
        certification_blocker = (severity == GapSeverity.CRITICAL or
                                (severity == GapSeverity.HIGH and gap_score >= 3))
        effort = self.estimate_remediation_effort(gap_score, assessment.theme.value)
        recommendations = self.generate_recommendations(assessment, gap_score)

        # Calculate priority (1-100, higher = more urgent)
        priority = 0
        if certification_blocker:
            priority += 50
        priority += (gap_score * 10)
        priority += (5 - assessment.current_maturity.value) * 5

        return GapAnalysis(
            control_id=assessment.control_id,
            control_name=assessment.control_name,
            theme=assessment.theme.value,
            current_maturity=assessment.current_maturity.value,
            target_maturity=assessment.target_maturity.value,
            gap_score=gap_score,
            severity=severity,
            certification_blocker=certification_blocker,
            estimated_effort_hours=effort,
            remediation_priority=priority,
            recommendations=recommendations
        )

    def analyze_all_controls(self) -> List[GapAnalysis]:
        """Perform gap analysis across all controls"""
        return [self.analyze_control(assessment) for assessment in self.assessments]

    def calculate_theme_scores(self) -> Dict[str, Dict[str, float]]:
        """Calculate maturity scores by theme"""
        theme_scores = {theme.value: {"current": [], "target": [], "gap": []}
                       for theme in ControlTheme}

        for assessment in self.assessments:
            if assessment.is_applicable:
                theme = assessment.theme.value
                theme_scores[theme]["current"].append(assessment.current_maturity.value)
                theme_scores[theme]["target"].append(assessment.target_maturity.value)
                theme_scores[theme]["gap"].append(
                    assessment.target_maturity.value - assessment.current_maturity.value
                )

        results = {}
        for theme, scores in theme_scores.items():
            if scores["current"]:
                results[theme] = {
                    "avg_current_maturity": round(sum(scores["current"]) / len(scores["current"]), 2),
                    "avg_target_maturity": round(sum(scores["target"]) / len(scores["target"]), 2),
                    "avg_gap": round(sum(scores["gap"]) / len(scores["gap"]), 2),
                    "control_count": len(scores["current"])
                }

        return results

    def calculate_certification_readiness(self, gaps: List[GapAnalysis]) -> Dict[str, Any]:
        """Assess overall ISO 27001 certification readiness"""
        total_controls = len([a for a in self.assessments if a.is_applicable])
        blockers = [g for g in gaps if g.certification_blocker]
        critical_gaps = [g for g in gaps if g.severity == GapSeverity.CRITICAL]
        high_gaps = [g for g in gaps if g.severity == GapSeverity.HIGH]

        # Calculate readiness percentage
        controls_at_target = len([a for a in self.assessments
                                 if a.current_maturity.value >= a.target_maturity.value])
        readiness_percentage = (controls_at_target / total_controls * 100) if total_controls > 0 else 0

        # Determine certification readiness status
        if len(blockers) == 0:
            status = "READY"
        elif len(blockers) <= 5:
            status = "NEAR_READY"
        elif len(blockers) <= 15:
            status = "MODERATE_GAPS"
        else:
            status = "SIGNIFICANT_GAPS"

        total_effort = sum(g.estimated_effort_hours for g in gaps)

        return {
            "status": status,
            "readiness_percentage": round(readiness_percentage, 1),
            "total_applicable_controls": total_controls,
            "controls_at_target": controls_at_target,
            "certification_blockers": len(blockers),
            "critical_gaps": len(critical_gaps),
            "high_gaps": len(high_gaps),
            "total_remediation_hours": total_effort,
            "estimated_weeks": round(total_effort / 40, 1)
        }

    def generate_remediation_roadmap(self, gaps: List[GapAnalysis]) -> Dict[str, List[str]]:
        """Generate phased remediation roadmap"""
        # Sort gaps by priority
        sorted_gaps = sorted(gaps, key=lambda g: g.remediation_priority, reverse=True)

        roadmap = {
            "Phase 1 - Critical (Weeks 1-4)": [],
            "Phase 2 - High Priority (Weeks 5-12)": [],
            "Phase 3 - Medium Priority (Weeks 13-24)": [],
            "Phase 4 - Low Priority (Weeks 25+)": []
        }

        for gap in sorted_gaps:
            if gap.certification_blocker:
                roadmap["Phase 1 - Critical (Weeks 1-4)"].append(
                    f"{gap.control_id}: {gap.control_name} (Gap: {gap.gap_score}, Effort: {gap.estimated_effort_hours}h)"
                )
            elif gap.severity == GapSeverity.HIGH:
                roadmap["Phase 2 - High Priority (Weeks 5-12)"].append(
                    f"{gap.control_id}: {gap.control_name} (Gap: {gap.gap_score}, Effort: {gap.estimated_effort_hours}h)"
                )
            elif gap.severity == GapSeverity.MEDIUM:
                roadmap["Phase 3 - Medium Priority (Weeks 13-24)"].append(
                    f"{gap.control_id}: {gap.control_name} (Gap: {gap.gap_score}, Effort: {gap.estimated_effort_hours}h)"
                )
            elif gap.gap_score > 0:
                roadmap["Phase 4 - Low Priority (Weeks 25+)"].append(
                    f"{gap.control_id}: {gap.control_name} (Gap: {gap.gap_score}, Effort: {gap.estimated_effort_hours}h)"
                )

        return roadmap

    def generate_text_report(self, verbose: bool = False) -> str:
        """Generate comprehensive text report"""
        report = []
        report.append("=" * 80)
        report.append("ISO 27001:2022 GAP ANALYSIS REPORT")
        report.append("Information Security Management System (ISMS) Audit")
        report.append("=" * 80)
        report.append(f"Report Generated: {datetime.date.today()}")
        report.append(f"Organization: {self.metadata.get('organization', 'Not specified')}")
        report.append(f"Audit Date: {self.metadata.get('audit_date', 'Not specified')}")
        report.append(f"Auditor: {self.metadata.get('auditor', 'Not specified')}")
        report.append("")

        gaps = self.analyze_all_controls()
        readiness = self.calculate_certification_readiness(gaps)

        # Executive Summary
        report.append("=" * 80)
        report.append("EXECUTIVE SUMMARY")
        report.append("=" * 80)
        report.append(f"Certification Readiness: {readiness['status']}")
        report.append(f"Overall Maturity: {readiness['readiness_percentage']}%")
        report.append(f"Total Controls Assessed: {readiness['total_applicable_controls']}")
        report.append(f"Controls at Target Maturity: {readiness['controls_at_target']}")
        report.append("")
        report.append(f"Certification Blockers: {readiness['certification_blockers']} controls")
        report.append(f"Critical Gaps: {readiness['critical_gaps']} controls")
        report.append(f"High Priority Gaps: {readiness['high_gaps']} controls")
        report.append("")
        report.append(f"Total Remediation Effort: {readiness['total_remediation_hours']} hours")
        report.append(f"Estimated Timeline: {readiness['estimated_weeks']} weeks")
        report.append("")

        # Theme Analysis
        report.append("=" * 80)
        report.append("MATURITY BY CONTROL THEME")
        report.append("=" * 80)
        theme_scores = self.calculate_theme_scores()
        for theme, scores in theme_scores.items():
            report.append(f"\n{theme} Controls:")
            report.append(f"  Current Maturity: {scores['avg_current_maturity']}/5.0")
            report.append(f"  Target Maturity:  {scores['avg_target_maturity']}/5.0")
            report.append(f"  Average Gap:      {scores['avg_gap']}")
            report.append(f"  Control Count:    {scores['control_count']}")
        report.append("")

        # Critical Gaps
        critical_gaps = [g for g in gaps if g.certification_blocker]
        if critical_gaps:
            report.append("=" * 80)
            report.append(f"CERTIFICATION BLOCKERS: {len(critical_gaps)} CONTROLS")
            report.append("=" * 80)
            report.append("These gaps MUST be addressed before certification audit:\n")
            for gap in sorted(critical_gaps, key=lambda g: g.remediation_priority, reverse=True):
                report.append(f"{gap.control_id}: {gap.control_name}")
                report.append(f"  Theme: {gap.theme}")
                report.append(f"  Current Maturity: Level {gap.current_maturity} → Target: Level {gap.target_maturity}")
                report.append(f"  Gap Score: {gap.gap_score} | Severity: {gap.severity.value}")
                report.append(f"  Estimated Effort: {gap.estimated_effort_hours} hours")
                report.append(f"  Priority Score: {gap.remediation_priority}/100")
                report.append("")

        # Remediation Roadmap
        report.append("=" * 80)
        report.append("REMEDIATION ROADMAP")
        report.append("=" * 80)
        roadmap = self.generate_remediation_roadmap(gaps)
        for phase, controls in roadmap.items():
            if controls:
                report.append(f"\n{phase}:")
                report.append(f"  Controls to Address: {len(controls)}")
                if verbose or "Critical" in phase:
                    for control in controls[:10]:  # Limit to first 10 in text report
                        report.append(f"  • {control}")
                    if len(controls) > 10:
                        report.append(f"  ... and {len(controls) - 10} more controls")
        report.append("")

        # Detailed Gap Analysis
        if verbose:
            report.append("=" * 80)
            report.append("DETAILED GAP ANALYSIS")
            report.append("=" * 80)

            for theme in ControlTheme:
                theme_gaps = [g for g in gaps if g.theme == theme.value and g.gap_score > 0]
                if theme_gaps:
                    report.append(f"\n{theme.value} Controls ({len(theme_gaps)} gaps):")
                    report.append("-" * 80)
                    for gap in theme_gaps:
                        report.append(f"\n{gap.control_id}: {gap.control_name}")
                        report.append(f"  Maturity: L{gap.current_maturity} → L{gap.target_maturity} | Gap: {gap.gap_score}")
                        report.append(f"  Severity: {gap.severity.value} | Effort: {gap.estimated_effort_hours}h")
                        report.append(f"  Recommendations:")
                        for rec in gap.recommendations:
                            report.append(f"    • {rec}")

        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        return "\n".join(report)

    def generate_json_report(self, verbose: bool = False) -> Dict[str, Any]:
        """Generate comprehensive JSON report"""
        gaps = self.analyze_all_controls()

        report = {
            "metadata": {
                "tool": "iso27001_gap_analyzer.py",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "generated_date": datetime.date.today().strftime('%Y-%m-%d'),
                "organization": self.metadata.get('organization', 'Not specified'),
                "audit_date": self.metadata.get('audit_date', 'Not specified'),
                "auditor": self.metadata.get('auditor', 'Not specified')
            },
            "summary": {
                "certification_readiness": self.calculate_certification_readiness(gaps),
                "theme_maturity": self.calculate_theme_scores(),
                "gap_distribution": {
                    "critical": len([g for g in gaps if g.severity == GapSeverity.CRITICAL]),
                    "high": len([g for g in gaps if g.severity == GapSeverity.HIGH]),
                    "medium": len([g for g in gaps if g.severity == GapSeverity.MEDIUM]),
                    "low": len([g for g in gaps if g.severity == GapSeverity.LOW]),
                    "none": len([g for g in gaps if g.severity == GapSeverity.NONE])
                }
            },
            "remediation_roadmap": self.generate_remediation_roadmap(gaps)
        }

        if verbose:
            report["detailed_gaps"] = []
            for gap in gaps:
                gap_dict = asdict(gap)
                gap_dict['severity'] = gap.severity.value
                report["detailed_gaps"].append(gap_dict)

        return report

    def generate_csv_report(self) -> str:
        """Generate CSV report"""
        output = []
        output.append("Control ID,Control Name,Theme,Current Maturity,Target Maturity,Gap Score,Severity,Certification Blocker,Estimated Effort (Hours),Priority")

        gaps = self.analyze_all_controls()
        for gap in sorted(gaps, key=lambda g: g.remediation_priority, reverse=True):
            output.append(
                f'"{gap.control_id}","{gap.control_name}",{gap.theme},'
                f'{gap.current_maturity},{gap.target_maturity},{gap.gap_score},'
                f'{gap.severity.value},{gap.certification_blocker},'
                f'{gap.estimated_effort_hours},{gap.remediation_priority}'
            )

        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Perform ISO 27001:2022 gap analysis and generate certification readiness report',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s controls_assessment.json
  %(prog)s assessment.json --output json
  %(prog)s assessment.json -o csv -f gap_report.csv -v

Maturity Levels:
  0 - Not Implemented: Control does not exist
  1 - Ad-hoc: Reactive, informal processes
  2 - Defined: Documented process exists
  3 - Consistent: Process consistently implemented
  4 - Measured: Process measured and monitored
  5 - Optimized: Continuous improvement in place

For more information:
ra-qm-team/isms-audit-expert/SKILL.md
        """
    )

    parser.add_argument('input', help='Control assessment data file (JSON format)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'],
                       default='text', help='Output format (default: text)')
    parser.add_argument('--file', '-f', help='Write output to file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Include detailed gap analysis and recommendations')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        analyzer = ISO27001GapAnalyzer(str(input_path))

        if args.output == 'json':
            output = json.dumps(analyzer.generate_json_report(verbose=args.verbose), indent=2)
        elif args.output == 'csv':
            output = analyzer.generate_csv_report()
        else:
            output = analyzer.generate_text_report(verbose=args.verbose)

        if args.file:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Gap analysis report saved to: {args.file}")
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
