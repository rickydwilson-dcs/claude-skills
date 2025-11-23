#!/usr/bin/env python3
"""
Win/Loss Analyzer - Deal Analysis and Insights

Analyzes won and lost deals to identify patterns, competitive insights,
and actionable improvements for sales and product strategy.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from collections import Counter

class WinLossAnalyzer:
    """Analyze win/loss patterns and generate insights"""

    LOSS_REASONS = [
        'price', 'features', 'competitor', 'timing', 'fit',
        'implementation', 'support', 'security', 'integration', 'other'
    ]

    WIN_REASONS = [
        'features', 'price', 'ease_of_use', 'support', 'implementation',
        'integration', 'reputation', 'relationship', 'roi', 'other'
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.deals = []
        self.insights = {}

    def load_deals(self, file_path: str) -> List[Dict]:
        """Load deal data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else data.get('deals', [])
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    def analyze_deals(self, deals: List[Dict]) -> Dict:
        """Analyze all deals and generate insights"""
        wins = [d for d in deals if d.get('outcome') == 'won']
        losses = [d for d in deals if d.get('outcome') == 'lost']

        analysis = {
            'summary': {
                'total_deals': len(deals),
                'wins': len(wins),
                'losses': len(losses),
                'win_rate': round((len(wins) / len(deals)) * 100, 1) if deals else 0
            },
            'win_analysis': self.analyze_wins(wins),
            'loss_analysis': self.analyze_losses(losses),
            'competitive_analysis': self.analyze_competitive(deals),
            'segment_analysis': self.analyze_segments(deals),
            'insights': self.generate_insights(wins, losses)
        }

        return analysis

    def analyze_wins(self, wins: List[Dict]) -> Dict:
        """Analyze won deals"""
        if not wins:
            return {'count': 0}

        # Top win reasons
        win_reasons = []
        for deal in wins:
            reasons = deal.get('win_reasons', [])
            if isinstance(reasons, list):
                win_reasons.extend(reasons)
            elif isinstance(reasons, str):
                win_reasons.append(reasons)

        reason_counts = Counter(win_reasons).most_common(5)

        # Deal value analysis
        deal_values = [d.get('value', 0) for d in wins if d.get('value')]
        avg_deal_value = sum(deal_values) / len(deal_values) if deal_values else 0

        # Sales cycle analysis
        sales_cycles = [d.get('sales_cycle_days', 0) for d in wins if d.get('sales_cycle_days')]
        avg_sales_cycle = sum(sales_cycles) / len(sales_cycles) if sales_cycles else 0

        return {
            'count': len(wins),
            'top_win_reasons': [{'reason': r, 'count': c} for r, c in reason_counts],
            'avg_deal_value': round(avg_deal_value, 2),
            'total_value': sum(deal_values),
            'avg_sales_cycle_days': round(avg_sales_cycle, 1),
            'fastest_win_days': min(sales_cycles) if sales_cycles else 0
        }

    def analyze_losses(self, losses: List[Dict]) -> Dict:
        """Analyze lost deals"""
        if not losses:
            return {'count': 0}

        # Top loss reasons
        loss_reasons = []
        for deal in losses:
            reasons = deal.get('loss_reasons', [])
            if isinstance(reasons, list):
                loss_reasons.extend(reasons)
            elif isinstance(reasons, str):
                loss_reasons.append(reasons)

        reason_counts = Counter(loss_reasons).most_common(5)

        # Competitor analysis
        competitors = [d.get('lost_to_competitor') for d in losses if d.get('lost_to_competitor')]
        competitor_counts = Counter(competitors).most_common(5)

        # Deal value analysis
        lost_values = [d.get('value', 0) for d in losses if d.get('value')]
        total_lost_value = sum(lost_values)

        return {
            'count': len(losses),
            'top_loss_reasons': [{'reason': r, 'count': c} for r, c in reason_counts],
            'lost_to_competitors': [{'competitor': c, 'count': cnt} for c, cnt in competitor_counts],
            'total_lost_value': total_lost_value,
            'avg_lost_deal_value': round(total_lost_value / len(lost_values), 2) if lost_values else 0
        }

    def analyze_competitive(self, deals: List[Dict]) -> Dict:
        """Analyze competitive win/loss patterns"""
        competitive_deals = [d for d in deals if d.get('competitor_present')]

        if not competitive_deals:
            return {'competitive_deals': 0}

        wins_competitive = [d for d in competitive_deals if d.get('outcome') == 'won']
        losses_competitive = [d for d in competitive_deals if d.get('outcome') == 'lost']

        # Win rate by competitor
        competitor_stats = {}
        for deal in competitive_deals:
            competitor = deal.get('competitor', deal.get('lost_to_competitor', 'Unknown'))
            if competitor not in competitor_stats:
                competitor_stats[competitor] = {'wins': 0, 'losses': 0}

            if deal.get('outcome') == 'won':
                competitor_stats[competitor]['wins'] += 1
            else:
                competitor_stats[competitor]['losses'] += 1

        # Calculate win rates
        for comp, stats in competitor_stats.items():
            total = stats['wins'] + stats['losses']
            stats['win_rate'] = round((stats['wins'] / total) * 100, 1) if total > 0 else 0

        return {
            'competitive_deals': len(competitive_deals),
            'competitive_win_rate': round((len(wins_competitive) / len(competitive_deals)) * 100, 1) if competitive_deals else 0,
            'competitor_stats': competitor_stats
        }

    def analyze_segments(self, deals: List[Dict]) -> Dict:
        """Analyze win/loss by segment"""
        segments = {}

        # By company size
        for deal in deals:
            size = deal.get('company_size', 'unknown')
            if size not in segments:
                segments[size] = {'wins': 0, 'losses': 0}

            if deal.get('outcome') == 'won':
                segments[size]['wins'] += 1
            else:
                segments[size]['losses'] += 1

        # Calculate win rates
        for segment, stats in segments.items():
            total = stats['wins'] + stats['losses']
            stats['win_rate'] = round((stats['wins'] / total) * 100, 1) if total > 0 else 0

        return {
            'by_company_size': segments
        }

    def generate_insights(self, wins: List[Dict], losses: List[Dict]) -> List[str]:
        """Generate actionable insights from win/loss data"""
        insights = []

        # Win rate insights
        total = len(wins) + len(losses)
        win_rate = (len(wins) / total) * 100 if total > 0 else 0

        if win_rate < 20:
            insights.append("Critical: Win rate below 20%. Immediate review of product-market fit and sales process needed.")
        elif win_rate < 30:
            insights.append("Low win rate. Focus on qualification criteria and competitive positioning.")
        elif win_rate > 50:
            insights.append("Strong win rate! Document and scale what's working.")

        # Loss reason insights
        loss_reasons = []
        for deal in losses:
            reasons = deal.get('loss_reasons', [])
            if isinstance(reasons, list):
                loss_reasons.extend(reasons)
            elif isinstance(reasons, str):
                loss_reasons.append(reasons)

        top_loss_reasons = Counter(loss_reasons).most_common(3)

        for reason, count in top_loss_reasons:
            pct = (count / len(losses)) * 100 if losses else 0
            if pct > 30:
                if reason == 'price':
                    insights.append(f"Price is primary loss reason ({pct:.0f}% of losses). Review pricing strategy or improve value communication.")
                elif reason == 'features':
                    insights.append(f"Feature gaps driving {pct:.0f}% of losses. Prioritize product roadmap accordingly.")
                elif reason == 'competitor':
                    insights.append(f"Losing {pct:.0f}% to specific competitors. Develop targeted competitive strategies.")

        # Sales cycle insights
        win_cycles = [d.get('sales_cycle_days', 0) for d in wins if d.get('sales_cycle_days')]
        loss_cycles = [d.get('sales_cycle_days', 0) for d in losses if d.get('sales_cycle_days')]

        if win_cycles and loss_cycles:
            avg_win_cycle = sum(win_cycles) / len(win_cycles)
            avg_loss_cycle = sum(loss_cycles) / len(loss_cycles)

            if avg_loss_cycle > avg_win_cycle * 1.3:
                insights.append(f"Lost deals have {(avg_loss_cycle/avg_win_cycle - 1)*100:.0f}% longer sales cycles. Improve early qualification.")

        return insights

    def generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []

        # Based on win rate
        win_rate = analysis['summary']['win_rate']
        if win_rate < 30:
            recommendations.extend([
                "Tighten lead qualification criteria to focus on winnable deals",
                "Develop competitive battlecards for top competitors",
                "Review and improve sales enablement materials"
            ])

        # Based on top loss reasons
        loss_analysis = analysis.get('loss_analysis', {})
        top_losses = loss_analysis.get('top_loss_reasons', [])

        for loss in top_losses[:2]:
            reason = loss['reason']
            if reason == 'price':
                recommendations.extend([
                    "Create ROI calculator to demonstrate value",
                    "Develop flexible pricing tiers or payment options",
                    "Train sales on value-based selling"
                ])
            elif reason == 'features':
                recommendations.extend([
                    "Accelerate product roadmap for critical feature gaps",
                    "Create workaround documentation for missing features",
                    "Consider partnerships to fill capability gaps"
                ])
            elif reason == 'competitor':
                recommendations.append("Conduct deep competitive analysis and develop counter-strategies")

        # Competitive insights
        comp_analysis = analysis.get('competitive_analysis', {})
        if comp_analysis.get('competitive_win_rate', 100) < 40:
            recommendations.append("Competitive win rate low. Review competitive positioning and differentiation")

        return recommendations[:8]

    def print_report(self, analysis: Dict):
        """Print human-readable win/loss report"""
        summary = analysis['summary']

        print("\n" + "="*60)
        print("WIN/LOSS ANALYSIS REPORT")
        print("="*60)

        print(f"\nSummary:")
        print(f"   Total Deals: {summary['total_deals']}")
        print(f"   Wins: {summary['wins']} | Losses: {summary['losses']}")
        print(f"   Win Rate: {summary['win_rate']}%")

        # Win analysis
        win_analysis = analysis.get('win_analysis', {})
        if win_analysis.get('count', 0) > 0:
            print(f"\nWin Analysis:")
            print(f"   Total Value Won: ${win_analysis['total_value']:,.0f}")
            print(f"   Avg Deal Value: ${win_analysis['avg_deal_value']:,.0f}")
            print(f"   Avg Sales Cycle: {win_analysis['avg_sales_cycle_days']:.0f} days")
            print(f"\n   Top Win Reasons:")
            for reason in win_analysis.get('top_win_reasons', [])[:3]:
                print(f"      - {reason['reason']}: {reason['count']} deals")

        # Loss analysis
        loss_analysis = analysis.get('loss_analysis', {})
        if loss_analysis.get('count', 0) > 0:
            print(f"\nLoss Analysis:")
            print(f"   Total Value Lost: ${loss_analysis['total_lost_value']:,.0f}")
            print(f"   Avg Lost Deal Value: ${loss_analysis['avg_lost_deal_value']:,.0f}")
            print(f"\n   Top Loss Reasons:")
            for reason in loss_analysis.get('top_loss_reasons', [])[:3]:
                print(f"      - {reason['reason']}: {reason['count']} deals")

            if loss_analysis.get('lost_to_competitors'):
                print(f"\n   Lost to Competitors:")
                for comp in loss_analysis['lost_to_competitors'][:3]:
                    print(f"      - {comp['competitor']}: {comp['count']} deals")

        # Competitive analysis
        comp_analysis = analysis.get('competitive_analysis', {})
        if comp_analysis.get('competitive_deals', 0) > 0:
            print(f"\nCompetitive Analysis:")
            print(f"   Competitive Win Rate: {comp_analysis['competitive_win_rate']}%")

        # Insights
        insights = analysis.get('insights', [])
        if insights:
            print(f"\nKey Insights:")
            for i, insight in enumerate(insights[:5], 1):
                print(f"   {i}. {insight}")

        # Recommendations
        recommendations = self.generate_recommendations(analysis)
        if recommendations:
            print(f"\nRecommendations:")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"   {i}. {rec}")

        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze won and lost deals for insights and patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Deal JSON Format:
  {
    "deal_id": "D123",
    "outcome": "won",
    "value": 50000,
    "company_size": "mid-market",
    "sales_cycle_days": 45,
    "win_reasons": ["features", "ease_of_use"],
    "competitor_present": true,
    "competitor": "Competitor X"
  }

Examples:
  # Analyze deals from file
  %(prog)s --file deals.json

  # Filter by date range
  %(prog)s --file deals.json --from 2024-01-01 --to 2024-12-31

  # JSON output
  %(prog)s --file deals.json --json
        """
    )

    parser.add_argument(
        '--file',
        required=True,
        help='JSON file containing deal data'
    )
    parser.add_argument(
        '--from',
        dest='date_from',
        help='Start date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--to',
        dest='date_to',
        help='End date (YYYY-MM-DD)'
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

    analyzer = WinLossAnalyzer(verbose=args.verbose)
    deals = analyzer.load_deals(args.file)

    # Filter by date if provided
    if args.date_from or args.date_to:
        filtered_deals = []
        for deal in deals:
            deal_date = deal.get('date', '')
            if args.date_from and deal_date < args.date_from:
                continue
            if args.date_to and deal_date > args.date_to:
                continue
            filtered_deals.append(deal)
        deals = filtered_deals

    # Analyze deals
    analysis = analyzer.analyze_deals(deals)

    # Output
    if args.json:
        output = json.dumps(analysis, indent=2)
        if args.output:
            Path(args.output).write_text(output)
            print(f"Report written to {args.output}")
        else:
            print(output)
    else:
        analyzer.print_report(analysis)

if __name__ == "__main__":
    main()
