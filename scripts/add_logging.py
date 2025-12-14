#!/usr/bin/env python3
"""
Add Logging to Python Scripts

Automatically adds logging import and configuration to Python scripts
that don't already have logging.
"""

import os
import re
import sys
from pathlib import Path

def has_logging(content: str) -> bool:
    """Check if script already has logging import"""
    return 'import logging' in content

def add_logging_to_script(filepath: Path) -> bool:
    """
    Add logging to a Python script.

    Returns True if modified, False if already has logging or error.
    """
    try:
        content = filepath.read_text()

        if has_logging(content):
            return False

        # Find the import section - look for the last import line
        lines = content.split('\n')

        # Find where imports end (look for first non-import, non-comment, non-blank line after imports start)
        import_end_idx = 0
        in_imports = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Skip initial comments, docstrings
            if not in_imports:
                if stripped.startswith('import ') or stripped.startswith('from '):
                    in_imports = True
                    import_end_idx = i
            else:
                # Continue tracking imports
                if stripped.startswith('import ') or stripped.startswith('from '):
                    import_end_idx = i
                elif stripped == '' or stripped.startswith('#'):
                    continue
                elif stripped.startswith('"""') or stripped.startswith("'''"):
                    # Skip multi-line strings between imports
                    continue
                else:
                    # We've hit non-import code
                    break

        # Insert logging import alphabetically after other imports
        # Find right place to insert (after 'import json' or similar)
        insert_idx = import_end_idx + 1

        for i, line in enumerate(lines[:import_end_idx + 1]):
            if line.strip().startswith('import ') and 'logging' > line.strip().split()[1]:
                insert_idx = i + 1

        # Look for where 'import logging' should go alphabetically
        for i, line in enumerate(lines[:import_end_idx + 1]):
            stripped = line.strip()
            if stripped.startswith('import '):
                module = stripped.split()[1].split('.')[0]
                if module > 'logging':
                    insert_idx = i
                    break

        # Insert logging import
        logging_import = 'import logging'
        lines.insert(insert_idx, logging_import)

        # Find where to add logging configuration (after all imports)
        config_idx = import_end_idx + 2  # +2 because we added one line

        # Skip any blank lines after imports
        while config_idx < len(lines) and lines[config_idx].strip() == '':
            config_idx += 1

        # Insert logging configuration
        logging_config = """
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
"""
        lines.insert(config_idx, logging_config)

        # Write back
        new_content = '\n'.join(lines)
        filepath.write_text(new_content)
        return True

    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False


def find_scripts_without_logging(skills_dir: Path) -> list:
    """Find all Python scripts in skills directory without logging"""
    scripts = []
    for script_path in skills_dir.rglob('scripts/*.py'):
        content = script_path.read_text()
        if not has_logging(content):
            scripts.append(script_path)
    return sorted(scripts)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Add logging to Python scripts without it'
    )
    parser.add_argument(
        '--skills-dir',
        type=Path,
        default=Path('skills'),
        help='Skills directory path (default: skills)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be modified without making changes'
    )
    parser.add_argument(
        '--file',
        type=Path,
        help='Process single file instead of all scripts'
    )

    args = parser.parse_args()

    if args.file:
        scripts = [args.file]
    else:
        scripts = find_scripts_without_logging(args.skills_dir)

    print(f"Found {len(scripts)} scripts without logging")

    modified = 0
    for script in scripts:
        if args.dry_run:
            print(f"  Would modify: {script}")
        else:
            if add_logging_to_script(script):
                print(f"  Modified: {script}")
                modified += 1
            else:
                print(f"  Skipped: {script}")

    if not args.dry_run:
        print(f"\nModified {modified} scripts")


if __name__ == '__main__':
    main()
