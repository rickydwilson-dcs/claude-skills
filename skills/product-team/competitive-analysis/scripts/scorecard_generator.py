#!/usr/bin/env python3
"""
Scorecard Generator - Generate visual competitive scorecards.

This tool generates visual scorecards and comparison tables from
competitive analysis data.

Usage:
    python scorecard_generator.py --help
    python scorecard_generator.py --analysis-file analysis.json
    python scorecard_generator.py --format ascii --analysis-file analysis.json
    python scorecard_generator.py --detailed --analysis-file analysis.json

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
        description="Generate visual competitive scorecards",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate scorecard from analysis file
    python scorecard_generator.py --analysis-file analysis.json

    # ASCII format output
    python scorecard_generator.py --format ascii --analysis-file analysis.json

    # Markdown format
    python scorecard_generator.py --format markdown --analysis-file analysis.json

    # Include detailed breakdown
    python scorecard_generator.py --detailed --analysis-file analysis.json
        """
    )

    parser.add_argument(
        "--analysis-file",
        type=str,
        help="Path to analysis JSON file (optional - generates sample if not provided)"
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["ascii", "markdown", "json"],
        default="ascii",
        help="Output format (default: ascii)"
    )

    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Include detailed dimension breakdown"
    )

    parser.add_argument(
        "--title",
        type=str,
        default="COMPETITIVE SCORECARD",
        help="Scorecard title"
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


def load_analysis(file_path: str) -> dict:
    """Load analysis data from JSON file."""
    logger.debug(f"Loading analysis from: {file_path if file_path else 'sample data'}")
    if file_path and Path(file_path).exists():
        with open(file_path, 'r') as f:
            return json.load(f)

    # Return sample data if no file provided
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "competitor": "Sample Competitor",
        "summary": {
            "better": 12,
            "same": 8,
            "different": 3,
            "behind": 2
        },
        "dimensions": {
            "ours": {
                "documentation": 4.5,
                "tool_quality": 4.0,
                "workflows": 5.0,
                "architecture": 5.0,
                "automation": 4.0,
                "references": 4.5
            },
            "theirs": {
                "documentation": 3.5,
                "tool_quality": 4.0,
                "workflows": 3.0,
                "architecture": 3.0,
                "automation": 3.5,
                "references": 3.0
            }
        },
        "overall": {
            "ours": 4.35,
            "theirs": 3.33,
            "assessment": "AHEAD"
        }
    }


def calculate_percentages(summary: dict) -> dict:
    """Calculate percentages for each category."""
    logger.debug("Calculating category percentages")
    total = sum(summary.values())
    if total == 0:
        logger.warning("Total summary count is 0, returning zero percentages")
        return {k: 0 for k in summary}
    return {k: round((v / total) * 100) for k, v in summary.items()}


def generate_ascii_scorecard(data: dict, title: str, detailed: bool) -> str:
    """Generate ASCII box scorecard."""
    logger.debug(f"Generating ASCII scorecard (detailed={detailed})")
    summary = data["summary"]
    percentages = calculate_percentages(summary)
    assessment = data["overall"]["assessment"]

    lines = []
    lines.append("┌─────────────────────────────────────┐")
    lines.append(f"│{title:^37}│")
    lines.append("├─────────────────────────────────────┤")
    lines.append(f"│  🟢 Better:    {summary['better']:>2} features  ({percentages['better']:>2}%)   │")
    lines.append(f"│  ✅ Same:      {summary['same']:>2} features  ({percentages['same']:>2}%)   │")
    lines.append(f"│  🟡 Different: {summary['different']:>2} features  ({percentages['different']:>2}%)   │")
    lines.append(f"│  ❌ Behind:    {summary['behind']:>2} features  ({percentages['behind']:>2}%)   │")
    lines.append("│                                     │")
    lines.append(f"│  Overall: {assessment:<25} │")
    lines.append("│  Confidence: HIGH                   │")
    lines.append("└─────────────────────────────────────┘")

    if detailed:
        lines.append("")
        lines.append("┌─────────────────────────────────────────────────┐")
        lines.append("│            DIMENSION BREAKDOWN                  │")
        lines.append("├──────────────────┬───────┬───────┬──────────────┤")
        lines.append("│ Dimension        │  Ours │Theirs │ Winner       │")
        lines.append("├──────────────────┼───────┼───────┼──────────────┤")

        dimensions = data["dimensions"]
        for dim in ["documentation", "tool_quality", "workflows", "architecture", "automation", "references"]:
            ours = dimensions["ours"].get(dim, 0)
            theirs = dimensions["theirs"].get(dim, 0)

            if ours > theirs + 0.5:
                winner = "🟢 Us"
            elif theirs > ours + 0.5:
                winner = "❌ Them"
            else:
                winner = "✅ Same"

            dim_display = dim.replace("_", " ").title()
            lines.append(f"│ {dim_display:<16} │ {ours:>5.1f} │ {theirs:>5.1f} │ {winner:<12} │")

        lines.append("├──────────────────┼───────┼───────┼──────────────┤")
        lines.append(f"│ {'TOTAL':<16} │ {data['overall']['ours']:>5.2f} │ {data['overall']['theirs']:>5.2f} │ {assessment:<12} │")
        lines.append("└──────────────────┴───────┴───────┴──────────────┘")

    return "\n".join(lines)


def generate_markdown_scorecard(data: dict, title: str, detailed: bool) -> str:
    """Generate markdown format scorecard."""
    logger.debug(f"Generating Markdown scorecard (detailed={detailed})")
    summary = data["summary"]
    percentages = calculate_percentages(summary)
    assessment = data["overall"]["assessment"]

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Date:** {data['date']}")
    lines.append(f"**Competitor:** {data['competitor']}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Category | Count | Percentage |")
    lines.append("|----------|:-----:|:----------:|")
    lines.append(f"| 🟢 Better | {summary['better']} | {percentages['better']}% |")
    lines.append(f"| ✅ Same | {summary['same']} | {percentages['same']}% |")
    lines.append(f"| 🟡 Different | {summary['different']} | {percentages['different']}% |")
    lines.append(f"| ❌ Behind | {summary['behind']} | {percentages['behind']}% |")
    lines.append("")
    lines.append(f"**Overall Assessment:** {assessment}")
    lines.append("")

    if detailed:
        lines.append("## Dimension Breakdown")
        lines.append("")
        lines.append("| Dimension | Ours | Theirs | Winner |")
        lines.append("|-----------|:----:|:------:|:------:|")

        dimensions = data["dimensions"]
        for dim in ["documentation", "tool_quality", "workflows", "architecture", "automation", "references"]:
            ours = dimensions["ours"].get(dim, 0)
            theirs = dimensions["theirs"].get(dim, 0)

            if ours > theirs + 0.5:
                winner = "🟢 Us"
            elif theirs > ours + 0.5:
                winner = "❌ Them"
            else:
                winner = "✅ Same"

            dim_display = dim.replace("_", " ").title()
            lines.append(f"| {dim_display} | {ours:.1f} | {theirs:.1f} | {winner} |")

        lines.append("")
        lines.append(f"**Total Score:** Ours: {data['overall']['ours']:.2f} vs Theirs: {data['overall']['theirs']:.2f}")

    return "\n".join(lines)


def main():
    """Main entry point."""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
        print(f"Loading analysis from: {args.analysis_file or 'sample data'}")
        print(f"Format: {args.format}")
        print("")

    # Load analysis data
    data = load_analysis(args.analysis_file)

    # Generate scorecard based on format
    if args.format == "json":
        output = json.dumps(data, indent=2)
    elif args.format == "markdown":
        output = generate_markdown_scorecard(data, args.title, args.detailed)
    else:  # ascii
        output = generate_ascii_scorecard(data, args.title, args.detailed)

    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
