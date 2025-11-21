# Business Analyst Toolkit - Skill Planning Session

**Date:** November 20, 2025
**Status:** Planning Phase - Awaiting User Decisions
**Agent:** Claude Code (Plan Mode)
**Topic:** Designing a new process mapping skill for the product-team

---

## Executive Summary

User identified a gap in the product-team skills: **no capability for business process mapping and documentation**. This session explored whether this should be one skill or multiple, where it should live in the repository, and what capabilities it should include.

### Key Recommendations:
1. **Create single comprehensive skill**: `business-analyst-toolkit`
2. **Location**: `skills/product-team/business-analyst-toolkit/` (6th product skill)
3. **Scope**: Process discovery, documentation, analysis, optimization, and measurement
4. **Agent**: `cs-business-analyst` in `agents/product/`
5. **V1 Priority**: Clarifying questions needed before implementation

---

## Original User Request

> "I think I am missing a skill within the product-team in relation to business process mapping (actually mapping any processes). I am looking for something that allows a user to upload documentation (or provide a link), or a sketch or a process or a transcript of a conversation that explains a process and for that to be documented and mapped. The skill should highlight where it needs more information to complete and also highlight where there are clear or obvious problems/missing info.
>
> In addition it should allow more experienced process owners to map success metrics and time taken/effort to help them assess where potential improvements could be made.
>
> What else should we consider for this skill to do? And is it many skills or one? And should we put it in product-management or create a new process-management team?
>
> Once we define this I will then ask you to suggest how we might use our agents/skills we have already in this codebase to create this new skill/agent along with any prompts that might be needed."

---

## Current Product Team Skills (Analysis Results)

### Existing 5 Skills:

1. **product-manager-toolkit**
   - Focus: Feature prioritization, customer discovery, PRD development
   - Tools: `rice_prioritizer.py`, `customer_interview_analyzer.py`
   - Target: Senior Product Manager

2. **agile-product-owner**
   - Focus: User story generation, sprint planning, backlog management
   - Tools: `user_story_generator.py`
   - Target: Senior Product Owner

3. **product-strategist**
   - Focus: OKR cascading, strategic planning, goal alignment
   - Tools: `okr_cascade_generator.py`
   - Target: Head of Product / Product Leadership

4. **ux-researcher-designer**
   - Focus: User research, persona generation, journey mapping
   - Tools: `persona_generator.py`
   - Target: Senior UX Researcher/Designer

5. **ui-design-system**
   - Focus: Design systems, design tokens, visual consistency
   - Tools: `design_token_generator.py`
   - Target: Senior UI Designer

### Gap Identified:

**Missing**: Cross-functional business process documentation and analysis capability

**Current State**: Each skill documents its internal workflows (how to use the skill), but no skill focuses on mapping business processes across teams/functions.

---

## Recommendation: Business Analyst Toolkit Skill

### Where Should It Live?

**RECOMMENDED: Product Team** (`skills/product-team/business-analyst-toolkit/`)

**Rationale:**
- Process mapping is a core product management competency
- Natural integration with existing product-strategist and product-manager skills
- Precedent: ux-researcher skill already spans product/design
- Can move to new `process-management` domain later if 3+ process skills emerge

**Alternative:** Create new `skills/process-management-team/` domain
- Only recommended if planning 3+ process-related skills
- Examples: process mining, workflow automation, RPA
- Current assessment: Premature for single skill

### One Skill or Multiple?

**RECOMMENDED: One Comprehensive Skill**

**Rationale:** Process discovery → documentation → analysis → optimization → measurement form a cohesive workflow. Splitting would create artificial boundaries.

---

## Proposed Skill Capabilities

### Core Capabilities (Must-Have for V1):

#### 1. Process Discovery & Documentation
- Parse multiple input formats (docs, transcripts, sketches/diagrams)
- Generate standardized process maps (BPMN, swimlanes, flowcharts)
- Identify gaps and ambiguities requiring clarification

#### 2. Process Analysis & Optimization
- Calculate efficiency metrics (cycle time, lead time, throughput)
- Identify bottlenecks, waste, handoff delays
- Suggest improvement opportunities (Lean/Six Sigma principles)

#### 3. Process Governance & Measurement
- Define success metrics and KPIs
- Track effort/time at each step
- Compare as-is vs to-be processes
- Version control for process changes

### Additional Capabilities Suggested:

#### 4. Multi-Format Input Processing
- ✅ Text documents (PDF, Word, Markdown)
- ✅ Conversation transcripts
- ✅ Hand-drawn sketches/diagrams (OCR + image analysis)
- ✅ URLs to documentation
- **NEW**: Structured data (CSV, JSON from tools like Jira)
- **NEW**: Video/audio transcripts (from Zoom, Teams recordings)

#### 5. Intelligent Gap Detection
- ✅ Highlight missing information
- ✅ Flag unclear process steps
- ✅ Identify undefined roles/responsibilities
- **NEW**: Detect contradictions in process descriptions
- **NEW**: Flag missing decision criteria
- **NEW**: Identify unspecified SLAs/timeframes

#### 6. Success Metrics & Measurement
- ✅ Define process KPIs
- ✅ Track time/effort per step
- ✅ Calculate improvement opportunities
- **NEW**: Benchmark against industry standards
- **NEW**: ROI calculator for process improvements
- **NEW**: Before/after comparison dashboard

#### 7. Compliance & Risk Management
- **NEW**: Flag compliance requirements (SOX, GDPR, HIPAA)
- **NEW**: Identify risk points and failure modes
- **NEW**: Document audit trails and approvals
- **NEW**: Map controls and checkpoints

#### 8. Collaboration & Iteration
- **NEW**: Multi-stakeholder review workflow
- **NEW**: Comment/annotation system for process maps
- **NEW**: Change tracking and version history
- **NEW**: Export to collaboration tools (Miro, Lucidchart, Confluence)

#### 9. Process Simulation & What-If Analysis
- **NEW**: Model process changes before implementation
- **NEW**: Predict impact of removing/adding steps
- **NEW**: Resource allocation optimization
- **NEW**: Capacity planning based on process throughput

#### 10. Integration with Existing Skills
- Link to `rice_prioritizer.py` for improvement prioritization
- Connect to `okr_cascade_generator.py` for process goals
- Reference `user_story_generator.py` for automation stories
- Use `customer_interview_analyzer.py` for process feedback

---

## Proposed Skill Structure

### Skill Name: `business-analyst-toolkit`

### Directory Structure:

```
skills/product-team/business-analyst-toolkit/
├── SKILL.md                          # Master documentation (500-700 lines)
├── scripts/                          # Python CLI tools (7 tools)
│   ├── process_parser.py             # Parse multiple input formats
│   ├── process_mapper.py             # Generate visual process maps
│   ├── gap_analyzer.py               # Identify missing info and problems
│   ├── efficiency_analyzer.py        # Calculate process metrics
│   ├── metrics_builder.py            # Define success metrics and KPIs
│   ├── process_comparator.py         # Compare as-is vs to-be
│   └── improvement_prioritizer.py    # Prioritize improvements
├── references/                       # Knowledge bases
│   ├── frameworks.md                 # BPMN, swimlanes, VSM, Six Sigma
│   ├── templates.md                  # Process documentation templates
│   └── tools.md                      # Tool integrations (Lucidchart, Miro)
└── assets/                          # User templates
    ├── process-charter-template.md
    ├── raci-matrix-template.md
    ├── improvement-proposal-template.md
    └── README.md
```

### Python Tools (7 scripts):

#### 1. `process_parser.py`
**Purpose**: Parse multiple input formats into structured process data

**Inputs:**
- PDF documents
- Word documents
- Text/Markdown files
- Transcripts (conversation logs)
- URLs (documentation pages)
- Images (hand-drawn sketches via OCR)

**Output:**
- JSON process structure with steps, roles, decisions, data flows
- Confidence scores for each parsed element
- List of ambiguities and missing information

**Usage:**
```bash
python process_parser.py --input document.pdf --output process.json
python process_parser.py --url "https://company.com/process" --format json
python process_parser.py --transcript conversation.txt --output process.json
```

#### 2. `process_mapper.py`
**Purpose**: Generate visual process maps from structured data

**Inputs:**
- JSON process structure (from process_parser.py)
- Diagram type preference (flowchart, swimlane, BPMN)

**Output:**
- Mermaid diagram markdown
- SVG/PNG exports
- HTML interactive diagrams

**Usage:**
```bash
python process_mapper.py --input process.json --type swimlane --output diagram.md
python process_mapper.py --input process.json --type bpmn --format svg
```

#### 3. `gap_analyzer.py`
**Purpose**: Identify missing information and problems in process

**Inputs:**
- JSON process structure

**Output:**
- Gap report with severity levels (critical, high, medium, low)
- Specific clarifying questions to ask stakeholders
- Problem areas (undefined roles, missing decisions, unclear handoffs)

**Usage:**
```bash
python gap_analyzer.py --input process.json --output gaps.md
python gap_analyzer.py --input process.json --format json --severity high
```

#### 4. `efficiency_analyzer.py`
**Purpose**: Calculate process efficiency metrics

**Inputs:**
- JSON process structure with time/effort data
- Historical performance data (optional)

**Output:**
- Cycle time analysis
- Lead time analysis
- Bottleneck identification
- Waste analysis (waiting, rework, handoffs)
- Throughput calculations

**Usage:**
```bash
python efficiency_analyzer.py --input process.json --output metrics.json
python efficiency_analyzer.py --input process.json --historical data.csv
```

#### 5. `metrics_builder.py`
**Purpose**: Define success metrics and KPIs for process

**Inputs:**
- JSON process structure
- Business objectives
- Industry benchmarks (optional)

**Output:**
- Balanced scorecard
- Leading and lagging indicators
- SLA recommendations
- Measurement plan

**Usage:**
```bash
python metrics_builder.py --input process.json --objectives objectives.txt
python metrics_builder.py --input process.json --benchmarks industry.json
```

#### 6. `process_comparator.py`
**Purpose**: Compare as-is vs to-be processes

**Inputs:**
- Two JSON process structures (current and proposed)

**Output:**
- Side-by-side comparison report
- Impact analysis (time savings, cost reduction)
- Change management requirements
- Risk assessment

**Usage:**
```bash
python process_comparator.py --current as-is.json --proposed to-be.json
python process_comparator.py --current as-is.json --proposed to-be.json --format html
```

#### 7. `improvement_prioritizer.py`
**Purpose**: Prioritize process improvements using RICE framework

**Inputs:**
- Gap analysis results
- Efficiency analysis results
- Business priorities

**Output:**
- Ranked list of improvements with scores
- Effort vs impact matrix
- Implementation roadmap
- Quick wins vs strategic initiatives

**Usage:**
```bash
python improvement_prioritizer.py --gaps gaps.json --metrics metrics.json
python improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --priorities high-priority.txt
```

### References (3 documents):

#### 1. `frameworks.md` (~500 lines)
- **BPMN Notation Standards**: Complete guide to Business Process Model and Notation
- **Swimlane Diagram Conventions**: Cross-functional process mapping
- **Value Stream Mapping (Lean)**: Identify waste and optimize flow
- **Six Sigma DMAIC**: Define, Measure, Analyze, Improve, Control
- **Process Mining Techniques**: Data-driven process discovery
- **Lean Principles**: 7 wastes, 5S, continuous improvement

#### 2. `templates.md` (~400 lines)
- **Process Documentation Templates**: Standard formats for process docs
- **RACI Matrix Templates**: Responsible, Accountable, Consulted, Informed
- **Process Charter Templates**: Define scope, objectives, stakeholders
- **Improvement Proposal Templates**: Structure for presenting changes
- **As-Is/To-Be Templates**: Before and after process states
- **SOP Templates**: Standard Operating Procedures

#### 3. `tools.md` (~300 lines)
- **Lucidchart Integration**: Export to Lucidchart format
- **Miro Integration**: Collaborative whiteboarding
- **Draw.io/Diagrams.net**: Open-source diagramming
- **Confluence Process Documentation**: Publish to Confluence
- **Jira Workflow Automation**: Map processes to Jira workflows
- **Process Mining Tools**: Celonis, UiPath Process Mining
- **Microsoft Visio**: Enterprise diagramming tool

### Assets (4 templates):

1. **process-charter-template.md**: Define process scope and objectives
2. **raci-matrix-template.md**: Map roles and responsibilities
3. **improvement-proposal-template.md**: Present process changes
4. **stakeholder-analysis-template.md**: Identify and engage stakeholders

---

## Proposed Agent: cs-business-analyst

### Agent Structure:

**File**: `agents/product/cs-business-analyst.md`

**YAML Frontmatter:**
```yaml
---
name: cs-business-analyst
description: Process mapping, analysis, and optimization specialist
skills: business-analyst-toolkit
domain: product
model: sonnet
tools: [Read, Write, Bash, Grep, Glob, WebFetch]
---
```

### Workflows (Minimum 4):

#### Workflow 1: Process Discovery
1. Gather process documentation (docs, transcripts, sketches)
2. Parse inputs using `process_parser.py`
3. Generate initial process map with `process_mapper.py`
4. Run gap analysis with `gap_analyzer.py`
5. Iterate with stakeholders to fill gaps
6. Finalize process documentation

#### Workflow 2: Process Optimization
1. Analyze current process efficiency with `efficiency_analyzer.py`
2. Identify improvement opportunities
3. Prioritize improvements with `improvement_prioritizer.py` (uses RICE)
4. Design to-be process
5. Compare as-is vs to-be with `process_comparator.py`
6. Create implementation roadmap

#### Workflow 3: Process Documentation & Governance
1. Standardize process documentation format
2. Create visual maps and RACI matrices
3. Define success metrics with `metrics_builder.py`
4. Export to Confluence/SharePoint
5. Set up version control and change management
6. Establish review and approval workflow

#### Workflow 4: Process Measurement & Continuous Improvement
1. Define baseline metrics
2. Set up data collection mechanisms
3. Create measurement dashboards
4. Track performance over time
5. Identify degradation or improvement
6. Trigger improvement cycles

---

## Integration with Existing Skills

### How business-analyst-toolkit Connects:

1. **product-manager-toolkit**:
   - Use `rice_prioritizer.py` to prioritize process improvements
   - Document "Feature Request to Launch" process
   - Map PRD development workflow

2. **agile-product-owner**:
   - Map sprint planning ceremony process
   - Document epic breakdown workflow
   - Use `user_story_generator.py` to create automation stories

3. **product-strategist**:
   - Connect process KPIs to OKRs using `okr_cascade_generator.py`
   - Map quarterly planning process
   - Document strategic alignment workflow

4. **ux-researcher-designer**:
   - Integrate with journey mapping capabilities
   - Use `customer_interview_analyzer.py` for process feedback
   - Map user research → insights → design process

5. **ui-design-system**:
   - Document design system creation process
   - Map design token workflow
   - Standardize design handoff process

### Example Cross-Skill Workflows:

**Scenario 1**: "Document Feature Development Process"
```bash
# 1. Parse existing documentation
python scripts/process_parser.py --input feature-dev-docs/ --output feature-dev.json

# 2. Generate swimlane diagram (Product, Design, Engineering)
python scripts/process_mapper.py --input feature-dev.json --type swimlane

# 3. Identify gaps
python scripts/gap_analyzer.py --input feature-dev.json

# 4. Calculate efficiency
python scripts/efficiency_analyzer.py --input feature-dev.json

# 5. Prioritize improvements using RICE
python ../../product-manager-toolkit/scripts/rice_prioritizer.py improvements.csv

# 6. Create improvement stories
python ../../agile-product-owner/scripts/user_story_generator.py improvements.txt
```

---

## Outstanding Questions (Need User Input)

### 1. Scope Priority
**Question**: Which capabilities are **must-have for v1** vs **nice-to-have for v2**?

**Options:**
- **V1 Minimal**: Process parsing, mapping, gap analysis, efficiency metrics only
- **V1 Moderate**: Add metrics builder, process comparator, improvement prioritizer
- **V1 Comprehensive**: Include compliance, simulation, collaboration features

**Recommendation**: Start with **V1 Moderate** (7 Python tools as proposed)

### 2. Input Format Priority
**Question**: Which input formats should we support **first**?

**Options:**
- **Phase 1**: Text documents only (Markdown, TXT)
- **Phase 2**: Add PDF/Word support
- **Phase 3**: Add image/sketch support (OCR)
- **Phase 4**: Add URL/web scraping
- **All at once**: Full multi-format support in V1

**Recommendation**: **Phase 1 + 2** (text and PDF/Word for V1)

### 3. Diagram Output Formats
**Question**: What diagram formats are most important?

**Options:**
- **Mermaid only**: Works in markdown, GitHub, Confluence (easiest)
- **Mermaid + SVG/PNG**: Static exports for presentations
- **Mermaid + Tool Integration**: Lucidchart/Miro API (requires credentials)
- **All of the above**: Maximum flexibility

**Recommendation**: **Mermaid + SVG/PNG** for V1

### 4. Process Complexity Support
**Question**: What level of process complexity should we support?

**Options:**
- **Simple**: Linear workflows (5-10 steps, no branches)
- **Moderate**: Branching workflows (20+ steps, decision points)
- **Complex**: Cross-functional workflows (multiple teams/swimlanes)
- **All**: Support any complexity level

**Recommendation**: **Moderate to Complex** (business processes are rarely simple)

### 5. Time/Effort Tracking
**Question**: How should we capture time and effort data?

**Options:**
- **Manual input**: User provides estimates when parsing
- **Historical data import**: CSV/JSON from existing tools
- **Real-time tracking integration**: Jira, GitHub API calls
- **Statistical modeling**: Estimate based on similar processes
- **All of the above**: Multiple data sources

**Recommendation**: **Manual input + Historical data import** for V1

### 6. Success Metrics Scope
**Question**: What types of metrics should we support?

**Options:**
- **Process-specific**: Cycle time, error rate, throughput
- **Business outcomes**: Revenue, customer satisfaction, retention
- **Efficiency metrics**: Cost per transaction, resource utilization
- **All of the above**: Comprehensive metric framework

**Recommendation**: **Process-specific + Efficiency metrics** for V1, business outcomes in V2

---

## Next Steps (When User Returns)

### Step 1: Answer Outstanding Questions
User to review and answer the 6 clarifying questions above to finalize V1 scope.

### Step 2: Create Implementation Plan
Once scope is defined, create detailed plan for:
1. Which existing skills/agents to use for building this skill
2. Specific prompts needed for each phase
3. Development sequence and dependencies
4. Testing and validation approach

### Step 3: Execute Implementation
1. Create directory structure
2. Develop Python tools (using cs-architect or cs-backend-engineer?)
3. Write documentation (using cs-product-manager for "PRD"?)
4. Create references (using cs-ux-researcher for research?)
5. Build templates
6. Create cs-business-analyst agent
7. Test and validate

### Step 4: Integration Testing
Test integration with existing product-team skills and agents.

---

## Meta-Skill Idea (Future Enhancement)

**User suggested**: Consider creating a **skill-architect-toolkit** for maintaining the skills repository itself.

**Potential Capabilities:**
- `skill_validator.py` - Check skill consistency and quality
- `gap_analyzer.py` - Identify missing capabilities in library
- `scaffold_generator.py` - Generate new skill boilerplate
- `integration_mapper.py` - Map skill dependencies and interactions
- `quality_checker.py` - Validate documentation completeness

**Rationale**: Make the repository self-maintaining and enable easier skill development.

**Priority**: After business-analyst-toolkit is complete

---

## Transparency Note: Tools Used for This Analysis

### What Was Used:
- **Task tool with Plan subagent** - Claude Code's built-in codebase exploration agent
- Used standard tools: Glob, Grep, Read, Bash
- Analyzed repository structure, skill patterns, existing capabilities

### What Was NOT Used:
- ❌ None of the existing `cs-*` agents (they're for end-user workflows, not meta-analysis)
- ❌ None of the existing skills (they're for domain work, not repository analysis)

### Why:
The existing skills/agents are designed for **domain-specific work** (build products, write code, conduct research), not for **analyzing the skills repository itself** or **designing new skills**.

This gap reinforces the need for a future `skill-architect-toolkit` meta-skill.

---

## Document Metadata

**Saved By**: Claude Code (Plan Mode)
**File Location**: `output/analysis/2025-11-20_business-analyst-skill-planning-session.md`
**Git Status**: New file (not yet committed)
**Next Action**: User to review, answer clarifying questions, then resume planning session

---

## Quick Reference: Key Decisions Needed

1. ✅ **Location**: `skills/product-team/business-analyst-toolkit/` (AGREED)
2. ✅ **Structure**: Single comprehensive skill (AGREED)
3. ❓ **V1 Scope**: Which capabilities are must-have?
4. ❓ **Input Formats**: Which formats to support first?
5. ❓ **Diagram Outputs**: Which export formats?
6. ❓ **Process Complexity**: What level to support?
7. ❓ **Time Tracking**: How to capture data?
8. ❓ **Metrics Scope**: Which types of metrics?

---

**Status**: 🟡 Planning session paused - awaiting user return and decisions

**To Resume**:
1. Review this document
2. Answer the 6 clarifying questions in "Outstanding Questions" section
3. Proceed to Step 2: Create Implementation Plan
