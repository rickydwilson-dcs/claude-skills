# Product Strategy Frameworks

Strategic frameworks for product leadership, OKRs, market analysis, and organizational design.

## OKR Framework

Objectives and Key Results for aligning teams around measurable outcomes.

### OKR Structure

**Objective:** Aspirational goal that describes what you want to achieve
- Qualitative and inspirational
- Time-bound (typically quarterly)
- Memorable and motivating
- Directional, not tactical

**Key Results:** Measurable outcomes that track progress toward objective
- Quantitative and specific
- 2-5 key results per objective
- Ambitious but achievable (70% success = good)
- Leading indicators, not lagging

### OKR Template

```
Objective: [Inspiring goal statement]

Key Result 1: [Metric] from [baseline] to [target] by [date]
Key Result 2: [Metric] from [baseline] to [target] by [date]
Key Result 3: [Metric] from [baseline] to [target] by [date]
```

### Example OKR

```
Objective: Become the #1 platform for mid-market sales teams

Key Result 1: Increase enterprise signups from 50/month to 200/month
Key Result 2: Improve Net Promoter Score from 35 to 50
Key Result 3: Achieve 95% customer retention rate (up from 88%)
```

### OKR Best Practices

**DO:**
- Start with company-level objectives
- Cascade down to teams
- Focus on outcomes, not outputs
- Set ambitious targets (stretch goals)
- Review and grade quarterly
- Make OKRs public across org

**DON'T:**
- Use OKRs as task lists
- Set too many objectives (3-5 max)
- Make key results binary (yes/no)
- Treat 100% achievement as expected
- Set OKRs in isolation
- Punish missed OKRs

### OKR Cascade Pattern

**Company Level:**
```
Objective: Expand market leadership in North America
├─ KR1: Grow revenue to $50M ARR
├─ KR2: Achieve 90% customer retention
└─ KR3: Launch in 5 new verticals
```

**Product Level:**
```
Objective: Deliver enterprise-grade platform capabilities
├─ KR1: Launch SSO and SAML integration
├─ KR2: Achieve <2s page load time for 95th percentile
└─ KR3: Reduce P0 bugs by 80%
```

**Team Level:**
```
Objective: Build scalable collaboration features
├─ KR1: Ship real-time co-editing for 10k concurrent users
├─ KR2: Achieve 95% uptime SLA
└─ KR3: Reduce API latency from 200ms to 50ms
```

### OKR Scoring

**Score each KR at end of quarter:**
- 0.0 - 0.3: Not achieved (red)
- 0.4 - 0.6: Progress made (yellow)
- 0.7 - 1.0: Success (green)
- 1.0+: Exceeded expectations

**Example Grading:**
```
KR1: Increase signups from 50 to 200/month
Actual: 140/month
Score: 0.6 (achieved 90/150 increase = 60%)

KR2: Improve NPS from 35 to 50
Actual: NPS 47
Score: 0.8 (achieved 12/15 increase = 80%)

KR3: Achieve 95% retention (from 88%)
Actual: 93% retention
Score: 0.7 (achieved 5/7 increase = 71%)

Overall Objective Score: (0.6 + 0.8 + 0.7) / 3 = 0.7
```

### OKR Review Cadence

**Weekly:** Team checks progress, identifies blockers
**Monthly:** Department reviews, course-corrects if needed
**Quarterly:** Grade OKRs, set next quarter's objectives

## Strategy Cascade Framework

### Company Strategy Types

#### Growth Strategy
**Focus:** Rapid user/revenue acquisition

**Key Metrics:**
- Monthly Active Users (MAU)
- Customer Acquisition Cost (CAC)
- Sign-up conversion rate
- Time to first value

**Product Focus:**
- Viral features
- Onboarding optimization
- Referral programs
- Free tier monetization

#### Retention Strategy
**Focus:** Customer lifetime value and churn reduction

**Key Metrics:**
- Net Retention Rate (NRR)
- Customer Churn Rate
- Product engagement score
- Feature adoption rate

**Product Focus:**
- Power user features
- Customer success tools
- Engagement triggers
- Value realization tracking

#### Revenue Strategy
**Focus:** Monetization and expansion

**Key Metrics:**
- Average Revenue Per User (ARPU)
- Expansion Revenue %
- Conversion from free to paid
- Upsell/cross-sell rate

**Product Focus:**
- Premium tiers
- Usage-based pricing
- Enterprise features
- Billing optimization

#### Innovation Strategy
**Focus:** New markets and product lines

**Key Metrics:**
- New product adoption
- Time to market
- Innovation pipeline health
- Market share in new segment

**Product Focus:**
- Experimental features
- New product development
- Market research
- Strategic partnerships

#### Operational Strategy
**Focus:** Efficiency and scalability

**Key Metrics:**
- Cost per transaction
- System uptime/reliability
- Team productivity
- Technical debt ratio

**Product Focus:**
- Platform improvements
- Infrastructure scaling
- Process automation
- Developer experience

## Market Analysis Frameworks

### Competitive Analysis Matrix

| Feature | Our Product | Competitor A | Competitor B | Competitor C |
|---------|------------|--------------|--------------|--------------|
| Feature 1 | ✓ | ✓ | ✗ | ✓ |
| Feature 2 | ✓ | ✗ | ✓ | ✓ |
| Feature 3 | ✗ | ✓ | ✓ | ✗ |
| Pricing | $99/mo | $149/mo | $79/mo | $199/mo |
| Target | SMB | Enterprise | SMB | Mid-market |

**Analysis Questions:**
- What do competitors do better?
- What are our unique advantages?
- Where are market gaps?
- What features are table stakes?

### Porter's Five Forces

**1. Competitive Rivalry**
- Number of competitors
- Market growth rate
- Differentiation level
- Switching costs

**2. Threat of New Entrants**
- Barriers to entry
- Capital requirements
- Technology barriers
- Network effects

**3. Bargaining Power of Suppliers**
- Supplier concentration
- Switching costs
- Forward integration threat

**4. Bargaining Power of Buyers**
- Customer concentration
- Price sensitivity
- Switching costs
- Backward integration threat

**5. Threat of Substitutes**
- Alternative solutions
- Price-performance trade-off
- Ease of switching

### TAM/SAM/SOM Model

**Total Addressable Market (TAM):**
- Total market demand
- Everyone who could theoretically use product
- Example: $50B global CRM market

**Serviceable Addressable Market (SAM):**
- Segment you can realistically serve
- Geographic, industry, or size constraints
- Example: $5B North American SMB CRM market

**Serviceable Obtainable Market (SOM):**
- Share you can capture short-term
- Realistic penetration based on resources
- Example: $50M (1% of SAM in 3 years)

**Market Sizing Calculation:**
```
SOM = SAM × Expected Market Share × Adoption Rate

Example:
- SAM: 100,000 potential customers
- Expected share: 5% (5,000 customers)
- Adoption rate: 60%
- SOM: 3,000 customers in target segment
- Revenue: 3,000 × $99/mo × 12 = $3.6M ARR
```

## Vision and Strategy Setting

### Product Vision Statement

**Format:**
```
For [target customer]
Who [statement of need]
The [product name] is a [product category]
That [key benefit, reason to buy]
Unlike [primary competitive alternative]
Our product [statement of primary differentiation]
```

**Example:**
```
For mid-market sales teams
Who need to close deals faster and more predictably
Salesforce Lightning is a CRM platform
That provides complete visibility into the sales pipeline
Unlike spreadsheets and basic CRM tools
Our product uses AI to prioritize high-value opportunities and automate follow-ups
```

### Strategy Canvas

Map your differentiation against industry factors:

```
High │                    ○ (Us)
     │              ×
     │         ×              × (Competitors)
Mid  │    ○         ○
     │
Low  │    ×              ○
     └─────────────────────────────
       Price  Features  Support  Speed  UX
```

**Analysis:**
- Where do we compete on same factors?
- Where do we differentiate?
- What can we eliminate?
- What should we create?

### Blue Ocean Strategy

**Red Ocean (Compete):**
- Fight for existing demand
- Beat the competition
- Exploit existing demand
- Trade-off: value vs cost

**Blue Ocean (Create):**
- Create uncontested market space
- Make competition irrelevant
- Create and capture new demand
- Break value-cost trade-off

**Four Actions Framework:**
- **Eliminate:** What factors can be eliminated?
- **Reduce:** What factors can be reduced below industry standard?
- **Raise:** What factors can be raised above industry standard?
- **Create:** What new factors can be created?

## Team Scaling and Organizational Design

### Product Team Structure

**Feature Teams (Recommended):**
```
Product Team "Checkout"
├─ Product Manager (1)
├─ Engineers (4-6)
├─ Designer (1)
└─ Data Analyst (0.5)

Owns: End-to-end checkout experience
Metrics: Conversion rate, cart abandonment
```

**Component Teams (Legacy):**
```
Platform Team
├─ Backend Engineers (8)
├─ Frontend Engineers (6)
└─ QA Engineers (4)

Problem: No clear product ownership or metrics
```

### Spotify Squad Model

**Squad:** Cross-functional team (5-9 people)
- Owns specific area of product
- Autonomous, self-organizing
- Long-lived (not project-based)

**Tribe:** Collection of squads (40-150 people)
- Work on related areas
- Tribe lead coordinates dependencies

**Chapter:** People with same skill across squads
- Engineers, designers, PMs
- Knowledge sharing and standards

**Guild:** Communities of interest
- Cross-tribe
- Voluntary participation
- Share learnings

### Team Topologies

**Stream-Aligned Teams:**
- Aligned to flow of business value
- Primary team type
- Example: "Payments Team"

**Enabling Teams:**
- Help stream teams overcome obstacles
- Temporary assistance
- Example: "Developer Experience Team"

**Complicated Subsystem Teams:**
- Build/maintain complex subsystems
- Requires specialized knowledge
- Example: "Search Infrastructure Team"

**Platform Teams:**
- Provide internal services
- Reduce cognitive load on stream teams
- Example: "API Platform Team"

### Conway's Law

"Organizations design systems that mirror their communication structure"

**Implications:**
- Structure teams around desired architecture
- Co-locate dependent teams
- Reduce hand-offs and dependencies
- Align team boundaries with product boundaries

### Scaling Principles

**Team Size:**
- Small: 2-5 people (startup)
- Optimal: 5-9 people (two-pizza team)
- Large: 10+ people (split into multiple teams)

**Product Manager Ratios:**
- Early: 1 PM : 3-5 engineers
- Scaling: 1 PM : 6-10 engineers
- Enterprise: 1 PM : 8-12 engineers

**When to Split Teams:**
- Team consistently over 10 people
- Too many competing priorities
- Slowed decision-making
- Clear product area separation

## North Star Metric Framework

### Finding Your North Star

**Criteria:**
1. Expresses core product value
2. Leads to revenue
3. Actionable by team
4. Measurable and understandable

**Examples by Product Type:**

**SaaS Platform:**
- Slack: Messages sent by teams
- Zoom: Total meeting minutes
- Notion: Weekly active collaborative documents

**Marketplace:**
- Airbnb: Nights booked
- Uber: Rides completed
- Etsy: GMS (Gross Merchandise Sales)

**Media/Content:**
- Netflix: Hours watched
- Spotify: Time spent listening
- YouTube: Watch time

**E-Commerce:**
- Amazon: Purchases per month
- Shopify: GMV (Gross Merchandise Volume)

### Input Metrics

Metrics that drive your North Star:

```
North Star: Weekly Active Teams (Slack)
├─ Breadth: New team signups
├─ Depth: Channels per team
├─ Frequency: Messages per team per week
└─ Efficiency: Time from signup to first message
```

### North Star Framework Template

```
Vision: [Product vision statement]

North Star Metric: [Core value metric]
Current: [Baseline]
Target: [6-month goal]

Input Metrics:
1. [Metric 1]: [Baseline] → [Target]
2. [Metric 2]: [Baseline] → [Target]
3. [Metric 3]: [Baseline] → [Target]

Team Workstreams:
- Team A: Improve [input metric 1]
- Team B: Improve [input metric 2]
- Team C: Improve [input metric 3]
```

---

**Last Updated:** 2025-11-08
**Related Files:**
- [templates.md](templates.md) - OKR templates and strategic planning formats
- [tools.md](tools.md) - okr_cascade_generator.py documentation
