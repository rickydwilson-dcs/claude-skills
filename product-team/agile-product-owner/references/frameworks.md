# Agile Product Ownership Frameworks

Comprehensive methodologies and best practices for agile product ownership.

## INVEST Criteria for User Stories

The gold standard for well-formed user stories.

### Independent
Stories should be self-contained and completable without dependencies.

**Good Example:**
```
US-001: As a user, I want to view my dashboard so that I can see key metrics
```

**Bad Example:**
```
US-002: As a user, I want to add widgets to my dashboard (depends on US-001)
```

**How to Fix:**
- Break dependencies by completing foundational work first
- Use epics to group related stories
- Identify minimal viable slice per story

### Negotiable
Stories should allow flexibility in implementation details.

**Good Example:**
```
US-003: As a user, I want to export data to analyze offline
(Implementation: CSV, Excel, or JSON - team can decide)
```

**Bad Example:**
```
US-004: As a user, I want export as CSV using Python pandas library with UTF-8 encoding
(Too prescriptive, removes team's technical decisions)
```

### Valuable
Every story must deliver value to users or business.

**Test Questions:**
- Would users notice if we didn't build this?
- Does this move us closer to business goals?
- Can we measure the impact?

**Red Flags:**
- "As a developer, I want to refactor..." (technical, not user-facing)
- "As a system, we need..." (no user benefit described)

**How to Make Valuable:**
- Connect technical work to user outcomes
- Frame as enabler: "Enable faster load times for dashboard"

### Estimable
Team should be able to size the story with reasonable confidence.

**Estimation Killers:**
- Too vague: "Improve performance"
- Too large: "Build complete analytics platform"
- Unknown technology: "Integrate with TBD third-party API"

**How to Make Estimable:**
- Break into smaller pieces
- Spike unknown technical areas first
- Add acceptance criteria for clarity

### Small
Stories should fit within one sprint (typically 1-2 weeks).

**Size Guidelines:**
- 1-2 points: Can complete in 1-2 days
- 3-5 points: Fits comfortably in sprint
- 8+ points: Too large, needs breakdown

**Breakdown Strategies:**
- By user workflow: Create → View → Edit → Delete
- By complexity: Basic → Advanced features
- By platform: Web → Mobile → API

### Testable
Clear acceptance criteria enable verification.

**Good Example:**
```
Acceptance Criteria:
- Given user is logged in
- When they click "Export Data"
- Then CSV file downloads with all visible rows
- And filename includes current date
```

**Bad Example:**
```
Acceptance Criteria:
- Export should work well
- Performance should be good
```

**Testable Pattern:**
```
Given [precondition]
When [action]
Then [expected outcome]
```

## Sprint Planning Framework

### Sprint Planning Part 1: What Will We Build? (2 hours)

**Participants:** Product Owner, Development Team, Scrum Master

**Agenda:**
1. Review sprint goal (15 min)
2. Review prioritized backlog (15 min)
3. Team pulls stories based on capacity (60 min)
4. Commit to sprint scope (15 min)
5. Identify dependencies and risks (15 min)

**Inputs:**
- Refined backlog (top stories estimated and ready)
- Team capacity (account for PTO, meetings, support)
- Sprint goal aligned with quarterly objectives

**Outputs:**
- Committed user stories
- Sprint goal statement
- Initial task breakdown

**Capacity Calculation:**
```
Team capacity = (# developers × working days × productive hours) × velocity adjustment

Example:
- 5 developers
- 10 working days (2 week sprint)
- 6 productive hours/day (accounting for meetings, email, etc.)
- 0.8 velocity adjustment (realistic delivery)

Capacity = 5 × 10 × 6 × 0.8 = 240 hours or ~30 story points
```

### Sprint Planning Part 2: How Will We Build It? (2 hours)

**Participants:** Development Team (Product Owner optional)

**Agenda:**
1. Break stories into tasks (90 min)
2. Identify technical dependencies (15 min)
3. Assign initial task owners (15 min)

**Task Breakdown:**
```
US-005: User can filter dashboard by date range
├─ Task 1: Design date picker component (4h)
├─ Task 2: Backend API for date filtering (6h)
├─ Task 3: Frontend integration (5h)
├─ Task 4: Write unit tests (3h)
├─ Task 5: Update documentation (2h)
Total: 20 hours (5 story points)
```

**Definition of Ready Checklist:**
- [ ] Story meets INVEST criteria
- [ ] Acceptance criteria defined
- [ ] Story estimated by team
- [ ] Dependencies identified
- [ ] UX/designs available (if needed)
- [ ] Technical approach discussed

### Sprint Review (1 hour)

**Purpose:** Demonstrate completed work to stakeholders

**Agenda:**
1. Recap sprint goal (5 min)
2. Demo completed stories (40 min)
3. Gather stakeholder feedback (10 min)
4. Review metrics and burn down (5 min)

**Demo Best Practices:**
- Show working software, not slides
- Follow user journeys, not feature lists
- Highlight user value, not technical details
- Be honest about incomplete work

**Stakeholder Questions:**
- What problem does this solve?
- How does this compare to competitors?
- When will customers get this?
- What's next?

### Sprint Retrospective (1 hour)

**Purpose:** Improve team processes

**Format: Start-Stop-Continue**
- **Start:** What should we begin doing?
- **Stop:** What should we stop doing?
- **Continue:** What's working well?

**Alternative Format: 4Ls**
- **Liked:** What went well?
- **Learned:** What did we learn?
- **Lacked:** What was missing?
- **Longed For:** What do we wish we had?

**Action Items:**
- Identify top 1-3 improvements
- Assign owners
- Make improvements visible
- Review in next retro

### Daily Standup (15 min)

**Three Questions:**
1. What did I complete yesterday?
2. What will I work on today?
3. What blockers do I have?

**Anti-Patterns to Avoid:**
- Status reports to manager (speak to team, not PO)
- Problem-solving discussions (take offline)
- Going over 15 minutes (time-box strictly)

**Standup Board Workflow:**
```
TODO → IN PROGRESS → CODE REVIEW → TESTING → DONE

Track:
- Story points in each column
- Blockers (red flag)
- Risks (yellow flag)
```

## Backlog Refinement

### Refinement Sessions (1 hour, mid-sprint)

**Participants:** Product Owner, Development Team

**Goals:**
- Break down upcoming epics into stories
- Estimate stories for next 2-3 sprints
- Clarify acceptance criteria
- Identify dependencies

**Refinement Output:**
- 2-3 sprints of refined backlog
- All top stories estimated and ready
- Questions answered, risks identified

### Story Estimation: Planning Poker

**Process:**
1. Product Owner reads story
2. Team asks clarifying questions
3. Each member selects estimate card (1,2,3,5,8,13,21)
4. Reveal simultaneously
5. Discuss high/low outliers
6. Re-vote until consensus

**Fibonacci Scale:**
- 1 point: Trivial change (2-4 hours)
- 2 points: Simple feature (4-8 hours)
- 3 points: Moderate complexity (1 day)
- 5 points: Complex feature (2-3 days)
- 8 points: Very complex (3-5 days)
- 13 points: Too large - needs breakdown

**Estimation Tips:**
- Estimate relative to reference stories
- Don't overthink - use gut feel
- Include testing, documentation, deployment
- When in doubt, go higher

## Velocity Tracking

### Calculating Velocity

**Velocity** = Average story points completed per sprint

**Example:**
```
Sprint 1: 28 points completed
Sprint 2: 32 points completed
Sprint 3: 27 points completed
Sprint 4: 31 points completed

Average velocity = (28 + 32 + 27 + 31) / 4 = 29.5 points/sprint
```

**Usage:**
- Forecast release dates
- Plan sprint capacity
- Identify trends (improving or declining)

### Velocity Trends

**Improving Velocity:**
- Team becoming more efficient
- Technical debt being paid down
- Better collaboration

**Declining Velocity:**
- Accumulating technical debt
- Team disruptions (new members, turnover)
- Scope creep in stories

**Volatile Velocity:**
- Inconsistent story sizing
- External interruptions (production issues)
- Unclear requirements

### Burndown Charts

**Sprint Burndown:**
```
30 points |⟍
          |  ⟍     Ideal
          |    ⟍
20 points |      ⟍⟋⟋ Actual
          |        ⟍
10 points |          ⟍
          |            ⟍
   0      |______________⟍___
          Day 1  →  Day 10
```

**Burndown Patterns:**

**Healthy:**
- Actual tracks close to ideal
- Steady downward trend
- Reaches zero by end of sprint

**Warning Signs:**
- Flat line (no stories completing)
- Late spike down (work rushed at end)
- Upward trend (scope added mid-sprint)

### Release Planning

**Formula:**
```
Sprints needed = Total story points / Average velocity

Example:
- Feature set: 120 story points
- Team velocity: 30 points/sprint
- Sprints needed: 120 / 30 = 4 sprints (8 weeks)
```

**Buffer for Risk:**
- Add 20-30% buffer for unknowns
- Account for holidays, PTO
- Reserve capacity for production issues

## Product Owner Ceremonies

### Backlog Prioritization Process

**Weekly Activity (1 hour):**
1. Review new feature requests
2. Update priorities based on:
   - Business value
   - User feedback
   - Technical dependencies
   - Strategic alignment
3. Ensure top 2-3 sprints are refined
4. Remove/archive obsolete stories

**Prioritization Framework:**
```
Priority Score = (Business Value + User Impact + Strategic Fit) - Technical Risk

Business Value: 1-5 (revenue, cost reduction)
User Impact: 1-5 (users affected, pain level)
Strategic Fit: 1-5 (OKR alignment)
Technical Risk: 0-5 (complexity, unknowns)
```

### Stakeholder Communication

**Weekly Stakeholder Update (30 min):**
- Sprint progress (velocity, burndown)
- Upcoming priorities
- Risks and blockers
- Decisions needed

**Monthly Product Review (1 hour):**
- Quarterly goals progress
- Feature delivery timeline
- User feedback themes
- Roadmap adjustments

### Acceptance Testing

**Definition of Done:**
- [ ] Code complete and merged
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests pass
- [ ] Acceptance criteria met
- [ ] Product Owner approved
- [ ] Documentation updated
- [ ] Deployed to production

**Acceptance Testing Process:**
1. Review acceptance criteria
2. Test happy path
3. Test error conditions
4. Test edge cases
5. Verify on multiple browsers/devices
6. Check accessibility compliance

**Rejection Scenarios:**
- Acceptance criteria not met
- Bugs found in testing
- Performance issues
- Accessibility failures
- Missing documentation

**When to Reject:**
- Clear defects preventing use
- Acceptance criteria not met
- Technical debt too high

**When to Accept with Follow-up:**
- Minor polish needed
- Edge case improvements
- Performance optimization opportunities

---

**Last Updated:** 2025-11-08
**Related Files:**
- [templates.md](templates.md) - User story templates and epic formats
- [tools.md](tools.md) - user_story_generator.py documentation
