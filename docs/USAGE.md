# Usage Guide

**Comprehensive examples and workflows for using Claude Skills Library with Claude AI and Claude Code**

This guide provides detailed usage examples focused on Pandora's software delivery lifecycle (SDLC) - architecture, security, product management, and engineering excellence.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Using Skills Directly](#using-skills-directly)
- [Using Agents](#using-agents)
- [Multi-Agent Workflows](#multi-agent-workflows)
- [CLI Tool Usage](#cli-tool-usage)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Tips & Tricks](#tips--tricks)

---

## Quick Start

### Option 1: Use a Skill Directly (Claude AI)

```markdown
I need help with architecture review.

Please use the Senior Architect skill located at:
skills/engineering-team/senior-architect/SKILL.md

Analyze my microservices architecture and identify scalability issues.
```

### Option 2: Use an Agent (Claude Code)

```markdown
@cs-architect

I need to review the architecture of this codebase before our major release.
Focus on microservices patterns, dependencies, and scalability.
```

### Option 3: Use CLI Tools

```bash
# Architecture analysis
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --verbose

# Security audit
python3 skills/engineering-team/senior-security/scripts/security_auditor.py \
  --input . --output text --verbose

# Feature prioritization
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  features.csv --capacity 20
```

---

## Using Skills Directly

### With Claude AI

Skills can be used in any Claude AI conversation by referencing the skill documentation.

#### Example 1: Architecture Analysis

```markdown
Please reference the Senior Architect skill:
File: skills/engineering-team/senior-architect/SKILL.md

Analyze this codebase architecture:

[Describe your system or paste relevant code]

Provide:
1. Architecture pattern identification
2. Dependency analysis
3. Scalability recommendations
4. ADR template for key decisions
```

#### Example 2: Security Audit

```markdown
Use the Senior Security skill:
File: skills/engineering-team/senior-security/SKILL.md

Audit this authentication module for security vulnerabilities:

[Paste authentication code]

Check for:
1. OWASP Top 10 vulnerabilities
2. Weak cryptography
3. Exposed secrets
4. Input validation issues
```

#### Example 3: Feature Prioritization

```markdown
Reference the Product Manager Toolkit skill:
File: skills/product-team/product-manager-toolkit/SKILL.md

I need to prioritize these features using RICE scoring:

1. SSO Integration - 1000 users/month, high impact, confident, 8 weeks
2. Dark Mode - 500 users/month, low impact, certain, 2 weeks
3. Mobile App - 2000 users/month, high impact, uncertain, 13 weeks

Provide RICE scores and recommend priority.
```

---

## Using Agents

Agents provide guided workflows and orchestrate skills automatically.

### Available Agents

| Agent | Best For | Example Use Case |
|-------|----------|------------------|
| `cs-architect` | Architecture design | "Review our microservices architecture" |
| `cs-security-engineer` | Security auditing | "Scan for OWASP Top 10 vulnerabilities" |
| `cs-product-manager` | Product decisions | "Prioritize our roadmap with RICE" |
| `cs-fullstack-engineer` | Full-stack dev | "Scaffold a Next.js + GraphQL project" |
| `cs-cto-advisor` | Technical leadership | "Assess our tech debt" |

### Agent Invocation Examples

#### Architecture Agent: System Design Review

```markdown
@cs-architect

Review the architecture of this microservices application:

Context:
- 12 microservices communicating via REST + message queue
- PostgreSQL for each service (no shared DB)
- Redis for caching
- Docker + Kubernetes deployment
- 50K active users, targeting 500K by EOY

Concerns:
- Service communication patterns
- Data consistency
- Scalability bottlenecks
- Tech debt areas
```

**What the agent does:**
1. Runs `project_architect.py` to analyze codebase structure
2. Identifies architecture patterns (microservices, event-driven, etc.)
3. Analyzes dependencies with `dependency_analyzer.py`
4. Reviews data flow and service boundaries
5. Identifies scalability concerns
6. Provides ADR templates for key decisions
7. Creates C4 diagram recommendations

---

#### Security Agent: Comprehensive Audit

```markdown
@cs-security-engineer

Run a comprehensive security audit on this web application:

Context:
- Node.js + Express backend
- React frontend
- PostgreSQL database
- User authentication with JWT
- File upload functionality
- API integrations with 3rd parties

Focus on:
- OWASP Top 10 vulnerabilities
- Authentication/authorization flaws
- Input validation
- Exposed secrets
```

**What the agent does:**
1. Runs `security_auditor.py` for OWASP Top 10 scan
2. Checks for exposed secrets in codebase
3. Analyzes authentication implementation
4. Reviews input validation patterns
5. Scans dependencies with `dependency_scanner.py`
6. Identifies weak cryptography
7. Provides prioritized remediation plan

---

#### Product Agent: RICE Prioritization

```markdown
@cs-product-manager

Prioritize our Q1 feature backlog using RICE framework:

Features:
1. SSO Integration (SAML + OAuth)
2. Advanced Analytics Dashboard
3. Mobile App (iOS + Android)
4. API Rate Limiting
5. Dark Mode UI Theme
6. Export to PDF functionality
7. Real-time Collaboration
8. Custom Integrations (Zapier)

Context:
- Team capacity: 20 person-months
- Strategic goal: Enterprise readiness
- Current users: 5000 companies
```

**What the agent does:**
1. Guides you through RICE scoring for each feature
2. Runs `rice_prioritizer.py` with your inputs
3. Analyzes portfolio (Quick Wins vs Big Bets)
4. Considers strategic alignment
5. Generates prioritized roadmap
6. Provides stakeholder communication templates
7. Creates PRD templates for top features

---

#### Fullstack Agent: Project Scaffolding

```markdown
@cs-fullstack-engineer

Scaffold a new SaaS application with these requirements:

Stack:
- Frontend: Next.js 14 with TypeScript
- Backend: tRPC for type-safe APIs
- Database: PostgreSQL with Prisma ORM
- Authentication: NextAuth.js with multiple providers
- Styling: Tailwind CSS + Shadcn UI

Features needed:
- User authentication (email + Google OAuth)
- Role-based access control
- Subscription management (Stripe)
- Admin dashboard
- API for mobile app
```

**What the agent does:**
1. Runs `project_scaffolder.py` with specified stack
2. Creates complete project structure
3. Configures authentication with NextAuth.js
4. Sets up database schema with Prisma
5. Creates tRPC router scaffolding
6. Implements RBAC middleware
7. Provides README with setup instructions

---

#### CTO Agent: Tech Debt Assessment

```markdown
@cs-cto-advisor

Assess our technical debt and provide a mitigation strategy:

Context:
- Rails monolith, 5 years old
- 100K LOC, 15 engineers
- User growth: 50K → 500K (10x target)
- Pain points:
  - Slow deploys (45 minutes)
  - Frequent outages during peak
  - Difficulty onboarding new engineers
  - Feature velocity declining

Goals:
- Improve deployment speed
- Increase reliability (99.9% uptime)
- Scale to 500K users
- Maintain feature velocity
```

**What the agent does:**
1. Runs `tech_debt_analyzer.py` to quantify debt
2. Analyzes architectural bottlenecks
3. Calculates team scaling needs with `team_capacity_planner.py`
4. Proposes migration strategy (monolith → microservices)
5. Estimates effort and timeline
6. Creates phased implementation roadmap
7. Provides DORA metrics tracking framework

---

## Multi-Agent Workflows

Combine multiple agents for complex workflows.

### Workflow 1: Product Launch (3 Agents)

```markdown
# Step 1: Technical Review (@cs-architect)
@cs-architect review the architecture for this new feature before launch

# Step 2: Security Check (@cs-security-engineer)
@cs-security-engineer audit the feature for security vulnerabilities

# Step 3: Feature Prioritization (@cs-product-manager)
@cs-product-manager prioritize post-launch enhancements based on feedback
```

---

### Workflow 2: Codebase Health Check (2 Agents)

```markdown
# Step 1: Architecture Analysis (@cs-architect)
@cs-architect analyze the codebase structure and identify architectural issues

# Step 2: Security Audit (@cs-security-engineer)
@cs-security-engineer scan for OWASP Top 10 and dependency vulnerabilities
```

---

### Workflow 3: Sprint Planning (2 Agents)

```markdown
# Step 1: Feature Prioritization (@cs-product-manager)
@cs-product-manager prioritize backlog items using RICE

# Step 2: Story Generation (@cs-agile-product-owner)
@cs-agile-product-owner generate user stories for the top 5 prioritized features
```

---

## CLI Tool Usage

### Basic Patterns

#### Pattern 1: Analyze → Report → Act

```bash
# Step 1: Run analysis
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --verbose --output json > analysis.json

# Step 2: Review results
cat analysis.json | python3 -m json.tool

# Step 3: Act on findings
# Create ADRs, refactor code, update documentation
```

#### Pattern 2: Batch Processing

```bash
# Analyze multiple services
for service in services/*; do
  echo "Analyzing $service..."
  python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
    --input "$service" --verbose > "reports/$(basename $service)-analysis.md"
done
```

#### Pattern 3: CI/CD Integration

```bash
# In GitHub Actions or Jenkins pipeline
python3 skills/engineering-team/senior-security/scripts/security_auditor.py \
  --input . --output json | \
  jq '.security_score' | \
  awk '{if ($1 < 7.0) exit 1}'  # Fail if security score < 7.0
```

### Advanced Usage

#### Using Multiple Output Formats

```bash
# Human-readable output
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --verbose

# Machine-readable output (for scripts)
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --output json > architecture.json

# CSV export (for spreadsheets)
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  features.csv --output csv > priorities.csv
```

#### Verbose Mode for Debugging

```bash
# See detailed execution
python3 skills/engineering-team/senior-security/scripts/security_auditor.py \
  --input . --verbose --output text
```

---

## Best Practices

### 1. Start with Agents for Complex Tasks

```markdown
# Good: Use agent for multi-step workflow
@cs-architect guide me through architecture review process

# Also Good: Use skill directly for quick analysis
[Use senior-architect skill to check architecture patterns]
```

### 2. Provide Detailed Context

```markdown
# Good: Rich context
@cs-security-engineer audit this authentication system

Context:
- Node.js + Express backend
- JWT token authentication
- Password reset via email
- OAuth integration (Google, GitHub)
- User roles: admin, user, viewer

Focus:
- Token security (expiration, refresh, revocation)
- Password storage (bcrypt configuration)
- OAuth implementation (state parameter, PKCE)
- Session management

# Less Effective: Minimal context
@cs-security-engineer check the auth code
```

### 3. Iterate with Feedback

```markdown
# First attempt
@cs-architect review this microservices architecture

# Provide feedback after initial review
The analysis is helpful. Please dive deeper into:
1. Service communication patterns (sync vs async)
2. Data consistency strategies
3. Service discovery mechanism
```

### 4. Combine Tools and Knowledge

```markdown
@cs-architect

1. Run project_architect.py to analyze the codebase
2. Review architecture patterns from knowledge base
3. Create ADR for the API gateway decision
4. Generate C4 diagrams for documentation
```

### 5. Save and Reuse Workflows

```markdown
# Save successful workflows as templates
# Example: Weekly Architecture Health Check

@cs-architect
Run weekly architecture analysis:
1. Analyze codebase with project_architect.py
2. Check for new circular dependencies
3. Review any new architectural decisions
4. Update architecture documentation
```

---

## Common Patterns

### Pattern 1: Weekly Codebase Health Check

```bash
#!/bin/bash
# weekly-health-check.sh

# Architecture analysis
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --verbose > reports/architecture-$(date +%Y-%m-%d).md

# Security audit
python3 skills/engineering-team/senior-security/scripts/security_auditor.py \
  --input . --verbose > reports/security-$(date +%Y-%m-%d).md

# Email results
cat reports/*-$(date +%Y-%m-%d).md | mail -s "Weekly Health Check" team@pandora.com
```

### Pattern 2: Pre-Release Checklist

```markdown
@cs-architect @cs-security-engineer @cs-qa-engineer

Pre-release checklist for v2.0:

1. Architecture review
   - Run project_architect.py
   - Verify no new circular dependencies
   - Check scalability for 10x user growth

2. Security audit
   - Run security_auditor.py
   - Scan dependencies for CVEs
   - Verify no exposed secrets

3. Quality assurance
   - Test coverage > 80%
   - All integration tests passing
   - Performance benchmarks met
```

### Pattern 3: Feature Development Workflow

```markdown
# Step 1: User Story (@cs-agile-product-owner)
@cs-agile-product-owner
Generate user stories for SSO integration feature

# Step 2: Technical Design (@cs-architect)
@cs-architect
Design system architecture for SSO integration

# Step 3: Implementation (@cs-fullstack-engineer)
@cs-fullstack-engineer
Scaffold SSO integration code with NextAuth.js

# Step 4: Security Review (@cs-security-engineer)
@cs-security-engineer
Audit SSO implementation for security issues

# Step 5: Documentation (@cs-confluence-expert)
@cs-confluence-expert
Create user guide for SSO configuration
```

---

## Tips & Tricks

### Efficiency Tips

**1. Create Aliases**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias arch-review='python3 ~/claude-skills/skills/engineering-team/senior-architect/scripts/project_architect.py'
alias sec-audit='python3 ~/claude-skills/skills/engineering-team/senior-security/scripts/security_auditor.py'
alias rice='python3 ~/claude-skills/skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py'

# Usage
arch-review --input . --verbose
sec-audit --input src/auth --verbose
rice features.csv --capacity 20
```

**2. Save Common Prompts**
```markdown
# Save as templates/architecture-review.md
@cs-architect

Review this codebase architecture:
- Analyze structure and patterns
- Identify circular dependencies
- Check for scalability issues
- Provide recommendations with priority

Output:
- Architecture analysis report
- Top 3 recommendations
- ADR templates for decisions
```

**3. Chain Commands**
```bash
# Architecture + Security audit in one command
arch-review --input . --verbose && sec-audit --input . --verbose
```

### Quality Tips

**1. Always Provide Context**
- Project/system description
- Tech stack and architecture
- Specific concerns or goals
- Constraints (time, resources, compliance)

**2. Use Verbose Mode When Learning**
```bash
# See detailed analysis steps
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --verbose
```

**3. Validate Results**
```bash
# Verify JSON output is valid
python3 script.py --output json | python3 -m json.tool
```

### Collaboration Tips

**1. Share Agent Workflows**
```markdown
# Document team-proven workflows in wiki
Team Workflows:
- Architecture Review: @cs-architect workflow
- Security Audit: @cs-security-engineer workflow
- Sprint Planning: @cs-product-manager + @cs-agile-product-owner workflow
```

**2. Export for Sharing**
```bash
# CSV for stakeholders
rice features.csv --output csv --file priorities.csv

# JSON for automation
sec-audit --input . --output json > security-report.json
```

**3. Version Control Inputs**
```bash
git add features.csv architecture-decisions/
git commit -m "Q1 2026 feature prioritization inputs"
```

---

## Getting Help

### Documentation

- **Skills Catalog:** [SKILLS_CATALOG.md](SKILLS_CATALOG.md) - All 42 skills
- **Agents Catalog:** [AGENTS_CATALOG.md](AGENTS_CATALOG.md) - All 27 agents
- **Quick Start:** [QUICK_START.md](QUICK_START.md) - Get started in 5 minutes
- **Installation:** [INSTALL.md](INSTALL.md) - Setup guide
- **CLI Standards:** [standards/cli-standards.md](standards/cli-standards.md)

### Support Channels

- **Questions:** [GitHub Discussions](https://github.com/rickydwilson-dcs/claude-skills/discussions)
- **Bug Reports:** [GitHub Issues](https://github.com/rickydwilson-dcs/claude-skills/issues)
- **Contributing:** [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## Next Steps

1. **Try the examples** in this guide
2. **Explore agent workflows** - [AGENTS_CATALOG.md](AGENTS_CATALOG.md)
3. **Review skill documentation** - [SKILLS_CATALOG.md](SKILLS_CATALOG.md)
4. **Share workflows** with your team
5. **Contribute improvements** via pull requests

---

**Last Updated:** November 17, 2025
**Focus:** Pandora's SDLC (Architecture, Security, Product, Engineering)
**Compatible With:** Claude AI, Claude Code, Python 3.8+
