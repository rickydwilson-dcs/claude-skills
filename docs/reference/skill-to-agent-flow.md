# How Skills and Agents Work Together

**For:** Anyone wanting to understand the complete picture
**Time to Read:** 8 minutes
**Goal:** See how skills, agents, and tools connect

---

## The Big Picture (In One Sentence)

**Skills** provide the tools and knowledge → **Agents** know how to use them → **You** get expert results faster

---

## Visual Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         YOU (The User)                           │
│                                                                   │
│  "I need to review the architecture of our microservices app"   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    AGENT (cs-architect)                           │
│                                                                    │
│  "I'll guide you through architecture analysis step-by-step"     │
│                                                                    │
│  Workflow 1: Architecture Review                                 │
│  Step 1: Run project analyzer                                    │
│  Step 2: Review structure and patterns                           │
│  Step 3: Analyze dependencies                                    │
│  Step 4: Generate ADR documentation                              │
│  Step 5: Create C4 diagrams                                      │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                  SKILL (senior-architect)                         │
│                                                                    │
│  Python Tools:                                                    │
│  • project_architect.py      → Analyze structure instantly       │
│  • dependency_analyzer.py    → Check dependencies                │
│                                                                    │
│  Knowledge Bases:                                                 │
│  • Architecture patterns     → Microservices, CQRS, DDD          │
│  • Design principles         → SOLID, clean architecture         │
│  • Scalability guides        → Performance, resilience           │
│                                                                    │
│  Templates:                                                       │
│  • ADR template              → Decision records                  │
│  • C4 diagram templates      → Visual architecture               │
│  • Review checklists         → Comprehensive assessment          │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                           OUTPUT                                   │
│                                                                    │
│  ✅ Architecture review (Score: 8.5/10)                          │
│  ✅ 3 issues identified with recommendations                     │
│  ✅ Complete analysis in 45 minutes (vs 4 hours manually)        │
└──────────────────────────────────────────────────────────────────┘
```

---

## Example 1: Architecture Review (Detailed)

### Scenario

You need to review the architecture of your microservices application before a major release.

### Step-by-Step Flow

#### 1. You Start

```
Your goal: Comprehensive architecture review, identify issues, document decisions
```

#### 2. Choose Your Path

**Option A: Use Agent (Guided)**
```bash
# Open cs-architect agent
open agents/engineering/cs-architect.md

# Agent tells you:
"Follow Workflow 1: Architecture Review"
# Then guides you through 5 steps
```

**Option B: Use Skill Directly (Expert)**
```bash
# You already know what to do, just use the tools:
cd skills/engineering-team/senior-architect/
```

#### 3. Agent Workflow (Option A)

**Step 1:** Agent says "Run project analyzer on your codebase"
```bash
# Agent runs this for you:
python ../../skills/engineering-team/senior-architect/scripts/project_architect.py --input . --verbose

# Output:
Architecture Score: 8.2/10
Pattern: Microservices with event-driven communication
✓ Good domain separation
✓ Clear API boundaries
⚠️ Missing shared utils library
⚠️ 3 circular dependencies detected
❌ API gateway has single point of failure
```

**Step 2:** Agent says "Analyze dependency structure"
```bash
# Agent runs:
python ../../skills/engineering-team/senior-architect/scripts/project_architect.py --input . --focus dependencies

# Output:
External Dependencies: 15 packages
⚠️ High-risk: axios@0.21.1 (CVE-2021-3749)
⚠️ Circular deps: user-service ↔ auth-service
✓ Python tools: Standard library only
```

**Step 3:** Agent says "Review the detected patterns"
```
# Agent explains:
Your architecture uses:
- Microservices pattern (good for scalability)
- Event-driven communication (good for decoupling)
- No API gateway redundancy (risk)

Recommendations:
1. Add load balancer for API gateway
2. Break circular dependency between user/auth services
3. Create shared utils library for common code
```

**Step 4:** Agent says "Document key decisions"
```bash
# Agent guides you to create ADR:
cp ../../skills/engineering-team/senior-architect/assets/adr-template.md docs/architecture/ADR-001-api-gateway-redundancy.md

# You document the API gateway decision
```

**Step 5:** Agent says "Generate architecture diagrams"
```
# Agent provides C4 template:
Use the Context diagram template to show system boundaries
Use the Container diagram to show microservices
Document the current state and proposed changes
```

**Step 6:** Agent says "Create action items"
```
Priority fixes:
1. HIGH: Add API gateway redundancy (2 days)
2. HIGH: Resolve circular dependencies (3 days)
3. MEDIUM: Create shared utils library (5 days)
```

**Done!** 45 minutes total (vs 4 hours without)

---

## Example 2: Feature Prioritization

### Scenario

You have 30 feature requests and need to prioritize them.

### The Flow

#### 1. You Prepare Data

```csv
feature,reach,impact,confidence,effort
Dashboard,500,3,0.8,5
API,1000,2,0.9,3
Dark Mode,300,1,1.0,2
```

#### 2. Agent Guides You

**Agent:** cs-product-manager
**Workflow:** "Feature Prioritization with RICE"

**Step 1:** Agent validates your CSV format
```bash
# Checks that you have: feature, reach, impact, confidence, effort
```

**Step 2:** Agent runs RICE calculation
```bash
python ../../skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 30

# Skill returns:
1. API - Score: 600 (Quick Win ⚡)
2. Dashboard - Score: 300 (Big Bet 🎯)
3. Dark Mode - Score: 150
```

**Step 3:** Agent interprets results
```
"Focus on API first (highest ROI)
Then Dashboard (strategic value)
Dark Mode is nice-to-have"
```

**Step 4:** Agent exports for Jira
```bash
python ../../skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --output json > priorities.json
```

**Done!** 30 minutes (vs 4 hours of spreadsheet work)

---

## The Relationship

### Skills Are Like:

**A Toolbox:**
- Contains specialized tools (Python scripts)
- Includes instruction manuals (knowledge bases)
- Provides templates (assets)

**You can use the toolbox directly if you know what you need**

### Agents Are Like:

**An Expert Craftsperson:**
- Knows which tools to use when
- Follows proven processes (workflows)
- Guides you step-by-step
- Ensures quality at each step

**You ask the expert when you need guidance**

---

## When to Use What

### Use SKILLS Directly When:

✅ **You're experienced** - You know exactly what you need
✅ **Quick tasks** - "Just run the architecture analyzer"
✅ **Automation** - Building scripts that use tools
✅ **Exploration** - Trying out tools to learn

**Example:**
```bash
# Quick architecture check before release
python skills/engineering-team/senior-architect/scripts/project_architect.py --input . --verbose
```

### Use AGENTS When:

✅ **You're learning** - Need step-by-step guidance
✅ **Complex workflows** - Multi-step processes
✅ **Best practices** - Want to follow proven patterns
✅ **Completeness** - Don't want to miss steps

**Example:**
```bash
# First time conducting comprehensive architecture review
# Open cs-architect agent
# Follow "Workflow 1: Architecture Review"
```

---

## Real-World Scenarios

### Scenario 1: New Software Architect

**Day 1:** Uses cs-architect agent
- Follows architecture review workflow step-by-step
- Learns which tools analyze what
- Understands the architecture patterns

**Week 2:** Mix of agent + direct tool use
- Uses agent for complex architecture decisions
- Runs project_architect.py directly for quick checks
- References pattern guides as needed

**Month 2:** Mostly direct tool use
- Knows all the analysis tools
- Has own review workflows
- Only uses agent for new architecture patterns

### Scenario 2: Product Manager

**Planning Week:** Uses cs-product-manager agent
- "Feature Prioritization" workflow
- "Customer Discovery" workflow
- "Roadmap Development" workflow

**Execution Week:** Direct skill use
- Quick RICE calculations
- Interview analysis
- Generates user stories

**Review Week:** Back to agent
- Uses "Quarterly Planning" workflow
- Comprehensive process
- Nothing forgotten

---

## How They Connect: Technical View

### File Structure

```
claude-skills/
│
├── agents/                          # Workflow guides
│   ├── engineering/
│   │   └── cs-architect.md         # Agent file
│   │       ↓
│   │       Uses skills via: ../../skills/engineering-team/senior-architect/
│   │
│   └── product/
│       └── cs-product-manager.md    # Agent file
│           ↓
│           Uses skills via: ../../skills/product-team/product-manager-toolkit/
│
└── skills/                          # The toolboxes
    ├── engineering-team/
    │   └── senior-architect/        # Skill package
    │       ├── scripts/             # Python tools
    │       ├── references/          # Knowledge
    │       └── assets/              # Templates
    │
    └── product-team/
        └── product-manager-toolkit/ # Skill package
            ├── scripts/
            ├── references/
            └── assets/
```

### Path Pattern

**Agents use relative paths to access skills:**

```markdown
# In: agents/engineering/cs-architect.md

## Python Tools

1. **Project Architect**
   - Path: `../../skills/engineering-team/senior-architect/scripts/project_architect.py`
   - Usage: `python ../../skills/.../project_architect.py --input . --verbose`
```

This means:
- Agent knows WHERE the tools are
- Agent knows HOW to use them
- Agent follows proven WORKFLOWS

---

## Quick Reference

| Question | Answer |
|----------|--------|
| **I'm new, where do I start?** | Read an agent file for your role (agents/[domain]/) |
| **I know what I want** | Go directly to skills/[domain]/[skill]/ |
| **I need step-by-step help** | Follow an agent workflow |
| **Just checking one thing** | Run a skill tool directly |
| **Building automation** | Import skill tools into your scripts |
| **Learning workflows** | Study agent files |

---

## Summary

```
Skills = The capability (tools + knowledge + templates)
Agents = The guide (workflows + best practices)
You = The user (gets work done faster + better quality)

Together = Expert results in less time
```

**Skills** give you superpowers
**Agents** teach you how to use them
**You** accomplish more

---

## Next Steps

**Ready to try it?**
→ Go to [using-skills.md](using-skills.md) for step-by-step examples

**Still confused about skills?**
→ Read [understanding-skills.md](understanding-skills.md) for basics

**Want to build agents?**
→ (For developers) See `docs/agent-development/`

---

**Remember:** Skills and agents are designed to work together OR separately. Use whichever fits your workflow!

---

**Last Updated:** November 17, 2025
**Difficulty:** Intermediate (assumes basic understanding)
**Estimated Reading Time:** 8 minutes
