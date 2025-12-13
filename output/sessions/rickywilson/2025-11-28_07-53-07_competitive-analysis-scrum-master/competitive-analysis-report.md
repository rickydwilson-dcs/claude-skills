# Competitive Analysis Report: Scrum Master Skills

**Analysis Date:** 2025-11-28
**Competitor:** claude-code-skill-factory (alirezarezvani)
**Our Asset:** claude-skills/skills/delivery-team/scrum-master

---

## Executive Summary

This analysis compares our `scrum-master` skill against the competitor's `scrum-master-agent` from the claude-code-skill-factory repository. **The competitor has a significant advantage in Python tooling depth**, featuring 7 specialized scripts compared to our 1 script. However, **we maintain advantages in documentation quality, knowledge base depth, and Atlassian MCP integration**.

**Overall Position:** Behind on tooling, ahead on knowledge frameworks. **Recommended Action:** Close the tooling gap while maintaining our documentation and integration strengths.

---

## Quick Scorecard

```
+-------------------------------------------------------------+
|                    COMPETITIVE ANALYSIS                      |
|           US (claude-skills) vs THEM (skill-factory)         |
+-------------------------------------------------------------+
|                                                              |
|  WE WIN:     4 areas (33%)  ========                         |
|  TIE:        3 areas (25%)  ======                           |
|  DIFFERENT:  2 areas (17%)  ====                             |
|  THEY WIN:   3 areas (25%)  ======                           |
|                                                              |
|  Overall Position: COMPETITIVE - GAPS TO CLOSE               |
|                                                              |
+-------------------------------------------------------------+
```

---

## Feature Comparison Matrix

| Category | Feature | US | THEM | Winner | Recommendation |
|----------|---------|:--:|:----:|:------:|----------------|
| **Python Tools** | Metrics Calculator | 1 script | 1 class | TIE | Maintain |
| | Backlog Prioritizer | None | Full module | THEM | **ADD** |
| | Tool Adapters (Jira/Linear/etc) | None | 4 adapters | THEM | **ADD** |
| | Input Parser | None | Multi-format | THEM | **ADD** |
| | Output Formatter | None | Context-aware | DIFF | Consider |
| | Notification System | None | Slack/Teams | DIFF | Consider |
| **Documentation** | SKILL.md Completeness | 460 lines | ~200 lines | US | Maintain |
| | YAML Metadata | 62 lines | Basic | US | Maintain |
| | Workflow Documentation | 6 workflows | 10 use cases | TIE | Expand |
| **Knowledge Base** | Ceremony Frameworks | 5 ceremonies | Basic | US | Maintain |
| | Retrospective Formats | 8 formats | None | US | Maintain |
| | Best Practices | DoD/DoR | Basic | US | Maintain |
| **Architecture** | Dependencies | stdlib only | stdlib only | TIE | Maintain |
| | Multi-Tool Support | MCP Integration | API Adapters | DIFF | Evaluate |

---

## Detailed Dimension Scores

```
Dimension              US          THEM        Winner
--------------------------------------------------------------
Documentation          *****       ***         US (+2)
Tool/Script Quality    **          *****       THEM (-3) <- Critical Gap
Workflow Coverage      ****        ****        TIE (0)
Architecture           *****       *****       TIE (0)
Automation Depth       **          ****        THEM (-2) <- Gap
Reference Depth        *****       **          US (+3)

OVERALL:               ***         ****        BEHIND ON TOOLING
```

---

## Critical Differentiators

### Where We Win (Maintain These Advantages)

| Advantage | Our Implementation | Their Gap |
|-----------|-------------------|-----------|
| **Retrospective Formats** | 8 detailed formats (Start/Stop/Continue, Glad/Sad/Mad, 4Ls, Sailboat, Timeline, Starfish, Speed Dating, Three Little Pigs) with facilitation tips | No retrospective frameworks |
| **Ceremony Documentation** | Detailed step-by-step workflows for all 5 Scrum ceremonies with timeboxes | Basic use case descriptions |
| **Atlassian MCP Integration** | Native Jira/Confluence through MCP server | Adapter-based approach requiring API setup |
| **Decision Frameworks** | Clear escalation paths, when to involve PM/Jira Expert/Confluence Expert | Generic recommendations |

### Where They Win (Gaps to Close)

| Gap | Their Implementation | Our Deficit |
|-----|---------------------|-------------|
| **Backlog Prioritization** | Full `prioritize_backlog.py` with value/effort/risk scoring, capacity-based allocation, quick wins identification | **No equivalent script** |
| **Tool Adapters** | 4 adapters (Linear, Jira, GitHub Projects, Azure DevOps) normalizing data formats | **MCP only - no direct adapters** |
| **Multi-Format Input** | JSON, CSV, YAML parser with auto-detection | **CLI args only** |
| **Sprint Health Formula** | 6-metric health calculation (40% velocity, 30% burndown, 20% blockers, 10% morale) | **Basic health score** |
| **Output Formatting** | Context-aware (CLI vs Desktop), ASCII charts, ANSI colors | **Human-readable text only** |

---

## Gap Analysis Summary

### Priority 1: Critical Gaps (Immediate Action)

| Gap | Impact | Effort | Priority Score |
|-----|--------|--------|----------------|
| Add `prioritize_backlog.py` | High - missing core PM function | Medium (2-3 days) | **P0** |
| Add tool adapters (Jira/Linear) | High - data import capability | Medium (3-4 days) | **P0** |
| Enhance metrics calculator | Medium - missing 3 metric types | Low (1-2 days) | **P1** |

### Priority 2: Enhancement Gaps (Short-term)

| Gap | Impact | Effort | Priority Score |
|-----|--------|--------|----------------|
| Multi-format input parser | Medium - UX improvement | Low (1 day) | **P2** |
| JSON output mode | Medium - integration capability | Low (1 day) | **P2** |
| Sprint health formula expansion | Low - marginal improvement | Low (1 day) | **P3** |

### Priority 3: Consider (Long-term)

| Gap | Impact | Effort | Priority Score |
|-----|--------|--------|----------------|
| Slack/Teams notifications | Low - optional feature | Medium (2 days) | **P3** |
| Context-aware output formatting | Low - nice-to-have | Medium (2 days) | **P3** |

---

## Adoption Recommendations

### Immediate Actions (This Sprint)

1. **ADOPT: Backlog Prioritization Script**
   - Create `prioritize_backlog.py` with value/effort/risk scoring
   - Include capacity-based sprint allocation
   - Add quick wins identification feature
   - **Estimated effort:** 2-3 days

2. **ADOPT: Enhanced Sprint Health Calculation**
   - Update `sprint_metrics_calculator.py` with 6-metric formula
   - Add weighted scoring (velocity 40%, burndown 30%, blockers 20%, morale 10%)
   - **Estimated effort:** 1 day

### Short-term Actions (This Quarter)

3. **CONSIDER: Tool Adapters**
   - Create `tool_adapters.py` for Jira/Linear/GitHub Projects
   - Normalize sprint data from different sources
   - **Estimated effort:** 3-4 days
   - **Decision factor:** Evaluate if MCP integration already covers this need

4. **CONSIDER: Multi-Format Input Parser**
   - Add JSON/CSV/YAML input support to metrics calculator
   - **Estimated effort:** 1-2 days

### Long-term Actions (Roadmap)

5. **MONITOR: Notification Integration**
   - Slack/Teams webhooks for alerts
   - **Decision:** Wait for user demand signals

6. **MONITOR: Context-Aware Output**
   - ASCII charts vs rich markdown based on environment
   - **Decision:** Low priority unless requested

---

## Strategic Assessment

```
+-----------------------------------------------------------------------------+
|                STRATEGIC RECOMMENDATIONS FOR US                              |
|                     (Based on competitive analysis)                          |
+-----------------------------------------------------------------------------+
|                                                                              |
|  DOUBLE DOWN (Extend Our Advantages)                                         |
|  ----------------------------------                                          |
|  - Retrospective formats library - expand to 10+ formats                     |
|  - Atlassian MCP integration - this is our differentiation                   |
|  - Ceremony frameworks - add facilitation scripts                            |
|                                                                              |
|  CLOSE GAPS (What We Need to Improve)                                        |
|  ------------------------------------                                        |
|  - Python tooling count (1 -> 4+ scripts)                                    |
|  - Backlog prioritization capabilities                                       |
|  - Multi-tool data import adapters                                           |
|                                                                              |
|  DIFFERENTIATE (Create New Advantages)                                       |
|  -------------------------------------                                       |
|  - Sprint planning AI assistant (using MCP)                                  |
|  - Retrospective facilitation automation                                     |
|  - Team health trend analysis over time                                      |
|                                                                              |
|  MONITOR (Watch What They Do)                                                |
|  ----------------------------                                                |
|  - Their notification integration adoption                                   |
|  - New tool adapters they add                                                |
|  - User feedback on their skill                                              |
|                                                                              |
+-----------------------------------------------------------------------------+
```

---

## Competitive Position Map

```
                    TOOLING DEPTH
                         |
           High          |          High
        Tooling +        |       Tooling +
      Weak Knowledge     |    Strong Knowledge
                         |
    +--------------------+--------------------+
    |                    |                    |
    |   skill-factory    |     IDEAL STATE    |
    |   scrum-master     |    (Our Target)    |
    |        *           |         X          |
    |                    |                    |
----+--------------------+--------------------+---- KNOWLEDGE DEPTH
    |                    |                    |
    |                    |   claude-skills    |
    |    Incomplete      |   scrum-master     |
    |      Skills        |        *           |
    |                    |                    |
    +--------------------+--------------------+
                         |
           Low           |          Low
        Tooling +        |       Tooling +
      Weak Knowledge     |    Strong Knowledge
                         |

Strategy: Move UP (add tools) while maintaining RIGHT position (knowledge)
```

---

## Implementation Roadmap

### Week 1-2: Close Critical Tooling Gaps

```
[ ] Create prioritize_backlog.py
    - Value/effort/risk scoring algorithm
    - Capacity-based sprint allocation
    - Quick wins identification
    - CLI interface with --help support

[ ] Enhance sprint_metrics_calculator.py
    - Add 6-metric health formula
    - Add weighted scoring system
    - Add JSON output mode
```

### Week 3-4: Add Data Import Capabilities

```
[ ] Create input_parser.py
    - JSON/CSV/YAML format detection
    - Sprint data normalization
    - Validation and error handling

[ ] Create tool_adapters.py (if MCP gap confirmed)
    - Jira adapter
    - Linear adapter
    - Common interface pattern
```

### Month 2: Differentiation Features

```
[ ] Retrospective automation scripts
[ ] Sprint planning assistant
[ ] Historical trend analysis
```

---

## Files to Create/Modify

### New Files Needed

| File | Purpose | Priority |
|------|---------|----------|
| `scripts/prioritize_backlog.py` | Backlog prioritization with scoring | P0 |
| `scripts/input_parser.py` | Multi-format input handling | P2 |
| `scripts/tool_adapters.py` | Data normalization from PM tools | P1 |

### Files to Enhance

| File | Enhancement | Priority |
|------|-------------|----------|
| `scripts/sprint_metrics_calculator.py` | Add 6-metric health, JSON output | P1 |
| `SKILL.md` | Document new tools | P2 |
| `HOW_TO_USE.md` | Add usage examples for new tools | P2 |

---

## Conclusion

**Our scrum-master skill has strong foundations in knowledge and documentation but is behind on automation tooling.** The competitor offers 7 Python modules vs our 1, giving them a significant advantage for teams wanting data-driven sprint management.

**Recommended Strategy:**
1. **Immediate:** Add backlog prioritization script (highest impact gap)
2. **Short-term:** Enhance metrics calculator with full health scoring
3. **Maintain:** Our documentation and retrospective format advantages
4. **Leverage:** Our Atlassian MCP integration as differentiation

**Success Metrics:**
- Python tool count: 1 -> 4+ (match competitor)
- Feature parity on core calculations
- Maintain documentation leadership

---

**Report Generated:** 2025-11-28T07:53:07
**Session:** 2025-11-28_07-53-07_competitive-analysis-scrum-master
**Analyst:** Claude Code
