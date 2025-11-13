# Contract: Relative Path Resolution

**Date**: November 12, 2025
**Purpose**: Define validation rules for agent relative path resolution

## Contract Overview

All agents MUST use relative paths following the `../../skills/` pattern. Absolute paths are strictly prohibited.

## Path Pattern Standard

**Pattern:** `../../skills/domain-team/skill-name/`

**Why:** Ensures portability across different machines and installations.

## Path Components

### From Agent to Skill Package

**Agent Location:** `agents/domain/cs-agent.md`
**Skill Location:** `skills/domain-team/skill-name/`

**Resolution:**
```
agents/domain/cs-agent.md
    └─→ ../../ (up two levels to repo root)
        └─→ skills/domain-team/skill-name/
```

### Domain Path Mappings

| Agent Location | Skill Path Pattern | Example |
|----------------|-------------------|---------|
| `agents/marketing/` | `../../skills/marketing-team/` | `../../skills/marketing-team/content-creator/` |
| `agents/product/` | `../../skills/product-team/` | `../../skills/product-team/product-manager/` |
| `agents/delivery/` | `../../skills/delivery-team/` | `../../skills/delivery-team/jira-expert/` |
| `agents/engineering/` | `../../skills/engineering-team/` | `../../skills/engineering-team/senior-backend/` |

## Required Path Documentation Sections

###1. Skill Location (REQUIRED)

**Format:**
```markdown
## Skill Integration

**Skill Location:** `../../skills/domain-team/skill-name/`
```

**Examples:**
```markdown
**Skill Location:** `../../skills/marketing-team/content-creator/`
**Skill Location:** `../../skills/engineering-team/senior-backend/`
**Skill Location:** `../../skills/delivery-team/jira-expert/`
```

### 2. Python Tool Paths (REQUIRED for each tool)

**Format:**
```markdown
1. **Tool Name**
   - **Purpose:** Description
   - **Path:** `../../skills/domain-team/skill-name/scripts/tool_name.py`
   - **Usage:** `python ../../skills/domain-team/skill-name/scripts/tool_name.py [arguments]`
```

**Example:**
```markdown
1. **Brand Voice Analyzer**
   - **Purpose:** Analyzes text for formality, tone, perspective, and readability
   - **Path:** `../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py`
   - **Usage:** `python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py content.txt`
```

### 3. Reference Paths (REQUIRED for each reference)

**Format:**
```markdown
1. **Reference Name**
   - **Location:** `../../skills/domain-team/skill-name/references/reference_file.md`
   - **Content:** Description
   - **Use Case:** When to use
```

**Example:**
```markdown
1. **API Design Patterns**
   - **Location:** `../../skills/engineering-team/senior-backend/references/api-design.md`
   - **Content:** REST and GraphQL API design patterns, authentication, versioning
   - **Use Case:** When designing new API endpoints
```

### 4. Template Paths (REQUIRED for each template)

**Format:**
```markdown
1. **Template Name**
   - **Location:** `../../skills/domain-team/skill-name/assets/template_name.md`
   - **Use Case:** When to use
```

**Example:**
```markdown
1. **API Documentation Template**
   - **Location:** `../../skills/engineering-team/senior-backend/assets/api-docs-template.md`
   - **Use Case:** Documenting new API endpoints
```

### 5. Reference Links (REQUIRED at end of agent)

**Format:**
```markdown
## References

- **Skill Documentation:** [../../skills/domain-team/skill-name/SKILL.md](../../skills/domain-team/skill-name/SKILL.md)
- **Domain Guide:** [../../skills/domain-team/CLAUDE.md](../../skills/domain-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)
```

**Example:**
```markdown
## References

- **Skill Documentation:** [../../skills/engineering-team/senior-backend/SKILL.md](../../skills/engineering-team/senior-backend/SKILL.md)
- **Domain Guide:** [../../skills/engineering-team/CLAUDE.md](../../skills/engineering-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)
```

## Prohibited Path Patterns

### ❌ Absolute Paths

```markdown
<!-- WRONG - absolute path -->
/Users/name/claude-skills/skills/engineering-team/senior-backend/scripts/tool.py

<!-- WRONG - absolute path from root -->
/claude-skills/skills/engineering-team/senior-backend/scripts/tool.py

<!-- WRONG - home directory expansion -->
~/claude-skills/skills/engineering-team/senior-backend/scripts/tool.py
```

### ❌ Incomplete Relative Paths

```markdown
<!-- WRONG - missing ../../ prefix -->
skills/engineering-team/senior-backend/scripts/tool.py

<!-- WRONG - only one level up -->
../skills/engineering-team/senior-backend/scripts/tool.py
```

### ❌ Wrong Skill Reference in YAML

```yaml
# WRONG - full path in skills field
skills: skills/engineering-team/senior-backend

# WRONG - relative path in skills field
skills: ../../skills/engineering-team/senior-backend

# WRONG - domain included in skills field
skills: engineering-team/senior-backend
```

## Path Validation Procedure

### Test 1: Skill Location Resolution

```bash
# Navigate to agent directory
cd agents/delivery/
# or: cd agents/engineering/

# Test that skill directory exists and is accessible
ls ../../skills/delivery-team/jira-expert/
# Should output: SKILL.md  scripts/  references/  assets/

ls ../../skills/engineering-team/senior-backend/
# Should output: SKILL.md  scripts/  references/  assets/
```

**Expected:** Directory listing without errors

### Test 2: Python Tool Execution

```bash
# From agent directory
cd agents/engineering/

# Test tool execution with --help
python ../../skills/engineering-team/senior-backend/scripts/api_generator.py --help

# Expected: Help text displayed without import errors
```

**Expected:** Help text displays without "No such file or directory" or import errors

### Test 3: Reference File Access

```bash
# From agent directory
cd agents/delivery/

# Test reference file can be read
cat ../../skills/delivery-team/jira-expert/references/jql-guide.md | head -20

# Expected: File contents displayed
```

**Expected:** File contents displayed without errors

### Test 4: Link Resolution

```bash
# From agent directory, test markdown links
cd agents/engineering/

# Test that skill SKILL.md link resolves
ls ../../skills/engineering-team/senior-backend/SKILL.md

# Test that domain CLAUDE.md link resolves
ls ../../skills/engineering-team/CLAUDE.md

# Test that agent CLAUDE.md link resolves
ls ../CLAUDE.md
```

**Expected:** All three files exist and are accessible

## Validation Checklist

Use this checklist for each agent:

**Skill Location:**
- [ ] Skill location uses `../../skills/` pattern
- [ ] Skill location path resolves from agent directory
- [ ] Skill directory contains SKILL.md, scripts/, references/, assets/

**Python Tools:**
- [ ] All tool paths use `../../skills/` pattern
- [ ] All tool paths resolve from agent directory
- [ ] All tools can be executed with `--help` flag
- [ ] Tool paths in "Path" and "Usage" fields match

**References:**
- [ ] All reference paths use `../../skills/` pattern
- [ ] All reference paths resolve from agent directory
- [ ] All references are .md files that exist

**Templates:**
- [ ] All template paths use `../../skills/` pattern
- [ ] All template paths resolve from agent directory
- [ ] All templates exist in assets/ directory

**Reference Links:**
- [ ] Skill documentation link uses `../../skills/` pattern
- [ ] Domain guide link uses `../../skills/` pattern
- [ ] Agent guide link uses `../CLAUDE.md` pattern
- [ ] All three reference links resolve correctly

**Workflows:**
- [ ] All example commands use `../../skills/` pattern
- [ ] All bash code blocks use relative paths
- [ ] No absolute paths in any workflow

**General:**
- [ ] No absolute paths anywhere in agent file
- [ ] No home directory (~/) paths
- [ ] No /Users/, /home/, C:\ paths
- [ ] All paths tested from agent directory

## Automated Path Validation Script

```bash
#!/bin/bash
# validate-paths.sh - Validate agent relative paths

AGENT_FILE=$1

if [ ! -f "$AGENT_FILE" ]; then
    echo "❌ Agent file not found: $AGENT_FILE"
    exit 1
fi

echo "🔍 Validating paths in $AGENT_FILE"

# Extract agent directory
AGENT_DIR=$(dirname "$AGENT_FILE")

# Extract all paths starting with ../../skills/
PATHS=$(grep -o "\.\./\.\./skills/[a-z-]*/[a-z-]*/[^ ]*" "$AGENT_FILE" | sort -u)

if [ -z "$PATHS" ]; then
    echo "❌ No relative paths found"
    exit 1
fi

# Test each path
cd "$AGENT_DIR" || exit 1
ERRORS=0

while IFS= read -r path; do
    # Remove trailing characters (/, `, ), etc.)
    clean_path=$(echo "$path" | sed 's/[`)\]]*$//')

    if [ -e "$clean_path" ]; then
        echo "✅ $clean_path"
    else
        echo "❌ $clean_path (not found)"
        ERRORS=$((ERRORS + 1))
    fi
done <<< "$PATHS"

# Check for absolute paths (prohibited)
ABSOLUTE=$(grep -E "(^|[^a-zA-Z0-9])(/Users/|/home/|C:\\|~/)" "$AGENT_FILE")
if [ -n "$ABSOLUTE" ]; then
    echo "❌ Found absolute paths (prohibited):"
    echo "$ABSOLUTE"
    ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -eq 0 ]; then
    echo "✅ All paths valid"
    exit 0
else
    echo "❌ Found $ERRORS path errors"
    exit 1
fi
```

**Usage:**
```bash
chmod +x validate-paths.sh
./validate-paths.sh agents/engineering/cs-backend-engineer.md
```

## Path Resolution Examples by Domain

### Marketing Domain

**Agent:** `agents/marketing/cs-content-creator.md`

```markdown
**Skill Location:** `../../skills/marketing-team/content-creator/`

### Python Tools

1. **Brand Voice Analyzer**
   - **Path:** `../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py`
   - **Usage:** `python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py content.txt`

### Knowledge Bases

1. **Brand Guidelines**
   - **Location:** `../../skills/marketing-team/content-creator/references/brand_guidelines.md`

## References

- **Skill Documentation:** [../../skills/marketing-team/content-creator/SKILL.md](../../skills/marketing-team/content-creator/SKILL.md)
- **Domain Guide:** [../../skills/marketing-team/CLAUDE.md](../../skills/marketing-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)
```

### Engineering Domain

**Agent:** `agents/engineering/cs-backend-engineer.md`

```markdown
**Skill Location:** `../../skills/engineering-team/senior-backend/`

### Python Tools

1. **API Generator**
   - **Path:** `../../skills/engineering-team/senior-backend/scripts/api_generator.py`
   - **Usage:** `python ../../skills/engineering-team/senior-backend/scripts/api_generator.py --framework flask`

### Knowledge Bases

1. **API Design Patterns**
   - **Location:** `../../skills/engineering-team/senior-backend/references/api-design.md`

## References

- **Skill Documentation:** [../../skills/engineering-team/senior-backend/SKILL.md](../../skills/engineering-team/senior-backend/SKILL.md)
- **Domain Guide:** [../../skills/engineering-team/CLAUDE.md](../../skills/engineering-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)
```

### Delivery Domain

**Agent:** `agents/delivery/cs-jira-expert.md`

```markdown
**Skill Location:** `../../skills/delivery-team/jira-expert/`

### Knowledge Bases

1. **JQL Query Guide**
   - **Location:** `../../skills/delivery-team/jira-expert/references/jql-guide.md`

## References

- **Skill Documentation:** [../../skills/delivery-team/jira-expert/SKILL.md](../../skills/delivery-team/jira-expert/SKILL.md)
- **Domain Guide:** [../../skills/delivery-team/CLAUDE.md](../../skills/delivery-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)
```

## Common Path Errors and Fixes

### Error 1: Path Works Locally But Not in Claude Code

**Symptom:** Path resolves in terminal but fails in Claude Code

**Cause:** Using absolute path that works on your machine only

**Fix:**
```markdown
<!-- ❌ WRONG -->
/Users/ricky/claude-skills/skills/engineering-team/senior-backend/scripts/tool.py

<!-- ✅ CORRECT -->
../../skills/engineering-team/senior-backend/scripts/tool.py
```

### Error 2: Tool Import Errors

**Symptom:** `ModuleNotFoundError` when running Python tools

**Cause:** Path incorrect or Python not finding script

**Fix:**
```bash
# Verify path from agent directory
cd agents/engineering/
python ../../skills/engineering-team/senior-backend/scripts/api_generator.py --help

# If it fails, check:
ls ../../skills/engineering-team/senior-backend/scripts/
python3 --version  # Ensure Python 3.8+
```

### Error 3: Reference Links Broken in Claude Code

**Symptom:** Markdown links don't resolve when clicked

**Cause:** Incorrect relative path in markdown link

**Fix:**
```markdown
<!-- ❌ WRONG - missing ../ prefix -->
[Skill Documentation](skills/engineering-team/senior-backend/SKILL.md)

<!-- ✅ CORRECT -->
[Skill Documentation](../../skills/engineering-team/senior-backend/SKILL.md)
```

---

**Last Updated:** November 12, 2025
**Contract Status:** Mandatory for all agents
**Validation:** Must pass path tests before marking production-ready
