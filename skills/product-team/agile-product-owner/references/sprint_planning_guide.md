# Sprint Planning Guide Reference

## Overview
Comprehensive guide for planning and executing successful sprint planning sessions, including preparation, facilitation techniques, capacity planning, and best practices for product owners and scrum masters.

## Sprint Planning Overview

### Two-Part Structure

**Part 1: What will we build? (2-4 hours)**
- Participants: Product Owner, Dev Team, Scrum Master
- Goal: Define sprint goal and commit to stories
- Output: Sprint backlog with committed stories

**Part 2: How will we build it? (2-4 hours)**
- Participants: Dev Team (PO optional)
- Goal: Break stories into tasks, identify dependencies
- Output: Detailed task breakdown with estimates

### Sprint Planning Inputs
- Refined product backlog (top stories estimated and ready)
- Team velocity (average story points per sprint)
- Team capacity (accounting for PTO, holidays, meetings)
- Product vision and roadmap
- Previous sprint retrospective actions

## Pre-Planning Preparation

### Product Owner Checklist (1 week before)
- [ ] Top 1-2 sprints of backlog refined and estimated
- [ ] Stories meet Definition of Ready
- [ ] Priority order clear and justified
- [ ] Sprint goal candidate identified
- [ ] Dependencies documented
- [ ] UX/design assets ready
- [ ] Stakeholder alignment on priorities

### Scrum Master Checklist (1 week before)
- [ ] Sprint planning meeting scheduled (4-8 hour block)
- [ ] Previous sprint retrospective actions reviewed
- [ ] Team velocity calculated (last 3-5 sprints average)
- [ ] Team capacity calculated (PTO, holidays accounted for)
- [ ] Planning tools ready (Jira, Miro, etc.)
- [ ] Room/Zoom set up with good tools (whiteboard, sticky notes)

### Development Team Prep (1 day before)
- [ ] Review top backlog stories
- [ ] Identify technical questions or unknowns
- [ ] Review previous sprint velocity
- [ ] Understand current technical constraints

## Capacity Planning

### Formula
```
Team Capacity = (# developers × working days × productive hours) × focus factor

Example for 2-week sprint:
- 5 developers
- 10 working days
- 6 hours/day productive time (accounting for meetings, email, etc.)
- 0.8 focus factor (realistic adjustment for interruptions)

Capacity = 5 × 10 × 6 × 0.8 = 240 hours
Or: ~30 story points (if 1 point ≈ 8 hours)
```

### Adjustments
**Reduce capacity for:**
- Team member PTO (-20% per person-day)
- Holidays (-full day)
- Onboarding new team members (-50% for first sprint)
- Production support rotation (-20% for on-call person)
- Large meetings/workshops (-hours blocked)

**Example Adjusted Capacity:**
```
Base: 30 story points
- Developer on PTO (3 days): -6 points
- Holiday (1 day): -6 points
- Production support: -6 points
Adjusted capacity: 12 story points
```

## Conducting Sprint Planning Part 1

### Agenda (2-4 hours)

**0-15 min: Review Sprint Goal**
- PO proposes sprint goal (1-2 sentences)
- Example: "Enable users to export reports in multiple formats"
- Team discusses feasibility
- Consensus on goal before pulling stories

**15-30 min: Review Top Backlog Stories**
- PO walks through prioritized backlog
- Clarify requirements, acceptance criteria
- Team asks questions

**30-150 min: Team Pulls Stories**
- Team self-selects stories based on capacity
- Start with highest priority stories
- Discuss technical approach briefly
- Check if story can be completed in sprint
- Continue until capacity reached

**150-180 min: Sprint Commitment**
- Review selected stories
- Confirm sprint goal still achievable
- Team commits to delivering stories
- Identify risks and dependencies
- Document in sprint planning notes

### Sprint Goal Examples

**Good Sprint Goals (Outcome-focused):**
- "Enable users to share reports with external stakeholders"
- "Reduce checkout abandonment rate with improved UX"
- "Launch MVP for mobile app onboarding"

**Bad Sprint Goals (Too vague or output-focused):**
- "Complete 30 story points"
- "Fix bugs and add features"
- "Work on project management features"

## Conducting Sprint Planning Part 2

### Agenda (2-4 hours)

**Task Breakdown Process:**
1. Take first story from sprint backlog
2. Team discusses technical approach
3. Break into granular tasks (2-8 hour chunks)
4. Estimate tasks in hours
5. Assign initial owners (optional, can happen during sprint)
6. Repeat for all stories

**Example Task Breakdown:**
```
Story: "User can export dashboard to PDF" (5 points)

Tasks:
├─ Design PDF template layout (4h)
├─ Backend: Create PDF generation API endpoint (6h)
├─ Backend: Fetch dashboard data for export (3h)
├─ Backend: Render charts as images for PDF (5h)
├─ Frontend: Add "Export PDF" button to dashboard (2h)
├─ Frontend: Show loading state during export (2h)
├─ Write unit tests for PDF generation (3h)
├─ Manual QA testing (3h)
└─ Update documentation (2h)

Total: 30 hours (matches ~5 point estimate at 6 hours/point)
```

### Technical Discussion Topics
- Architecture approach (API design, database schema)
- Third-party libraries or services needed
- Performance considerations
- Security implications
- Testing strategy
- Deployment approach

### Identifying Dependencies
**Types of Dependencies:**
- **Technical:** Requires another team's API, infrastructure change
- **Team:** Blocked by another team's work
- **Product:** Requires UX design, legal approval
- **External:** Third-party vendor, customer input

**Dependency Management:**
- Document dependencies clearly
- Assign owner to resolve
- Set deadlines earlier than needed
- Have backup plan if dependency blocks

## Common Planning Challenges

### Challenge 1: Team Over-Commits
**Symptom:** Team regularly completes <70% of committed work

**Solutions:**
- Calculate realistic velocity (past 3-5 sprints)
- Apply focus factor (0.7-0.8 typical)
- Include buffer for unknowns (10-20%)
- Break large stories into smaller pieces
- Improve backlog refinement (reduce unknowns)

### Challenge 2: Stories Not "Ready"
**Symptom:** Stories pulled into sprint lack clarity, acceptance criteria

**Solutions:**
- Implement Definition of Ready checklist
- Hold backlog refinement sessions mid-sprint
- PO spends more time on upcoming stories
- Block stories from sprint if not ready

### Challenge 3: Planning Takes Too Long
**Symptom:** Sprint planning consistently runs over 4 hours

**Solutions:**
- Pre-refine stories (don't do refinement in planning)
- Limit attendees (core team only)
- Use timebox techniques (5 min per story)
- Park detailed technical discussions for Part 2
- Improve facilitation (keep on track)

### Challenge 4: Sprint Goal Unclear
**Symptom:** Team doesn't understand what they're working toward

**Solutions:**
- PO proposes specific goal upfront
- Connect goal to customer value/outcome
- Limit goal to 1-2 sentences
- Test: Can anyone recite goal from memory?

### Challenge 5: Team Can't Estimate Accurately
**Symptom:** Estimates consistently off (2x or 0.5x actual)

**Solutions:**
- Use planning poker (avoid anchoring bias)
- Estimate relative to reference stories
- Break stories smaller (reduce uncertainty)
- Track actuals vs estimates, refine process
- Allow team to challenge PO requirements

## Sprint Planning Best Practices

### Before Sprint Planning
1. **Refine backlog continuously** - Don't wait until planning
2. **Involve the whole team** - Diverse perspectives improve estimates
3. **Prepare sprint goal candidate** - PO comes with proposed goal
4. **Calculate capacity realistically** - Factor in all constraints

### During Sprint Planning
1. **Start on time** - Respect everyone's calendar
2. **Focus on value** - Prioritize customer-facing work
3. **Ask questions early** - Clarify before committing
4. **Break large stories** - 8+ points too big for sprint
5. **Document decisions** - Record sprint goal, commitments, risks

### After Sprint Planning
1. **Update sprint board** - Jira/Linear reflects all stories and tasks
2. **Communicate dependencies** - Alert other teams ASAP
3. **Kick off work immediately** - Don't wait until next day
4. **Hold daily standups** - Track progress against plan

## Tools & Templates

### Sprint Planning Artifacts

**Sprint Goal Template:**
```
Sprint Goal: [One sentence describing the outcome]

Why: [Business value or customer benefit]

Success Criteria:
- [Metric or outcome 1]
- [Metric or outcome 2]

Stories in Scope:
- [Story 1 - X points]
- [Story 2 - Y points]
Total: Z points

Risks:
- [Risk 1 - mitigation plan]
- [Risk 2 - mitigation plan]
```

**Sprint Planning Notes Template:**
```
Sprint: [Number/Date Range]
Participants: [Names]
Capacity: [X points / Y hours]
Velocity (avg): [Z points]

Sprint Goal: [Goal statement]

Committed Stories:
□ Story 1 (X points) - [Brief description]
□ Story 2 (Y points) - [Brief description]
...

Risks & Dependencies:
- [Risk 1]
- [Dependency 1 - owner, deadline]

Decisions Made:
- [Decision 1]
- [Decision 2]
```

## Resources
- Sprint planning facilitation guide
- Capacity planning spreadsheet
- Story point reference guide
- Definition of Ready checklist

---
**Last Updated:** November 23, 2025
**Related:** agile_story_framework.md, frameworks.md
