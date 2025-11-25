#!/usr/bin/env python3
"""
Skill Builder - Interactive CLI for creating skill packages

This tool automates skill creation with comprehensive validation,
directory scaffolding, and template population.

Usage:
    python skill_builder.py                        # Interactive mode
    python skill_builder.py --config config.yaml   # Config file mode
    python skill_builder.py --validate path/       # Validation mode
    python skill_builder.py --help                 # Show help

ARCHITECTURE NOTE - Single-File Design:
    This script is intentionally monolithic (1,621 lines) for portability.
    Users can extract this single file and run it anywhere with Python 3.8+.
    This aligns with the repository's zero-dependency, portable-skills philosophy.

    Code is organized into logical sections for maintainability:

    SECTION 1: Configuration & Constants (Lines 15-38)
        - Exit codes, imports, global configuration

    SECTION 2: YAML Parsing Utilities (Lines 40-139)
        - simple_yaml_parse() - Standard library YAML parser
        - Handles basic YAML without external dependencies

    SECTION 3: Team & Domain Management (Lines 140-237)
        - SkillTeamManager class
        - Dynamic team discovery, validation, domain handling

    SECTION 4: Validation Logic (Lines 238-638)
        - SkillValidator class
        - 12 validation checks for skill structure

    SECTION 5: Template Management (Lines 639-792)
        - SkillTemplateLoader class
        - Template file loading and generation

    SECTION 6: Directory Scaffolding (Lines 919-1075)
        - DirectoryScaffolder class
        - Creates skill directory structure

    SECTION 7: Core Skill Builder (Lines 1076-1545)
        - SkillBuilder class
        - Main orchestration logic

    SECTION 8: CLI Entry Point (Lines 1546-1621)
        - main() function
        - Argument parsing and mode selection
"""

# ============================================================================
# SECTION 1: CONFIGURATION & CONSTANTS
# ============================================================================
# Import statements, exit codes, and global configuration

import os
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Try to import PyYAML, provide fallback if not available
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    # Use simple YAML parser fallback (no external dependencies)


# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_FAILED = 1
EXIT_FILE_ERROR = 2
EXIT_CONFIG_ERROR = 3
EXIT_UNKNOWN_ERROR = 99


# ============================================================================
# SECTION 2: YAML PARSING UTILITIES
# ============================================================================
# Standard library YAML parser for skill frontmatter (zero dependencies)

def simple_yaml_parse(yaml_str: str) -> Dict:
    """
    Simple YAML parser for skill frontmatter (standard library only)

    Handles basic key-value pairs, lists, and one level of nesting.
    Supports nested metadata objects.
    """
    result = {}
    current_key = None
    list_items = []
    in_nested = False
    nested_key = None
    nested_dict = {}

    for line in yaml_str.strip().split('\n'):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())

        if not stripped or stripped.startswith('#'):
            continue

        # List item
        if stripped.startswith('- '):
            item = stripped[2:].strip()
            list_items.append(item)
            continue

        # Key-value pair
        if ':' in stripped:
            # Save previous list if any
            if current_key and list_items:
                if in_nested:
                    nested_dict[current_key] = list_items
                else:
                    result[current_key] = list_items
                list_items = []

            key, value = stripped.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Nested object (indented with 2+ spaces)
            if indent >= 2:
                in_nested = True
                # Handle inline lists [item1, item2]
                if value.startswith('[') and value.endswith(']'):
                    if value == '[]':
                        nested_dict[key] = []
                    else:
                        items = value[1:-1].split(',')
                        nested_dict[key] = [item.strip() for item in items]
                    current_key = None
                # Empty value - expect list on next lines
                elif not value:
                    current_key = key
                # Simple value
                else:
                    nested_dict[key] = value
                    current_key = None
            # Top-level key
            else:
                # Save previous nested dict if any
                if in_nested and nested_key:
                    result[nested_key] = nested_dict
                    nested_dict = {}

                in_nested = False

                # Handle inline lists [item1, item2]
                if value.startswith('[') and value.endswith(']'):
                    if value == '[]':
                        result[key] = []
                    else:
                        items = value[1:-1].split(',')
                        result[key] = [item.strip() for item in items]
                    current_key = None
                # Empty value - could be nested object or list
                elif not value:
                    current_key = key
                    nested_key = key
                    in_nested = False
                # Simple value
                else:
                    result[key] = value
                    current_key = None

    # Save final list if any
    if current_key and list_items:
        if in_nested:
            nested_dict[current_key] = list_items
        else:
            result[current_key] = list_items

    # Save final nested dict if any
    if in_nested and nested_key:
        result[nested_key] = nested_dict

    return result


def ensure_session_tracking() -> Optional[str]:
    """
    Check if user is in an active session, offer to create one

    Returns:
        Session ID if active session exists, None otherwise
    """
    repo_root = Path(__file__).parent.parent
    current_session_file = repo_root / "output" / ".current-session"

    # Check if there's an active session
    if current_session_file.exists():
        try:
            session_id = current_session_file.read_text().strip()
            if session_id:
                return session_id
        except Exception:
            pass

    # No active session - offer to create one
    print("\n" + "="*60)
    print("SESSION TRACKING")
    print("="*60)
    print("No active session detected.")
    print("\nSession tracking helps:")
    print("  • Attribute work to specific initiatives")
    print("  • Preserve context for collaboration")
    print("  • Track decisions and changes over time")
    print("\nCreate a new session? (y/n): ", end="")

    try:
        response = input().strip().lower()
        if response in ('y', 'yes'):
            print("\nSession ID (e.g., 'feature-name' or press Enter to skip): ", end="")
            session_desc = input().strip()

            if session_desc:
                user = os.getenv('USER', 'unknown')
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                session_id = f"{timestamp}_{session_desc}"
                session_path = repo_root / "output" / "sessions" / user / session_id

                # Create session directory
                session_path.mkdir(parents=True, exist_ok=True)

                # Update current session pointer
                current_session_file.parent.mkdir(parents=True, exist_ok=True)
                current_session_file.write_text(f"{user}/{session_id}")

                print(f"\n✓ Created session: {session_id}")
                print(f"  Location: {session_path}")
                print("\nContinuing with skill creation...\n")
                return session_id
            else:
                print("\nSkipping session creation. Continuing with skill creation...\n")
        else:
            print("\nSkipping session creation. Continuing with skill creation...\n")
    except (KeyboardInterrupt, EOFError):
        print("\n\nSkipping session creation...\n")

    return None


# ============================================================================
# SECTION 3: TEAM & DOMAIN MANAGEMENT
# ============================================================================
# Dynamic team discovery, validation, and domain handling

class SkillTeamManager:
    """Manage skill teams dynamically"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.skills_dir = repo_root / "skills"

    def get_existing_teams(self) -> List[str]:
        """Discover existing skill teams from file system"""
        if not self.skills_dir.exists():
            return []
        return [d.name for d in self.skills_dir.iterdir()
                if d.is_dir() and not d.name.startswith('.')]

    def validate_team_format(self, team_name: str) -> Tuple[bool, str]:
        """Validate team name format (kebab-case, typically ends with -team)"""
        # Remove '-team' suffix for validation
        base_name = team_name.replace('-team', '')

        pattern = r'^[a-z][a-z0-9-]*$'
        if not re.match(pattern, base_name):
            return False, f"Team name must be lowercase kebab-case: {team_name}"
        if len(team_name) < 3:
            return False, f"Team name too short (min 3 chars): {team_name}"
        if len(team_name) > 40:
            return False, f"Team name too long (max 40 chars): {team_name}"
        if '--' in team_name:
            return False, f"Team name cannot have consecutive hyphens: {team_name}"
        return True, "Valid team format"

    def create_new_team(self, team_name: str) -> None:
        """Create new skill team directory with README and CLAUDE.md"""
        team_path = self.skills_dir / team_name
        team_path.mkdir(parents=True, exist_ok=True)

        # Create README.md
        readme_content = f"""# {team_name.replace('-', ' ').title()}

Skills for the {team_name.replace('-team', '')} domain.

## Overview

This skill team provides tools, frameworks, and workflows for {team_name.replace('-team', '')} functions.

## Skills

<!-- Skills will be listed here automatically -->

## Quick Start

[Documentation to be added]

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Skill Count:** 0
"""
        (team_path / "README.md").write_text(readme_content)

        # Create CLAUDE.md
        claude_md_content = f"""# {team_name.replace('-', ' ').title()} - Domain Guide

## Purpose

This directory contains skills for the {team_name.replace('-team', '')} domain.

## Available Skills

[Skills will be documented here]

## Development Guidelines

[Guidelines to be added]

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""
        (team_path / "CLAUDE.md").write_text(claude_md_content)

        print(f"✅ Created: {team_path}/")
        print(f"✅ Created: {team_path}/README.md")
        print(f"✅ Created: {team_path}/CLAUDE.md")

    def map_domain_to_team(self, domain: str) -> str:
        """Map domain to skill team (default: domain-team)"""
        # Known exceptions
        DOMAIN_EXCEPTIONS = {
            'c-level': 'c-level-advisor',
        }

        if domain in DOMAIN_EXCEPTIONS:
            return DOMAIN_EXCEPTIONS[domain]

        # Default pattern: append '-team'
        return f"{domain}-team"


# ============================================================================
# SECTION 4: VALIDATION LOGIC
# ============================================================================
# Comprehensive validation checks for skill structure and metadata

class SkillValidator:
    """Validation logic for skill packages"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def validate_name(self, name: str) -> Tuple[bool, str]:
        """Validate skill name format (kebab-case, no cs- prefix)"""
        if name.startswith('cs-'):
            return False, "Skill names must NOT start with 'cs-' (reserved for agents)"

        if not re.match(r'^[a-z][a-z0-9-]+$', name):
            return False, "Skill name must be kebab-case (lowercase, hyphens only)"

        if len(name) < 3:
            return False, f"Skill name too short (min 3 chars): {name}"

        if len(name) > 50:
            return False, f"Skill name too long (max 50 chars): {name}"

        if '--' in name:
            return False, "Skill name cannot have consecutive hyphens"

        if name.endswith('-'):
            return False, "Skill name cannot end with hyphen"

        return True, "Valid"

    def validate_directory_structure(self, skill_path: Path) -> Tuple[bool, str]:
        """Validate skill directory structure"""
        if not skill_path.exists():
            return False, f"Skill directory does not exist: {skill_path}"

        required_dirs = ['scripts', 'references', 'assets']
        missing = []
        for dir_name in required_dirs:
            if not (skill_path / dir_name).exists():
                missing.append(dir_name)

        if missing:
            return False, f"Missing directories: {', '.join(missing)}"

        return True, "Valid structure"

    def validate_skill_md(self, skill_path: Path) -> Tuple[bool, str]:
        """Validate SKILL.md completeness"""
        skill_md_path = skill_path / "SKILL.md"

        if not skill_md_path.exists():
            return False, "SKILL.md not found"

        try:
            content = skill_md_path.read_text()
        except Exception as e:
            return False, f"Cannot read SKILL.md: {e}"

        # Check YAML frontmatter
        if not content.startswith('---'):
            return False, "Missing YAML frontmatter"

        # Check required sections
        required_sections = [
            '## Overview',
            '## Core Capabilities',
            '## Quick Start',
            '## Key Workflows',
            '## Python Tools',
        ]

        missing = []
        for section in required_sections:
            if section not in content:
                missing.append(section)

        if missing:
            return False, f"Missing sections: {', '.join(missing)}"

        return True, "Valid SKILL.md"

    def validate_python_tools(self, scripts_dir: Path) -> Tuple[bool, str]:
        """Validate Python tools follow standards"""
        if not scripts_dir.exists():
            return False, "scripts/ directory not found"

        py_files = list(scripts_dir.glob("*.py"))

        if len(py_files) == 0:
            return False, "No Python tools found in scripts/"

        errors = []
        for py_file in py_files:
            # Check executable permission
            if not os.access(py_file, os.X_OK):
                errors.append(f"{py_file.name}: not executable")

            # Check for --help support (basic check for argparse)
            try:
                content = py_file.read_text()
                if 'argparse' not in content:
                    errors.append(f"{py_file.name}: missing argparse (no --help)")
            except Exception as e:
                errors.append(f"{py_file.name}: cannot read file")

        if errors:
            return False, "; ".join(errors)

        return True, f"Valid ({len(py_files)} tools)"

    def validate_reference_guides(self, references_dir: Path) -> Tuple[bool, str]:
        """Validate reference guides present"""
        if not references_dir.exists():
            return False, "references/ directory not found"

        md_files = list(references_dir.glob("*.md"))

        # Allow empty references directory (optional)
        if len(md_files) == 0:
            return True, "No references (optional)"

        # Check that files have content
        empty_files = []
        for md_file in md_files:
            try:
                content = md_file.read_text().strip()
                if len(content) < 100:  # Minimum meaningful content
                    empty_files.append(md_file.name)
            except Exception:
                empty_files.append(md_file.name)

        if empty_files:
            return False, f"Empty or invalid files: {', '.join(empty_files)}"

        return True, f"Valid ({len(md_files)} guides)"

    def validate_metadata(self, skill_md_path: Path) -> Tuple[bool, str]:
        """Validate YAML metadata completeness"""
        try:
            content = skill_md_path.read_text()
        except Exception as e:
            return False, f"Cannot read SKILL.md: {e}"

        # Extract YAML frontmatter
        if not content.startswith('---'):
            return False, "No YAML frontmatter"

        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Malformed YAML frontmatter"

        yaml_str = parts[1]

        try:
            if YAML_AVAILABLE:
                metadata = yaml.safe_load(yaml_str)
            else:
                metadata = simple_yaml_parse(yaml_str)
        except Exception as e:
            return False, f"Invalid YAML syntax: {e}"

        # Required fields
        required = ['name', 'description', 'metadata']
        missing = []
        for field in required:
            if field not in metadata:
                missing.append(field)

        if missing:
            return False, f"Missing YAML fields: {', '.join(missing)}"

        # Validate name is kebab-case
        name = metadata.get('name', '')
        if not re.match(r'^[a-z][a-z0-9-]+$', name):
            return False, f"YAML name must be kebab-case: {name}"

        # Check nested metadata
        if isinstance(metadata.get('metadata'), dict):
            meta_required = ['version', 'updated', 'keywords']
            meta_missing = []
            for field in meta_required:
                if field not in metadata['metadata']:
                    meta_missing.append(field)

            if meta_missing:
                return False, f"Missing metadata fields: {', '.join(meta_missing)}"

        return True, "Valid metadata"

    def validate_documentation_quality(self, skill_path: Path) -> Tuple[bool, str]:
        """Validate documentation quality"""
        skill_md_path = skill_path / "SKILL.md"

        if not skill_md_path.exists():
            return False, "SKILL.md not found"

        try:
            content = skill_md_path.read_text()
        except Exception:
            return False, "Cannot read SKILL.md"

        # Check for Quick Start section with code examples
        if '## Quick Start' not in content:
            return False, "Missing Quick Start section"

        # Check for at least one workflow
        workflow_pattern = r'###\s+\d+\.\s+[A-Z]'
        workflows = re.findall(workflow_pattern, content)

        if len(workflows) < 1:
            return False, "No workflows documented"

        return True, f"Valid ({len(workflows)} workflows)"

    def validate_integration_points(self, skill_path: Path) -> Tuple[bool, str]:
        """Validate cross-references are valid"""
        skill_md_path = skill_path / "SKILL.md"

        if not skill_md_path.exists():
            return False, "SKILL.md not found"

        try:
            content = skill_md_path.read_text()
        except Exception:
            return False, "Cannot read SKILL.md"

        # Extract markdown links [text](path)
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, content)

        errors = []
        for text, path in links:
            # Skip external links
            if path.startswith('http://') or path.startswith('https://'):
                continue

            # Check internal references
            if path.startswith('references/') or path.startswith('assets/') or path.startswith('scripts/'):
                full_path = skill_path / path
                if not full_path.exists():
                    errors.append(f"Broken link: {path}")

        if errors:
            return False, "; ".join(errors[:3])  # Show first 3 errors

        return True, f"Valid ({len([l for l in links if not l[1].startswith('http')])} internal links)"

    def validate_cleanup(self, skill_path: Path) -> Tuple[bool, str]:
        """Validate skill directory is clean (no backup files or artifacts)"""
        if not skill_path.exists():
            return False, f"Skill directory not found: {skill_path}"

        artifacts = []

        # Check for backup files
        backup_patterns = ['*.backup', '*.bak', '*.old', '*~']
        for pattern in backup_patterns:
            found = list(skill_path.rglob(pattern))
            if found:
                artifacts.extend([f.name for f in found[:3]])  # Show first 3

        # Check for __pycache__ directories
        pycache_dirs = list(skill_path.rglob('__pycache__'))
        if pycache_dirs:
            artifacts.extend(['__pycache__/' for _ in pycache_dirs[:3]])

        # Check for .pyc files
        pyc_files = list(skill_path.rglob('*.pyc'))
        if pyc_files:
            artifacts.extend([f.name for f in pyc_files[:3]])

        # Check for internal summary/notes documents
        summary_patterns = ['*_SUMMARY.md', '*_NOTES.md', '*_INTERNAL.md']
        for pattern in summary_patterns:
            found = list(skill_path.rglob(pattern))
            if found:
                artifacts.extend([f.name for f in found[:3]])

        # Check for temporary files
        temp_patterns = ['*.tmp', '*.temp', '.DS_Store', 'Thumbs.db']
        for pattern in temp_patterns:
            found = list(skill_path.rglob(pattern))
            if found:
                artifacts.extend([f.name for f in found[:3]])

        if artifacts:
            return False, f"Found artifacts: {', '.join(artifacts[:5])}"

        return True, "Clean (no artifacts)"

    def run_all_checks(self, skill_path: Path, include_cleanup: bool = False) -> Dict:
        """Run all validation checks and return results

        Args:
            skill_path: Path to skill directory
            include_cleanup: Whether to include cleanup validation (default: False)
        """
        checks_total = 10 if include_cleanup else 9

        if not skill_path.exists():
            return {
                'status': 'failed',
                'checks_passed': 0,
                'checks_total': checks_total,
                'error': f"Skill directory not found: {skill_path}"
            }

        skill_name = skill_path.name
        checks = []

        # Check 1: Name format
        valid, msg = self.validate_name(skill_name)
        checks.append({
            'name': 'name_format',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 2: Directory structure
        valid, msg = self.validate_directory_structure(skill_path)
        checks.append({
            'name': 'directory_structure',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 3: SKILL.md completeness
        valid, msg = self.validate_skill_md(skill_path)
        checks.append({
            'name': 'skill_md_completeness',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 4: Python tools
        valid, msg = self.validate_python_tools(skill_path / 'scripts')
        checks.append({
            'name': 'python_tools',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 5: Reference guides
        valid, msg = self.validate_reference_guides(skill_path / 'references')
        checks.append({
            'name': 'reference_guides',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 6: Assets directory
        assets_dir = skill_path / 'assets'
        valid = assets_dir.exists()
        checks.append({
            'name': 'assets_directory',
            'status': 'passed' if valid else 'failed',
            'message': 'Valid' if valid else 'assets/ directory not found'
        })

        # Check 7: Metadata completeness
        valid, msg = self.validate_metadata(skill_path / "SKILL.md")
        checks.append({
            'name': 'metadata_completeness',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 8: Documentation quality
        valid, msg = self.validate_documentation_quality(skill_path)
        checks.append({
            'name': 'documentation_quality',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 9: Integration points
        valid, msg = self.validate_integration_points(skill_path)
        checks.append({
            'name': 'integration_points',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 10: File cleanliness (optional)
        if include_cleanup:
            valid, msg = self.validate_cleanup(skill_path)
            checks.append({
                'name': 'file_cleanliness',
                'status': 'passed' if valid else 'failed',
                'message': msg
            })

        checks_passed = sum(1 for c in checks if c['status'] == 'passed')

        return {
            'skill': skill_name,
            'status': 'passed' if checks_passed == len(checks) else 'failed',
            'checks_passed': checks_passed,
            'checks_total': len(checks),
            'checks': checks
        }


# ============================================================================
# SECTION 5: TEMPLATE MANAGEMENT
# ============================================================================
# Template file loading and content generation

class SkillTemplateLoader:
    """Load and populate skill templates"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.template_path = repo_root / "templates" / "skill-template.md"

    def load_template(self) -> str:
        """Load templates/skill-template.md"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")

        return self.template_path.read_text()

    def populate_template(self, template: str, config: Dict) -> str:
        """Replace placeholders in SKILL.md template"""
        # Replace YAML frontmatter
        yaml_frontmatter = f"""---
name: {config['name']}
description: {config['description']}
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: {config['domain'].replace('-team', '')}
  domain: {config['domain'].replace('-team', '')}
  updated: {datetime.now().strftime('%Y-%m-%d')}
  keywords:
{self._format_yaml_list(config.get('keywords', []), indent=4)}
  tech-stack:
{self._format_yaml_list(config.get('tech_stack', []), indent=4)}
  python-tools:
{self._format_yaml_list(config.get('tools', []), indent=4)}
---"""

        # Find and replace frontmatter
        parts = template.split('---', 2)
        if len(parts) >= 3:
            template = yaml_frontmatter + '\n' + parts[2]

        # Replace skill name (Title Case)
        skill_name_title = config['name'].replace('-', ' ').title()
        template = template.replace('# Skill Name', f"# {skill_name_title}")
        template = template.replace('skill-name', config['name'])
        template = template.replace('Skill Name', skill_name_title)

        # Replace domain
        template = template.replace('{domain-team}', config['domain'])
        template = template.replace('domain-category', config['domain'].replace('-team', ''))
        template = template.replace('domain-name', config['domain'].replace('-team', ''))

        # Replace placeholders
        template = template.replace('[One-line tagline describing core value proposition]',
                                  config['description'])
        template = template.replace('YYYY-MM-DD', datetime.now().strftime('%Y-%m-%d'))

        return template

    def _format_yaml_list(self, items: List[str], indent: int = 4) -> str:
        """Format list items as YAML"""
        if not items:
            return ' ' * indent + '- (to be added)'

        spaces = ' ' * indent
        return '\n'.join([f"{spaces}- {item}" for item in items])

    def generate_placeholder_tool(self, tool_name: str, config: Dict) -> str:
        """Generate placeholder Python tool from template"""
        # Convert tool name to class name (e.g., data_validator.py -> DataValidator)
        base_name = tool_name.replace('.py', '')
        class_name = ''.join(word.capitalize() for word in base_name.split('_'))
        tool_name_human = base_name.replace('_', ' ').title()

        template = f'''#!/usr/bin/env python3
"""
{tool_name_human}

Automated tool for {config['name']} tasks.

Part of {config['name']} skill for {config['domain']}.

TODO: Implement actual functionality
This is a placeholder generated by skill_builder.py
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class {class_name}:
    """Main class for {tool_name_human} functionality"""

    def __init__(self, target: str, verbose: bool = False):
        """
        Initialize {tool_name_human}

        Args:
            target: Input file or data to process
            verbose: Enable verbose output
        """
        self.target = target
        self.verbose = verbose
        self.results = {{}}

    def run(self) -> Dict:
        """Execute the main functionality"""
        if self.verbose:
            print(f"🚀 Running {{self.__class__.__name__}}...")
            print(f"📁 Target: {{self.target}}")

        try:
            self.validate_input()
            self.process()
            self.generate_output()

            if self.verbose:
                print("✅ Completed successfully!")

            return self.results

        except Exception as e:
            print(f"❌ Error: {{e}}", file=sys.stderr)
            sys.exit(1)

    def validate_input(self):
        """Validate input parameters"""
        # TODO: Add validation logic
        if self.verbose:
            print("✓ Input validated")

    def process(self):
        """Perform main processing"""
        # TODO: Implement core functionality
        self.results['status'] = 'success'
        self.results['message'] = 'TODO: Add implementation'
        self.results['data'] = {{}}

        if self.verbose:
            print("✓ Processing complete")

    def generate_output(self):
        """Generate and display output"""
        # TODO: Format output
        print("\\n" + "="*50)
        print("RESULTS")
        print("="*50)
        print(json.dumps(self.results, indent=2))
        print("="*50 + "\\n")


def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="{tool_name_human} - Automated processing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python {{}} input.txt
  python {{}} input.txt --verbose
  python {{}} input.txt --output results.json

Part of {config['name']} skill.
""".format(os.path.basename(__file__), os.path.basename(__file__), os.path.basename(__file__))
    )

    parser.add_argument(
        'target',
        help='Input file or data to process'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)',
        default=None
    )

    args = parser.parse_args()

    # Create and run tool
    tool = {class_name}(args.target, verbose=args.verbose)
    results = tool.run()

    # Save output if specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"✅ Results saved to: {{args.output}}")


if __name__ == "__main__":
    main()
'''
        return template

    def generate_placeholder_reference(self, ref_name: str, config: Dict) -> str:
        """Generate placeholder reference guide"""
        ref_title = ref_name.replace('.md', '').replace('_', ' ').replace('-', ' ').title()

        template = f"""# {ref_title}

Part of {config['name']} skill for {config['domain']}.

## Overview

[TODO: Add overview of this reference guide]

This reference provides comprehensive guidance for [topic area].

## Key Concepts

[TODO: Document key concepts]

### Concept 1

[Description]

### Concept 2

[Description]

### Concept 3

[Description]

## Best Practices

[TODO: Add best practices]

1. **Practice 1** - Description and rationale
2. **Practice 2** - Description and rationale
3. **Practice 3** - Description and rationale

## Frameworks

[TODO: Provide frameworks and methodologies]

### Framework 1

[Description]

### Framework 2

[Description]

## Examples

[TODO: Provide examples]

### Example 1: [Use Case]

**Scenario:** [Description]

**Approach:** [Steps]

**Outcome:** [Result]

## Resources

- [External resource 1]
- [External resource 2]

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Status:** Draft - To be expanded
**Part of:** {config['name']} skill
"""
        return template


# ============================================================================
# SECTION 6: DIRECTORY SCAFFOLDING
# ============================================================================
# Creates skill directory structure with files and permissions

class DirectoryScaffolder:
    """Create skill directory structure"""

    def __init__(self, repo_root: Path, template_loader: SkillTemplateLoader):
        self.repo_root = repo_root
        self.template_loader = template_loader

    def create_skill_structure(self, base_path: Path, config: Dict) -> None:
        """
        Create complete skill directory structure

        Args:
            base_path: Path to skill (e.g., skills/engineering-team/data-analyst-toolkit/)
            config: Skill configuration dict
        """
        # Create main directory
        base_path.mkdir(parents=True, exist_ok=False)
        print(f"✓ Created {base_path.relative_to(self.repo_root)}/")

        # Create subdirectories
        scripts_dir = base_path / "scripts"
        references_dir = base_path / "references"
        assets_dir = base_path / "assets"

        scripts_dir.mkdir()
        references_dir.mkdir()
        assets_dir.mkdir()

        print(f"✓ Created scripts/")
        print(f"✓ Created references/")
        print(f"✓ Created assets/")

        # Create SKILL.md
        try:
            template = self.template_loader.load_template()
            skill_md = self.template_loader.populate_template(template, config)
            (base_path / "SKILL.md").write_text(skill_md)
            print(f"✓ Created SKILL.md")
        except Exception as e:
            print(f"⚠️  SKILL.md creation failed: {e}")

        # Create Python tools
        for tool_name in config.get('tools', []):
            try:
                tool_content = self.template_loader.generate_placeholder_tool(tool_name, config)
                tool_path = scripts_dir / tool_name
                tool_path.write_text(tool_content)
                tool_path.chmod(0o755)  # Make executable
                print(f"✓ Created scripts/{tool_name}")
            except Exception as e:
                print(f"⚠️  Tool creation failed ({tool_name}): {e}")

        # Create reference guides
        for guide_name in config.get('references', []):
            try:
                guide_content = self.template_loader.generate_placeholder_reference(guide_name, config)
                guide_path = references_dir / guide_name
                guide_path.write_text(guide_content)
                print(f"✓ Created references/{guide_name}")
            except Exception as e:
                print(f"⚠️  Reference creation failed ({guide_name}): {e}")

        # Create .gitkeep in assets
        (assets_dir / ".gitkeep").write_text("")
        print(f"✓ Created assets/.gitkeep")

        # Create HOW_TO_USE.md
        try:
            how_to_use = self._generate_how_to_use(config)
            (base_path / "HOW_TO_USE.md").write_text(how_to_use)
            print(f"✓ Created HOW_TO_USE.md")
        except Exception as e:
            print(f"⚠️  HOW_TO_USE.md creation failed: {e}")

    def _generate_how_to_use(self, config: Dict) -> str:
        """Generate HOW_TO_USE.md content"""
        skill_name_title = config['name'].replace('-', ' ').title()

        content = f"""# How to Use the {skill_name_title} Skill

## Quick Start

Hey Claude—I just added the "{config['name']}" skill. Can you help me with [describe your task]?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "{config['name']}" skill. Can you [specific task related to this skill]?
```

### Example 2: Advanced Usage
```
Hey Claude—I just added the "{config['name']}" skill. Can you [more complex task with specific requirements]?
```

### Example 3: Integration with Other Skills
```
Hey Claude—I just added the "{config['name']}" skill. Can you use it together with [another skill] to [combined task]?
```

## What to Provide

When using this skill, provide:

- **Primary Input**: [Describe the main input needed]
- **Context** (optional): [What context helps improve results]
- **Preferences** (optional): [Any customization options]

## What You'll Get

This skill will provide:

- **Output Format**: {config.get('output_format', 'Results formatted according to skill specifications')}
- **Analysis**: Insights and recommendations based on the input
- **Deliverables**: {', '.join(config.get('tools', ['Reports and actionable outputs']))}

## Python Tools Available

This skill includes the following Python tools:

"""
        for tool in config.get('tools', []):
            tool_name = tool.replace('.py', '').replace('_', ' ').title()
            content += f"- **{tool}**: {tool_name} functionality\n"

        content += f"""
You can also run these tools directly:

```bash
python scripts/{config.get('tools', ['tool_name.py'])[0]} --help
```

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements for better results
2. **Provide Context**: Include relevant background information
3. **Iterate**: Start simple, then refine based on initial results
4. **Combine Skills**: This skill works well with other {config['domain'].replace('-team', '')} skills

## Related Skills

Consider using these skills together:

- [List related skills from the same domain]
- [Skills that complement this one]

---

**Skill**: {config['name']}
**Domain**: {config['domain']}
**Version**: 1.0.0
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
"""
        return content


# ============================================================================
# SECTION 7: CORE SKILL BUILDER
# ============================================================================
# Main orchestration logic for skill creation and validation

class SkillBuilder:
    """Main orchestrator for skill creation"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.validator = SkillValidator(repo_root)
        self.template_loader = SkillTemplateLoader(repo_root)
        self.scaffolder = DirectoryScaffolder(repo_root, self.template_loader)
        self.team_manager = SkillTeamManager(repo_root)

    def interactive_mode(self) -> None:
        """Run interactive skill creation workflow"""
        print("📦 Skill Builder")
        print("=" * 50)
        print()

        config = {}

        # Step 1: Skill Name
        config['name'] = self._prompt_skill_name()

        # Step 2: Domain Team
        config['domain'] = self._prompt_domain_team()

        # Step 3: Description
        config['description'] = self._prompt_description()

        # Step 4: Keywords
        config['keywords'] = self._prompt_keywords()

        # Step 5: Tech Stack
        config['tech_stack'] = self._prompt_tech_stack()

        # Step 6: Python Tools
        config['tools'] = self._prompt_python_tools()

        # Step 7: Reference Guides
        config['references'] = self._prompt_reference_guides()

        # Step 8: Preview and Confirm
        if not self._preview_and_confirm(config):
            print("❌ Skill creation cancelled")
            sys.exit(EXIT_SUCCESS)

        # Generate skill
        self.generate_skill(config)

    def _prompt_skill_name(self) -> str:
        """Prompt for skill name with validation"""
        print("Step 1/8: Skill Name")
        print("-" * 50)
        print("Enter skill name (kebab-case):")
        print("Example: data-analyst-toolkit, senior-architect")
        print()

        while True:
            name = input("Name: ").strip().lower()

            valid, msg = self.validator.validate_name(name)
            if valid:
                print(f"✓ Valid name format")
                print()
                return name
            else:
                print(f"❌ {msg}")
                print()

    def _prompt_domain_team(self) -> str:
        """Prompt for skill team domain"""
        print("Step 2/8: Skill Team Domain")
        print("-" * 50)

        existing_teams = self.team_manager.get_existing_teams()

        print("Select skill team:")
        for idx, team in enumerate(existing_teams, 1):
            # Count skills in team
            team_path = self.repo_root / "skills" / team
            skill_count = len([d for d in team_path.iterdir() if d.is_dir() and not d.name.startswith('.')])
            print(f"{idx}. {team} ({skill_count} skills)")

        print(f"{len(existing_teams) + 1}. Create new skill team")
        print()

        while True:
            choice = input(f"Skill team (1-{len(existing_teams) + 1}): ").strip()

            # Existing team selected
            if choice.isdigit() and 1 <= int(choice) <= len(existing_teams):
                team = existing_teams[int(choice) - 1]
                print(f"✓ Domain: {team}")
                print()
                return team

            # New team requested
            if choice.isdigit() and int(choice) == len(existing_teams) + 1:
                return self._create_new_skill_team()

            print("❌ Invalid selection")
            print()

    def _create_new_skill_team(self) -> str:
        """Interactive workflow for creating new skill team"""
        print()
        print("🆕 Create New Skill Team")
        print("-" * 50)
        print("Skill team names should be:")
        print("  • Lowercase kebab-case with '-team' suffix")
        print("  • Descriptive and concise (e.g., 'sales-team', 'finance-team')")
        print()

        while True:
            team_name = input("New skill team name: ").strip().lower()

            # Auto-add -team suffix if missing
            if not team_name.endswith('-team'):
                print("⚠️  Skill teams typically end with '-team' suffix")
                add_suffix = input("Add '-team' suffix? (y/n): ").strip().lower()
                if add_suffix == 'y':
                    team_name = f"{team_name}-team"

            # Validate format
            valid, message = self.team_manager.validate_team_format(team_name)
            if not valid:
                print(f"❌ {message}")
                print()
                continue

            # Check conflicts
            if (self.repo_root / "skills" / team_name).exists():
                print(f"❌ Skill team '{team_name}' already exists")
                print()
                continue

            # Confirm creation
            print()
            print(f"✓ Team format valid: {team_name}")
            print(f"\nThis will create:")
            print(f"  • skills/{team_name}/ directory")
            print(f"  • skills/{team_name}/README.md")
            print(f"  • skills/{team_name}/CLAUDE.md")
            print()

            confirm = input("Create this skill team? (y/n): ").strip().lower()
            if confirm == 'y':
                self.team_manager.create_new_team(team_name)
                print(f"✓ Domain: {team_name}")
                print()
                return team_name
            else:
                print("❌ Team creation cancelled")
                print()
                return self._prompt_domain_team()

    def _prompt_description(self) -> str:
        """Prompt for skill description"""
        print("Step 3/8: Description")
        print("-" * 50)
        print("Enter skill description (used in YAML frontmatter):")
        print("This appears in search and skill browsing.")
        print("Keep under 300 characters.")
        print()

        while True:
            description = input("Description: ").strip()

            if len(description) < 20:
                print("❌ Description too short (minimum 20 chars)")
                print()
                continue

            if len(description) > 300:
                print(f"❌ Description too long ({len(description)} chars, max 300)")
                print()
                continue

            print(f"✓ Length: {len(description)} chars")
            print()
            return description

    def _prompt_keywords(self) -> List[str]:
        """Prompt for keywords"""
        print("Step 4/8: Keywords")
        print("-" * 50)
        print("Enter keywords (comma-separated, 6-15 recommended):")
        print("Example: data analysis, reporting, SQL, Python, dashboards")
        print()

        while True:
            keywords_str = input("Keywords: ").strip()
            keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]

            if len(keywords) < 3:
                print(f"❌ Too few keywords ({len(keywords)}, minimum 3)")
                print()
                continue

            if len(keywords) > 20:
                print(f"❌ Too many keywords ({len(keywords)}, maximum 20)")
                print()
                continue

            print(f"✓ {len(keywords)} keywords")
            print()
            return keywords

    def _prompt_tech_stack(self) -> List[str]:
        """Prompt for tech stack"""
        print("Step 5/8: Tech Stack")
        print("-" * 50)
        print("Enter tech stack (comma-separated):")
        print("Example: Python 3.8+, PostgreSQL, Pandas, Matplotlib")
        print()

        tech_str = input("Tech Stack: ").strip()
        tech_stack = [t.strip() for t in tech_str.split(',') if t.strip()]

        print(f"✓ {len(tech_stack)} technologies")
        print()
        return tech_stack

    def _prompt_python_tools(self) -> List[str]:
        """Prompt for Python tools"""
        print("Step 6/8: Python Tools")
        print("-" * 50)
        print()
        print("When to Use Python Tools:")
        print("  ✓ USE Python when skill needs:")
        print("    - Mathematical calculations or data processing")
        print("    - File generation (Excel, PDF, CSV, JSON)")
        print("    - Complex algorithms or transformations")
        print("    - API interactions or external integrations")
        print()
        print("  ✗ DON'T use Python when skill is:")
        print("    - Purely instructional (style guides, tone of voice)")
        print("    - Simple template/framework application")
        print("    - Decision-making guidance or advisory")
        print("    - Prompt-based formatting or content generation")
        print()
        print("How many Python CLI tools will this skill have?")
        print("Minimum: 1, Recommended: 2-4")
        print()

        while True:
            try:
                count = int(input("Count: ").strip())
                if count < 1:
                    print("❌ Must have at least 1 tool")
                    print()
                    continue
                break
            except ValueError:
                print("❌ Please enter a number")
                print()

        print()
        print("Enter tool names (one per line):")
        print("Example: data_analyzer.py")
        tools = []
        for i in range(count):
            while True:
                tool = input(f"Tool {i+1}: ").strip()

                # Auto-add .py extension if missing
                if not tool.endswith('.py'):
                    tool = f"{tool}.py"

                # Validate format
                if not re.match(r'^[a-z][a-z0-9_]+\.py$', tool):
                    print("❌ Tool name must be lowercase snake_case.py")
                    continue

                tools.append(tool)
                break

        print()
        print(f"✓ {len(tools)} tools configured")
        print()
        return tools

    def _prompt_reference_guides(self) -> List[str]:
        """Prompt for reference guides"""
        print("Step 7/8: Reference Guides")
        print("-" * 50)
        print("How many reference guides (markdown docs)?")
        print("Minimum: 0, Recommended: 2-3")
        print()

        while True:
            try:
                count = int(input("Count: ").strip())
                if count < 0:
                    print("❌ Cannot be negative")
                    print()
                    continue
                break
            except ValueError:
                print("❌ Please enter a number")
                print()

        if count == 0:
            print("✓ No reference guides")
            print()
            return []

        print()
        print("Enter guide names (one per line):")
        print("Example: analysis_frameworks.md")
        guides = []
        for i in range(count):
            while True:
                guide = input(f"Guide {i+1}: ").strip()

                # Auto-add .md extension if missing
                if not guide.endswith('.md'):
                    guide = f"{guide}.md"

                # Validate format
                if not re.match(r'^[a-z][a-z0-9_-]+\.md$', guide):
                    print("❌ Guide name must be lowercase with underscores/hyphens.md")
                    continue

                guides.append(guide)
                break

        print()
        print(f"✓ {len(guides)} reference guides configured")
        print()
        return guides

    def _preview_and_confirm(self, config: Dict) -> bool:
        """Preview configuration and confirm creation"""
        print("Step 8/8: Preview")
        print("-" * 50)
        print("Review your skill configuration:")
        print()
        print(f"Name:        {config['name']}")
        print(f"Domain:      {config['domain']}")
        print(f"Description: {config['description']}")
        print(f"Keywords:    {len(config['keywords'])} keywords")
        print(f"Tech Stack:  {', '.join(config['tech_stack'])}")
        print(f"Tools:       {len(config['tools'])} ({', '.join(config['tools'])})")
        print(f"References:  {len(config['references'])} ({', '.join(config['references']) if config['references'] else 'none'})")
        print()
        print("Directory structure to create:")
        print(f"skills/{config['domain']}/{config['name']}/")
        print("├── SKILL.md")
        print("├── HOW_TO_USE.md")
        print("├── scripts/")
        for tool in config['tools']:
            print(f"│   ├── {tool}")
        print("├── references/")
        for guide in config['references']:
            print(f"│   ├── {guide}")
        print("└── assets/")
        print("    └── (empty - add templates as needed)")
        print()

        confirm = input("Proceed? (y/n): ").strip().lower()
        return confirm == 'y'

    def generate_skill(self, config: Dict) -> None:
        """Generate skill directory structure and files"""
        skill_path = self.repo_root / "skills" / config['domain'] / config['name']

        if skill_path.exists():
            print(f"❌ Skill already exists: {skill_path}")
            sys.exit(EXIT_FILE_ERROR)

        print()
        print("Creating skill...")
        print()

        try:
            self.scaffolder.create_skill_structure(skill_path, config)

            print()
            print("✅ Skill created successfully!")
            print()
            print("Next steps:")
            print(f"1. Review and customize SKILL.md")
            print(f"2. Implement Python tools in scripts/")
            print(f"3. Add reference content to references/")
            print(f"4. Add user templates to assets/")
            print(f"5. Test with: python scripts/skill_builder.py --validate {skill_path.relative_to(self.repo_root)}")
            print()
            print(f"Skill location: {skill_path.relative_to(self.repo_root)}/")

        except Exception as e:
            print(f"❌ Skill creation failed: {e}")
            sys.exit(EXIT_FILE_ERROR)

    def config_mode(self, config_path: str) -> None:
        """Create skill from config file"""
        config_file = Path(config_path)

        if not config_file.exists():
            print(f"❌ Config file not found: {config_path}")
            sys.exit(EXIT_CONFIG_ERROR)

        try:
            if YAML_AVAILABLE:
                config = yaml.safe_load(config_file.read_text())
            else:
                config = simple_yaml_parse(config_file.read_text())
        except Exception as e:
            print(f"❌ Invalid config file: {e}")
            sys.exit(EXIT_CONFIG_ERROR)

        # Validate required fields
        required = ['name', 'domain', 'description', 'keywords', 'tech_stack', 'tools']
        missing = [f for f in required if f not in config]
        if missing:
            print(f"❌ Missing required fields: {', '.join(missing)}")
            sys.exit(EXIT_CONFIG_ERROR)

        # Set defaults
        config.setdefault('references', [])

        print(f"Creating skill from config: {config_path}")
        print()

        self.generate_skill(config)

    def validate_existing(self, skill_path: str, include_cleanup: bool = False) -> int:
        """Validate an existing skill package

        Args:
            skill_path: Path to skill directory
            include_cleanup: Whether to include cleanup validation
        """
        path = Path(skill_path)

        if not path.is_absolute():
            path = self.repo_root / path

        print(f"Validating skill: {path.name}")
        print("=" * 50)
        if include_cleanup:
            print("Mode: Full validation (including file cleanliness)")
        else:
            print("Mode: Standard validation")
        print()

        result = self.validator.run_all_checks(path, include_cleanup=include_cleanup)

        # Print results
        for check in result['checks']:
            status_icon = "✓" if check['status'] == 'passed' else "✗"
            print(f"{status_icon} {check['name']}: {check['message']}")

        print()
        print(f"Results: {result['checks_passed']}/{result['checks_total']} checks passed")
        print()

        if result['status'] == 'passed':
            print("✅ Skill validation passed")
            return EXIT_SUCCESS
        else:
            print("❌ Skill validation failed")
            if include_cleanup:
                print()
                print("Cleanup recommendations:")
                print("  • Remove backup files (.backup, .bak, .old)")
                print("  • Delete __pycache__/ directories")
                print("  • Remove internal summary/notes documents")
                print("  • Delete temporary files (.tmp, .temp, .DS_Store)")
            return EXIT_VALIDATION_FAILED


# ============================================================================
# SECTION 8: CLI ENTRY POINT
# ============================================================================
# Command-line argument parsing and mode selection

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Skill Builder - Interactive CLI for creating skill packages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python skill_builder.py                                             # Interactive mode
  python skill_builder.py --config skill-config.yaml                 # Config file mode
  python skill_builder.py --validate skills/team/skill/              # Standard validation
  python skill_builder.py --validate skills/team/skill/ --validate-cleanup  # Full validation with cleanup checks
  python skill_builder.py --dry-run --config config.yaml             # Dry run

For more information, see: docs/CLAUDE.md
"""
    )

    parser.add_argument(
        '--config',
        help='Config file path (YAML)',
        default=None
    )

    parser.add_argument(
        '--validate',
        help='Validate existing skill package',
        default=None
    )

    parser.add_argument(
        '--validate-cleanup',
        action='store_true',
        help='Include file cleanliness validation (checks for backup files, __pycache__, etc.)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without creating files'
    )

    args = parser.parse_args()

    # Determine repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    builder = SkillBuilder(repo_root)

    try:
        # Validation mode
        if args.validate:
            exit_code = builder.validate_existing(args.validate, include_cleanup=args.validate_cleanup)
            sys.exit(exit_code)

        # Config mode
        elif args.config:
            if args.dry_run:
                print("⚠️  Dry run mode not yet implemented for config mode")
                sys.exit(EXIT_SUCCESS)
            builder.config_mode(args.config)

        # Interactive mode (default)
        else:
            builder.interactive_mode()

    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(EXIT_SUCCESS)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(EXIT_UNKNOWN_ERROR)


if __name__ == "__main__":
    main()
