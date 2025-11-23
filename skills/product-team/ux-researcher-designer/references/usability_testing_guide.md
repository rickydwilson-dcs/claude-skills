# Usability Testing Guide Reference

## Overview
Comprehensive guide to planning, conducting, and analyzing usability tests to identify user experience issues and validate design decisions.

## Usability Testing Fundamentals

### Definition
Usability testing is a method to evaluate a product by testing it with representative users who perform realistic tasks while observers watch, listen, and take notes.

### Goals
- Identify usability problems
- Uncover opportunities for improvement
- Learn about user behavior and preferences
- Validate design decisions

### Types of Usability Tests

**Moderated Testing:**
- Facilitator guides participant through tasks
- Can ask follow-up questions
- Can probe for reasoning
- More insights but slower

**Unmoderated Testing:**
- Participant completes tasks independently
- Recorded for later review
- Faster and cheaper
- Less contextual insights

**Remote Testing:**
- Conducted via video call (moderated) or online tool (unmoderated)
- Broader geographic reach
- More convenient for participants

**In-Person Testing:**
- Conducted in same location
- Better observation of body language
- Easier to build rapport

## Planning Usability Tests

### Step 1: Define Goals & Research Questions (1-2 days)
**Questions to answer:**
- What do we want to learn?
- What decisions will this inform?
- What specific flows/features to test?

**Example Goals:**
- Validate new onboarding flow
- Identify pain points in checkout process
- Assess discoverability of key features

### Step 2: Recruit Participants (1-2 weeks)
**Target:** 5-8 participants per user segment

**Why 5 users?** Nielsen Norman Group research shows 5 users uncover 85% of usability issues

**Recruitment Criteria:**
- Match target persona (role, experience, tech savviness)
- Have not participated in recent studies (avoid bias)
- Incentivize appropriately ($50-100 for 1 hour is typical)

**Recruitment Methods:**
- Customer email list
- UserTesting.com, Respondent.io
- Social media (LinkedIn, Twitter)
- User research panels

### Step 3: Prepare Test Materials (2-3 days)
**Checklist:**
- [ ] Test script with tasks
- [ ] Prototype or product access
- [ ] Recording consent form
- [ ] Note-taking template
- [ ] Incentive (gift card, payment)

### Step 4: Conduct Pilot Test (1 day)
**Why?** Catch issues with script, prototype, or logistics

**Process:**
- Run test with colleague or friend
- Identify confusing instructions
- Ensure tasks are realistic
- Check technology works (screen sharing, recording)

## Conducting Usability Tests

### Test Script Structure (60 minutes)

**Introduction (5 min):**
- Welcome and thank participant
- Explain purpose: "We're testing the product, not you"
- Get consent for recording
- Encourage thinking aloud

**Background Questions (5 min):**
- Current role and responsibilities
- Experience with similar products
- Context for their workflow

**Tasks (40 min):**
- 4-6 tasks max
- Give realistic scenarios
- Let them struggle (don't help immediately)
- Encourage thinking aloud

**Debrief (10 min):**
- Overall impressions
- Most/least liked features
- Comparison to current solution
- Open-ended feedback

### Task Writing Best Practices

**Good Task:**
"Scenario: Your team's monthly report is due tomorrow. Export last month's project data to share with your manager."

**Bad Task:**
"Click on the export button and download a CSV file."

**Why?** Good tasks provide context, bad tasks are too prescriptive.

### Facilitator Techniques

**Think Aloud Protocol:**
- Ask: "Please narrate your thoughts as you go"
- Remind periodically if participant goes quiet
- Don't interrupt mid-task

**Probing Questions:**
- "What are you looking for?"
- "What do you expect to happen?"
- "Why did you choose that option?"
- "How does this compare to what you're used to?"

**When to Intervene:**
- Participant completely stuck (>2 minutes)
- Technical issue with prototype
- Task is impossible (design flaw)

**What Not to Do:**
- Lead the participant ("Try clicking that button")
- Defend the design ("That's intentional because...")
- Explain how it works (defeats purpose of test)

## Analyzing Results

### Step 1: Review Sessions (1-2 days)
- Watch recordings
- Take detailed notes
- Identify patterns across participants

### Step 2: Categorize Issues (1 day)
**Severity Levels:**

**Critical (P0):**
- Prevents task completion
- Causes data loss
- Security/privacy issue
- Examples: Broken flow, missing button

**High (P1):**
- Significantly frustrates users
- Causes errors/confusion
- Slows down completion
- Examples: Unclear labels, confusing navigation

**Medium (P2):**
- Minor annoyance
- Doesn't prevent completion
- Suggestion for improvement
- Examples: Copy clarity, visual polish

**Low (P3):**
- Nice-to-have
- Aesthetic preference
- Edge case
- Examples: Color choice, icon selection

### Step 3: Calculate Metrics

**Task Success Rate:**
```
Success Rate = (# successful completions / # total attempts) × 100%

Example:
- 5 participants attempted checkout
- 4 completed successfully
- Success rate: 80%
```

**Time on Task:**
```
Average time = Sum of all completion times / # of participants

Example:
- Participant 1: 120 seconds
- Participant 2: 95 seconds
- Participant 3: 130 seconds
- Average: 115 seconds
```

**System Usability Scale (SUS):**
- 10-question survey (1-5 scale)
- Score 0-100 (>68 is above average)
- Quick benchmark of overall usability

### Step 4: Synthesize Findings (1-2 days)
**Report Structure:**
1. Executive summary (1 page)
2. Methodology (participants, tasks)
3. Key findings (top 5-10 issues)
4. Recommendations (prioritized by severity)
5. Appendix (detailed notes, quotes, screenshots)

**Findings Template:**
```
**Issue #1: Users can't find export button** (P0)

Frequency: 5/5 participants struggled
Quote: "I looked everywhere for a download option"
Impact: 0% task success rate

Recommendation: Add prominent "Export" button in top nav
```

## Presenting Results

### Stakeholder Presentation
**Format:** 30-minute meeting with slides + video clips

**Structure:**
- Summary: What we tested, with whom
- Top findings: 3-5 critical issues (with video evidence)
- Impact: How issues affect business goals (conversion, retention)
- Recommendations: Prioritized fixes
- Next steps: Who owns what, timeline

**Tips:**
- Show video clips (30-60 seconds each)
- Use participant quotes
- Focus on actionable insights
- Connect to business metrics

### Video Highlights Reel
**Purpose:** Quick way to share findings broadly

**Format:**
- 3-5 minute compilation
- Show 3-5 key issues
- 30-60 seconds per issue
- Include participant quote + observation

## Resources
- Usability test script template
- Note-taking template
- Consent form template
- Findings report template
- SUS questionnaire

---
**Last Updated:** November 23, 2025
**Related:** ux_research_methods.md, persona_framework.md
