---
name: cs-agent-name
description: One-line description of what this agent does (keep under 150 characters)
skills: skill-folder-name
domain: domain-name
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
color: blue
field: product
expertise: expert
execution: parallel
mcp_tools: []
---

<!--
  YAML FRONTMATTER FIELD GUIDE:

  REQUIRED FIELDS:
  - name: Agent identifier (kebab-case with cs- prefix, e.g., cs-content-creator)
  - description: One-line summary (max 150 chars)
  - skills: Folder name of skill package (e.g., content-creator)
  - domain: Domain category (marketing-team, product-team, engineering-team, delivery-team)
  - model: AI model (sonnet, haiku, opus)
  - tools: Array of required tools [Read, Write, Bash, Grep, Glob, WebSearch, etc.]

  ENHANCED FIELDS:

  color: Visual category for agent classification
    - blue: Strategic planning, analysis, decision-making (CEO, CTO, Product Manager)
    - green: Implementation, building, development (Frontend Dev, Fullstack Dev, AI Engineer)
    - red: Quality assurance, testing, review (QA Engineer, Code Reviewer)
    - purple: Coordination, orchestration, multi-agent workflows (Project Manager, Scrum Master)
    - orange: Domain-specific expertise (Content Creator, SEO Specialist, Data Scientist)

  field: Expertise area for specialized knowledge
    - quality: QA, testing, code review, validation
    - frontend: UI/UX, React, Vue, Angular, design systems
    - backend: APIs, databases, server-side logic, microservices
    - fullstack: End-to-end development, both frontend and backend
    - product: Product management, roadmaps, strategy, user research
    - architecture: System design, technical architecture, patterns
    - testing: Test automation, test strategy, QA processes
    - devops: CI/CD, infrastructure, deployment, monitoring
    - data: Data analysis, ETL, data pipelines, analytics
    - ai: Machine learning, AI/ML, model training, LLMs
    - security: Security audits, penetration testing, compliance
    - performance: Optimization, profiling, scaling, load testing
    - design: UI/UX design, design systems, accessibility
    - research: User research, market research, competitive analysis
    - content: Content creation, copywriting, SEO, brand voice
    - finance: Financial analysis, budgeting, forecasting, metrics
    - agile: Agile methodologies, scrum, sprint planning, ceremonies
    - tools: Specialized tools expertise (Jira, Confluence, etc.)

  expertise: Complexity level of operations
    - beginner: Simple, single-step tasks; basic workflows; minimal decision-making
    - intermediate: Moderate complexity; multi-step processes; some analysis required
    - expert: Complex operations; advanced analysis; strategic decision-making; multi-tool orchestration

  execution: Concurrent execution safety pattern
    - parallel: Safe to run 4-5 agents simultaneously; independent operations; no resource conflicts
    - coordinated: Safe for 2-3 agents; some shared resources; requires coordination
    - sequential: One agent only; critical operations; file locking; exclusive access needed

  mcp_tools: Optional MCP (Model Context Protocol) server tools
    - Examples: [mcp__github, mcp__playwright, mcp__context7, mcp__atlassian]
    - Leave empty [] if no MCP tools required
    - GitHub operations: mcp__github
    - Browser automation: mcp__playwright
    - Context management: mcp__context7
    - Atlassian/Jira: mcp__atlassian
    - Multiple tools: [mcp__github, mcp__playwright]

  EXAMPLES BY AGENT TYPE:

  Strategic Planning Agent:
    color: blue
    field: product
    expertise: expert
    execution: coordinated
    mcp_tools: []

  Implementation Agent:
    color: green
    field: fullstack
    expertise: intermediate
    execution: parallel
    mcp_tools: [mcp__github]

  Quality Assurance Agent:
    color: red
    field: quality
    expertise: intermediate
    execution: sequential
    mcp_tools: [mcp__playwright]

  Coordination Agent:
    color: purple
    field: product
    expertise: expert
    execution: coordinated
    mcp_tools: [mcp__atlassian]

  Domain Expert Agent:
    color: orange
    field: content
    expertise: intermediate
    execution: parallel
    mcp_tools: []
-->

# Agent Name

<!--
  INSTRUCTIONS FOR USING THIS TEMPLATE:

  1. Replace "cs-agent-name" with your agent's name (use kebab-case with cs- prefix)
  2. Replace "Agent Name" with the display name (Title Case)
  3. Fill in all sections below following the structure
  4. Configure YAML frontmatter fields (see guide above)
  5. Test all relative paths (../../) before committing
  6. Ensure minimum 3 workflows documented
  7. Provide concrete integration examples
  8. Define measurable success metrics

  EXAMPLES OF COMPLETED AGENTS:
  - agents/marketing/cs-content-creator.md
  - agents/marketing/cs-demand-gen-specialist.md
  - agents/c-level/cs-ceo-advisor.md
  - agents/c-level/cs-cto-advisor.md
  - agents/product/cs-product-manager.md
-->

## Purpose

<!--
  Write 2-3 paragraphs describing:
  - What this agent does
  - Who it's designed for (target users)
  - How it enables better decisions/outcomes
  - The specific gap it bridges

  Example structure:
  Paragraph 1: Agent's primary function and skill orchestration
  Paragraph 2: Target audience and their pain points
  Paragraph 3: Value proposition and outcome focus
-->

[Paragraph 1: Describe what this agent does and which skill package it orchestrates]

[Paragraph 2: Describe target users, their roles, and why they need this agent]

[Paragraph 3: Explain the gap this agent bridges and the outcomes it enables]

## Skill Integration

**Skill Location:** `../../domain-skill/skill-name/`

<!--
  Document how this agent integrates with the underlying skill package.
  Test all paths to ensure they resolve correctly from agents/domain/ directory.
-->

### Python Tools

<!--
  List all Python automation tools from the skill package.
  Minimum 1 tool, ideally 2-4 tools.

  For each tool, provide:
  - Clear purpose statement
  - Exact file path (relative from agent location)
  - Usage examples with arguments
  - Key features
  - Common use cases
-->

1. **Tool Name**
   - **Purpose:** What this tool does (one sentence)
   - **Path:** `../../domain-skill/skill-name/scripts/tool_name.py`
   - **Usage:** `python ../../domain-skill/skill-name/scripts/tool_name.py [arguments]`
   - **Features:** Key capabilities (bullet list)
   - **Use Cases:** When to use this tool

2. **Second Tool** (if applicable)
   - **Purpose:** What this tool does
   - **Path:** `../../domain-skill/skill-name/scripts/second_tool.py`
   - **Usage:** `python ../../domain-skill/skill-name/scripts/second_tool.py [arguments]`
   - **Features:** Key capabilities
   - **Use Cases:** When to use this tool

### Knowledge Bases

<!--
  List reference documentation from the skill package.
  These are markdown files with frameworks, best practices, templates.
-->

1. **Reference Name**
   - **Location:** `../../domain-skill/skill-name/references/reference_file.md`
   - **Content:** What knowledge this file contains
   - **Use Case:** When to consult this reference

2. **Second Reference** (if applicable)
   - **Location:** `../../domain-skill/skill-name/references/second_reference.md`
   - **Content:** What knowledge this file contains
   - **Use Case:** When to consult this reference

### Templates

<!--
  List user-facing templates from the skill package's assets/ folder.
  Optional section - only if skill has templates.
-->

1. **Template Name** (if applicable)
   - **Location:** `../../domain-skill/skill-name/assets/template.md`
   - **Use Case:** When users would copy and customize this template

## Workflows

<!--
  Document MINIMUM 3 workflows. Ideally 4 workflows.
  Each workflow must have: Goal, Steps, Expected Output, Time Estimate

  Workflow types to consider:
  - Primary use case (most common)
  - Advanced use case (complex scenario)
  - Integration use case (combining multiple tools)
  - Automated workflow (scripting/batching)
-->

### Workflow 1: [Primary Use Case Name]

**Goal:** One-sentence description of what this workflow accomplishes

**Steps:**
1. **[Action Step]** - Description of first step
   ```bash
   # Command example if applicable
   python ../../domain-skill/skill-name/scripts/tool.py input.txt
   ```
2. **[Action Step]** - Description of second step
3. **[Action Step]** - Description of third step
4. **[Action Step]** - Description of fourth step
5. **[Action Step]** - Description of final step

**Expected Output:** What success looks like (deliverable, metric, decision made)

**Time Estimate:** How long this workflow typically takes

**Example:**
```bash
# Complete workflow example with real commands
command1
command2
# Review output
```

### Workflow 2: [Advanced Use Case Name]

**Goal:** One-sentence description

**Steps:**
1. **[Action Step]** - Description
2. **[Action Step]** - Description
3. **[Action Step]** - Description
4. **[Action Step]** - Description

**Expected Output:** What success looks like

**Time Estimate:** Duration estimate

### Workflow 3: [Integration Use Case Name]

**Goal:** One-sentence description

**Steps:**
1. **[Action Step]** - Description
2. **[Action Step]** - Description
3. **[Action Step]** - Description

**Expected Output:** What success looks like

**Time Estimate:** Duration estimate

### Workflow 4: [Optional Fourth Workflow]

<!-- Delete this section if you only have 3 workflows -->

**Goal:** One-sentence description

**Steps:**
1. **[Action Step]** - Description
2. **[Action Step]** - Description

**Expected Output:** What success looks like

**Time Estimate:** Duration estimate

## Integration Examples

<!--
  Provide 2-3 concrete code examples showing real-world usage.
  These should be copy-paste ready bash scripts or commands.

  Example types:
  - Weekly/daily automation scripts
  - Multi-tool workflows
  - Output processing examples
  - Real-time monitoring
-->

### Example 1: [Example Name]

```bash
#!/bin/bash
# script-name.sh - Brief description

# Setup variables
INPUT_FILE=$1

# Execute workflow
python ../../domain-skill/skill-name/scripts/tool.py "$INPUT_FILE"

# Process output
echo "Analysis complete. Review results above."
```

### Example 2: [Example Name]

```bash
# Multi-step workflow example

# Step 1: Prepare data
echo "Step 1: Data preparation"

# Step 2: Run analysis
python ../../domain-skill/skill-name/scripts/tool.py input.csv

# Step 3: Generate report
echo "Report generation complete"
```

### Example 3: [Example Name]

```bash
# Automation example (e.g., weekly report, daily check)

DATE=$(date +%Y-%m-%d)
echo "📊 Report for $DATE"

# Execute tools
python ../../domain-skill/skill-name/scripts/tool.py current-data.csv > report-$DATE.txt
```

## Success Metrics

<!--
  Define how to measure this agent's effectiveness.
  Group metrics into logical categories (3-4 categories).
  Each metric should be specific and measurable.

  Categories might include:
  - Quality metrics
  - Efficiency metrics
  - Business impact metrics
  - User satisfaction metrics
-->

**[Metric Category 1]:**
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage

**[Metric Category 2]:**
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage

**[Metric Category 3]:**
- **[Metric Name]:** Target value or improvement percentage
- **[Metric Name]:** Target value or improvement percentage

**[Metric Category 4]** (optional):
- **[Metric Name]:** Target value or improvement percentage

## Related Agents

<!--
  Cross-reference other agents in the same domain or related domains.
  Use relative paths from agents/ directory.
  Explain how agents complement each other.
-->

- [cs-related-agent](../domain/cs-related-agent.md) - How this agent relates (e.g., "Provides strategic context for tactical execution")
- [cs-another-agent](cs-another-agent.md) - How this agent relates (same directory)
- [cs-future-agent](cs-future-agent.md) - Planned agent (mark as "planned")

## References

<!--
  Link to all related documentation.
  Always include these three links with correct relative paths.
-->

- **Skill Documentation:** [../../domain-skill/skill-name/SKILL.md](../../domain-skill/skill-name/SKILL.md)
- **Domain Guide:** [../../domain-skill/CLAUDE.md](../../domain-skill/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)

---

<!--
  Update metadata when publishing.
  Sprint format: sprint-MM-DD-YYYY
  Status: Production Ready, Beta, Alpha
-->

**Last Updated:** [Date]
**Sprint:** [sprint-MM-DD-YYYY] (Day X)
**Status:** Production Ready
**Version:** 1.0
