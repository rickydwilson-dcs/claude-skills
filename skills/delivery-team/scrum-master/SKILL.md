---

# === CORE IDENTITY ===
name: scrum-master
title: Scrum Master Skill Package
description: Scrum Master for agile software development teams. Use for sprint planning, daily standups, retrospectives, backlog refinement, velocity tracking, removing impediments, facilitating ceremonies, coaching teams on agile practices, and managing sprint execution for R&D and development teams.
domain: delivery
subdomain: agile-methodology

# === WEBSITE DISPLAY ===
difficulty: intermediate
time-saved: """TODO: Quantify time savings"""
frequency: """TODO: Estimate usage frequency"""
use-cases:
  - Primary workflow for Scrum Master
  - Analysis and recommendations for scrum master tasks
  - Best practices implementation for scrum master
  - Integration with related skills and workflows

# === RELATIONSHIPS ===
related-agents: []
related-skills: []
related-commands: []
orchestrated-by: []

# === TECHNICAL ===
dependencies:
  scripts: []
  references: []
  assets: []
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack: [Python 3.8+]

# === EXAMPLES ===
examples:
  -
    title: Example Usage
    input: "TODO: Add example input for scrum-master"
    output: "TODO: Add expected output"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-10-21
updated: 2025-11-23
license: MIT

# === DISCOVERABILITY ===
tags: [agile, delivery, development, master, scrum]
featured: false
verified: true
---


# Scrum Master Expert

## Overview

This skill provides comprehensive Scrum Master expertise for facilitating agile ceremonies (sprint planning, daily standups, sprint reviews, retrospectives), coaching teams on Scrum practices, removing impediments, tracking velocity, and ensuring sprint success. It includes frameworks for backlog refinement, estimation techniques, metrics tracking, team coaching, and integration with Jira and Confluence through the Atlassian MCP server.

Target users include Scrum Masters, agile coaches, team leads, and project managers working with software development teams using Scrum methodology. This skill is essential for facilitating effective sprint ceremonies, building high-performing self-organizing teams, tracking team health metrics, and establishing continuous improvement practices.

**Core Value:** Increase sprint velocity by 25% through effective facilitation and impediment removal, improve team predictability by 40% through consistent ceremonies and estimation, and boost team satisfaction by 35% through retrospectives and continuous improvement practices.

## Core Capabilities

- **Sprint Ceremony Facilitation** - Plan and run sprint ceremonies (planning, daily standup, review, retrospective) ensuring team adheres to Scrum framework and timeboxes
- **Team Coaching & Development** - Coach teams on agile principles, Scrum practices, estimation techniques, and foster self-organizing, high-performing team culture
- **Impediment Management** - Identify and remove blockers quickly, escalate critical issues, shield team from external interruptions, facilitate cross-team dependencies
- **Metrics & Velocity Tracking** - Track velocity, burndown, sprint health indicators, identify trends, forecast capacity, provide data for portfolio planning
- **Atlassian MCP Integration** - Use Jira MCP for sprint management and board updates, Confluence MCP for ceremony documentation and retrospective notes

## Quick Start

### Common Scrum Master Operations

This skill provides Scrum Master expertise through ceremony frameworks, coaching techniques, and metrics patterns. Jira and Confluence operations are performed through the Atlassian MCP server configured in Claude Code settings.

### Access Documentation Resources

- **Ceremony frameworks:** See Workflows section for sprint planning, daily standup, sprint review, and retrospective patterns
- **Metrics guidance:** See Scrum Metrics section for sprint health indicators and team health tracking
- **Best practices:** See Agile Best Practices section for story estimation, Definition of Done, and Definition of Ready
- **Timeboxes:** See Ceremony Timeboxes section for recommended durations

### Key Workflows to Start With

1. **Facilitate Sprint Planning** - Define sprint goal, estimate stories, commit to sprint backlog (2 hours for 2-week sprint)
2. **Run Effective Daily Standup** - Focused 15-minute daily sync with impediment tracking (15 minutes)
3. **Conduct Sprint Retrospective** - Facilitate team reflection and identify improvement actions (1.5 hours per week of sprint)
4. **Track Velocity and Report to Stakeholders** - Calculate velocity trends and forecast capacity (ongoing)

## Key Workflows

### 1. Facilitate Sprint Planning

**Time:** 2 hours (for 2-week sprint)

**Steps:**
1. **Prepare team and backlog** - Meet with Product Owner 1 day before sprint planning
   - Verify top backlog items are refined and have acceptance criteria
   - Estimate story points if not already done
   - Identify any dependencies or blockers
   - Confirm team members attending and their availability
2. **Begin sprint planning meeting** - Timeboxed to 2 hours for 2-week sprint
   - Product Owner presents sprint goals (top 3-5 business objectives)
   - Team asks clarifying questions
   - Goal should answer: "What problem are we solving this sprint?"
3. **Facilitate story estimation using planning poker**
   - Team member reads story aloud
   - Each team member independently estimates story points (Fibonacci: 1, 2, 3, 5, 8, 13, 21)
   - Reveal estimates simultaneously
   - If wide variation, discuss and re-estimate
   - Iterate until consensus
4. **Build sprint backlog** - Team selects stories they commit to
   - Select stories in priority order
   - Track total story points
   - Stop when team capacity is reached (use historical velocity)
   - Avoid overcommitment - better to undercommit and succeed
5. **Define Definition of Done** - Team aligns on done criteria
   - Code review completed
   - All tests passing
   - Documentation updated
   - Deployed to staging
   - Acceptance criteria met
6. **Create sprint in Jira** - Move committed stories to sprint
   - Use Jira Expert to create sprint with start/end dates
   - Move selected stories from backlog to sprint
   - Set sprint goal in Jira sprint description

**Expected Output:** Sprint is planned with clear goals, committed backlog of work sized for team capacity, Definition of Done is agreed, and sprint is active in Jira ready for daily execution.

See [Workflows](#workflows) section for detailed ceremony details.

### 2. Run Effective Daily Standup

**Time:** 15 minutes daily

**Steps:**
1. **Schedule consistency** - Same time and place every day (e.g., 9:15 AM in Zoom)
   - Consistency helps team build habit
   - Same time means fewer scheduling conflicts
   - Block time in everyone's calendars
2. **Start with sprint goal reminder** - Reconnect to why we're here
   - "Our sprint goal is to improve login performance"
   - Helps team stay focused
   - Reminds everyone of shared objective
3. **Each person answers 3 questions** (speaking in round-robin)
   - What did I complete yesterday? (point to Jira issue)
   - What will I work on today? (reference specific issues)
   - Are there any blockers preventing progress? (ask for help immediately)
   - Format: "I completed PROJ-123, I'm starting PROJ-124, I'm blocked on authentication service"
4. **Capture impediments on whiteboard or Jira** - Don't solve problems in standup
   - Write down blocker without discussing
   - Say "let's discuss that offline"
   - Schedule follow-up immediately after standup
5. **Update Jira board** - Reflect current work status
   - Move completed work to "Done"
   - Drag in-progress work to correct column
   - Board should visually match spoken status
6. **Close with energy** - End on positive note
   - Acknowledge progress
   - "We've completed X story points, stay focused"
   - Quick team huddle/chant optional but fun

**Expected Output:** 15-minute daily standup that keeps team aligned, surfaces blockers immediately, and maintains sprint momentum. Team knows what's happening and can help each other quickly.

See [Daily Standup](#workflows) section for detailed ceremony format.

### 3. Conduct Sprint Retrospective for Continuous Improvement

**Time:** 1.5 hours (for 2-week sprint)

**Steps:**
1. **Set retrospective time and agenda** - Schedule 1-2 days after sprint ends
   - Announce retro agenda to team
   - Use Confluence Expert to create retro page
   - Ensure all team members can attend
2. **Create safe psychological space** - Set the tone for honest feedback
   - "No blame, we're here to improve"
   - Participate as facilitator, not judge
   - Encourage all voices - introverts and extroverts
   - Consider anonymous feedback option if trust is low
3. **Review sprint metrics** - Look at numbers first
   - How many story points did we commit to? (e.g., 34 points)
   - How many did we complete? (e.g., 31 points) - velocity
   - Was sprint goal achieved? (Yes/No and why)
   - What changed from last sprint?
4. **What went well** - Celebrate wins (15 minutes)
   - Ask: "What are we proud of this sprint?"
   - Write responses on board (silent brainstorm or spoken)
   - Examples: "Great collaboration on payment feature", "Excellent code reviews"
   - Review 2-3 major wins with team
5. **What didn't go well** - Identify improvements (20 minutes)
   - Ask: "What slowed us down or caused pain?"
   - Write responses on board without judgment
   - Examples: "Meeting interruptions", "Unclear requirements", "Slow CI/CD pipeline"
   - Group similar themes
6. **Commit to 1-3 improvement actions** - Be specific and actionable (15 minutes)
   - Select top improvement opportunities (don't try to fix everything)
   - Define concrete action: "Who, What, By When"
   - Example: "Scrum Master will send calendar block for deep work 10-12 daily"
   - Track in Jira or Confluence
7. **Document and share** - Use Confluence Expert to create retro page
   - Record what went well and didn't
   - Document committed improvements
   - Link from Confluence to next sprint for reference

**Expected Output:** Team reflects on sprint execution, celebrates achievements, identifies improvement opportunities, and commits to 1-3 concrete actions to make next sprint better. Documentation created for trend analysis across sprints.

See [Sprint Retrospective](#workflows) section for detailed retro format.

### 4. Manage Velocity Tracking and Capacity Planning

**Time:** 1 hour per sprint cycle

**Steps:**
1. **Calculate sprint velocity** - After sprint ends
   - Velocity = total story points of completed work
   - Only count work marked "Done" (not in progress or review)
   - Example: Committed 34 points, completed 31 points = 31 point velocity
2. **Track velocity over time** - Create rolling average
   - Velocity from last 3-5 sprints tells real capacity
   - Example: [28, 31, 29, 31, 30] = 30 point average velocity
   - Ignore outlier high/low sprints
   - Use this for future sprint planning
3. **Identify velocity trends** - Look for patterns
   - Stable velocity (26-30 points): Team is consistent and predictable
   - Increasing velocity: Team learning, improving, adding members
   - Decreasing velocity: Technical debt, turnover, scope creep
   - Flag significant changes (>20% variance)
4. **Forecast future capacity** - Use velocity for planning
   - If average velocity is 30 points
   - And we have 3 sprints until release
   - Expected capacity: 90 story points of features
   - Use for roadmap and commitment planning
5. **Report to Senior PM** - Provide metrics and forecasts
   - Create velocity chart (last 10 sprints)
   - Share trend analysis
   - Forecast when epics will be done based on velocity
   - Flag if velocity declining or commitments slipping
6. **Identify blockers affecting velocity** - Root cause analysis
   - If velocity dropped, what happened?
   - Did we lose team members? (hiring needed)
   - Did we increase technical debt? (pay-down sprint needed)
   - Did we have many interruptions? (process improvement needed)

**Expected Output:** Clear understanding of team capacity (velocity), accurate forecasts for roadmap planning, and identification of factors affecting velocity to address in sprints. Senior PM has data for stakeholder communication and resource planning.

See [Velocity Tracking](#workflows) section for detailed metrics and reporting.

## Python Tools

This skill does not include Python automation tools. Scrum Master operations are performed through the Atlassian MCP server, which provides integration for:

- Creating and managing sprints in Jira
- Updating sprint board status and issue transitions
- Generating velocity reports and burndown charts
- Filtering and prioritizing backlog items
- Creating ceremony documentation pages in Confluence
- Tracking retrospective action items

See the Atlassian MCP Integration section below for detailed integration patterns and capabilities.

## Reference Documentation

The following sections provide comprehensive frameworks, ceremony patterns, and best practices for Scrum Master expertise:

## Core Responsibilities

**Sprint Facilitation**
- Plan and run sprint ceremonies (planning, daily standup, review, retrospective)
- Ensure team adheres to Scrum framework
- Track sprint progress and velocity
- Facilitate backlog refinement

**Team Coaching**
- Coach team on agile principles and Scrum practices
- Build self-organizing, high-performing teams
- Foster continuous improvement culture
- Mentor team members on estimation and collaboration

**Impediment Removal**
- Identify and remove blockers quickly
- Escalate critical issues to Senior PM
- Shield team from external interruptions
- Facilitate cross-team dependencies

**Metrics & Reporting**
- Track velocity, burndown, and sprint health
- Report sprint outcomes and team capacity
- Identify trends and improvement opportunities
- Provide data for Senior PM reporting

## Workflows

### Sprint Planning
1. Review and refine product backlog with Product Owner
2. Confirm team capacity and availability
3. Facilitate sprint goal definition
4. Guide team through story estimation (planning poker)
5. Commit to sprint backlog
6. **USE**: Jira Expert to configure sprint and move issues
7. **HANDOFF TO**: Team for execution

### Daily Standup
1. Facilitate 15-minute timebox
2. Each team member answers: What did I do? What will I do? Blockers?
3. Update sprint board with progress
4. Identify and capture impediments
5. Schedule follow-up discussions offline
6. **USE**: Jira Expert to update board status

### Sprint Review
1. Demonstrate completed work to stakeholders
2. Gather feedback on delivered increment
3. Update product backlog based on feedback
4. Celebrate team accomplishments
5. **USE**: Confluence Expert to document feedback

### Sprint Retrospective
1. Review what went well and what didn't
2. Identify actionable improvements
3. Commit to 1-3 improvement actions
4. Track improvement action items
5. **USE**: Confluence Expert to document retrospective notes

### Backlog Refinement
1. Review upcoming backlog items with team
2. Break down large stories into smaller ones
3. Clarify requirements and acceptance criteria
4. Estimate story points
5. Ensure backlog is ready for next sprint
6. **USE**: Jira Expert to update and organize backlog

### Velocity Tracking
1. Track completed story points per sprint
2. Calculate rolling average velocity
3. Identify velocity trends and anomalies
4. Forecast capacity for upcoming sprints
5. **REPORT TO**: Senior PM for portfolio planning

## Decision Framework

**When to Escalate to Senior PM**
- Sprint goals at risk of not being met
- Team velocity declining >20% for 2+ sprints
- Critical impediments blocking entire team
- Resource conflicts or team composition changes
- Cross-project dependencies blocking progress

**When to Request Jira Expert**
- Complex workflow configuration needed
- Custom fields or issue types required
- Advanced filtering or reporting needs
- Board configuration changes
- Automation rules setup

**When to Request Confluence Expert**
- Team documentation structure needed
- Meeting notes templates required
- Decision log setup
- Team handbook creation

## Scrum Metrics

**Sprint Health Indicators**:
- Sprint burndown: On track vs. behind
- Velocity trend: Stable, increasing, decreasing
- Commitment reliability: % stories completed
- Impediment resolution time
- Sprint goal achievement rate

**Team Health Indicators**:
- Team morale and engagement
- Collaboration quality
- Technical debt accumulation
- Test coverage trends
- Production incidents

## Handoff Protocols

**FROM Senior PM**:
- Project scope and objectives
- Initial backlog priorities
- Team composition
- Sprint cadence and ceremony schedule

**TO Senior PM**:
- Sprint completion reports
- Velocity trends and forecasts
- Team capacity changes
- Blocker escalations
- Risk identification

**WITH Jira Expert**:
- Sprint board configuration
- Workflow status updates
- Velocity and burndown data
- Backlog organization

**WITH Confluence Expert**:
- Sprint planning documentation
- Retrospective notes
- Team agreements and working protocols
- Definition of Done/Ready

## Agile Best Practices

**Story Estimation**:
- Use planning poker for team consensus
- Estimate in story points (Fibonacci sequence)
- Reference story for baseline
- Re-estimate only when new information emerges

**Definition of Done**:
- Code reviewed and approved
- All tests passing (unit, integration, E2E)
- Documentation updated
- Deployed to staging
- Acceptance criteria met

**Definition of Ready**:
- User story clearly defined
- Acceptance criteria documented
- Story estimated by team
- Dependencies identified
- No blockers

## Ceremony Timeboxes

- Daily Standup: 15 minutes
- Sprint Planning: 2 hours per week of sprint
- Sprint Review: 1 hour per week of sprint
- Sprint Retrospective: 1.5 hours per week of sprint
- Backlog Refinement: 10% of sprint capacity

## Atlassian MCP Integration

**Tools Used**:
- Jira for sprint management, backlog, and velocity tracking
- Confluence for ceremony notes, team documentation, and retrospectives

**Key Actions**:
- Use Jira MCP to create sprints, move issues, track progress
- Use Jira MCP to generate burndown charts and velocity reports
- Use Confluence MCP to create sprint planning and retrospective pages
- Use Jira MCP for backlog filtering and prioritization
