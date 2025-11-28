#!/usr/bin/env python3
"""
Backlog Prioritization Tool
Prioritizes product backlog items using value/effort/risk scoring formula.

Formula: Priority Score = (value * 0.4) + ((10 - effort) * 0.3) + ((10 - risk) * 0.3)
Where value, effort, and risk are scored 1-10.
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class BacklogPrioritizer:
    """Prioritize backlog items using value/effort/risk scoring"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.weights = {
            'value': 0.4,
            'effort': 0.3,
            'risk': 0.3
        }

    def calculate_priority_score(self, value: int, effort: int, risk: int) -> float:
        """
        Calculate priority score using weighted formula.

        Args:
            value: Business value (1-10, higher = more valuable)
            effort: Implementation effort (1-10, higher = harder)
            risk: Risk/uncertainty (1-10, higher = riskier)

        Returns:
            Priority score (0-10 scale)
        """
        # Clamp values to 1-10 range
        value = max(1, min(10, value))
        effort = max(1, min(10, effort))
        risk = max(1, min(10, risk))

        # Formula: high value good, low effort good, low risk good
        score = (
            (value * self.weights['value']) +
            ((10 - effort) * self.weights['effort']) +
            ((10 - risk) * self.weights['risk'])
        )
        return round(score, 2)

    def prioritize_items(self, items: List[Dict]) -> List[Dict]:
        """
        Calculate priority scores and rank backlog items.

        Args:
            items: List of backlog item dictionaries

        Returns:
            Sorted list with priority_score added to each item
        """
        for item in items:
            item['priority_score'] = self.calculate_priority_score(
                item.get('value', 5),
                item.get('effort', 5),
                item.get('risk', 5)
            )
            item['priority_rank'] = self._get_priority_rank(item['priority_score'])

        # Sort by priority score descending
        return sorted(items, key=lambda x: x['priority_score'], reverse=True)

    def _get_priority_rank(self, score: float) -> str:
        """Convert score to priority rank label"""
        if score >= 8.0:
            return 'P0-Critical'
        elif score >= 6.5:
            return 'P1-High'
        elif score >= 5.0:
            return 'P2-Medium'
        else:
            return 'P3-Low'

    def identify_quick_wins(self, items: List[Dict],
                            value_threshold: int = 7,
                            effort_threshold: int = 3) -> List[Dict]:
        """
        Identify quick wins: high value, low effort items.

        Args:
            items: Prioritized backlog items
            value_threshold: Minimum value score (default: 7)
            effort_threshold: Maximum effort score (default: 3)

        Returns:
            List of quick win items
        """
        quick_wins = [
            item for item in items
            if item.get('value', 0) >= value_threshold
            and item.get('effort', 10) <= effort_threshold
        ]
        return quick_wins

    def identify_high_risk(self, items: List[Dict],
                           risk_threshold: int = 7) -> List[Dict]:
        """
        Identify high-risk items that need attention.

        Args:
            items: Prioritized backlog items
            risk_threshold: Minimum risk score to flag (default: 7)

        Returns:
            List of high-risk items with mitigation suggestions
        """
        high_risk = []
        for item in items:
            if item.get('risk', 0) >= risk_threshold:
                risk_item = item.copy()
                risk_item['mitigation_suggestions'] = self._suggest_mitigations(item)
                high_risk.append(risk_item)
        return high_risk

    def _suggest_mitigations(self, item: Dict) -> List[str]:
        """Generate risk mitigation suggestions"""
        suggestions = []
        risk = item.get('risk', 0)
        effort = item.get('effort', 0)

        if risk >= 8:
            suggestions.append("Consider spike/proof-of-concept first")
        if effort >= 8:
            suggestions.append("Break down into smaller stories")
        if risk >= 7:
            suggestions.append("Add technical review before sprint commitment")
        if item.get('dependencies'):
            suggestions.append("Resolve dependencies before sprint start")

        return suggestions if suggestions else ["Review complexity and unknowns"]

    def allocate_to_sprint(self, items: List[Dict],
                           capacity: int,
                           buffer_percent: float = 0.15) -> Dict:
        """
        Allocate items to sprint based on capacity.

        Args:
            items: Prioritized backlog items (must have story_points)
            capacity: Total sprint capacity in story points
            buffer_percent: Safety buffer (default: 15%)

        Returns:
            Dictionary with sprint allocation details
        """
        target_capacity = int(capacity * (1 - buffer_percent))
        sprint_items = []
        backlog_items = []
        allocated_points = 0

        for item in items:
            points = item.get('story_points', 0)
            if allocated_points + points <= target_capacity:
                sprint_items.append(item)
                allocated_points += points
            else:
                backlog_items.append(item)

        return {
            'sprint_items': sprint_items,
            'sprint_points': allocated_points,
            'sprint_count': len(sprint_items),
            'backlog_items': backlog_items,
            'backlog_count': len(backlog_items),
            'capacity': capacity,
            'target_capacity': target_capacity,
            'buffer_points': capacity - target_capacity,
            'utilization': round(allocated_points / capacity * 100, 1) if capacity > 0 else 0
        }

    def analyze_backlog(self, items: List[Dict]) -> Dict:
        """
        Generate backlog analysis summary.

        Args:
            items: Prioritized backlog items

        Returns:
            Analysis dictionary with statistics
        """
        if not items:
            return {'status': 'empty', 'total_items': 0}

        total_points = sum(item.get('story_points', 0) for item in items)
        scores = [item.get('priority_score', 0) for item in items]

        # Count by priority rank
        rank_distribution = {}
        for item in items:
            rank = item.get('priority_rank', 'Unknown')
            rank_distribution[rank] = rank_distribution.get(rank, 0) + 1

        return {
            'total_items': len(items),
            'total_story_points': total_points,
            'average_priority_score': round(sum(scores) / len(scores), 2),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'rank_distribution': rank_distribution,
            'average_value': round(sum(item.get('value', 0) for item in items) / len(items), 1),
            'average_effort': round(sum(item.get('effort', 0) for item in items) / len(items), 1),
            'average_risk': round(sum(item.get('risk', 0) for item in items) / len(items), 1)
        }


def load_from_json(filepath: str) -> List[Dict]:
    """Load backlog items from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Handle both array and object with 'items' key
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'items' in data:
            return data['items']
        else:
            raise ValueError("JSON must be an array or object with 'items' key")


def load_from_csv(filepath: str) -> List[Dict]:
    """Load backlog items from CSV file"""
    items = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = {
                'id': row.get('id', ''),
                'title': row.get('title', row.get('name', '')),
                'value': int(row.get('value', 5)),
                'effort': int(row.get('effort', 5)),
                'risk': int(row.get('risk', 5)),
                'story_points': int(row.get('story_points', row.get('points', 0))),
                'description': row.get('description', '')
            }
            items.append(item)
    return items


def detect_and_load(filepath: str) -> List[Dict]:
    """Detect file format and load accordingly"""
    path = Path(filepath)
    suffix = path.suffix.lower()

    if suffix == '.json':
        return load_from_json(filepath)
    elif suffix == '.csv':
        return load_from_csv(filepath)
    else:
        # Try JSON first, then CSV
        try:
            return load_from_json(filepath)
        except (json.JSONDecodeError, ValueError):
            return load_from_csv(filepath)


def format_text_output(items: List[Dict], analysis: Dict,
                       allocation: Optional[Dict] = None,
                       quick_wins: Optional[List[Dict]] = None,
                       high_risk: Optional[List[Dict]] = None) -> str:
    """Format results as human-readable text"""
    output = []
    output.append("=" * 60)
    output.append("BACKLOG PRIORITIZATION RESULTS")
    output.append("=" * 60)
    output.append("")
    output.append("Formula: Priority = (value * 0.4) + ((10-effort) * 0.3) + ((10-risk) * 0.3)")
    output.append("")

    # Prioritized list
    output.append(f"PRIORITIZED BACKLOG ({len(items)} items)")
    output.append("-" * 60)
    output.append(f"{'Rank':<5} {'ID':<10} {'Title':<25} {'Score':<7} {'Priority'}")
    output.append("-" * 60)

    for i, item in enumerate(items[:15], 1):
        title = item.get('title', item.get('name', 'Unnamed'))[:24]
        output.append(
            f"{i:<5} {item.get('id', '-'):<10} {title:<25} "
            f"{item['priority_score']:<7} {item['priority_rank']}"
        )

    if len(items) > 15:
        output.append(f"... and {len(items) - 15} more items")

    # Analysis summary
    output.append("")
    output.append("ANALYSIS SUMMARY")
    output.append("-" * 60)
    output.append(f"Total Items: {analysis['total_items']}")
    output.append(f"Total Story Points: {analysis['total_story_points']}")
    output.append(f"Average Priority Score: {analysis['average_priority_score']}")
    output.append(f"Score Range: {analysis['lowest_score']} - {analysis['highest_score']}")
    output.append("")
    output.append("Priority Distribution:")
    for rank, count in sorted(analysis['rank_distribution'].items()):
        output.append(f"  {rank}: {count} items")

    # Quick wins
    if quick_wins:
        output.append("")
        output.append(f"QUICK WINS ({len(quick_wins)} items)")
        output.append("-" * 60)
        output.append("High value (>=7), low effort (<=3):")
        for item in quick_wins[:5]:
            title = item.get('title', item.get('name', 'Unnamed'))[:30]
            output.append(f"  * {item.get('id', '-')}: {title} (Score: {item['priority_score']})")

    # High risk
    if high_risk:
        output.append("")
        output.append(f"HIGH RISK ITEMS ({len(high_risk)} items)")
        output.append("-" * 60)
        for item in high_risk[:5]:
            title = item.get('title', item.get('name', 'Unnamed'))[:30]
            output.append(f"  * {item.get('id', '-')}: {title} (Risk: {item.get('risk', 0)})")
            for suggestion in item.get('mitigation_suggestions', [])[:2]:
                output.append(f"    -> {suggestion}")

    # Sprint allocation
    if allocation:
        output.append("")
        output.append("SPRINT ALLOCATION")
        output.append("-" * 60)
        output.append(f"Capacity: {allocation['capacity']} points")
        output.append(f"Target (with 15% buffer): {allocation['target_capacity']} points")
        output.append(f"Allocated: {allocation['sprint_points']} points ({allocation['utilization']}%)")
        output.append(f"Sprint Items: {allocation['sprint_count']}")
        output.append(f"Remaining Backlog: {allocation['backlog_count']} items")
        output.append("")
        output.append("Sprint Backlog:")
        for item in allocation['sprint_items'][:10]:
            title = item.get('title', item.get('name', 'Unnamed'))[:25]
            output.append(f"  [{item.get('story_points', 0)} pts] {item.get('id', '-')}: {title}")

    output.append("")
    output.append("=" * 60)
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Prioritize backlog items using value/effort/risk scoring',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s backlog.json
  %(prog)s backlog.csv --capacity 30
  %(prog)s backlog.json --json
  %(prog)s backlog.json --quick-wins --high-risk
  %(prog)s backlog.csv --capacity 45 --output results.json

Input Format (JSON):
  [{"id": "US-001", "title": "Feature", "value": 8, "effort": 5, "risk": 3, "story_points": 5}]

Input Format (CSV):
  id,title,value,effort,risk,story_points
  US-001,Feature,8,5,3,5

Scoring Guide:
  value:  1-10 (business value, 10 = highest)
  effort: 1-10 (implementation difficulty, 10 = hardest)
  risk:   1-10 (uncertainty/risk, 10 = riskiest)
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='JSON or CSV file with backlog items'
    )
    parser.add_argument(
        '--capacity',
        type=int,
        help='Sprint capacity in story points (enables allocation)'
    )
    parser.add_argument(
        '--quick-wins',
        action='store_true',
        help='Identify quick wins (high value, low effort)'
    )
    parser.add_argument(
        '--high-risk',
        action='store_true',
        help='Flag high-risk items with mitigation suggestions'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--output', '-o',
        help='Write output to file'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Use sample data if no input
    if not args.input:
        if args.verbose:
            print("No input file specified, using sample data", file=sys.stderr)
        items = [
            {'id': 'US-001', 'title': 'User Authentication', 'value': 9, 'effort': 6, 'risk': 4, 'story_points': 8},
            {'id': 'US-002', 'title': 'Password Reset', 'value': 7, 'effort': 3, 'risk': 2, 'story_points': 3},
            {'id': 'US-003', 'title': 'Dark Mode', 'value': 5, 'effort': 4, 'risk': 2, 'story_points': 5},
            {'id': 'US-004', 'title': 'Real-time Sync', 'value': 8, 'effort': 9, 'risk': 8, 'story_points': 13},
            {'id': 'US-005', 'title': 'Email Notifications', 'value': 7, 'effort': 2, 'risk': 1, 'story_points': 2},
            {'id': 'US-006', 'title': 'Export to CSV', 'value': 4, 'effort': 2, 'risk': 1, 'story_points': 2},
            {'id': 'US-007', 'title': 'API Rate Limiting', 'value': 6, 'effort': 5, 'risk': 3, 'story_points': 5},
            {'id': 'US-008', 'title': 'Mobile App', 'value': 9, 'effort': 10, 'risk': 7, 'story_points': 21},
        ]
    else:
        if args.verbose:
            print(f"Loading backlog from: {args.input}", file=sys.stderr)
        try:
            items = detect_and_load(args.input)
        except FileNotFoundError:
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error loading file: {e}", file=sys.stderr)
            sys.exit(1)

    # Prioritize
    prioritizer = BacklogPrioritizer(verbose=args.verbose)

    if args.verbose:
        print(f"Prioritizing {len(items)} items...", file=sys.stderr)

    prioritized = prioritizer.prioritize_items(items)
    analysis = prioritizer.analyze_backlog(prioritized)

    # Optional analyses
    quick_wins = None
    high_risk = None
    allocation = None

    if args.quick_wins:
        quick_wins = prioritizer.identify_quick_wins(prioritized)
        if args.verbose:
            print(f"Found {len(quick_wins)} quick wins", file=sys.stderr)

    if args.high_risk:
        high_risk = prioritizer.identify_high_risk(prioritized)
        if args.verbose:
            print(f"Found {len(high_risk)} high-risk items", file=sys.stderr)

    if args.capacity:
        allocation = prioritizer.allocate_to_sprint(prioritized, args.capacity)
        if args.verbose:
            print(f"Allocated {allocation['sprint_count']} items to sprint", file=sys.stderr)

    # Format output
    if args.json:
        result = {
            'metadata': {
                'tool': 'prioritize_backlog',
                'version': '1.0.0',
                'generated_at': datetime.now().isoformat(),
                'formula': 'Priority = (value * 0.4) + ((10-effort) * 0.3) + ((10-risk) * 0.3)'
            },
            'prioritized_items': prioritized,
            'analysis': analysis
        }
        if quick_wins is not None:
            result['quick_wins'] = quick_wins
        if high_risk is not None:
            result['high_risk_items'] = high_risk
        if allocation is not None:
            result['sprint_allocation'] = allocation

        output = json.dumps(result, indent=2)
    else:
        output = format_text_output(
            prioritized, analysis, allocation, quick_wins, high_risk
        )

    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Output saved to: {args.output}")
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()
