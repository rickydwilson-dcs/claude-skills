# Command Creation Guide

This guide provides comprehensive instructions for creating new slash commands for the claude-skills library.

---

## Table of Contents

- [Overview](#overview)
- [Before You Start](#before-you-start)
- [Creation Methods](#creation-methods)
- [Command Structure](#command-structure)
- [Patterns Deep Dive](#patterns-deep-dive)
- [Step-by-Step Tutorial](#step-by-step-tutorial)
- [Best Practices](#best-practices)
- [Validation](#validation)
- [Publishing](#publishing)

---

## Overview

### What You'll Create

A **slash command** is a markdown file with:
- YAML frontmatter (metadata)
- Structured content (instructions for Claude)
- Examples and documentation
- Error handling guidelines

### Time Investment

- **Manual creation**: ~30 minutes per command
- **With command_builder.py**: ~5 minutes per command
- **Validation**: ~30 seconds per command

### Quality Standards

All commands must:
- Pass 8 validation checks
- Follow one of 3 official patterns
- Include comprehensive examples
- Document error handling
- Provide clear success criteria

---

## Before You Start

### 1. Research Existing Commands

Check if a similar command already exists:

```bash
# List all commands
python3 scripts/install_commands.py --list

# Search for related commands
python3 scripts/install_commands.py --search "review"

# Review command catalog
cat commands/CATALOG.md
```

**Why:** Avoid duplication, maintain consistency, learn from existing patterns.

---

### 2. Identify the Use Case

Ask yourself:

**Frequency**
- How often will this be used? (Daily? Weekly? Monthly?)
- Is it truly repetitive work?

**Value**
- How much time will it save?
- Does it improve quality/consistency?
- Is it worth maintaining?

**Scope**
- Is it a single focused task? (Good for command)
- Or a multi-step workflow? (Maybe use agent instead)

**Target:** Commands should be used multiple times per week and save 50%+ time.

---

### 3. Choose the Right Pattern

Commands follow one of **3 official Anthropic patterns**:

| Pattern | Complexity | Duration | Use Case |
|---------|-----------|----------|----------|
| **Simple** | Low | < 1 min | Direct task execution |
| **Multi-Phase** | Medium | 1-5 min | Analysis + execution |
| **Agent-Style** | High | 3-10 min | Expert workflow |

**Decision Tree:**

```
Does task require domain expertise or strategic thinking?
├─ YES → Agent-Style Pattern
└─ NO → Does task require analysis/discovery?
    ├─ YES → Multi-Phase Pattern
    └─ NO → Simple Pattern
```

**Examples:**

- **Simple**: Update README, format code, commit with message
- **Multi-Phase**: Code review, security audit, test generation
- **Agent-Style**: Architecture review, UX analysis, technical writing

---

### 4. Review Standards

Read these before creating:

- [commands/CLAUDE.md](../commands/CLAUDE.md) - Development guide
- [templates/command-template.md](../templates/command-template.md) - Template file
- [docs/standards/command-standards.md](../docs/standards/command-standards.md) - Validation rules (if exists)

---

## Creation Methods

### Method 1: Interactive Builder (Recommended)

**Status:** Planned for future release

```bash
# Will provide interactive prompts
python3 scripts/command_builder.py

# Steps:
# 1. Enter command name
# 2. Enter description
# 3. Choose category
# 4. Select pattern
# 5. Configure metadata
# 6. Review and generate
```

**Time:** ~5 minutes per command

---

### Method 2: Manual Creation (Current Method)

Create command files manually:

```bash
# 1. Copy template
cp templates/command-template.md commands/category/command-name.md

# 2. Edit file
vim commands/category/command-name.md

# 3. Fill in all sections
# 4. Validate
# 5. Test
```

**Time:** ~30 minutes per command

**When to Use:**
- Command builder not yet available
- Need full control over content
- Creating complex agent-style command
- Learning command structure

---

### Method 3: Configuration File (Future)

**Status:** Planned

```bash
# Create config file
vim my-commands.yaml

# Generate multiple commands
python3 scripts/command_builder.py --config my-commands.yaml
```

**Use Case:** Batch creation, team standardization

---

## Command Structure

### File Location

Commands are organized by category:

```
commands/
├── analysis/
│   ├── analysis.code-review.md
│   └── analysis.security-audit.md
├── generation/
│   ├── generation.test-generate.md
│   └── generation.api-document.md
├── git/
│   ├── git.commit-assist.md
│   └── git.branch-cleanup.md
└── workflow/
    ├── workflow.pr-create.md
    └── workflow.update-docs.md
```

**Naming:** `commands/{category}/{category}.{command-name}.md`

---

### File Structure

Every command has this structure:

```markdown
---
# YAML Frontmatter (metadata)
name: category.command-name
description: Brief description
category: category-name
pattern: simple|multi-phase|agent-style
version: 1.0.0
# ... other metadata
---

# Command Title

Brief introduction paragraph.

## Usage

How to invoke the command.

## What This Command Does

Detailed explanation of behavior.

## Expected Output

What the user receives.

## Examples

Concrete usage examples.

## Error Handling

Common issues and solutions.

## Related Commands

Links to similar commands.
```

---

### YAML Frontmatter

#### Required Fields

```yaml
---
name: category.command-name
description: One-line summary (max 150 chars)
category: category-name
pattern: simple
---
```

#### Recommended Fields

```yaml
version: 1.0.0
author: Your Name
tags: [tag1, tag2, tag3]
estimated_time: 30s
model_preference: sonnet
output_format: markdown
```

#### Optional Fields

```yaml
requires_input: false        # Needs user arguments?
requires_context: false      # Needs project structure?
interactive: false           # Prompts during execution?
dangerous: false             # Modifies files?
tools_required: [Read, Write]
related_commands: []
related_agents: []
related_skills: []
```

---

## Patterns Deep Dive

### Pattern 1: Simple (Context → Task)

**Structure:**

```markdown
## Usage
/command-name [arguments]

## What This Command Does

### Context Gathering
1. Read necessary files
2. Validate inputs
3. Gather context

### Task Execution
1. Perform action
2. Validate results
3. Handle errors

### Expected Output
- Output location
- Format
- Content summary
```

**Example: Update README**

```markdown
---
name: docs.update-readme
description: Updates README.md with current repository statistics
category: docs
pattern: simple
---

# Update README

Updates README.md with current counts of agents, skills, and commands.

## Usage

```bash
/docs.update-readme
```

## What This Command Does

### Context Gathering
1. Counts agents in `agents/` directory
2. Counts skills in `skills/` directory
3. Counts commands in `commands/` directory
4. Reads current README.md

### Task Execution
1. Updates statistics section
2. Updates last modified date
3. Writes updated README.md
4. Validates markdown formatting

### Expected Output
- Updated README.md with current statistics
- Summary of changes made
```

---

### Pattern 2: Multi-Phase (Discovery → Analysis → Task)

**Structure:**

```markdown
## Multi-Phase Execution

### Phase 1: Discovery
**Goal:** Gather comprehensive data

**Steps:**
1. Scan codebase
2. Collect relevant files
3. Build data catalog

### Phase 2: Analysis
**Goal:** Process and evaluate findings

**Steps:**
1. Analyze collected data
2. Apply quality criteria
3. Categorize findings
4. Calculate metrics

### Phase 3: Task Execution
**Goal:** Take action based on analysis

**Steps:**
1. Execute recommended changes
2. Validate results
3. Handle errors

### Phase 4: Reporting
**Goal:** Present comprehensive results

**Report Includes:**
- Executive summary
- Detailed findings
- Recommendations
- Metrics/scores
```

**Example: Code Review**

```markdown
---
name: analysis.code-review
description: Comprehensive code quality review with actionable recommendations
category: analysis
pattern: multi-phase
estimated_time: 2-5 min
---

# Code Review

Performs systematic code quality analysis.

## Multi-Phase Execution

### Phase 1: Discovery
**Goal:** Scan codebase for review candidates

**Steps:**
1. Use Glob to find source files
2. Read file contents
3. Extract code structure
4. Identify review areas

**Tools Used:** Glob, Read

### Phase 2: Analysis
**Goal:** Evaluate code quality

**Steps:**
1. Check code complexity
2. Identify code smells
3. Review naming conventions
4. Assess test coverage
5. Check documentation

**Analysis Criteria:**
- Complexity metrics
- Best practice compliance
- Maintainability score
- Test coverage percentage

### Phase 3: Task Execution
**Goal:** Generate actionable recommendations

**Steps:**
1. Prioritize findings
2. Suggest improvements
3. Provide code examples
4. Estimate effort

### Phase 4: Reporting
**Goal:** Present comprehensive review

**Report Includes:**
- Executive summary
- Detailed findings by category
- Code examples (before/after)
- Priority rankings
- Effort estimates

**Report Location:** `output/{session}/code-review-report.md`
```

---

### Pattern 3: Agent-Style (Role → Process → Guidelines)

**Structure:**

```markdown
## Agent Role

You are a [domain expert] with expertise in [areas].

Your responsibilities:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

## Expert Process

### Step 1: Understanding Requirements
[How expert gathers context]

### Step 2: Analysis & Planning
[How expert evaluates options]

### Step 3: Expert Execution
[How expert implements solution]

### Step 4: Expert Review
[How expert validates quality]

## Expert Guidelines

### Best Practices
- [Practice 1]
- [Practice 2]

### Anti-Patterns to Avoid
- [Anti-pattern 1]
- [Anti-pattern 2]

### Decision Framework
[How expert makes decisions]

## Deliverables

[Expert-quality outputs with specific format]
```

**Example: Architecture Review**

```markdown
---
name: architecture.design-review
description: Expert architecture review with system design recommendations
category: architecture
pattern: agent-style
estimated_time: 5-10 min
model_preference: opus
---

# Architecture Design Review

Expert-level architecture review and recommendations.

## Agent Role

You are a **Senior Software Architect** with 15+ years of experience in:
- System design and architecture
- Scalability and performance
- Security and compliance
- Cloud infrastructure
- Microservices architecture

Your responsibilities:
- Evaluate system design decisions
- Identify architectural risks
- Recommend improvements
- Ensure best practices

## Expert Process

### Step 1: Understanding Requirements

**Context Gathering:**
1. Review system architecture documentation
2. Understand business requirements
3. Identify technical constraints
4. Map stakeholder concerns

**Questions to Answer:**
- What problem does the system solve?
- What are the scale requirements?
- What are the critical quality attributes?
- What are the integration points?

### Step 2: Analysis & Planning

**Architecture Evaluation:**
1. Assess architectural patterns
2. Evaluate component boundaries
3. Review data flow
4. Analyze dependencies
5. Identify bottlenecks

**Evaluation Criteria:**
- Scalability
- Maintainability
- Security
- Performance
- Cost efficiency

### Step 3: Expert Execution

**Review Activities:**
1. Document current architecture
2. Identify design issues
3. Propose alternatives
4. Provide recommendations
5. Create decision records

### Step 4: Expert Review

**Quality Validation:**
1. Verify recommendations are actionable
2. Ensure trade-offs are clear
3. Validate technical feasibility
4. Check alignment with best practices

## Expert Guidelines

### Best Practices

**System Design:**
- Start with requirements, not technology
- Design for change
- Keep it simple (KISS)
- Plan for failure

**Architecture Patterns:**
- Choose patterns based on requirements
- Don't over-engineer
- Document decisions (ADRs)
- Consider operational complexity

### Anti-Patterns to Avoid

- Big Ball of Mud (no clear structure)
- Premature optimization
- Technology-driven design
- Ignoring non-functional requirements
- Tight coupling between components

### Decision Framework

**When evaluating options:**

1. **Understand trade-offs**
   - Performance vs. Complexity
   - Cost vs. Scalability
   - Speed of delivery vs. Quality

2. **Consider constraints**
   - Team skills
   - Budget
   - Timeline
   - Technical debt

3. **Prioritize quality attributes**
   - What matters most?
   - What's the acceptable threshold?

## Deliverables

### Architecture Review Report

**Format:** Markdown document

**Sections:**
1. **Executive Summary**
   - Overall assessment
   - Key findings
   - Recommendations

2. **Current Architecture**
   - Component diagram
   - Data flow
   - Technology stack

3. **Findings**
   - Issues by severity
   - Risk analysis
   - Impact assessment

4. **Recommendations**
   - Proposed changes
   - Implementation approach
   - Effort estimates
   - Priority rankings

5. **Architecture Decision Records**
   - Key decisions
   - Rationale
   - Consequences

**Report Location:** `output/{session}/architecture-review.md`
```

---

## Step-by-Step Tutorial

Let's create a complete command from scratch.

### Example: Create "docs.spell-check" Command

#### Step 1: Define Requirements

**Use Case:** Check documentation for spelling errors

**Frequency:** Multiple times per week

**Value:** Catches errors before commit, improves quality

**Pattern:** Multi-Phase (discovery + analysis + report)

---

#### Step 2: Create File

```bash
# Create file in correct location
touch commands/docs/docs.spell-check.md
```

---

#### Step 3: Add YAML Frontmatter

```yaml
---
name: docs.spell-check
description: Checks documentation files for spelling errors and typos
category: docs
pattern: multi-phase
version: 1.0.0
author: Your Name
tags: [documentation, quality, spelling]
estimated_time: 1-2 min
model_preference: sonnet
tools_required: [Glob, Read]
output_format: markdown
requires_input: false
requires_context: true
interactive: false
dangerous: false
related_commands: [docs.update-readme, docs.validate-links]
---
```

---

#### Step 4: Add Introduction

```markdown
# Spell Check Documentation

Automatically checks all documentation files for spelling errors, typos, and common mistakes.

This command scans markdown files throughout the repository, identifies potential spelling issues, and generates a comprehensive report with suggestions.
```

---

#### Step 5: Add Usage Section

```markdown
## Usage

```bash
# Check all documentation
/docs.spell-check

# Results saved to output/{session}/spell-check-report.md
```

**Arguments:** None (discovers files automatically)

**Requirements:**
- Must be run from repository root
- Scans all `.md` files except `node_modules/`
```

---

#### Step 6: Add Multi-Phase Structure

```markdown
## Multi-Phase Execution

### Phase 1: Discovery
**Goal:** Find all documentation files to check

**Steps:**
1. Use Glob to find all `.md` files
2. Exclude `node_modules/`, `.git/`, `output/`
3. Read file contents
4. Extract text from code blocks

**Tools Used:** Glob, Read

**Example:**
```bash
# Finds files like:
# - README.md
# - docs/**/*.md
# - commands/**/*.md
# - agents/**/*.md
# - skills/**/*.md
```

### Phase 2: Analysis
**Goal:** Identify spelling errors

**Steps:**
1. Tokenize text (separate words)
2. Check against common dictionary
3. Identify technical terms (known false positives)
4. Flag potential errors
5. Categorize by confidence (high/medium/low)

**Analysis Criteria:**
- Common misspellings
- Repeated words ("the the")
- Capitalization errors
- Technical term variations

**Known Technical Terms:**
- claude-skills
- frontmatter
- kebab-case
- pytest
- (add repository-specific terms)

### Phase 3: Reporting
**Goal:** Generate actionable report

**Report Includes:**
- Summary statistics
- Errors by file
- Error by category
- Suggestions for corrections
- False positive rate estimate

**Report Location:** `output/{session}/spell-check-report.md`
```

---

#### Step 7: Add Examples

```markdown
## Examples

### Basic Usage

```bash
/docs.spell-check
```

**Output:**
```
Scanning documentation files...
Found 127 markdown files

Checking spelling...
Found 8 potential issues

Report saved: output/2025-11-24_14-30-45/spell-check-report.md
```

### Report Format

```markdown
# Spell Check Report

**Date:** 2025-11-24 14:30:45
**Files Scanned:** 127
**Issues Found:** 8

## Summary

| Category | Count |
|----------|-------|
| Misspellings | 5 |
| Repeated Words | 2 |
| Capitalization | 1 |

## Issues by File

### docs/INSTALL.md

**Line 42:** "recieve" → "receive"
**Line 89:** "the the" → "the"

### README.md

**Line 15:** "acommodate" → "accommodate"
```
```

---

#### Step 8: Add Error Handling

```markdown
## Error Handling

### Common Issues

#### Issue: No markdown files found

**Cause:** Running from wrong directory or all `.md` files excluded

**Solution:**
```bash
# Ensure you're in repository root
cd /path/to/claude-skills
/docs.spell-check
```

#### Issue: Too many false positives

**Cause:** Technical terms flagged as errors

**Solution:** Update known technical terms list in command file

#### Issue: Performance is slow

**Cause:** Large number of files to scan

**Solution:** Command may take 1-2 minutes for large repositories
```

---

#### Step 9: Add Success Criteria

```markdown
## Success Criteria

This command is successful when:
- [x] All `.md` files are discovered
- [x] Spelling errors are identified
- [x] Report is generated in `output/{session}/`
- [x] False positive rate is < 20%
- [x] Execution time is < 3 minutes
```

---

#### Step 10: Add Related Commands

```markdown
## Related Commands

- [docs.update-readme](docs.update-readme.md) - Update README statistics
- [docs.validate-links](docs.validate-links.md) - Check for broken links
- [docs.generate-catalog](docs.generate-catalog.md) - Generate catalogs

## Related Agents

- [cs-technical-writer](../../agents/cs-technical-writer.md) - Expert technical writing
```

---

#### Step 11: Validate

```bash
# Validate command structure (when tool is available)
python3 scripts/command_builder.py --validate commands/docs/docs.spell-check.md
```

**Checks:**
- ✓ Name format correct
- ✓ YAML frontmatter valid
- ✓ Description length OK
- ✓ Pattern structure matches
- ✓ Category recognized
- ✓ Content complete
- ✓ Markdown valid
- ✓ Related commands exist

---

#### Step 12: Test

```bash
# Install command
python3 scripts/install_commands.py --command docs.spell-check

# Test it
cd /path/to/test-repo
/docs.spell-check

# Verify:
# - Command executes without errors
# - Report is generated
# - Output is accurate
# - Performance is acceptable
```

---

## Best Practices

### Command Design

**Single Responsibility**
- One command = one focused task
- Don't try to do too much
- Keep it simple and clear

**Clear Inputs/Outputs**
- Document what's required
- Specify output format and location
- Make success criteria measurable

**Idempotent Execution**
- Safe to run multiple times
- Same input = same output
- No unintended side effects

---

### Documentation Quality

**Write for Beginners**
- Assume no prior knowledge
- Define technical terms
- Provide context

**Provide Examples**
- Basic usage (simplest case)
- Common usage (typical scenario)
- Advanced usage (edge cases)
- Error cases

**Document Errors**
- Common issues
- Root causes
- Clear solutions
- Prevention tips

---

### Performance

**Execute Quickly**
- Target: < 5 minutes
- Show progress for long operations
- Allow cancellation
- Use haiku model for simple tasks

**Resource Efficient**
- Don't scan unnecessary files
- Cache when appropriate
- Limit memory usage
- Clean up temporary files

---

### Safety

**Dangerous Operations**
- Mark `dangerous: true` in frontmatter
- Ask for confirmation
- Provide dry-run mode
- Allow rollback if possible

**Error Handling**
- Validate inputs first
- Fail gracefully
- Provide clear error messages
- Log for debugging

---

## Validation

### 8 Validation Checks

All commands must pass:

1. **Name Format** - `category.command-name` pattern, kebab-case
2. **YAML Frontmatter** - Valid syntax, required fields present
3. **Description Length** - Max 150 characters, action-oriented
4. **Pattern Validity** - simple/multi-phase/agent-style
5. **Category Validity** - Recognized or valid custom category
6. **Content Completeness** - All required sections present
7. **Markdown Structure** - Valid syntax, proper hierarchy
8. **Integration References** - Related commands/agents/skills exist

### Running Validation

```bash
# Validate single command (when tool available)
python3 scripts/command_builder.py --validate commands/category/command-name.md

# Validate all commands
python3 scripts/command_builder.py --validate-all

# Validate just metadata
python3 scripts/command_builder.py --validate-metadata commands/category/command-name.md
```

---

## Publishing

### Contribution Workflow

```bash
# 1. Create feature branch
git checkout develop
git checkout -b feature/command-category-name

# 2. Create command
# (follow steps above)

# 3. Validate
python3 scripts/command_builder.py --validate commands/category/command-name.md

# 4. Test
python3 scripts/install_commands.py --command category.command-name
/category.command-name  # Test it works

# 5. Update catalog (manual for now)
# Add command to commands/CATALOG.md

# 6. Commit
git add commands/category/command-name.md
git add commands/CATALOG.md
git commit -m "feat(commands): add category.command-name command"

# 7. Push and create PR
git push origin feature/command-category-name
# Create PR to develop branch
```

---

### PR Checklist

Before submitting:

- [ ] Command validates successfully
- [ ] Command tested and works
- [ ] All sections complete
- [ ] Examples provided
- [ ] Error handling documented
- [ ] Related commands linked
- [ ] Catalog updated
- [ ] Conventional commit message
- [ ] Branch from develop
- [ ] PR description includes usage example

---

### Review Criteria

Reviewers will check:

- **Functionality** - Does it work as described?
- **Quality** - Is documentation clear and complete?
- **Standards** - Does it follow patterns and conventions?
- **Value** - Does it save time and improve quality?
- **Safety** - Are dangerous operations handled properly?

---

## Next Steps

### Start Creating

1. **Review existing commands** for patterns
2. **Copy template** from `templates/command-template.md`
3. **Follow this guide** step-by-step
4. **Validate and test** thoroughly
5. **Submit PR** to contribute

### Get Help

- **Documentation:** [commands/CLAUDE.md](../commands/CLAUDE.md)
- **Examples:** Browse `commands/` directory
- **Standards:** [docs/standards/](../docs/standards/)
- **Questions:** Open GitHub discussion

---

## Additional Resources

### Templates

- **[command-template.md](../templates/command-template.md)** - Base template
- **[command-config.yaml](../templates/command-config.yaml)** - Batch config (planned)

### Documentation

- **[commands/CLAUDE.md](../commands/CLAUDE.md)** - Development guide
- **[commands/CATALOG.md](../commands/CATALOG.md)** - All commands
- **[COMMANDS_INSTALLATION.md](COMMANDS_INSTALLATION.md)** - Installation guide

### Related Guides

- **[Agent Development](../agents/CLAUDE.md)** - Create agents
- **[Skill Development](../skills/marketing-team/CLAUDE.md)** - Create skills
- **[Standards](../docs/standards/)** - Quality standards

---

**Last Updated:** November 24, 2025
**Status:** Production guide
**Maintained By:** Claude Skills Team
