#!/usr/bin/env python3
"""
Review Report Generator - Code Review Report Generation Tool

Generates comprehensive, human-readable code review reports from
quality analysis findings. Supports markdown, JSON, CSV, and text output.

Part of the code-reviewer skill package.
"""

import argparse
import csv
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class ReviewCategory(Enum):
    """Review categories for issue grouping"""
    BLOCKING = "blocking"    # Must fix before merge
    MAJOR = "major"          # Should fix before merge
    MINOR = "minor"          # Consider fixing
    NITPICK = "nitpick"      # Optional/stylistic


@dataclass
class Finding:
    """A code quality finding"""
    pattern_id: str
    file_path: str
    line_number: int
    line_content: str
    severity: Severity
    category: str
    message: str
    suggestion: str


class ReviewReportGenerator:
    """Generates comprehensive code review reports"""

    # Severity to review category mapping
    SEVERITY_TO_CATEGORY = {
        Severity.CRITICAL: ReviewCategory.BLOCKING,
        Severity.HIGH: ReviewCategory.MAJOR,
        Severity.MEDIUM: ReviewCategory.MINOR,
        Severity.LOW: ReviewCategory.NITPICK,
    }

    def __init__(self, findings_file: str = None, findings_data: List[Dict] = None,
                 quality_score: Dict = None, pr_metrics: Dict = None,
                 title: str = "Code Review Report", output_format: str = 'markdown',
                 verbose: bool = False):
        self.findings_file = findings_file
        self.findings_data = findings_data or []
        self.quality_score = quality_score or {}
        self.pr_metrics = pr_metrics or {}
        self.title = title
        self.output_format = output_format
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.findings: List[Finding] = []
        self.report_data: Dict = {}
        logger.debug("ReviewReportGenerator initialized")

    def load_findings(self) -> bool:
        """Load findings from file or provided data"""
        logger.debug("Loading findings")
        # Load from file if specified
        if self.findings_file:
            try:
                file_path = Path(self.findings_file)
                if not file_path.exists():
                    logger.warning(f"File not found: {self.findings_file}")
                    if self.verbose:
                        print(f"Warning: File not found: {self.findings_file}")
                    return False

                content = file_path.read_text()
                data = json.loads(content)

                # Handle code_quality_checker output format
                if 'findings' in data:
                    self.findings_data = data['findings']
                    if 'quality_score' in data and not self.quality_score:
                        self.quality_score = data['quality_score']
                else:
                    # Assume it's a list of findings
                    self.findings_data = data if isinstance(data, list) else []

            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in {self.findings_file}: {e}")
                if self.verbose:
                    print(f"Warning: Invalid JSON in {self.findings_file}: {e}")
                return False
            except Exception as e:
                logger.error(f"Error reading {self.findings_file}: {e}")
                if self.verbose:
                    print(f"Warning: Error reading {self.findings_file}: {e}")
                return False

        # Convert findings data to Finding objects
        for item in self.findings_data:
            try:
                # Handle different severity formats
                severity_str = item.get('severity', 'LOW')
                if isinstance(severity_str, str):
                    severity = Severity[severity_str.upper()]
                else:
                    severity = Severity.LOW

                finding = Finding(
                    pattern_id=item.get('pattern_id', item.get('id', 'UNKNOWN')),
                    file_path=item.get('file', item.get('file_path', 'unknown')),
                    line_number=item.get('line', item.get('line_number', 0)),
                    line_content=item.get('line_content', item.get('code', ''))[:100],
                    severity=severity,
                    category=item.get('category', 'general'),
                    message=item.get('message', 'No description'),
                    suggestion=item.get('suggestion', item.get('fix', 'No suggestion'))
                )
                self.findings.append(finding)
            except (KeyError, ValueError) as e:
                if self.verbose:
                    print(f"Warning: Skipping malformed finding: {e}")
                continue

        return True

    def categorize_by_severity(self) -> Dict[Severity, List[Finding]]:
        """Group findings by severity level"""
        result: Dict[Severity, List[Finding]] = {s: [] for s in Severity}
        for finding in self.findings:
            result[finding.severity].append(finding)
        return result

    def categorize_by_file(self) -> Dict[str, List[Finding]]:
        """Group findings by file path"""
        result: Dict[str, List[Finding]] = {}
        for finding in self.findings:
            if finding.file_path not in result:
                result[finding.file_path] = []
            result[finding.file_path].append(finding)
        return result

    def categorize_by_review_category(self) -> Dict[ReviewCategory, List[Finding]]:
        """Group findings by review category"""
        result: Dict[ReviewCategory, List[Finding]] = {c: [] for c in ReviewCategory}
        for finding in self.findings:
            category = self.SEVERITY_TO_CATEGORY.get(finding.severity, ReviewCategory.MINOR)
            result[category].append(finding)
        return result

    def prioritize_findings(self) -> List[Finding]:
        """Sort findings by severity (highest first), then by file"""
        return sorted(
            self.findings,
            key=lambda f: (-f.severity.value, f.file_path, f.line_number)
        )

    def generate_summary(self) -> Dict:
        """Generate summary statistics"""
        by_severity = self.categorize_by_severity()
        by_file = self.categorize_by_file()

        return {
            'total_findings': len(self.findings),
            'files_affected': len(by_file),
            'critical': len(by_severity[Severity.CRITICAL]),
            'high': len(by_severity[Severity.HIGH]),
            'medium': len(by_severity[Severity.MEDIUM]),
            'low': len(by_severity[Severity.LOW]),
        }

    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on findings"""
        recommendations = []
        summary = self.generate_summary()

        # Critical issues
        if summary['critical'] > 0:
            recommendations.append(
                f"URGENT: Fix {summary['critical']} critical security issue(s) immediately before merging"
            )

        # High severity issues
        if summary['high'] > 0:
            recommendations.append(
                f"Address {summary['high']} high-severity issue(s) before merging"
            )

        # Pattern-specific recommendations
        pattern_counts: Dict[str, int] = {}
        for finding in self.findings:
            pattern_counts[finding.pattern_id] = pattern_counts.get(finding.pattern_id, 0) + 1

        # Suggest bulk fixes for repeated patterns
        for pattern_id, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
            if count >= 3:
                recommendations.append(
                    f"Found {count} instances of {pattern_id} - consider a bulk fix or linter rule"
                )

        # File-specific recommendations
        by_file = self.categorize_by_file()
        high_issue_files = [
            (f, len(issues)) for f, issues in by_file.items()
            if len(issues) >= 5
        ]
        for file_path, count in sorted(high_issue_files, key=lambda x: -x[1])[:3]:
            recommendations.append(
                f"File '{file_path}' has {count} issues - consider refactoring"
            )

        # Positive recommendation if score is good
        score = self.quality_score.get('score', 0)
        if score >= 90 and not recommendations:
            recommendations.append("Code quality is excellent! No critical issues found.")
        elif score >= 80 and summary['critical'] == 0 and summary['high'] <= 2:
            recommendations.append("Good overall quality - address minor issues when convenient")

        return recommendations[:7]  # Limit to top 7

    def generate_positive_notes(self) -> List[str]:
        """Generate positive feedback based on analysis"""
        notes = []
        summary = self.generate_summary()
        score = self.quality_score.get('score', 0)

        if score >= 90:
            notes.append("Excellent code quality score (A grade)")
        elif score >= 80:
            notes.append("Good code quality score (B grade)")

        if summary['critical'] == 0:
            notes.append("No critical security issues detected")

        if summary['total_findings'] == 0:
            notes.append("No issues found - clean code!")

        if summary['files_affected'] == 0:
            notes.append("All analyzed files passed quality checks")

        # Check for good patterns (low issue density)
        by_file = self.categorize_by_file()
        clean_files = sum(1 for issues in by_file.values() if len(issues) <= 1)
        if clean_files > 0 and len(by_file) > 0:
            pct = (clean_files / len(by_file)) * 100
            if pct >= 80:
                notes.append(f"{pct:.0f}% of files have minimal or no issues")

        return notes[:5]  # Limit to top 5

    def _format_finding_detail(self, finding: Finding) -> str:
        """Format a single finding with full details (for blocking/major)"""
        lines = []
        lines.append(f"### {finding.pattern_id}: {finding.message}")
        lines.append(f"- **File:** `{finding.file_path}` (line {finding.line_number})")
        lines.append(f"- **Severity:** {finding.severity.name}")
        if finding.line_content:
            # Escape backticks in code
            code = finding.line_content.replace('`', '\\`')
            lines.append(f"- **Code:** `{code}`")
        lines.append(f"- **Fix:** {finding.suggestion}")
        lines.append("")
        return '\n'.join(lines)

    def _format_finding_compact(self, finding: Finding) -> str:
        """Format a single finding compactly (for minor/nitpick)"""
        return f"- **{finding.pattern_id}** `{finding.file_path}:{finding.line_number}` - {finding.message}"

    def format_markdown(self) -> str:
        """Generate full markdown report"""
        lines = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Header
        lines.append(f"# {self.title}")
        lines.append("")
        lines.append(f"**Generated:** {timestamp}")

        # Quality score
        if self.quality_score:
            score = self.quality_score.get('score', 'N/A')
            grade = self.quality_score.get('grade', 'N/A')
            lines.append(f"**Quality Score:** {score}/100 ({grade})")
        lines.append("")

        # Summary table
        summary = self.generate_summary()
        lines.append("## Summary")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Files Analyzed | {summary['files_affected']} |")
        lines.append(f"| Total Findings | {summary['total_findings']} |")
        lines.append(f"| Critical Issues | {summary['critical']} |")
        lines.append(f"| High Issues | {summary['high']} |")
        lines.append(f"| Medium Issues | {summary['medium']} |")
        lines.append(f"| Low Issues | {summary['low']} |")
        lines.append("")

        # Get findings by category
        by_category = self.categorize_by_review_category()

        # Blocking Issues
        lines.append("## Blocking Issues (Must Fix)")
        lines.append("")
        blocking = by_category[ReviewCategory.BLOCKING]
        if blocking:
            for finding in blocking:
                lines.append(self._format_finding_detail(finding))
        else:
            lines.append("> No blocking issues found.")
            lines.append("")

        # Major Issues
        lines.append("## Major Issues (Should Fix)")
        lines.append("")
        major = by_category[ReviewCategory.MAJOR]
        if major:
            for finding in major[:10]:  # Limit to 10
                lines.append(self._format_finding_detail(finding))
            if len(major) > 10:
                lines.append(f"*... and {len(major) - 10} more major issues*")
                lines.append("")
        else:
            lines.append("> No major issues found.")
            lines.append("")

        # Minor Issues
        lines.append("## Minor Issues (Consider)")
        lines.append("")
        minor = by_category[ReviewCategory.MINOR]
        if minor:
            for finding in minor[:15]:  # Limit to 15
                lines.append(self._format_finding_compact(finding))
            if len(minor) > 15:
                lines.append(f"- *... and {len(minor) - 15} more minor issues*")
            lines.append("")
        else:
            lines.append("> No minor issues found.")
            lines.append("")

        # Nitpicks
        lines.append("## Nitpicks")
        lines.append("")
        nitpicks = by_category[ReviewCategory.NITPICK]
        if nitpicks:
            for finding in nitpicks[:10]:  # Limit to 10
                lines.append(f"- `{finding.file_path}:{finding.line_number}` - {finding.message}")
            if len(nitpicks) > 10:
                lines.append(f"- *... and {len(nitpicks) - 10} more nitpicks*")
            lines.append("")
        else:
            lines.append("> No nitpicks.")
            lines.append("")

        # Positive Notes
        positive = self.generate_positive_notes()
        if positive:
            lines.append("## Positive Notes")
            lines.append("")
            for note in positive:
                lines.append(f"- {note}")
            lines.append("")

        # Recommendations
        recommendations = self.generate_recommendations()
        if recommendations:
            lines.append("## Recommendations")
            lines.append("")
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")

        # Footer
        lines.append("---")
        lines.append("*Generated by code-reviewer skill*")

        return '\n'.join(lines)

    def format_json(self) -> str:
        """Generate JSON report"""
        by_category = self.categorize_by_review_category()

        def findings_to_list(findings: List[Finding]) -> List[Dict]:
            return [
                {
                    'pattern_id': f.pattern_id,
                    'file': f.file_path,
                    'line': f.line_number,
                    'severity': f.severity.name,
                    'category': f.category,
                    'message': f.message,
                    'suggestion': f.suggestion,
                    'line_content': f.line_content
                }
                for f in findings
            ]

        self.report_data = {
            'title': self.title,
            'generated_at': datetime.now().isoformat(),
            'quality_score': self.quality_score,
            'summary': self.generate_summary(),
            'blocking_issues': findings_to_list(by_category[ReviewCategory.BLOCKING]),
            'major_issues': findings_to_list(by_category[ReviewCategory.MAJOR]),
            'minor_issues': findings_to_list(by_category[ReviewCategory.MINOR]),
            'nitpicks': findings_to_list(by_category[ReviewCategory.NITPICK]),
            'positive_notes': self.generate_positive_notes(),
            'recommendations': self.generate_recommendations(),
            'all_findings': findings_to_list(self.prioritize_findings())
        }

        return json.dumps(self.report_data, indent=2)

    def format_csv(self) -> str:
        """Generate CSV report"""
        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            'file', 'line', 'severity', 'category', 'pattern_id',
            'message', 'suggestion', 'review_category'
        ])

        # Data rows
        for finding in self.prioritize_findings():
            review_cat = self.SEVERITY_TO_CATEGORY.get(
                finding.severity, ReviewCategory.MINOR
            ).value
            writer.writerow([
                finding.file_path,
                finding.line_number,
                finding.severity.name,
                finding.category,
                finding.pattern_id,
                finding.message,
                finding.suggestion,
                review_cat
            ])

        return output.getvalue()

    def format_text(self) -> str:
        """Generate plain text report"""
        lines = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines.append("=" * 60)
        lines.append(self.title.upper())
        lines.append("=" * 60)
        lines.append(f"Generated: {timestamp}")

        if self.quality_score:
            score = self.quality_score.get('score', 'N/A')
            grade = self.quality_score.get('grade', 'N/A')
            lines.append(f"Quality Score: {score}/100 (Grade: {grade})")

        lines.append("")

        # Summary
        summary = self.generate_summary()
        lines.append("SUMMARY")
        lines.append("-" * 40)
        lines.append(f"Files Analyzed:  {summary['files_affected']}")
        lines.append(f"Total Findings:  {summary['total_findings']}")
        lines.append(f"  Critical:      {summary['critical']}")
        lines.append(f"  High:          {summary['high']}")
        lines.append(f"  Medium:        {summary['medium']}")
        lines.append(f"  Low:           {summary['low']}")
        lines.append("")

        # Findings by category
        by_category = self.categorize_by_review_category()

        # Blocking
        blocking = by_category[ReviewCategory.BLOCKING]
        lines.append("BLOCKING ISSUES (Must Fix)")
        lines.append("-" * 40)
        if blocking:
            for f in blocking:
                lines.append(f"[{f.severity.name}] {f.pattern_id}: {f.file_path}:{f.line_number}")
                lines.append(f"  {f.message}")
                lines.append(f"  Fix: {f.suggestion}")
                lines.append("")
        else:
            lines.append("  No blocking issues.")
            lines.append("")

        # Major
        major = by_category[ReviewCategory.MAJOR]
        lines.append("MAJOR ISSUES (Should Fix)")
        lines.append("-" * 40)
        if major:
            for f in major[:10]:
                lines.append(f"[{f.severity.name}] {f.pattern_id}: {f.file_path}:{f.line_number}")
                lines.append(f"  {f.message}")
            if len(major) > 10:
                lines.append(f"  ... and {len(major) - 10} more")
            lines.append("")
        else:
            lines.append("  No major issues.")
            lines.append("")

        # Recommendations
        recommendations = self.generate_recommendations()
        if recommendations:
            lines.append("RECOMMENDATIONS")
            lines.append("-" * 40)
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"{i}. {rec}")

        lines.append("")
        lines.append("=" * 60)

        return '\n'.join(lines)

    def run(self) -> str:
        """Execute report generation"""
        if self.verbose:
            print(f"Generating {self.output_format} report...")

        # Load findings
        self.load_findings()

        if self.verbose:
            print(f"Loaded {len(self.findings)} findings")

        # Generate report in requested format
        if self.output_format == 'json':
            return self.format_json()
        elif self.output_format == 'csv':
            return self.format_csv()
        elif self.output_format == 'text':
            return self.format_text()
        else:  # markdown
            return self.format_markdown()

    def write_report(self, output_path: str) -> None:
        """Write report to file"""
        report = self.run()
        Path(output_path).write_text(report)
        if self.verbose:
            print(f"Report written to {output_path}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Review Report Generator - Generate code review reports from analysis findings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input analysis.json
  %(prog)s --input analysis.json --output markdown --file report.md
  %(prog)s --input analysis.json --output json
  %(prog)s --input analysis.json --title "Sprint 5 Code Review"

Input Format:
  Accepts JSON from code_quality_checker.py or custom findings:
  {
    "quality_score": {"score": 78, "grade": "B"},
    "findings": [
      {"file": "app.py", "line": 10, "severity": "HIGH", ...}
    ]
  }
        """
    )

    parser.add_argument(
        '--input', '-i',
        help='JSON file with findings (from code_quality_checker.py)'
    )
    parser.add_argument(
        '--quality-score',
        help='Quality score as JSON string (e.g., \'{"score": 85, "grade": "B"}\')'
    )
    parser.add_argument(
        '--output', '-o',
        choices=['markdown', 'json', 'csv', 'text'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )
    parser.add_argument(
        '--title', '-t',
        default='Code Review Report',
        help='Report title (default: "Code Review Report")'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Parse quality score if provided
    quality_score = {}
    if args.quality_score:
        try:
            quality_score = json.loads(args.quality_score)
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid quality-score JSON: {e}", file=sys.stderr)

    # Create generator
    generator = ReviewReportGenerator(
        findings_file=args.input,
        quality_score=quality_score,
        title=args.title,
        output_format=args.output,
        verbose=args.verbose
    )

    # Generate report
    report = generator.run()

    # Output
    if args.file:
        Path(args.file).write_text(report)
        print(f"Report written to {args.file}")
    else:
        print(report)


if __name__ == '__main__':
    main()
