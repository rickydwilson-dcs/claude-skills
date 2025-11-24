# Command Standards

**Version**: 1.0.0
**Last Updated**: November 24, 2025
**Status**: Foundation

This document defines validation standards and quality criteria for slash commands in the Claude Skills repository.

---

## Table of Contents

1. [Overview](#overview)
2. [Validation Standards](#validation-standards)
3. [Quality Standards](#quality-standards)
4. [Website-Ready Checklist](#website-ready-checklist)
5. [PR Submission Requirements](#pr-submission-requirements)

---

## Overview

### Purpose

Command standards ensure:
- **Consistency** - All commands follow same structure and format
- **Quality** - Commands are well-documented and reliable
- **Discoverability** - Users can find and understand commands easily
- **Maintainability** - Commands are easy to update and extend

### Zero-Dependency Requirement

Command builder **MUST**:
- Use Python 3.8+ standard library only
- Implement custom YAML parser (no PyYAML)
- Work in air-gapped environments
- Have no external API dependencies

**Rationale:** Maximum portability and security for enterprise use

---

## Validation Standards

All commands must pass 8 validation checks before being accepted:

### 1. Name Format Validation

**Standard:** Command names **MUST** follow `verb.object` pattern with category prefix

**Rules:**
- Kebab-case (lowercase with hyphens only)
- **MUST start with action verb** (analyze, generate, review, create, update, etc.)
- Format: `verb.object` or `verb.object-details`
- Separator is dot (`.`) between verb and object
- Max 40 characters total
- Action-oriented, command-style naming

**Rationale:** Commands represent actions we want performed. Using verbs makes intent clear and matches how we naturally communicate ("analyze this", "generate that").

**Valid Examples:**
```
✓ analyze.code-quality      (verb: analyze, object: code-quality)
✓ generate.tests            (verb: generate, object: tests)
✓ review.security           (verb: review, object: security)
✓ create.documentation      (verb: create, object: documentation)
✓ update.dependencies       (verb: update, object: dependencies)
✓ check.vulnerabilities     (verb: check, object: vulnerabilities)
✓ format.code               (verb: format, object: code)
✓ deploy.staging            (verb: deploy, object: staging)
```

**Invalid Examples:**
```
✗ code.review               (noun first, verb second - backwards)
✗ security.scan             (noun first, not action-oriented)
✗ CodeReview                (no separator, not kebab-case)
✗ code_review               (underscore instead of hyphen)
✗ git-review                (hyphen instead of dot separator)
✗ Review                    (uppercase letter)
✗ review                    (no object specified)
✗ analyze.this-very-long-command-name-exceeds-limits  (> 40 chars)
```

**Common Action Verbs:**
- `analyze.*` - Code analysis, metrics, patterns
- `generate.*` - Create code, docs, tests
- `review.*` - Code review, security review
- `create.*` - New resources, files, configs
- `update.*` - Modify existing resources
- `check.*` - Validation, verification
- `format.*` - Code formatting, styling
- `deploy.*` - Deployment operations
- `test.*` - Testing operations
- `commit.*` - Git commit operations
- `merge.*` - Git merge operations
- `cleanup.*` - Cleanup operations

**Implementation:** `^[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$` regex pattern

**Validation:**
```python
import re

def validate_command_name(name: str) -> tuple[bool, str]:
    """Validate command name format."""
    if not name:
        return False, "Command name cannot be empty"

    if len(name) > 40:
        return False, f"Command name too long ({len(name)} chars, max 40)"

    if '.' not in name:
        return False, "Command name must include category prefix (category.name)"

    pattern = r'^[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$'
    if not re.match(pattern, name):
        return False, "Command name must be kebab-case with category prefix (category.command-name)"

    return True, "Valid"
```

---

### 2. YAML Frontmatter Validation

**Standard:** All commands **MUST** include valid YAML frontmatter with required fields

**Required Fields:**
```yaml
---
name: category.command-name           # Must match filename
description: Brief description        # Max 150 characters
category: category-name               # Valid category
pattern: simple                       # simple, multi-phase, or agent-style
---
```

**Optional Fields:**
```yaml
version: 1.0.0                        # Semantic version (X.Y.Z)
author: Your Name                     # Command author
tags: [tag1, tag2, tag3]             # 3-5 searchable keywords
example_usage: /command-name arg      # Quick usage example
requires_input: false                 # Needs user-provided data?
requires_context: false               # Needs project context?
estimated_time: 30s                   # Execution time estimate
model_preference: sonnet              # sonnet, opus, or haiku
tools_required: [Read, Write, Bash]   # Claude Code tools
output_format: markdown               # markdown, json, text, file
interactive: false                    # Prompts during execution?
dangerous: false                      # Modifies files/destructive?
related_commands: [other-cmd]         # Related commands
related_agents: [cs-agent]            # Related agents
related_skills: [skill-name]          # Related skills
```

**Validation Checks:**
- ✓ Frontmatter enclosed in `---` delimiters
- ✓ Valid YAML syntax (no parsing errors)
- ✓ All required fields present
- ✓ `name` matches filename
- ✓ `description` ≤ 150 characters
- ✓ `category` is recognized or valid custom
- ✓ `pattern` is one of: simple, multi-phase, agent-style
- ✓ `version` follows semver (if present)
- ✓ `model_preference` is one of: sonnet, opus, haiku (if present)
- ✓ `tools_required` is valid array (if present)
- ✓ `tags` has 3-5 items (if present)

**Error Examples:**
```yaml
# ✗ Missing required field 'name'
---
description: Updates README
category: docs
pattern: simple
---

# ✗ Description too long (160 chars)
---
name: docs.update
description: This is a very long description that exceeds the maximum allowed character limit and will fail validation because it is way too verbose and detailed
category: docs
pattern: simple
---

# ✗ Invalid pattern value
---
name: docs.update
description: Updates README
category: docs
pattern: complex  # Should be: simple, multi-phase, or agent-style
---

# ✗ Invalid model_preference
---
name: code.review
description: Code review
category: code
pattern: multi-phase
model_preference: gpt4  # Should be: sonnet, opus, or haiku
---
```

---

### 3. Description Length Validation

**Standard:** Description **MUST** be ≤ 150 characters

**Rules:**
- Action-oriented (starts with verb)
- Clear and concise
- Describes what, not how
- No technical jargon (when possible)

**Valid Examples:**
```
✓ "Updates README.md with latest agent and skill counts" (56 chars)
✓ "Performs comprehensive code review with quality analysis" (60 chars)
✓ "Deploys current branch to staging environment with health checks" (67 chars)
```

**Invalid Examples:**
```
✗ "This command updates the README file" (37 chars but vague - what does it update?)
✗ "Updates README.md with the latest counts of agents and skills and also updates the version numbers and ensures all links are working properly and validates" (161 chars - too long)
```

---

### 4. Pattern Validity Validation

**Standard:** Pattern **MUST** be one of: `simple`, `multi-phase`, `agent-style`

**Pattern Requirements:**

#### Simple Pattern
Must include these sections:
- `## Usage` - Clear invocation syntax
- `## What This Command Does` - Context, Task, Output subsections
- `## Examples` - At least 2 usage examples

#### Multi-Phase Pattern
Must include these sections:
- `## Usage` - Clear invocation syntax
- `## Multi-Phase Execution` - All 4 phases documented:
  - Phase 1: Discovery
  - Phase 2: Analysis
  - Phase 3: Task Execution
  - Phase 4: Reporting
- `## Examples` - At least 2 usage examples

#### Agent-Style Pattern
Must include these sections:
- `## Usage` - Clear invocation syntax
- `## Agent Role` - Expert persona definition
- `## Expert Process` - All 4 steps documented:
  - Step 1: Understanding Requirements
  - Step 2: Analysis & Planning
  - Step 3: Expert Execution
  - Step 4: Expert Review
- `## Expert Guidelines` - Best practices and anti-patterns
- `## Deliverables` - Expert-quality outputs
- `## Examples` - At least 2 usage examples

**Validation:**
```python
def validate_pattern(content: str, pattern: str) -> tuple[bool, str]:
    """Validate command matches declared pattern structure."""
    if pattern == 'simple':
        required = ['## Usage', '## What This Command Does', '## Examples']
    elif pattern == 'multi-phase':
        required = ['## Usage', '## Multi-Phase Execution', '## Examples']
        phases = ['Phase 1: Discovery', 'Phase 2: Analysis',
                  'Phase 3: Task Execution', 'Phase 4: Reporting']
        for phase in phases:
            if phase not in content:
                return False, f"Multi-phase pattern missing: {phase}"
    elif pattern == 'agent-style':
        required = ['## Usage', '## Agent Role', '## Expert Process',
                    '## Expert Guidelines', '## Deliverables', '## Examples']
        steps = ['Step 1: Understanding Requirements', 'Step 2: Analysis & Planning',
                 'Step 3: Expert Execution', 'Step 4: Expert Review']
        for step in steps:
            if step not in content:
                return False, f"Agent-style pattern missing: {step}"
    else:
        return False, f"Invalid pattern: {pattern}"

    for section in required:
        if section not in content:
            return False, f"Missing required section: {section}"

    return True, "Valid"
```

---

### 5. Category Validity Validation

**Standard:** Category **MUST** be recognized or valid custom category

**Standard Categories:**
- `code` - Code-related operations (review, format, refactor)
- `docs` - Documentation operations (update, generate, validate)
- `git` - Git workflow operations (branch, commit, PR)
- `test` - Testing operations (run tests, coverage, QA)
- `deploy` - Deployment operations (staging, production, rollback)
- `workflow` - General workflow automation
- `security` - Security scanning and analysis
- `architecture` - System design and architecture
- `content` - Content creation and marketing
- `data` - Data analysis and processing

**Custom Categories:**
Valid if:
- Kebab-case
- Lowercase only
- 3-20 characters
- Represents clear grouping

**Validation:**
```python
STANDARD_CATEGORIES = {
    'code', 'docs', 'git', 'test', 'deploy', 'workflow',
    'security', 'architecture', 'content', 'data'
}

def validate_category(category: str) -> tuple[bool, str]:
    """Validate command category."""
    if not category:
        return False, "Category cannot be empty"

    if category in STANDARD_CATEGORIES:
        return True, "Valid standard category"

    # Check custom category format
    if not re.match(r'^[a-z][a-z0-9-]{2,19}$', category):
        return False, "Custom category must be kebab-case, 3-20 chars"

    return True, f"Valid custom category: {category}"
```

---

### 6. Content Completeness Validation

**Standard:** Commands **MUST** include comprehensive documentation

**Required Sections:**
- `## Usage` - Invocation syntax and arguments
- `## Examples` - At least 2 concrete usage examples
- `## Error Handling` - Common issues and solutions
- `## Success Criteria` - How to measure success
- `## Related Commands` - Links to related commands

**Usage Section Requirements:**
```markdown
## Usage

\`\`\`bash
/command-name [required-arg] [optional-arg]
\`\`\`

### Arguments

- `required-arg` - Description (required)
- `optional-arg` - Description (optional, default: value)

### Examples

\`\`\`bash
# Example 1: Basic usage
/command-name input.txt

# Example 2: Advanced usage
/command-name input.txt --option value
\`\`\`
```

**Error Handling Requirements:**
```markdown
## Error Handling

### Common Issues

**Issue:** [Problem description]
**Cause:** [Why it happens]
**Solution:** [How to fix it]
**Prevention:** [How to avoid it]

---

[Repeat for at least 3 common issues]
```

**Success Criteria Requirements:**
```markdown
## Success Criteria

This command is successful when:

- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]

### Quality Metrics

**Expected Outcomes:**
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]
```

---

### 7. Markdown Structure Validation

**Standard:** Commands **MUST** follow proper markdown structure

**Required Structure:**
- H1 title (only one)
- H2 major sections
- H3 subsections
- Proper heading hierarchy (no skipped levels)
- Valid markdown syntax
- Code blocks with syntax highlighting
- Working internal links

**Validation Checks:**
- ✓ Single H1 title
- ✓ No skipped heading levels
- ✓ Code blocks have language specifiers
- ✓ Lists properly formatted
- ✓ Tables have headers
- ✓ No broken internal links

**Example:**
```markdown
# Command Name                    # ✓ Single H1

## Usage                          # ✓ H2 section

### Arguments                     # ✓ H3 subsection

#### Detailed Options             # ✓ H4 if needed

### Examples                      # ✓ H3 subsection

## Error Handling                 # ✓ H2 section

### Common Issues                 # ✓ H3 subsection
```

**Invalid Examples:**
```markdown
# Title
### Subsection                    # ✗ Skipped H2
```

---

### 8. Integration References Validation

**Standard:** Referenced agents, skills, and commands **MUST** exist

**Validation:**
- If `related_agents` listed → verify agent files exist
- If `related_skills` listed → verify skill directories exist
- If `related_commands` listed → verify command files exist
- All internal links resolve correctly

**Example Validation:**
```python
def validate_references(metadata: dict, repo_root: Path) -> tuple[bool, list[str]]:
    """Validate all referenced agents, skills, commands exist."""
    errors = []

    # Check related agents
    if 'related_agents' in metadata:
        for agent in metadata['related_agents']:
            if not find_agent_file(agent, repo_root):
                errors.append(f"Agent not found: {agent}")

    # Check related skills
    if 'related_skills' in metadata:
        for skill in metadata['related_skills']:
            if not find_skill_dir(skill, repo_root):
                errors.append(f"Skill not found: {skill}")

    # Check related commands
    if 'related_commands' in metadata:
        for cmd in metadata['related_commands']:
            if not find_command_file(cmd, repo_root):
                errors.append(f"Command not found: {cmd}")

    return len(errors) == 0, errors
```

---

## Quality Standards

Beyond validation, commands should meet these quality criteria:

### Documentation Quality

**Clear Examples**
- At least 2 concrete examples
- Basic usage example
- Advanced usage example
- Real-world scenarios

**Comprehensive Error Handling**
- Document 3+ common issues
- Include cause and solution
- Provide prevention tips

**Actionable Instructions**
- Step-by-step procedures
- Specific commands to run
- Expected outputs shown

### Code Quality (for executable commands)

**Standard Output**
- Support JSON output format (for automation)
- Human-readable default output
- Clear progress indicators
- Informative error messages

**Error Handling**
- Validate inputs before execution
- Fail fast with clear messages
- No silent failures
- Appropriate exit codes (0 = success, 1 = error)

**Performance**
- Execute in reasonable time (< 5 minutes typical)
- Show progress for long operations
- Efficient resource usage
- Cancel-able for interactive commands

### User Experience

**Discoverability**
- Clear, descriptive name
- Action-oriented description
- Relevant tags for search
- Related commands linked

**Usability**
- Intuitive invocation
- Sensible defaults
- Helpful error messages
- Success feedback

---

## The 8 Validation Checks Explained

### Check 1: Name Format ✓
- Validates: `category.command-name` pattern, kebab-case, length
- Purpose: Ensures consistent naming and discoverability
- Common failures: Missing category, wrong separator, uppercase

### Check 2: YAML Frontmatter ✓
- Validates: Valid YAML, required fields, field constraints
- Purpose: Enables metadata-driven features and cataloging
- Common failures: Missing fields, invalid values, syntax errors

### Check 3: Description Length ✓
- Validates: ≤ 150 characters, action-oriented
- Purpose: Ensures concise, clear communication
- Common failures: Too verbose, vague descriptions

### Check 4: Pattern Validity ✓
- Validates: Pattern type and required sections
- Purpose: Ensures command follows appropriate structure
- Common failures: Missing pattern sections, wrong structure

### Check 5: Category Validity ✓
- Validates: Standard or valid custom category
- Purpose: Enables proper organization and grouping
- Common failures: Invalid format, too long/short

### Check 6: Content Completeness ✓
- Validates: Required sections present and complete
- Purpose: Ensures comprehensive documentation
- Common failures: Missing examples, no error handling

### Check 7: Markdown Structure ✓
- Validates: Proper markdown syntax and hierarchy
- Purpose: Ensures readable, properly formatted docs
- Common failures: Skipped headings, invalid syntax

### Check 8: Integration References ✓
- Validates: Referenced resources exist
- Purpose: Prevents broken links and references
- Common failures: Referenced non-existent agents/skills

---

## Website-Ready Checklist

Before marking command as website-ready:

### Content Quality
- [ ] Description is user-friendly (non-engineers understand)
- [ ] Examples are comprehensive (basic, common, advanced)
- [ ] Error messages are actionable
- [ ] Success criteria are specific
- [ ] All sections complete and well-written

### Technical Quality
- [ ] All 8 validations pass
- [ ] Command tested and working
- [ ] Examples tested and verified
- [ ] Links resolve correctly
- [ ] Code blocks have syntax highlighting

### Presentation Quality
- [ ] Proper heading hierarchy
- [ ] Consistent formatting
- [ ] Clear, organized structure
- [ ] No spelling/grammar errors
- [ ] Professional tone

### Searchability
- [ ] 3-5 relevant tags
- [ ] Keywords in description
- [ ] Related content linked
- [ ] Category appropriate

### Accessibility
- [ ] Alt text for images (if any)
- [ ] Clear, simple language
- [ ] Logical structure
- [ ] Scannable format

---

## PR Submission Requirements

### Required Files

When submitting command PR, include:

```
commands/
  category/
    command-name.md       # ✓ Command file
  CATALOG.md              # ✓ Updated catalog entry
```

### PR Description Template

```markdown
## Command: /category.command-name

### Description
[Brief description of what command does]

### Pattern
[simple | multi-phase | agent-style]

### Testing
- [ ] All 8 validations pass
- [ ] Tested basic usage
- [ ] Tested with various inputs
- [ ] Tested error cases
- [ ] Verified output format

### Checklist
- [ ] Follows naming conventions
- [ ] YAML frontmatter complete
- [ ] Examples provided and tested
- [ ] Error handling documented
- [ ] Related commands linked
- [ ] Catalog updated

### Related
- Related agents: [list]
- Related skills: [list]
- Related commands: [list]
```

### Review Criteria

PR reviewers will check:

1. **Validation** - All 8 checks pass
2. **Testing** - Command tested and works
3. **Documentation** - Complete and clear
4. **Standards** - Follows command standards
5. **Integration** - Works with agents/skills
6. **Quality** - Meets quality standards

### Approval Requirements

Command PRs require:
- ✓ All 8 validations pass
- ✓ 1 reviewer approval
- ✓ Testing evidence provided
- ✓ Catalog updated
- ✓ Conventional commit message

**Commit Format:**
```bash
feat(commands): add category.command-name command

- Pattern: [simple/multi-phase/agent-style]
- Category: [category]
- Purpose: [brief description]

Closes #[issue-number]
```

---

## Command Builder Tool

### Usage

```bash
# Interactive mode (recommended)
python3 scripts/command_builder.py

# Config file mode
python3 scripts/command_builder.py --config commands-config.yaml

# Validate existing command
python3 scripts/command_builder.py --validate commands/category/command-name.md

# Validate all commands
python3 scripts/command_builder.py --validate-all

# Generate catalog
python3 scripts/command_builder.py --generate-catalog
```

### Features

- **Interactive Creation** - Step-by-step command creation
- **Config-Based Creation** - Batch command creation
- **Validation** - All 8 checks automated
- **Catalog Generation** - Auto-update command catalog
- **Template Support** - Uses command-template.md
- **Zero Dependencies** - Python standard library only

---

## Version History

**v1.0.0** (November 24, 2025)
- Initial command standards documentation
- 8 validation checks defined
- Quality standards established
- Website-ready checklist created
- PR submission requirements documented

---

## References

- [Command Development Guide](../../commands/CLAUDE.md) - How to create commands
- [Command Template](../../templates/command-template.md) - Starting template
- [Command Config Example](../../templates/command-config.yaml) - Config examples
- [Builder Standards](builder-standards.md) - General builder standards

---

**Maintained By**: Claude Skills Team
**Review Cadence**: Quarterly
**Next Review**: February 2026
