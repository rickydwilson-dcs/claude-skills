---
name: product-strategist
description: Strategic product leadership toolkit for Head of Product including OKR cascade generation, market analysis, vision setting, and team scaling. Use for strategic planning, goal alignment, competitive analysis, and organizational design.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: product
  domain: product-strategy
  updated: 2025-11-08
  keywords:
    - OKR framework
    - strategic planning
    - goal alignment
    - market analysis
    - competitive analysis
    - vision setting
    - team scaling
    - organizational design
    - strategy cascade
    - key results
    - alignment tracking
    - metrics definition
    - KPI development
    - strategic roadmap
    - business strategy
    - market positioning
  tech-stack:
    - Python 3.8+
    - CLI
    - JSON export
    - Alignment scoring
  python-tools:
    - okr_cascade_generator.py
---

# Product Strategist

Strategic toolkit for Head of Product to drive vision, alignment, and organizational excellence. This skill provides Python tools for OKR cascading, comprehensive frameworks for strategy development, and battle-tested templates for vision documents and strategic planning.

**What This Skill Provides:**
- OKR cascade generator with alignment tracking
- Strategic planning frameworks (growth, retention, revenue, innovation, operational)
- Market analysis and competitive positioning methods
- Team scaling and organizational design patterns
- North Star metric framework

**Best For:**
- Cascading company OKRs to product and team levels
- Strategic planning and quarterly goal-setting
- Market analysis and competitive positioning
- Team scaling and organizational design
- Aligning product strategy with business objectives

## Quick Start

### Generate OKR Cascade
```bash
# Growth strategy
python scripts/okr_cascade_generator.py growth

# Retention strategy
python scripts/okr_cascade_generator.py retention

# Revenue strategy
python scripts/okr_cascade_generator.py revenue
```

### OKR Structure
**Objective:** Inspiring, qualitative goal (what you want to achieve)
**Key Results:** 2-5 measurable outcomes (how you'll know you achieved it)

```
Objective: Become #1 platform for mid-market sales teams

Key Result 1: Increase enterprise signups from 50 to 200/month
Key Result 2: Improve NPS from 35 to 50
Key Result 3: Achieve 95% retention rate (up from 88%)
```

See [frameworks.md](references/frameworks.md) for complete OKR methodology.

## Core Workflows

### 1. Quarterly OKR Planning Process

**Steps:**
1. Define company strategic priorities
2. Generate OKR cascade: `python scripts/okr_cascade_generator.py [strategy]`
3. Review alignment scores (target: >75%)
4. Customize OKRs to your context
5. Assign owners and set tracking dashboards
6. Review weekly, grade quarterly

**OKR Cascade Levels:**
- **Company:** 3-5 objectives, 3 key results each
- **Product:** 2-3 objectives aligned to company
- **Team:** 1-2 objectives per team

**Alignment Scoring:**
- 90-100%: Excellent alignment
- 75-89%: Good alignment
- 60-74%: Moderate (review)
- <60%: Poor (needs revision)

**Detailed Framework:** See [frameworks.md](references/frameworks.md) for OKR structure, scoring, and review cadence.

**Templates:** See [templates.md](references/templates.md) for company, product, and team OKR templates.

### 2. Strategic Planning Process

**Annual Planning:**
1. Analyze market position (TAM/SAM/SOM)
2. Conduct competitive analysis
3. Define strategic priorities (3-5 max)
4. Create product vision document
5. Set annual OKRs and quarterly themes
6. Plan resources and hiring

**Strategy Types:**
- **Growth:** User/revenue acquisition
- **Retention:** LTV and churn reduction
- **Revenue:** Monetization optimization
- **Innovation:** New products/markets
- **Operational:** Efficiency and scale

**Strategy Selection Tool:**
```bash
python scripts/okr_cascade_generator.py [growth|retention|revenue|innovation|operational]
```

**Detailed Frameworks:** See [frameworks.md](references/frameworks.md) for each strategy type, market analysis methods, and vision-setting.

**Templates:** See [templates.md](references.md) for annual strategic plan and product vision document templates.

### 3. Team Scaling Process

**Hiring Planning:**
1. Calculate team capacity needs
2. Define team structure (feature vs component teams)
3. Create hiring plan (roles, timeline, budget)
4. Design team charters
5. Set success metrics per team

**Team Structure Patterns:**
- **Feature Teams:** Own end-to-end product area (recommended)
- **Platform Teams:** Provide internal services
- **Enabling Teams:** Help others overcome obstacles

**PM-to-Engineer Ratios:**
- Early stage: 1 PM : 3-5 engineers
- Scaling: 1 PM : 6-10 engineers
- Enterprise: 1 PM : 8-12 engineers

**Detailed Frameworks:** See [frameworks.md](references/frameworks.md) for team topologies, Spotify model, Conway's Law implications.

**Templates:** See [templates.md](references/templates.md) for hiring plans and team charter templates.

## Python Tools

### okr_cascade_generator.py
Automated OKR hierarchy generator with alignment tracking.

**Key Features:**
- 5 pre-built strategy templates
- Three-level cascade (company → product → team)
- Alignment score calculation
- Contribution percentage tracking
- Multiple output formats (text, JSON, CSV)
- Detailed metric definitions

**Usage:**
```bash
# Generate growth strategy OKRs
python3 scripts/okr_cascade_generator.py growth

# With detailed metrics
python3 scripts/okr_cascade_generator.py growth --metrics

# JSON output for dashboards
python3 scripts/okr_cascade_generator.py growth -o json -f okrs.json

# CSV for spreadsheets
python3 scripts/okr_cascade_generator.py growth -o csv -f okrs.csv

# Verbose mode (detailed explanations)
python3 scripts/okr_cascade_generator.py growth -v
```

**Available Strategies:**
- **growth:** User acquisition and market expansion
- **retention:** Customer LTV and churn reduction
- **revenue:** Monetization and ARPU optimization
- **innovation:** New products and market opportunities
- **operational:** Efficiency, scalability, technical excellence

**Output Includes:**
- Company-level objectives and key results
- Product-level OKRs with alignment scores
- Team-level OKRs with contribution percentages
- Metric definitions and tracking guidance

**Complete Documentation:** See [tools.md](references/tools.md) for full usage guide, strategy templates, and integration patterns.

## Reference Documentation

### Frameworks ([frameworks.md](references/frameworks.md))
Comprehensive strategic frameworks:
- OKR Framework: Structure, scoring, cascading, review cadence
- Strategy Cascade: Growth, retention, revenue, innovation, operational strategies
- Market Analysis: Competitive matrix, Porter's Five Forces, TAM/SAM/SOM
- Vision Setting: Vision statement format, strategy canvas, Blue Ocean strategy
- Team Scaling: Team topologies, Spotify model, Conway's Law, scaling principles
- North Star Metric: Finding your North Star, input metrics, framework template

### Templates ([templates.md](references/templates.md))
Ready-to-use templates:
- OKR Templates: Company-level, product team, complete examples
- Strategic Planning: Annual strategic plan, product vision document
- Team Scaling: Hiring plan, team charter templates
- Example OKRs: Complete examples for each strategy type

### Tools ([tools.md](references/tools.md))
Python tool documentation:
- okr_cascade_generator.py: Complete usage guide
- Strategy Templates: Detailed description of each strategy
- Output Formats: Text, JSON, CSV examples
- Alignment Scoring: Formula and interpretation
- Contribution Tracking: How percentages are calculated
- Integration Patterns: Dashboard, spreadsheet, Confluence, Slack
- Customization Guide: Modifying templates and alignment weights
- Troubleshooting: Common issues and solutions

## Integration Points

This toolkit integrates with:
- **OKR Tools:** Lattice, 15Five, Workboard, Ally.io
- **Analytics:** Amplitude, Mixpanel, Tableau, Looker
- **Documentation:** Confluence, Notion, Google Docs
- **Collaboration:** Slack, Teams, Miro
- **Project Management:** Jira, Asana, Monday.com

See [tools.md](references/tools.md) for detailed integration workflows.

## Quick Commands

```bash
# Generate OKRs for different strategies
python scripts/okr_cascade_generator.py growth
python scripts/okr_cascade_generator.py retention
python scripts/okr_cascade_generator.py revenue
python scripts/okr_cascade_generator.py innovation
python scripts/okr_cascade_generator.py operational

# With metric definitions
python scripts/okr_cascade_generator.py growth --metrics

# Export formats
python scripts/okr_cascade_generator.py growth -o json -f okrs.json
python scripts/okr_cascade_generator.py growth -o csv -f okrs.csv

# Verbose output
python scripts/okr_cascade_generator.py growth -v
```
