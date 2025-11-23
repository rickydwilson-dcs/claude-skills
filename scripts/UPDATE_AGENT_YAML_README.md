# Agent YAML Updater - Documentation

## Overview

The `update_agent_yaml.py` script intelligently updates all 28 existing agents with new YAML frontmatter fields that enable enhanced agent classification, resource management, and MCP integration.

## New YAML Fields

The script adds these 5 new fields to each agent's YAML frontmatter:

| Field | Type | Description | Example Values |
|-------|------|-------------|----------------|
| `color` | string | Agent type classification for visual organization | blue, green, red, purple, orange |
| `field` | string | Primary domain focus area | frontend, backend, product, ai, security |
| `expertise` | string | Skill level indicator | beginner, intermediate, expert |
| `execution` | string | Work pattern and resource requirements | parallel, coordinated, sequential |
| `mcp_tools` | array | MCP server integrations | [mcp__github], [mcp__atlassian] |

## Color Classification System

### 🔵 Blue - Strategic Agents (5 agents)
**Characteristics:** Planning, research, analysis, strategic decision-making
**Resource Usage:** Low CPU, moderate memory, minimal I/O
**Concurrency:** Safe to run 4-5 agents in parallel

**Agents:**
- cs-product-strategist
- cs-business-analyst
- cs-product-manager
- cs-ux-researcher
- cs-product-marketer

### 🟢 Green - Implementation Agents (7 agents)
**Characteristics:** Active code development, feature building, system implementation
**Resource Usage:** Moderate CPU, high memory, high I/O
**Concurrency:** Run 2-3 agents with coordination

**Agents:**
- cs-backend-engineer
- cs-frontend-engineer
- cs-fullstack-engineer
- cs-devops-engineer
- cs-ml-engineer
- cs-data-engineer
- cs-prompt-engineer

### 🔴 Red - Quality Agents (4 agents)
**Characteristics:** Testing, validation, code review, security scanning
**Resource Usage:** High CPU, high memory, intensive I/O
**Concurrency:** MUST run sequentially (1 at a time)

**Agents:**
- cs-code-reviewer
- cs-qa-engineer
- cs-security-engineer
- cs-secops-engineer

### 🟣 Purple - Coordination Agents (5 agents)
**Characteristics:** Architecture, orchestration, workflow management
**Resource Usage:** Low across all metrics
**Concurrency:** Can run alongside other agents

**Agents:**
- cs-architect
- cs-cto-advisor
- cs-scrum-master
- cs-senior-pm
- cs-agile-product-owner

### 🟠 Orange - Domain Specialist Agents (7 agents)
**Characteristics:** Specialized domain expertise (content, design, data analysis, tools)
**Resource Usage:** Varies by specialization
**Concurrency:** Generally parallel-safe

**Agents:**
- cs-content-creator
- cs-demand-gen-specialist
- cs-ui-designer
- cs-data-scientist
- cs-computer-vision
- cs-jira-expert
- cs-confluence-expert

## Field Categories

### Product & Strategy
- **product** (5): product-manager, product-strategist, agile-product-owner, senior-pm, business-analyst
- **strategy** (1): ceo-advisor

### Engineering
- **frontend** (1): frontend-engineer
- **backend** (1): backend-engineer
- **fullstack** (1): fullstack-engineer
- **devops** (1): devops-engineer
- **architecture** (2): architect, cto-advisor

### Quality & Security
- **quality** (1): code-reviewer
- **testing** (1): qa-engineer
- **security** (2): security-engineer, secops-engineer

### Data & AI
- **data** (2): data-engineer, data-scientist
- **ai** (3): ml-engineer, computer-vision, prompt-engineer

### Domain Specialists
- **content** (3): content-creator, demand-gen-specialist, product-marketer
- **design** (1): ui-designer
- **research** (1): ux-researcher
- **agile** (1): scrum-master
- **tools** (2): jira-expert, confluence-expert

## Execution Patterns

### Parallel (15 agents)
**Safe Concurrency:** 4-5 agents simultaneously
**Use Cases:** Research, planning, analysis, domain expertise
**Resource Impact:** Low - primarily read operations

**Agents:** All strategic (blue), coordination (purple), and most domain (orange) agents

### Coordinated (9 agents)
**Safe Concurrency:** 2-3 agents with coordination
**Use Cases:** Active development, feature implementation
**Resource Impact:** Moderate-High - code generation, file modifications

**Agents:** All implementation (green) agents + data-scientist, computer-vision

### Sequential (4 agents)
**Safe Concurrency:** 1 agent at a time ONLY
**Use Cases:** Testing, quality assurance, security scanning
**Resource Impact:** High - spawns multiple sub-processes

**Agents:** All quality (red) agents

## MCP Integration

### GitHub MCP (`mcp__github`)
**Purpose:** PR review, issue management, code analysis
**Agents:** code-reviewer, qa-engineer, security-engineer

### Playwright MCP (`mcp__playwright`)
**Purpose:** Browser automation, E2E testing, visual regression
**Agents:** qa-engineer

### Atlassian MCP (`mcp__atlassian`)
**Purpose:** Jira/Confluence integration
**Agents:** jira-expert, confluence-expert, scrum-master, agile-product-owner, senior-pm

## Usage

### Preview Changes (Dry Run)
```bash
# Preview all agent updates
python scripts/update_agent_yaml.py --dry-run

# Preview single agent update
python scripts/update_agent_yaml.py --dry-run --agent agents/marketing/cs-content-creator.md
```

### Apply Updates
```bash
# Update all agents
python scripts/update_agent_yaml.py

# Update single agent
python scripts/update_agent_yaml.py --agent agents/marketing/cs-content-creator.md
```

### Help
```bash
python scripts/update_agent_yaml.py --help
```

## Update Logic

### Color Assignment
1. Check agent name against direct mappings
2. Fallback to keyword analysis in description
3. Default to appropriate color based on role characteristics

### Field Assignment
- Direct lookup based on agent name slug (without `cs-` prefix)
- Fallback to 'general' if not found

### Expertise Assignment
- Check for 'junior' or 'beginner' keywords → beginner
- Check for 'intermediate' keyword → intermediate
- Default to 'expert' (all current production agents)

### Execution Assignment
1. Quality agents (code-reviewer, qa, security) → sequential
2. Implementation engineers → coordinated
3. Strategic/coordination agents → parallel
4. Fallback based on tool count (5+ = coordinated, <5 = parallel)

### MCP Tools Assignment
- Direct lookup based on agent capabilities
- Empty array [] if no MCP integration

## Output Format

### Before Update
```yaml
---
name: cs-content-creator
description: AI-powered content creation specialist...
skills: marketing-team/content-creator
domain: marketing
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---
```

### After Update
```yaml
---
name: cs-content-creator
description: AI-powered content creation specialist...
skills: marketing-team/content-creator
domain: marketing
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
color: orange
field: content
expertise: expert
execution: parallel
mcp_tools: []
---
```

## Summary Report Example

```
📊 Update Summary
================================================================================

Total agents: 28
  ✅ Updated: 28
  ⏭️  Skipped: 0
  ❌ Errors: 0

🎨 By Color:
  🔵 blue: 5
  🟢 green: 7
  🟠 orange: 7
  🟣 purple: 5
  🔴 red: 4

🏷️  By Field:
  • ai: 3
  • architecture: 2
  • backend: 1
  • content: 3
  • data: 2
  • design: 1
  • devops: 1
  • frontend: 1
  • fullstack: 1
  • product: 5
  • quality: 1
  • research: 1
  • security: 2
  • testing: 1
  • tools: 2

🎓 By Expertise:
  • expert: 28

⚙️  By Execution:
  • coordinated: 9
  • parallel: 15
  • sequential: 4
```

## Validation

### Pre-Update Checks
- Validates YAML frontmatter exists
- Checks for existing updates (skips if already updated)
- Parses YAML without external dependencies

### Post-Update Validation
- Ensures YAML remains parseable
- Preserves all existing fields
- Maintains markdown formatting

### Error Handling
- Graceful handling of malformed YAML
- Detailed error messages with file paths
- Rollback capability (dry-run mode)

## Technical Details

### Dependencies
- **Zero external dependencies** - uses Python standard library only
- Works with Python 3.8+
- No pip install required

### YAML Parsing
- Custom lightweight YAML parser for frontmatter
- Handles simple key-value pairs and arrays
- No heavy YAML library dependency

### File Safety
- Preserves exact formatting and spacing
- Maintains all existing fields
- No data loss risk with dry-run mode

## Troubleshooting

### Issue: "No valid YAML frontmatter found"
**Solution:** Ensure agent file has YAML frontmatter between `---` delimiters

### Issue: "Already updated (color field exists)"
**Solution:** Expected behavior - agent already has new fields. Re-run if updates needed.

### Issue: "YAML parsing error"
**Solution:** Check for malformed YAML syntax in frontmatter

## Best Practices

1. **Always run dry-run first** to preview changes
2. **Commit before updating** to enable easy rollback if needed
3. **Validate one agent first** before bulk updates
4. **Review the summary report** to ensure classification is correct
5. **Test updated agents** to confirm they still function properly

## Next Steps After Update

1. Update agent builder to include new fields for new agents
2. Update agent validation to check new fields
3. Update documentation to reference new classification system
4. Consider adding visual indicators in agent catalog based on colors
5. Implement resource management based on execution patterns

---

**Last Updated:** November 23, 2025
**Script Version:** 1.0
**Total Agents:** 28
**Python Version:** 3.8+
