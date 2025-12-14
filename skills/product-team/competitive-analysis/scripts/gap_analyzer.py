#!/usr/bin/env python3
"""
Gap Analyzer - Identify and prioritize competitive gaps.

This tool analyzes gaps between your product and competitors,
categorizes them by severity, and calculates priority scores.

Usage:
    python gap_analyzer.py --help
    python gap_analyzer.py --competitor-path ./competitor
    python gap_analyzer.py --severity critical --competitor-path ./competitor
    python gap_analyzer.py --prioritize --competitor-path ./competitor

Author: Claude Skills Team
Version: 1.0.0
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Gap analysis for competitive intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic gap analysis
    python gap_analyzer.py --competitor-path ./competitor

    # Filter by severity
    python gap_analyzer.py --severity critical --competitor-path ./competitor

    # Generate prioritized list
    python gap_analyzer.py --prioritize --competitor-path ./competitor

    # JSON output
    python gap_analyzer.py --output json --competitor-path ./competitor
        """
    )

    parser.add_argument(
        "--competitor-path",
        type=str,
        required=True,
        help="Path to competitor repository or code"
    )

    parser.add_argument(
        "--our-path",
        type=str,
        default=".",
        help="Path to our repository (default: current directory)"
    )

    parser.add_argument(
        "--severity",
        type=str,
        choices=["all", "critical", "important", "nice-to-have"],
        default="all",
        help="Filter by severity level (default: all)"
    )

    parser.add_argument(
        "--prioritize",
        action="store_true",
        help="Sort results by priority score"
    )

    parser.add_argument(
        "--output",
        type=str,
        choices=["markdown", "json", "console"],
        default="console",
        help="Output format (default: console)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    return parser.parse_args()


def calculate_priority(impact: int, urgency: int, strategic: int, effort: int) -> float:
    """
    Calculate priority score using weighted formula.

    Formula: (Impact × 0.4) + (Urgency × 0.3) + (Strategic × 0.2) + (1/Effort × 0.1)

    Args:
        impact: User impact score (1-5)
        urgency: Competitive urgency (1-5)
        strategic: Strategic alignment (1-5)
        effort: Implementation effort (1-5, lower is less effort)

    Returns:
        Priority score (0-5)
    """
    logger.debug(f"Calculating priority: impact={impact}, urgency={urgency}, strategic={strategic}, effort={effort}")
    if effort == 0:
        logger.warning("Effort is 0, using default value of 5 for inverse calculation")
    effort_inverse = 5 / effort if effort > 0 else 5
    score = (impact * 0.4) + (urgency * 0.3) + (strategic * 0.2) + (effort_inverse * 0.1)
    return round(score, 2)


def classify_severity(priority_score: float) -> str:
    """Classify gap severity based on priority score."""
    logger.debug(f"Classifying severity for priority score: {priority_score}")
    if priority_score >= 4.0:
        return "critical"
    elif priority_score >= 3.0:
        return "important"
    elif priority_score >= 2.0:
        return "nice-to-have"
    else:
        return "low"


def identify_gaps(our_path: str, competitor_path: str) -> list:
    """
    Identify gaps between our product and competitor.

    Returns list of gap dictionaries with scoring.
    """
    logger.debug(f"Identifying gaps: our_path={our_path}, competitor_path={competitor_path}")
    gaps = []

    # Placeholder gap identification
    # Actual implementation would analyze both repositories

    our_path = Path(our_path)
    competitor_path = Path(competitor_path)

    # Example gaps for demonstration
    example_gaps = [
        {
            "name": "Automated Test Generation",
            "category": "gap_to_fill",
            "description": "Competitor has automated test generation, we don't",
            "impact": 4,
            "urgency": 3,
            "strategic": 5,
            "effort": 2,
            "recommendation": "Prioritize for Q1 implementation"
        },
        {
            "name": "CLI Error Messages",
            "category": "behind",
            "description": "Competitor has better CLI error messages",
            "impact": 3,
            "urgency": 2,
            "strategic": 3,
            "effort": 4,
            "recommendation": "Improve error handling in existing tools"
        },
        {
            "name": "Zero Dependencies",
            "category": "advantage",
            "description": "We have zero-dependency design, they require pip installs",
            "impact": 4,
            "urgency": 0,
            "strategic": 5,
            "effort": 0,
            "recommendation": "Maintain and highlight as differentiator"
        }
    ]

    for gap in example_gaps:
        gap["priority_score"] = calculate_priority(
            gap["impact"],
            gap["urgency"],
            gap["strategic"],
            gap["effort"] if gap["effort"] > 0 else 1
        )
        gap["severity"] = classify_severity(gap["priority_score"])
        gaps.append(gap)

    return gaps


def filter_gaps(gaps: list, severity: str) -> list:
    """Filter gaps by severity level."""
    logger.debug(f"Filtering gaps by severity: {severity}")
    if severity == "all":
        return gaps
    filtered = [g for g in gaps if g["severity"] == severity]
    logger.debug(f"Filtered {len(filtered)} gaps out of {len(gaps)}")
    return filtered


def sort_by_priority(gaps: list) -> list:
    """Sort gaps by priority score (descending)."""
    logger.debug("Sorting gaps by priority score")
    return sorted(gaps, key=lambda x: x["priority_score"], reverse=True)


def generate_report(gaps: list, output_format: str) -> str:
    """Generate gap analysis report."""
    logger.debug(f"Generating report in {output_format} format with {len(gaps)} gaps")

    if output_format == "json":
        return json.dumps(gaps, indent=2)

    # Console/Markdown format
    report = []
    report.append("=" * 50)
    report.append("         GAP ANALYSIS REPORT")
    report.append("=" * 50)
    report.append("")
    report.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Total Gaps Identified: {len(gaps)}")
    report.append("")

    # Summary by category
    categories = {}
    for gap in gaps:
        cat = gap["category"]
        categories[cat] = categories.get(cat, 0) + 1

    report.append("┌─────────────────────────────────────┐")
    report.append("│         GAP SUMMARY                 │")
    report.append("├─────────────────────────────────────┤")
    report.append(f"│  🔴 Gaps to Fill:    {categories.get('gap_to_fill', 0):>2}            │")
    report.append(f"│  🟢 Advantages:      {categories.get('advantage', 0):>2}            │")
    report.append(f"│  ❌ Areas Behind:    {categories.get('behind', 0):>2}            │")
    report.append(f"│  🟡 Different:       {categories.get('different', 0):>2}            │")
    report.append("└─────────────────────────────────────┘")
    report.append("")

    # Detailed gaps
    report.append("## Prioritized Gap List")
    report.append("")

    for i, gap in enumerate(gaps, 1):
        severity_icon = {
            "critical": "🔴",
            "important": "🟠",
            "nice-to-have": "🟡",
            "low": "⚪"
        }.get(gap["severity"], "⚪")

        category_icon = {
            "gap_to_fill": "🔴",
            "advantage": "🟢",
            "behind": "❌",
            "different": "🟡"
        }.get(gap["category"], "⚪")

        report.append(f"{i}. {category_icon} **{gap['name']}** {severity_icon}")
        report.append(f"   Priority: {gap['priority_score']}/5.00 | Severity: {gap['severity'].upper()}")
        report.append(f"   {gap['description']}")
        report.append(f"   → {gap['recommendation']}")
        report.append("")

    return "\n".join(report)


def main():
    """Main entry point."""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
        print(f"Analyzing gaps with competitor at: {args.competitor_path}")
        print(f"Severity filter: {args.severity}")
        print("")

    # Identify gaps
    gaps = identify_gaps(args.our_path, args.competitor_path)

    # Filter by severity
    gaps = filter_gaps(gaps, args.severity)

    # Sort by priority if requested
    if args.prioritize:
        gaps = sort_by_priority(gaps)

    if args.verbose:
        print(f"Found {len(gaps)} gaps matching criteria")
        print("")

    # Generate report
    report = generate_report(gaps, args.output)
    print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
