---
name: ceo-advisor
description: Executive leadership guidance for strategic decision-making, organizational development, and stakeholder management. Includes strategy analyzer, financial scenario modeling, board governance frameworks, and investor relations playbooks. Use when planning strategy, preparing board presentations, managing investors, developing organizational culture, making executive decisions, or when user mentions CEO, strategic planning, board meetings, investor updates, organizational leadership, or executive strategy.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: executive-advisory
  domain: ceo
  updated: 2025-11-08
  keywords:
    - strategic planning
    - executive leadership
    - board governance
    - investor relations
    - financial modeling
    - organizational strategy
    - business strategy
    - stakeholder management
    - capital allocation
    - M&A decisions
    - fundraising strategy
    - company culture
    - OKR development
    - market positioning
    - competitive strategy
    - financial planning
    - risk management
    - talent strategy
    - organizational design
    - CEO succession planning
  tech-stack:
    - financial modeling tools
    - strategy frameworks
    - board management platforms
    - OKR management systems
    - investor CRM
    - executive dashboards
    - communication platforms
  python-tools:
    - strategy_analyzer.py
    - financial_scenario_analyzer.py
---

# CEO Advisor

Strategic frameworks and tools for chief executive leadership, organizational transformation, and stakeholder management.

## Keywords
CEO, chief executive officer, executive leadership, strategic planning, board governance, investor relations, board meetings, board presentations, financial modeling, strategic decisions, organizational culture, company culture, leadership development, stakeholder management, executive strategy, crisis management, organizational transformation, investor updates, strategic initiatives, company vision

## Quick Start

### For Strategic Planning
```bash
# Create company data JSON file (see example below)
# Run strategic analysis
python scripts/strategy_analyzer.py company_data.json

# Generate JSON output for board presentations
python scripts/strategy_analyzer.py company_data.json --output json

# Save report to file
python scripts/strategy_analyzer.py company_data.json -o json -f strategy_report.json

# View help and JSON schema
python scripts/strategy_analyzer.py --help
```

Example `company_data.json`:
```json
{
  "name": "TechCorp Inc.",
  "market_position": {"market_share": 35, "brand_strength": 65, "competitive_advantage": 70},
  "financial_health": {"revenue_growth": 45, "profitability": 40, "cash_flow": 55},
  "organizational_capability": {"talent": 70, "culture": 65, "leadership": 75},
  "growth_potential": {"market_size": 80, "expansion_opportunities": 70},
  "competitive_forces": {"rivalry": 70, "suppliers": 40, "buyers": 60},
  "context": {"industry_disruption": true, "cash_available": 150000000},
  "timeline": 18
}
```

Analyzes strategic position using SWOT, Porter's Five Forces, and BCG Matrix.

### For Financial Scenarios
```bash
# Create scenarios JSON file (see example below)
# Run financial analysis
python scripts/financial_scenario_analyzer.py scenarios.json

# Generate JSON output for executive dashboards
python scripts/financial_scenario_analyzer.py scenarios.json --output json

# Save report to file
python scripts/financial_scenario_analyzer.py scenarios.json -o json -f analysis.json

# View help and JSON schema
python scripts/financial_scenario_analyzer.py --help
```

Example `scenarios.json`:
```json
{
  "base_case": {
    "revenue": 5000000,
    "cogs": 1500000,
    "operating_expenses": 3000000,
    "cash": 2000000,
    "burn_rate": 200000,
    "valuation": 20000000
  },
  "scenarios": [
    {
      "name": "Aggressive Growth",
      "probability": 0.3,
      "growth_model": "exponential",
      "growth_rate": 0.5,
      "cogs_ratio": 0.25,
      "discount_rate": 0.12
    },
    {
      "name": "Moderate Growth",
      "probability": 0.5,
      "growth_rate": 0.3,
      "cogs_ratio": 0.3
    }
  ]
}
```

Models scenarios with NPV, IRR, and risk-adjusted projections.

### For Decision Making
Review `references/executive_decision_framework.md` for structured decision processes.

### For Board Management
Use templates in `references/board_governance_investor_relations.md` for board packages.

### For Culture Building
Implement frameworks from `references/leadership_organizational_culture.md` for transformation.

## Core CEO Responsibilities

### 1. Vision & Strategy

#### Setting Direction
- **Vision Development**: Define 10-year aspirational future
- **Mission Articulation**: Clear purpose and why we exist
- **Strategy Formulation**: 3-5 year competitive positioning
- **Value Definition**: Core beliefs and principles

#### Strategic Planning Cycle
```
Q1: Environmental Scan
- Market analysis
- Competitive intelligence
- Technology trends
- Regulatory landscape

Q2: Strategy Development
- Strategic options generation
- Scenario planning
- Resource allocation
- Risk assessment

Q3: Planning & Budgeting
- Annual operating plan
- Budget allocation
- OKR setting
- Initiative prioritization

Q4: Communication & Launch
- Board approval
- Investor communication
- Employee cascade
- Partner alignment
```

### 2. Capital & Resource Management

#### Capital Allocation Framework
```bash
# Run financial scenario analysis
python scripts/financial_scenario_analyzer.py scenarios.json

# Generate report for board
python scripts/financial_scenario_analyzer.py scenarios.json -o json -f capital_allocation.json

# Allocation priorities:
1. Core Operations (40-50%)
2. Growth Investments (25-35%)
3. Innovation/R&D (10-15%)
4. Strategic Reserve (10-15%)
5. Shareholder Returns (varies)
```

#### Fundraising Strategy
- **Seed/Series A**: Product-market fit focus
- **Series B/C**: Growth acceleration
- **Late Stage**: Market expansion
- **IPO**: Public market access
- **Debt**: Non-dilutive growth

### 3. Stakeholder Leadership

#### Stakeholder Priority Matrix
```
         Influence →
         Low        High
    High ┌─────────┬─────────┐
Interest │ Keep    │ Manage  │
    ↑    │Informed │ Closely │
         ├─────────┼─────────┤
    Low  │Monitor  │  Keep   │
         │         │Satisfied│
         └─────────┴─────────┘

Primary Stakeholders:
- Board of Directors
- Investors
- Employees
- Customers

Secondary Stakeholders:
- Partners
- Community
- Media
- Regulators
```

### 4. Organizational Leadership

#### Culture Development
From `references/leadership_organizational_culture.md`:

**Culture Transformation Timeline**:
- Months 1-2: Assessment
- Months 2-3: Design
- Months 4-12: Implementation
- Months 12+: Embedding

**Key Levers**:
- Leadership modeling
- Communication
- Systems alignment
- Recognition
- Accountability

### 5. External Representation

#### CEO Communication Calendar

**Daily**:
- Customer touchpoint
- Team check-in
- Metric review

**Weekly**:
- Executive team meeting
- Board member update
- Key customer/partner call
- Media opportunity

**Monthly**:
- All-hands meeting
- Board report
- Investor update
- Industry engagement

**Quarterly**:
- Board meeting
- Earnings call
- Strategy review
- Town hall

## Executive Routines

### Daily CEO Schedule Template

```
6:00 AM - Personal development (reading, exercise)
7:00 AM - Day planning & priority review
8:00 AM - Metric dashboard review
8:30 AM - Customer/market intelligence
9:00 AM - Strategic work block
10:30 AM - Meetings block
12:00 PM - Lunch (networking/thinking)
1:00 PM - External meetings
3:00 PM - Internal meetings
4:30 PM - Email/communication
5:30 PM - Team walk-around
6:00 PM - Transition/reflection
```

### Weekly Leadership Rhythm

**Monday**: Strategy & Planning
- Executive team meeting
- Metrics review
- Week planning

**Tuesday**: External Focus
- Customer meetings
- Partner discussions
- Investor relations

**Wednesday**: Operations
- Deep dives
- Problem solving
- Process review

**Thursday**: People & Culture
- 1-on-1s
- Talent reviews
- Culture initiatives

**Friday**: Innovation & Future
- Strategic projects
- Learning time
- Planning ahead

## Critical CEO Decisions

### Go/No-Go Decision Framework

Use framework from `references/executive_decision_framework.md`:

**Major Decisions Requiring Framework**:
- M&A opportunities
- Market expansion
- Major pivots
- Large investments
- Restructuring
- Leadership changes

**Decision Checklist**:
- [ ] Problem clearly defined
- [ ] Data/evidence gathered
- [ ] Options evaluated
- [ ] Stakeholders consulted
- [ ] Risks assessed
- [ ] Implementation planned
- [ ] Success metrics defined
- [ ] Communication prepared

### Crisis Management

#### Crisis Leadership Playbook

**Level 1 Crisis** (Department)
- Monitor situation
- Support as needed
- Review afterwards

**Level 2 Crisis** (Company)
- Activate crisis team
- Lead response
- Communicate frequently

**Level 3 Crisis** (Existential)
- Take direct control
- Board engagement
- All-hands focus
- External communication

## Board Management

### Board Meeting Success

From `references/board_governance_investor_relations.md`:

**Preparation Timeline**:
- T-4 weeks: Agenda development
- T-2 weeks: Material preparation
- T-1 week: Package distribution
- T-0: Meeting execution

**Board Package Components**:
1. CEO Letter (1-2 pages)
2. Dashboard (1 page)
3. Financial review (5 pages)
4. Strategic updates (10 pages)
5. Risk register (2 pages)
6. Appendices

### Managing Board Dynamics

**Building Trust**:
- Regular communication
- No surprises
- Transparency
- Follow-through
- Respect expertise

**Difficult Conversations**:
- Prepare thoroughly
- Lead with facts
- Own responsibility
- Present solutions
- Seek alignment

## Investor Relations

### Investor Communication

**Earnings Cycle**:
1. Pre-announcement quiet period
2. Earnings release
3. Conference call
4. Follow-up meetings
5. Conference participation

**Key Messages**:
- Growth trajectory
- Competitive position
- Financial performance
- Strategic progress
- Future outlook

### Fundraising Excellence

**Pitch Deck Structure**:
1. Problem (1 slide)
2. Solution (1-2 slides)
3. Market (1-2 slides)
4. Product (2-3 slides)
5. Business Model (1 slide)
6. Go-to-Market (1-2 slides)
7. Competition (1 slide)
8. Team (1 slide)
9. Financials (2 slides)
10. Ask (1 slide)

## Performance Management

### Company Scorecard

**Financial Metrics**:
- Revenue growth
- Gross margin
- EBITDA
- Cash flow
- Runway

**Customer Metrics**:
- Acquisition
- Retention
- NPS
- LTV/CAC

**Operational Metrics**:
- Productivity
- Quality
- Efficiency
- Innovation

**People Metrics**:
- Engagement
- Retention
- Diversity
- Development

### CEO Self-Assessment

**Quarterly Reflection**:
- What went well?
- What could improve?
- Key learnings?
- Priority adjustments?

**Annual 360 Review**:
- Board feedback
- Executive team input
- Skip-level insights
- Self-evaluation
- Development plan

## Succession Planning

### CEO Succession Timeline

**Ongoing**:
- Identify internal candidates
- Develop high potentials
- External benchmarking

**T-3 Years**:
- Formal succession planning
- Candidate assessment
- Development acceleration

**T-1 Year**:
- Final selection
- Transition planning
- Communication strategy

**Transition**:
- Knowledge transfer
- Stakeholder handoff
- Gradual transition

## Personal Development

### CEO Learning Agenda

**Core Competencies**:
- Strategic thinking
- Financial acumen
- Leadership presence
- Communication
- Decision making

**Development Activities**:
- Executive coaching
- Peer networking (YPO/EO)
- Board service
- Industry involvement
- Continuous education

### Work-Life Integration

**Sustainability Practices**:
- Protected family time
- Exercise routine
- Mental health support
- Vacation planning
- Delegation discipline

**Energy Management**:
- Know peak hours
- Block deep work time
- Batch similar tasks
- Take breaks
- Reflect daily

## Tools & Resources

### Essential CEO Tools

**Strategy & Planning**:
- Strategy frameworks (Porter, BCG, McKinsey)
- Scenario planning tools
- OKR management systems

**Financial Management**:
- Financial modeling
- Cap table management
- Investor CRM

**Communication**:
- Board portal
- Investor relations platform
- Employee communication tools

**Personal Productivity**:
- Calendar management
- Task management
- Note-taking system

### Key Resources

**Books**:
- "Good to Great" - Jim Collins
- "The Hard Thing About Hard Things" - Ben Horowitz
- "High Output Management" - Andy Grove
- "The Lean Startup" - Eric Ries

**Frameworks**:
- Jobs-to-be-Done
- Blue Ocean Strategy
- Balanced Scorecard
- OKRs

**Networks**:
- YPO (Young Presidents' Organization)
- EO (Entrepreneurs' Organization)
- Industry associations
- CEO peer groups

## Success Metrics

### CEO Effectiveness Indicators

✅ **Strategic Success**
- Vision clarity and buy-in
- Strategy execution on track
- Market position improving
- Innovation pipeline strong

✅ **Financial Success**
- Revenue growth targets met
- Profitability improving
- Cash position strong
- Valuation increasing

✅ **Organizational Success**
- Culture thriving
- Talent retained
- Engagement high
- Succession ready

✅ **Stakeholder Success**
- Board confidence high
- Investor satisfaction
- Customer NPS strong
- Employee approval rating

## Red Flags

⚠️ Missing targets consistently  
⚠️ High executive turnover  
⚠️ Board relationship strained  
⚠️ Culture deteriorating  
⚠️ Market share declining  
⚠️ Cash burn increasing  
⚠️ Innovation stalling  
⚠️ Personal burnout signs
