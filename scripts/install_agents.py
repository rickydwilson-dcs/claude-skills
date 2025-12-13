#!/usr/bin/env python3
"""
Agent Installation Tool - Interactive agent installer for Claude Code

This tool provides an easy way to install agents from the claude-skills
library to a user's ~/.claude/agents/ directory with interactive selection,
validation, and manifest tracking.

Usage:
    python3 scripts/install_agents.py                     # Interactive mode
    python3 scripts/install_agents.py --list              # List all agents
    python3 scripts/install_agents.py --agent cs-architect
    python3 scripts/install_agents.py --domain engineering
    python3 scripts/install_agents.py --all               # Install all agents
    python3 scripts/install_agents.py --dry-run           # Preview changes
    python3 scripts/install_agents.py --help              # Show help
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict


# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_FAILED = 1
EXIT_FILE_ERROR = 2
EXIT_USER_CANCEL = 3
EXIT_UNKNOWN_ERROR = 99


class AgentMetadata:
    """Parse and manage agent metadata from YAML frontmatter"""

    @staticmethod
    def parse(file_path: Path) -> Optional[Dict]:
        """Parse YAML frontmatter from agent file"""
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
            metadata = AgentMetadata._parse_yaml(yaml_content)

            # Extract agent name from filename if not in metadata
            if 'name' not in metadata:
                metadata['name'] = file_path.stem

            # Add file path
            metadata['file_path'] = str(file_path)

            # Determine domain from path
            domain = file_path.parent.name
            if domain not in metadata:
                metadata['domain'] = domain

            return metadata

        except Exception as e:
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)
            return None

    @staticmethod
    def _parse_yaml(yaml_str: str) -> Dict:
        """Simple YAML parser for agent frontmatter (stdlib only)"""
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


class AgentCatalog:
    """Manage agent discovery and categorization"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.agents_dir = repo_root / "agents"
        self.agents: Dict[str, Dict] = {}
        self.domains: Dict[str, List[str]] = defaultdict(list)
        self._discover_agents()

    def _discover_agents(self) -> None:
        """Discover all available agents in agents/ directory"""
        if not self.agents_dir.exists():
            return

        # Find all cs-*.md files in subdirectories
        for md_file in self.agents_dir.rglob("cs-*.md"):
            # Skip non-agent files
            if md_file.name in ("CLAUDE.md", "README.md"):
                continue

            metadata = AgentMetadata.parse(md_file)
            if metadata:
                agent_name = metadata.get('name', md_file.stem)
                domain = metadata.get('domain', 'general')

                self.agents[agent_name] = metadata
                self.domains[domain].append(agent_name)

    def get_all_domains(self) -> List[str]:
        """Get all available domains, sorted"""
        return sorted(self.domains.keys())

    def get_domain_agents(self, domain: str) -> List[Dict]:
        """Get all agents in a domain"""
        agent_names = self.domains.get(domain, [])
        return [self.agents[name] for name in sorted(agent_names)]

    def get_agent(self, name: str) -> Optional[Dict]:
        """Get agent metadata by name"""
        return self.agents.get(name)

    def get_all_agents(self) -> List[Dict]:
        """Get all agents, sorted by domain then name"""
        agents = list(self.agents.values())
        return sorted(
            agents,
            key=lambda a: (a.get('domain', 'general'), a.get('name', ''))
        )

    def search_agents(self, query: str) -> List[Dict]:
        """Search agents by name or description"""
        query_lower = query.lower()
        results = []

        for agent in self.agents.values():
            name = agent.get('name', '').lower()
            desc = agent.get('description', '').lower()

            if query_lower in name or query_lower in desc:
                results.append(agent)

        return sorted(results, key=lambda a: a.get('name', ''))


class AgentInstaller:
    """Manage agent installation to ~/.claude/agents/"""

    def __init__(self, target_dir: Optional[Path] = None):
        """Initialize installer with target directory"""
        if target_dir is None:
            # Default to ~/.claude/agents/
            target_dir = Path.home() / ".claude" / "agents"

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
            "version": "1.0.0",
            "source": "claude-skills"
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

    def is_installed(self, agent_name: str) -> bool:
        """Check if agent is already installed"""
        installed_names = [a['name'] for a in self.manifest.get('installed', [])]
        return agent_name in installed_names

    def get_installed_agents(self) -> List[Dict]:
        """Get list of installed agents"""
        return self.manifest.get('installed', [])

    def install_agents(
        self,
        agents: List[Dict],
        overwrite: bool = False,
        dry_run: bool = False,
        show_progress: bool = True
    ) -> Tuple[int, List[str], List[str]]:
        """
        Install multiple agents

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

        # Install each agent
        for agent in agents:
            result = self._install_single(agent, overwrite, dry_run, show_progress)
            if result['success']:
                installed.append(agent['name'])
                success_count += 1
            else:
                errors.append(result['error'])

        # Update manifest
        if not dry_run and installed:
            self._update_manifest(agents, installed)

        return success_count, installed, errors

    def _install_single(
        self,
        agent: Dict,
        overwrite: bool,
        dry_run: bool,
        show_progress: bool
    ) -> Dict:
        """Install a single agent"""
        try:
            source_path = Path(agent['file_path'])
            target_path = self.target_dir / source_path.name
            agent_name = agent['name']

            # Check if already installed
            if target_path.exists() and not overwrite:
                return {
                    'success': False,
                    'error': f"Already installed: {agent_name} (use --overwrite to update)"
                }

            if show_progress:
                status = "[DRY RUN] " if dry_run else ""
                print(f"✓ Installing {status}{agent_name} → {target_path.name}")

            if dry_run:
                return {'success': True}

            # Copy file
            shutil.copy2(source_path, target_path)
            return {'success': True}

        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to install {agent.get('name', 'unknown')}: {e}"
            }

    def _update_manifest(self, agents: List[Dict], installed: List[str]) -> None:
        """Update manifest with installed agents"""
        installed_set = set(installed)

        for agent in agents:
            if agent['name'] in installed_set:
                # Check if already in manifest
                existing = [a for a in self.manifest['installed'] if a['name'] == agent['name']]

                if existing:
                    # Update existing entry
                    existing[0].update({
                        'installedAt': datetime.now().isoformat() + "Z",
                        'model': agent.get('model', 'sonnet'),
                    })
                else:
                    # Add new entry
                    self.manifest['installed'].append({
                        'name': agent['name'],
                        'domain': agent.get('domain', 'general'),
                        'model': agent.get('model', 'sonnet'),
                        'installedAt': datetime.now().isoformat() + "Z",
                        'source': 'claude-skills',
                        'description': agent.get('description', '')
                    })

        self.save_manifest()


class InteractiveUI:
    """Provide interactive UI for agent selection"""

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
    def display_agent_details(agent: Dict) -> None:
        """Display detailed agent information"""
        print(f"\n  Name: {agent.get('name', 'N/A')}")
        print(f"  Domain: {agent.get('domain', 'N/A')}")
        print(f"  Model: {agent.get('model', 'sonnet')}")
        print(f"  Description: {agent.get('description', 'N/A')}")

        if 'tools' in agent:
            tools = agent['tools']
            if isinstance(tools, list):
                print(f"  Tools: {', '.join(tools)}")
            else:
                print(f"  Tools: {tools}")

        if 'skills' in agent:
            skills = agent['skills']
            if isinstance(skills, list):
                print(f"  Skills: {', '.join(skills)}")
            else:
                print(f"  Skills: {skills}")

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


class AgentInstallationFlow:
    """Orchestrate interactive installation flow"""

    def __init__(self, repo_root: Path, target_dir: Optional[Path] = None):
        self.repo_root = repo_root
        self.catalog = AgentCatalog(repo_root)
        self.installer = AgentInstaller(target_dir)
        self.ui = InteractiveUI()

    def run_interactive(self) -> bool:
        """Run interactive installation flow"""
        print("\n" + "=" * 60)
        print("AGENT INSTALLATION TOOL")
        print("=" * 60)

        # Step 1: Select domain
        all_domains = self.catalog.get_all_domains()
        if not all_domains:
            print("No agents available to install")
            return False

        domains = ["All Agents"] + all_domains
        selected_domain = self.ui.select_from_list(
            domains,
            "Step 1: Select domain to browse"
        )

        if not selected_domain:
            print("Installation cancelled")
            return False

        # Get agents for selected domain
        if selected_domain[0] == "All Agents":
            agents = self.catalog.get_all_agents()
        else:
            agents = self.catalog.get_domain_agents(selected_domain[0])

        if not agents:
            print("No agents in this domain")
            return False

        # Step 2: Display and select agents
        print(f"\nStep 2: Select agents to install ({len(agents)} available)")

        # Format agent display
        agent_displays = []
        for agent in agents:
            display = f"{agent['name']} - {agent.get('description', 'N/A')[:50]}"
            agent_displays.append(display)
            self.ui.display_agent_details(agent)

        print()
        selected_displays = self.ui.select_from_list(
            agent_displays,
            "Select agents (comma-separated for multiple)",
            allow_multiple=True
        )

        if not selected_displays:
            print("No agents selected")
            return False

        # Extract selected agents
        selected_indices = [
            agent_displays.index(d) for d in selected_displays
        ]
        selected_agents = [agents[i] for i in selected_indices]

        # Step 3: Check for conflicts
        conflicts = []
        for agent in selected_agents:
            if self.installer.is_installed(agent['name']):
                conflicts.append(agent['name'])

        if conflicts:
            print(f"\nWarning: {len(conflicts)} agent(s) already installed:")
            for name in conflicts:
                print(f"  • {name}")

            if not self.ui.prompt_yes_no("Overwrite existing agents?"):
                print("Installation cancelled")
                return False
            overwrite = True
        else:
            overwrite = False

        # Step 4: Summary and confirmation
        print("\n" + "=" * 60)
        print("INSTALLATION SUMMARY")
        print("=" * 60)
        print(f"Agents to install: {len(selected_agents)}")
        for agent in selected_agents:
            status = "(update)" if self.installer.is_installed(agent['name']) else "(new)"
            print(f"  • {agent['name']} {status}")

        print(f"Target directory: {self.installer.target_dir}")

        if not self.ui.prompt_yes_no("\nProceed with installation?"):
            print("Installation cancelled")
            return False

        # Step 5: Install agents
        success_count, installed, errors = self.installer.install_agents(
            selected_agents,
            overwrite=overwrite,
            show_progress=True
        )

        # Step 6: Report results
        skipped = [(agent['name'], "Already installed") for agent in selected_agents
                   if agent['name'] not in installed and not errors]

        self.ui.display_installation_summary(installed, skipped, errors)

        return success_count > 0

    def run_list_mode(self, domain: Optional[str] = None) -> bool:
        """List available agents"""
        print("\n" + "=" * 60)
        print("AVAILABLE AGENTS")
        print("=" * 60)

        if domain:
            agents = self.catalog.get_domain_agents(domain)
            if not agents:
                print(f"No agents in domain: {domain}")
                return False
            print(f"\nDomain: {domain}")
        else:
            agents = self.catalog.get_all_agents()

        if not agents:
            print("No agents available")
            return False

        # Group by domain
        by_domain = defaultdict(list)
        for agent in agents:
            dom = agent.get('domain', 'general')
            by_domain[dom].append(agent)

        for dom in sorted(by_domain.keys()):
            print(f"\n{dom.upper()} ({len(by_domain[dom])}):")
            for agent in sorted(by_domain[dom], key=lambda a: a.get('name', '')):
                installed = "✓" if self.installer.is_installed(agent['name']) else " "
                print(f"  [{installed}] {agent['name']:<30} - {agent.get('description', '')[:45]}")

        print("\n[✓] = Already installed")
        return True

    def run_install_agent(
        self,
        agent_name: str,
        overwrite: bool = False,
        dry_run: bool = False
    ) -> bool:
        """Install specific agent"""
        agent = self.catalog.get_agent(agent_name)
        if not agent:
            print(f"Agent not found: {agent_name}")
            return False

        print(f"\nInstalling {agent_name}...")
        self.ui.display_agent_details(agent)

        success_count, installed, errors = self.installer.install_agents(
            [agent],
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
                print(f"\n✓ Would install: {agent_name}")
            else:
                print(f"\n✓ Successfully installed: {agent_name}")
            print(f"  Location: {self.installer.target_dir / Path(agent['file_path']).name}")
            return True

        return False

    def run_install_domain(
        self,
        domain: str,
        overwrite: bool = False,
        dry_run: bool = False
    ) -> bool:
        """Install all agents in a domain"""
        agents = self.catalog.get_domain_agents(domain)
        if not agents:
            print(f"No agents in domain: {domain}")
            return False

        print(f"\nInstalling all {len(agents)} agents in '{domain}'...")

        success_count, installed, errors = self.installer.install_agents(
            agents,
            overwrite=overwrite,
            dry_run=dry_run,
            show_progress=True
        )

        skipped = [(agent['name'], "Already installed") for agent in agents
                   if agent['name'] not in installed and not errors]

        self.ui.display_installation_summary(installed, skipped, errors)
        return success_count > 0

    def run_install_all(
        self,
        overwrite: bool = False,
        dry_run: bool = False
    ) -> bool:
        """Install all agents"""
        agents = self.catalog.get_all_agents()
        if not agents:
            print("No agents available")
            return False

        print(f"\nInstalling all {len(agents)} agents...")

        success_count, installed, errors = self.installer.install_agents(
            agents,
            overwrite=overwrite,
            dry_run=dry_run,
            show_progress=True
        )

        skipped = [(agent['name'], "Already installed") for agent in agents
                   if agent['name'] not in installed and not errors]

        self.ui.display_installation_summary(installed, skipped, errors)
        return success_count > 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Interactive agent installation tool for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  python3 scripts/install_agents.py

  # List all available agents
  python3 scripts/install_agents.py --list

  # List agents in domain
  python3 scripts/install_agents.py --list --domain engineering

  # Install specific agent
  python3 scripts/install_agents.py --agent cs-architect

  # Install all in domain
  python3 scripts/install_agents.py --domain engineering

  # Install ALL agents
  python3 scripts/install_agents.py --all

  # Preview changes without installing
  python3 scripts/install_agents.py --dry-run

  # Overwrite existing agents
  python3 scripts/install_agents.py --agent cs-architect --overwrite
        """
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available agents'
    )

    parser.add_argument(
        '--agent',
        type=str,
        help='Install specific agent (e.g., cs-architect)'
    )

    parser.add_argument(
        '--domain',
        type=str,
        help='Install all agents in domain or list by domain'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Install all agents'
    )

    parser.add_argument(
        '--target',
        type=str,
        help='Target directory for installation (default: ~/.claude/agents/)'
    )

    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing agents'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without installing'
    )

    parser.add_argument(
        '--search',
        type=str,
        help='Search for agents by name or description'
    )

    args = parser.parse_args()

    # Find repository root
    repo_root = Path(__file__).parent.parent
    if not (repo_root / "agents").exists():
        print("Error: agents/ directory not found. Are you in the claude-skills repository?")
        sys.exit(EXIT_FILE_ERROR)

    # Parse target directory
    target_dir = Path(args.target) if args.target else None

    # Create flow manager
    flow = AgentInstallationFlow(repo_root, target_dir)

    # Handle different modes
    try:
        if args.agent:
            # Install specific agent
            success = flow.run_install_agent(args.agent, args.overwrite, args.dry_run)
            sys.exit(EXIT_SUCCESS if success else EXIT_VALIDATION_FAILED)

        elif args.all:
            # Install all agents
            success = flow.run_install_all(args.overwrite, args.dry_run)
            sys.exit(EXIT_SUCCESS if success else EXIT_VALIDATION_FAILED)

        elif args.domain and not args.list:
            # Install all in domain
            success = flow.run_install_domain(args.domain, args.overwrite, args.dry_run)
            sys.exit(EXIT_SUCCESS if success else EXIT_VALIDATION_FAILED)

        elif args.search:
            # Search for agents
            results = flow.catalog.search_agents(args.search)
            if results:
                print(f"\nSearch results for '{args.search}':")
                for agent in results:
                    print(f"  • {agent['name']} - {agent.get('description', '')[:60]}")
            else:
                print(f"No agents found matching '{args.search}'")
            sys.exit(EXIT_SUCCESS)

        elif args.list:
            # List mode
            success = flow.run_list_mode(args.domain)
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
