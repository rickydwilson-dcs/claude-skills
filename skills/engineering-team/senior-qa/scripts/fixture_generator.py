#!/usr/bin/env python3
"""
Fixture Generator
Generate test fixtures with boundary values, edge cases, and realistic test data
"""

import argparse
import csv
import json
import logging
import os
import random
import string
import sys
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FixtureGenerator:
    """Generate comprehensive test fixtures and test data"""

    # Common boundary values by type
    BOUNDARY_VALUES = {
        'integer': {
            'min': -2147483648,
            'max': 2147483647,
            'zero': 0,
            'negative_one': -1,
            'one': 1,
            'common': [0, 1, -1, 10, 100, 1000],
        },
        'string': {
            'empty': '',
            'single_char': 'a',
            'whitespace': '   ',
            'unicode': 'Hello 世界 🌍',
            'special_chars': '!@#$%^&*()',
            'sql_injection': "'; DROP TABLE users; --",
            'xss': '<script>alert("xss")</script>',
            'long': 'a' * 1000,
            'newlines': 'line1\nline2\r\nline3',
        },
        'array': {
            'empty': [],
            'single': ['item'],
            'many': list(range(100)),
            'nested': [[1, 2], [3, 4]],
            'mixed': [1, 'two', None, True],
        },
        'boolean': {
            'true': True,
            'false': False,
        },
        'null': {
            'null': None,
        },
        'email': {
            'valid': 'user@example.com',
            'valid_subdomain': 'user@mail.example.com',
            'valid_plus': 'user+tag@example.com',
            'invalid_no_at': 'userexample.com',
            'invalid_no_domain': 'user@',
            'invalid_no_user': '@example.com',
            'invalid_spaces': 'user @example.com',
            'invalid_double_at': 'user@@example.com',
        },
        'url': {
            'valid_http': 'http://example.com',
            'valid_https': 'https://example.com/path?query=1',
            'valid_port': 'http://localhost:3000',
            'invalid_no_protocol': 'example.com',
            'invalid_spaces': 'http://exam ple.com',
        },
        'date': {
            'valid_iso': '2024-01-15',
            'valid_datetime': '2024-01-15T10:30:00Z',
            'epoch': '1970-01-01',
            'future': '2099-12-31',
            'invalid_format': '15-01-2024',
            'invalid_day': '2024-01-32',
        },
    }

    # Common edge case categories
    EDGE_CASES = {
        'nullability': ['null', 'undefined', 'empty'],
        'boundaries': ['min', 'max', 'zero', 'negative'],
        'format': ['malformed', 'wrong_type', 'truncated'],
        'security': ['injection', 'xss', 'overflow'],
        'encoding': ['unicode', 'special_chars', 'escape_sequences'],
    }

    def __init__(self, target_path: str, verbose: bool = False,
                 data_type: str = None, count: int = 5, include_edge_cases: bool = True):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("FixtureGenerator initialized")

        self.target_path = Path(target_path)
        self.verbose = verbose
        self.data_type = data_type
        self.count = count
        self.include_edge_cases = include_edge_cases
        self.results = {
            'status': 'success',
            'target': str(target_path),
            'fixtures': [],
            'edge_cases': [],
            'factories': {},
            'recommendations': [],
        }

    def run(self) -> Dict:
        """Execute fixture generation"""
        logger.debug("Starting fixture generation run")
        print(f"🚀 Running {self.__class__.__name__}...")
        print(f"📁 Target: {self.target_path}")

        try:
            self.validate_target()
            self.generate_fixtures()
            if self.include_edge_cases:
                self.generate_edge_cases()
            self.create_factories()
            self.generate_recommendations()
            self.generate_report()

            print("✅ Completed successfully!")
            return self.results

        except Exception as e:
            logger.error(f"Error during fixture generation: {e}")
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

    def generate_fixtures(self):
        """Generate test fixtures for specified data type"""
        fixtures = []

        if self.data_type and self.data_type in self.BOUNDARY_VALUES:
            # Generate specific type fixtures
            type_values = self.BOUNDARY_VALUES[self.data_type]
            for name, value in type_values.items():
                fixtures.append({
                    'name': f'{self.data_type}_{name}',
                    'type': self.data_type,
                    'value': value,
                    'description': f'{self.data_type} {name} value',
                })
        else:
            # Generate common fixtures for all types
            for dtype, values in self.BOUNDARY_VALUES.items():
                for name, value in list(values.items())[:3]:
                    fixtures.append({
                        'name': f'{dtype}_{name}',
                        'type': dtype,
                        'value': value,
                        'description': f'{dtype} {name} value',
                    })

        self.results['fixtures'] = fixtures[:self.count * 5]

        if self.verbose:
            print(f"✓ Generated {len(self.results['fixtures'])} fixtures")

    def generate_edge_cases(self):
        """Generate edge case test data"""
        edge_cases = []

        # Null/undefined cases
        edge_cases.extend([
            {'category': 'nullability', 'name': 'null_input', 'value': None, 'expected': 'error or default'},
            {'category': 'nullability', 'name': 'undefined_field', 'value': {'other': 1}, 'expected': 'handle missing field'},
            {'category': 'nullability', 'name': 'empty_string', 'value': '', 'expected': 'validation error or empty result'},
        ])

        # Boundary cases
        edge_cases.extend([
            {'category': 'boundaries', 'name': 'max_integer', 'value': 2147483647, 'expected': 'handle or overflow'},
            {'category': 'boundaries', 'name': 'min_integer', 'value': -2147483648, 'expected': 'handle or underflow'},
            {'category': 'boundaries', 'name': 'empty_array', 'value': [], 'expected': 'return empty or error'},
            {'category': 'boundaries', 'name': 'large_array', 'value': list(range(10000)), 'expected': 'performance consideration'},
        ])

        # Security cases
        edge_cases.extend([
            {'category': 'security', 'name': 'sql_injection', 'value': "'; DROP TABLE users; --", 'expected': 'escaped or rejected'},
            {'category': 'security', 'name': 'xss_script', 'value': '<script>alert("xss")</script>', 'expected': 'sanitized'},
            {'category': 'security', 'name': 'path_traversal', 'value': '../../../etc/passwd', 'expected': 'rejected'},
        ])

        # Encoding cases
        edge_cases.extend([
            {'category': 'encoding', 'name': 'unicode_emoji', 'value': 'Hello 🌍 World', 'expected': 'handle utf-8'},
            {'category': 'encoding', 'name': 'chinese_chars', 'value': '你好世界', 'expected': 'handle multi-byte'},
            {'category': 'encoding', 'name': 'rtl_text', 'value': 'مرحبا', 'expected': 'handle rtl'},
        ])

        self.results['edge_cases'] = edge_cases

        if self.verbose:
            print(f"✓ Generated {len(edge_cases)} edge cases")

    def create_factories(self):
        """Create factory patterns for generating test data"""
        factories = {
            'user': {
                'description': 'Generate user fixture',
                'template': {
                    'id': '${sequence}',
                    'email': '${email}',
                    'name': '${name}',
                    'created_at': '${timestamp}',
                },
                'example': self._generate_user_fixture(),
            },
            'product': {
                'description': 'Generate product fixture',
                'template': {
                    'id': '${sequence}',
                    'name': '${product_name}',
                    'price': '${price}',
                    'quantity': '${quantity}',
                },
                'example': self._generate_product_fixture(),
            },
            'order': {
                'description': 'Generate order fixture',
                'template': {
                    'id': '${sequence}',
                    'user_id': '${user_id}',
                    'items': '${items}',
                    'total': '${total}',
                    'status': '${status}',
                },
                'example': self._generate_order_fixture(),
            },
        }

        self.results['factories'] = factories

    def _generate_user_fixture(self) -> Dict:
        """Generate sample user fixture"""
        return {
            'id': 1,
            'email': 'testuser@example.com',
            'name': 'Test User',
            'created_at': datetime.now().isoformat(),
        }

    def _generate_product_fixture(self) -> Dict:
        """Generate sample product fixture"""
        return {
            'id': 1,
            'name': 'Test Product',
            'price': 99.99,
            'quantity': 100,
        }

    def _generate_order_fixture(self) -> Dict:
        """Generate sample order fixture"""
        return {
            'id': 1,
            'user_id': 1,
            'items': [{'product_id': 1, 'quantity': 2}],
            'total': 199.98,
            'status': 'pending',
        }

    def generate_recommendations(self):
        """Generate fixture usage recommendations"""
        recommendations = [
            {
                'type': 'organization',
                'message': 'Keep fixtures in a dedicated fixtures/ directory',
                'example': 'fixtures/users.json, fixtures/products.json',
            },
            {
                'type': 'naming',
                'message': 'Use descriptive names that indicate the scenario',
                'example': 'valid_user, invalid_email_user, admin_user',
            },
            {
                'type': 'coverage',
                'message': 'Include happy path, edge cases, and error scenarios',
                'categories': ['valid', 'invalid', 'boundary', 'null', 'security'],
            },
            {
                'type': 'maintenance',
                'message': 'Use factories for dynamic data generation',
                'benefit': 'Reduces fixture maintenance and improves test isolation',
            },
        ]

        self.results['recommendations'] = recommendations

    def generate_report(self):
        """Generate and display the fixture generation report"""
        print("\n" + "=" * 60)
        print("FIXTURE GENERATOR REPORT")
        print("=" * 60)

        # Fixtures summary
        print(f"\n📦 Generated {len(self.results['fixtures'])} Fixtures:")
        for fixture in self.results['fixtures'][:10]:
            value_preview = str(fixture['value'])[:30]
            if len(str(fixture['value'])) > 30:
                value_preview += '...'
            print(f"   - {fixture['name']}: {value_preview}")

        if len(self.results['fixtures']) > 10:
            print(f"   ... and {len(self.results['fixtures']) - 10} more")

        # Edge cases summary
        if self.results['edge_cases']:
            print(f"\n⚠️  Generated {len(self.results['edge_cases'])} Edge Cases:")
            categories = set(ec['category'] for ec in self.results['edge_cases'])
            for cat in categories:
                count = sum(1 for ec in self.results['edge_cases'] if ec['category'] == cat)
                print(f"   - {cat}: {count} cases")

        # Factories
        print(f"\n🏭 Available Factories:")
        for name, factory in self.results['factories'].items():
            print(f"   - {name}: {factory['description']}")

        # Recommendations
        print(f"\n💡 Recommendations:")
        for rec in self.results['recommendations'][:3]:
            print(f"   - [{rec['type'].upper()}] {rec['message']}")

        print("\n" + "=" * 60)


def format_csv_output(results: Dict) -> str:
    """Format fixture results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['name', 'type', 'value', 'description'])

    for fixture in results.get('fixtures', []):
        writer.writerow([
            fixture.get('name', ''),
            fixture.get('type', ''),
            json.dumps(fixture.get('value')),
            fixture.get('description', ''),
        ])

    return output.getvalue()


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="FixtureGenerator - Generate test fixtures and edge cases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input /path/to/project
  %(prog)s --input . --type email --count 10
  %(prog)s --input ./tests --output json --file fixtures.json
  %(prog)s --input . --no-edge-cases -v

Data Types:
  integer, string, array, boolean, null, email, url, date

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
        '--type', '-t',
        choices=['integer', 'string', 'array', 'boolean', 'null', 'email', 'url', 'date'],
        help='Specific data type to generate fixtures for'
    )

    parser.add_argument(
        '--count', '-n',
        type=int,
        default=5,
        help='Number of fixtures to generate per category (default: 5)'
    )

    parser.add_argument(
        '--no-edge-cases',
        action='store_true',
        help='Skip edge case generation'
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

    generator = FixtureGenerator(
        args.target,
        verbose=args.verbose,
        data_type=args.type,
        count=args.count,
        include_edge_cases=not args.no_edge_cases
    )

    results = generator.run()

    if args.output == 'csv':
        output = format_csv_output(results)
    elif args.output == 'json':
        output = json.dumps(results, indent=2, default=str)
    else:
        output = json.dumps(results, indent=2, default=str)

    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Results written to {args.file}")
    else:
        print(output)


if __name__ == '__main__':
    main()
