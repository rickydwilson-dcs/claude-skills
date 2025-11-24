# Agent Development Documentation

Complete guide for creating, testing, and maintaining Claude Skills agents.

## Overview

This directory contains comprehensive documentation for developing production-quality agents that orchestrate skills and provide guided workflows.

**What's an Agent?** An agent is a workflow orchestrator that intelligently invokes skills, coordinates Python tools, and guides users through complex multi-step processes.

## Documentation Files

### For Agent Developers

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[AGENT_DEVELOPMENT_GUIDE.md](AGENT_DEVELOPMENT_GUIDE.md)** | Complete patterns & best practices | Deep learning, training contributors |
| **[AGENT_QUICK_START.md](AGENT_QUICK_START.md)** | Quick-lookup templates | During development, rapid creation |
| **[COMPLETENESS_CHECKLIST.md](COMPLETENESS_CHECKLIST.md)** | Quality verification | Before committing agents |

### For Users

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[../guides/understanding-skills.md](../guides/understanding-skills.md)** | ELI5: What are skills? | New users, onboarding |
| **[../guides/using-skills.md](../guides/using-skills.md)** | How to use skills & agents | Daily usage, integration |
| **[../guides/skill-to-agent-flow.md](../guides/skill-to-agent-flow.md)** | How everything connects | Understanding architecture |

## Quick Start: Create Your First Agent

**Time (Automated):** 1 hour | **Time (Manual):** 4-6 hours | **Time Savings:** 96%

### Automated Way (Recommended)

```bash
# Interactive agent creation (1 hour instead of 2 days)
python3 scripts/agent_builder.py

# Or use config file for automation
python3 scripts/agent_builder.py --config examples/agent-config-example.yaml

# Validate after creation
python3 scripts/agent_builder.py --validate agents/marketing/cs-content-creator.md
```

**Features:**
- Interactive 7-step workflow with validation
- Automatic YAML frontmatter generation
- Template-based file creation
- Post-generation validation (9 checks)
- Zero dependencies (Python 3.8+ standard library only)

See [Agent Builder Documentation](../../scripts/agent_builder.py) and [Builder Standards](../standards/builder-standards.md).

### Manual Way (Legacy - For Deep Learning)

**Time:** 4-6 hours | **Difficulty:** Intermediate | **Prerequisites:** Understanding of skills

#### 1. Choose Your Domain

```bash
# Agents are organized by domain
agents/
├── marketing/      # Marketing domain agents
├── product/        # Product domain agents
├── engineering/    # Engineering domain agents
└── delivery/       # Delivery/PM domain agents
```

#### 2. Use the Quick Start Template

Open [AGENT_QUICK_START.md](AGENT_QUICK_START.md) and copy Section 1 (Agent Specification Template).

#### 3. Follow the Pattern

All agents follow the same structure:
1. YAML frontmatter (name, description, skills, domain, model, tools)
2. Purpose (2-3 paragraphs)
3. Skill Integration (Python tools, knowledge bases, templates)
4. Workflows (4 minimum)
5. Integration Examples (3 examples)
6. Success Metrics (3-4 categories)
7. Related Agents (3-5 agents)
8. References & Metadata

#### 4. Test Thoroughly

```bash
# From agent directory, test all paths
cd agents/marketing/
ls ../../skills/marketing-team/content-creator/

# Test Python tool execution
python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py --help
```

#### 5. Verify with Checklist

Use [COMPLETENESS_CHECKLIST.md](COMPLETENESS_CHECKLIST.md) before committing.

## Agent Architecture

### Agents vs Skills

**Skills** = Tools + Knowledge + Templates
- Self-contained packages
- Include Python CLI tools
- Provide knowledge bases
- Offer ready-to-use templates

**Agents** = Workflow Orchestrators
- Invoke skills intelligently
- Guide multi-step processes
- Coordinate tools and knowledge
- Provide concrete workflows

### Example Flow

```
User Request
    ↓
Agent (cs-content-creator)
    ↓
Invokes Skills (content-creator skill)
    ↓
Uses Python Tools (brand_voice_analyzer.py, seo_optimizer.py)
    ↓
References Knowledge (brand guidelines, SEO frameworks)
    ↓
Applies Templates (content calendar, social media templates)
    ↓
Delivers Output (Optimized content with metrics)
```

## Key Principles

### 1. Agents Are Formulaic (By Design)

Every agent follows an identical structure. This consistency enables:
- Rapid creation (4-6 hours vs 8-12 hours)
- Quality consistency
- Easy maintenance
- Predictable user experience

### 2. Workflows Are Concrete

Each workflow includes:
- Clear goal statement
- 5-6 specific steps
- Inline bash examples
- Expected output with metrics
- Time estimates with context

### 3. Paths Are Relative

All paths use the `../../skills/[domain]/[skill]/` pattern from the agent directory:
- ✅ `../../skills/marketing-team/content-creator/scripts/tool.py`
- ❌ `/absolute/path/to/scripts/tool.py`

### 4. Tools Are Documented

Every Python tool needs:
- Purpose (one-sentence)
- Path (relative from agent)
- Usage (copy-paste command)
- Features (capability list)
- Use Cases (when to use)

### 5. Metrics Are Quantified

Success metrics must be specific:
- ✅ "Reduce content creation time by 40%"
- ❌ "Improve efficiency"

## Production Standards

### Minimum Requirements

- ✅ 4 workflows minimum
- ✅ 1 Python tool minimum (target: 2)
- ✅ 3 integration examples
- ✅ 3-4 metric categories
- ✅ All paths tested from agent directory
- ✅ Checklist verified

### Target Metrics

Based on 27 production agents:
- **File size:** 400-500 lines
- **Workflows:** 4 (exactly)
- **Steps per workflow:** 5-6 average
- **Python tools:** 1-2 per agent
- **Knowledge bases:** 2-3 per agent
- **Related agents:** 3-5 listed

## Common Pitfalls

1. **Absolute Paths** - Always use relative `../../` pattern
2. **Generic Metrics** - Quantify everything (%, time, ratios)
3. **Missing Tool Docs** - Document every Python script
4. **Complex Workflows** - Keep steps concrete and actionable
5. **No Testing** - Test all paths before committing
6. **Structure Innovation** - Follow patterns exactly

## Development Workflow

### Automated Workflow (Recommended - 96% Faster)

```bash
# 1. Run agent builder interactively
python3 scripts/agent_builder.py

# 2. Follow 7-step interactive workflow:
#    - Agent name (cs-* prefix)
#    - Domain selection (marketing/product/engineering/delivery)
#    - Skill package selection
#    - Model selection (sonnet/opus/haiku)
#    - Description (max 150 chars)
#    - Tools selection
#    - Confirmation

# 3. Builder generates agent file with validation

# 4. Manually enhance workflows and examples (if needed)

# 5. Commit
git add agents/[domain]/cs-[name].md
git commit -m "feat(agents): implement cs-[name]"

# Time: 1 hour total (96% faster than manual)
```

### Manual Workflow (Legacy)

```bash
# 1. Copy template from AGENT_QUICK_START.md
cp docs/agent-development/AGENT_QUICK_START.md agents/[domain]/cs-[name].md

# 2. Fill in YAML frontmatter
# 3. Write Purpose section
# 4. Document Python tools
# 5. Create 4 workflows
# 6. Add 3 integration examples
# 7. Define success metrics
# 8. List related agents
# 9. Test all paths

# 10. Verify with checklist
docs/agent-development/COMPLETENESS_CHECKLIST.md

# 11. Commit
git add agents/[domain]/cs-[name].md
git commit -m "feat(agents): implement cs-[name]"

# Time: 4-6 hours total
```

## Resources

### Internal Documentation

- **[agents/CLAUDE.md](../../agents/CLAUDE.md)** - Agent system overview
- **[templates/agent-template.md](../../templates/agent-template.md)** - Official template
- **[CLAUDE.md](../../CLAUDE.md)** - Repository overview

### External Resources

- **[Claude Code Documentation](https://code.claude.com/docs)** - Claude Code guides
- **[Agent Skills Spec](https://code.claude.com/docs/agent-skills)** - Anthropic standards

## Statistics

**Current Production Agents:** 27
**Total Domains:** 4 (Marketing, Product, Engineering, Delivery)
**Total Workflows:** 108 (4 × 27)
**Total Python Tools:** 53 across all skills
**Average Creation Time:** 4-6 hours per agent

## Support

**Questions?**
- Check [AGENT_QUICK_START.md](AGENT_QUICK_START.md) for templates
- Review existing agents in `agents/[domain]/` for examples
- See [AGENT_DEVELOPMENT_GUIDE.md](AGENT_DEVELOPMENT_GUIDE.md) for deep patterns

**Issues?**
- Verify paths with checklist
- Test from agent directory
- Compare with production agents

---

**Last Updated:** November 17, 2025
**Version:** 1.0
**Status:** Production-ready guide for 27 existing agents + future development
