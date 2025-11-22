---
name: cto-advisor
description: Technical leadership guidance for engineering teams, architecture decisions, and technology strategy. Includes tech debt analyzer, team scaling calculator, engineering metrics frameworks, technology evaluation tools, and ADR templates. Use when assessing technical debt, scaling engineering teams, evaluating technologies, making architecture decisions, establishing engineering metrics, or when user mentions CTO, tech debt, technical debt, team scaling, architecture decisions, technology evaluation, engineering metrics, DORA metrics, or technology strategy.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: executive-advisory
  domain: cto
  updated: 2025-11-08
  keywords:
    - technical leadership
    - tech debt management
    - team scaling
    - architecture decisions
    - engineering metrics
    - DORA metrics
    - technology strategy
    - engineering excellence
    - infrastructure planning
    - team structure
    - hiring strategy
    - vendor evaluation
    - technology selection
    - CI/CD optimization
    - system design
    - microservices architecture
    - cloud migration
    - engineering culture
    - performance optimization
    - security governance
  tech-stack:
    - architecture tools
    - metrics platforms
    - monitoring systems
    - CI/CD systems
    - project management tools
    - development platforms
    - engineering dashboards
  python-tools:
    - tech_debt_analyzer.py
    - team_scaling_calculator.py
---

# CTO Advisor

## Key Workflows

### Workflow 1: [Workflow Name]

**Time:** [Duration estimate]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Output:** [What success looks like]

### Workflow 2: [Workflow Name]

**Time:** [Duration estimate]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Output:** [What success looks like]


Technical leadership guidance for engineering teams, architecture decisions, and technology strategy.

## Overview

The CTO Advisor skill provides comprehensive frameworks, tools, and templates for technical leadership excellence. It combines technology strategy methodologies, team scaling frameworks, architecture governance patterns, and engineering metrics to support CTOs in building world-class engineering organizations.

This skill addresses the full scope of CTO responsibilities: defining technology vision and roadmap, scaling engineering teams effectively, establishing architecture standards, managing vendor relationships, and driving engineering excellence through metrics and culture. All content is designed for immediate application in quarterly planning, architecture reviews, hiring initiatives, and engineering transformation programs.

## Core Capabilities

**Technology Strategy & Planning**
- 3-5 year technology vision development
- Quarterly roadmap planning and execution
- Innovation management frameworks
- Technical debt assessment and reduction
- Python-based tech debt analyzer tool

**Team Scaling & Development**
- Engineering team scaling strategies
- Hiring velocity and pipeline planning
- Performance management frameworks
- Engineering culture building
- Python-based team scaling calculator

**Architecture Governance**
- Architecture Decision Records (ADR) templates
- Technology standards and guidelines
- System design review processes
- Vendor evaluation frameworks
- Build vs buy analysis

**Engineering Excellence**
- DORA metrics implementation
- Quality metrics tracking
- Team health indicators
- Incident management processes
- Post-mortem frameworks

**Stakeholder Management**
- Board and executive reporting
- Cross-functional partnerships
- Strategic initiative planning
- Crisis management playbooks
- Communication templates

## Quick Start

### Technical Debt Assessment

```bash
# Analyze technical debt across 5 categories with prioritized reduction plan
python scripts/tech_debt_analyzer.py system_data.json

# Generate JSON output for executive dashboards
python scripts/tech_debt_analyzer.py system_data.json --output json -f debt_report.json

# View help and input schema
python scripts/tech_debt_analyzer.py --help
```

See [references/tools.md](references/tools.md) for detailed tool documentation, scoring guidelines, and reduction planning.

### Team Scaling Planning

```bash
# Calculate optimal hiring plan, team structure, and budget projections
python scripts/team_scaling_calculator.py team_data.json

# Generate JSON output for board planning
python scripts/team_scaling_calculator.py team_data.json --output json -f scaling_plan.json

# View help and input schema
python scripts/team_scaling_calculator.py --help
```

See [references/tools.md](references/tools.md) for scenario examples, budget estimation, and risk assessment guidance.

## Reference Materials

All detailed frameworks, templates, and tool documentation have been organized into focused reference files:

### [Technical Leadership Frameworks](references/frameworks.md)
- Technology strategy and roadmap development
- Innovation management frameworks
- Technical debt assessment strategies
- Team scaling and structure patterns
- Performance management systems
- Architecture governance (ADRs)
- Technology evaluation frameworks
- Vendor relationship management
- DORA and quality metrics
- Crisis management playbooks
- Stakeholder reporting frameworks
- Strategic initiatives (cloud, AI/ML, platform)

### [Communication Templates](references/templates.md)
- Weekly CTO schedule template
- Technology strategy presentation
- Team all-hands structure
- Board update email format
- ADR (Architecture Decision Record) template
- Incident post-mortem template
- Technology evaluation scorecard
- Engineering team OKR template
- Hiring scorecard template
- 1-on-1 meeting template

### [Python Tools Guide](references/tools.md)
- Tech debt analyzer comprehensive documentation
- Team scaling calculator detailed guide
- Input format specifications and examples
- Output interpretation guidelines
- Integration workflow examples
- Best practices and troubleshooting
- Real-world scenario examples
- Data privacy and security notes

## Success Indicators

**Technical Excellence**
- System uptime >99.9%
- Deploy frequency >1 per day
- Technical debt <10% capacity allocation
- Zero critical security incidents
- Lead time for changes <1 day

**Team Success**
- Team satisfaction score >8/10
- Voluntary attrition <10% annually
- Key positions filled >90%
- Diversity metrics improving
- Internal promotion rate >30%

**Business Impact**
- Features delivered on-time >80%
- Engineering enables revenue growth
- Cost per transaction decreasing
- Innovation driving competitive advantage
- Customer-reported issues declining

## Red Flags

- Technical debt increasing quarter-over-quarter
- Attrition rate rising above 15%
- Sprint velocity declining consistently
- Production incidents increasing
- Team morale scores dropping
- Budget overruns (>10% variance)
- Vendor lock-in concerns growing
- Security vulnerabilities accumulating
