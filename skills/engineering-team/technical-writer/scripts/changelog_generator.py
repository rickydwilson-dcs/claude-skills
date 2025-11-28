#!/usr/bin/env python3
"""
Changelog Generator - Generate CHANGELOG entries from git commit history

Parses conventional commits and generates Keep a Changelog formatted output.
"""

import subprocess
import re
import json
from typing import Dict, List, Tuple
from datetime import datetime
from pathlib import Path


class ChangelogGenerator:
    def __init__(self):
        """Initialize the changelog generator"""
        # Conventional commit type mappings
        self.type_mappings = {
            'feat': 'Added',
            'fix': 'Fixed',
            'docs': 'Documentation',
            'refactor': 'Changed',
            'perf': 'Performance',
            'test': 'Testing',
            'chore': 'Maintenance',
            'style': 'Changed',
            'ci': 'Maintenance',
            'build': 'Maintenance',
            'revert': 'Fixed'
        }

        # Keep a Changelog categories in display order
        self.categories = [
            'Breaking Changes',
            'Added',
            'Changed',
            'Deprecated',
            'Removed',
            'Fixed',
            'Security',
            'Performance',
            'Documentation',
            'Testing',
            'Maintenance'
        ]

    def get_last_tag(self) -> str:
        """Get the last git tag or return None"""
        try:
            result = subprocess.run(
                ['git', 'describe', '--tags', '--abbrev=0'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def get_commits(self, since: str, until: str = 'HEAD') -> List[Dict]:
        """Get commits between two refs"""
        try:
            # Use a unique separator to handle multiline commit bodies
            sep = '|||COMMIT_SEP|||'
            field_sep = '|||FIELD_SEP|||'

            result = subprocess.run(
                ['git', 'log', f'{since}..{until}',
                 f'--pretty=format:%H{field_sep}%s{field_sep}%b{field_sep}%an{field_sep}%ad{sep}',
                 '--date=short'],
                capture_output=True,
                text=True,
                check=True
            )

            if not result.stdout.strip():
                return []

            commits = []
            # Split by commit separator
            commit_texts = result.stdout.strip().split(sep)

            for commit_text in commit_texts:
                commit_text = commit_text.strip()
                if not commit_text:
                    continue

                # Split fields by field separator
                parts = commit_text.split(field_sep)
                if len(parts) >= 5:
                    commits.append({
                        'hash': parts[0].strip(),
                        'subject': parts[1].strip(),
                        'body': parts[2].strip() if len(parts) > 2 else '',
                        'author': parts[3].strip() if len(parts) > 3 else '',
                        'date': parts[4].strip() if len(parts) > 4 else ''
                    })

            return commits

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get git commits: {e}")
        except FileNotFoundError:
            raise RuntimeError("git command not found. Ensure git is installed and in PATH")

    def parse_conventional_commit(self, commit: Dict) -> Tuple[str, str, str, str, bool, List[str]]:
        """
        Parse a conventional commit message

        Returns: (type, scope, description, body, is_breaking, issues)
        """
        subject = commit['subject']
        body = commit['body']

        # Pattern: type(scope)!: description
        pattern = r'^(\w+)(\(([^)]+)\))?(!)?:\s*(.+)$'
        match = re.match(pattern, subject)

        if not match:
            # Not a conventional commit, categorize as Maintenance
            return 'chore', '', subject, body, False, self._extract_issues(subject + ' ' + body)

        commit_type = match.group(1)
        scope = match.group(3) or ''
        breaking_marker = match.group(4) or ''
        description = match.group(5)

        # Check for breaking changes
        is_breaking = bool(breaking_marker) or 'BREAKING CHANGE' in body

        # Extract issue/PR references
        issues = self._extract_issues(subject + ' ' + body)

        return commit_type, scope, description, body, is_breaking, issues

    def _extract_issues(self, text: str) -> List[str]:
        """Extract issue/PR references like #123"""
        return re.findall(r'#(\d+)', text)

    def categorize_commits(self, commits: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize commits by type"""
        categorized = {category: [] for category in self.categories}

        for commit in commits:
            commit_type, scope, description, body, is_breaking, issues = self.parse_conventional_commit(commit)

            # Build formatted message
            formatted = description
            if scope:
                formatted = f"{scope}: {description}"

            # Add issue references
            if issues:
                issue_refs = ', '.join(f"#{issue}" for issue in issues)
                formatted = f"{formatted} ({issue_refs})"

            entry = {
                'message': formatted,
                'hash': commit['hash'][:7],
                'author': commit['author'],
                'date': commit['date'],
                'full_message': commit['subject']
            }

            # Handle breaking changes
            if is_breaking:
                categorized['Breaking Changes'].append(entry)

            # Map to category
            category = self.type_mappings.get(commit_type, 'Maintenance')
            if category in categorized:
                categorized[category].append(entry)

        return categorized

    def generate_keep_a_changelog(self, categorized: Dict[str, List[Dict]],
                                   version: str = 'Unreleased',
                                   date: str = None) -> str:
        """Generate Keep a Changelog formatted output"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        lines = []

        # Version header
        if version == 'Unreleased':
            lines.append(f"## [{version}]")
        else:
            lines.append(f"## [{version}] - {date}")

        lines.append("")

        # Add each category with entries
        for category in self.categories:
            entries = categorized.get(category, [])
            if entries:
                lines.append(f"### {category}")
                for entry in entries:
                    lines.append(f"- {entry['message']}")
                lines.append("")

        return '\n'.join(lines)

    def generate_simple_format(self, categorized: Dict[str, List[Dict]],
                               version: str = 'Unreleased') -> str:
        """Generate simple changelog format"""
        lines = [f"# {version}", ""]

        for category in self.categories:
            entries = categorized.get(category, [])
            if entries:
                lines.append(f"## {category}")
                for entry in entries:
                    lines.append(f"- {entry['message']}")
                lines.append("")

        return '\n'.join(lines)

    def generate_json_format(self, categorized: Dict[str, List[Dict]],
                            version: str, since: str, until: str,
                            total_commits: int) -> str:
        """Generate JSON changelog format"""
        # Filter out empty categories
        categories_with_content = {
            category: [entry['message'] for entry in entries]
            for category, entries in categorized.items()
            if entries
        }

        data = {
            'version': version,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'commits_parsed': total_commits,
            'categories': categories_with_content,
            'since': since,
            'until': until
        }

        return json.dumps(data, indent=2)

    def prepend_to_changelog(self, content: str, changelog_path: Path) -> None:
        """Prepend new content to existing CHANGELOG.md"""
        existing_content = ""

        if changelog_path.exists():
            with open(changelog_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()

            # Skip the "# Changelog" header if it exists
            if existing_content.startswith('# Changelog'):
                lines = existing_content.split('\n')
                header = lines[0]
                rest = '\n'.join(lines[1:]).lstrip('\n')
                existing_content = f"{header}\n\n{rest}"
        else:
            existing_content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\nThe format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\nand this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n"

        # Combine new content with existing
        if existing_content.startswith('# Changelog'):
            lines = existing_content.split('\n')
            header_lines = []
            rest_lines = []
            in_header = True

            for line in lines:
                if in_header and (line.startswith('# ') or line.startswith('All notable') or line.startswith('The format') or not line.strip()):
                    header_lines.append(line)
                else:
                    in_header = False
                    rest_lines.append(line)

            header = '\n'.join(header_lines).rstrip()
            rest = '\n'.join(rest_lines).lstrip('\n')

            combined = f"{header}\n\n{content.strip()}\n\n{rest}".rstrip() + '\n'
        else:
            combined = f"{content}\n\n{existing_content}".rstrip() + '\n'

        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write(combined)


def generate_changelog(since: str = None, until: str = 'HEAD',
                       output_format: str = 'keep-a-changelog',
                       version: str = 'Unreleased',
                       output_file: str = None,
                       prepend: bool = False,
                       dry_run: bool = False) -> str:
    """
    Generate changelog from git commits

    Args:
        since: Start ref (tag, commit, HEAD~N)
        until: End ref (default: HEAD)
        output_format: Output format (keep-a-changelog, simple, json)
        version: Version number for the release
        output_file: Output file path
        prepend: Prepend to existing CHANGELOG.md
        dry_run: Preview without writing

    Returns:
        Generated changelog content
    """
    generator = ChangelogGenerator()

    # Determine since ref
    if since is None:
        last_tag = generator.get_last_tag()
        if last_tag:
            since = last_tag
            print(f"📋 Using last tag as starting point: {last_tag}")
        else:
            since = 'HEAD~20'
            print(f"📋 No tags found, using: {since}")

    print(f"📋 Generating changelog from {since} to {until}")

    # Get commits
    try:
        commits = generator.get_commits(since, until)
    except RuntimeError as e:
        raise RuntimeError(f"Failed to retrieve commits: {e}")

    if not commits:
        print(f"📋 No commits found between {since} and {until}")
        return ""

    print(f"📋 Found {len(commits)} commits")

    # Categorize commits
    categorized = generator.categorize_commits(commits)

    # Count non-empty categories
    non_empty = sum(1 for entries in categorized.values() if entries)
    print(f"📋 Categorized into {non_empty} sections")

    # Generate output
    if output_format == 'json':
        content = generator.generate_json_format(categorized, version, since, until, len(commits))
    elif output_format == 'simple':
        content = generator.generate_simple_format(categorized, version)
    else:  # keep-a-changelog
        content = generator.generate_keep_a_changelog(categorized, version)

    # Handle output
    if dry_run:
        print("\n📝 Dry run - preview:\n")
        print(content)
        return content

    # Determine output path
    if output_file:
        output_path = Path(output_file)
    elif prepend:
        output_path = Path('CHANGELOG.md')
    else:
        output_path = None

    # Write or prepend
    if output_path:
        if prepend and output_format == 'keep-a-changelog':
            generator.prepend_to_changelog(content, output_path)
            print(f"✅ Changelog prepended to {output_path}")
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Changelog written to {output_path}")
    else:
        print(content)

    return content


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate CHANGELOG entries from git commit history',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate changelog from last tag to HEAD
  %(prog)s

  # Generate from specific tag
  %(prog)s --since v1.0.0

  # Generate from last 10 commits
  %(prog)s --since HEAD~10

  # Generate and prepend to CHANGELOG.md
  %(prog)s --prepend

  # Generate with version number
  %(prog)s --version 2.0.0 --prepend

  # JSON output
  %(prog)s --format json --output changelog.json

  # Dry run (preview)
  %(prog)s --dry-run

Conventional Commit Types:
  feat:      New features → Added
  fix:       Bug fixes → Fixed
  docs:      Documentation → Documentation
  refactor:  Code refactoring → Changed
  perf:      Performance improvements → Performance
  test:      Test additions → Testing
  chore:     Maintenance tasks → Maintenance

Breaking Changes:
  feat!:     Breaking feature
  fix!:      Breaking fix
  Or include "BREAKING CHANGE:" in commit body

For more information, see the technical-writer skill documentation.
        """
    )

    parser.add_argument(
        '--since', '-s',
        help='Start ref (tag, commit, HEAD~N). Default: last tag or HEAD~20'
    )

    parser.add_argument(
        '--until', '-u',
        default='HEAD',
        help='End ref. Default: HEAD'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['keep-a-changelog', 'simple', 'json'],
        default='keep-a-changelog',
        help='Output format (default: keep-a-changelog)'
    )

    parser.add_argument(
        '--prepend', '-p',
        action='store_true',
        help='Prepend to existing CHANGELOG.md'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file (default: CHANGELOG.md or stdout)'
    )

    parser.add_argument(
        '--version', '-v',
        default='Unreleased',
        help='Version number for the release (default: Unreleased)'
    )

    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Preview without writing'
    )

    args = parser.parse_args()

    try:
        # Check if we're in a git repository
        try:
            subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True,
                check=True
            )
        except subprocess.CalledProcessError:
            print("Error: Not a git repository", file=sys.stderr)
            print("Run this command from within a git repository", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Error: git command not found", file=sys.stderr)
            print("Please install git and ensure it's in your PATH", file=sys.stderr)
            sys.exit(1)

        # Generate changelog
        result = generate_changelog(
            since=args.since,
            until=args.until,
            output_format=args.format,
            version=args.version,
            output_file=args.output,
            prepend=args.prepend,
            dry_run=args.dry_run
        )

        if not result:
            print("📋 No changelog generated (no commits found)", file=sys.stderr)
            sys.exit(2)

        sys.exit(0)

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except PermissionError as e:
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
