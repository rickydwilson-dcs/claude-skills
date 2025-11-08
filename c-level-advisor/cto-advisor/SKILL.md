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

Strategic frameworks and tools for technology leadership, team scaling, and engineering excellence.

## Keywords
CTO, chief technology officer, technical leadership, tech debt, technical debt, engineering team, team scaling, architecture decisions, technology evaluation, engineering metrics, DORA metrics, ADR, architecture decision records, technology strategy, engineering leadership, engineering organization, team structure, hiring plan, technical strategy, vendor evaluation, technology selection

## Quick Start

### For Technical Debt Assessment
```bash
# Create system data JSON file (see example below)
# Run analysis
python scripts/tech_debt_analyzer.py system_data.json

# Generate JSON output for dashboards
python scripts/tech_debt_analyzer.py system_data.json --output json

# Save report to file
python scripts/tech_debt_analyzer.py system_data.json -o json -f debt_report.json

# View help and JSON schema
python scripts/tech_debt_analyzer.py --help
```

Example `system_data.json`:
```json
{
  "name": "Legacy E-commerce Platform",
  "architecture": {"monolithic_design": 80, "tight_coupling": 70, "no_microservices": 90},
  "code_quality": {"low_test_coverage": 75, "high_complexity": 65},
  "infrastructure": {"manual_deployments": 70, "no_ci_cd": 60},
  "security": {"outdated_dependencies": 85, "no_security_scans": 70},
  "performance": {"slow_response_times": 60, "no_caching": 50},
  "team_size": 8,
  "system_criticality": "high",
  "business_context": {"growth_phase": "rapid", "compliance_required": true}
}
```

Analyzes system across 5 debt categories with prioritized reduction plan.

### For Team Scaling Planning
```bash
# Create team data JSON file (see example below)
# Run analysis
python scripts/team_scaling_calculator.py team_data.json

# Generate JSON output for planning tools
python scripts/team_scaling_calculator.py team_data.json --output json

# Save report to file
python scripts/team_scaling_calculator.py team_data.json -o json -f scaling_plan.json

# View help and JSON schema
python scripts/team_scaling_calculator.py --help
```

Example `team_data.json`:
```json
{
  "current_state": {
    "headcount": 25,
    "velocity": 450,
    "roles": {"engineering_manager": 2, "senior_engineer": 8, "mid_engineer": 10},
    "attrition_rate": 12,
    "location": "US"
  },
  "growth_targets": {
    "target_headcount": 75,
    "timeline_quarters": 4
  }
}
```

Calculates optimal hiring plan, team structure, and budget projections.

### For Architecture Decisions
Review `references/architecture_decision_records.md` for ADR templates and examples.

### For Technology Evaluation
Use framework in `references/technology_evaluation_framework.md` for vendor selection.

### For Engineering Metrics
Implement KPIs from `references/engineering_metrics.md` for team performance tracking.

## Core Responsibilities

### 1. Technology Strategy

#### Vision & Roadmap
- Define 3-5 year technology vision
- Create quarterly roadmaps
- Align with business strategy
- Communicate to stakeholders

#### Innovation Management
- Allocate 20% time for innovation
- Run hackathons quarterly
- Evaluate emerging technologies
- Build proof of concepts

#### Technical Debt Strategy
```bash
# Assess current debt
python scripts/tech_debt_analyzer.py system_data.json

# Generate report for executives
python scripts/tech_debt_analyzer.py system_data.json -o json -f debt_report.json

# Allocate capacity based on debt level
- Critical debt (>80): 40% capacity
- High debt (60-80): 25% capacity
- Medium debt (40-60): 15% capacity
- Low debt (<40): Ongoing maintenance
```

### 2. Team Leadership

#### Scaling Engineering
```bash
# Calculate scaling needs
python scripts/team_scaling_calculator.py team_data.json

# Generate hiring plan for board
python scripts/team_scaling_calculator.py team_data.json -o json -f hiring_plan.json

# Key ratios to maintain:
- Manager:Engineer = 1:8
- Senior:Mid:Junior = 3:4:2
- Product:Engineering = 1:10
- QA:Engineering = 1.5:10
```

#### Performance Management
- Set clear OKRs quarterly
- Conduct 1:1s weekly
- Review performance quarterly
- Provide growth opportunities

#### Culture Building
- Define engineering values
- Establish coding standards
- Create learning programs
- Foster collaboration

### 3. Architecture Governance

#### Decision Making
Use ADR template from `references/architecture_decision_records.md`:
1. Document context and problem
2. List all options considered
3. Record decision and rationale
4. Track consequences

#### Technology Standards
- Language choices
- Framework selection
- Database standards
- Security requirements
- API design guidelines

#### System Design Review
- Weekly architecture reviews
- Design documentation standards
- Prototype requirements
- Performance criteria

### 4. Vendor Management

#### Evaluation Process
Follow framework in `references/technology_evaluation_framework.md`:
1. Gather requirements (Week 1)
2. Market research (Week 1-2)
3. Deep evaluation (Week 2-4)
4. Decision and documentation (Week 4)

#### Vendor Relationships
- Quarterly business reviews
- SLA monitoring
- Cost optimization
- Strategic partnerships

### 5. Engineering Excellence

#### Metrics Implementation
From `references/engineering_metrics.md`:

**DORA Metrics** (Deploy to production targets):
- Deployment Frequency: >1/day
- Lead Time: <1 day
- MTTR: <1 hour
- Change Failure Rate: <15%

**Quality Metrics**:
- Test Coverage: >80%
- Code Review: 100%
- Technical Debt: <10%

**Team Health**:
- Sprint Velocity: ±10% variance
- Unplanned Work: <20%
- On-call Incidents: <5/week

## Weekly Cadence

### Monday
- Leadership team sync
- Review metrics dashboard
- Address escalations

### Tuesday
- Architecture review
- Technical interviews
- 1:1s with directs

### Wednesday
- Cross-functional meetings
- Vendor meetings
- Strategy work

### Thursday
- Team all-hands (monthly)
- Sprint reviews (bi-weekly)
- Technical deep dives

### Friday
- Strategic planning
- Innovation time
- Week recap and planning

## Quarterly Planning

### Q1 Focus: Foundation
- Annual planning
- Budget allocation
- Team goal setting
- Technology assessment

### Q2 Focus: Execution
- Major initiatives launch
- Mid-year hiring push
- Performance reviews
- Architecture evolution

### Q3 Focus: Innovation
- Hackathon
- Technology exploration
- Team development
- Process optimization

### Q4 Focus: Planning
- Next year strategy
- Budget planning
- Promotion cycles
- Debt reduction sprint

## Crisis Management

### Incident Response
1. **Immediate** (0-15 min):
   - Assess severity
   - Activate incident team
   - Begin communication

2. **Short-term** (15-60 min):
   - Implement fixes
   - Update stakeholders
   - Monitor systems

3. **Resolution** (1-24 hours):
   - Verify fix
   - Document timeline
   - Customer communication

4. **Post-mortem** (48-72 hours):
   - Root cause analysis
   - Action items
   - Process improvements

### Types of Crises

#### Security Breach
- Isolate affected systems
- Engage security team
- Legal/compliance notification
- Customer communication plan

#### Major Outage
- All-hands response
- Status page updates
- Executive briefings
- Customer outreach

#### Data Loss
- Stop writes immediately
- Assess recovery options
- Begin restoration
- Impact analysis

## Stakeholder Management

### Board/Executive Reporting
**Monthly**:
- KPI dashboard
- Risk register
- Major initiatives status

**Quarterly**:
- Technology strategy update
- Team growth and health
- Innovation highlights
- Budget review

### Cross-functional Partners

#### Product Team
- Weekly roadmap sync
- Sprint planning participation
- Technical feasibility reviews
- Feature estimation

#### Sales/Marketing
- Technical sales support
- Product capability briefings
- Customer reference calls
- Competitive analysis

#### Finance
- Budget management
- Cost optimization
- Vendor negotiations
- Capex planning

## Strategic Initiatives

### Digital Transformation
1. Assess current state
2. Define target architecture
3. Create migration plan
4. Execute in phases
5. Measure and adjust

### Cloud Migration
1. Application assessment
2. Migration strategy (7Rs)
3. Pilot applications
4. Full migration
5. Optimization

### Platform Engineering
1. Define platform vision
2. Build core services
3. Create self-service tools
4. Enable team adoption
5. Measure efficiency

### AI/ML Integration
1. Identify use cases
2. Build data infrastructure
3. Develop models
4. Deploy and monitor
5. Scale adoption

## Communication Templates

### Technology Strategy Presentation
```
1. Executive Summary (1 slide)
2. Current State Assessment (2 slides)
3. Vision & Strategy (2 slides)
4. Roadmap & Milestones (3 slides)
5. Investment Required (1 slide)
6. Risks & Mitigation (1 slide)
7. Success Metrics (1 slide)
```

### Team All-hands
```
1. Wins & Recognition (5 min)
2. Metrics Review (5 min)
3. Strategic Updates (10 min)
4. Demo/Deep Dive (15 min)
5. Q&A (10 min)
```

### Board Update Email
```
Subject: Engineering Update - [Month]

Highlights:
• [Major achievement]
• [Key metric improvement]
• [Strategic progress]

Challenges:
• [Issue and mitigation]

Next Month:
• [Priority 1]
• [Priority 2]

Detailed metrics attached.
```

## Tools & Resources

### Essential Tools
- **Architecture**: Draw.io, Lucidchart, C4 Model
- **Metrics**: DataDog, Grafana, LinearB
- **Planning**: Jira, Confluence, Notion
- **Communication**: Slack, Zoom, Loom
- **Development**: GitHub, GitLab, Bitbucket

### Key Resources
- **Books**: 
  - "The Manager's Path" - Camille Fournier
  - "Accelerate" - Nicole Forsgren
  - "Team Topologies" - Skelton & Pais
  
- **Frameworks**:
  - DORA metrics
  - SPACE framework
  - Team Topologies
  
- **Communities**:
  - CTO Craft
  - Engineering Leadership Slack
  - LeadDev community

## Success Indicators

✅ **Technical Excellence**
- System uptime >99.9%
- Deploy multiple times daily
- Technical debt <10% capacity
- Security incidents = 0

✅ **Team Success**
- Team satisfaction >8/10
- Attrition <10%
- Filled positions >90%
- Diversity improving

✅ **Business Impact**
- Features on-time >80%
- Engineering enables revenue
- Cost per transaction decreasing
- Innovation driving growth

## Red Flags to Watch

⚠️ Increasing technical debt  
⚠️ Rising attrition rate  
⚠️ Slowing velocity  
⚠️ Growing incidents  
⚠️ Team morale declining  
⚠️ Budget overruns  
⚠️ Vendor dependencies  
⚠️ Security vulnerabilities
