# Quickstart: Agent Creation Workflow

**Date**: November 12, 2025
**Purpose**: Step-by-step guide to create new agents following validated patterns

## Prerequisites

Before creating a new agent:

1. **Skill package exists** - Skill must be in `skills/domain-team/skill-name/` directory
2. **Research complete** - Skill analysis done (tools, references, workflows identified)
3. **Template available** - `templates/agent-template.md` ready to use
4. **Domain directory exists** - `agents/delivery/` and `agents/engineering/` created

## Agent Creation Process

### Step 1: Identify Skill and Domain

**Determine:**
- Skill location: `skills/domain-team/skill-name/`
- Agent domain: `marketing`, `product`, `engineering`, or `delivery`
- Agent name: `cs-{role-name}`

**Example:**
```bash
# For senior-backend skill:
Skill location: skills/engineering-team/senior-backend/
Agent domain: engineering
Agent name: cs-backend-engineer
```

### Step 2: Copy Agent Template

```bash
# Navigate to repository root
cd /path/to/claude-skills

# Copy template to correct domain directory
cp templates/agent-template.md agents/{domain}/cs-{agent-name}.md

# Examples:
cp templates/agent-template.md agents/delivery/cs-jira-expert.md
cp templates/agent-template.md agents/engineering/cs-backend-engineer.md
```

### Step 3: Update YAML Frontmatter

Open the new agent file and update the YAML frontmatter:

```yaml
---
name: cs-agent-name              # Replace with actual agent name (kebab-case)
description: One-line description # Under 150 characters, specific outcome focus
skills: skill-folder-name        # Exact skill folder name (NOT full path)
domain: domain-name              # marketing|product|engineering|delivery
model: sonnet                    # Use 'sonnet' for production agents
tools: [Read, Write, Bash, Grep, Glob]  # Standard tool set
---
```

**Example for cs-backend-engineer:**
```yaml
---
name: cs-backend-engineer
description: Backend development specialist for API design, database optimization, and system architecture
skills: senior-backend
domain: engineering
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
---
```

**Field Reference:**
- **name:** `cs-` + role in kebab-case
- **description:** Focus on outcomes, under 150 chars
- **skills:** Just folder name (`senior-backend`, NOT `skills/engineering-team/senior-backend`)
- **domain:** Must match where skill is located
- **model:** Always `sonnet` for production
- **tools:** Always this exact array

### Step 4: Write Purpose Section

Replace template placeholders with 2-3 paragraphs:

**Paragraph 1 - What:**
```markdown
The cs-{agent-name} agent orchestrates the {skill-name} skill package to [primary function].
This agent [core capabilities overview].
```

**Paragraph 2 - Who:**
```markdown
This agent is designed for [target users, roles, job titles] who [pain points addressed].
By leveraging [tools/frameworks], the agent enables [what they can do without].
```

**Paragraph 3 - Value:**
```markdown
The cs-{agent-name} agent bridges the gap between [problem A] and [problem B],
ensuring [outcome]. It provides [specific benefits delivered].
```

**Length:** 150-250 words total

### Step 5: Document Skill Integration

#### 5a. Update Skill Location Path

```markdown
**Skill Location:** `../../skills/domain-team/skill-name/`
```

**Examples:**
- Delivery: `../../skills/delivery-team/jira-expert/`
- Engineering: `../../skills/engineering-team/senior-backend/`

#### 5b. Document Python Tools

For each Python tool in `skills/domain-team/skill-name/scripts/`:

```bash
# First, list tools in the skill
ls skills/domain-team/skill-name/scripts/

# Then document each tool:
```

```markdown
1. **Tool Name**
   - **Purpose:** One-sentence description of what tool does
   - **Path:** `../../skills/domain-team/skill-name/scripts/tool_name.py`
   - **Usage:** `python ../../skills/domain-team/skill-name/scripts/tool_name.py [arguments]`
   - **Features:**
     - Feature 1 (from tool --help or SKILL.md)
     - Feature 2
     - Feature 3
   - **Use Cases:** When to use this tool
```

**How to get tool information:**
```bash
# Run tool with --help to see features
python skills/domain-team/skill-name/scripts/tool_name.py --help

# Or check SKILL.md for tool documentation
cat skills/domain-team/skill-name/SKILL.md
```

#### 5c. Document Knowledge Bases

For each reference in `skills/domain-team/skill-name/references/`:

```bash
# List references
ls skills/domain-team/skill-name/references/

# Document each:
```

```markdown
1. **Reference Name**
   - **Location:** `../../skills/domain-team/skill-name/references/reference_file.md`
   - **Content:** Summary of frameworks/knowledge in this file
   - **Use Case:** When to consult this reference
```

**How to summarize references:**
```bash
# Read first 50 lines to understand content
head -50 skills/domain-team/skill-name/references/reference_file.md
```

#### 5d. Document Templates

For each template in `skills/domain-team/skill-name/assets/`:

```bash
# List templates
ls skills/domain-team/skill-name/assets/

# Document each:
```

```markdown
1. **Template Name**
   - **Location:** `../../skills/domain-team/skill-name/assets/template.md`
   - **Use Case:** When users would customize and use this
```

### Step 6: Create 4 Workflows

#### Workflow Types to Include:

1. **Primary Use Case** (Workflow 1)
   - Most common scenario
   - Single tool focus
   - Clear entry point for new users

2. **Advanced Use Case** (Workflow 2)
   - Complex scenario
   - Multiple tool integration
   - For experienced users

3. **Integration Use Case** (Workflow 3)
   - Cross-functional workflow
   - Tool orchestration
   - Combines multiple capabilities

4. **Automation Use Case** (Workflow 4)
   - Scriptable workflow
   - Batch processing
   - Ongoing automation

#### Workflow Structure (5 Required Fields):

```markdown
### Workflow X: [Descriptive Name]

**Goal:** One-sentence outcome description

**Steps:**
1. **[Action Verb + Object]** - Clear description
   ```bash
   # Optional command example
   python ../../skills/domain-team/skill-name/scripts/tool.py input
   ```
2. **[Action Verb + Object]** - Clear description
3. **[Action Verb + Object]** - Clear description
4. **[Action Verb + Object]** - Clear description
5. **[Action Verb + Object]** - Clear description

**Expected Output:** Concrete deliverable or measurable result

**Time Estimate:** Realistic duration (e.g., "2-3 hours", "30-45 minutes")

**Example:**
```bash
# Complete workflow example with real commands
cd /path/to/project
python ../../skills/domain-team/skill-name/scripts/tool.py input.txt
# Review output
```
```

**How to identify workflows:**
```bash
# Check SKILL.md for documented workflows
cat skills/domain-team/skill-name/SKILL.md | grep -A 20 "## Workflows"

# Or analyze tool purposes to create logical workflows
python skills/domain-team/skill-name/scripts/tool1.py --help
python skills/domain-team/skill-name/scripts/tool2.py --help
python skills/domain-team/skill-name/scripts/tool3.py --help
```

### Step 7: Create Integration Examples

Provide 3 concrete bash script examples:

**Example 1: Daily/Weekly Automation**
```markdown
### Example 1: Daily Security Scan

```bash
#!/bin/bash
# daily-security-scan.sh - Automated daily security scanning

DATE=$(date +%Y-%m-%d)
PROJECT_PATH=$1

echo "🔒 Security Scan for $DATE"

# Run security scanner
python ../../skills/engineering-team/senior-secops/scripts/security_scanner.py "$PROJECT_PATH"

# Generate report
echo "✅ Scan complete. Review output above."
```
```

**Example 2: Multi-Tool Workflow**
```markdown
### Example 2: Complete Security Audit

```bash
# Multi-step security workflow

# Step 1: Scan for vulnerabilities
python ../../skills/engineering-team/senior-secops/scripts/security_scanner.py /app

# Step 2: Assess critical findings
python ../../skills/engineering-team/senior-secops/scripts/vulnerability_assessor.py /app

# Step 3: Check compliance
python ../../skills/engineering-team/senior-secops/scripts/compliance_checker.py /app
```
```

**Example 3: Output Processing**
```markdown
### Example 3: Automated Report Generation

```bash
# Generate and process security reports

# Run scan with JSON output
python ../../skills/engineering-team/senior-secops/scripts/security_scanner.py /app --output json > scan-results.json

# Process results (custom logic)
cat scan-results.json | jq '.findings[] | select(.severity=="critical")'
```
```

### Step 8: Define Success Metrics

Create 3-4 metric categories based on domain:

**Delivery Domain:**
```markdown
## Success Metrics

**Efficiency:**
- **Sprint Velocity:** 20% increase in story points completed
- **Cycle Time:** 30% reduction in issue-to-done time
- **Planning Time:** 50% reduction in sprint planning duration

**Collaboration Quality:**
- **Team Satisfaction:** 90% positive feedback on ceremonies
- **Documentation Clarity:** 95% of decisions documented in Confluence

**Delivery Predictability:**
- **Estimation Accuracy:** Within 10% of estimates 80% of time
- **Risk Identification:** 90% of impediments identified proactively
```

**Engineering Domain:**
```markdown
## Success Metrics

**Code Quality:**
- **Defect Reduction:** 40% fewer production bugs
- **Test Coverage:** Minimum 80% coverage maintained
- **Review Thoroughness:** 100% of PRs reviewed within 24 hours

**Development Velocity:**
- **Deployment Frequency:** 2x increase in deployments per week
- **Lead Time:** 50% reduction in feature-to-production time

**System Reliability:**
- **Uptime:** 99.9% availability maintained
- **Incident Response:** 30% faster mean time to resolution
```

### Step 9: Add Related Agents

Cross-reference 2-4 related agents:

```markdown
## Related Agents

- [cs-architect](cs-architect.md) - Provides system design that backend implements
- [cs-frontend-engineer](cs-frontend-engineer.md) - Consumes backend APIs
- [cs-devops-engineer](cs-devops-engineer.md) - Deploys backend services
- [cs-code-reviewer](cs-code-reviewer.md) - Reviews backend code quality
```

**Path patterns:**
- Same directory: `[cs-agent](cs-agent.md)`
- Different directory: `[cs-agent](../domain/cs-agent.md)`

### Step 10: Add Reference Links

Always include these 3 links:

```markdown
## References

- **Skill Documentation:** [../../skills/domain-team/skill-name/SKILL.md](../../skills/domain-team/skill-name/SKILL.md)
- **Domain Guide:** [../../skills/domain-team/CLAUDE.md](../../skills/domain-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)
```

### Step 11: Add Metadata Footer

```markdown
---

**Last Updated:** November 12, 2025
**Sprint:** sprint-11-12-2025 (Day 1)
**Status:** Production Ready
**Version:** 1.0
```

## Path Validation Checklist

After completing the agent, validate all paths:

```bash
# Navigate to agent directory
cd agents/domain/

# Test that skill location resolves
ls ../../skills/domain-team/skill-name/
# Should list: SKILL.md, scripts/, references/, assets/

# Test that Python tools resolve
ls ../../skills/domain-team/skill-name/scripts/*.py
# Should list all Python tools

# Test that references resolve
ls ../../skills/domain-team/skill-name/references/*.md
# Should list all reference files

# Test that templates resolve (if applicable)
ls ../../skills/domain-team/skill-name/assets/*.md
# Should list all templates

# Test Python tool execution
python ../../skills/domain-team/skill-name/scripts/tool_name.py --help
# Should display help text without errors
```

## Quality Validation Checklist

Before marking agent as complete:

**YAML Frontmatter:**
- [ ] All 6 required fields present
- [ ] `name` uses cs- prefix and kebab-case
- [ ] `description` under 150 characters
- [ ] `skills` matches skill folder name exactly
- [ ] `domain` matches skill location
- [ ] `model` is `sonnet`
- [ ] `tools` is `[Read, Write, Bash, Grep, Glob]`

**Purpose Section:**
- [ ] 2-3 paragraphs (150-250 words)
- [ ] Paragraph 1 explains what/which skill
- [ ] Paragraph 2 explains who/pain points
- [ ] Paragraph 3 explains value/outcomes

**Skill Integration:**
- [ ] Skill location path correct
- [ ] All Python tools documented (3 per skill, 2 for CTO)
- [ ] All references documented (4-5 per skill)
- [ ] All templates documented (if skill has templates)
- [ ] All paths use `../../skills/` pattern

**Workflows:**
- [ ] Exactly 4 workflows documented
- [ ] Each has Goal field
- [ ] Each has Steps field (4-7 steps)
- [ ] Each has Expected Output field
- [ ] Each has Time Estimate field
- [ ] Each has Example field (bash code block)

**Integration Examples:**
- [ ] 3 examples provided
- [ ] Each is a complete bash script
- [ ] Examples show real tool usage
- [ ] Examples include comments

**Success Metrics:**
- [ ] 3-4 metric categories
- [ ] Categories appropriate for domain
- [ ] Each metric has specific target
- [ ] Metrics are measurable

**Related Agents:**
- [ ] 2-4 agents cross-referenced
- [ ] Relationship explained for each
- [ ] Paths correct (relative from agent location)

**References:**
- [ ] All 3 required links present
- [ ] Skill documentation link correct
- [ ] Domain guide link correct
- [ ] Agent development guide link correct

**General:**
- [ ] No absolute paths used
- [ ] No hardcoded user directories
- [ ] Agent length 400-500 lines
- [ ] All markdown properly formatted
- [ ] No placeholder text remaining

## Path Testing Commands

### Test from Agent Location

```bash
# Navigate to specific agent
cd agents/delivery/
# Or: cd agents/engineering/

# Test skill package exists
ls ../../skills/delivery-team/jira-expert/
ls ../../skills/engineering-team/senior-backend/

# Test Python tools work
python ../../skills/delivery-team/jira-expert/scripts/tool.py --help
python ../../skills/engineering-team/senior-backend/scripts/api_generator.py --help

# Test references exist
cat ../../skills/delivery-team/jira-expert/references/reference.md
cat ../../skills/engineering-team/senior-backend/references/api-design.md

# Test skill documentation exists
cat ../../skills/delivery-team/jira-expert/SKILL.md
cat ../../skills/engineering-team/senior-backend/SKILL.md
```

### Test from Repository Root

```bash
# From repo root
cd /path/to/claude-skills

# Verify agent file structure
cat agents/delivery/cs-jira-expert.md | head -20
cat agents/engineering/cs-backend-engineer.md | head -20

# Extract and test paths
grep "../../skills/" agents/delivery/cs-jira-expert.md
grep "../../skills/" agents/engineering/cs-backend-engineer.md
```

## Common Mistakes to Avoid

### ❌ Wrong YAML Frontmatter

```yaml
# WRONG - includes full path in skills field
skills: skills/engineering-team/senior-backend

# WRONG - missing cs- prefix
name: backend-engineer

# WRONG - wrong model for production
model: opus
```

### ✅ Correct YAML Frontmatter

```yaml
# CORRECT
skills: senior-backend
name: cs-backend-engineer
model: sonnet
```

### ❌ Wrong Path Patterns

```markdown
<!-- WRONG - absolute path -->
**Path:** `/Users/name/claude-skills/skills/engineering-team/senior-backend/scripts/tool.py`

<!-- WRONG - missing ../../ -->
**Path:** `skills/engineering-team/senior-backend/scripts/tool.py`

<!-- WRONG - wrong skill reference in YAML -->
skills: engineering-team/senior-backend
```

### ✅ Correct Path Patterns

```markdown
<!-- CORRECT - relative from agent location -->
**Path:** `../../skills/engineering-team/senior-backend/scripts/tool.py`

<!-- CORRECT - skill folder name only in YAML -->
skills: senior-backend
```

### ❌ Incomplete Workflows

```markdown
<!-- WRONG - missing required fields -->
### Workflow 1: Backend Setup

**Steps:**
1. Run tool
2. Review output
```

### ✅ Complete Workflows

```markdown
<!-- CORRECT - all 5 fields present -->
### Workflow 1: Backend API Scaffolding

**Goal:** Generate production-ready REST API structure with authentication

**Steps:**
1. **Initialize Project** - Create project directory structure
2. **Generate API** - Run API generator tool
3. **Configure Authentication** - Set up JWT auth
4. **Add Database** - Configure database connection
5. **Test Endpoints** - Verify API responds correctly

**Expected Output:** Fully scaffolded API with 5+ endpoints and auth

**Time Estimate:** 45-60 minutes

**Example:**
```bash
mkdir my-api && cd my-api
python ../../skills/engineering-team/senior-backend/scripts/api_generator.py --auth jwt
python -m pytest tests/
```
```

## Tips for Efficient Agent Creation

1. **Start with similar agent** - Copy structure from existing agent in same domain
2. **Batch similar sections** - Document all tools first, then all references
3. **Use skill SKILL.md** - Most information already documented in skill file
4. **Test paths early** - Validate paths in Step 11 before writing workflows
5. **Use real commands** - Run actual Python tools to create authentic examples
6. **Review existing agents** - Check [agents/marketing/cs-content-creator.md](../../agents/marketing/cs-content-creator.md) for reference

---

**Last Updated:** November 12, 2025
**Purpose:** Step-by-step guide for creating production-ready agents
**Estimated Time:** 2-3 hours per agent following this process
