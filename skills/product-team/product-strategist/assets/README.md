# Product Strategist - Sample Assets

This directory contains sample data for OKR (Objectives and Key Results) cascade generation and strategic planning.

## Sample Files

### 1. sample-metrics.json
**Purpose:** Current business metrics and targets for OKR generation

**Description:** Realistic Series A company metrics including:
- Current performance (MAU, ARR, NPS, churn rate)
- Growth targets (30% ARR growth typical for Series A)
- Retention and revenue targets
- Team structure (current and target)
- Strategic initiatives for the year

**Key Sections:**
- `current_metrics`: Today's baseline
- `targets_growth`: User and revenue growth goals
- `targets_retention`: Engagement and churn targets
- `targets_revenue`: ARR and margin goals
- `targets_innovation`: New products and features
- `team_structure`: Current headcount by function
- `strategic_initiatives`: Key projects for the year

**How to Use:**
```bash
# Generate growth-focused OKRs
python ../scripts/okr_cascade_generator.py

# Or load metrics for reference
cat sample-metrics.json
```

**What to Expect:**
- Company-level OKRs
- Product team OKRs
- Engineering team OKRs
- Sales/Marketing team OKRs
- Key results with success metrics

---

## Using This Sample

### Quick Start

```bash
cd /Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My\ Drive/Websites/GitHub/claude-skills/product-team/product-strategist/

# Generate OKRs with sample metrics
python scripts/okr_cascade_generator.py

# Different strategic focus
python scripts/okr_cascade_generator.py growth    # Growth strategy
python scripts/okr_cascade_generator.py retention # Retention strategy
python scripts/okr_cascade_generator.py revenue   # Revenue strategy
```

---

## Understanding OKRs

### OKR Framework

**Objectives:** Qualitative goals
- Direction for the company
- Inspirational and memorable
- Example: "Become the analytics leader for mid-market"

**Key Results:** Quantitative measures
- 3-5 per objective
- Measurable and time-bound
- Examples:
  - "Grow MAU from 15K to 25K"
  - "Achieve 60 NPS (from 42)"
  - "Launch 3 new integrations"

### OKR Levels

1. **Company OKRs** → 3-5 objectives for the whole company
2. **Department OKRs** → Each team contributes to company goals
3. **Team OKRs** → Individual contributor goals aligned to team

---

## Metric Baselines & Targets

### Growth Strategy Metrics

| Metric | Baseline | Target | Growth Rate |
|--------|----------|--------|-------------|
| MAU | 15,000 | 25,000 | 67% |
| ARR | $2.2M | $4.5M | 104% |
| CAC | $18 | $15 | -17% (efficient) |
| LTV/CAC | 3.2x | 5.0x | +56% |

### Retention Strategy Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| NPS | 42 | 60 |
| Annual Retention | 92% | 95% |
| Monthly Churn | 0.8% | 0.5% |
| Net Retention Rate | 110% | 125% |

### Revenue Strategy Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| ARR | $2.2M | $4.5M |
| ARPU | $148 | $185 |
| Gross Margin | 72% | 75% |
| Revenue Churn | 0% | <0.5% |

---

## OKR Examples by Strategy

### Growth Strategy

```
Company Objective: "Expand market reach and accelerate growth"

Key Results:
1. Grow MAU from 15K to 25K (67% growth)
2. Achieve $4.5M ARR (104% growth)
3. Expand to 3 new geographic markets
4. Reduce CAC from $18 to $15

Product Team Aligns With:
- Objective: "Build features that drive adoption"
- Key Results:
  - New onboarding reduces time-to-value by 50%
  - 3 integrations with top platforms
  - Mobile app reaches 20% of user base

Engineering Aligns With:
- Objective: "Enable product growth through performance"
- Key Results:
  - API response time <200ms p95
  - System handles 3x current load
  - Zero critical incidents
```

### Retention Strategy

```
Company Objective: "Create lasting customer loyalty"

Key Results:
1. Improve NPS from 42 to 60
2. Increase annual retention to 95%
3. Reduce churn to <0.5% monthly
4. Increase LTV/CAC ratio from 3.2x to 5.0x

Product Team Aligns With:
- Objective: "Deliver delightful customer experiences"
- Key Results:
  - Customer satisfaction score reaches 90%
  - Feature adoption for top 5 features reaches 80%
  - Support ticket response time <2 hours

Success Team Aligns With:
- Objective: "Become trusted advisors to customers"
- Key Results:
  - Net Retention Rate reaches 125%
  - 95% of customers adopt recommended features
  - Expand accounts by avg 30% within 12 months
```

---

## Creating Your Metrics

### Data Collection

Required metrics:
1. **User Metrics**: MAU, DAU, new users, activation rate
2. **Revenue Metrics**: MRR, ARR, ARPU, gross margin
3. **Retention Metrics**: Churn rate, NPS, retention cohorts
4. **Efficiency Metrics**: CAC, LTV, LTV/CAC ratio, Rule of 40

### Baseline Establishment

```
Step 1: Collect current month/quarter data
Step 2: Calculate each metric
Step 3: Understand trend (growing? declining? stable?)
Step 4: Review last year for seasonality
Step 5: Establish "current baseline"
```

### Target Setting

**Growth Targets by Stage:**
- Series A: 100%+ YoY growth
- Series B: 50-100% YoY growth
- Series C: 30-50% YoY growth
- Public: 20-30% YoY growth

**Retention Targets:**
- SaaS Average: 90% annual retention
- Best-in-class: 95%+ annual retention
- High-growth: Often 100-110% NRR (expansion revenue)

---

## Strategy Examples

### Series A Focus: Growth
```json
{
  "strategy": "growth",
  "objectives": [
    "Accelerate user acquisition and market expansion",
    "Achieve product-market fit in new segments",
    "Build sustainable growth engine"
  ]
}
```

### Mid-Market Shift: Retention
```json
{
  "strategy": "retention",
  "objectives": [
    "Create lasting customer value and loyalty",
    "Build best-in-class user experience",
    "Maximize customer lifetime value"
  ]
}
```

### Enterprise Play: Revenue
```json
{
  "strategy": "revenue",
  "objectives": [
    "Drive sustainable revenue growth",
    "Optimize monetization strategy",
    "Expand revenue per customer"
  ]
}
```

---

## Cascading OKRs

### Framework

```
Company Level (Q1 2025):
  O1: Grow market leadership
    KR1: Grow ARR to $4.5M
    KR2: Achieve 60 NPS

Product Team (Contributes):
  O1: Enable company growth through features
    KR1: Launch 3 enterprise features
    KR2: Improve onboarding (T2V -50%)

Engineering Team (Contributes):
  O1: Support product goals through infrastructure
    KR1: Reduce API response time to <200ms
    KR2: Handle 3x current load
```

### Alignment Principles

1. **Cascade Down**: Company → Product → Teams
2. **Inform Sideways**: Cross-functional alignment
3. **Limit Scope**: 3-5 objectives per level (usually)
4. **Stretch But Achievable**: 70-80% success rate
5. **Review Quarterly**: Adjust based on progress

---

## Grading OKRs

### Success Scoring

- **1.0**: Achieved 100%+ of key result
- **0.7-0.9**: Good progress (typical 70-80%)
- **0.4-0.6**: Made progress but missed
- **<0.4**: Minimal progress, needs review

### What to Measure

```
Good KR: "Grow ARR from $2.2M to $4.5M"
- Measurable: Specific dollar amount
- Achievable: Stretchy but possible
- Relevant: Core to strategy
- Time-bound: Clear quarter

Bad KR: "Improve retention"
- Too vague: No target metric
- Unmeasurable: Can't track objectively
- No time bound: When by?
```

---

## Tools & Integration

### Spreadsheet Tracking
```bash
# Export OKRs for team tracking
python scripts/okr_cascade_generator.py --output csv > okrs.csv
```

### Wiki/Confluence
```bash
# Generate OKR documentation
python scripts/okr_cascade_generator.py --output markdown > OKRs-Q1-2025.md
```

### Dashboard
```bash
# JSON for integration with dashboards
python scripts/okr_cascade_generator.py --output json > okr-data.json
```

---

## Common Mistakes to Avoid

1. **Too Many OKRs**: Limit to 3-5 per level
2. **Task Confusion**: KRs are goals, not tasks/initiatives
3. **No Ownership**: Each OKR needs a single owner
4. **Not Stretch**: Should be ambitious (70-80% success)
5. **Siloed Goals**: Need cross-team alignment
6. **Activity Goals**: "Launch feature" ≠ outcome
7. **No Tracking**: Monthly reviews are critical

---

## Best Practices

1. **Quarterly Cadence**
   - Set at start of quarter
   - Review weekly in all-hands
   - Grade and adjust at end of quarter

2. **Company Alignment**
   - Start with company-level OKRs
   - All departments map to company OKRs
   - Create draft → Get feedback → Finalize

3. **Visibility**
   - Share broadly
   - Track progress weekly
   - Communicate blockers
   - Celebrate wins publicly

4. **Flexibility**
   - Can adjust if market changes
   - If not progressing by mid-quarter, discuss
   - Document reasons for changes

---

## File Specifications

**sample-metrics.json:**
- Format: JSON
- Encoding: UTF-8
- Required: current_metrics, targets (at least one)
- Optional: team_structure, strategic_initiatives
- Units: Users (count), Revenue (USD), Rates (percentage or decimal)

---

## Related Documentation

- **OKR Cascade Generator:** [../scripts/okr_cascade_generator.py](../scripts/okr_cascade_generator.py)
- **OKR Framework Guide:** [../references/](../references/) (if available)
- **Product Strategy Guide:** [../SKILL.md](../SKILL.md)

---

**Last Updated:** November 5, 2025
**Format:** Sample Assets README
**Included Files:** 1 (sample-metrics.json)
**Script Version:** okr_cascade_generator.py 1.0.0
