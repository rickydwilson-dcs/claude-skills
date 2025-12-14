#!/usr/bin/env python3
"""
PR Analyzer - Pull Request Change Analysis Tool

Analyzes pull request changes by examining git diff output to calculate
metrics, identify risk areas, and estimate review effort.

Part of the code-reviewer skill package.
"""

import argparse
import csv
import json
import logging
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class FileChange:
    """Represents a changed file in the PR"""
    path: str
    additions: int
    deletions: int
    status: str  # modified, added, deleted, renamed
    category: str  # source, test, config, docs, other


@dataclass
class RiskFlag:
    """A risk indicator found in the changes"""
    file_path: str
    risk_type: str  # security, breaking_change, config, dependency
    reason: str
    severity: RiskLevel


class PrAnalyzer:
    """Analyzes pull request changes for risks and review effort"""

    # File category patterns
    SOURCE_EXTENSIONS = {'.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.java', '.rb', '.rs', '.cpp', '.c', '.h'}
    CONFIG_PATTERNS = [
        r'package\.json$', r'requirements\.txt$', r'go\.mod$', r'Cargo\.toml$',
        r'\.env', r'config\.(yaml|yml|json|toml)$', r'settings\.(yaml|yml|json)$',
        r'Dockerfile$', r'docker-compose', r'\.github/workflows/',
        r'tsconfig\.json$', r'pyproject\.toml$', r'setup\.py$', r'setup\.cfg$'
    ]
    TEST_PATTERNS = [
        r'test_', r'_test\.', r'\.test\.', r'\.spec\.', r'/tests?/', r'__tests__/'
    ]
    DOC_PATTERNS = [
        r'\.md$', r'\.rst$', r'\.txt$', r'/docs?/', r'README', r'CHANGELOG', r'LICENSE'
    ]

    # Security-sensitive path patterns
    SECURITY_PATTERNS = [
        (r'auth|authentication|login|logout|signin|signout', 'Authentication logic'),
        (r'password|passwd|credential|secret', 'Password/credential handling'),
        (r'payment|billing|stripe|paypal|checkout', 'Payment processing'),
        (r'crypto|encrypt|decrypt|hash|cipher', 'Cryptography'),
        (r'token|jwt|oauth|session', 'Token/session management'),
        (r'permission|access|role|privilege|rbac|acl', 'Access control'),
        (r'sql|query|database|migration', 'Database operations'),
    ]

    # Breaking change patterns in diff content
    BREAKING_PATTERNS = [
        (r'^\-\s*export\s+(interface|type|class|function|const)', 'Removed export'),
        (r'^\+.*@deprecated', 'Added deprecation'),
        (r'ALTER\s+TABLE|DROP\s+(TABLE|COLUMN|INDEX)', 'Schema change'),
        (r'^\-\s*def\s+\w+\s*\(|^\-\s*function\s+\w+', 'Removed function'),
        (r'BREAKING\s*CHANGE', 'Breaking change marker'),
    ]

    # Security issues in diff content (additions only)
    SECURITY_DIFF_PATTERNS = [
        (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
        (r'api[_-]?key\s*[:=]\s*["\'][^"\']+["\']', 'Hardcoded API key'),
        (r'AKIA[0-9A-Z]{16}', 'AWS access key'),
        (r'-----BEGIN.*PRIVATE\s+KEY', 'Private key'),
        (r'eval\s*\(', 'eval() usage'),
        (r'subprocess.*shell\s*=\s*True', 'Shell injection risk'),
    ]

    def __init__(self, target_path: str, base_branch: str = 'main',
                 head_branch: str = 'HEAD', verbose: bool = False):
        self.target_path = Path(target_path).resolve()
        self.base_branch = base_branch
        self.head_branch = head_branch
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.file_changes: List[FileChange] = []
        self.risk_flags: List[RiskFlag] = []
        self.results: Dict = {}
        logger.debug("PrAnalyzer initialized")

    def run_git_command(self, args: List[str]) -> Tuple[str, int]:
        """Run a git command and return output and return code"""
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.target_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.stdout, result.returncode
        except subprocess.TimeoutExpired:
            return "Command timed out", 1
        except FileNotFoundError:
            return "Git not found", 1
        except Exception as e:
            return str(e), 1

    def check_git_repo(self) -> bool:
        """Check if target is a valid git repository"""
        output, code = self.run_git_command(['rev-parse', '--git-dir'])
        return code == 0

    def get_merge_base(self) -> Optional[str]:
        """Get the merge base between branches"""
        output, code = self.run_git_command(['merge-base', self.base_branch, self.head_branch])
        if code == 0:
            return output.strip()
        return None

    def get_diff_output(self) -> str:
        """Get the full diff between branches"""
        output, code = self.run_git_command([
            'diff', f'{self.base_branch}...{self.head_branch}'
        ])
        return output if code == 0 else ""

    def get_diff_stat(self) -> str:
        """Get diff statistics"""
        output, code = self.run_git_command([
            'diff', '--stat', f'{self.base_branch}...{self.head_branch}'
        ])
        return output if code == 0 else ""

    def get_changed_files(self) -> List[str]:
        """Get list of changed files"""
        output, code = self.run_git_command([
            'diff', '--name-only', f'{self.base_branch}...{self.head_branch}'
        ])
        if code == 0 and output:
            return [f.strip() for f in output.strip().split('\n') if f.strip()]
        return []

    def get_file_status(self) -> Dict[str, str]:
        """Get status (A/M/D/R) for each changed file"""
        output, code = self.run_git_command([
            'diff', '--name-status', f'{self.base_branch}...{self.head_branch}'
        ])
        status_map = {}
        if code == 0 and output:
            for line in output.strip().split('\n'):
                if line:
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        status = parts[0][0]  # First char: A, M, D, R
                        file_path = parts[-1]  # Last part is the filename
                        status_map[file_path] = {
                            'A': 'added', 'M': 'modified', 'D': 'deleted', 'R': 'renamed'
                        }.get(status, 'modified')
        return status_map

    def get_commit_messages(self) -> List[str]:
        """Get commit messages between branches"""
        output, code = self.run_git_command([
            'log', '--oneline', f'{self.base_branch}..{self.head_branch}'
        ])
        if code == 0 and output:
            return [line.strip() for line in output.strip().split('\n') if line.strip()]
        return []

    def get_file_diff_stats(self, file_path: str) -> Tuple[int, int]:
        """Get additions and deletions for a specific file"""
        output, code = self.run_git_command([
            'diff', '--numstat', f'{self.base_branch}...{self.head_branch}', '--', file_path
        ])
        if code == 0 and output:
            parts = output.strip().split('\t')
            if len(parts) >= 2:
                try:
                    additions = int(parts[0]) if parts[0] != '-' else 0
                    deletions = int(parts[1]) if parts[1] != '-' else 0
                    return additions, deletions
                except ValueError:
                    pass
        return 0, 0

    def categorize_file(self, file_path: str) -> str:
        """Categorize a file based on its path and extension"""
        file_lower = file_path.lower()

        # Check test patterns first
        for pattern in self.TEST_PATTERNS:
            if re.search(pattern, file_lower):
                return 'test'

        # Check config patterns
        for pattern in self.CONFIG_PATTERNS:
            if re.search(pattern, file_lower):
                return 'config'

        # Check doc patterns
        for pattern in self.DOC_PATTERNS:
            if re.search(pattern, file_lower):
                return 'docs'

        # Check source extensions
        ext = Path(file_path).suffix.lower()
        if ext in self.SOURCE_EXTENSIONS:
            return 'source'

        return 'other'

    def parse_file_changes(self) -> List[FileChange]:
        """Parse all file changes with stats"""
        files = self.get_changed_files()
        status_map = self.get_file_status()
        changes = []

        for file_path in files:
            additions, deletions = self.get_file_diff_stats(file_path)
            status = status_map.get(file_path, 'modified')
            category = self.categorize_file(file_path)

            changes.append(FileChange(
                path=file_path,
                additions=additions,
                deletions=deletions,
                status=status,
                category=category
            ))

        return changes

    def identify_path_risks(self) -> List[RiskFlag]:
        """Identify risks based on file paths"""
        risks = []

        for change in self.file_changes:
            file_lower = change.path.lower()

            # Check security-sensitive paths
            for pattern, description in self.SECURITY_PATTERNS:
                if re.search(pattern, file_lower, re.IGNORECASE):
                    risks.append(RiskFlag(
                        file_path=change.path,
                        risk_type='security',
                        reason=f"{description} modified",
                        severity=RiskLevel.HIGH
                    ))
                    break  # One risk per file for path-based checks

            # Config file changes
            if change.category == 'config':
                risks.append(RiskFlag(
                    file_path=change.path,
                    risk_type='config',
                    reason='Configuration file changed',
                    severity=RiskLevel.MEDIUM
                ))

        return risks

    def scan_diff_for_security(self, diff_output: str) -> List[RiskFlag]:
        """Scan diff for security issues in added lines"""
        logger.debug("Scanning diff for security issues")
        risks = []
        current_file = ""

        for line in diff_output.split('\n'):
            # Track current file
            if line.startswith('+++ b/'):
                current_file = line[6:]
            elif line.startswith('+++ '):
                current_file = line[4:]

            # Only check added lines (not file headers)
            if line.startswith('+') and not line.startswith('+++'):
                added_content = line[1:]  # Remove the '+' prefix

                for pattern, description in self.SECURITY_DIFF_PATTERNS:
                    if re.search(pattern, added_content, re.IGNORECASE):
                        risks.append(RiskFlag(
                            file_path=current_file,
                            risk_type='security',
                            reason=f"{description} in added code",
                            severity=RiskLevel.CRITICAL
                        ))

        return risks

    def detect_breaking_changes(self, diff_output: str) -> List[RiskFlag]:
        """Detect potential breaking changes in the diff"""
        risks = []
        current_file = ""

        for line in diff_output.split('\n'):
            # Track current file
            if line.startswith('+++ b/'):
                current_file = line[6:]
            elif line.startswith('--- a/'):
                current_file = line[6:]

            for pattern, description in self.BREAKING_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    risks.append(RiskFlag(
                        file_path=current_file,
                        risk_type='breaking_change',
                        reason=description,
                        severity=RiskLevel.HIGH
                    ))

        # Deduplicate by file and reason
        seen = set()
        unique_risks = []
        for risk in risks:
            key = (risk.file_path, risk.reason)
            if key not in seen:
                seen.add(key)
                unique_risks.append(risk)

        return unique_risks

    def calculate_risk_score(self) -> int:
        """Calculate overall risk score"""
        score = 0
        for risk in self.risk_flags:
            if risk.severity == RiskLevel.CRITICAL:
                score += 25
            elif risk.severity == RiskLevel.HIGH:
                score += 15
            elif risk.severity == RiskLevel.MEDIUM:
                score += 5
            else:
                score += 1

        return min(100, score)

    def determine_risk_level(self, score: int) -> str:
        """Convert risk score to risk level"""
        if score >= 75:
            return 'critical'
        if score >= 50:
            return 'high'
        if score >= 20:
            return 'medium'
        return 'low'

    def estimate_review_time(self) -> int:
        """Estimate review time in minutes"""
        total_files = len(self.file_changes)
        total_lines = sum(c.additions + c.deletions for c in self.file_changes)
        num_risks = len(self.risk_flags)

        # Base formula: 2 min per file + 1 min per 50 lines
        base_time = (total_files * 2) + (total_lines // 50)

        # Risk multiplier
        if num_risks > 5:
            base_time = int(base_time * 1.75)
        elif num_risks > 3:
            base_time = int(base_time * 1.5)
        elif num_risks > 0:
            base_time = int(base_time * 1.2)

        # Clamp to reasonable bounds
        return max(10, min(120, base_time))

    def determine_priority(self) -> str:
        """Determine review priority based on risks and changes"""
        risk_score = self.calculate_risk_score()

        # Check for critical risks
        has_critical = any(r.severity == RiskLevel.CRITICAL for r in self.risk_flags)
        has_security = any(r.risk_type == 'security' for r in self.risk_flags)
        has_breaking = any(r.risk_type == 'breaking_change' for r in self.risk_flags)

        if has_critical or risk_score >= 75:
            return 'critical'
        if has_security or has_breaking or risk_score >= 50:
            return 'high'
        if risk_score >= 20:
            return 'medium'
        return 'low'

    def generate_focus_areas(self) -> List[str]:
        """Generate list of areas requiring careful review"""
        focus_areas = []

        # Group risks by file
        file_risks: Dict[str, List[str]] = {}
        for risk in self.risk_flags:
            if risk.file_path not in file_risks:
                file_risks[risk.file_path] = []
            file_risks[risk.file_path].append(risk.reason)

        # Create focus area descriptions
        for file_path, reasons in sorted(file_risks.items(), key=lambda x: -len(x[1])):
            if len(reasons) > 1:
                focus_areas.append(f"{file_path} - Multiple concerns: {', '.join(set(reasons[:2]))}")
            else:
                focus_areas.append(f"{file_path} - {reasons[0]}")

        # Add high-churn files (lots of changes)
        sorted_by_changes = sorted(
            self.file_changes,
            key=lambda x: x.additions + x.deletions,
            reverse=True
        )
        for change in sorted_by_changes[:3]:
            if change.additions + change.deletions > 100:
                area = f"{change.path} - Large change ({change.additions}+ / {change.deletions}-)"
                if area not in focus_areas:
                    focus_areas.append(area)

        return focus_areas[:10]  # Limit to top 10

    def run(self) -> Dict:
        """Execute the PR analysis"""
        logger.debug("Starting PR analysis")
        if self.verbose:
            print(f"Analyzing: {self.target_path}")
            print(f"Comparing: {self.base_branch}...{self.head_branch}")

        # Validate git repo
        if not self.check_git_repo():
            logger.error(f"Not a git repository: {self.target_path}")
            return {
                'status': 'error',
                'error': f"Not a git repository: {self.target_path}"
            }

        # Check if branches exist
        merge_base = self.get_merge_base()
        if not merge_base:
            logger.error(f"Cannot find merge base between {self.base_branch} and {self.head_branch}")
            return {
                'status': 'error',
                'error': f"Cannot find merge base between {self.base_branch} and {self.head_branch}"
            }

        # Parse file changes
        logger.debug("Parsing file changes")
        self.file_changes = self.parse_file_changes()
        if self.verbose:
            print(f"Found {len(self.file_changes)} changed files")

        # Get diff for content analysis
        diff_output = self.get_diff_output()

        # Identify risks
        self.risk_flags = []
        self.risk_flags.extend(self.identify_path_risks())
        self.risk_flags.extend(self.scan_diff_for_security(diff_output))
        self.risk_flags.extend(self.detect_breaking_changes(diff_output))

        if self.verbose:
            print(f"Found {len(self.risk_flags)} risk flags")

        # Calculate metrics
        total_additions = sum(c.additions for c in self.file_changes)
        total_deletions = sum(c.deletions for c in self.file_changes)
        commit_messages = self.get_commit_messages()
        risk_score = self.calculate_risk_score()

        # Organize file breakdown by category
        file_breakdown: Dict[str, List[str]] = {
            'source': [], 'test': [], 'config': [], 'docs': [], 'other': []
        }
        for change in self.file_changes:
            file_breakdown[change.category].append(change.path)

        # Remove empty categories
        file_breakdown = {k: v for k, v in file_breakdown.items() if v}

        # Build results
        self.results = {
            'status': 'success',
            'analyzed_at': datetime.now().isoformat(),
            'pr_info': {
                'base_branch': self.base_branch,
                'head_branch': self.head_branch,
                'merge_base': merge_base,
                'commits': len(commit_messages),
                'commit_messages': commit_messages[:10]  # Limit to 10
            },
            'summary': {
                'files_changed': len(self.file_changes),
                'lines_added': total_additions,
                'lines_removed': total_deletions,
                'net_change': total_additions - total_deletions
            },
            'file_breakdown': file_breakdown,
            'file_details': [
                {
                    'path': c.path,
                    'status': c.status,
                    'category': c.category,
                    'additions': c.additions,
                    'deletions': c.deletions
                }
                for c in sorted(self.file_changes, key=lambda x: -(x.additions + x.deletions))
            ],
            'risk_assessment': {
                'risk_score': risk_score,
                'risk_level': self.determine_risk_level(risk_score),
                'flags': [
                    {
                        'file': r.file_path,
                        'type': r.risk_type,
                        'reason': r.reason,
                        'severity': r.severity.name
                    }
                    for r in sorted(self.risk_flags, key=lambda x: -x.severity.value)
                ]
            },
            'security_findings': [
                {
                    'file': r.file_path,
                    'reason': r.reason,
                    'severity': r.severity.name
                }
                for r in self.risk_flags if r.risk_type == 'security'
            ],
            'breaking_changes': [
                {
                    'file': r.file_path,
                    'reason': r.reason
                }
                for r in self.risk_flags if r.risk_type == 'breaking_change'
            ],
            'review_recommendation': {
                'priority': self.determine_priority(),
                'estimated_time_minutes': self.estimate_review_time(),
                'focus_areas': self.generate_focus_areas()
            }
        }

        return self.results

    def format_json(self) -> str:
        """Format results as JSON"""
        return json.dumps(self.results, indent=2)

    def format_csv(self) -> str:
        """Format file changes as CSV"""
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['file', 'status', 'category', 'additions', 'deletions', 'risks'])

        # Create risk lookup
        file_risks: Dict[str, List[str]] = {}
        for risk in self.risk_flags:
            if risk.file_path not in file_risks:
                file_risks[risk.file_path] = []
            file_risks[risk.file_path].append(risk.reason)

        for change in self.file_changes:
            risks = '; '.join(file_risks.get(change.path, []))
            writer.writerow([
                change.path, change.status, change.category,
                change.additions, change.deletions, risks
            ])

        return output.getvalue()

    def format_text(self) -> str:
        """Format results as human-readable text"""
        lines = []
        lines.append("=" * 60)
        lines.append("PR ANALYSIS REPORT")
        lines.append("=" * 60)

        pr = self.results.get('pr_info', {})
        lines.append(f"Base: {pr.get('base_branch')}")
        lines.append(f"Head: {pr.get('head_branch')}")
        lines.append(f"Commits: {pr.get('commits', 0)}")
        lines.append("")

        summary = self.results.get('summary', {})
        lines.append(f"Files Changed: {summary.get('files_changed', 0)}")
        lines.append(f"Lines Added:   +{summary.get('lines_added', 0)}")
        lines.append(f"Lines Removed: -{summary.get('lines_removed', 0)}")
        lines.append(f"Net Change:    {summary.get('net_change', 0)}")
        lines.append("")

        # File breakdown
        breakdown = self.results.get('file_breakdown', {})
        if breakdown:
            lines.append("File Breakdown:")
            for category, files in breakdown.items():
                lines.append(f"  {category}: {len(files)} files")
            lines.append("")

        # Risk assessment
        risk = self.results.get('risk_assessment', {})
        lines.append(f"Risk Score: {risk.get('risk_score', 0)}/100 ({risk.get('risk_level', 'unknown').upper()})")

        flags = risk.get('flags', [])
        if flags:
            lines.append("")
            lines.append("Risk Flags:")
            lines.append("-" * 40)
            for flag in flags[:10]:
                lines.append(f"[{flag['severity']}] {flag['type']}: {flag['file']}")
                lines.append(f"  {flag['reason']}")

        # Security findings
        security = self.results.get('security_findings', [])
        if security:
            lines.append("")
            lines.append("Security Findings:")
            lines.append("-" * 40)
            for finding in security:
                lines.append(f"[{finding['severity']}] {finding['file']}: {finding['reason']}")

        # Review recommendation
        lines.append("")
        rec = self.results.get('review_recommendation', {})
        lines.append(f"Review Priority: {rec.get('priority', 'unknown').upper()}")
        lines.append(f"Estimated Time: {rec.get('estimated_time_minutes', 0)} minutes")

        focus = rec.get('focus_areas', [])
        if focus:
            lines.append("")
            lines.append("Focus Areas:")
            for area in focus[:5]:
                lines.append(f"  - {area}")

        lines.append("=" * 60)
        return '\n'.join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="PR Analyzer - Analyze pull request changes for risks and review effort",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input .
  %(prog)s --input . --base main --head feature/auth
  %(prog)s --input . --output json --file pr-analysis.json
  %(prog)s --input /path/to/repo -v

Risk Levels:
  CRITICAL - Security vulnerabilities in code
  HIGH     - Security-sensitive files, breaking changes
  MEDIUM   - Config changes, large modifications
  LOW      - Minor concerns
        """
    )

    parser.add_argument(
        '--input', '-i', required=True,
        help='Path to git repository'
    )
    parser.add_argument(
        '--base', default='main',
        help='Base branch for comparison (default: main)'
    )
    parser.add_argument(
        '--head', default='HEAD',
        help='Head branch/commit to analyze (default: HEAD)'
    )
    parser.add_argument(
        '--output', '-o', choices=['text', 'json', 'csv'], default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    analyzer = PrAnalyzer(
        target_path=args.input,
        base_branch=args.base,
        head_branch=args.head,
        verbose=args.verbose
    )

    results = analyzer.run()

    if results.get('status') == 'error':
        print(f"Error: {results.get('error')}", file=sys.stderr)
        sys.exit(1)

    if args.output == 'json':
        output = analyzer.format_json()
    elif args.output == 'csv':
        output = analyzer.format_csv()
    else:
        output = analyzer.format_text()

    if args.file:
        Path(args.file).write_text(output)
        print(f"Results written to {args.file}")
    else:
        print(output)

    # Exit with non-zero if critical risks found
    risk_level = results.get('risk_assessment', {}).get('risk_level', 'low')
    if risk_level == 'critical':
        sys.exit(1)


if __name__ == '__main__':
    main()
