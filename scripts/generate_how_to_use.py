#!/usr/bin/env python3
"""
Generate HOW_TO_USE.md files for all existing skills

This script reads SKILL.md files from all skill directories and generates
HOW_TO_USE.md files based on the v1.1.0 standard template.

Usage:
    python generate_how_to_use.py                    # Generate for all skills
    python generate_how_to_use.py --dry-run          # Preview without writing
    python generate_how_to_use.py --skill-path path  # Generate for specific skill
"""

import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


def simple_yaml_parse(yaml_str: str) -> Dict:
    """
    Simple YAML parser for skill frontmatter (standard library only)

    Handles basic key-value pairs and lists.
    """
    result = {}
    current_key = None
    list_items = []

    for line in yaml_str.strip().split('\n'):
        line = line.strip()

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


def extract_skill_metadata(skill_md_path: Path) -> Optional[Dict]:
    """
    Extract metadata from SKILL.md file

    Returns:
        Dict with name, description, domain, tools, etc.
        None if file doesn't exist or is malformed
    """
    if not skill_md_path.exists():
        return None

    try:
        content = skill_md_path.read_text()
    except Exception as e:
        print(f"⚠️  Cannot read {skill_md_path}: {e}")
        return None

    # Check for YAML frontmatter
    if not content.startswith('---'):
        print(f"⚠️  No YAML frontmatter in {skill_md_path}")
        return None

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"⚠️  Malformed YAML frontmatter in {skill_md_path}")
        return None

    yaml_str = parts[1]

    try:
        metadata = simple_yaml_parse(yaml_str)
    except Exception as e:
        print(f"⚠️  Invalid YAML in {skill_md_path}: {e}")
        return None

    # Extract nested metadata
    if 'metadata' in metadata and isinstance(metadata['metadata'], dict):
        # Flatten for easier access
        nested_meta = metadata['metadata']
        metadata['domain'] = nested_meta.get('domain', 'unknown')
        metadata['version'] = nested_meta.get('version', '1.0.0')
        metadata['updated'] = nested_meta.get('updated', datetime.now().strftime('%Y-%m-%d'))
        metadata['python-tools'] = nested_meta.get('python-tools', [])

    # Handle python-tools at root level (some skills may have it there)
    if 'python-tools' in metadata:
        metadata['tools'] = metadata['python-tools']
    elif 'python_tools' in metadata:
        metadata['tools'] = metadata['python_tools']
    else:
        metadata['tools'] = []

    return metadata


def get_domain_from_path(skill_path: Path) -> str:
    """
    Extract domain team from skill path

    Example: skills/marketing-team/content-creator -> marketing-team
    """
    parts = skill_path.parts

    # Find 'skills' index
    if 'skills' in parts:
        skills_idx = parts.index('skills')
        if len(parts) > skills_idx + 1:
            return parts[skills_idx + 1]

    return 'unknown-team'


def generate_how_to_use(metadata: Dict) -> str:
    """
    Generate HOW_TO_USE.md content based on skill metadata

    Args:
        metadata: Dict with name, description, tools, domain, etc.

    Returns:
        String content for HOW_TO_USE.md
    """
    skill_name = metadata.get('name', 'unknown-skill')
    skill_name_title = skill_name.replace('-', ' ').title()
    description = metadata.get('description', 'No description available')
    domain = metadata.get('domain', 'unknown')
    tools = metadata.get('tools', [])

    content = f"""# How to Use the {skill_name_title} Skill

## Quick Start

Hey Claude—I just added the "{skill_name}" skill. Can you help me with [describe your task]?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "{skill_name}" skill. Can you [specific task related to this skill]?
```

### Example 2: Advanced Usage
```
Hey Claude—I just added the "{skill_name}" skill. Can you [more complex task with specific requirements]?
```

### Example 3: Integration with Other Skills
```
Hey Claude—I just added the "{skill_name}" skill. Can you use it together with [another skill] to [combined task]?
```

## What to Provide

When using this skill, provide:

- **Primary Input**: [Describe the main input needed]
- **Context** (optional): [What context helps improve results]
- **Preferences** (optional): [Any customization options]

## What You'll Get

This skill will provide:

- **Output Format**: Results formatted according to skill specifications
- **Analysis**: Insights and recommendations based on the input
- **Deliverables**: {', '.join(tools) if tools else 'Reports and actionable outputs'}

## Python Tools Available

This skill includes the following Python tools:

"""

    if tools:
        for tool in tools:
            tool_name = tool.replace('.py', '').replace('_', ' ').title()
            content += f"- **{tool}**: {tool_name} functionality\n"

        content += f"""
You can also run these tools directly:

```bash
python scripts/{tools[0]} --help
```
"""
    else:
        content += "- No Python tools available (this skill focuses on frameworks and guidance)\n"

    content += f"""
## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements for better results
2. **Provide Context**: Include relevant background information
3. **Iterate**: Start simple, then refine based on initial results
4. **Combine Skills**: This skill works well with other {domain.replace('-team', '')} skills

## Related Skills

Consider using these skills together:

- [List related skills from the same domain]
- [Skills that complement this one]

---

**Skill**: {skill_name}
**Domain**: {domain}
**Version**: {metadata.get('version', '1.0.0')}
**Last Updated**: {metadata.get('updated', datetime.now().strftime('%Y-%m-%d'))}
"""

    return content


def find_all_skills(repo_root: Path) -> List[Path]:
    """
    Find all skill directories in the repository

    Returns:
        List of Path objects pointing to skill directories
    """
    skills_dir = repo_root / "skills"

    if not skills_dir.exists():
        print(f"❌ Skills directory not found: {skills_dir}")
        return []

    skill_paths = []

    # Iterate through skill teams (e.g., marketing-team, product-team)
    for team_dir in skills_dir.iterdir():
        if not team_dir.is_dir():
            continue
        if team_dir.name.startswith('.'):
            continue

        # Iterate through skills in each team
        for skill_dir in team_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith('.'):
                continue

            # Check if SKILL.md exists
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skill_paths.append(skill_dir)

    return sorted(skill_paths)


def generate_for_skill(skill_path: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """
    Generate HOW_TO_USE.md for a single skill

    Args:
        skill_path: Path to skill directory
        dry_run: If True, don't write files

    Returns:
        Tuple of (success: bool, message: str)
    """
    skill_md_path = skill_path / "SKILL.md"
    how_to_use_path = skill_path / "HOW_TO_USE.md"

    # Extract metadata
    metadata = extract_skill_metadata(skill_md_path)
    if not metadata:
        return False, f"Could not extract metadata from {skill_md_path}"

    # Add domain from path if missing
    if 'domain' not in metadata or metadata['domain'] == 'unknown':
        metadata['domain'] = get_domain_from_path(skill_path)

    # Generate content
    try:
        content = generate_how_to_use(metadata)
    except Exception as e:
        return False, f"Failed to generate content: {e}"

    # Write file (unless dry run)
    if dry_run:
        return True, f"[DRY RUN] Would create {how_to_use_path}"

    try:
        how_to_use_path.write_text(content)
        return True, f"✓ Created {how_to_use_path.relative_to(skill_path.parent.parent.parent)}"
    except Exception as e:
        return False, f"Failed to write {how_to_use_path}: {e}"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate HOW_TO_USE.md files for all skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_how_to_use.py                                    # Generate for all skills
  python generate_how_to_use.py --dry-run                          # Preview without writing
  python generate_how_to_use.py --skill-path skills/team/skill/   # Generate for specific skill

This script reads SKILL.md files and generates HOW_TO_USE.md based on the v1.1.0 standard.
"""
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without creating files'
    )

    parser.add_argument(
        '--skill-path',
        help='Generate for specific skill path (relative to repo root)',
        default=None
    )

    args = parser.parse_args()

    # Determine repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    print("📦 HOW_TO_USE.md Generator")
    print("=" * 60)

    if args.dry_run:
        print("⚠️  DRY RUN MODE - No files will be written")

    print()

    # Single skill mode
    if args.skill_path:
        skill_path = repo_root / args.skill_path

        if not skill_path.exists():
            print(f"❌ Skill path not found: {skill_path}")
            sys.exit(1)

        success, message = generate_for_skill(skill_path, dry_run=args.dry_run)
        print(message)

        sys.exit(0 if success else 1)

    # All skills mode
    skill_paths = find_all_skills(repo_root)

    if not skill_paths:
        print("❌ No skills found")
        sys.exit(1)

    print(f"Found {len(skill_paths)} skills")
    print()

    # Process each skill
    results = {
        'success': 0,
        'failed': 0,
        'skipped': 0
    }

    errors = []

    for skill_path in skill_paths:
        skill_name = skill_path.name
        how_to_use_path = skill_path / "HOW_TO_USE.md"

        # Skip if already exists (unless dry run)
        if how_to_use_path.exists() and not args.dry_run:
            print(f"⊘ Skipped {skill_name} (already exists)")
            results['skipped'] += 1
            continue

        success, message = generate_for_skill(skill_path, dry_run=args.dry_run)

        if success:
            print(message)
            results['success'] += 1
        else:
            print(f"✗ {skill_name}: {message}")
            results['failed'] += 1
            errors.append((skill_name, message))

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Success: {results['success']}")
    print(f"✗ Failed:  {results['failed']}")
    print(f"⊘ Skipped: {results['skipped']}")
    print(f"Total:     {len(skill_paths)}")
    print()

    if errors:
        print("ERRORS:")
        for skill_name, error in errors:
            print(f"  • {skill_name}: {error}")
        print()

    if args.dry_run:
        print("⚠️  DRY RUN - No files were written")
        print("Run without --dry-run to create files")

    sys.exit(0 if results['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
