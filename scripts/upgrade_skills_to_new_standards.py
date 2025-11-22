#!/usr/bin/env python3
"""
Upgrade Skills to New Standards

Automatically upgrades all existing skills to meet new validation requirements:
1. Add extended metadata YAML field
2. Make Python tools executable (chmod +x)
3. Create missing assets/ directories
4. Add missing SKILL.md sections (Overview, Core Capabilities, Key Workflows)
5. Create missing scripts/ directories (if needed)

Usage:
    python scripts/upgrade_skills_to_new_standards.py                # Dry run (preview)
    python scripts/upgrade_skills_to_new_standards.py --execute     # Apply changes
    python scripts/upgrade_skills_to_new_standards.py --skill content-creator  # Single skill
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class SkillUpgrader:
    """Upgrade existing skills to meet new validation standards"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.skills_dir = Path("skills")
        self.changes_made = []
        self.errors = []

    def find_all_skills(self) -> List[Path]:
        """Find all skill directories"""
        skills = []
        for team_dir in self.skills_dir.iterdir():
            if not team_dir.is_dir() or team_dir.name.startswith('.'):
                continue
            for skill_dir in team_dir.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                    if (skill_dir / "SKILL.md").exists():
                        skills.append(skill_dir)
        return sorted(skills)

    def upgrade_skill(self, skill_path: Path) -> Tuple[int, List[str]]:
        """
        Upgrade a single skill to new standards

        Returns:
            (fixes_applied, changes_list)
        """
        skill_name = f"{skill_path.parent.name}/{skill_path.name}"
        print(f"\n{'='*70}")
        print(f"Upgrading: {skill_name}")
        print(f"{'='*70}")

        changes = []
        fixes = 0

        # Fix 1: Make Python tools executable
        fix_count = self.fix_python_tool_permissions(skill_path)
        if fix_count > 0:
            changes.append(f"  ✓ Made {fix_count} Python tools executable")
            fixes += 1

        # Fix 2: Create missing assets/ directory
        if self.fix_missing_assets_directory(skill_path):
            changes.append(f"  ✓ Created assets/ directory")
            fixes += 1

        # Fix 3: Create missing scripts/ directory (if needed)
        if self.fix_missing_scripts_directory(skill_path):
            changes.append(f"  ✓ Created scripts/ directory")
            fixes += 1

        # Fix 4: Add extended metadata YAML field
        if self.fix_missing_metadata(skill_path):
            changes.append(f"  ✓ Added extended metadata YAML field")
            fixes += 1

        # Fix 5: Add missing SKILL.md sections
        sections_added = self.fix_missing_skill_sections(skill_path)
        if sections_added:
            changes.append(f"  ✓ Added sections: {', '.join(sections_added)}")
            fixes += 1

        if changes:
            print("\n".join(changes))
            self.changes_made.extend(changes)
        else:
            print("  No changes needed")

        return fixes, changes

    def fix_python_tool_permissions(self, skill_path: Path) -> int:
        """Make Python tools executable"""
        scripts_dir = skill_path / "scripts"
        if not scripts_dir.exists():
            return 0

        fixed = 0
        for tool in scripts_dir.glob("*.py"):
            if not os.access(tool, os.X_OK):
                if not self.dry_run:
                    tool.chmod(tool.stat().st_mode | 0o111)  # Add execute for all
                print(f"    chmod +x {tool}")
                fixed += 1

        return fixed

    def fix_missing_assets_directory(self, skill_path: Path) -> bool:
        """Create assets/ directory if missing"""
        assets_dir = skill_path / "assets"
        if assets_dir.exists():
            return False

        if not self.dry_run:
            assets_dir.mkdir(exist_ok=True)
            (assets_dir / ".gitkeep").touch()

        print(f"    mkdir {assets_dir}/")
        print(f"    touch {assets_dir}/.gitkeep")
        return True

    def fix_missing_scripts_directory(self, skill_path: Path) -> bool:
        """Create scripts/ directory if missing"""
        scripts_dir = skill_path / "scripts"
        if scripts_dir.exists():
            return False

        if not self.dry_run:
            scripts_dir.mkdir(exist_ok=True)
            (scripts_dir / ".gitkeep").touch()

        print(f"    mkdir {scripts_dir}/")
        print(f"    touch {scripts_dir}/.gitkeep")
        return True

    def fix_missing_metadata(self, skill_path: Path) -> bool:
        """Add extended metadata YAML field to SKILL.md frontmatter"""
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            return False

        content = skill_md.read_text()

        # Check if metadata already exists
        if re.search(r'^\s*metadata:\s*$', content, re.MULTILINE):
            return False

        # Extract existing frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            print("    ⚠️  No YAML frontmatter found")
            return False

        frontmatter = match.group(1)
        rest_of_content = content[match.end():]

        # Extract key info for metadata
        name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
        desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)

        skill_name = name_match.group(1).strip() if name_match else skill_path.name

        # Determine domain from team
        team_name = skill_path.parent.name
        domain_map = {
            'marketing-team': 'marketing',
            'product-team': 'product',
            'engineering-team': 'engineering',
            'delivery-team': 'delivery'
        }
        domain = domain_map.get(team_name, 'general')

        # Extract existing keywords or generate defaults
        keywords = self.extract_keywords_from_description(
            desc_match.group(1) if desc_match else ""
        )

        # Find Python tools
        scripts_dir = skill_path / "scripts"
        python_tools = []
        if scripts_dir.exists():
            python_tools = [f.name for f in scripts_dir.glob("*.py")]

        # Determine tech stack (basic inference)
        tech_stack = ["Python 3.8+"]
        if "sql" in skill_name.lower() or "database" in skill_name.lower():
            tech_stack.append("PostgreSQL")
        if "data" in skill_name.lower():
            tech_stack.extend(["Pandas", "NumPy"])
        if "ml" in skill_name.lower() or "machine" in skill_name.lower():
            tech_stack.extend(["scikit-learn", "TensorFlow"])

        # Build metadata section
        metadata = f"""metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: {domain}
  domain: {skill_name.replace('-', ' ')}
  updated: {datetime.now().strftime('%Y-%m-%d')}
  keywords:"""

        for kw in keywords[:10]:  # Limit to 10 keywords
            metadata += f"\n    - {kw}"

        metadata += f"\n  tech-stack:"
        for tech in tech_stack:
            metadata += f"\n    - {tech}"

        if python_tools:
            metadata += f"\n  python-tools:"
            for tool in python_tools:
                metadata += f"\n    - {tool}"

        # Insert metadata before closing ---
        new_frontmatter = frontmatter + "\n" + metadata + "\n"
        new_content = f"---\n{new_frontmatter}---{rest_of_content}"

        if not self.dry_run:
            skill_md.write_text(new_content)

        print(f"    Updated {skill_md}")
        return True

    def extract_keywords_from_description(self, description: str) -> List[str]:
        """Extract keywords from skill description"""
        # Common words to filter out
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                      'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is'}

        # Extract meaningful words
        words = re.findall(r'\b[a-z]{3,}\b', description.lower())
        keywords = [w for w in words if w not in stop_words]

        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)

        return unique_keywords[:15]  # Return up to 15 keywords

    def fix_missing_skill_sections(self, skill_path: Path) -> List[str]:
        """Add missing SKILL.md sections (Overview, Core Capabilities, Key Workflows)"""
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            return []

        content = skill_md.read_text()
        sections_added = []

        # Check for missing sections
        has_overview = bool(re.search(r'^## Overview\s*$', content, re.MULTILINE))
        has_core_capabilities = bool(re.search(r'^## Core Capabilities\s*$', content, re.MULTILINE))
        has_key_workflows = bool(re.search(r'^## Key Workflows\s*$', content, re.MULTILINE))

        if has_overview and has_core_capabilities and has_key_workflows:
            return []  # All sections present

        # Find insertion point (after YAML frontmatter and title)
        match = re.search(r'^---\n.*?\n---\n\n#\s+[^\n]+\n', content, re.DOTALL)
        if not match:
            print("    ⚠️  Could not find insertion point")
            return []

        insertion_point = match.end()
        before = content[:insertion_point]
        after = content[insertion_point:]

        # Build sections to add
        new_sections = []

        if not has_overview:
            new_sections.append("""
## Overview

This skill provides [TODO: Add 2-3 sentence overview].

**Core Value:** [TODO: Add value proposition with metrics]

**Target Audience:** [TODO: Define target users]

**Use Cases:** [TODO: List 3-5 primary use cases]
""")
            sections_added.append("Overview")

        if not has_core_capabilities:
            new_sections.append("""
## Core Capabilities

- **[Capability 1]** - [Description]
- **[Capability 2]** - [Description]
- **[Capability 3]** - [Description]
- **[Capability 4]** - [Description]
""")
            sections_added.append("Core Capabilities")

        if not has_key_workflows:
            new_sections.append("""
## Key Workflows

### Workflow 1: [Workflow Name]

**Time:** [Duration estimate]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Output:** [What success looks like]

### Workflow 2: [Workflow Name]

**Time:** [Duration estimate]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Output:** [What success looks like]
""")
            sections_added.append("Key Workflows")

        if new_sections:
            new_content = before + "\n".join(new_sections) + "\n" + after

            if not self.dry_run:
                skill_md.write_text(new_content)

            print(f"    Updated {skill_md}")

        return sections_added

    def generate_report(self, skills_upgraded: int, total_fixes: int):
        """Generate upgrade summary report"""
        print("\n" + "="*70)
        print("UPGRADE SUMMARY")
        print("="*70)
        print(f"\nSkills Upgraded: {skills_upgraded}")
        print(f"Total Fixes Applied: {total_fixes}")

        if self.dry_run:
            print("\n⚠️  DRY RUN MODE - No changes were made")
            print("Run with --execute to apply changes")
        else:
            print("\n✅ Changes Applied Successfully")

        if self.changes_made:
            print(f"\nChanges Made ({len(self.changes_made)}):")
            for change in self.changes_made[:20]:  # Show first 20
                print(change)
            if len(self.changes_made) > 20:
                print(f"  ... and {len(self.changes_made) - 20} more")

        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Upgrade skills to new validation standards"
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Apply changes (default is dry run)'
    )
    parser.add_argument(
        '--skill',
        help='Upgrade specific skill only (e.g., content-creator)'
    )

    args = parser.parse_args()

    upgrader = SkillUpgrader(dry_run=not args.execute)

    # Find skills to upgrade
    if args.skill:
        # Find specific skill
        skills = [s for s in upgrader.find_all_skills() if args.skill in str(s)]
        if not skills:
            print(f"❌ Skill not found: {args.skill}")
            return 1
    else:
        skills = upgrader.find_all_skills()

    print(f"Found {len(skills)} skills to upgrade")

    if not args.execute:
        print("\n⚠️  DRY RUN MODE - Previewing changes only")
        print("Run with --execute to apply changes\n")

    # Upgrade each skill
    total_fixes = 0
    skills_upgraded = 0

    for skill_path in skills:
        try:
            fixes, changes = upgrader.upgrade_skill(skill_path)
            if fixes > 0:
                skills_upgraded += 1
                total_fixes += fixes
        except Exception as e:
            error_msg = f"Error upgrading {skill_path.name}: {e}"
            print(f"  ❌ {error_msg}")
            upgrader.errors.append(error_msg)

    # Generate report
    upgrader.generate_report(skills_upgraded, total_fixes)

    return 0 if not upgrader.errors else 1


if __name__ == "__main__":
    sys.exit(main())
