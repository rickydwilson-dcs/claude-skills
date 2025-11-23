#!/usr/bin/env python3
"""
Validate all skills and generate comprehensive report
"""

import subprocess
import re
from pathlib import Path
from datetime import datetime

def run_validation(skill_path, include_cleanup=False):
    """Run validation and parse results"""
    cmd = ['python3', 'scripts/skill_builder.py', '--validate', str(skill_path)]
    if include_cleanup:
        cmd.append('--validate-cleanup')

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        output = result.stdout + result.stderr

        # Parse results
        results_match = re.search(r'Results: (\d+)/(\d+)', output)
        if results_match:
            passed = int(results_match.group(1))
            total = int(results_match.group(2))
        else:
            return None

        # Extract failed checks
        failed_checks = []
        for line in output.split('\n'):
            if line.startswith('✗'):
                check_name = line.split(':')[0].replace('✗ ', '').strip()
                failed_checks.append(check_name)

        return {
            'passed': passed,
            'total': total,
            'percent': (passed/total)*100 if total > 0 else 0,
            'failed_checks': failed_checks
        }
    except Exception as e:
        print(f"Error validating {skill_path}: {e}")
        return None

def main():
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / 'skills'

    print("# Skill Validation Report - Enhanced Standards v1.1.0")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Find all skills
    skill_paths = []
    for team_dir in skills_dir.iterdir():
        if team_dir.is_dir() and not team_dir.name.startswith('.'):
            for skill_dir in team_dir.iterdir():
                if skill_dir.is_dir() and (skill_dir / 'scripts').exists():
                    skill_paths.append(skill_dir)

    print(f"Found {len(skill_paths)} skills to validate")
    print()

    # Validate all skills
    results = []
    for skill_path in sorted(skill_paths):
        team_name = skill_path.parent.name
        skill_name = skill_path.name

        print(f"Validating {team_name}/{skill_name}...", end=' ')

        standard = run_validation(skill_path, include_cleanup=False)
        cleanup = run_validation(skill_path, include_cleanup=True)

        if standard and cleanup:
            results.append({
                'team': team_name,
                'skill': skill_name,
                'path': skill_path,
                'standard': standard,
                'cleanup': cleanup
            })

            status = "✓" if cleanup['passed'] == cleanup['total'] else "✗"
            print(f"{status} {cleanup['passed']}/{cleanup['total']}")
        else:
            print("ERROR")

    print()
    print("## Detailed Results")
    print()
    print("| Team | Skill | Standard (9) | With Cleanup (10) | Failed Checks |")
    print("|------|-------|--------------|-------------------|---------------|")

    for r in results:
        team = r['team']
        skill = r['skill']
        std_score = f"{r['standard']['passed']}/{r['standard']['total']}"
        cleanup_score = f"{r['cleanup']['passed']}/{r['cleanup']['total']}"
        failed = ', '.join(r['cleanup']['failed_checks']) if r['cleanup']['failed_checks'] else 'None'

        print(f"| {team} | {skill} | {std_score} | {cleanup_score} | {failed} |")

    print()
    print("## Summary Statistics")
    print()

    perfect_standard = len([r for r in results if r['standard']['passed'] == r['standard']['total']])
    perfect_cleanup = len([r for r in results if r['cleanup']['passed'] == r['cleanup']['total']])

    print(f"**Standard Validation (9 checks):**")
    print(f"- Perfect (9/9): {perfect_standard}/{len(results)} skills ({(perfect_standard/len(results))*100:.1f}%)")
    print(f"- Need Work: {len(results)-perfect_standard}/{len(results)} skills")
    print()

    print(f"**With Cleanup Validation (10 checks):**")
    print(f"- Perfect (10/10): {perfect_cleanup}/{len(results)} skills ({(perfect_cleanup/len(results))*100:.1f}%)")
    print(f"- Need Work: {len(results)-perfect_cleanup}/{len(results)} skills")
    print()

    avg_cleanup = sum(r['cleanup']['percent'] for r in results) / len(results)
    print(f"**Average Score (with cleanup): {avg_cleanup:.1f}%**")
    print()

    # Group by issue type
    print("## Common Issues")
    print()
    issue_counts = {}
    for r in results:
        for check in r['cleanup']['failed_checks']:
            issue_counts[check] = issue_counts.get(check, 0) + 1

    for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"- **{issue}**: {count} skills ({(count/len(results))*100:.1f}%)")

    print()
    print("## Skills Requiring Attention")
    print()

    needs_work = [r for r in results if r['cleanup']['passed'] < r['cleanup']['total']]
    for r in sorted(needs_work, key=lambda x: x['cleanup']['percent']):
        score = f"{r['cleanup']['passed']}/{r['cleanup']['total']}"
        issues = ', '.join(r['cleanup']['failed_checks'])
        print(f"- **{r['team']}/{r['skill']}** ({score}): {issues}")

if __name__ == '__main__':
    main()
