# Competitive Scoring Framework

## Overview

This framework defines the scoring criteria, rubrics, and methodology for evaluating competitive products against the claude-skills library. Use this reference when conducting competitive analysis to ensure consistent, objective scoring.

---

## Scoring Dimensions

### Dimension 1: Documentation Completeness (20%)

**What to Evaluate**: Quality, depth, and usability of documentation

| Score | Criteria |
|-------|----------|
| ⭐⭐⭐⭐⭐ (5) | Complete YAML metadata, all sections present, 3+ examples, clear navigation, comprehensive API docs |
| ⭐⭐⭐⭐ (4) | Most metadata present, key sections covered, 2+ examples, good structure |
| ⭐⭐⭐ (3) | Basic metadata, main sections present, at least 1 example, readable |
| ⭐⭐ (2) | Incomplete metadata, missing sections, no examples, basic structure |
| ⭐ (1) | Minimal or no documentation, unclear structure, unusable |

**Checklist**:
- [ ] YAML frontmatter with required fields
- [ ] Overview/description section
- [ ] Usage examples (3+ for full score)
- [ ] API/CLI documentation
- [ ] Error handling documented
- [ ] Integration guides
- [ ] Version history

---

### Dimension 2: Tool/Script Quality (20%)

**What to Evaluate**: Quality of Python tools, CLI support, and automation

| Score | Criteria |
|-------|----------|
| ⭐⭐⭐⭐⭐ (5) | Multiple tools, full CLI with --help, error handling, JSON output, tests, zero dependencies |
| ⭐⭐⭐⭐ (4) | 2+ tools, CLI support, good error handling, multiple output formats |
| ⭐⭐⭐ (3) | 1-2 tools, basic CLI, some error handling, single output format |
| ⭐⭐ (2) | Tools present but limited, minimal CLI, poor error handling |
| ⭐ (1) | No tools or broken/unusable scripts |

**Checklist**:
- [ ] CLI interface with argparse
- [ ] --help flag support
- [ ] Error handling with useful messages
- [ ] Multiple output formats (json, markdown, console)
- [ ] Zero external dependencies
- [ ] Input validation
- [ ] Tests or validation scripts

---

### Dimension 3: Workflow Coverage (15%)

**What to Evaluate**: Number and depth of documented workflows

| Score | Criteria |
|-------|----------|
| ⭐⭐⭐⭐⭐ (5) | 4+ complete workflows, clear triggers, detailed steps, deliverables defined |
| ⭐⭐⭐⭐ (4) | 3-4 workflows, good detail, most steps documented |
| ⭐⭐⭐ (3) | 2-3 workflows, moderate detail, basic steps |
| ⭐⭐ (2) | 1-2 workflows, limited detail |
| ⭐ (1) | No documented workflows or unclear processes |

**Workflow Quality Criteria**:
- Purpose clearly stated
- Trigger conditions defined
- Step-by-step process
- Tools/resources referenced
- Expected deliverables
- Example outputs

---

### Dimension 4: Architecture (15%)

**What to Evaluate**: Modularity, portability, dependency management

| Score | Criteria |
|-------|----------|
| ⭐⭐⭐⭐⭐ (5) | Zero dependencies, fully modular, works standalone, clean separation of concerns |
| ⭐⭐⭐⭐ (4) | Minimal dependencies, modular design, portable |
| ⭐⭐⭐ (3) | Some dependencies, mostly modular, some portability issues |
| ⭐⭐ (2) | Heavy dependencies, tightly coupled, difficult to extract |
| ⭐ (1) | Monolithic, many dependencies, not portable |

**Checklist**:
- [ ] Zero external pip dependencies
- [ ] Self-contained skill packages
- [ ] Clean folder structure
- [ ] Relative path usage
- [ ] No hardcoded values
- [ ] Platform-agnostic code

---

### Dimension 5: Automation (15%)

**What to Evaluate**: Auto-generation, validation, CI/CD integration

| Score | Criteria |
|-------|----------|
| ⭐⭐⭐⭐⭐ (5) | Builder tools, full validation, 100% pass rate, automated updates |
| ⭐⭐⭐⭐ (4) | Builder tools, validation checks, high pass rate |
| ⭐⭐⭐ (3) | Some automation, basic validation |
| ⭐⭐ (2) | Limited automation, manual processes |
| ⭐ (1) | No automation, all manual |

**Checklist**:
- [ ] Builder/scaffolding tools
- [ ] Validation scripts
- [ ] Documented validation criteria
- [ ] Pass/fail reporting
- [ ] Automated catalog updates
- [ ] CI/CD integration

---

### Dimension 6: Reference Depth (15%)

**What to Evaluate**: Knowledge bases, templates, supporting materials

| Score | Criteria |
|-------|----------|
| ⭐⭐⭐⭐⭐ (5) | Comprehensive references, multiple templates, expert knowledge bases, examples for all use cases |
| ⭐⭐⭐⭐ (4) | Good references, useful templates, solid knowledge base |
| ⭐⭐⭐ (3) | Some references, basic templates |
| ⭐⭐ (2) | Limited references, few templates |
| ⭐ (1) | No references or templates |

**Checklist**:
- [ ] Reference markdown files
- [ ] User-facing templates
- [ ] Best practices documentation
- [ ] Example outputs
- [ ] Integration guides
- [ ] FAQ or troubleshooting

---

## Scoring Calculation

### Per-Item Score

```
Item Score = Σ (Dimension Score × Weight)

Where:
- Documentation: Score × 0.20
- Tool Quality:  Score × 0.20
- Workflows:     Score × 0.15
- Architecture:  Score × 0.15
- Automation:    Score × 0.15
- References:    Score × 0.15
```

**Example**:
```
Skill: competitor-skill-a
- Documentation: 4 × 0.20 = 0.80
- Tool Quality:  3 × 0.20 = 0.60
- Workflows:     5 × 0.15 = 0.75
- Architecture:  4 × 0.15 = 0.60
- Automation:    2 × 0.15 = 0.30
- References:    3 × 0.15 = 0.45
-----------------------------
Total: 3.50 / 5.00 (70%)
```

### Aggregate Score

```
Overall Score = Σ (All Item Scores) / Number of Items
```

---

## Comparison Outcomes

### Winner Determination

| Symbol | Outcome | Criteria |
|--------|---------|----------|
| 🟢 | Better | Our score > Competitor score by ≥0.5 |
| ✅ | Same | Scores within 0.5 of each other |
| 🟡 | Different | Different approaches, neither objectively better |
| ❌ | Behind | Competitor score > Our score by ≥0.5 |

### Overall Assessment

| Assessment | Criteria |
|------------|----------|
| **SIGNIFICANTLY AHEAD** | 70%+ features 🟢 Better |
| **AHEAD** | 50-69% features 🟢 Better, <20% ❌ Behind |
| **COMPETITIVE** | 40-60% features ✅ Same |
| **BEHIND** | 30%+ features ❌ Behind |
| **SIGNIFICANTLY BEHIND** | 50%+ features ❌ Behind |

---

## Confidence Levels

| Level | Criteria |
|-------|----------|
| **HIGH** | Full access to competitor code, all dimensions evaluated |
| **MEDIUM** | Partial access, most dimensions evaluated |
| **LOW** | Limited access, some dimensions estimated |

---

## Scoring Tips

### Do's

1. **Be Objective**: Apply same criteria to both sides
2. **Document Evidence**: Note specific examples for each score
3. **Use Checklists**: Ensure comprehensive evaluation
4. **Compare Apples to Apples**: Match similar items

### Don'ts

1. **Don't Assume**: Score based on evidence, not assumptions
2. **Don't Over-Weight**: Stick to defined percentages
3. **Don't Rush**: Take time for thorough analysis
4. **Don't Bias**: Acknowledge competitor strengths honestly

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│           SCORING QUICK REFERENCE               │
├─────────────────────────────────────────────────┤
│  Dimension          │ Weight │ Max Score        │
├─────────────────────┼────────┼──────────────────┤
│  Documentation      │  20%   │  5 (1.00 pts)   │
│  Tool Quality       │  20%   │  5 (1.00 pts)   │
│  Workflows          │  15%   │  5 (0.75 pts)   │
│  Architecture       │  15%   │  5 (0.75 pts)   │
│  Automation         │  15%   │  5 (0.75 pts)   │
│  References         │  15%   │  5 (0.75 pts)   │
├─────────────────────┴────────┴──────────────────┤
│  Maximum Total Score: 5.00 (100%)               │
├─────────────────────────────────────────────────┤
│  🟢 Better: >0.5 ahead  │  ✅ Same: ±0.5       │
│  🟡 Different approach  │  ❌ Behind: >0.5     │
└─────────────────────────────────────────────────┘
```

---

**Last Updated**: November 27, 2025
