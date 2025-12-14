#!/usr/bin/env python3
"""
Coverage Analyzer
Parse test coverage reports (lcov, cobertura, istanbul) and identify coverage gaps
with actionable recommendations for improvement.

Supports:
- LCOV format (lcov.info)
- Cobertura XML (coverage.xml)
- Istanbul JSON (coverage-final.json, coverage-summary.json)
- Jest coverage summary

Features:
- Coverage metrics calculation (line, branch, function, statement)
- Gap identification with severity ranking
- Trend analysis with baseline comparison
- Priority-ranked recommendations
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class CoverageMetrics:
    """Coverage metrics for a single category"""
    covered: int = 0
    total: int = 0

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 100.0
        return round((self.covered / self.total) * 100, 2)


@dataclass
class FileCoverage:
    """Coverage data for a single file"""
    path: str
    lines: CoverageMetrics = field(default_factory=CoverageMetrics)
    branches: CoverageMetrics = field(default_factory=CoverageMetrics)
    functions: CoverageMetrics = field(default_factory=CoverageMetrics)
    uncovered_lines: List[int] = field(default_factory=list)
    uncovered_branches: List[int] = field(default_factory=list)
    uncovered_functions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'path': self.path,
            'line_coverage': self.lines.percentage,
            'branch_coverage': self.branches.percentage,
            'function_coverage': self.functions.percentage,
            'uncovered_lines': self.uncovered_lines[:20],  # Limit for readability
            'uncovered_branches': self.uncovered_branches[:10],
            'uncovered_functions': self.uncovered_functions[:10],
        }


@dataclass
class CoverageGap:
    """Identified coverage gap"""
    file: str
    severity: str  # critical, high, medium, low
    reason: str
    lines: List[int] = field(default_factory=list)
    effort: str = 'medium'  # easy, medium, hard

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Recommendation:
    """Actionable recommendation for improving coverage"""
    priority: int
    file: str
    effort: str
    suggestion: str
    impact: str = 'medium'
    estimated_tests: int = 1

    def to_dict(self) -> Dict:
        return asdict(self)


class CoverageAnalyzer:
    """Analyze test coverage reports and identify gaps"""

    # File patterns that indicate critical business logic
    CRITICAL_PATTERNS = [
        r'auth', r'payment', r'security', r'crypto', r'password',
        r'session', r'token', r'permission', r'access', r'admin',
        r'transaction', r'order', r'checkout', r'billing',
    ]

    # File patterns for lower priority (utilities, helpers)
    LOW_PRIORITY_PATTERNS = [
        r'test', r'spec', r'mock', r'stub', r'fixture',
        r'__pycache__', r'node_modules', r'dist', r'build',
        r'\.d\.ts$', r'types?\.ts$', r'index\.(ts|js)$',
    ]

    def __init__(self, target_path: str, verbose: bool = False,
                 format_type: str = 'auto', threshold: float = 80.0,
                 baseline: Optional[float] = None):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("CoverageAnalyzer initialized")

        self.target_path = Path(target_path)
        self.verbose = verbose
        self.format_type = format_type
        self.threshold = threshold
        self.baseline = baseline

        self.files: List[FileCoverage] = []
        self.total_metrics = {
            'lines': CoverageMetrics(),
            'branches': CoverageMetrics(),
            'functions': CoverageMetrics(),
            'statements': CoverageMetrics(),
        }

        self.results = {
            'status': 'success',
            'target': str(target_path),
            'format_detected': None,
            'coverage': {},
            'files': [],
            'gaps': [],
            'recommendations': [],
            'trend': {},
            'summary': {},
        }

    def run(self) -> Dict:
        """Execute coverage analysis"""
        logger.debug("Starting coverage analysis run")
        print(f"Running CoverageAnalyzer...")
        print(f"Target: {self.target_path}")

        try:
            coverage_file = self.find_coverage_file()
            if not coverage_file:
                logger.warning(f"No coverage file found in {self.target_path}")
                raise ValueError(f"No coverage file found in {self.target_path}")

            print(f"Found coverage file: {coverage_file}")
            self.parse_coverage(coverage_file)
            self.calculate_totals()
            self.identify_gaps()
            self.generate_recommendations()
            self.analyze_trend()
            self.generate_summary()
            self.generate_report()

            print("Completed successfully!")
            return self.results

        except Exception as e:
            logger.error(f"Error during coverage analysis: {e}")
            print(f"Error: {e}")
            self.results['status'] = 'error'
            self.results['error'] = str(e)
            if self.verbose:
                import traceback
                traceback.print_exc()
            return self.results

    def find_coverage_file(self) -> Optional[Path]:
        """Find coverage file based on format or auto-detect"""
        logger.debug("Finding coverage file")
        if self.target_path.is_file():
            return self.target_path

        # Common coverage file locations
        coverage_files = {
            'lcov': ['coverage/lcov.info', 'lcov.info', 'coverage/lcov-report/lcov.info'],
            'cobertura': ['coverage.xml', 'coverage/cobertura-coverage.xml', 'cobertura.xml'],
            'istanbul': ['coverage/coverage-final.json', 'coverage-final.json',
                        '.nyc_output/coverage-final.json'],
            'jest': ['coverage/coverage-summary.json', 'coverage-summary.json'],
        }

        if self.format_type != 'auto':
            for filename in coverage_files.get(self.format_type, []):
                path = self.target_path / filename
                if path.exists():
                    self.results['format_detected'] = self.format_type
                    return path

        # Auto-detect
        for fmt, filenames in coverage_files.items():
            for filename in filenames:
                path = self.target_path / filename
                if path.exists():
                    self.format_type = fmt
                    self.results['format_detected'] = fmt
                    if self.verbose:
                        print(f"Auto-detected format: {fmt}")
                    return path

        logger.warning("No coverage file found")
        return None

    def parse_coverage(self, coverage_file: Path):
        """Parse coverage file based on detected format"""
        logger.debug(f"Parsing coverage file: {coverage_file}")
        content = coverage_file.read_text()

        if not content:
            logger.warning(f"Empty coverage file: {coverage_file}")
            return

        if self.format_type == 'lcov':
            self.parse_lcov(content)
        elif self.format_type == 'cobertura':
            self.parse_cobertura(content)
        elif self.format_type in ('istanbul', 'jest'):
            self.parse_istanbul(content)
        else:
            # Try to auto-detect from content
            if content.strip().startswith('TN:') or content.strip().startswith('SF:'):
                self.parse_lcov(content)
            elif content.strip().startswith('<?xml') or content.strip().startswith('<coverage'):
                self.parse_cobertura(content)
            elif content.strip().startswith('{'):
                self.parse_istanbul(content)
            else:
                logger.error(f"Unable to detect coverage format for {coverage_file}")
                raise ValueError(f"Unable to detect coverage format for {coverage_file}")

    def parse_lcov(self, content: str):
        """Parse LCOV format coverage data"""
        if self.verbose:
            print("Parsing LCOV format...")

        current_file = None
        file_coverage = None

        for line in content.split('\n'):
            line = line.strip()

            if line.startswith('SF:'):
                # Source file
                filepath = line[3:]
                file_coverage = FileCoverage(path=filepath)
                current_file = filepath

            elif line.startswith('FN:'):
                # Function definition: FN:line,name
                pass  # Track function names if needed

            elif line.startswith('FNDA:'):
                # Function data: FNDA:hits,name
                parts = line[5:].split(',', 1)
                if len(parts) == 2:
                    hits = int(parts[0])
                    name = parts[1]
                    file_coverage.functions.total += 1
                    if hits > 0:
                        file_coverage.functions.covered += 1
                    else:
                        file_coverage.uncovered_functions.append(name)

            elif line.startswith('FNF:'):
                # Functions found
                file_coverage.functions.total = int(line[4:])

            elif line.startswith('FNH:'):
                # Functions hit
                file_coverage.functions.covered = int(line[4:])

            elif line.startswith('DA:'):
                # Line data: DA:line,hits
                parts = line[3:].split(',')
                if len(parts) >= 2:
                    line_num = int(parts[0])
                    hits = int(parts[1])
                    file_coverage.lines.total += 1
                    if hits > 0:
                        file_coverage.lines.covered += 1
                    else:
                        file_coverage.uncovered_lines.append(line_num)

            elif line.startswith('LF:'):
                # Lines found
                file_coverage.lines.total = int(line[3:])

            elif line.startswith('LH:'):
                # Lines hit
                file_coverage.lines.covered = int(line[3:])

            elif line.startswith('BRDA:'):
                # Branch data: BRDA:line,block,branch,hits
                parts = line[5:].split(',')
                if len(parts) >= 4:
                    line_num = int(parts[0])
                    hits = parts[3]
                    file_coverage.branches.total += 1
                    if hits != '-' and int(hits) > 0:
                        file_coverage.branches.covered += 1
                    else:
                        if line_num not in file_coverage.uncovered_branches:
                            file_coverage.uncovered_branches.append(line_num)

            elif line.startswith('BRF:'):
                # Branches found
                file_coverage.branches.total = int(line[4:])

            elif line.startswith('BRH:'):
                # Branches hit
                file_coverage.branches.covered = int(line[4:])

            elif line == 'end_of_record':
                if file_coverage:
                    self.files.append(file_coverage)
                    file_coverage = None
                    current_file = None

        if self.verbose:
            print(f"Parsed {len(self.files)} files from LCOV")

    def parse_cobertura(self, content: str):
        """Parse Cobertura XML format coverage data"""
        if self.verbose:
            print("Parsing Cobertura XML format...")

        root = ET.fromstring(content)

        # Handle different Cobertura XML structures
        packages = root.findall('.//package') or root.findall('.//packages/package')

        for package in packages:
            classes = package.findall('.//class') or package.findall('.//classes/class')

            for cls in classes:
                filename = cls.get('filename', cls.get('name', 'unknown'))
                file_coverage = FileCoverage(path=filename)

                # Parse line coverage
                lines = cls.findall('.//line') or cls.findall('.//lines/line')
                for line in lines:
                    hits = int(line.get('hits', 0))
                    line_num = int(line.get('number', 0))
                    file_coverage.lines.total += 1
                    if hits > 0:
                        file_coverage.lines.covered += 1
                    else:
                        file_coverage.uncovered_lines.append(line_num)

                    # Branch coverage from line attributes
                    if line.get('branch') == 'true':
                        condition_coverage = line.get('condition-coverage', '')
                        match = re.search(r'(\d+)/(\d+)', condition_coverage)
                        if match:
                            covered = int(match.group(1))
                            total = int(match.group(2))
                            file_coverage.branches.covered += covered
                            file_coverage.branches.total += total
                            if covered < total:
                                file_coverage.uncovered_branches.append(line_num)

                # Parse method/function coverage
                methods = cls.findall('.//method') or cls.findall('.//methods/method')
                for method in methods:
                    name = method.get('name', 'unknown')
                    file_coverage.functions.total += 1

                    # Check if method has any hits
                    method_lines = method.findall('.//line')
                    has_hits = any(int(l.get('hits', 0)) > 0 for l in method_lines)
                    if has_hits:
                        file_coverage.functions.covered += 1
                    else:
                        file_coverage.uncovered_functions.append(name)

                self.files.append(file_coverage)

        if self.verbose:
            print(f"Parsed {len(self.files)} files from Cobertura XML")

    def parse_istanbul(self, content: str):
        """Parse Istanbul/NYC JSON format coverage data"""
        if self.verbose:
            print("Parsing Istanbul JSON format...")

        data = json.loads(content)

        # Handle coverage-summary.json format
        if 'total' in data and all(k in data for k in ['total']):
            self._parse_istanbul_summary(data)
            return

        # Handle coverage-final.json format
        for filepath, file_data in data.items():
            if filepath == 'total':
                continue

            file_coverage = FileCoverage(path=filepath)

            # Statement coverage (maps to lines)
            stmt_map = file_data.get('statementMap', {})
            stmt_hits = file_data.get('s', {})
            for stmt_id, hits in stmt_hits.items():
                file_coverage.lines.total += 1
                if hits > 0:
                    file_coverage.lines.covered += 1
                else:
                    stmt_info = stmt_map.get(stmt_id, {})
                    start_line = stmt_info.get('start', {}).get('line', 0)
                    if start_line and start_line not in file_coverage.uncovered_lines:
                        file_coverage.uncovered_lines.append(start_line)

            # Branch coverage
            branch_map = file_data.get('branchMap', {})
            branch_hits = file_data.get('b', {})
            for branch_id, hits_list in branch_hits.items():
                branch_info = branch_map.get(branch_id, {})
                start_line = branch_info.get('loc', {}).get('start', {}).get('line', 0)

                for hits in hits_list:
                    file_coverage.branches.total += 1
                    if hits > 0:
                        file_coverage.branches.covered += 1
                    else:
                        if start_line and start_line not in file_coverage.uncovered_branches:
                            file_coverage.uncovered_branches.append(start_line)

            # Function coverage
            fn_map = file_data.get('fnMap', {})
            fn_hits = file_data.get('f', {})
            for fn_id, hits in fn_hits.items():
                fn_info = fn_map.get(fn_id, {})
                fn_name = fn_info.get('name', f'function_{fn_id}')

                file_coverage.functions.total += 1
                if hits > 0:
                    file_coverage.functions.covered += 1
                else:
                    file_coverage.uncovered_functions.append(fn_name)

            self.files.append(file_coverage)

        if self.verbose:
            print(f"Parsed {len(self.files)} files from Istanbul JSON")

    def _parse_istanbul_summary(self, data: Dict):
        """Parse Istanbul coverage-summary.json format"""
        for filepath, metrics in data.items():
            if filepath == 'total':
                continue

            file_coverage = FileCoverage(path=filepath)

            if 'lines' in metrics:
                file_coverage.lines.covered = metrics['lines'].get('covered', 0)
                file_coverage.lines.total = metrics['lines'].get('total', 0)

            if 'branches' in metrics:
                file_coverage.branches.covered = metrics['branches'].get('covered', 0)
                file_coverage.branches.total = metrics['branches'].get('total', 0)

            if 'functions' in metrics:
                file_coverage.functions.covered = metrics['functions'].get('covered', 0)
                file_coverage.functions.total = metrics['functions'].get('total', 0)

            self.files.append(file_coverage)

    def calculate_totals(self):
        """Calculate total coverage metrics across all files"""
        for file_cov in self.files:
            self.total_metrics['lines'].covered += file_cov.lines.covered
            self.total_metrics['lines'].total += file_cov.lines.total
            self.total_metrics['branches'].covered += file_cov.branches.covered
            self.total_metrics['branches'].total += file_cov.branches.total
            self.total_metrics['functions'].covered += file_cov.functions.covered
            self.total_metrics['functions'].total += file_cov.functions.total

        # Copy statements from lines for compatibility
        self.total_metrics['statements'] = self.total_metrics['lines']

        self.results['coverage'] = {
            'lines': {
                'covered': self.total_metrics['lines'].covered,
                'total': self.total_metrics['lines'].total,
                'percentage': self.total_metrics['lines'].percentage,
            },
            'branches': {
                'covered': self.total_metrics['branches'].covered,
                'total': self.total_metrics['branches'].total,
                'percentage': self.total_metrics['branches'].percentage,
            },
            'functions': {
                'covered': self.total_metrics['functions'].covered,
                'total': self.total_metrics['functions'].total,
                'percentage': self.total_metrics['functions'].percentage,
            },
        }

        self.results['files'] = [f.to_dict() for f in self.files]

    def identify_gaps(self):
        """Identify coverage gaps with severity ranking"""
        gaps = []

        for file_cov in self.files:
            # Skip test files and low-priority patterns
            if self._is_low_priority(file_cov.path):
                continue

            is_critical = self._is_critical(file_cov.path)

            # Check line coverage
            if file_cov.lines.percentage < self.threshold:
                severity = self._calculate_severity(
                    file_cov.lines.percentage,
                    is_critical
                )
                gaps.append(CoverageGap(
                    file=file_cov.path,
                    severity=severity,
                    reason=f"Line coverage {file_cov.lines.percentage}% below threshold {self.threshold}%",
                    lines=file_cov.uncovered_lines[:20],
                    effort=self._estimate_effort(len(file_cov.uncovered_lines)),
                ))

            # Check branch coverage (if available)
            if file_cov.branches.total > 0 and file_cov.branches.percentage < self.threshold:
                severity = self._calculate_severity(
                    file_cov.branches.percentage,
                    is_critical
                )
                gaps.append(CoverageGap(
                    file=file_cov.path,
                    severity=severity,
                    reason=f"Branch coverage {file_cov.branches.percentage}% below threshold",
                    lines=file_cov.uncovered_branches[:10],
                    effort=self._estimate_effort(len(file_cov.uncovered_branches)),
                ))

            # Check function coverage
            if file_cov.functions.total > 0 and file_cov.functions.percentage < self.threshold:
                severity = self._calculate_severity(
                    file_cov.functions.percentage,
                    is_critical
                )
                gaps.append(CoverageGap(
                    file=file_cov.path,
                    severity=severity,
                    reason=f"Function coverage {file_cov.functions.percentage}% - uncovered: {', '.join(file_cov.uncovered_functions[:5])}",
                    lines=[],
                    effort=self._estimate_effort(len(file_cov.uncovered_functions) * 10),
                ))

        # Sort by severity (critical first)
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        gaps.sort(key=lambda g: severity_order.get(g.severity, 4))

        self.results['gaps'] = [g.to_dict() for g in gaps]

    def _is_critical(self, filepath: str) -> bool:
        """Check if file is in critical path"""
        filepath_lower = filepath.lower()
        return any(re.search(pattern, filepath_lower) for pattern in self.CRITICAL_PATTERNS)

    def _is_low_priority(self, filepath: str) -> bool:
        """Check if file is low priority (tests, utilities)"""
        filepath_lower = filepath.lower()
        return any(re.search(pattern, filepath_lower) for pattern in self.LOW_PRIORITY_PATTERNS)

    def _calculate_severity(self, coverage: float, is_critical: bool) -> str:
        """Calculate gap severity based on coverage and criticality"""
        if is_critical:
            if coverage < 50:
                return 'critical'
            elif coverage < 70:
                return 'high'
            else:
                return 'medium'
        else:
            if coverage < 30:
                return 'high'
            elif coverage < 60:
                return 'medium'
            else:
                return 'low'

    def _estimate_effort(self, uncovered_count: int) -> str:
        """Estimate effort to cover the gap"""
        if uncovered_count <= 5:
            return 'easy'
        elif uncovered_count <= 20:
            return 'medium'
        else:
            return 'hard'

    def generate_recommendations(self):
        """Generate actionable recommendations for improving coverage"""
        recommendations = []
        priority = 1

        # Sort files by coverage (lowest first) and criticality
        files_by_priority = []
        for file_cov in self.files:
            if self._is_low_priority(file_cov.path):
                continue

            is_critical = self._is_critical(file_cov.path)
            score = file_cov.lines.percentage
            if is_critical:
                score -= 20  # Lower score = higher priority

            files_by_priority.append((score, file_cov, is_critical))

        files_by_priority.sort(key=lambda x: x[0])

        for score, file_cov, is_critical in files_by_priority[:15]:
            if file_cov.lines.percentage >= self.threshold:
                continue

            # Generate specific recommendation
            suggestion = self._generate_suggestion(file_cov)
            impact = 'high' if is_critical else 'medium'
            estimated_tests = max(1, len(file_cov.uncovered_functions) or len(file_cov.uncovered_lines) // 10)

            recommendations.append(Recommendation(
                priority=priority,
                file=file_cov.path,
                effort=self._estimate_effort(len(file_cov.uncovered_lines)),
                suggestion=suggestion,
                impact=impact,
                estimated_tests=estimated_tests,
            ))
            priority += 1

        # Add general recommendations
        if self.total_metrics['branches'].percentage < self.total_metrics['lines'].percentage - 10:
            recommendations.append(Recommendation(
                priority=priority,
                file='(project-wide)',
                effort='medium',
                suggestion='Focus on branch coverage - add tests for conditional logic and edge cases',
                impact='high',
                estimated_tests=5,
            ))
            priority += 1

        if len([f for f in self.files if f.functions.percentage < 50]) > len(self.files) * 0.3:
            recommendations.append(Recommendation(
                priority=priority,
                file='(project-wide)',
                effort='medium',
                suggestion='Many functions are untested - consider adding unit tests for core functions',
                impact='high',
                estimated_tests=10,
            ))

        self.results['recommendations'] = [r.to_dict() for r in recommendations]

    def _generate_suggestion(self, file_cov: FileCoverage) -> str:
        """Generate specific suggestion for a file"""
        suggestions = []

        if file_cov.uncovered_functions:
            fn_list = ', '.join(file_cov.uncovered_functions[:3])
            suggestions.append(f"Add unit tests for: {fn_list}")

        if file_cov.uncovered_branches:
            suggestions.append(f"Add branch tests for lines: {file_cov.uncovered_branches[:5]}")

        if file_cov.lines.percentage < 50:
            suggestions.append("Consider splitting large functions for better testability")

        if not suggestions:
            suggestions.append(f"Increase line coverage from {file_cov.lines.percentage}% to {self.threshold}%")

        return '; '.join(suggestions)

    def analyze_trend(self):
        """Analyze coverage trend against baseline"""
        current = self.total_metrics['lines'].percentage

        trend = {
            'current': current,
            'threshold': self.threshold,
            'meets_threshold': current >= self.threshold,
        }

        if self.baseline is not None:
            delta = current - self.baseline
            trend['baseline'] = self.baseline
            trend['delta'] = round(delta, 2)
            trend['status'] = 'improving' if delta > 0 else ('stable' if delta == 0 else 'declining')
        else:
            trend['status'] = 'no_baseline'

        self.results['trend'] = trend

    def generate_summary(self):
        """Generate executive summary"""
        total_lines = self.total_metrics['lines']
        total_branches = self.total_metrics['branches']
        total_functions = self.total_metrics['functions']

        # Count files below threshold
        files_below = sum(1 for f in self.files if f.lines.percentage < self.threshold)
        critical_gaps = sum(1 for g in self.results['gaps'] if g.get('severity') == 'critical')
        high_gaps = sum(1 for g in self.results['gaps'] if g.get('severity') == 'high')

        # Determine health status
        if total_lines.percentage >= 90 and critical_gaps == 0:
            health = 'excellent'
        elif total_lines.percentage >= self.threshold and critical_gaps == 0:
            health = 'good'
        elif total_lines.percentage >= 60:
            health = 'needs_improvement'
        else:
            health = 'critical'

        self.results['summary'] = {
            'health': health,
            'overall_coverage': total_lines.percentage,
            'files_analyzed': len(self.files),
            'files_below_threshold': files_below,
            'critical_gaps': critical_gaps,
            'high_gaps': high_gaps,
            'total_recommendations': len(self.results['recommendations']),
            'quick_wins': sum(1 for r in self.results['recommendations'] if r.get('effort') == 'easy'),
        }

    def generate_report(self):
        """Generate and display the coverage report"""
        print("\n" + "=" * 70)
        print("COVERAGE ANALYSIS REPORT")
        print("=" * 70)

        # Summary
        summary = self.results['summary']
        health_emoji = {'excellent': '++', 'good': '+', 'needs_improvement': '!', 'critical': '!!'}
        print(f"\n[{health_emoji.get(summary['health'], '?')}] Health Status: {summary['health'].upper()}")

        # Coverage metrics
        cov = self.results['coverage']
        print(f"\nCoverage Metrics:")
        print(f"   Lines:     {cov['lines']['covered']}/{cov['lines']['total']} ({cov['lines']['percentage']}%)")
        print(f"   Branches:  {cov['branches']['covered']}/{cov['branches']['total']} ({cov['branches']['percentage']}%)")
        print(f"   Functions: {cov['functions']['covered']}/{cov['functions']['total']} ({cov['functions']['percentage']}%)")

        # Threshold check
        trend = self.results['trend']
        threshold_status = "PASS" if trend['meets_threshold'] else "FAIL"
        print(f"\n   Threshold: {self.threshold}% - {threshold_status}")

        if 'delta' in trend:
            delta_sign = '+' if trend['delta'] > 0 else ''
            print(f"   vs Baseline: {delta_sign}{trend['delta']}% ({trend['status']})")

        # Files summary
        print(f"\nFiles Analyzed: {summary['files_analyzed']}")
        print(f"   Below threshold: {summary['files_below_threshold']}")

        # Gaps
        if self.results['gaps']:
            print(f"\nCoverage Gaps ({len(self.results['gaps'])}):")
            for gap in self.results['gaps'][:5]:
                print(f"   [{gap['severity'].upper()}] {gap['file']}")
                print(f"           {gap['reason']}")
            if len(self.results['gaps']) > 5:
                print(f"   ... and {len(self.results['gaps']) - 5} more gaps")

        # Recommendations
        if self.results['recommendations']:
            print(f"\nTop Recommendations:")
            for rec in self.results['recommendations'][:5]:
                print(f"   {rec['priority']}. [{rec['effort'].upper()}] {rec['file']}")
                print(f"      {rec['suggestion']}")

        # Quick wins
        if summary['quick_wins'] > 0:
            print(f"\nQuick Wins Available: {summary['quick_wins']} easy improvements identified")

        print("\n" + "=" * 70)


def format_csv_output(results: Dict) -> str:
    """Format coverage results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(['file', 'line_coverage', 'branch_coverage', 'function_coverage', 'uncovered_lines_count'])

    # File data
    for file_data in results.get('files', []):
        writer.writerow([
            file_data.get('path', ''),
            file_data.get('line_coverage', 0),
            file_data.get('branch_coverage', 0),
            file_data.get('function_coverage', 0),
            len(file_data.get('uncovered_lines', [])),
        ])

    return output.getvalue()


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="CoverageAnalyzer - Parse test coverage reports and identify gaps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input coverage/lcov.info --format lcov
  %(prog)s --input . --format auto --threshold 85
  %(prog)s --input coverage.xml --format cobertura --baseline 80
  %(prog)s --input . --output json --file report.json
  %(prog)s --input . -v --threshold 90

Supported Formats:
  lcov      - LCOV format (lcov.info)
  cobertura - Cobertura XML (coverage.xml)
  istanbul  - Istanbul/NYC JSON (coverage-final.json)
  jest      - Jest coverage summary (coverage-summary.json)
  auto      - Auto-detect format (default)

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Coverage file or directory containing coverage reports'
    )

    parser.add_argument(
        '--format', '-F',
        choices=['auto', 'lcov', 'cobertura', 'istanbul', 'jest'],
        default='auto',
        help='Coverage format (default: auto-detect)'
    )

    parser.add_argument(
        '--threshold', '-t',
        type=float,
        default=80.0,
        help='Coverage threshold percentage (default: 80)'
    )

    parser.add_argument(
        '--baseline', '-b',
        type=float,
        help='Baseline coverage percentage for trend analysis'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
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

    analyzer = CoverageAnalyzer(
        args.target,
        verbose=args.verbose,
        format_type=args.format,
        threshold=args.threshold,
        baseline=args.baseline,
    )

    results = analyzer.run()

    # Format output
    if args.output == 'csv':
        output = format_csv_output(results)
    elif args.output == 'json':
        output = json.dumps(results, indent=2, default=str)
    else:
        # Text output is handled by generate_report()
        output = json.dumps(results, indent=2, default=str)

    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Results written to {args.file}")
    elif args.output != 'text':
        print(output)

    # Exit with appropriate code
    if results.get('status') == 'error':
        sys.exit(1)
    elif not results.get('trend', {}).get('meets_threshold', True):
        sys.exit(2)  # Below threshold
    sys.exit(0)


if __name__ == '__main__':
    main()
