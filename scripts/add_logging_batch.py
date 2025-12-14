#!/usr/bin/env python3
"""
Batch add logging to Python scripts
"""
import re
from pathlib import Path

FILES_TO_UPDATE = [
    "skills/engineering-team/legacy-codebase-analyzer/scripts/architecture_health_analyzer.py",
    "skills/engineering-team/legacy-codebase-analyzer/scripts/code_quality_analyzer.py",
    "skills/engineering-team/legacy-codebase-analyzer/scripts/codebase_inventory.py",
    "skills/engineering-team/legacy-codebase-analyzer/scripts/modernization_roadmap_generator.py",
    "skills/engineering-team/legacy-codebase-analyzer/scripts/performance_bottleneck_detector.py",
    "skills/engineering-team/legacy-codebase-analyzer/scripts/security_vulnerability_scanner.py",
    "skills/engineering-team/legacy-codebase-analyzer/scripts/technical_debt_scorer.py",
]

def add_logging_to_file(file_path: Path):
    """Add logging to a Python file"""
    content = file_path.read_text()

    # Check if logging already added
    if 'import logging' in content and 'logger = logging.getLogger(__name__)' in content:
        print(f"✓ {file_path.name} already has logging")
        return False

    # Find import section
    import_match = re.search(r'(import \w+\n(?:import \w+\n|from \w+.*?\n)*)', content)
    if not import_match:
        print(f"✗ {file_path.name} - Could not find import section")
        return False

    # Add logging import (alphabetically)
    imports = import_match.group(1)
    if 'import logging' not in imports:
        import_lines = imports.strip().split('\n')
        import_lines.append('import logging')
        import_lines.sort()
        new_imports = '\n'.join(import_lines) + '\n'
        content = content.replace(imports, new_imports)

    # Add logging configuration after imports
    config_block = """
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
"""

    # Find where to insert (after all imports, before first class/function)
    class_match = re.search(r'\n(class |def |@dataclass)', content)
    if class_match:
        insert_pos = class_match.start()
        content = content[:insert_pos] + config_block + content[insert_pos:]

    # Find __init__ methods and add logging
    init_pattern = r'(    def __init__\(self[^)]*\):)\n(        .*?)\n(        .*?)\n'

    def add_init_logging(match):
        method_def = match.group(1)
        first_line = match.group(2)
        second_line = match.group(3)

        # Check if verbose parameter exists
        has_verbose = 'verbose' in method_def

        additions = []
        if has_verbose and 'if verbose:' not in first_line:
            additions.append('        if verbose:')
            additions.append('            logging.getLogger().setLevel(logging.DEBUG)')

        # Find class name
        class_match = re.search(r'class (\w+)', content[:match.start()])
        if class_match:
            class_name = class_match.group(1)
            additions.append(f'        logger.debug("{class_name} initialized")')

        if additions:
            insert = '\n' + '\n'.join(additions) + '\n'
            return method_def + '\n' + first_line + '\n' + insert + second_line + '\n'
        return match.group(0)

    content = re.sub(init_pattern, add_init_logging, content)

    # Write back
    file_path.write_text(content)
    print(f"✓ {file_path.name} updated with logging")
    return True

def main():
    base_path = Path(__file__).parent.parent

    for file_rel_path in FILES_TO_UPDATE:
        file_path = base_path / file_rel_path
        if file_path.exists():
            add_logging_to_file(file_path)
        else:
            print(f"✗ File not found: {file_path}")

if __name__ == '__main__':
    main()
