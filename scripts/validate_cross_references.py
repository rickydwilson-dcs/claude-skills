#!/usr/bin/env python3
"""
Cross-Reference Validator

Validates that all cross-references between agents, skills, and commands
are valid and point to existing resources.

Checks:
1. Agent 'skills' field points to existing skill directory
2. Agent relative paths (../../) resolve correctly
3. Command 'related_agents' references exist
4. Command 'related_skills' references exist
5. Agent 'related-agents' references exist

Usage:
    python3 scripts/validate_cross_references.py           # Validate all
    python3 scripts/validate_cross_references.py --json    # JSON output
    python3 scripts/validate_cross_references.py --verbose # Detailed output
    python3 scripts/validate_cross_references.py --fix     # Show fix suggestions

Exit Codes:
    0 - All references valid
    1 - Some references invalid
    2 - File/directory errors
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def parse_yaml_frontmatter(content: str) -> Dict:
    """Simple YAML frontmatter parser for agent/skill files."""
    result = {}

    # Check for YAML frontmatter
    if not content.startswith('---'):
        return result

    # Find end of frontmatter
    end_match = content.find('\n---', 3)
    if end_match == -1:
        return result

    frontmatter = content[3:end_match]

    # Extract key fields
    for line in frontmatter.split('\n'):
        line = line.strip()

        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue

        # Simple key: value parsing
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Handle arrays [item1, item2]
            if value.startswith('[') and value.endswith(']'):
                items = value[1:-1].split(',')
                result[key] = [item.strip().strip('"\'') for item in items if item.strip()]
            elif value:
                result[key] = value.strip('"\'')

    return result


def find_relative_paths(content: str) -> List[str]:
    """Find all relative path references in content."""
    # Match ../../skills/team/skill-name/ patterns
    pattern = r'\.\./\.\./skills/[a-z-]+/[a-z-]+'
    return list(set(re.findall(pattern, content)))


def validate_agent(agent_path: Path, agents_dir: Path, skills_dir: Path) -> List[Dict]:
    """Validate cross-references in an agent file."""
    errors = []

    try:
        content = agent_path.read_text(encoding='utf-8')
    except Exception as e:
        return [{"type": "read_error", "path": str(agent_path), "message": str(e)}]

    frontmatter = parse_yaml_frontmatter(content)

    # Check 'skills' field
    if 'skills' in frontmatter:
        skill_ref = frontmatter['skills']
        # Convert skill name to path
        for team_dir in skills_dir.iterdir():
            if team_dir.is_dir():
                potential_skill = team_dir / skill_ref
                if potential_skill.exists():
                    break
        else:
            # Skill not found in any team
            errors.append({
                "type": "missing_skill",
                "agent": str(agent_path),
                "reference": skill_ref,
                "message": f"Skill '{skill_ref}' not found in any team directory"
            })

    # Check related-agents
    if 'related-agents' in frontmatter:
        related = frontmatter['related-agents']
        if isinstance(related, list):
            for ref in related:
                if ref and ref != '[]':
                    # Find agent in any domain
                    found = False
                    for domain_dir in agents_dir.iterdir():
                        if domain_dir.is_dir():
                            agent_file = domain_dir / f"{ref}.md"
                            if agent_file.exists():
                                found = True
                                break
                    if not found:
                        errors.append({
                            "type": "missing_related_agent",
                            "agent": str(agent_path),
                            "reference": ref,
                            "message": f"Related agent '{ref}' not found"
                        })

    # Check relative paths in content
    relative_paths = find_relative_paths(content)
    for rel_path in relative_paths:
        # Convert relative path from agent location
        abs_path = (agent_path.parent / rel_path).resolve()
        if not abs_path.exists():
            # Try from repo root
            repo_path = Path(rel_path.replace('../../', ''))
            if not repo_path.exists():
                errors.append({
                    "type": "broken_relative_path",
                    "agent": str(agent_path),
                    "reference": rel_path,
                    "message": f"Relative path does not resolve to existing directory"
                })

    return errors


def validate_command(cmd_path: Path, agents_dir: Path, skills_dir: Path) -> List[Dict]:
    """Validate cross-references in a command file."""
    errors = []

    try:
        content = cmd_path.read_text(encoding='utf-8')
    except Exception as e:
        return [{"type": "read_error", "path": str(cmd_path), "message": str(e)}]

    frontmatter = parse_yaml_frontmatter(content)

    # Check related_agents
    if 'related_agents' in frontmatter:
        related = frontmatter['related_agents']
        if isinstance(related, list):
            for ref in related:
                if ref:
                    found = False
                    for domain_dir in agents_dir.iterdir():
                        if domain_dir.is_dir():
                            agent_file = domain_dir / f"{ref}.md"
                            if agent_file.exists():
                                found = True
                                break
                    if not found:
                        errors.append({
                            "type": "missing_related_agent",
                            "command": str(cmd_path),
                            "reference": ref,
                            "message": f"Related agent '{ref}' not found"
                        })

    # Check related_skills
    if 'related_skills' in frontmatter:
        related = frontmatter['related_skills']
        if isinstance(related, list):
            for ref in related:
                if ref:
                    found = False
                    for team_dir in skills_dir.iterdir():
                        if team_dir.is_dir():
                            skill_dir = team_dir / ref
                            if skill_dir.exists():
                                found = True
                                break
                    if not found:
                        errors.append({
                            "type": "missing_related_skill",
                            "command": str(cmd_path),
                            "reference": ref,
                            "message": f"Related skill '{ref}' not found"
                        })

    return errors


def validate_all(agents_dir: Path, skills_dir: Path, commands_dir: Path,
                 verbose: bool = False) -> Dict:
    """Validate all cross-references."""
    results = {
        "total_checked": 0,
        "agents_checked": 0,
        "commands_checked": 0,
        "errors": [],
        "valid": True
    }

    # Validate agents
    if agents_dir.exists():
        for domain_dir in agents_dir.iterdir():
            if domain_dir.is_dir():
                for agent_file in domain_dir.glob("cs-*.md"):
                    results["agents_checked"] += 1
                    results["total_checked"] += 1

                    if verbose:
                        print(f"Checking: {agent_file}")

                    errors = validate_agent(agent_file, agents_dir, skills_dir)
                    results["errors"].extend(errors)

    # Validate commands
    if commands_dir.exists():
        for category_dir in commands_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                for cmd_file in category_dir.glob("*.md"):
                    if cmd_file.name not in ['README.md', 'CLAUDE.md', 'CATALOG.md']:
                        results["commands_checked"] += 1
                        results["total_checked"] += 1

                        if verbose:
                            print(f"Checking: {cmd_file}")

                        errors = validate_command(cmd_file, agents_dir, skills_dir)
                        results["errors"].extend(errors)

    results["valid"] = len(results["errors"]) == 0
    return results


def print_summary(results: Dict, show_fixes: bool = False):
    """Print human-readable summary."""
    print("\n" + "=" * 60)
    print("Cross-Reference Validation Results")
    print("=" * 60)
    print(f"Total files checked: {results['total_checked']}")
    print(f"  Agents:   {results['agents_checked']}")
    print(f"  Commands: {results['commands_checked']}")
    print(f"Errors found: {len(results['errors'])}")

    if results['errors']:
        print("\nErrors:")
        for error in results['errors']:
            print(f"\n  Type: {error['type']}")
            if 'agent' in error:
                print(f"  File: {error['agent']}")
            elif 'command' in error:
                print(f"  File: {error['command']}")
            print(f"  Reference: {error.get('reference', 'N/A')}")
            print(f"  Message: {error['message']}")

            if show_fixes:
                if error['type'] == 'missing_skill':
                    print(f"  Fix: Create skill at skills/{{team}}/{error['reference']}/")
                elif error['type'] == 'missing_related_agent':
                    print(f"  Fix: Create agent or remove reference from related-agents")
                elif error['type'] == 'broken_relative_path':
                    print(f"  Fix: Update path or create missing directory")

    else:
        print("\n✓ All cross-references are valid!")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Validate cross-references between agents, skills, and commands"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed progress"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Show fix suggestions for errors"
    )
    parser.add_argument(
        "--agents-dir",
        default="agents",
        help="Path to agents directory (default: agents)"
    )
    parser.add_argument(
        "--skills-dir",
        default="skills",
        help="Path to skills directory (default: skills)"
    )
    parser.add_argument(
        "--commands-dir",
        default="commands",
        help="Path to commands directory (default: commands)"
    )

    args = parser.parse_args()

    agents_dir = Path(args.agents_dir)
    skills_dir = Path(args.skills_dir)
    commands_dir = Path(args.commands_dir)

    # Validate directories exist
    if not agents_dir.exists():
        print(f"Error: Agents directory not found: {agents_dir}", file=sys.stderr)
        sys.exit(2)

    if not skills_dir.exists():
        print(f"Error: Skills directory not found: {skills_dir}", file=sys.stderr)
        sys.exit(2)

    # Run validation
    results = validate_all(agents_dir, skills_dir, commands_dir, verbose=args.verbose)

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_summary(results, show_fixes=args.fix)

    # Exit with appropriate code
    if not results['valid']:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
