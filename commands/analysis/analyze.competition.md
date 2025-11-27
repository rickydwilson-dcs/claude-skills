---
# === CORE IDENTITY ===
name: analyze.competition
title: Competitive Analysis for Claude Skills
description: Competitive analysis command comparing skills, commands, and agents against external repositories with scorecard generation and adoption recommendations
category: analysis
subcategory: competitive-intelligence

# === WEBSITE DISPLAY ===
difficulty: intermediate
time-saved: "3-4 hours per competitive analysis"
frequency: "Monthly per product team"

use-cases:
  - "Comparing skill packages against competitor implementations to identify feature gaps"
  - "Benchmarking command coverage and capabilities against similar automation tools"
  - "Evaluating agent workflows against external orchestration patterns"
  - "Generating strategic adoption recommendations based on competitive intelligence"
  - "Creating executive-ready scorecards for product strategy decisions"

# === RELATIONSHIPS (Cross-linking) ===
related-agents:
  - cs-code-reviewer
  - cs-architect
  - cs-product-strategist
  - cs-business-analyst

related-skills:
  - engineering-team/code-reviewer
  - product-team/product-strategist
  - product-team/product-manager-toolkit

related-commands:
  - /review.code
  - /audit.dependencies
  - /audit.security

# === TECHNICAL ===
dependencies:
  tools:
    - Read
    - Write
    - Bash
    - Grep
    - Glob

  scripts: []
  python-packages: []

compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows

# === EXAMPLES ===
examples:
  - title: "Basic Competitive Analysis from Pasted Code"
    input: |
      /analyze.competition
      [User pastes competitor skill/command code directly in chat]
    output: |
      Competitive Analysis Report
      US (claude-skills) vs THEM (Competitor)

      SCORECARD
      ┌─────────────────────┬───────────┬───────────┬─────────────────┐
      │ Category            │ US        │ THEM      │ Winner          │
      ├─────────────────────┼───────────┼───────────┼─────────────────┤
      │ Documentation       │ 92        │ 60        │ 🏆 US (+32)     │
      │ Python Tooling      │ 78        │ 85        │ ❌ THEM (-7)    │
      └─────────────────────┴───────────┴───────────┴─────────────────┘

      RECOMMENDATIONS FOR US:
      - Add more Python tooling to close gap

      Report saved to: output/sessions/{user}/{session}/competition-analysis.md

  - title: "Skill Package Comparison"
    input: |
      /analyze.competition --scope skills
      [User pastes competitor SKILL.md and scripts]
    output: |
      Skill Package Competitive Analysis
      US (claude-skills) vs THEM (Competitor)

      PACKAGE COMPARISON
      ┌────────────────────┬──────────────┬──────────────┬─────────────┐
      │ Aspect             │ US           │ THEM         │ Winner      │
      ├────────────────────┼──────────────┼──────────────┼─────────────┤
      │ Python Tools       │ 3 scripts    │ 5 scripts    │ ❌ THEM     │
      │ Reference Docs     │ 3 guides     │ 1 guide      │ 🏆 US       │
      │ Dependencies       │ stdlib only  │ 4 packages   │ 🏆 US       │
      └────────────────────┴──────────────┴──────────────┴─────────────┘

      RECOMMENDATIONS FOR US:
      - Add 2 more Python scripts to match their tooling depth

  - title: "Agent Workflow Comparison"
    input: |
      /analyze.competition --scope agents
      [User pastes competitor agent/workflow definition]
    output: |
      Agent Workflow Competitive Analysis
      US (claude-skills) vs THEM (Competitor)

      ORCHESTRATION PATTERNS:
      ┌──────────────────┬───────────────┬───────────────┬─────────────┐
      │ Pattern          │ US            │ THEM          │ Winner      │
      ├──────────────────┼───────────────┼───────────────┼─────────────┤
      │ Multi-Phase      │ Supported     │ Supported     │ 🤝 TIE      │
      │ Skill Refs       │ Relative      │ Absolute      │ 🏆 US       │
      │ Model Selection  │ Configurable  │ Fixed         │ 🏆 US       │
      └──────────────────┴───────────────┴───────────────┴─────────────┘

  - title: "Command Pattern Analysis"
    input: |
      /analyze.competition --scope commands
      [User pastes competitor command definition]
    output: |
      Command Pattern Competitive Analysis
      US (claude-skills) vs THEM (Competitor)

      US Pattern: Multi-Phase (Discovery -> Analysis -> Task -> Report)
      THEM Pattern: Simple (Context -> Task)

      Winner: 🏆 US - Our multi-phase approach provides 40% more insights

      RECOMMENDATIONS FOR US:
      - None needed - maintain this advantage

# === ANALYTICS ===
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors:
  - Product Team
  - Engineering Team
created: 2025-11-27
updated: 2025-11-27

# === DISCOVERABILITY ===
tags:
  - competitive-analysis
  - gap-analysis
  - scorecard
  - benchmarking
  - strategic-planning
  - skill-comparison
  - command-comparison
  - agent-comparison
  - adoption-recommendations

featured: false
verified: true
license: MIT

---

# Competitive Analysis

Comprehensive competitive analysis command that compares skills, commands, and agents against external repositories. This multi-phase command generates scorecards, identifies feature gaps, and provides strategic adoption recommendations to inform product decisions.

---

## Pattern Type: Multi-Phase

**Complexity:** Intermediate
**Execution Time:** 5-15 minutes depending on analysis scope
**Destructive:** No (read-only analysis, outputs saved to session)

---

## Usage

```bash
/analyze.competition [options]
```

### Input Method

**Paste competitor code directly in chat after invoking the command:**

```bash
# Basic usage - then paste competitor code in chat
/analyze.competition

# Scope filtering
/analyze.competition --scope skills
/analyze.competition --scope commands
/analyze.competition --scope agents
/analyze.competition --scope all  # default

# Output format
/analyze.competition --output markdown  # default
/analyze.competition --output json
```

### Workflow

1. User invokes `/analyze.competition`
2. Command prompts: "Please paste the competitor code you want to analyze..."
3. User pastes code (SKILL.md, agent files, command files, etc.)
4. Command analyzes and generates report
5. Report displayed in console AND auto-saved to session directory

### Output Behavior

- Always displays full report in console
- Always auto-saves to `output/sessions/{user}/{session-id}/competitive-analysis-{timestamp}.md`
- Creates session if none exists
- Updates `.session-metadata.yaml` with output entry

---

## What This Command Does

### Context Gathering

The command will:
1. Parse the pasted competitor code to identify structure
2. Detect type (skill package, command, or agent)
3. Extract metadata, features, and technical details
4. Load comparable claude-skills assets for comparison
5. Build feature comparison matrix

### Task Execution

Then it will:
1. Score each category for both implementations
2. Calculate competitive deltas
3. Identify gaps requiring attention
4. Highlight advantages to leverage
5. Generate prioritized adoption recommendations
6. Create comprehensive report

### Expected Output

You will receive:
- Competitive scorecard with category scores
- Gap analysis with prioritized findings
- Adoption recommendations (ADOPT/CONSIDER/MONITOR)
- Executive summary of competitive position
- Detailed report saved to session directory

---

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Inventory pasted competitor content and catalog our repository assets to build a comparison matrix

**Steps:**

1. **Parse Competitor Input**
   - Accept pasted code/content from user in chat (markdown files, agent definitions, skill packages)
   - Extract any YAML frontmatter metadata from competitor content
   - Identify content type based on structural patterns:
     - **Skills:** Presence of `SKILL.md` file, `scripts/` directory, `references/` directory
     - **Commands:** YAML frontmatter with `name:`, `pattern:`, `category:` fields
     - **Agents:** `cs-*` prefix in filename, `skills:` field in frontmatter, `workflows` sections

2. **Inventory Our Repository**
   - Scan `skills/` directory for all SKILL.md files (28 skills across 4 domains)
   - Scan `agents/` directory for all cs-* prefixed files (28 agents)
   - Scan `commands/` directory for command markdown files (13 commands)
   - Extract metadata from each asset's YAML frontmatter

3. **Build Comparison Matrix**
   - **Name Matching:** Direct name/title comparison (exact or fuzzy)
   - **Domain Matching:** Map competitor domains to our domains (engineering, product, marketing, delivery)
   - **Semantic Matching:** Identify functional equivalents based on description similarity, use-case overlap, tags and keywords

4. **Generate Match Candidates**
   - For each competitor item, identify 0-3 potential matches from our repository
   - Categorize matches by confidence: High (>80%), Medium (50-80%), Low (<50%)
   - Flag items with no matches as potential gaps

**Tools Used:** Read, Glob, Grep

**Output:**
```
Discovery Summary
================
Competitor Assets Detected:
- Skills: [count] identified
- Commands: [count] identified
- Agents: [count] identified

Our Repository Assets:
- Skills: 28 (4 domains)
- Commands: 13 (5 categories)
- Agents: 28 (4 domains)

Match Candidates Generated: [count] comparisons queued
```

---

### Phase 2: Analysis

**Goal:** Deep comparison across six scoring dimensions with weighted scoring

**Scoring Dimensions:**

| Dimension | Weight | What to Evaluate |
|-----------|--------|------------------|
| **Documentation Completeness** | 20% | YAML metadata, sections, examples |
| **Tool/Script Quality** | 20% | Python tools, CLI support, dependencies |
| **Workflow Coverage** | 15% | Documented workflows (4+ for agents) |
| **Architecture** | 15% | Zero-dependency, portability |
| **Automation** | 15% | Auto-generation, validation |
| **Reference Depth** | 15% | Knowledge bases, templates |

**Scoring System (per dimension):**
- 5 stars (90-100): Industry-leading (significant competitive advantage)
- 4 stars (80-89): Strong (clear advantage)
- 3 stars (70-79): Competitive (at parity)
- 2 stars (60-69): Needs improvement (competitive gap)
- 1 star (<60): Critical gap (urgent attention required)

**Winner Determination:**
- **Better** (our score higher by >10 points)
- **Same** (scores within 10 points)
- **Different** (similar score, different approach)
- **Behind** (our score lower by >10 points)

**Tools Used:** Read, Grep, Glob

---

### Phase 3: Gap Analysis

**Goal:** Identify opportunities and threats through systematic gap identification

**Analysis Types:**

1. **Gaps to Fill** (What they have that we don't)
   - New capabilities: Entirely new skill/command/agent types
   - Feature enhancements: Additional features in existing equivalents
   - Domain expansion: Coverage of domains we don't address
   - Tool additions: Scripts or automation we lack

2. **Competitive Advantages** (What we have that they don't)
   - Unique assets: Skills/commands/agents they lack entirely
   - Superior implementation: Better quality in matched items
   - Deeper coverage: More workflows, tools, or documentation
   - Architectural strengths: Zero dependencies, better portability

3. **Different Approaches** (Neither better, just different)
   - Structural differences: Different file/folder organization
   - Tooling choices: Different languages, frameworks, or patterns
   - Workflow philosophy: Different approaches to same problem

4. **Priority Improvements** (Areas where we're behind)
   - Items where competitor scores higher
   - Specific dimensions where we underperform
   - Prioritized improvement backlog

**Prioritization Scoring:**
```
Priority Score = (Impact * 0.4) + (Urgency * 0.3) + (Strategic * 0.2) + (1/Effort * 0.1)
```

---

### Phase 4: Reporting

**Goal:** Generate comprehensive output with executive summary and actionable recommendations

**Report Sections:**

1. **Executive Summary**
   - One-paragraph competitive landscape overview
   - Key metrics: items analyzed, overall scores, critical findings
   - Top 3 strategic recommendations
   - Overall competitive position assessment

2. **Quick Scorecard** (visual ASCII box)
   ```
   ┌─────────────────────────────────────────────────────────────┐
   │                    COMPETITIVE ANALYSIS                      │
   ├─────────────────────────────────────────────────────────────┤
   │                                                              │
   │  Better:    X features  (XX%)  ████████████░░░░░░░░        │
   │  Same:      X features  (XX%)  ████░░░░░░░░░░░░░░░░        │
   │  Different: X features  (XX%)  ██░░░░░░░░░░░░░░░░░░        │
   │  Behind:    X features  (XX%)  ██░░░░░░░░░░░░░░░░░░        │
   │                                                              │
   │  Overall Assessment: [POSITION]                              │
   │                                                              │
   └─────────────────────────────────────────────────────────────┘
   ```

3. **Feature Comparison Matrix** (table)
   - Side-by-side capability comparison
   - Presence/absence indicators
   - Quality ratings per feature

4. **Critical Differentiators**
   - Top 5 competitive advantages (with star ratings)
   - Top gaps requiring attention
   - Strategic implications

5. **Gap Analysis Summary**
   - Prioritized gap list with effort/impact ratings
   - Advantages to leverage
   - Improvements needed

6. **Adoption Recommendations**
   - **Immediate Actions** (This Sprint): Complete within 2 weeks
   - **Short-term Actions** (This Quarter): Complete within 90 days
   - **Long-term Actions** (Next 2-4 Quarters): Roadmap items

7. **Strategic Assessment**
   - Market position map (ASCII diagram)
   - Competitive threat assessment
   - Recommended strategy: Double Down / Close Gaps / Differentiate / Monitor

**Output Delivery:**
- Console display: Full report rendered in terminal
- Session file: Auto-save to `output/sessions/{user}/{session-id}/competitive-analysis-{timestamp}.md`

---

## Report Templates

### Quick Scorecard Format

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPETITIVE ANALYSIS                      │
│                US (claude-skills) vs THEM (Competitor)       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🏆 WE WIN:    12 areas (60%)  ████████████░░░░░░░░        │
│  🤝 TIE:        4 areas (20%)  ████░░░░░░░░░░░░░░░░        │
│  🔄 DIFFERENT:  2 areas (10%)  ██░░░░░░░░░░░░░░░░░░        │
│  ❌ THEY WIN:   2 areas (10%)  ██░░░░░░░░░░░░░░░░░░        │
│                                                              │
│  Overall Position: WE ARE AHEAD                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Feature Comparison Matrix Format

| Category | Feature | US | THEM | Winner | Recommendation for US |
|----------|---------|-----|------|--------|----------------------|
| **Documentation** | YAML Metadata | Complete | Partial | 🏆 US | Maintain advantage |
| | Workflow Docs | 4+ workflows | 2 workflows | 🏆 US | Maintain advantage |
| **Tooling** | Python Scripts | 3 scripts | 5 scripts | ❌ THEM | Add more scripts |
| | CLI Support | Full --help | Basic | 🏆 US | Maintain advantage |
| **Architecture** | Dependencies | stdlib only | 4 packages | 🏆 US | Maintain advantage |

### Differentiator Scores Format

```
US (claude-skills) vs THEM (Competitor)

Dimension         US          THEM        Winner
─────────────────────────────────────────────────
Documentation     ★★★★★       ★★★☆☆       🏆 US (+2)
Tool Quality      ★★★★☆       ★★★★★       ❌ THEM (-1) ← Gap to fill
Workflow Coverage ★★★★★       ★★★☆☆       🏆 US (+2)
Architecture      ★★★★★       ★★★☆☆       🏆 US (+2)
Automation        ★★★★☆       ★★★☆☆       🏆 US (+1)
References        ★★★★☆       ★★★☆☆       🏆 US (+1)

OVERALL:          ★★★★☆       ★★★☆☆       🏆 WE ARE AHEAD
```

### Strategic Assessment Format

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                STRATEGIC RECOMMENDATIONS FOR US                              │
│                     (Based on competitive analysis)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🏆 DOUBLE DOWN (Extend Our Advantages)                                      │
│  ──────────────────────────────────────                                      │
│  - Zero-dependency architecture - this is our moat                           │
│  - Documentation quality - expand our tutorials and examples                 │
│                                                                              │
│  ❌ CLOSE GAPS (What We Need to Improve)                                     │
│  ───────────────────────────────────────                                     │
│  - Python tooling count - add missing automation scripts                     │
│  - Integration patterns - learn from their approach                          │
│                                                                              │
│  🚀 DIFFERENTIATE (Create New Advantages for Us)                             │
│  ───────────────────────────────────────────────                             │
│  - AI-powered features - get ahead of commoditization                        │
│  - Developer community - build ecosystem lock-in                             │
│                                                                              │
│  👀 MONITOR (Watch What They Do)                                             │
│  ───────────────────────────────                                             │
│  - Their feature releases                                                    │
│  - New market entrants                                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Success Criteria

This command is successful when:

- [ ] All competitor content is correctly parsed and categorized
- [ ] Match candidates are generated with confidence scores
- [ ] All 6 scoring dimensions are evaluated per item
- [ ] Weighted scores are calculated correctly
- [ ] Gaps and advantages are identified and prioritized
- [ ] Complete report is generated with all 7 sections
- [ ] Report is saved to session directory automatically
- [ ] Actionable recommendations are provided

### Quality Metrics

**Expected Outcomes:**
- **Match Accuracy:** 85%+ of semantic matches correctly identified
- **Scoring Consistency:** Inter-rater reliability >90% on dimension scoring
- **Gap Detection:** 95%+ of significant gaps identified
- **Report Completeness:** All 7 sections populated with relevant content
- **Actionable Output:** Each finding includes specific next steps

---

## Error Handling

### Common Issues

**Issue:** "Unable to determine competitor type"
**Cause:** Pasted code lacks identifiable structure (no YAML frontmatter, no recognizable patterns)
**Solution:** Use --scope flag to specify: skills, commands, or agents
**Prevention:** Paste complete files with metadata/frontmatter

---

**Issue:** "No comparable local asset found"
**Cause:** Competitor code is in a domain we don't cover
**Solution:** Analysis will proceed as gap identification (new capability to consider)
**Prevention:** Expected for truly novel competitor features

---

**Issue:** "Incomplete analysis - missing sections"
**Cause:** Competitor code is partial or malformed
**Solution:** Request complete file(s) from source
**Prevention:** Verify all sections present before pasting

---

**Issue:** "Feature status mismatch - manual review recommended"
**Cause:** Ambiguous implementations that automated analysis cannot confidently categorize
**Solution:** Review flagged features manually; report marks these with `[?]` indicator
**Prevention:** Expected for ~5-10% of features; part of normal operation

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-code-reviewer](../../agents/engineering/cs-code-reviewer.md)** - Technical quality assessment of competitor implementations
- **[cs-architect](../../agents/engineering/cs-architect.md)** - Architecture pattern comparison and evaluation
- **[cs-product-strategist](../../agents/product/cs-product-strategist.md)** - Strategic roadmap integration of findings
- **[cs-business-analyst](../../agents/product/cs-business-analyst.md)** - Market positioning analysis

### Related Skills

This command leverages:

- **[engineering-team/code-reviewer](../../skills/engineering-team/code-reviewer/)** - Code quality assessment patterns
- **[product-team/product-strategist](../../skills/product-team/product-strategist/)** - Strategic planning frameworks
- **[product-team/product-manager-toolkit](../../skills/product-team/product-manager-toolkit/)** - Prioritization tools

---

## Tips for Best Results

1. **Prepare Complete Code**
   - Include all relevant files (SKILL.md, scripts, references)
   - Ensure metadata/frontmatter is present
   - Include multiple files for comprehensive analysis

2. **Specify Scope When Known**
   - Use --scope flag for focused analysis
   - Match competitor type to our assets
   - Reduces noise in comparison

3. **Act on Findings**
   - Prioritize ADOPT recommendations immediately
   - Schedule CONSIDER items for roadmap review
   - Track MONITOR items for future reference

4. **Iterate Analysis**
   - Re-run after implementing recommendations
   - Track score improvements over time
   - Monitor competitor updates regularly

5. **Share Insights**
   - Format recommendations for different stakeholders
   - Engineering: Focus on architecture and technical gaps
   - Product: Focus on feature matrix and priorities
   - Executive: Use executive summary and strategic assessment

---

## Related Commands

- `/review.code` - Technical code quality analysis
- `/audit.dependencies` - Dependency security and currency analysis
- `/audit.security` - Security vulnerability scanning
- `/prioritize.features` - RICE-based feature prioritization

---

## References

- [Competitive Analysis Best Practices](https://www.pragmaticmarketing.com/) - Strategic frameworks
- [RICE Prioritization Framework](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) - Prioritization methodology
- Previous Analysis: `output/sessions/*/skill-builder-comparison-scorecard.md` - Reference implementation

---

**Last Updated:** November 27, 2025
**Version:** v1.0.0
**Maintained By:** Claude Skills Team
**Feedback:** Submit issues or feature requests in repository issues
