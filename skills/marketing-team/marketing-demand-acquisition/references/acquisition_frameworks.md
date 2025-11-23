# Customer Acquisition Frameworks Reference Guide

## Overview

This comprehensive guide provides proven frameworks, methodologies, and best practices for customer acquisition across digital marketing channels. Designed for demand generation marketers, growth leads, and marketing directors working in B2B SaaS, enterprise software, and high-growth technology companies.

## Key Concepts

### Customer Acquisition Cost (CAC)

**Definition:** Total cost of acquiring a new customer, including all marketing and sales expenses.

**Formula:**
```
CAC = (Total Marketing Spend + Total Sales Spend) / Number of New Customers Acquired

Example:
- Marketing: $50,000/month
- Sales: $30,000/month
- New customers: 20
- CAC = ($50,000 + $30,000) / 20 = $4,000
```

**Benchmarks by Industry:**
- B2B SaaS (SMB): $200-$500
- B2B SaaS (Mid-Market): $500-$2,000
- B2B SaaS (Enterprise): $2,000-$10,000+
- E-commerce: $10-$50
- Consumer Apps: $1-$5

**CAC Payback Period:**
```
CAC Payback = CAC / (Monthly Revenue per Customer × Gross Margin %)

Target: <12 months for healthy SaaS business
```

### LTV:CAC Ratio

**Definition:** Customer Lifetime Value divided by Customer Acquisition Cost

**Formula:**
```
LTV = (Average Revenue per Customer × Gross Margin %) / Monthly Churn Rate
LTV:CAC Ratio = LTV / CAC

Example:
- ARPC: $500/month
- Gross Margin: 80%
- Monthly Churn: 2% (0.02)
- CAC: $2,000

LTV = ($500 × 0.80) / 0.02 = $20,000
LTV:CAC = $20,000 / $2,000 = 10:1
```

**Benchmarks:**
- 1:1 - Unsustainable (spending more than earning)
- 3:1 - Healthy and investable
- 5:1 - Strong unit economics
- 10:1+ - Underinvesting in growth (leave money on table)

### North Star Metric

**Definition:** Single metric that best captures core value delivered to customers

**Examples by Business Model:**
- Slack: Daily Active Teams
- Spotify: Time Spent Listening
- Airbnb: Nights Booked
- HubSpot: Weekly Active Customers
- Shopify: GMV (Gross Merchandise Value)

**Criteria for North Star Metric:**
1. Reflects customer value delivery
2. Measures product success
3. Actionable by team
4. Leading indicator of revenue

## Frameworks

### Framework 1: AARRR Pirate Metrics (Dave McClure)

**Purpose:** Full-funnel growth framework for startups and product-led companies

#### 1. Acquisition

**Definition:** Users discover and visit your product

**Channels:**
- Organic search (SEO)
- Paid search (Google Ads)
- Social media (organic and paid)
- Content marketing
- Referrals
- Partnerships

**Key Metrics:**
- Website visitors
- Traffic sources
- Cost per visit (CPV)
- Channel mix

**Optimization Tactics:**
- SEO: Target high-intent keywords, optimize conversion paths
- Paid: A/B test ad creative, landing pages, audience segments
- Content: Create TOFU awareness content, guest posting, PR
- Referrals: Implement referral program with incentives

#### 2. Activation

**Definition:** Users have great first experience (aha moment)

**Activation Events (Examples):**
- SaaS Tool: Complete onboarding, connect first integration
- E-commerce: Browse 5+ products, add to cart
- Social App: Follow 10 people, post first content
- Marketplace: Complete profile, make first transaction

**Key Metrics:**
- Activation rate (% of signups reaching aha moment)
- Time to activation
- Drop-off points in onboarding

**Optimization Tactics:**
- Reduce onboarding friction (minimize form fields)
- Progressive disclosure (don't overwhelm with features)
- Personalized onboarding (based on use case)
- In-app guidance (tooltips, checklists, videos)
- Trigger-based emails (nudge incomplete signups)

#### 3. Retention

**Definition:** Users return and continue using product

**Cohort Analysis:**
```
Retention Cohort Table:
           Week 0  Week 1  Week 2  Week 3  Week 4
Jan Users   100%     45%     32%     28%     25%
Feb Users   100%     50%     38%     35%     32%
Mar Users   100%     55%     42%     40%     38%
```

**Key Metrics:**
- Day 1, Day 7, Day 30 retention
- Monthly Active Users (MAU)
- Churn rate (monthly, annual)
- Engagement frequency

**Optimization Tactics:**
- Email re-engagement campaigns
- Push notifications (mobile)
- Feature adoption programs
- Customer success check-ins
- Build habits (streak features, daily rewards)

#### 4. Revenue

**Definition:** Users become paying customers

**Monetization Models:**
- Freemium (free plan  paid upgrade)
- Free trial (14-30 days  subscription)
- Reverse trial (start paid, refund if not satisfied)
- Usage-based (pay per API call, seat, etc.)
- Tiered pricing (Starter, Pro, Enterprise)

**Key Metrics:**
- Free-to-paid conversion rate
- Average Revenue Per User (ARPU)
- Customer Lifetime Value (LTV)
- MRR/ARR growth

**Optimization Tactics:**
- Pricing page A/B tests
- Feature gating (limit free plan features)
- Usage limits (trigger upgrade prompts)
- Sales-assisted conversions (demo calls for enterprise)
- Annual prepay discounts (10-20% off)

#### 5. Referral

**Definition:** Users refer others to your product

**Referral Loop Formula:**
```
Viral Coefficient (K) = % of customers who refer × # of referrals per customer

K > 1.0 = Viral growth (self-sustaining)
K = 0.5 = 50% of growth comes from referrals

Example:
- 20% of customers refer
- Average 3 referrals per customer
- K = 0.20 × 3 = 0.6 (60% of growth from referrals)
```

**Key Metrics:**
- Referral participation rate
- Referrals per customer
- Referred customer LTV
- Viral coefficient (K)

**Optimization Tactics:**
- Incentivized referrals (both referrer and referee get credit)
- Built-in sharing (invite teammates, share content)
- Network effects (product better with more users)
- Social proof (show user counts, testimonials)

**AARRR Prioritization:**
- Early stage (0-PMF): Focus on Activation and Retention
- Growth stage (PMF): Focus on Acquisition and Revenue
- Scale stage: Optimize all five, focus on Referral

### Framework 2: Jobs-to-be-Done (JTBD) for Acquisition

**Purpose:** Understand customer motivations to craft resonant marketing

**Core Concept:** People "hire" products to get jobs done in their lives

#### JTBD Interview Questions

**Situation Questions:**
- When did you first realize you needed a solution?
- What was the trigger that made you start looking?
- Describe the situation that led you to search

**Functional Job Questions:**
- What were you trying to accomplish?
- What was the job you needed done?
- What outcome were you hoping for?

**Emotional Job Questions:**
- How did the situation make you feel?
- What were your fears or anxieties?
- What would success feel like?

**Social Job Questions:**
- How do you want others to perceive you?
- What would your team/boss say if you chose wrong?
- What social pressure influenced your decision?

#### JTBD Forces Diagram

```
                Progress-Making Forces
                        
        Push (Pain)          Pull (Attraction)
         of current           of new solution
                        
    [Current State] ----- [Desired State]
                        
        Anxiety              Habit
         of new solution      of present
                        
                Change-Resisting Forces
```

**Application to Acquisition:**
1. **Push Messaging:** "Tired of spreadsheet chaos?"
2. **Pull Messaging:** "Streamlined workflows in 5 minutes"
3. **Reduce Anxiety:** Free trial, money-back guarantee, case studies
4. **Overcome Habit:** Migration support, training, onboarding

#### JTBD Ad Copy Framework

**Template:**
```
Headline: [Desired Outcome] without [Anxiety/Fear]
Subhead: [How it works in 3 steps]
CTA: [Start free trial]

Example:
Headline: "Launch products 2x faster without endless meetings"
Subhead: "Align teams, track progress, ship with confidence"
CTA: "Start 14-day free trial"
```

### Framework 3: ICE Score for Channel Prioritization

**Purpose:** Prioritize acquisition channels based on Impact, Confidence, Ease

**Formula:**
```
ICE Score = (Impact + Confidence + Ease) / 3

Rate each factor 1-10:
- Impact: How much will this move the needle?
- Confidence: How sure are you it will work?
- Ease: How easy is it to implement?
```

**Example Scoring:**

| Channel | Impact | Confidence | Ease | ICE | Priority |
|---------|--------|------------|------|-----|----------|
| SEO | 9 | 7 | 5 | 7.0 | High |
| LinkedIn Ads | 8 | 8 | 8 | 8.0 | High |
| Google Ads | 7 | 9 | 8 | 8.0 | High |
| Reddit Ads | 6 | 5 | 7 | 6.0 | Medium |
| Partnerships | 9 | 6 | 4 | 6.3 | Medium |
| Twitter Ads | 5 | 6 | 7 | 6.0 | Medium |
| Podcast Ads | 7 | 4 | 5 | 5.3 | Low |

**Decision Framework:**
- ICE 7.5+: Launch immediately
- ICE 6.0-7.5: Prioritize after quick wins
- ICE <6.0: Deprioritize or test minimally

### Framework 4: Bullseye Framework (Traction)

**Purpose:** Find the one acquisition channel that will dominate your growth

**Three Rings:**

#### Outer Ring: Brainstorm (All Possible Channels)
- Paid channels (Google, LinkedIn, Meta, etc.)
- Organic channels (SEO, content, social)
- Earned channels (PR, partnerships, referrals)
- Viral channels (word-of-mouth, product virality)

**19 Traction Channels:**
1. Viral marketing
2. Public relations (PR)
3. Unconventional PR (stunts, controversy)
4. Search Engine Marketing (SEM)
5. Social & display ads
6. Offline ads (billboards, print, TV)
7. Search Engine Optimization (SEO)
8. Content marketing
9. Email marketing
10. Engineering as marketing (free tools, calculators)
11. Targeting blogs (guest posts, sponsored)
12. Business development (partnerships, integrations)
13. Sales
14. Affiliate programs
15. Existing platforms (marketplaces, app stores)
16. Trade shows
17. Offline events (meetups, conferences)
18. Speaking engagements
19. Community building

#### Middle Ring: Test (Run Cheap Experiments)

**Test Budget:** $1,000-$5,000 per channel
**Test Duration:** 2-4 weeks
**Success Criteria:** Define before testing

**Example Tests:**
- LinkedIn Ads: $2,000 budget, test 3 audiences, measure CPL
- SEO: Write 10 blog posts, track rankings and traffic
- Partnerships: Reach out to 20 partners, close 2 deals

**Evaluation Criteria:**
1. **Cost:** CAC below target?
2. **Scale:** Can this channel reach 10,000+ customers?
3. **Time:** How long to see results?
4. **Defensibility:** Can competitors copy easily?

#### Inner Ring: Focus (Double Down)

**Decision:** Pick the ONE channel that will be your core growth driver

**Focus Strategy:**
- Allocate 70% of budget to inner ring channel
- Allocate 20% to middle ring (second-best channels)
- Allocate 10% to outer ring (experimentation)

**Example: SaaS Company Focus**
- Inner Ring: SEO (70% - content production, link building)
- Middle Ring: LinkedIn Ads (20% - retargeting, ABM)
- Outer Ring: Podcasts (10% - test sponsorships)

**Re-evaluation:** Every quarter, reassess if inner ring channel is saturating

## Best Practices

### 1. Channel-Specific Best Practices

#### Paid Search (Google Ads)

**Campaign Structure:**
```
Account  Campaign  Ad Group  Keywords & Ads

Best Practice Structure:
- Separate campaigns by funnel stage (TOFU, MOFU, BOFU)
- Single keyword theme per ad group (5-10 keywords max)
- 3 responsive search ads per ad group
- Use exact match for brand terms, phrase match for others
```

**Bidding Strategy Evolution:**
- Week 1-2: Manual CPC (learn and control costs)
- Week 3-4: Enhanced CPC (let Google optimize bids)
- After 50 conversions: Target CPA (automated bidding)
- After 100 conversions: Maximize conversions with tCPA

**Quality Score Optimization:**
- Expected CTR: Write compelling ad copy with keywords
- Ad Relevance: Match ad copy to keyword theme
- Landing Page Experience: Fast load, mobile-friendly, clear CTA

#### Paid Social (LinkedIn Ads)

**Audience Targeting Strategy:**
```
Tier 1: High-Intent Retargeting
- Website visitors (30 days)
- Video viewers (50%+)
- Lead gen form openers

Tier 2: Account-Based Marketing (ABM)
- Upload target account list (500-1000 companies)
- Target by company name + job title

Tier 3: Cold Prospecting
- Job titles (Director+, VP, C-level)
- Industries (Software, SaaS, Tech)
- Company size (50-5000 employees)
```

**Creative Best Practices:**
- Use native ad formats (single image, carousel, video)
- Hook in first 3 seconds (problem or result)
- Social proof (customer logos, testimonials)
- Clear CTA (Start free trial, Book demo)

**Budget Allocation:**
- 40% to retargeting (highest ROI)
- 40% to ABM (mid-funnel)
- 20% to cold prospecting (top-of-funnel)

#### SEO (Organic Search)

**Content Strategy:**
```
Keyword Research  Content Creation  On-Page SEO  Link Building  Monitoring

Priority Tiers:
1. High-intent commercial keywords (low difficulty, high conversion)
2. Solution-aware keywords (moderate difficulty, moderate volume)
3. Problem-aware keywords (high difficulty, high volume)
```

**On-Page SEO Checklist:**
- [ ] Target keyword in title tag (front-loaded)
- [ ] Target keyword in H1 (exactly or variant)
- [ ] Target keyword in first 100 words
- [ ] Keyword density 1-2% (natural)
- [ ] Internal links to related content (3-5 links)
- [ ] External links to authoritative sources (2-3 links)
- [ ] Alt text on images with keywords
- [ ] Meta description with keyword (155 chars)
- [ ] URL slug with keyword (short and clean)

**Link Building Tactics (Priority Order):**
1. Digital PR (publish original research, pitch journalists)
2. Guest posting (DA 40+ sites, dofollow links)
3. Broken link building (find broken links, offer your content)
4. Resource page link building (find "[topic] resources" pages)
5. HARO (Help A Reporter Out) - respond to journalist queries

### 2. Conversion Rate Optimization (CRO)

**Landing Page CRO Checklist:**
- [ ] Headline matches ad/email copy (message match)
- [ ] Clear value proposition above fold
- [ ] Single focused CTA (remove navigation)
- [ ] Social proof (logos, testimonials, numbers)
- [ ] Short form (2-3 fields max for top-of-funnel)
- [ ] Mobile optimized (50%+ traffic is mobile)
- [ ] Fast load time (<3 seconds)
- [ ] Trust signals (security badges, privacy policy)

**A/B Testing Prioritization (ICE Score):**
- High Impact, High Confidence, High Ease: Test first
- Example: CTA button color (Easy), headline rewrite (High Impact)

**Statistical Significance:**
- Minimum sample size: 1,000 visitors per variant
- Confidence level: 95% minimum
- Don't stop tests early (week-over-week consistency)

### 3. Attribution Modeling

**Attribution Models:**

**First-Touch Attribution:**
- Credit: 100% to first interaction
- Use case: Measure brand awareness campaigns
- Pro: Shows what drives discovery
- Con: Ignores nurturing influence

**Last-Touch Attribution:**
- Credit: 100% to last interaction before conversion
- Use case: Direct response, BOFU campaigns
- Pro: Shows what closes deals
- Con: Ignores earlier touchpoints

**Multi-Touch Attribution (W-Shaped):**
- Credit: 40% first touch, 20% middle touches, 40% last touch
- Use case: Hybrid PLG/Sales-Led (recommended for B2B SaaS)
- Pro: Full-funnel view
- Con: More complex implementation

**Recommended Setup:**
- Default: Multi-touch for holistic view
- Compare: Run first-touch and last-touch reports side-by-side
- Action: Allocate budget based on multi-touch insights

## Examples

### Example 1: B2B SaaS Customer Acquisition Strategy

**Scenario:** Series A SaaS company, $50k MRR, target SMB/Mid-Market, $40k/month acquisition budget

**Target Metrics:**
- CAC: $500 (LTV $5,000 = 10:1 LTV:CAC)
- MQLSQL: 20%
- SQLCustomer: 25%
- Goal: 20 new customers/month

**Approach:**

**Month 1-2: Foundation**
1. Build acquisition infrastructure
   - Google Analytics 4 + HubSpot setup
   - Landing pages for each channel
   - Lead scoring model (MQL definition)

2. Launch quick-win channels
   - Google Search (brand + competitor keywords): $8k/month
   - LinkedIn Ads (retargeting + ABM): $10k/month
   - SEO foundation (technical audit, 10 blog posts): $5k investment

**Month 3-4: Test & Learn**
3. Run channel experiments
   - Test 1: LinkedIn Lead Gen Forms vs Landing Pages
   - Test 2: Google RSAs with 3 messaging angles
   - Test 3: Reddit ads to r/[industry] communities ($2k test)

4. Measure and optimize
   - Calculate CAC by channel
   - Analyze MQLSQL conversion by source
   - Double down on winners, pause losers

**Month 5-6: Scale**
5. Allocate budget to winning channels
   - Google Search: $15k (proven CAC $400)
   - LinkedIn Ads: $18k (proven CAC $550)
   - SEO: $5k ongoing (long-term investment)
   - Partnerships: $2k (test affiliate program)

**Outcome:**
- Achieved 22 new customers/month (110% of goal)
- Blended CAC: $480 (under $500 target)
- Channel mix: 45% Google, 40% LinkedIn, 10% SEO, 5% Partners

### Example 2: E-commerce Growth Strategy

**Scenario:** D2C fashion brand, $200k/month revenue, 30% gross margin, focus on profitability

**Target Metrics:**
- CAC: $25 (AOV $80, 3 purchases/year, LTV $240 at 30% margin = 72/25 = 2.9:1 LTV:CAC)
- ROAS: 3:1 minimum on paid ads
- Goal: $500k/month revenue in 6 months

**Approach:**

**Phase 1: Paid Social (Meta) Optimization**
1. Audience strategy
   - Lookalike: 1% of past purchasers ($10k/month)
   - Interest: Fashion, competitor brands ($8k/month)
   - Retargeting: Website 30-day, abandoned cart ($5k/month)

2. Creative testing
   - User-generated content (UGC) videos
   - Product demos (before/after, styling tips)
   - Influencer testimonials
   - Static ads with social proof

**Phase 2: Retention & LTV Expansion**
3. Email marketing (increase repeat purchase rate)
   - Welcome series (5 emails over 30 days)
   - Browse abandonment (3 emails)
   - Post-purchase upsell (60 days after first order)
   - Win-back campaign (120 days inactive)

4. Loyalty program
   - Points for purchases (1 point = $1)
   - Bonus for referrals (+500 points)
   - VIP tier (spend $500+, get 20% off)

**Phase 3: Organic Growth (SEO + Influencer)**
5. Content marketing
   - "[Style] outfit ideas" (100+ search volume keywords)
   - Fashion guides (seasonal trends, how-to style)
   - Comparison content ("[brand] vs [competitor]")

6. Influencer partnerships
   - Micro-influencers (10k-50k followers, higher engagement)
   - Affiliate commission (15% per sale)
   - Free product in exchange for content

**Outcome:**
- Revenue growth: $200k  $480k (140% increase in 6 months)
- CAC decreased: $25  $18 (scale efficiency)
- Repeat purchase rate: 15%  28% (email + loyalty program)
- Channel mix: 60% Meta, 20% Email, 10% SEO, 10% Influencer

### Example 3: Product-Led Growth (PLG) Strategy

**Scenario:** Freemium SaaS productivity tool, 10k free users, 2% free-to-paid, $50 MRR/customer

**Target Metrics:**
- Activation rate: 40% of signups complete onboarding
- Free-to-paid: 5% conversion (2.5x from 2%)
- Goal: 500 paid customers in 12 months

**Approach:**

**Phase 1: Improve Activation**
1. Onboarding optimization
   - Reduce signup fields (email + password only)
   - Interactive product tour (5 steps to first value)
   - Trigger-based emails (nudge inactive users)

2. Aha moment faster
   - Checklist: Connect integration  Import data  Create first project
   - Progress bar (gamification: 80% complete!)
   - In-app tooltips for key features

**Phase 2: Increase Free-to-Paid Conversion**
3. Feature gating
   - Free plan: 3 projects, 5 team members
   - Paid plan: Unlimited projects, unlimited team members
   - Trigger upgrade prompts when hitting limits

4. Time-based nudges
   - Day 7: "You've created 2 projects! Upgrade for unlimited."
   - Day 14: "Your team is growing! Add more members with Pro."
   - Day 21: "Unlock advanced reports to track progress."

5. Sales-assisted conversions
   - Offer demo calls for high-value leads (10+ team members)
   - Personalized emails from founders to power users
   - Case studies for specific industries

**Phase 3: Referral Loop (Viral Growth)**
6. Built-in sharing
   - Invite teammates (product works better with team)
   - Share projects (collaborate with external stakeholders)
   - Public templates (share best practices, get credit)

7. Incentivized referrals
   - Referrer: 1 month free for each referred paid customer
   - Referee: 20% off first 3 months
   - Track referrals via unique links

**Outcome:**
- Activation rate: 25%  42% (onboarding improvements)
- Free-to-paid: 2%  5.8% (feature gating + nudges)
- Viral coefficient: 0.0  0.4 (referral program)
- Paid customers: 200  580 (190% growth in 12 months)

## Resources

### Books
- **"Traction" by Gabriel Weinberg & Justin Mares** - Bullseye framework for channel prioritization
- **"Hacking Growth" by Sean Ellis & Morgan Brown** - Growth hacking methodologies
- **"Obviously Awesome" by April Dunford** - Positioning for customer acquisition
- **"The Mom Test" by Rob Fitzpatrick** - Customer interviews for JTBD insights

### Tools
- **Google Analytics 4** - Website traffic and conversion tracking
- **HubSpot / Marketo** - Marketing automation and attribution
- **Ahrefs / SEMrush** - SEO keyword research and competitor analysis
- **Hotjar / FullStory** - User behavior analytics (heatmaps, session recordings)
- **Optimizely / Google Optimize** - A/B testing and experimentation
- **Amplitude / Mixpanel** - Product analytics for PLG

### Benchmarks & Data
- **OpenView SaaS Benchmarks** - CAC, LTV, retention benchmarks
- **Bessemer Cloud Index** - SaaS metrics and public company comparables
- **First Round Review** - Growth case studies and tactics
- **Reforge** - Growth courses and frameworks

### Communities
- **GrowthHackers** - Community forum for growth marketers
- **Demand Gen Chat (Slack)** - B2B demand generation professionals
- **SaaS Growth Hacks (Facebook)** - SaaS growth tactics and discussions
- **r/marketing (Reddit)** - Marketing strategies and advice

---

**Last Updated:** November 23, 2025
**Related Files:**
- [channel_best_practices.md](channel_best_practices.md) - Deep dive into channel-specific tactics
- [conversion_optimization.md](conversion_optimization.md) - CRO methodologies and experiments
- [frameworks.md](frameworks.md) - Additional demand generation frameworks
