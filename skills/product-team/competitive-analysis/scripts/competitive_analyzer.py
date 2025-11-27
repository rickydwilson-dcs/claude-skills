#!/usr/bin/env python3
"""
Competitive Analyzer - Core analysis engine for competitive comparison.

This tool analyzes competitor repositories against the claude-skills library,
scoring across 6 weighted dimensions and generating comparison reports.

Usage:
    python competitive_analyzer.py --help
    python competitive_analyzer.py --competitor-path ./competitor --our-path ./
    python competitive_analyzer.py --scope skills --competitor-path ./competitor
    python competitive_analyzer.py --output json --competitor-path ./competitor

Author: Claude Skills Team
Version: 1.0.0
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Competitive analysis engine for claude-skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic analysis
    python competitive_analyzer.py --competitor-path ./competitor-repo

    # Scope to skills only
    python competitive_analyzer.py --scope skills --competitor-path ./competitor

    # JSON output
    python competitive_analyzer.py --output json --competitor-path ./competitor

    # Full analysis with custom paths
    python competitive_analyzer.py --competitor-path ./competitor --our-path ./claude-skills
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
        "--scope",
        type=str,
        choices=["all", "skills", "commands", "agents"],
        default="all",
        help="Scope of analysis (default: all)"
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


def discover_items(path: str, scope: str) -> dict:
    """
    Discover skills, commands, and agents in a repository.

    Args:
        path: Path to repository
        scope: What to discover (all, skills, commands, agents)

    Returns:
        Dictionary with discovered items
    """
    items = {
        "skills": [],
        "commands": [],
        "agents": []
    }

    path = Path(path)

    if not path.exists():
        return items

    # Discover skills
    if scope in ["all", "skills"]:
        skills_paths = [
            path / "skills",
            path / "skill",
            path
        ]
        for skills_path in skills_paths:
            if skills_path.exists():
                for item in skills_path.rglob("SKILL.md"):
                    items["skills"].append({
                        "name": item.parent.name,
                        "path": str(item),
                        "type": "skill"
                    })

    # Discover commands
    if scope in ["all", "commands"]:
        commands_paths = [
            path / "commands",
            path / ".claude" / "commands"
        ]
        for cmd_path in commands_paths:
            if cmd_path.exists():
                for item in cmd_path.rglob("*.md"):
                    if item.name not in ["README.md", "CATALOG.md", "CLAUDE.md"]:
                        items["commands"].append({
                            "name": item.stem,
                            "path": str(item),
                            "type": "command"
                        })

    # Discover agents
    if scope in ["all", "agents"]:
        agents_paths = [
            path / "agents",
            path / "agent"
        ]
        for agents_path in agents_paths:
            if agents_path.exists():
                for item in agents_path.rglob("cs-*.md"):
                    items["agents"].append({
                        "name": item.stem,
                        "path": str(item),
                        "type": "agent"
                    })

    return items


def score_item(item_path: str) -> dict:
    """
    Score an individual item across 6 dimensions.

    Args:
        item_path: Path to the item file

    Returns:
        Dictionary with scores per dimension
    """
    # Placeholder scoring - actual implementation would parse and analyze content
    scores = {
        "documentation": 3,
        "tool_quality": 3,
        "workflows": 3,
        "architecture": 3,
        "automation": 3,
        "references": 3
    }

    try:
        with open(item_path, 'r') as f:
            content = f.read()

            # Documentation completeness
            if "```yaml" in content and "## Overview" in content:
                scores["documentation"] = 4
            if "## Examples" in content or "## Usage" in content:
                scores["documentation"] = 5

            # Workflow coverage
            workflow_count = content.count("## Workflow") + content.count("### Workflow")
            if workflow_count >= 4:
                scores["workflows"] = 5
            elif workflow_count >= 2:
                scores["workflows"] = 4

            # References
            if "references/" in content or "## References" in content:
                scores["references"] = 4
            if "assets/" in content or "templates/" in content:
                scores["references"] = 5

    except Exception:
        pass

    return scores


def calculate_weighted_score(scores: dict) -> float:
    """
    Calculate weighted total score.

    Weights:
    - Documentation: 20%
    - Tool Quality: 20%
    - Workflows: 15%
    - Architecture: 15%
    - Automation: 15%
    - References: 15%
    """
    weights = {
        "documentation": 0.20,
        "tool_quality": 0.20,
        "workflows": 0.15,
        "architecture": 0.15,
        "automation": 0.15,
        "references": 0.15
    }

    total = sum(scores[dim] * weights[dim] for dim in weights)
    return round(total, 2)


def compare_items(our_items: dict, their_items: dict) -> dict:
    """
    Compare items between repositories.

    Returns comparison results with winners for each item.
    """
    results = {
        "better": [],
        "same": [],
        "different": [],
        "behind": [],
        "only_ours": [],
        "only_theirs": []
    }

    # Placeholder comparison logic
    # Actual implementation would do semantic matching

    our_names = {item["name"] for items in our_items.values() for item in items}
    their_names = {item["name"] for items in their_items.values() for item in items}

    results["only_ours"] = list(our_names - their_names)
    results["only_theirs"] = list(their_names - our_names)

    return results


def generate_report(results: dict, output_format: str) -> str:
    """Generate analysis report in specified format."""

    if output_format == "json":
        return json.dumps(results, indent=2)

    # Console/Markdown format
    report = []
    report.append("=" * 50)
    report.append("       COMPETITIVE ANALYSIS REPORT")
    report.append("=" * 50)
    report.append("")
    report.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    report.append("┌─────────────────────────────────────┐")
    report.append("│      COMPETITIVE SCORECARD          │")
    report.append("├─────────────────────────────────────┤")
    report.append(f"│  🟢 Better:    {len(results.get('better', []):>2} features          │")
    report.append(f"│  ✅ Same:      {len(results.get('same', []):>2} features          │")
    report.append(f"│  🟡 Different: {len(results.get('different', []):>2} features          │")
    report.append(f"│  ❌ Behind:    {len(results.get('behind', []):>2} features          │")
    report.append("│                                     │")
    report.append("│  Overall: ANALYSIS COMPLETE         │")
    report.append("└─────────────────────────────────────┘")
    report.append("")

    if results.get("only_ours"):
        report.append("## Our Unique Features")
        for item in results["only_ours"][:5]:
            report.append(f"  🟢 {item}")
        report.append("")

    if results.get("only_theirs"):
        report.append("## Their Unique Features (Gaps)")
        for item in results["only_theirs"][:5]:
            report.append(f"  🔴 {item}")
        report.append("")

    return "\n".join(report)


def main():
    """Main entry point."""
    args = parse_args()

    if args.verbose:
        print(f"Analyzing competitor at: {args.competitor_path}")
        print(f"Our repository: {args.our_path}")
        print(f"Scope: {args.scope}")
        print("")

    # Discover items
    our_items = discover_items(args.our_path, args.scope)
    their_items = discover_items(args.competitor_path, args.scope)

    if args.verbose:
        print(f"Found {sum(len(v) for v in our_items.values())} items in our repo")
        print(f"Found {sum(len(v) for v in their_items.values())} items in competitor repo")
        print("")

    # Compare
    results = compare_items(our_items, their_items)
    results["our_items"] = our_items
    results["their_items"] = their_items

    # Generate report
    report = generate_report(results, args.output)
    print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
