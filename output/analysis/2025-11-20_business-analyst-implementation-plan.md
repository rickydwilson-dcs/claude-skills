# Business Analyst Toolkit - Implementation Plan (FINAL)

**Date:** November 20, 2025
**Status:** Ready for Implementation
**Agent:** Claude Code (Plan Mode)
**Based On:** User clarifications received

---

## Executive Summary

This document provides the **finalized scope and detailed implementation plan** for creating the `business-analyst-toolkit` skill and `cs-business-analyst` agent for the product-team domain.

### User Decisions (Confirmed):

1. ✅ **V1 Scope**: Must-have capabilities (7 Python tools - process discovery, documentation, analysis, optimization)
2. ✅ **Input Formats**: URLs (Confluence), text files, sketches/images, transcripts
3. ✅ **Diagram Outputs**: All formats (Mermaid, SVG, PNG, tool integrations)
4. ✅ **Process Complexity**: All levels (simple to complex cross-functional)
5. ✅ **Time/Effort Tracking**: Manual input initially
6. ✅ **Metrics Scope**: Process-specific and efficiency metrics

---

## V1 Scope - Finalized Capabilities

### Core Features (Must-Have):

#### 1. Process Discovery & Documentation
- ✅ Parse URLs (Confluence, web documentation)
- ✅ Parse text files (Markdown, TXT, plain text)
- ✅ Parse sketches/images (OCR for hand-drawn processes)
- ✅ Parse conversation transcripts
- ✅ Generate standardized process maps (BPMN, swimlanes, flowcharts)
- ✅ Identify gaps and missing information

#### 2. Process Analysis & Optimization
- ✅ Calculate efficiency metrics (cycle time, lead time, throughput)
- ✅ Identify bottlenecks, waste, handoff delays
- ✅ Suggest improvement opportunities (Lean/Six Sigma)

#### 3. Process Governance & Measurement
- ✅ Define process-specific KPIs
- ✅ Define efficiency metrics (cost per transaction, resource utilization)
- ✅ Track effort/time at each step (manual input)
- ✅ Compare as-is vs to-be processes
- ✅ Version control for process changes

#### 4. Diagram Output (All Formats)
- ✅ Mermaid diagrams (markdown, GitHub, Confluence compatible)
- ✅ SVG exports (scalable, presentation-ready)
- ✅ PNG exports (static images)
- ✅ HTML interactive diagrams
- ✅ Export formats for Lucidchart, Miro, Draw.io

#### 5. Process Complexity Support (All Levels)
- ✅ Simple linear workflows (5-10 steps)
- ✅ Branching workflows (decision points, conditional logic)
- ✅ Complex cross-functional workflows (multiple teams, swimlanes)
- ✅ Subprocess and hierarchical process support

### Deferred to V2 (Nice-to-Have):

- ❌ Real-time tracking integration (Jira, GitHub APIs) - manual input for V1
- ❌ Statistical modeling for time estimation - user provides estimates
- ❌ Business outcome metrics (revenue, satisfaction) - process/efficiency only for V1
- ❌ Compliance & risk management (SOX, GDPR) - basic identification only
- ❌ Process simulation & what-if analysis - comparison only for V1
- ❌ Advanced collaboration features (multi-stakeholder review, annotations) - basic export only

---

## Skill Structure - Finalized

### Location:
```
skills/product-team/business-analyst-toolkit/
```

### Directory Structure:
```
business-analyst-toolkit/
├── SKILL.md                          # Master documentation (600-800 lines)
├── scripts/                          # 7 Python CLI tools
│   ├── process_parser.py             # Parse URLs, text, images, transcripts
│   ├── process_mapper.py             # Generate diagrams (all formats)
│   ├── gap_analyzer.py               # Identify missing information
│   ├── efficiency_analyzer.py        # Calculate process metrics
│   ├── metrics_builder.py            # Define KPIs and metrics
│   ├── process_comparator.py         # Compare as-is vs to-be
│   └── improvement_prioritizer.py    # Prioritize improvements (RICE)
├── references/                       # 3 knowledge base documents
│   ├── frameworks.md                 # BPMN, swimlanes, VSM, Lean, Six Sigma
│   ├── templates.md                  # Process docs, RACI, charters
│   └── tools.md                      # Lucidchart, Miro, Confluence, Jira
└── assets/                          # 4 user templates
    ├── process-charter-template.md
    ├── raci-matrix-template.md
    ├── improvement-proposal-template.md
    └── stakeholder-analysis-template.md
```

---

## Python Tools - Detailed Specifications

### 1. `process_parser.py` (Priority: CRITICAL)

**Purpose**: Universal process parser supporting multiple input formats

**Input Formats:**
- URLs (Confluence, web documentation) - HTTP GET + HTML parsing
- Text files (Markdown, TXT, plain text) - File I/O
- Images (sketches, diagrams) - Pillow + pytesseract for OCR
- Transcripts (conversation logs) - NLP parsing

**Arguments:**
```bash
--input PATH           # File path or directory
--url URL             # Web URL (Confluence, etc.)
--type TYPE           # Input type (auto-detect if not specified)
--output FILE         # Output JSON file path
--format FORMAT       # Output format (json, yaml, csv)
--verbose             # Verbose output with confidence scores
```

**Output Schema (JSON):**
```json
{
  "process_name": "string",
  "process_owner": "string",
  "source": "string",
  "confidence_score": 0.0-1.0,
  "steps": [
    {
      "id": "step_001",
      "name": "Step name",
      "description": "Step description",
      "role": "Responsible role",
      "duration_minutes": 30,
      "effort_hours": 2.0,
      "inputs": ["Input 1", "Input 2"],
      "outputs": ["Output 1"],
      "decisions": ["Decision point"],
      "handoffs": ["Team/Role"],
      "confidence": 0.0-1.0
    }
  ],
  "roles": ["Role 1", "Role 2"],
  "gaps": [
    {
      "type": "missing_info",
      "severity": "high",
      "description": "Missing duration for step X"
    }
  ]
}
```

**Dependencies:**
- Standard library: `json`, `argparse`, `re`, `urllib`, `html.parser`
- Optional: `pytesseract` (OCR), `Pillow` (image processing)
- Note: Make OCR dependencies optional with graceful fallback

**Testing:**
```bash
# Test text parsing
python process_parser.py --input process-doc.md --output process.json

# Test URL parsing (Confluence)
python process_parser.py --url "https://company.atlassian.net/wiki/process" --output process.json

# Test image parsing (sketch)
python process_parser.py --input sketch.png --type image --output process.json

# Test transcript parsing
python process_parser.py --input meeting-transcript.txt --type transcript --output process.json
```

---

### 2. `process_mapper.py` (Priority: CRITICAL)

**Purpose**: Generate visual process diagrams in multiple formats

**Arguments:**
```bash
--input FILE          # JSON process file (from process_parser.py)
--type TYPE           # Diagram type (flowchart, swimlane, bpmn)
--format FORMAT       # Output format (mermaid, svg, png, html, lucidchart, miro)
--output FILE         # Output file path
--theme THEME         # Visual theme (default, professional, minimal)
--complexity LEVEL    # Detail level (simple, detailed, comprehensive)
```

**Supported Diagram Types:**
1. **Flowchart**: Simple top-to-bottom process flow
2. **Swimlane**: Cross-functional with role/team lanes
3. **BPMN**: Full Business Process Model and Notation

**Supported Output Formats:**
1. **Mermaid** (.md) - Markdown with Mermaid syntax
2. **SVG** (.svg) - Scalable vector graphics
3. **PNG** (.png) - Raster image (requires mermaid-cli or similar)
4. **HTML** (.html) - Interactive diagram with zoom/pan
5. **Lucidchart** (.json) - Lucidchart import format
6. **Miro** (.json) - Miro board import format

**Dependencies:**
- Standard library: `json`, `argparse`
- Optional: `mermaid-cli` (for SVG/PNG generation)
- Optional: `cairosvg` (for SVG to PNG conversion)

**Testing:**
```bash
# Generate Mermaid flowchart
python process_mapper.py --input process.json --type flowchart --format mermaid --output diagram.md

# Generate SVG swimlane diagram
python process_mapper.py --input process.json --type swimlane --format svg --output diagram.svg

# Generate interactive HTML
python process_mapper.py --input process.json --type bpmn --format html --output diagram.html

# Export to Lucidchart
python process_mapper.py --input process.json --type swimlane --format lucidchart --output lucidchart.json
```

---

### 3. `gap_analyzer.py` (Priority: HIGH)

**Purpose**: Identify missing information and problems in process definition

**Arguments:**
```bash
--input FILE          # JSON process file
--output FILE         # Gap report output (markdown or JSON)
--format FORMAT       # Output format (markdown, json, html)
--severity LEVEL      # Minimum severity to report (all, critical, high, medium, low)
--questions           # Generate stakeholder questions
```

**Gap Types Detected:**
1. **Missing Information**: Undefined roles, missing durations, unclear inputs/outputs
2. **Undefined Roles**: Steps without assigned roles
3. **Missing Decisions**: Decision points without criteria
4. **Unclear Handoffs**: Handoffs without clear ownership transfer
5. **Incomplete Steps**: Steps with low confidence scores
6. **Contradictions**: Conflicting information in process description
7. **Missing SLAs**: No timeframes or performance targets

**Severity Levels:**
- **Critical**: Process cannot be executed (missing essential info)
- **High**: Process will likely fail or produce poor results
- **Medium**: Process may be inefficient or unclear
- **Low**: Minor improvements or clarifications needed

**Output Format (Markdown):**
```markdown
# Process Gap Analysis Report

## Summary
- Total Gaps: 12
- Critical: 2
- High: 4
- Medium: 5
- Low: 1

## Critical Gaps

### Gap #1: Missing Process Owner
**Severity:** Critical
**Type:** Missing Information
**Description:** No process owner identified
**Impact:** Unclear accountability and governance
**Questions to Ask:**
- Who is responsible for this process?
- Who should approve changes to this process?

## Stakeholder Questions (15 questions)
1. [Step 3] Who is responsible for reviewing the proposal?
2. [Step 5] What criteria determine approval vs rejection?
...
```

**Testing:**
```bash
# Generate full gap report
python gap_analyzer.py --input process.json --output gaps.md

# Show only critical/high gaps
python gap_analyzer.py --input process.json --severity high --output critical-gaps.md

# Generate stakeholder questions
python gap_analyzer.py --input process.json --questions --output questions.md
```

---

### 4. `efficiency_analyzer.py` (Priority: HIGH)

**Purpose**: Calculate process efficiency metrics and identify bottlenecks

**Arguments:**
```bash
--input FILE          # JSON process file (with time/effort data)
--output FILE         # Metrics report output
--format FORMAT       # Output format (json, markdown, csv, html)
--historical FILE     # Optional: Historical performance data (CSV)
--benchmark FILE      # Optional: Industry benchmark data (JSON)
```

**Metrics Calculated:**

**Time Metrics:**
- **Cycle Time**: Total time from start to finish (calendar time)
- **Lead Time**: Customer-facing time (from request to delivery)
- **Processing Time**: Actual work time (excluding waiting)
- **Wait Time**: Time spent waiting between steps

**Efficiency Metrics:**
- **Process Efficiency**: Processing Time / Cycle Time (%)
- **Value-Added Ratio**: Value-added time / Total time (%)
- **Throughput**: Process completions per time period

**Waste Analysis (Lean 7 Wastes):**
1. **Waiting**: Time between steps
2. **Transportation**: Handoffs between teams
3. **Motion**: Unnecessary movement/switching
4. **Defects**: Rework loops
5. **Overprocessing**: Unnecessary steps
6. **Overproduction**: Work before needed
7. **Inventory**: Work in progress (WIP)

**Bottleneck Identification:**
- Steps with longest duration
- Steps with most handoffs
- Steps with lowest confidence
- Steps with highest wait time

**Output Format (JSON):**
```json
{
  "summary": {
    "cycle_time_minutes": 480,
    "processing_time_minutes": 120,
    "wait_time_minutes": 360,
    "process_efficiency_percent": 25.0,
    "throughput_per_day": 12
  },
  "bottlenecks": [
    {
      "step_id": "step_005",
      "step_name": "Legal Review",
      "duration_minutes": 120,
      "wait_time_minutes": 180,
      "severity": "high",
      "recommendation": "Consider parallel review or pre-approval templates"
    }
  ],
  "waste_analysis": {
    "waiting": {"minutes": 360, "percent": 75.0},
    "handoffs": {"count": 8, "minutes": 60},
    "rework": {"count": 2, "minutes": 30}
  }
}
```

**Testing:**
```bash
# Basic efficiency analysis
python efficiency_analyzer.py --input process.json --output metrics.json

# With historical data
python efficiency_analyzer.py --input process.json --historical historical.csv --output metrics.md

# HTML dashboard
python efficiency_analyzer.py --input process.json --format html --output dashboard.html
```

---

### 5. `metrics_builder.py` (Priority: MEDIUM)

**Purpose**: Define success metrics and KPIs for process

**Arguments:**
```bash
--input FILE          # JSON process file
--output FILE         # Metrics plan output
--format FORMAT       # Output format (json, markdown, yaml)
--objectives FILE     # Business objectives (text file)
--focus AREA          # Focus area (process, efficiency, quality, cost)
```

**Metric Categories:**

**Process-Specific Metrics:**
- **Cycle Time**: Average time to complete process
- **Error Rate**: Percentage of processes with defects
- **Throughput**: Number of completions per time period
- **First-Pass Yield**: Percentage completed without rework
- **On-Time Delivery**: Percentage completed within SLA

**Efficiency Metrics:**
- **Cost Per Transaction**: Total cost / number of completions
- **Resource Utilization**: Actual time / available time (%)
- **Automation Rate**: Automated steps / total steps (%)
- **Handoff Count**: Number of team/role handoffs
- **Wait Time Ratio**: Wait time / cycle time (%)

**Output Format (Markdown):**
```markdown
# Process Metrics Plan

## Leading Indicators (Early Warning)
1. **Backlog Size**
   - Definition: Number of pending requests
   - Target: < 20 items
   - Measurement: Daily count
   - Owner: Process Manager

## Lagging Indicators (Outcome)
1. **Cycle Time**
   - Definition: Average time from request to completion
   - Target: < 5 days
   - Measurement: Weekly average
   - Owner: Process Owner

## Measurement Plan
- **Data Collection**: Manual entry in process tracker
- **Reporting Frequency**: Weekly dashboard
- **Review Cadence**: Monthly process review meeting
- **Owner**: Process Owner
```

**Testing:**
```bash
# Generate metrics plan
python metrics_builder.py --input process.json --output metrics-plan.md

# Focus on efficiency metrics
python metrics_builder.py --input process.json --focus efficiency --output efficiency-metrics.json
```

---

### 6. `process_comparator.py` (Priority: MEDIUM)

**Purpose**: Compare as-is vs to-be processes and calculate impact

**Arguments:**
```bash
--current FILE        # Current (as-is) process JSON
--proposed FILE       # Proposed (to-be) process JSON
--output FILE         # Comparison report output
--format FORMAT       # Output format (json, markdown, html)
--impact              # Include impact analysis (time, cost, risk)
```

**Comparison Areas:**
1. **Structure Changes**: Added/removed/modified steps
2. **Time Impact**: Cycle time reduction/increase
3. **Efficiency Impact**: Process efficiency improvement
4. **Complexity Changes**: More/fewer steps, handoffs
5. **Risk Assessment**: Risks introduced by changes
6. **Change Management**: Training, communication needs

**Output Format (Markdown):**
```markdown
# Process Comparison Report

## Summary
- **As-Is Cycle Time**: 480 minutes (8 hours)
- **To-Be Cycle Time**: 300 minutes (5 hours)
- **Time Savings**: 180 minutes (37.5%)
- **As-Is Steps**: 12
- **To-Be Steps**: 9
- **Steps Removed**: 3

## Detailed Changes

### Removed Steps
1. **Step 4: Manual Data Entry** (30 min)
   - Reason: Automated with form integration
   - Impact: 30 min time savings, reduced errors

### Modified Steps
1. **Step 3: Review Process** (60 min → 30 min)
   - Change: Parallel review instead of sequential
   - Impact: 30 min time savings

## Impact Analysis
- **Estimated Annual Time Savings**: 900 hours
- **Estimated Annual Cost Savings**: $45,000
- **Risk Level**: Medium
- **Implementation Effort**: 2-3 weeks

## Change Management Requirements
- Training: 2-hour workshop for reviewers
- Communication: Announce 2 weeks before rollout
- Support: Dedicated support for first 2 weeks
```

**Testing:**
```bash
# Basic comparison
python process_comparator.py --current as-is.json --proposed to-be.json --output comparison.md

# With impact analysis
python process_comparator.py --current as-is.json --proposed to-be.json --impact --output impact-report.html
```

---

### 7. `improvement_prioritizer.py` (Priority: MEDIUM)

**Purpose**: Prioritize process improvements using RICE framework

**Arguments:**
```bash
--gaps FILE           # Gap analysis results (JSON)
--metrics FILE        # Efficiency analysis results (JSON)
--output FILE         # Prioritized improvements output
--format FORMAT       # Output format (json, markdown, csv)
--priorities FILE     # Optional: Business priorities (text)
--threshold SCORE     # Minimum RICE score to include
```

**RICE Framework:**
- **Reach**: How many process executions affected? (High/Medium/Low)
- **Impact**: How much improvement per execution? (3=Massive, 2=High, 1=Medium, 0.5=Low, 0.25=Minimal)
- **Confidence**: How confident in estimates? (100%=High, 80%=Medium, 50%=Low)
- **Effort**: Person-weeks to implement (0.5, 1, 2, 4, 8+ weeks)

**RICE Score = (Reach × Impact × Confidence) / Effort**

**Output Format (Markdown):**
```markdown
# Process Improvement Prioritization

## Summary
- Total Improvements: 12
- Quick Wins (RICE > 10): 3
- Strategic Initiatives (RICE 5-10): 5
- Backlog (RICE < 5): 4

## Prioritized Improvements

### 1. Automate Legal Review (RICE: 18.0) 🎯 QUICK WIN
- **Gap**: Manual review causes 180-min bottleneck
- **Reach**: 50 processes/month
- **Impact**: 3 (Massive) - 3-hour time savings per process
- **Confidence**: 80%
- **Effort**: 2 weeks
- **Expected Savings**: 150 hours/month
- **Recommendation**: IMPLEMENT IMMEDIATELY

### 2. Parallel Approval Workflow (RICE: 12.0)
- **Gap**: Sequential approvals cause delays
- **Reach**: 50 processes/month
- **Impact**: 2 (High) - 1-hour time savings per process
- **Confidence**: 80%
- **Effort**: 1 week
- **Expected Savings**: 50 hours/month
- **Recommendation**: IMPLEMENT IN Q1

## Implementation Roadmap

### Phase 1 (Weeks 1-2): Quick Wins
1. Automate Legal Review
2. Parallel Approval Workflow
3. Pre-fill Form Templates

### Phase 2 (Weeks 3-6): Strategic Initiatives
...
```

**Integration with product-manager-toolkit:**
```bash
# Generate improvements CSV for RICE prioritizer
python improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --format csv --output improvements.csv

# Use product-manager RICE prioritizer
python ../../product-manager-toolkit/scripts/rice_prioritizer.py --input improvements.csv --output prioritized.csv
```

**Testing:**
```bash
# Basic prioritization
python improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --output priorities.md

# With business priorities
python improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --priorities high-priority.txt --output priorities.md

# Show only high-score improvements
python improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --threshold 10 --output quick-wins.md
```

---

## Dependencies Summary

### Core Dependencies (Required):
- **Python 3.8+** (standard library only for core functionality)
- `json` - Process data handling
- `argparse` - CLI argument parsing
- `re` - Text parsing and pattern matching
- `urllib` - URL fetching
- `html.parser` - HTML parsing for URLs
- `csv` - CSV export/import

### Optional Dependencies (Enhanced Features):
- **pytesseract** + **Pillow** - OCR for image/sketch parsing
  - Fallback: Skip image parsing or manual text extraction
- **cairosvg** - SVG to PNG conversion
  - Fallback: SVG output only, or use external tool
- **mermaid-cli** - Mermaid to SVG/PNG rendering
  - Fallback: Mermaid markdown only

### Installation Strategy:
```bash
# Core installation (no dependencies)
python3 -m venv business-analyst_venv
source business-analyst_venv/bin/activate

# Test core functionality immediately
python scripts/process_parser.py --help

# Optional: Install OCR support
pip install pytesseract Pillow

# Optional: Install diagram rendering
npm install -g @mermaid-js/mermaid-cli
pip install cairosvg
```

---

## Implementation Sequence & Timeline

### Phase 1: Foundation (Week 1)
**Goal**: Create directory structure, documentation skeleton, and first Python tool

**Tasks:**
1. Create directory structure
   ```bash
   mkdir -p skills/product-team/business-analyst-toolkit/{scripts,references,assets}
   ```

2. Create SKILL.md skeleton (use template)
   ```bash
   cp templates/skill-template.md skills/product-team/business-analyst-toolkit/SKILL.md
   ```

3. Develop `process_parser.py` (CRITICAL PATH)
   - Text parsing (Markdown, TXT)
   - URL parsing (Confluence, web)
   - JSON output schema
   - Test with sample inputs

4. Create basic references/frameworks.md
   - BPMN overview
   - Swimlane conventions
   - Process documentation standards

**Deliverables:**
- ✅ Directory structure
- ✅ SKILL.md skeleton
- ✅ `process_parser.py` (text + URL support)
- ✅ Basic frameworks.md

**Validation:**
```bash
# Test text parsing
echo "Process: Feature Request
Step 1: User submits request (30 min)
Step 2: PM reviews (60 min)
Step 3: Engineering estimates (120 min)" > test-process.txt

python scripts/process_parser.py --input test-process.txt --output test-process.json
cat test-process.json  # Verify JSON output
```

---

### Phase 2: Core Tools (Week 2)
**Goal**: Complete critical tools for process mapping and gap analysis

**Tasks:**
1. Develop `process_mapper.py` (CRITICAL PATH)
   - Mermaid diagram generation (flowchart, swimlane)
   - SVG export (if dependencies available)
   - Test with parsed process data

2. Develop `gap_analyzer.py` (CRITICAL PATH)
   - Gap detection logic
   - Severity scoring
   - Stakeholder question generation
   - Test with incomplete process data

3. Add image parsing to `process_parser.py`
   - OCR integration (pytesseract)
   - Hand-drawn sketch parsing
   - Graceful fallback if OCR unavailable

4. Create references/templates.md
   - Process documentation templates
   - RACI matrix template
   - Process charter template

**Deliverables:**
- ✅ `process_mapper.py` (Mermaid + SVG)
- ✅ `gap_analyzer.py` (full functionality)
- ✅ Image parsing in `process_parser.py`
- ✅ templates.md

**Validation:**
```bash
# End-to-end workflow test
python scripts/process_parser.py --input test-process.txt --output process.json
python scripts/process_mapper.py --input process.json --type swimlane --format mermaid --output diagram.md
python scripts/gap_analyzer.py --input process.json --output gaps.md

# Verify outputs
cat diagram.md  # Should contain valid Mermaid syntax
cat gaps.md     # Should identify missing roles, durations, etc.
```

---

### Phase 3: Analysis Tools (Week 3)
**Goal**: Complete efficiency analysis and metrics tools

**Tasks:**
1. Develop `efficiency_analyzer.py`
   - Cycle time, lead time calculations
   - Bottleneck identification
   - Waste analysis (Lean 7 wastes)
   - Test with process data containing time estimates

2. Develop `metrics_builder.py`
   - Process-specific metrics
   - Efficiency metrics
   - Measurement plan generation
   - Test with various process types

3. Create references/tools.md
   - Lucidchart integration guide
   - Miro integration guide
   - Confluence export guide
   - Jira workflow mapping

4. Update SKILL.md with all tools
   - Tool documentation
   - Usage examples
   - Workflow documentation

**Deliverables:**
- ✅ `efficiency_analyzer.py`
- ✅ `metrics_builder.py`
- ✅ tools.md
- ✅ SKILL.md (80% complete)

**Validation:**
```bash
# Efficiency analysis test
python scripts/efficiency_analyzer.py --input process.json --output metrics.json
cat metrics.json  # Verify cycle time, bottlenecks calculated

# Metrics builder test
python scripts/metrics_builder.py --input process.json --output metrics-plan.md
cat metrics-plan.md  # Verify KPIs and measurement plan
```

---

### Phase 4: Comparison & Prioritization (Week 4)
**Goal**: Complete remaining tools and integration

**Tasks:**
1. Develop `process_comparator.py`
   - As-is vs to-be comparison logic
   - Impact analysis (time, cost, risk)
   - Change management recommendations
   - Test with two process versions

2. Develop `improvement_prioritizer.py`
   - RICE framework implementation
   - Integration with product-manager-toolkit
   - Roadmap generation
   - Test with gap and metrics data

3. Create all asset templates
   - process-charter-template.md
   - raci-matrix-template.md
   - improvement-proposal-template.md
   - stakeholder-analysis-template.md

4. Finalize SKILL.md
   - Complete all sections
   - Add integration examples
   - Add troubleshooting guide

**Deliverables:**
- ✅ `process_comparator.py`
- ✅ `improvement_prioritizer.py`
- ✅ All asset templates (4 files)
- ✅ SKILL.md (100% complete)

**Validation:**
```bash
# Comparison test (create modified process)
cp process.json process-improved.json
# Manually edit process-improved.json to remove a step
python scripts/process_comparator.py --current process.json --proposed process-improved.json --output comparison.md
cat comparison.md  # Verify changes detected

# Prioritization test
python scripts/improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --output priorities.md
cat priorities.md  # Verify RICE scores and roadmap
```

---

### Phase 5: Agent Development (Week 5)
**Goal**: Create cs-business-analyst agent and final integration

**Tasks:**
1. Create agent file
   ```bash
   cp templates/agent-template.md agents/product/cs-business-analyst.md
   ```

2. Write agent documentation
   - YAML frontmatter
   - Purpose and description
   - 4+ complete workflows
   - Tool integration examples
   - Success metrics

3. Test agent workflows
   - Process Discovery workflow (end-to-end)
   - Process Optimization workflow
   - Process Documentation workflow
   - Process Measurement workflow

4. Integration testing
   - Test with product-manager-toolkit (RICE prioritizer)
   - Test with agile-product-owner (user story generator)
   - Test with product-strategist (OKR connector)

5. Update product-team CLAUDE.md
   - Add business-analyst-toolkit to skills list
   - Add integration examples
   - Update roadmap

**Deliverables:**
- ✅ cs-business-analyst.md (complete)
- ✅ Integration tests (all passing)
- ✅ product-team/CLAUDE.md updated
- ✅ Root CLAUDE.md updated (skill count)

**Validation:**
```bash
# Agent path validation
cd agents/product/
ls ../../skills/product-team/business-analyst-toolkit/  # Must resolve

# Integration test with RICE prioritizer
cd skills/product-team/business-analyst-toolkit/
python scripts/improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --format csv --output improvements.csv
python ../product-manager-toolkit/scripts/rice_prioritizer.py --input improvements.csv --output prioritized.csv
```

---

### Phase 6: Documentation & Polish (Week 6)
**Goal**: Final documentation, testing, and quality assurance

**Tasks:**
1. Comprehensive testing
   - Test all 7 Python tools with various inputs
   - Test all output formats
   - Test error handling and edge cases
   - Test --help flags

2. Documentation review
   - Proofread SKILL.md
   - Verify all references complete
   - Verify all templates usable
   - Add more examples and troubleshooting

3. Integration documentation
   - Document cross-skill workflows
   - Create example scenarios
   - Add to USAGE.md examples

4. Create output directory structure
   ```bash
   mkdir -p output/process-analysis
   ```

5. Final validation
   - Run through all 4 agent workflows
   - Verify all relative paths work
   - Test in fresh environment (no dependencies)

**Deliverables:**
- ✅ All tools tested and validated
- ✅ Documentation complete and proofread
- ✅ Integration examples documented
- ✅ Ready for production use

**Validation:**
```bash
# Fresh environment test
python3 -m venv test_venv
source test_venv/bin/activate
cd skills/product-team/business-analyst-toolkit/

# Run all tools with --help
for tool in scripts/*.py; do
    echo "Testing: $tool"
    python "$tool" --help || echo "FAILED: $tool"
done

# Run end-to-end workflow
python scripts/process_parser.py --input sample-process.txt --output process.json
python scripts/process_mapper.py --input process.json --type swimlane --format mermaid --output diagram.md
python scripts/gap_analyzer.py --input process.json --output gaps.md
python scripts/efficiency_analyzer.py --input process.json --output metrics.json
python scripts/metrics_builder.py --input process.json --output metrics-plan.md
python scripts/improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --output priorities.md
```

---

## Leveraging Existing Skills/Agents for Development

### How to Use Your Existing Skills to Build This Skill:

#### 1. Use `cs-product-manager` for "PRD" Creation

**Task**: Define requirements for the business-analyst-toolkit

**Workflow:**
1. Create requirements document describing the skill
2. Use cs-product-manager to structure it as a PRD
3. Use RICE prioritizer to rank feature priorities

**Prompt:**
```
I need to create a "Product Requirements Document" for a new skill in our repository called business-analyst-toolkit. The skill should enable users to:
- Parse process documentation from multiple sources
- Generate visual process maps
- Identify gaps in process definition
- Analyze process efficiency
- Define success metrics

Use the product-manager-toolkit to help me create a structured PRD that includes:
- Problem statement
- User personas (who will use this skill?)
- Use cases and user stories
- Feature requirements (prioritized)
- Success metrics
```

**Expected Output**: PRD document that guides development

---

#### 2. Use `cs-architect` for Python Tool Design

**Task**: Design architecture for the 7 Python tools

**Workflow:**
1. Review requirements from PRD
2. Use cs-architect to design tool architecture
3. Define data schemas (JSON process format)
4. Plan module structure and dependencies

**Prompt:**
```
I need to design the architecture for 7 Python CLI tools that form the business-analyst-toolkit skill. The tools are:
1. process_parser.py - Parse multiple input formats
2. process_mapper.py - Generate diagrams
3. gap_analyzer.py - Identify missing information
4. efficiency_analyzer.py - Calculate metrics
5. metrics_builder.py - Define KPIs
6. process_comparator.py - Compare processes
7. improvement_prioritizer.py - Prioritize improvements

Use the senior-architect skill to help me:
- Design the shared JSON schema for process data
- Plan module structure and code reuse
- Identify dependencies and integration points
- Design CLI interfaces for consistency
- Plan for extensibility and future features

Generate architecture documentation including:
- Data model (JSON schema)
- Module dependencies diagram
- CLI interface specifications
- Error handling strategy
```

**Expected Output**: Architecture design document

---

#### 3. Use `cs-backend-engineer` for Python Tool Implementation

**Task**: Implement the 7 Python tools

**Workflow:**
1. Use architecture design from cs-architect
2. Use cs-backend-engineer to implement each tool
3. Follow CLI-first design pattern
4. Ensure standard library only (or graceful fallbacks)

**Prompt (per tool):**
```
I need to implement `process_parser.py`, a Python CLI tool that parses process documentation from multiple formats (text, URL, images, transcripts) and outputs structured JSON.

Requirements:
- Support --input (file path), --url (web URL), --type (format), --output (JSON file)
- Parse text formats (Markdown, TXT) using regex and NLP
- Parse URLs (fetch HTML, convert to text, parse)
- Parse images (OCR with pytesseract, graceful fallback)
- Output JSON schema: {process_name, steps: [{id, name, role, duration, ...}], roles, gaps}
- Standard library only (urllib, json, argparse, re)
- Proper error handling and --help flag

Use the senior-backend-engineer skill to implement this tool following the repository's coding standards.
```

**Expected Output**: Working Python script with tests

**Repeat for all 7 tools**

---

#### 4. Use `cs-ux-researcher` for Reference Documentation

**Task**: Create the 3 reference documents (frameworks.md, templates.md, tools.md)

**Workflow:**
1. Use cs-ux-researcher to research best practices
2. Compile industry-standard frameworks
3. Create templates based on UX research

**Prompt:**
```
I need to create `references/frameworks.md` for the business-analyst-toolkit skill. This document should be a comprehensive guide to process mapping frameworks and methodologies.

Topics to cover:
- BPMN (Business Process Model and Notation) standards
- Swimlane diagram conventions
- Value Stream Mapping (Lean methodology)
- Six Sigma DMAIC framework
- Process mining techniques
- Lean principles (7 wastes, 5S, continuous improvement)

Use the ux-researcher-designer skill to:
- Research industry best practices
- Find authoritative sources and examples
- Structure the content for easy reference
- Create actionable guidance (not just theory)

The document should be 500+ lines and include visual examples (Mermaid diagrams).
```

**Expected Output**: Comprehensive reference document

**Repeat for templates.md and tools.md**

---

#### 5. Use `cs-agile-product-owner` for User Stories

**Task**: Create user stories for skill features and testing scenarios

**Workflow:**
1. Use cs-agile-product-owner to generate user stories
2. Create acceptance criteria for each tool
3. Plan testing scenarios

**Prompt:**
```
I need to create user stories for the business-analyst-toolkit skill to guide development and testing.

Personas:
- Business Analyst: Maps and optimizes business processes
- Product Manager: Documents product development workflows
- Operations Manager: Standardizes operational processes

Features to create stories for:
1. Parse process documentation from Confluence
2. Generate swimlane diagram from parsed process
3. Identify gaps in process definition
4. Calculate process efficiency metrics
5. Compare as-is vs to-be processes
6. Prioritize process improvements

Use the agile-product-owner skill to generate INVEST-compliant user stories with:
- User story format (As a..., I want..., So that...)
- Acceptance criteria
- Test scenarios
- Estimated effort (story points)
```

**Expected Output**: Backlog of user stories for implementation

---

#### 6. Use `cs-product-strategist` for OKR Alignment

**Task**: Define success metrics and OKRs for the skill

**Workflow:**
1. Use cs-product-strategist to define OKRs
2. Align skill metrics to repository goals
3. Plan rollout strategy

**Prompt:**
```
I need to define OKRs (Objectives and Key Results) for the new business-analyst-toolkit skill.

Objective: Launch business-analyst-toolkit as the 6th product-team skill and drive adoption

Use the product-strategist skill to help me:
- Define measurable key results
- Align to repository goals (26+ skills, community adoption)
- Create success metrics (usage, quality, time savings)
- Plan rollout and adoption strategy

Generate:
- OKR document
- Success metrics dashboard plan
- Adoption strategy
```

**Expected Output**: OKR document and success metrics plan

---

#### 7. Use `cs-code-reviewer` for Quality Assurance

**Task**: Review all Python tools and documentation for quality

**Workflow:**
1. Use cs-code-reviewer after each tool is implemented
2. Check for code quality, security, performance
3. Verify CLI standards and error handling

**Prompt (per tool):**
```
I've implemented `process_parser.py`. Please review the code for:
- Code quality and readability
- Security vulnerabilities (command injection, path traversal)
- Error handling and edge cases
- CLI interface consistency (--help, argument parsing)
- Performance (file I/O, parsing efficiency)
- Documentation (docstrings, comments)
- Repository standards compliance

Use the code-reviewer skill to provide a comprehensive code review with specific recommendations for improvement.
```

**Expected Output**: Code review report with actionable feedback

---

### Development Workflow Using Existing Skills:

```
Week 1: Foundation
├─ cs-product-manager: Create PRD
├─ cs-architect: Design architecture
└─ cs-backend-engineer: Implement process_parser.py
    └─ cs-code-reviewer: Review code

Week 2: Core Tools
├─ cs-backend-engineer: Implement process_mapper.py
│   └─ cs-code-reviewer: Review code
├─ cs-backend-engineer: Implement gap_analyzer.py
│   └─ cs-code-reviewer: Review code
└─ cs-ux-researcher: Create frameworks.md

Week 3: Analysis Tools
├─ cs-backend-engineer: Implement efficiency_analyzer.py
│   └─ cs-code-reviewer: Review code
├─ cs-backend-engineer: Implement metrics_builder.py
│   └─ cs-code-reviewer: Review code
└─ cs-ux-researcher: Create templates.md and tools.md

Week 4: Comparison & Prioritization
├─ cs-backend-engineer: Implement process_comparator.py
│   └─ cs-code-reviewer: Review code
├─ cs-backend-engineer: Implement improvement_prioritizer.py
│   └─ cs-code-reviewer: Review code
└─ cs-agile-product-owner: Create user stories for testing

Week 5: Agent Development
├─ cs-product-manager: Create agent "PRD"
├─ Create cs-business-analyst.md
└─ cs-product-strategist: Define OKRs and success metrics

Week 6: Documentation & Polish
├─ cs-code-reviewer: Final code review (all tools)
├─ cs-ux-researcher: Documentation review
└─ cs-agile-product-owner: Acceptance testing
```

---

## Testing Strategy

### Unit Testing (Per Tool):
```bash
# Test each tool with --help
python scripts/process_parser.py --help
python scripts/process_mapper.py --help
python scripts/gap_analyzer.py --help
python scripts/efficiency_analyzer.py --help
python scripts/metrics_builder.py --help
python scripts/process_comparator.py --help
python scripts/improvement_prioritizer.py --help

# Test each tool with sample data
python scripts/process_parser.py --input sample.txt --output process.json
cat process.json  # Verify valid JSON
```

### Integration Testing (Workflows):
```bash
# Workflow 1: Process Discovery
python scripts/process_parser.py --input process-doc.md --output process.json
python scripts/process_mapper.py --input process.json --type swimlane --format mermaid --output diagram.md
python scripts/gap_analyzer.py --input process.json --output gaps.md

# Workflow 2: Process Optimization
python scripts/efficiency_analyzer.py --input process.json --output metrics.json
python scripts/improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --output priorities.md
python scripts/process_comparator.py --current as-is.json --proposed to-be.json --output comparison.md

# Workflow 3: Cross-Skill Integration
python scripts/improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --format csv --output improvements.csv
python ../product-manager-toolkit/scripts/rice_prioritizer.py --input improvements.csv --output prioritized.csv
```

### End-to-End Testing (Agent Workflows):
```bash
# Test all 4 cs-business-analyst workflows
# 1. Process Discovery
# 2. Process Optimization
# 3. Process Documentation
# 4. Process Measurement

# Verify all outputs saved to output/process-analysis/
ls -la output/process-analysis/
```

---

## Success Criteria

### Skill Launch Ready When:

1. ✅ **All 7 Python tools implemented**
   - process_parser.py
   - process_mapper.py
   - gap_analyzer.py
   - efficiency_analyzer.py
   - metrics_builder.py
   - process_comparator.py
   - improvement_prioritizer.py

2. ✅ **All tools support required features**
   - --help flag
   - JSON output mode
   - Error handling
   - Multiple input/output formats

3. ✅ **All reference documents complete**
   - frameworks.md (500+ lines)
   - templates.md (400+ lines)
   - tools.md (300+ lines)

4. ✅ **All asset templates created**
   - process-charter-template.md
   - raci-matrix-template.md
   - improvement-proposal-template.md
   - stakeholder-analysis-template.md

5. ✅ **SKILL.md complete and comprehensive**
   - 600-800 lines
   - Quick start section
   - 3+ core workflows
   - Tool documentation
   - Integration examples

6. ✅ **cs-business-analyst agent complete**
   - YAML frontmatter
   - 4+ complete workflows
   - Tool integration examples
   - Success metrics

7. ✅ **Integration with existing skills tested**
   - product-manager-toolkit (RICE prioritizer)
   - agile-product-owner (user story generator)
   - product-strategist (OKR connector)

8. ✅ **All workflows tested end-to-end**
   - Process Discovery workflow
   - Process Optimization workflow
   - Process Documentation workflow
   - Process Measurement workflow

9. ✅ **Documentation updated**
   - skills/product-team/CLAUDE.md
   - Root CLAUDE.md (skill count: 26 → 27)
   - README.md (if applicable)

10. ✅ **Quality assurance passed**
    - Code reviewed by cs-code-reviewer
    - Documentation reviewed by cs-ux-researcher
    - Acceptance criteria met (cs-agile-product-owner)

---

## Git Workflow for Implementation

### Branch Strategy:
```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/business-analyst-toolkit

# Work in feature branch
# Commit frequently with conventional commits

# Examples:
git commit -m "feat(product-team): add business-analyst-toolkit skeleton"
git commit -m "feat(tools): implement process_parser.py"
git commit -m "feat(tools): implement process_mapper.py"
git commit -m "docs(references): add frameworks.md"
git commit -m "feat(agent): create cs-business-analyst agent"
git commit -m "test(integration): add cross-skill workflow tests"

# Push and create PR to dev
git push origin feature/business-analyst-toolkit
gh pr create --base dev --head feature/business-analyst-toolkit --title "feat: Add business-analyst-toolkit skill and agent"
```

### Commit Checklist:
- ✅ Use conventional commits (feat, fix, docs, test, chore)
- ✅ Keep commits atomic (one logical change per commit)
- ✅ Test before committing
- ✅ No secrets or credentials
- ✅ Update CLAUDE.md files when adding new features

---

## Expected Timeline

**Total Duration: 6 weeks**

| Week | Focus | Deliverables | Status |
|------|-------|-------------|--------|
| 1 | Foundation | Directory structure, SKILL.md skeleton, process_parser.py, frameworks.md | 🔴 Not Started |
| 2 | Core Tools | process_mapper.py, gap_analyzer.py, image parsing, templates.md | 🔴 Not Started |
| 3 | Analysis Tools | efficiency_analyzer.py, metrics_builder.py, tools.md, SKILL.md 80% | 🔴 Not Started |
| 4 | Comparison & Prioritization | process_comparator.py, improvement_prioritizer.py, asset templates, SKILL.md 100% | 🔴 Not Started |
| 5 | Agent Development | cs-business-analyst.md, integration testing, CLAUDE.md updates | 🔴 Not Started |
| 6 | Documentation & Polish | Comprehensive testing, documentation review, integration docs, QA | 🔴 Not Started |

---

## Post-Launch Tasks

### After V1 Launch:

1. **Gather User Feedback**
   - Survey users who try the skill
   - Track adoption metrics
   - Identify pain points and feature requests

2. **Plan V2 Features** (Based on deferred capabilities)
   - Real-time tracking integration (Jira, GitHub APIs)
   - Business outcome metrics (revenue, satisfaction)
   - Compliance & risk management
   - Process simulation & what-if analysis
   - Advanced collaboration features

3. **Create Tutorial/Demo**
   - Video walkthrough of key workflows
   - Blog post announcing the skill
   - Example processes for common use cases

4. **Integration Expansion**
   - Deeper integration with delivery-team skills (Jira, Confluence)
   - Integration with engineering-team skills (SDLC processes)
   - Integration with marketing-team skills (campaign processes)

---

## Quick Reference: Key Decisions

### Finalized Scope (V1):

| Decision | User Choice | Implementation |
|----------|------------|----------------|
| **V1 Scope** | Must-have capabilities | 7 Python tools (discovery, mapping, analysis, optimization) |
| **Input Formats** | URLs, text, sketches, transcripts | process_parser.py supports all |
| **Diagram Outputs** | All formats | Mermaid, SVG, PNG, HTML, Lucidchart, Miro |
| **Process Complexity** | All levels | Simple to complex cross-functional |
| **Time/Effort Tracking** | Manual input initially | User provides estimates when parsing |
| **Metrics Scope** | Process + efficiency | Cycle time, throughput, efficiency, cost |

### Future Enhancements (V2):

| Feature | Priority | Timeline |
|---------|---------|----------|
| Real-time tracking integration | Medium | Q1 2026 |
| Business outcome metrics | Medium | Q1 2026 |
| Compliance & risk management | Low | Q2 2026 |
| Process simulation | Low | Q2 2026 |
| Advanced collaboration | Low | Q2 2026 |

---

## Next Steps

### Immediate Actions:

1. **Review this implementation plan** ✅ (You are here)
2. **Exit plan mode and begin implementation** 🔴 (Ready when you are)
3. **Start with Week 1: Foundation**
   - Create directory structure
   - Use cs-product-manager to create PRD
   - Use cs-architect to design architecture
   - Use cs-backend-engineer to implement process_parser.py

### Commands to Execute (When Ready):

```bash
# 1. Create feature branch
git checkout dev
git pull origin dev
git checkout -b feature/business-analyst-toolkit

# 2. Create directory structure
mkdir -p skills/product-team/business-analyst-toolkit/{scripts,references,assets}

# 3. Copy templates
cp templates/skill-template.md skills/product-team/business-analyst-toolkit/SKILL.md

# 4. Begin Week 1 tasks
# Use cs-product-manager for PRD
# Use cs-architect for architecture design
# Use cs-backend-engineer for process_parser.py implementation
```

---

## Document Metadata

**Created By:** Claude Code (Plan Mode)
**Date:** November 20, 2025
**Based On:** User clarifications for business-analyst-toolkit
**Status:** ✅ READY FOR IMPLEMENTATION
**File Location:** `output/analysis/2025-11-20_business-analyst-implementation-plan.md`
**Related Documents:**
- Original planning session: `output/analysis/2025-11-20_business-analyst-skill-planning-session.md`
- Skill location: `skills/product-team/business-analyst-toolkit/` (to be created)
- Agent location: `agents/product/cs-business-analyst.md` (to be created)

---

**🎯 Ready to proceed with implementation when you exit plan mode! 🚀**
