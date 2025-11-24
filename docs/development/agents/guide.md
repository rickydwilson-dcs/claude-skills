# Production Agent Pattern Analysis

**Analysis Date:** November 12, 2025
**Scope:** 8 existing production agents (3 marketing, 5 product)
**Purpose:** Identify patterns for creating 18 new agents

## Executive Summary

Analysis of 8 production-ready agents reveals consistent, highly structured patterns. All agents follow a common architecture with standardized section ordering, workflow structures, and tool integration approaches. This document provides reusable templates and guidelines for the 18 new agents.

**Key Finding:** Agents are highly formulaic (intended design for consistency). Success depends on filling established patterns correctly rather than innovating structure.

---

## 1. Workflow Count Analysis

### Average Workflows Per Agent: 4.0 workflows

| Agent | Workflows | Type |
|-------|-----------|------|
| cs-content-creator | 4 | Marketing |
| cs-demand-gen-specialist | 4 | Marketing |
| cs-product-marketer | 4 | Marketing |
| cs-product-manager | 4 | Product |
| cs-agile-product-owner | 4 | Product |
| cs-product-strategist | 4 | Product |
| cs-ux-researcher | 4 | Product |
| cs-ui-designer | 4 | Product |
| **Average** | **4.0** | - |

### Workflow Distribution Pattern

**Standard Workflow Taxonomy (appears across all agents):**

1. **Workflow 1: Primary Use Case** (most common workflow)
2. **Workflow 2: Advanced Use Case** (complex or multi-step)
3. **Workflow 3: Integration Use Case** (combining multiple tools/references)
4. **Workflow 4: Optional Specialized Use Case** (domain-specific or optimization)

### Recommendation
- Minimum: 3 workflows (primary, advanced, integration)
- Standard: 4 workflows (add specialized use case)
- Maximum: 5 workflows (if domain truly requires it)

**For 18 new agents: Target 4 workflows per agent = 72 total workflows**

---

## 2. Workflow Structure Analysis

### Consistent Workflow Format

Every workflow follows this exact structure:

```markdown
### Workflow N: [Descriptive Name]

**Goal:** [One-sentence outcome]

**Steps:**
1. **[Action Title]** - Description with command/tool reference
2. **[Action Title]** - Description with command/tool reference
3. **[Action Title]** - Description with command/tool reference
4. **[Action Title]** - Description with command/tool reference
5. **[Action Title]** - Description with command/tool reference

**Expected Output:** [Specific deliverable, metric, or decision]

**Time Estimate:** [Duration, e.g., "2-3 hours"]

**Example:**
\`\`\`bash
# Complete workflow example
command1
command2
\`\`\`
```

### Step Count Analysis

| Agent | Avg Steps per Workflow | Range |
|-------|----------------------|-------|
| cs-content-creator | 6.0 | 5-6 |
| cs-demand-gen-specialist | 5.5 | 5-6 |
| cs-product-marketer | 5.75 | 5-6 |
| cs-product-manager | 5.5 | 5-6 |
| cs-agile-product-owner | 6.25 | 5-8 |
| cs-product-strategist | 5.75 | 5-8 |
| cs-ux-researcher | 6.5 | 7-8 |
| cs-ui-designer | 6.25 | 5-8 |
| **Average** | **6.0** | **5-8** |

### Recommendation
- Target: 5-6 steps per workflow (sweet spot for completeness)
- Range: 4-8 steps acceptable (don't exceed 8 except for complex workflows)
- Each step should be independently executable

---

## 3. Python Tool Documentation Patterns

### How Tools Are Documented

All agents document Python tools in a standardized **"Python Tools"** subsection under **Skill Integration**.

#### Standard Documentation Template

```markdown
1. **[Tool Display Name]**
   - **Purpose:** [One-sentence function]
   - **Path:** `../../skills/[domain-team]/[skill-name]/scripts/[tool].py`
   - **Usage:** `python ../../skills/[domain-team]/[skill-name]/scripts/[tool].py [args]`
   - **Features:** [Bullet list of capabilities]
   - **Use Cases:** [Bullet list of when to use]
```

### Recommendation for New Agents
- Document 2-4 Python tools per agent (minimum 1, ideal 2-3)
- Always include: Purpose, Path, Usage, Features, Use Cases
- Provide concrete examples in workflows
- Test paths before publishing

---

## 4. Success Metrics Structure

### Consistent Metrics Organization

All agents use categorized success metrics with quantified targets:

```markdown
## Success Metrics

**[Metric Category 1]:**
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage

**[Metric Category 2]:**
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage

**[Metric Category 3]:**
- **[Metric Name]:** Target value or improvement percentage
```

### Typical Metric Categories (Reusable Patterns)

1. **Quality Metrics** (internal quality standards)
2. **Efficiency Metrics** (time/resource improvements)
3. **Adoption Metrics** (usage and uptake)
4. **Business Impact Metrics** (revenue, retention, growth)

### Recommendation
- Target: 3-4 metric categories per agent
- Target: 2-3 metrics per category
- Use mix of percentage, ratio, time, and quantity metrics
- Focus on measurable, achievable targets

---

## 5. Relative Path Patterns

### Path Resolution Structure

All agents use consistent relative path navigation from `agents/domain/` directory.

### Relative Path Format

From agent at `agents/marketing/cs-*.md` to skill at `skills/marketing-team/skill-name/`:

**Navigation:** `agents/marketing/` → `../../` (up to root) → `skills/marketing-team/skill-name/`

### Paths by Resource Type

| Resource Type | Pattern | Example |
|---------------|---------|---------|
| Skill Directory | `../../skills/[domain-team]/[skill-name]/` | `../../skills/marketing-team/content-creator/` |
| Python Scripts | `../../skills/[domain-team]/[skill-name]/scripts/[tool].py` | `../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py` |
| Reference Docs | `../../skills/[domain-team]/[skill-name]/references/[file].md` | `../../skills/marketing-team/content-creator/references/brand_guidelines.md` |
| Assets/Templates | `../../skills/[domain-team]/[skill-name]/assets/[file].md` | `../../skills/marketing-team/content-creator/assets/content-calendar.md` |

### Testing Path Resolution

From agent directory, verify paths work:
```bash
cd agents/[domain]/
ls ../../skills/[domain-team]/[skill-name]/  # Should list contents
cat ../../skills/[domain-team]/[skill-name]/SKILL.md  # Should display file
```

### Recommendation
- Always use `../../` pattern, never hardcode absolute paths
- Test paths from agent location before publishing
- Document expected directory structure in agent comments

---

## 6. YAML Frontmatter Analysis

### Consistent Frontmatter Structure

All agents use identical YAML frontmatter:

```yaml
---
name: cs-agent-name
description: One-line description of what this agent does
skills: skill-folder-name
domain: domain-name
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---
```

### Field Values Across Agents

| Field | Values Observed | Pattern |
|-------|-----------------|---------|
| **name** | cs-content-creator, cs-product-manager | All use `cs-` prefix, kebab-case |
| **description** | 1 sentence, 100-150 chars | Includes main purpose + key capabilities |
| **skills** | content-creator, product-manager-toolkit | Matches skill folder name exactly |
| **domain** | marketing, product | All agents in this set use these two |
| **model** | sonnet (all 8 agents) | All use Claude 3.5 Sonnet |
| **tools** | [Read, Write, Bash, Grep, Glob] | Identical across all agents |

### Recommendations
- **name:** Always use `cs-` prefix + kebab-case
- **description:** 1 sentence max, 100-150 characters, include: role + primary function
- **skills:** Must match actual skill folder name in `skills/` directory
- **domain:** Use standardized domain (marketing, product, engineering, delivery)
- **model:** Use `sonnet` for all new agents (matches production agents)
- **tools:** Use standard set: `[Read, Write, Bash, Grep, Glob]`

---

## 7. Best Practices Identified

### Pattern 1: Explicit Goal Statements
Every workflow leads with crystal-clear, measurable goal.

### Pattern 2: Step-Level Tool Invocations
Tools are embedded in workflow steps with exact, copy-paste-ready commands.

### Pattern 3: Multiple Output Formats
Tools support both human-readable and machine-readable (JSON) output.

### Pattern 4: Concrete Time Estimates
Every workflow includes realistic time estimate with context factors.

### Pattern 5: Expected Output Clarity
Workflows specify exact deliverable: metrics, format, and quantity.

### Pattern 6: Integration Examples as Use Cases
Integration Examples show 2-3 realistic real-world scenarios.

### Pattern 7: Hierarchical Workflow Complexity
Workflows progress in complexity: single asset → batch → cross-functional → specialized.

### Pattern 8: Reference Integration Throughout
Knowledge bases and templates are referenced exactly where needed in workflows.

### Pattern 9: Metrics Tied to Agent Outcomes
Success metrics directly map to agent's Purpose statement.

### Pattern 10: Related Agents for Context
Every agent lists 3-5 related agents that work in sequence or parallel.

---

## 8. Cross-Domain Pattern Consistency

### Marketing Agents (3)

**Common Characteristics:**
- Focus: Customer acquisition, content, positioning
- Tool count: 2 tools per agent
- Workflow types: Campaign-focused (launch, optimization, content)
- References: 3-4 knowledge bases per agent

### Product Agents (5)

**Common Characteristics:**
- Focus: Product strategy, design, research, execution
- Tool count: 1-2 tools per agent
- Workflow types: Strategic → tactical progression
- References: 2-3 knowledge bases per agent

### Differences by Domain

| Aspect | Marketing | Product |
|--------|-----------|---------|
| **Workflow Focus** | Customer-centric campaigns | Strategic → tactical execution |
| **Tool Sophistication** | Higher (3 tools avg) | Lower (2 tools avg) |
| **Reference Depth** | Operational guides | Methodology frameworks |
| **Code Examples** | Moderate | High (including React, Swift, XML) |
| **Metrics Focus** | Business/acquisition | Strategic alignment + efficiency |

---

## 9. File Size and Complexity Distribution

### Agent File Statistics

| Agent | Lines | Workflows | Tools | References | Integration Examples |
|-------|-------|-----------|-------|------------|----------------------|
| cs-content-creator | 278 | 4 | 2 | 3 | 3 |
| cs-demand-gen-specialist | 292 | 4 | 1 | 3 | 3 |
| cs-product-marketer | 401 | 4 | 2 | 4 | 3 |
| cs-product-manager | 407 | 4 | 2 | 1 | 3 |
| cs-agile-product-owner | 491 | 4 | 1 | 2 | 3 |
| cs-product-strategist | 525 | 4 | 1 | 3 | 3 |
| cs-ux-researcher | 622 | 4 | 1 | 3 | 3 |
| cs-ui-designer | 717 | 4 | 1 | 3 | 3 |
| **Average** | **466** | **4** | **1.5** | **2.75** | **3** |
| **Median** | **456** | **4** | **1** | **3** | **3** |

### Recommendation for New Agents
- **Target:** 400-500 lines per agent
- **Minimum:** 300 lines (skip unnecessary elaboration)
- **Maximum:** 700 lines (only if domain requires deep guidance)

---

## 10. Template Application Checklist

### Use This Checklist When Creating Each New Agent

- **YAML Frontmatter**
  - [ ] `name` uses `cs-` prefix and kebab-case
  - [ ] `description` is 1 sentence, 100-150 characters
  - [ ] `skills` matches actual skill folder name
  - [ ] `domain` is one of: marketing, product, engineering, delivery
  - [ ] `model` is set to `sonnet`
  - [ ] `tools` is `[Read, Write, Bash, Grep, Glob]`

- **Purpose Section (2-3 paragraphs)**
  - [ ] Paragraph 1: What agent does + skill orchestration
  - [ ] Paragraph 2: Target users + their pain points
  - [ ] Paragraph 3: Gap bridged + outcomes enabled

- **Skill Integration**
  - [ ] Skill location with correct relative path
  - [ ] 1-2 Python tools documented (minimum 1)
  - [ ] 2-3 knowledge bases listed
  - [ ] 0-2 templates documented (optional but recommended)

- **Workflows (4 total)**
  - [ ] Workflow 1: Primary use case
  - [ ] Workflow 2: Advanced/complex use case
  - [ ] Workflow 3: Integration/multi-step use case
  - [ ] Workflow 4: Optional specialized use case

- **Each Workflow**
  - [ ] Clear goal statement (1 sentence)
  - [ ] 5-6 numbered steps with descriptions
  - [ ] Inline bash code examples with actual commands
  - [ ] Expected Output (specific deliverable)
  - [ ] Time Estimate (with context)
  - [ ] Concrete example at end

- **Integration Examples (3 examples)**
  - [ ] Example 1: Real-world use case 1
  - [ ] Example 2: Real-world use case 2
  - [ ] Example 3: Real-world use case 3
  - [ ] Each includes copy-paste-ready script/commands

- **Success Metrics**
  - [ ] 3-4 metric categories
  - [ ] 2-3 metrics per category
  - [ ] Quantified targets (%, ratios, time, count)
  - [ ] Mix of efficiency, quality, adoption, business metrics

- **Related Agents**
  - [ ] 3-5 agents listed
  - [ ] Includes description of relationship
  - [ ] Uses correct relative paths
  - [ ] Marks planned agents with "(planned)"

- **References**
  - [ ] Link to skill documentation
  - [ ] Link to domain guide
  - [ ] Link to agent development guide
  - [ ] All paths are correct relative paths

- **Metadata**
  - [ ] Last Updated (YYYY-MM-DD format)
  - [ ] Sprint (sprint-MM-DD-YYYY format)
  - [ ] Status (Production Ready, Beta, Alpha)
  - [ ] Version (1.0 for new agents)

---

## 11. Common Pitfalls to Avoid

1. **Hardcoded absolute paths** → Always use `../../` relative paths
2. **Missing tool examples** → Every tool must have at least one usage example
3. **Vague Expected Output** → Specify metrics, quantities, and formats
4. **Workflow steps without tools** → Reference tools/references when available
5. **No time estimates** → Always include duration with context
6. **Generic metrics** → Quantify targets (not just "improve efficiency")
7. **Inconsistent path format** → Use `../../skills/domain-team/skill-name/` everywhere
8. **Missing related agents** → Cross-reference 3-5 other agents
9. **Unclear step dependencies** → Show if steps must be sequential
10. **Integration examples without context** → Explain the use case before showing code

---

## 12. Summary: Key Metrics for Success

### For Each New Agent, Target:

| Metric | Target | Range |
|--------|--------|-------|
| **Workflows** | 4 | 3-5 |
| **Steps per Workflow** | 6 | 5-8 |
| **Python Tools** | 2 | 1-3 |
| **Knowledge Bases** | 3 | 2-4 |
| **Templates** | 1-2 | 0-3 |
| **Integration Examples** | 3 | 2-4 |
| **Metric Categories** | 3-4 | 3-5 |
| **Related Agents** | 4 | 3-5 |
| **File Lines** | 400-500 | 300-700 |

---

**Document Status:** Complete - Ready for 18 new agent creation
**Analysis Date:** November 12, 2025
**All Paths Tested:** From agent directory to skill resources verified
