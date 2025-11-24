# Slash Commands Development Guide

This guide provides comprehensive instructions for creating **slash commands** that automate high-frequency developer tasks in the claude-skills repository.

---

## What are Slash Commands?

**Slash commands** are task automation shortcuts that save developers time on repetitive workflows. They are invoked using a simple `/command-name` syntax and execute predefined workflows.

**Examples:**
- `/docs.update-readme` - Updates README with latest counts
- `/code.review-pr` - Performs comprehensive code review
- `/git.create-pr` - Creates pull request with proper formatting
- `/test.run-suite` - Executes full test suite with coverage

**Key Characteristics:**
- **High-frequency** - Used multiple times per day/week
- **Repetitive** - Same workflow steps each time
- **Time-saving** - Reduces manual work by 50-90%
- **Consistent** - Ensures standard quality and format

---

## Slash Commands vs Agents vs Skills

Understanding the distinction is critical for proper architecture:

| Aspect | Slash Command | Agent | Skill |
|--------|--------------|-------|-------|
| **Purpose** | Automate specific task | Orchestrate workflows | Provide tools + knowledge |
| **Invocation** | `/command-name` | `cs-agent-name` | Referenced by agents |
| **Scope** | Single focused task | Multi-step workflows | Comprehensive domain |
| **Location** | `commands/` | `agents/` | `skills/` |
| **Complexity** | Low-Medium | Medium-High | High |
| **Duration** | Seconds-Minutes | Minutes-Hours | N/A (reference) |
| **Examples** | Update docs, format code | Content creation, QA testing | Content creator, QA toolkit |

**When to Create Each:**

**Slash Command:**
- Task is repetitive and high-frequency
- Workflow is standardized
- Execution time < 5 minutes
- Clear input/output

**Agent:**
- Requires multi-step orchestration
- Needs decision-making and analysis
- Coordinates multiple tools/skills
- Complex workflows

**Skill:**
- Comprehensive domain expertise
- Reusable across agents
- Includes tools, knowledge, templates
- Foundational capability

---

## The 3 Anthropic Command Patterns

Anthropic defines 3 official patterns for structuring commands based on complexity and purpose:

### Pattern 1: Simple (Context → Task)

**Use For:** Straightforward tasks with direct execution

**Structure:**
1. **Context** - Gather necessary information
2. **Task** - Execute the action
3. **Report** - Return results

**Characteristics:**
- Single-purpose
- Minimal analysis
- Fast execution (< 1 minute)
- Clear success criteria

**Examples:**
- `/docs.update-readme` - Read files, update counts, write file
- `/git.format-code` - Read code, apply formatter, write changes
- `/test.generate-report` - Run tests, collect results, write report

**Template Structure:**
```markdown
## Usage
[Clear invocation syntax]

## What This Command Does
### Context Gathering
[What files/data are read]

### Task Execution
[Actions performed]

### Expected Output
[What user receives]
```

**When to Use:**
- Task has < 3 steps
- No complex analysis needed
- Input/output clearly defined
- Minimal decision-making

---

### Pattern 2: Multi-Phase (Discovery → Analysis → Task)

**Use For:** Complex analysis requiring systematic exploration

**Structure:**
1. **Discovery** - Explore codebase, gather comprehensive data
2. **Analysis** - Process findings, identify patterns/issues
3. **Task** - Execute actions based on analysis
4. **Report** - Present findings with recommendations

**Characteristics:**
- Multi-step process
- Requires analysis and decision-making
- Moderate execution time (1-5 minutes)
- Rich output with insights

**Examples:**
- `/code.review-pr` - Scan files, analyze quality, suggest improvements, generate report
- `/security.audit-code` - Scan for vulnerabilities, categorize by severity, recommend fixes
- `/performance.analyze-app` - Profile code, identify bottlenecks, suggest optimizations

**Template Structure:**
```markdown
## Multi-Phase Execution

### Phase 1: Discovery
**Goal:** [What we're gathering]
**Steps:** [How we gather it]
**Tools Used:** [Tools employed]

### Phase 2: Analysis
**Goal:** [What we're analyzing]
**Steps:** [How we analyze]
**Analysis Criteria:** [What we check]

### Phase 3: Task Execution
**Goal:** [What actions we take]
**Steps:** [How we execute]
**Actions:** [Specific changes made]

### Phase 4: Reporting
**Goal:** [What we present]
**Report Includes:** [Content of report]
**Report Location:** [Where saved]
```

**When to Use:**
- Task requires exploration
- Need to process/analyze data
- Multiple possible outcomes
- Recommendations needed

---

### Pattern 3: Agent-Style (Role → Process → Guidelines)

**Use For:** Specialized expertise requiring domain-specific perspective

**Structure:**
1. **Role** - Establish expert persona with specific expertise
2. **Process** - Systematic expert workflow with domain knowledge
3. **Guidelines** - Domain-specific rules and best practices
4. **Deliverables** - Expert-quality outputs

**Characteristics:**
- Mimics domain expert behavior
- Applies specialized knowledge
- Deep analysis with context
- High-quality, professional outputs

**Examples:**
- `/architecture.design-review` - Expert architect evaluates system design
- `/ux.usability-review` - UX expert assesses interface design
- `/technical-writing.edit` - Technical writer edits documentation

**Template Structure:**
```markdown
## Agent Role
You are a [domain expert] with [expertise areas]

## Expert Process

### Step 1: Understanding Requirements
[How expert gathers context]

### Step 2: Analysis & Planning
[How expert evaluates options]

### Step 3: Expert Execution
[How expert implements solution]

### Step 4: Expert Review
[How expert validates work]

## Expert Guidelines
[Domain-specific best practices]
[Anti-patterns to avoid]
[Decision framework]

## Deliverables
[Expert-quality outputs]
```

**When to Use:**
- Need domain expertise
- Quality standards matter
- Multiple approaches exist
- Requires professional judgment

---

## How to Create a Command

### Method 1: Interactive Mode (Recommended)

The easiest way to create a new command:

```bash
# Run interactive command builder
python3 scripts/command_builder.py

# Follow the prompts:
# 1. Enter command name (category.command-name)
# 2. Enter description
# 3. Select category
# 4. Choose pattern (simple, multi-phase, agent-style)
# 5. Specify optional metadata
# 6. Review and confirm
```

**Time Savings:** 30 minutes → 5 minutes (83% faster)

### Method 2: Configuration File

For creating multiple commands at once:

```bash
# Create config file (see templates/command-config.yaml)
# Then run:
python3 scripts/command_builder.py --config my-commands.yaml
```

**Benefits:**
- Batch creation
- Version control
- Team collaboration
- Repeatable

### Method 3: Manual Creation

For full control:

```bash
# 1. Copy template
cp templates/command-template.md commands/category/command-name.md

# 2. Edit metadata and content
vim commands/category/command-name.md

# 3. Validate
python3 scripts/command_builder.py --validate commands/category/command-name.md
```

---

## Command Metadata (YAML Frontmatter)

Every command must include YAML frontmatter with metadata:

### Required Fields

```yaml
---
name: category.command-name           # Kebab-case with category prefix
description: Brief description        # Max 150 characters
category: category-name               # Command category
pattern: simple                       # simple, multi-phase, or agent-style
---
```

### Optional Fields

```yaml
version: 1.0.0                        # Semantic version
author: Your Name                     # Command author
tags: [tag1, tag2, tag3]             # Searchable keywords
example_usage: /command-name arg      # Quick example
requires_input: false                 # Needs user-provided data?
requires_context: false               # Needs project context?
estimated_time: 30s                   # Execution time
model_preference: sonnet              # sonnet, opus, or haiku
tools_required: [Read, Write, Bash]   # Claude Code tools
output_format: markdown               # markdown, json, text, file
interactive: false                    # Prompts during execution?
dangerous: false                      # Modifies files/destructive?
related_commands: [other-cmd]         # Related commands
related_agents: [cs-agent]            # Related agents
related_skills: [skill-name]          # Related skills
```

### Field Explanations

**name** (required)
- Format: `category.command-name`
- Must be kebab-case (lowercase with hyphens)
- Category prefix helps organization
- Examples: `git.code-review`, `docs.update-readme`

**description** (required)
- One-line summary of command purpose
- Max 150 characters
- Action-oriented (starts with verb)
- Examples: "Updates README with latest counts", "Reviews code for quality issues"

**category** (required)
- Groups related commands
- Common categories: code, docs, git, test, deploy, workflow, security, architecture, content, data
- Used for catalog organization

**pattern** (required)
- Defines command structure
- Values: `simple`, `multi-phase`, `agent-style`
- Choose based on complexity (see patterns above)

**requires_input** (optional, default: false)
- Does command need user to provide files/arguments?
- `true` = requires arguments (e.g., `/code.review-pr 123`)
- `false` = discovers inputs automatically

**requires_context** (optional, default: false)
- Does command need specific project structure?
- `true` = must run in specific directory/project
- `false` = works anywhere

**dangerous** (optional, default: false)
- Does command modify files or run destructive operations?
- `true` = modifies git state, deletes files, runs builds
- `false` = read-only analysis and reporting
- Commands marked dangerous should ask for confirmation

**model_preference** (optional, default: sonnet)
- Preferred Claude model for execution
- `haiku` = Fast, simple tasks (< 10 seconds)
- `sonnet` = Balanced performance (most commands)
- `opus` = Complex reasoning, strategic decisions

---

## Validation Requirements

All commands must pass 8 validation checks:

### 1. Name Format
- Must follow `category.command-name` pattern
- Kebab-case (lowercase with hyphens)
- Category prefix required
- Max 40 characters

### 2. YAML Frontmatter
- Valid YAML syntax
- All required fields present
- Field values within limits
- No parsing errors

### 3. Description Length
- Max 150 characters
- Action-oriented
- Clear and concise

### 4. Pattern Validity
- Must be: `simple`, `multi-phase`, or `agent-style`
- Pattern structure must match type

### 5. Category Validity
- Recognized category
- Or valid custom category
- Used for organization

### 6. Content Completeness
- Usage section present
- Examples provided
- Error handling documented
- Related commands listed

### 7. Markdown Structure
- Valid markdown syntax
- Proper heading hierarchy
- Code blocks formatted
- Links working

### 8. Integration References
- Related agents exist (if listed)
- Related skills exist (if listed)
- Related commands exist (if listed)
- Paths resolve correctly

**Run Validation:**
```bash
# Validate single command
python3 scripts/command_builder.py --validate commands/category/command-name.md

# Validate all commands
python3 scripts/command_builder.py --validate-all
```

---

## Quality Standards

### Documentation Quality

Every command must include:

**Clear Usage Examples**
```bash
# Basic usage
/command-name arg1

# Advanced usage
/command-name arg1 --option value

# Multiple inputs
/command-name file1.txt file2.txt
```

**Error Handling Documentation**
```markdown
## Common Issues

**Issue:** [Problem description]
**Cause:** [Why it happens]
**Solution:** [How to fix]
**Prevention:** [How to avoid]
```

**Success Criteria**
```markdown
## Success Criteria

This command is successful when:
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]
```

### Code Quality (for commands that execute code)

**Standard Output**
- Support both human-readable and JSON formats
- Clear progress indicators
- Informative error messages
- Appropriate exit codes

**Error Handling**
- Validate inputs before execution
- Graceful failure with clear messages
- Rollback on errors (if modifying files)
- Log errors for debugging

**Performance**
- Execute in reasonable time (< 5 minutes)
- Show progress for long operations
- Cancel-able for interactive commands
- Efficient resource usage

---

## Testing Commands

### Manual Testing

Before committing a command:

```bash
# 1. Validate structure
python3 scripts/command_builder.py --validate commands/category/command-name.md

# 2. Test basic usage
/command-name

# 3. Test with various inputs
/command-name arg1
/command-name arg1 arg2
/command-name --help

# 4. Test error cases
/command-name invalid-input
/command-name # (if requires input)

# 5. Verify output
# Check output format, location, content
```

### Automated Testing

Commands should be testable:

```bash
# Test command exists
test -f commands/category/command-name.md

# Test validation passes
python3 scripts/command_builder.py --validate commands/category/command-name.md

# Test metadata is valid
python3 scripts/command_builder.py --validate-metadata commands/category/command-name.md
```

---

## Contribution Workflow

### Creating a New Command

```bash
# 1. Create feature branch
git checkout develop
git checkout -b feature/command-category-name

# 2. Create command (interactive)
python3 scripts/command_builder.py

# 3. Validate command
python3 scripts/command_builder.py --validate commands/category/command-name.md

# 4. Test command
/command-name
# Verify it works as expected

# 5. Update catalog (automatic in builder)
# catalog updated in commands/CATALOG.md

# 6. Commit with conventional commit
git add commands/category/command-name.md
git add commands/CATALOG.md
git commit -m "feat(commands): add category.command-name command"

# 7. Push and create PR
git push origin feature/command-category-name
# Create PR to develop branch
```

### Updating Existing Command

```bash
# 1. Create feature branch
git checkout develop
git checkout -b fix/command-category-name

# 2. Edit command file
vim commands/category/command-name.md

# 3. Validate changes
python3 scripts/command_builder.py --validate commands/category/command-name.md

# 4. Test changes
/command-name
# Verify changes work

# 5. Update version in frontmatter
# Bump version: 1.0.0 → 1.0.1 (patch)
#               1.0.0 → 1.1.0 (minor)
#               1.0.0 → 2.0.0 (major/breaking)

# 6. Commit with conventional commit
git add commands/category/command-name.md
git commit -m "fix(commands): improve category.command-name error handling"

# 7. Push and create PR
git push origin fix/command-category-name
```

---

## Website-Ready Considerations

Commands in this repository will be published to the claude-skills website. Ensure:

### Presentation Quality

**Clear Descriptions**
- User-friendly language (non-engineers should understand)
- Action-oriented (what it does, not how)
- Benefit-focused (why it's useful)

**Comprehensive Examples**
- Basic usage (simplest case)
- Common usage (typical scenario)
- Advanced usage (power user features)

**Visual Organization**
- Proper heading hierarchy
- Code blocks with syntax highlighting
- Tables for comparisons
- Lists for steps/options

### Searchability

**Tags**
- Include 3-5 relevant tags
- Use common terminology
- Think about how users search

**Keywords in Description**
- Include domain terms
- Use action verbs
- Mention key features

**Related Content**
- Link to related commands
- Reference related agents
- Mention related skills

### Accessibility

**Alt Text**
- Provide for all images/diagrams
- Describe visual content

**Clear Language**
- Simple, direct sentences
- Define technical terms
- Avoid jargon when possible

**Logical Structure**
- Sequential steps
- Clear hierarchy
- Consistent formatting

---

## Best Practices

### Naming Conventions

**Do:**
- ✓ Use category prefix: `git.create-pr`
- ✓ Use action verbs: `update`, `create`, `analyze`
- ✓ Be specific: `code.review-pr` not `review`
- ✓ Use kebab-case: `create-feature-branch`

**Don't:**
- ✗ Omit category: `create-pr`
- ✗ Use vague names: `do-stuff`
- ✗ Use underscores: `create_pr`
- ✗ Use camelCase: `createPr`

### Documentation Style

**Do:**
- ✓ Write for beginners
- ✓ Provide concrete examples
- ✓ Explain error messages
- ✓ Include success criteria
- ✓ Document edge cases

**Don't:**
- ✗ Assume prior knowledge
- ✗ Use vague instructions
- ✗ Skip error handling
- ✗ Forget examples
- ✗ Use jargon without explanation

### Command Design

**Do:**
- ✓ Single responsibility
- ✓ Clear inputs/outputs
- ✓ Idempotent (safe to re-run)
- ✓ Fast execution (< 5 min)
- ✓ Informative feedback

**Don't:**
- ✗ Try to do too much
- ✗ Hidden side effects
- ✗ Destructive without confirmation
- ✗ Long-running without progress
- ✗ Silent failures

---

## Command Categories

### Code Category

Commands for code-related operations:
- `code.review-pr` - PR code review
- `code.format-check` - Format validation
- `code.refactor-suggest` - Refactoring suggestions
- `code.complexity-analyze` - Complexity analysis

### Docs Category

Commands for documentation:
- `docs.update-readme` - Update README
- `docs.validate-links` - Check broken links
- `docs.generate-catalog` - Create catalog
- `docs.spell-check` - Spell checking

### Git Category

Commands for git workflows:
- `git.create-pr` - Create pull request
- `git.create-branch` - Create feature branch
- `git.commit-conventional` - Conventional commit
- `git.sync-develop` - Sync with develop

### Test Category

Commands for testing:
- `test.run-suite` - Run full test suite
- `test.coverage-report` - Generate coverage
- `test.integration-tests` - Run integration tests
- `test.e2e-tests` - Run E2E tests

### Deploy Category

Commands for deployment:
- `deploy.staging` - Deploy to staging
- `deploy.production` - Deploy to production
- `deploy.rollback` - Rollback deployment
- `deploy.health-check` - Health check

### Security Category

Commands for security:
- `security.scan-secrets` - Scan for secrets
- `security.audit-deps` - Audit dependencies
- `security.vulnerability-scan` - Vulnerability scan
- `security.compliance-check` - Compliance check

### Architecture Category

Commands for architecture:
- `architecture.design-review` - Design review
- `architecture.generate-diagram` - Generate diagram
- `architecture.dependency-analysis` - Analyze dependencies
- `architecture.api-design` - API design review

---

## Common Patterns

### File Processing Pattern

```markdown
## Context Gathering
1. Use Glob to find target files
2. Read files with Read tool
3. Validate file format/content

## Task Execution
1. Process each file
2. Apply transformations
3. Validate results

## Expected Output
- Modified files (or report)
- Summary of changes
- Error report (if any)
```

### Analysis Pattern

```markdown
## Discovery Phase
1. Scan codebase with Grep/Glob
2. Collect relevant data
3. Catalog findings

## Analysis Phase
1. Process collected data
2. Apply analysis criteria
3. Calculate metrics/scores
4. Categorize findings

## Reporting Phase
1. Generate summary report
2. List detailed findings
3. Provide recommendations
4. Include metrics
```

### Git Workflow Pattern

```markdown
## Pre-Flight Checks
1. Check git status
2. Verify branch state
3. Ensure no conflicts

## Execution
1. Perform git operations
2. Validate results
3. Update tracking

## Post-Execution
1. Verify success
2. Report changes
3. Suggest next steps
```

---

## Troubleshooting

### Command Not Found

**Issue:** `/command-name` not recognized
**Solution:**
1. Check file exists: `ls commands/category/command-name.md`
2. Check file name matches metadata `name:` field
3. Restart Claude Code to reload commands

### Validation Fails

**Issue:** `command_builder.py --validate` reports errors
**Solution:**
1. Read error messages carefully
2. Fix reported issues
3. Re-run validation
4. See [docs/standards/command-standards.md](../docs/standards/command-standards.md)

### Command Execution Errors

**Issue:** Command runs but fails
**Solution:**
1. Check requires_input: does it need arguments?
2. Check requires_context: are you in right directory?
3. Check error messages in output
4. Verify required tools available
5. Check file permissions

---

## Additional Resources

### Documentation
- **[Command Standards](../docs/standards/command-standards.md)** - Validation rules
- **[Command Template](../templates/command-template.md)** - Starting template
- **[Command Config Example](../templates/command-config.yaml)** - Config file example
- **[Command Catalog](CATALOG.md)** - All available commands

### Related Guides
- **[Agent Development](../agents/CLAUDE.md)** - Creating agents
- **[Skill Development](../skills/marketing-team/CLAUDE.md)** - Creating skills
- **[Builder Standards](../docs/standards/builder-standards.md)** - Quality standards

### Tools
- **command_builder.py** - Command creation and validation tool
- **agent_builder.py** - Agent creation (commands can reference agents)
- **skill_builder.py** - Skill creation (commands can use skills)

---

**Last Updated:** November 24, 2025
**Current Status:** Foundation documentation, builder tool pending
**Next Steps:** Implement command_builder.py, create initial command set
**Maintained By:** Claude Skills Team
