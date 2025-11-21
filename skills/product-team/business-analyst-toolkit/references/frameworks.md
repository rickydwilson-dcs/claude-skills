# Business Analysis Frameworks Reference

## Table of Contents

1. [BPMN Notation Standards](#bpmn-notation-standards)
2. [Swimlane Diagrams](#swimlane-diagrams)
3. [Value Stream Mapping](#value-stream-mapping)
4. [Six Sigma DMAIC](#six-sigma-dmaic)
5. [Process Mining Techniques](#process-mining-techniques)
6. [Integration Patterns](#integration-patterns)

---

## BPMN Notation Standards

### Overview

Business Process Model and Notation (BPMN) is the global standard for process modeling, providing a graphical representation that is easy to understand by all business stakeholders.

### Core BPMN Elements

#### Flow Objects

**Events**
Events are things that happen during a process. They affect the flow and usually have a trigger or result.

1. **Start Events** (thin circle)
   - Simple Start Event: Unspecified trigger
   - Message Start Event: Receipt of a message
   - Timer Start Event: Specific time/date or cycle
   - Conditional Start Event: Condition becomes true
   - Signal Start Event: Signal broadcast received

2. **Intermediate Events** (double-line circle)
   - Message Intermediate Event: Send/receive messages
   - Timer Intermediate Event: Delay or schedule
   - Error Intermediate Event: Named error caught
   - Escalation Intermediate Event: Escalation triggered
   - Conditional Intermediate Event: Condition monitoring
   - Link Intermediate Event: Off-page connectors
   - Signal Intermediate Event: Signal broadcast/catch

3. **End Events** (thick circle)
   - Simple End Event: Process completes
   - Message End Event: Send final message
   - Error End Event: Throw error to parent
   - Escalation End Event: Trigger escalation
   - Terminate End Event: Force immediate termination
   - Signal End Event: Broadcast signal at end

**Activities**

1. **Tasks** (rounded rectangle)
   - Service Task: Automated service call
   - User Task: Human interaction required
   - Manual Task: Physical task (no system)
   - Business Rule Task: Rule engine execution
   - Script Task: Automated script execution
   - Send Task: Send message
   - Receive Task: Wait for message

2. **Sub-Processes** (rounded rectangle with + icon)
   - Embedded Sub-Process: Contained within parent
   - Call Activity: Reference to reusable process
   - Event Sub-Process: Triggered by events
   - Transaction Sub-Process: Atomic unit of work

3. **Task Markers**
   - Loop Marker (circular arrow): Repeating task
   - Multi-Instance Parallel (three vertical lines): Execute simultaneously
   - Multi-Instance Sequential (three horizontal lines): Execute in sequence
   - Compensation Marker (rewind icon): Undo/rollback capability

**Gateways**

Gateways control how sequence flows interact within a process.

1. **Exclusive Gateway** (diamond with X)
   - Only one path can be taken
   - Based on condition evaluation
   - Default flow available
   - Example: If-then-else logic

2. **Parallel Gateway** (diamond with +)
   - All paths are taken simultaneously
   - Used for forking and joining
   - No conditions evaluated
   - Synchronization point for join

3. **Inclusive Gateway** (diamond with O)
   - One or more paths can be taken
   - Conditions evaluated on each path
   - At least one path must be valid
   - Join waits for all active paths

4. **Event-Based Gateway** (diamond with pentagon)
   - Wait for one of several events
   - First event determines path
   - Used with intermediate events
   - Exclusive choice based on events

5. **Complex Gateway** (diamond with *)
   - Complex conditions
   - Custom synchronization logic
   - Used for advanced scenarios

#### Connecting Objects

**Sequence Flow** (solid arrow)
- Shows order of activities
- Can have conditions (except after parallel gateway)
- Default flow indicated by diagonal slash

**Message Flow** (dashed arrow)
- Communication between participants
- Crosses pool boundaries
- Shows message exchange

**Association** (dotted line)
- Links artifacts to flow objects
- Non-directional or directional
- Does not affect process flow

#### Swimlanes

**Pools** (large container)
- Represents participant/organization
- Contains complete process
- Separated by message flows
- Can be collapsed (black box)

**Lanes** (subdivisions within pool)
- Represents roles/departments
- Organizes activities by responsibility
- Within same organization
- Can be nested for hierarchy

#### Artifacts

**Data Objects**
- Data Object: Information flowing through process
- Data Input: Required input for activity
- Data Output: Produced by activity
- Data Store: Persistent data repository

**Groups** (dashed rectangle)
- Visual grouping mechanism
- No semantic meaning
- For documentation purposes
- Categorization aid

**Annotations** (text with bracket)
- Additional text information
- Clarify or explain elements
- Does not affect execution
- Documentation tool

### BPMN Best Practices

#### Modeling Guidelines

1. **Start with Happy Path**
   - Model the standard flow first
   - Add exceptions after core process
   - Keep it simple initially
   - Iterate to add complexity

2. **Use Descriptive Names**
   - Tasks: Verb + Object (e.g., "Review Application")
   - Events: Object + State (e.g., "Order Received")
   - Gateways: Question format (e.g., "Approved?")
   - Data: Noun + Descriptor (e.g., "Customer Data")

3. **Maintain Proper Granularity**
   - Level 1: High-level process overview (5-10 activities)
   - Level 2: Detailed process steps (10-30 activities)
   - Level 3: Task-level details (use sub-processes)
   - Don't mix levels in same diagram

4. **Balance Detail and Clarity**
   - Aim for one page when printed
   - Use sub-processes for detail
   - Maximum 15-20 elements per diagram
   - Group related activities

5. **Consistent Layout**
   - Left to right flow
   - Top to bottom for alternatives
   - Align elements to grid
   - Minimize crossing lines

#### Common BPMN Patterns

**Pattern 1: Request-Approval-Fulfillment**

```
[Start Event: Request Received]
    ↓
[User Task: Review Request]
    ↓
[Exclusive Gateway: Approved?]
    ↓ Yes                      ↓ No
[Service Task: Process]    [User Task: Reject]
    ↓                          ↓
[End Event: Fulfilled]     [End Event: Rejected]
```

**Pattern 2: Parallel Processing**

```
[Start Event]
    ↓
[Parallel Gateway: Fork]
    ↓              ↓              ↓
[Task A]       [Task B]       [Task C]
    ↓              ↓              ↓
[Parallel Gateway: Join]
    ↓
[End Event]
```

**Pattern 3: Error Handling**

```
[Start Event]
    ↓
[Service Task: Process Payment]
    ↓ (happy path)          ↓ (error boundary)
[End Event: Success]    [Error Event: Payment Failed]
                            ↓
                        [User Task: Manual Review]
                            ↓
                        [End Event: Escalated]
```

**Pattern 4: Timeout Handling**

```
[Start Event]
    ↓
[User Task: Approve Request]
    ↓                          ↓ (timer boundary)
[End Event: Approved]      [Timer Event: 48 hours]
                               ↓
                           [User Task: Escalate]
                               ↓
                           [End Event: Escalated]
```

**Pattern 5: Event-Based Decision**

```
[Start Event]
    ↓
[Event Gateway]
    ↓                  ↓                    ↓
[Message: Email]   [Message: API]      [Timer: Timeout]
    ↓                  ↓                    ↓
[Task A]           [Task B]             [Task C]
```

### Advanced BPMN Concepts

#### Compensation

Used to undo completed activities when process fails later.

```
[Task: Book Flight] (with compensation handler)
    ↓
[Task: Book Hotel] (with compensation handler)
    ↓
[Task: Charge Card] → [Error Event: Payment Failed]
    ↓                        ↓
[End: Success]          [Trigger Compensation]
                            ↓
                        [Cancel Hotel] → [Cancel Flight]
                            ↓
                        [End: Cancelled]
```

#### Transaction Sub-Process

Atomic unit of work with built-in compensation.

```
[Transaction Sub-Process: Purchase Package]
    Contains:
    - Book Flight
    - Book Hotel
    - Process Payment

If any fails:
    - All compensated automatically
    - Hazard Event: Partial completion warning
    - Cancel Event: Full rollback
```

#### Choreography

Shows interaction between participants without assigning to pools.

```
[Choreography Task: Customer Places Order]
    ↓
[Choreography Task: Merchant Confirms Stock]
    ↓
[Choreography Task: Customer Provides Payment]
    ↓
[Choreography Task: Merchant Ships Order]
```

---

## Swimlane Diagrams

### Overview

Swimlane diagrams (also called Rummler-Brache diagrams) organize process activities into lanes representing different actors, departments, or systems responsible for those activities.

### Components

#### Lanes

**Horizontal Lanes** (most common)
- Each lane represents a different actor/role
- Process flows left to right
- Handoffs cross lane boundaries
- Clear responsibility assignment

**Vertical Lanes** (less common)
- Process flows top to bottom
- Used when horizontal space limited
- Same principles apply

**Lane Types**

1. **Role-Based Lanes**
   - Customer
   - Sales Representative
   - Order Fulfillment
   - Finance
   - IT Support

2. **Department-Based Lanes**
   - Marketing
   - Sales
   - Operations
   - Customer Service
   - Management

3. **System-Based Lanes**
   - Manual Process
   - CRM System
   - ERP System
   - Email
   - Reporting System

4. **Hybrid Lanes**
   - Customer (external)
   - Front Office (human)
   - Back Office (human)
   - Core Systems (automated)

#### Process Elements

**Activities in Lanes**
- Placed in responsible actor's lane
- Shape indicates activity type
- Connected by flow lines
- Decision points shown as diamonds

**Handoffs**
- Flow lines crossing lane boundaries
- Represent transfer of responsibility
- Document what is transferred
- May indicate delays or friction

**Documents/Data**
- Show information flow
- Can cross lanes
- Indicate inputs/outputs
- Reference or create data

### Design Principles

#### 1. Clear Responsibility

Each activity must be in exactly one lane:
- No ambiguous ownership
- Clear accountability
- Easy to identify bottlenecks
- Facilitates improvement

#### 2. Minimize Handoffs

Handoffs create risk:
- Potential for delay
- Information loss
- Quality issues
- Coordination overhead

Strategies:
- Consolidate activities in single lane
- Automate handoffs where possible
- Create clear handoff protocols
- Measure handoff quality

#### 3. Logical Flow

Process should flow naturally:
- Minimize backtracking
- Group related activities
- Reduce cross-lane jumps
- Clear start and end points

#### 4. Appropriate Granularity

Balance detail with clarity:
- High-level: 5-15 activities
- Detailed: 15-30 activities
- Use sub-processes for detail
- One process per diagram

### Swimlane Diagram Examples

#### Example 1: Customer Onboarding Process

```
Lane: Customer
[Submit Application] → [Provide Documents] → [Sign Contract] → [Receive Welcome Kit]

Lane: Sales Team
                      [Review Application] → [Request Documents] → [Prepare Contract] → [Deliver Welcome Kit]
                           ↓ Approved?
                      [Process Onboarding]

Lane: Credit Team
                      [Credit Check] → [Approve/Reject] → [Update System]

Lane: Operations
                                                              [Create Account] → [Send Credentials] → [Schedule Training]

Lane: IT Systems
                                                              [CRM Update] → [Provision Access] → [Generate Reports]
```

Handoffs:
1. Customer → Sales: Application submission
2. Sales → Credit: Credit check request
3. Credit → Sales: Approval decision
4. Sales → Operations: Account creation request
5. Operations → Customer: Welcome kit delivery

#### Example 2: Expense Approval Process

```
Lane: Employee
[Submit Expense] → [Receive Decision] → [Receive Reimbursement]

Lane: Manager
                [Review Expense] → [Approve/Reject] → [Forward to Finance]
                      ↓ Amount?
                [Over $500] → [Escalate to Director]

Lane: Director
                                  [Review High-Value] → [Approve/Reject]

Lane: Finance
                                                        [Validate Expense] → [Process Payment] → [Update Records]

Lane: Accounting System
                                                                            [Generate Payment] → [Record Transaction]
```

Key Observations:
- Clear approval hierarchy
- Escalation path defined
- System automation at end
- Feedback to employee

#### Example 3: Software Development Workflow

```
Lane: Product Owner
[Define Story] → [Prioritize Backlog] → [Accept Story] → [Deploy to Production]

Lane: Developer
              [Pick Story] → [Develop] → [Unit Test] → [Submit PR] → [Fix Issues]

Lane: QA Engineer
                                         [Test Story] → [Report Bugs] → [Verify Fixes] → [Approve Release]

Lane: DevOps
                                                                                        [Build] → [Deploy Staging] → [Deploy Production]

Lane: CI/CD System
                            [Run Tests] → [Build Artifact] → [Automated Tests]
```

Handoffs:
1. Product → Developer: Story assignment
2. Developer → QA: Code for testing
3. QA → Developer: Bug reports (may loop)
4. QA → DevOps: Approval for release
5. DevOps → Product: Production deployment

### Analysis Techniques

#### Handoff Analysis

Count and evaluate each handoff:

| From Lane | To Lane | Transfer | Delay Risk | Frequency | Priority |
|-----------|---------|----------|------------|-----------|----------|
| Customer | Sales | Application | Medium | High | P1 |
| Sales | Credit | Credit Request | High | High | P1 |
| Credit | Sales | Decision | Low | High | P2 |
| Sales | Operations | Account Setup | Medium | High | P1 |

Improvement Opportunities:
- High delay risk + High frequency = Top priority
- Automate where possible
- Create SLAs for handoffs
- Implement tracking/monitoring

#### Time-Value Analysis

Add time and value metrics:

| Activity | Lane | Time | Value Add | Wait Time |
|----------|------|------|-----------|-----------|
| Submit Application | Customer | 30 min | Yes | 0 |
| Review Application | Sales | 2 hours | Yes | 24 hours |
| Credit Check | Credit | 1 hour | Yes | 8 hours |
| Create Account | Operations | 30 min | Yes | 16 hours |

Findings:
- Wait time exceeds process time 10:1
- Most waiting happens at handoffs
- Only 4.5 hours of actual work in 48-hour process
- 90% of time is non-value-adding wait

---

## Value Stream Mapping

### Overview

Value Stream Mapping (VSM) is a Lean manufacturing technique adapted for knowledge work. It visualizes the flow of materials and information required to deliver a product or service to the customer.

### Core Concepts

#### Value vs. Waste

**Value-Adding Activities**
- Customer willing to pay for it
- Transforms product/service
- Done right the first time
- Moves closer to customer need

Examples:
- Writing code that meets requirements
- Manufacturing a component
- Providing customer support
- Designing a feature

**Non-Value-Adding but Necessary**
- Required for business/compliance
- Customer won't pay for directly
- Cannot eliminate immediately
- Should minimize

Examples:
- Quality inspections
- Approval processes
- Compliance documentation
- Security reviews

**Pure Waste (Muda)**
- Adds no value
- Customer won't pay for it
- Should eliminate
- Eight types defined by Lean

#### The 8 Wastes (TIM WOODS)

1. **Transportation**
   - Moving materials, information, or people
   - Handoffs between teams
   - Transferring files/data
   - Relocation of work

2. **Inventory**
   - Work in progress (WIP)
   - Queues and backlogs
   - Partially completed work
   - Unreleased features

3. **Motion**
   - Unnecessary movement
   - Searching for information
   - Switching contexts
   - Multiple tools/systems

4. **Waiting**
   - Idle time between activities
   - Approval delays
   - Dependencies blocking progress
   - Information requests

5. **Overproduction**
   - Producing more than needed
   - Building unused features
   - Excessive documentation
   - Premature optimization

6. **Over-processing**
   - More work than necessary
   - Excessive quality checks
   - Redundant approvals
   - Unnecessary complexity

7. **Defects**
   - Errors and mistakes
   - Rework and corrections
   - Bug fixes
   - Customer complaints

8. **Skills (underutilization)**
   - Not using people's talents
   - Overqualified for tasks
   - Lack of training
   - Poor delegation

### VSM Symbols and Notation

#### Process Boxes

```
┌─────────────────┐
│  Process Name   │
│                 │
│  C/T = 2 hours  │  (Cycle Time)
│  C/O = 30 min   │  (Changeover)
│  Uptime = 85%   │
│  FTT = 90%      │  (First Time Through)
└─────────────────┘
```

#### Inventory Triangles

```
    ▼
   WIP
  5 days
```
Shows work sitting between processes.

#### Data Boxes

```
┌──────────────┐
│ Daily Demand │
│   100 units  │
│              │
│ Batch Size   │
│   20 units   │
└──────────────┘
```

#### Push Arrow

```
────────>
```
Indicates push system (produce without demand signal).

#### Pull Signal

```
- - - - >
```
Indicates pull system (produce based on demand).

#### Information Flow

```
⚡ (Lightning bolt)
```
Electronic information flow.

```
📄→ (Paper with arrow)
```
Manual information flow.

#### Timeline

```
Value-Add Time:    █ 2h  █ 1h  █ 3h    = 6 hours
Non-Value Time:  ▬▬▬ 2d ▬▬▬ 5d ▬▬▬    = 7 days

Lead Time = 7 days 6 hours
```

### Creating a Current State Map

#### Step 1: Define Scope

**Start and End Points**
- Customer request (start)
- Customer receives value (end)
- Don't start too broad
- Focus on specific value stream

**Boundaries**
- What's included
- What's excluded
- Interface points
- Dependencies

#### Step 2: Walk the Process

**Physical Observation**
- Follow actual process
- Don't rely on documentation
- Talk to people doing work
- Collect real data

**Data Collection**
- Cycle time (C/T): Time to complete when working
- Lead time (L/T): Total elapsed time
- Changeover time (C/O): Time to switch between items
- Uptime/reliability
- First-time-through (FTT) quality
- Number of people
- Working time available
- Batch sizes
- Queue sizes

#### Step 3: Map Material/Work Flow

```
[Customer] ──Order──> [Process 1] ──WIP──> [Process 2] ──WIP──> [Shipping]
                          │                    │
                       ▼ WIP                ▼ WIP
                       2 days               5 days
```

#### Step 4: Map Information Flow

```
[Sales Forecast]
       │
       ▼
[Production Control]
       │
       ├─────> [Process 1] (daily schedule)
       │
       └─────> [Process 2] (weekly schedule)
```

#### Step 5: Add Timeline

```
Process:     [P1]     [P2]     [P3]     [P4]
Value-Add:    2h       1h       3h       2h    = 8 hours
Wait Time:  ▬3d▬    ▬5d▬     ▬2d▬            = 10 days

Total Lead Time: 10 days 8 hours
Process Efficiency: 8h / 248h = 3.2%
```

#### Step 6: Calculate Metrics

**Lead Time**
Total time from start to finish (including wait time).

**Process Time (Value-Add Time)**
Actual time working on the item.

**Process Cycle Efficiency (PCE)**
```
PCE = Value-Add Time / Lead Time × 100%
```

Target: >25% for knowledge work, >50% for manufacturing

**Takt Time**
```
Takt Time = Available Working Time / Customer Demand
```
Example: 8 hours × 60 min / 100 orders = 4.8 min/order

**Throughput**
Units completed per time period.

### Example: Software Feature Development VSM

#### Current State Map

```
[Product Owner]
    │ Monthly Priority List
    ▼
┌──────────┐  ▼WIP      ┌──────────┐  ▼WIP      ┌──────────┐  ▼WIP      ┌──────────┐
│  Backlog │  30 stories │   Dev    │  10 stories│    QA    │  8 stories │  Deploy  │
│          │→ ▬▬▬▬▬▬▬▬→│          │→ ▬▬▬▬▬▬▬→│          │→ ▬▬▬▬▬▬→│          │
│          │   15 days  │  C/T=3d  │   5 days  │  C/T=2d  │   3 days  │  C/T=1d  │
│          │            │  FTT=70% │           │  FTT=80% │           │  FTT=95% │
└──────────┘            └──────────┘           └──────────┘           └──────────┘

Timeline:
Value-Add:             3 days        2 days        1 day      = 6 days
Wait Time:          15 days        5 days        3 days      = 23 days

Total Lead Time: 29 days
PCE: 6/29 = 20.7%
```

**Observations:**
- Low first-time-through quality in dev (70%)
- Large WIP in backlog (30 stories)
- Long wait times between stages
- PCE below target (20.7% < 25%)

### Future State Design

#### Principles

1. **Design to Takt Time**
   - Match capacity to demand
   - Don't overproduce
   - Balance workloads

2. **Develop Continuous Flow**
   - Eliminate batching where possible
   - Reduce WIP
   - Single-piece flow ideal
   - Small batches if batching needed

3. **Use Pull Systems**
   - Downstream signals upstream
   - Kanban systems
   - WIP limits
   - Demand-driven

4. **Level the Load**
   - Distribute work evenly
   - Avoid peaks and valleys
   - Smooth scheduling
   - Heijunka boards

5. **Build in Quality**
   - Stop and fix problems
   - Jidoka (autonomation)
   - Error-proofing (poke-yoke)
   - Right first time

6. **Standardize**
   - Standard work processes
   - Best practices documented
   - Baseline for improvement
   - Consistency

#### Example: Software Development Future State

```
[Product Owner]
    │ Weekly Priority (WIP Limit: 10)
    ▼ PULL
┌──────────┐  ▼WIP      ┌──────────┐  ▼WIP      ┌──────────┐
│ Ready    │  5 stories │   Dev+QA │  3 stories │  Deploy  │
│          │→ ▬▬▬▬▬▬▬→│ (paired) │→ ▬▬▬▬▬▬→│ (auto)   │
│          │   3 days  │  C/T=3d  │   1 day   │  C/T=1h  │
│          │           │  FTT=90% │           │  FTT=99% │
└──────────┘           └──────────┘           └──────────┘

Timeline:
Value-Add:             3 days        1 hour       = 3 days
Wait Time:           3 days        1 day          = 4 days

Total Lead Time: 7 days
PCE: 3/7 = 42.9%
```

**Improvements:**
- Dev and QA working together (FTT 70%→90%)
- Reduced WIP (30→5 in backlog)
- Automated deployment (1d→1h)
- Pull system with WIP limits
- Lead time reduced 29d→7d
- PCE improved 20.7%→42.9%

---

## Six Sigma DMAIC

### Overview

DMAIC (Define, Measure, Analyze, Improve, Control) is the Six Sigma methodology for process improvement. It provides a structured, data-driven approach to solving problems and improving processes.

### Six Sigma Fundamentals

#### What is Six Sigma?

**Quality Level**
- 3.4 defects per million opportunities (DPMO)
- 99.99966% quality level
- Statistical measurement of variation
- Target for process excellence

**Sigma Levels:**

| Sigma | DPMO | Yield | Example |
|-------|------|-------|---------|
| 1σ | 690,000 | 31% | Unsafe at any speed |
| 2σ | 308,000 | 69% | Average company performance |
| 3σ | 66,800 | 93.3% | Many current processes |
| 4σ | 6,210 | 99.38% | Good process performance |
| 5σ | 230 | 99.977% | High performance |
| 6σ | 3.4 | 99.99966% | World class |

#### Key Concepts

**CTQ (Critical to Quality)**
- Customer requirements
- Measurable characteristics
- Defines quality
- Translated from VOC

**Defect**
- Any instance of not meeting CTQ
- Measured and counted
- Basis for DPMO calculation
- Focus of improvement

**Process Capability**
- Cp: Potential capability (assumes perfect centering)
- Cpk: Actual capability (accounts for centering)
- Target: Cpk ≥ 1.33 (4σ) or ≥ 2.0 (6σ)

**Variation**
- Common cause: Inherent to process
- Special cause: External factors
- Reduce both types
- Statistical control

### Phase 1: Define

#### Purpose
Clearly define the problem, project scope, and customer requirements.

#### Key Activities

**1. Create Project Charter**

Components:
- Business case
- Problem statement
- Goal statement
- Project scope
- Team members
- Timeline
- Expected benefits

Example Problem Statement:
"Customer complaint resolution time has increased from 24 hours to 72 hours over the past 6 months, resulting in a 15% decrease in customer satisfaction scores."

Example Goal Statement:
"Reduce complaint resolution time from 72 hours to 24 hours within 3 months while maintaining or improving resolution quality."

**2. Identify Customers**

External Customers:
- End users
- Buyers
- Service recipients
- Beneficiaries

Internal Customers:
- Downstream processes
- Other departments
- Management
- Employees

**3. Voice of Customer (VOC)**

Collection Methods:
- Surveys and questionnaires
- Interviews (structured/unstructured)
- Focus groups
- Customer complaints
- Sales feedback
- Social media analysis
- Customer observation

**4. Define CTQ Requirements**

CTQ Tree Example:

```
Need: Fast Service
├── Short wait time
│   ├── CTQ: Queue time < 2 minutes
│   └── CTQ: Ring time < 3 rings
├── Quick resolution
│   ├── CTQ: Resolve in first call 80%+
│   └── CTQ: Total resolution < 24 hours
└── Easy access
    ├── CTQ: Available 24/7
    └── CTQ: Multiple contact channels
```

**5. Create SIPOC Diagram**

SIPOC = Suppliers, Inputs, Process, Outputs, Customers

Example: Order Fulfillment

| Suppliers | Inputs | Process | Outputs | Customers |
|-----------|--------|---------|---------|-----------|
| Customer | Order | 1. Receive order | Shipped product | Customer |
| Warehouse | Inventory | 2. Check inventory | Tracking number | Sales |
| Shipping vendor | Boxes | 3. Pick items | Invoice | Finance |
| IT system | Order data | 4. Pack order | Delivery confirmation | Customer service |
| | | 5. Ship order | | |

#### Deliverables

- Project charter (approved)
- SIPOC diagram
- CTQ requirements
- High-level process map
- Stakeholder analysis

### Phase 2: Measure

#### Purpose
Establish baseline performance and develop data collection plan.

#### Key Activities

**1. Select Process Metrics**

**Y Variables (Outputs - What we want to improve):**
- Customer satisfaction score
- Defect rate
- Cycle time
- Cost per unit
- On-time delivery rate

**X Variables (Inputs - What affects Y):**
- Process parameters
- Environmental factors
- Material characteristics
- Human factors
- Equipment settings

**2. Develop Measurement System**

**Data Types:**

Continuous Data:
- Can take any value
- Examples: time, temperature, weight
- More powerful for analysis
- Preferred when possible

Discrete Data:
- Countable
- Examples: defects, complaints, errors
- Attribute data (pass/fail)
- Easier to collect

**3. Validate Measurement System**

**Gage R&R (Repeatability & Reproducibility) Study:**

Tests measurement system for:
- Repeatability: Same operator, same part, multiple times
- Reproducibility: Different operators, same part
- Accuracy: Comparison to standard
- Precision: Consistency of measurements

Acceptance Criteria:
- %GR&R < 10%: Acceptable
- %GR&R 10-30%: Marginal (may be acceptable)
- %GR&R > 30%: Unacceptable (fix measurement system)

**4. Collect Baseline Data**

Sample Size Considerations:
- Larger samples = more confidence
- Consider time, cost, practicality
- Minimum 30 data points recommended
- Use statistical calculations for precision

Data Collection Plan:

| Metric | Definition | Target | Data Source | Collection Method | Frequency | Responsible |
|--------|-----------|--------|-------------|-------------------|-----------|-------------|
| Resolution Time | Hours from receipt to close | <24h | CRM system | Automated export | Daily | Team Lead |
| First Call Resolution | % resolved in first contact | >80% | Call records | Manual review | Weekly | QA Analyst |

**5. Calculate Baseline Sigma**

Steps:
1. Count defects
2. Count opportunities
3. Calculate DPMO
4. Convert to Sigma level

Example:
- 100 orders processed
- 5 opportunities per order = 500 total opportunities
- 8 defects found
- DPMO = (8 / 500) × 1,000,000 = 16,000
- Sigma level ≈ 3.7σ

#### Deliverables

- Data collection plan
- Baseline performance metrics
- Measurement system analysis
- Process capability analysis
- Current sigma level

### Phase 3: Analyze

#### Purpose
Identify root causes of defects and performance gaps using data analysis.

#### Key Activities

**1. Analyze Process Flow**

Techniques:
- Value stream mapping
- Spaghetti diagrams
- Swim lane diagrams
- Process cycle efficiency

Look for:
- Non-value-adding steps
- Rework loops
- Wait times
- Handoffs

**2. Statistical Analysis**

**Descriptive Statistics:**
- Mean, median, mode
- Standard deviation
- Range
- Quartiles

**Graphical Analysis:**

Histogram:
- Shows distribution
- Identifies centering
- Reveals patterns

Box Plot:
- Shows median, quartiles
- Identifies outliers
- Compares groups

Run Chart:
- Plots over time
- Shows trends
- Identifies shifts

Control Chart:
- Distinguishes common/special cause
- Monitors stability
- Detects patterns

**3. Root Cause Analysis**

**Fishbone Diagram (Ishikawa):**

```
                    Long Resolution Time
                           │
    Methods          Materials        Machines
        │                │                │
    No standard ─┐       │           Slow ─┤
    process      ├───────┼────────────────┼────────
                 │       │                │
    Complex ─────┘   Limited info    Old system
                         │                │
                    Measurements      People
```

**6 M Categories:**
- Methods: Procedures, processes
- Materials: Inputs, supplies
- Machines: Equipment, technology
- Measurements: Data, metrics
- Mother Nature: Environment
- People: Training, skills

**5 Whys Technique:**

Problem: Customer complaints are increasing

1. Why? Resolution times are too long
2. Why? Agents can't find information quickly
3. Why? Knowledge base is outdated and poorly organized
4. Why? No process for updating it
5. Why? No owner assigned for knowledge management

Root Cause: Lack of knowledge management ownership

**4. Hypothesis Testing**

Test relationships between X's and Y:

Example Hypotheses:
- H0: Agent training level has no effect on resolution time
- H1: More training leads to faster resolution

Statistical Tests:
- t-test: Compare two groups
- ANOVA: Compare multiple groups
- Chi-square: Test independence (categorical)
- Regression: Quantify relationships

Significance Level:
- α = 0.05 (standard)
- p-value < 0.05 = statistically significant
- Reject null hypothesis

**5. Identify Vital Few X's**

From many possible causes, identify vital few:

Pareto Analysis (80/20 rule):
- 80% of problems from 20% of causes
- Focus on vital few
- Prioritize improvement efforts

Example:
```
Cause             | Defects | % | Cumulative %
------------------|---------|---|-------------
Knowledge gaps    | 45      | 45% | 45%
System complexity | 25      | 25% | 70%
Inadequate tools  | 15      | 15% | 85%
Training issues   | 10      | 10% | 95%
Other             | 5       | 5%  | 100%
```

Focus on top 3 causes (85% of defects).

#### Deliverables

- Root cause analysis
- Statistical analysis results
- Hypothesis test results
- Vital few X's identified
- Verified cause-and-effect relationships

### Phase 4: Improve

#### Purpose
Develop, test, and implement solutions that address root causes.

#### Key Activities

**1. Generate Solutions**

Brainstorming Techniques:
- Traditional brainstorming
- Brainwriting (6-3-5 method)
- SCAMPER (Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse)
- Mind mapping

Solution Categories:
- Eliminate: Remove non-value steps
- Simplify: Reduce complexity
- Automate: Use technology
- Standardize: Create consistency
- Error-proof: Prevent mistakes (poka-yoke)

**2. Evaluate Solutions**

Impact-Effort Matrix:

```
High Impact │ Plan      │ DO IT!
            │ Carefully │
            ├───────────┼─────────
Low Impact  │ Forget It │ Quick
            │           │ Wins
            └───────────┴─────────
              High Effort Low Effort
```

Prioritize: High impact, low effort (quick wins) first

**3. Pilot Solutions**

Design of Experiments (DOE):

Purpose:
- Test multiple factors simultaneously
- Understand interactions
- Optimize settings
- Efficient testing

Example 2³ Factorial Design:

Factors:
- A: Training (current vs. enhanced)
- B: Tool (old vs. new)
- C: Process (current vs. simplified)

8 Test Conditions:
1. Current training, old tool, current process
2. Enhanced training, old tool, current process
3. Current training, new tool, current process
4. Enhanced training, new tool, current process
5. Current training, old tool, simplified process
6. Enhanced training, old tool, simplified process
7. Current training, new tool, simplified process
8. Enhanced training, new tool, simplified process

Analyze results to find optimal combination.

**Pilot Testing Steps:**
1. Define pilot scope (small, controlled)
2. Set success criteria
3. Establish monitoring plan
4. Run pilot
5. Collect data
6. Analyze results
7. Refine solution
8. Get approval to implement

**4. Implement Solution**

Implementation Plan Components:
- Detailed action steps
- Responsible parties
- Timeline/milestones
- Resources required
- Training needs
- Communication plan
- Risk mitigation
- Quick wins

Change Management:
- Stakeholder engagement
- Communication strategy
- Training program
- Support structure
- Resistance management

**5. Verify Improvement**

Before/After Comparison:

| Metric | Baseline | Target | Actual | Improvement |
|--------|----------|--------|--------|-------------|
| Resolution Time | 72h | 24h | 26h | 64% |
| First Call Resolution | 65% | 80% | 78% | 20% |
| Customer Satisfaction | 3.5/5 | 4.2/5 | 4.1/5 | 17% |
| Sigma Level | 3.2σ | 4.0σ | 3.9σ | 21% |

Statistical Verification:
- Control charts showing improvement
- Process capability improved
- Variation reduced
- Sustainable performance

#### Deliverables

- Solution recommendations
- Pilot test results
- Implementation plan
- Training materials
- Updated process documentation
- Before/after comparison

### Phase 5: Control

#### Purpose
Sustain improvements and ensure gains are maintained over time.

#### Key Activities

**1. Document New Process**

Standard Operating Procedures (SOPs):
- Step-by-step instructions
- Decision criteria
- Quality checks
- Escalation procedures
- Tools and templates

Process Control Plan:

| Process Step | CTQ | Specification | Measurement Method | Sample Size | Frequency | Response Plan |
|--------------|-----|---------------|-------------------|-------------|-----------|---------------|
| Receive complaint | Response time | <5 min | System timestamp | All | Continuous | Alert supervisor if >5 min |
| Initial diagnosis | Accuracy | >90% | QA review | 20/day | Daily | Retrain if <90% |

**2. Implement Process Controls**

Visual Management:
- Dashboard displays
- KPI boards
- Status indicators
- Trend charts

Mistake-Proofing (Poka-Yoke):
- Physical: Design prevents errors
- Detection: Sensor catches errors
- Warning: Alert before error occurs
- Examples: Dropdown lists, validation rules, checklists

Automated Controls:
- System validation
- Alerts and notifications
- Workflow enforcement
- Data capture

**3. Monitor Performance**

Control Charts:

Types:
- X-bar & R chart: Continuous data (mean and range)
- Individual-X & MR chart: Individual measurements
- p-chart: Proportion defective
- c-chart: Count of defects

Control Limits:
- Upper Control Limit (UCL) = μ + 3σ
- Center Line (CL) = μ
- Lower Control Limit (LCL) = μ - 3σ

Out-of-Control Signals:
- Point beyond control limits
- 7 points in a row above/below center
- 7 points trending up/down
- 14 points alternating up/down
- 2 out of 3 points beyond 2σ

**4. Create Response Plans**

Action triggers:
- What conditions require action?
- Who is responsible?
- What actions to take?
- How to document?

Example Response Plan:

IF resolution time > 30 hours:
1. Supervisor reviews case within 1 hour
2. Escalate to senior agent if needed
3. Document reason for delay
4. Update customer every 4 hours
5. Review in weekly meeting

**5. Transfer Ownership**

Handoff Process:
1. Train process owners
2. Demonstrate monitoring
3. Review response plans
4. Transfer documentation
5. Schedule follow-up reviews
6. Close project

Ongoing Reviews:
- Weekly: Check dashboard
- Monthly: Review trends
- Quarterly: Process audit
- Annually: Full reassessment

#### Deliverables

- Standard operating procedures
- Process control plan
- Control charts
- Response plans
- Training completion records
- Project closeout report
- Benefits realization summary

---

## Process Mining Techniques

### Overview

Process mining uses event log data from IT systems to automatically discover, monitor, and improve real processes. It bridges the gap between data science and process science.

### Three Types of Process Mining

#### 1. Process Discovery

**Purpose:** Automatically create process models from event logs.

**Input:** Event log with:
- Case ID (process instance)
- Activity name
- Timestamp
- Additional attributes

**Output:** Process model showing:
- Activities performed
- Order of activities
- Frequencies
- Variants

**Algorithms:**

Alpha Algorithm:
- First process discovery algorithm
- Works on simple processes
- Clear start/end activities
- No noise tolerance

Heuristic Miner:
- Handles noise better
- Works with complex logs
- Adjustable parameters
- Most commonly used

Inductive Miner:
- Guarantees sound models
- Good for imperfect logs
- Handles noise well
- Preferred for quality

**Example Event Log:**

| Case ID | Activity | Timestamp | Resource | Cost |
|---------|----------|-----------|----------|------|
| 001 | Receive Order | 2025-01-01 09:00 | System | $0 |
| 001 | Check Credit | 2025-01-01 09:15 | Agent A | $25 |
| 001 | Approve Order | 2025-01-01 10:30 | Manager | $50 |
| 001 | Ship Order | 2025-01-02 14:00 | Warehouse | $100 |
| 002 | Receive Order | 2025-01-01 09:30 | System | $0 |
| 002 | Check Credit | 2025-01-01 09:45 | Agent B | $25 |
| 002 | Reject Order | 2025-01-01 10:00 | Manager | $50 |

**Discovered Process:**

```
[Receive Order]
    ↓
[Check Credit]
    ↓ 80%                ↓ 20%
[Approve Order]      [Reject Order]
    ↓                    ↓
[Ship Order]         [END]
    ↓
[END]
```

#### 2. Conformance Checking

**Purpose:** Compare actual process execution (event log) against intended process (model).

**Detects:**
- Deviations from standard process
- Skipped activities
- Repeated activities
- Different activity order
- Compliance violations

**Metrics:**

Fitness (0-1):
- How much of the log can model explain?
- 1.0 = Perfect fit
- <0.9 = Significant deviations

Precision (0-1):
- How much behavior does model allow that's not in log?
- 1.0 = Only observed behavior allowed
- Low precision = Model too general

**Example:**

Standard Process:
```
[A] → [B] → [C] → [D]
```

Actual Executions:
```
Case 1: [A] → [B] → [C] → [D]  ✓ Conforming
Case 2: [A] → [C] → [B] → [D]  ✗ B and C swapped
Case 3: [A] → [B] → [D]        ✗ C skipped
Case 4: [A] → [B] → [B] → [C] → [D]  ✗ B repeated
```

Fitness: 1/4 = 0.25 (only 1 case conforms perfectly)

**3. Enhancement**

**Purpose:** Improve or extend process models using event log information.

**Adds to Model:**
- Performance data (times)
- Resource information
- Costs
- Decision rules
- Bottlenecks

**Types:**

Repair:
- Fix discovered model
- Add missing elements
- Remove incorrect elements
- Improve model quality

Extension:
- Add timestamps
- Calculate waiting times
- Show resource allocation
- Display costs
- Identify bottlenecks

**Example Enhanced Model:**

```
[Receive Order]
    ↓ (Avg: 15 min, Resource: System, Cost: $0)
[Check Credit]
    ↓ 80% (Avg: 1.25h, Resource: Agents, Cost: $25)  ↓ 20% (Avg: 15m, Cost: $25)
[Approve Order] ←← BOTTLENECK                     [Reject Order]
    ↓ (Avg: 18h wait, then 2h work)                 ↓
[Ship Order]                                       [END]
    ↓ (Avg: 3h, Cost: $100)
[END]
```

### Process Mining Workflow

#### Step 1: Define Objective

Questions to Answer:
- What process to analyze?
- What questions need answers?
- What improvements sought?
- Who are stakeholders?

Example Objectives:
- Reduce order-to-cash cycle time
- Improve compliance rates
- Identify automation opportunities
- Optimize resource allocation

#### Step 2: Extract Event Logs

Data Sources:
- ERP systems (SAP, Oracle)
- CRM systems (Salesforce)
- Workflow systems (Jira, ServiceNow)
- Custom applications
- Databases

Required Fields:
- Case ID (mandatory)
- Activity name (mandatory)
- Timestamp (mandatory)
- Resource (optional but valuable)
- Other attributes (costs, departments, etc.)

Data Quality Checks:
- Complete timestamps
- Consistent activity names
- Valid case IDs
- No missing mandatory fields
- Reasonable date ranges

#### Step 3: Prepare Data

Cleaning:
- Remove test cases
- Filter incomplete cases
- Handle missing values
- Standardize activity names
- Convert timestamps to proper format

Enrichment:
- Add derived attributes
- Calculate durations
- Merge with master data
- Add organizational context

Filtering:
- Select time period
- Choose specific variants
- Focus on subset of activities
- Sample if dataset too large

#### Step 4: Discover Process

Tools:
- Disco (Fluxicon) - Commercial, user-friendly
- ProM - Open source, academic
- Celonis - Enterprise platform
- QPR ProcessAnalyzer - Commercial
- Signavio - Commercial
- UiPath Process Mining - Commercial

Settings:
- Select discovery algorithm
- Set noise threshold
- Choose simplification level
- Define activity grouping

#### Step 5: Analyze Results

Key Analyses:

**Variant Analysis:**
- How many different paths?
- Which variants most common?
- Which variants are outliers?
- Should variants be reduced?

**Performance Analysis:**
- Where are bottlenecks?
- What causes delays?
- Which activities take longest?
- Where is waiting time?

**Conformance Analysis:**
- How many deviations?
- What types of deviations?
- Are deviations problematic?
- Compliance violations?

**Resource Analysis:**
- Who performs activities?
- Resource utilization rates?
- Handover patterns?
- Workload distribution?

#### Step 6: Identify Improvements

Common Findings:

Rework Loops:
- Activities repeated
- Quality issues
- Unclear requirements
- → Improve quality checks, training

Long Waiting Times:
- Work sitting idle
- Dependencies blocking work
- Resource unavailability
- → Balance capacity, parallelize work

Process Variants:
- Too many different paths
- Inconsistent execution
- No standardization
- → Standardize process, provide guidance

Manual Activities:
- Repetitive tasks
- System integration gaps
- Data entry
- → Automate where possible

#### Step 7: Simulate and Validate

What-if Analysis:
- Model proposed changes
- Simulate future state
- Predict impact
- Test assumptions

Simulation Inputs:
- Arrival rates
- Activity durations
- Resource availability
- Decision probabilities
- Costs

Simulation Outputs:
- Cycle time predictions
- Resource utilization
- Bottleneck identification
- Cost estimates
- Capacity requirements

### Advanced Process Mining

#### Social Network Analysis

Analyze handover patterns:

```
Handover Matrix:
                Receiver
              A    B    C    D
Sender  A     -    45   12   3
        B     8    -    67   15
        C     2    34   -    89
        D     1    5    23   -
```

Insights:
- Frequent handovers: B→C (67), C→D (89)
- Infrequent handovers: A→D (3), D→A (1)
- Central roles: C (high incoming/outgoing)
- Isolated roles: A→B→C→D sequential pattern

#### Organizational Mining

Discover organizational structure from process execution:

Clusters Based on:
- Similar activities performed
- Frequent collaboration
- Common case handling
- Shared resources

Example Discovery:
```
Team 1: Activities A, B, E (Front office)
Team 2: Activities C, D (Back office)
Team 3: Activities F, G (Fulfillment)
```

#### Decision Mining

Extract decision rules from data:

Example:
- When is credit check approved vs. rejected?
- Analysis of 1000 cases shows:
  - IF Credit Score > 700 AND Order Value < $10,000 → Approve (98%)
  - IF Credit Score > 650 AND Customer Age > 5 years → Approve (92%)
  - ELSE → Manual Review

Rules extracted can be:
- Automated in system
- Used for training
- Standardized across team
- Documented in procedures

---

## Integration Patterns

### Combining Frameworks

#### BPMN + Value Stream Mapping

Use VSM for high-level analysis:
- Identify waste and delays
- Calculate lead times
- Find bottlenecks

Then use BPMN for detailed design:
- Document precise workflows
- Design exception handling
- Create executable processes
- Add business rules

#### Process Mining + Six Sigma

Process mining for Measure/Analyze phases:
- Automated data collection
- Discover actual process
- Identify variations
- Measure performance

Six Sigma for Improve/Control:
- Root cause analysis
- Solution development
- Implementation planning
- Control mechanisms

#### Value Stream Mapping + Process Mining

Process mining validates VSM:
- Confirms actual vs. documented
- Provides objective data
- Shows all variants
- Measures actual times

VSM provides context:
- Customer perspective
- Value vs. waste
- Improvement priorities
- Future state vision

### Framework Selection Guide

| Situation | Recommended Framework |
|-----------|----------------------|
| Well-documented process, need formal model | BPMN |
| Cross-functional inefficiency | Swimlane Diagram |
| Lead time reduction focus | Value Stream Mapping |
| Quality/defect reduction | Six Sigma DMAIC |
| Large dataset available from IT systems | Process Mining |
| Compliance and governance | BPMN + Conformance Checking |
| New process design | BPMN |
| Existing process improvement | VSM or DMAIC |
| Understanding current state | Process Mining |

---

## References and Standards

### BPMN Standards
- OMG BPMN 2.0 Specification: https://www.omg.org/spec/BPMN/2.0/
- BPMN Method & Style: Bruce Silver
- Real-Life BPMN: Jakob Freund & Bernd Rücker

### Lean/VSM Resources
- Learning to See: Mike Rother & John Shook
- Creating Continuous Flow: Mike Rother & Rick Harris
- The Machine That Changed the World: Womack, Jones & Roos

### Six Sigma Resources
- The Six Sigma Handbook: Pyzdek & Keller
- Lean Six Sigma Pocket Toolbook: George et al.
- ASQ Six Sigma Black Belt Certification

### Process Mining
- Process Mining: Data Science in Action - Wil van der Aalst
- IEEE Task Force on Process Mining: https://www.tf-pm.org/
- Process Mining Manifesto: http://www.processmining.org/

### Industry Standards
- ISO 9001: Quality Management Systems
- ISO/IEC 15504: Process Assessment
- CMMI: Capability Maturity Model Integration
- APQC Process Classification Framework

---

**Document Version:** 1.0
**Last Updated:** November 21, 2025
**Total Lines:** 500+
