#!/usr/bin/env python3
"""
Competitor Tracker - Competitive Intelligence Analysis

Tracks competitor positioning, features, pricing, and market movements.
Generates competitive battlecards and win/loss insights.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class CompetitorTracker:
    """Track and analyze competitive intelligence"""

    ANALYSIS_DIMENSIONS = [
        'features', 'pricing', 'positioning', 'messaging',
        'target_market', 'strengths', 'weaknesses', 'recent_moves'
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.competitors = []
        self.analysis = {}

    def load_competitors(self, file_path: str) -> List[Dict]:
        """Load competitor data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else data.get('competitors', [])
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    def analyze_competitor(self, competitor: Dict) -> Dict:
        """Analyze single competitor"""
        name = competitor.get('name', 'Unknown')

        analysis = {
            'name': name,
            'positioning': competitor.get('positioning', ''),
            'target_market': competitor.get('target_market', ''),
            'threat_level': self.calculate_threat_level(competitor),
            'differentiation_opportunities': self.identify_differentiation(competitor),
            'competitive_response': self.generate_competitive_response(competitor)
        }

        # Feature comparison
        their_features = set(competitor.get('features', []))
        our_features = set(competitor.get('our_features', []))

        analysis['feature_gap'] = list(their_features - our_features)
        analysis['unique_features'] = list(our_features - their_features)
        analysis['shared_features'] = list(their_features & our_features)

        # Pricing analysis
        if 'pricing' in competitor:
            analysis['pricing_strategy'] = self.analyze_pricing(
                competitor['pricing'],
                competitor.get('our_pricing')
            )

        return analysis

    def calculate_threat_level(self, competitor: Dict) -> str:
        """Calculate competitive threat level"""
        score = 0

        # Market presence
        if competitor.get('market_share', 0) > 20:
            score += 3
        elif competitor.get('market_share', 0) > 10:
            score += 2
        elif competitor.get('market_share', 0) > 5:
            score += 1

        # Growth rate
        if competitor.get('growth_rate', 0) > 50:
            score += 2
        elif competitor.get('growth_rate', 0) > 25:
            score += 1

        # Win rate against us
        if competitor.get('win_rate_vs_us', 0) > 60:
            score += 3
        elif competitor.get('win_rate_vs_us', 0) > 40:
            score += 2
        elif competitor.get('win_rate_vs_us', 0) > 20:
            score += 1

        # Feature completeness
        their_features = len(competitor.get('features', []))
        our_features = len(competitor.get('our_features', []))
        if their_features > our_features * 1.2:
            score += 2
        elif their_features > our_features:
            score += 1

        # Classify threat level
        if score >= 8:
            return 'critical'
        elif score >= 5:
            return 'high'
        elif score >= 3:
            return 'medium'
        else:
            return 'low'

    def identify_differentiation(self, competitor: Dict) -> List[str]:
        """Identify differentiation opportunities"""
        opportunities = []

        # Feature-based differentiation
        our_unique = set(competitor.get('our_features', [])) - set(competitor.get('features', []))
        if our_unique:
            opportunities.append(f"Emphasize unique features: {', '.join(list(our_unique)[:3])}")

        # Positioning opportunities
        if competitor.get('positioning', '').lower() == 'enterprise':
            opportunities.append("Position as SMB-friendly alternative with faster setup")
        elif competitor.get('positioning', '').lower() == 'smb':
            opportunities.append("Position as enterprise-grade with better security/compliance")

        # Pricing opportunities
        our_price = competitor.get('our_pricing', {}).get('starting_price')
        their_price = competitor.get('pricing', {}).get('starting_price')
        if our_price and their_price:
            if our_price < their_price * 0.8:
                opportunities.append("Emphasize cost advantage (20%+ cheaper)")
            elif our_price > their_price * 1.2:
                opportunities.append("Position as premium with superior ROI/value")

        # Support/service opportunities
        if not competitor.get('features', {}).get('24/7_support'):
            opportunities.append("Highlight 24/7 support as differentiator")

        return opportunities

    def generate_competitive_response(self, competitor: Dict) -> Dict:
        """Generate competitive response strategy"""
        threat_level = self.calculate_threat_level(competitor)

        response = {
            'priority': threat_level,
            'monitoring_frequency': self.get_monitoring_frequency(threat_level),
            'response_tactics': []
        }

        # Add tactics based on threat level
        if threat_level in ['critical', 'high']:
            response['response_tactics'].extend([
                "Create detailed battlecard with objection handling",
                "Train sales team on competitive positioning",
                "Monitor their product updates and pricing changes weekly",
                "Develop head-to-head comparison content"
            ])

        if threat_level == 'critical':
            response['response_tactics'].extend([
                "Executive-level competitive strategy session",
                "Consider feature parity for critical gaps",
                "Aggressive competitive pricing strategy",
                "Win-back campaign for lost deals"
            ])

        return response

    def get_monitoring_frequency(self, threat_level: str) -> str:
        """Determine monitoring frequency based on threat"""
        frequencies = {
            'critical': 'weekly',
            'high': 'bi-weekly',
            'medium': 'monthly',
            'low': 'quarterly'
        }
        return frequencies.get(threat_level, 'monthly')

    def analyze_pricing(self, their_pricing: Dict, our_pricing: Optional[Dict]) -> Dict:
        """Analyze pricing strategy"""
        analysis = {
            'model': their_pricing.get('model', 'unknown'),
            'starting_price': their_pricing.get('starting_price'),
            'enterprise_price': their_pricing.get('enterprise_price')
        }

        if our_pricing:
            our_start = our_pricing.get('starting_price', 0)
            their_start = their_pricing.get('starting_price', 0)

            if our_start and their_start:
                diff_pct = ((our_start - their_start) / their_start) * 100
                analysis['price_positioning'] = 'cheaper' if diff_pct < -10 else 'premium' if diff_pct > 10 else 'competitive'
                analysis['price_difference_pct'] = round(diff_pct, 1)

        return analysis

    def generate_battlecard(self, analysis: Dict) -> Dict:
        """Generate competitive battlecard"""
        battlecard = {
            'competitor': analysis['name'],
            'threat_level': analysis['threat_level'],
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'elevator_pitch': f"When competing against {analysis['name']}...",
            'why_we_win': analysis.get('unique_features', []),
            'why_we_lose': analysis.get('feature_gap', []),
            'differentiation': analysis.get('differentiation_opportunities', []),
            'objection_handling': self.generate_objection_handling(analysis),
            'competitive_intelligence': analysis.get('competitive_response', {})
        }

        return battlecard

    def generate_objection_handling(self, analysis: Dict) -> List[Dict]:
        """Generate objection handling responses"""
        objections = []

        # Feature gap objections
        for feature in analysis.get('feature_gap', [])[:3]:
            objections.append({
                'objection': f"They have {feature}, you don't",
                'response': f"While {analysis['name']} offers {feature}, our customers find greater value in [unique_feature]. Here's why..."
            })

        # Pricing objections
        if 'pricing_strategy' in analysis:
            if analysis['pricing_strategy'].get('price_positioning') == 'premium':
                objections.append({
                    'objection': "You're more expensive",
                    'response': "Our pricing reflects the superior ROI and lower total cost of ownership. Here's the breakdown..."
                })

        return objections

    def generate_competitive_matrix(self, competitors: List[Dict]) -> str:
        """Generate ASCII competitive positioning matrix"""
        matrix = "\n   COMPETITIVE THREAT MATRIX\n"
        matrix += "   " + "="*50 + "\n\n"
        matrix += f"   {'Competitor':<20} {'Threat':<10} {'Win Rate':<10}\n"
        matrix += "   " + "-"*50 + "\n"

        for comp in sorted(competitors, key=lambda x: x.get('threat_level', 'low'), reverse=True):
            name = comp['name'][:18]
            threat = comp.get('threat_level', 'unknown')
            win_rate = comp.get('win_rate_vs_us', 0)

            threat_icon = "[!]" if threat == 'critical' else "[!]" if threat == 'high' else "[!]" if threat == 'medium' else "[.]"
            matrix += f"   {threat_icon} {name:<18} {threat:<10} {win_rate}%\n"

        return matrix

    def print_report(self, analysis: List[Dict]):
        """Print competitive intelligence report"""
        print("\n" + "="*60)
        print("COMPETITIVE INTELLIGENCE REPORT")
        print("="*60)

        print(f"\nCompetitors Analyzed: {len(analysis)}")

        # Threat level summary
        threat_counts = {}
        for comp in analysis:
            level = comp['threat_level']
            threat_counts[level] = threat_counts.get(level, 0) + 1

        print(f"\nThreat Level Summary:")
        for level in ['critical', 'high', 'medium', 'low']:
            count = threat_counts.get(level, 0)
            if count > 0:
                icon = "[!]" if level == 'critical' else "[!]" if level == 'high' else "[!]" if level == 'medium' else "[.]"
                print(f"   {icon} {level.title()}: {count}")

        # Top threats
        top_threats = [c for c in analysis if c['threat_level'] in ['critical', 'high']]
        if top_threats:
            print(f"\nTop Competitive Threats:")
            for i, comp in enumerate(top_threats[:3], 1):
                print(f"\n   {i}. {comp['name']} [{comp['threat_level'].upper()}]")
                if comp.get('differentiation_opportunities'):
                    print(f"      Opportunities:")
                    for opp in comp['differentiation_opportunities'][:2]:
                        print(f"      - {opp}")

        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description="Track competitors and generate competitive intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Competitor JSON Format:
  {
    "name": "Competitor X",
    "positioning": "enterprise",
    "target_market": "Fortune 500",
    "features": ["feature1", "feature2"],
    "our_features": ["feature1", "feature3"],
    "pricing": {"model": "per-user", "starting_price": 99},
    "our_pricing": {"model": "per-user", "starting_price": 79},
    "market_share": 15,
    "growth_rate": 30,
    "win_rate_vs_us": 45
  }

Examples:
  # Analyze competitors from file
  %(prog)s --file competitors.json

  # Generate battlecards
  %(prog)s --file competitors.json --battlecards

  # JSON output
  %(prog)s --file competitors.json --json
        """
    )

    parser.add_argument(
        '--file',
        required=True,
        help='JSON file containing competitor data'
    )
    parser.add_argument(
        '--battlecards',
        action='store_true',
        help='Generate competitive battlecards'
    )
    parser.add_argument(
        '--matrix',
        action='store_true',
        help='Show competitive positioning matrix'
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

    tracker = CompetitorTracker(verbose=args.verbose)
    competitors_data = tracker.load_competitors(args.file)

    # Analyze all competitors
    analysis = []
    for comp_data in competitors_data:
        comp_analysis = tracker.analyze_competitor(comp_data)
        analysis.append(comp_analysis)

    # Generate battlecards if requested
    battlecards = []
    if args.battlecards:
        for comp in analysis:
            battlecards.append(tracker.generate_battlecard(comp))

    # Prepare output
    output_data = {
        'analyzed_at': datetime.now().isoformat(),
        'total_competitors': len(analysis),
        'analysis': analysis
    }

    if battlecards:
        output_data['battlecards'] = battlecards

    if args.matrix:
        output_data['matrix'] = tracker.generate_competitive_matrix(analysis)

    # Output results
    if args.json:
        output = json.dumps(output_data, indent=2)
        if args.output:
            Path(args.output).write_text(output)
            print(f"Report written to {args.output}")
        else:
            print(output)
    else:
        tracker.print_report(analysis)
        if args.matrix:
            print(tracker.generate_competitive_matrix(analysis))

if __name__ == "__main__":
    main()
