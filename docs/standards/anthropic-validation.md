# Anthropic Agent Skills Validation Framework

**Purpose:** Ensure all refactored skills meet Anthropic's official Agent Skills standards
**Version:** 1.0
**Last Updated:** November 17, 2025

---

## Table of Contents

- [Anthropic Standards Reference](#anthropic-standards-reference)
- [Validation Layers](#validation-layers)
- [Automated Validation](#automated-validation)
- [Manual Validation Checklist](#manual-validation-checklist)
- [Claude Activation Testing](#claude-activation-testing)
- [Validation Tools](#validation-tools)

---

## Anthropic Standards Reference

### Official Anthropic Agent Skills Specification

Based on Anthropic's official guidelines, skills should follow these principles:

#### 1. **Focused Scope**
- ✅ One skill = one clear capability (not entire domains)
- ✅ Skills should have a single, well-defined purpose
- ❌ Avoid "swiss army knife" skills that do everything

#### 2. **Lean SKILL.md**
- ✅ Target: 50-200 lines (core instructions only)
- ✅ Quick to load, easy to scan
- ❌ Avoid long-form documentation in SKILL.md

#### 3. **Progressive Disclosure**
- ✅ Metadata → SKILL.md → References → Scripts
- ✅ Users discover details as needed
- ✅ Core info in SKILL.md, details in references/

#### 4. **Rich Descriptions**
- ✅ What the skill does
- ✅ When to use it (triggers)
- ✅ Keywords users might say
- ✅ Clear activation patterns

#### 5. **Proper Metadata**
- ✅ License declaration (MIT, Apache, etc.)
- ✅ Version tracking (semantic versioning)
- ✅ Category classification
- ✅ Author attribution

#### 6. **Tool Restrictions**
- ✅ Use `allowed-tools` for security when appropriate
- ✅ Restrict read-only skills (code-reviewer, audit)
- ✅ Document why restrictions are in place

#### 7. **Keywords Section**
- ✅ Help users discover skills
- ✅ 10-20 terms users would actually say
- ✅ Include variations and synonyms

---

## Validation Layers

We use a **5-layer validation approach** to ensure compliance:

### Layer 1: Automated Structural Validation
- YAML frontmatter syntax validation
- Required fields presence check
- Line count verification
- Link integrity checking

### Layer 2: Anthropic Standards Compliance
- Manual checklist review against official standards
- Structure pattern matching
- Progressive disclosure verification

### Layer 3: Claude Activation Testing
- Real-world testing with Claude AI
- Trigger phrase validation
- Keyword effectiveness testing

### Layer 4: Functional Testing
- Python scripts execution
- Reference file accessibility
- Asset availability

### Layer 5: User Experience Review
- Clarity and readability
- Example quality
- Documentation completeness

---

## Automated Validation

### Tool: `tools/validate_skills.py`

**Purpose:** Automated checking of structural requirements

```python
#!/usr/bin/env python3
"""
Validate all SKILL.md files against Anthropic standards.

Checks:
1. Valid YAML frontmatter
2. Required metadata fields
3. Line count (warn if >250, target: 100-200)
4. Keywords section present
5. Reference links valid (relative paths work)
6. Description includes trigger phrases
7. No broken internal links
8. Proper tool restrictions where appropriate

Usage:
    python tools/validate_skills.py
    python tools/validate_skills.py --skill content-creator
    python tools/validate_skills.py --output json --file report.json
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

class SkillValidator:
    """Validate skills against Anthropic standards."""

    REQUIRED_FIELDS = [
        'name',
        'description',
        'license',
        'metadata.version',
        'metadata.author',
        'metadata.category',
        'metadata.updated'
    ]

    TARGET_LINE_COUNT = (100, 200)
    WARNING_LINE_COUNT = 250

    CATEGORIES = [
        'marketing',
        'c-level',
        'product',
        'engineering',
        'project-management',
        'regulatory-quality'
    ]

    # Skills that should have allowed-tools restrictions
    RESTRICTED_SKILLS = [
        'code-reviewer',      # Read-only review
        'senior-architect',   # Analysis-heavy
        'senior-qa',          # Testing execution
        'qms-audit-expert',   # Read-only audit
        'isms-audit-expert'   # Read-only audit
    ]

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.results = []

    def validate_skill(self, skill_path: Path) -> Dict:
        """Validate a single SKILL.md file."""
        result = {
            'skill': str(skill_path.relative_to(self.repo_root)),
            'status': 'pass',
            'checks': {},
            'warnings': [],
            'errors': []
        }

        content = skill_path.read_text()

        # Check 1: Valid YAML frontmatter
        frontmatter = self._extract_frontmatter(content)
        if frontmatter is None:
            result['errors'].append('Invalid or missing YAML frontmatter')
            result['status'] = 'fail'
            return result

        result['checks']['yaml_valid'] = True

        # Check 2: Required fields
        missing_fields = self._check_required_fields(frontmatter)
        if missing_fields:
            result['errors'].append(f'Missing required fields: {", ".join(missing_fields)}')
            result['status'] = 'fail'
        result['checks']['required_fields'] = len(missing_fields) == 0

        # Check 3: Line count
        line_count = len(content.splitlines())
        result['checks']['line_count'] = line_count
        if line_count > self.WARNING_LINE_COUNT:
            result['warnings'].append(f'Line count ({line_count}) exceeds warning threshold ({self.WARNING_LINE_COUNT}). Target: {self.TARGET_LINE_COUNT[0]}-{self.TARGET_LINE_COUNT[1]}')
        elif line_count < self.TARGET_LINE_COUNT[0]:
            result['warnings'].append(f'Line count ({line_count}) below target minimum ({self.TARGET_LINE_COUNT[0]})')

        # Check 4: Keywords section
        has_keywords = self._check_keywords_section(content)
        result['checks']['keywords_section'] = has_keywords
        if not has_keywords:
            result['errors'].append('Missing ## Keywords section')
            result['status'] = 'fail'

        # Check 5: Description quality
        desc_check = self._check_description_quality(frontmatter.get('description', ''))
        result['checks']['description_quality'] = desc_check
        if not desc_check['has_triggers']:
            result['warnings'].append('Description missing "Use when" trigger phrases')
        if not desc_check['has_keywords']:
            result['warnings'].append('Description missing "or when user mentions" keywords')

        # Check 6: License present
        if 'license' not in frontmatter:
            result['errors'].append('Missing license field')
            result['status'] = 'fail'
        result['checks']['license'] = 'license' in frontmatter

        # Check 7: Version format (semantic versioning)
        version = frontmatter.get('metadata', {}).get('version', '')
        version_valid = bool(re.match(r'^\d+\.\d+\.\d+$', version))
        result['checks']['semantic_version'] = version_valid
        if not version_valid:
            result['warnings'].append(f'Version "{version}" not semantic (expected x.y.z)')

        # Check 8: Category valid
        category = frontmatter.get('metadata', {}).get('category', '')
        category_valid = category in self.CATEGORIES
        result['checks']['category_valid'] = category_valid
        if not category_valid:
            result['errors'].append(f'Invalid category "{category}". Must be one of: {", ".join(self.CATEGORIES)}')
            result['status'] = 'fail'

        # Check 9: Tool restrictions (if applicable)
        skill_name = frontmatter.get('name', '')
        if skill_name in self.RESTRICTED_SKILLS:
            has_allowed_tools = 'allowed-tools' in frontmatter
            result['checks']['tool_restrictions'] = has_allowed_tools
            if not has_allowed_tools:
                result['warnings'].append(f'Skill "{skill_name}" should have allowed-tools restrictions')

        # Check 10: Reference links integrity
        broken_links = self._check_reference_links(content, skill_path)
        result['checks']['reference_links'] = len(broken_links) == 0
        if broken_links:
            result['errors'].append(f'Broken reference links: {", ".join(broken_links)}')
            result['status'] = 'fail'

        # Check 11: Standard sections present
        sections = self._check_standard_sections(content)
        result['checks']['standard_sections'] = sections
        missing_sections = [s for s, present in sections.items() if not present]
        if missing_sections:
            result['warnings'].append(f'Missing recommended sections: {", ".join(missing_sections)}')

        return result

    def _extract_frontmatter(self, content: str) -> dict:
        """Extract and parse YAML frontmatter."""
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None

        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None

    def _check_required_fields(self, frontmatter: dict) -> List[str]:
        """Check for required fields in frontmatter."""
        missing = []
        for field in self.REQUIRED_FIELDS:
            parts = field.split('.')
            current = frontmatter
            for part in parts:
                if not isinstance(current, dict) or part not in current:
                    missing.append(field)
                    break
                current = current[part]
        return missing

    def _check_keywords_section(self, content: str) -> bool:
        """Check if ## Keywords section exists."""
        return bool(re.search(r'^## Keywords\s*\n', content, re.MULTILINE))

    def _check_description_quality(self, description: str) -> Dict:
        """Check description has triggers and keywords."""
        return {
            'has_triggers': 'Use when' in description or 'use when' in description,
            'has_keywords': 'user mentions' in description or 'when user' in description,
            'length': len(description),
            'has_capability_summary': len(description) > 100
        }

    def _check_reference_links(self, content: str, skill_path: Path) -> List[str]:
        """Check that reference links point to existing files."""
        broken = []
        skill_dir = skill_path.parent

        # Find all markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

        for text, link in links:
            # Only check relative links to references/
            if link.startswith('references/') or link.startswith('./references/'):
                link_path = skill_dir / link
                if not link_path.exists():
                    broken.append(link)

        return broken

    def _check_standard_sections(self, content: str) -> Dict[str, bool]:
        """Check for recommended sections."""
        sections = {
            'Keywords': bool(re.search(r'^## Keywords', content, re.MULTILINE)),
            'Quick Start': bool(re.search(r'^## Quick Start', content, re.MULTILINE)),
            'Core Workflows': bool(re.search(r'^## (Core )?Workflows?', content, re.MULTILINE)),
            'Scripts': bool(re.search(r'^## Scripts?', content, re.MULTILINE)),
            'References': bool(re.search(r'^## References?', content, re.MULTILINE)),
            'Best Practices': bool(re.search(r'^## Best Practices', content, re.MULTILINE)),
            'Examples': bool(re.search(r'^## Examples?', content, re.MULTILINE))
        }
        return sections

    def validate_all_skills(self) -> Dict:
        """Validate all SKILL.md files in repository."""
        skill_files = list(self.repo_root.glob('*/*/SKILL.md'))

        results = {
            'total': len(skill_files),
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'skills': []
        }

        for skill_path in sorted(skill_files):
            result = self.validate_skill(skill_path)
            results['skills'].append(result)

            if result['status'] == 'pass':
                results['passed'] += 1
            else:
                results['failed'] += 1

            if result['warnings']:
                results['warnings'] += len(result['warnings'])

        return results

    def print_report(self, results: Dict):
        """Print validation report."""
        print("=" * 80)
        print("ANTHROPIC SKILLS VALIDATION REPORT")
        print("=" * 80)
        print(f"\nTotal Skills: {results['total']}")
        print(f"Passed: {results['passed']} ✅")
        print(f"Failed: {results['failed']} ❌")
        print(f"Warnings: {results['warnings']} ⚠️")
        print(f"Success Rate: {results['passed'] / results['total'] * 100:.1f}%")

        if results['failed'] > 0:
            print("\n" + "=" * 80)
            print("FAILED SKILLS")
            print("=" * 80)
            for skill_result in results['skills']:
                if skill_result['status'] == 'fail':
                    print(f"\n❌ {skill_result['skill']}")
                    for error in skill_result['errors']:
                        print(f"   ERROR: {error}")

        if results['warnings'] > 0:
            print("\n" + "=" * 80)
            print("WARNINGS")
            print("=" * 80)
            for skill_result in results['skills']:
                if skill_result['warnings']:
                    print(f"\n⚠️  {skill_result['skill']}")
                    for warning in skill_result['warnings']:
                        print(f"   WARN: {warning}")

        print("\n" + "=" * 80)
        print("DETAILED CHECKS")
        print("=" * 80)
        for skill_result in results['skills']:
            status_icon = "✅" if skill_result['status'] == 'pass' else "❌"
            print(f"\n{status_icon} {skill_result['skill']}")
            print(f"   Lines: {skill_result['checks'].get('line_count', 'N/A')}")
            print(f"   YAML Valid: {'✅' if skill_result['checks'].get('yaml_valid') else '❌'}")
            print(f"   Required Fields: {'✅' if skill_result['checks'].get('required_fields') else '❌'}")
            print(f"   Keywords Section: {'✅' if skill_result['checks'].get('keywords_section') else '❌'}")
            print(f"   License: {'✅' if skill_result['checks'].get('license') else '❌'}")
            print(f"   Reference Links: {'✅' if skill_result['checks'].get('reference_links') else '❌'}")


def main():
    """Main validation entry point."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Validate skills against Anthropic standards')
    parser.add_argument('--skill', help='Validate specific skill (e.g., content-creator)')
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--file', help='Output file path')

    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    validator = SkillValidator(repo_root)

    if args.skill:
        # Find specific skill
        skill_files = list(repo_root.glob(f'*/{args.skill}/SKILL.md'))
        if not skill_files:
            print(f"Error: Skill '{args.skill}' not found")
            return 1

        result = validator.validate_skill(skill_files[0])
        results = {
            'total': 1,
            'passed': 1 if result['status'] == 'pass' else 0,
            'failed': 0 if result['status'] == 'pass' else 1,
            'warnings': len(result['warnings']),
            'skills': [result]
        }
    else:
        # Validate all skills
        results = validator.validate_all_skills()

    if args.output == 'json':
        output = json.dumps(results, indent=2)
        if args.file:
            Path(args.file).write_text(output)
            print(f"Results written to {args.file}")
        else:
            print(output)
    else:
        validator.print_report(results)

    # Exit code: 0 if all passed, 1 if any failed
    return 0 if results['failed'] == 0 else 1


if __name__ == '__main__':
    exit(main())
```

---

## Manual Validation Checklist

For each refactored skill, manually verify:

### ✅ Anthropic Standards Compliance

#### Structure (Progressive Disclosure)
- [ ] SKILL.md is 100-200 lines (150 target)
- [ ] Detailed content moved to references/
- [ ] Scripts in scripts/ with proper --help
- [ ] Assets in assets/ (templates, samples)
- [ ] No long-form documentation in SKILL.md

#### Frontmatter (Metadata)
- [ ] YAML frontmatter valid syntax
- [ ] `name` field present and correct
- [ ] `description` field includes:
  - [ ] What the skill does (1 sentence)
  - [ ] Key capabilities (1 sentence)
  - [ ] "Use when" trigger phrases
  - [ ] "or when user mentions" keywords
- [ ] `license` field present (MIT, Apache, etc.)
- [ ] `metadata` section includes:
  - [ ] `version` (semantic: x.y.z)
  - [ ] `author` (Alireza Rezvani)
  - [ ] `category` (valid category)
  - [ ] `domain` (specific domain)
  - [ ] `updated` (YYYY-MM-DD)
  - [ ] `python-tools` (if applicable)
  - [ ] `tech-stack` (if applicable)
  - [ ] `frameworks` (if applicable)
- [ ] `allowed-tools` (if skill should be restricted)

#### Content Sections
- [ ] ## Keywords section present (10-20 terms)
- [ ] ## Quick Start section (2-3 examples)
- [ ] ## Core Workflows section (high-level overview)
- [ ] ## Scripts section (if skill has Python tools)
- [ ] ## References section (pointers to references/)
- [ ] ## Best Practices section (top 5 only)
- [ ] ## Examples section (2 concrete scenarios)

#### Quality Checks
- [ ] Clear, concise writing
- [ ] No redundancy between sections
- [ ] Proper markdown formatting
- [ ] All links work (relative paths)
- [ ] Code blocks properly formatted
- [ ] Consistent terminology

#### Keywords Quality
- [ ] 10-20 keywords listed
- [ ] Terms users would actually say
- [ ] Includes variations (e.g., "tech debt", "technical debt")
- [ ] Mix of general and specific terms
- [ ] Includes tool/framework names if relevant

#### Tool Restrictions (Security)
- [ ] Read-only skills use `allowed-tools: Read, Grep, Glob`
- [ ] Analysis skills appropriately restricted
- [ ] Audit skills read-only
- [ ] Restrictions documented if unusual

---

## Claude Activation Testing

**Purpose:** Ensure skills trigger correctly when users ask questions

### Test Protocol

For each refactored skill, perform these activation tests:

#### Test 1: Direct Mention
```
User query: "Use the [skill-name] skill to help me with [task]"
Expected: Claude activates the skill
Verification: Skill loads and provides guidance
```

#### Test 2: Trigger Phrase
```
User query: Use one of the "Use when" phrases from description
Expected: Claude activates the skill
Verification: Skill selected automatically
```

#### Test 3: Keyword Match
```
User query: Use one of the keywords from ## Keywords section
Expected: Claude activates the skill
Verification: Skill selected based on keyword
```

#### Test 4: Negative Test
```
User query: Ask about unrelated topic
Expected: Skill does NOT activate
Verification: Different skill or no skill selected
```

### Activation Test Matrix

| Skill | Direct Mention | Trigger Phrase | Keyword Match | Negative Test | Status |
|-------|----------------|----------------|---------------|---------------|--------|
| content-creator | ✅ | ✅ | ✅ | ✅ | Pass |
| product-manager-toolkit | ✅ | ✅ | ✅ | ✅ | Pass |
| senior-fullstack | ✅ | ✅ | ✅ | ✅ | Pass |
| ... | | | | | |

### Recording Test Results

```bash
# Create test log
cat > tests/skill-activation-tests.log <<EOF
Skill Activation Testing - $(date)
==================================================

Skill: content-creator
- Direct: ✅ Activated when user said "use content-creator skill"
- Trigger: ✅ Activated when user said "help me write a blog post"
- Keyword: ✅ Activated when user said "I need to optimize SEO"
- Negative: ✅ Did NOT activate when asked about database design
Status: PASS

...
EOF
```

---

## Validation Tools

### Tool 1: Automated Validator (Python)

**File:** `tools/validate_skills.py` (see code above)

**Usage:**
```bash
# Validate all skills
python tools/validate_skills.py

# Validate specific skill
python tools/validate_skills.py --skill content-creator

# Output JSON report
python tools/validate_skills.py --output json --file validation-report.json

# Check exit code
python tools/validate_skills.py && echo "All passed" || echo "Some failed"
```

**Output:**
```
================================================================================
ANTHROPIC SKILLS VALIDATION REPORT
================================================================================

Total Skills: 40
Passed: 38 ✅
Failed: 2 ❌
Warnings: 5 ⚠️
Success Rate: 95.0%

================================================================================
FAILED SKILLS
================================================================================

❌ skills/marketing-team/example-skill/SKILL.md
   ERROR: Missing required fields: metadata.version
   ERROR: Missing ## Keywords section

================================================================================
WARNINGS
================================================================================

⚠️  skills/engineering-team/senior-fullstack/SKILL.md
   WARN: Line count (215) exceeds target (100-200)
   WARN: Skill "code-reviewer" should have allowed-tools restrictions

================================================================================
DETAILED CHECKS
================================================================================

✅ skills/marketing-team/content-creator/SKILL.md
   Lines: 120
   YAML Valid: ✅
   Required Fields: ✅
   Keywords Section: ✅
   License: ✅
   Reference Links: ✅
```

### Tool 2: Line Count Tracker

**File:** `tools/track_skill_lines.py`

```python
#!/usr/bin/env python3
"""Track SKILL.md line counts before/after refactoring."""

from pathlib import Path

def track_lines():
    repo_root = Path(__file__).parent.parent
    skills = list(repo_root.glob('*/*/SKILL.md'))

    print("Skill Line Count Report")
    print("=" * 80)

    total = 0
    for skill in sorted(skills):
        lines = len(skill.read_text().splitlines())
        total += lines

        # Color code based on target
        if lines <= 150:
            status = "✅ Excellent"
        elif lines <= 200:
            status = "✓  Good"
        elif lines <= 250:
            status = "⚠️  Warning"
        else:
            status = "❌ Too long"

        print(f"{skill.relative_to(repo_root)}: {lines:3d} lines {status}")

    avg = total / len(skills)
    print("=" * 80)
    print(f"Total: {total:,} lines across {len(skills)} skills")
    print(f"Average: {avg:.0f} lines per skill")
    print(f"Target: 150 lines (current: {avg:.0f}, {((avg - 150) / 150 * 100):+.1f}%)")

if __name__ == '__main__':
    track_lines()
```

**Usage:**
```bash
python tools/track_skill_lines.py
```

### Tool 3: Reference Link Checker

**File:** `tools/check_references.sh`

```bash
#!/bin/bash
# Check that all reference links in SKILL.md files work

echo "Checking reference links..."

failures=0

for skill in $(find . -name "SKILL.md"); do
    skill_dir=$(dirname "$skill")

    # Extract all markdown links to references/
    links=$(grep -oP '\[.*?\]\(\K(\.\/)?references/[^)]+' "$skill" 2>/dev/null || true)

    for link in $links; do
        # Remove leading ./
        link="${link#./}"

        target="$skill_dir/$link"

        if [ ! -f "$target" ]; then
            echo "❌ BROKEN: $skill -> $link"
            ((failures++))
        fi
    done
done

if [ $failures -eq 0 ]; then
    echo "✅ All reference links valid"
    exit 0
else
    echo "❌ $failures broken reference links found"
    exit 1
fi
```

**Usage:**
```bash
chmod +x tools/check_references.sh
./tools/check_references.sh
```

---

## Validation Phases

### Phase 1: Post-Metadata (After Week 1)

**Run:**
```bash
# Automated validation
python tools/validate_skills.py

# Manual spot checks (sample 5 skills from different domains)
# - content-creator (Marketing)
# - ceo-advisor (C-Level)
# - product-manager-toolkit (Product)
# - senior-backend (Engineering)
# - qms-audit-expert (RA/QM)
```

**Acceptance Criteria:**
- [ ] All 40 skills pass automated validation
- [ ] All 5 sample skills pass manual checklist
- [ ] Zero broken reference links
- [ ] Zero YAML syntax errors

### Phase 2: Post-Pilots (After Week 2)

**Run:**
```bash
# Validate 3 pilot skills thoroughly
python tools/validate_skills.py --skill content-creator
python tools/validate_skills.py --skill product-manager-toolkit
python tools/validate_skills.py --skill senior-fullstack

# Run Claude activation tests on pilots
# (manual testing in Claude AI)
```

**Acceptance Criteria:**
- [ ] All 3 pilots pass automated validation
- [ ] All 3 pilots pass manual checklist
- [ ] All 3 pilots pass Claude activation tests
- [ ] All 3 pilots have working reference links
- [ ] Line counts within target (100-200)

### Phase 3: Post-Rollout (After Week 3)

**Run:**
```bash
# Full validation suite
python tools/validate_skills.py --output json --file final-validation.json

# Line count check
python tools/track_skill_lines.py

# Reference link check
./tools/check_references.sh

# Claude activation testing (sample 10 skills)
```

**Acceptance Criteria:**
- [ ] All 40 skills pass automated validation
- [ ] Average line count ≤ 150
- [ ] Zero broken reference links
- [ ] 10/10 sample skills pass activation tests
- [ ] All agents still work (28/28)

### Phase 4: Final Validation (Week 4)

**Run:**
```bash
# Complete validation suite
python tools/validate_skills.py
python tools/track_skill_lines.py
./tools/check_references.sh

# Full test suite
source /tmp/test_venv/bin/activate
pytest tests/ -v

# Agent testing (sample 5 agents)
# - cs-content-creator
# - cs-product-manager
# - cs-fullstack-engineer
# - cs-ceo-advisor
# - cs-senior-pm
```

**Acceptance Criteria:**
- [ ] 100% skills pass validation
- [ ] Average line count target met (≤150)
- [ ] Zero broken links
- [ ] All pytest tests pass (2,814 tests)
- [ ] All 5 sample agents work correctly
- [ ] Documentation updated and accurate

---

## Anthropic Standards Checklist

Use this checklist for each refactored skill:

### ✅ Core Standards

| Check | Standard | Pass | Notes |
|-------|----------|------|-------|
| [ ] | Focused scope (one capability) | | |
| [ ] | SKILL.md 100-200 lines | | Actual: ___ lines |
| [ ] | Progressive disclosure implemented | | |
| [ ] | Rich description with triggers | | |
| [ ] | Proper metadata (license, version) | | |
| [ ] | Keywords section (10-20 terms) | | |
| [ ] | Tool restrictions if needed | | |

### ✅ Metadata Completeness

| Field | Required | Present | Value |
|-------|----------|---------|-------|
| name | Yes | [ ] | |
| description | Yes | [ ] | |
| license | Yes | [ ] | |
| metadata.version | Yes | [ ] | |
| metadata.author | Yes | [ ] | |
| metadata.category | Yes | [ ] | |
| metadata.domain | Yes | [ ] | |
| metadata.updated | Yes | [ ] | |
| allowed-tools | Conditional | [ ] | |

### ✅ Content Quality

| Section | Present | Quality | Notes |
|---------|---------|---------|-------|
| Keywords | [ ] | [ ] | 10-20 terms |
| Quick Start | [ ] | [ ] | 2-3 examples |
| Core Workflows | [ ] | [ ] | High-level |
| Scripts | [ ] | [ ] | Clear usage |
| References | [ ] | [ ] | Valid links |
| Best Practices | [ ] | [ ] | Top 5 |
| Examples | [ ] | [ ] | 2 concrete |

---

## Success Metrics

### Validation Success Rate

**Target:** 100% of skills pass all validation checks

**Measurement:**
```bash
python tools/validate_skills.py | grep "Success Rate"
# Target output: Success Rate: 100.0%
```

### Line Count Compliance

**Target:** Average ≤ 150 lines, all skills ≤ 250 lines

**Measurement:**
```bash
python tools/track_skill_lines.py | grep "Average"
# Target output: Average: 150 lines per skill
```

### Activation Success

**Target:** 100% of sampled skills activate correctly in Claude

**Measurement:** Manual testing of 10 random skills with Claude AI

### Zero Breakage

**Target:** All agents and scripts work unchanged

**Measurement:**
```bash
# All pytest tests pass
pytest tests/

# All reference links valid
./tools/check_references.sh

# All agents tested (sample 5)
```

---

## Continuous Validation

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Validate changed SKILL.md files before commit

changed_skills=$(git diff --cached --name-only | grep "SKILL.md$")

if [ -z "$changed_skills" ]; then
    exit 0
fi

echo "Validating changed skills..."

for skill in $changed_skills; do
    python tools/validate_skills.py --skill $(basename $(dirname "$skill"))
    if [ $? -ne 0 ]; then
        echo "❌ Validation failed for $skill"
        echo "Fix issues before committing"
        exit 1
    fi
done

echo "✅ All changed skills valid"
exit 0
```

### CI/CD Integration

```yaml
# .github/workflows/validate-skills.yml
name: Validate Skills

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install pyyaml

      - name: Validate all skills
        run: python tools/validate_skills.py

      - name: Check reference links
        run: ./tools/check_references.sh

      - name: Track line counts
        run: python tools/track_skill_lines.py
```

---

## Summary

**We confirm refactored skills meet Anthropic standards through:**

1. ✅ **Automated validation** (structural checks, required fields)
2. ✅ **Manual checklists** (compliance with official standards)
3. ✅ **Claude activation testing** (real-world usage validation)
4. ✅ **Functional testing** (scripts work, links valid)
5. ✅ **Continuous monitoring** (pre-commit hooks, CI/CD)

**Validation occurs at each phase:**
- Phase 1: Metadata completeness
- Phase 2: Pilot skill quality
- Phase 3: Full rollout compliance
- Phase 4: Final comprehensive validation

**Tools provided:**
- `tools/validate_skills.py` - Automated structural validation
- `tools/track_skill_lines.py` - Line count monitoring
- `tools/check_references.sh` - Link integrity checking
- Manual checklists for Anthropic standards compliance
- Claude activation testing protocol

**Result:** 100% confidence that refactored skills meet Anthropic's official Agent Skills standards.
