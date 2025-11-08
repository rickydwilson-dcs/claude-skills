# Product Strategy Tools Documentation

Complete documentation for strategic planning Python tools.

## okr_cascade_generator.py

Automated OKR hierarchy generator with alignment tracking.

### Overview

**Purpose:** Generate cascading OKRs from company level down to team level, with automatic alignment scoring and contribution analysis.

**Key Capabilities:**
- Pre-built strategy templates (growth, retention, revenue, innovation, operational)
- Three-level cascade (company → product → team)
- Alignment score calculation
- Contribution percentage tracking
- Multiple output formats (text, JSON, CSV)
- Detailed metric definitions

### Installation

**Requirements:**
- Python 3.8+
- No external dependencies (uses standard library only)

**Setup:**
```bash
# No installation needed - uses Python standard library
python3 scripts/okr_cascade_generator.py --help
```

### Usage

#### Basic Usage

**Growth strategy OKRs:**
```bash
python3 scripts/okr_cascade_generator.py growth
```

**Retention strategy:**
```bash
python3 scripts/okr_cascade_generator.py retention
```

**Revenue strategy:**
```bash
python3 scripts/okr_cascade_generator.py revenue
```

**Innovation strategy:**
```bash
python3 scripts/okr_cascade_generator.py innovation
```

**Operational excellence:**
```bash
python3 scripts/okr_cascade_generator.py operational
```

#### Output Formats

**JSON output (for dashboards):**
```bash
python3 scripts/okr_cascade_generator.py growth --output json
```

**CSV output (for spreadsheets):**
```bash
python3 scripts/okr_cascade_generator.py growth --output csv
```

**Save to file:**
```bash
python3 scripts/okr_cascade_generator.py growth -o json -f okrs.json
```

#### Advanced Options

**Include detailed metric definitions:**
```bash
python3 scripts/okr_cascade_generator.py growth --metrics
```

**Verbose mode (detailed output):**
```bash
python3 scripts/okr_cascade_generator.py growth -v
```

**Combined:**
```bash
python3 scripts/okr_cascade_generator.py growth --metrics -v -o json -f growth_okrs.json
```

### Command-Line Options

```
usage: okr_cascade_generator.py [-h] [--output {text,json,csv}]
                                [--file FILE] [--metrics] [--verbose]
                                [--version]
                                {growth,retention,revenue,innovation,operational}

Generate cascading OKRs with alignment tracking

positional arguments:
  {growth,retention,revenue,innovation,operational}
                        Strategy type to generate OKRs for

options:
  -h, --help            show this help message and exit
  --output {text,json,csv}, -o {text,json,csv}
                        Output format (default: text)
  --file FILE, -f FILE  Write output to file instead of stdout
  --metrics             Include detailed metric definitions
  --verbose, -v         Enable detailed output with explanations
  --version             show program's version number and exit
```

### Strategy Templates

#### Growth Strategy
**Focus:** User/revenue acquisition and market expansion

**Company-Level Objective:**
"Expand market leadership and accelerate growth"

**Key Results:**
- Increase monthly active users from 100K to 250K
- Grow revenue from $10M to $25M ARR
- Launch in 3 new geographic markets

**Product-Level:**
- Build viral features for user acquisition
- Optimize onboarding conversion
- Enable multi-language support

**Team-Level:**
- Ship referral program
- Reduce time-to-first-value
- Implement localization framework

**Use When:**
- Entering growth phase
- Seeking market expansion
- Raising growth funding round

#### Retention Strategy
**Focus:** Customer lifetime value and churn reduction

**Company-Level Objective:**
"Maximize customer lifetime value and reduce churn"

**Key Results:**
- Increase Net Retention Rate from 95% to 110%
- Reduce customer churn from 5% to 3%
- Achieve 95% customer satisfaction score

**Product-Level:**
- Build customer success dashboard
- Implement usage analytics
- Create engagement triggers

**Team-Level:**
- Ship health scoring system
- Build automated playbooks
- Implement proactive outreach

**Use When:**
- High churn rates observed
- Focusing on profitability
- Mature product with stable acquisition

#### Revenue Strategy
**Focus:** Monetization and revenue optimization

**Company-Level Objective:**
"Optimize monetization and drive revenue growth"

**Key Results:**
- Increase ARPU from $50 to $75
- Achieve 30% upsell rate from freemium
- Launch premium tier generating $5M ARR

**Product-Level:**
- Build premium feature set
- Implement usage-based pricing
- Create upgrade prompts

**Team-Level:**
- Ship analytics premium tier
- Build billing management
- Implement pricing experiments

**Use When:**
- Need to improve unit economics
- Expanding pricing tiers
- Optimizing monetization strategy

#### Innovation Strategy
**Focus:** New products and market opportunities

**Company-Level Objective:**
"Drive innovation and explore new market opportunities"

**Key Results:**
- Launch 2 new product lines
- Achieve 10K beta users for new products
- Generate $2M ARR from innovations

**Product-Level:**
- Build experimentation framework
- Ship new product MVP
- Validate product-market fit

**Team-Level:**
- Research new use cases
- Build prototype and test
- Iterate based on feedback

**Use When:**
- Exploring adjacent markets
- Building new product lines
- Innovating on core product

#### Operational Strategy
**Focus:** Efficiency, scalability, and technical excellence

**Company-Level Objective:**
"Build operational excellence and scalable systems"

**Key Results:**
- Achieve 99.9% uptime (from 99.5%)
- Reduce cost per transaction by 30%
- Improve deployment frequency to daily

**Product-Level:**
- Refactor core platform
- Implement monitoring and alerts
- Automate deployment pipeline

**Team-Level:**
- Build CI/CD automation
- Implement performance monitoring
- Reduce technical debt by 40%

**Use When:**
- Scaling infrastructure
- Improving reliability
- Paying down technical debt

### Output Formats

#### Text Output (Default)

Human-readable format with full OKR hierarchy:

```
=================================================================
CASCADING OKRs: GROWTH STRATEGY
=================================================================

COMPANY LEVEL
=================================================================

Objective: Expand market leadership and accelerate growth

Key Result 1: Increase monthly active users from 100,000 to 250,000
  Baseline: 100,000 MAU
  Target: 250,000 MAU
  Progress: 0% (Not started)

Key Result 2: Grow annual recurring revenue from $10M to $25M
  Baseline: $10M ARR
  Target: $25M ARR
  Progress: 0% (Not started)

Key Result 3: Launch in 3 new geographic markets
  Baseline: 1 market
  Target: 4 markets
  Progress: 0% (Not started)

-----------------------------------------------------------------

PRODUCT LEVEL
=================================================================

Objective: Build viral growth features to accelerate user acquisition

Alignment Score: 95%
Contribution to Company KR1: 60%
Contribution to Company KR2: 30%

Key Result 1: Increase viral coefficient from 0.8 to 1.5
  Baseline: 0.8 K-factor
  Target: 1.5 K-factor
  Progress: 0% (Not started)
  Supports: Company KR1 (MAU growth)

[...more key results...]

-----------------------------------------------------------------

TEAM LEVEL
=================================================================

Team: Growth Engineering

Objective: Ship viral features to drive user-driven growth

Alignment Score: 90%
Contribution to Product KR1: 70%
Contribution to Product KR2: 20%

[...team key results...]
```

#### JSON Output

Machine-readable format for dashboards and tools:

```json
{
  "metadata": {
    "strategy_type": "growth",
    "generated_date": "2025-11-08",
    "tool_version": "1.0.0"
  },
  "company": {
    "objective": "Expand market leadership and accelerate growth",
    "key_results": [
      {
        "id": "C-KR1",
        "description": "Increase monthly active users from 100,000 to 250,000",
        "baseline": 100000,
        "target": 250000,
        "unit": "users",
        "progress": 0,
        "status": "not_started"
      }
    ]
  },
  "product": {
    "objective": "Build viral growth features to accelerate user acquisition",
    "alignment_score": 95,
    "key_results": [
      {
        "id": "P-KR1",
        "description": "Increase viral coefficient from 0.8 to 1.5",
        "baseline": 0.8,
        "target": 1.5,
        "unit": "k-factor",
        "contributes_to": ["C-KR1"],
        "contribution_pct": 60
      }
    ]
  },
  "teams": [
    {
      "name": "Growth Engineering",
      "objective": "Ship viral features to drive user-driven growth",
      "alignment_score": 90,
      "key_results": [...]
    }
  ]
}
```

#### CSV Output

Spreadsheet format for Excel/Google Sheets:

```csv
level,team,objective,kr_id,key_result,baseline,target,unit,contributes_to,alignment_score
company,,Expand market leadership,C-KR1,Increase MAU,100000,250000,users,,100
company,,Expand market leadership,C-KR2,Grow ARR,10000000,25000000,dollars,,100
product,,Build viral features,P-KR1,Viral coefficient,0.8,1.5,k-factor,C-KR1,95
team,Growth Eng,Ship viral features,T-KR1,Referral program,0,10000,users,P-KR1,90
```

### Alignment Scoring

The tool calculates alignment between levels:

**Alignment Score Formula:**
```
Alignment = (Direct Contribution + Strategic Fit + Metric Correlation) / 3

Components:
- Direct Contribution: Does team KR directly support product KR?
- Strategic Fit: Does objective align with higher-level objective?
- Metric Correlation: Are metrics causally related?

Score Range:
- 90-100%: Excellent alignment
- 75-89%: Good alignment
- 60-74%: Moderate alignment
- <60%: Poor alignment (needs revision)
```

**Example:**
```
Company KR: Increase MAU from 100K to 250K
Product KR: Increase viral coefficient from 0.8 to 1.5
Team KR: Ship referral program with 10K referred users

Alignment Analysis:
- Direct Contribution: 100% (referrals directly increase MAU)
- Strategic Fit: 90% (viral growth supports user growth)
- Metric Correlation: 80% (referrals → K-factor → MAU)
Average Alignment: 90%
```

### Contribution Tracking

**Contribution Percentage:**
Shows how much each lower-level KR contributes to higher-level KR.

```
Company KR1: Increase MAU from 100K to 250K (150K increase)

Product Contributions:
- P-KR1 (Viral Growth): 60% (90K users from referrals)
- P-KR2 (Onboarding): 30% (45K users from better conversion)
- P-KR3 (Multi-language): 10% (15K users from new markets)
Total: 100% (all paths to achieving company KR)

Team Contributions to P-KR1:
- T-KR1 (Referral Program): 70% (63K users)
- T-KR2 (Sharing Features): 20% (18K users)
- T-KR3 (Social Integration): 10% (9K users)
```

### Integration Patterns

#### OKR Dashboard Integration

```bash
# Generate OKRs as JSON
python3 scripts/okr_cascade_generator.py growth -o json -f okrs.json

# Import to dashboard tool
curl -X POST https://okr-tool.com/api/okrs \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d @okrs.json
```

#### Spreadsheet Workflow

```bash
# Export as CSV
python3 scripts/okr_cascade_generator.py growth -o csv -f okrs.csv

# Open in Excel/Google Sheets
# Add columns: Owner, Status, Weekly Progress
# Share with team for tracking
```

#### Confluence Documentation

```bash
# Generate with metrics
python3 scripts/okr_cascade_generator.py growth --metrics -v > okrs.txt

# Copy to Confluence page
# Format as table for easy reading
# Link to tracking dashboards
```

#### Slack Notifications

```bash
# Generate text summary
OKRS=$(python3 scripts/okr_cascade_generator.py growth)

# Post to Slack
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer TOKEN" \
  -d "channel=#okrs" \
  -d "text=$OKRS"
```

### Customization Guide

#### Modifying Strategy Templates

The tool uses pre-built templates, but you can modify the script to add custom strategies:

**Template Structure:**
```python
{
    'strategy_type': 'custom',
    'company': {
        'objective': 'Custom objective',
        'key_results': [
            {
                'description': 'KR description',
                'baseline': 0,
                'target': 100,
                'unit': 'units'
            }
        ]
    },
    'product': {...},
    'teams': [...]
}
```

#### Adjusting Alignment Weights

Modify alignment calculation by editing the script:

```python
# Default weights
ALIGNMENT_WEIGHTS = {
    'direct_contribution': 0.5,
    'strategic_fit': 0.3,
    'metric_correlation': 0.2
}

# Adjust for your org
ALIGNMENT_WEIGHTS = {
    'direct_contribution': 0.6,  # Emphasize direct impact
    'strategic_fit': 0.25,
    'metric_correlation': 0.15
}
```

### Best Practices

**DO:**
- Start with pre-built strategy template that matches your focus
- Review generated OKRs and customize for your context
- Use alignment scores to identify misaligned OKRs
- Track contribution percentages to ensure balanced effort
- Export to JSON/CSV for dashboard integration
- Include metric definitions for clarity
- Review OKRs with team before committing

**DON'T:**
- Use generated OKRs without customization
- Ignore low alignment scores (<75%)
- Create OKRs that don't contribute to higher levels
- Set too many key results (3-5 max per objective)
- Use vague or unmeasurable key results
- Skip team-level cascading
- Treat OKRs as fixed (adjust quarterly based on learnings)

### Troubleshooting

#### Issue: Generated OKRs don't fit our context

**Solution:** Use template as starting point, customize for your needs

```bash
# Generate base template
python3 scripts/okr_cascade_generator.py growth -o json -f template.json

# Edit JSON to match your metrics
# Example: Change "MAU" to "Daily Active Users"
# Adjust baselines and targets to your reality
```

#### Issue: Alignment scores seem incorrect

**Solution:** Review the alignment logic and contribution percentages

```bash
# Use verbose mode to see alignment calculation
python3 scripts/okr_cascade_generator.py growth -v

# Check that:
# - Team KRs directly support product KRs
# - Product KRs directly support company KRs
# - Metrics have causal relationship
```

#### Issue: Too many OKRs generated

**Solution:** Focus on top priorities, remove lower-priority KRs

```bash
# Generate full set
python3 scripts/okr_cascade_generator.py growth -o json -f full_okrs.json

# Edit JSON to keep only top 3 company OKRs
# Keep top 3 product KRs per company KR
# Keep top 3 team KRs per product KR
```

#### Issue: Need different strategy type

**Solution:** Combine strategies or create custom template

```bash
# Generate two strategies
python3 scripts/okr_cascade_generator.py growth -o json -f growth.json
python3 scripts/okr_cascade_generator.py retention -o json -f retention.json

# Merge manually, keeping best OKRs from each
# Focus: 2 OKRs from growth + 1 from retention
```

### Performance Tips

**Large Organizations:**
- Generate OKRs for each department separately
- Use JSON format for programmatic merging
- Create one master OKR file per quarter

**Quarterly Cadence:**
- Generate new OKRs at start of quarter
- Track progress weekly in separate tool
- Grade OKRs at end of quarter (0.0-1.0 scale)
- Use learnings to inform next quarter

**Tool Integration:**
- Export to JSON for API integration
- Use CSV for manual tracking in spreadsheets
- Use text format for documentation and sharing

---

**Last Updated:** 2025-11-08
**Tool Version:** 1.0.0
**Related Files:**
- [frameworks.md](frameworks.md) - OKR frameworks, strategy types, alignment principles
- [templates.md](templates.md) - OKR templates and strategic planning formats
