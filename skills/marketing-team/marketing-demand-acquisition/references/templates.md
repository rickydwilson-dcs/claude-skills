# Campaign Templates & Examples

## 1. Campaign Planning Template

**Campaign Brief** (use this for every campaign):

```
Campaign Name: [Q2-2025-LinkedIn-ABM-Enterprise]
Objective: [Generate 50 SQLs from Enterprise accounts ($50k+ ACV)]
Budget: [$15k/month]
Duration: [90 days]
Channels: [LinkedIn Ads, Retargeting, Email]
Audience: [Director+ at SaaS companies, 500-5000 employees, EU/US]
Offer: [Gated Industry Benchmark Report]
Success Metrics:
  - Primary: 50 SQLs, <$300 CPO
  - Secondary: 500 MQLs, 10% MQL→SQL rate, 40% email open rate
HubSpot Setup:
  - Campaign ID: [create in HubSpot]
  - Lead scoring: +20 for download, +30 for demo request
  - Attribution: First-touch + Multi-touch
Handoff Protocol:
  - SQL criteria: Title + Company size + Budget confirmed
  - Routing: Enterprise SDR team via HubSpot workflow
  - SLA: 4-hour response time
```

## 2. HubSpot Campaign Tracking Setup

**Step-by-step**:

1. **Create Campaign in HubSpot**
   - Marketing → Campaigns → Create Campaign
   - Name: `Q2-2025-LinkedIn-ABM-Enterprise`
   - Tag all assets (landing pages, emails, ads) with campaign ID

2. **UTM Parameter Structure** (critical for attribution)
   ```
   utm_source={channel}       // linkedin, google, facebook
   utm_medium={type}          // cpc, display, email, organic
   utm_campaign={campaign-id} // q2-2025-linkedin-abm-enterprise
   utm_content={variant}      // ad-variant-a, email-1
   utm_term={keyword}         // [for paid search only]
   ```

3. **Lead Scoring Configuration**
   - Navigate to: Settings → Marketing → Lead Scoring
   - Campaign engagement: +10-30 points based on action depth
   - Channel quality: LinkedIn +5, Google Search +10, Organic +15

4. **Attribution Reports**
   - Use HubSpot's multi-touch attribution (W-shaped for hybrid motion)
   - First-touch: Awareness credit
   - Multi-touch: Full journey credit
   - Build custom report: Marketing → Reports → Attribution

## 3. HubSpot Workflow Templates

### Lead Scoring Workflow

```
Workflow Name: Lead Scoring - Campaign Engagement
Trigger: Contact property changed (Campaign ID)

Actions:
1. IF Campaign ID contains "Enterprise"
   THEN Increase lead score by 20

2. IF Form submission = "Demo Request"
   THEN Increase lead score by 30

3. IF Lead score >= 75
   THEN Send internal email to SDR team

4. IF Lead score >= 75 AND ICP Fit = "A"
   THEN Create task for SDR (Priority: High)

5. IF Lead score >= 90
   THEN Mark as MQL
   THEN Assign to SDR owner
```

### Nurture Workflow

```
Workflow Name: Nurture - Downloaded Content
Trigger: Form submission (eBook, whitepaper, template)

Email Sequence:
Day 0: Thank you email + download link
Day 2: Related blog post + case study
Day 5: Invitation to webinar or demo
Day 10: Customer testimonial + social proof
Day 15: Limited-time offer or CTA
Day 20: Last chance email

Branch Logic:
- IF Contact opens 3+ emails → Flag as "Engaged"
- IF Contact clicks demo CTA → Send to sales immediately
- IF No engagement after 20 days → Move to quarterly check-in list
```

### Lead Assignment Workflow

```
Workflow Name: SQL Assignment - Geographic Routing
Trigger: Contact lifecycle stage = SQL

Actions:
1. IF Country = "United States"
   THEN Assign to US Sales Team

2. IF Country IN ("United Kingdom", "Ireland")
   THEN Assign to UK Sales Team

3. IF Country IN ("Germany", "Austria", "Switzerland")
   THEN Assign to DACH Sales Team

4. IF Country IN ("France", "Belgium", "Luxembourg")
   THEN Assign to France Sales Team

5. ELSE
   THEN Assign to International Sales Team

6. Send notification email to assigned owner
7. Create follow-up task (Due: 4 hours)
```

## 4. Campaign Launch Checklist

### Pre-Launch (2 weeks before)

**Week -2:**
- [ ] Campaign brief approved by stakeholders
- [ ] Budget allocated in paid platforms
- [ ] Landing page built and tested (mobile + desktop)
- [ ] Forms created and connected to HubSpot
- [ ] Email templates designed and approved
- [ ] Ad creatives finalized (3-5 variants per platform)
- [ ] UTM parameters defined and documented
- [ ] HubSpot campaign created with tracking

**Week -1:**
- [ ] Test all conversion paths (landing page → form → thank you)
- [ ] Verify HubSpot tracking (test form submission)
- [ ] Set up paid campaigns (LinkedIn, Google, Meta)
- [ ] Schedule launch emails
- [ ] Train sales team on new campaign
- [ ] Create sales enablement materials
- [ ] Set up reporting dashboard
- [ ] Final stakeholder approval

### Launch Week

**Day 1:**
- [ ] Launch paid campaigns at 50% budget (test phase)
- [ ] Send announcement email to existing database
- [ ] Post social media announcement
- [ ] Monitor conversion rates hourly

**Days 2-3:**
- [ ] Analyze initial results
- [ ] Optimize underperforming ads
- [ ] A/B test landing page variants
- [ ] Scale budget on winning ads to 100%

**Days 4-7:**
- [ ] Weekly performance review
- [ ] Adjust bids and targeting
- [ ] Sales follow-up on leads
- [ ] Prepare week 2 optimizations

### Post-Launch (Weeks 2-4)

**Week 2:**
- [ ] Deep dive on conversion funnel
- [ ] Identify drop-off points
- [ ] Test new ad variants
- [ ] Optimize form fields
- [ ] Sales feedback session

**Week 3:**
- [ ] Mid-campaign performance report
- [ ] Budget reallocation (kill losers, scale winners)
- [ ] Launch retargeting campaigns
- [ ] Email nurture sequence optimization

**Week 4:**
- [ ] Final campaign report
- [ ] ROI analysis
- [ ] Document learnings
- [ ] Plan next campaign iteration

## 5. HubSpot Partner Tracking Setup

**Setup Instructions:**

1. **Create Partner Property**
   - Settings → Properties → Create "Partner Source" dropdown
   - Values: Partner A, Partner B, Affiliate Network, etc.

2. **UTM Tracking**
   - Partner links: `?utm_source=partner-name&utm_medium=referral`
   - HubSpot auto-captures UTM parameters

3. **Lead Assignment**
   - Workflow: If "Partner Source" is set → Assign to Partner Manager
   - Notification: Slack alert when partner lead arrives

4. **Reporting**
   - Dashboard: Partner-sourced leads, pipeline, revenue
   - Report to partners: Monthly performance summary

## 6. HubSpot ROI Dashboard Template

**Dashboard Configuration:**

```
Dashboard Name: Marketing ROI - Monthly Performance
Frequency: Real-time with monthly snapshots

Reports:
1. Marketing Spend (by channel)
   - Data: Custom property "Ad Spend"
   - Dimensions: Channel, Campaign, Month

2. Leads Generated
   - Metrics: MQLs, SQLs, Customers
   - Dimensions: Channel, Campaign, Source

3. CAC by Channel
   - Formula: Spend ÷ Customers
   - Benchmark: Display target CAC line

4. Pipeline Generated ($)
   - Metrics: Opportunity amount
   - Filters: Marketing-sourced
   - Dimensions: Channel, Campaign

5. ROAS/ROMI
   - Formula: Revenue ÷ Spend
   - Target: 3:1 minimum

6. Conversion Rates
   - Visitor → MQL
   - MQL → SQL
   - SQL → Customer

7. Top Performing Campaigns
   - Sort by: Pipeline $
   - Display: Top 10
```

## 7. Campaign Performance Report Template

```
CAMPAIGN PERFORMANCE REPORT
Campaign: [Q2-2025-LinkedIn-ABM-Enterprise]
Period: [April 1 - June 30, 2025]
Owner: [Demand Gen Manager]

EXECUTIVE SUMMARY
Goal: Generate 50 SQLs from Enterprise accounts
Result: 58 SQLs (116% of goal) ✅
Total Spend: $45k
CAC: $776 (vs. $1,000 target) ✅

KEY METRICS
Traffic:
- Landing page visitors: 12,450
- Unique visitors: 9,800
- Bounce rate: 42% (target: <50%) ✅

Leads:
- MQLs: 520 (goal: 500) ✅
- SQLs: 58 (goal: 50) ✅
- MQL→SQL rate: 11% (target: 10%) ✅

Pipeline:
- Opportunities created: 28
- Pipeline value: $1.4M
- Average deal size: $50k

CHANNEL BREAKDOWN
LinkedIn Ads:
- Spend: $20k
- MQLs: 280
- SQLs: 32
- CPL: $71
- CAC: $625

Google Search:
- Spend: $15k
- MQLs: 180
- SQLs: 20
- CPL: $83
- CAC: $750

Email:
- Spend: $2k (tools)
- MQLs: 60
- SQLs: 6
- CPL: $33
- CAC: $333

TOP PERFORMERS
1. LinkedIn - Thought Leadership Carousel (28% CTR)
2. Google - "[Competitor] Alternative" keywords (5.2% CVR)
3. Email - Case Study Sequence (22% open, 4.5% CTR)

UNDERPERFORMERS
1. LinkedIn - Product Demo Video (0.3% CTR) - Paused
2. Google Display - Broad Targeting (0.1% CVR) - Optimized
3. Email - Generic Pitch (8% open) - Retired

KEY LEARNINGS
1. Enterprise audience responds better to thought leadership than direct product pitches
2. Competitor keywords have 2x higher intent than category keywords
3. Case studies drive 3x higher engagement than product feature emails
4. LinkedIn lead gen forms have higher volume but lower quality than landing pages

NEXT STEPS
1. Double down on LinkedIn thought leadership content
2. Expand competitor keyword targeting
3. Create more industry-specific case studies
4. Test video testimonials in ads
5. Launch ABM retargeting campaign for engaged accounts

BUDGET RECOMMENDATION
Increase budget to $60k/month:
- LinkedIn: +$10k (proven winner)
- Google Search: +$5k (scale competitor keywords)
- New: $5k for ABM retargeting
```

## 8. Email Campaign Templates

### Cold Outreach Email

```
Subject: [First Name], quick question about [Pain Point]

Hi [First Name],

I noticed [Company] is [recent trigger event - hiring, funding, expansion].

Most [Job Title]s we work with struggle with [specific pain point]. They're spending [X hours/week] on [manual task] when they could be [desired outcome].

We help companies like [Similar Company 1] and [Similar Company 2] [achieve specific result] by [unique approach].

Would it make sense to explore how we could help [Company] do the same?

[CTA Button: Book 15-Min Call]

Best,
[Your Name]
[Title]

P.S. Here's a quick case study showing how [Similar Company] saved [X hours/month]: [Link]
```

### Demo Follow-Up Email

```
Subject: Thanks for your time today, [First Name]

Hi [First Name],

Great chatting with you about [Company]'s [specific challenge discussed].

As promised, here are the resources we discussed:
- [Resource 1]: [Link with UTM]
- [Resource 2]: [Link with UTM]
- Case study: [Similar Company] achieved [Result]: [Link]

Next steps:
1. [Action item from demo - e.g., "Share with your team"]
2. [Follow-up action - e.g., "I'll send over pricing options"]
3. [Proposed timeline - e.g., "Let's reconnect next week"]

[CTA Button: Schedule Follow-Up Call]

Any questions in the meantime? Just reply to this email.

Best,
[Your Name]

P.S. Here's a 2-min video recap of what we covered: [Loom link]
```

### Trial Conversion Email

```
Subject: [First Name], you're halfway through your trial

Hi [First Name],

You've been using [Product] for 7 days (halfway through your 14-day trial).

I wanted to check in and see how it's going:
- Have you been able to [key value prop]?
- Any questions about [specific feature]?
- Is there anything blocking you from [desired outcome]?

Here are the top 3 features our most successful customers use in their first week:
1. [Feature 1] - [Benefit]
2. [Feature 2] - [Benefit]
3. [Feature 3] - [Benefit]

[CTA Button: Book Onboarding Call]

Want to get more value before your trial ends? Let's jump on a quick call and I'll help you set up [specific workflow].

Best,
[Your Name]
[Customer Success Team]

P.S. Check out this 3-min video showing [Feature 1] in action: [Link]
```

### Closed Lost Re-Engagement

```
Subject: Still thinking about [Pain Point]?

Hi [First Name],

We spoke [X months] ago about helping [Company] with [specific challenge].

I know timing wasn't right back then, but I wanted to reach out because:
1. We've launched [new feature] that addresses [objection you had]
2. [Similar Company] just achieved [impressive result] using our platform
3. We're offering [limited-time incentive] for companies like yours

If [original pain point] is still a priority, I'd love to show you what's changed.

[CTA Button: Book 15-Min Catch-Up]

No pressure - just wanted to make sure you knew about these updates.

Best,
[Your Name]

P.S. Here's the case study I mentioned: [Similar Company] saved [X hours/month] and increased [metric] by [Y%]: [Link]
```

## 9. Ad Copy Templates

### LinkedIn Ad Copy

**Thought Leadership (Awareness):**
```
Headline: The hidden cost of [problem]
Body: Most [Job Title]s don't realize they're losing [X hours/week] to [manual task].

We analyzed 500+ [Industry] companies and found:
- [Surprising statistic 1]
- [Surprising statistic 2]
- [Surprising statistic 3]

Download our free report to see how top performers are solving this.

CTA: Get the Report
```

**Social Proof (Consideration):**
```
Headline: How [Well-Known Company] achieved [Impressive Result]
Body: [Company] was struggling with [problem].

After implementing [Your Solution], they:
✓ [Result 1]
✓ [Result 2]
✓ [Result 3]

See how they did it in this 3-min case study.

CTA: Read Case Study
```

**Direct Response (Conversion):**
```
Headline: [Product] for [Job Title]s who want [Desired Outcome]
Body: Stop [pain point]. Start [desired outcome].

[Product] helps [ICP] [achieve result] in [timeframe].

Trusted by [Social Proof]:
• [Company 1]
• [Company 2]
• [Company 3]

Try free for 14 days. No credit card required.

CTA: Start Free Trial
```

### Google Search Ad Copy

**Responsive Search Ad Template:**

```
Headlines (15):
H1: [Product Category] for [Use Case]
H2: [Primary Keyword] - Try Free
H3: Trusted by [X] Companies
H4: [Key Feature 1] + [Key Feature 2]
H5: Save [X Hours/Week] with [Product]
H6: [Competitor] Alternative
H7: Best [Product Category] 2025
H8: [Social Proof - e.g., 4.8★ on G2]
H9: No Credit Card Required
H10: Start Free Trial Today
H11: [Value Prop - e.g., 10x Faster]
H12: [Customer Logo - e.g., Used by Microsoft]
H13: {KeyWord:[Primary Keyword]}
H14: [Unique Feature]
H15: [Problem Solved]

Descriptions (4):
D1: [Product] helps [ICP] [achieve result]. Try free for 14 days. No credit card.
D2: [Feature 1], [Feature 2], [Feature 3]. Trusted by [X] companies. Get started in minutes.
D3: Stop [pain point]. [Product] is [X%] faster than [alternative]. See why [Customer] switched.
D4: [Social proof]. [Guarantee]. [CTA]. {KeyWord:[Primary Keyword]} made simple.
```

## 10. Landing Page Templates

### Demo Request Landing Page

```
HERO SECTION
Headline: [Problem Solved] in [Timeframe]
Subheadline: [Product] helps [ICP] [achieve specific result] without [pain point]
CTA: Book Your Demo
Image: Product screenshot or customer testimonial

SOCIAL PROOF
Logos: [5-10 customer logos]
Testimonial: "[Quote from happy customer]" - [Name, Title, Company]

VALUE PROPS (3-4 bullets)
✓ [Benefit 1] - [Supporting detail]
✓ [Benefit 2] - [Supporting detail]
✓ [Benefit 3] - [Supporting detail]
✓ [Benefit 4] - [Supporting detail]

FORM SECTION
Form Fields:
- First Name
- Last Name
- Work Email
- Company
- Company Size (dropdown)
- Phone (optional)

CTA Button: Book My Demo
Privacy: "We respect your privacy. Read our policy."

BELOW FOLD
How It Works (3 steps):
1. [Step 1] - [Description]
2. [Step 2] - [Description]
3. [Step 3] - [Description]

Case Study Carousel:
[Company 1] achieved [Result 1]
[Company 2] achieved [Result 2]
[Company 3] achieved [Result 3]

FAQ (3-5 questions):
Q: [Common objection]
A: [Answer with proof point]

FOOTER
Final CTA: Ready to get started?
Button: Book Your Demo
Links: Privacy Policy, Terms, Contact
```

### Gated Content Landing Page

```
HERO SECTION
Headline: [Content Title] - Free Download
Subheadline: Learn how [target audience] [achieve outcome]
Image: eBook cover or report preview

WHAT'S INSIDE (4-6 bullets)
In this [content type], you'll discover:
→ [Key insight 1]
→ [Key insight 2]
→ [Key insight 3]
→ [Key insight 4]

SOCIAL PROOF
"[Testimonial about content quality]" - [Name, Title]
Downloaded by [X]+ [job titles]

FORM SECTION
Form Fields:
- First Name
- Work Email
- Company (optional)

CTA Button: Download Now
Privacy: "Your email is safe with us."

PREVIEW
Table of Contents:
- Chapter 1: [Title]
- Chapter 2: [Title]
- Chapter 3: [Title]
- Chapter 4: [Title]

Key Takeaways:
✓ [Takeaway 1]
✓ [Takeaway 2]
✓ [Takeaway 3]

FOOTER
Company info, links, social media
```

## 11. Webinar Promotion Template

### Webinar Campaign Timeline

**4 Weeks Before:**
- [ ] Create webinar landing page with registration form
- [ ] Set up confirmation and reminder emails
- [ ] Design promotional graphics (social, email, ads)
- [ ] Write promotional copy (emails, social posts, ads)
- [ ] Launch paid promotion (LinkedIn, Google)

**3 Weeks Before:**
- [ ] Email announcement to database
- [ ] Social media promotion begins (3x per week)
- [ ] Partner cross-promotion
- [ ] First reminder email to registrants

**2 Weeks Before:**
- [ ] Email reminder to database (last chance to register)
- [ ] Increase social media frequency (daily)
- [ ] Scale winning paid ads
- [ ] Second reminder email to registrants

**1 Week Before:**
- [ ] Final email reminder to database
- [ ] Social media countdown (daily)
- [ ] Test webinar platform and tech
- [ ] Third reminder email to registrants (24 hours before)

**Day Of:**
- [ ] Final reminder email (1 hour before)
- [ ] Social media "live now" posts
- [ ] Monitor attendance
- [ ] Record session

**After Webinar:**
- [ ] Send recording to all registrants (within 24 hours)
- [ ] Follow-up email with resources and CTA
- [ ] Sales follow-up on engaged attendees
- [ ] Publish recording as gated content

### Webinar Promotion Email Sequence

**Email 1: Announcement (3 weeks before)**
```
Subject: [Free Webinar] [Topic] on [Date]

Hi [First Name],

Join us for a free webinar on [Date] at [Time]:

"[Webinar Title]"

You'll learn:
• [Key takeaway 1]
• [Key takeaway 2]
• [Key takeaway 3]

[CTA Button: Register Now]

Featuring:
- [Speaker 1], [Title] at [Company]
- [Speaker 2], [Title] at [Company]

Space is limited. Reserve your spot today.

Best,
[Your Name]
```

**Email 2: Reminder (1 week before)**
```
Subject: Reminder: [Webinar Title] next week

Hi [First Name],

Just a reminder - our webinar "[Webinar Title]" is next week.

[Date] at [Time] [Timezone]

[CTA Button: Add to Calendar]

What you'll learn:
→ [Benefit 1]
→ [Benefit 2]
→ [Benefit 3]

Can't make it live? Register anyway and we'll send you the recording.

See you there!
[Your Name]
```

**Email 3: Last Chance (1 day before)**
```
Subject: Tomorrow: [Webinar Title]

Hi [First Name],

Our webinar is tomorrow at [Time]:

"[Webinar Title]"

[CTA Button: Add to Calendar]

We'll cover:
✓ [Specific tactic 1]
✓ [Specific tactic 2]
✓ [Specific tactic 3]

Plus live Q&A with [Speaker Names].

Don't miss it!
[Your Name]

P.S. Register even if you can't attend live - we'll send the recording.
```

**Email 4: Recording (1 day after)**
```
Subject: [Recording] [Webinar Title]

Hi [First Name],

Thanks for registering for our webinar "[Webinar Title]"!

Here's the full recording: [Link]

Key resources mentioned:
- [Resource 1]: [Link]
- [Resource 2]: [Link]
- [Resource 3]: [Link]

[CTA Button: Book a Demo]

Want to see how [Product] can help you [achieve outcome]? Let's chat.

Best,
[Your Name]

P.S. Have questions? Reply to this email or book a call: [Calendar Link]
```
