# Product Management Templates

PRD templates, interview guides, and best practices for product documentation.

## PRD Templates

### 1. Standard PRD Template

Comprehensive format for major features (6-8 week projects).

```markdown
# [Feature Name] PRD

**Author:** [Your Name]
**Status:** Draft | In Review | Approved
**Last Updated:** [Date]
**Target Release:** [Quarter/Version]

## 1. Executive Summary
**Problem:** [2-3 sentences on the problem]
**Solution:** [2-3 sentences on proposed solution]
**Impact:** [Expected business/user outcome]
**Effort:** [Estimated person-months]

## 2. Background & Context
- Why now? What's changed?
- Market trends or competitive pressure
- Strategic alignment (OKRs, company goals)
- Previous attempts or related work

## 3. Problem Statement
**Who has this problem?**
- User persona/segment
- How many users? (market size)

**What is the problem?**
- Specific pain points
- Current workarounds
- Frequency and severity

**Why does it matter?**
- Business impact (revenue, retention, cost)
- User impact (time saved, frustration reduced)

## 4. Goals & Success Metrics
**Primary Goal:** [One sentence]

**Success Metrics:**
- Metric 1: [Baseline → Target by date]
- Metric 2: [Baseline → Target by date]
- Metric 3: [Baseline → Target by date]

**How we'll measure:**
- Analytics events to track
- Dashboard/report to monitor
- Review cadence (weekly/monthly)

## 5. Proposed Solution
**High-Level Approach:**
[Describe solution in 2-3 paragraphs]

**User Experience:**
- User journey/flow diagram
- Wireframes or mockups (link to Figma)
- Key interactions and states

**Key Features:**
1. Feature A: Description
2. Feature B: Description
3. Feature C: Description

## 6. Scope
**In Scope:**
- Feature 1
- Feature 2
- Feature 3

**Out of Scope (for this release):**
- Feature X: Reason for exclusion
- Feature Y: Planned for future release
- Feature Z: Not aligned with goals

## 7. User Stories & Acceptance Criteria
**Epic:** [Epic name and Jira link]

**User Stories:**
```
US-1: As a [user type], I want to [action] so that [benefit]
Acceptance Criteria:
- Given [context], when [action], then [outcome]
- Given [context], when [action], then [outcome]
```

## 8. Design & UX Considerations
- Design principles applied
- Accessibility requirements (WCAG 2.1 AA)
- Mobile/responsive behavior
- Internationalization needs
- Link to design specs

## 9. Technical Considerations
**Architecture:**
- High-level technical approach
- Key components affected
- API changes

**Dependencies:**
- External services/APIs
- Other features or teams
- Infrastructure requirements

**Technical Risks:**
- Risk 1: Mitigation plan
- Risk 2: Mitigation plan

## 10. Launch Plan
**Rollout Strategy:**
- Beta testing (who, when, duration)
- Gradual rollout % (e.g., 10% → 50% → 100%)
- Feature flag configuration

**Marketing/Communication:**
- Internal announcement plan
- Customer communication (email, in-app)
- Documentation updates needed

**Support Readiness:**
- Support team training
- Help docs/FAQs to create
- Expected support volume

## 11. Open Questions & Decisions
- [ ] Question 1: Owner, due date
- [ ] Question 2: Owner, due date
- [ ] Decision needed: Options, decision maker

## Appendix
### Research & Validation
- User interview findings (link)
- Usage data analysis (link)
- Competitive analysis (link)

### Timeline
- Discovery: [Dates]
- Design: [Dates]
- Development: [Dates]
- Testing: [Dates]
- Launch: [Date]

### Stakeholders
- PM: [Name]
- Engineering: [Name]
- Design: [Name]
- Marketing: [Name]
- Support: [Name]
```

**When to Use:**
- Complex features affecting multiple user flows
- Features requiring cross-team coordination
- Strategic initiatives with executive visibility
- Features with significant technical complexity

---

### 2. One-Page PRD

Concise format for smaller features (2-4 week projects).

```markdown
# [Feature Name]

**PM:** [Name] | **Engineer:** [Name] | **Designer:** [Name]
**Target:** [Q2 2025] | **Status:** [Draft]

## Problem
[2-3 sentences describing the user problem and why it matters]

## Solution
[2-3 sentences describing the proposed solution]

**User Flow:**
1. User does [action]
2. System shows [result]
3. User achieves [outcome]

## Success Metrics
- [Metric 1]: [Current] → [Target]
- [Metric 2]: [Current] → [Target]

## Scope
**In:** Feature A, Feature B, Feature C
**Out:** Feature X (future), Feature Y (not aligned)

## Key Decisions
- Decision 1: [Chosen approach and why]
- Decision 2: [Chosen approach and why]

## Risks
- Risk 1: [Mitigation]
- Risk 2: [Mitigation]

## Timeline
Design: [Week 1-2] | Dev: [Week 3-5] | QA: [Week 6] | Launch: [Week 7]
```

**When to Use:**
- Incremental improvements to existing features
- Quick wins identified in prioritization
- Features with clear scope and low ambiguity
- Internal tools or admin features

---

### 3. Agile Epic Template

Sprint-based format for iterative delivery.

```markdown
# Epic: [Epic Name]

**Epic ID:** [JIRA-123]
**Product Owner:** [Name]
**Squad:** [Team Name]
**Sprint Target:** [Sprint 24]

## Epic Goal
[One sentence describing the outcome we're trying to achieve]

## User Value
**As a** [user type]
**I want to** [capability]
**So that** [benefit/value]

## Success Criteria
- [ ] Metric 1 achieves [target]
- [ ] Metric 2 achieves [target]
- [ ] User feedback score [target]

## User Stories

### Story 1: [Story Name] (8 points)
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

**Definition of Done:**
- [ ] Code reviewed and merged
- [ ] Unit tests written (>80% coverage)
- [ ] QA tested and passed
- [ ] Documentation updated
- [ ] Demo to stakeholders

### Story 2: [Story Name] (5 points)
[Repeat structure above]

## Dependencies
- Dependency 1: [Description, team, blocker status]
- Dependency 2: [Description, team, blocker status]

## Technical Notes
- Architecture considerations
- API changes
- Data migration needs

## Sprint Plan
**Sprint 24:** Stories 1-3 (21 points)
**Sprint 25:** Stories 4-6 (18 points)
**Sprint 26:** Polish & launch (8 points)

## Demo Plan
- Sprint 24 demo: [Feature X working end-to-end]
- Sprint 25 demo: [Feature Y integrated]
- Sprint 26 demo: [Full epic launch-ready]
```

**When to Use:**
- Teams practicing Agile/Scrum
- Features that can be broken into 2-week sprints
- Projects with evolving requirements
- Cross-functional squad delivery

---

### 4. Feature Brief

Lightweight exploration format for pre-PRD phase.

```markdown
# [Feature Name] - Exploration Brief

**Status:** Exploring | **Owner:** [Name] | **Date:** [Date]

## Hypothesis
We believe that [building this feature]
For [these users]
Will achieve [this outcome]
We'll know we're right when [metric/signal]

## Problem Evidence
**User Research:**
- Interview finding 1
- Interview finding 2
- Interview finding 3

**Data:**
- Usage metric showing problem
- Support ticket volume
- Competitive gap

## Potential Solutions
**Option A:** [Brief description]
- Pros: [List]
- Cons: [List]
- Effort: [Rough estimate]

**Option B:** [Brief description]
- Pros: [List]
- Cons: [List]
- Effort: [Rough estimate]

**Option C:** [Brief description]
- Pros: [List]
- Cons: [List]
- Effort: [Rough estimate]

## Next Steps
- [ ] User testing with prototype (Week 1-2)
- [ ] Technical spike for Option A (Week 2)
- [ ] Decision: Go/No-Go (Week 3)
- [ ] Write full PRD if Go (Week 4)

## Open Questions
- Question 1: What data/research would answer this?
- Question 2: What data/research would answer this?
```

**When to Use:**
- Early exploration phase
- Testing hypotheses before full PRD
- Getting alignment on problem before solution
- Comparing multiple solution approaches

---

## Interview Guides

### Discovery Interview Script

**Goal:** Understand user problems and workflows

**Duration:** 30-45 minutes

**Pre-Interview Checklist:**
- [ ] Review participant background
- [ ] Test recording setup
- [ ] Prepare 3 hypotheses to test
- [ ] Have note-taker join

**Script:**

**Introduction (2 min)**
```
Hi [Name], thanks for joining! I'm [Your Name], PM for [Product Area].

Today I want to learn about [problem space] and how you currently handle [workflow]. There are no right or wrong answers - I'm just trying to understand your experience.

I'll record this for note-taking. Everything shared is confidential. Sound good?
```

**Context Questions (5 min)**
```
1. Tell me about your role - what are you responsible for?
2. Walk me through a typical [day/week] in your job
3. What tools do you use regularly for [task area]?
4. How does [our product area] fit into your workflow?
```

**Problem Exploration (20 min)**
```
5. What are the biggest challenges you face with [problem area]?
   → Follow-up: Tell me about the last time that happened
   → Follow-up: How did you handle it?
   → Follow-up: How often does this come up?

6. Walk me through your current process for [specific task]
   → Probe: What's frustrating about that?
   → Probe: What takes the most time?
   → Probe: Where do things usually go wrong?

7. Have you tried other solutions or workarounds?
   → Follow-up: What did you try?
   → Follow-up: Why didn't that work?

8. If you could wave a magic wand, what would you change?
   → Probe: What would that enable you to do?
   → Probe: How much time would that save?
   → Probe: What's the impact if this stays broken?
```

**Solution Validation (10 min - Optional)**
```
9. [Show concept] What's your initial reaction to this?
   → Follow-up: How would this fit into your workflow?
   → Follow-up: What concerns do you have?

10. On a scale of 1-10, how much would this improve your workflow?
    → Follow-up: What would make it a 10?

11. Would you pay for something like this? How much?
```

**Wrap-Up (3 min)**
```
12. Is there anything I didn't ask about that I should have?
13. Who else should I talk to about this problem?
14. Can I follow up with you as we develop this?
15. Would you be interested in testing an early version?
```

**Post-Interview (10 min)**
- Debrief with note-taker
- Rate pain level: High | Medium | Low
- Extract key quotes
- Update research synthesis doc

---

### Solution Validation Interview

**Goal:** Test solution concepts with users

**Duration:** 45-60 minutes

**Materials Needed:**
- Interactive prototype or mockups
- Task list for usability testing
- Recording setup

**Script:**

**Introduction (3 min)**
```
Thanks for joining! Today I want to show you something we're exploring and get your honest feedback.

I'll ask you to try some tasks and think out loud as you go. Remember - we're testing the design, not you. If something is confusing, that's valuable feedback.

I'll be recording, but everything is confidential. Any questions before we start?
```

**Context Refresh (5 min)**
```
1. Quick reminder - tell me about [the problem we're solving]
2. How do you currently handle [task]?
```

**Prototype Testing (30 min)**
```
For each task:

"I'm going to give you a scenario. Try to complete the task while thinking out loud."

TASK 1: [Specific task]
- Observe: Where do they click first?
- Note: Confusion points, error states
- Ask: "What did you expect to happen?"
- Ask: "How would you describe this feature to a colleague?"

TASK 2: [Specific task]
[Repeat]

After all tasks:
3. What did you find confusing or frustrating?
4. What worked well?
5. How does this compare to [competitor/current solution]?
6. Would you use this in your daily work?
7. What's missing that would make this more useful?
```

**Value Assessment (10 min)**
```
8. How much would this improve your workflow? (1-10)
   → Follow-up: Why that score?
   → Follow-up: What would make it higher?

9. Is this a must-have, nice-to-have, or don't-need?
   → Follow-up: Why?

10. Would you pay for this? How much?
    → Follow-up: What price feels fair?
```

**Wrap-Up (2 min)**
```
11. Any other thoughts before we finish?
12. Can I follow up if we have more questions?
```

**Post-Interview (15 min)**
- Score prototype: SUS (System Usability Scale)
- Document usability issues (severity)
- Extract key quotes
- Update design backlog

---

## Best Practices

### Writing Great PRDs

1. **Start with the problem, not solution**
   - Users don't care about features, they care about problems solved
   - Validate problem before prescribing solution
   - Include user research evidence

2. **Include clear success metrics upfront**
   - Define metrics before building
   - Baseline → Target → Timeline
   - Leading indicators (adoption) and lagging (revenue)

3. **Explicitly state what's out of scope**
   - Prevents scope creep
   - Sets stakeholder expectations
   - Documents trade-off decisions

4. **Use visuals (wireframes, flows)**
   - Link to Figma/design tool
   - Embed key screens in PRD
   - User flow diagrams for complex journeys

5. **Keep technical details in appendix**
   - PRD = product story, not technical spec
   - Link to technical design doc
   - Focus on "what" and "why," not "how"

6. **Version control changes**
   - Track decisions and rationale
   - Update changelog when scope changes
   - Archive old versions

### Effective Prioritization

1. **Mix quick wins with strategic bets**
   - 60% core roadmap, 20% quick wins, 20% technical debt
   - Balance short-term and long-term value

2. **Consider opportunity cost**
   - What are you NOT building?
   - Say no to good ideas for great ones

3. **Account for dependencies**
   - Map cross-team dependencies early
   - Build foundational pieces first
   - Communicate blockers proactively

4. **Buffer for unexpected work (20%)**
   - Production issues
   - Customer escalations
   - Scope changes

5. **Revisit quarterly**
   - Market conditions change
   - New data invalidates assumptions
   - Re-prioritize based on learnings

6. **Communicate decisions clearly**
   - Why we're doing X
   - Why we're NOT doing Y
   - Trade-offs made

### Customer Discovery Tips

1. **Ask "why" 5 times**
   - Surface root causes, not symptoms
   - Example: "It's too slow" → "Why does speed matter?" → [continue]

2. **Focus on past behavior, not future intentions**
   - "Tell me about the last time..." vs "Would you use...?"
   - Actions speak louder than hypothetical words

3. **Avoid leading questions**
   - Bad: "Don't you think feature X would be great?"
   - Good: "How do you currently solve problem Y?"

4. **Interview in their environment**
   - Watch them use current tools
   - Observe actual workflow
   - See real pain points

5. **Look for emotional reactions**
   - Frustration = pain point
   - Excitement = job-to-be-done
   - Indifference = low priority

6. **Validate with data**
   - Interviews = qualitative (why)
   - Analytics = quantitative (what/how much)
   - Combine both for full picture

### Stakeholder Management

1. **Identify RACI for decisions**
   - Responsible: Does the work
   - Accountable: Makes final decision
   - Consulted: Provides input
   - Informed: Kept in the loop

2. **Regular async updates**
   - Weekly progress emails
   - Slack/status updates
   - Shared docs with changelog

3. **Demo over documentation**
   - Working prototype > 20-page PRD
   - Show, don't just tell
   - Get feedback early and often

4. **Address concerns early**
   - Don't let small issues become big blockers
   - Proactive 1:1s with skeptical stakeholders
   - Seek to understand objections

5. **Celebrate wins publicly**
   - Credit the team
   - Share metrics/impact
   - Build momentum

6. **Learn from failures openly**
   - Share what didn't work
   - Document lessons learned
   - Update process to prevent recurrence

---

## Common Pitfalls to Avoid

1. **Solution-First Thinking**
   - Problem: Jumping to features before understanding problems
   - Fix: Always write problem statement before solution

2. **Analysis Paralysis**
   - Problem: Over-researching without shipping
   - Fix: Set research timebox, ship iteratively

3. **Feature Factory**
   - Problem: Shipping features without measuring impact
   - Fix: Define success metrics before building

4. **Ignoring Technical Debt**
   - Problem: Not allocating time for platform health
   - Fix: Reserve 20% capacity for tech debt

5. **Stakeholder Surprise**
   - Problem: Not communicating early and often
   - Fix: Weekly updates, no-surprise culture

6. **Metric Theater**
   - Problem: Optimizing vanity metrics over real value
   - Fix: Focus on metrics tied to business outcomes

---

**Last Updated:** 2025-11-08
**Related Files:**
- [frameworks.md](frameworks.md) - RICE, discovery frameworks, metrics
- [tools.md](tools.md) - Python scripts and integrations
