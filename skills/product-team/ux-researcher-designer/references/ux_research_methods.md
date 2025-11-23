# UX Research Methods Reference Guide

## Overview
Comprehensive guide to UX research methods, when to use them, and how to conduct them effectively to inform product and design decisions.

## Research Method Selection

### Attitudinal vs Behavioral
**Attitudinal:** What people say
- Surveys, interviews, focus groups
- Understand perceptions and opinions

**Behavioral:** What people do
- Usability tests, analytics, A/B tests
- Understand actual behavior (often differs from attitudes)

### Qualitative vs Quantitative
**Qualitative:** Why and how
- Interviews, usability tests, field studies
- Rich insights, understand motivations
- Small sample size (5-30 participants)

**Quantitative:** How many and how much
- Surveys, analytics, A/B tests
- Statistical significance, measure trends
- Large sample size (100+ participants)

### Generative vs Evaluative
**Generative:** Discover needs and opportunities
- User interviews, field studies, diary studies
- Early in product development
- Answer: "What should we build?"

**Evaluative:** Test and validate solutions
- Usability tests, A/B tests, surveys
- During/after design
- Answer: "Did we build it right?"

## Research Methods

### 1. User Interviews (Qualitative, Attitudinal, Generative)

**When to use:**
- Understanding user needs, goals, pain points
- Exploring new problem space
- Early discovery phase

**Participants:** 5-15 people per segment

**Format:** 30-60 minute 1-on-1 conversations

**Process:**
1. Recruit target users
2. Prepare interview guide (10-15 questions)
3. Conduct interviews (record with consent)
4. Analyze and synthesize themes
5. Document findings (quotes, insights)

**Question Types:**
- Open-ended: "Tell me about your process for..."
- Probing: "Why is that important to you?"
- Scenario: "Walk me through the last time you..."

**Tips:**
- Ask open-ended questions
- Listen more than talk (80/20 rule)
- Follow up on interesting responses
- Avoid leading questions

### 2. Surveys (Quantitative, Attitudinal, Evaluative)

**When to use:**
- Measure satisfaction, preferences, behaviors
- Validate findings from qualitative research
- Track changes over time

**Participants:** 100+ for statistical significance

**Format:** 5-20 questions, 5-10 minutes to complete

**Question Types:**
- Multiple choice: "Which feature do you use most?"
- Likert scale: "How satisfied are you? (1-5)"
- Open-ended: "What's your biggest frustration?"

**Best Practices:**
- Keep it short (10 min max)
- Avoid biased/leading questions
- Use validated scales (NPS, SUS, UMUX)
- Pilot test before full launch

**Metrics:**
- Net Promoter Score (NPS): "How likely to recommend?"
- Customer Satisfaction (CSAT): "How satisfied are you?"
- Customer Effort Score (CES): "How easy was it?"

### 3. Usability Testing (Qualitative, Behavioral, Evaluative)

**When to use:**
- Evaluate ease of use
- Identify usability problems
- Validate design solutions

**Participants:** 5-8 per user segment

**Format:** 60-minute session, 4-6 tasks

**Process:**
1. Define test goals and tasks
2. Recruit participants
3. Conduct test (think aloud protocol)
4. Analyze results (success rate, time on task, issues)
5. Prioritize fixes

**Metrics:**
- Task success rate
- Time on task
- Error rate
- Satisfaction (SUS score)

**See:** usability_testing_guide.md for detailed guide

### 4. Card Sorting (Qualitative/Quantitative, Behavioral, Generative)

**When to use:**
- Design information architecture
- Understand mental models
- Organize navigation/menus

**Types:**
- **Open:** Participants create own categories
- **Closed:** Participants sort into predefined categories
- **Hybrid:** Participants can create or use existing categories

**Tools:** OptimalSort, Miro, physical cards

**Analysis:**
- Identify common groupings
- Calculate agreement rates
- Create dendrogram (similarity matrix)

### 5. Tree Testing (Quantitative, Behavioral, Evaluative)

**When to use:**
- Evaluate information architecture
- Test navigation structure
- Validate sitemap before building

**Format:** Present text-only hierarchy, ask users to find items

**Metrics:**
- Success rate: Did they find correct location?
- Directness: Did they go straight there?
- Time: How long did it take?

**Tools:** Treejack (Optimal Workshop), UsabilityHub

### 6. A/B Testing (Quantitative, Behavioral, Evaluative)

**When to use:**
- Compare two design variations
- Make data-driven decisions
- Optimize conversion rates

**Requirements:**
- Large traffic volume (1000+ users per variant)
- Clear hypothesis
- Defined success metric

**Process:**
1. Identify element to test (headline, CTA, layout)
2. Create variations (A vs B)
3. Split traffic 50/50
4. Run until statistical significance
5. Implement winner

**Tools:** Optimizely, VWO, Google Optimize

### 7. Field Studies (Qualitative, Behavioral, Generative)

**When to use:**
- Understand context of use
- Observe real behavior in natural environment
- Deep contextual insights

**Format:** 2-4 hours observing users in their environment

**Methods:**
- Shadowing: Follow user through typical day
- Contextual inquiry: Observe + interview in context
- Diary study: Users self-report over time

**Applications:**
- Enterprise software (observe in office)
- Consumer products (observe at home)
- Mobile apps (observe on-the-go)

### 8. Analytics Analysis (Quantitative, Behavioral, Evaluative)

**When to use:**
- Understand actual usage patterns
- Identify drop-off points
- Track feature adoption

**Metrics:**
- Pageviews, sessions, users
- Conversion rates (signup, purchase)
- Feature adoption rates
- Time in app/on page
- Retention (D1, D7, D30)

**Tools:** Google Analytics, Mixpanel, Amplitude

**Analysis:**
- Funnel analysis: Where do users drop off?
- Cohort analysis: How does behavior change over time?
- Heatmaps: Where do users click?

### 9. Competitive Analysis (Qualitative, Attitudinal/Behavioral, Generative)

**When to use:**
- Understand market landscape
- Identify opportunities for differentiation
- Benchmark against competitors

**Process:**
1. Identify competitors (direct and indirect)
2. Evaluate on key dimensions (features, UX, pricing)
3. Test competitor products hands-on
4. Document strengths/weaknesses
5. Identify gaps and opportunities

**Deliverable:** Competitive feature matrix

### 10. Heuristic Evaluation (Qualitative, Attitudinal, Evaluative)

**When to use:**
- Quick UX audit
- Identify usability issues without user testing
- Expert review of interface

**Heuristics (Nielsen's 10):**
1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, and recover from errors
10. Help and documentation

**Process:**
1. Expert reviews interface against heuristics
2. Documents violations (severity: low, medium, high, critical)
3. Provides recommendations

## Research Planning

### Research Question Framework
**Format:** "How might we [objective] for [user] in [context]?"

**Examples:**
- "How might we reduce onboarding time for new users?"
- "How might we increase feature discoverability for power users?"
- "How might we simplify the checkout process for mobile shoppers?"

### Method Selection Matrix
| Goal | Method | Participants | Timeline |
|------|--------|-------------|----------|
| Discover needs | User interviews | 10-15 | 2-3 weeks |
| Validate idea | Surveys | 100+ | 1-2 weeks |
| Test usability | Usability testing | 5-8 | 1-2 weeks |
| Measure adoption | Analytics | All users | Ongoing |
| Optimize conversion | A/B test | 1000+ | 2-4 weeks |

### Research Plan Template
```
Research Goal: [What do we want to learn?]
Research Questions: [Specific questions to answer]
Method: [Which method(s) to use]
Participants: [Who and how many]
Timeline: [Start and end dates]
Deliverables: [What we'll produce]
Success Criteria: [How we'll know we learned enough]
```

## Resources
- Research method decision tree
- Research plan template
- Interview script template
- Survey template library
- Analytics dashboard templates

---
**Last Updated:** November 23, 2025
**Related:** persona_framework.md, usability_testing_guide.md
