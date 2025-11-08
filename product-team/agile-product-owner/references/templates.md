# Agile Templates and Examples

Practical templates for user stories, epics, and agile ceremonies.

## User Story Templates

### Standard User Story Format

```markdown
# US-[ID]: [Short Title]

**As a** [user type/persona]
**I want to** [action/capability]
**So that** [business value/benefit]

## Acceptance Criteria

**Given** [precondition/context]
**When** [action taken]
**Then** [expected outcome]

**Given** [alternative precondition]
**When** [action taken]
**Then** [expected outcome]

## Additional Details

**Priority:** High | Medium | Low
**Story Points:** [1, 2, 3, 5, 8, 13, 21]
**Sprint:** Sprint [number]
**Epic:** [Epic name and link]
**Dependencies:** [List of blocking stories]

## Definition of Done

- [ ] Code complete and peer reviewed
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests pass
- [ ] Acceptance criteria verified
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Product Owner approved
```

### Feature User Story Example

```markdown
# US-047: Dashboard Date Filter

**As a** sales manager
**I want to** filter my dashboard by custom date ranges
**So that** I can analyze performance for specific time periods

## Acceptance Criteria

**Given** I am viewing my sales dashboard
**When** I select a start and end date from the date picker
**Then** the dashboard updates to show only data within that range
**And** the URL includes the selected date range
**And** the selection persists when I refresh the page

**Given** I select an invalid date range (end before start)
**When** I attempt to apply the filter
**Then** I see an error message: "End date must be after start date"
**And** the filter is not applied

**Given** I have applied a date filter
**When** I click "Clear Filters"
**Then** the dashboard returns to showing all available data

## Additional Details

**Priority:** High
**Story Points:** 5
**Sprint:** Sprint 24
**Epic:** [EPIC-012: Dashboard Customization](link-to-epic)
**Dependencies:** US-042 (Dashboard API must support date filtering)

## Technical Notes

- Use existing DatePicker component from design system
- Backend API already supports date range parameters
- Cache filtered results for 5 minutes

## Definition of Done

- [ ] Code complete and peer reviewed
- [ ] Unit tests for date validation logic
- [ ] Integration test for API date filtering
- [ ] Browser tested (Chrome, Firefox, Safari)
- [ ] Mobile responsive verified
- [ ] Accessibility: keyboard navigation works
- [ ] Documentation: API parameters documented
- [ ] Product Owner demo and approval
```

### Technical User Story (Enabler)

```markdown
# US-089: Implement Caching Layer

**As a** development team
**We need to** implement Redis caching for dashboard queries
**So that** users experience faster load times (<2 seconds)

## Acceptance Criteria

**Given** a dashboard query is executed
**When** the data is fetched from the database
**Then** the result is cached in Redis with 5-minute TTL
**And** subsequent identical queries return cached data

**Given** cached data exists for a query
**When** the cache TTL expires or data is invalidated
**Then** the next query fetches fresh data from the database
**And** updates the cache

**Given** the Redis cache is unavailable
**When** a query is executed
**Then** the system falls back to direct database queries
**And** logs a warning about cache unavailability

## Additional Details

**Priority:** High
**Story Points:** 8
**Sprint:** Sprint 23
**Epic:** EPIC-015: Performance Optimization
**Dependencies:** None

## Technical Notes

- Use Redis 6.x with cluster support
- Implement cache-aside pattern
- Add monitoring for cache hit rate
- Set up alerts for cache failures

## Definition of Done

- [ ] Redis cluster configured and deployed
- [ ] Caching implemented for top 5 query types
- [ ] Cache hit rate >70% in staging tests
- [ ] Fallback to database tested
- [ ] Performance benchmarks show <2s load times
- [ ] Monitoring dashboard created
- [ ] Runbook updated for cache failures
```

### Bug Fix User Story

```markdown
# US-102: Fix Dashboard Export Timeout

**As a** user
**I expect** dashboard exports to complete successfully
**When** I export large datasets (>10,000 rows)

## Current Behavior

- Export times out after 30 seconds for datasets >10,000 rows
- User sees "Request Timeout" error
- No indication of progress
- Exported file is not generated

## Expected Behavior

- Exports complete within 2 minutes for datasets up to 50,000 rows
- User sees progress indicator during export
- If export takes >5 seconds, process asynchronously
- User receives email notification when export is ready
- Download link available for 24 hours

## Acceptance Criteria

**Given** I request an export of >10,000 rows
**When** the export is processing
**Then** I see a progress bar with estimated time
**And** I receive an email when the export completes
**And** I can download the file from the provided link

**Given** the export fails
**When** an error occurs during processing
**Then** I see a clear error message explaining what went wrong
**And** I receive guidance on how to reduce the dataset size

## Additional Details

**Priority:** Critical
**Story Points:** 5
**Sprint:** Sprint 25
**Severity:** High (impacts 20% of users daily)
**Steps to Reproduce:**
1. Open dashboard with 15,000+ rows
2. Click "Export to CSV"
3. Wait 30 seconds
4. Observe timeout error

## Technical Notes

- Increase server timeout from 30s to 120s
- Implement async export queue (Celery/RabbitMQ)
- Add export progress tracking
- Store exports in S3 with signed URLs

## Definition of Done

- [ ] Exports of 50,000 rows complete successfully
- [ ] Progress indicators working
- [ ] Email notifications sent
- [ ] Async queue configured and monitored
- [ ] Load tested with 100 concurrent exports
- [ ] User documentation updated
- [ ] Support team notified of fix
```

## Epic Templates

### Epic Template

```markdown
# EPIC-[ID]: [Epic Name]

## Epic Goal

[One-sentence description of what this epic achieves]

## Business Value

**Problem:** [What problem are we solving?]
**Opportunity:** [What's the business opportunity?]
**Impact:** [Expected business outcomes]

**Success Metrics:**
- Metric 1: [Baseline] → [Target]
- Metric 2: [Baseline] → [Target]
- Metric 3: [Baseline] → [Target]

## User Segments

- **Primary:** [Primary users who benefit]
- **Secondary:** [Secondary beneficiaries]
- **Admin/Internal:** [Internal users if applicable]

## Scope

### In Scope
- Feature/capability 1
- Feature/capability 2
- Feature/capability 3

### Out of Scope (This Release)
- Feature X: [Reason for exclusion, future plans]
- Feature Y: [Reason for exclusion, future plans]

## User Stories

**Total Story Points:** [Sum of all story estimates]
**Target Sprint:** Sprint [start] - Sprint [end]

### Core Stories (MVP)
- [ ] US-001: [Story title] (8 pts)
- [ ] US-002: [Story title] (5 pts)
- [ ] US-003: [Story title] (3 pts)

### Enhancement Stories (Post-MVP)
- [ ] US-010: [Story title] (5 pts)
- [ ] US-011: [Story title] (3 pts)

### Technical Enablers
- [ ] US-020: [Technical requirement] (8 pts)
- [ ] US-021: [Technical requirement] (5 pts)

## Dependencies

**Blocking:**
- Dependency 1: [Description, owner, status]
- Dependency 2: [Description, owner, status]

**Blocked By:**
- None / [List items waiting on this epic]

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|---------|------------|
| Risk 1 | High/Med/Low | High/Med/Low | [Mitigation plan] |
| Risk 2 | High/Med/Low | High/Med/Low | [Mitigation plan] |

## Design & UX

**Designs:** [Link to Figma/design tool]
**User Flows:** [Link to flow diagrams]
**Research:** [Link to user research findings]

## Technical Architecture

**High-Level Approach:** [Brief technical overview]
**Key Components:** [List of systems/services affected]
**API Changes:** [New or modified APIs]
**Data Model:** [Database schema changes]

## Launch Plan

**Beta Testing:** [Plan for beta/early access]
**Rollout Strategy:** [Gradual, feature-flagged, etc.]
**Monitoring:** [Key metrics to watch post-launch]
**Rollback Plan:** [How to roll back if issues arise]

## Timeline

| Phase | Duration | Stories | Target Date |
|-------|----------|---------|-------------|
| Discovery | 1 sprint | Research, spikes | [Date] |
| MVP Development | 3 sprints | US-001 to US-005 | [Date] |
| Beta Testing | 1 sprint | Feedback iteration | [Date] |
| Enhancements | 2 sprints | US-010 to US-015 | [Date] |
| Launch | 1 sprint | Rollout, monitoring | [Date] |

## Stakeholders

- **Product Owner:** [Name]
- **Engineering Lead:** [Name]
- **Design Lead:** [Name]
- **Stakeholders:** [Names of key stakeholders]

## Success Criteria

- [ ] All MVP stories completed
- [ ] Success metrics hit targets
- [ ] User satisfaction score >4.0/5
- [ ] No critical bugs in production
- [ ] Documentation complete
- [ ] Stakeholder approval received
```

### Epic Example: Dashboard Customization

```markdown
# EPIC-012: Dashboard Customization

## Epic Goal

Enable users to customize their dashboard layout and widget selection to focus on metrics that matter most to them.

## Business Value

**Problem:** Users are overwhelmed by default dashboard with 15+ widgets. Analytics show 60% of users only use 3-5 widgets regularly. Support tickets cite "too cluttered" and "can't find what I need."

**Opportunity:** Increase dashboard engagement from 3x/week to daily use by showing only relevant data.

**Impact:**
- Increase daily active users by 25%
- Reduce support tickets about "missing features" by 40%
- Improve user satisfaction (NPS) from 35 to 45

**Success Metrics:**
- Dashboard views per user: 3/week → 5/week
- Time spent on dashboard: 2 min → 4 min
- Customization adoption: 0% → 60% of users
- NPS score: 35 → 45

## User Segments

- **Primary:** Sales managers (200 users) - need sales-specific KPIs
- **Secondary:** Customer success teams (150 users) - need customer health metrics
- **Admin/Internal:** Admins can create default layouts per role

## Scope

### In Scope
- Drag-and-drop widget repositioning
- Show/hide individual widgets
- Widget resize (small, medium, large)
- Save custom layouts per user
- Reset to default layout option
- Role-based default layouts (admin feature)

### Out of Scope (This Release)
- Custom widget creation: Too complex for V1, planned for Q2
- Dashboard sharing: Security concerns to address first
- Mobile layout customization: Mobile redesign planned separately

## User Stories

**Total Story Points:** 47
**Target Sprint:** Sprint 24-27 (8 weeks)

### Core Stories (MVP)
- [ ] US-047: Filter dashboard by date range (5 pts)
- [ ] US-048: Drag and drop widgets (8 pts)
- [ ] US-049: Show/hide widgets (3 pts)
- [ ] US-050: Save custom layout (5 pts)
- [ ] US-051: Reset to default layout (2 pts)

### Enhancement Stories (Post-MVP)
- [ ] US-052: Resize widgets (5 pts)
- [ ] US-053: Role-based default layouts (8 pts)
- [ ] US-054: Export custom layout (3 pts)

### Technical Enablers
- [ ] US-055: Implement drag-drop library (5 pts)
- [ ] US-056: User preferences API (3 pts)

## Dependencies

**Blocking:**
- Dashboard API refactor (EPIC-010) - IN PROGRESS, Sprint 23
- Design system grid component - COMPLETE

**Blocked By:**
- Mobile dashboard redesign (planned Q2) - waiting on this epic's learnings

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|---------|------------|
| Performance degradation with custom layouts | Medium | High | Load test with 50+ widgets, implement lazy loading |
| Users break layout and can't recover | High | Medium | Prominent "Reset" button, save layout history |
| Low adoption of customization | Medium | High | Onboarding tutorial, default suggestions based on role |

## Design & UX

**Designs:** [figma.com/dashboard-customization](#)
**User Flows:** [miro.com/user-flows](#)
**Research:** 12 user interviews conducted, 85% want customization

**Key Design Decisions:**
- Grid-based layout (not freeform) for consistency
- 12-column responsive grid
- Widget sizes: 1/4, 1/3, 1/2, 2/3, full-width
- "Customize" mode separate from viewing mode

## Technical Architecture

**High-Level Approach:**
- React DnD for drag-and-drop
- User preferences stored in PostgreSQL (JSON column)
- Real-time layout save (debounced)
- Client-side layout engine for performance

**Key Components:**
- Frontend: Dashboard layout engine (new)
- Backend: User preferences service (new endpoint)
- Database: user_preferences table (new)

**API Changes:**
```
POST /api/users/preferences/dashboard
GET  /api/users/preferences/dashboard
PUT  /api/users/preferences/dashboard
DELETE /api/users/preferences/dashboard
```

**Data Model:**
```json
{
  "user_id": "uuid",
  "layout": {
    "widgets": [
      {"id": "revenue", "position": {"x": 0, "y": 0}, "size": "large"},
      {"id": "deals", "position": {"x": 4, "y": 0}, "size": "medium"}
    ],
    "hidden": ["activity_feed", "calendar"]
  },
  "updated_at": "timestamp"
}
```

## Launch Plan

**Beta Testing:**
- Week 1: Internal team (10 users)
- Week 2: Power users cohort (50 users)
- Week 3: Early access program (200 users)

**Rollout Strategy:**
- Feature flag: gradual rollout 10% → 50% → 100%
- A/B test: 50% get customization, 50% control
- Monitor: engagement, errors, support tickets

**Monitoring:**
- Customization adoption rate
- Layout save frequency
- Error rate (drag-drop failures)
- Performance: dashboard load time

**Rollback Plan:**
- Feature flag disable (instant)
- Revert to default layouts
- Preserve saved layouts in database for re-enable

## Timeline

| Phase | Duration | Stories | Target Date |
|-------|----------|---------|-------------|
| Discovery | Complete | Research done | Feb 1 |
| MVP Development | 3 sprints | US-047 to US-051 | Mar 15 |
| Beta Testing | 3 weeks | Feedback iteration | Apr 5 |
| Enhancements | 2 sprints | US-052 to US-054 | May 10 |
| Launch | 2 weeks | Rollout, monitoring | May 24 |

## Stakeholders

- **Product Owner:** Sarah Chen
- **Engineering Lead:** Mike Rodriguez
- **Design Lead:** Alex Kim
- **Stakeholders:** VP Product, Head of Sales, Head of CS

## Success Criteria

- [ ] All MVP stories completed and tested
- [ ] Dashboard views per user increases to 5/week
- [ ] 60% of users customize their layout
- [ ] No P0/P1 bugs in production
- [ ] User satisfaction score >4.0/5 in post-launch survey
- [ ] Stakeholder demo completed and approved
```

## Sprint Ceremony Templates

### Sprint Planning Agenda

```markdown
# Sprint [Number] Planning

**Date:** [Date]
**Sprint Duration:** [Dates]
**Participants:** Product Owner, Scrum Master, Development Team

## Part 1: What Will We Build? (2 hours)

### Sprint Goal (15 min)
**Goal:** [One sentence describing the sprint objective]

**Why this goal?**
- Aligns with Q[X] OKR: [OKR description]
- Addresses user feedback from [source]
- Unblocks [downstream dependency]

### Team Capacity (10 min)
**Team Members:** [Count]
**Sprint Days:** [Number of working days]
**PTO/Holidays:** [List any time off]
**Available Capacity:** [Story points or hours]

**Capacity Calculation:**
```
Base capacity: [team size] × [sprint days] × [hours/day] = [total hours]
Adjusted for:
- Meetings/ceremonies: -[hours]
- Support rotation: -[hours]
- PTO: -[hours]
= [net capacity] hours ≈ [story points]
```

### Backlog Review (30 min)
**Top Priorities:**
1. [Story 1] - [Priority] - [Points]
2. [Story 2] - [Priority] - [Points]
3. [Story 3] - [Priority] - [Points]

**Team Questions:**
- [Question about story 1]
- [Question about story 2]

### Story Selection (45 min)
**Committed Stories:**
- [ ] US-XXX: [Title] ([points])
- [ ] US-XXX: [Title] ([points])
- [ ] US-XXX: [Title] ([points])

**Total Committed:** [X] points

**Stretch Goals:**
- [ ] US-XXX: [Title] ([points])

### Risks & Dependencies (20 min)
**Risks:**
- Risk 1: [Description, likelihood, mitigation]
- Risk 2: [Description, likelihood, mitigation]

**Dependencies:**
- Dependency 1: [What we need, from who, when]
- Dependency 2: [What we need, from who, when]

## Part 2: How Will We Build It? (2 hours)

### Task Breakdown (90 min)

**US-XXX: [Story Title]**
- [ ] Task 1: [Description] ([hours], [owner])
- [ ] Task 2: [Description] ([hours], [owner])
- [ ] Task 3: [Description] ([hours], [owner])

**US-XXX: [Story Title]**
- [ ] Task 1: [Description] ([hours], [owner])
- [ ] Task 2: [Description] ([hours], [owner])

### Technical Dependencies (15 min)
- [List technical dependencies identified during task breakdown]

### Sprint Commitment (15 min)
**Team commits to:**
- Deliver [X] story points
- Achieve sprint goal: [Goal statement]
- Daily standups at [time]
- Mid-sprint refinement on [day]
```

### Sprint Review Agenda

```markdown
# Sprint [Number] Review

**Date:** [Date]
**Attendees:** Product Owner, Scrum Master, Development Team, Stakeholders

## Sprint Summary (5 min)

**Sprint Goal:** [Goal from planning]
**Outcome:** [Achieved / Partially Achieved / Not Achieved]

**Velocity:**
- Committed: [X] points
- Completed: [Y] points
- Velocity: [Y] points

## Demo (40 min)

### Story 1: [Title]
**Demo:** [Show working software]
**Value:** [What problem does this solve?]
**Feedback:** [Stakeholder questions/comments]

### Story 2: [Title]
**Demo:** [Show working software]
**Value:** [What problem does this solve?]
**Feedback:** [Stakeholder questions/comments]

### Story 3: [Title]
**Demo:** [Show working software]
**Value:** [What problem does this solve?]
**Feedback:** [Stakeholder questions/comments]

## Incomplete Work (5 min)
- [Story X: Reason not completed, plan to finish]
- [Story Y: Reason not completed, plan to finish]

## Metrics Review (5 min)

**Burndown:**
[Attach burndown chart image or describe trend]

**Impediments:**
- [List major blockers encountered]

## Next Sprint Preview (5 min)
**Upcoming Work:**
- [Preview top priorities for next sprint]
- [Any major changes to roadmap]
```

### Sprint Retrospective Agenda

```markdown
# Sprint [Number] Retrospective

**Date:** [Date]
**Format:** [Start-Stop-Continue / 4Ls / Sailboat / Other]

## Set the Stage (5 min)
- Reminder: Safe space, focus on improvement not blame
- Reminder: One conversation at a time
- Check-in: One-word mood check

## Gather Data (20 min)

### What went well? ✅
- [Item 1]
- [Item 2]
- [Item 3]

### What didn't go well? ⚠️
- [Item 1]
- [Item 2]
- [Item 3]

### What should we try? 💡
- [Idea 1]
- [Idea 2]
- [Idea 3]

## Generate Insights (20 min)

**Themes:**
- Theme 1: [Pattern across multiple items]
- Theme 2: [Pattern across multiple items]

**Root Cause Analysis:**
- Issue: [Top issue]
  - Why? [First why]
    - Why? [Second why]
      - Why? [Root cause]

## Decide What To Do (10 min)

**Action Items:**
1. [Action 1]
   - Owner: [Name]
   - Due: [Date]
   - Success metric: [How we'll know it worked]

2. [Action 2]
   - Owner: [Name]
   - Due: [Date]
   - Success metric: [How we'll know it worked]

## Close (5 min)
- Review action items
- Assign action item owner to share with team
- Schedule follow-up check-in

## Previous Action Items Review
- [Previous action 1]: [Status: Done / In Progress / Blocked]
- [Previous action 2]: [Status: Done / In Progress / Blocked]
```

## Best Practices

### Writing Effective User Stories

**DO:**
- Focus on user value, not implementation
- Include clear acceptance criteria
- Keep stories small (completable in <1 week)
- Write from user perspective
- Define "done" upfront

**DON'T:**
- Write technical tasks as user stories
- Make stories too large (>8 points)
- Omit acceptance criteria
- Be vague about success criteria
- Skip the "so that" clause (the why)

### Story Splitting Techniques

**By Workflow:**
```
Original: As a user, I want to manage my profile
Split:
- US-001: View my profile
- US-002: Edit my profile
- US-003: Change my password
- US-004: Upload profile picture
```

**By Business Rules:**
```
Original: As a user, I want to search products
Split:
- US-010: Search by keyword
- US-011: Filter by category
- US-012: Sort results
- US-013: Save search
```

**By Data Entry Methods:**
```
Original: As a user, I want to create a record
Split:
- US-020: Create record manually
- US-021: Import records from CSV
- US-022: Create via API
```

**By Happy/Unhappy Path:**
```
Original: As a user, I want to reset my password
Split:
- US-030: Reset password (happy path)
- US-031: Handle invalid email
- US-032: Handle expired reset link
```

---

**Last Updated:** 2025-11-08
**Related Files:**
- [frameworks.md](frameworks.md) - INVEST criteria, sprint planning, velocity tracking
- [tools.md](tools.md) - user_story_generator.py documentation
