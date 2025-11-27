#!/usr/bin/env python3
"""
Validate All Skills - Batch validation script

Tests skill_builder.py validation against all existing skills
"""

import subprocess
from pathlib import Path
import sys

def main():
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / "skills"

    # Directories to exclude from validation (not actual skills)
    EXCLUDED_DIRS = {'packaged-skills'}

    all_skills = []
    for team_dir in skills_dir.iterdir():
        if not team_dir.is_dir() or team_dir.name.startswith('.'):
            continue

        for skill_dir in team_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('.') and skill_dir.name not in EXCLUDED_DIRS:
                all_skills.append(skill_dir)

    print(f"Found {len(all_skills)} skills to validate")
    print("=" * 70)
    print()

    passed = 0
    failed = 0
    results = []

    for skill_path in sorted(all_skills):
        skill_name = f"{skill_path.parent.name}/{skill_path.name}"

        result = subprocess.run(
            ['python3', 'scripts/skill_builder.py', '--validate', str(skill_path)],
            cwd=repo_root,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            passed += 1
            status = "✅ PASS"
        else:
            failed += 1
            status = "❌ FAIL"

        # Extract checks passed/total
        checks_line = [line for line in result.stdout.split('\n') if 'checks passed' in line]
        checks_info = checks_line[0].split(':')[1].strip() if checks_line else "unknown"

        results.append({
            'name': skill_name,
            'status': status,
            'checks': checks_info
        })

        print(f"{status} {skill_name:50s} {checks_info}")

    print()
    print("=" * 70)
    print(f"Summary: {passed}/{len(all_skills)} passed ({passed*100//len(all_skills)}%)")
    print()

    if failed > 0:
        print("Failed skills:")
        for r in results:
            if '❌' in r['status']:
                print(f"  - {r['name']}")

    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
