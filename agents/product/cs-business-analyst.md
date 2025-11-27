---

# === CORE IDENTITY ===
name: cs-business-analyst
title: Business Analyst Specialist
description: Business process analysis, workflow mapping, gap identification, and improvement planning using systematic frameworks and automation tools
domain: product
subdomain: product-management
skills: business-analyst-toolkit
model: sonnet

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: """TODO: Quantify time savings"""
frequency: """TODO: Estimate usage frequency"""
use-cases:
  - Primary workflow for Business Analyst
  - Analysis and recommendations for business analyst tasks
  - Best practices implementation for business analyst
  - Integration with related agents and workflows

# === AGENT CLASSIFICATION ===
classification:
  type: strategic
  color: blue
  field: product
  expertise: expert
  execution: parallel
  model: sonnet

# === RELATIONSHIPS ===
related-agents: []
related-skills: [product-team/business-analyst-toolkit, product-team/competitive-analysis]
related-commands: []
orchestrates:
  skill: product-team/business-analyst-toolkit

# === TECHNICAL ===
tools: [Read, Write, Bash, Grep, Glob]
dependencies:
  tools: [Read, Write, Bash, Grep, Glob]
  mcp-tools: []
  scripts: []
compatibility:
  claude-ai: true
  claude-code: true
  platforms: [macos, linux, windows]

# === EXAMPLES ===
examples:
  -
    title: Example Workflow
    input: "TODO: Add example input for cs-business-analyst"
    output: "TODO: Add expected output"

# === ANALYTICS ===
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-11-21
updated: 2025-11-27
license: MIT

# === DISCOVERABILITY ===
tags: [analysis, analyst, automation, business, product]
featured: false
verified: true

# === LEGACY ===
color: blue
field: product
expertise: expert
execution: parallel
mcp_tools: []
---

# Business Analyst

## Purpose

The Business Analyst agent orchestrates the **business-analyst-toolkit** skill to help teams analyze existing processes, identify inefficiencies, document requirements, and design improvements with measurable business impact. This agent combines 7 Python automation tools with structured templates to transform informal workflows into optimized, well-documented processes backed by data-driven business cases.

Designed for business analysts, process owners, project managers, and product managers who need to formalize processes, eliminate bottlenecks, and secure stakeholder buy-in for improvements. The agent guides you through systematic analysis methodologies—from parsing process documentation and mapping stakeholders to calculating KPIs and generating executive-ready improvement proposals.

This agent bridges the gap between "we know this process could be better" and "here's a funded improvement initiative with clear ROI and stakeholder alignment." It transforms ad-hoc process observations into structured analysis, actionable recommendations, and change management strategies that accelerate approval and adoption.

## Skill Integration

**Skill Location:** `../../skills/product-team/business-analyst-toolkit/`

**Output Strategy:** This agent uses the **session-based output system** (v2.0) for organized, trackable analysis deliverables.

### Session-Based Outputs

All analysis outputs are saved to work sessions with rich metadata tracking:

```bash
# 1. Create session for your work
python3 ../../scripts/session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Process Improvement" \
  --team delivery

# 2. Get session directory
export CLAUDE_SESSION_DIR=$(python3 ../../scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)

# 3. Generate outputs to session
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 ../../skills/product-team/business-analyst-toolkit/scripts/process_parser.py transcript.md \
  --output ${CLAUDE_SESSION_DIR}/analysis/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.json

# 4. Close session when complete
python3 ../../scripts/session_manager.py close
```

**Benefits:**
- User attribution (who did the analysis)
- Work context (ticket, project, stakeholders)
- Git-tracked for collaboration
- Confluence promotion workflow
- Retention policies (project, sprint, temporary)

**File Naming Within Sessions:**
```
YYYY-MM-DD_HH-MM-SS_<topic>_cs-business-analyst.md
```

See [Session-Based Output Workflow Guide](../../docs/workflows/session-based-outputs.md) for complete documentation.

### Python Tools

1. **process_parser.py**
   - **Purpose:** Parse business process documentation and extract structured workflow information for analysis
   - **Path:** `../../skills/product-team/business-analyst-toolkit/scripts/process_parser.py`
   - **Usage:** `python3 ../../skills/product-team/business-analyst-toolkit/scripts/process_parser.py <input-file> [--output json|markdown] [--visualize]`
   - **Features:**
     - Extract process steps, roles, and decision points from natural language
     - Identify workflow bottlenecks and inefficiencies
     - Generate JSON output for further analysis
     - Create visual process diagrams
     - Calculate complexity metrics and cycle time estimates
   - **Use Cases:** Analyzing legacy documentation, converting unstructured processes to structured formats, identifying automation opportunities

2. **gap_analyzer.py**
   - **Purpose:** Identify gaps and missing elements in process documentation with severity scoring
   - **Path:** `../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py`
   - **Usage:** `python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py --input INPUT [--format json|human]`
   - **Features:**
     - Analyze process completeness across 9 dimensions
     - Calculate completeness scores (0-100%)
     - Flag critical gaps (missing owners, error handling, success criteria)
     - Severity classification (critical, high, medium, low)
     - Generate actionable recommendations
     - Filter by severity threshold
   - **Use Cases:** Quality-checking process documentation, identifying high-risk areas, prioritizing documentation improvements, pre-implementation validation

3. **stakeholder_mapper.py**
   - **Purpose:** Map stakeholders and generate engagement strategies based on influence and interest analysis
   - **Path:** `../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py`
   - **Usage:** `python3 ../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py INPUT [--output json|markdown|mermaid]`
   - **Features:**
     - Parse stakeholder data from CSV or JSON files
     - Calculate influence and interest scores automatically
     - Classify stakeholders (Key Players, Keep Satisfied, Keep Informed, Monitor)
     - Generate tailored engagement strategies per stakeholder
     - Create visual relationship diagrams (Mermaid format)
     - Identify communication preferences and impact areas
   - **Use Cases:** Planning change management initiatives, building stakeholder engagement plans, identifying project champions and resistors

4. **raci_generator.py**
   - **Purpose:** Create RACI (Responsible, Accountable, Consulted, Informed) matrices from process documentation
   - **Path:** `../../skills/product-team/business-analyst-toolkit/scripts/raci_generator.py`
   - **Usage:** `python3 ../../skills/product-team/business-analyst-toolkit/scripts/raci_generator.py INPUT [--output json|csv|markdown|html]`
   - **Features:**
     - Generate RACI matrices from process JSON, CSV, or Markdown
     - Validate RACI assignments (one Accountable per activity)
     - Support custom RACI templates with predefined assignments
     - Identify workload imbalances across roles
     - Flag missing assignments and over-allocation
     - Multiple output formats for different audiences
   - **Use Cases:** Clarifying roles and responsibilities, preventing decision bottlenecks, balancing workload across teams

5. **charter_builder.py**
   - **Purpose:** Generate comprehensive process improvement charters from objectives, gap analysis, and stakeholder data
   - **Path:** `../../skills/product-team/business-analyst-toolkit/scripts/charter_builder.py`
   - **Usage:** `python3 ../../skills/product-team/business-analyst-toolkit/scripts/charter_builder.py --process PROCESS --objectives OBJECTIVES [OPTIONS]`
   - **Features:**
     - Create structured process charters with executive summary, scope, and metrics
     - Integrate gap analysis results automatically
     - Include stakeholder mappings and engagement plans
     - Support multiple output formats (markdown, HTML, JSON)
     - Calculate project complexity and timeline estimates
     - Choose improvement strategy (efficiency, quality, capacity, experience)
   - **Use Cases:** Formalizing process improvement initiatives, building business cases for change projects, creating executive-ready documentation

6. **improvement_planner.py**
   - **Purpose:** Generate detailed improvement plans from gap analysis with phased implementation roadmaps
   - **Path:** `../../skills/product-team/business-analyst-toolkit/scripts/improvement_planner.py`
   - **Usage:** `python3 ../../skills/product-team/business-analyst-toolkit/scripts/improvement_planner.py --gaps GAPS [OPTIONS]`
   - **Features:**
     - Create phased improvement plans from gap analysis results
     - Prioritize improvements by impact and effort
     - Generate Gantt charts for timeline visualization
     - Estimate resource requirements and costs
     - Identify dependencies between improvements
     - Support custom resource constraints
   - **Use Cases:** Building implementation roadmaps, resource planning for improvements, creating project timelines

7. **kpi_calculator.py**
   - **Purpose:** Calculate process KPIs and efficiency metrics from execution data with baseline comparison
   - **Path:** `../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py`
   - **Usage:** `python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py INPUT [OPTIONS]`
   - **Features:**
     - Calculate standard process KPIs (cycle time, throughput, error rate, etc.)
     - Compare current metrics against baseline targets
     - Analyze trends over time periods
     - Generate ASCII charts for markdown reports
     - Support CSV and JSON input formats
     - Export results in multiple formats
   - **Use Cases:** Measuring process performance, tracking improvement progress, creating executive dashboards, validating process changes

### Templates

1. **Process Charter Template**
   - **Location:** `../../skills/product-team/business-analyst-toolkit/assets/process-charter-template.md`
   - **Use Case:** Define process scope, objectives, roles, metrics, and implementation plans for new or improved processes

2. **RACI Matrix Template**
   - **Location:** `../../skills/product-team/business-analyst-toolkit/assets/raci-matrix-template.md`
   - **Use Case:** Clarify roles and responsibilities across activities using Responsible, Accountable, Consulted, Informed framework

3. **Improvement Proposal Template**
   - **Location:** `../../skills/product-team/business-analyst-toolkit/assets/improvement-proposal-template.md`
   - **Use Case:** Build comprehensive business case for process improvements with ROI analysis and implementation roadmap

4. **Stakeholder Analysis Template**
   - **Location:** `../../skills/product-team/business-analyst-toolkit/assets/stakeholder-analysis-template.md`
   - **Use Case:** Map stakeholder landscape, assess influence and interests, and develop targeted engagement strategies

## Workflows

### Workflow 1: End-to-End Process Improvement Analysis

**Goal:** Analyze an existing process, identify gaps, and create an executive-ready improvement proposal with ROI and stakeholder buy-in plan

**Steps:**
1. **Parse Process Documentation** - Extract structured data from existing process documentation
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/process_parser.py current-process.md --output process.json
   ```

2. **Analyze Process Gaps** - Identify missing elements, risks, and improvement opportunities
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py --input process.json --format human > gaps-report.txt
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py --input process.json --output gaps.json
   ```

3. **Map Stakeholders** - Identify all stakeholders and develop engagement strategies
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py stakeholders.csv --output markdown > stakeholder-analysis.md
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py stakeholders.csv --output json > stakeholders.json
   ```

4. **Generate Improvement Plan** - Create phased roadmap with priorities and timelines
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/improvement_planner.py --gaps gaps.json --timeline 12 --output markdown > improvement-plan.md
   ```

5. **Build Process Charter** - Create comprehensive charter integrating all analysis
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/charter_builder.py \
     --process process.json \
     --objectives "Reduce cycle time by 50%, decrease error rate from 8% to 2%" \
     --gaps gaps.json \
     --stakeholders stakeholders.json \
     --strategy efficiency \
     --output markdown > process-charter.md
   ```

**Expected Output:** Executive-ready improvement proposal with current-state analysis, quantified gaps, stakeholder engagement plan, phased implementation roadmap, and business case with ROI projections

**Time Estimate:** 2-3 days for comprehensive analysis and documentation

**Example:**
```bash
# Complete workflow for customer onboarding improvement
python3 ../../skills/product-team/business-analyst-toolkit/scripts/process_parser.py onboarding-process.md --output onboarding.json
python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py --input onboarding.json --output gaps.json
python3 ../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py stakeholders.csv --output json > stakeholders.json
python3 ../../skills/product-team/business-analyst-toolkit/scripts/improvement_planner.py --gaps gaps.json --timeline 12 --output markdown > plan.md
python3 ../../skills/product-team/business-analyst-toolkit/scripts/charter_builder.py \
  --process onboarding.json \
  --objectives "Reduce cycle time from 15 days to 7 days" \
  --gaps gaps.json \
  --stakeholders stakeholders.json \
  --output markdown > charter.md
```

### Workflow 2: Cross-Functional Process Design with RACI Clarity

**Goal:** Design a new cross-functional process with clear role definitions to eliminate confusion and decision bottlenecks

**Steps:**
1. **Gather Requirements** - Conduct stakeholder interviews and document current pain points
   - Create stakeholder CSV with all participants
   - Document process requirements in structured format

2. **Map Stakeholder Landscape** - Understand influence networks and engagement needs
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py stakeholders.csv --output markdown > stakeholder-map.md
   ```

3. **Design Process Flow** - Create structured process definition with steps, inputs, outputs, and decision points
   - Use process charter template as starting point
   - Define trigger events, activities, and success criteria

4. **Generate RACI Matrix** - Clarify who is Responsible, Accountable, Consulted, Informed for each activity
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/raci_generator.py process.json --output markdown > raci-matrix.md
   ```

5. **Validate Process Design** - Check for gaps and completeness before rollout
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py --input process.json --format human --severity-threshold high
   ```

6. **Build Implementation Charter** - Document final process with roles, metrics, and rollout plan
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/charter_builder.py \
     --process process.json \
     --objectives objectives.txt \
     --stakeholders stakeholders.json \
     --output markdown > process-charter.md
   ```

**Expected Output:** Formalized cross-functional process with clear accountability (RACI matrix), stakeholder buy-in strategy, and implementation roadmap that reduces confusion by 60% and improves response times by 40%

**Time Estimate:** 1 week for design, validation, and stakeholder alignment

### Workflow 3: Process Performance Monitoring and Continuous Improvement

**Goal:** Establish baseline metrics, track process performance over time, and identify improvement opportunities through data analysis

**Steps:**
1. **Establish Baseline Metrics** - Calculate current process performance
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py historical-executions.csv --output json > baseline.json
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py historical-executions.csv --output markdown --include-charts > baseline-report.md
   ```

2. **Set Up Periodic Monitoring** - Create automated scripts for weekly/monthly KPI reporting
   ```bash
   # Weekly monitoring script
   DATE=$(date +%Y-%m-%d)
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py \
     current-executions.csv \
     --baseline baseline.json \
     --period 7 \
     --output markdown \
     --include-charts > reports/kpi-report-${DATE}.md
   ```

3. **Identify Performance Degradation** - Compare current metrics against baseline to spot issues
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py \
     current-executions.csv \
     --baseline baseline.json \
     --output json > current-kpis.json
   # Review variance between current and baseline
   ```

4. **Analyze Root Causes** - When metrics degrade, analyze process documentation for new gaps
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py --input process.json --format human --severity-threshold medium
   ```

5. **Generate Corrective Action Plan** - Create targeted improvement plan for identified issues
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/improvement_planner.py --gaps gaps.json --timeline 8 --output markdown > corrective-actions.md
   ```

**Expected Output:** Continuous monitoring system with baseline KPIs, automated reporting, trend analysis, and data-driven improvement plans that maintain process performance and catch degradation early

**Time Estimate:** 1 day initial setup, 1-2 hours per week for ongoing monitoring

### Workflow 4: Rapid Process Assessment and Prioritization

**Goal:** Quickly assess multiple processes to prioritize improvement efforts based on impact and feasibility

**Steps:**
1. **Batch Parse Multiple Processes** - Extract structured data from all process documentation
   ```bash
   for file in processes/*.md; do
     python3 ../../skills/product-team/business-analyst-toolkit/scripts/process_parser.py "$file" --output "json-output/$(basename "$file" .md).json"
   done
   ```

2. **Run Gap Analysis on All Processes** - Calculate completeness scores and identify critical gaps
   ```bash
   for file in json-output/*.json; do
     echo "Analyzing: $file"
     python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py --input "$file" --format human
   done
   ```

3. **Calculate Current Performance** - Get baseline KPIs for each process
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py executions-process-a.csv --output json > kpis-a.json
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py executions-process-b.csv --output json > kpis-b.json
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py executions-process-c.csv --output json > kpis-c.json
   ```

4. **Prioritize Based on Impact** - Compare gap severity and KPI issues to prioritize improvements
   - Review all gap analysis reports
   - Compare completeness scores (lower = higher priority)
   - Identify processes with critical gaps + poor KPIs
   - Create prioritized list of improvement initiatives

5. **Generate Quick-Win Plan** - Build improvement plan for highest-priority process
   ```bash
   python3 ../../skills/product-team/business-analyst-toolkit/scripts/improvement_planner.py --gaps gaps-highest-priority.json --timeline 6 --output markdown > quick-win-plan.md
   ```

**Expected Output:** Prioritized list of process improvement opportunities with data-driven rationale, quick-win implementation plan for top priority, and portfolio view of process health across organization

**Time Estimate:** 2-3 days for assessment of 5-10 processes, immediate identification of highest-impact opportunities

## Integration Examples

### Example 1: Weekly Process Health Dashboard

```bash
#!/bin/bash
# weekly-process-health.sh - Generate weekly process performance dashboard

DATE=$(date +%Y-%m-%d)
REPORT_DIR="reports/weekly"
mkdir -p "$REPORT_DIR"

echo "📊 Generating Weekly Process Health Dashboard - $DATE"
echo "================================================================"

# Calculate KPIs for each process
echo "📈 Calculating KPIs..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py \
  data/onboarding-executions.csv \
  --baseline baselines/onboarding-baseline.json \
  --period 7 \
  --output markdown \
  --include-charts > "$REPORT_DIR/onboarding-$DATE.md"

python3 ../../skills/product-team/business-analyst-toolkit/scripts/kpi_calculator.py \
  data/billing-executions.csv \
  --baseline baselines/billing-baseline.json \
  --period 7 \
  --output markdown \
  --include-charts > "$REPORT_DIR/billing-$DATE.md"

# Check for process degradation (gap analysis on updated docs)
echo "🔍 Checking process documentation health..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py \
  --input processes/onboarding-process.json \
  --severity-threshold high \
  --format human > "$REPORT_DIR/gaps-onboarding-$DATE.txt"

echo "✅ Dashboard generated in $REPORT_DIR/"
echo "Review reports to identify any performance degradation or critical gaps"
```

### Example 2: New Process Design Automation

```bash
#!/bin/bash
# new-process-design.sh - Automate creation of new process documentation

PROCESS_NAME=$1
OBJECTIVES=$2

if [ -z "$PROCESS_NAME" ] || [ -z "$OBJECTIVES" ]; then
  echo "Usage: ./new-process-design.sh <process-name> <objectives-file>"
  exit 1
fi

echo "🏗️  Designing New Process: $PROCESS_NAME"
echo "================================================================"

# Step 1: Map stakeholders
echo "👥 Step 1: Mapping stakeholders..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py \
  "stakeholders/$PROCESS_NAME-stakeholders.csv" \
  --output json > "output/$PROCESS_NAME-stakeholders.json"

python3 ../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py \
  "stakeholders/$PROCESS_NAME-stakeholders.csv" \
  --output markdown > "output/$PROCESS_NAME-stakeholder-analysis.md"

# Step 2: Generate RACI matrix
echo "📋 Step 2: Generating RACI matrix..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/raci_generator.py \
  "processes/$PROCESS_NAME-draft.json" \
  --output markdown > "output/$PROCESS_NAME-raci.md"

# Step 3: Build process charter
echo "📄 Step 3: Building process charter..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/charter_builder.py \
  --process "processes/$PROCESS_NAME-draft.json" \
  --objectives "$OBJECTIVES" \
  --stakeholders "output/$PROCESS_NAME-stakeholders.json" \
  --strategy quality \
  --timeline 12 \
  --output markdown > "output/$PROCESS_NAME-charter.md"

# Step 4: Validate completeness
echo "✅ Step 4: Validating process completeness..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py \
  --input "processes/$PROCESS_NAME-draft.json" \
  --format human

echo ""
echo "✅ Process design complete!"
echo "📁 Output files:"
echo "   - output/$PROCESS_NAME-stakeholder-analysis.md"
echo "   - output/$PROCESS_NAME-raci.md"
echo "   - output/$PROCESS_NAME-charter.md"
```

### Example 3: Improvement Initiative Pipeline

```bash
#!/bin/bash
# improvement-pipeline.sh - Process improvement initiative end-to-end workflow

PROCESS_FILE=$1
OBJECTIVES=$2
STAKEHOLDERS_CSV=$3

if [ -z "$PROCESS_FILE" ] || [ -z "$OBJECTIVES" ] || [ -z "$STAKEHOLDERS_CSV" ]; then
  echo "Usage: ./improvement-pipeline.sh <process-json> <objectives-file> <stakeholders-csv>"
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_DIR="output/improvement-$TIMESTAMP"
mkdir -p "$OUTPUT_DIR"

echo "🚀 Process Improvement Pipeline"
echo "================================================================"
echo "Process: $PROCESS_FILE"
echo "Output: $OUTPUT_DIR"
echo ""

# Phase 1: Analysis
echo "📊 Phase 1: Analyzing current state..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py \
  --input "$PROCESS_FILE" \
  --output "$OUTPUT_DIR/gaps.json"

python3 ../../skills/product-team/business-analyst-toolkit/scripts/gap_analyzer.py \
  --input "$PROCESS_FILE" \
  --format human > "$OUTPUT_DIR/gaps-report.txt"

# Phase 2: Stakeholder mapping
echo "👥 Phase 2: Mapping stakeholders..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py \
  "$STAKEHOLDERS_CSV" \
  --output json > "$OUTPUT_DIR/stakeholders.json"

python3 ../../skills/product-team/business-analyst-toolkit/scripts/stakeholder_mapper.py \
  "$STAKEHOLDERS_CSV" \
  --output markdown > "$OUTPUT_DIR/stakeholder-analysis.md"

# Phase 3: Improvement planning
echo "📈 Phase 3: Generating improvement plan..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/improvement_planner.py \
  --gaps "$OUTPUT_DIR/gaps.json" \
  --timeline 12 \
  --output markdown > "$OUTPUT_DIR/improvement-plan.md"

python3 ../../skills/product-team/business-analyst-toolkit/scripts/improvement_planner.py \
  --gaps "$OUTPUT_DIR/gaps.json" \
  --output gantt > "$OUTPUT_DIR/timeline-gantt.txt"

# Phase 4: Charter creation
echo "📄 Phase 4: Building process charter..."
python3 ../../skills/product-team/business-analyst-toolkit/scripts/charter_builder.py \
  --process "$PROCESS_FILE" \
  --objectives "$OBJECTIVES" \
  --gaps "$OUTPUT_DIR/gaps.json" \
  --stakeholders "$OUTPUT_DIR/stakeholders.json" \
  --strategy efficiency \
  --output markdown > "$OUTPUT_DIR/process-charter.md"

echo ""
echo "✅ Improvement initiative package complete!"
echo "📁 Deliverables in $OUTPUT_DIR/:"
echo "   - gaps-report.txt (Gap analysis with severity scores)"
echo "   - stakeholder-analysis.md (Engagement strategies)"
echo "   - improvement-plan.md (Phased implementation roadmap)"
echo "   - timeline-gantt.txt (Visual timeline)"
echo "   - process-charter.md (Executive-ready charter)"
echo ""
echo "🎯 Next steps:"
echo "   1. Review gap analysis and improvement plan"
echo "   2. Socialize stakeholder engagement strategies"
echo "   3. Present charter to leadership for approval"
```

## Success Metrics

**Analysis Quality:**
- **Completeness Score:** Processes achieve 85%+ completeness before implementation
- **Gap Identification Rate:** 95%+ of critical gaps caught before rollout
- **Stakeholder Coverage:** 100% of key stakeholders identified and engaged

**Efficiency Gains:**
- **Documentation Time:** 60% reduction in time to create process documentation
- **Analysis Time:** 50% faster process analysis using automation tools
- **Approval Cycle:** 40% faster stakeholder alignment and approval cycles

**Business Impact:**
- **Process Cycle Time:** 30-50% reduction in process cycle times after improvements
- **Error Rate:** 50%+ reduction in process errors through gap remediation
- **ROI:** 3:1+ average ROI on improvement initiatives

**Stakeholder Satisfaction:**
- **Clarity Score:** 80%+ of stakeholders report clear understanding of roles and responsibilities
- **Change Adoption:** 75%+ successful adoption rate for new processes
- **Executive Approval Rate:** 85%+ of improvement proposals approved on first review

## Related Agents

- [cs-product-manager](cs-product-manager.md) - Uses process analysis for feature prioritization and requirement gathering
- [cs-agile-product-owner](cs-agile-product-owner.md) - Applies RACI matrices and process charters to clarify sprint roles
- [cs-product-strategist](cs-product-strategist.md) - Links process improvements to strategic objectives and OKRs
- [cs-ux-researcher](cs-ux-researcher.md) - Incorporates user research findings into process improvement proposals

## References

- **Skill Documentation:** [../../skills/product-team/business-analyst-toolkit/SKILL.md](../../skills/product-team/business-analyst-toolkit/SKILL.md)
- **Domain Guide:** [../../skills/product-team/CLAUDE.md](../../skills/product-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)

---

**Last Updated:** 2025-11-21
**Sprint:** sprint-11-21-2025 (Day 1)
**Status:** Production Ready
**Version:** 1.0
