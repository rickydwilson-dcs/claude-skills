#!/usr/bin/env python3
"""
Risk Assessment Tool - Project Risk Management

Analyzes project risks using probability-impact matrix, calculates risk scores,
prioritizes mitigation strategies, and generates risk registers for software projects.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class RiskAssessmentTool:
    """Assess and prioritize project risks"""

    IMPACT_LEVELS = {
        'critical': 5,
        'high': 4,
        'medium': 3,
        'low': 2,
        'minimal': 1
    }

    PROBABILITY_LEVELS = {
        'very_high': 5,
        'high': 4,
        'medium': 3,
        'low': 2,
        'very_low': 1
    }

    RISK_CATEGORIES = [
        'technical', 'resource', 'schedule', 'budget', 'scope',
        'quality', 'security', 'compliance', 'vendor', 'market'
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.risks = []
        self.assessment = {
            'assessed_at': datetime.now().isoformat(),
            'total_risks': 0,
            'critical_risks': 0,
            'high_risks': 0,
            'overall_score': 0
        }

    def calculate_risk_score(self, probability: str, impact: str) -> int:
        """Calculate risk score from probability and impact"""
        prob_value = self.PROBABILITY_LEVELS.get(probability.lower(), 3)
        impact_value = self.IMPACT_LEVELS.get(impact.lower(), 3)
        return prob_value * impact_value

    def classify_risk_level(self, score: int) -> str:
        """Classify risk level based on score"""
        if score >= 15:
            return 'critical'
        elif score >= 10:
            return 'high'
        elif score >= 6:
            return 'medium'
        else:
            return 'low'

    def assess_risk(self, risk_data: Dict) -> Dict:
        """Assess a single risk"""
        probability = risk_data.get('probability', 'medium')
        impact = risk_data.get('impact', 'medium')

        score = self.calculate_risk_score(probability, impact)
        level = self.classify_risk_level(score)

        return {
            'id': risk_data.get('id', len(self.risks) + 1),
            'name': risk_data.get('name', 'Unnamed Risk'),
            'description': risk_data.get('description', ''),
            'category': risk_data.get('category', 'technical'),
            'probability': probability,
            'impact': impact,
            'score': score,
            'level': level,
            'mitigation': risk_data.get('mitigation', ''),
            'owner': risk_data.get('owner', 'Unassigned'),
            'status': risk_data.get('status', 'identified')
        }

    def load_risks_from_file(self, file_path: str) -> List[Dict]:
        """Load risks from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else data.get('risks', [])
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_mitigation_strategies(self, risk: Dict) -> List[str]:
        """Generate mitigation strategies based on risk category and level"""
        strategies = []
        category = risk['category']
        level = risk['level']

        # Category-specific strategies
        if category == 'technical':
            strategies.extend([
                "Conduct technical spike or proof-of-concept",
                "Engage technical architect for design review",
                "Implement progressive enhancement approach"
            ])
        elif category == 'resource':
            strategies.extend([
                "Cross-train team members on critical skills",
                "Establish backup resource plan",
                "Consider contractor or consulting support"
            ])
        elif category == 'schedule':
            strategies.extend([
                "Add buffer time to critical path activities",
                "Identify opportunities to parallelize work",
                "Implement agile approach with regular checkpoints"
            ])
        elif category == 'budget':
            strategies.extend([
                "Establish contingency reserve (10-20%)",
                "Implement cost tracking and variance analysis",
                "Identify cost reduction opportunities"
            ])
        elif category == 'security':
            strategies.extend([
                "Conduct security audit or penetration testing",
                "Implement security best practices from start",
                "Engage security specialist for review"
            ])

        # Level-specific strategies
        if level in ['critical', 'high']:
            strategies.append("⚠️  PRIORITY: Escalate to executive stakeholders immediately")
            strategies.append("Develop comprehensive contingency plan")
            strategies.append("Assign dedicated owner for daily monitoring")

        return strategies[:5]  # Return top 5

    def prioritize_risks(self, risks: List[Dict]) -> List[Dict]:
        """Sort risks by score (descending) and level"""
        level_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        return sorted(risks,
                     key=lambda r: (level_order.get(r['level'], 4), -r['score']))

    def generate_risk_matrix(self, risks: List[Dict]) -> str:
        """Generate ASCII risk matrix visualization"""
        matrix = "\n   RISK PROBABILITY-IMPACT MATRIX\n"
        matrix += "   " + "="*40 + "\n\n"
        matrix += "   Impact →\n"
        matrix += "   P  │ Min  Low  Med  High Crit\n"
        matrix += "   r  ├──────────────────────────\n"

        prob_labels = {'very_high': 'VH', 'high': 'H ', 'medium': 'M ',
                      'low': 'L ', 'very_low': 'VL'}

        for prob_level in ['very_high', 'high', 'medium', 'low', 'very_low']:
            row = f"   {prob_labels[prob_level]} │"
            for impact_level in ['minimal', 'low', 'medium', 'high', 'critical']:
                score = self.calculate_risk_score(prob_level, impact_level)
                # Count risks in this cell
                count = sum(1 for r in risks
                          if r['probability'] == prob_level and r['impact'] == impact_level)
                cell = f" {count:2d}  " if count > 0 else "  -  "
                row += cell
            matrix += row + "\n"

        matrix += "\n   Legend: Number = Risk count in cell\n"
        return matrix

    def generate_report(self, risks: List[Dict]) -> Dict:
        """Generate comprehensive risk assessment report"""
        prioritized = self.prioritize_risks(risks)

        # Count by level
        level_counts = {
            'critical': sum(1 for r in risks if r['level'] == 'critical'),
            'high': sum(1 for r in risks if r['level'] == 'high'),
            'medium': sum(1 for r in risks if r['level'] == 'medium'),
            'low': sum(1 for r in risks if r['level'] == 'low')
        }

        # Count by category
        category_counts = {}
        for risk in risks:
            cat = risk['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Calculate overall risk score (weighted average)
        total_score = sum(r['score'] for r in risks)
        overall_score = total_score / len(risks) if risks else 0

        return {
            'summary': {
                'total_risks': len(risks),
                'overall_score': round(overall_score, 2),
                'level_counts': level_counts,
                'category_counts': category_counts
            },
            'top_risks': prioritized[:10],
            'matrix': self.generate_risk_matrix(risks),
            'recommendations': self.generate_overall_recommendations(level_counts)
        }

    def generate_overall_recommendations(self, level_counts: Dict) -> List[str]:
        """Generate project-level recommendations"""
        recommendations = []

        if level_counts['critical'] > 0:
            recommendations.append(
                f"🚨 URGENT: {level_counts['critical']} critical risk(s) require immediate action"
            )
            recommendations.append(
                "Schedule emergency stakeholder meeting to address critical risks"
            )

        if level_counts['high'] >= 3:
            recommendations.append(
                f"⚠️  {level_counts['high']} high-priority risks identified - establish mitigation task force"
            )

        if level_counts['critical'] + level_counts['high'] > 5:
            recommendations.append(
                "Consider project re-planning or scope reduction to manage risk exposure"
            )

        recommendations.extend([
            "Conduct weekly risk review meetings with project team",
            "Update risk register bi-weekly with mitigation progress",
            "Establish clear escalation path for emerging risks"
        ])

        return recommendations

    def print_report(self, report: Dict):
        """Print human-readable risk report"""
        summary = report['summary']

        print("\n" + "="*60)
        print("RISK ASSESSMENT REPORT")
        print("="*60)

        print(f"\n📊 Summary:")
        print(f"   Total Risks: {summary['total_risks']}")
        print(f"   Overall Risk Score: {summary['overall_score']:.2f}/25")
        print(f"\n   By Level:")
        for level, count in summary['level_counts'].items():
            if count > 0:
                icon = "🚨" if level == 'critical' else "⚠️" if level == 'high' else "⚡" if level == 'medium' else "ℹ️"
                print(f"   {icon}  {level.title()}: {count}")

        print(f"\n   By Category:")
        for cat, count in sorted(summary['category_counts'].items(), key=lambda x: -x[1])[:5]:
            print(f"      {cat.title()}: {count}")

        print(report['matrix'])

        print(f"\n🎯 Top Risks (by priority):")
        for i, risk in enumerate(report['top_risks'][:5], 1):
            level_icon = "🚨" if risk['level'] == 'critical' else "⚠️" if risk['level'] == 'high' else "⚡"
            print(f"\n   {i}. {level_icon} [{risk['level'].upper()}] {risk['name']}")
            print(f"      Score: {risk['score']}/25 | Category: {risk['category']}")
            if risk['description']:
                print(f"      Description: {risk['description']}")
            print(f"      Owner: {risk['owner']}")

        if report['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"   • {rec}")

        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description="Assess and prioritize project risks for software projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Risk JSON Format:
  {
    "name": "API integration delay",
    "description": "Third-party API may not be ready",
    "category": "technical",
    "probability": "high",
    "impact": "high",
    "mitigation": "Develop mock API for parallel development",
    "owner": "Tech Lead"
  }

Examples:
  # Assess single risk
  %(prog)s --name "Resource loss" --probability high --impact critical --category resource

  # Load from file
  %(prog)s --file risks.json

  # Generate mitigation strategies
  %(prog)s --file risks.json --suggest-mitigations

  # JSON output
  %(prog)s --file risks.json --json
        """
    )

    parser.add_argument(
        '--file',
        help='JSON file containing risks'
    )
    parser.add_argument(
        '--name',
        help='Risk name (for single risk assessment)'
    )
    parser.add_argument(
        '--description',
        help='Risk description'
    )
    parser.add_argument(
        '--category',
        choices=RiskAssessmentTool.RISK_CATEGORIES,
        help='Risk category'
    )
    parser.add_argument(
        '--probability',
        choices=['very_high', 'high', 'medium', 'low', 'very_low'],
        help='Probability of occurrence'
    )
    parser.add_argument(
        '--impact',
        choices=['critical', 'high', 'medium', 'low', 'minimal'],
        help='Impact if occurs'
    )
    parser.add_argument(
        '--mitigation',
        help='Mitigation strategy'
    )
    parser.add_argument(
        '--owner',
        help='Risk owner'
    )
    parser.add_argument(
        '--suggest-mitigations',
        action='store_true',
        help='Generate mitigation strategy suggestions'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path'
    )

    args = parser.parse_args()

    tool = RiskAssessmentTool(verbose=args.verbose)
    risks = []

    # Load from file
    if args.file:
        risks_data = tool.load_risks_from_file(args.file)
        for risk_data in risks_data:
            risk = tool.assess_risk(risk_data)
            if args.suggest_mitigations:
                risk['suggested_mitigations'] = tool.generate_mitigation_strategies(risk)
            risks.append(risk)

    # Or assess single risk
    elif args.name and args.probability and args.impact:
        risk_data = {
            'name': args.name,
            'description': args.description or '',
            'category': args.category or 'technical',
            'probability': args.probability,
            'impact': args.impact,
            'mitigation': args.mitigation or '',
            'owner': args.owner or 'Unassigned'
        }
        risk = tool.assess_risk(risk_data)
        if args.suggest_mitigations:
            risk['suggested_mitigations'] = tool.generate_mitigation_strategies(risk)
        risks.append(risk)

    else:
        parser.print_help()
        sys.exit(0)

    # Generate report
    report = tool.generate_report(risks)
    report['risks'] = risks

    # Output
    if args.json:
        output = json.dumps(report, indent=2)
        if args.output:
            Path(args.output).write_text(output)
            print(f"✅ Report written to {args.output}")
        else:
            print(output)
    else:
        tool.print_report(report)

if __name__ == "__main__":
    main()
