---
# YAML Frontmatter - Command Metadata
# This metadata is used for command discovery, categorization, and website display

# REQUIRED FIELDS
name: category.command-name           # Kebab-case, includes category prefix (e.g., git.code-review, docs.update)
description: Brief one-line description of what this command does (max 150 characters)
category: category-name                # Command category (code, docs, git, test, deploy, workflow, etc.)
pattern: simple                        # Command pattern: simple, multi-phase, or agent-style (see below)

# OPTIONAL FIELDS
version: 1.0.0                        # Semantic version (X.Y.Z)
author: Your Name                     # Command author
tags: [tag1, tag2, tag3]             # Searchable keywords for discovery
example_usage: /command-name arg1 arg2  # Quick usage example
requires_input: false                 # Does command need user to provide files/data?
requires_context: false               # Does command need specific project context?
estimated_time: 30s                   # Typical execution time (e.g., 30s, 2m, 5m)
related_commands: [other-command, another-command]  # Related slash commands
related_agents: [cs-agent-name]       # Related agents that might use this command
related_skills: [skill-name]          # Related skills this command leverages

# ADVANCED FIELDS
model_preference: sonnet              # Preferred model: sonnet (default), opus, haiku
tools_required: [Read, Write, Bash]   # Claude Code tools needed
output_format: markdown               # Expected output format: markdown, json, text, file
interactive: false                    # Does command prompt user for input during execution?
dangerous: false                      # Does command modify files or run potentially destructive operations?
---

<!--
═══════════════════════════════════════════════════════════════════════════════
  COMMAND TEMPLATE GUIDE
═══════════════════════════════════════════════════════════════════════════════

This template supports Anthropic's 3 official command patterns:

1. SIMPLE (Context → Task)
   - For straightforward, single-purpose tasks
   - Direct execution with minimal analysis
   - Examples: /update-docs, /format-code, /generate-changelog

2. MULTI-PHASE (Discovery → Analysis → Task)
   - For complex analysis requiring multiple steps
   - Systematic exploration before execution
   - Examples: /code-review, /security-audit, /performance-analysis

3. AGENT-STYLE (Role → Process → Guidelines)
   - For specialized expertise requiring specific perspective
   - Mimics domain expert behavior
   - Examples: /architect-design, /ux-review, /technical-writing

Choose the pattern that matches your command's complexity and purpose.

═══════════════════════════════════════════════════════════════════════════════
  NAMING CONVENTIONS
═══════════════════════════════════════════════════════════════════════════════

Command names MUST follow these rules:
- Kebab-case (lowercase with hyphens)
- Include category prefix: category.command-name
- Descriptive and action-oriented
- Max 40 characters

VALID EXAMPLES:
✓ git.code-review
✓ docs.update-readme
✓ test.run-suite
✓ deploy.staging
✓ workflow.create-pr

INVALID EXAMPLES:
✗ CodeReview (not kebab-case)
✗ code_review (underscore instead of hyphen)
✗ review (missing category prefix)
✗ git-code-review (use dot, not hyphen, for category separator)

═══════════════════════════════════════════════════════════════════════════════
-->

# Command Name

Brief 1-2 sentence description of what this command does and when to use it.

---

## Pattern Type: [Simple | Multi-Phase | Agent-Style]

**Complexity:** [Low | Medium | High]
**Execution Time:** [Estimated duration]
**Destructive:** [Yes | No]

---

<!--
═══════════════════════════════════════════════════════════════════════════════
  PATTERN 1: SIMPLE (Context → Task)
═══════════════════════════════════════════════════════════════════════════════

Use this pattern for straightforward tasks with clear inputs and outputs.

Structure:
1. Gather context (read files, check state)
2. Execute task (perform action)
3. Report results

Example commands: /update-docs, /format-code, /generate-changelog
-->

## Usage

```bash
/command-name [required-arg] [optional-arg]
```

### Arguments

- `required-arg` - Description of what this argument does (required)
- `optional-arg` - Description of optional argument (optional, default: value)

### Examples

```bash
# Basic usage
/command-name input.txt

# With optional arguments
/command-name input.txt --format json

# Multiple inputs
/command-name file1.txt file2.txt --merge
```

---

## What This Command Does

### Context Gathering

The command will:
1. Read and analyze [specific files/directories]
2. Check [specific conditions/state]
3. Validate [specific requirements]

### Task Execution

Then it will:
1. [First action with specific details]
2. [Second action with specific details]
3. [Third action with specific details]

### Expected Output

You will receive:
- [Output item 1]
- [Output item 2]
- [Output item 3]

**Output Location:** [Where results are saved, if applicable]
**Output Format:** [markdown | json | text | files]

---

<!--
═══════════════════════════════════════════════════════════════════════════════
  PATTERN 2: MULTI-PHASE (Discovery → Analysis → Task)
═══════════════════════════════════════════════════════════════════════════════

Use this pattern for complex analysis requiring systematic exploration.

Structure:
1. Discovery Phase - Explore codebase, gather information
2. Analysis Phase - Process findings, identify patterns
3. Task Phase - Execute actions based on analysis
4. Report Phase - Present findings and recommendations

Example commands: /code-review, /security-audit, /performance-analysis
-->

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Gather comprehensive information about [target area]

**Steps:**
1. Scan [directories/files] for [specific patterns]
2. Identify [key elements] using [tools/methods]
3. Catalog [findings] for analysis

**Tools Used:** [Grep, Glob, Read, etc.]

### Phase 2: Analysis

**Goal:** Process findings and identify [issues/patterns/opportunities]

**Steps:**
1. Analyze [gathered data] for [specific criteria]
2. Compare findings against [standards/best practices]
3. Categorize issues by [severity/type/impact]
4. Calculate [metrics/scores] based on [criteria]

**Analysis Criteria:**
- [Criterion 1] - What we're checking and why
- [Criterion 2] - What we're checking and why
- [Criterion 3] - What we're checking and why

### Phase 3: Task Execution

**Goal:** Take action based on analysis

**Steps:**
1. [Action 1] for issues categorized as [category]
2. [Action 2] for issues categorized as [category]
3. [Action 3] for issues categorized as [category]

**Actions:**
- **Automated Fixes:** [What gets fixed automatically]
- **Manual Review:** [What requires human decision]
- **Documentation:** [What gets documented]

### Phase 4: Reporting

**Goal:** Present findings and recommendations

**Report Includes:**
- Summary of findings
- Detailed issue list with severity
- Recommendations for improvement
- Metrics and statistics
- Next steps

**Report Location:** [Where report is saved]

---

<!--
═══════════════════════════════════════════════════════════════════════════════
  PATTERN 3: AGENT-STYLE (Role → Process → Guidelines)
═══════════════════════════════════════════════════════════════════════════════

Use this pattern for specialized expertise requiring domain-specific perspective.

Structure:
1. Role Definition - Establish expert persona
2. Process - Systematic expert workflow
3. Guidelines - Domain-specific rules and best practices
4. Deliverables - Expert-quality outputs

Example commands: /architect-design, /ux-review, /technical-writing
-->

## Agent Role

You are a [domain expert title] with [X] years of experience in [domain area].

**Expertise Areas:**
- [Expertise area 1]
- [Expertise area 2]
- [Expertise area 3]

**Perspective:** [How this expert approaches problems]

**Standards:** [What quality standards this expert upholds]

---

## Expert Process

### Step 1: Understanding Requirements

**Goal:** Deeply understand [what needs to be accomplished]

**Expert Approach:**
1. Review [relevant documentation/code/designs]
2. Identify [key requirements/constraints]
3. Ask clarifying questions about [specific aspects]
4. Establish success criteria

**Questions to Consider:**
- [Question 1 this expert would ask]
- [Question 2 this expert would ask]
- [Question 3 this expert would ask]

### Step 2: Analysis & Planning

**Goal:** Apply expert knowledge to plan solution

**Expert Approach:**
1. Evaluate [multiple approaches] against [criteria]
2. Consider [domain-specific factors]
3. Identify [risks and tradeoffs]
4. Select optimal approach based on [reasoning]

**Evaluation Criteria:**
- [Criterion 1] - Why it matters to this expert
- [Criterion 2] - Why it matters to this expert
- [Criterion 3] - Why it matters to this expert

### Step 3: Expert Execution

**Goal:** Implement solution with expert quality

**Expert Approach:**
1. Follow [domain-specific methodology]
2. Apply [best practices] for [specific aspects]
3. Ensure [quality standards] are met
4. Document [decisions and rationale]

**Quality Standards:**
- [Standard 1] - Specific measurable criterion
- [Standard 2] - Specific measurable criterion
- [Standard 3] - Specific measurable criterion

### Step 4: Expert Review

**Goal:** Validate work meets expert standards

**Expert Approach:**
1. Review output against [quality checklist]
2. Verify [domain-specific requirements]
3. Identify areas for improvement
4. Provide expert recommendations

**Review Checklist:**
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

---

## Expert Guidelines

### Domain-Specific Best Practices

1. **[Practice Area 1]**
   - Guideline: [Specific rule or principle]
   - Rationale: [Why experts follow this]
   - Example: [Concrete example]

2. **[Practice Area 2]**
   - Guideline: [Specific rule or principle]
   - Rationale: [Why experts follow this]
   - Example: [Concrete example]

3. **[Practice Area 3]**
   - Guideline: [Specific rule or principle]
   - Rationale: [Why experts follow this]
   - Example: [Concrete example]

### Anti-Patterns to Avoid

- **[Anti-pattern 1]** - Why experts avoid this and what to do instead
- **[Anti-pattern 2]** - Why experts avoid this and what to do instead
- **[Anti-pattern 3]** - Why experts avoid this and what to do instead

### Decision Framework

When [making specific type of decision], experts consider:

1. **[Factor 1]** - How to evaluate this factor
2. **[Factor 2]** - How to evaluate this factor
3. **[Factor 3]** - How to evaluate this factor

**Decision Matrix:** [How to weigh these factors]

---

## Deliverables

This command produces expert-quality outputs:

### Primary Deliverable

**Format:** [Document type/file format]
**Location:** [Where it's saved]
**Contains:**
- [Section 1 with description]
- [Section 2 with description]
- [Section 3 with description]

### Supporting Deliverables

1. **[Supporting item 1]**
   - Purpose: [Why this is included]
   - Format: [File format]
   - Use: [How to use this]

2. **[Supporting item 2]**
   - Purpose: [Why this is included]
   - Format: [File format]
   - Use: [How to use this]

### Quality Assurance

All deliverables are verified against:
- [ ] [Quality check 1]
- [ ] [Quality check 2]
- [ ] [Quality check 3]

---

## Error Handling

### Common Issues

**Issue:** [Description of common problem]
**Cause:** [Why this happens]
**Solution:** [How to fix it]
**Prevention:** [How to avoid it]

---

**Issue:** [Description of common problem]
**Cause:** [Why this happens]
**Solution:** [How to fix it]
**Prevention:** [How to avoid it]

---

**Issue:** [Description of common problem]
**Cause:** [Why this happens]
**Solution:** [How to fix it]
**Prevention:** [How to avoid it]

---

### Validation Failures

If the command reports validation errors:

1. **[Error type 1]**
   - Check: [What to verify]
   - Fix: [How to resolve]

2. **[Error type 2]**
   - Check: [What to verify]
   - Fix: [How to resolve]

3. **[Error type 3]**
   - Check: [What to verify]
   - Fix: [How to resolve]

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-agent-name](../agents/domain/cs-agent-name.md)** - [How they integrate]
- **[cs-agent-name](../agents/domain/cs-agent-name.md)** - [How they integrate]

### Related Skills

This command leverages:

- **[skill-name](../skills/domain-team/skill-name/)** - [What it uses from this skill]
- **[skill-name](../skills/domain-team/skill-name/)** - [What it uses from this skill]

### Python Tools

This command may execute:

```bash
# Tool 1
python skills/domain-team/skill-name/scripts/tool1.py [args]

# Tool 2
python skills/domain-team/skill-name/scripts/tool2.py [args]
```

---

## Success Criteria

This command is successful when:

- [ ] [Success criterion 1 - specific and measurable]
- [ ] [Success criterion 2 - specific and measurable]
- [ ] [Success criterion 3 - specific and measurable]
- [ ] [Success criterion 4 - specific and measurable]

### Quality Metrics

**Expected Outcomes:**
- [Metric 1]: [Target value or range]
- [Metric 2]: [Target value or range]
- [Metric 3]: [Target value or range]

---

## Tips for Best Results

1. **[Tip category 1]**
   - [Specific actionable tip]
   - [Why this helps]

2. **[Tip category 2]**
   - [Specific actionable tip]
   - [Why this helps]

3. **[Tip category 3]**
   - [Specific actionable tip]
   - [Why this helps]

---

## Related Commands

- `/related-command-1` - [How it relates]
- `/related-command-2` - [How it relates]
- `/related-command-3` - [How it relates]

---

## References

- [Documentation 1](link) - Description
- [Documentation 2](link) - Description
- [Best Practices Guide](link) - Description

---

**Last Updated:** YYYY-MM-DD
**Version:** X.Y.Z
**Maintained By:** [Team/Person]
**Feedback:** [How to provide feedback or report issues]
