#!/bin/bash
# Validate all skills with cleanup checks
# Usage: bash scripts/validate_all_skills.sh

REPO_ROOT="/Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My Drive/Websites/GitHub/claude-skills"
cd "$REPO_ROOT"

echo "# Skill Validation Report - Enhanced Standards v1.1.0"
echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "| Skill | Standard (9) | With Cleanup (10) | Issues |"
echo "|-------|-------------|-------------------|--------|"

for skill_dir in skills/*/*; do
    if [ -d "$skill_dir/scripts" ]; then
        skill_name=$(basename "$skill_dir")
        team_name=$(basename $(dirname "$skill_dir"))

        # Run standard validation (9 checks)
        standard_result=$(python3 scripts/skill_builder.py --validate "$skill_dir" 2>&1)
        standard_passed=$(echo "$standard_result" | grep "Results:" | awk '{print $2}')

        # Run cleanup validation (10 checks)
        cleanup_result=$(python3 scripts/skill_builder.py --validate "$skill_dir" --validate-cleanup 2>&1)
        cleanup_passed=$(echo "$cleanup_result" | grep "Results:" | awk '{print $2}')

        # Extract issues
        issues=$(echo "$cleanup_result" | grep "✗" | cut -d: -f1 | sed 's/✗ //' | tr '\n' '; ' | sed 's/; $//')

        if [ -z "$issues" ]; then
            issues="None"
        fi

        echo "| $team_name/$skill_name | $standard_passed | $cleanup_passed | $issues |"
    fi
done

echo ""
echo "## Summary Statistics"
echo ""
python3 << 'PYEOF'
import subprocess
import re

skills = []
for line in subprocess.check_output(['find', 'skills', '-type', 'd', '-name', 'scripts']).decode().strip().split('\n'):
    skill_dir = line.replace('/scripts', '')
    result = subprocess.check_output(['python3', 'scripts/skill_builder.py', '--validate', skill_dir, '--validate-cleanup'],
                                    stderr=subprocess.STDOUT).decode()

    passed = int(re.search(r'Results: (\d+)/(\d+)', result).group(1))
    total = int(re.search(r'Results: (\d+)/(\d+)', result).group(2))

    skills.append({
        'path': skill_dir,
        'passed': passed,
        'total': total,
        'percent': (passed/total)*100
    })

perfect = len([s for s in skills if s['passed'] == s['total']])
print(f"✓ Perfect (10/10): {perfect}/{len(skills)} skills ({(perfect/len(skills))*100:.1f}%)")

need_work = len([s for s in skills if s['passed'] < s['total']])
print(f"✗ Need Work: {need_work}/{len(skills)} skills ({(need_work/len(skills))*100:.1f}%)")

print(f"\nAverage Score: {sum(s['percent'] for s in skills)/len(skills):.1f}%")
PYEOF
