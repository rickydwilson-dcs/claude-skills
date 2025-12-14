#!/usr/bin/env python3
"""
Performance Bottleneck Detector

Identifies performance anti-patterns and optimization opportunities in legacy code.
Detects database inefficiencies, loop problems, memory issues, I/O bottlenecks,
and algorithmic inefficiencies.

Usage:
    python performance_bottleneck_detector.py --input /path/to/code
    python performance_bottleneck_detector.py -i src/ --output json
    python performance_bottleneck_detector.py -i app.py --output csv --file report.csv
    python performance_bottleneck_detector.py -i . --verbose

Author: Claude Skills - Legacy Codebase Analyzer
Version: 1.0.0
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import IntEnum
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
import argparse
import json
import logging
import os
import re
import sys


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Severity(IntEnum):
    """Severity levels for bottleneck findings"""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class BottleneckCategory(IntEnum):
    """Categories of performance bottlenecks"""
    DATABASE = 1
    LOOP = 2
    MEMORY = 3
    IO = 4
    ALGORITHM = 5
    NETWORK = 6


@dataclass
class BottleneckFinding:
    """Represents a detected performance bottleneck"""
    category: str
    severity: str
    severity_value: int
    file_path: str
    line_number: int
    issue: str
    code_snippet: str
    recommendation: str
    impact: str
    estimated_improvement: str


class PerformanceBottleneckDetector:
    """Main detector class for identifying performance bottlenecks"""

    # Supported file extensions for analysis
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.java', '.cs', '.go', '.rb', '.php',
        '.jsx', '.tsx', '.cpp', '.c', '.h', '.hpp', '.sql'
    }

    # Database anti-patterns
    DB_PATTERNS = {
        'n_plus_one': {
            'pattern': r'for\s+\w+\s+in\s+\w+.*?\.query\(|\.find\(|\.get\(',
            'severity': Severity.CRITICAL,
            'issue': 'Potential N+1 query pattern detected',
            'recommendation': 'Use eager loading, joins, or batch queries to reduce database round trips',
            'impact': 'Can cause exponential increase in database queries with data growth',
            'improvement': '80-95% reduction in database queries'
        },
        'select_star': {
            'pattern': r'SELECT\s+\*\s+FROM|select\s+\*\s+from|\.findAll\(\)|\.find\(\s*\{?\s*\}?\s*\)',
            'severity': Severity.HIGH,
            'issue': 'SELECT * or fetch all fields detected',
            'recommendation': 'Specify only required fields to reduce data transfer and memory usage',
            'impact': 'Unnecessary data transfer and increased memory consumption',
            'improvement': '40-60% reduction in data transfer'
        },
        'unbounded_query': {
            'pattern': r'SELECT.*FROM(?!.*LIMIT|.*TOP\s+\d+).*?(?:WHERE|;)|\.find\(\)(?!.*limit)|\.query\(\)(?!.*limit)',
            'severity': Severity.CRITICAL,
            'issue': 'Unbounded query without LIMIT/pagination detected',
            'recommendation': 'Add LIMIT clause and implement pagination',
            'impact': 'Can load entire table into memory, causing OOM errors',
            'improvement': '90%+ reduction in memory usage'
        },
        'missing_index': {
            'pattern': r'WHERE\s+\w+\s*=|JOIN\s+\w+\s+ON\s+\w+\.',
            'severity': Severity.HIGH,
            'issue': 'Query with WHERE/JOIN that may need index',
            'recommendation': 'Add database index on frequently queried columns',
            'impact': 'Slow query execution, full table scans',
            'improvement': '70-99% reduction in query time'
        },
        'in_loop_query': {
            'pattern': r'for\s+.*?:\s*\n\s*.*?\.(execute|query|find|get)\(',
            'severity': Severity.CRITICAL,
            'issue': 'Database query inside loop',
            'recommendation': 'Move query outside loop and use batch operations',
            'impact': 'Multiple database round trips in loop iterations',
            'improvement': '85-95% reduction in query count'
        }
    }

    # Loop anti-patterns
    LOOP_PATTERNS = {
        'nested_loops': {
            'pattern': r'for\s+\w+\s+in\s+.*?:\s*\n\s*.*?for\s+\w+\s+in',
            'severity': Severity.HIGH,
            'issue': 'Nested loops with O(n²) or worse complexity',
            'recommendation': 'Use hash maps, sets, or algorithmic optimization to reduce complexity',
            'impact': 'Quadratic or worse time complexity',
            'improvement': '60-90% reduction in execution time'
        },
        'string_concat_loop': {
            'pattern': r'for\s+.*?:\s*\n\s*.*?\w+\s*\+=\s*["\']|for\s+.*?:\s*\n\s*.*?\.concat\(',
            'severity': Severity.MEDIUM,
            'issue': 'String concatenation in loop',
            'recommendation': 'Use StringBuilder, StringBuffer, or array.join() for efficient string building',
            'impact': 'Creates new string object on each iteration',
            'improvement': '50-70% reduction in memory allocations'
        },
        'inefficient_search': {
            'pattern': r'for\s+.*?:\s*\n\s*.*?if\s+\w+\s*==',
            'severity': Severity.MEDIUM,
            'issue': 'Linear search in loop (potential O(n²))',
            'recommendation': 'Use hash map/set for O(1) lookups',
            'impact': 'Linear search complexity on each iteration',
            'improvement': '70-95% reduction in search time'
        },
        'list_append_loop': {
            'pattern': r'for\s+.*?:\s*\n\s*.*?\.append\(|\.push\(',
            'severity': Severity.LOW,
            'issue': 'List append in loop (possible array resizing)',
            'recommendation': 'Pre-allocate list size if known, or use list comprehension',
            'impact': 'Potential memory reallocations',
            'improvement': '20-40% reduction in allocations'
        }
    }

    # Memory anti-patterns
    MEMORY_PATTERNS = {
        'large_allocation_loop': {
            'pattern': r'for\s+.*?:\s*\n\s*.*?(?:new\s+\w+\[|malloc|List\(|Dict\(|\[\]|\{\})',
            'severity': Severity.HIGH,
            'issue': 'Large object allocation inside loop',
            'recommendation': 'Reuse objects or move allocation outside loop',
            'impact': 'Excessive memory allocations and GC pressure',
            'improvement': '60-80% reduction in memory allocations'
        },
        'unbounded_list': {
            'pattern': r'\.append\(|\.push\(|\.add\((?!.*?\.pop\(|\.shift\()',
            'severity': Severity.MEDIUM,
            'issue': 'Unbounded list growth without clear limits',
            'recommendation': 'Add size limits, implement cleanup, or use bounded collections',
            'impact': 'Potential memory leak and OOM errors',
            'improvement': '50-90% reduction in memory usage'
        },
        'global_cache': {
            'pattern': r'(?:global|static)\s+\w+\s*=\s*(?:\{\}|\[\]|dict\(|list\()',
            'severity': Severity.MEDIUM,
            'issue': 'Global/static cache without size limits',
            'recommendation': 'Implement LRU cache with max size or TTL',
            'impact': 'Unbounded memory growth over time',
            'improvement': '70-95% reduction in memory footprint'
        },
        'large_file_read': {
            'pattern': r'\.read\(\)|\.readlines\(\)|File\.ReadAllText|File\.ReadAllLines',
            'severity': Severity.HIGH,
            'issue': 'Reading entire file into memory',
            'recommendation': 'Use streaming/chunked reading for large files',
            'impact': 'Can cause OOM with large files',
            'improvement': '80-99% reduction in memory usage'
        }
    }

    # I/O anti-patterns
    IO_PATTERNS = {
        'sync_io_loop': {
            'pattern': r'for\s+.*?:\s*\n\s*.*?(?:requests\.get|fetch|http\.get|File\.Read)',
            'severity': Severity.CRITICAL,
            'issue': 'Synchronous I/O operation in loop',
            'recommendation': 'Use async/await, Promise.all(), or parallel processing',
            'impact': 'Sequential I/O blocking on each iteration',
            'improvement': '80-95% reduction in total I/O time'
        },
        'missing_cache': {
            'pattern': r'(?:requests\.get|fetch|http\.get).*?(?!cache)',
            'severity': Severity.MEDIUM,
            'issue': 'HTTP request without apparent caching',
            'recommendation': 'Implement response caching for frequently accessed data',
            'impact': 'Redundant network requests',
            'improvement': '70-99% reduction in API calls'
        },
        'unbuffered_io': {
            'pattern': r'open\([^)]*\)(?!.*buffering)|FileStream\([^)]*\)(?!.*buffer)',
            'severity': Severity.LOW,
            'issue': 'File I/O without explicit buffering',
            'recommendation': 'Use buffered I/O for better performance',
            'impact': 'Increased system calls',
            'improvement': '30-50% improvement in I/O throughput'
        },
        'sync_file_ops': {
            'pattern': r'fs\.readFileSync|fs\.writeFileSync|File\.ReadAllBytes',
            'severity': Severity.HIGH,
            'issue': 'Synchronous file operation blocking execution',
            'recommendation': 'Use async file operations to avoid blocking',
            'impact': 'Blocks event loop/thread during I/O',
            'improvement': '60-90% improvement in responsiveness'
        }
    }

    # Algorithm anti-patterns
    ALGORITHM_PATTERNS = {
        'regex_in_loop': {
            'pattern': r'for\s+.*?:\s*\n\s*.*?(?:re\.compile|new RegExp|Pattern\.compile)',
            'severity': Severity.MEDIUM,
            'issue': 'Regex compilation inside loop',
            'recommendation': 'Compile regex once outside loop and reuse',
            'impact': 'Repeated regex compilation overhead',
            'improvement': '50-80% reduction in regex overhead'
        },
        'repeated_computation': {
            'pattern': r'for\s+\w+\s+in\s+range\((?:len\(|size\(|count\()',
            'severity': Severity.LOW,
            'issue': 'Repeated function call in loop condition',
            'recommendation': 'Cache result in variable before loop',
            'impact': 'Unnecessary repeated computation',
            'improvement': '10-30% reduction in loop overhead'
        },
        'inefficient_sort': {
            'pattern': r'\.sort\(\s*(?:lambda|function|def)',
            'severity': Severity.MEDIUM,
            'issue': 'Complex comparison function in sort',
            'recommendation': 'Simplify comparison or use key function',
            'impact': 'Slow sort performance',
            'improvement': '40-70% improvement in sort time'
        },
        'deep_recursion': {
            'pattern': r'def\s+(\w+)\(.*?\):\s*\n(?:.*\n)*?\s*\1\(',
            'severity': Severity.HIGH,
            'issue': 'Recursive function without apparent depth limit',
            'recommendation': 'Add depth limit or convert to iterative approach',
            'impact': 'Stack overflow risk with deep recursion',
            'improvement': '50-90% reduction in stack usage'
        }
    }

    # Network anti-patterns
    NETWORK_PATTERNS = {
        'no_timeout': {
            'pattern': r'(?:requests\.get|fetch|http\.get|urllib\.request)(?!.*timeout)',
            'severity': Severity.MEDIUM,
            'issue': 'Network request without timeout',
            'recommendation': 'Add timeout parameter to prevent indefinite hanging',
            'impact': 'Can hang indefinitely on network issues',
            'improvement': '100% prevention of timeout-related hangs'
        },
        'no_retry': {
            'pattern': r'(?:requests\.get|fetch|http\.get)(?!.*retry)',
            'severity': Severity.LOW,
            'issue': 'Network request without retry logic',
            'recommendation': 'Implement retry with exponential backoff',
            'impact': 'Fails immediately on transient errors',
            'improvement': '60-90% improvement in reliability'
        },
        'sequential_requests': {
            'pattern': r'(?:requests\.get|fetch).*?\n\s*(?:requests\.get|fetch)',
            'severity': Severity.HIGH,
            'issue': 'Sequential network requests that could be parallel',
            'recommendation': 'Use Promise.all(), async gather, or parallel execution',
            'impact': 'Unnecessary sequential waiting',
            'improvement': '70-95% reduction in total request time'
        }
    }

    def __init__(self, input_path: str, output_format: str = 'text',
                 output_file: Optional[str] = None, verbose: bool = False):
        """Initialize the detector"""
        self.input_path = Path(input_path)
        self.output_format = output_format.lower()
        self.output_file = output_file
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.bottlenecks: List[BottleneckFinding] = []
        self.files_analyzed = 0
        self.lines_analyzed = 0
        logger.debug("PerformanceBottleneckDetector initialized")

    def log(self, message: str) -> None:
        """Log message if verbose mode enabled"""
        if self.verbose:
            print(f"[INFO] {message}", file=sys.stderr)

    def analyze(self) -> Dict:
        """Main analysis method"""
        self.log(f"Starting performance bottleneck analysis: {self.input_path}")

        if not self.input_path.exists():
            return {
                'status': 'error',
                'message': f"Input path does not exist: {self.input_path}"
            }

        # Analyze files
        if self.input_path.is_file():
            self._analyze_file(self.input_path)
        else:
            self._analyze_directory(self.input_path)

        # Calculate performance score
        performance_score = self._calculate_performance_score()

        # Group bottlenecks by category
        by_category = self._group_by_category()

        # Identify hotspots (files with most issues)
        hotspots = self._identify_hotspots()

        # Generate recommendations
        recommendations = self._generate_recommendations()

        self.log(f"Analysis complete: {len(self.bottlenecks)} bottlenecks found")

        return {
            'status': 'success',
            'summary': {
                'total_bottlenecks': len(self.bottlenecks),
                'files_analyzed': self.files_analyzed,
                'lines_analyzed': self.lines_analyzed,
                'critical_issues': len([b for b in self.bottlenecks if b.severity == 'CRITICAL']),
                'high_issues': len([b for b in self.bottlenecks if b.severity == 'HIGH']),
                'medium_issues': len([b for b in self.bottlenecks if b.severity == 'MEDIUM']),
                'low_issues': len([b for b in self.bottlenecks if b.severity == 'LOW']),
                'performance_score': performance_score
            },
            'bottlenecks': [asdict(b) for b in self.bottlenecks],
            'by_category': by_category,
            'hotspots': hotspots,
            'performance_score': performance_score,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }

    def _analyze_directory(self, directory: Path) -> None:
        """Recursively analyze all files in directory"""
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.SUPPORTED_EXTENSIONS:
                self._analyze_file(file_path)

    def _analyze_file(self, file_path: Path) -> None:
        """Analyze a single file for performance bottlenecks"""
        self.log(f"Analyzing file: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            self.files_analyzed += 1
            self.lines_analyzed += len(lines)

            # Run all pattern checks
            self._check_patterns(file_path, content, lines, self.DB_PATTERNS, 'DATABASE')
            self._check_patterns(file_path, content, lines, self.LOOP_PATTERNS, 'LOOP')
            self._check_patterns(file_path, content, lines, self.MEMORY_PATTERNS, 'MEMORY')
            self._check_patterns(file_path, content, lines, self.IO_PATTERNS, 'IO')
            self._check_patterns(file_path, content, lines, self.ALGORITHM_PATTERNS, 'ALGORITHM')
            self._check_patterns(file_path, content, lines, self.NETWORK_PATTERNS, 'NETWORK')

        except Exception as e:
            self.log(f"Error analyzing {file_path}: {e}")

    def _check_patterns(self, file_path: Path, content: str, lines: List[str],
                       patterns: Dict, category: str) -> None:
        """Check file content against pattern dictionary"""
        for pattern_name, pattern_info in patterns.items():
            regex = re.compile(pattern_info['pattern'], re.MULTILINE | re.IGNORECASE)

            for match in regex.finditer(content):
                line_number = content[:match.start()].count('\n') + 1

                # Extract code snippet (3 lines context)
                start_line = max(0, line_number - 2)
                end_line = min(len(lines), line_number + 2)
                snippet = '\n'.join(lines[start_line:end_line])

                # Create finding
                severity_name = pattern_info['severity'].name
                finding = BottleneckFinding(
                    category=category,
                    severity=severity_name,
                    severity_value=pattern_info['severity'].value,
                    file_path=str(file_path),
                    line_number=line_number,
                    issue=pattern_info['issue'],
                    code_snippet=snippet.strip(),
                    recommendation=pattern_info['recommendation'],
                    impact=pattern_info['impact'],
                    estimated_improvement=pattern_info['improvement']
                )

                self.bottlenecks.append(finding)

    def _calculate_performance_score(self) -> int:
        """Calculate overall performance score (0-100, higher is better)"""
        if not self.bottlenecks:
            return 100

        # Weight by severity
        total_penalty = sum(
            b.severity_value * 10 for b in self.bottlenecks
        )

        # Normalize to 0-100 scale (assume 10 critical issues = 0 score)
        max_penalty = self.files_analyzed * 100  # Max expected penalty
        score = max(0, 100 - (total_penalty / max(max_penalty, 1)) * 100)

        return int(score)

    def _group_by_category(self) -> Dict:
        """Group bottlenecks by category"""
        by_category = {}

        for bottleneck in self.bottlenecks:
            category = bottleneck.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(asdict(bottleneck))

        return by_category

    def _identify_hotspots(self) -> List[Dict]:
        """Identify files with most performance issues"""
        file_counts = {}

        for bottleneck in self.bottlenecks:
            file_path = bottleneck.file_path
            if file_path not in file_counts:
                file_counts[file_path] = {
                    'file': file_path,
                    'total_issues': 0,
                    'critical': 0,
                    'high': 0,
                    'medium': 0,
                    'low': 0
                }

            file_counts[file_path]['total_issues'] += 1
            file_counts[file_path][bottleneck.severity.lower()] += 1

        # Sort by total issues descending
        hotspots = sorted(
            file_counts.values(),
            key=lambda x: x['total_issues'],
            reverse=True
        )

        return hotspots[:10]  # Top 10 hotspots

    def _generate_recommendations(self) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []

        # Group by category and severity
        critical = [b for b in self.bottlenecks if b.severity == 'CRITICAL']
        high = [b for b in self.bottlenecks if b.severity == 'HIGH']

        if critical:
            recommendations.append(
                f"URGENT: Address {len(critical)} critical performance bottlenecks immediately. "
                "These can cause system failures or severe performance degradation."
            )

        if high:
            recommendations.append(
                f"HIGH PRIORITY: Fix {len(high)} high-severity issues. "
                "These significantly impact performance and user experience."
            )

        # Category-specific recommendations
        by_category = {}
        for b in self.bottlenecks:
            by_category.setdefault(b.category, []).append(b)

        for category, issues in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True):
            if len(issues) >= 3:
                recommendations.append(
                    f"{category}: Found {len(issues)} issues. Focus on {category.lower()} optimization. "
                    f"Common fix: {issues[0].recommendation}"
                )

        # General recommendations
        if self.bottlenecks:
            recommendations.append(
                "Implement performance monitoring and profiling to measure improvement impact."
            )
            recommendations.append(
                "Add load testing to validate optimizations under realistic conditions."
            )
            recommendations.append(
                "Document performance requirements and set up automated performance regression tests."
            )

        return recommendations

    def generate_output(self, results: Dict) -> str:
        """Generate output in requested format"""
        if self.output_format == 'json':
            return json.dumps(results, indent=2)
        elif self.output_format == 'csv':
            return self._generate_csv(results)
        else:
            return self._generate_text_report(results)

    def _generate_csv(self, results: Dict) -> str:
        """Generate CSV output"""
        lines = [
            'Category,Severity,File,Line,Issue,Recommendation,Impact,Estimated Improvement'
        ]

        for bottleneck in results['bottlenecks']:
            lines.append(
                f'"{bottleneck["category"]}",'
                f'"{bottleneck["severity"]}",'
                f'"{bottleneck["file_path"]}",'
                f'{bottleneck["line_number"]},'
                f'"{bottleneck["issue"]}",'
                f'"{bottleneck["recommendation"]}",'
                f'"{bottleneck["impact"]}",'
                f'"{bottleneck["estimated_improvement"]}"'
            )

        return '\n'.join(lines)

    def _generate_text_report(self, results: Dict) -> str:
        """Generate human-readable text report"""
        lines = [
            "=" * 80,
            "PERFORMANCE BOTTLENECK ANALYSIS REPORT",
            "=" * 80,
            "",
            f"Analysis Date: {results['timestamp']}",
            f"Input Path: {self.input_path}",
            "",
            "SUMMARY",
            "-" * 80,
            f"Files Analyzed: {results['summary']['files_analyzed']}",
            f"Lines Analyzed: {results['summary']['lines_analyzed']:,}",
            f"Total Bottlenecks: {results['summary']['total_bottlenecks']}",
            f"Performance Score: {results['summary']['performance_score']}/100",
            "",
            "Issues by Severity:",
            f"  CRITICAL: {results['summary']['critical_issues']}",
            f"  HIGH:     {results['summary']['high_issues']}",
            f"  MEDIUM:   {results['summary']['medium_issues']}",
            f"  LOW:      {results['summary']['low_issues']}",
            "",
        ]

        # Hotspots
        if results['hotspots']:
            lines.extend([
                "TOP PERFORMANCE HOTSPOTS",
                "-" * 80,
            ])
            for idx, hotspot in enumerate(results['hotspots'][:5], 1):
                lines.append(
                    f"{idx}. {hotspot['file']} "
                    f"({hotspot['total_issues']} issues: "
                    f"{hotspot['critical']} critical, "
                    f"{hotspot['high']} high, "
                    f"{hotspot['medium']} medium, "
                    f"{hotspot['low']} low)"
                )
            lines.append("")

        # Detailed findings
        lines.extend([
            "DETAILED FINDINGS",
            "-" * 80,
            ""
        ])

        # Group by severity
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            severity_issues = [b for b in results['bottlenecks'] if b['severity'] == severity]

            if severity_issues:
                lines.extend([
                    f"{severity} ISSUES ({len(severity_issues)})",
                    "=" * 80,
                    ""
                ])

                for idx, issue in enumerate(severity_issues[:10], 1):  # Limit to 10 per severity
                    lines.extend([
                        f"[{idx}] {issue['category']}: {issue['issue']}",
                        f"    File: {issue['file_path']}:{issue['line_number']}",
                        f"    Impact: {issue['impact']}",
                        f"    Improvement: {issue['estimated_improvement']}",
                        f"    Recommendation: {issue['recommendation']}",
                        f"    Code:",
                    ])

                    for line in issue['code_snippet'].split('\n')[:5]:
                        lines.append(f"        {line}")

                    lines.append("")

                if len(severity_issues) > 10:
                    lines.append(f"    ... and {len(severity_issues) - 10} more {severity} issues")
                    lines.append("")

        # Recommendations
        lines.extend([
            "",
            "RECOMMENDATIONS",
            "-" * 80,
        ])
        for idx, rec in enumerate(results['recommendations'], 1):
            lines.append(f"{idx}. {rec}")

        lines.extend([
            "",
            "=" * 80,
            "END OF REPORT",
            "=" * 80
        ])

        return '\n'.join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Identify performance bottlenecks and optimization opportunities in code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input /path/to/code
  %(prog)s -i src/ --output json
  %(prog)s -i app.py --output csv --file report.csv
  %(prog)s -i . --verbose

Categories Detected:
  DATABASE: N+1 queries, SELECT *, unbounded queries, missing indexes
  LOOP: Nested loops, inefficient iterations, string concatenation
  MEMORY: Large allocations in loops, unbounded growth, memory leaks
  IO: Synchronous blocking, missing caching, unbuffered operations
  ALGORITHM: Repeated regex compilation, redundant computations
  NETWORK: Missing timeouts, sequential requests, no retry logic

Output Formats:
  text: Human-readable report with detailed findings
  json: Structured JSON for programmatic analysis
  csv: Tabular format for spreadsheet import
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input file or directory to analyze'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Create detector and run analysis
    detector = PerformanceBottleneckDetector(
        input_path=args.input,
        output_format=args.output,
        output_file=args.file,
        verbose=args.verbose
    )

    results = detector.analyze()

    if results['status'] == 'error':
        print(f"Error: {results['message']}", file=sys.stderr)
        return 1

    # Generate output
    output = detector.generate_output(results)

    # Write to file or stdout
    if args.file:
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report saved to: {args.file}")
    else:
        print(output)

    # Return exit code based on critical issues
    critical_count = results['summary']['critical_issues']
    if critical_count > 0:
        return 2  # Critical issues found

    return 0


if __name__ == '__main__':
    sys.exit(main())
