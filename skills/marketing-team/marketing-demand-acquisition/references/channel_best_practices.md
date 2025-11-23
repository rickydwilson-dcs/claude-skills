# Channel-Specific Best Practices Reference Guide

## Overview

This guide provides deep tactical knowledge for executing successful campaigns across major digital marketing channels. Each section includes platform-specific strategies, creative guidelines, audience targeting approaches, and optimization techniques based on current industry best practices (2025).

## Key Concepts

### Channel Selection Matrix

**Factors for Channel Selection:**
1. **Audience Match** - Where does your ICP spend time?
2. **Intent Level** - High intent (search) vs awareness (social)
3. **Budget Efficiency** - Cost per acquisition benchmarks
4. **Scalability** - Can you reach 10k+ customers via this channel?
5. **Competitive Saturation** - How crowded is the space?

### Channel Lifecycle Stages

**Stage 1: Testing (Month 1-2)**
- Budget: $1k-5k
- Goal: Prove unit economics (CAC < target)
- Success: 2x ROAS minimum, clear conversion path

**Stage 2: Scaling (Month 3-6)**
- Budget: Increase 20% weekly if profitable
- Goal: Reach 50% of target monthly volume
- Success: Maintain CAC while increasing spend

**Stage 3: Optimization (Month 6+)**
- Budget: 70% of total acquisition budget
- Goal: Incremental improvements, prevent saturation
- Success: <10% CAC increase as you scale

## Google Ads Best Practices

### Campaign Architecture

#### Campaign Types Priority

**1. Search - Brand Protection (Highest Priority)**
```
Campaign: Brand Terms
├─ Ad Group: Exact Brand Match
│  ├─ Keywords: [YourBrand], [YourBrand software]
│  ├─ Bid Strategy: Manual CPC (bid high, protect brand)
│  └─ Budget: $500-1000/month (5-10% of total)
│
└─ Ad Group: Misspellings
   ├─ Keywords: Common misspellings
   └─ Bid Strategy: Manual CPC
```

**Why:** Competitors bid on your brand. If you don't show up, you lose 20-30% of branded searches.

**2. Search - Competitor Conquest**
```
Campaign: Competitor Terms
├─ Ad Group: [Competitor 1] Alternative
│  ├─ Keywords: "[Competitor] alternative", "[Competitor] vs"
│  ├─ Headline: "Better than [Competitor]"
│  └─ Landing Page: Comparison page
│
├─ Ad Group: [Competitor 2] Alternative
│  └─ Similar structure
```

**Why:** Users searching competitors are in buying mode. Win them over with comparison content.

**3. Search - Solution/Problem Keywords**
```
Campaign: Solution Keywords
├─ Ad Group: [project management software]
│  ├─ Keywords: 5-10 tightly themed keywords
│  ├─ Match Types: Phrase + exact (avoid broad)
│  └─ Landing Page: Product overview
│
├─ Ad Group: [team collaboration tools]
   └─ Similar structure
```

**Why:** These users know what they need, ready to evaluate solutions.

### Responsive Search Ads (RSA) Strategy

**Headline Formula (15 headlines required):**
```
Position 1-3: Primary value props
- "Save 10 Hours Per Week"
- "Trusted by 500+ Teams"
- "#1 Rated on G2"

Position 4-6: Features
- "AI-Powered Automation"
- "Real-Time Collaboration"
- "Enterprise-Grade Security"

Position 7-9: Social proof
- "Used by Microsoft & Tesla"
- "4.8★ Rating on G2"
- "50,000+ Active Users"

Position 10-12: CTAs
- "Start Free 14-Day Trial"
- "Book Demo - See in 15 Min"
- "Get Started Today - No CC"

Position 13-15: Dynamic
- {KeyWord:Project Management}
- Pin for specific ad groups
```

**Description Formula (4 descriptions required):**
```
D1 (90 chars): Primary benefit + CTA
"Streamline projects, automate workflows, ship faster. Start free trial today."

D2 (90 chars): Feature list + differentiator
"Task management, time tracking, reporting, integrations. Built for modern teams."

D3 (90 chars): Social proof + urgency
"Join 500+ companies achieving 2x productivity. Limited spots for onboarding support."

D4 (90 chars): Generic backup
"The complete project management platform. Try free for 14 days, no credit card required."
```

### Bidding Strategy Evolution

**Phase 1: Manual CPC (Week 1-2)**
- Start: $1-3 per click
- Goal: Learn which keywords convert
- Adjust: Daily based on conversion data

**Phase 2: Enhanced CPC (Week 3-4)**
- Enable: eCPC lets Google adjust bids ±30%
- Goal: Improve conversions while learning
- Monitor: Ensure CPC doesn't spike >50%

**Phase 3: Target CPA (After 50 conversions)**
- Set target: Your acceptable CAC
- Goal: Automate bidding for scale
- Budget: Increase 20% weekly if hitting target

**Phase 4: Maximize Conversions (After 100 conversions)**
- Use: When you want volume over CAC
- Goal: Spend full daily budget efficiently
- Monitor: Watch for CAC creep

### Quality Score Optimization

**Quality Score Formula:**
```
Quality Score (1-10) = Expected CTR + Ad Relevance + Landing Page Experience
```

**Expected CTR (Weight: 40%)**
- **Action:** Write compelling headlines with keywords
- **Example:** "Best [Keyword] Software" → CTR 3-5%
- **Avoid:** Generic headlines → CTR <1%

**Ad Relevance (Weight: 30%)**
- **Action:** Match ad copy exactly to keyword theme
- **Example:** Keyword "project tracking" → Headline "Track Projects in Real-Time"
- **Avoid:** Unrelated messaging in ad copy

**Landing Page Experience (Weight: 30%)**
- **Action:** Fast load (<3s), mobile-friendly, clear CTA
- **Checklist:**
  - [ ] Keyword in H1 tag
  - [ ] Mobile-optimized (50%+ traffic)
  - [ ] Page load <3 seconds (Google PageSpeed 90+)
  - [ ] Clear CTA above fold
  - [ ] Content matches ad promise

**Quality Score Impact:**
```
QS 10: Pay 50% less per click
QS 7: Pay average CPC
QS 4: Pay 50% more per click
```

### Negative Keywords Strategy

**Build List of 100+ Negative Keywords:**

**Category 1: Irrelevant Intent**
- free, cheap, crack, torrent
- jobs, careers, hiring
- reviews, complaints
- DIY, homemade

**Category 2: Wrong Audience**
- for kids, for students
- personal, individual
- small business (if you target enterprise)

**Category 3: Wrong Product**
- competitor names (unless conquest campaign)
- adjacent products you don't offer

**Maintenance:**
- Weekly: Review search terms report
- Add: Any irrelevant queries with >10 impressions
- Goal: Waste <5% of budget on non-converting searches

## LinkedIn Ads Best Practices

### Audience Targeting Strategy

#### Tier 1: High-Intent Retargeting (Highest ROI)

```
Audience: Website Visitors - High Intent Pages
Settings:
- Pages: /pricing, /demo, /book-call
- Timeframe: 30 days
- Budget: 40% of LinkedIn budget

Creative:
- Headline: "Ready to get started?"
- CTA: "Start free trial" (direct response)
- Format: Single image or video
```

**Expected Performance:**
- CTR: 1-2%
- CPL: $30-50
- MQL→SQL: 30-40%

#### Tier 2: Account-Based Marketing (ABM)

```
Audience: Target Account List + Job Title
Upload List:
- 500-1000 target companies (matched via LinkedIn)
- Filter: Job titles (Director+, VP, C-level)
- Company size: 50-5000 employees

Creative:
- Headline: "Built for [Industry] Leaders"
- Social proof: "Trusted by [Similar Company]"
- CTA: "See customer stories"
```

**Expected Performance:**
- CTR: 0.5-1%
- CPL: $80-150
- MQL→SQL: 20-30%

#### Tier 3: Cold Prospecting

```
Audience: Job Title + Industry + Company Size
Settings:
- Job Titles: Marketing Director, VP Marketing, CMO
- Industries: Software, SaaS, Technology
- Company Size: 50-1000 employees
- Geography: US, CA, UK (test separately)

Creative:
- Headline: "For Marketing Leaders Scaling Fast"
- Hook: Problem statement in first 3 seconds
- CTA: "Download free guide" (TOFU offer)
```

**Expected Performance:**
- CTR: 0.3-0.7%
- CPL: $150-300
- MQL→SQL: 10-20%

### Creative Best Practices

#### Single Image Ads

**Image Requirements:**
- Size: 1200x627 pixels (1.91:1 ratio)
- File: <5 MB, PNG or JPG
- Text: <20% of image (LinkedIn doesn't restrict like Meta used to, but less is more)

**Design Principles:**
- **Hook:** Problem or result in visual
- **Social proof:** Customer logos, testimonial quote
- **Contrast:** Brand colors that pop against LinkedIn blue/white
- **Mobile-first:** 60% view ads on mobile

#### Carousel Ads

**Use Cases:**
- Feature showcase (5 features across 5 cards)
- Customer stories (problem → solution → result)
- Step-by-step guide

**Structure:**
```
Card 1: Hook (problem statement)
Card 2-4: Solution (features or benefits)
Card 5: CTA (try now, book demo)
```

**Performance:**
- Higher engagement than single image (2x swipe-through rate)
- Lower CTR to website (people engage with carousel, don't click through)

#### Video Ads

**Best for:**
- Product demos (show UI in action)
- Customer testimonials (real people, real results)
- Thought leadership (founder/exec sharing insights)

**Specs:**
- Length: 15-60 seconds (hook in first 3 seconds)
- Format: 1:1 square or 9:16 vertical (mobile-optimized)
- Captions: Always include (85% watch muted)
- Hook: Problem or result in first frame

**Performance:**
- 2-3x higher engagement than static
- 30-50% higher CPM (more expensive)
- Best for mid-funnel (awareness → consideration)

### Lead Gen Forms vs Landing Pages

**Lead Gen Forms (LinkedIn Native)**

**Pros:**
- 2-3x higher conversion rate (pre-filled form)
- Mobile-optimized (60% of traffic)
- Native experience (no page load)

**Cons:**
- Lower lead quality (easy to submit)
- Less context (no landing page copy)
- Limited customization

**When to Use:**
- TOFU: Content downloads, webinar registration
- MOFU: Newsletter signup, free tool access

**Landing Page (Off-Platform)**

**Pros:**
- Higher lead quality (more friction = more intent)
- Full control over messaging
- Better for complex offers

**Cons:**
- Lower conversion rate (20-50% drop-off)
- Slower page load (mobile issues)
- Requires more optimization

**When to Use:**
- BOFU: Demo requests, free trial signups
- Enterprise: High ACV offers requiring more context

### Budget Allocation

**Recommended Split (Series A, $15k-20k/month):**
```
Retargeting:        $6k-8k (40%) - Highest ROI
ABM:                $6k-8k (40%) - Mid-funnel pipeline
Cold Prospecting:   $3k-4k (20%) - TOFU awareness

Daily Budget per Campaign:
- Retargeting: $200-250/day
- ABM: $200-250/day
- Cold: $100-150/day
```

**Scaling Rules:**
- If CAC < target: Increase 20% weekly
- If CAC > target: Pause, optimize creative/audience
- If CTR < 0.3%: Creative fatigue, refresh ads

## Meta Ads (Facebook/Instagram) Best Practices

### When to Use Meta vs LinkedIn

**Use Meta if:**
- ✅ Target SMB/prosumer (not enterprise)
- ✅ Product ACV <$10k
- ✅ Visual product (UI, consumer-facing)
- ✅ Broader audience (millions of potential customers)
- ✅ Lower CAC requirements (<$200)

**Use LinkedIn if:**
- ✅ Target enterprise/mid-market
- ✅ Product ACV >$10k
- ✅ B2B with specific job titles
- ✅ Complex sales cycle

### Campaign Structure (Conversions Objective)

```
Campaign: [Q4-2025-Acquisition]
├─ Ad Set 1: Lookalike 1% (Past Purchasers)
│  ├─ Budget: $150/day
│  ├─ Placement: Feed + Stories (auto)
│  └─ Creative: 3 video ads, 2 carousel ads
│
├─ Ad Set 2: Interest Targeting (Business Software)
│  ├─ Budget: $100/day
│  ├─ Placement: Feed only
│  └─ Creative: 3 single image ads
│
└─ Ad Set 3: Retargeting (Website 30d)
   ├─ Budget: $100/day
   ├─ Placement: All placements
   └─ Creative: 2 video testimonials
```

### Audience Strategies

#### Lookalike Audiences

**Seed Audience Options (ranked by quality):**
1. Past purchasers (best quality)
2. High-value leads (SQL, demo requests)
3. Trial signups (if freemium)
4. Email subscribers (lowest quality)

**Lookalike %:**
- 1%: Highest quality, smallest reach (recommended start)
- 2-5%: Medium quality, scale option
- 6-10%: Lowest quality, large reach (avoid)

#### Interest Targeting

**Layering Strategy:**
```
Base Interest: Business Tools
AND
Behaviors: Small business owners
AND
Job Title: Manager, Director, VP
```

**Avoid:**
- Too narrow: <100k audience (won't scale)
- Too broad: >5M audience (inefficient spend)

#### Retargeting

**Segmentation:**
```
Hot: Visited /pricing, /demo (last 7 days)
- Budget: 40% of retargeting
- Creative: Direct CTA ("Start trial")

Warm: Visited blog, features (last 30 days)
- Budget: 40% of retargeting
- Creative: Educational ("See how it works")

Cold: Any page visit (last 60 days)
- Budget: 20% of retargeting
- Creative: Awareness ("What is [Product]?")
```

### Creative Best Practices

#### Video Ads (Best Performance)

**Format:**
- 1:1 square (feed) or 9:16 vertical (stories/reels)
- 15-30 seconds total
- Hook in first 3 seconds

**Hook Examples:**
- Problem statement: "Tired of messy spreadsheets?"
- Result preview: "See how we grew 300% in 6 months"
- Shocking stat: "95% of teams waste 10 hours/week on manual work"

**Structure:**
```
0-3s: Hook (problem or result)
3-10s: Solution (show product UI)
10-25s: Proof (testimonial, stats, demo)
25-30s: CTA (try now, learn more)
```

**Caption Strategy:**
- Always include captions (85% watch muted)
- Use bold text for emphasis
- Include CTA in captions too

#### UGC (User-Generated Content)

**Why it works:**
- Feels native to platform (not "salesy")
- Higher trust (real people, not brands)
- 2-3x better CTR than branded content

**How to source:**
- Pay customers $100-500 for testimonial video
- Use platforms: Billo, Minisocial, Afluencer
- Script: Keep it authentic, not scripted

**Format:**
```
Scene 1: "I used to struggle with [problem]"
Scene 2: "Then I found [Product]"
Scene 3: "Now I [result] in [timeframe]"
Scene 4: "You should try it too!"
```

### Performance Benchmarks (B2B SaaS)

| Metric | Target | Good | Excellent |
|--------|--------|------|-----------|
| CTR | 1% | 2% | 3%+ |
| CPM | $15 | $10 | $8 |
| CPL | $30 | $20 | $15 |
| CVR | 3% | 5% | 8%+ |
| CAC | $200 | $150 | $100 |

## SEO Best Practices

### Technical SEO Foundation

**Critical Setup (Do First):**

1. **XML Sitemap**
   - Generate: Use Yoast (WordPress) or Screaming Frog
   - Submit: Google Search Console, Bing Webmaster Tools
   - Update: Auto-regenerate on new content

2. **Robots.txt**
   ```
   User-agent: *
   Allow: /
   Disallow: /admin/
   Disallow: /cart/
   Sitemap: https://yoursite.com/sitemap.xml
   ```

3. **HTTPS / SSL**
   - Required: Google ranking factor since 2014
   - Get free: Let's Encrypt or Cloudflare

4. **Page Speed**
   - Target: 90+ on mobile (Google PageSpeed Insights)
   - Optimize:
     - Compress images (WebP format)
     - Enable caching
     - Minify CSS/JS
     - Use CDN

5. **Core Web Vitals**
   - **LCP (Largest Contentful Paint):** <2.5s
   - **FID (First Input Delay):** <100ms
   - **CLS (Cumulative Layout Shift):** <0.1

### Keyword Research Process

**Step 1: Seed Keywords**
- Your product category: "project management software"
- Competitors: "Asana alternative", "Monday.com vs"
- Use cases: "remote team collaboration"

**Step 2: Expand with Tools**
- **Ahrefs Keywords Explorer:** Enter seed, get 1000s of variations
- **Google Keyword Planner:** Free, good for volume estimates
- **AnswerThePublic:** Question-based keywords ("how to...", "what is...")

**Step 3: Analyze Metrics**
```
Keyword: "project management software"
- Volume: 10,000/month (search demand)
- Difficulty: 65/100 (how hard to rank)
- CPC: $15 (commercial value indicator)
- SERP: Mixed (articles + product pages)
```

**Step 4: Prioritize (ICE Score)**
```
ICE = (Search Volume × Commercial Intent × Low Difficulty) / 3

High Priority:
- Volume: 1000-5000/month
- Difficulty: <30
- Intent: High (commercial, transactional)
```

### Content Strategy by Intent

#### High-Intent Commercial Keywords (Priority 1)

**Examples:**
- "best [category] software"
- "[category] for [use case]"
- "[competitor] alternative"

**Content Type:** Comparison pages, product roundups

**Structure:**
```
Title: Best Project Management Software in 2025 (Top 10 Compared)

H1: Best Project Management Software
H2: What is Project Management Software?
H2: Top 10 PM Tools Compared
  H3: 1. [Your Product] - Best Overall
  H3: 2. [Competitor 1]
  ...
H2: How to Choose
H2: FAQ

Word Count: 2500-3500 words
```

#### Solution-Aware Keywords (Priority 2)

**Examples:**
- "how to [solve problem]"
- "[problem] solution"
- "[use case] best practices"

**Content Type:** How-to guides, tutorials

**Structure:**
```
Title: How to Manage Remote Teams (15 Best Practices)

H1: How to Manage Remote Teams Effectively
H2: Why Remote Team Management is Challenging
H2: 15 Best Practices for Remote Team Management
  H3: 1. Set clear expectations
  H3: 2. Use the right tools
  ...
H2: Tools for Remote Team Management (CTA to product)
H2: Conclusion

Word Count: 1500-2500 words
```

#### Problem-Aware Keywords (Priority 3)

**Examples:**
- "what is [concept]"
- "[problem] examples"
- "[industry] challenges"

**Content Type:** Educational articles, glossary

**Structure:**
```
Title: What is Agile Project Management? (Complete Guide)

H1: What is Agile Project Management?
H2: Definition
H2: Key Principles
H2: Agile vs Waterfall
H2: How to Implement Agile
H2: Agile Tools (soft CTA to product)

Word Count: 1000-2000 words
```

### Link Building Tactics (Ranked by ROI)

#### 1. Digital PR (Highest ROI, Hardest Execution)

**Strategy:** Publish original research, pitch to journalists

**Process:**
1. Run survey (500+ respondents in your industry)
2. Analyze data, find interesting insights
3. Create report with charts/visuals
4. Write press release
5. Pitch to journalists (HARO, Terkel, direct outreach)

**Expected Results:**
- 10-30 high-quality backlinks (DA 60+)
- Brand mentions in top publications
- 6-12 weeks effort

#### 2. Guest Posting (Medium ROI, Medium Difficulty)

**Strategy:** Write valuable content for relevant sites

**Qualifying Sites:**
- Domain Authority (DA) 40+
- Relevant niche (B2B SaaS, productivity, etc.)
- Allows dofollow links
- Publishes regularly (not abandoned)

**Outreach Template:**
```
Subject: Guest post idea for [Their Site]

Hi [Name],

I'm [Your Name] at [Company]. I've been reading [Their Site] for a while and loved your recent post on [Topic].

I'd love to contribute a guest post on [Specific Topic] for your audience. Here's a quick outline:

- [Point 1]
- [Point 2]
- [Point 3]

I'll include actionable tips and examples (no promotional content beyond author bio).

Let me know if you're interested!

Best,
[Your Name]
```

#### 3. Broken Link Building (High ROI, Medium Effort)

**Strategy:** Find broken links on relevant sites, offer your content as replacement

**Process:**
1. Find resource pages in your niche
   - Google: "[topic] resources", "[topic] links"
2. Use Ahrefs: Check for broken outbound links
3. Recreate missing content on your site
4. Email site owner with replacement suggestion

**Outreach Template:**
```
Subject: Broken link on [Page Title]

Hi [Name],

I was reading your resource page on [Topic] and noticed a broken link in the [Section] section.

The link to [Old URL] returns a 404 error.

I actually wrote a similar guide on [Topic]: [Your URL]

Feel free to use it as a replacement if it fits!

Best,
[Your Name]
```

## Email Marketing Best Practices

### Segmentation Strategy

**Behavioral Segments:**
```
1. Product Users
   - Active users (logged in last 7 days)
   - Inactive users (no login 30+ days)
   - Power users (daily usage)

2. Free Trial Users
   - New trials (day 1-3)
   - Mid-trial (day 4-10)
   - Ending trials (day 11-14)
   - Expired trials

3. Website Visitors
   - Pricing page visitors
   - Blog readers
   - Resource downloaders
   - Demo request (no show)
```

**Demographic Segments:**
- Company size (SMB, mid-market, enterprise)
- Industry (tech, healthcare, finance, etc.)
- Role (individual contributor, manager, executive)
- Geography (US, EU, APAC)

### Campaign Types & Triggers

#### Welcome Series (5 emails, 30 days)

```
Email 1: Day 0 (Welcome + first action)
Subject: Welcome to [Product]! Here's how to get started
CTA: Complete setup, watch demo video

Email 2: Day 2 (Feature highlight)
Subject: How [Customer] achieved [Result] with [Feature]
CTA: Try feature, read case study

Email 3: Day 5 (Education + resource)
Subject: The complete guide to [Use Case]
CTA: Download guide, join webinar

Email 4: Day 10 (Social proof)
Subject: See why 500+ teams love [Product]
CTA: Read testimonials, watch customer stories

Email 5: Day 30 (Re-engagement)
Subject: We've missed you! Here's what you can do with [Product]
CTA: Explore features, contact support
```

#### Nurture Campaigns

**Content Drip:**
- Frequency: 1 email per week
- Focus: Educational (not promotional)
- Goal: Stay top-of-mind until ready to buy

**Topics:**
- Industry insights
- Best practices
- Customer success stories
- Product updates (sparingly)

### Deliverability Best Practices

**Authentication (Required):**
- **SPF:** Authenticate sending domain
- **DKIM:** Sign emails with cryptographic key
- **DMARC:** Policy for failed authentication

**List Hygiene:**
- Remove bounces immediately
- Suppress unsubscribes
- Re-engagement: Email inactive subscribers, remove non-openers after 6 months

**Engagement Optimization:**
- Test send times: Weekdays 9-11am best for B2B
- Optimize subject lines: A/B test every send
- Mobile-first: 60% open emails on mobile

## Resources

### Tools
- **Google Ads:** google.com/ads
- **LinkedIn Campaign Manager:** business.linkedin.com/marketing-solutions
- **Meta Business Suite:** business.facebook.com
- **Ahrefs:** ahrefs.com (SEO & competitor research)
- **SEMrush:** semrush.com (All-in-one marketing toolkit)

### Learning Resources
- **Google Skillshop:** Free Google Ads certification
- **LinkedIn Learning:** Platform-specific courses
- **HubSpot Academy:** Free inbound marketing courses
- **Reforge:** Advanced growth marketing programs

---

**Last Updated:** November 23, 2025
**Related Files:**
- [acquisition_frameworks.md](acquisition_frameworks.md) - High-level acquisition frameworks
- [conversion_optimization.md](conversion_optimization.md) - CRO methodologies
- [frameworks.md](frameworks.md) - Demand generation frameworks
