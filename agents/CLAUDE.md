# Agent Development Guide

This guide provides comprehensive instructions for creating **cs-* prefixed agents** that seamlessly integrate with the 42 production skills in this repository.

## Agent Architecture

### What are cs-* Agents?

**cs-* agents** are specialized Claude Code agents that orchestrate the 42 existing skills. Each agent:
- References skills via relative paths (`../../skills/marketing-team/`)
- Executes Python automation tools from skill packages
- Follows established workflows and templates
- Maintains skill portability and independence

**Key Principle**: Agents ORCHESTRATE skills, they don't replace them. Skills remain self-contained and portable.

### Production Agents

**36 Agents Currently Available** (as of December 16, 2025):

| Agent | Domain | Description | Skills Used | Lines |
|-------|--------|-------------|-------------|-------|
| **Marketing (3 agents)** |||||
| [cs-content-creator](marketing/cs-content-creator.md) | Marketing | AI-powered content creation with brand voice consistency and SEO optimization | content-creator | 327 |
| [cs-demand-gen-specialist](marketing/cs-demand-gen-specialist.md) | Marketing | Demand generation and customer acquisition specialist | marketing-demand-acquisition | 289 |
| [cs-product-marketer](marketing/cs-product-marketer.md) | Marketing | Product positioning, GTM strategy, and competitive analysis | marketing-strategy-pmm | 401 |
| **C-Level (2 agents)** |||||
| [cs-ceo-advisor](c-level/cs-ceo-advisor.md) | C-Level | Strategic leadership advisor for CEOs covering vision, strategy, board management | ceo-advisor | 360 |
| [cs-cto-advisor](c-level/cs-cto-advisor.md) | C-Level | Technical leadership advisor for CTOs covering tech strategy and team scaling | cto-advisor | 412 |
| **Product (5 agents)** |||||
| [cs-product-manager](product/cs-product-manager.md) | Product | Product management agent for RICE prioritization and customer discovery | product-manager-toolkit | 407 |
| [cs-agile-product-owner](product/cs-agile-product-owner.md) | Product | User story creation, backlog grooming, sprint planning | agile-product-owner | 490 |
| [cs-product-strategist](product/cs-product-strategist.md) | Product | OKR cascades, strategic roadmaps, vision-driven prioritization | product-strategist | 524 |
| [cs-ux-researcher](product/cs-ux-researcher.md) | Product | Persona development, usability testing, customer interview analysis | ux-researcher-designer | 621 |
| [cs-ui-designer](product/cs-ui-designer.md) | Product | Design tokens, component libraries, design system documentation | ui-design-system | 716 |
| **Project Management (4 agents)** |||||
| [cs-senior-pm](project-management/cs-senior-pm.md) | Project Management | Portfolio planning, stakeholder management, program governance | senior-pm | 546 |
| [cs-scrum-master](project-management/cs-scrum-master.md) | Project Management | Sprint ceremonies, team facilitation, Agile coaching | scrum-master | 588 |
| [cs-jira-expert](project-management/cs-jira-expert.md) | Project Management | JQL queries, workflow configuration, automation rules | jira-expert | 710 |
| [cs-confluence-expert](project-management/cs-confluence-expert.md) | Project Management | Space architecture, template creation, documentation governance | confluence-expert | 788 |
| **Engineering (14 agents)** |||||
| [cs-backend-engineer](engineering/cs-backend-engineer.md) | Engineering | API development, database optimization, microservices architecture | senior-backend | 745 |
| [cs-frontend-engineer](engineering/cs-frontend-engineer.md) | Engineering | React/Vue development, UI/UX implementation, frontend performance | senior-frontend | 982 |
| [cs-fullstack-engineer](engineering/cs-fullstack-engineer.md) | Engineering | End-to-end development, API integration, full-stack architecture | senior-fullstack | 1,191 |
| [cs-devops-engineer](engineering/cs-devops-engineer.md) | Engineering | CI/CD pipelines, infrastructure as code, container orchestration | senior-devops | 799 |
| [cs-architect](engineering/cs-architect.md) | Engineering | System design, architecture patterns, scalability planning | senior-architect | 869 |
| [cs-security-engineer](engineering/cs-security-engineer.md) | Engineering | Security audits, vulnerability assessment, secure coding | senior-security | 1,094 |
| [cs-secops-engineer](engineering/cs-secops-engineer.md) | Engineering | Security operations, incident response, threat detection | senior-secops | 365 |
| [cs-qa-engineer](engineering/cs-qa-engineer.md) | Engineering | Test automation, quality assurance, test strategy | senior-qa | 383 |
| [cs-code-reviewer](engineering/cs-code-reviewer.md) | Engineering | Code review, quality assessment, refactoring guidance | code-reviewer | 427 |
| [cs-ml-engineer](engineering/cs-ml-engineer.md) | Engineering | Model training, MLOps pipelines, experiment tracking, model deployment | senior-ml-engineer | 1,059 |
| [cs-data-engineer](engineering/cs-data-engineer.md) | Engineering | ETL/ELT pipelines, data warehousing, data quality, scalable data infrastructure | senior-data-engineer | 1,305 |
| [cs-data-scientist](engineering/cs-data-scientist.md) | Engineering | Statistical analysis, exploratory data analysis, feature engineering, model evaluation | senior-data-scientist | 1,368 |
| [cs-computer-vision-engineer](engineering/cs-computer-vision-engineer.md) | Engineering | Image classification, object detection, semantic segmentation, computer vision pipelines | senior-computer-vision | 1,183 |
| [cs-prompt-engineer](engineering/cs-prompt-engineer.md) | Engineering | Prompt design, LLM optimization, RAG systems, multi-agent orchestration | senior-prompt-engineer | 1,381 |

**Total**: 20,330 lines of comprehensive agent documentation

**Template Available**: [templates/agent-template.md](../templates/agent-template.md) (318 lines) - Use this to create new agents

## Agent Type Classification System

Agents are classified into four distinct types based on their operational characteristics, resource usage, and execution patterns:

| Type | Color | Tools | Execution | Process Count | Model | Examples |
|------|-------|-------|-----------|---------------|-------|----------|
| **Strategic** | 🔵 Blue | Read, Write, Grep | Parallel (4-5) | 15-20 | opus/sonnet | cs-product-strategist, cs-ceo-advisor, cs-ux-researcher |
| **Implementation** | 🟢 Green | Full tools | Coordinated (2-3) | 20-30 | sonnet | cs-fullstack, cs-backend-engineer, cs-frontend-engineer |
| **Quality** | 🔴 Red | Full + Heavy Bash | Sequential (1) | 12-18 | sonnet | cs-code-reviewer, cs-qa-engineer, cs-security-engineer |
| **Coordination** | 🟣 Purple | Read, Write, Grep | Lightweight | 10-15 | opus | cs-architect, cs-team-coordinator, cs-cto-advisor |

### Agent Type Details

#### Strategic Agents (Blue)
- **Purpose:** Planning, research, analysis, and strategic decision-making
- **Characteristics:** Read-heavy operations, no code execution, document generation
- **Resource Usage:** Low CPU, moderate memory, minimal I/O
- **Concurrency:** Safe to run 4-5 agents in parallel
- **Examples:** Product strategy, market analysis, UX research, business planning
- **Tools:** Primarily Read, Write, and Grep for knowledge extraction

#### Implementation Agents (Green)
- **Purpose:** Active code development, feature building, system implementation
- **Characteristics:** Full tool access, code generation, file modifications
- **Resource Usage:** Moderate CPU, high memory, high I/O
- **Concurrency:** Run 2-3 agents with coordination to avoid conflicts
- **Examples:** Frontend/backend development, API creation, database work
- **Tools:** Full toolset including Bash for builds and execution

#### Quality Agents (Red)
- **Purpose:** Testing, validation, code review, security scanning
- **Characteristics:** Heavy Bash operations, test runners, linting, scanning
- **Resource Usage:** High CPU, high memory, intensive I/O operations
- **Concurrency:** MUST run sequentially (1 at a time) to avoid resource contention
- **Examples:** Automated testing, security audits, performance profiling
- **Tools:** Full tools with extensive Bash for test execution

#### Coordination Agents (Purple)
- **Purpose:** Orchestrate other agents, manage workflows, delegate tasks
- **Characteristics:** Lightweight operations, workflow coordination, delegation
- **Resource Usage:** Low across all metrics
- **Concurrency:** Can run alongside other agents as they delegate work
- **Examples:** Architecture planning, team coordination, workflow management
- **Tools:** Limited toolset focused on reading and coordination

## Execution Safety Rules

### ✅ SAFE - Parallel Execution

**Strategic Agents in Parallel (4-5 agents max):**
```bash
# Safe to run together - low resource usage
cs-product-strategist &
cs-ux-researcher &
cs-ceo-advisor &
cs-product-marketer &
wait
```

**Why it's safe:** Strategic agents primarily read and analyze, with minimal resource contention.

### ✅ SAFE - Coordinated Execution

**Implementation Agents with Coordination (2-3 agents):**
```bash
# Frontend and backend development with coordination
cs-frontend-engineer --component user-dashboard &
cs-backend-engineer --api user-endpoints &
wait

# Ensure no file conflicts before continuing
cs-fullstack --integrate
```

**Why it's safe:** Limited concurrency with explicit coordination prevents file conflicts.

### ❌ UNSAFE - Never Do This

**Quality Agents in Parallel - SYSTEM CRASH RISK:**
```bash
# DANGEROUS - Will cause system overload
cs-qa-engineer --full-suite &
cs-code-reviewer --deep-analysis &
cs-security-engineer --full-scan &
# DON'T DO THIS - System will become unresponsive
```

**Why it's dangerous:** Quality agents spawn multiple sub-processes (test runners, linters, scanners) that quickly exhaust system resources.

### Process Count Monitoring

Monitor system load with this command:
```bash
ps aux | grep -E "mcp|npm|claude|python|node" | wc -l
```

**Safe Operating Ranges:**

| State | Process Count | Status | Action |
|-------|--------------|--------|--------|
| Idle | 6-10 | ✅ Normal | Ready for work |
| Strategic (4-5 agents) | 15-20 | ✅ Safe | Operating normally |
| Implementation (2-3 agents) | 20-30 | ✅ Safe | Monitor closely |
| Quality (1 agent) | 12-18 | ✅ Safe | Single agent only |
| Warning Zone | 30-40 | ⚠️ Warning | Complete current, avoid new |
| High Load | 40-60 | ⚠️ High | Stop non-critical agents |
| Critical | >60 | 🚫 Critical | Restart required |

**Emergency Recovery:**
```bash
# If system becomes unresponsive
killall -9 node python npm
# Restart Claude Code
```

## Model Selection by Agent Type

Choose the appropriate Claude model based on agent type and task complexity:

### Opus 4.5 (Recommended Default)
**When to use:** All tasks - same price as Sonnet but faster and better quality
- **Strengths:** Superior reasoning, faster execution, excellent code generation, nuanced understanding
- **Best for:** All agent tasks - strategic planning, code development, testing, review, general-purpose
- **Examples:**
  - All agents now default to `model: opus`
  - `cs-architect` - System design and patterns
  - `cs-fullstack-engineer` - Full application development
  - `cs-code-reviewer` - Code quality assessment

### Sonnet (Legacy Option)
**When to use:** Still valid, but Opus 4.5 is now preferred at same price point
- **Strengths:** Excellent code generation, reliable output
- **Best for:** If you need to specify Sonnet explicitly for compatibility
- **Note:** All agents have been updated to use Opus by default

### Haiku (Fast, Simple Tasks)
**When to use:** Simple, repetitive, or time-sensitive tasks where speed > depth
- **Strengths:** Very fast response, low resource usage, cost-effective
- **Best for:** Simple automation, data formatting, quick checks, commit messages
- **Examples:**
  - Simple git operations (branch cleanup, commit messages)
  - Quick status checks
  - Template-based documentation generation

## MCP Integration Patterns

Modern agents can leverage MCP (Model Context Protocol) servers for enhanced capabilities:

### Common MCP Servers

#### mcp__github
- **Purpose:** GitHub integration for PRs, issues, and code review
- **Use with:** `cs-code-reviewer`, `cs-qa-engineer`
- **Example:**
```bash
# Review PR with GitHub MCP
cs-code-reviewer --mcp github --pr 123
```

#### mcp__playwright
- **Purpose:** Browser automation, E2E testing, visual regression
- **Use with:** `cs-qa-engineer`, `cs-frontend-engineer`
- **Example:**
```bash
# Run E2E tests with screenshots
cs-qa-engineer --mcp playwright --test-suite e2e
```

#### mcp__context7
- **Purpose:** Documentation search and knowledge extraction
- **Use with:** `cs-tech-writer`, `cs-architect`
- **Example:**
```bash
# Search documentation
cs-tech-writer --mcp context7 --query "API patterns"
```

#### mcp__atlassian
- **Purpose:** Jira and Confluence integration
- **Use with:** `cs-jira-expert`, `cs-confluence-expert`, `cs-scrum-master`
- **Example:**
```bash
# Update Jira tickets
cs-jira-expert --mcp atlassian --update-sprint
```

### MCP Best Practices

1. **Check MCP availability:** Not all environments have MCP servers
2. **Graceful fallback:** Agents should work without MCP when unavailable
3. **Resource awareness:** MCP servers add to process count
4. **Security:** MCP servers may require authentication tokens

### Agent vs Skill

| Aspect | Agent (cs-*) | Skill |
|--------|-------------|-------|
| **Purpose** | Orchestrate and execute workflows | Provide tools, knowledge, templates |
| **Location** | `agents/domain/` | `domain-skill/skill-name/` |
| **Structure** | Single .md file with YAML frontmatter | SKILL.md + scripts/ + references/ + assets/ |
| **Integration** | References skills via `../../` | Self-contained, no dependencies |
| **Naming** | cs-content-creator, cs-ceo-advisor | content-creator, ceo-advisor |

## Agent File Structure

### Required YAML Frontmatter (Website-Ready Format)

Every agent file uses a comprehensive 9-section YAML frontmatter structure:

```yaml
---
# === CORE IDENTITY ===
name: cs-agent-name                  # Required: cs-* prefix
title: Human Readable Title          # Display name for website
description: One-line description    # Under 300 chars
domain: engineering                  # engineering, product, marketing, delivery
subdomain: backend-development       # Finer categorization
skills: skill-folder-name            # Skill this agent orchestrates
model: sonnet                        # sonnet, opus, haiku

# === WEBSITE DISPLAY ===
difficulty: intermediate             # beginner, intermediate, advanced
time-saved: "2-4 hours per project"  # Quantified benefit
frequency: "Weekly"                  # Usage frequency
use-cases:                           # 3-5 concrete scenarios
  - "Developing REST APIs"
  - "Database schema design"

# === AGENT CLASSIFICATION ===
classification:
  type: implementation               # strategic, implementation, quality, coordination
  color: green                       # blue, green, red, purple
  field: backend                     # functional domain
  expertise: expert                  # beginner, intermediate, expert
  execution: coordinated             # parallel, coordinated, sequential
  model: sonnet                      # recommended model

# === RELATIONSHIPS ===
related-agents: [cs-frontend-engineer, cs-architect]
related-skills: [engineering-team/senior-backend]
related-commands: [/review.code, /generate.tests]
orchestrates:
  skill: engineering-team/senior-backend

# === COLLABORATION ===
collaborates-with:                   # Optional: Agent dependencies for enhanced features
  - agent: cs-technical-writer       # Agent name (must be cs-* prefixed)
    purpose: Architecture diagram generation using Mermaid
    required: optional               # optional, recommended, required
    features-enabled: [architecture-diagrams, sequence-diagrams]
    without-collaborator: "Documentation will be text-only without visual diagrams"

# === TECHNICAL ===
tools: [Read, Write, Bash, Grep, Glob]
dependencies:
  tools: [Read, Write, Bash, Grep, Glob]
  mcp-tools: []                      # Optional MCP servers
  scripts: []                        # Python tools used
compatibility:
  claude-ai: true
  claude-code: true
  platforms: [macos, linux, windows]

# === EXAMPLES ===
examples:
  - title: "Create REST API"
    input: "Design a user authentication API"
    output: "API endpoints created with JWT auth..."

# === ANALYTICS ===
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-11-17
updated: 2025-11-27
license: MIT

# === DISCOVERABILITY ===
tags: [backend, api, nodejs, express]
featured: false
verified: true

# === CLASSIFICATION (for agent type system) ===
color: green
field: backend
expertise: expert
execution: coordinated
---
```

**Section Overview:**
- **Core Identity**: Basic identification (name, title, description, domain)
- **Website Display**: User-facing information (difficulty, time-saved, use-cases)
- **Agent Classification**: Type system for resource management
- **Relationships**: Cross-references to other assets
- **Collaboration**: Optional dependencies on other agents for enhanced features
- **Technical**: Tools and dependencies
- **Examples**: Sample inputs/outputs
- **Analytics**: Marketplace metrics (placeholder)
- **Versioning**: Author and version tracking
- **Discoverability**: Tags and feature flags

### Agent Collaboration Pattern (collaborates-with)

The `collaborates-with` section defines optional dependencies between agents. This enables:
- **Website downloads**: Prompting users to download collaborator agents for full functionality
- **Feature discovery**: Showing what capabilities are unlocked with collaborators
- **Graceful degradation**: Clear communication of what works without collaborators

**Schema:**
```yaml
collaborates-with:
  - agent: cs-technical-writer          # Required: Agent name (must be cs-* prefixed)
    purpose: "Description of collaboration"  # Required: Why this collaboration exists
    required: optional                  # Optional: optional|recommended|required
    features-enabled: [feature-1, feature-2]  # Optional: Features unlocked
    without-collaborator: "What doesn't work"  # Optional: Degraded functionality
```

**Field Definitions:**
| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `agent` | Yes | cs-* name | The collaborating agent identifier |
| `purpose` | Yes | string | Why this collaboration adds value |
| `required` | No | optional, recommended, required | Dependency strength |
| `features-enabled` | No | list | Specific features unlocked by collaborator |
| `without-collaborator` | No | string | What functionality is lost without collaborator |

**Examples:**

**Documentation Collaboration (optional):**
```yaml
collaborates-with:
  - agent: cs-technical-writer
    purpose: API documentation generation with sequence diagrams
    required: optional
    features-enabled: [api-docs, sequence-diagrams, architecture-diagrams]
    without-collaborator: "API documentation will be text-only without visual diagrams"
```

**Quality Collaboration (recommended):**
```yaml
collaborates-with:
  - agent: cs-qa-engineer
    purpose: Test strategy and quality assurance for backend services
    required: recommended
    features-enabled: [api-test-generation, integration-tests, load-testing]
    without-collaborator: "Backend code will lack comprehensive test coverage"
```

**Security Collaboration (recommended):**
```yaml
collaborates-with:
  - agent: cs-security-engineer
    purpose: Security review for authentication and API security patterns
    required: recommended
    features-enabled: [security-audit, auth-patterns, owasp-compliance]
    without-collaborator: "Security vulnerabilities may go undetected"
```

**Validation:**
The `agent_builder.py` validator checks:
- `agent` field is present and starts with `cs-`
- `purpose` field is present
- `required` is one of: optional, recommended, required
- `features-enabled` is a list or string
- `without-collaborator` is a string

### Required Markdown Sections

After YAML frontmatter, include these sections:

1. **Purpose** (2-3 paragraphs)
2. **Skill Integration** (with subsections)
   - Skill Location
   - Python Tools
   - Knowledge Bases
   - Templates
3. **Workflows** (minimum 3 workflows)
4. **Integration Examples** (concrete code/command examples)
5. **Success Metrics** (how to measure effectiveness)
6. **Related Agents** (cross-references)
7. **References** (links to documentation)

## Relative Path Resolution

### Path Pattern

All skill references use the `../../` pattern:

```markdown
**Skill Location:** `../../skills/marketing-team/content-creator/`

### Python Tools

1. **Brand Voice Analyzer**
   - **Path:** `../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py`
   - **Usage:** `python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py content.txt`

2. **SEO Optimizer**
   - **Path:** `../../skills/marketing-team/content-creator/scripts/seo_optimizer.py`
   - **Usage:** `python ../../skills/marketing-team/content-creator/scripts/seo_optimizer.py article.md "keyword"`
```

### Why `../../`?

From agent location: `agents/marketing/cs-content-creator.md`
To skill location: `marketing-skill/content-creator/`

Navigation: `agents/marketing/` → `../../` (up to root) → `marketing-skill/content-creator/`

**Always test paths resolve correctly!**

## Python Tool Integration

### Execution Pattern

Agents execute Python tools from skill packages:

```bash
# From agent context
python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py input.txt

# With JSON output
python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py input.txt json

# With arguments
python ../../skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20
```

### Tool Requirements

All Python tools must:
- Use standard library only (or minimal dependencies documented in SKILL.md)
- Support both JSON and human-readable output
- Provide `--help` flag with usage information
- Return appropriate exit codes (0 = success, 1 = error)
- Handle missing arguments gracefully

### Error Handling

When Python tools fail:
1. Check file path resolution
2. Verify input file exists
3. Check Python version compatibility (3.8+)
4. Review tool's `--help` output
5. Inspect error messages in stderr

## Workflow Documentation

### Workflow Structure

Each workflow must include:

```markdown
### Workflow 1: [Clear Descriptive Name]

**Goal:** One-sentence description

**Steps:**
1. **[Action]** - Description with specific commands/tools
2. **[Action]** - Description with specific commands/tools
3. **[Action]** - Description with specific commands/tools

**Expected Output:** What success looks like

**Time Estimate:** How long this workflow takes

**Example:**
\`\`\`bash
# Concrete example command
python ../../skills/marketing-team/content-creator/scripts/seo_optimizer.py article.md "primary keyword"
\`\`\`
```

### Minimum Requirements

Each agent must document **at least 3 workflows** covering:
1. Primary use case (most common scenario)
2. Advanced use case (complex scenario)
3. Integration use case (combining multiple tools)

## Agent Template

Use this template when creating new agents:

```markdown
---
name: cs-agent-name
description: One-line description
skills: skill-folder-name
domain: domain-name
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---

# Agent Name

## Purpose

[2-3 paragraphs describing what this agent does, why it exists, and who it serves]

## Skill Integration

**Skill Location:** \`../../domain-skill/skill-name/\`

### Python Tools

1. **Tool Name**
   - **Purpose:** What it does
   - **Path:** \`../../domain-skill/skill-name/scripts/tool.py\`
   - **Usage:** \`python ../../domain-skill/skill-name/scripts/tool.py [args]\`

### Knowledge Bases

1. **Reference Name**
   - **Location:** \`../../domain-skill/skill-name/references/file.md\`
   - **Content:** What's inside

### Templates

1. **Template Name**
   - **Location:** \`../../domain-skill/skill-name/assets/template.md\`
   - **Use Case:** When to use

## Workflows

### Workflow 1: [Name]

**Goal:** Description

**Steps:**
1. Step 1
2. Step 2
3. Step 3

**Expected Output:** Success criteria

**Example:**
\`\`\`bash
python ../../domain-skill/skill-name/scripts/tool.py input.txt
\`\`\`

### Workflow 2: [Name]
[Same structure]

### Workflow 3: [Name]
[Same structure]

## Integration Examples

[Concrete examples with actual commands and expected outputs]

## Success Metrics

- Metric 1: How to measure
- Metric 2: How to measure
- Metric 3: How to measure

## Related Agents

- [cs-related-agent](../domain/cs-related-agent.md) - How they relate

## References

- [Skill Documentation](../../domain-skill/skill-name/SKILL.md)
- [Domain Roadmap](../../domain-skill/roadmap.md)
```

## Quality Standards

### Agent Quality Checklist

Before committing an agent:

- [ ] YAML frontmatter valid (no parsing errors)
- [ ] All required fields present (name, description, skills, domain, model, tools)
- [ ] cs-* prefix used for agent naming
- [ ] Relative paths resolve correctly (../../ pattern)
- [ ] Skill location documented and accessible
- [ ] Python tools referenced with correct paths
- [ ] At least 3 workflows documented
- [ ] Integration examples provided and tested
- [ ] Success metrics defined
- [ ] Related agents cross-referenced

### Testing Agent Integration

Test these aspects:

**1. Path Resolution**
```bash
# From agent directory
cd agents/marketing/
ls ../../skills/marketing-team/content-creator/  # Should list contents
```

**2. Python Tool Execution**
```bash
# Create test input
echo "Test content" > test-input.txt

# Execute tool
python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py test-input.txt

# Verify output
```

**3. Knowledge Base Access**
```bash
# Verify reference files exist
cat ../../skills/marketing-team/content-creator/references/brand_guidelines.md
```

## Domain-Specific Guidelines

### Marketing Agents (agents/marketing/)
- Focus on content creation, SEO, demand generation
- Reference: `../../skills/marketing-team/`
- Tools: brand_voice_analyzer.py, seo_optimizer.py

### Product Agents (agents/product/)
- Focus on prioritization, user research, agile workflows
- Reference: `../../skills/product-team/`
- Tools: rice_prioritizer.py, user_story_generator.py, okr_cascade_generator.py

### C-Level Agents (agents/c-level/)
- Focus on strategic decision-making
- Reference: `../../c-level-advisor/`
- Tools: Strategic analysis and planning tools

### Engineering Agents (agents/engineering/)
- Focus on scaffolding, code quality, fullstack development
- Reference: `../../skills/engineering-team/`
- Tools: project_scaffolder.py, code_quality_analyzer.py

## Common Pitfalls

**Avoid these mistakes:**

❌ Hardcoding absolute paths
❌ Skipping YAML frontmatter validation
❌ Forgetting to test relative paths
❌ Documenting workflows without examples
❌ Creating agent dependencies (keep them independent)
❌ Duplicating skill content in agent files
❌ Using LLM calls instead of referencing Python tools

## Next Steps

After creating an agent:

1. Test all relative paths resolve
2. Execute all Python tools from agent context
3. Verify all workflows with concrete examples
4. Update agent catalog in main README.md
5. Create GitHub issue for agent testing
6. Commit with conventional commit message: `feat(agents): implement cs-agent-name`

---

**Last Updated:** December 16, 2025
**Current Status:** 36 production agents, website-ready format with 10-section YAML frontmatter (includes collaborates-with)
**Related:** See [main CLAUDE.md](../CLAUDE.md) for repository overview
