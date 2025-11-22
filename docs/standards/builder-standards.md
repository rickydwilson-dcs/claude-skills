# Builder Standards

**Version**: 1.0.0
**Last Updated**: November 22, 2025
**Status**: Production

This document defines validation standards and quality criteria for agent and skill builders in the Claude Skills repository.

---

## Table of Contents

1. [Overview](#overview)
2. [Agent Validation Standards](#agent-validation-standards)
3. [Skill Validation Standards](#skill-validation-standards)
4. [Builder Architecture Standards](#builder-architecture-standards)
5. [Testing Standards](#testing-standards)
6. [Performance Standards](#performance-standards)

---

## Overview

### Purpose

The builder tools enforce consistent quality standards across all agents and skills, ensuring:
- **Structural Integrity**: All required sections and files present
- **Path Correctness**: Relative paths resolve correctly
- **Content Completeness**: Workflows, examples, and metrics documented
- **Maintainability**: Consistent format enables automated tooling

### Zero-Dependency Requirement

All builders **MUST**:
- Use Python 3.8+ standard library only
- Implement custom parsers (no PyYAML, lxml, etc.)
- Work in air-gapped environments
- Have no external API dependencies

**Rationale**: Maximum portability and security for enterprise use

---

## Agent Validation Standards

### 1. Name Format Validation

**Standard**: Agent names **MUST** follow the `cs-*` prefix convention

**Valid Examples**:
```
cs-content-creator
cs-product-manager
cs-backend-engineer
```

**Invalid Examples**:
```
❌ content-creator (missing cs- prefix)
❌ cs_product_manager (underscore instead of hyphen)
❌ CS-Content-Creator (uppercase letters)
```

**Implementation**: `^cs-[a-z][a-z0-9-]*$` regex pattern

---

### 2. YAML Frontmatter Validation

**Standard**: All agents **MUST** include valid YAML frontmatter with required fields

**Required Fields**:
```yaml
---
name: cs-agent-name              # Must match filename
description: Brief description   # Max 150 characters
skills: skill-package-name       # Skill directory reference
domain: domain-name              # marketing, product, engineering, delivery
model: sonnet                    # sonnet, opus, or haiku
tools: [Read, Write, Bash]       # Array of Claude Code tools
---
```

**Validation Checks**:
- ✓ Frontmatter enclosed in `---` delimiters
- ✓ All required fields present
- ✓ `name` matches filename (cs-content-creator.md → name: cs-content-creator)
- ✓ `description` ≤ 150 characters
- ✓ `domain` is valid (existing or new)
- ✓ `model` is one of: sonnet, opus, haiku
- ✓ `tools` is valid array format

**Error Examples**:
```yaml
# ❌ Missing name field
---
description: Agent description
skills: skill-name
domain: marketing
---

# ❌ Description too long (160 chars)
---
name: cs-agent
description: This is a very long description that exceeds the maximum allowed character limit and will fail validation because it is longer than one hundred fifty characters
skills: skill-name
---

# ❌ Invalid tools format
---
name: cs-agent
tools: Read, Write, Bash  # Should be [Read, Write, Bash]
---
```

---

### 3. Relative Path Validation

**Standard**: All skill references **MUST** use correct relative paths from agent location

**Path Pattern**: `../../skills/team-name/skill-name/`

**Valid Examples**:
```markdown
**Skill Location:** `../../skills/marketing-team/content-creator/`

**Python Tool:**
`../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py`

**Reference:**
`../../skills/marketing-team/content-creator/references/brand_guidelines.md`
```

**Invalid Examples**:
```markdown
❌ /skills/marketing-team/content-creator/  (absolute path)
❌ ../skills/marketing-team/content-creator/ (incorrect depth)
❌ marketing-skill/content-creator/          (old naming convention)
```

**Validation Process**:
1. Extract all paths matching `../../skills/` pattern
2. Resolve paths relative to agent file location
3. Verify files/directories exist on filesystem
4. Report missing files as validation errors

---

### 4. Workflow Validation

**Standard**: Agents **MUST** document at least 4 workflows

**Required Structure**:
```markdown
## Workflows

### Workflow 1: [Clear Descriptive Name]

**Goal:** One-sentence description

**Steps:**
1. Step 1 with specific actions
2. Step 2 with specific actions
3. Step 3 with specific actions

**Expected Output:** Success criteria

**Time Estimate:** Duration

**Example:**
\`\`\`bash
# Concrete command example
\`\`\`
```

**Validation Checks**:
- ✓ At least 4 `### Workflow N:` headers found
- ✓ Each workflow has **Goal**, **Steps**, **Expected Output**
- ✓ Workflows numbered sequentially (1, 2, 3, 4...)

---

### 5. Integration Examples Validation

**Standard**: Agents **MUST** include at least 2 integration examples

**Required Pattern**: `### Example N:` headers within `## Integration Examples` section

**Valid Format**:
```markdown
## Integration Examples

### Example 1: Daily Automation Script

\`\`\`bash
#!/bin/bash
# automation.sh
python ../../skills/domain/skill/scripts/tool.py input.txt
\`\`\`

### Example 2: CI/CD Integration

\`\`\`bash
# .github/workflows/ci.yml
python ../../skills/domain/skill/scripts/tool.py --json
\`\`\`
```

**Validation Checks**:
- ✓ `## Integration Examples` section exists
- ✓ At least 2 `### Example N:` headers found
- ✓ Examples show concrete code (bash, python, yaml, etc.)

**Common Issue**: H2 headers (`##`) inside bash heredocs terminate section parsing

**Solution**: Use H3 headers (`###`) inside code blocks:
```bash
cat > report.md << EOF
### Report Summary  # ✓ H3 won't terminate Integration Examples section
## Key Findings      # ❌ H2 will terminate section (use ### instead)
EOF
```

---

### 6. Success Metrics Validation

**Standard**: Agents **MUST** document at least 3 metric categories

**Required Format**: Bold text with colon (`**Category:**`)

**Valid Examples**:
```markdown
## Success Metrics

**Test Coverage:**
- Line Coverage: 80%+ across codebase
- Branch Coverage: 75%+ for decision logic

**Quality Assurance:**
- Test Automation Rate: 90%+ automated
- Defect Escape Rate: < 5% bugs reach production

**Development Efficiency:**
- Time to Quality Gate: < 5 minutes
- PR Review Time: 30-40% reduction
```

**Validation Pattern**: `^**[^*]+:**$` (line starting with `**`, ending with `:**`)

**Validation Checks**:
- ✓ `## Success Metrics` section exists
- ✓ At least 3 lines match `**Category:**` pattern
- ✓ Each category has bullet points with metrics

**Alternative Format** (also valid):
```markdown
## Success Metrics

### Test Coverage Metrics
- Metric 1
- Metric 2

### Quality Metrics
- Metric 3
- Metric 4
```
*Note: H3 headers count as metric categories*

---

### 7. Markdown Structure Validation

**Standard**: Agents **MUST** include core sections

**Required Sections**:
- `# Agent Name` (H1 title)
- `## Purpose`
- `## Skill Integration`
- `## Workflows`
- `## Integration Examples`
- `## Success Metrics`
- `## Related Agents` OR `## References`

**Optional Sections**:
- `## Integration with Other Skills`
- `## Additional Resources`
- `## Known Limitations`

**Validation**: Check for presence of each required H2 section

---

### 8. Cross-Reference Validation

**Standard**: Agents **MUST** include either "Related Agents" or "References" section

**Valid Formats**:
```markdown
## Related Agents

- [cs-frontend-engineer](cs-frontend-engineer.md) - Frontend development
- [cs-devops-engineer](cs-devops-engineer.md) - Deployment automation

## References

- **Skill Documentation:** [../../skills/domain/skill/SKILL.md](...)
- **Domain Guide:** [../../skills/domain/CLAUDE.md](...)
```

**Validation**: At least one section must be present

---

## Skill Validation Standards

### 1. Directory Structure Validation

**Standard**: Skills **MUST** follow the canonical structure

**Required Directories**:
```
skill-name/
├── SKILL.md          # REQUIRED: Master documentation
├── scripts/          # REQUIRED: Python tools (even if empty with .gitkeep)
├── references/       # REQUIRED: Knowledge bases (even if empty with .gitkeep)
└── assets/           # REQUIRED: Templates (even if empty with .gitkeep)
```

**Validation Checks**:
- ✓ SKILL.md exists
- ✓ scripts/ directory exists
- ✓ references/ directory exists
- ✓ assets/ directory exists

---

### 2. SKILL.md Metadata Validation

**Standard**: SKILL.md **MUST** include extended metadata YAML

**Required Fields**:
```yaml
---
name: Skill Name
description: Brief description
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: domain
  domain: skill-domain
  updated: YYYY-MM-DD
  keywords:
    - keyword1
    - keyword2
  tech-stack:
    - Python 3.8+
  python-tools:
    - tool1.py
    - tool2.py
---
```

**Validation Checks**:
- ✓ Basic fields: name, description, license
- ✓ Extended metadata section present
- ✓ Version follows semver (X.Y.Z)
- ✓ Updated date in ISO format (YYYY-MM-DD)
- ✓ Keywords is array with 3+ items
- ✓ Tech-stack is array with 1+ items

---

### 3. Required Sections Validation

**Standard**: SKILL.md **MUST** include core sections

**Required Sections**:
- `# Skill Name` (H1 title)
- `## Overview`
- `## Core Capabilities`
- `## Key Workflows`

**Validation Pattern**:
```markdown
## Overview

[2-3 sentence overview]

**Core Value:** [Value proposition]

**Target Audience:** [Who this is for]

**Use Cases:** [3-5 primary use cases]

## Core Capabilities

- **Capability 1** - Description
- **Capability 2** - Description
- **Capability 3** - Description

## Key Workflows

### Workflow 1: [Name]
[Details]

### Workflow 2: [Name]
[Details]
```

---

### 4. Python Tool Validation

**Standard**: All Python scripts in `scripts/` **MUST** be executable

**Validation**:
```bash
# Check executable permission
for tool in scripts/*.py; do
    [ -x "$tool" ] && echo "✓ $tool" || echo "❌ $tool not executable"
done
```

**Automated Fix**:
```bash
chmod +x scripts/*.py
```

**Standard Interface** (recommended, not enforced):
- Support `--help` flag
- Accept `--output json` for machine-readable format
- Use standard exit codes (0 = success, 1 = error)
- Handle UTF-8 encoding

---

## Builder Architecture Standards

### 1. Zero-Dependency Requirement

**Standard**: Builders **MUST NOT** import external packages

**Allowed Imports** (Python 3.8+ standard library):
```python
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
```

**Forbidden Imports**:
```python
import yaml        # ❌ Use custom parser
import requests    # ❌ No network calls
import lxml        # ❌ Use standard library
```

### 2. Custom YAML Parser

**Standard**: Builders **MUST** implement custom YAML parsing

**Example Implementation**:
```python
def simple_yaml_parse(yaml_content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter without external dependencies"""
    result = {}
    lines = yaml_content.strip().split('\n')
    current_key = None
    current_list = None

    for line in lines:
        if ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if value:
                result[key] = value
            else:
                current_key = key
                current_list = []
                result[key] = current_list
        elif line.strip().startswith('-') and current_list is not None:
            value = line.strip()[1:].strip()
            current_list.append(value)

    return result
```

**Features**:
- Parse key-value pairs
- Parse arrays (lines starting with `-`)
- Handle nested structures (basic)
- No external dependencies

### 3. Dynamic Discovery

**Standard**: Builders **MUST** discover domains/teams dynamically

**Anti-Pattern** (hardcoded lists):
```python
VALID_DOMAINS = ['marketing', 'product', 'engineering', 'delivery']  # ❌
```

**Correct Pattern** (filesystem discovery):
```python
def get_existing_domains() -> List[str]:
    """Discover domains from filesystem"""
    agents_dir = Path("agents")
    return [d.name for d in agents_dir.iterdir() if d.is_dir()]
```

**Benefits**:
- Users can create custom domains
- No code changes needed for new domains
- Scales automatically

### 4. Validation-First Design

**Standard**: Builders **MUST** validate before generating

**Workflow**:
1. **Pre-Generation Validation**: Check inputs (name format, domain validity, etc.)
2. **Generation**: Create files if validation passes
3. **Post-Generation Validation**: Verify output meets standards

**Example**:
```python
def generate_agent(self, config: Dict) -> None:
    # 1. Pre-validate
    if not self.validator.validate_name(config['name'])[0]:
        raise ValueError("Invalid agent name")

    # 2. Generate
    agent_path = self.create_agent_file(config)

    # 3. Post-validate
    result = self.validator.validate_agent_file(agent_path)
    if not result.is_valid:
        print(f"⚠️  Generated agent has validation issues")
```

---

## Testing Standards

### Manual Testing Checklist

Before committing builder changes, test:

```bash
# 1. Validate all existing agents
for agent in agents/**/cs-*.md; do
    python3 scripts/agent_builder.py --validate "$agent" || echo "FAIL: $agent"
done

# 2. Validate all existing skills
for skill in skills/*/*/SKILL.md; do
    skill_dir=$(dirname "$skill")
    python3 scripts/skill_builder.py --validate "$skill_dir" || echo "FAIL: $skill_dir"
done

# 3. Test agent generation
python3 scripts/agent_builder.py --config examples/agent-config-example.yaml

# 4. Test skill generation
python3 scripts/skill_builder.py  # Run interactive mode, test all inputs
```

### Validation Success Criteria

**Agents**: 28/28 passing (100%)
**Skills**: 28/28 passing (100%)
**Generation Time**: < 5 seconds per agent/skill
**Validation Time**: < 2 seconds per agent/skill

---

## Performance Standards

### Speed Requirements

**Agent Generation**: < 5 seconds
**Skill Generation**: < 10 seconds (includes directory scaffolding)
**Agent Validation**: < 2 seconds
**Skill Validation**: < 3 seconds
**Batch Validation (28 agents)**: < 60 seconds

### Memory Requirements

**Maximum Memory Usage**: < 50MB per builder
**Rationale**: Builders run in constrained CI/CD environments

### File Size Limits

**Generated Agent**: 300-1,500 lines (typical)
**Generated Skill SKILL.md**: 500-2,000 lines (typical)
**Validation Error Output**: < 1,000 lines (keep error messages concise)

---

## Version History

**v1.0.0** (November 22, 2025)
- Initial builder standards documentation
- Agent validation: 9 checks (YAML, paths, workflows, examples, metrics, structure, cross-refs)
- Skill validation: 9 checks (structure, metadata, sections, tools, references)
- Zero-dependency requirement formalized
- Performance benchmarks established

---

## References

- [Agent Builder](../../scripts/agent_builder.py) - Implementation
- [Skill Builder](../../scripts/skill_builder.py) - Implementation
- [Agent Development Guide](../agents/CLAUDE.md) - Agent standards
- [CLAUDE.md](../../CLAUDE.md) - Builder usage guide

---

**Maintained By**: Claude Skills Team
**Review Cadence**: Quarterly
**Next Review**: February 2026
