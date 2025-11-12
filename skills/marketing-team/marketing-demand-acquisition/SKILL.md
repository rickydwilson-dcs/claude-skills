---
name: marketing-demand-acquisition
description: Multi-channel demand generation, paid media optimization, SEO strategy, and partnership programs for Series A+ startups. Includes CAC calculator, channel playbooks, HubSpot integration, and international expansion tactics. Use when planning demand generation campaigns, optimizing paid media, building SEO strategies, establishing partnerships, or when user mentions demand gen, paid ads, LinkedIn ads, Google ads, CAC, acquisition, lead generation, or pipeline generation.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: marketing
  domain: demand-generation
  updated: 2025-11-08
  keywords:
    - demand generation
    - lead generation
    - paid advertising
    - LinkedIn Ads
    - Google Ads
    - customer acquisition cost
    - CAC calculator
    - paid media
    - performance marketing
    - SEO strategy
    - SEM
    - paid search
    - retargeting
    - conversion optimization
    - marketing funnel
    - pipeline generation
    - MQL to SQL
    - affiliate marketing
    - partnership marketing
    - marketing automation
  tech-stack:
    - HubSpot CRM
    - LinkedIn Campaign Manager
    - Google Ads
    - Google Analytics
    - Meta Ads Manager
    - Search Console
    - Python 3.8+
  python-tools:
    - calculate_cac.py
---

# Marketing Demand & Acquisition

Expert acquisition playbook for Series A+ startups scaling internationally (EU/US/Canada) with hybrid PLG/Sales-Led motion.

## Overview

This skill provides comprehensive frameworks for building and scaling demand generation programs across paid media, SEO, and partnerships. Designed for B2B SaaS companies from Series A through growth stage, it includes proven channel strategies, campaign templates, and automated CAC analysis.

**Core Value:** Generate predictable pipeline at $500-$1,000 CAC while scaling from $1M to $10M+ ARR across international markets.

## Core Capabilities

- **Full-Funnel Demand Generation** - TOFU/MOFU/BOFU strategies with channel-specific tactics
- **Paid Media Optimization** - LinkedIn, Google Ads, Meta campaign frameworks with targeting and creative guidance
- **SEO Strategy** - Technical SEO, keyword research, link building, and content strategy
- **Partnership Programs** - Strategic partnerships, affiliate programs, co-marketing campaigns
- **CAC Analysis** - Automated customer acquisition cost calculation and optimization
- **HubSpot Integration** - Campaign tracking, lead scoring, attribution, workflow automation
- **International Expansion** - Market-specific tactics for EU, US, and Canada entry
- **Attribution & Reporting** - Multi-touch attribution setup and performance dashboards

## Role Coverage

This skill serves:
- **Demand Generation Manager** - Multi-channel campaigns, pipeline generation
- **Paid Media/Performance Marketer** - Paid search/social/display optimization
- **SEO Manager** - Organic acquisition and technical SEO
- **Affiliate/Partnerships Manager** - Co-marketing and channel partnerships

## Core KPIs by Role

**Demand Gen**: MQL/SQL volume, cost per opportunity, marketing-sourced pipeline $, pipeline velocity, MQL→SQL conversion rate

**Paid Media**: CAC, ROAS, CPL, CPA, incrementality lift, channel efficiency ratio

**SEO**: Organic sessions, non-brand traffic %, keyword rankings (P1-P3), organic-assisted conversions, technical health score

**Partnerships**: Partner-sourced pipeline $, partner CAC, net new logos via partners, co-marketing ROI

## Quick Start

### Calculate CAC
```bash
python scripts/calculate_cac.py data/campaign-results.csv
python scripts/calculate_cac.py data/q2-2025.csv --target-cac 500 --ltv 2500
```

### Access Frameworks
- Marketing frameworks: [frameworks.md](references/frameworks.md)
- Campaign templates: [templates.md](references/templates.md)
- Tool documentation: [tools.md](references/tools.md)

## Key Workflows

### 1. Launch Demand Generation Campaign

**Time:** 4-6 weeks end-to-end

1. **Planning (Week 1-2)** - Define objectives, budget, audience, channels
   - Use campaign brief template from [templates.md](references/templates.md)
   - Select channels based on ICP and funnel stage
   - Set success metrics (MQLs, SQLs, CAC target)

2. **Setup (Week 3-4)** - Build campaigns, landing pages, HubSpot tracking
   - Configure HubSpot campaigns and UTM parameters
   - Create ad campaigns (LinkedIn, Google, Meta)
   - Set up lead scoring and workflows

3. **Launch (Week 5)** - Go live and monitor performance
   - Start at 50% budget for testing
   - Monitor conversion rates hourly
   - Scale winning ads to 100% budget

4. **Optimize (Week 6+)** - Analyze, iterate, scale
   - Run A/B tests on ads and landing pages
   - Scale winning channels by 20% weekly
   - Pause underperforming campaigns

See [frameworks.md](references/frameworks.md) for full-funnel strategy and [templates.md](references/templates.md) for HubSpot setup.

### 2. Optimize Paid Media Performance

**Time:** 2-3 hours per week ongoing

1. **Analyze Performance** - Review CAC, conversion rates, spend by channel
   - Calculate CAC: `python scripts/calculate_cac.py data/weekly.csv`
   - Compare to benchmarks (LinkedIn $150-400, Google $80-250)

2. **Identify Opportunities** - Find underperforming campaigns and winning strategies
   - CAC >target → Optimize or pause
   - CAC <target → Scale budget 20% weekly

3. **Implement Changes** - Adjust bids, targeting, creative, budgets
   - Use channel playbooks from [frameworks.md](references/frameworks.md)
   - Test 3-5 creative variants per campaign

4. **Monitor Results** - Track improvements and iterate
   - Daily: Conversion rates, spend pacing
   - Weekly: CAC analysis and optimization review

See [frameworks.md](references/frameworks.md) for LinkedIn, Google, and Meta playbooks.

### 3. Build SEO Foundation

**Time:** 8-12 weeks initial setup, ongoing optimization

1. **Technical SEO (Week 1-2)** - Ensure site is crawlable and fast
   - Complete pre-launch checklist from [frameworks.md](references/frameworks.md)
   - Submit sitemap, enable HTTPS, optimize speed
   - Add structured data and canonical tags

2. **Keyword Research (Week 3-4)** - Identify target keywords by funnel stage
   - Tier 1 (BOFU): Best [category], [competitor] alternative
   - Tier 2 (MOFU): How to [solve problem]
   - Tier 3 (TOFU): What is [concept]

3. **Content Creation (Week 5-12)** - Publish optimized content
   - TOFU: 4 posts/month (educational)
   - MOFU: 2 posts/month (solution-focused)
   - BOFU: 1 post/month (product/conversion)

4. **Link Building (Ongoing)** - Acquire quality backlinks
   - Digital PR, guest posting, partnerships
   - Target: 5-10 links/month initially, 20-30 after 6 months

See [frameworks.md](references/frameworks.md) for SEO strategy framework and on-page templates.

### 4. Establish Partnership Program

**Time:** 6-12 months to full activation

1. **Identify Partners (Month 1-2)** - Research complementary companies
   - Similar ICP, no direct competition
   - Product fit (complementary, not substitute)
   - Similar scale and values

2. **Outreach & Negotiate (Month 2-4)** - Propose partnership
   - Use outreach template from [templates.md](references/templates.md)
   - Define partnership agreement (scope, revenue model, metrics)

3. **Activate & Enable (Month 4-6)** - Launch partnership
   - Create co-branded assets
   - Train partner sales team
   - Set up tracking in HubSpot

4. **Manage Ongoing (Month 6+)** - QBRs, co-marketing, optimization
   - Quarterly business reviews
   - 1-2 co-marketing activities per quarter
   - Monthly pipeline reporting

See [frameworks.md](references/frameworks.md) for partnership playbook and [templates.md](references/templates.md) for co-marketing campaigns.

## Python Tools

### calculate_cac.py

Calculate blended and channel-specific Customer Acquisition Cost with automated recommendations.

**Key Features:**
- Multi-channel CAC analysis (LinkedIn, Google, Meta, SEO, Partnerships)
- Efficiency scoring and channel comparison
- Budget allocation recommendations
- LTV:CAC ratio calculation
- JSON and text output formats

**Common Usage:**
```bash
# Basic CAC calculation
python scripts/calculate_cac.py data/results.csv

# With target CAC and LTV
python scripts/calculate_cac.py data/q2-2025.csv --target-cac 500 --ltv 2500

# JSON output for dashboards
python scripts/calculate_cac.py data/results.csv --output json --file report.json

# Compare time periods
python scripts/calculate_cac.py data/q2.csv --compare data/q1.csv
```

See [tools.md](references/tools.md) for comprehensive documentation, input formats, and integration examples.

## Reference Guides

### When to Use Each Reference

**[frameworks.md](references/frameworks.md)** - Marketing strategies and methodologies
- Full-funnel demand generation (TOFU/MOFU/BOFU)
- Paid media channel strategies (LinkedIn, Google, Meta)
- SEO framework (technical, content, link building)
- Partnership types and playbooks
- Experimentation framework (A/B testing, ICE scoring)
- International expansion considerations
- Attribution models and reporting
- Handoff protocols (MQL→SQL→Opportunity)

**[templates.md](references/templates.md)** - Ready-to-use campaign assets
- Campaign planning briefs
- HubSpot workflow templates
- Campaign launch checklists
- Email campaign sequences
- Ad copy templates (LinkedIn, Google, Meta)
- Landing page structures
- Webinar promotion timeline
- Performance report templates

**[tools.md](references/tools.md)** - Python tool documentation
- calculate_cac.py comprehensive guide
- All command-line options and flags
- Input/output formats
- Integration examples (CI/CD, dashboards, alerts)
- Troubleshooting and best practices
- Metrics explained (CAC, efficiency score, LTV:CAC)

## Best Practices

### Channel Strategy
- Start with 2-3 channels (LinkedIn + Google for B2B)
- Test at 50% budget, scale winners by 20% weekly
- Kill underperformers after 2 weeks if CAC >2x target
- Maintain 40% paid, 25% SEO, 20% partnerships, 15% other

### Campaign Management
- Review performance weekly (CAC, conversion rates)
- A/B test constantly (4-6 tests/month)
- Update tracking and attribution continuously
- Document learnings from every campaign

### HubSpot Integration
- Tag all campaigns with UTM parameters
- Set up lead scoring for each campaign type
- Use multi-touch attribution (W-shaped)
- Monitor MQL→SQL conversion rates

### International Expansion
- Start with US (largest TAM), then UK (English-speaking gateway)
- Localize pricing and content by market
- EU: Focus on GDPR compliance and LinkedIn ads
- Budget: 50% US, 20% UK, 15% DACH, 10% France, 5% Canada

See [frameworks.md](references/frameworks.md) for detailed channel benchmarks and [templates.md](references/templates.md) for execution checklists.

## Performance Benchmarks

**B2B SaaS Series A Targets:**
- Blended CAC: $500-$1,000
- MQL→SQL conversion: 10-20%
- Marketing-sourced pipeline: 40-60% of total
- ROMI (return on marketing investment): 3:1 minimum
- Budget allocation: 40% paid, 25% SEO, 20% partnerships, 15% other

**Channel-Specific (see [frameworks.md](references/frameworks.md) for full matrix):**
- LinkedIn: $150-$400 CAC, 0.5-2% CVR
- Google Search: $80-$250 CAC, 2-5% CVR
- SEO: $50-$150 CAC, 2-5% CVR
- Partnerships: $100-$300 CAC, 5-10% CVR

## Integration

This skill works best with:
- HubSpot CRM (campaign tracking, lead scoring, workflows)
- LinkedIn Campaign Manager (B2B paid social)
- Google Ads (search and display advertising)
- Google Analytics (traffic analysis, funnel optimization)
- Search Console (SEO performance monitoring)
- Partnership platforms (PartnerStack, Impact, Rewardful)

See [templates.md](references/templates.md) for HubSpot setup guides and [tools.md](references/tools.md) for tool integrations.

## Additional Resources

- **Frameworks:** [frameworks.md](references/frameworks.md)
- **Templates:** [templates.md](references/templates.md)
- **Tools:** [tools.md](references/tools.md)
- **Campaign Assets:** `assets/` directory (dashboards, briefs, checklists)

---

**Last Updated**: November 2025 | **Version**: 1.0
