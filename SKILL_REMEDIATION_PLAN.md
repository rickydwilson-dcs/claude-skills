# Skill Remediation Plan - Enhanced Standards v1.1.0

**Generated**: November 23, 2025
**Status**: Planning
**Target Completion**: TBD

---

## Executive Summary

**Current State**: 0/28 skills (0%) passing all validation checks
**Average Score**: 69.3% (6.9/10 checks passing)
**Target State**: 28/28 skills (100%) passing all validation checks

### Critical Issues

1. **metadata_completeness**: 28 skills (100%) - Missing `metadata` section in YAML frontmatter
2. **file_cleanliness**: 22 skills (78.6%) - Python cache files (__pycache__/, *.pyc)
3. **skill_md_completeness**: 18 skills (64.3%) - Missing required sections
4. **reference_guides**: 7 skills (25%) - Empty or insufficient reference documentation
5. **python_tools**: 6 skills (21.4%) - No tools or non-executable tools
6. **documentation_quality**: 5 skills (17.9%) - < 1 workflow documented

---

## Issue 1: Metadata Completeness (28 skills - 100%)

### Problem
All skills have YAML frontmatter but are missing the nested `metadata` section required by v1.1.0 standards.

### Current Format
```yaml
---
name: skill-name
description: Description text
license: MIT
---
```

### Required Format
```yaml
---
name: skill-name              # MUST be kebab-case
description: Description text
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: domain
  domain: skill-domain
  updated: 2025-11-23
  keywords:
    - keyword1
    - keyword2
    - keyword3
  tech-stack:
    - Python 3.8+
  python-tools:
    - tool1.py
    - tool2.py
---
```

### Remediation Steps

**Automated Fix (Recommended)**:
```python
# Create script: scripts/fix_metadata.py
#!/usr/bin/env python3
"""
Add missing metadata section to all SKILL.md files
"""

import re
from pathlib import Path
from datetime import datetime

def fix_metadata(skill_md_path):
    """Add metadata section to YAML frontmatter"""
    content = skill_md_path.read_text()

    # Extract existing frontmatter
    if not content.startswith('---'):
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    yaml_content = parts[1]
    body_content = parts[2]

    # Parse existing fields
    name_match = re.search(r'name: (.+)', yaml_content)
    desc_match = re.search(r'description: (.+)', yaml_content)

    if not name_match:
        return False

    name = name_match.group(1).strip()
    description = desc_match.group(1).strip() if desc_match else ""

    # Determine domain from path
    team_dir = skill_md_path.parent.parent.name
    domain = team_dir.replace('-team', '')

    # Build new frontmatter with metadata
    new_yaml = f"""---
name: {name}
description: {description}
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: {domain}
  domain: {domain}
  updated: {datetime.now().strftime('%Y-%m-%d')}
  keywords:
    - (to be added)
  tech-stack:
    - Python 3.8+
  python-tools:
    - (to be added)
---"""

    new_content = new_yaml + body_content
    skill_md_path.write_text(new_content)
    return True

# Run on all skills
for skill_md in Path('skills').rglob('SKILL.md'):
    if fix_metadata(skill_md):
        print(f"✓ Fixed: {skill_md}")
    else:
        print(f"✗ Failed: {skill_md}")
```

**Manual Fix (Per Skill)**:
1. Open `skills/domain/skill-name/SKILL.md`
2. Locate YAML frontmatter (between `---` markers)
3. Add `metadata:` section after `license: MIT`
4. Fill in appropriate values for version, category, keywords, tech-stack, python-tools
5. Validate: `python3 scripts/skill_builder.py --validate skills/domain/skill-name/`

**Time Estimate**:
- Automated: 30 minutes (script development) + 5 minutes (execution)
- Manual: 15 minutes per skill × 28 = 7 hours

**Priority**: **CRITICAL** - Blocking 100% of skills

---

## Issue 2: File Cleanliness (22 skills - 78.6%)

### Problem
Python cache directories and compiled bytecode files present in skill directories.

### Artifacts Found
- `__pycache__/` directories
- `*.pyc` files (Python 3 bytecode)
- `*.pyo` files (optimized bytecode)

### Remediation Steps

**Automated Fix (Recommended)**:
```bash
#!/bin/bash
# Clean all Python cache files from skills/

find skills/ -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find skills/ -type f -name "*.pyc" -delete
find skills/ -type f -name "*.pyo" -delete

echo "✓ Cleaned all Python cache files"

# Verify
python3 scripts/skill_builder.py --validate skills/domain/skill-name/ --validate-cleanup
```

**Add .gitignore**:
```bash
# Add to skills/.gitignore or root .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "*.pyo" >> .gitignore
echo ".DS_Store" >> .gitignore
```

**Prevention**:
- Run `find skills/ -name "__pycache__" -exec rm -rf {} +` before commits
- Add pre-commit hook to prevent cache commits
- Configure IDE to exclude __pycache__/ from git

**Time Estimate**: 5 minutes (one-time cleanup)

**Priority**: **HIGH** - Quick fix, improves professionalism

---

## Issue 3: Skill.md Completeness (18 skills - 64.3%)

### Problem
Missing required sections in SKILL.md files.

### Required Sections
- `## Overview`
- `## Core Capabilities`
- `## Quick Start`
- `## Key Workflows`
- `## Python Tools`

### Affected Skills (18 total)

**Delivery Team (4 skills)**:
- confluence-expert
- jira-expert
- scrum-master
- senior-pm

**Engineering Team (12 skills)**:
- code-reviewer
- cto-advisor
- senior-architect
- senior-computer-vision
- senior-data-scientist
- senior-devops
- senior-fullstack
- senior-ml-engineer
- senior-prompt-engineer
- senior-qa
- senior-secops
- senior-security

**Marketing Team (1 skill)**:
- marketing-strategy-pmm

**Product Team (1 skill)**:
- business-analyst-toolkit

### Remediation Steps

**Per Skill**:
1. Open `skills/domain/skill-name/SKILL.md`
2. Check for missing sections using: `grep "^## " SKILL.md`
3. Add missing sections using [templates/skill-template.md](templates/skill-template.md) as reference
4. Ensure each section has meaningful content (not just placeholders)
5. Validate: `python3 scripts/skill_builder.py --validate skills/domain/skill-name/`

**Template Reference**:
```markdown
## Overview

[2-3 paragraphs describing what this skill provides, who it's for, and core value]

**Core Value:** [Quantified benefit - time savings, quality improvements]

## Core Capabilities

- **Capability 1** - Description
- **Capability 2** - Description
- **Capability 3** - Description
- **Capability 4** - Description

## Quick Start

### [Primary Use Case]
```bash
python scripts/tool_name.py input.txt
```

## Key Workflows

### 1. [Workflow Name]

**Time:** [Duration]

1. **[Step]** - Description
2. **[Step]** - Description
3. **[Step]** - Description

### 2. [Second Workflow]
...
```

**Time Estimate**: 45-60 minutes per skill × 18 = 13.5-18 hours

**Priority**: **HIGH** - Essential for usability

---

## Issue 4: Reference Guides (7 skills - 25%)

### Problem
Empty reference directories or insufficient reference documentation.

### Affected Skills (7 total)
- marketing-team/marketing-demand-acquisition
- marketing-team/marketing-strategy-pmm
- engineering-team/senior-secops
- product-team/agile-product-owner
- product-team/product-strategist
- product-team/ui-design-system
- product-team/ux-researcher-designer

### Standard
- Minimum 100 characters per .md file in references/
- At least 1-2 meaningful reference guides
- Reference guides should contain frameworks, best practices, or domain knowledge

### Remediation Steps

**Per Skill**:
1. Identify what reference content is needed (frameworks, methodologies, best practices)
2. Create 2-3 reference guides in `references/` directory
3. Each guide should be 200+ lines with structured content
4. Link to references from SKILL.md

**Example Structure**:
```markdown
# [Topic] Reference Guide

## Overview

[Introduction to the topic]

## Key Concepts

### Concept 1
[Detailed explanation]

### Concept 2
[Detailed explanation]

## Frameworks

### Framework 1: [Name]
[Step-by-step framework]

### Framework 2: [Name]
[Step-by-step framework]

## Best Practices

1. **Practice 1** - Description and rationale
2. **Practice 2** - Description and rationale

## Examples

### Example 1: [Use Case]
**Scenario:** [Description]
**Approach:** [Steps]
**Outcome:** [Result]

## Resources

- [External resource 1]
- [External resource 2]
```

**Time Estimate**: 2-3 hours per skill × 7 = 14-21 hours

**Priority**: **MEDIUM** - Improves skill value but not blocking

---

## Issue 5: Python Tools (6 skills - 21.4%)

### Problem
Either no Python tools in scripts/ directory, or tools are not executable.

### Affected Skills (6 total)
- delivery-team/confluence-expert
- delivery-team/jira-expert
- delivery-team/scrum-master
- delivery-team/senior-pm
- engineering-team/senior-backend
- marketing-team/marketing-strategy-pmm

### Standard
- Minimum 1 Python tool in scripts/ directory
- All .py files must be executable (`chmod +x`)
- All tools must support `--help` flag (argparse)

### Remediation Steps

**Option 1: Add Python Tools** (if missing):
```bash
# Use skill builder placeholder generation
cd skills/domain/skill-name/scripts/

# Create tool template
cat > analyze_data.py << 'EOF'
#!/usr/bin/env python3
"""
Data Analysis Tool

Automated tool for skill-name tasks.
"""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Data analysis tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('input', help='Input file or data')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    print(f"Processing: {args.input}")
    # TODO: Add implementation

if __name__ == "__main__":
    main()
EOF

chmod +x analyze_data.py
```

**Option 2: Fix Executable Permissions** (if tools exist):
```bash
chmod +x skills/domain/skill-name/scripts/*.py
```

**Time Estimate**:
- Add tools: 2 hours per skill × 6 = 12 hours
- Fix permissions: 5 minutes

**Priority**: **HIGH** - Tools are core to skill value

---

## Issue 6: Documentation Quality (5 skills - 17.9%)

### Problem
Less than 1 workflow documented (standard requires 1+ workflows).

### Affected Skills (5 total)
- delivery-team/confluence-expert
- delivery-team/jira-expert
- delivery-team/scrum-master
- delivery-team/senior-pm
- engineering-team/cto-advisor

### Standard
- Minimum 1 documented workflow in `## Key Workflows` section
- Each workflow must have: Title, Time Estimate, Steps, Expected Output
- Pattern: `### N. [Workflow Name]` where N is sequential

### Remediation Steps

**Per Skill**:
1. Open `skills/domain/skill-name/SKILL.md`
2. Locate or create `## Key Workflows` section
3. Add at least 1 complete workflow following this template:

```markdown
## Key Workflows

### 1. [Workflow Name]

**Time:** [X hours/minutes]

1. **[Action Step]** - Description of first step
   ```bash
   # Command example
   python scripts/tool.py input.txt
   ```
2. **[Action Step]** - Description of second step
3. **[Action Step]** - Description of third step
4. **[Action Step]** - Description of final step

**Expected Output:** [What success looks like]

See [reference_guide.md](references/reference_guide.md) for detailed walkthrough.
```

**Time Estimate**: 30-45 minutes per skill × 5 = 2.5-3.75 hours

**Priority**: **MEDIUM** - Improves usability

---

## Issue 7: HOW_TO_USE.md Generation (28 skills - 100%)

### Problem
None of the existing skills have HOW_TO_USE.md files (new requirement in v1.1.0).

### Standard
All skills must include a HOW_TO_USE.md file with:
- Quick Start examples
- Example Invocations (3 examples)
- What to Provide
- What You'll Get
- Python Tools Available
- Tips for Best Results
- Related Skills

### Remediation Steps

**Automated Generation**:
```python
#!/usr/bin/env python3
"""
Generate HOW_TO_USE.md for existing skills
"""

from pathlib import Path
from datetime import datetime

def generate_how_to_use(skill_dir):
    """Generate HOW_TO_USE.md for a skill"""
    skill_name = skill_dir.name
    team_name = skill_dir.parent.name
    domain = team_name.replace('-team', '')

    # Find Python tools
    scripts_dir = skill_dir / 'scripts'
    tools = [f.name for f in scripts_dir.glob('*.py')] if scripts_dir.exists() else []

    content = f"""# How to Use the {skill_name.replace('-', ' ').title()} Skill

## Quick Start

Hey Claude—I just added the "{skill_name}" skill. Can you help me with [describe your task]?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "{skill_name}" skill. Can you [specific task]?
```

### Example 2: Advanced Usage
```
Hey Claude—I just added the "{skill_name}" skill. Can you [complex task with requirements]?
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
- **Deliverables**: Reports and actionable outputs

## Python Tools Available

This skill includes the following Python tools:

"""

    for tool in tools:
        tool_name = tool.replace('.py', '').replace('_', ' ').title()
        content += f"- **{tool}**: {tool_name} functionality\n"

    if tools:
        content += f"""
You can also run these tools directly:

```bash
python scripts/{tools[0]} --help
```
"""

    content += f"""
## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements for better results
2. **Provide Context**: Include relevant background information
3. **Iterate**: Start simple, then refine based on initial results
4. **Combine Skills**: This skill works well with other {domain} skills

## Related Skills

Consider using these skills together:

- [List related skills from the same domain]
- [Skills that complement this one]

---

**Skill**: {skill_name}
**Domain**: {team_name}
**Version**: 1.0.0
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
"""

    how_to_use_path = skill_dir / 'HOW_TO_USE.md'
    how_to_use_path.write_text(content)
    print(f"✓ Created: {how_to_use_path}")

# Run on all skills
for skill_dir in Path('skills').glob('*/*/'):
    if (skill_dir / 'scripts').exists():
        generate_how_to_use(skill_dir)
```

**Time Estimate**: 30 minutes (script development) + 5 minutes (execution)

**Priority**: **HIGH** - New standard requirement, improves UX

---

## Execution Plan

### Phase 1: Quick Wins (1-2 hours)
**Target**: Fix 22 skills to 8-9/10

1. ✅ Clean Python cache files (5 min)
   - Run: `find skills/ -type d -name "__pycache__" -exec rm -rf {} +`
   - Run: `find skills/ -type f -name "*.pyc" -delete`
   - Add to .gitignore

2. ✅ Fix executable permissions (5 min)
   - Run: `chmod +x skills/*/scripts/*.py`

3. ✅ Generate HOW_TO_USE.md files (40 min)
   - Develop generation script (30 min)
   - Execute on all skills (5 min)
   - Manual review (5 min)

**Result**: 22 skills move from ~7/10 to ~8/10

---

### Phase 2: Metadata Fix (2-3 hours)
**Target**: Fix all 28 skills to 9+/10

4. ✅ Fix metadata_completeness (2-3 hours)
   - Develop automated script (1 hour)
   - Execute on all skills (5 min)
   - Manual review and refinement (1-2 hours)
     - Fill in accurate keywords per skill
     - List actual python-tools per skill
     - Verify tech-stack is accurate

**Result**: All 28 skills at minimum 9/10

---

### Phase 3: Content Enhancement (20-30 hours)
**Target**: Fix all 28 skills to 10/10

5. 🔄 Fix skill_md_completeness (14-18 hours)
   - Prioritize high-traffic skills first
   - Use template for consistency
   - Add missing sections with meaningful content

6. 🔄 Improve documentation_quality (3-4 hours)
   - Add workflows to 5 skills
   - Each workflow: 30-45 minutes

7. 🔄 Add reference_guides (14-21 hours)
   - 7 skills need reference content
   - 2-3 hours per skill for quality content

8. 🔄 Add/fix python_tools (12 hours)
   - 6 skills need tools
   - 2 hours per skill for basic tools

**Result**: All 28 skills at 10/10

---

### Phase 4: Validation & Documentation (2-3 hours)

9. ✅ Re-run validation report
   - `python3 scripts/validate_all_skills_report.py`
   - Verify 28/28 passing

10. ✅ Update SKILLS_CATALOG.md
    - Reflect 100% validation status
    - Note v1.1.0 compliance

11. ✅ Update CLAUDE.md
    - Document enhanced standards
    - Update validation statistics

---

## Timeline & Effort

| Phase | Tasks | Effort | Who | Target Date |
|-------|-------|--------|-----|-------------|
| Phase 1 | Quick Wins | 1-2 hours | Automated | Day 1 |
| Phase 2 | Metadata Fix | 2-3 hours | Automated + Manual | Day 1-2 |
| Phase 3 | Content Enhancement | 20-30 hours | Manual | Week 1-2 |
| Phase 4 | Validation | 2-3 hours | Automated | Week 2 |
| **TOTAL** | | **25-38 hours** | | **2 weeks** |

---

## Success Criteria

- ✅ 28/28 skills passing standard validation (9/9 checks)
- ✅ 28/28 skills passing cleanup validation (10/10 checks)
- ✅ 100% average validation score
- ✅ All skills have HOW_TO_USE.md
- ✅ All skills have proper metadata YAML
- ✅ Zero Python cache artifacts
- ✅ All Python tools executable with --help support
- ✅ All skills have minimum 1 documented workflow

---

## Appendix: Validation Script

Save and run this to check progress:

```bash
#!/bin/bash
# Quick validation progress check

python3 scripts/validate_all_skills_report.py | grep -E "(Perfect|Average Score)"
```

Expected output after completion:
```
- Perfect (10/10): 28/28 skills (100.0%)
**Average Score (with cleanup): 100.0%**
```

---

**Last Updated**: November 23, 2025
**Status**: Planning Phase
**Next Action**: Begin Phase 1 (Quick Wins)
