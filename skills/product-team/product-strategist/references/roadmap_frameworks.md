# Product Roadmap Frameworks Reference Guide

## Overview
Frameworks and best practices for creating, communicating, and maintaining product roadmaps that align teams, manage stakeholder expectations, and drive strategic outcomes.

## Roadmap Types

### Now-Next-Later Roadmap
**Best for:** Early-stage products, high uncertainty
**Timeline:** Flexible, no hard dates

**Structure:**
```
Now (0-3 months):
- Feature A (in progress)
- Feature B (starting soon)

Next (3-6 months):
- Feature C (validated, prioritized)
- Feature D (customer research complete)

Later (6+ months):
- Feature E (exploratory)
- Feature F (on the radar)
```

**Benefits:**
- Flexible, easy to adjust
- No commitment to dates
- Focus on sequencing

### Theme-Based Roadmap
**Best for:** Strategic alignment, multiple teams
**Timeline:** Quarterly or annual

**Structure:**
```
Q1: Customer Acquisition
- Features: Referral program, SEO optimization, trial experience
- Metrics: 50% increase in signups

Q2: Engagement & Retention
- Features: Personalization engine, habit-building features
- Metrics: +20% DAU/MAU ratio

Q3: Revenue Expansion
- Features: Premium tier, usage-based pricing, upsell flows
- Metrics: +30% ARPU
```

**Benefits:**
- Outcome-focused
- Easy to communicate strategy
- Flexible on specific features

### Timeline Roadmap
**Best for:** Committed deliverables, external stakeholders
**Timeline:** Specific dates/quarters

**Structure:**
```
Q1 2025        Q2 2025         Q3 2025
───────────    ───────────     ───────────
Feature A      Feature C       Feature E
Feature B      Feature D       Feature F
```

**Risks:**
- Stakeholders expect dates
- Less flexibility
- Pressure to ship vs iterate

## Prioritization Frameworks

### RICE Score
```
RICE = (Reach × Impact × Confidence) / Effort

Reach: # of users affected per time period
Impact: 0.25 (minimal), 0.5 (low), 1 (medium), 2 (high), 3 (massive)
Confidence: 0-100% (how sure you are)
Effort: Person-months required
```

**Example:**
```
Feature: In-app notifications
Reach: 10,000 users/month
Impact: 2 (high)
Confidence: 80%
Effort: 2 person-months

RICE = (10000 × 2 × 0.8) / 2 = 8,000
```

### Value vs Effort Matrix
```
          High Value
              │
    Quick    │    Strategic
    Wins     │    Bets
             │
────────────┼────────────────→
             │         High Effort
    Fill-Ins │    Time
             │    Sinks
          Low Value
```

**Decision Rules:**
- Quick Wins: Do first (high value, low effort)
- Strategic Bets: Plan carefully (high value, high effort)
- Fill-Ins: Do if capacity allows (low value, low effort)
- Time Sinks: Avoid (low value, high effort)

## Roadmap Communication

### Stakeholder-Specific Views

**Executive Roadmap:**
- Focus: Strategic themes, OKRs, business outcomes
- Timeline: Annual with quarterly milestones
- Metrics: Revenue, retention, market share

**Sales Roadmap:**
- Focus: Customer-facing features, competitive positioning
- Timeline: Now-Next-Later (no hard dates)
- Include: Customer pain points solved, deal enablers

**Engineering Roadmap:**
- Focus: Technical initiatives, architecture, infrastructure
- Timeline: Quarterly sprints
- Include: Tech debt, performance, scalability

**Customer Roadmap (Public):**
- Focus: Upcoming features, improvements
- Timeline: Vague ("Coming soon", "In progress")
- Avoid: Specific dates, internal projects

## Roadmap Maintenance

### Review Cadence
- **Weekly:** Progress check with team
- **Monthly:** Stakeholder sync, reprioritize
- **Quarterly:** Strategic review, next quarter planning
- **Annual:** Vision refresh, long-term goals

### When to Update
- Major customer feedback received
- Competitive landscape shifts
- Technical blockers discovered
- Strategic priorities change
- Capacity constraints emerge

## Resources
- Roadmap templates (Now-Next-Later, Timeline, Theme-based)
- Prioritization calculator (RICE score)
- Stakeholder communication templates

---
**Last Updated:** November 23, 2025
**Related:** okr_methodology.md, frameworks.md
