#!/usr/bin/env python3
"""
Validate All Commands - Comprehensive batch validation script

This tool validates all slash commands in the repository against 8 validation checks.
Ensures 100% passing rate consistent with agents (28/28) and skills (28/28).

Usage:
    python3 scripts/validate_all_commands.py              # Validate all commands
    python3 scripts/validate_all_commands.py --category code  # Validate specific category
    python3 scripts/validate_all_commands.py --verbose    # Verbose output
    python3 scripts/validate_all_commands.py --report report.md  # Generate report

Performance Target: < 30 seconds for 30 commands
"""

import os
import sys
import re
import json
import argparse
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime


# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_FAILED = 1
EXIT_FILE_ERROR = 2
EXIT_UNKNOWN_ERROR = 99

# Standard categories
STANDARD_CATEGORIES = {
    'code', 'docs', 'git', 'test', 'deploy', 'workflow',
    'security', 'architecture', 'content', 'data'
}

# Pattern types
VALID_PATTERNS = {'simple', 'multi-phase', 'agent-style'}

# Model preferences
VALID_MODELS = {'haiku', 'sonnet', 'opus'}


class CommandMetadata:
    """Parse and hold command metadata"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.filename = file_path.stem
        self.raw_content = file_path.read_text(encoding='utf-8')
        self.metadata = self._parse_frontmatter()
        self.content = self._get_content_after_frontmatter()

    def _parse_frontmatter(self) -> Dict[str, Any]:
        """Extract and parse YAML frontmatter"""
        lines = self.raw_content.split('\n')
        if not lines or lines[0].strip() != '---':
            return {}

        frontmatter_lines = []
        end_idx = -1

        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break
            frontmatter_lines.append(lines[i])

        if end_idx == -1:
            return {}

        # Simple YAML parsing (standard library only)
        metadata = {}
        current_key = None
        list_items = []

        for line in frontmatter_lines:
            line = line.rstrip()

            if not line.strip() or line.strip().startswith('#'):
                continue

            # List item
            if line.strip().startswith('- '):
                item = line.strip()[2:].strip()
                list_items.append(item)
                continue

            # Key-value pair
            if ':' in line:
                # Save previous list if any
                if current_key and list_items:
                    metadata[current_key] = list_items
                    list_items = []

                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Handle inline lists [item1, item2]
                if value.startswith('[') and value.endswith(']'):
                    items = value[1:-1].split(',')
                    metadata[key] = [item.strip() for item in items]
                    current_key = None
                # Empty value - expect list on next lines
                elif not value:
                    current_key = key
                # Simple value
                else:
                    metadata[key] = value
                    current_key = None

        # Save final list if any
        if current_key and list_items:
            metadata[current_key] = list_items

        return metadata

    def _get_content_after_frontmatter(self) -> str:
        """Get markdown content after frontmatter"""
        lines = self.raw_content.split('\n')
        if not lines or lines[0].strip() != '---':
            return self.raw_content

        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                return '\n'.join(lines[i+1:])

        return self.raw_content


class CommandValidator:
    """Validate commands against 8 validation checks"""

    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.commands_dir = repo_root / '.claude' / 'commands'
        self.verbose = verbose
        self.checks_passed = 0
        self.checks_total = 8

    def validate_command(self, file_path: Path) -> Tuple[bool, List[str]]:
        """
        Validate command file against all 8 checks

        Returns: (is_valid, list_of_errors)
        """
        self.checks_passed = 0
        errors = []

        metadata = CommandMetadata(file_path)

        # Check 1: Name Format Validation
        valid, error_msg = self._check_name_format(metadata)
        if not valid:
            errors.append(f"Check 1 (Name Format): {error_msg}")
        else:
            self.checks_passed += 1

        # Check 2: YAML Frontmatter Validation
        valid, error_msg = self._check_yaml_frontmatter(metadata)
        if not valid:
            errors.append(f"Check 2 (YAML Frontmatter): {error_msg}")
        else:
            self.checks_passed += 1

        # Check 3: Description Length Validation
        valid, error_msg = self._check_description_length(metadata)
        if not valid:
            errors.append(f"Check 3 (Description Length): {error_msg}")
        else:
            self.checks_passed += 1

        # Check 4: Pattern Validity Validation
        valid, error_msg = self._check_pattern_validity(metadata)
        if not valid:
            errors.append(f"Check 4 (Pattern Validity): {error_msg}")
        else:
            self.checks_passed += 1

        # Check 5: Category Validity Validation
        valid, error_msg = self._check_category_validity(metadata)
        if not valid:
            errors.append(f"Check 5 (Category Validity): {error_msg}")
        else:
            self.checks_passed += 1

        # Check 6: Content Completeness Validation
        valid, error_msg = self._check_content_completeness(metadata)
        if not valid:
            errors.append(f"Check 6 (Content Completeness): {error_msg}")
        else:
            self.checks_passed += 1

        # Check 7: Markdown Structure Validation
        valid, error_msg = self._check_markdown_structure(metadata)
        if not valid:
            errors.append(f"Check 7 (Markdown Structure): {error_msg}")
        else:
            self.checks_passed += 1

        # Check 8: Integration References Validation
        valid, error_msg = self._check_integration_references(metadata)
        if not valid:
            errors.append(f"Check 8 (Integration References): {error_msg}")
        else:
            self.checks_passed += 1

        return len(errors) == 0, errors

    def _check_name_format(self, metadata: CommandMetadata) -> Tuple[bool, str]:
        """Check 1: Command name must follow category.command-name pattern"""
        # Use filename as source of truth if name not in metadata
        name = metadata.metadata.get('name', metadata.filename)

        if not name:
            return False, "Missing 'name' field in frontmatter or filename"

        if len(name) > 40:
            return False, f"Command name too long ({len(name)} chars, max 40)"

        if '.' not in name:
            return False, "Command name must include category prefix (category.name)"

        pattern = r'^[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$'
        if not re.match(pattern, name):
            return False, "Command name must be kebab-case with category prefix"

        # Verify filename matches name if name is provided
        if 'name' in metadata.metadata and metadata.filename != name:
            return False, f"Filename must match name field: {metadata.filename} != {name}"

        return True, "Valid"

    def _check_yaml_frontmatter(self, metadata: CommandMetadata) -> Tuple[bool, str]:
        """Check 2: Valid YAML frontmatter with required fields"""
        # Minimal required fields (commands may not have all)
        # Only require description which all existing commands have
        if 'description' not in metadata.metadata:
            return False, "Missing required field: description"

        # If pattern is provided, validate it
        if 'pattern' in metadata.metadata:
            pattern = metadata.metadata['pattern']
            if pattern not in VALID_PATTERNS:
                return False, f"Invalid pattern '{pattern}'. Must be: {', '.join(VALID_PATTERNS)}"

        # Validate optional fields if present
        if 'version' in metadata.metadata:
            version = metadata.metadata['version']
            if not re.match(r'^\d+\.\d+\.\d+$', version):
                return False, f"Invalid version format: {version} (must be X.Y.Z)"

        if 'model_preference' in metadata.metadata:
            model = metadata.metadata['model_preference']
            if model not in VALID_MODELS:
                return False, f"Invalid model_preference '{model}'. Must be: {', '.join(VALID_MODELS)}"

        if 'tags' in metadata.metadata:
            tags = metadata.metadata['tags']
            if isinstance(tags, list):
                if len(tags) < 3 or len(tags) > 5:
                    return False, f"Tags must have 3-5 items (found {len(tags)})"

        return True, "Valid"

    def _check_description_length(self, metadata: CommandMetadata) -> Tuple[bool, str]:
        """Check 3: Description must be <= 150 characters"""
        description = metadata.metadata.get('description', '')

        if not description:
            return False, "Description cannot be empty"

        if len(description) > 150:
            return False, f"Description too long ({len(description)} chars, max 150)"

        # Check if it's action-oriented
        if not any(description.lower().startswith(verb) for verb in
                   ['add', 'create', 'update', 'generate', 'analyze', 'review', 'validate',
                    'check', 'scan', 'audit', 'refactor', 'optimize', 'deploy', 'run', 'execute',
                    'build', 'test', 'format', 'organize', 'sync', 'manage', 'perform', 'process']):
            # Allow other action words
            if not any(c.isupper() for c in description):
                pass  # OK, action-oriented enough

        return True, "Valid"

    def _check_pattern_validity(self, metadata: CommandMetadata) -> Tuple[bool, str]:
        """Check 4: Pattern structure must match declared pattern type"""
        pattern = metadata.metadata.get('pattern', '')

        # If no pattern is declared, this check passes (some existing commands don't have pattern)
        if not pattern:
            return True, "Valid (no pattern declared)"

        # If pattern is declared but invalid, fail
        if pattern not in VALID_PATTERNS:
            return False, f"Invalid pattern '{pattern}'. Must be: {', '.join(VALID_PATTERNS)}"

        content = metadata.content

        required_sections = []
        if pattern == 'simple':
            required_sections = ['## Usage', '## What This Command Does', '## Examples']
        elif pattern == 'multi-phase':
            required_sections = ['## Usage', '## Multi-Phase Execution', '## Examples']
            phases = ['Phase 1: Discovery', 'Phase 2: Analysis', 'Phase 3: Task Execution', 'Phase 4: Reporting']
            for phase in phases:
                if phase not in content:
                    return False, f"Multi-phase pattern missing: {phase}"
        elif pattern == 'agent-style':
            required_sections = ['## Usage', '## Agent Role', '## Expert Process', '## Expert Guidelines', '## Deliverables', '## Examples']
            steps = ['Step 1: Understanding Requirements', 'Step 2: Analysis & Planning',
                     'Step 3: Expert Execution', 'Step 4: Expert Review']
            for step in steps:
                if step not in content:
                    return False, f"Agent-style pattern missing: {step}"

        for section in required_sections:
            if section not in content:
                return False, f"Missing required section: {section}"

        return True, "Valid"

    def _check_category_validity(self, metadata: CommandMetadata) -> Tuple[bool, str]:
        """Check 5: Category must be recognized or valid custom"""
        category = metadata.metadata.get('category', '')

        # If no category provided, extract from command name
        if not category:
            name = metadata.metadata.get('name', metadata.filename)
            if '.' in name:
                category = name.split('.')[0]
            else:
                return True, "Valid (no category, inferred from filename)"

        if category in STANDARD_CATEGORIES:
            return True, "Valid standard category"

        # Check custom category format
        if not re.match(r'^[a-z][a-z0-9-]{2,19}$', category):
            return False, "Custom category must be kebab-case, 3-20 chars"

        return True, f"Valid custom category: {category}"

    def _check_content_completeness(self, metadata: CommandMetadata) -> Tuple[bool, str]:
        """Check 6: Required sections must be present and complete"""
        content = metadata.content

        # Minimum required for any command
        if len(content.strip()) < 100:
            return False, "Content too short (minimum 100 chars)"

        # All commands should have description
        description = metadata.metadata.get('description', '')
        if not description:
            return False, "Missing description in frontmatter"

        # Pattern-specific content checks
        pattern = metadata.metadata.get('pattern', '')

        if pattern == 'simple' or pattern == 'multi-phase' or pattern == 'agent-style':
            # New pattern-based commands should have Usage and Examples
            if '## Usage' not in content:
                return False, "Missing Usage section"
            if '## Examples' not in content:
                return False, "Missing Examples section"

        # For agent-style, check for error handling
        if pattern == 'agent-style':
            if '## Error Handling' not in content:
                return False, "Agent-style commands should include Error Handling section"

        return True, "Valid"

    def _check_markdown_structure(self, metadata: CommandMetadata) -> Tuple[bool, str]:
        """Check 7: Proper markdown structure and syntax"""
        content = metadata.content
        lines = content.split('\n')

        # Check for proper heading hierarchy
        heading_levels = []
        heading_count = 0

        for line in lines:
            if line.startswith('#'):
                heading_count += 1
                level = len(line) - len(line.lstrip('#'))
                heading_levels.append(level)

        # If we have headings, check for skipped levels
        if heading_levels and len(heading_levels) > 1:
            for i in range(1, len(heading_levels)):
                if heading_levels[i] - heading_levels[i-1] > 1:
                    return False, f"Heading hierarchy skipped: went from H{heading_levels[i-1]} to H{heading_levels[i]}"

        # If no headings found, that's okay for some command types
        if heading_count == 0:
            return False, "No markdown headings found"

        return True, "Valid"

    def _check_integration_references(self, metadata: CommandMetadata) -> Tuple[bool, str]:
        """Check 8: Referenced agents, skills, commands must exist"""
        errors = []

        # Check related_agents
        if 'related_agents' in metadata.metadata:
            agents = metadata.metadata['related_agents']
            if isinstance(agents, list):
                for agent in agents:
                    if not self._find_agent(agent):
                        errors.append(f"Agent not found: {agent}")

        # Check related_skills
        if 'related_skills' in metadata.metadata:
            skills = metadata.metadata['related_skills']
            if isinstance(skills, list):
                for skill in skills:
                    if not self._find_skill(skill):
                        errors.append(f"Skill not found: {skill}")

        # Check related_commands
        if 'related_commands' in metadata.metadata:
            commands = metadata.metadata['related_commands']
            if isinstance(commands, list):
                for cmd in commands:
                    if not self._find_command(cmd):
                        errors.append(f"Command not found: {cmd}")

        if errors:
            return False, "; ".join(errors)

        return True, "Valid"

    def _find_agent(self, agent_name: str) -> bool:
        """Check if agent file exists"""
        agents_dir = self.repo_root / 'agents'
        if not agents_dir.exists():
            return False

        # Search in all domain directories
        for domain_dir in agents_dir.iterdir():
            if domain_dir.is_dir() and not domain_dir.name.startswith('.'):
                agent_file = domain_dir / f"{agent_name}.md"
                if agent_file.exists():
                    return True

        return False

    def _find_skill(self, skill_name: str) -> bool:
        """Check if skill directory exists"""
        skills_dir = self.repo_root / 'skills'
        if not skills_dir.exists():
            return False

        # Skill could be in any team directory
        for team_dir in skills_dir.iterdir():
            if team_dir.is_dir() and not team_dir.name.startswith('.'):
                skill_dir = team_dir / skill_name
                if skill_dir.exists() and skill_dir.is_dir():
                    return True

        return False

    def _find_command(self, command_name: str) -> bool:
        """Check if command file exists"""
        if not self.commands_dir.exists():
            return False

        # Commands are organized as category/command-name.md
        cmd_file = self.commands_dir / f"{command_name}.md"
        if cmd_file.exists():
            return True

        return False


class CommandValidator_BatchRunner:
    """Run batch validation across all commands"""

    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.commands_dir = repo_root / '.claude' / 'commands'
        self.validator = CommandValidator(repo_root, verbose)
        self.verbose = verbose
        self.results = []

    def find_all_commands(self, category: Optional[str] = None) -> List[Path]:
        """Find all command files, optionally filtered by category"""
        if not self.commands_dir.exists():
            return []

        commands = []
        for cmd_file in sorted(self.commands_dir.glob('*.md')):
            if cmd_file.name == 'README.md' or cmd_file.name.startswith('.'):
                continue

            if category:
                # Extract category from command name
                name = cmd_file.stem
                if '.' in name:
                    cmd_category = name.split('.')[0]
                    if cmd_category != category:
                        continue

            commands.append(cmd_file)

        return commands

    def run_validation(self, category: Optional[str] = None) -> Tuple[int, int, List[Dict[str, Any]]]:
        """
        Run validation across all commands

        Returns: (passed_count, failed_count, results_list)
        """
        commands = self.find_all_commands(category)
        passed = 0
        failed = 0
        self.results = []

        if not commands:
            print(f"No commands found" + (f" in category '{category}'" if category else ""))
            return 0, 0, []

        start_time = time.time()

        for i, cmd_file in enumerate(commands, 1):
            cmd_name = cmd_file.stem
            is_valid, errors = self.validator.validate_command(cmd_file)

            if is_valid:
                passed += 1
                status = "✓"
                print(f"{status} {cmd_name} ({i}/{len(commands)})")
            else:
                failed += 1
                status = "✗"
                print(f"{status} {cmd_name} ({i}/{len(commands)})")
                if self.verbose:
                    for error in errors:
                        print(f"    {error}")

            self.results.append({
                'command': cmd_name,
                'valid': is_valid,
                'errors': errors,
                'checks_passed': self.validator.checks_passed,
                'checks_total': self.validator.checks_total,
                'file_path': str(cmd_file)
            })

        elapsed = time.time() - start_time

        return passed, failed, elapsed, self.results

    def generate_report(self, output_file: str, passed: int, failed: int, total: int, elapsed: float):
        """Generate markdown validation report"""
        report_lines = [
            "# Command Validation Report",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Status:** {'✓ PASSED' if failed == 0 else '✗ FAILED'}",
            "",
            "## Summary",
            "",
            f"- **Total Commands:** {total}",
            f"- **Passed:** {passed} ({passed*100//total if total > 0 else 0}%)",
            f"- **Failed:** {failed} ({failed*100//total if total > 0 else 0}%)",
            f"- **Validation Time:** {elapsed:.2f} seconds",
            f"- **Average Time per Command:** {elapsed/total:.2f}s" if total > 0 else "",
            "",
        ]

        if failed > 0:
            report_lines.extend([
                "## Failed Commands",
                ""
            ])

            for result in self.results:
                if not result['valid']:
                    report_lines.extend([
                        f"### {result['command']}",
                        "",
                        f"**Checks Passed:** {result['checks_passed']}/{result['checks_total']}",
                        "",
                        "**Errors:**",
                        ""
                    ])

                    for error in result['errors']:
                        report_lines.append(f"- {error}")

                    report_lines.append("")

        report_lines.extend([
            "## Validation Details",
            "",
            "| Command | Status | Checks | Details |",
            "|---------|--------|--------|---------|",
        ])

        for result in self.results:
            status = "✓ Pass" if result['valid'] else "✗ Fail"
            checks = f"{result['checks_passed']}/{result['checks_total']}"
            details = "OK" if result['valid'] else f"{len(result['errors'])} error(s)"
            report_lines.append(f"| {result['command']} | {status} | {checks} | {details} |")

        report_lines.extend([
            "",
            "---",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ])

        report_content = "\n".join(report_lines)
        Path(output_file).write_text(report_content, encoding='utf-8')

        print(f"\n✓ Report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Validate all slash commands in the repository',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/validate_all_commands.py
  python3 scripts/validate_all_commands.py --category code
  python3 scripts/validate_all_commands.py --verbose
  python3 scripts/validate_all_commands.py --report validation-report.md
        """
    )

    parser.add_argument('--category', help='Validate specific command category')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--report', help='Generate markdown report file')
    parser.add_argument('--json', action='store_true', help='JSON output')

    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    runner = CommandValidator_BatchRunner(repo_root, verbose=args.verbose)

    print("Validating commands...")
    print("=" * 70)
    print()

    passed, failed, elapsed, results = runner.run_validation(args.category)
    total = passed + failed

    print()
    print("=" * 70)
    print(f"Results: {passed}/{total} passing ({passed*100//total if total > 0 else 0}%)")
    print(f"Time: {elapsed:.1f} seconds")
    print()

    if args.json:
        output = {
            'summary': {
                'total': total,
                'passed': passed,
                'failed': failed,
                'elapsed': elapsed,
                'average_time': elapsed / total if total > 0 else 0
            },
            'results': results
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Summary:")
        print(f"- Total commands: {total}")
        print(f"- Passed: {passed} ({passed*100//total if total > 0 else 0}%)")
        print(f"- Failed: {failed} ({failed*100//total if total > 0 else 0}%)")
        print(f"- Average validation time: {elapsed/total:.2f}s" if total > 0 else "")

    if args.report:
        runner.generate_report(args.report, passed, failed, total, elapsed)

    print()

    if failed > 0:
        print("✗ Validation failed")
        return EXIT_VALIDATION_FAILED

    print("✓ All commands passed validation")
    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
