# Contract: YAML Frontmatter Validation

**Date**: November 12, 2025
**Purpose**: Define validation rules for agent YAML frontmatter

## Contract Overview

Every agent file MUST begin with valid YAML frontmatter containing exactly 6 required fields.

## Required Schema

```yaml
---
name: string
description: string
skills: string
domain: enum
model: enum
tools: array
---
```

## Field Specifications

### 1. name (REQUIRED)

**Type:** `string`
**Format:** `cs-{agent-name}`
**Case:** kebab-case (lowercase with hyphens)

**Rules:**
- MUST start with `cs-` prefix
- MUST use kebab-case (lowercase, hyphens only)
- MUST NOT contain underscores, spaces, or uppercase letters
- MUST match filename (without .md extension)

**Valid Examples:**
```yaml
name: cs-content-creator
name: cs-backend-engineer
name: cs-jira-expert
name: cs-cto-advisor
```

**Invalid Examples:**
```yaml
name: content-creator          # ❌ Missing cs- prefix
name: cs_backend_engineer      # ❌ Uses underscores
name: cs-Backend-Engineer      # ❌ Uses uppercase
name: cs backend engineer      # ❌ Contains spaces
```

### 2. description (REQUIRED)

**Type:** `string`
**Length:** Under 150 characters (strict limit)
**Style:** Active voice, outcome-focused

**Rules:**
- MUST be under 150 characters
- MUST be a single sentence
- SHOULD focus on outcomes, not just features
- MUST be specific (not generic)

**Valid Examples:**
```yaml
description: AI-powered content creation specialist for brand voice consistency, SEO optimization, and multi-platform content strategy

description: Backend development specialist for API design, database optimization, and system architecture

description: Security operations engineer for vulnerability management, threat detection, and incident response
```

**Invalid Examples:**
```yaml
description: Helps with content       # ❌ Too vague, too short
description: This agent is designed to help teams create content for marketing purposes and also optimize SEO and maintain brand voice consistency across all platforms and channels including social media and blogs. It provides comprehensive analysis.  # ❌ Too long (>150 chars)
```

### 3. skills (REQUIRED)

**Type:** `string`
**Format:** Exact skill folder name (NOT full path)

**Rules:**
- MUST match skill folder name exactly
- MUST NOT include path components (no `skills/`, no `domain-team/`)
- MUST correspond to existing skill directory

**Valid Examples:**
```yaml
skills: content-creator            # For skills/marketing-team/content-creator/
skills: senior-backend             # For skills/engineering-team/senior-backend/
skills: jira-expert                # For skills/delivery-team/jira-expert/
```

**Invalid Examples:**
```yaml
skills: skills/marketing-team/content-creator   # ❌ Includes path
skills: marketing-team/content-creator          # ❌ Includes domain
skills: ../../skills/marketing-team/content-creator  # ❌ Relative path
```

**Validation Test:**
```bash
# From repo root, verify skill exists:
ls skills/*/[skills-value]/
# Should list: SKILL.md, scripts/, references/, assets/
```

### 4. domain (REQUIRED)

**Type:** `enum`
**Valid Values:** `marketing`, `product`, `engineering`, `delivery`

**Rules:**
- MUST be one of the 4 valid values
- MUST be lowercase
- MUST match the domain where skill is located

**Domain Mapping Table:**

| Skill Location | domain Value |
|----------------|--------------|
| `skills/marketing-team/` | `marketing` |
| `skills/product-team/` | `product` |
| `skills/engineering-team/` | `engineering` |
| `skills/delivery-team/` | `delivery` |

**Valid Examples:**
```yaml
domain: marketing     # For skills in skills/marketing-team/
domain: engineering   # For skills in skills/engineering-team/
domain: delivery      # For skills in skills/delivery-team/
```

**Invalid Examples:**
```yaml
domain: Marketing     # ❌ Uppercase
domain: eng          # ❌ Abbreviation not allowed
domain: pm           # ❌ Invalid value
domain: c-level      # ❌ No longer supported (moved to engineering)
```

### 5. model (REQUIRED)

**Type:** `enum`
**Valid Values:** `sonnet`, `opus`, `haiku`
**Standard:** `sonnet` (for all production agents)

**Rules:**
- MUST be one of the 3 valid values
- MUST be lowercase
- SHOULD be `sonnet` for production agents (100% consistency observed)

**Valid Examples:**
```yaml
model: sonnet    # ✅ Standard for production agents
model: opus      # ⚠️  Only for extremely complex reasoning
model: haiku     # ⚠️  Only for simple, fast tasks
```

**Invalid Examples:**
```yaml
model: claude-sonnet-3-5  # ❌ Use short form only
model: Sonnet             # ❌ Uppercase not allowed
model: gpt-4             # ❌ Invalid model
```

**When to Deviate from Sonnet:**
- Use `opus`: Complex multi-step reasoning, strategic planning
- Use `haiku`: Simple lookups, quick responses, low latency needs
- **Default**: Always use `sonnet` unless specific need identified

### 6. tools (REQUIRED)

**Type:** `array`
**Standard Value:** `[Read, Write, Bash, Grep, Glob]`

**Rules:**
- MUST be a YAML array
- SHOULD use the standard tool set (100% consistency in existing agents)
- MUST use proper array syntax

**Valid Examples:**
```yaml
tools: [Read, Write, Bash, Grep, Glob]     # ✅ Standard set (recommended)
tools: [Read, Bash]                         # ✅ Valid but non-standard
tools:                                      # ✅ Multi-line format
  - Read
  - Write
  - Bash
  - Grep
  - Glob
```

**Invalid Examples:**
```yaml
tools: Read, Write, Bash      # ❌ Not an array (missing brackets)
tools: ["Read", "Write"]      # ⚠️  Quotes not needed but valid
tools: []                     # ❌ Empty array not useful
```

## Complete Valid Example

```yaml
---
name: cs-backend-engineer
description: Backend development specialist for API design, database optimization, and system architecture
skills: senior-backend
domain: engineering
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---
```

## Validation Procedure

### Automated Validation

```bash
# 1. Extract YAML frontmatter
sed -n '/^---$/,/^---$/p' agents/domain/cs-agent.md | head -n -1 | tail -n +2 > /tmp/frontmatter.yaml

# 2. Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('/tmp/frontmatter.yaml'))"

# 3. Check required fields
python3 << 'EOF'
import yaml
with open('/tmp/frontmatter.yaml') as f:
    data = yaml.safe_load(f)
    required = ['name', 'description', 'skills', 'domain', 'model', 'tools']
    missing = [field for field in required if field not in data]
    if missing:
        print(f"❌ Missing fields: {missing}")
        exit(1)
    else:
        print("✅ All required fields present")
EOF
```

### Manual Validation Checklist

Use this checklist for each agent:

- [ ] **name** field present
- [ ] **name** starts with `cs-`
- [ ] **name** uses kebab-case
- [ ] **name** matches filename
- [ ] **description** field present
- [ ] **description** under 150 characters
- [ ] **description** is outcome-focused
- [ ] **skills** field present
- [ ] **skills** is folder name only (no path)
- [ ] **skills** folder exists in `skills/*/`
- [ ] **domain** field present
- [ ] **domain** is one of: marketing, product, engineering, delivery
- [ ] **domain** matches skill location
- [ ] **model** field present
- [ ] **model** is one of: sonnet, opus, haiku
- [ ] **model** is `sonnet` (unless justified deviation)
- [ ] **tools** field present
- [ ] **tools** is a YAML array
- [ ] **tools** uses standard set (recommended)
- [ ] YAML syntax valid (no parsing errors)

## Common Violations and Fixes

### Violation 1: Wrong skills Path

```yaml
# ❌ WRONG
skills: skills/engineering-team/senior-backend

# ✅ CORRECT
skills: senior-backend
```

### Violation 2: Missing cs- Prefix

```yaml
# ❌ WRONG
name: backend-engineer

# ✅ CORRECT
name: cs-backend-engineer
```

### Violation 3: Description Too Long

```yaml
# ❌ WRONG (172 characters)
description: This is a comprehensive backend development agent that helps teams build scalable APIs, optimize database queries, implement microservices, and maintain high-quality code

# ✅ CORRECT (145 characters)
description: Backend development specialist for API design, database optimization, microservices architecture, and code quality maintenance
```

### Violation 4: Invalid Domain

```yaml
# ❌ WRONG
domain: project-management

# ✅ CORRECT (project-management skills moved to delivery-team)
domain: delivery
```

### Violation 5: Inconsistent Model

```yaml
# ⚠️  NOT RECOMMENDED (all existing agents use sonnet)
model: opus

# ✅ RECOMMENDED (consistent with 100% of existing agents)
model: sonnet
```

## Python Validation Script

```python
#!/usr/bin/env python3
"""
Validate agent YAML frontmatter against contract
"""
import yaml
import sys
from pathlib import Path

def validate_frontmatter(agent_file):
    """Validate agent YAML frontmatter"""
    content = Path(agent_file).read_text()

    # Extract YAML frontmatter
    if not content.startswith('---\n'):
        return False, "Missing YAML frontmatter"

    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return False, "Invalid YAML frontmatter structure"

    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return False, f"YAML parsing error: {e}"

    # Check required fields
    required = ['name', 'description', 'skills', 'domain', 'model', 'tools']
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing required fields: {missing}"

    # Validate name
    if not data['name'].startswith('cs-'):
        return False, f"name must start with 'cs-': {data['name']}"

    # Validate description length
    if len(data['description']) > 150:
        return False, f"description too long: {len(data['description'])} chars (max 150)"

    # Validate domain
    valid_domains = ['marketing', 'product', 'engineering', 'delivery']
    if data['domain'] not in valid_domains:
        return False, f"invalid domain: {data['domain']} (must be one of {valid_domains})"

    # Validate model
    valid_models = ['sonnet', 'opus', 'haiku']
    if data['model'] not in valid_models:
        return False, f"invalid model: {data['model']} (must be one of {valid_models})"

    # Validate tools
    if not isinstance(data['tools'], list):
        return False, f"tools must be an array"

    return True, "Valid"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: validate_frontmatter.py <agent-file.md>")
        sys.exit(1)

    valid, message = validate_frontmatter(sys.argv[1])
    print(f"{'✅' if valid else '❌'} {message}")
    sys.exit(0 if valid else 1)
```

**Usage:**
```bash
python validate_frontmatter.py agents/engineering/cs-backend-engineer.md
```

---

**Last Updated:** November 12, 2025
**Contract Status:** Mandatory for all agents
**Validation:** Must pass before agent is marked production-ready
