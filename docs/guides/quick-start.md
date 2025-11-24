# Quick Start Guide

**Get started with Claude Skills Library in 5 minutes**

This guide will get you up and running with Pandora's SDLC skills quickly, whether you're using Claude AI or Claude Code.

---

## Table of Contents

- [For Claude AI Users](#for-claude-ai-users)
- [For Claude Code Users](#for-claude-code-users)
- [Example Workflows](#example-workflows)
- [Next Steps](#next-steps)

---

## For Claude AI Users

Use skills to enhance your Claude AI conversations with specialized expertise.

### Method 1: Upload Skill Documentation (Recommended)

**Step 1:** Navigate to the skill you need
```bash
# Example: Architecture skill for Pandora's codebase
cd skills/engineering-team/senior-architect/
```

**Step 2:** Upload SKILL.md to Claude AI
- Click the attachment icon 📎
- Select `SKILL.md` from the skill folder
- Upload to your conversation

**Step 3:** Reference the skill in your prompts
```
Using the senior-architect skill, help me:
- Analyze our microservices architecture
- Create an ADR for our API gateway decision
- Review our system design for scalability issues
```

### Method 2: Clone and Reference

**Step 1:** Clone the repository
```bash
git clone https://github.com/rickydwilson-dcs/claude-skills.git
cd claude-skills
```

**Step 2:** Reference skills in prompts
```
I have the Claude Skills Library available.
Using the senior-security skill, audit this codebase for OWASP Top 10 vulnerabilities.
```

---

## For Claude Code Users

Integrate skills directly into your development workflow.

### Setup (One-Time)

**Step 1:** Clone the repository
```bash
cd ~/projects  # or your preferred location
git clone https://github.com/rickydwilson-dcs/claude-skills.git
cd claude-skills
```

**Step 2:** Verify Python installation
```bash
python3 --version  # Should be 3.8 or higher
```

**Step 3:** Test a skill tool
```bash
# Test architecture analyzer
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --help

# Test security auditor
python3 skills/engineering-team/senior-security/scripts/security_auditor.py --help

# Test RICE prioritizer
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py --help
```

### Usage Patterns

#### Pattern 1: Run Analysis Tools Directly

```bash
# Architecture review of Pandora's codebase
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . --verbose

# Security audit
python3 skills/engineering-team/senior-security/scripts/security_auditor.py --input . --output text --verbose

# Feature prioritization
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20
```

#### Pattern 2: Use Agents for Guided Workflows

```markdown
In Claude Code, reference an agent:

@cs-architect analyze the architecture of this codebase and provide recommendations

@cs-security-engineer run a comprehensive security audit focusing on authentication

@cs-product-manager help me prioritize these 15 feature requests using RICE
```

#### Pattern 3: Integrate into Your Workflow

```bash
# Create alias for frequent use
echo 'alias arch-review="python3 ~/claude-skills/skills/engineering-team/senior-architect/scripts/project_architect.py"' >> ~/.bashrc
source ~/.bashrc

# Now just run:
arch-review --input . --verbose
```

---

## Example Workflows

### Workflow 1: Architecture Review (15 minutes)

**Scenario:** Review Pandora's microservices architecture before a major release

```bash
# Step 1: Run architecture analyzer (30 seconds)
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --verbose > architecture-report.md

# Step 2: Review findings (10 minutes)
# - Check architecture score
# - Review detected patterns
# - Identify issues and recommendations

# Step 3: Create ADR for key decisions (5 minutes)
cp skills/engineering-team/senior-architect/assets/adr-template.md \
  docs/architecture/ADR-001-microservices-communication.md
# Edit ADR with findings
```

**Output:**
- Architecture analysis report
- Actionable recommendations
- ADR documentation
- **Time saved:** 3.75 hours (vs manual review)

---

### Workflow 2: Security Audit (10 minutes)

**Scenario:** Run OWASP Top 10 security scan on Pandora's authentication service

```bash
# Step 1: Run security auditor (45 seconds)
python3 skills/engineering-team/senior-security/scripts/security_auditor.py \
  --input src/auth --output text --verbose > security-audit.md

# Step 2: Review vulnerabilities (5 minutes)
# - Check OWASP Top 10 issues
# - Review exposed secrets
# - Identify weak cryptography

# Step 3: Fix critical issues (5 minutes)
# Follow recommendations from audit output
```

**Output:**
- Security audit report with severity ratings
- Specific file/line locations for issues
- Remediation recommendations
- **Time saved:** 2.75 hours (vs manual audit)

---

### Workflow 3: Feature Prioritization (15 minutes)

**Scenario:** Prioritize 30 feature requests for Pandora's Q1 roadmap

```bash
# Step 1: Create features CSV (5 minutes)
cat > features.csv << 'EOF'
feature,reach,impact,confidence,effort
SSO Integration,1000,3,0.9,8
Dark Mode,500,1,1.0,2
Mobile App,2000,3,0.7,13
Dashboard Analytics,800,2,0.8,5
API Rate Limiting,1200,2,0.9,3
EOF

# Step 2: Run RICE prioritizer (5 seconds)
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  features.csv --capacity 20 > priorities.md

# Step 3: Review recommendations (10 minutes)
# - Check RICE scores
# - Review Quick Wins vs Big Bets
# - Validate against capacity
```

**Output:**
- Prioritized feature list with RICE scores
- Portfolio analysis (Quick Wins, Big Bets, Fill-Ins, Money Pits)
- Quarterly roadmap recommendations
- **Time saved:** 3.5 hours (vs manual spreadsheet work)

---

### Workflow 4: User Story Generation (10 minutes)

**Scenario:** Generate user stories for Pandora's authentication epic

```bash
# In Claude Code:
@cs-agile-product-owner

Generate user stories for our authentication feature:
- Epic: User Authentication System
- Sprint capacity: 30 story points
- Must include: Login, signup, password reset, 2FA
```

**Output:**
- 8-10 well-formed user stories
- Acceptance criteria for each story
- Story point estimates
- Technical dependencies identified
- **Time saved:** 1.75 hours (vs manual story writing)

---

## Next Steps

### Learn More

- **Skills Catalog** - [docs/SKILLS_CATALOG.md](SKILLS_CATALOG.md) - Browse all 42 skills
- **Agents Catalog** - [docs/AGENTS_CATALOG.md](AGENTS_CATALOG.md) - Explore 27 workflow agents
- **Usage Guide** - [docs/USAGE.md](USAGE.md) - Detailed examples and patterns
- **Installation** - [docs/INSTALL.md](INSTALL.md) - Complete setup instructions

### Try These Skills

**For Architects:**
- [senior-architect](../skills/engineering-team/senior-architect/SKILL.md) - Architecture analysis and system design

**For Security Engineers:**
- [senior-security](../skills/engineering-team/senior-security/SKILL.md) - Security auditing and vulnerability scanning

**For Product Managers:**
- [product-manager-toolkit](../skills/product-team/product-manager-toolkit/SKILL.md) - RICE prioritization and customer discovery

**For Engineers:**
- [senior-fullstack](../skills/engineering-team/senior-fullstack/SKILL.md) - Full-stack development and scaffolding

### Get Help

- **Questions?** [GitHub Discussions](https://github.com/rickydwilson-dcs/claude-skills/discussions)
- **Bug Reports?** [GitHub Issues](https://github.com/rickydwilson-dcs/claude-skills/issues)
- **Contributing?** [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## Common Questions

**Q: Do I need to install dependencies?**
A: No! All Python tools use Python 3.8+ standard library only. No pip install required.

**Q: Can I use skills without cloning the repository?**
A: Yes! Just download the skill folder you need and upload SKILL.md to Claude AI.

**Q: Which skills should I start with?**
A: Start with skills for your role:
- **Architects:** senior-architect
- **Security:** senior-security
- **Product:** product-manager-toolkit
- **Engineers:** senior-fullstack or your specific domain

**Q: Can I use multiple skills together?**
A: Absolutely! For example, use cs-architect + cs-security-engineer for comprehensive codebase review.

**Q: How do I update skills?**
A: Run `git pull origin main` in the claude-skills directory to get the latest updates.

---

**Last Updated:** November 17, 2025
**Time to Complete:** 5 minutes setup + 10-15 minutes per workflow
**Prerequisites:** Python 3.8+ (for Python tools) or Claude AI account
