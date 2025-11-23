# Agent YAML Updater - Quick Start Guide

## One-Minute Quick Start

```bash
# 1. Preview what will change (SAFE - no writes)
python scripts/update_agent_yaml.py --dry-run

# 2. Apply updates to all 28 agents
python scripts/update_agent_yaml.py

# Done! All agents now have 5 new YAML fields.
```

## What Gets Added

Five new fields to each agent's YAML frontmatter:

```yaml
color: orange          # Agent type: blue, green, red, purple, orange
field: content         # Domain: frontend, backend, product, ai, etc.
expertise: expert      # Level: beginner, intermediate, expert
execution: parallel    # Pattern: parallel, coordinated, sequential
mcp_tools: []         # MCP integrations: [mcp__github], [mcp__atlassian], etc.
```

## Color System (Quick Reference)

| Color | Type | Count | Examples |
|-------|------|-------|----------|
| 🔵 Blue | Strategic | 5 | product-strategist, ux-researcher |
| 🟢 Green | Implementation | 7 | backend-engineer, fullstack-engineer |
| 🔴 Red | Quality | 4 | code-reviewer, qa-engineer |
| 🟣 Purple | Coordination | 5 | architect, scrum-master |
| 🟠 Orange | Domain | 7 | content-creator, data-scientist |

## Execution Patterns (Quick Reference)

| Pattern | Count | Usage | Agents |
|---------|-------|-------|--------|
| **Parallel** | 15 | Run 4-5 together | Strategic, coordination, domain specialists |
| **Coordinated** | 9 | Run 2-3 together | Engineers, data scientists |
| **Sequential** | 4 | Run 1 at a time | Quality, security, testing agents |

## Common Commands

### Preview Before Applying
```bash
# See all changes without writing files
python scripts/update_agent_yaml.py --dry-run
```

### Update All Agents
```bash
# Apply updates to all 28 agents
python scripts/update_agent_yaml.py
```

### Update Single Agent
```bash
# Test on one agent first
python scripts/update_agent_yaml.py --agent agents/marketing/cs-content-creator.md
```

### Get Help
```bash
python scripts/update_agent_yaml.py --help
```

## Expected Output

```
📊 Update Summary
================================================================================

Total agents: 28
  ✅ Updated: 28
  ⏭️  Skipped: 0
  ❌ Errors: 0

🎨 By Color:
  🔵 blue: 5      (Strategic)
  🟢 green: 7     (Implementation)
  🟠 orange: 7    (Domain)
  🟣 purple: 5    (Coordination)
  🔴 red: 4       (Quality)

⚙️  By Execution:
  • coordinated: 9
  • parallel: 15
  • sequential: 4
```

## Safety Features

- ✅ Dry-run mode (preview before apply)
- ✅ Skip already-updated agents
- ✅ Preserve all existing fields
- ✅ Maintain exact formatting
- ✅ Zero external dependencies
- ✅ Detailed error messages

## What If Something Goes Wrong?

### Rollback Updates
```bash
# Git-based rollback (easiest)
git checkout agents/
```

### Check Before Committing
```bash
# View changes
git diff agents/

# Review specific agent
git diff agents/marketing/cs-content-creator.md
```

## Agent Classification Examples

### Blue (Strategic) - cs-product-strategist
```yaml
color: blue
field: product
expertise: expert
execution: parallel
mcp_tools: []
```

### Green (Implementation) - cs-backend-engineer
```yaml
color: green
field: backend
expertise: expert
execution: coordinated
mcp_tools: []
```

### Red (Quality) - cs-code-reviewer
```yaml
color: red
field: quality
expertise: expert
execution: sequential
mcp_tools: [mcp__github]
```

### Purple (Coordination) - cs-architect
```yaml
color: purple
field: architecture
expertise: expert
execution: parallel
mcp_tools: []
```

### Orange (Domain) - cs-content-creator
```yaml
color: orange
field: content
expertise: expert
execution: parallel
mcp_tools: []
```

## MCP Integration Quick Reference

| MCP Tool | Agents | Purpose |
|----------|--------|---------|
| `mcp__github` | 3 agents | PR review, issues, code analysis |
| `mcp__playwright` | 1 agent | Browser automation, E2E testing |
| `mcp__atlassian` | 5 agents | Jira/Confluence integration |

**Agents with MCP:**
- **GitHub:** code-reviewer, qa-engineer, security-engineer
- **Playwright:** qa-engineer (also has GitHub)
- **Atlassian:** jira-expert, confluence-expert, scrum-master, agile-product-owner, senior-pm

## Troubleshooting

### "No module named 'yaml'"
**Not a problem!** Script uses custom YAML parser. No pip install needed.

### "No valid YAML frontmatter found"
**Check:** Ensure agent file has `---` delimiters around YAML.

### "Already updated (color field exists)"
**Expected behavior.** Agent already has new fields. Re-run if needed.

## Full Documentation

- **Complete Guide:** `scripts/UPDATE_AGENT_YAML_README.md`
- **Implementation Details:** `scripts/AGENT_YAML_UPDATE_SUMMARY.md`
- **Script Source:** `scripts/update_agent_yaml.py`

## Quick Decision Tree

```
Do you want to see changes first?
├─ YES → python scripts/update_agent_yaml.py --dry-run
└─ NO  → Continue

Ready to update all agents?
├─ YES → python scripts/update_agent_yaml.py
└─ NO  → Test one: python scripts/update_agent_yaml.py --agent agents/.../agent.md

Seeing errors?
├─ Check documentation
└─ Run with dry-run first

Need to rollback?
└─ git checkout agents/
```

## Best Practices

1. ✅ **Always run dry-run first**
2. ✅ **Commit current state before bulk update**
3. ✅ **Review the summary report**
4. ✅ **Test one agent before bulk update**
5. ✅ **Verify git diff after update**

## Next Steps After Update

1. Update `scripts/agent_builder.py` to include new fields
2. Update validation logic to check new fields
3. Update documentation to reference classification system
4. Add visual indicators to agent catalog
5. Implement resource management based on execution patterns

---

**Quick Start Guide** | Last Updated: November 23, 2025
**Script Version:** 1.0 | **Python:** 3.8+ | **Dependencies:** None
