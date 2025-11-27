# Gap Analysis Methodology

## Overview

This methodology defines how to identify, categorize, and prioritize gaps discovered during competitive analysis. Use this reference when conducting gap analysis workflows.

---

## Gap Categories

### Category 1: Gaps to Fill 🔴

**Definition**: Features or capabilities competitors have that we don't

**Identification Criteria**:
- Competitor has feature, we don't
- Feature provides clear user value
- Absence creates competitive disadvantage

**Example**:
```
Gap: Competitor has automated test generation
Impact: Users must write tests manually
Action: Prioritize for implementation
```

---

### Category 2: Competitive Advantages 🟢

**Definition**: Features or capabilities we have that competitors don't

**Identification Criteria**:
- We have feature, competitor doesn't
- Feature provides differentiation
- Worth maintaining and promoting

**Example**:
```
Advantage: Zero-dependency Python tools
Impact: Easier adoption, no pip install required
Action: Maintain and highlight in marketing
```

---

### Category 3: Different Approaches 🟡

**Definition**: Same problem solved differently, neither objectively better

**Identification Criteria**:
- Both have the capability
- Implementation approaches differ
- Trade-offs exist on both sides

**Example**:
```
Approach: We use markdown, they use YAML for configs
Trade-off: Markdown more readable, YAML more structured
Action: Document as design choice, not gap
```

---

### Category 4: Areas Behind ❌

**Definition**: Features where competitor implementation is superior

**Identification Criteria**:
- Both have the capability
- Competitor execution is better
- Improvement would benefit users

**Example**:
```
Behind: Competitor's CLI has better error messages
Impact: Our users get confused by cryptic errors
Action: Improve error handling in next sprint
```

---

## Severity Classification

| Severity | Symbol | Criteria | Action Timeframe |
|----------|--------|----------|------------------|
| **Critical** | 🔴 | Major competitive disadvantage, user churn risk | This sprint |
| **Important** | 🟠 | Notable gap, affects user satisfaction | This quarter |
| **Nice-to-Have** | 🟡 | Minor gap, quality of life improvement | Next quarter |
| **Strategic Choice** | ⚪ | Intentional difference, not a gap | No action needed |

---

## Impact Assessment

### Scoring Criteria

| Factor | Weight | Description |
|--------|--------|-------------|
| **User Impact** | 40% | How much does this affect user experience? |
| **Competitive Urgency** | 30% | How urgent is closing this gap? |
| **Strategic Alignment** | 20% | Does it fit our product direction? |
| **Effort Inverse** | 10% | Lower effort = higher priority |

### Scoring Scale (1-5)

**User Impact**:
- 5: Affects all users significantly
- 4: Affects most users moderately
- 3: Affects some users
- 2: Affects few users
- 1: Minimal user impact

**Competitive Urgency**:
- 5: Competitor actively winning deals on this
- 4: Frequently mentioned in competitive losses
- 3: Occasionally mentioned
- 2: Rarely mentioned
- 1: Not a competitive factor

**Strategic Alignment**:
- 5: Core to our product vision
- 4: Supports key initiatives
- 3: Aligns with direction
- 2: Tangential to strategy
- 1: Outside our focus

**Effort (Inverse)**:
- 5: < 1 day effort
- 4: 1-3 days effort
- 3: 1-2 weeks effort
- 2: 1 month effort
- 1: > 1 month effort

---

## Priority Calculation

### Formula

```
Priority Score = (Impact × 0.4) + (Urgency × 0.3) + (Strategic × 0.2) + (1/Effort × 0.1)
```

### Example Calculation

```
Gap: Add automated test generation

Scores:
- User Impact: 4 (affects most users)
- Urgency: 3 (occasionally mentioned)
- Strategic: 5 (core capability)
- Effort: 2 (1 month)

Calculation:
(4 × 0.4) + (3 × 0.3) + (5 × 0.2) + (5/2 × 0.1)
= 1.6 + 0.9 + 1.0 + 0.25
= 3.75 / 5.0

Priority: HIGH
```

### Priority Thresholds

| Score Range | Priority | Action |
|-------------|----------|--------|
| 4.0 - 5.0 | **CRITICAL** | Immediate action required |
| 3.0 - 3.9 | **HIGH** | This quarter |
| 2.0 - 2.9 | **MEDIUM** | Next quarter |
| 1.0 - 1.9 | **LOW** | Future consideration |

---

## Gap Analysis Process

### Step 1: Inventory

```
┌─────────────────────────────────────────┐
│           INVENTORY PHASE               │
├─────────────────────────────────────────┤
│                                         │
│  1. List all competitor capabilities    │
│  2. List all our capabilities           │
│  3. Match items by:                     │
│     - Name (exact match)               │
│     - Domain (functional area)         │
│     - Semantic (similar purpose)       │
│                                         │
└─────────────────────────────────────────┘
```

### Step 2: Categorize

For each unmatched or partially matched item:

```
┌─────────────────────────────────────────┐
│         CATEGORIZATION MATRIX           │
├─────────────────────────────────────────┤
│                                         │
│  They Have │ We Have │ Category         │
│  ──────────┼─────────┼─────────────     │
│     Yes    │   No    │ Gap to Fill 🔴   │
│     No     │   Yes   │ Advantage 🟢     │
│     Yes    │   Yes   │ Compare...       │
│            │         │  ├─ Better: ✅   │
│            │         │  ├─ Same: ✅     │
│            │         │  ├─ Behind: ❌   │
│            │         │  └─ Different:🟡 │
│                                         │
└─────────────────────────────────────────┘
```

### Step 3: Score

Apply impact assessment to all gaps and areas behind:

```
┌─────────────────────────────────────────────────────────────┐
│                    SCORING WORKSHEET                         │
├───────────────────┬────────┬────────┬──────────┬───────────┤
│ Gap               │ Impact │ Urgent │ Strategy │ Effort    │
├───────────────────┼────────┼────────┼──────────┼───────────┤
│ Test generation   │   4    │   3    │    5     │   2       │
│ CLI error msgs    │   3    │   2    │    3     │   4       │
│ Visual dashboards │   2    │   1    │    2     │   1       │
└───────────────────┴────────┴────────┴──────────┴───────────┘
```

### Step 4: Prioritize

Sort by calculated priority score:

```
┌─────────────────────────────────────────────────────────────┐
│                  PRIORITIZED GAP LIST                        │
├─────────────────────────────────────────────────────────────┤
│  Rank │ Gap                  │ Score │ Priority │ Action    │
│  ─────┼──────────────────────┼───────┼──────────┼─────────  │
│   1   │ Test generation      │ 3.75  │ HIGH     │ Q1 2026   │
│   2   │ CLI error messages   │ 2.95  │ MEDIUM   │ Q1 2026   │
│   3   │ Visual dashboards    │ 1.60  │ LOW      │ Future    │
└─────────────────────────────────────────────────────────────┘
```

---

## Gap Analysis Report Template

```markdown
# Gap Analysis Report

## Executive Summary
- Total Gaps Identified: X
- Critical Gaps: X
- Advantages Maintained: X
- Overall Position: [AHEAD/EVEN/BEHIND]

## Gap Inventory

### 🔴 Gaps to Fill (X items)
| Gap | Impact | Urgency | Priority | Recommendation |
|-----|--------|---------|----------|----------------|
| ... | ... | ... | ... | ... |

### 🟢 Competitive Advantages (X items)
| Advantage | Strength | Sustainability | Action |
|-----------|----------|----------------|--------|
| ... | ... | ... | ... |

### ❌ Areas Behind (X items)
| Area | Delta | Priority | Improvement Plan |
|------|-------|----------|------------------|
| ... | ... | ... | ... |

### 🟡 Different Approaches (X items)
| Approach | Our Way | Their Way | Trade-offs |
|----------|---------|-----------|------------|
| ... | ... | ... | ... |

## Recommended Actions

### Immediate (This Sprint)
1. ...

### Short-term (This Quarter)
1. ...

### Medium-term (Next Quarter)
1. ...

## Appendix
- Full scoring data
- Methodology notes
- Data sources
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────┐
│        GAP ANALYSIS QUICK REFERENCE             │
├─────────────────────────────────────────────────┤
│                                                 │
│  CATEGORIES                                     │
│  🔴 Gap to Fill    - They have, we don't       │
│  🟢 Advantage      - We have, they don't       │
│  🟡 Different      - Both have, different way  │
│  ❌ Behind         - Both have, they're better │
│                                                 │
│  PRIORITY FORMULA                               │
│  (Impact×0.4)+(Urgency×0.3)+(Strategy×0.2)+   │
│  (1/Effort×0.1)                                │
│                                                 │
│  PRIORITY THRESHOLDS                            │
│  4.0-5.0 = CRITICAL  │  2.0-2.9 = MEDIUM      │
│  3.0-3.9 = HIGH      │  1.0-1.9 = LOW         │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

**Last Updated**: November 27, 2025
