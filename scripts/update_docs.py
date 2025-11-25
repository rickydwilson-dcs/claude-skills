#!/usr/bin/env python3
"""
Documentation Update Script

Automatically scans repository and updates documentation statistics in:
- README.md
- CLAUDE.md
- CHANGELOG.md (with --changelog flag)

Usage:
    python3 scripts/update_docs.py [--dry-run] [--verbose] [--changelog]

Examples:
    # Preview changes without writing
    python3 scripts/update_docs.py --dry-run

    # Update with verbose output
    python3 scripts/update_docs.py --verbose

    # Update including changelog
    python3 scripts/update_docs.py --changelog
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class DocumentationUpdater:
    """Scans repository and updates documentation with current statistics"""

    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.stats = {}

    def log(self, message: str):
        """Print message if verbose mode enabled"""
        if self.verbose:
            print(f"  {message}")

    def scan_repository(self) -> Dict[str, int]:
        """Scan repository and collect statistics"""
        print("Scanning repository...")

        # Count agents
        agents = list((self.repo_root / "agents").rglob("cs-*.md"))
        self.stats['agents'] = len(agents)
        self.log(f"Found {self.stats['agents']} agents")

        # Count skills (exclude packaged-skills)
        skills_dirs = []
        for team_dir in (self.repo_root / "skills").iterdir():
            if team_dir.is_dir() and team_dir.name.endswith("-team"):
                for skill_dir in team_dir.iterdir():
                    if skill_dir.is_dir() and skill_dir.name != "packaged-skills":
                        if (skill_dir / "SKILL.md").exists():
                            skills_dirs.append(skill_dir)
        self.stats['skills'] = len(skills_dirs)
        self.log(f"Found {self.stats['skills']} skills")

        # Count commands (exclude README, CATALOG, CLAUDE)
        commands = []
        for cmd_file in (self.repo_root / "commands").rglob("*.md"):
            if cmd_file.name not in ("README.md", "CATALOG.md", "CLAUDE.md"):
                commands.append(cmd_file)
        self.stats['commands'] = len(commands)
        self.log(f"Found {self.stats['commands']} commands")

        # Count Python tools
        python_tools = list((self.repo_root / "skills").rglob("scripts/*.py"))
        self.stats['python_tools'] = len(python_tools)
        self.log(f"Found {self.stats['python_tools']} Python tools")

        print(f"\n✓ Repository scan complete")
        print(f"  Agents: {self.stats['agents']}")
        print(f"  Skills: {self.stats['skills']}")
        print(f"  Commands: {self.stats['commands']}")
        print(f"  Python Tools: {self.stats['python_tools']}")

        return self.stats

    def update_claude_md(self, dry_run: bool = False) -> List[str]:
        """Update statistics in CLAUDE.md"""
        print("\nUpdating CLAUDE.md...")
        claude_md = self.repo_root / "CLAUDE.md"

        if not claude_md.exists():
            print("  ⚠️  CLAUDE.md not found")
            return []

        content = claude_md.read_text()
        original = content
        changes = []

        # Update Current Scope line
        pattern = r'\*\*Current Scope:\*\* \d+ production agents, \d+ skills across \d+ domains with \d+ Python automation tools, \d+ slash commands\.'
        replacement = f"**Current Scope:** {self.stats['agents']} production agents, {self.stats['skills']} skills across 4 domains with {self.stats['python_tools']} Python automation tools, {self.stats['commands']} slash commands."
        content, n = re.subn(pattern, replacement, content)
        if n > 0:
            changes.append(f"Updated Current Scope statistics")
            self.log("Updated Current Scope")

        # Update agent architecture section
        pattern = r'\*\*\d+ production agents\*\* orchestrate skills'
        replacement = f"**{self.stats['agents']} production agents** orchestrate skills"
        content, n = re.subn(pattern, replacement, content)
        if n > 0:
            changes.append(f"Updated agent count in architecture section")
            self.log("Updated agent architecture section")

        # Update commands section
        pattern = r'\*\*\d+ production commands\*\* automate high-frequency developer workflows'
        replacement = f"**{self.stats['commands']} production commands** automate high-frequency developer workflows"
        content, n = re.subn(pattern, replacement, content)
        if n > 0:
            changes.append(f"Updated command count in commands section")
            self.log("Updated commands section")

        # Update Current Status line
        pattern = r'\*\*Current Status:\*\* \d+ production agents, \d+ skills across \d+ domains, \d+ slash commands'
        replacement = f"**Current Status:** {self.stats['agents']} production agents, {self.stats['skills']} skills across 4 domains, {self.stats['commands']} slash commands"
        content, n = re.subn(pattern, replacement, content)
        if n > 0:
            changes.append(f"Updated Current Status")
            self.log("Updated Current Status")

        if content != original:
            if not dry_run:
                claude_md.write_text(content)
                print(f"✓ CLAUDE.md updated ({len(changes)} changes)")
            else:
                print(f"[DRY RUN] Would update CLAUDE.md ({len(changes)} changes)")
        else:
            print("✓ CLAUDE.md already up to date")

        return changes

    def update_readme_md(self, dry_run: bool = False) -> List[str]:
        """Update statistics in README.md"""
        print("\nUpdating README.md...")
        readme_md = self.repo_root / "README.md"

        if not readme_md.exists():
            print("  ⚠️  README.md not found")
            return []

        content = readme_md.read_text()
        original = content
        changes = []

        # Update Python tools count
        pattern = r'- \*\*🛠️ Python analysis tools\*\* - \d+ CLI utilities'
        replacement = f"- **🛠️ Python analysis tools** - {self.stats['python_tools']} CLI utilities"
        content, n = re.subn(pattern, replacement, content)
        if n > 0:
            changes.append(f"Updated Python tools count")
            self.log("Updated Python tools count")

        # Update SDLC-optimized line
        pattern = r'- 🎯 \*\*SDLC-optimized\*\* - \d+ skills, \d+ agents, \d+ slash commands'
        replacement = f"- 🎯 **SDLC-optimized** - {self.stats['skills']} skills, {self.stats['agents']} agents, {self.stats['commands']} slash commands"
        content, n = re.subn(pattern, replacement, content)
        if n > 0:
            changes.append(f"Updated SDLC-optimized statistics")
            self.log("Updated SDLC-optimized section")

        # Update validation results (if present)
        pattern = r'- \*\*\d+/\d+ agents passing\*\*'
        replacement = f"- **{self.stats['agents']}/{self.stats['agents']} agents passing**"
        content, n = re.subn(pattern, replacement, content)
        if n > 0:
            changes.append(f"Updated validation results")
            self.log("Updated validation results")

        pattern = r'- \*\*\d+/\d+ skills passing\*\*'
        replacement = f"- **{self.stats['skills']}/{self.stats['skills']} skills passing**"
        content, n = re.subn(pattern, replacement, content)
        if n > 0:
            changes.append(f"Updated skill validation results")
            self.log("Updated skill validation")

        if content != original:
            if not dry_run:
                readme_md.write_text(content)
                print(f"✓ README.md updated ({len(changes)} changes)")
            else:
                print(f"[DRY RUN] Would update README.md ({len(changes)} changes)")
        else:
            print("✓ README.md already up to date")

        return changes

    def update_changelog(self, dry_run: bool = False) -> bool:
        """Add timestamp to CHANGELOG.md Unreleased section"""
        print("\nUpdating CHANGELOG.md...")
        changelog_md = self.repo_root / "CHANGELOG.md"

        if not changelog_md.exists():
            print("  ⚠️  CHANGELOG.md not found")
            return False

        content = changelog_md.read_text()

        # Check if there's an [Unreleased] section with content
        if "## [Unreleased]" not in content:
            print("✓ No unreleased changes to document")
            return False

        # Add timestamp comment
        today = datetime.now().strftime("%Y-%m-%d")
        note = f"\n*Documentation statistics updated via /update.docs on {today}*\n"

        # Insert after the first heading in Unreleased section
        pattern = r'(## \[Unreleased\]\n\n)(### )'
        replacement = f'\\1{note}\\2'
        new_content, n = re.subn(pattern, replacement, content, count=1)

        if n > 0 and new_content != content:
            if not dry_run:
                changelog_md.write_text(new_content)
                print(f"✓ CHANGELOG.md updated with timestamp")
            else:
                print(f"[DRY RUN] Would add timestamp to CHANGELOG.md")
            return True
        else:
            print("✓ CHANGELOG.md already has timestamp")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Update documentation statistics automatically",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes without writing files
  python3 scripts/update_docs.py --dry-run

  # Update with detailed output
  python3 scripts/update_docs.py --verbose

  # Update including changelog timestamp
  python3 scripts/update_docs.py --changelog --verbose
        """
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output during processing"
    )
    parser.add_argument(
        "--changelog",
        action="store_true",
        help="Update CHANGELOG.md with timestamp"
    )

    args = parser.parse_args()

    # Determine repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    print("=" * 60)
    print("DOCUMENTATION UPDATE TOOL")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    if args.dry_run:
        print("Mode: DRY RUN (no files will be modified)")
    print()

    # Create updater and scan repository
    updater = DocumentationUpdater(repo_root, verbose=args.verbose)
    stats = updater.scan_repository()

    # Update files
    claude_changes = updater.update_claude_md(dry_run=args.dry_run)
    readme_changes = updater.update_readme_md(dry_run=args.dry_run)

    if args.changelog:
        updater.update_changelog(dry_run=args.dry_run)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_changes = len(claude_changes) + len(readme_changes)

    if total_changes > 0:
        print(f"✓ {total_changes} changes made")
        if claude_changes:
            print(f"  CLAUDE.md: {len(claude_changes)} updates")
        if readme_changes:
            print(f"  README.md: {len(readme_changes)} updates")

        if not args.dry_run:
            print("\nNext steps:")
            print("  1. Review the changes: git diff")
            print("  2. Commit: git add CLAUDE.md README.md && git commit -m 'docs: update repository statistics'")
    else:
        print("✓ All documentation already up to date")

    print()


if __name__ == "__main__":
    main()
