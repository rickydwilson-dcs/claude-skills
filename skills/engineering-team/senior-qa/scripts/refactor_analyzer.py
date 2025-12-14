#!/usr/bin/env python3
"""
Refactor Analyzer
Validate refactoring safety and suggest improvements during TDD refactor phase
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RefactorAnalyzer:
    """Analyze code for safe refactoring opportunities during TDD refactor phase"""

    # Common refactoring patterns and their safety requirements
    REFACTORING_PATTERNS = {
        'extract_method': {
            'description': 'Extract code block into a separate method',
            'safety_requirements': ['Tests must pass before and after', 'Maintain same behavior'],
            'indicators': ['duplicated code', 'long method', 'nested conditionals'],
        },
        'rename': {
            'description': 'Rename variable, method, or class for clarity',
            'safety_requirements': ['All references updated', 'Tests still pass'],
            'indicators': ['unclear names', 'abbreviations', 'misleading names'],
        },
        'inline': {
            'description': 'Inline a method that adds no value',
            'safety_requirements': ['Method not overridden', 'Tests pass'],
            'indicators': ['trivial methods', 'unnecessary indirection'],
        },
        'move_method': {
            'description': 'Move method to a more appropriate class',
            'safety_requirements': ['Update all callers', 'Tests pass'],
            'indicators': ['feature envy', 'inappropriate intimacy'],
        },
        'extract_variable': {
            'description': 'Extract expression into a named variable',
            'safety_requirements': ['Expression evaluated once', 'Tests pass'],
            'indicators': ['complex expressions', 'repeated calculations'],
        },
        'simplify_conditional': {
            'description': 'Simplify complex conditional logic',
            'safety_requirements': ['Same logical outcomes', 'All branches tested'],
            'indicators': ['nested if/else', 'complex boolean expressions'],
        },
    }

    # Code smell indicators
    CODE_SMELLS = {
        'long_method': {
            'threshold': 20,
            'unit': 'lines',
            'severity': 'medium',
            'suggested_refactoring': 'extract_method',
        },
        'long_parameter_list': {
            'threshold': 4,
            'unit': 'parameters',
            'severity': 'medium',
            'suggested_refactoring': 'parameter_object',
        },
        'duplicated_code': {
            'threshold': 3,
            'unit': 'similar blocks',
            'severity': 'high',
            'suggested_refactoring': 'extract_method',
        },
        'deep_nesting': {
            'threshold': 3,
            'unit': 'levels',
            'severity': 'medium',
            'suggested_refactoring': 'extract_method',
        },
        'magic_numbers': {
            'threshold': 1,
            'unit': 'occurrences',
            'severity': 'low',
            'suggested_refactoring': 'extract_variable',
        },
    }

    def __init__(self, target_path: str, verbose: bool = False,
                 check_tests: bool = True, suggest_only: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("RefactorAnalyzer initialized")

        self.target_path = Path(target_path)
        self.verbose = verbose
        self.check_tests = check_tests
        self.suggest_only = suggest_only
        self.results = {
            'status': 'success',
            'target': str(target_path),
            'analysis_time': datetime.now().isoformat(),
            'files_analyzed': 0,
            'smells_detected': [],
            'refactoring_suggestions': [],
            'safety_checks': [],
            'metrics': {},
            'recommendations': [],
        }

    def run(self) -> Dict:
        """Execute refactoring analysis"""
        logger.debug("Starting refactoring analysis run")
        print(f"🚀 Running {self.__class__.__name__}...")
        print(f"📁 Target: {self.target_path}")

        try:
            self.validate_target()
            self.analyze_files()
            self.detect_smells()
            self.generate_suggestions()
            if self.check_tests:
                self.check_test_safety()
            self.calculate_metrics()
            self.generate_recommendations()
            self.generate_report()

            print("✅ Completed successfully!")
            return self.results

        except Exception as e:
            logger.error(f"Error during refactoring analysis: {e}")
            print(f"❌ Error: {e}")
            self.results['status'] = 'error'
            self.results['error'] = str(e)
            sys.exit(1)

    def validate_target(self):
        """Validate the target path exists"""
        logger.debug("Validating target path")
        if not self.target_path.exists():
            logger.warning(f"Target path does not exist: {self.target_path}")
            raise ValueError(f"Target path does not exist: {self.target_path}")

        if self.verbose:
            print(f"✓ Target validated: {self.target_path}")

    def analyze_files(self):
        """Analyze source files in target directory"""
        source_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.rb', '.go'}
        files_analyzed = []

        if self.target_path.is_file():
            if self.target_path.suffix in source_extensions:
                files_analyzed.append(self._analyze_file(self.target_path))
        else:
            for ext in source_extensions:
                for file_path in self.target_path.glob(f'**/*{ext}'):
                    # Skip test files, node_modules, venv
                    if any(skip in str(file_path) for skip in ['test', 'spec', 'node_modules', 'venv', '__pycache__']):
                        continue
                    files_analyzed.append(self._analyze_file(file_path))

        self.results['files_analyzed'] = len(files_analyzed)
        self.results['file_analysis'] = files_analyzed[:50]  # Limit stored results

        if self.verbose:
            print(f"✓ Analyzed {len(files_analyzed)} source files")

    def _analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single file for refactoring opportunities"""
        try:
            content = file_path.read_text()
            lines = content.splitlines()

            analysis = {
                'file': str(file_path.relative_to(self.target_path) if file_path.is_relative_to(self.target_path) else file_path),
                'lines': len(lines),
                'functions': self._count_functions(content, file_path.suffix),
                'complexity_indicators': self._analyze_complexity(content, lines),
                'potential_smells': [],
            }

            return analysis

        except Exception as e:
            return {
                'file': str(file_path),
                'error': str(e),
            }

    def _count_functions(self, content: str, extension: str) -> int:
        """Count functions/methods in file"""
        patterns = {
            '.py': r'^\s*def\s+\w+',
            '.js': r'(?:function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\()',
            '.ts': r'(?:function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\()',
            '.jsx': r'(?:function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\()',
            '.tsx': r'(?:function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\()',
            '.java': r'(?:public|private|protected)?\s+(?:static\s+)?(?:\w+\s+)+\w+\s*\(',
            '.rb': r'^\s*def\s+\w+',
            '.go': r'func\s+(?:\(\w+\s+\*?\w+\)\s+)?\w+\s*\(',
        }
        pattern = patterns.get(extension, r'function')
        return len(re.findall(pattern, content, re.MULTILINE))

    def _analyze_complexity(self, content: str, lines: List[str]) -> Dict:
        """Analyze complexity indicators"""
        return {
            'max_line_length': max((len(line) for line in lines), default=0),
            'nesting_depth': self._calculate_max_nesting(lines),
            'conditional_count': len(re.findall(r'\b(?:if|else|elif|switch|case|when)\b', content)),
            'loop_count': len(re.findall(r'\b(?:for|while|each|forEach|map|filter)\b', content)),
            'try_catch_count': len(re.findall(r'\b(?:try|catch|except|rescue)\b', content)),
        }

    def _calculate_max_nesting(self, lines: List[str]) -> int:
        """Calculate maximum nesting depth"""
        max_depth = 0
        current_depth = 0

        for line in lines:
            stripped = line.lstrip()
            indent = len(line) - len(stripped) if stripped else 0
            # Estimate nesting by indentation (assuming 2-4 space indent)
            estimated_depth = indent // 2
            max_depth = max(max_depth, estimated_depth)

        return min(max_depth // 2, 10)  # Normalize

    def detect_smells(self):
        """Detect code smells across analyzed files"""
        smells = []

        for file_analysis in self.results.get('file_analysis', []):
            if 'error' in file_analysis:
                continue

            file_path = file_analysis['file']
            complexity = file_analysis.get('complexity_indicators', {})

            # Check for long files
            if file_analysis['lines'] > 300:
                smells.append({
                    'file': file_path,
                    'smell': 'long_file',
                    'severity': 'medium',
                    'detail': f"{file_analysis['lines']} lines (threshold: 300)",
                    'suggestion': 'Consider splitting into multiple modules',
                })

            # Check for deep nesting
            if complexity.get('nesting_depth', 0) > 3:
                smells.append({
                    'file': file_path,
                    'smell': 'deep_nesting',
                    'severity': 'medium',
                    'detail': f"Max nesting depth: {complexity['nesting_depth']}",
                    'suggestion': 'Extract nested logic into separate methods',
                })

            # Check for high complexity
            conditionals = complexity.get('conditional_count', 0)
            loops = complexity.get('loop_count', 0)
            if conditionals + loops > 20:
                smells.append({
                    'file': file_path,
                    'smell': 'high_complexity',
                    'severity': 'high',
                    'detail': f"{conditionals} conditionals, {loops} loops",
                    'suggestion': 'Break down into smaller, focused functions',
                })

            # Check for many functions (might indicate god class)
            if file_analysis.get('functions', 0) > 15:
                smells.append({
                    'file': file_path,
                    'smell': 'too_many_functions',
                    'severity': 'low',
                    'detail': f"{file_analysis['functions']} functions",
                    'suggestion': 'Consider splitting related functions into separate modules',
                })

        self.results['smells_detected'] = smells

        if self.verbose:
            print(f"✓ Detected {len(smells)} code smells")

    def generate_suggestions(self):
        """Generate refactoring suggestions based on detected smells"""
        suggestions = []

        for smell in self.results.get('smells_detected', []):
            smell_type = smell.get('smell', '')

            # Map smells to refactoring patterns
            if smell_type in ['long_file', 'too_many_functions']:
                suggestions.append(self._create_suggestion(
                    smell['file'],
                    'extract_class',
                    'Split file into cohesive modules',
                    smell['severity'],
                    ['Identify related functions', 'Create new module', 'Move functions', 'Update imports'],
                ))
            elif smell_type == 'deep_nesting':
                suggestions.append(self._create_suggestion(
                    smell['file'],
                    'extract_method',
                    'Extract nested logic into separate methods',
                    smell['severity'],
                    ['Identify nested block', 'Extract to new method', 'Replace with method call', 'Run tests'],
                ))
            elif smell_type == 'high_complexity':
                suggestions.append(self._create_suggestion(
                    smell['file'],
                    'simplify_conditional',
                    'Simplify complex conditional logic',
                    smell['severity'],
                    ['Identify complex conditions', 'Extract to boolean methods', 'Use early returns', 'Run tests'],
                ))

        # Add general TDD refactoring suggestions
        suggestions.append(self._create_suggestion(
            'general',
            'improve_naming',
            'Review and improve variable/function names',
            'low',
            ['Scan for unclear names', 'Rename using domain language', 'Update all references', 'Run tests'],
        ))

        self.results['refactoring_suggestions'] = suggestions

        if self.verbose:
            print(f"✓ Generated {len(suggestions)} refactoring suggestions")

    def _create_suggestion(self, file: str, refactoring_type: str, description: str,
                          priority: str, steps: List[str]) -> Dict:
        """Create a refactoring suggestion"""
        pattern = self.REFACTORING_PATTERNS.get(refactoring_type, {})
        return {
            'file': file,
            'type': refactoring_type,
            'description': description,
            'priority': priority,
            'pattern_description': pattern.get('description', ''),
            'safety_requirements': pattern.get('safety_requirements', ['Run tests before and after']),
            'steps': steps,
        }

    def check_test_safety(self):
        """Check test coverage and safety for refactoring"""
        safety_checks = []

        # Check for test files
        test_patterns = ['test_*.py', '*_test.py', '*.test.js', '*.spec.js',
                        '*.test.ts', '*.spec.ts', '*Test.java']

        test_files_found = []
        for pattern in test_patterns:
            test_files_found.extend(list(self.target_path.glob(f'**/{pattern}')))

        if test_files_found:
            safety_checks.append({
                'check': 'test_files_exist',
                'status': 'pass',
                'message': f'Found {len(test_files_found)} test files',
                'files': [str(f.name) for f in test_files_found[:5]],
            })
        else:
            safety_checks.append({
                'check': 'test_files_exist',
                'status': 'fail',
                'message': 'No test files found - UNSAFE to refactor',
                'recommendation': 'Write characterization tests before refactoring',
            })

        # Check for coverage reports
        coverage_files = list(self.target_path.glob('**/coverage*')) + \
                        list(self.target_path.glob('**/.coverage'))

        if coverage_files:
            safety_checks.append({
                'check': 'coverage_reports',
                'status': 'pass',
                'message': 'Coverage reports found',
            })
        else:
            safety_checks.append({
                'check': 'coverage_reports',
                'status': 'warning',
                'message': 'No coverage reports - run tests with coverage before refactoring',
                'recommendation': 'npm test -- --coverage OR pytest --cov',
            })

        # Check for CI configuration
        ci_files = ['.github/workflows', '.gitlab-ci.yml', 'Jenkinsfile', '.circleci']
        ci_found = any((self.target_path / ci).exists() for ci in ci_files)

        safety_checks.append({
            'check': 'ci_configuration',
            'status': 'pass' if ci_found else 'warning',
            'message': 'CI pipeline configured' if ci_found else 'No CI found - manual test verification needed',
        })

        self.results['safety_checks'] = safety_checks

        if self.verbose:
            passed = sum(1 for c in safety_checks if c['status'] == 'pass')
            print(f"✓ Safety checks: {passed}/{len(safety_checks)} passed")

    def calculate_metrics(self):
        """Calculate refactoring metrics"""
        smells = self.results.get('smells_detected', [])
        suggestions = self.results.get('refactoring_suggestions', [])
        safety_checks = self.results.get('safety_checks', [])

        metrics = {
            'files_analyzed': self.results['files_analyzed'],
            'total_smells': len(smells),
            'smells_by_severity': {
                'high': sum(1 for s in smells if s.get('severity') == 'high'),
                'medium': sum(1 for s in smells if s.get('severity') == 'medium'),
                'low': sum(1 for s in smells if s.get('severity') == 'low'),
            },
            'total_suggestions': len(suggestions),
            'safety_score': self._calculate_safety_score(safety_checks),
            'refactoring_readiness': 'ready' if all(c['status'] != 'fail' for c in safety_checks) else 'not_ready',
        }

        self.results['metrics'] = metrics

    def _calculate_safety_score(self, safety_checks: List[Dict]) -> str:
        """Calculate overall safety score"""
        if not safety_checks:
            return 'unknown'

        passed = sum(1 for c in safety_checks if c['status'] == 'pass')
        total = len(safety_checks)
        ratio = passed / total

        if ratio >= 0.8:
            return 'high'
        elif ratio >= 0.5:
            return 'medium'
        else:
            return 'low'

    def generate_recommendations(self):
        """Generate refactoring recommendations"""
        recommendations = []

        metrics = self.results.get('metrics', {})

        # Safety recommendations
        if metrics.get('refactoring_readiness') == 'not_ready':
            recommendations.append({
                'type': 'safety',
                'priority': 'critical',
                'message': 'Add test coverage before refactoring',
                'action': 'Write characterization tests to capture current behavior',
            })

        # Smell-based recommendations
        if metrics.get('smells_by_severity', {}).get('high', 0) > 0:
            recommendations.append({
                'type': 'quality',
                'priority': 'high',
                'message': 'Address high-severity smells first',
                'action': 'Focus on complexity reduction before other refactorings',
            })

        # TDD workflow recommendations
        recommendations.extend([
            {
                'type': 'tdd',
                'priority': 'info',
                'message': 'Follow TDD refactor phase rules',
                'rules': [
                    'Run tests after EVERY change',
                    'Revert immediately if tests fail',
                    'Make one small change at a time',
                    'NO new behavior during refactor',
                ],
            },
            {
                'type': 'incremental',
                'priority': 'info',
                'message': 'Use small, reversible steps',
                'example': 'Extract method → Verify tests → Commit → Next step',
            },
        ])

        self.results['recommendations'] = recommendations

    def generate_report(self):
        """Generate and display the analysis report"""
        print("\n" + "=" * 60)
        print("REFACTOR ANALYZER REPORT")
        print("=" * 60)

        metrics = self.results.get('metrics', {})
        smells = self.results.get('smells_detected', [])
        suggestions = self.results.get('refactoring_suggestions', [])
        safety_checks = self.results.get('safety_checks', [])

        # Overview
        print(f"\n📊 Analysis Overview:")
        print(f"   Files Analyzed: {metrics.get('files_analyzed', 0)}")
        print(f"   Code Smells Found: {metrics.get('total_smells', 0)}")
        print(f"   Refactoring Suggestions: {metrics.get('total_suggestions', 0)}")

        # Safety Status
        readiness = metrics.get('refactoring_readiness', 'unknown')
        readiness_icon = '✅' if readiness == 'ready' else '⚠️'
        print(f"\n{readiness_icon} Refactoring Readiness: {readiness.upper()}")
        print(f"   Safety Score: {metrics.get('safety_score', 'unknown')}")

        # Safety Checks
        print(f"\n🔒 Safety Checks:")
        for check in safety_checks:
            icon = '✅' if check['status'] == 'pass' else '⚠️' if check['status'] == 'warning' else '❌'
            print(f"   {icon} {check['check']}: {check['message']}")

        # Code Smells
        if smells:
            print(f"\n🔍 Code Smells Detected ({len(smells)}):")
            by_severity = metrics.get('smells_by_severity', {})
            for severity in ['high', 'medium', 'low']:
                count = by_severity.get(severity, 0)
                if count > 0:
                    print(f"   - {severity.upper()}: {count}")

            print(f"\n   Top Issues:")
            for smell in smells[:5]:
                print(f"   - [{smell['severity'].upper()}] {smell['file']}: {smell['smell']}")

        # Suggestions
        if suggestions:
            print(f"\n💡 Refactoring Suggestions ({len(suggestions)}):")
            for suggestion in suggestions[:5]:
                print(f"   - [{suggestion['priority'].upper()}] {suggestion['type']}: {suggestion['description']}")

        # Recommendations
        print(f"\n📝 Recommendations:")
        for rec in self.results.get('recommendations', [])[:3]:
            icon = '❗' if rec['priority'] in ['critical', 'high'] else '💡'
            print(f"   {icon} [{rec['type'].upper()}] {rec['message']}")

        print("\n" + "=" * 60)


def format_csv_output(results: Dict) -> str:
    """Format analysis results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['file', 'smell', 'severity', 'detail', 'suggestion'])

    for smell in results.get('smells_detected', []):
        writer.writerow([
            smell.get('file', ''),
            smell.get('smell', ''),
            smell.get('severity', ''),
            smell.get('detail', ''),
            smell.get('suggestion', ''),
        ])

    return output.getvalue()


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="RefactorAnalyzer - Validate refactoring safety and suggest improvements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input /path/to/project
  %(prog)s --input ./src --output json
  %(prog)s --input . --no-test-check --output json --file analysis.json
  %(prog)s --input ./lib --suggest-only -v

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Source directory or file to analyze'
    )

    parser.add_argument(
        '--no-test-check',
        action='store_true',
        help='Skip test coverage safety checks'
    )

    parser.add_argument(
        '--suggest-only',
        action='store_true',
        help='Only generate suggestions, skip detailed analysis'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--config', '-c',
        help='Configuration file path'
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

    analyzer = RefactorAnalyzer(
        args.target,
        verbose=args.verbose,
        check_tests=not args.no_test_check,
        suggest_only=args.suggest_only
    )

    results = analyzer.run()

    if args.output == 'csv':
        output = format_csv_output(results)
    elif args.output == 'json':
        output = json.dumps(results, indent=2)
    else:
        output = json.dumps(results, indent=2)

    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Results written to {args.file}")
    else:
        print(output)


if __name__ == '__main__':
    main()
