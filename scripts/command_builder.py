#!/usr/bin/env python3
"""
Command Builder - Interactive CLI for creating slash commands

This tool automates command creation with comprehensive validation,
template population, and catalog integration.

Usage:
    python command_builder.py                        # Interactive mode
    python command_builder.py --config config.yaml   # Config file mode
    python command_builder.py --validate path.md     # Validation mode
    python command_builder.py --help                 # Show help

ARCHITECTURE NOTE - Single-File Design:
    This script is intentionally monolithic (1,285 lines) for portability.
    Users can extract this single file and run it anywhere with Python 3.8+.
    This aligns with the repository's zero-dependency, portable-skills philosophy.

    Code is organized into logical sections for maintainability:

    SECTION 1: Configuration & Constants (Lines 15-38)
        - Exit codes, imports, global configuration

    SECTION 2: YAML Parsing Utilities (Lines 40-142)
        - simple_yaml_parse() - Standard library YAML parser
        - Handles basic YAML without external dependencies

    SECTION 3: Category Management (Lines 143-202)
        - CategoryManager class
        - Dynamic category discovery and validation

    SECTION 4: Validation Logic (Lines 203-551)
        - CommandValidator class
        - 10+ validation checks for command structure

    SECTION 5: Template Management (Lines 552-687)
        - TemplateLoader class
        - Template file loading and generation

    SECTION 6: Catalog Integration (Lines 688-735)
        - CatalogUpdater class
        - Updates commands/CATALOG.md automatically

    SECTION 7: Core Command Builder (Lines 736-1239)
        - CommandBuilder class
        - Main orchestration logic

    SECTION 8: CLI Entry Point (Lines 1240-1285)
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
# Standard library YAML parser for command frontmatter (zero dependencies)

def simple_yaml_parse(yaml_str: str) -> Dict:
    """
    Simple YAML parser for command frontmatter (standard library only)

    Handles basic key-value pairs, lists, and one level of nesting.
    Does NOT support deep nesting or complex YAML features.
    """
    result = {}
    current_key = None
    current_nested_key = None
    list_items = []
    nested_dict = {}
    nested_list = []

    lines = yaml_str.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        original_line = line
        line = line.rstrip()

        if not line.strip() or line.strip().startswith('#'):
            i += 1
            continue

        # Calculate indentation
        indent = len(line) - len(line.lstrip())

        line = line.strip()

        # List item at various indentation levels
        if line.startswith('- '):
            item = line[2:].strip()
            if indent > 2:
                # Nested list item
                nested_list.append(item)
            else:
                # Top-level list item
                list_items.append(item)
            i += 1
            continue

        # Key-value pair
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if indent == 0:
                # Top-level key
                # Save previous nested structure
                if current_key and nested_dict:
                    result[current_key] = nested_dict
                    nested_dict = {}
                    current_nested_key = None
                # Save previous list
                if current_key and list_items:
                    result[current_key] = list_items
                    list_items = []

                current_key = key

                # Handle inline values
                if value.startswith('[') and value.endswith(']'):
                    items = value[1:-1].split(',')
                    result[key] = [item.strip() for item in items]
                    current_key = None
                elif value:
                    result[key] = value
                    current_key = None
                # else: value will come on next lines

            elif indent > 0:
                # Nested key (second level)
                # Save previous nested list
                if current_nested_key and nested_list:
                    nested_dict[current_nested_key] = nested_list
                    nested_list = []

                current_nested_key = key

                if value.startswith('[') and value.endswith(']'):
                    items = value[1:-1].split(',')
                    nested_dict[key] = [item.strip() for item in items]
                    current_nested_key = None
                elif value:
                    nested_dict[key] = value
                    current_nested_key = None
                # else: value will come on next lines

        i += 1

    # Save final structures
    if current_nested_key and nested_list:
        nested_dict[current_nested_key] = nested_list
    if current_key and nested_dict:
        result[current_key] = nested_dict
    if current_key and list_items:
        result[current_key] = list_items

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
                print("\nContinuing with command creation...\n")
                return session_id
            else:
                print("\nSkipping session creation. Continuing with command creation...\n")
        else:
            print("\nSkipping session creation. Continuing with command creation...\n")
    except (KeyboardInterrupt, EOFError):
        print("\n\nSkipping session creation...\n")

    return None


# ============================================================================
# SECTION 3: CATEGORY MANAGEMENT
# ============================================================================
# Dynamic category discovery and validation

class CategoryManager:
    """Manage command categories dynamically"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.commands_dir = repo_root / "commands"

    def get_existing_categories(self) -> List[str]:
        """Discover existing command categories from file system"""
        if not self.commands_dir.exists():
            return []

        categories = []
        for item in self.commands_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                categories.append(item.name)

        return sorted(categories)

    def validate_category_format(self, category: str) -> Tuple[bool, str]:
        """Validate category name format (kebab-case, lowercase)"""
        pattern = r'^[a-z][a-z0-9-]*$'
        if not re.match(pattern, category):
            return False, f"Category must be lowercase kebab-case: {category}"
        if len(category) < 3:
            return False, f"Category too short (min 3 chars): {category}"
        if len(category) > 20:
            return False, f"Category too long (max 20 chars): {category}"
        if '--' in category:
            return False, f"Category cannot have consecutive hyphens: {category}"
        return True, "Valid category format"

    def create_category_directory(self, category: str) -> None:
        """Create new category directory structure"""
        category_path = self.commands_dir / category
        category_path.mkdir(parents=True, exist_ok=True)

        # Create CATALOG.md
        catalog_content = f"""# {category.replace('-', ' ').title()} Commands

This directory contains commands for the {category} category.

## Commands

<!-- Commands will be listed here automatically by command_builder.py -->

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Category:** {category}
**Command Count:** 0
"""

        catalog_path = category_path / "CATALOG.md"
        catalog_path.write_text(catalog_content)

        print(f"✅ Created: {category_path}/")
        print(f"✅ Created: {catalog_path}")


# ============================================================================
# SECTION 4: VALIDATION LOGIC
# ============================================================================
# Comprehensive validation checks for command structure and metadata

class CommandValidator:
    """Validation logic for command files"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.standard_categories = {
            'code', 'docs', 'git', 'test', 'deploy', 'workflow',
            'security', 'architecture', 'content', 'data'
        }

    def validate_name(self, name: str) -> Tuple[bool, str]:
        """Validate command name format (category.command-name)"""
        if not name:
            return False, "Command name cannot be empty"

        if len(name) > 40:
            return False, f"Command name too long ({len(name)} chars, max 40)"

        if '.' not in name:
            return False, "Command name must include category prefix (category.command-name)"

        pattern = r'^[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$'
        if not re.match(pattern, name):
            return False, "Command name must be kebab-case with category prefix (category.command-name)"

        return True, "Valid"

    def parse_yaml_frontmatter(self, content: str) -> Tuple[Optional[Dict], str, Optional[str]]:
        """
        Extract YAML frontmatter and content body

        Returns:
            (frontmatter_dict, markdown_body, error_message)
        """
        if not content.startswith('---'):
            return None, content, "No YAML frontmatter found"

        # Split at first and second ---
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, content, "Malformed YAML frontmatter"

        yaml_str = parts[1]
        body = parts[2]

        try:
            if YAML_AVAILABLE:
                frontmatter = yaml.safe_load(yaml_str)
            else:
                # Use simple parser fallback
                frontmatter = simple_yaml_parse(yaml_str)
            return frontmatter, body, None
        except Exception as e:
            return None, body, f"Invalid YAML syntax: {e}"

    def validate_yaml_frontmatter(self, content: str) -> Tuple[bool, str]:
        """Validate YAML frontmatter is present and valid"""
        frontmatter, body, error = self.parse_yaml_frontmatter(content)

        if error:
            return False, error

        if not frontmatter:
            return False, "Missing YAML frontmatter"

        # Required fields
        required = ['name', 'title', 'description', 'category', 'subcategory']
        for field in required:
            if field not in frontmatter:
                return False, f"Missing required YAML field: {field}"

        # Field validation
        if len(frontmatter['description']) > 150:
            return False, f"Description too long: {len(frontmatter['description'])} chars (max: 150)"

        # Validate difficulty if present
        if 'difficulty' in frontmatter:
            valid_difficulty = ['beginner', 'intermediate', 'advanced']
            if frontmatter['difficulty'] not in valid_difficulty:
                return False, f"Invalid difficulty: {frontmatter['difficulty']} (must be: {', '.join(valid_difficulty)})"

        # Validate tags if present (min 3)
        if 'tags' in frontmatter:
            if not isinstance(frontmatter['tags'], list):
                return False, "Tags must be a list"
            if len(frontmatter['tags']) < 3:
                return False, f"Minimum 3 tags required (found: {len(frontmatter['tags'])})"

        return True, "Valid"

    def validate_extended_metadata(self, content: str) -> Tuple[bool, str]:
        """Validate extended metadata for website readiness"""
        frontmatter, body, error = self.parse_yaml_frontmatter(content)

        if error or not frontmatter:
            return False, "Cannot validate extended metadata: invalid frontmatter"

        # Check website-required fields
        website_fields = ['difficulty', 'time-saved', 'frequency', 'use-cases']
        missing = []
        for field in website_fields:
            if field not in frontmatter:
                missing.append(field)

        if missing:
            return False, f"Missing website fields: {', '.join(missing)}"

        # Validate use-cases (min 2)
        if 'use-cases' in frontmatter:
            if not isinstance(frontmatter['use-cases'], list):
                return False, "use-cases must be a list"
            if len(frontmatter['use-cases']) < 2:
                return False, f"Minimum 2 use cases required (found: {len(frontmatter['use-cases'])})"

        return True, "Valid"

    def validate_argument_handling(self, content: str) -> Tuple[bool, str]:
        """Validate $ARGUMENTS usage pattern"""
        # Check if command uses arguments
        if '## Usage' not in content:
            return False, "Missing Usage section"

        # Extract usage section
        usage_start = content.find('## Usage')
        usage_end = content.find('\n## ', usage_start + 8)
        if usage_end == -1:
            usage_section = content[usage_start:]
        else:
            usage_section = content[usage_start:usage_end]

        # Check for Arguments subsection if command takes arguments
        has_args_in_usage = '[' in usage_section and ']' in usage_section
        has_args_section = '### Arguments' in usage_section

        if has_args_in_usage and not has_args_section:
            return False, "Usage shows arguments but no Arguments subsection found"

        return True, "Valid"

    def validate_execution_steps(self, content: str) -> Tuple[bool, str]:
        """Validate execution steps are present based on pattern"""
        frontmatter, body, error = self.parse_yaml_frontmatter(content)

        if error or not frontmatter:
            return False, "Cannot validate execution steps: invalid frontmatter"

        # Pattern-specific validation would go here
        # For now, just check that body has substantial content
        if len(body.strip()) < 500:
            return False, "Command documentation too brief (< 500 chars)"

        return True, "Valid"

    def validate_usage_examples(self, content: str) -> Tuple[bool, str]:
        """Ensure minimum 2 examples documented"""
        # Check for Examples section - could be under Usage or standalone
        examples_patterns = ['## Examples', '### Examples']
        examples_start = -1

        for pattern in examples_patterns:
            pos = content.find(pattern)
            if pos != -1:
                examples_start = pos
                break

        if examples_start == -1:
            return False, "Examples section not found"

        # Get content until next H2 or H3 section
        examples_end = content.find('\n## ', examples_start + 12)
        if examples_end == -1:
            examples_end = content.find('\n### ', examples_start + 12)
        if examples_end == -1:
            examples_section = content[examples_start:]
        else:
            examples_section = content[examples_start:examples_end]

        # Count distinct example indicators:
        # 1. Code blocks with bash language
        # 2. Comments starting with "# Example" or "# Basic" or "# Advanced"
        # 3. Separate code blocks (count pairs of ```)

        bash_blocks = examples_section.count('```bash')
        example_comments = len(re.findall(r'#\s+(Example|Basic|Advanced|Simple|Common)', examples_section))

        # Count total code blocks
        total_code_blocks = examples_section.count('```') // 2

        # Use the maximum as number of examples
        num_examples = max(bash_blocks, example_comments, total_code_blocks)

        if num_examples < 2:
            return False, f"Only {num_examples} examples found (minimum: 2)"

        return True, f"Valid ({num_examples} examples)"

    def validate_dependencies(self, content: str) -> Tuple[bool, str]:
        """Ensure dependencies documented"""
        frontmatter, body, error = self.parse_yaml_frontmatter(content)

        if error or not frontmatter:
            return False, "Cannot validate dependencies: invalid frontmatter"

        # Check for dependencies field
        if 'dependencies' not in frontmatter:
            return False, "Missing dependencies field in frontmatter"

        deps = frontmatter['dependencies']
        if not isinstance(deps, dict):
            return False, "Dependencies must be a dict"

        # Check required subfields
        required_keys = ['tools', 'scripts', 'python-packages']
        for key in required_keys:
            if key not in deps:
                return False, f"Missing dependencies.{key}"

        return True, "Valid"

    def validate_markdown_structure(self, content: str) -> Tuple[bool, str]:
        """Validate proper markdown headings and structure"""
        # Count H1 headings (only count lines starting with # followed by space, not in frontmatter)
        # First, remove YAML frontmatter
        parts = content.split('---', 2)
        if len(parts) >= 3:
            markdown_content = parts[2]
        else:
            markdown_content = content

        # Remove code blocks from consideration
        # This prevents counting # comments in bash code as H1 headings
        content_no_code = re.sub(r'```.*?```', '', markdown_content, flags=re.DOTALL)

        # Count H1 headings in markdown content only (excluding code blocks)
        lines = content_no_code.split('\n')
        h1_count = 0
        for line in lines:
            stripped = line.strip()
            # Match: starts with single #, followed by space, not multiple #
            if re.match(r'^#\s+[^#]', stripped):
                h1_count += 1

        if h1_count == 0:
            return False, "Missing H1 title"
        if h1_count > 1:
            return False, f"Multiple H1 headings found ({h1_count}), should have exactly 1"

        # Check for required sections
        required_sections = ['## Usage', '## Error Handling', '## Success Criteria']
        missing = []
        for section in required_sections:
            if section not in markdown_content:
                missing.append(section)

        if missing:
            return False, f"Missing sections: {', '.join(missing)}"

        return True, "Valid"

    def run_all_checks(self, command_path: Path) -> Dict:
        """Run all validation checks and return results"""
        if not command_path.exists():
            return {
                'status': 'failed',
                'checks_passed': 0,
                'checks_total': 8,
                'error': f"Command file not found: {command_path}"
            }

        content = command_path.read_text()

        checks = []

        # Check 1: Name format
        command_name = command_path.stem
        valid, msg = self.validate_name(command_name)
        checks.append({
            'name': 'name_format',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 2: YAML frontmatter
        valid, msg = self.validate_yaml_frontmatter(content)
        checks.append({
            'name': 'yaml_frontmatter',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 3: Extended metadata
        valid, msg = self.validate_extended_metadata(content)
        checks.append({
            'name': 'extended_metadata',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 4: Argument handling
        valid, msg = self.validate_argument_handling(content)
        checks.append({
            'name': 'argument_handling',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 5: Execution steps
        valid, msg = self.validate_execution_steps(content)
        checks.append({
            'name': 'execution_steps',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 6: Usage examples
        valid, msg = self.validate_usage_examples(content)
        checks.append({
            'name': 'usage_examples',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 7: Dependencies
        valid, msg = self.validate_dependencies(content)
        checks.append({
            'name': 'dependencies',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 8: Markdown structure
        valid, msg = self.validate_markdown_structure(content)
        checks.append({
            'name': 'markdown_structure',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        checks_passed = sum(1 for c in checks if c['status'] == 'passed')

        return {
            'command': command_name,
            'status': 'passed' if checks_passed == len(checks) else 'failed',
            'checks_passed': checks_passed,
            'checks_total': len(checks),
            'checks': checks
        }


# ============================================================================
# SECTION 5: TEMPLATE MANAGEMENT
# ============================================================================
# Template file loading and content generation

class TemplateLoader:
    """Load and populate command template"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.template_path = repo_root / "templates" / "command-template.md"

    def load_template(self) -> str:
        """Load command-template.md"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        return self.template_path.read_text()

    def populate_template(self, config: Dict) -> str:
        """Replace placeholders with actual values"""
        template = self.load_template()

        # Build YAML frontmatter
        yaml_lines = [
            '---',
            f"name: {config['name']}",
            f"title: {config['title']}",
            f"description: {config['description']}",
            f"category: {config['category']}",
            f"subcategory: {config['subcategory']}",
        ]

        # Add required website fields
        if 'difficulty' in config:
            yaml_lines.append(f"difficulty: {config['difficulty']}")
        if 'time-saved' in config:
            yaml_lines.append(f"time-saved: \"{config['time-saved']}\"")
        if 'frequency' in config:
            yaml_lines.append(f"frequency: \"{config['frequency']}\"")

        # Add use-cases
        if 'use-cases' in config:
            yaml_lines.append("use-cases:")
            for case in config['use-cases']:
                yaml_lines.append(f"  - \"{case}\"")

        # Add relationships
        if 'related-agents' in config and config['related-agents']:
            yaml_lines.append("related-agents:")
            for agent in config['related-agents']:
                yaml_lines.append(f"  - {agent}")

        if 'related-skills' in config and config['related-skills']:
            yaml_lines.append("related-skills:")
            for skill in config['related-skills']:
                yaml_lines.append(f"  - {skill}")

        if 'related-commands' in config and config['related-commands']:
            yaml_lines.append("related-commands:")
            for cmd in config['related-commands']:
                yaml_lines.append(f"  - {cmd}")

        # Add dependencies
        yaml_lines.append("dependencies:")
        yaml_lines.append("  tools:")
        for tool in config.get('tools', []):
            yaml_lines.append(f"    - {tool}")
        yaml_lines.append("  scripts:")
        for script in config.get('scripts', []):
            yaml_lines.append(f"    - {script}")
        yaml_lines.append(f"  python-packages: []")

        # Add compatibility
        yaml_lines.append("compatibility:")
        yaml_lines.append("  claude-ai: true")
        yaml_lines.append("  claude-code: true")
        yaml_lines.append("  platforms:")
        yaml_lines.append("    - macos")
        yaml_lines.append("    - linux")
        yaml_lines.append("    - windows")

        # Add examples (min 2)
        yaml_lines.append("examples:")
        for i, example in enumerate(config.get('examples', []), 1):
            yaml_lines.append(f"  - title: \"Example {i}\"")
            yaml_lines.append(f"    input: \"{example.get('input', '')}\"")
            yaml_lines.append(f"    output: \"{example.get('output', '')}\"")

        # Add stats
        yaml_lines.append("stats:")
        yaml_lines.append("  installs: 0")
        yaml_lines.append("  upvotes: 0")
        yaml_lines.append("  rating: 0.0")
        yaml_lines.append("  reviews: 0")

        # Add versioning
        yaml_lines.append(f"version: {config.get('version', 'v1.0.0')}")
        yaml_lines.append(f"author: {config.get('author', 'Claude Skills Team')}")
        if 'contributors' in config and config['contributors']:
            yaml_lines.append("contributors:")
            for contributor in config['contributors']:
                yaml_lines.append(f"  - {contributor}")

        today = datetime.now().strftime('%Y-%m-%d')
        yaml_lines.append(f"created: {today}")
        yaml_lines.append(f"updated: {today}")

        # Add tags
        yaml_lines.append("tags:")
        for tag in config.get('tags', []):
            yaml_lines.append(f"  - {tag}")

        yaml_lines.append(f"featured: {str(config.get('featured', False)).lower()}")
        yaml_lines.append(f"verified: {str(config.get('verified', True)).lower()}")
        yaml_lines.append(f"license: {config.get('license', 'MIT')}")

        yaml_lines.append('---')
        yaml_section = '\n'.join(yaml_lines)

        # Replace first YAML block
        template = re.sub(
            r'^---\n.*?---',
            yaml_section,
            template,
            count=1,
            flags=re.DOTALL | re.MULTILINE
        )

        # Replace command name placeholders
        command_title = config['title']
        template = template.replace('# Command Name', f"# {command_title}")
        template = template.replace('/command-name', f"/{config['name']}")
        template = template.replace('category.command-name', config['name'])

        # Replace pattern placeholder
        pattern = config.get('pattern', 'simple')
        template = template.replace('[Simple | Multi-Phase | Agent-Style]', pattern.title())

        return template


# ============================================================================
# SECTION 6: CATALOG INTEGRATION
# ============================================================================
# Updates commands/CATALOG.md with new command entries

class CatalogUpdater:
    """Update command catalogs"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def append_to_catalog(self, category: str, name: str, description: str) -> None:
        """Append entry to category catalog"""
        catalog_path = self.repo_root / "commands" / category / "CATALOG.md"

        if not catalog_path.exists():
            print(f"⚠️  Warning: {catalog_path} not found")
            return

        # Read existing catalog
        content = catalog_path.read_text()

        # Generate entry
        entry = f"- [{name}]({name}.md) - {description}\n"

        # Find insertion point (end of command list)
        lines = content.split('\n')
        insert_index = -1

        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith('- [') and '.md' in lines[i]:
                insert_index = i + 1
                break

        if insert_index == -1:
            # No existing commands, insert after "## Commands" heading
            for i, line in enumerate(lines):
                if 'Commands' in line and line.startswith('##'):
                    insert_index = i + 2  # Skip heading and blank line
                    break

        if insert_index == -1:
            insert_index = len(lines)

        # Insert entry
        lines.insert(insert_index, entry.rstrip('\n'))

        # Write back
        catalog_path.write_text('\n'.join(lines))

        print(f"✓ Updated {catalog_path}")


# ============================================================================
# SECTION 7: CORE COMMAND BUILDER
# ============================================================================
# Main orchestration logic for command creation and validation

class CommandBuilder:
    """Main orchestrator for command creation"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.validator = CommandValidator(repo_root)
        self.template_loader = TemplateLoader(repo_root)
        self.catalog_updater = CatalogUpdater(repo_root)
        self.category_manager = CategoryManager(repo_root)

    def interactive_mode(self) -> None:
        """Run interactive command creation workflow"""
        print("🔧 Command Builder")
        print("=" * 50)
        print()

        # Step 1: Command Name
        print("Step 1/15: Command Name")
        print("-" * 50)
        print("Enter command name (category.command-name format):")
        print("Example: git.code-review, docs.update-readme")
        print()

        while True:
            name = input("Name: ").strip()
            valid, msg = self.validator.validate_name(name)
            if valid:
                print(f"✓ Valid name format")
                break
            else:
                print(f"❌ {msg}")
                print("Try again:")

        # Extract category from name
        category = name.split('.')[0]
        print()

        # Step 2: Title
        print("Step 2/15: Title")
        print("-" * 50)
        print("Enter human-readable title (10-80 chars):")
        print('Example: "Code Review Assistant", "README Updater"')
        print()

        while True:
            title = input("Title: ").strip()
            if 10 <= len(title) <= 80:
                print(f"✓ Length: {len(title)} chars")
                break
            else:
                print(f"❌ Title must be 10-80 chars (got: {len(title)})")

        print()

        # Step 3: Description
        print("Step 3/15: Description")
        print("-" * 50)
        print("Enter one-line description (max 150 chars):")
        print('Example: "Performs comprehensive code review with quality analysis"')
        print()

        while True:
            description = input("Description: ").strip()
            if len(description) <= 150:
                print(f"✓ Length: {len(description)} chars")
                break
            else:
                print(f"❌ Description too long: {len(description)} chars (max: 150)")

        print()

        # Step 4: Category Verification/Creation
        print("Step 4/15: Category")
        print("-" * 50)

        existing_categories = self.category_manager.get_existing_categories()
        print(f"Category from name: {category}")

        if category in existing_categories:
            print(f"✓ Category exists: {category}")
        else:
            print(f"⚠️  Category '{category}' does not exist")
            confirm = input("Create this category? (y/n): ").strip().lower()
            if confirm == 'y':
                self.category_manager.create_category_directory(category)
            else:
                print("❌ Command creation cancelled")
                sys.exit(0)

        print()

        # Step 5: Subcategory
        print("Step 5/15: Subcategory")
        print("-" * 50)
        print("Enter subcategory (kebab-case, 3-30 chars):")
        print("Example: feature-planning, code-quality, deployment")
        print()

        while True:
            subcategory = input("Subcategory: ").strip()
            if 3 <= len(subcategory) <= 30 and re.match(r'^[a-z][a-z0-9-]*$', subcategory):
                print(f"✓ Valid subcategory")
                break
            else:
                print(f"❌ Subcategory must be 3-30 chars, kebab-case")

        print()

        # Step 6: Pattern
        print("Step 6/15: Pattern")
        print("-" * 50)
        print("Select command pattern:")
        print("1. simple - Straightforward, single-purpose tasks")
        print("2. multi-phase - Complex analysis with multiple steps")
        print("3. agent-style - Specialized expertise with domain perspective")
        print()

        patterns = ['simple', 'multi-phase', 'agent-style']
        while True:
            choice = input("Pattern (1-3): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= 3:
                pattern = patterns[int(choice) - 1]
                print(f"✓ Pattern: {pattern}")
                break
            else:
                print("❌ Invalid selection")

        print()

        # Step 7: Difficulty
        print("Step 7/15: Difficulty")
        print("-" * 50)
        print("Select difficulty level:")
        print("1. beginner - No prerequisites, simple to use")
        print("2. intermediate - Some domain knowledge required")
        print("3. advanced - Expert-level, complex workflows")
        print()

        difficulties = ['beginner', 'intermediate', 'advanced']
        while True:
            choice = input("Difficulty (1-3): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= 3:
                difficulty = difficulties[int(choice) - 1]
                print(f"✓ Difficulty: {difficulty}")
                break
            else:
                print("❌ Invalid selection")

        print()

        # Step 8: Time Saved
        print("Step 8/15: Time Saved")
        print("-" * 50)
        print("Enter estimated time saved per use:")
        print('Example: "15 minutes per use", "2-3 hours per sprint"')
        print()

        time_saved = input("Time saved: ").strip()
        print(f"✓ Time saved: {time_saved}")
        print()

        # Step 9: Frequency
        print("Step 9/15: Frequency of Use")
        print("-" * 50)
        print("Enter typical usage frequency:")
        print('Example: "Weekly per developer", "Daily during sprints"')
        print()

        frequency = input("Frequency: ").strip()
        print(f"✓ Frequency: {frequency}")
        print()

        # Step 10: Use Cases
        print("Step 10/15: Use Cases")
        print("-" * 50)
        print("Enter use cases (minimum 2, press Enter after each, blank to finish):")
        print()

        use_cases = []
        for i in range(1, 6):
            case = input(f"Use case {i}: ").strip()
            if not case:
                if i <= 2:
                    print("❌ Minimum 2 use cases required")
                    continue
                else:
                    break
            use_cases.append(case)
            if len(use_cases) >= 5:
                print("✓ Maximum 5 use cases reached")
                break

        print(f"✓ Added {len(use_cases)} use cases")
        print()

        # Step 11: Related Agents/Skills/Commands
        print("Step 11/15: Related Resources")
        print("-" * 50)
        print("Enter related agents (comma-separated, or press Enter to skip):")
        agents_input = input("Related agents: ").strip()
        related_agents = [a.strip() for a in agents_input.split(',')] if agents_input else []

        print("Enter related skills (comma-separated, or press Enter to skip):")
        skills_input = input("Related skills: ").strip()
        related_skills = [s.strip() for s in skills_input.split(',')] if skills_input else []

        print("Enter related commands (comma-separated, or press Enter to skip):")
        commands_input = input("Related commands: ").strip()
        related_commands = [c.strip() for c in commands_input.split(',')] if commands_input else []

        print(f"✓ Relationships configured")
        print()

        # Step 12: Dependencies
        print("Step 12/15: Dependencies")
        print("-" * 50)
        print("Select tools (comma-separated):")
        print("Available: Read, Write, Bash, Grep, Glob, Edit")
        print()
        print("Default: Read, Write, Bash")

        tools_input = input("Tools (Enter for default): ").strip()

        if tools_input:
            tools = [t.strip() for t in tools_input.split(',')]
        else:
            tools = ['Read', 'Write', 'Bash']

        print(f"✓ Tools: {tools}")

        print()
        print("Enter Python scripts used (comma-separated, or press Enter to skip):")
        scripts_input = input("Scripts: ").strip()
        scripts = [s.strip() for s in scripts_input.split(',')] if scripts_input else []

        print(f"✓ Dependencies configured")
        print()

        # Step 13: Compatibility
        print("Step 13/15: Compatibility")
        print("-" * 50)
        print("Platform support (all by default):")
        print("1. macos, linux, windows (all)")
        print("2. Custom selection")
        print()

        choice = input("Choice (1-2, default=1): ").strip()
        if choice == '2':
            platforms = []
            if input("macOS? (y/n): ").strip().lower() == 'y':
                platforms.append('macos')
            if input("Linux? (y/n): ").strip().lower() == 'y':
                platforms.append('linux')
            if input("Windows? (y/n): ").strip().lower() == 'y':
                platforms.append('windows')
        else:
            platforms = ['macos', 'linux', 'windows']

        print(f"✓ Platforms: {platforms}")
        print()

        # Step 14: Examples
        print("Step 14/15: Examples")
        print("-" * 50)
        print("Provide at least 2 usage examples:")
        print()

        examples = []
        for i in range(1, 6):
            print(f"Example {i}:")
            example_input = input("  Input command: ").strip()
            if not example_input:
                if i <= 2:
                    print("❌ Minimum 2 examples required")
                    continue
                else:
                    break
            example_output = input("  Expected output: ").strip()
            examples.append({'input': example_input, 'output': example_output})
            if len(examples) >= 5:
                print("✓ Maximum 5 examples reached")
                break

        print(f"✓ Added {len(examples)} examples")
        print()

        # Step 15: Tags
        print("Step 15/15: Tags")
        print("-" * 50)
        print("Enter tags for discoverability (comma-separated, minimum 3):")
        print("Example: code-review, quality, automation")
        print()

        while True:
            tags_input = input("Tags: ").strip()
            tags = [t.strip() for t in tags_input.split(',')]
            if len(tags) >= 3:
                print(f"✓ Tags: {tags}")
                break
            else:
                print(f"❌ Minimum 3 tags required (got: {len(tags)})")

        print()

        # Preview and Confirm
        print("Preview")
        print("-" * 50)
        print("Review your command configuration:")
        print()
        print(f"Name:           {name}")
        print(f"Title:          {title}")
        print(f"Category:       {category}")
        print(f"Subcategory:    {subcategory}")
        print(f"Description:    {description}")
        print(f"Pattern:        {pattern}")
        print(f"Difficulty:     {difficulty}")
        print(f"Time saved:     {time_saved}")
        print(f"Frequency:      {frequency}")
        print(f"Use cases:      {len(use_cases)}")
        print(f"Tools:          {tools}")
        print(f"Examples:       {len(examples)}")
        print(f"Tags:           {tags}")
        print()
        print("Files to create:")
        print(f"- commands/{category}/{name}.md")
        print()
        print("Catalog updates:")
        print(f"- commands/{category}/CATALOG.md (append)")
        print()

        confirm = input("Proceed? (y/n): ").strip().lower()

        if confirm != 'y':
            print("❌ Command creation cancelled")
            sys.exit(0)

        # Generate command
        config = {
            'name': name,
            'title': title,
            'category': category,
            'subcategory': subcategory,
            'description': description,
            'pattern': pattern,
            'difficulty': difficulty,
            'time-saved': time_saved,
            'frequency': frequency,
            'use-cases': use_cases,
            'related-agents': related_agents,
            'related-skills': related_skills,
            'related-commands': related_commands,
            'tools': tools,
            'scripts': scripts,
            'examples': examples,
            'tags': tags,
            'version': 'v1.0.0',
            'author': 'Claude Skills Team',
            'featured': False,
            'verified': True,
            'license': 'MIT'
        }

        self.generate_command(config)

    def config_mode(self, config_path: str) -> None:
        """Create command from config file"""
        config_file = Path(config_path)

        if not config_file.exists():
            print(f"❌ Config file not found: {config_path}")
            sys.exit(EXIT_CONFIG_ERROR)

        try:
            with open(config_file, 'r') as f:
                yaml_content = f.read()

            if YAML_AVAILABLE:
                config = yaml.safe_load(yaml_content)
            else:
                # Use simple parser fallback
                config = simple_yaml_parse(yaml_content)
        except Exception as e:
            print(f"❌ Invalid YAML config: {e}")
            sys.exit(EXIT_CONFIG_ERROR)

        # Validate required fields
        required = ['name', 'title', 'category', 'subcategory', 'description']
        missing = [f for f in required if f not in config]

        if missing:
            print(f"❌ Missing required fields in config: {', '.join(missing)}")
            sys.exit(EXIT_CONFIG_ERROR)

        # Set defaults
        if 'pattern' not in config:
            config['pattern'] = 'simple'
        if 'difficulty' not in config:
            config['difficulty'] = 'intermediate'
        if 'tags' not in config:
            config['tags'] = []
        if 'tools' not in config:
            config['tools'] = ['Read', 'Write', 'Bash']
        if 'examples' not in config:
            config['examples'] = []
        if 'use-cases' not in config:
            config['use-cases'] = []

        # Generate command
        self.generate_command(config)

    def validate_existing(self, command_path: str) -> None:
        """Validate an existing command file"""
        path = Path(command_path)

        print(f"✅ Validating: {command_path}")
        print()

        result = self.validator.run_all_checks(path)

        if 'error' in result:
            print(f"❌ {result['error']}")
            sys.exit(EXIT_VALIDATION_FAILED)

        # Print results
        for check in result['checks']:
            status_icon = "✓" if check['status'] == 'passed' else "✗"
            check_name = check['name'].replace('_', ' ').title()
            print(f"{status_icon} Check {result['checks'].index(check) + 1}: {check_name}")
            print(f"   {check['message']}")

        print()

        if result['status'] == 'passed':
            print(f"🎉 Validation passed: {result['checks_passed']}/{result['checks_total']} checks")
            sys.exit(EXIT_SUCCESS)
        else:
            print(f"❌ Validation failed: {result['checks_passed']}/{result['checks_total']} checks passed")
            sys.exit(EXIT_VALIDATION_FAILED)

    def generate_command(self, config: Dict) -> None:
        """Generate command file and update catalogs"""
        # Pre-generation validation
        print()
        print("Validating configuration...")

        # Validate name
        valid, msg = self.validator.validate_name(config['name'])
        if not valid:
            print(f"❌ Invalid name: {msg}")
            sys.exit(EXIT_VALIDATION_FAILED)

        # Check if command already exists
        category = config['name'].split('.')[0]
        command_path = self.repo_root / "commands" / category / f"{config['name']}.md"
        if command_path.exists():
            print(f"❌ Command already exists: {command_path}")
            sys.exit(EXIT_FILE_ERROR)

        # Generate from template
        print("Generating command from template...")
        try:
            content = self.template_loader.populate_template(config)
        except Exception as e:
            print(f"❌ Template generation failed: {e}")
            sys.exit(EXIT_UNKNOWN_ERROR)

        # Write command file
        print("Writing command file...")
        try:
            command_path.parent.mkdir(parents=True, exist_ok=True)
            command_path.write_text(content)
            print(f"✓ Created: {command_path}")
        except Exception as e:
            print(f"❌ Failed to write command file: {e}")
            sys.exit(EXIT_FILE_ERROR)

        # Update catalog
        print("Updating catalog...")
        try:
            self.catalog_updater.append_to_catalog(
                category,
                config['name'],
                config['description']
            )
        except Exception as e:
            print(f"⚠️  Warning: Catalog update failed: {e}")

        # Success!
        print()
        print("✅ Command created successfully!")
        print()
        print(f"📁 Location: {command_path}")
        print()
        print("📝 Next steps:")
        print("   1. Review and customize the template sections")
        print("   2. Add detailed execution steps")
        print("   3. Provide comprehensive examples")
        print("   4. Test the command")
        print("   5. Commit changes:")
        print(f"      git add {command_path}")
        print(f'      git commit -m "feat(commands): add {config["name"]} command"')
        print()


# ============================================================================
# SECTION 8: CLI ENTRY POINT
# ============================================================================
# Command-line argument parsing and mode selection

def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="Command Builder - Interactive CLI for creating slash commands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Interactive mode
  %(prog)s --config command-config.yaml # Config file mode
  %(prog)s --validate commands/git/git.code-review.md  # Validation mode
  %(prog)s --help                       # Show this help

For more information, see docs/standards/command-standards.md
        """
    )

    parser.add_argument(
        '--config',
        help='Config file path (YAML format)'
    )

    parser.add_argument(
        '--validate',
        help='Validate existing command file'
    )

    args = parser.parse_args()

    # Detect repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Initialize builder
    builder = CommandBuilder(repo_root)

    # Route to appropriate mode
    if args.validate:
        builder.validate_existing(args.validate)
    elif args.config:
        builder.config_mode(args.config)
    else:
        builder.interactive_mode()


if __name__ == "__main__":
    main()
