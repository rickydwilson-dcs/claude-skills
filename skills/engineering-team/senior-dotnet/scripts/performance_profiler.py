#!/usr/bin/env python3
"""
.NET Performance Profiler

Analyze .NET source code for performance issues including N+1 queries,
async/await antipatterns, memory allocation patterns, and EF Core issues.

Part of senior-dotnet skill for engineering-team.

Usage:
    python performance_profiler.py [options]
    python performance_profiler.py --analyze-queries src/
    python performance_profiler.py --help
    python performance_profiler.py --version
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict

__version__ = "1.0.0"


class PerformanceProfiler:
    """Analyze .NET code for performance issues."""

    # Patterns for detecting issues
    PATTERNS = {
        'n_plus_one': [
            (r'foreach.*\n.*await.*\.Find', 'N+1: Query inside foreach loop'),
            (r'for\s*\(.*\n.*await.*DbContext', 'N+1: Database call inside for loop'),
            (r'\.Select\(.*=>.*\.Where\(', 'N+1: Query inside Select projection'),
            (r'foreach.*\n.*\.Include\(', 'N+1: Include inside loop'),
        ],
        'async_antipatterns': [
            (r'\.Result\b', 'Blocking: Using .Result on async task'),
            (r'\.Wait\(\)', 'Blocking: Using .Wait() on async task'),
            (r'\.GetAwaiter\(\)\.GetResult\(\)', 'Blocking: Using GetAwaiter().GetResult()'),
            (r'Task\.Run\(.*async', 'Unnecessary Task.Run wrapping async method'),
            (r'async.*void\s+\w+\(', 'Async void method (except event handlers)'),
        ],
        'ef_core_issues': [
            (r'\.ToList\(\).*\.Where\(', 'Client evaluation: ToList() before Where()'),
            (r'\.ToList\(\).*\.Select\(', 'Potential client evaluation: ToList() before Select()'),
            (r'\.Include\(.*\.Include\(.*\.Include\(', 'Excessive Include: Consider using split queries'),
            (r'\.AsNoTracking\(\).*\.Update\(', 'AsNoTracking followed by Update'),
            (r'context\.SaveChanges\(\)', 'Synchronous SaveChanges: Use SaveChangesAsync'),
        ],
        'memory_issues': [
            (r'new\s+List<.*>\(\).*\.ToList\(\)', 'Double allocation: new List with ToList()'),
            (r'string\s+\+=', 'String concatenation in loop: Use StringBuilder'),
            (r'\.ToArray\(\).*\.ToList\(\)', 'Unnecessary conversion: ToArray then ToList'),
            (r'GC\.Collect\(\)', 'Manual GC.Collect: Usually unnecessary'),
        ],
        'general_issues': [
            (r'Thread\.Sleep\(', 'Blocking: Use Task.Delay instead'),
            (r'lock\s*\(.*this\)', 'Lock on this: Use dedicated lock object'),
            (r'catch\s*\(Exception\s*\)\s*\{', 'Empty catch: Swallowing exception'),
            (r'HttpClient\s+\w+\s*=\s*new\s+HttpClient', 'HttpClient instantiation: Use IHttpClientFactory'),
        ]
    }

    def __init__(self, source_path: str, analyze_queries: bool = True,
                 analyze_async: bool = True, analyze_memory: bool = True,
                 output_format: str = 'text', output_file: Optional[str] = None,
                 verbose: bool = False):
        """
        Initialize Performance Profiler.

        Args:
            source_path: Path to source code directory or file
            analyze_queries: Analyze for N+1 and EF Core issues
            analyze_async: Analyze for async/await antipatterns
            analyze_memory: Analyze for memory allocation issues
            output_format: Output format (text, json, markdown)
            output_file: Output file path
            verbose: Enable verbose output
        """
        self.source_path = Path(source_path)
        self.analyze_queries = analyze_queries
        self.analyze_async = analyze_async
        self.analyze_memory = analyze_memory
        self.output_format = output_format
        self.output_file = output_file
        self.verbose = verbose

    def _log(self, message: str) -> None:
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"  {message}")

    def analyze(self) -> Dict:
        """Analyze source code for performance issues."""
        results = {
            'success': True,
            'analyzed_at': datetime.now().isoformat(),
            'source_path': str(self.source_path),
            'files_analyzed': 0,
            'issues': [],
            'summary': {
                'n_plus_one': 0,
                'async_antipatterns': 0,
                'ef_core_issues': 0,
                'memory_issues': 0,
                'general_issues': 0,
                'total': 0
            },
            'recommendations': []
        }

        try:
            # Find all C# files
            if self.source_path.is_file():
                cs_files = [self.source_path]
            else:
                cs_files = list(self.source_path.rglob('*.cs'))

            if not cs_files:
                results['success'] = False
                results['error'] = f"No C# files found in {self.source_path}"
                return results

            for cs_file in cs_files:
                self._log(f"Analyzing {cs_file.name}")
                file_issues = self._analyze_file(cs_file)
                results['issues'].extend(file_issues)
                results['files_analyzed'] += 1

            # Categorize and count issues
            for issue in results['issues']:
                category = issue['category']
                if category in results['summary']:
                    results['summary'][category] += 1
                results['summary']['total'] += 1

            # Generate recommendations
            results['recommendations'] = self._generate_recommendations(results['summary'])

            # Write output if specified
            if self.output_file:
                self._write_output(results)

            return results

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'issues': []
            }

    def _analyze_file(self, file_path: Path) -> List[Dict]:
        """Analyze a single file for issues."""
        issues = []

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            # Check patterns by category
            categories_to_check = []

            if self.analyze_queries:
                categories_to_check.extend(['n_plus_one', 'ef_core_issues'])
            if self.analyze_async:
                categories_to_check.append('async_antipatterns')
            if self.analyze_memory:
                categories_to_check.append('memory_issues')

            categories_to_check.append('general_issues')

            for category in categories_to_check:
                if category not in self.PATTERNS:
                    continue

                for pattern, description in self.PATTERNS[category]:
                    matches = list(re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE))

                    for match in matches:
                        # Find line number
                        line_num = content[:match.start()].count('\n') + 1
                        line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ''

                        # Get context (surrounding lines)
                        start_line = max(0, line_num - 2)
                        end_line = min(len(lines), line_num + 2)
                        context = '\n'.join(lines[start_line:end_line])

                        issues.append({
                            'file': str(file_path),
                            'line': line_num,
                            'category': category,
                            'severity': self._get_severity(category),
                            'description': description,
                            'code': line_content,
                            'context': context,
                            'suggestion': self._get_suggestion(category, pattern)
                        })

        except Exception as e:
            self._log(f"Error analyzing {file_path}: {e}")

        return issues

    def _get_severity(self, category: str) -> str:
        """Get severity level for issue category."""
        severities = {
            'n_plus_one': 'high',
            'async_antipatterns': 'high',
            'ef_core_issues': 'medium',
            'memory_issues': 'medium',
            'general_issues': 'low'
        }
        return severities.get(category, 'low')

    def _get_suggestion(self, category: str, pattern: str) -> str:
        """Get fix suggestion for pattern."""
        suggestions = {
            r'\.Result\b': 'Use await instead of .Result',
            r'\.Wait\(\)': 'Use await instead of .Wait()',
            r'\.GetAwaiter\(\)\.GetResult\(\)': 'Use await or refactor to async',
            r'Task\.Run\(.*async': 'Remove Task.Run wrapper for async methods',
            r'async.*void\s+\w+\(': 'Return Task instead of void (except event handlers)',
            r'\.ToList\(\).*\.Where\(': 'Move Where() before ToList()',
            r'\.ToList\(\).*\.Select\(': 'Consider moving Select() before ToList()',
            r'context\.SaveChanges\(\)': 'Use SaveChangesAsync() for async operations',
            r'string\s+\+=': 'Use StringBuilder for string concatenation',
            r'Thread\.Sleep\(': 'Use await Task.Delay() instead',
            r'HttpClient\s+\w+\s*=\s*new\s+HttpClient': 'Use IHttpClientFactory for HttpClient instances',
        }

        for p, suggestion in suggestions.items():
            if p in pattern:
                return suggestion

        return 'Review and optimize this code pattern'

    def _generate_recommendations(self, summary: Dict) -> List[Dict]:
        """Generate recommendations based on analysis."""
        recommendations = []

        if summary['n_plus_one'] > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'N+1 Queries',
                'count': summary['n_plus_one'],
                'recommendation': 'Use eager loading with Include() or batch queries with AsSplitQuery()',
                'documentation': 'https://learn.microsoft.com/ef/core/querying/related-data'
            })

        if summary['async_antipatterns'] > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'Async Antipatterns',
                'count': summary['async_antipatterns'],
                'recommendation': 'Always use await instead of .Result/.Wait(). These cause deadlocks.',
                'documentation': 'https://learn.microsoft.com/dotnet/csharp/asynchronous-programming'
            })

        if summary['ef_core_issues'] > 0:
            recommendations.append({
                'priority': 'medium',
                'category': 'EF Core Issues',
                'count': summary['ef_core_issues'],
                'recommendation': 'Review query patterns to avoid client-side evaluation',
                'documentation': 'https://learn.microsoft.com/ef/core/querying'
            })

        if summary['memory_issues'] > 0:
            recommendations.append({
                'priority': 'medium',
                'category': 'Memory Allocation',
                'count': summary['memory_issues'],
                'recommendation': 'Reduce unnecessary allocations with Span<T>, ArrayPool, or StringBuilder',
                'documentation': 'https://learn.microsoft.com/dotnet/standard/memory-and-spans'
            })

        return recommendations

    def _write_output(self, results: Dict) -> None:
        """Write results to output file."""
        output_path = Path(self.output_file)

        if self.output_format == 'json':
            content = json.dumps(results, indent=2)
        elif self.output_format == 'markdown':
            content = self._format_markdown(results)
        else:
            content = self._format_text(results)

        output_path.write_text(content)
        self._log(f"Results written to {output_path}")

    def _format_text(self, results: Dict) -> str:
        """Format results as plain text."""
        lines = [
            "=" * 60,
            ".NET Performance Analysis Report",
            f"Generated: {results['analyzed_at']}",
            f"Source: {results['source_path']}",
            f"Files Analyzed: {results['files_analyzed']}",
            "=" * 60,
            "",
            "SUMMARY",
            "-" * 40,
            f"Total Issues: {results['summary']['total']}",
            f"  N+1 Queries: {results['summary']['n_plus_one']}",
            f"  Async Antipatterns: {results['summary']['async_antipatterns']}",
            f"  EF Core Issues: {results['summary']['ef_core_issues']}",
            f"  Memory Issues: {results['summary']['memory_issues']}",
            f"  General Issues: {results['summary']['general_issues']}",
            ""
        ]

        # Issues by severity
        high_issues = [i for i in results['issues'] if i['severity'] == 'high']
        medium_issues = [i for i in results['issues'] if i['severity'] == 'medium']
        low_issues = [i for i in results['issues'] if i['severity'] == 'low']

        if high_issues:
            lines.extend([
                "HIGH PRIORITY ISSUES",
                "-" * 40
            ])
            for issue in high_issues:
                lines.extend([
                    f"\n[{issue['category']}] {Path(issue['file']).name}:{issue['line']}",
                    f"  {issue['description']}",
                    f"  Code: {issue['code'][:80]}...",
                    f"  Fix: {issue['suggestion']}"
                ])

        if medium_issues:
            lines.extend([
                "",
                "MEDIUM PRIORITY ISSUES",
                "-" * 40
            ])
            for issue in medium_issues[:10]:  # Limit to 10
                lines.extend([
                    f"\n[{issue['category']}] {Path(issue['file']).name}:{issue['line']}",
                    f"  {issue['description']}"
                ])
            if len(medium_issues) > 10:
                lines.append(f"\n  ... and {len(medium_issues) - 10} more")

        # Recommendations
        if results['recommendations']:
            lines.extend([
                "",
                "RECOMMENDATIONS",
                "-" * 40
            ])
            for rec in results['recommendations']:
                lines.extend([
                    f"\n[{rec['priority'].upper()}] {rec['category']} ({rec['count']} issues)",
                    f"  {rec['recommendation']}",
                    f"  Docs: {rec['documentation']}"
                ])

        return '\n'.join(lines)

    def _format_markdown(self, results: Dict) -> str:
        """Format results as Markdown."""
        lines = [
            "# .NET Performance Analysis Report",
            "",
            f"**Generated:** {results['analyzed_at']}",
            f"**Source:** `{results['source_path']}`",
            f"**Files Analyzed:** {results['files_analyzed']}",
            "",
            "## Summary",
            "",
            "| Category | Count | Severity |",
            "|----------|-------|----------|",
            f"| N+1 Queries | {results['summary']['n_plus_one']} | High |",
            f"| Async Antipatterns | {results['summary']['async_antipatterns']} | High |",
            f"| EF Core Issues | {results['summary']['ef_core_issues']} | Medium |",
            f"| Memory Issues | {results['summary']['memory_issues']} | Medium |",
            f"| General Issues | {results['summary']['general_issues']} | Low |",
            f"| **Total** | **{results['summary']['total']}** | |",
            ""
        ]

        # High priority issues
        high_issues = [i for i in results['issues'] if i['severity'] == 'high']
        if high_issues:
            lines.extend([
                "## High Priority Issues",
                ""
            ])
            for issue in high_issues:
                lines.extend([
                    f"### {issue['description']}",
                    "",
                    f"- **File:** `{Path(issue['file']).name}:{issue['line']}`",
                    f"- **Category:** {issue['category']}",
                    f"- **Code:** `{issue['code'][:60]}...`",
                    f"- **Fix:** {issue['suggestion']}",
                    ""
                ])

        # Recommendations
        if results['recommendations']:
            lines.extend([
                "## Recommendations",
                ""
            ])
            for rec in results['recommendations']:
                lines.extend([
                    f"### {rec['category']}",
                    "",
                    f"**Priority:** {rec['priority'].upper()}",
                    f"**Issues Found:** {rec['count']}",
                    "",
                    f"{rec['recommendation']}",
                    "",
                    f"[Documentation]({rec['documentation']})",
                    ""
                ])

        lines.extend([
            "---",
            "",
            "*Generated by senior-dotnet performance_profiler.py*"
        ])

        return '\n'.join(lines)


def main():
    """Main entry point with CLI interface."""
    parser = argparse.ArgumentParser(
        description="Performance Profiler - Analyze .NET code for performance issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --analyze-queries src/
  %(prog)s src/ --output report.md --format markdown
  %(prog)s MyProject/ --format json

Analysis Types:
  --analyze-queries  Check for N+1 queries and EF Core issues
  --analyze-async    Check for async/await antipatterns
  --analyze-memory   Check for memory allocation issues

Output Formats:
  text     - Plain text report (default)
  json     - JSON format
  markdown - Markdown format

Part of senior-dotnet skill.
"""
    )

    parser.add_argument(
        'source_path',
        nargs='?',
        default='.',
        help='Path to source code directory or file (default: current directory)'
    )

    parser.add_argument(
        '--analyze-queries', '-q',
        action='store_true',
        default=True,
        help='Analyze for N+1 queries and EF Core issues (default: enabled)'
    )

    parser.add_argument(
        '--analyze-async', '-a',
        action='store_true',
        default=True,
        help='Analyze for async/await antipatterns (default: enabled)'
    )

    parser.add_argument(
        '--analyze-memory', '-m',
        action='store_true',
        default=True,
        help='Analyze for memory allocation issues (default: enabled)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file path'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()

    print(f"Analyzing: {args.source_path}")
    print()

    profiler = PerformanceProfiler(
        source_path=args.source_path,
        analyze_queries=args.analyze_queries,
        analyze_async=args.analyze_async,
        analyze_memory=args.analyze_memory,
        output_format=args.format,
        output_file=args.output,
        verbose=args.verbose
    )

    results = profiler.analyze()

    if results['success']:
        print(f"Analysis complete!")
        print(f"  Files analyzed: {results['files_analyzed']}")
        print(f"  Total issues: {results['summary']['total']}")
        print()

        if results['summary']['n_plus_one'] > 0:
            print(f"  [HIGH] N+1 Queries: {results['summary']['n_plus_one']}")
        if results['summary']['async_antipatterns'] > 0:
            print(f"  [HIGH] Async Antipatterns: {results['summary']['async_antipatterns']}")
        if results['summary']['ef_core_issues'] > 0:
            print(f"  [MEDIUM] EF Core Issues: {results['summary']['ef_core_issues']}")
        if results['summary']['memory_issues'] > 0:
            print(f"  [MEDIUM] Memory Issues: {results['summary']['memory_issues']}")

        if args.output:
            print(f"\nReport saved to: {args.output}")

        # Exit with non-zero if high priority issues found
        if results['summary']['n_plus_one'] > 0 or results['summary']['async_antipatterns'] > 0:
            sys.exit(1)
    else:
        print(f"Error: {results.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
