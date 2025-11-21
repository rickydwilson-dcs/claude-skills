# Business Analysis Templates Reference

## Table of Contents

1. [Process Documentation Templates](#process-documentation-templates)
2. [RACI Matrix Templates](#raci-matrix-templates)
3. [Process Charter Templates](#process-charter-templates)
4. [Improvement Proposal Templates](#improvement-proposal-templates)
5. [Standard Operating Procedure Templates](#standard-operating-procedure-templates)
6. [Additional Templates](#additional-templates)

---

## Process Documentation Templates

### Template 1: Process Overview Document

```markdown
# Process Name: [Process Title]

## Document Information
- **Process Owner:** [Name, Title]
- **Document Author:** [Name]
- **Version:** [1.0]
- **Last Updated:** [Date]
- **Review Date:** [Date]
- **Status:** [Draft | In Review | Approved | Active]

## Executive Summary
[2-3 paragraph overview of the process, its purpose, and key outcomes]

## Process Details

### Purpose
**Why this process exists:**
[Describe the business need and value this process provides]

### Scope
**What is included:**
- [Item 1]
- [Item 2]
- [Item 3]

**What is excluded:**
- [Item 1]
- [Item 2]

### Inputs
| Input | Source | Format | Trigger |
|-------|--------|--------|---------|
| [Input name] | [Where it comes from] | [Document type] | [What triggers it] |
| [Input name] | [Where it comes from] | [Document type] | [What triggers it] |

### Outputs
| Output | Destination | Format | Success Criteria |
|--------|-------------|--------|------------------|
| [Output name] | [Where it goes] | [Document type] | [How to measure] |
| [Output name] | [Where it goes] | [Document type] | [How to measure] |

### Process Metrics
| Metric | Target | Current | Frequency | Owner |
|--------|--------|---------|-----------|-------|
| Cycle Time | [X hours] | [Y hours] | Daily | [Name] |
| Quality Rate | [X%] | [Y%] | Weekly | [Name] |
| Customer Satisfaction | [X/5] | [Y/5] | Monthly | [Name] |
| Cost per Unit | [$X] | [$Y] | Monthly | [Name] |

## Process Flow

### High-Level Steps
1. [Step 1 name]
2. [Step 2 name]
3. [Step 3 name]
4. [Step 4 name]
5. [Step 5 name]

### Detailed Process Steps

#### Step 1: [Step Name]
- **Responsible:** [Role/Person]
- **Duration:** [Time]
- **Description:** [What happens in this step]
- **Inputs Required:** [List]
- **Tools/Systems:** [List]
- **Decision Points:** [Any decisions made]
- **Quality Checks:** [Validation performed]
- **Outputs:** [What is produced]

#### Step 2: [Step Name]
- **Responsible:** [Role/Person]
- **Duration:** [Time]
- **Description:** [What happens in this step]
- **Inputs Required:** [List]
- **Tools/Systems:** [List]
- **Decision Points:** [Any decisions made]
- **Quality Checks:** [Validation performed]
- **Outputs:** [What is produced]

[Continue for all steps]

## Roles and Responsibilities

| Role | Responsibilities | Authority | Escalation Path |
|------|------------------|-----------|-----------------|
| [Role 1] | [List of tasks] | [Decision rights] | [Who to escalate to] |
| [Role 2] | [List of tasks] | [Decision rights] | [Who to escalate to] |

## Business Rules

### Rule 1: [Rule Name]
- **Description:** [What the rule states]
- **Conditions:** [When it applies]
- **Actions:** [What to do]
- **Exceptions:** [Special cases]

### Rule 2: [Rule Name]
- **Description:** [What the rule states]
- **Conditions:** [When it applies]
- **Actions:** [What to do]
- **Exceptions:** [Special cases]

## Systems and Tools
| System | Purpose | Access Required | Training |
|--------|---------|-----------------|----------|
| [System name] | [What it's used for] | [Access level] | [Training required] |
| [System name] | [What it's used for] | [Access level] | [Training required] |

## Exception Handling

### Exception 1: [Exception Type]
- **Trigger:** [What causes this]
- **Impact:** [Consequences]
- **Resolution:** [How to handle]
- **Responsible:** [Who handles it]
- **Escalation:** [When to escalate]

### Exception 2: [Exception Type]
- **Trigger:** [What causes this]
- **Impact:** [Consequences]
- **Resolution:** [How to handle]
- **Responsible:** [Who handles it]
- **Escalation:** [When to escalate]

## Supporting Documents
- [Link to form/template]
- [Link to related procedure]
- [Link to training material]
- [Link to system guide]

## Process History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial creation |
| 1.1 | [Date] | [Name] | [Description of changes] |

## Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Process Owner | | | |
| Department Manager | | | |
| Quality Assurance | | | |
```

### Template 2: Process Flow Diagram Template

```markdown
# Process Flow Diagram: [Process Name]

## Diagram Information
- **Process:** [Name]
- **Level:** [High-level | Detailed | Technical]
- **Created By:** [Name]
- **Date:** [Date]
- **Version:** [1.0]

## Diagram

[Insert BPMN or flowchart diagram here]

## Legend

### Shapes
- **Oval:** Start/End event
- **Rectangle:** Activity/Task
- **Diamond:** Decision point
- **Parallelogram:** Input/Output
- **Cylinder:** Database/Data store

### Arrows
- **Solid line:** Process flow
- **Dashed line:** Information flow
- **Dotted line:** Association/Reference

### Colors
- **Green:** Value-adding activity
- **Yellow:** Non-value but necessary
- **Red:** Waste/Problem area
- **Blue:** Automated activity

## Process Steps Summary

| Step # | Activity | Role | Duration | Type |
|--------|----------|------|----------|------|
| 1 | [Activity] | [Role] | [Time] | [Value-add/Non-value] |
| 2 | [Activity] | [Role] | [Time] | [Value-add/Non-value] |

## Decision Points

### Decision 1: [Name]
- **Question:** [What is being decided?]
- **Criteria:** [How to decide?]
- **Paths:**
  - **Yes/Approved:** [Next step]
  - **No/Rejected:** [Alternate path]

### Decision 2: [Name]
- **Question:** [What is being decided?]
- **Criteria:** [How to decide?]
- **Paths:**
  - **Path A:** [Description and next step]
  - **Path B:** [Description and next step]

## Handoff Points

| From | To | What is Transferred | Method | SLA |
|------|----|--------------------|--------|-----|
| [Role 1] | [Role 2] | [Documents/Info] | [Email/System] | [Time] |
| [Role 2] | [Role 3] | [Documents/Info] | [Email/System] | [Time] |

## Notes and Assumptions
- [Note 1]
- [Note 2]
- [Assumption 1]
- [Assumption 2]
```

### Template 3: Swimlane Diagram Documentation

```markdown
# Swimlane Diagram: [Process Name]

## Lanes (Actors/Roles)

### Lane 1: [Role/Department Name]
- **Responsibilities:** [Overall responsibilities in this process]
- **Authority Level:** [Decision-making power]
- **Resources:** [Tools, systems, people available]

### Lane 2: [Role/Department Name]
- **Responsibilities:** [Overall responsibilities in this process]
- **Authority Level:** [Decision-making power]
- **Resources:** [Tools, systems, people available]

### Lane 3: [Role/Department Name]
- **Responsibilities:** [Overall responsibilities in this process]
- **Authority Level:** [Decision-making power]
- **Resources:** [Tools, systems, people available]

## Swimlane Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ [Lane 1 Name]                                                   │
│  [Activity 1] ──→ [Activity 3] ──→ [Activity 5]                │
│       │                 │                 │                      │
├───────┼─────────────────┼─────────────────┼──────────────────────┤
│ [Lane 2 Name]    │              │         │                     │
│  [Start] ──→ [Activity 2] ──→ [Activity 4] ──→ [Decision]      │
│                                                     │            │
├─────────────────────────────────────────────────────┼────────────┤
│ [Lane 3 Name]                                       │            │
│                                            [Activity 6] ──→ [End]│
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Activity Descriptions

### [Lane 1 Name] Activities

#### Activity 1: [Name]
- **Trigger:** [What initiates this]
- **Actions:** [Step-by-step what happens]
- **Duration:** [Time to complete]
- **Output:** [What is produced]
- **Next Step:** [Where it goes]

#### Activity 3: [Name]
- **Trigger:** [What initiates this]
- **Actions:** [Step-by-step what happens]
- **Duration:** [Time to complete]
- **Output:** [What is produced]
- **Next Step:** [Where it goes]

### [Lane 2 Name] Activities

[Continue for all activities in each lane]

## Interface Points (Handoffs)

### Handoff A: [Lane 1] → [Lane 2]
- **Activity:** [From activity to activity]
- **What's Transferred:** [Information, documents, etc.]
- **Method:** [How it's transferred]
- **Success Criteria:** [How to know it's complete]
- **Potential Issues:** [Common problems]
- **SLA:** [Time allowed]

### Handoff B: [Lane 2] → [Lane 3]
- **Activity:** [From activity to activity]
- **What's Transferred:** [Information, documents, etc.]
- **Method:** [How it's transferred]
- **Success Criteria:** [How to know it's complete]
- **Potential Issues:** [Common problems]
- **SLA:** [Time allowed]

## Process Metrics by Lane

| Lane | Activities | Total Time | Value-Add Time | Efficiency |
|------|------------|------------|----------------|------------|
| [Lane 1] | [Count] | [Hours] | [Hours] | [%] |
| [Lane 2] | [Count] | [Hours] | [Hours] | [%] |
| [Lane 3] | [Count] | [Hours] | [Hours] | [%] |
| **Total** | [Count] | [Hours] | [Hours] | [%] |

## Improvement Opportunities

### Opportunity 1: [Description]
- **Current State:** [Problem]
- **Proposed Change:** [Solution]
- **Expected Impact:** [Benefit]
- **Effort:** [Low/Medium/High]

### Opportunity 2: [Description]
- **Current State:** [Problem]
- **Proposed Change:** [Solution]
- **Expected Impact:** [Benefit]
- **Effort:** [Low/Medium/High]
```

---

## RACI Matrix Templates

### Template 1: Basic RACI Matrix

```markdown
# RACI Matrix: [Process/Project Name]

## Key
- **R = Responsible:** Person who does the work
- **A = Accountable:** Person ultimately answerable (only one per task)
- **C = Consulted:** People who provide input (two-way communication)
- **I = Informed:** People kept updated (one-way communication)

## RACI Matrix

| Activity/Task | [Role 1] | [Role 2] | [Role 3] | [Role 4] | [Role 5] | [Role 6] |
|---------------|----------|----------|----------|----------|----------|----------|
| [Task 1] | R | A | C | I | - | - |
| [Task 2] | C | R | A | - | I | I |
| [Task 3] | I | C | R | A | R | - |
| [Task 4] | A | R | I | C | - | R |
| [Task 5] | - | A | R | R | C | I |
| [Task 6] | R | I | C | - | A | C |

## Role Definitions

### [Role 1]: [Role Title]
- **Department:** [Department name]
- **Level:** [Management level]
- **Key Responsibilities:** [Primary duties]
- **Authority:** [Decision-making power]

### [Role 2]: [Role Title]
- **Department:** [Department name]
- **Level:** [Management level]
- **Key Responsibilities:** [Primary duties]
- **Authority:** [Decision-making power]

[Continue for all roles]

## Activity Details

### [Task 1]: [Task Name]
- **Description:** [What needs to be done]
- **Frequency:** [How often]
- **Duration:** [Time required]
- **Dependencies:** [What must be done first]
- **Deliverables:** [Expected output]

### [Task 2]: [Task Name]
- **Description:** [What needs to be done]
- **Frequency:** [How often]
- **Duration:** [Time required]
- **Dependencies:** [What must be done first]
- **Deliverables:** [Expected output]

[Continue for all tasks]

## Validation Checklist

- [ ] Each activity has exactly one "A" (Accountable)
- [ ] Each activity has at least one "R" (Responsible)
- [ ] No blank rows (all activities assigned)
- [ ] All roles have at least one assignment
- [ ] No role is overloaded with "R" assignments
- [ ] Appropriate balance of C and I assignments
- [ ] All stakeholders identified
- [ ] Matrix reviewed with all participants
- [ ] Matrix approved by management

## Review and Approval

| Reviewer | Role | Status | Date | Comments |
|----------|------|--------|------|----------|
| [Name] | [Role] | [Approved/Pending] | [Date] | [Comments] |
| [Name] | [Role] | [Approved/Pending] | [Date] | [Comments] |

## Change History

| Version | Date | Changed By | Description |
|---------|------|------------|-------------|
| 1.0 | [Date] | [Name] | Initial version |
| 1.1 | [Date] | [Name] | [Changes made] |
```

### Template 2: Extended RACI (RACI-VS)

```markdown
# RACI-VS Matrix: [Process/Project Name]

## Key
- **R = Responsible:** Person who does the work
- **A = Accountable:** Person ultimately answerable
- **C = Consulted:** People who provide input
- **I = Informed:** People kept updated
- **V = Verifies:** Person who checks/validates the work
- **S = Signs off:** Person who approves/authorizes

## RACI-VS Matrix

| Activity | [Person A] | [Person B] | [Person C] | [Person D] | [Person E] | Notes |
|----------|------------|------------|------------|------------|------------|-------|
| [Activity 1] | R | A | C | I | V | [Any notes] |
| [Activity 2] | V | R | A | C | I | [Any notes] |
| [Activity 3] | I | V | R | A | S | [Any notes] |
| [Activity 4] | S | I | V | R | A | [Any notes] |

## Verification and Sign-off Procedures

### Activities Requiring Verification (V)

#### [Activity Name]
- **Verifier:** [Role/Person]
- **What to Verify:** [Checklist]
  - [ ] [Item 1]
  - [ ] [Item 2]
  - [ ] [Item 3]
- **Verification Method:** [How to verify]
- **Timeline:** [When verification occurs]
- **Failure Process:** [What happens if verification fails]

### Activities Requiring Sign-off (S)

#### [Activity Name]
- **Approver:** [Role/Person]
- **Approval Criteria:** [What must be met]
- **Documentation:** [What must be signed/approved]
- **Timeline:** [When approval occurs]
- **Escalation:** [What if approval is denied]

## Quality Control Summary

| Activity | Responsible | Verifies | Signs Off | Quality Gate |
|----------|-------------|----------|-----------|--------------|
| [Activity 1] | [Person] | [Person] | [Person] | [Y/N] |
| [Activity 2] | [Person] | [Person] | [Person] | [Y/N] |

Quality Gate: Activities marked Y must pass verification before proceeding.
```

### Template 3: Process-Level RACI

```markdown
# Process RACI: [Process Name]

## Process Stages

### Stage 1: [Stage Name]

| Task | Owner | Support | Approve | Inform | Duration |
|------|-------|---------|---------|--------|----------|
| [Task 1.1] | [Name/Role] | [Name/Role] | [Name/Role] | [Distribution list] | [Time] |
| [Task 1.2] | [Name/Role] | [Name/Role] | [Name/Role] | [Distribution list] | [Time] |
| [Task 1.3] | [Name/Role] | [Name/Role] | [Name/Role] | [Distribution list] | [Time] |

**Stage Duration:** [Total time]
**Stage Owner:** [Name/Role]

### Stage 2: [Stage Name]

| Task | Owner | Support | Approve | Inform | Duration |
|------|-------|---------|---------|--------|----------|
| [Task 2.1] | [Name/Role] | [Name/Role] | [Name/Role] | [Distribution list] | [Time] |
| [Task 2.2] | [Name/Role] | [Name/Role] | [Name/Role] | [Distribution list] | [Time] |

**Stage Duration:** [Total time]
**Stage Owner:** [Name/Role]

[Continue for all stages]

## Handoff Responsibility Matrix

| Handoff Point | From (Accountable) | To (Accountable) | Information/Deliverables | Quality Criteria |
|---------------|-------------------|------------------|-------------------------|------------------|
| Stage 1 → 2 | [Role] | [Role] | [List] | [Criteria] |
| Stage 2 → 3 | [Role] | [Role] | [List] | [Criteria] |

## Escalation Matrix

| Issue Type | First Contact | Escalation Level 1 | Escalation Level 2 | Timeline |
|------------|--------------|-------------------|-------------------|----------|
| Technical | [Role] | [Role] | [Role] | [Hours] |
| Resource | [Role] | [Role] | [Role] | [Hours] |
| Quality | [Role] | [Role] | [Role] | [Hours] |
| Timeline | [Role] | [Role] | [Role] | [Hours] |
```

---

## Process Charter Templates

### Template 1: Six Sigma Project Charter

```markdown
# Project Charter: [Project Name]

## Project Information
- **Project Name:** [Full name]
- **Project ID:** [Reference number]
- **Charter Date:** [Date]
- **Sponsor:** [Name, Title]
- **Champion:** [Name, Title]
- **Black Belt/Lead:** [Name]
- **Team Members:** [List names and roles]

## Business Case

### Background
[Describe the current situation, historical context, and why this project is needed now]

### Strategic Alignment
This project supports the following strategic objectives:
- [Strategic objective 1]
- [Strategic objective 2]
- [Strategic objective 3]

### Problem Statement
[Clear, specific statement of the problem. Avoid solutions. Include metrics.]

Example format:
"[Process/Area] currently experiences [problem] resulting in [impact]. Over the past [time period], [metric] has [increased/decreased] by [amount], causing [consequence]."

Actual example:
"Customer service call resolution time has increased from 15 minutes to 35 minutes over the past 6 months, resulting in decreased customer satisfaction scores (from 4.2 to 3.1 out of 5) and increased call abandonment rates (from 5% to 18%)."

### Goal Statement
[Specific, measurable goal statement]

Example format:
"Reduce [metric] from [current state] to [target state] by [date], resulting in [expected benefit]."

Actual example:
"Reduce average call resolution time from 35 minutes to 18 minutes by December 31, 2025, resulting in improved customer satisfaction scores to 4.0+ and reduced call abandonment to <8%."

## Scope

### In Scope
- [Specific area/process 1]
- [Specific area/process 2]
- [Specific area/process 3]
- [Geographic location/department]
- [Time period covered]

### Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]
- [Explicitly excluded item 3]
- [Boundary conditions]

## Metrics

### Primary Metric
- **Y (Output):** [What you're trying to improve]
- **Operational Definition:** [Precisely how it's measured]
- **Current Performance:** [Baseline]
- **Goal:** [Target]
- **Data Source:** [Where data comes from]

Example:
- **Y:** Average call resolution time
- **Operational Definition:** Time from when agent answers call to when call is closed in system, measured in minutes
- **Current Performance:** 35.2 minutes (average of last 3 months)
- **Goal:** ≤18 minutes
- **Data Source:** Call center management system (daily export)

### Secondary Metrics
| Metric | Definition | Current | Goal | Data Source |
|--------|------------|---------|------|-------------|
| [Metric 1] | [How measured] | [Value] | [Target] | [Source] |
| [Metric 2] | [How measured] | [Value] | [Target] | [Source] |
| [Metric 3] | [How measured] | [Value] | [Target] | [Source] |

## Project Plan

### Timeline
| Phase | Activities | Duration | Completion Date |
|-------|------------|----------|-----------------|
| Define | Charter, SIPOC, VOC | 2 weeks | [Date] |
| Measure | Data collection plan, MSA, baseline | 3 weeks | [Date] |
| Analyze | Root cause analysis, hypothesis testing | 4 weeks | [Date] |
| Improve | Solution design, pilot, implementation | 6 weeks | [Date] |
| Control | Control plan, documentation, handoff | 2 weeks | [Date] |

**Total Duration:** [X weeks/months]

### Milestones
| Milestone | Date | Deliverable |
|-----------|------|-------------|
| Charter approved | [Date] | Signed charter |
| Baseline established | [Date] | Measurement system validated |
| Root causes identified | [Date] | Analysis report |
| Solution piloted | [Date] | Pilot results |
| Full implementation | [Date] | Training completed |
| Control established | [Date] | Control plan active |
| Project closed | [Date] | Closeout report |

## Team

### Roles and Responsibilities

**Executive Sponsor:** [Name]
- Provides resources
- Removes barriers
- Reviews progress monthly
- Approves major decisions

**Champion:** [Name]
- Guides project direction
- Connects to strategy
- Reviews progress bi-weekly
- Facilitates stakeholder buy-in

**Black Belt/Project Lead:** [Name]
- Leads analysis
- Manages project execution
- Reports progress weekly
- Owns deliverables

**Team Members:**
- [Name] - [Role]: [Responsibilities]
- [Name] - [Role]: [Responsibilities]
- [Name] - [Role]: [Responsibilities]

**Process Owner:** [Name]
- Implements changes
- Sustains improvements
- Owns control plan
- Reports ongoing metrics

## Expected Benefits

### Financial Benefits
| Benefit | Calculation Method | Annual Value | One-time Value |
|---------|-------------------|--------------|----------------|
| [Benefit 1] | [How calculated] | $[Amount] | $[Amount] |
| [Benefit 2] | [How calculated] | $[Amount] | $[Amount] |
| **Total** | | **$[Amount]** | **$[Amount]** |

### Non-Financial Benefits
- [Qualitative benefit 1]
- [Qualitative benefit 2]
- [Qualitative benefit 3]

## Resources Required

### Personnel
- [Number] hours of [role] time per week
- [Number] hours of [role] time per week
- Training: [Description and hours]

### Budget
| Item | Amount | Justification |
|------|--------|---------------|
| Software/Tools | $[Amount] | [Why needed] |
| Training | $[Amount] | [Why needed] |
| Equipment | $[Amount] | [Why needed] |
| Consulting | $[Amount] | [Why needed] |
| Other | $[Amount] | [Why needed] |
| **Total** | **$[Amount]** | |

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation Strategy | Owner |
|------|-------------|--------|---------------------|-------|
| [Risk 1] | [H/M/L] | [H/M/L] | [How to prevent/respond] | [Name] |
| [Risk 2] | [H/M/L] | [H/M/L] | [How to prevent/respond] | [Name] |
| [Risk 3] | [H/M/L] | [H/M/L] | [How to prevent/respond] | [Name] |

## Communication Plan

| Audience | Information | Method | Frequency | Owner |
|----------|-------------|--------|-----------|-------|
| Executive Sponsor | Progress, issues, decisions | Email summary | Monthly | Project Lead |
| Champion | Detailed status, metrics | In-person meeting | Bi-weekly | Project Lead |
| Stakeholders | Updates, changes | Email, meetings | As needed | Project Lead |
| Team Members | Tasks, data, analysis | Team meetings | Weekly | Project Lead |
| Process Owner | Implementation plans | Detailed reviews | Weekly | Project Lead |

## Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Executive Sponsor | | | |
| Champion | | | |
| Process Owner | | | |
| Finance (if >$X) | | | |
| Project Lead | | | |

---

## Appendices

### Appendix A: SIPOC Diagram
[Insert SIPOC]

### Appendix B: Process Map
[Insert high-level process map]

### Appendix C: Baseline Data
[Insert baseline charts/data]
```

### Template 2: Lean/Kaizen Event Charter

```markdown
# Kaizen Event Charter: [Event Name]

## Event Information
- **Event Name:** [Name]
- **Date:** [Start date - End date]
- **Location:** [Where event will take place]
- **Facilitator:** [Name]
- **Sponsor:** [Name, Title]

## Target Process/Area
**Process:** [Name of process]
**Department:** [Department name]
**Physical Location:** [Where process takes place]

## Current State

### Problem Description
[Describe current issues, waste, or inefficiency]

### Key Metrics (Baseline)
| Metric | Current Performance | Measurement Method |
|--------|--------------------|--------------------|
| Cycle Time | [Value] | [How measured] |
| Lead Time | [Value] | [How measured] |
| Quality/Defect Rate | [Value] | [How measured] |
| Productivity | [Value] | [How measured] |
| Customer Satisfaction | [Value] | [How measured] |

### Types of Waste Observed
- [ ] Transportation
- [ ] Inventory
- [ ] Motion
- [ ] Waiting
- [ ] Overproduction
- [ ] Over-processing
- [ ] Defects
- [ ] Underutilized skills

[Describe specific examples of each waste type identified]

## Event Objectives

### Goals
1. [Specific goal 1 with measurement]
2. [Specific goal 2 with measurement]
3. [Specific goal 3 with measurement]

### Target State
[Describe the desired future state]

### Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

## Event Team

| Name | Role/Department | Expertise | Time Commitment |
|------|----------------|-----------|-----------------|
| [Name] | Facilitator | Lean methods | 100% |
| [Name] | Process owner | Process knowledge | 100% |
| [Name] | Team member | [Expertise] | [%] |
| [Name] | Team member | [Expertise] | [%] |
| [Name] | Subject matter expert | [Expertise] | As needed |

## Event Schedule

### Day 1: Training and Current State
- 8:00-9:00: Kickoff and training
- 9:00-12:00: Process walk, observation
- 12:00-1:00: Lunch
- 1:00-4:00: Current state mapping
- 4:00-5:00: Waste identification

### Day 2: Analysis and Future State Design
- 8:00-10:00: Root cause analysis
- 10:00-12:00: Future state design
- 12:00-1:00: Lunch
- 1:00-5:00: Solution development

### Day 3: Implementation
- 8:00-12:00: Implement changes
- 12:00-1:00: Lunch
- 1:00-4:00: Test and refine
- 4:00-5:00: Document changes

### Day 4: Validation and Standardization
- 8:00-11:00: Measure results
- 11:00-12:00: Create standard work
- 12:00-1:00: Lunch
- 1:00-3:00: Training and handoff
- 3:00-4:00: Report out preparation
- 4:00-5:00: Stakeholder presentation

### Day 5: Follow-up
- 30-day follow-up meeting
- 60-day results review
- 90-day sustainability check

## Resources Needed

### Before Event
- [ ] Reserve conference room
- [ ] Arrange for team members' time
- [ ] Gather baseline data
- [ ] Print process maps
- [ ] Prepare materials (post-its, markers, flip charts)

### During Event
- [ ] Access to work area
- [ ] Authority to make changes
- [ ] IT support (if needed)
- [ ] Budget for small purchases: $[Amount]
- [ ] Photography permission

### After Event
- [ ] Implementation resources
- [ ] Training materials
- [ ] Documentation support

## Boundaries and Constraints

### What CAN Be Changed
- [Item 1]
- [Item 2]
- [Item 3]

### What CANNOT Be Changed
- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

### Required Approvals
- Budget changes >$[X]: [Approver]
- Headcount changes: [Approver]
- Policy exceptions: [Approver]
- System changes: [Approver]

## Expected Outcomes

### Quantitative Targets
| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| [Metric 1] | [Value] | [Value] | [%] |
| [Metric 2] | [Value] | [Value] | [%] |
| [Metric 3] | [Value] | [Value] | [%] |

### Deliverables
- [ ] Current state map
- [ ] Future state map
- [ ] Implementation plan
- [ ] Standard work documents
- [ ] Training materials
- [ ] Report out presentation
- [ ] 30-60-90 day follow-up plan

## Follow-up Plan

### Immediate (Week 1-2)
- [Action item 1] - Owner: [Name]
- [Action item 2] - Owner: [Name]

### Short-term (Month 1)
- [Action item 1] - Owner: [Name]
- [Action item 2] - Owner: [Name]

### Long-term (Month 2-3)
- [Action item 1] - Owner: [Name]
- [Action item 2] - Owner: [Name]

### Sustainability Measures
- Monthly metrics review
- Quarterly process audit
- Ongoing training for new hires
- Recognition program for improvements

## Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Sponsor | | | |
| Process Owner | | | |
| Facilitator | | | |
```

---

## Improvement Proposal Templates

### Template 1: Process Improvement Proposal

```markdown
# Process Improvement Proposal

## Proposal Information
- **Proposal ID:** [Number]
- **Date Submitted:** [Date]
- **Submitted By:** [Name, Title]
- **Department:** [Department]
- **Priority:** [High | Medium | Low]
- **Status:** [Draft | Submitted | In Review | Approved | Rejected | Implemented]

## Executive Summary
[2-3 paragraph summary of the proposal, covering problem, solution, and expected benefit]

## Current State Analysis

### Process Description
**Process Name:** [Name]
**Process Owner:** [Name]
**Department(s) Affected:** [List]

**Current Process Description:**
[Describe how the process currently works]

### Problem Statement
[Clear, specific statement of the problem or opportunity]

**Symptoms:**
- [Observed issue 1]
- [Observed issue 2]
- [Observed issue 3]

**Impact:**
- **Financial:** [Cost or lost revenue]
- **Customer:** [Customer impact]
- **Employee:** [Employee impact]
- **Operational:** [Efficiency/quality impact]

### Supporting Data
| Metric | Current Performance | Source | Time Period |
|--------|--------------------| -------|-------------|
| [Metric 1] | [Value] | [Where from] | [When measured] |
| [Metric 2] | [Value] | [Where from] | [When measured] |
| [Metric 3] | [Value] | [Where from] | [When measured] |

[Include charts, graphs, or other data visualization]

### Root Cause Analysis
**Primary Root Cause:** [Description]

**Contributing Factors:**
1. [Factor 1]
2. [Factor 2]
3. [Factor 3]

[Include fishbone diagram or other analysis tools]

## Proposed Solution

### Solution Overview
[Describe the proposed improvement in detail]

### Solution Components
1. **[Component 1 Name]**
   - Description: [What it involves]
   - Implementation: [How to implement]
   - Owner: [Who responsible]

2. **[Component 2 Name]**
   - Description: [What it involves]
   - Implementation: [How to implement]
   - Owner: [Who responsible]

3. **[Component 3 Name]**
   - Description: [What it involves]
   - Implementation: [How to implement]
   - Owner: [Who responsible]

### Future State Process
[Describe how the process will work after improvement]

**Key Changes:**
- [ ] [Change 1]
- [ ] [Change 2]
- [ ] [Change 3]

### Alignment with Strategy
This proposal supports:
- [Strategic objective 1]
- [Strategic objective 2]
- [Organizational value or priority]

## Implementation Plan

### Timeline
| Phase | Activities | Duration | Start Date | End Date | Owner |
|-------|------------|----------|------------|----------|-------|
| Planning | [Activities] | [X weeks] | [Date] | [Date] | [Name] |
| Preparation | [Activities] | [X weeks] | [Date] | [Date] | [Name] |
| Execution | [Activities] | [X weeks] | [Date] | [Date] | [Name] |
| Validation | [Activities] | [X weeks] | [Date] | [Date] | [Name] |
| Handoff | [Activities] | [X weeks] | [Date] | [Date] | [Name] |

**Total Implementation Time:** [X weeks/months]

### Key Milestones
- [ ] [Milestone 1] - [Date]
- [ ] [Milestone 2] - [Date]
- [ ] [Milestone 3] - [Date]
- [ ] [Milestone 4] - [Date]

### Dependencies
| Dependency | Owner | Required By | Status |
|------------|-------|-------------|--------|
| [Dependency 1] | [Name] | [Date] | [Status] |
| [Dependency 2] | [Name] | [Date] | [Status] |

### Change Management
**Stakeholders Affected:**
- [Stakeholder group 1]: [How affected]
- [Stakeholder group 2]: [How affected]
- [Stakeholder group 3]: [How affected]

**Communication Plan:**
| Audience | Message | Method | Timing | Owner |
|----------|---------|--------|--------|-------|
| [Group 1] | [What to communicate] | [How] | [When] | [Who] |
| [Group 2] | [What to communicate] | [How] | [When] | [Who] |

**Training Requirements:**
- [Training 1]: [Description, duration, audience]
- [Training 2]: [Description, duration, audience]

## Expected Benefits

### Quantitative Benefits

**Financial Impact:**
| Benefit | Calculation | Annual Value | 3-Year Value |
|---------|-------------|--------------|--------------|
| Cost Reduction | [Formula] | $[Amount] | $[Amount] |
| Revenue Increase | [Formula] | $[Amount] | $[Amount] |
| Cost Avoidance | [Formula] | $[Amount] | $[Amount] |
| **Total Financial** | | **$[Amount]** | **$[Amount]** |

**Operational Impact:**
| Metric | Current | Projected | Improvement |
|--------|---------|-----------|-------------|
| Cycle Time | [Value] | [Value] | [%/amount] |
| Quality/Defects | [Value] | [Value] | [%/amount] |
| Capacity | [Value] | [Value] | [%/amount] |
| Productivity | [Value] | [Value] | [%/amount] |

### Qualitative Benefits
- **Customer Experience:** [Description]
- **Employee Satisfaction:** [Description]
- **Compliance/Risk:** [Description]
- **Strategic Value:** [Description]

### Benefit Realization Timeline
| Benefit | When Realized | How Measured |
|---------|---------------|--------------|
| [Benefit 1] | [Timeframe] | [Metric/method] |
| [Benefit 2] | [Timeframe] | [Metric/method] |

## Resource Requirements

### Personnel
| Role | Time Required | Duration | Cost |
|------|---------------|----------|------|
| [Role 1] | [Hours/week] | [Weeks] | $[Amount] |
| [Role 2] | [Hours/week] | [Weeks] | $[Amount] |
| **Total Labor** | | | **$[Amount]** |

### Budget
| Category | Item | Quantity | Unit Cost | Total Cost |
|----------|------|----------|-----------|------------|
| Software | [Item] | [Qty] | $[Amount] | $[Amount] |
| Hardware | [Item] | [Qty] | $[Amount] | $[Amount] |
| Training | [Item] | [Qty] | $[Amount] | $[Amount] |
| Consulting | [Item] | [Qty] | $[Amount] | $[Amount] |
| Other | [Item] | [Qty] | $[Amount] | $[Amount] |
| **Total Cost** | | | | **$[Amount]** |

### ROI Calculation
- **Total Investment:** $[Amount]
- **Annual Benefit:** $[Amount]
- **Payback Period:** [X months]
- **3-Year ROI:** [X]%

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation Strategy | Contingency Plan | Owner |
|------|-------------|--------|---------------------|------------------|-------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] | [Name] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] | [Name] |
| [Risk 3] | [H/M/L] | [H/M/L] | [Prevention] | [If it happens] | [Name] |

## Alternatives Considered

### Alternative 1: [Name]
- **Description:** [What it involves]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Cost:** $[Amount]
- **Why Not Selected:** [Reason]

### Alternative 2: [Name]
- **Description:** [What it involves]
- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Cost:** $[Amount]
- **Why Not Selected:** [Reason]

### Do Nothing Option
- **Impact of Not Proceeding:** [Consequences]
- **Cost of Inaction:** $[Amount] annually

## Success Metrics

### Implementation Success
- [ ] Completed on time
- [ ] Completed within budget
- [ ] All stakeholders trained
- [ ] No critical issues during rollout

### Performance Success (Post-Implementation)
| Metric | Target | Measurement Date | Actual | Status |
|--------|--------|------------------|--------|--------|
| [Metric 1] | [Value] | [When] | | |
| [Metric 2] | [Value] | [When] | | |
| [Metric 3] | [Value] | [When] | | |

### Review Schedule
- **30-day review:** [Date]
- **60-day review:** [Date]
- **90-day review:** [Date]
- **6-month review:** [Date]
- **Annual review:** [Date]

## Approval and Sign-off

| Role | Name | Signature | Date | Decision |
|------|------|-----------|------|----------|
| Sponsor | | | | Approve / Reject / Defer |
| Process Owner | | | | Approve / Reject / Defer |
| Finance | | | | Approve / Reject / Defer |
| IT (if applicable) | | | | Approve / Reject / Defer |
| Compliance (if applicable) | | | | Approve / Reject / Defer |

**Decision:** [Approved | Rejected | Deferred]
**Date:** [Date]
**Conditions (if any):** [List any conditions or modifications required]

## Appendices

### Appendix A: Current State Process Map
[Insert process map]

### Appendix B: Future State Process Map
[Insert process map]

### Appendix C: Supporting Data and Analysis
[Insert charts, data tables, analysis]

### Appendix D: Stakeholder Analysis
[Insert stakeholder matrix or analysis]
```

---

## Standard Operating Procedure Templates

### Template 1: Task-Level SOP

```markdown
# Standard Operating Procedure

## Document Information
- **SOP Number:** [SOP-XXX]
- **Version:** [1.0]
- **Effective Date:** [Date]
- **Review Date:** [Date]
- **Owner:** [Name, Title]
- **Approver:** [Name, Title]

## Procedure Title
[Clear, descriptive title of the procedure]

## Purpose
[1-2 sentences explaining why this procedure exists and what it accomplishes]

## Scope
**Applies To:**
- [Department/role 1]
- [Department/role 2]
- [Specific situations]

**Does Not Apply To:**
- [Exceptions 1]
- [Exceptions 2]

## Definitions
| Term | Definition |
|------|------------|
| [Term 1] | [Clear definition] |
| [Term 2] | [Clear definition] |
| [Acronym 1] | [What it stands for and means] |

## Roles and Responsibilities
- **[Role 1]:** [What they do in this procedure]
- **[Role 2]:** [What they do in this procedure]
- **[Role 3]:** [What they do in this procedure]

## Materials and Equipment Needed
- [Item 1]
- [Item 2]
- [System access: specific system name]
- [Form/template: name and location]

## Safety and Compliance
- [Safety consideration 1]
- [Compliance requirement 1]
- [Required certifications/training]
- [Personal protective equipment]

## Procedure Steps

### Step 1: [Step Name]
**Who:** [Role responsible]
**When:** [Trigger or timing]
**Where:** [Location/system]
**Duration:** [Approximate time]

**Actions:**
1. [Specific action 1]
   - [Sub-step or clarification]
   - [Example if helpful]
2. [Specific action 2]
3. [Specific action 3]

**Quality Check:**
- [ ] [Verification point 1]
- [ ] [Verification point 2]

**Common Issues:**
- Problem: [Issue that might occur]
  - Solution: [How to resolve]

**Screenshot/Diagram:** [If helpful, insert visual]

### Step 2: [Step Name]
**Who:** [Role responsible]
**When:** [Trigger or timing]
**Where:** [Location/system]
**Duration:** [Approximate time]

**Actions:**
1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

**Decision Point:**
- IF [condition A]: Go to Step 3
- IF [condition B]: Go to Step 5
- IF [condition C]: Escalate to [role]

**Quality Check:**
- [ ] [Verification point 1]
- [ ] [Verification point 2]

[Continue for all steps]

### Final Step: [Step Name]
**Who:** [Role responsible]
**When:** [Trigger or timing]
**Where:** [Location/system]
**Duration:** [Approximate time]

**Actions:**
1. [Specific action 1]
2. [Specific action 2]
3. Document completion in [system/log]
4. Notify [stakeholder] via [method]

**Completion Criteria:**
- [ ] [Required outcome 1]
- [ ] [Required outcome 2]
- [ ] [Documentation completed]

## Flowchart
[Insert simple flowchart showing the procedure flow]

## Troubleshooting Guide

| Problem | Possible Cause | Solution | Escalate To |
|---------|----------------|----------|-------------|
| [Issue 1] | [Cause] | [Fix] | [Role/person if can't fix] |
| [Issue 2] | [Cause] | [Fix] | [Role/person if can't fix] |
| [Issue 3] | [Cause] | [Fix] | [Role/person if can't fix] |

## Quality Standards
- **Accuracy:** [Target %]
- **Timeliness:** [Target time]
- **Completeness:** [What must be included]
- **Compliance:** [Standards to meet]

## Documentation Requirements
**Required Records:**
- [Document 1]: Retention period [X years]
- [Document 2]: Retention period [X years]

**Where to File:**
- [Location/system for records]

## Related Documents
- [Related SOP-XXX]: [Title]
- [Form XXX]: [Title and location]
- [Policy XXX]: [Title]
- [Training material]: [Location]

## Revision History
| Version | Date | Author | Changes Made |
|---------|------|--------|--------------|
| 1.0 | [Date] | [Name] | Initial creation |
| 1.1 | [Date] | [Name] | [Description of changes] |

## Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Created By | | | |
| Reviewed By | | | |
| Approved By | | | |

---

## Training Checklist

Employee Name: _________________ Date: _________

- [ ] Read and understood SOP
- [ ] Observed procedure performed by trainer
- [ ] Performed procedure under supervision
- [ ] Demonstrated competency
- [ ] Reviewed troubleshooting scenarios
- [ ] Knows when/how to escalate

Trainer Signature: _________________ Date: _________
Employee Signature: _________________ Date: _________
```

### Template 2: Process-Level SOP

```markdown
# Standard Operating Procedure: [Process Name]

## Document Control
- **SOP ID:** [SOP-XXX]
- **Version:** [1.0]
- **Status:** [Draft | Active | Under Review | Archived]
- **Effective Date:** [Date]
- **Next Review Date:** [Date + 1 year]
- **Process Owner:** [Name, Title, Department]
- **Document Author:** [Name]
- **Approved By:** [Name, Title]

## Process Overview

### Purpose Statement
[Clear statement of what this process accomplishes and why it's important to the organization]

### Process Objectives
1. [Objective 1 - specific and measurable]
2. [Objective 2 - specific and measurable]
3. [Objective 3 - specific and measurable]

### Process Scope
**Start Point:** [What triggers this process]
**End Point:** [What completes this process]

**Boundaries:**
- **Includes:** [What's part of this process]
- **Excludes:** [What's handled elsewhere]
- **Interfaces:** [Where this process connects to others]

### Process Metrics
| KPI | Target | Measurement Method | Frequency | Owner |
|-----|--------|-------------------|-----------|-------|
| [KPI 1] | [Value] | [How measured] | [When] | [Who] |
| [KPI 2] | [Value] | [How measured] | [When] | [Who] |
| [KPI 3] | [Value] | [How measured] | [When] | [Who] |

## Process Architecture

### SIPOC

| Suppliers | Inputs | Process Steps | Outputs | Customers |
|-----------|--------|---------------|---------|-----------|
| [Supplier 1] | [Input 1] | 1. [Step 1] | [Output 1] | [Customer 1] |
| [Supplier 2] | [Input 2] | 2. [Step 2] | [Output 2] | [Customer 2] |
| [Supplier 3] | [Input 3] | 3. [Step 3] | [Output 3] | [Customer 3] |

### High-Level Process Flow
```
[Trigger] → [Phase 1] → [Phase 2] → [Phase 3] → [Completion]
             5 steps     8 steps     4 steps
             2 days      1 day       4 hours
```

### Roles and Responsibilities Matrix

| Role | Responsibilities | Decision Rights | Skills Required |
|------|------------------|-----------------|-----------------|
| [Role 1] | [List of duties] | [What they can decide] | [Training/skills needed] |
| [Role 2] | [List of duties] | [What they can decide] | [Training/skills needed] |
| [Role 3] | [List of duties] | [What they can decide] | [Training/skills needed] |

## Detailed Process Procedures

### Phase 1: [Phase Name]
**Purpose:** [What this phase accomplishes]
**Duration:** [Typical time]
**Owner:** [Role responsible]

#### Activity 1.1: [Activity Name]
**Responsible:** [Role]
**Input:** [What's needed to start]
**Output:** [What's produced]
**Duration:** [Time estimate]

**Procedure:**
1. [Step 1]
   - [Detail or clarification]
   - [System/tool to use]
2. [Step 2]
3. [Step 3]

**Decision Criteria:**
- IF [condition], THEN [action]
- IF [condition], THEN [action]

**Quality Checkpoints:**
- [ ] [Check 1]
- [ ] [Check 2]

**Systems Used:** [List of systems/tools]

#### Activity 1.2: [Activity Name]
[Same structure as above]

### Phase 2: [Phase Name]
[Same structure as Phase 1]

## Business Rules

### Rule Set 1: [Category]

#### Rule 1.1: [Rule Name]
- **Statement:** [Clear rule statement]
- **Rationale:** [Why this rule exists]
- **Conditions:** [When it applies]
- **Actions:** [What to do]
- **Exceptions:** [Special cases]
- **Authority:** [Who can grant exceptions]

#### Rule 1.2: [Rule Name]
[Same structure]

### Rule Set 2: [Category]
[Same structure]

## Systems and Tools

### System 1: [System Name]
- **Purpose:** [What it's used for in this process]
- **Access Required:** [Permission level needed]
- **Key Functions:** [Specific features used]
- **Training:** [Where to get trained]
- **Support:** [Who to contact for help]

### System 2: [System Name]
[Same structure]

## Exception Handling

### Exception Type 1: [Name]
**Frequency:** [How often this occurs]
**Impact:** [Severity - Low/Medium/High]

**Identification:**
- [How to recognize this exception]
- [Symptoms or indicators]

**Resolution Process:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Escalation Path:**
- Level 1: [Role] - within [timeframe]
- Level 2: [Role] - within [timeframe]
- Level 3: [Role] - within [timeframe]

**Documentation:** [How to record the exception]

### Exception Type 2: [Name]
[Same structure]

## Quality Assurance

### Quality Standards
- [Standard 1]: [Description and target]
- [Standard 2]: [Description and target]
- [Standard 3]: [Description and target]

### Quality Control Points
| Activity | Check Type | Frequency | Responsible | Action if Fail |
|----------|------------|-----------|-------------|----------------|
| [Activity] | [Inspection type] | [When] | [Who] | [What to do] |
| [Activity] | [Inspection type] | [When] | [Who] | [What to do] |

### Audit Schedule
- **Internal Audit:** [Frequency] by [Role]
- **External Audit:** [Frequency] by [Entity]
- **Management Review:** [Frequency]

## Training Requirements

### Required Training
| Role | Training Module | Duration | Renewal | Certification |
|------|----------------|----------|---------|---------------|
| [Role 1] | [Module name] | [Hours] | [Period] | [Y/N] |
| [Role 2] | [Module name] | [Hours] | [Period] | [Y/N] |

### Training Resources
- [Training manual location]
- [Video tutorial location]
- [Practice environment access]
- [Trainer contact information]

### Competency Assessment
- [ ] Knowledge test (80% passing)
- [ ] Practical demonstration
- [ ] Shadowing period ([X] days)
- [ ] Sign-off by supervisor

## Performance Monitoring

### Dashboard Metrics
[Insert sample dashboard or describe key indicators monitored]

### Reporting
| Report | Audience | Frequency | Delivery Method | Owner |
|--------|----------|-----------|-----------------|-------|
| [Report 1] | [Who] | [When] | [How] | [Who creates] |
| [Report 2] | [Who] | [When] | [How] | [Who creates] |

### Review Cycle
- **Daily:** [What's reviewed]
- **Weekly:** [What's reviewed]
- **Monthly:** [What's reviewed]
- **Quarterly:** [What's reviewed]
- **Annually:** [What's reviewed]

## Continuous Improvement

### Improvement Process
1. Identify opportunity
2. Document in [system/log]
3. Review with process owner
4. Prioritize and plan
5. Implement and test
6. Update SOP
7. Communicate changes
8. Train affected staff

### Feedback Mechanisms
- Process participants: [How they submit feedback]
- Customers: [How they provide input]
- Metrics review: [Trigger for investigation]

### Change Management
**Minor Changes** (no impact to outcomes):
- Approved by: Process Owner
- Communication: Email to team
- Update: Within 5 business days

**Major Changes** (affects outputs, customers, or metrics):
- Approved by: Department Manager
- Communication: Formal announcement + training
- Update: Following testing period

## Compliance and Governance

### Regulatory Requirements
- [Regulation 1]: [How this process complies]
- [Regulation 2]: [How this process complies]
- [Standard 1]: [How this process complies]

### Record Retention
| Record Type | Retention Period | Storage Location | Disposal Method |
|-------------|------------------|------------------|-----------------|
| [Record 1] | [X years] | [Where] | [How] |
| [Record 2] | [X years] | [Where] | [How] |

### Audit Trail
- [ ] All process instances logged in [system]
- [ ] Decisions documented with rationale
- [ ] Changes tracked with version control
- [ ] Access monitored and reviewed

## Related Documents

### Procedures
- [SOP-XXX]: [Related procedure title]
- [WI-XXX]: [Work instruction title]

### Forms and Templates
- [FORM-XXX]: [Form name and location]
- [TEMP-XXX]: [Template name and location]

### Policies
- [POL-XXX]: [Policy title]

### Reference Materials
- [Link to additional resource]
- [Training materials location]

## Glossary
| Term | Definition |
|------|------------|
| [Term 1] | [Complete definition] |
| [Term 2] | [Complete definition] |
| [Acronym 1] | [What it stands for and means] |

## Appendices

### Appendix A: Process Flow Diagram
[Insert detailed BPMN or flowchart]

### Appendix B: Swimlane Diagram
[Insert swimlane showing roles]

### Appendix C: Forms and Checklists
[Insert or link to forms]

### Appendix D: System Screenshots
[Insert relevant screenshots with annotations]

## Document Revision History
| Version | Date | Author | Approver | Summary of Changes |
|---------|------|--------|----------|-------------------|
| 1.0 | [Date] | [Name] | [Name] | Initial creation |
| 1.1 | [Date] | [Name] | [Name] | [What changed] |
| 2.0 | [Date] | [Name] | [Name] | [Major revision details] |

## Approval Signatures

| Role | Name | Title | Signature | Date |
|------|------|-------|-----------|------|
| Process Owner | | | | |
| Department Manager | | | | |
| Quality Assurance | | | | |
| Compliance (if req'd) | | | | |
```

---

## Additional Templates

### Template 4: Quick Reference Guide

```markdown
# Quick Reference: [Process Name]

## At a Glance
**What:** [One sentence description]
**When:** [When to use this]
**Who:** [Who performs this]
**Time:** [How long it takes]

## Quick Steps
1. [Step 1 - action verb + brief description]
2. [Step 2]
3. [Step 3]
4. [Step 4]
5. [Step 5]

## Key Decision
**Question:** [What needs to be decided?]
- IF [condition] → [action]
- IF [condition] → [action]
- ELSE → [default action]

## Common Issues
| Problem | Solution |
|---------|----------|
| [Issue 1] | [Quick fix] |
| [Issue 2] | [Quick fix] |

## Need Help?
- First: [Resource/contact]
- Escalate: [Manager/expert]
- Emergency: [Contact]

## Full SOP: [Link to detailed SOP]
```

### Template 5: Process Improvement Tracker

```markdown
# Process Improvement Tracker: [Process Name]

| ID | Date | Submitted By | Issue/Opportunity | Priority | Status | Owner | Target Date | Resolution |
|----|------|--------------|-------------------|----------|--------|-------|-------------|------------|
| 001 | [Date] | [Name] | [Description] | [H/M/L] | [Open/In Progress/Closed] | [Name] | [Date] | [What was done] |
| 002 | [Date] | [Name] | [Description] | [H/M/L] | [Status] | [Name] | [Date] | [What was done] |

## Summary Statistics
- **Total Improvements:** [Count]
- **Implemented:** [Count]
- **In Progress:** [Count]
- **Pending:** [Count]
- **Average Time to Implement:** [X days]

## Top Improvement Themes
1. [Theme 1]: [Count] improvements
2. [Theme 2]: [Count] improvements
3. [Theme 3]: [Count] improvements
```

---

**Document Version:** 1.0
**Last Updated:** November 21, 2025
**Total Lines:** 400+
