# Agent Creation Quick Reference

**Quick lookup guide for 18 new agents based on 8 production agents analysis**

## 1. Agent Specification Template

```yaml
---
name: cs-[kebab-case-name]
description: [Role] for [primary-function], [secondary-function]
skills: [skill-folder-name]
domain: [marketing|product|engineering|delivery]
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---
```

**Naming Examples:**
- cs-content-creator
- cs-product-manager
- cs-data-scientist

## 2. Section Order (Fixed)

1. Purpose (2-3 paragraphs)
2. Skill Integration (subsections: Python Tools, Knowledge Bases, Templates)
3. Workflows (4 workflows minimum)
4. Integration Examples (3 examples)
5. Success Metrics (3-4 categories)
6. Related Agents (3-5 agents)
7. References (3 standard links)
8. Metadata (Last Updated, Sprint, Status, Version)

## 3. Workflow Template (Repeat 4x)

```markdown
### Workflow N: [Clear Name]

**Goal:** [One-sentence outcome]

**Steps:**
1. **[Action]** - Description
   \`\`\`bash
   command example
   \`\`\`
2. **[Action]** - Description
3. **[Action]** - Description
4. **[Action]** - Description
5. **[Action]** - Description

**Expected Output:** [Specific deliverable with metrics]

**Time Estimate:** [Duration with context]

**Example:**
\`\`\`bash
# Full command example
\`\`\`
```

**Target:** 5-6 steps per workflow, 4 workflows total

## 4. Python Tools Documentation

```markdown
1. **[Tool Name]**
   - **Purpose:** [One-sentence function]
   - **Path:** `../../skills/[domain-team]/[skill]/scripts/[tool].py`
   - **Usage:** `python ../../skills/.../[tool].py [args]`
   - **Features:** [Capability list]
   - **Use Cases:** [When to use]
```

**Requirements:**
- Minimum 1 tool per agent
- Target 2 tools per agent
- Include path, usage, and features

## 5. Success Metrics Template

```markdown
## Success Metrics

**[Category 1: Quality/Efficiency/Adoption/Impact]:**
- **[Metric Name]:** [Quantified target]
- **[Metric Name]:** [Quantified target]
- **[Metric Name]:** [Quantified target]

**[Category 2]:**
[Continue with 2-3 metrics]

**[Category 3]:**
[Continue with 2-3 metrics]
```

**Target:** 3-4 categories, 2-3 metrics each

## 6. Path Patterns (CRITICAL)

### Agent Location
`agents/[domain]/cs-[name].md`

### Skill Reference
`../../skills/[domain-team]/[skill-name]/`

### Python Tool
`../../skills/[domain-team]/[skill-name]/scripts/[tool].py`

### Knowledge Base
`../../skills/[domain-team]/[skill-name]/references/[file].md`

### Template
`../../skills/[domain-team]/[skill-name]/assets/[file].md`

### Cross-Agent (Same Domain)
`cs-other-agent.md`

### Cross-Agent (Different Domain)
`../[domain]/cs-other-agent.md`

**Test from agent directory:**
```bash
cd agents/[domain]/
ls ../../skills/[domain-team]/[skill-name]/
```

## 7. Integration Examples Template

```markdown
## Integration Examples

### Example 1: [Real-world scenario]

\`\`\`bash
#!/bin/bash
# description

# Step 1
echo "Description"
python ../../skills/.../[tool].py input.txt

# Step 2
echo "Next step"
\`\`\`

**Usage:** [Specific use case]

### Example 2: [Different scenario]
[Repeat pattern]

### Example 3: [Third scenario]
[Repeat pattern]
```

**Target:** 3 examples showing different real-world use cases

## 8. Completeness Checklist (Before Commit)

- [ ] YAML frontmatter valid (name, description, skills, domain, model, tools)
- [ ] Purpose: 2-3 paragraphs (what, who, gap)
- [ ] Skill Integration: Tools (1+), Bases (2-3), Templates (0-2)
- [ ] Workflows: 4 total, 5-6 steps each
- [ ] Steps: Include inline bash examples with actual commands
- [ ] Expected Output: Specific, quantified
- [ ] Time Estimate: With context
- [ ] Integration Examples: 3 examples, copy-paste-ready
- [ ] Success Metrics: 3-4 categories, quantified targets
- [ ] Related Agents: 3-5 agents with descriptions
- [ ] References: 3 standard links
- [ ] Metadata: Last Updated, Sprint, Status, Version
- [ ] All paths tested: `cd agents/[domain]/ && ls ../../skills/.../`
- [ ] File size: 300-700 lines (target 400-500)

## 9. File Size Reference

- **Small (300 lines):** Minimal domain, 1-2 tools, simple workflows
- **Medium (400-500 lines):** Standard agent, 2 tools, detailed workflows
- **Large (600-700 lines):** Complex domain, 3+ tools, extensive examples

**8 Production Agents Average:** 466 lines

## 10. Marketing vs Product Patterns

### Marketing Agents
- Focus: Customer acquisition, campaigns, positioning
- Tools: 2 per agent (analyzers, calculators)
- Workflows: Campaign launch → optimization → analysis → strategy
- Examples: 3-4 Bash scripts with real-world scenarios
- Metrics: Heavy on business/acquisition metrics

### Product Agents
- Focus: Strategy → execution, design, research
- Tools: 1-2 per agent (generators, analyzers)
- Workflows: Planning → execution → validation → refinement
- Examples: Detailed code examples (React, Swift, XML)
- Metrics: Heavy on strategic alignment + efficiency

## 11. Common Tool Types (By Domain)

### Marketing
- Analyzers (brand_voice_analyzer.py, win_loss_analyzer.py)
- Calculators (calculate_cac.py)
- Optimizers (seo_optimizer.py)

### Product
- Generators (rice_prioritizer.py, user_story_generator.py, persona_generator.py)
- Cascade tools (okr_cascade_generator.py)
- Validators (design_token_generator.py)

### Engineering (Anticipated for 18 new)
- Scaffolders (project_scaffolder.py)
- Quality analyzers (code_quality_analyzer.py)
- Performance analyzers (performance_analyzer.py)

## 12. Related Agents Pattern

Show progression/workflow:
```markdown
- [cs-product-manager](cs-product-manager.md) - Strategic prioritization, feeds into sprint backlog
- [cs-agile-product-owner](cs-agile-product-owner.md) - Sprint planning, translates features into stories
- [cs-ux-researcher](cs-ux-researcher.md) - Research insights inform user story creation (planned)
```

Mark planned agents with "(planned)" - helps roadmap visibility

## 13. Workflow Complexity Progression

**Workflow 1 → 4 increases in scope:**

- W1: Single artifact creation (blog post, story, OKR)
- W2: Batch operations (audit multiple pieces, cascade multiple OKRs)
- W3: Cross-functional (strategy, multi-tool integration, design systems)
- W4: Specialized/optimization (international expansion, health checks)

## 14. Metadata Format

```markdown
---

**Last Updated:** YYYY-MM-DD
**Sprint:** sprint-MM-DD-YYYY (Day X)
**Status:** Production Ready
**Version:** 1.0
```

**Status Options:**
- Production Ready (for finished agents)
- Beta (for agents in review)
- Alpha (for draft agents)

## 15. Quick Start for New Agent

### Automated Way (Recommended - 96% Faster)

```bash
# Create new agent interactively (1 hour instead of 2 days)
python3 scripts/agent_builder.py

# Or use config file for automation
python3 scripts/agent_builder.py --config examples/agent-config-example.yaml

# Validate after creation
python3 scripts/agent_builder.py --validate agents/[domain]/cs-[name].md

# Time savings: 2 days → 1 hour (96% reduction)
```

**Features:**
- Interactive 7-step workflow with validation
- Automatic YAML frontmatter generation
- Template-based file creation with placeholders
- Post-generation validation (9 checks)
- Zero dependencies (Python 3.8+ standard library only)

See [Agent Builder Documentation](../../scripts/agent_builder.py) and [Builder Standards](../standards/builder-standards.md).

### Manual Way (Legacy - For Reference)

```bash
# 1. Copy template
cp templates/agent-template.md agents/[domain]/cs-[name].md

# 2. Fill YAML frontmatter
# 3. Write purpose (2-3 paragraphs)
# 4. Document skill integration (1-2 tools, 2-3 bases)
# 5. Create 4 workflows (5-6 steps each)
# 6. Add 3 integration examples
# 7. Define success metrics (3-4 categories)
# 8. List related agents (3-5)
# 9. Add references and metadata
# 10. Test paths from agent directory
# 11. Verify against checklist (Section 8)
# 12. Commit with conventional message

git commit -m "feat(agents): implement cs-[agent-name]"
```

---

**Reference:** Based on comprehensive analysis of 8 production agents
**Agents Analyzed:** cs-content-creator, cs-demand-gen-specialist, cs-product-marketer, cs-product-manager, cs-agile-product-owner, cs-product-strategist, cs-ux-researcher, cs-ui-designer
**Created:** November 12, 2025
