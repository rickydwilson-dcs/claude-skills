#!/usr/bin/env python3
"""
Export Catalog JSON Generator

Generates website API JSON from repository .md files with YAML frontmatter.
Parses commands/**/*.md and outputs JSON conforming to json-export-schema.json.

Features:
  - Parse YAML frontmatter from markdown files
  - Convert to JSON schema structure
  - Generate api/commands.json and api/catalog.json
  - Fast parsing (< 10 seconds for 30+ commands)
  - Comprehensive error handling
  - CLI interface with filtering options

Usage:
    python3 export_catalog_json.py                    # Export all
    python3 export_catalog_json.py --type commands    # Export specific type
    python3 export_catalog_json.py --verbose          # Verbose output
    python3 export_catalog_json.py --help             # Show help
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
import re

# Exit codes
EXIT_SUCCESS = 0
EXIT_PARSE_ERROR = 1
EXIT_FILE_ERROR = 2
EXIT_CONFIG_ERROR = 3
EXIT_VALIDATION_ERROR = 4
EXIT_UNKNOWN_ERROR = 99


def get_utc_timestamp() -> str:
    """Get ISO 8601 UTC timestamp compatible with Python 3.8+"""
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


class YAMLFrontmatterParser:
    """Parse YAML frontmatter from markdown files (stdlib only)"""

    @staticmethod
    def extract_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
        """
        Extract YAML frontmatter from markdown content.

        Returns:
            Tuple of (frontmatter_dict, body_content) or (None, original_content) if no frontmatter
        """
        if not content.startswith('---'):
            return None, content

        lines = content.split('\n')
        if len(lines) < 3:
            return None, content

        # Find closing ---
        end_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break

        if end_idx is None:
            return None, content

        yaml_str = '\n'.join(lines[1:end_idx])
        body = '\n'.join(lines[end_idx + 1:])

        frontmatter = YAMLFrontmatterParser.parse_yaml(yaml_str)
        return frontmatter, body

    @staticmethod
    def parse_yaml(yaml_str: str) -> Dict:
        """
        Simple YAML parser for frontmatter (standard library only).

        Handles:
        - Key-value pairs
        - Lists (both - item format and [item1, item2] format)
        - Strings, numbers, booleans
        - Nested objects (one level only)
        """
        result = {}
        lines = yaml_str.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                i += 1
                continue

            # Determine indentation level
            indent = len(line) - len(line.lstrip())

            # Top-level key (no indentation)
            if indent == 0 and ':' in stripped:
                key, value = stripped.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Inline list [item1, item2]
                if value.startswith('[') and value.endswith(']'):
                    items = value[1:-1].split(',')
                    result[key] = [item.strip().strip('"\'') for item in items]
                    i += 1

                # Empty value - check what comes next
                elif not value:
                    # Look ahead to determine if this is a list or nested dict
                    i += 1
                    if i < len(lines):
                        lookahead_line = lines[i]
                        lookahead_stripped = lookahead_line.strip()
                        lookahead_indent = len(lookahead_line) - len(lookahead_line.lstrip())

                        # List of items (starts with -)
                        if lookahead_stripped.startswith('- '):
                            item_list = []
                            while i < len(lines):
                                item_line = lines[i]
                                item_stripped = item_line.strip()
                                item_indent = len(item_line) - len(item_line.lstrip())

                                # Exit if back to top level or found a key
                                if item_indent == 0:
                                    i -= 1
                                    break
                                # Exit if found a sibling key at same indent level
                                if item_indent == 2 and ':' in item_stripped and not item_stripped.startswith('- '):
                                    i -= 1
                                    break

                                if item_stripped.startswith('- '):
                                    item = item_stripped[2:].strip().strip('"\'')
                                    if item:
                                        item_list.append(item)

                                i += 1

                            result[key] = item_list

                        # Nested dict
                        elif ':' in lookahead_stripped:
                            nested_dict = {}
                            while i < len(lines):
                                nested_line = lines[i]
                                nested_stripped = nested_line.strip()
                                nested_indent = len(nested_line) - len(nested_line.lstrip())

                                # Exit if back to top level
                                if nested_indent == 0:
                                    i -= 1
                                    break
                                # Skip empty lines
                                if not nested_stripped:
                                    i += 1
                                    continue

                                # Process nested key
                                if ':' in nested_stripped:
                                    subkey, subvalue = nested_stripped.split(':', 1)
                                    subkey = subkey.strip()
                                    subvalue = subvalue.strip()

                                    # Nested inline list
                                    if subvalue.startswith('[') and subvalue.endswith(']'):
                                        items = subvalue[1:-1].split(',')
                                        nested_dict[subkey] = [item.strip().strip('"\'') for item in items]
                                    # Nested empty value - collect list
                                    elif not subvalue:
                                        nested_list = []
                                        i += 1
                                        while i < len(lines):
                                            list_line = lines[i]
                                            list_stripped = list_line.strip()
                                            list_indent = len(list_line) - len(list_line.lstrip())

                                            if list_indent <= nested_indent:
                                                i -= 1
                                                break

                                            if list_stripped.startswith('- '):
                                                item = list_stripped[2:].strip().strip('"\'')
                                                if item:
                                                    nested_list.append(item)

                                            i += 1

                                        nested_dict[subkey] = nested_list
                                    # Simple nested value
                                    else:
                                        nested_dict[subkey] = YAMLFrontmatterParser.parse_value(subvalue)

                                i += 1

                            result[key] = nested_dict
                        else:
                            i -= 1

                # Simple value
                else:
                    # Remove quotes
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    result[key] = YAMLFrontmatterParser.parse_value(value)
                    i += 1

            else:
                i += 1

        return result

    @staticmethod
    def parse_value(value: str) -> Any:
        """Parse YAML value to appropriate Python type"""
        if value.lower() in ('true', 'yes'):
            return True
        elif value.lower() in ('false', 'no'):
            return False
        elif value.lower() in ('null', 'none', '~'):
            return None

        # Try to parse as number
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass

        return value


class CommandMetadataMapper:
    """Map command YAML metadata to JSON schema structure"""

    # Field mapping from YAML to JSON schema
    FIELD_MAPPINGS = {
        # Core identity
        'name': 'name',
        'title': 'title',
        'description': 'description',
        'category': 'category',
        'subcategory': 'subcategory',

        # Display
        'difficulty': 'difficulty',
        'time-saved': 'time_saved',
        'time_saved': 'time_saved',
        'frequency': 'frequency',
        'use-cases': 'use_cases',
        'use_cases': 'use_cases',

        # Relationships
        'related-agents': 'related_agents',
        'related_agents': 'related_agents',
        'related-skills': 'related_skills',
        'related_skills': 'related_skills',
        'related-commands': 'related_commands',
        'related_commands': 'related_commands',

        # Technical
        'dependencies': 'dependencies',
        'compatibility': 'compatibility',

        # Examples
        'examples': 'examples',

        # Analytics
        'stats': 'stats',

        # Versioning
        'version': 'version',
        'author': 'author',
        'contributors': 'contributors',
        'created': 'created',
        'updated': 'updated',

        # Discoverability
        'tags': 'tags',
        'featured': 'featured',
        'verified': 'verified',
        'license': 'license',
    }

    @staticmethod
    def normalize_field_name(name: str) -> str:
        """Normalize field name: kebab-case -> snake_case"""
        return name.replace('-', '_')

    @staticmethod
    def map_to_json_schema(yaml_data: Dict) -> Dict:
        """
        Convert YAML frontmatter to JSON schema structure.

        Args:
            yaml_data: Parsed YAML frontmatter

        Returns:
            JSON object conforming to json-export-schema.json
        """
        # Normalize YAML keys to snake_case
        normalized = {}
        for key, value in yaml_data.items():
            normalized_key = CommandMetadataMapper.normalize_field_name(key)
            normalized[normalized_key] = value

        # Build JSON structure
        json_obj = {
            "metadata": {
                "schema_version": "v1.0.0",
                "export_timestamp": get_utc_timestamp(),
                "api_version": "v1"
            },
            "core": {
                "name": normalized.get("name", ""),
                "title": normalized.get("title", ""),
                "description": normalized.get("description", ""),
                "category": normalized.get("category", ""),
                "subcategory": normalized.get("subcategory", "")
            },
            "display": {
                "difficulty": normalized.get("difficulty", "beginner"),
                "time_saved": normalized.get("time_saved", ""),
                "frequency": normalized.get("frequency", ""),
                "use_cases": normalized.get("use_cases", [])
            },
            "relationships": {
                "related_agents": normalized.get("related_agents", []),
                "related_skills": normalized.get("related_skills", []),
                "related_commands": normalized.get("related_commands", [])
            },
            "technical": {
                "dependencies": CommandMetadataMapper.normalize_dependencies(
                    normalized.get("dependencies", {})
                ),
                "compatibility": CommandMetadataMapper.normalize_compatibility(
                    normalized.get("compatibility", {})
                )
            },
            "examples": CommandMetadataMapper.normalize_examples(
                normalized.get("examples", [])
            ),
            "analytics": {
                "installs": 0,
                "upvotes": 0,
                "rating": 0.0,
                "reviews": 0
            },
            "versioning": {
                "version": normalized.get("version", "v1.0.0"),
                "author": normalized.get("author", "Claude Skills Team"),
                "contributors": normalized.get("contributors", []),
                "created": normalized.get("created", ""),
                "updated": normalized.get("updated", "")
            },
            "discoverability": {
                "tags": normalized.get("tags", []),
                "featured": normalized.get("featured", False),
                "verified": normalized.get("verified", True),
                "license": normalized.get("license", "MIT")
            }
        }

        return json_obj

    @staticmethod
    def normalize_dependencies(deps: Any) -> Dict:
        """Normalize dependencies structure"""
        if isinstance(deps, dict):
            return {
                "tools": deps.get("tools", []) if isinstance(deps.get("tools"), list) else [],
                "scripts": deps.get("scripts", []) if isinstance(deps.get("scripts"), list) else [],
                "python_packages": deps.get("python_packages", deps.get("python-packages", []))
            }
        return {"tools": [], "scripts": [], "python_packages": []}

    @staticmethod
    def normalize_compatibility(compat: Any) -> Dict:
        """Normalize compatibility structure"""
        if isinstance(compat, dict):
            platforms = compat.get("platforms", [])
            if not isinstance(platforms, list):
                platforms = [platforms] if platforms else []
            return {
                "claude_ai": compat.get("claude_ai", compat.get("claude-ai", True)),
                "claude_code": compat.get("claude_code", compat.get("claude-code", True)),
                "platforms": platforms
            }
        return {"claude_ai": True, "claude_code": True, "platforms": ["macos", "linux", "windows"]}

    @staticmethod
    def normalize_examples(examples: Any) -> List[Dict]:
        """Normalize examples structure"""
        if not isinstance(examples, list):
            return []

        normalized = []
        for ex in examples:
            if isinstance(ex, dict):
                normalized.append({
                    "title": ex.get("title", ""),
                    "input": ex.get("input", ""),
                    "output": ex.get("output", "")
                })
        return normalized


class CatalogExporter:
    """Export commands catalog to JSON files"""

    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.commands_dir = repo_root / "commands"
        self.api_dir = repo_root / "api"
        self.verbose = verbose
        self.errors = []
        self.warnings = []

    def ensure_api_dir(self):
        """Create api directory if it doesn't exist"""
        self.api_dir.mkdir(parents=True, exist_ok=True)
        if self.verbose:
            print(f"Ensured api directory: {self.api_dir}")

    def find_command_files(self) -> List[Path]:
        """Find all command markdown files"""
        command_files = []

        if not self.commands_dir.exists():
            self.warnings.append(f"Commands directory not found: {self.commands_dir}")
            return command_files

        # Find all .md files in commands directory (excluding CATALOG.md and CLAUDE.md)
        for md_file in self.commands_dir.glob("**/*.md"):
            if md_file.name not in ("CATALOG.md", "CLAUDE.md"):
                command_files.append(md_file)

        if self.verbose:
            print(f"Found {len(command_files)} command files")

        return sorted(command_files)

    def parse_command_file(self, file_path: Path) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Parse a command file and extract metadata.

        Returns:
            Tuple of (json_object, error_message) or (json_object, None) if successful
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract YAML frontmatter
            frontmatter, body = YAMLFrontmatterParser.extract_frontmatter(content)

            if frontmatter is None:
                error = f"No YAML frontmatter found in {file_path.name}"
                self.errors.append(error)
                return None, error

            # Map to JSON schema
            json_obj = CommandMetadataMapper.map_to_json_schema(frontmatter)

            # Validate required fields
            validation_error = self.validate_command_json(json_obj)
            if validation_error:
                self.warnings.append(f"{file_path.name}: {validation_error}")

            if self.verbose:
                print(f"✓ Parsed {file_path.name}: {json_obj['core'].get('name', 'unknown')}")

            return json_obj, None

        except Exception as e:
            error = f"Error parsing {file_path.name}: {str(e)}"
            self.errors.append(error)
            return None, error

    @staticmethod
    def validate_command_json(json_obj: Dict) -> Optional[str]:
        """
        Validate command JSON structure.

        Returns:
            Error message if invalid, None if valid
        """
        # Check required core fields
        core = json_obj.get("core", {})
        required_core = ["name", "title", "description", "category", "subcategory"]
        for field in required_core:
            if not core.get(field):
                return f"Missing required field: core.{field}"

        # Check required display fields
        display = json_obj.get("display", {})
        required_display = ["difficulty", "time_saved", "frequency", "use_cases"]
        for field in required_display:
            if field not in display:
                return f"Missing required field: display.{field}"

        # Check valid difficulty
        if display.get("difficulty") not in ("beginner", "intermediate", "advanced"):
            return f"Invalid difficulty: {display.get('difficulty')}"

        # Check minimum use cases
        use_cases = display.get("use_cases", [])
        if not isinstance(use_cases, list) or len(use_cases) < 1:
            return f"Must have at least 1 use case (found {len(use_cases)})"

        # Check examples
        examples = json_obj.get("examples", [])
        if not isinstance(examples, list) or len(examples) < 1:
            return f"Must have at least 1 example (found {len(examples)})"

        # Check tags
        tags = json_obj.get("discoverability", {}).get("tags", [])
        if not isinstance(tags, list) or len(tags) < 1:
            return f"Must have at least 1 tag (found {len(tags)})"

        return None

    def export_commands_json(self) -> Tuple[int, int, int]:
        """
        Export all commands to JSON.

        Returns:
            Tuple of (total_found, successfully_parsed, failed)
        """
        self.ensure_api_dir()

        # Find all command files
        command_files = self.find_command_files()
        total_found = len(command_files)

        # Parse each file
        commands = []
        failed = 0

        for file_path in command_files:
            json_obj, error = self.parse_command_file(file_path)
            if error:
                failed += 1
            else:
                commands.append(json_obj)

        successfully_parsed = len(commands)

        # Create catalog structure
        catalog = {
            "metadata": {
                "schema_version": "v1.0.0",
                "export_timestamp": get_utc_timestamp(),
                "api_version": "v1",
                "total_commands": successfully_parsed,
                "last_updated": get_utc_timestamp(),
                "version": "1.0.0"
            },
            "commands": commands
        }

        # Write commands.json
        commands_json_path = self.api_dir / "commands.json"
        with open(commands_json_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)

        if self.verbose:
            print(f"✓ Exported {commands_json_path}")

        # Write catalog.json (same structure for now, can be extended)
        catalog_json_path = self.api_dir / "catalog.json"
        with open(catalog_json_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)

        if self.verbose:
            print(f"✓ Exported {catalog_json_path}")

        return total_found, successfully_parsed, failed

    def print_summary(self, total_found: int, successfully_parsed: int, failed: int):
        """Print export summary"""
        print("\n" + "=" * 60)
        print("CATALOG EXPORT SUMMARY")
        print("=" * 60)
        print(f"Total files found:     {total_found}")
        print(f"Successfully parsed:   {successfully_parsed}")
        print(f"Failed:                {failed}")

        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for error in self.errors[:10]:  # Show first 10
                print(f"  ✗ {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more")

        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"  ⚠ {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")

        print(f"\nExported to: {self.api_dir}")
        print("  - api/commands.json")
        print("  - api/catalog.json")
        print("=" * 60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Export catalog JSON from repository command files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 export_catalog_json.py              # Export all with summary
  python3 export_catalog_json.py --verbose    # Verbose output
  python3 export_catalog_json.py --type commands  # Export specific type
        """
    )

    parser.add_argument(
        "--type",
        choices=["commands", "all"],
        default="commands",
        help="Type of catalog to export (default: commands)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress summary output"
    )

    args = parser.parse_args()

    # Find repository root
    repo_root = Path(__file__).parent.parent

    try:
        # Create exporter
        exporter = CatalogExporter(repo_root, verbose=args.verbose)

        # Export based on type
        if args.type in ("commands", "all"):
            total_found, successfully_parsed, failed = exporter.export_commands_json()

            if not args.quiet:
                exporter.print_summary(total_found, successfully_parsed, failed)

            # Return appropriate exit code
            if failed > 0 and failed == total_found:
                return EXIT_PARSE_ERROR
            elif failed > 0:
                return EXIT_VALIDATION_ERROR

        return EXIT_SUCCESS

    except KeyboardInterrupt:
        print("\nExport cancelled by user")
        return EXIT_UNKNOWN_ERROR
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return EXIT_UNKNOWN_ERROR


if __name__ == "__main__":
    sys.exit(main())
