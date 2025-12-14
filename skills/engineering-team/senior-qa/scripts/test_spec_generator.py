#!/usr/bin/env python3
"""
Test Spec Generator
Generate Given-When-Then test specifications from feature requirements
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
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestSpecGenerator:
    """Generate BDD-style test specifications from requirements"""

    # Common action verbs for requirement parsing
    ACTION_VERBS = [
        'create', 'read', 'update', 'delete', 'get', 'set', 'add', 'remove',
        'validate', 'verify', 'check', 'calculate', 'process', 'transform',
        'send', 'receive', 'submit', 'cancel', 'approve', 'reject',
        'login', 'logout', 'register', 'authenticate', 'authorize',
        'search', 'filter', 'sort', 'paginate', 'export', 'import',
    ]

    # Common subjects for test scenarios
    SUBJECTS = [
        'user', 'admin', 'system', 'service', 'api', 'client',
        'customer', 'guest', 'authenticated user', 'anonymous user',
    ]

    # Edge case categories to consider
    EDGE_CASE_CATEGORIES = {
        'input_validation': [
            'empty input', 'null input', 'whitespace only',
            'maximum length', 'minimum length', 'invalid format',
        ],
        'authentication': [
            'unauthenticated user', 'expired token', 'invalid credentials',
            'insufficient permissions', 'locked account',
        ],
        'data_state': [
            'resource not found', 'resource already exists', 'stale data',
            'concurrent modification', 'cascade effects',
        ],
        'boundary': [
            'zero value', 'negative value', 'maximum value',
            'empty collection', 'single item', 'large collection',
        ],
        'network': [
            'timeout', 'connection refused', 'rate limited',
            'partial response', 'retry scenario',
        ],
    }

    def __init__(self, target_path: str, verbose: bool = False,
                 requirement: str = None, framework: str = 'jest',
                 include_edge_cases: bool = True):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("TestSpecGenerator initialized")

        self.target_path = Path(target_path)
        self.verbose = verbose
        self.requirement = requirement or ''
        self.framework = framework
        self.include_edge_cases = include_edge_cases
        self.results = {
            'status': 'success',
            'target': str(target_path),
            'requirement': self.requirement,
            'framework': framework,
            'specs': [],
            'edge_cases': [],
            'test_file_template': '',
            'recommendations': [],
        }

    def run(self) -> Dict:
        """Execute test spec generation"""
        logger.debug("Starting test spec generation run")
        print(f"🚀 Running {self.__class__.__name__}...")
        print(f"📁 Target: {self.target_path}")
        if self.requirement:
            print(f"📋 Requirement: {self.requirement[:50]}...")

        try:
            self.validate_target()
            self.parse_requirement()
            self.generate_specs()
            if self.include_edge_cases:
                self.generate_edge_case_specs()
            self.generate_test_template()
            self.generate_recommendations()
            self.generate_report()

            print("✅ Completed successfully!")
            return self.results

        except Exception as e:
            logger.error(f"Error during test spec generation: {e}")
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

    def parse_requirement(self):
        """Parse requirement text to extract key components"""
        parsed = {
            'original': self.requirement,
            'subject': None,
            'action': None,
            'object': None,
            'conditions': [],
            'outcomes': [],
        }

        req_lower = self.requirement.lower()

        # Extract subject (who/what performs the action)
        for subject in self.SUBJECTS:
            if subject in req_lower:
                parsed['subject'] = subject
                break
        if not parsed['subject']:
            parsed['subject'] = 'system'

        # Extract action verb
        for verb in self.ACTION_VERBS:
            if verb in req_lower:
                parsed['action'] = verb
                break
        if not parsed['action']:
            parsed['action'] = 'process'

        # Extract conditions (when/if clauses)
        condition_patterns = [
            r'when\s+([^,\.]+)',
            r'if\s+([^,\.]+)',
            r'given\s+([^,\.]+)',
        ]
        for pattern in condition_patterns:
            matches = re.findall(pattern, req_lower)
            parsed['conditions'].extend(matches)

        # Extract expected outcomes (should/must/will)
        outcome_patterns = [
            r'should\s+([^,\.]+)',
            r'must\s+([^,\.]+)',
            r'will\s+([^,\.]+)',
        ]
        for pattern in outcome_patterns:
            matches = re.findall(pattern, req_lower)
            parsed['outcomes'].extend(matches)

        self.results['parsed_requirement'] = parsed

        if self.verbose:
            print(f"✓ Parsed requirement: {parsed['action']} by {parsed['subject']}")

    def generate_specs(self):
        """Generate Given-When-Then specifications"""
        specs = []
        parsed = self.results.get('parsed_requirement', {})

        # Main happy path spec
        main_spec = self._create_spec(
            title=f"should {parsed.get('action', 'process')} successfully",
            given=self._generate_given(parsed),
            when=self._generate_when(parsed),
            then=self._generate_then(parsed),
            category='happy_path',
            priority='high',
        )
        specs.append(main_spec)

        # Generate variations based on conditions
        for condition in parsed.get('conditions', [])[:3]:
            spec = self._create_spec(
                title=f"should handle {condition}",
                given=f"the {parsed.get('subject', 'system')} is ready AND {condition}",
                when=f"attempting to {parsed.get('action', 'process')}",
                then="the operation completes appropriately",
                category='conditional',
                priority='medium',
            )
            specs.append(spec)

        # Generate specs for expected outcomes
        for outcome in parsed.get('outcomes', [])[:3]:
            spec = self._create_spec(
                title=f"should {outcome}",
                given=self._generate_given(parsed),
                when=self._generate_when(parsed),
                then=f"it {outcome}",
                category='outcome',
                priority='high',
            )
            specs.append(spec)

        self.results['specs'] = specs

        if self.verbose:
            print(f"✓ Generated {len(specs)} test specifications")

    def _create_spec(self, title: str, given: str, when: str, then: str,
                     category: str, priority: str) -> Dict:
        """Create a test specification object"""
        return {
            'title': title,
            'given': given,
            'when': when,
            'then': then,
            'category': category,
            'priority': priority,
            'test_name': self._generate_test_name(title),
        }

    def _generate_given(self, parsed: Dict) -> str:
        """Generate Given clause"""
        subject = parsed.get('subject', 'the system')
        return f"{subject} is in a valid state"

    def _generate_when(self, parsed: Dict) -> str:
        """Generate When clause"""
        action = parsed.get('action', 'processing')
        return f"{action} is invoked"

    def _generate_then(self, parsed: Dict) -> str:
        """Generate Then clause"""
        action = parsed.get('action', 'process')
        return f"the {action} operation succeeds"

    def _generate_test_name(self, title: str) -> str:
        """Convert title to test function name"""
        # Remove non-alphanumeric, convert to snake_case
        name = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
        name = re.sub(r'\s+', '_', name.strip())
        return f"test_{name}"

    def generate_edge_case_specs(self):
        """Generate edge case test specifications"""
        edge_cases = []
        parsed = self.results.get('parsed_requirement', {})
        action = parsed.get('action', 'process')

        # Input validation edge cases
        edge_cases.extend([
            self._create_spec(
                title=f"should reject empty input when {action}",
                given="empty input is provided",
                when=f"attempting to {action}",
                then="a validation error is returned",
                category='input_validation',
                priority='high',
            ),
            self._create_spec(
                title=f"should handle null input gracefully",
                given="null/undefined input is provided",
                when=f"attempting to {action}",
                then="appropriate error handling occurs",
                category='input_validation',
                priority='high',
            ),
        ])

        # Authentication edge cases (if action suggests auth)
        if action in ['login', 'authenticate', 'authorize', 'create', 'update', 'delete']:
            edge_cases.extend([
                self._create_spec(
                    title=f"should deny access for unauthenticated user",
                    given="user is not authenticated",
                    when=f"attempting to {action}",
                    then="401 Unauthorized is returned",
                    category='authentication',
                    priority='high',
                ),
                self._create_spec(
                    title=f"should deny access for insufficient permissions",
                    given="user lacks required permissions",
                    when=f"attempting to {action}",
                    then="403 Forbidden is returned",
                    category='authentication',
                    priority='medium',
                ),
            ])

        # Data state edge cases
        edge_cases.extend([
            self._create_spec(
                title=f"should handle resource not found",
                given="the requested resource does not exist",
                when=f"attempting to {action}",
                then="404 Not Found is returned",
                category='data_state',
                priority='medium',
            ),
        ])

        # Boundary cases
        edge_cases.extend([
            self._create_spec(
                title=f"should handle boundary values",
                given="input is at boundary (min/max/zero)",
                when=f"attempting to {action}",
                then="boundary is handled correctly",
                category='boundary',
                priority='medium',
            ),
        ])

        self.results['edge_cases'] = edge_cases

        if self.verbose:
            print(f"✓ Generated {len(edge_cases)} edge case specifications")

    def generate_test_template(self):
        """Generate test file template based on framework"""
        specs = self.results.get('specs', []) + self.results.get('edge_cases', [])

        if self.framework == 'jest':
            template = self._generate_jest_template(specs)
        elif self.framework == 'pytest':
            template = self._generate_pytest_template(specs)
        elif self.framework == 'vitest':
            template = self._generate_vitest_template(specs)
        elif self.framework == 'mocha':
            template = self._generate_mocha_template(specs)
        else:
            template = self._generate_generic_template(specs)

        self.results['test_file_template'] = template

    def _generate_jest_template(self, specs: List[Dict]) -> str:
        """Generate Jest test template"""
        lines = [
            "// Auto-generated test specifications",
            f"// Generated: {datetime.now().isoformat()}",
            "// Framework: Jest",
            "",
            "describe('Feature: ${FEATURE_NAME}', () => {",
            "  beforeEach(() => {",
            "    // Setup test fixtures",
            "  });",
            "",
            "  afterEach(() => {",
            "    // Cleanup",
            "  });",
            "",
        ]

        # Group by category
        categories = {}
        for spec in specs:
            cat = spec.get('category', 'general')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(spec)

        for category, cat_specs in categories.items():
            lines.append(f"  describe('{category}', () => {{")
            for spec in cat_specs:
                lines.extend([
                    f"    it('{spec['title']}', () => {{",
                    f"      // GIVEN: {spec['given']}",
                    f"      // TODO: Setup preconditions",
                    "",
                    f"      // WHEN: {spec['when']}",
                    f"      // TODO: Execute action",
                    "",
                    f"      // THEN: {spec['then']}",
                    f"      // TODO: Assert expectations",
                    "      expect(true).toBe(false); // RED phase - implement me",
                    "    });",
                    "",
                ])
            lines.append("  });")
            lines.append("")

        lines.append("});")
        return '\n'.join(lines)

    def _generate_pytest_template(self, specs: List[Dict]) -> str:
        """Generate Pytest template"""
        lines = [
            '"""',
            "Auto-generated test specifications",
            f"Generated: {datetime.now().isoformat()}",
            "Framework: Pytest",
            '"""',
            "",
            "import pytest",
            "",
            "",
            "class TestFeature:",
            '    """Feature: ${FEATURE_NAME}"""',
            "",
            "    @pytest.fixture(autouse=True)",
            "    def setup(self):",
            '        """Setup test fixtures"""',
            "        pass",
            "",
        ]

        for spec in specs:
            lines.extend([
                f"    def {spec['test_name']}(self):",
                f'        """',
                f"        GIVEN: {spec['given']}",
                f"        WHEN: {spec['when']}",
                f"        THEN: {spec['then']}",
                f'        """',
                "        # TODO: Setup preconditions (GIVEN)",
                "",
                "        # TODO: Execute action (WHEN)",
                "",
                "        # TODO: Assert expectations (THEN)",
                "        assert False, 'RED phase - implement me'",
                "",
            ])

        return '\n'.join(lines)

    def _generate_vitest_template(self, specs: List[Dict]) -> str:
        """Generate Vitest template"""
        lines = [
            "// Auto-generated test specifications",
            f"// Generated: {datetime.now().isoformat()}",
            "// Framework: Vitest",
            "",
            "import { describe, it, expect, beforeEach, afterEach } from 'vitest';",
            "",
            "describe('Feature: ${FEATURE_NAME}', () => {",
            "  beforeEach(() => {",
            "    // Setup test fixtures",
            "  });",
            "",
        ]

        for spec in specs:
            lines.extend([
                f"  it('{spec['title']}', () => {{",
                f"    // GIVEN: {spec['given']}",
                "",
                f"    // WHEN: {spec['when']}",
                "",
                f"    // THEN: {spec['then']}",
                "    expect(true).toBe(false); // RED phase - implement me",
                "  });",
                "",
            ])

        lines.append("});")
        return '\n'.join(lines)

    def _generate_mocha_template(self, specs: List[Dict]) -> str:
        """Generate Mocha template"""
        lines = [
            "// Auto-generated test specifications",
            f"// Generated: {datetime.now().isoformat()}",
            "// Framework: Mocha",
            "",
            "const { expect } = require('chai');",
            "",
            "describe('Feature: ${FEATURE_NAME}', function() {",
            "  beforeEach(function() {",
            "    // Setup test fixtures",
            "  });",
            "",
        ]

        for spec in specs:
            lines.extend([
                f"  it('{spec['title']}', function() {{",
                f"    // GIVEN: {spec['given']}",
                "",
                f"    // WHEN: {spec['when']}",
                "",
                f"    // THEN: {spec['then']}",
                "    expect(true).to.equal(false); // RED phase - implement me",
                "  });",
                "",
            ])

        lines.append("});")
        return '\n'.join(lines)

    def _generate_generic_template(self, specs: List[Dict]) -> str:
        """Generate generic pseudo-code template"""
        lines = [
            "# Auto-generated test specifications",
            f"# Generated: {datetime.now().isoformat()}",
            "",
            "Feature: ${FEATURE_NAME}",
            "",
        ]

        for spec in specs:
            lines.extend([
                f"  Scenario: {spec['title']}",
                f"    Given {spec['given']}",
                f"    When {spec['when']}",
                f"    Then {spec['then']}",
                "",
            ])

        return '\n'.join(lines)

    def generate_recommendations(self):
        """Generate test writing recommendations"""
        recommendations = [
            {
                'type': 'tdd_workflow',
                'message': 'Start with RED phase - run tests to confirm they fail',
                'command': f"Run tests with: {'npm test' if self.framework in ['jest', 'vitest', 'mocha'] else 'pytest'}",
            },
            {
                'type': 'naming',
                'message': 'Use descriptive test names following should_X_when_Y pattern',
                'example': 'should_return_error_when_input_is_empty',
            },
            {
                'type': 'isolation',
                'message': 'Each test should be independent - use setup/teardown',
                'tip': 'Avoid shared state between tests',
            },
            {
                'type': 'coverage',
                'message': 'Prioritize high-priority specs first',
                'priority_order': ['happy_path', 'input_validation', 'authentication'],
            },
            {
                'type': 'assertions',
                'message': 'Use specific assertions over generic ones',
                'example': "expect(result.status).toBe(200) over expect(result).toBeTruthy()",
            },
        ]

        self.results['recommendations'] = recommendations

    def generate_report(self):
        """Generate and display the spec generation report"""
        print("\n" + "=" * 60)
        print("TEST SPECIFICATION GENERATOR REPORT")
        print("=" * 60)

        # Requirement summary
        print(f"\n📋 Requirement: {self.requirement[:80]}...")
        print(f"🧪 Framework: {self.framework}")

        # Parsed requirement
        parsed = self.results.get('parsed_requirement', {})
        print(f"\n🔍 Parsed:")
        print(f"   Subject: {parsed.get('subject', 'N/A')}")
        print(f"   Action: {parsed.get('action', 'N/A')}")
        if parsed.get('conditions'):
            print(f"   Conditions: {', '.join(parsed['conditions'][:3])}")

        # Specs summary
        specs = self.results.get('specs', [])
        edge_cases = self.results.get('edge_cases', [])
        print(f"\n✅ Generated {len(specs)} Main Specs:")
        for spec in specs[:5]:
            print(f"   - [{spec['priority'].upper()}] {spec['title']}")

        if edge_cases:
            print(f"\n⚠️  Generated {len(edge_cases)} Edge Case Specs:")
            categories = set(ec['category'] for ec in edge_cases)
            for cat in categories:
                count = sum(1 for ec in edge_cases if ec['category'] == cat)
                print(f"   - {cat}: {count} specs")

        # Recommendations
        print(f"\n💡 Recommendations:")
        for rec in self.results.get('recommendations', [])[:3]:
            print(f"   - [{rec['type'].upper()}] {rec['message']}")

        print("\n" + "=" * 60)


def format_csv_output(results: Dict) -> str:
    """Format spec results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['title', 'given', 'when', 'then', 'category', 'priority'])

    for spec in results.get('specs', []) + results.get('edge_cases', []):
        writer.writerow([
            spec.get('title', ''),
            spec.get('given', ''),
            spec.get('when', ''),
            spec.get('then', ''),
            spec.get('category', ''),
            spec.get('priority', ''),
        ])

    return output.getvalue()


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="TestSpecGenerator - Generate Given-When-Then test specifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input /path/to/project --requirement "User can login with email"
  %(prog)s --input . --requirement "API validates input" --framework pytest
  %(prog)s --input ./tests --requirement "Calculate total" --output json --file specs.json
  %(prog)s --input . --requirement "Send notification" --no-edge-cases -v

Frameworks:
  jest, vitest, mocha, pytest

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Project or test directory path'
    )

    parser.add_argument(
        '--requirement', '-r',
        required=True,
        help='Feature requirement text to generate specs from'
    )

    parser.add_argument(
        '--framework', '-fw',
        choices=['jest', 'vitest', 'mocha', 'pytest'],
        default='jest',
        help='Test framework for template generation (default: jest)'
    )

    parser.add_argument(
        '--no-edge-cases',
        action='store_true',
        help='Skip edge case spec generation'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv', 'template'],
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

    generator = TestSpecGenerator(
        args.target,
        verbose=args.verbose,
        requirement=args.requirement,
        framework=args.framework,
        include_edge_cases=not args.no_edge_cases
    )

    results = generator.run()

    if args.output == 'csv':
        output = format_csv_output(results)
    elif args.output == 'template':
        output = results.get('test_file_template', '')
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
