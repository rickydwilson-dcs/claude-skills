#!/usr/bin/env python3
"""
Format Detector
Auto-detect test framework and coverage format from project configuration
"""

import os
import sys
import json
import csv
from io import StringIO
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class FormatDetector:
    """Detect test framework, coverage format, and project configuration"""

    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        'jest': {
            'files': ['jest.config.js', 'jest.config.ts', 'jest.config.mjs', 'jest.config.cjs'],
            'package_keys': ['jest'],
            'dev_deps': ['jest', '@jest/core'],
            'scripts': ['jest'],
        },
        'vitest': {
            'files': ['vitest.config.js', 'vitest.config.ts', 'vite.config.js', 'vite.config.ts'],
            'package_keys': ['vitest'],
            'dev_deps': ['vitest'],
            'scripts': ['vitest'],
        },
        'mocha': {
            'files': ['.mocharc.js', '.mocharc.json', '.mocharc.yml', 'mocha.opts'],
            'package_keys': ['mocha'],
            'dev_deps': ['mocha'],
            'scripts': ['mocha'],
        },
        'pytest': {
            'files': ['pytest.ini', 'pyproject.toml', 'setup.cfg', 'conftest.py'],
            'package_keys': ['pytest'],
            'config_sections': ['tool.pytest', '[pytest]'],
        },
        'unittest': {
            'files': ['test_*.py', '*_test.py'],
            'imports': ['import unittest', 'from unittest'],
        },
        'junit': {
            'files': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
            'package_keys': ['junit'],
            'deps': ['junit-jupiter', 'junit-vintage'],
        },
        'rspec': {
            'files': ['.rspec', 'spec/spec_helper.rb'],
            'gem_deps': ['rspec', 'rspec-rails'],
        },
    }

    # Coverage format patterns
    COVERAGE_PATTERNS = {
        'istanbul': {
            'files': ['coverage/coverage-final.json', 'coverage/lcov.info'],
            'format': 'json',
            'tools': ['nyc', 'istanbul', 'c8'],
        },
        'lcov': {
            'files': ['coverage/lcov.info', 'lcov.info'],
            'format': 'lcov',
            'tools': ['lcov', 'genhtml'],
        },
        'cobertura': {
            'files': ['coverage.xml', 'cobertura.xml'],
            'format': 'xml',
            'tools': ['cobertura', 'coverage.py'],
        },
        'jacoco': {
            'files': ['target/site/jacoco/jacoco.xml', 'build/reports/jacoco/test/jacocoTestReport.xml'],
            'format': 'xml',
            'tools': ['jacoco'],
        },
        'coverage_py': {
            'files': ['.coverage', 'htmlcov/index.html', 'coverage.json'],
            'format': 'sqlite',
            'tools': ['coverage', 'pytest-cov'],
        },
    }

    def __init__(self, target_path: str, verbose: bool = False):
        self.target_path = Path(target_path)
        self.verbose = verbose
        self.results = {
            'status': 'success',
            'target': str(target_path),
            'framework': None,
            'coverage_format': None,
            'language': None,
            'config_files': [],
            'recommendations': [],
            'confidence': 0.0,
        }

    def run(self) -> Dict:
        """Execute the detection process"""
        print(f"🚀 Running {self.__class__.__name__}...")
        print(f"📁 Target: {self.target_path}")

        try:
            self.validate_target()
            self.detect_language()
            self.detect_framework()
            self.detect_coverage_format()
            self.generate_recommendations()
            self.generate_report()

            print("✅ Completed successfully!")
            return self.results

        except Exception as e:
            print(f"❌ Error: {e}")
            self.results['status'] = 'error'
            self.results['error'] = str(e)
            sys.exit(1)

    def validate_target(self):
        """Validate the target path exists"""
        if not self.target_path.exists():
            raise ValueError(f"Target path does not exist: {self.target_path}")

        if self.verbose:
            print(f"✓ Target validated: {self.target_path}")

    def detect_language(self):
        """Detect primary programming language"""
        language_indicators = {
            'javascript': ['package.json', 'node_modules', '.npmrc', 'yarn.lock', 'pnpm-lock.yaml'],
            'typescript': ['tsconfig.json', '*.ts', '*.tsx'],
            'python': ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile', '*.py'],
            'java': ['pom.xml', 'build.gradle', 'build.gradle.kts', '*.java'],
            'ruby': ['Gemfile', 'Rakefile', '*.rb'],
            'go': ['go.mod', 'go.sum', '*.go'],
        }

        detected = []
        for lang, indicators in language_indicators.items():
            for indicator in indicators:
                if '*' in indicator:
                    # Glob pattern
                    pattern = indicator
                    matches = list(self.target_path.glob(f"**/{pattern}"))[:5]
                    if matches:
                        detected.append((lang, len(matches)))
                        break
                else:
                    # Exact file
                    if (self.target_path / indicator).exists():
                        detected.append((lang, 10))  # Higher weight for config files
                        break

        if detected:
            # Sort by weight and take highest
            detected.sort(key=lambda x: x[1], reverse=True)
            self.results['language'] = detected[0][0]
            if self.verbose:
                print(f"✓ Detected language: {self.results['language']}")

    def detect_framework(self):
        """Detect test framework from project files"""
        framework_scores = {}

        for framework, patterns in self.FRAMEWORK_PATTERNS.items():
            score = 0

            # Check config files
            for config_file in patterns.get('files', []):
                if '*' in config_file:
                    matches = list(self.target_path.glob(f"**/{config_file}"))[:3]
                    if matches:
                        score += 5
                        self.results['config_files'].extend([str(m) for m in matches])
                elif (self.target_path / config_file).exists():
                    score += 10
                    self.results['config_files'].append(config_file)

            # Check package.json for JS/TS frameworks
            package_json = self.target_path / 'package.json'
            if package_json.exists():
                try:
                    with open(package_json) as f:
                        pkg = json.load(f)

                    # Check devDependencies
                    dev_deps = pkg.get('devDependencies', {})
                    for dep in patterns.get('dev_deps', []):
                        if dep in dev_deps:
                            score += 15

                    # Check scripts
                    scripts = pkg.get('scripts', {})
                    for script_name in patterns.get('scripts', []):
                        for script_value in scripts.values():
                            if script_name in script_value:
                                score += 8
                                break

                except (json.JSONDecodeError, IOError):
                    pass

            # Check pyproject.toml for Python frameworks
            pyproject = self.target_path / 'pyproject.toml'
            if pyproject.exists():
                try:
                    content = pyproject.read_text()
                    for section in patterns.get('config_sections', []):
                        if section in content:
                            score += 12
                except IOError:
                    pass

            if score > 0:
                framework_scores[framework] = score

        if framework_scores:
            best_framework = max(framework_scores, key=framework_scores.get)
            max_score = framework_scores[best_framework]
            self.results['framework'] = {
                'name': best_framework,
                'confidence': min(max_score / 30.0, 1.0),
                'alternatives': [
                    {'name': k, 'score': v}
                    for k, v in sorted(framework_scores.items(), key=lambda x: -x[1])
                    if k != best_framework
                ][:3],
            }
            self.results['confidence'] = self.results['framework']['confidence']

            if self.verbose:
                print(f"✓ Detected framework: {best_framework} (confidence: {self.results['confidence']:.0%})")

    def detect_coverage_format(self):
        """Detect coverage report format"""
        for coverage_type, patterns in self.COVERAGE_PATTERNS.items():
            for coverage_file in patterns.get('files', []):
                file_path = self.target_path / coverage_file
                if file_path.exists():
                    self.results['coverage_format'] = {
                        'type': coverage_type,
                        'format': patterns['format'],
                        'file': str(coverage_file),
                        'tools': patterns.get('tools', []),
                    }
                    if self.verbose:
                        print(f"✓ Detected coverage format: {coverage_type}")
                    return

    def generate_recommendations(self):
        """Generate configuration recommendations"""
        recommendations = []

        # Framework-specific recommendations
        if self.results['framework']:
            framework = self.results['framework']['name']

            if framework == 'jest':
                recommendations.append({
                    'type': 'config',
                    'priority': 'high',
                    'message': 'Enable coverage collection in jest.config.js',
                    'example': "collectCoverage: true, coverageThreshold: { global: { lines: 80 } }",
                })
            elif framework == 'pytest':
                recommendations.append({
                    'type': 'config',
                    'priority': 'high',
                    'message': 'Add pytest-cov for coverage reporting',
                    'example': 'pip install pytest-cov && pytest --cov=src --cov-report=json',
                })
            elif framework == 'vitest':
                recommendations.append({
                    'type': 'config',
                    'priority': 'high',
                    'message': 'Enable coverage in vitest.config.ts',
                    'example': "coverage: { enabled: true, provider: 'v8' }",
                })

        # Coverage recommendations
        if not self.results['coverage_format']:
            recommendations.append({
                'type': 'coverage',
                'priority': 'medium',
                'message': 'No coverage reports detected - run tests with coverage enabled',
                'example': 'npm test -- --coverage (Jest) or pytest --cov (Python)',
            })

        # TDD recommendations
        recommendations.append({
            'type': 'tdd',
            'priority': 'info',
            'message': 'For TDD workflow, use tdd_workflow.py to track Red-Green-Refactor cycles',
            'example': 'python tdd_workflow.py --phase red --test-file tests/test_feature.py',
        })

        self.results['recommendations'] = recommendations

    def generate_report(self):
        """Generate and display the detection report"""
        print("\n" + "=" * 60)
        print("FORMAT DETECTION REPORT")
        print("=" * 60)

        print(f"\n📁 Project: {self.results['target']}")

        if self.results['language']:
            print(f"🔤 Language: {self.results['language']}")

        if self.results['framework']:
            fw = self.results['framework']
            print(f"🧪 Test Framework: {fw['name']} (confidence: {fw['confidence']:.0%})")
            if fw.get('alternatives'):
                alts = ', '.join([a['name'] for a in fw['alternatives']])
                print(f"   Alternatives: {alts}")

        if self.results['coverage_format']:
            cv = self.results['coverage_format']
            print(f"📊 Coverage Format: {cv['type']} ({cv['format']})")
            print(f"   File: {cv['file']}")

        if self.results['config_files']:
            print(f"\n📄 Config Files Found:")
            for cf in self.results['config_files'][:5]:
                print(f"   - {cf}")

        if self.results['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in self.results['recommendations']:
                icon = '❗' if rec['priority'] == 'high' else '💡'
                print(f"   {icon} [{rec['type'].upper()}] {rec['message']}")

        print("\n" + "=" * 60)


def format_csv_output(results: Dict) -> str:
    """Format detection results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['field', 'value', 'confidence'])

    writer.writerow(['language', results.get('language', 'unknown'), ''])
    if results.get('framework'):
        fw = results['framework']
        writer.writerow(['framework', fw['name'], f"{fw['confidence']:.0%}"])
    if results.get('coverage_format'):
        cv = results['coverage_format']
        writer.writerow(['coverage_format', cv['type'], cv['format']])

    return output.getvalue()


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="FormatDetector - Auto-detect test framework and coverage format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input /path/to/project
  %(prog)s --input . --output json
  %(prog)s --input ./myapp --output json --file detection.json
  %(prog)s --input . -v

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Project root path to analyze'
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

    args = parser.parse_args()

    detector = FormatDetector(
        args.target,
        verbose=args.verbose
    )

    results = detector.run()

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
