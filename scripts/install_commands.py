#!/usr/bin/env python3
"""
Command Installation Tool - Interactive command installer for Claude Code

This tool provides an easy way to install slash commands from the claude-skills
library to a user's .claude/commands/ directory with interactive selection,
dependency checking, and manifest tracking.

Usage:
    python3 scripts/install_commands.py                     # Interactive mode
    python3 scripts/install_commands.py --list              # List all commands
    python3 scripts/install_commands.py --command workflow.update-docs
    python3 scripts/install_commands.py --category workflow
    python3 scripts/install_commands.py --dry-run           # Preview changes
    python3 scripts/install_commands.py --help              # Show help
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
from collections import defaultdict


# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_FAILED = 1
EXIT_FILE_ERROR = 2
EXIT_USER_CANCEL = 3
EXIT_UNKNOWN_ERROR = 99


class CommandMetadata:
    """Parse and manage command metadata from YAML frontmatter"""

    @staticmethod
    def parse(file_path: Path) -> Optional[Dict]:
        """Parse YAML frontmatter from command file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract YAML frontmatter (between --- markers)
            if not content.startswith('---'):
                return None

            end_marker = content.find('---', 3)
            if end_marker == -1:
                return None

            yaml_content = content[3:end_marker].strip()
            metadata = CommandMetadata._parse_yaml(yaml_content)

            # Extract command name from filename if not in metadata
            if 'name' not in metadata:
                metadata['name'] = file_path.stem

            # Add file path
            metadata['file_path'] = str(file_path)

            return metadata

        except Exception as e:
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)
            return None

    @staticmethod
    def _parse_yaml(yaml_str: str) -> Dict:
        """Simple YAML parser for command frontmatter (stdlib only)"""
        result = {}
        current_key = None
        list_items = []

        for line in yaml_str.split('\n'):
            line = line.rstrip()

            if not line or line.startswith('#'):
                continue

            # List item
            if line.startswith('- '):
                item = line[2:].strip()
                list_items.append(item)
                continue

            # Key-value pair
            if ':' in line:
                # Save previous list if any
                if current_key and list_items:
                    result[current_key] = list_items
                    list_items = []

                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Handle inline lists [item1, item2]
                if value.startswith('[') and value.endswith(']'):
                    items = value[1:-1].split(',')
                    result[key] = [item.strip() for item in items]
                    current_key = None
                # Empty value - expect list on next lines
                elif not value:
                    current_key = key
                # Simple value
                else:
                    result[key] = value
                    current_key = None

        # Save final list if any
        if current_key and list_items:
            result[current_key] = list_items

        return result


class CommandCatalog:
    """Manage command discovery and categorization"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.commands_dir = repo_root / "commands"
        self.library_dir = repo_root / ".claude" / "commands"
        self.commands: Dict[str, Dict] = {}
        self.categories: Dict[str, List[str]] = defaultdict(list)
        self._discover_commands()

    def _discover_commands(self) -> None:
        """Discover all available commands in commands/ and .claude/commands/ directories"""
        # First check commands/ (template library)
        if self.commands_dir.exists():
            self._discover_from_directory(self.commands_dir)

        # Then check .claude/commands/ (fallback source)
        if self.library_dir.exists():
            self._discover_from_directory(self.library_dir)

    def _discover_from_directory(self, directory: Path) -> None:
        """Discover commands from a specific directory"""
        for md_file in directory.glob("*.md"):
            # Skip non-command files
            if md_file.name in ("CATALOG.md", "CLAUDE.md", "manifest.json"):
                continue

            metadata = CommandMetadata.parse(md_file)
            if metadata:
                cmd_name = metadata.get('name', md_file.stem)
                category = metadata.get('category', 'general')

                # Don't overwrite if already discovered from primary location
                if cmd_name not in self.commands:
                    self.commands[cmd_name] = metadata
                    self.categories[category].append(cmd_name)

    def get_all_categories(self) -> List[str]:
        """Get all available categories, sorted"""
        return sorted(self.categories.keys())

    def get_category_commands(self, category: str) -> List[Dict]:
        """Get all commands in a category"""
        cmd_names = self.categories.get(category, [])
        return [self.commands[name] for name in sorted(cmd_names)]

    def get_command(self, name: str) -> Optional[Dict]:
        """Get command metadata by name"""
        return self.commands.get(name)

    def get_all_commands(self) -> List[Dict]:
        """Get all commands, sorted by category then name"""
        commands = list(self.commands.values())
        return sorted(
            commands,
            key=lambda c: (c.get('category', 'general'), c.get('name', ''))
        )

    def search_commands(self, query: str) -> List[Dict]:
        """Search commands by name or description"""
        query_lower = query.lower()
        results = []

        for cmd in self.commands.values():
            name = cmd.get('name', '').lower()
            desc = cmd.get('description', '').lower()

            if query_lower in name or query_lower in desc:
                results.append(cmd)

        return sorted(results, key=lambda c: c.get('name', ''))


class CommandInstaller:
    """Manage command installation to .claude/commands/"""

    def __init__(self, target_dir: Optional[Path] = None):
        """Initialize installer with target directory"""
        if target_dir is None:
            # Default to ~/.claude/commands/
            target_dir = Path.home() / ".claude" / "commands"

        self.target_dir = Path(target_dir)
        self.manifest_path = self.target_dir / "manifest.json"
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> Dict:
        """Load manifest.json or create new one"""
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load manifest: {e}", file=sys.stderr)
                return self._empty_manifest()
        else:
            return self._empty_manifest()

    @staticmethod
    def _empty_manifest() -> Dict:
        """Create empty manifest structure"""
        return {
            "installed": [],
            "lastSync": None,
            "version": "1.0.0"
        }

    def save_manifest(self) -> bool:
        """Save manifest to disk"""
        try:
            self.target_dir.mkdir(parents=True, exist_ok=True)

            # Update lastSync timestamp
            self.manifest["lastSync"] = datetime.now().isoformat() + "Z"

            with open(self.manifest_path, 'w') as f:
                json.dump(self.manifest, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving manifest: {e}", file=sys.stderr)
            return False

    def is_installed(self, command_name: str) -> bool:
        """Check if command is already installed"""
        installed_names = [c['name'] for c in self.manifest.get('installed', [])]
        return command_name in installed_names

    def get_installed_commands(self) -> List[Dict]:
        """Get list of installed commands"""
        return self.manifest.get('installed', [])

    def install_commands(
        self,
        commands: List[Dict],
        overwrite: bool = False,
        dry_run: bool = False,
        show_progress: bool = True
    ) -> Tuple[int, List[str], List[str]]:
        """
        Install multiple commands

        Returns:
            Tuple of (success_count, installed_names, errors)
        """
        installed = []
        errors = []
        success_count = 0

        # Create target directory if needed
        if not dry_run:
            try:
                self.target_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Failed to create target directory: {e}")
                return 0, [], errors

        # Install each command
        for cmd in commands:
            result = self._install_single(cmd, overwrite, dry_run, show_progress)
            if result['success']:
                installed.append(cmd['name'])
                success_count += 1
            else:
                errors.append(result['error'])

        # Update manifest
        if not dry_run and installed:
            self._update_manifest(commands, installed)

        return success_count, installed, errors

    def _install_single(
        self,
        cmd: Dict,
        overwrite: bool,
        dry_run: bool,
        show_progress: bool
    ) -> Dict:
        """Install a single command"""
        try:
            source_path = Path(cmd['file_path'])
            target_path = self.target_dir / source_path.name
            cmd_name = cmd['name']

            # Check if already installed
            if target_path.exists() and not overwrite:
                return {
                    'success': False,
                    'error': f"Already installed: {cmd_name} (use --overwrite to update)"
                }

            if show_progress:
                status = "[DRY RUN] " if dry_run else ""
                print(f"✓ Installing {status}{cmd_name} → {target_path.name}")

            if dry_run:
                return {'success': True}

            # Copy file
            shutil.copy2(source_path, target_path)
            return {'success': True}

        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to install {cmd.get('name', 'unknown')}: {e}"
            }

    def _update_manifest(self, commands: List[Dict], installed: List[str]) -> None:
        """Update manifest with installed commands"""
        installed_set = set(installed)

        for cmd in commands:
            if cmd['name'] in installed_set:
                # Check if already in manifest
                existing = [c for c in self.manifest['installed'] if c['name'] == cmd['name']]

                if existing:
                    # Update existing entry
                    existing[0].update({
                        'installedAt': datetime.now().isoformat() + "Z",
                        'version': cmd.get('version', '1.0.0'),
                    })
                else:
                    # Add new entry
                    self.manifest['installed'].append({
                        'name': cmd['name'],
                        'version': cmd.get('version', '1.0.0'),
                        'category': cmd.get('category', 'general'),
                        'installedAt': datetime.now().isoformat() + "Z",
                        'source': 'claude-skills',
                        'description': cmd.get('description', '')
                    })

        self.save_manifest()


class InteractiveUI:
    """Provide interactive UI for command selection"""

    @staticmethod
    def prompt_yes_no(question: str) -> bool:
        """Prompt user for yes/no answer"""
        while True:
            answer = input(f"{question} (y/n): ").lower().strip()
            if answer in ('y', 'yes'):
                return True
            elif answer in ('n', 'no'):
                return False
            else:
                print("Please enter 'y' or 'n'")

    @staticmethod
    def prompt_number(prompt: str, min_val: int = 1, max_val: Optional[int] = None) -> Optional[int]:
        """Prompt user for a number"""
        while True:
            try:
                value = int(input(prompt))
                if value < min_val:
                    print(f"Please enter a number >= {min_val}")
                    continue
                if max_val and value > max_val:
                    print(f"Please enter a number <= {max_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number")

    @staticmethod
    def select_from_list(
        items: List[str],
        title: str = "Select an option",
        allow_multiple: bool = False
    ) -> Optional[List[str]]:
        """Interactive list selection"""
        if not items:
            print("No items to select from")
            return []

        print(f"\n{title}:")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")

        if allow_multiple:
            print("  (Enter comma-separated numbers, e.g., '1,3,5' or '1' for single)")
            selection = input("Your selection: ").strip()

            if not selection:
                return []

            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                selected = [items[i] for i in indices if 0 <= i < len(items)]
                return selected
            except (ValueError, IndexError):
                print("Invalid selection")
                return None
        else:
            choice = InteractiveUI.prompt_number(
                "Your selection: ",
                min_val=1,
                max_val=len(items)
            )
            if choice is None:
                return None
            return [items[choice - 1]]

    @staticmethod
    def display_command_details(cmd: Dict) -> None:
        """Display detailed command information"""
        print(f"\n  Name: {cmd.get('name', 'N/A')}")
        print(f"  Category: {cmd.get('category', 'N/A')}")
        print(f"  Version: {cmd.get('version', '1.0.0')}")
        print(f"  Description: {cmd.get('description', 'N/A')}")

        if 'pattern' in cmd:
            print(f"  Pattern: {cmd['pattern']}")

        if 'tools_required' in cmd:
            print(f"  Tools: {', '.join(cmd['tools_required'])}")

        if 'estimated_time' in cmd:
            print(f"  Estimated Time: {cmd['estimated_time']}")

        if cmd.get('dangerous', False):
            print("  ⚠️  Dangerous: This command modifies files")

        if cmd.get('requires_input', False):
            print("  ℹ️  Requires Input: This command needs arguments")

        if cmd.get('interactive', False):
            print("  ℹ️  Interactive: This command prompts during execution")

    @staticmethod
    def display_installation_summary(
        installed: List[str],
        skipped: List[Tuple[str, str]],
        errors: List[str]
    ) -> None:
        """Display installation summary"""
        print("\n" + "=" * 60)
        print("INSTALLATION SUMMARY")
        print("=" * 60)

        if installed:
            print(f"\n✓ Successfully installed ({len(installed)}):")
            for name in installed:
                print(f"  • {name}")

        if skipped:
            print(f"\n⊘ Skipped ({len(skipped)}):")
            for name, reason in skipped:
                print(f"  • {name}: {reason}")

        if errors:
            print(f"\n✗ Errors ({len(errors)}):")
            for error in errors:
                print(f"  • {error}")

        print("\n" + "=" * 60)


class CommandInstallationFlow:
    """Orchestrate interactive installation flow"""

    def __init__(self, repo_root: Path, target_dir: Optional[Path] = None):
        self.repo_root = repo_root
        self.catalog = CommandCatalog(repo_root)
        self.installer = CommandInstaller(target_dir)
        self.ui = InteractiveUI()

    def run_interactive(self) -> bool:
        """Run interactive installation flow"""
        print("\n" + "=" * 60)
        print("COMMAND INSTALLATION TOOL")
        print("=" * 60)

        # Step 1: Select category
        all_categories = self.catalog.get_all_categories()
        if not all_categories:
            print("No commands available to install")
            return False

        categories = ["All Commands"] + all_categories
        selected_cat = self.ui.select_from_list(
            categories,
            "Step 1: Select category to browse"
        )

        if not selected_cat:
            print("Installation cancelled")
            return False

        # Get commands for selected category
        if selected_cat[0] == "All Commands":
            commands = self.catalog.get_all_commands()
        else:
            commands = self.catalog.get_category_commands(selected_cat[0])

        if not commands:
            print("No commands in this category")
            return False

        # Step 2: Display and select commands
        print(f"\nStep 2: Select commands to install ({len(commands)} available)")

        # Format command display
        command_displays = []
        for cmd in commands:
            display = f"{cmd['name']} - {cmd.get('description', 'N/A')[:50]}"
            command_displays.append(display)
            self.ui.display_command_details(cmd)

        print()
        selected_displays = self.ui.select_from_list(
            command_displays,
            "Select commands (comma-separated for multiple)",
            allow_multiple=True
        )

        if not selected_displays:
            print("No commands selected")
            return False

        # Extract selected commands
        selected_indices = [
            command_displays.index(d) for d in selected_displays
        ]
        selected_commands = [commands[i] for i in selected_indices]

        # Step 3: Check for conflicts
        conflicts = []
        for cmd in selected_commands:
            if self.installer.is_installed(cmd['name']):
                conflicts.append(cmd['name'])

        if conflicts:
            print(f"\nWarning: {len(conflicts)} command(s) already installed:")
            for name in conflicts:
                print(f"  • {name}")

            if not self.ui.prompt_yes_no("Overwrite existing commands?"):
                print("Installation cancelled")
                return False
            overwrite = True
        else:
            overwrite = False

        # Step 4: Summary and confirmation
        print("\n" + "=" * 60)
        print("INSTALLATION SUMMARY")
        print("=" * 60)
        print(f"Commands to install: {len(selected_commands)}")
        for cmd in selected_commands:
            status = "(update)" if self.installer.is_installed(cmd['name']) else "(new)"
            print(f"  • {cmd['name']} {status}")

        print(f"Target directory: {self.installer.target_dir}")

        if not self.ui.prompt_yes_no("\nProceed with installation?"):
            print("Installation cancelled")
            return False

        # Step 5: Install commands
        success_count, installed, errors = self.installer.install_commands(
            selected_commands,
            overwrite=overwrite,
            show_progress=True
        )

        # Step 6: Report results
        skipped = [(cmd['name'], "Already installed") for cmd in selected_commands
                   if cmd['name'] not in installed and not errors]

        self.ui.display_installation_summary(installed, skipped, errors)

        return success_count > 0

    def run_list_mode(self, category: Optional[str] = None) -> bool:
        """List available commands"""
        print("\n" + "=" * 60)
        print("AVAILABLE COMMANDS")
        print("=" * 60)

        if category:
            commands = self.catalog.get_category_commands(category)
            if not commands:
                print(f"No commands in category: {category}")
                return False
            print(f"\nCategory: {category}")
        else:
            commands = self.catalog.get_all_commands()

        if not commands:
            print("No commands available")
            return False

        # Group by category
        by_category = defaultdict(list)
        for cmd in commands:
            cat = cmd.get('category', 'general')
            by_category[cat].append(cmd)

        for cat in sorted(by_category.keys()):
            print(f"\n{cat.upper()} ({len(by_category[cat])}):")
            for cmd in sorted(by_category[cat], key=lambda c: c.get('name', '')):
                installed = "✓" if self.installer.is_installed(cmd['name']) else " "
                print(f"  [{installed}] {cmd['name']:<30} - {cmd.get('description', '')[:45]}")

        print("\n[✓] = Already installed")
        return True

    def run_install_command(
        self,
        command_name: str,
        overwrite: bool = False,
        dry_run: bool = False
    ) -> bool:
        """Install specific command"""
        cmd = self.catalog.get_command(command_name)
        if not cmd:
            print(f"Command not found: {command_name}")
            return False

        print(f"\nInstalling {command_name}...")
        self.ui.display_command_details(cmd)

        success_count, installed, errors = self.installer.install_commands(
            [cmd],
            overwrite=overwrite,
            dry_run=dry_run,
            show_progress=True
        )

        if errors:
            print(f"\nErrors:")
            for error in errors:
                print(f"  • {error}")
            return False

        if installed:
            if dry_run:
                print(f"\n✓ Would install: {command_name}")
            else:
                print(f"\n✓ Successfully installed: {command_name}")
            print(f"  Location: {self.installer.target_dir / cmd['file_path'].split('/')[-1]}")
            return True

        return False

    def run_install_category(
        self,
        category: str,
        overwrite: bool = False,
        dry_run: bool = False
    ) -> bool:
        """Install all commands in a category"""
        commands = self.catalog.get_category_commands(category)
        if not commands:
            print(f"No commands in category: {category}")
            return False

        print(f"\nInstalling all {len(commands)} commands in '{category}'...")

        success_count, installed, errors = self.installer.install_commands(
            commands,
            overwrite=overwrite,
            dry_run=dry_run,
            show_progress=True
        )

        skipped = [(cmd['name'], "Already installed") for cmd in commands
                   if cmd['name'] not in installed and not errors]

        self.ui.display_installation_summary(installed, skipped, errors)
        return success_count > 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Interactive command installation tool for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  python3 scripts/install_commands.py

  # List all available commands
  python3 scripts/install_commands.py --list

  # List commands in category
  python3 scripts/install_commands.py --list --category workflow

  # Install specific command
  python3 scripts/install_commands.py --command workflow.update-docs

  # Install all in category
  python3 scripts/install_commands.py --category workflow

  # Preview changes without installing
  python3 scripts/install_commands.py --dry-run

  # Overwrite existing commands
  python3 scripts/install_commands.py --command workflow.update-docs --overwrite
        """
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available commands'
    )

    parser.add_argument(
        '--command',
        type=str,
        help='Install specific command (e.g., workflow.update-docs)'
    )

    parser.add_argument(
        '--category',
        type=str,
        help='Install all commands in category or list by category'
    )

    parser.add_argument(
        '--target',
        type=str,
        help='Target directory for installation (default: ~/.claude/commands/)'
    )

    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing commands'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without installing'
    )

    parser.add_argument(
        '--search',
        type=str,
        help='Search for commands by name or description'
    )

    args = parser.parse_args()

    # Find repository root
    repo_root = Path(__file__).parent.parent
    if not (repo_root / "commands").exists():
        print("Error: commands/ directory not found. Are you in the claude-skills repository?")
        sys.exit(EXIT_FILE_ERROR)

    # Parse target directory
    target_dir = Path(args.target) if args.target else None

    # Create flow manager
    flow = CommandInstallationFlow(repo_root, target_dir)

    # Handle different modes
    try:
        if args.command:
            # Install specific command
            success = flow.run_install_command(args.command, args.overwrite, args.dry_run)
            sys.exit(EXIT_SUCCESS if success else EXIT_VALIDATION_FAILED)

        elif args.category and not args.list:
            # Install all in category
            success = flow.run_install_category(args.category, args.overwrite, args.dry_run)
            sys.exit(EXIT_SUCCESS if success else EXIT_VALIDATION_FAILED)

        elif args.search:
            # Search for commands
            results = flow.catalog.search_commands(args.search)
            if results:
                print(f"\nSearch results for '{args.search}':")
                for cmd in results:
                    print(f"  • {cmd['name']} - {cmd.get('description', '')[:60]}")
            else:
                print(f"No commands found matching '{args.search}'")
            sys.exit(EXIT_SUCCESS)

        elif args.list:
            # List mode
            success = flow.run_list_mode(args.category)
            sys.exit(EXIT_SUCCESS if success else EXIT_VALIDATION_FAILED)

        else:
            # Interactive mode (default)
            success = flow.run_interactive()
            sys.exit(EXIT_SUCCESS if success else EXIT_USER_CANCEL)

    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user")
        sys.exit(EXIT_USER_CANCEL)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(EXIT_UNKNOWN_ERROR)


if __name__ == '__main__':
    main()
