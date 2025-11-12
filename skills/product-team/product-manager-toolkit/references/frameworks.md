# Product Management Frameworks

Detailed frameworks and methodologies for product prioritization, discovery, and metrics.

## Prioritization Frameworks

### RICE Framework

Complete scoring methodology for feature prioritization.

```
Score = (Reach × Impact × Confidence) / Effort

Reach: # of users/quarter
Impact:
  - Massive = 3x
  - High = 2x
  - Medium = 1x
  - Low = 0.5x
  - Minimal = 0.25x
Confidence:
  - High = 100%
  - Medium = 80%
  - Low = 50%
Effort: Person-months
```

**How to Apply:**

1. **Estimate Reach**: How many users/customers will this feature affect per quarter?
   - Count actual users, not page views
   - Use quarterly timeframe for consistency
   - Example: 500 users/quarter

2. **Score Impact**: How much will this move the needle per person?
   - Massive (3x): Core value proposition, game-changing
   - High (2x): Significant improvement to key workflow
   - Medium (1x): Noticeable improvement
   - Low (0.5x): Small improvement
   - Minimal (0.25x): Barely noticeable

3. **Assess Confidence**: How certain are you about reach and impact?
   - High (100%): Strong data, validated with users
   - Medium (80%): Some data, reasonable assumptions
   - Low (50%): Hypothesis-driven, little validation

4. **Calculate Effort**: Person-months to ship to production
   - Include design, development, testing, deployment
   - Use T-shirt sizes if helpful: XS(0.5), S(1), M(2), L(5), XL(8+)

**Portfolio Analysis:**

Sort features by RICE score and categorize:
- Top 20%: Must-haves for roadmap
- Middle 60%: Evaluate based on strategy fit
- Bottom 20%: Deprioritize or eliminate

### Value vs Effort Matrix

2x2 prioritization for quick decisions.

```
         Low Effort    High Effort

High     QUICK WINS    BIG BETS
Value    [Prioritize]   [Strategic]

Low      FILL-INS      TIME SINKS
Value    [Maybe]       [Avoid]
```

**Quick Wins**: High value, low effort - do these first
- Example: Add keyboard shortcuts, fix high-impact bugs

**Big Bets**: High value, high effort - strategic investments
- Example: New product line, major platform rewrite

**Fill-Ins**: Low value, low effort - do when capacity available
- Example: UI polish, minor features

**Time Sinks**: Low value, high effort - avoid or eliminate
- Example: Low-usage features, edge cases

**Usage Tips:**
- Use for quick portfolio review (15-30 min)
- Best with cross-functional team input
- Combine with RICE for detailed scoring

### MoSCoW Method

Collaborative prioritization for stakeholder alignment.

- **Must Have**: Critical for launch, business won't work without it
  - Non-negotiable features
  - Regulatory requirements
  - Core value proposition

- **Should Have**: Important but not critical, can launch without
  - Enhances user experience
  - Competitive parity features
  - Can be delayed 1-2 quarters

- **Could Have**: Nice to have, adds value but not essential
  - Delighters
  - Edge case support
  - Future-proofing features

- **Won't Have**: Out of scope for this release
  - Explicitly call out to prevent scope creep
  - Revisit in future planning cycles

**When to Use:**
- Sprint planning with stakeholders
- Scope negotiation for fixed timelines
- Post-prioritization alignment

### Kano Model

Understand feature types and satisfaction impact.

**Feature Categories:**

1. **Basic Expectations**: Must work, but don't delight
   - Example: Login, basic CRUD operations
   - Absence creates dissatisfaction
   - Presence doesn't increase satisfaction

2. **Performance Features**: More is better
   - Example: Speed, capacity, accuracy
   - Linear relationship with satisfaction
   - Focus on cost-effective improvements

3. **Delighters**: Unexpected features that wow users
   - Example: Smart defaults, thoughtful UX touches
   - High satisfaction when present
   - No dissatisfaction when absent

4. **Indifferent**: Users don't care either way
   - Example: Edge case features, technical preferences
   - Don't invest resources here

**Application:**
- Survey users: "How would you feel if this feature existed?"
- Plot responses on satisfaction curve
- Prioritize delighters and performance features
- Ensure all basic expectations are met

## Discovery Frameworks

### Customer Interview Guide

Structured format for conducting effective interviews.

#### Pre-Interview Preparation (15 min)
- Review customer background (company, role, usage)
- Prepare hypothesis to test
- Set up recording (with permission)
- Have note-taker join if possible

#### Interview Structure (35 min total)

**1. Context Questions (5 min)**
```
- Tell me about your role and what you're responsible for
- Walk me through a typical day/week in your role
- What tools and systems do you use regularly?
- How does [our product area] fit into your workflow?
```

**2. Problem Exploration (15 min)**
```
- What are the biggest challenges you face in [problem area]?
- Tell me about the last time you encountered [specific problem]
- How do you currently solve/work around this?
- How often does this come up? (daily/weekly/monthly)
- What's the impact when this problem occurs? (time/money/frustration)
- Have you tried other solutions? What happened?
```

**Key Technique:** Ask "Tell me about the last time..." for concrete examples vs hypothetical futures.

**3. Solution Validation (10 min)**
```
- [Show concept/mockup] What's your initial reaction?
- How would this fit into your current workflow?
- What concerns do you have about this approach?
- What would make this a must-have vs nice-to-have?
- Would you be willing to pay for this? How much?
- What's missing that would make this more valuable?
```

**4. Wrap-up (5 min)**
```
- Is there anything I didn't ask about that I should have?
- Who else should I talk to about this problem?
- Can I follow up with you as we develop this?
- Would you be interested in beta testing?
```

#### Post-Interview (10 min)
- Transcribe key quotes immediately
- Rate pain level (high/medium/low)
- Identify patterns across interviews
- Update interview tracker

### Hypothesis Template

Structured format for testable product hypotheses.

```
We believe that [building this feature/making this change]
For [these specific users/customer segment]
Will achieve [this measurable outcome]
We'll know we're right when we see [this metric/signal]
```

**Example:**
```
We believe that adding real-time collaboration
For teams of 5+ users
Will increase daily active usage by 30%
We'll know we're right when we see average session time increase from 15 to 25 minutes
```

**Validation Criteria:**
- Falsifiable: Can prove it wrong
- Measurable: Clear success metrics
- Specific: Targeted user segment
- Time-bound: When will you know?

**Testing Approaches:**
- Prototype testing (qualitative)
- A/B test (quantitative)
- Fake door test (interest)
- Concierge MVP (manual version)

### Opportunity Solution Tree

Visual framework for connecting outcomes to solutions.

```
Desired Outcome
├── Opportunity 1
│   ├── Solution A
│   ├── Solution B
│   └── Solution C
└── Opportunity 2
    ├── Solution D
    └── Solution E
```

**Complete Example:**
```
Outcome: Increase enterprise customer retention to 95%
├── Opportunity: Reduce onboarding time
│   ├── Solution: Interactive product tour
│   ├── Solution: Onboarding checklist
│   └── Solution: Dedicated CSM for first 30 days
├── Opportunity: Improve admin controls
│   ├── Solution: SSO integration
│   ├── Solution: User provisioning API
│   └── Solution: Custom role permissions
└── Opportunity: Increase feature adoption
    ├── Solution: In-app feature announcements
    ├── Solution: Usage analytics dashboard
    └── Solution: Quarterly business review reports
```

**Usage Process:**
1. Start with business outcome (top)
2. Identify opportunity areas through research
3. Generate multiple solutions per opportunity
4. Test solutions continuously
5. Prune/add branches based on learnings

**Benefits:**
- Shows many paths to same outcome
- Prevents solution fixation
- Communicates strategy visually
- Guides discovery work

## Metrics & Analytics

### North Star Metric Framework

Find the metric that defines product success.

**Criteria for North Star Metric:**

1. **Expresses Core Value**: What's the #1 value to users?
   - Example (Airbnb): Nights booked
   - Example (Slack): Messages sent by teams
   - Example (Spotify): Time spent listening

2. **Leads to Revenue**: Predicts business success
   - May not be revenue directly
   - But correlates with monetization

3. **Actionable**: Teams can influence it
   - Not too high-level (vanity metrics)
   - Not too low-level (micrometrics)

4. **Measurable**: Can track reliably
   - Available in analytics tools
   - Updates frequently enough for feedback

**Process to Find Your North Star:**

1. List top 3 value propositions
2. For each, identify measurable user action
3. Validate correlation with retention/revenue
4. Choose metric teams can influence
5. Define input metrics that drive North Star

**Input Metrics (Leading Indicators):**
```
North Star: Weekly Active Users
├── Breadth: New user signups
├── Depth: Features used per session
└── Frequency: Days active per week
```

### Funnel Analysis Template

Track user journey from acquisition to revenue.

**AARRR Framework (Pirate Metrics):**

```
Acquisition → Activation → Retention → Revenue → Referral

Key Metrics:
- Conversion rate at each step
- Drop-off points and reasons
- Time between steps
- Cohort variations
- Channel performance
```

**Example E-Commerce Funnel:**
```
1. Acquisition: Visit website (100%)
   ↓ 40% conversion
2. Activation: View product (40%)
   ↓ 30% conversion
3. Retention: Add to cart (12%)
   ↓ 60% conversion
4. Revenue: Complete purchase (7.2%)
   ↓ 20% conversion
5. Referral: Share with friend (1.4%)
```

**Analysis Questions:**
- Where is biggest drop-off?
- How do cohorts compare (mobile vs desktop, organic vs paid)?
- What's time-to-conversion for successful users?
- Which channel has best cost-per-acquisition?

**Optimization Process:**
1. Identify weakest conversion step
2. Hypothesis for why users drop off
3. Test solutions (A/B tests)
4. Measure impact on funnel
5. Repeat for next bottleneck

### Feature Success Metrics

Framework for measuring feature performance.

**5 Key Dimensions:**

1. **Adoption**: % of users who tried feature
   - Target: 40%+ of target segment in first quarter
   - Measured: Unique users who performed key action

2. **Frequency**: How often users engage with feature
   - Target: Varies by feature type (daily/weekly/monthly)
   - Measured: Average uses per user per time period

3. **Depth**: % of feature capability used
   - Target: Users engage with multiple aspects
   - Measured: # of sub-features used per session

4. **Retention**: Continued usage over time
   - Target: 60%+ of adopters still using after 30 days
   - Measured: Cohort retention curves

5. **Satisfaction**: User sentiment about feature
   - Target: NPS 40+ or CSAT 4.0+
   - Measured: In-app surveys, support tickets

**Feature Health Scorecard:**
```
Feature: Real-time Collaboration
- Adoption: 45% (target: 40%) ✓
- Frequency: 3.2x/week (target: 2x/week) ✓
- Depth: 2.1 features/session (target: 2) ✓
- Retention: 55% at Day 30 (target: 60%) ✗
- Satisfaction: NPS 38 (target: 40) ✗

Action: Focus on retention - interview churned users
```

### Cohort Analysis Framework

Track user behavior over time by cohort.

**Common Cohort Types:**
- Signup date (monthly cohorts)
- Acquisition channel (organic, paid, referral)
- User segment (enterprise, SMB, individual)
- Feature adoption (adopted feature X in week 1)

**Example Retention Cohort:**
```
         Week 0  Week 1  Week 2  Week 4  Week 8
Jan '24   100%    45%     32%     22%     18%
Feb '24   100%    48%     35%     25%     21%
Mar '24   100%    52%     38%     28%     --
Apr '24   100%    55%     42%     --      --
```

**Analysis Questions:**
- Are newer cohorts performing better? (product improvements working?)
- Which acquisition channel has best retention?
- When do users typically churn? (onboarding issue vs long-term value?)
- Do power features improve retention?

**Usage:**
- Monthly product reviews
- Feature impact analysis
- Pricing/packaging changes
- Growth experiment validation

---

**Last Updated:** 2025-11-08
**Related Files:**
- [templates.md](templates.md) - Interview guides and PRD templates
- [tools.md](tools.md) - RICE calculator and integration setup
