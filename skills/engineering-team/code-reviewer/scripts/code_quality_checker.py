#!/usr/bin/env python3
"""
Code Quality Checker - Static Analysis Tool

Scans source files for anti-patterns, code smells, and quality issues
across multiple programming languages. Uses pattern matching and AST
analysis for Python-specific checks.

Part of the code-reviewer skill package.
"""

import argparse
import ast
import csv
import json
import logging
import os
import re
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


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = 4  # Block merge - security vulnerabilities, data loss
    HIGH = 3      # Fix before merge - major bugs, significant debt
    MEDIUM = 2    # Plan to fix - code smells, minor issues
    LOW = 1       # Consider fixing - style, minor improvements


@dataclass
class Pattern:
    """Detection pattern definition"""
    id: str
    name: str
    regex: str
    severity: Severity
    languages: List[str]  # ["all"] or specific languages
    category: str
    message: str
    suggestion: str


@dataclass
class Finding:
    """A detected issue in the codebase"""
    pattern_id: str
    file_path: str
    line_number: int
    line_content: str
    severity: Severity
    category: str
    message: str
    suggestion: str


class CodeQualityChecker:
    """Static analysis tool for detecting code quality issues"""

    LANGUAGE_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.jsx': 'javascript',
        '.go': 'go',
        '.java': 'java',
        '.rb': 'ruby',
        '.rs': 'rust',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.hpp': 'cpp',
    }

    SKIP_DIRS = {
        'node_modules', '__pycache__', '.git', '.svn', '.hg',
        'venv', 'env', '.venv', '.env', 'dist', 'build',
        '.tox', '.pytest_cache', '.mypy_cache', 'coverage',
        'vendor', 'third_party', '.idea', '.vscode'
    }

    def __init__(self, target_path: str, language: str = 'auto',
                 min_severity: str = 'LOW', verbose: bool = False):
        self.target_path = Path(target_path)
        self.language = language
        self.min_severity = Severity[min_severity.upper()]
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.patterns = self._load_patterns()
        self.findings: List[Finding] = []
        self.files_analyzed = 0
        self.results: Dict = {}
        logger.debug("CodeQualityChecker initialized")

    def _load_patterns(self) -> List[Pattern]:
        """Load all detection patterns"""
        patterns = []

        # === SECURITY PATTERNS (CRITICAL) ===
        patterns.extend([
            Pattern(
                id="SEC-001", name="SQL Injection Risk",
                regex=r'["\'].*SELECT.*["\'].*\+|["\'].*INSERT.*["\'].*\+|["\'].*UPDATE.*["\'].*\+|["\'].*DELETE.*["\'].*\+',
                severity=Severity.CRITICAL, languages=["all"], category="security",
                message="Potential SQL injection - string concatenation in SQL query",
                suggestion="Use parameterized queries or prepared statements"
            ),
            Pattern(
                id="SEC-002", name="Command Injection",
                regex=r'subprocess.*shell\s*=\s*True|os\.system\s*\(|os\.popen\s*\(',
                severity=Severity.CRITICAL, languages=["python"], category="security",
                message="Potential command injection - shell execution detected",
                suggestion="Use subprocess with shell=False and pass args as list"
            ),
            Pattern(
                id="SEC-003", name="Hardcoded Password",
                regex=r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
                severity=Severity.CRITICAL, languages=["all"], category="security",
                message="Hardcoded password detected",
                suggestion="Use environment variables or secure credential storage"
            ),
            Pattern(
                id="SEC-004", name="Hardcoded API Key",
                regex=r'(?i)(api[_-]?key|apikey|api_secret)\s*[:=]\s*["\'][^"\']+["\']',
                severity=Severity.CRITICAL, languages=["all"], category="security",
                message="Hardcoded API key detected",
                suggestion="Use environment variables or secure secrets management"
            ),
            Pattern(
                id="SEC-005", name="AWS Credentials",
                regex=r'AKIA[0-9A-Z]{16}',
                severity=Severity.CRITICAL, languages=["all"], category="security",
                message="AWS access key ID detected",
                suggestion="Remove credentials and use IAM roles or environment variables"
            ),
            Pattern(
                id="SEC-006", name="Private Key",
                regex=r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
                severity=Severity.CRITICAL, languages=["all"], category="security",
                message="Private key detected in source code",
                suggestion="Remove private keys from source code immediately"
            ),
            Pattern(
                id="SEC-007", name="Eval Usage",
                regex=r'\beval\s*\(',
                severity=Severity.CRITICAL, languages=["python", "javascript", "typescript"], category="security",
                message="Use of eval() detected - potential code injection",
                suggestion="Avoid eval(); use safer alternatives like ast.literal_eval() or JSON.parse()"
            ),
            Pattern(
                id="SEC-008", name="innerHTML XSS",
                regex=r'\.innerHTML\s*=',
                severity=Severity.HIGH, languages=["javascript", "typescript"], category="security",
                message="innerHTML assignment - potential XSS vulnerability",
                suggestion="Use textContent or sanitize input before using innerHTML"
            ),
            Pattern(
                id="SEC-009", name="document.write",
                regex=r'document\.write\s*\(',
                severity=Severity.HIGH, languages=["javascript", "typescript"], category="security",
                message="document.write() usage - potential XSS and performance issues",
                suggestion="Use DOM manipulation methods instead"
            ),
        ])

        # === PYTHON-SPECIFIC PATTERNS ===
        patterns.extend([
            Pattern(
                id="PY-002", name="Bare Except",
                regex=r'except\s*:',
                severity=Severity.HIGH, languages=["python"], category="anti-pattern",
                message="Bare except clause catches all exceptions including KeyboardInterrupt",
                suggestion="Specify exception type: except Exception: or except SpecificError:"
            ),
            Pattern(
                id="PY-003", name="Except Pass",
                regex=r'except.*:\s*\n\s*pass\s*$',
                severity=Severity.HIGH, languages=["python"], category="anti-pattern",
                message="Exception silently ignored with pass",
                suggestion="Log the exception or handle it appropriately"
            ),
            Pattern(
                id="PY-004", name="Broad Exception",
                regex=r'except\s+Exception\s*:',
                severity=Severity.MEDIUM, languages=["python"], category="anti-pattern",
                message="Catching broad Exception type",
                suggestion="Catch specific exception types when possible"
            ),
            Pattern(
                id="PY-005", name="Import Star",
                regex=r'from\s+\w+(\.\w+)*\s+import\s+\*',
                severity=Severity.MEDIUM, languages=["python"], category="anti-pattern",
                message="Wildcard import pollutes namespace",
                suggestion="Import specific names: from module import name1, name2"
            ),
            Pattern(
                id="PY-006", name="Global Variable",
                regex=r'\bglobal\s+\w+',
                severity=Severity.MEDIUM, languages=["python"], category="anti-pattern",
                message="Global variable declaration",
                suggestion="Avoid globals; use class attributes or function parameters"
            ),
            Pattern(
                id="PY-007", name="Print Statement",
                regex=r'\bprint\s*\(',
                severity=Severity.LOW, languages=["python"], category="code-smell",
                message="Print statement found (may be debug code)",
                suggestion="Use logging module for production code"
            ),
        ])

        # === TYPESCRIPT/JAVASCRIPT PATTERNS ===
        patterns.extend([
            Pattern(
                id="TS-001", name="Any Type",
                regex=r':\s*any\b|<any>',
                severity=Severity.HIGH, languages=["typescript"], category="anti-pattern",
                message="Using 'any' type defeats TypeScript's type safety",
                suggestion="Use specific types or 'unknown' if type is truly unknown"
            ),
            Pattern(
                id="TS-002", name="Type Assertion to Any",
                regex=r'\bas\s+any\b',
                severity=Severity.HIGH, languages=["typescript"], category="anti-pattern",
                message="Type assertion to 'any' bypasses type checking",
                suggestion="Use proper type narrowing or fix the underlying type issue"
            ),
            Pattern(
                id="TS-003", name="Empty Catch Block",
                regex=r'catch\s*\([^)]*\)\s*\{\s*\}',
                severity=Severity.HIGH, languages=["javascript", "typescript"], category="anti-pattern",
                message="Empty catch block silently swallows errors",
                suggestion="Log the error or handle it appropriately"
            ),
            Pattern(
                id="TS-004", name="Var Declaration",
                regex=r'\bvar\s+\w+',
                severity=Severity.MEDIUM, languages=["javascript", "typescript"], category="anti-pattern",
                message="Using 'var' instead of 'let' or 'const'",
                suggestion="Use 'const' for constants, 'let' for variables"
            ),
            Pattern(
                id="TS-005", name="Loose Equality",
                regex=r'[^!=]==[^=]',
                severity=Severity.MEDIUM, languages=["javascript", "typescript"], category="anti-pattern",
                message="Using == instead of === (loose equality)",
                suggestion="Use === for strict equality comparison"
            ),
            Pattern(
                id="TS-006", name="Console Log",
                regex=r'console\.(log|debug|info)\s*\(',
                severity=Severity.LOW, languages=["javascript", "typescript"], category="code-smell",
                message="Console statement found (may be debug code)",
                suggestion="Remove or use proper logging framework"
            ),
            Pattern(
                id="TS-007", name="Props Mutation",
                regex=r'props\.\w+\s*=',
                severity=Severity.CRITICAL, languages=["javascript", "typescript"], category="anti-pattern",
                message="Direct mutation of props (React anti-pattern)",
                suggestion="Props should be read-only; use state or callbacks"
            ),
        ])

        # === GO PATTERNS ===
        patterns.extend([
            Pattern(
                id="GO-001", name="Ignored Error",
                regex=r',\s*_\s*:?=\s*\w+\s*\(',
                severity=Severity.HIGH, languages=["go"], category="anti-pattern",
                message="Error return value ignored",
                suggestion="Handle or explicitly check the error"
            ),
            Pattern(
                id="GO-002", name="Panic in Library",
                regex=r'\bpanic\s*\(',
                severity=Severity.HIGH, languages=["go"], category="anti-pattern",
                message="Using panic() - should return error instead",
                suggestion="Return error values instead of panicking"
            ),
        ])

        # === GENERAL PATTERNS ===
        patterns.extend([
            Pattern(
                id="GEN-001", name="TODO/FIXME",
                regex=r'\b(TODO|FIXME|HACK|XXX|BUG)\b',
                severity=Severity.LOW, languages=["all"], category="code-smell",
                message="TODO/FIXME comment found",
                suggestion="Address the TODO or create a ticket to track it"
            ),
            Pattern(
                id="GEN-002", name="Magic Number",
                regex=r'(?<![a-zA-Z_\d.])\d{4,}(?![a-zA-Z_\d.])',
                severity=Severity.MEDIUM, languages=["all"], category="code-smell",
                message="Magic number detected (4+ digits)",
                suggestion="Extract to a named constant with descriptive name"
            ),
            Pattern(
                id="GEN-003", name="Commented Code",
                regex=r'^\s*(#|//)\s*(if|for|while|def|function|class|return|import)\b',
                severity=Severity.LOW, languages=["all"], category="code-smell",
                message="Commented-out code detected",
                suggestion="Remove dead code; use version control for history"
            ),
        ])

        return patterns

    def discover_files(self) -> List[Path]:
        """Recursively find source files to analyze"""
        logger.debug(f"Discovering files in {self.target_path}")
        files = []

        if self.target_path.is_file():
            if self._is_source_file(self.target_path):
                return [self.target_path]
            logger.warning(f"File {self.target_path} is not a recognized source file")
            return []

        for root, dirs, filenames in os.walk(self.target_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]

            for filename in filenames:
                file_path = Path(root) / filename
                if self._is_source_file(file_path):
                    files.append(file_path)

        return sorted(files)

    def _is_source_file(self, path: Path) -> bool:
        """Check if file is a recognized source file"""
        return path.suffix.lower() in self.LANGUAGE_EXTENSIONS

    def detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        return self.LANGUAGE_EXTENSIONS.get(file_path.suffix.lower(), 'unknown')

    def read_file_safe(self, file_path: Path) -> Optional[str]:
        """Read file with graceful encoding error handling"""
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for encoding in encodings:
            try:
                return file_path.read_text(encoding=encoding)
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
                return None
        logger.warning(f"Failed to read {file_path} with any encoding")
        return None

    def match_patterns(self, content: str, language: str, file_path: str) -> List[Finding]:
        """Match regex patterns against file content"""
        findings = []
        lines = content.split('\n')

        for pattern in self.patterns:
            # Skip if pattern doesn't apply to this language
            if 'all' not in pattern.languages and language not in pattern.languages:
                continue

            # Skip if below minimum severity
            if pattern.severity.value < self.min_severity.value:
                continue

            try:
                regex = re.compile(pattern.regex, re.IGNORECASE if 'SEC-' in pattern.id else 0)
                for line_num, line in enumerate(lines, 1):
                    if regex.search(line):
                        findings.append(Finding(
                            pattern_id=pattern.id,
                            file_path=file_path,
                            line_number=line_num,
                            line_content=line.strip()[:100],
                            severity=pattern.severity,
                            category=pattern.category,
                            message=pattern.message,
                            suggestion=pattern.suggestion
                        ))
            except re.error as e:
                if self.verbose:
                    print(f"  Warning: Invalid regex for {pattern.id}: {e}")

        return findings

    def analyze_python_ast(self, content: str, file_path: str) -> List[Finding]:
        """Use AST to detect Python-specific issues"""
        findings = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return findings

        for node in ast.walk(tree):
            # PY-001: Mutable Default Arguments
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults + node.args.kw_defaults:
                    if default is not None and isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        findings.append(Finding(
                            pattern_id="PY-001",
                            file_path=file_path,
                            line_number=node.lineno,
                            line_content=f"def {node.name}(...)",
                            severity=Severity.HIGH,
                            category="anti-pattern",
                            message=f"Mutable default argument in function '{node.name}'",
                            suggestion="Use None as default and initialize inside function"
                        ))

        return findings

    def detect_long_lines(self, lines: List[str], file_path: str) -> List[Finding]:
        """Detect lines exceeding maximum length"""
        findings = []
        max_length = 120

        for line_num, line in enumerate(lines, 1):
            if len(line) > max_length:
                if Severity.LOW.value >= self.min_severity.value:
                    findings.append(Finding(
                        pattern_id="GEN-004",
                        file_path=file_path,
                        line_number=line_num,
                        line_content=f"Line length: {len(line)} chars",
                        severity=Severity.LOW,
                        category="style",
                        message=f"Line exceeds {max_length} characters ({len(line)} chars)",
                        suggestion=f"Break line to stay under {max_length} characters"
                    ))

        return findings

    def detect_deep_nesting(self, lines: List[str], file_path: str) -> List[Finding]:
        """Detect deeply nested code blocks"""
        findings = []
        max_depth = 4

        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue

            # Count leading whitespace
            stripped = line.lstrip()
            indent = len(line) - len(stripped)

            # Estimate nesting level (4 spaces or 1 tab = 1 level)
            if '\t' in line[:indent]:
                depth = line[:indent].count('\t')
            else:
                depth = indent // 4

            if depth >= max_depth:
                if Severity.MEDIUM.value >= self.min_severity.value:
                    findings.append(Finding(
                        pattern_id="GEN-005",
                        file_path=file_path,
                        line_number=line_num,
                        line_content=stripped[:80],
                        severity=Severity.MEDIUM,
                        category="complexity",
                        message=f"Deep nesting detected (level {depth})",
                        suggestion="Refactor to reduce nesting: extract methods, use early returns"
                    ))

        return findings

    def analyze_file(self, file_path: Path) -> List[Finding]:
        """Analyze a single file for issues"""
        findings = []
        language = self.detect_language(file_path)

        # Filter by language if specified
        if self.language != 'auto' and self.language != 'all':
            if language != self.language:
                return []

        content = self.read_file_safe(file_path)
        if content is None:
            return []

        rel_path = str(file_path.relative_to(self.target_path) if file_path.is_relative_to(self.target_path) else file_path)

        # Pattern matching
        findings.extend(self.match_patterns(content, language, rel_path))

        # Python AST analysis
        if language == 'python':
            findings.extend(self.analyze_python_ast(content, rel_path))

        # Line-based checks
        lines = content.split('\n')
        findings.extend(self.detect_long_lines(lines, rel_path))
        findings.extend(self.detect_deep_nesting(lines, rel_path))

        return findings

    def calculate_quality_score(self) -> Dict:
        """Calculate weighted quality score"""
        critical_count = sum(1 for f in self.findings if f.severity == Severity.CRITICAL)
        high_count = sum(1 for f in self.findings if f.severity == Severity.HIGH)
        medium_count = sum(1 for f in self.findings if f.severity == Severity.MEDIUM)
        low_count = sum(1 for f in self.findings if f.severity == Severity.LOW)

        # Penalty formula
        penalty = (critical_count * 20) + (high_count * 10) + (medium_count * 3) + (low_count * 1)
        score = max(0, min(100, 100 - penalty))

        return {
            'score': score,
            'grade': self._get_grade(score),
            'breakdown': {
                'critical': critical_count,
                'high': high_count,
                'medium': medium_count,
                'low': low_count
            }
        }

    def _get_grade(self, score: int) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return 'A'
        if score >= 80:
            return 'B'
        if score >= 70:
            return 'C'
        if score >= 60:
            return 'D'
        return 'F'

    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on findings"""
        recommendations = []
        quality = self.calculate_quality_score()

        if quality['breakdown']['critical'] > 0:
            recommendations.append(
                f"URGENT: Fix {quality['breakdown']['critical']} critical security issue(s) before merging"
            )

        if quality['breakdown']['high'] > 0:
            recommendations.append(
                f"Address {quality['breakdown']['high']} high-severity issue(s) before merging"
            )

        # Group findings by pattern
        pattern_counts: Dict[str, int] = {}
        for f in self.findings:
            pattern_counts[f.pattern_id] = pattern_counts.get(f.pattern_id, 0) + 1

        for pattern_id, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
            if count >= 3:
                recommendations.append(f"Found {count} instances of {pattern_id} - consider a bulk fix")

        if not recommendations and quality['score'] >= 90:
            recommendations.append("Code quality is excellent! No critical issues found.")

        return recommendations[:5]  # Limit to top 5 recommendations

    def run(self) -> Dict:
        """Execute the analysis"""
        logger.debug("Starting code quality analysis")
        if self.verbose:
            print(f"Analyzing: {self.target_path}")

        if not self.target_path.exists():
            logger.error(f"Target path does not exist: {self.target_path}")
            return {
                'status': 'error',
                'error': f"Target path does not exist: {self.target_path}"
            }

        files = self.discover_files()
        if self.verbose:
            print(f"Found {len(files)} source files")

        for file_path in files:
            if self.verbose:
                print(f"  Scanning: {file_path}")
            file_findings = self.analyze_file(file_path)
            self.findings.extend(file_findings)
            self.files_analyzed += 1

        quality_score = self.calculate_quality_score()

        self.results = {
            'status': 'success',
            'target': str(self.target_path),
            'analyzed_at': datetime.now().isoformat(),
            'files_analyzed': self.files_analyzed,
            'quality_score': quality_score,
            'findings': [
                {
                    'file': f.file_path,
                    'line': f.line_number,
                    'severity': f.severity.name,
                    'category': f.category,
                    'pattern_id': f.pattern_id,
                    'message': f.message,
                    'suggestion': f.suggestion,
                    'line_content': f.line_content
                }
                for f in sorted(self.findings, key=lambda x: (-x.severity.value, x.file_path, x.line_number))
            ],
            'recommendations': self.generate_recommendations()
        }

        return self.results

    def format_json(self) -> str:
        """Format results as JSON"""
        return json.dumps(self.results, indent=2)

    def format_csv(self) -> str:
        """Format results as CSV"""
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['file', 'line', 'severity', 'category', 'pattern_id', 'message', 'suggestion'])

        for f in self.results.get('findings', []):
            writer.writerow([
                f['file'], f['line'], f['severity'], f['category'],
                f['pattern_id'], f['message'], f['suggestion']
            ])

        return output.getvalue()

    def format_text(self) -> str:
        """Format results as human-readable text"""
        lines = []
        lines.append("=" * 60)
        lines.append("CODE QUALITY REPORT")
        lines.append("=" * 60)
        lines.append(f"Target: {self.results.get('target')}")
        lines.append(f"Files Analyzed: {self.results.get('files_analyzed')}")
        lines.append(f"Analyzed At: {self.results.get('analyzed_at')}")
        lines.append("")

        qs = self.results.get('quality_score', {})
        lines.append(f"Quality Score: {qs.get('score', 0)}/100 (Grade: {qs.get('grade', 'N/A')})")
        breakdown = qs.get('breakdown', {})
        lines.append(f"  Critical: {breakdown.get('critical', 0)}")
        lines.append(f"  High:     {breakdown.get('high', 0)}")
        lines.append(f"  Medium:   {breakdown.get('medium', 0)}")
        lines.append(f"  Low:      {breakdown.get('low', 0)}")
        lines.append("")

        findings = self.results.get('findings', [])
        if findings:
            lines.append(f"Findings ({len(findings)} total):")
            lines.append("-" * 40)
            for f in findings[:20]:  # Limit to first 20 in text output
                lines.append(f"[{f['severity']}] {f['pattern_id']}: {f['file']}:{f['line']}")
                lines.append(f"  {f['message']}")
                lines.append(f"  Fix: {f['suggestion']}")
                lines.append("")

            if len(findings) > 20:
                lines.append(f"... and {len(findings) - 20} more findings")
                lines.append("")

        recommendations = self.results.get('recommendations', [])
        if recommendations:
            lines.append("Recommendations:")
            lines.append("-" * 40)
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"{i}. {rec}")

        lines.append("=" * 60)
        return '\n'.join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Code Quality Checker - Static analysis for anti-patterns and code smells",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input ./src
  %(prog)s --input ./src --output json --file report.json
  %(prog)s --input ./src --language python --min-severity HIGH
  %(prog)s --input ./src -v

Severity Levels:
  CRITICAL - Security vulnerabilities, must fix immediately
  HIGH     - Major bugs/debt, fix before merge
  MEDIUM   - Code smells, plan to fix
  LOW      - Style issues, consider fixing
        """
    )

    parser.add_argument(
        '--input', '-i', required=True,
        help='Target file or directory to analyze'
    )
    parser.add_argument(
        '--output', '-o', choices=['text', 'json', 'csv'], default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--language', choices=['auto', 'python', 'typescript', 'javascript', 'go', 'all'],
        default='auto',
        help='Filter by language (default: auto-detect)'
    )
    parser.add_argument(
        '--min-severity', choices=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
        default='LOW',
        help='Minimum severity level to report (default: LOW)'
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

    checker = CodeQualityChecker(
        target_path=args.input,
        language=args.language,
        min_severity=args.min_severity,
        verbose=args.verbose
    )

    results = checker.run()

    if results.get('status') == 'error':
        print(f"Error: {results.get('error')}", file=sys.stderr)
        sys.exit(1)

    if args.output == 'json':
        output = checker.format_json()
    elif args.output == 'csv':
        output = checker.format_csv()
    else:
        output = checker.format_text()

    if args.file:
        Path(args.file).write_text(output)
        print(f"Results written to {args.file}")
    else:
        print(output)

    # Exit with non-zero if critical issues found
    if results.get('quality_score', {}).get('breakdown', {}).get('critical', 0) > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
