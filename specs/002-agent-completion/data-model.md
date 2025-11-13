# Data Model: Agent Structure Specification

**Date**: November 12, 2025
**Purpose**: Define the canonical agent structure for all 18 new agents

## Agent File Structure

### Complete Agent Template

```markdown
---
name: cs-agent-name
description: One-line description (under 150 characters)
skills: skill-folder-name
domain: marketing|product|engineering|delivery
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---

# Agent Name

## Purpose

[Paragraph 1: What this agent does and which skill it orchestrates]

[Paragraph 2: Target users, roles, and pain points]

[Paragraph 3: Value proposition and outcomes enabled]

## Skill Integration

**Skill Location:** `../../skills/domain-team/skill-name/`

### Python Tools

1. **Tool Name**
   - **Purpose:** One-sentence description
   - **Path:** `../../skills/domain-team/skill-name/scripts/tool_name.py`
   - **Usage:** `python ../../skills/domain-team/skill-name/scripts/tool_name.py [arguments]`
   - **Features:**
     - Feature 1
     - Feature 2
     - Feature 3
   - **Use Cases:** When to use this tool

2. **Second Tool** (if applicable)
   [Same structure as Tool 1]

### Knowledge Bases

1. **Reference Name**
   - **Location:** `../../skills/domain-team/skill-name/references/reference_file.md`
   - **Content:** What knowledge this file contains
   - **Use Case:** When to consult this reference

[Repeat for all references - typically 4-5 per skill]

### Templates

1. **Template Name** (if applicable)
   - **Location:** `../../skills/domain-team/skill-name/assets/template.md`
   - **Use Case:** When users would use this template

## Workflows

### Workflow 1: [Primary Use Case Name]

**Goal:** One-sentence description of what this accomplishes

**Steps:**
1. **[Action Step]** - Description
   ```bash
   # Command example if applicable
   ```
2. **[Action Step]** - Description
3. **[Action Step]** - Description
4. **[Action Step]** - Description
5. **[Action Step]** - Description

**Expected Output:** What success looks like

**Time Estimate:** Duration

**Example:**
```bash
# Complete workflow example
command1
command2
```

### Workflow 2: [Advanced Use Case Name]
[Same structure as Workflow 1]

### Workflow 3: [Integration Use Case Name]
[Same structure as Workflow 1]

### Workflow 4: [Automation/Batch Use Case Name]
[Same structure as Workflow 1]

## Integration Examples

### Example 1: [Example Name]

```bash
#!/bin/bash
# script-name.sh - Brief description

# Setup
INPUT_FILE=$1

# Execute workflow
python ../../skills/domain-team/skill-name/scripts/tool.py "$INPUT_FILE"

# Process output
echo "Complete"
```

### Example 2: [Example Name]
[Same structure as Example 1]

### Example 3: [Example Name]
[Same structure as Example 1]

## Success Metrics

**[Metric Category 1]:**
- **[Metric Name]:** Target value
- **[Metric Name]:** Target value
- **[Metric Name]:** Target value

**[Metric Category 2]:**
- **[Metric Name]:** Target value
- **[Metric Name]:** Target value

**[Metric Category 3]:**
- **[Metric Name]:** Target value
- **[Metric Name]:** Target value

## Related Agents

- [cs-related-agent](../domain/cs-related-agent.md) - Relationship description
- [cs-another-agent](cs-another-agent.md) - Relationship description

## References

- **Skill Documentation:** [../../skills/domain-team/skill-name/SKILL.md](../../skills/domain-team/skill-name/SKILL.md)
- **Domain Guide:** [../../skills/domain-team/CLAUDE.md](../../skills/domain-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)

---

**Last Updated:** [Date]
**Sprint:** [sprint-MM-DD-YYYY] (Day X)
**Status:** Production Ready
**Version:** 1.0
```

## YAML Frontmatter Schema

### Required Fields

```yaml
---
name: string                  # REQUIRED: cs-{agent-name} format, kebab-case
description: string           # REQUIRED: <150 characters, one-line purpose
skills: string                # REQUIRED: exact skill folder name (not path)
domain: enum                  # REQUIRED: marketing|product|engineering|delivery
model: enum                   # REQUIRED: sonnet|opus|haiku (use sonnet for production)
tools: array                  # REQUIRED: [Read, Write, Bash, Grep, Glob] (standard set)
---
```

### Field Specifications

**name:**
- Format: `cs-{agent-name}`
- Case: kebab-case (lowercase with hyphens)
- Prefix: Always `cs-` (claude-skills)
- Example: `cs-content-creator`, `cs-backend-engineer`, `cs-jira-expert`

**description:**
- Length: Under 150 characters (strict)
- Content: One-line summary of agent purpose
- Style: Active voice, specific outcome focus
- Example: "AI-powered content creation specialist for brand voice consistency, SEO optimization, and multi-platform content strategy"

**skills:**
- Value: Exact folder name from `skills/domain-team/{skill-name}/`
- Format: skill-folder-name (NOT full path)
- Example: `content-creator`, `senior-backend`, `jira-expert`
- Note: Do NOT include `skills/` or `domain-team/` in this field

**domain:**
- Values: `marketing`, `product`, `engineering`, `delivery`
- Match: Must match the domain where skill is located
- Example: If skill is in `skills/engineering-team/`, domain is `engineering`

**model:**
- Values: `sonnet`, `opus`, `haiku`
- Standard: Use `sonnet` for all production agents (100% consistency)
- When to vary: Only use `opus` for extremely complex reasoning, `haiku` for simple tasks

**tools:**
- Standard Set: `[Read, Write, Bash, Grep, Glob]`
- Format: YAML array
- Consistency: Use this exact set for all agents (100% consistency in existing agents)

### Domain Mapping

| Skill Location | Domain Value | Agent Location |
|----------------|--------------|----------------|
| `skills/marketing-team/` | `marketing` | `agents/marketing/` |
| `skills/product-team/` | `product` | `agents/product/` |
| `skills/engineering-team/` | `engineering` | `agents/engineering/` |
| `skills/delivery-team/` | `delivery` | `agents/delivery/` |

## Section Specifications

### Purpose Section (2-3 paragraphs)

**Paragraph 1: What**
- Agent's primary function
- Which skill package it orchestrates
- Core capabilities overview

**Paragraph 2: Who**
- Target users (roles, job titles)
- Pain points addressed
- Why they need this agent

**Paragraph 3: Value**
- Outcomes enabled
- Gap bridged
- Benefits delivered

**Length:** 150-250 words total

### Skill Integration Section

**Python Tools Subsection:**
- Document ALL Python tools from `skill/scripts/` directory
- Use 5-field format: Purpose, Path, Usage, Features, Use Cases
- Provide concrete usage examples with arguments
- Include output format information

**Knowledge Bases Subsection:**
- Document ALL references from `skill/references/` directory
- Use 3-field format: Location, Content, Use Case
- Summarize key frameworks/knowledge in each reference

**Templates Subsection:**
- Document ALL templates from `skill/assets/` directory
- Use 2-field format: Location, Use Case
- Explain when users would customize and use each template

### Workflows Section (Exactly 4 Workflows)

**Workflow Types:**
1. **Primary Use Case** - Most common scenario, single tool focus
2. **Advanced Use Case** - Complex scenario, multiple tool integration
3. **Integration Use Case** - Cross-functional workflow, tool orchestration
4. **Automation Use Case** - Scriptable, batch processing, ongoing automation

**Workflow Structure (5 required fields):**
- **Goal:** One-sentence outcome description
- **Steps:** 4-7 numbered steps with action verb + description
- **Expected Output:** Concrete deliverable or measurable result
- **Time Estimate:** Realistic duration (e.g., "2-3 hours", "30-45 minutes")
- **Example:** Code block with complete bash workflow

**Step Format:**
```markdown
1. **[Action Verb + Object]** - Clear description
   ```bash
   # Optional command example
   ```
```

### Integration Examples Section (3 examples)

**Example Types:**
1. **Daily/Weekly Automation** - Scheduled workflow script
2. **Multi-Tool Workflow** - Combining multiple tools sequentially
3. **Output Processing** - Parsing and acting on tool results

**Example Format:**
```bash
#!/bin/bash
# script-name.sh - Brief description

# Setup variables
INPUT=$1

# Execute workflow steps
step1_command
step2_command

# Output results
echo "Complete"
```

### Success Metrics Section (3-4 categories)

**Metric Categories by Domain:**

**Delivery:**
- Efficiency (time saved, velocity)
- Collaboration Quality (team satisfaction, communication clarity)
- Delivery Predictability (estimation accuracy, risk reduction)
- Team Satisfaction (ceremony effectiveness, impediment resolution)

**Engineering:**
- Code Quality (defect reduction, test coverage, review thoroughness)
- Development Velocity (deployment frequency, lead time)
- System Reliability (uptime, incident reduction, performance)
- Innovation Capacity (tech debt reduction, experimentation time)

**Marketing:**
- Content Quality (brand consistency, SEO score)
- Production Efficiency (time saved, output volume)
- Engagement Impact (reach, conversions, performance)

**Product:**
- Decision Quality (prioritization accuracy, validated assumptions)
- Strategy Alignment (roadmap clarity, stakeholder satisfaction)
- User Impact (satisfaction scores, feature adoption)

**Metric Format:**
```markdown
**[Category Name]:**
- **[Specific Metric]:** Target value or percentage improvement
- **[Specific Metric]:** Target value or percentage improvement
```

### Related Agents Section

**Cross-References:**
- List 2-4 related agents (same or different domains)
- Explain relationship (orchestrates, provides input to, complements)
- Use relative paths from agent location

**Path Patterns:**
- Same domain: `[cs-agent](cs-agent.md)`
- Different domain: `[cs-agent](../domain/cs-agent.md)`

**Relationship Types:**
- **Orchestrates:** Senior PM orchestrates Jira Expert, Scrum Master
- **Provides Input:** UX Researcher provides input to Frontend Engineer
- **Complements:** Backend Engineer complements Frontend Engineer
- **Strategic Context:** CTO Advisor provides strategic context for Architect

### References Section (Always 3 links)

**Required Links:**
1. Skill documentation (SKILL.md)
2. Domain guide (domain CLAUDE.md)
3. Agent development guide (agents/CLAUDE.md)

**Path Pattern from agent location:**
```markdown
- **Skill Documentation:** [../../skills/domain-team/skill-name/SKILL.md](../../skills/domain-team/skill-name/SKILL.md)
- **Domain Guide:** [../../skills/domain-team/CLAUDE.md](../../skills/domain-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)
```

## Path Resolution Patterns

### From Agent Location to Skill

**Pattern:** `../../skills/domain-team/skill-name/`

**Examples:**

**Marketing agents** (`agents/marketing/cs-agent.md`):
```
../../skills/marketing-team/content-creator/
../../skills/marketing-team/demand-gen-specialist/
../../skills/marketing-team/product-marketer/
```

**Product agents** (`agents/product/cs-agent.md`):
```
../../skills/product-team/product-manager/
../../skills/product-team/agile-product-owner/
../../skills/product-team/ux-researcher/
```

**Delivery agents** (`agents/delivery/cs-agent.md`):
```
../../skills/delivery-team/jira-expert/
../../skills/delivery-team/confluence-expert/
../../skills/delivery-team/scrum-master/
../../skills/delivery-team/senior-pm/
```

**Engineering agents** (`agents/engineering/cs-agent.md`):
```
../../skills/engineering-team/code-reviewer/
../../skills/engineering-team/senior-backend/
../../skills/engineering-team/senior-devops/
../../skills/engineering-team/cto-advisor/
```

### Path Components

**Python Tools:**
```
../../skills/domain-team/skill-name/scripts/tool_name.py
```

**Knowledge Bases:**
```
../../skills/domain-team/skill-name/references/reference_name.md
```

**Templates:**
```
../../skills/domain-team/skill-name/assets/template_name.md
```

**Skill Documentation:**
```
../../skills/domain-team/skill-name/SKILL.md
```

**Domain Guide:**
```
../../skills/domain-team/CLAUDE.md
```

**Agent Guide:**
```
../CLAUDE.md  (from agents/domain/ to agents/CLAUDE.md)
```

## Agent Naming Conventions

### Agent Filename Pattern

**Format:** `cs-{role}.md`

**Rules:**
- Always lowercase
- Use hyphens for spaces
- Match role name (not skill folder name necessarily)
- Keep concise (2-3 words max)

**Examples:**

**Delivery Team:**
- `cs-jira-expert.md` (skill: jira-expert)
- `cs-confluence-expert.md` (skill: confluence-expert)
- `cs-scrum-master.md` (skill: scrum-master)
- `cs-senior-pm.md` (skill: senior-pm)

**Engineering Team:**
- `cs-code-reviewer.md` (skill: code-reviewer)
- `cs-architect.md` (skill: senior-architect)
- `cs-backend-engineer.md` (skill: senior-backend)
- `cs-frontend-engineer.md` (skill: senior-frontend)
- `cs-fullstack-engineer.md` (skill: senior-fullstack)
- `cs-devops-engineer.md` (skill: senior-devops)
- `cs-security-engineer.md` (skill: senior-security)
- `cs-secops-engineer.md` (skill: senior-secops)
- `cs-qa-engineer.md` (skill: senior-qa)
- `cs-ml-engineer.md` (skill: senior-ml-engineer)
- `cs-data-engineer.md` (skill: senior-data-engineer)
- `cs-data-scientist.md` (skill: senior-data-scientist)
- `cs-computer-vision.md` (skill: senior-computer-vision)
- `cs-prompt-engineer.md` (skill: senior-prompt-engineer)
- `cs-cto-advisor.md` (skill: cto-advisor)

## Agent Display Name Pattern

**Format:** Title Case, remove "senior-" prefix if present

**Examples:**
- Filename: `cs-backend-engineer.md` → Display: "Backend Engineer Agent"
- Filename: `cs-jira-expert.md` → Display: "Jira Expert Agent"
- Filename: `cs-cto-advisor.md` → Display: "CTO Advisor Agent"

## Quality Standards

### Consistency Requirements (100% compliance)

1. **YAML Frontmatter:**
   - All 6 fields present
   - `model: sonnet` for production
   - `tools: [Read, Write, Bash, Grep, Glob]` (exact array)

2. **Workflows:**
   - Exactly 4 workflows
   - All 5 fields per workflow (Goal, Steps, Output, Time, Example)
   - 4-7 steps per workflow (average 6)

3. **Path Pattern:**
   - 100% relative paths using `../../skills/` pattern
   - No absolute paths
   - No hardcoded user directories

4. **Agent Length:**
   - 400-500 lines (based on existing agent analysis)
   - Comprehensive but concise

5. **Documentation Completeness:**
   - All Python tools documented (3 per skill, except CTO with 2)
   - All references documented (4-5 per skill average)
   - All templates documented (if skill has templates)

### Validation Checklist

Before marking agent as complete:

- [ ] YAML frontmatter has all 6 required fields
- [ ] `skills:` field matches skill folder name exactly
- [ ] `domain:` field matches skill location
- [ ] Purpose section is 2-3 paragraphs (150-250 words)
- [ ] All Python tools from skill documented
- [ ] All references from skill documented
- [ ] Exactly 4 workflows documented
- [ ] Each workflow has Goal/Steps/Output/Time/Example
- [ ] 3 integration examples provided
- [ ] Success metrics in 3-4 categories
- [ ] Related agents cross-referenced
- [ ] 3 reference links present and correct
- [ ] All paths use `../../skills/` pattern
- [ ] No absolute paths present
- [ ] Agent length 400-500 lines

---

**Last Updated:** November 12, 2025
**Purpose:** Canonical structure for all 18 new agents
**Based On:** Analysis of 8 existing production agents (100% consistency)
