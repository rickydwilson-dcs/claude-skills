#!/usr/bin/env python3
"""
TDD Workflow
Red-Green-Refactor cycle orchestration and phase management
"""

import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TDDPhase(Enum):
    """TDD cycle phases"""
    RED = "red"
    GREEN = "green"
    REFACTOR = "refactor"
    COMPLETE = "complete"


class TDDWorkflow:
    """Orchestrate TDD Red-Green-Refactor cycles with tracking and validation"""

    PHASE_DESCRIPTIONS = {
        TDDPhase.RED: "Write a failing test that defines expected behavior",
        TDDPhase.GREEN: "Write minimal code to make the test pass",
        TDDPhase.REFACTOR: "Improve code quality while keeping tests green",
        TDDPhase.COMPLETE: "Cycle complete - ready for next feature",
    }

    PHASE_CHECKLIST = {
        TDDPhase.RED: [
            "Test describes expected behavior clearly",
            "Test fails for the right reason (not syntax error)",
            "Test is focused on one behavior",
            "Test uses descriptive naming (should_X_when_Y)",
        ],
        TDDPhase.GREEN: [
            "All tests pass",
            "Implementation is minimal (no extra features)",
            "No premature optimization",
            "Code compiles/runs without errors",
        ],
        TDDPhase.REFACTOR: [
            "All tests still pass",
            "Code is more readable",
            "Duplication is reduced",
            "Names are meaningful",
            "No behavior changes introduced",
        ],
    }

    def __init__(self, target_path: str, verbose: bool = False, phase: str = None, test_file: str = None):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("TDDWorkflow initialized")

        self.target_path = Path(target_path)
        self.verbose = verbose
        self.current_phase = TDDPhase(phase) if phase else TDDPhase.RED
        self.test_file = test_file
        self.results = {
            'status': 'success',
            'target': str(target_path),
            'phase': self.current_phase.value,
            'cycle_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'checklist': [],
            'guidance': [],
            'metrics': {},
            'next_steps': [],
        }

    def run(self) -> Dict:
        """Execute the TDD workflow guidance"""
        logger.debug("Starting TDD workflow run")
        print(f"🚀 Running {self.__class__.__name__}...")
        print(f"📁 Target: {self.target_path}")
        print(f"🔄 Phase: {self.current_phase.value.upper()}")

        try:
            self.validate_target()
            self.analyze_phase()
            self.generate_checklist()
            self.generate_guidance()
            self.calculate_metrics()
            self.suggest_next_steps()
            self.generate_report()

            print("✅ Completed successfully!")
            return self.results

        except Exception as e:
            logger.error(f"Error during TDD workflow: {e}")
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

    def analyze_phase(self):
        """Analyze current TDD phase requirements"""
        phase_info = {
            'name': self.current_phase.value,
            'description': self.PHASE_DESCRIPTIONS[self.current_phase],
            'color': self._get_phase_color(),
        }
        self.results['phase_info'] = phase_info

        if self.verbose:
            print(f"✓ Phase: {phase_info['description']}")

    def _get_phase_color(self) -> str:
        """Get color associated with phase"""
        colors = {
            TDDPhase.RED: '🔴',
            TDDPhase.GREEN: '🟢',
            TDDPhase.REFACTOR: '🔵',
            TDDPhase.COMPLETE: '✅',
        }
        return colors.get(self.current_phase, '⚪')

    def generate_checklist(self):
        """Generate phase-specific checklist"""
        if self.current_phase in self.PHASE_CHECKLIST:
            self.results['checklist'] = [
                {'item': item, 'checked': False}
                for item in self.PHASE_CHECKLIST[self.current_phase]
            ]

    def generate_guidance(self):
        """Generate phase-specific guidance and tips"""
        guidance = []

        if self.current_phase == TDDPhase.RED:
            guidance = [
                {
                    'title': 'Write the Test First',
                    'description': 'Start by writing a test that describes what you want to achieve',
                    'example': '''
// Jest example
describe('EmailValidator', () => {
  it('should return true for valid email format', () => {
    expect(validateEmail('user@example.com')).toBe(true);
  });
});
''',
                },
                {
                    'title': 'Test Should Fail Initially',
                    'description': 'Run the test and verify it fails for the RIGHT reason',
                    'tip': 'The error should be about missing functionality, not syntax',
                },
                {
                    'title': 'One Behavior Per Test',
                    'description': 'Each test should verify exactly one behavior',
                    'anti_pattern': 'Avoid testing multiple scenarios in a single test',
                },
            ]
        elif self.current_phase == TDDPhase.GREEN:
            guidance = [
                {
                    'title': 'Write Minimal Code',
                    'description': 'Write just enough code to make the test pass',
                    'example': '''
// Minimal implementation
function validateEmail(email) {
  return email.includes('@');  // Simple first pass
}
''',
                },
                {
                    'title': 'Avoid Premature Optimization',
                    'description': 'Focus on making the test pass, not perfect code',
                    'tip': 'You can improve the code in the REFACTOR phase',
                },
                {
                    'title': 'Run Tests Frequently',
                    'description': 'Run tests after each small change',
                    'command': 'npm test -- --watch (Jest) or pytest -f (pytest)',
                },
            ]
        elif self.current_phase == TDDPhase.REFACTOR:
            guidance = [
                {
                    'title': 'Keep Tests Green',
                    'description': 'Run tests after every refactoring step',
                    'tip': 'If tests fail, revert immediately',
                },
                {
                    'title': 'Small Steps',
                    'description': 'Make small, incremental improvements',
                    'examples': [
                        'Extract method',
                        'Rename variable',
                        'Remove duplication',
                        'Simplify conditionals',
                    ],
                },
                {
                    'title': 'No Behavior Changes',
                    'description': 'Refactoring changes structure, not behavior',
                    'anti_pattern': 'Adding new features during refactor phase',
                },
            ]

        self.results['guidance'] = guidance

    def calculate_metrics(self):
        """Calculate TDD cycle metrics"""
        metrics = {
            'cycle_id': self.results['cycle_id'],
            'phase': self.current_phase.value,
            'timestamp': datetime.now().isoformat(),
            'checklist_items': len(self.results['checklist']),
            'guidance_items': len(self.results['guidance']),
        }

        # Try to detect test file stats
        if self.test_file:
            test_path = Path(self.test_file)
            if test_path.exists():
                content = test_path.read_text()
                metrics['test_file'] = str(test_path)
                metrics['test_lines'] = len(content.splitlines())
                metrics['test_count'] = content.count('it(') + content.count('test(') + content.count('def test_')

        self.results['metrics'] = metrics

    def suggest_next_steps(self):
        """Suggest next steps based on current phase"""
        next_steps = []

        if self.current_phase == TDDPhase.RED:
            next_steps = [
                'Write a failing test that describes the behavior',
                'Run the test and verify it fails',
                f'Move to GREEN phase: python tdd_workflow.py --input {self.target_path} --phase green',
            ]
        elif self.current_phase == TDDPhase.GREEN:
            next_steps = [
                'Write minimal code to make the test pass',
                'Run tests and verify all pass',
                f'Move to REFACTOR phase: python tdd_workflow.py --input {self.target_path} --phase refactor',
            ]
        elif self.current_phase == TDDPhase.REFACTOR:
            next_steps = [
                'Improve code quality (extract, rename, simplify)',
                'Run tests after each change',
                f'Start new cycle: python tdd_workflow.py --input {self.target_path} --phase red',
            ]

        self.results['next_steps'] = next_steps

    def generate_report(self):
        """Generate and display the TDD workflow report"""
        phase_color = self._get_phase_color()

        print("\n" + "=" * 60)
        print(f"TDD WORKFLOW - {phase_color} {self.current_phase.value.upper()} PHASE")
        print("=" * 60)

        print(f"\n📋 {self.PHASE_DESCRIPTIONS[self.current_phase]}")

        # Checklist
        if self.results['checklist']:
            print(f"\n✓ Phase Checklist:")
            for item in self.results['checklist']:
                print(f"   [ ] {item['item']}")

        # Guidance
        if self.results['guidance']:
            print(f"\n💡 Guidance:")
            for g in self.results['guidance']:
                print(f"\n   {g['title']}")
                print(f"   {g['description']}")
                if 'tip' in g:
                    print(f"   💡 Tip: {g['tip']}")

        # Next steps
        if self.results['next_steps']:
            print(f"\n➡️  Next Steps:")
            for i, step in enumerate(self.results['next_steps'], 1):
                print(f"   {i}. {step}")

        # Metrics
        if self.results['metrics']:
            print(f"\n📊 Metrics:")
            print(f"   Cycle ID: {self.results['metrics']['cycle_id']}")
            if 'test_count' in self.results['metrics']:
                print(f"   Tests: {self.results['metrics']['test_count']}")

        print("\n" + "=" * 60)


def format_csv_output(results: Dict) -> str:
    """Format TDD workflow results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['field', 'value'])
    writer.writerow(['cycle_id', results.get('cycle_id', '')])
    writer.writerow(['phase', results.get('phase', '')])
    writer.writerow(['status', results.get('status', '')])

    if results.get('metrics'):
        for k, v in results['metrics'].items():
            writer.writerow([f'metric_{k}', str(v)])

    return output.getvalue()


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="TDDWorkflow - Red-Green-Refactor cycle orchestration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input /path/to/project --phase red
  %(prog)s --input . --phase green --test-file tests/test_feature.py
  %(prog)s --input ./src --phase refactor --output json
  %(prog)s --input . --phase red -v

TDD Phases:
  red      - Write failing test
  green    - Make test pass with minimal code
  refactor - Improve code while keeping tests green

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Project root path'
    )

    parser.add_argument(
        '--phase', '-p',
        choices=['red', 'green', 'refactor'],
        default='red',
        help='Current TDD phase (default: red)'
    )

    parser.add_argument(
        '--test-file', '-t',
        help='Path to test file being worked on'
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

    workflow = TDDWorkflow(
        args.target,
        verbose=args.verbose,
        phase=args.phase,
        test_file=args.test_file
    )

    results = workflow.run()

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
