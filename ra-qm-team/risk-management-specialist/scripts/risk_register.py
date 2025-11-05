#!/usr/bin/env python3
"""
Risk Register - ISO 14971 Risk Management
Manages risk assessment, risk mitigation tracking, and risk-benefit analysis.

This script implements ISO 14971 medical device risk management including
FMEA/FMECA analysis, risk evaluation, and residual risk assessment.

Usage:
    python risk_register.py risk_data.json
    python risk_register.py data.json --output json
    python risk_register.py data.json -o csv -f risk_report.csv

Author: Risk Management Team
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

class RiskSeverity(Enum):
    CATASTROPHIC = "CATASTROPHIC"  # Score: 5
    CRITICAL = "CRITICAL"           # Score: 4
    SERIOUS = "SERIOUS"             # Score: 3
    MINOR = "MINOR"                 # Score: 2
    NEGLIGIBLE = "NEGLIGIBLE"       # Score: 1

class RiskProbability(Enum):
    FREQUENT = "FREQUENT"           # Score: 5
    PROBABLE = "PROBABLE"           # Score: 4
    OCCASIONAL = "OCCASIONAL"       # Score: 3
    REMOTE = "REMOTE"               # Score: 2
    IMPROBABLE = "IMPROBABLE"       # Score: 1

class RiskLevel(Enum):
    UNACCEPTABLE = "UNACCEPTABLE"   # RPN >= 15
    HIGH = "HIGH"                    # RPN 10-14
    MEDIUM = "MEDIUM"                # RPN 5-9
    LOW = "LOW"                      # RPN 1-4

@dataclass
class RiskRecord:
    risk_id: str
    hazard: str
    hazardous_situation: str
    harm: str
    severity_initial: RiskSeverity
    probability_initial: RiskProbability
    risk_control_measures: str
    severity_residual: RiskSeverity
    probability_residual: RiskProbability
    benefit_analysis: str = ""
    risk_acceptable: bool = False
    verification_method: str = ""
    verification_status: str = "PENDING"
    responsible_person: str = ""
    target_date: str = ""
    notes: str = ""

    def calculate_rpn(self, severity: RiskSeverity, probability: RiskProbability) -> int:
        """Calculate Risk Priority Number"""
        severity_scores = {
            RiskSeverity.CATASTROPHIC: 5,
            RiskSeverity.CRITICAL: 4,
            RiskSeverity.SERIOUS: 3,
            RiskSeverity.MINOR: 2,
            RiskSeverity.NEGLIGIBLE: 1
        }
        prob_scores = {
            RiskProbability.FREQUENT: 5,
            RiskProbability.PROBABLE: 4,
            RiskProbability.OCCASIONAL: 3,
            RiskProbability.REMOTE: 2,
            RiskProbability.IMPROBABLE: 1
        }
        return severity_scores[severity] * prob_scores[probability]

    def get_risk_level(self, rpn: int) -> RiskLevel:
        """Determine risk level from RPN"""
        if rpn >= 15:
            return RiskLevel.UNACCEPTABLE
        elif rpn >= 10:
            return RiskLevel.HIGH
        elif rpn >= 5:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

class RiskRegister:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.risks: List[RiskRecord] = []
        self.metadata: Dict[str, Any] = {}
        self.load_data()

    def load_data(self):
        """Load risk data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.metadata = data.get('metadata', {})

                for risk_data in data.get('risks', []):
                    risk_data['severity_initial'] = RiskSeverity(risk_data['severity_initial'])
                    risk_data['probability_initial'] = RiskProbability(risk_data['probability_initial'])
                    risk_data['severity_residual'] = RiskSeverity(risk_data['severity_residual'])
                    risk_data['probability_residual'] = RiskProbability(risk_data['probability_residual'])
                    self.risks.append(RiskRecord(**risk_data))

        except FileNotFoundError:
            print(f"Error: Data file not found: {self.data_file}", file=sys.stderr)
            sys.exit(1)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error: Invalid data format: {e}", file=sys.stderr)
            sys.exit(3)

    def analyze_risk_levels(self) -> Dict[str, Any]:
        """Analyze initial vs residual risk levels"""
        initial_levels = {}
        residual_levels = {}

        for risk in self.risks:
            initial_rpn = risk.calculate_rpn(risk.severity_initial, risk.probability_initial)
            residual_rpn = risk.calculate_rpn(risk.severity_residual, risk.probability_residual)

            initial_level = risk.get_risk_level(initial_rpn).value
            residual_level = risk.get_risk_level(residual_rpn).value

            initial_levels[initial_level] = initial_levels.get(initial_level, 0) + 1
            residual_levels[residual_level] = residual_levels.get(residual_level, 0) + 1

        unacceptable_risks = [r for r in self.risks 
                             if r.get_risk_level(r.calculate_rpn(r.severity_residual, r.probability_residual)) == RiskLevel.UNACCEPTABLE]

        return {
            "total_risks": len(self.risks),
            "initial_distribution": initial_levels,
            "residual_distribution": residual_levels,
            "unacceptable_count": len(unacceptable_risks),
            "risk_reduction_achieved": self.calculate_risk_reduction()
        }

    def calculate_risk_reduction(self) -> float:
        """Calculate average risk reduction percentage"""
        if not self.risks:
            return 0.0

        total_reduction = 0
        for risk in self.risks:
            initial_rpn = risk.calculate_rpn(risk.severity_initial, risk.probability_initial)
            residual_rpn = risk.calculate_rpn(risk.severity_residual, risk.probability_residual)
            if initial_rpn > 0:
                reduction = ((initial_rpn - residual_rpn) / initial_rpn) * 100
                total_reduction += reduction

        return round(total_reduction / len(self.risks), 1)

    def get_unacceptable_risks(self) -> List[RiskRecord]:
        """Get all unacceptable residual risks"""
        unacceptable = []
        for risk in self.risks:
            residual_rpn = risk.calculate_rpn(risk.severity_residual, risk.probability_residual)
            if risk.get_risk_level(residual_rpn) == RiskLevel.UNACCEPTABLE:
                unacceptable.append(risk)
        return unacceptable

    def get_verification_pending(self) -> List[RiskRecord]:
        """Get risks with pending verification"""
        return [r for r in self.risks if r.verification_status.upper() == "PENDING"]

    def generate_text_report(self, verbose: bool = False) -> str:
        """Generate text report"""
        report = []
        report.append("=" * 70)
        report.append("RISK MANAGEMENT REGISTER - ISO 14971")
        report.append("=" * 70)
        report.append(f"Report Generated: {datetime.date.today()}")
        report.append(f"Device/Product: {self.metadata.get('device_name', 'Not specified')}")
        report.append("")

        analysis = self.analyze_risk_levels()
        report.append("--- RISK ANALYSIS SUMMARY ---")
        report.append(f"Total Identified Risks: {analysis['total_risks']}")
        report.append(f"Average Risk Reduction: {analysis['risk_reduction_achieved']}%")
        report.append("")

        report.append("Initial Risk Distribution:")
        for level, count in analysis['initial_distribution'].items():
            report.append(f"  • {level}: {count}")
        report.append("")

        report.append("Residual Risk Distribution:")
        for level, count in analysis['residual_distribution'].items():
            report.append(f"  • {level}: {count}")
        report.append("")

        unacceptable = self.get_unacceptable_risks()
        if unacceptable:
            report.append(f"--- UNACCEPTABLE RESIDUAL RISKS: {len(unacceptable)} ---")
            for risk in unacceptable:
                residual_rpn = risk.calculate_rpn(risk.severity_residual, risk.probability_residual)
                report.append(f"  • {risk.risk_id}: {risk.hazard}")
                report.append(f"    Harm: {risk.harm}")
                report.append(f"    Residual RPN: {residual_rpn} ({risk.get_risk_level(residual_rpn).value})")
                report.append(f"    Control Measures: {risk.risk_control_measures}")
            report.append("")

        verification_pending = self.get_verification_pending()
        if verification_pending:
            report.append(f"--- VERIFICATION PENDING: {len(verification_pending)} ---")
            for risk in verification_pending[:10]:
                report.append(f"  • {risk.risk_id}: {risk.hazard}")
                report.append(f"    Method: {risk.verification_method}")
                report.append(f"    Responsible: {risk.responsible_person} | Target: {risk.target_date}")
            report.append("")

        if verbose:
            report.append("--- DETAILED RISK ASSESSMENT ---")
            for risk in self.risks:
                initial_rpn = risk.calculate_rpn(risk.severity_initial, risk.probability_initial)
                residual_rpn = risk.calculate_rpn(risk.severity_residual, risk.probability_residual)
                reduction = ((initial_rpn - residual_rpn) / initial_rpn * 100) if initial_rpn > 0 else 0

                report.append(f"\n{risk.risk_id}: {risk.hazard}")
                report.append(f"  Hazardous Situation: {risk.hazardous_situation}")
                report.append(f"  Harm: {risk.harm}")
                report.append(f"  Initial Risk: {initial_rpn} ({risk.get_risk_level(initial_rpn).value})")
                report.append(f"  Control Measures: {risk.risk_control_measures}")
                report.append(f"  Residual Risk: {residual_rpn} ({risk.get_risk_level(residual_rpn).value})")
                report.append(f"  Risk Reduction: {reduction:.1f}%")
                report.append(f"  Acceptable: {'Yes' if risk.risk_acceptable else 'No'}")

        report.append("=" * 70)
        return "\n".join(report)

    def generate_json_report(self, verbose: bool = False) -> Dict[str, Any]:
        """Generate JSON report"""
        report = {
            "metadata": {
                "tool": "risk_register.py",
                "version": "1.0.0",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "device_name": self.metadata.get('device_name', 'Not specified')
            },
            "summary": self.analyze_risk_levels()
        }

        if verbose:
            risks_detailed = []
            for risk in self.risks:
                risk_dict = asdict(risk)
                risk_dict['severity_initial'] = risk_dict['severity_initial'].value
                risk_dict['probability_initial'] = risk_dict['probability_initial'].value
                risk_dict['severity_residual'] = risk_dict['severity_residual'].value
                risk_dict['probability_residual'] = risk_dict['probability_residual'].value
                
                initial_rpn = risk.calculate_rpn(risk.severity_initial, risk.probability_initial)
                residual_rpn = risk.calculate_rpn(risk.severity_residual, risk.probability_residual)
                
                risk_dict['initial_rpn'] = initial_rpn
                risk_dict['residual_rpn'] = residual_rpn
                risk_dict['initial_level'] = risk.get_risk_level(initial_rpn).value
                risk_dict['residual_level'] = risk.get_risk_level(residual_rpn).value
                
                risks_detailed.append(risk_dict)

            report["detailed_data"] = {
                "all_risks": risks_detailed,
                "unacceptable_risks": [asdict(r) for r in self.get_unacceptable_risks()],
                "verification_pending": [asdict(r) for r in self.get_verification_pending()]
            }

        return report

    def generate_csv_report(self) -> str:
        """Generate CSV report"""
        output = []
        output.append("Risk ID,Hazard,Harm,Initial RPN,Initial Level,Control Measures,Residual RPN,Residual Level,Risk Reduction %,Acceptable,Verification Status")
        
        for risk in self.risks:
            initial_rpn = risk.calculate_rpn(risk.severity_initial, risk.probability_initial)
            residual_rpn = risk.calculate_rpn(risk.severity_residual, risk.probability_residual)
            reduction = ((initial_rpn - residual_rpn) / initial_rpn * 100) if initial_rpn > 0 else 0

            output.append(f'"{risk.risk_id}","{risk.hazard}","{risk.harm}",{initial_rpn},'
                         f'{risk.get_risk_level(initial_rpn).value},"{risk.risk_control_measures}",'
                         f'{residual_rpn},{risk.get_risk_level(residual_rpn).value},{reduction:.1f},'
                         f'{risk.risk_acceptable},{risk.verification_status}')
        
        return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Manage ISO 14971 risk assessment, mitigation tracking, and risk-benefit analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s risk_data.json
  %(prog)s risk_data.json --output json
  %(prog)s risk_data.json -o csv -f risk_report.csv -v

For more information:
ra-qm-team/risk-management-specialist/SKILL.md
        """
    )

    parser.add_argument('input', help='Risk data file (JSON format)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text')
    parser.add_argument('--file', '-f', help='Write output to file')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        register = RiskRegister(str(input_path))

        if args.output == 'json':
            output = json.dumps(register.generate_json_report(verbose=args.verbose), indent=2)
        elif args.output == 'csv':
            output = register.generate_csv_report()
        else:
            output = register.generate_text_report(verbose=args.verbose)

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
