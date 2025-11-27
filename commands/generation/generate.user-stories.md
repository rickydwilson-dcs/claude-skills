---
name: generate.user-stories
title: User Story Generator with INVEST Criteria
description: Generate INVEST-compliant user stories from epic descriptions with acceptance criteria, story point estimates, and sprint planning
category: generation
subcategory: product-management
difficulty: beginner
time-saved: "2-3 hours per sprint planning session"
frequency: "Every sprint (bi-weekly)"
use-cases:
  - "Breaking down epics into deliverable user stories with acceptance criteria"
  - "Sprint planning with capacity-based story allocation"
  - "Generating INVEST-compliant stories for backlog refinement"
  - "Creating enabler stories for technical requirements"
  - "Exporting stories to CSV for Jira/Linear import"
related-agents:
  - cs-agile-product-owner
  - cs-product-manager
  - cs-scrum-master
related-skills:
  - product-team/agile-product-owner
  - product-team/product-manager-toolkit
related-commands:
  - /prioritize.features
  - /create.pr
dependencies:
  tools:
    - Read
    - Write
    - Bash
    - Glob
  scripts:
    - product-team/agile-product-owner/scripts/user_story_generator.py
  python-packages: []
compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows
examples:
  - title: "Generate from Epic Description"
    input: '/generate.user-stories "User authentication with OAuth support"'
    output: "Generated 8 user stories (42 points total). Top priority: US-001 Login with Google OAuth (5pts)"
  - title: "Sprint Planning with Capacity"
    input: "/generate.user-stories epic.json --sprint --capacity 30"
    output: "Sprint planned: 6 committed stories (28pts, 93% utilization), 2 stretch goals"
  - title: "Export to CSV for Jira"
    input: "/generate.user-stories epic.json --output csv --file backlog.csv"
    output: "Exported 12 stories to backlog.csv (ready for Jira import)"
  - title: "Verbose Epic Breakdown"
    input: "/generate.user-stories epic.json --verbose"
    output: "Full breakdown with all 15 stories, acceptance criteria, and INVEST checklist"
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0
version: v1.0.0
author: Claude Skills Team
contributors:
  - Product Team
created: 2025-11-27
updated: 2025-11-27
tags:
  - user-stories
  - agile
  - sprint-planning
  - invest
  - backlog
  - product-management
  - scrum
  - epic-breakdown
featured: false
verified: true
license: MIT
---

## Overview

User stories are the building blocks of agile development. This command generates INVEST-compliant user stories from epic descriptions, complete with acceptance criteria, story point estimates, and priority assignments.

### INVEST Criteria

Every generated story is validated against INVEST principles:

- **I**ndependent: Can be developed without dependencies on other stories
- **N**egotiable: Details can be refined through conversation
- **V**aluable: Delivers value to the user or business
- **E**stimable: Can be sized with reasonable confidence
- **S**mall: Fits within a single sprint
- **T**estable: Has clear acceptance criteria

## Usage

```bash
# Quick generation from epic description
/generate.user-stories "User dashboard with analytics and export"

# Generate from JSON epic file
/generate.user-stories epic.json

# Sprint planning with 30-point capacity
/generate.user-stories epic.json --sprint --capacity 30

# Export as CSV for Jira import
/generate.user-stories epic.json --output csv --file backlog.csv

# JSON output for API integration
/generate.user-stories epic.json --output json

# Verbose output with all story details
/generate.user-stories epic.json --verbose
```

### Epic JSON Format

```json
{
  "name": "User Dashboard",
  "description": "Create a comprehensive dashboard for users to view their data",
  "personas": ["end_user", "power_user", "admin"],
  "scope": [
    "View key metrics and KPIs",
    "Customize dashboard layout",
    "Export dashboard data",
    "Share dashboard with team members",
    "Set up automated reports"
  ],
  "technical_requirements": [
    "Implement caching for performance",
    "Set up real-time data pipeline"
  ]
}
```

### Available Personas

| Persona | Focus | Typical Needs |
|---------|-------|---------------|
| `end_user` | Daily usage | Efficiency, simplicity, reliability |
| `admin` | System management | Control, visibility, security |
| `power_user` | Expert workflows | Advanced features, automation, shortcuts |
| `new_user` | Onboarding | Guidance, learning, clarity |

## Implementation

### Phase 1: Input Processing

1. **Parse Input**
   - Accept epic description string or JSON file path
   - Validate JSON structure if file provided
   - Extract personas, scope items, and technical requirements

2. **Determine Mode**
   - Epic breakdown (default): Generate all stories from epic
   - Sprint planning (--sprint): Allocate stories to sprint capacity

### Phase 2: Story Generation

1. **Generate User Stories**
   - Create story for each scope item × persona combination
   - Apply story template: "As a {persona}, I want to {action} so that {benefit}"
   - Generate unique story IDs (e.g., USE-001, USE-002)

2. **Generate Acceptance Criteria**
   - Happy path: Given/When/Then format
   - Validation: Input validation requirements
   - Error handling: Clear error messaging
   - Performance: Response time expectations
   - Accessibility: Keyboard navigation support

3. **Estimate Complexity**
   - Simple (1pt): View, display, basic read operations
   - Medium (3pt): Create, edit, update operations
   - Complex (8pt): Integration, advanced features
   - Epic-level (13pt): Redesign, refactor, architecture changes

4. **Assign Priority**
   - Critical: Security, fixes, broken functionality
   - High: Core features for primary personas
   - Medium: Improvements and enhancements
   - Low: Nice-to-have features

5. **INVEST Validation**
   - Check each criterion
   - Flag stories that fail criteria
   - Suggest improvements for non-compliant stories

### Phase 3: Sprint Planning (if --sprint)

1. **Sort Backlog**
   - Order by priority (critical → high → medium → low)
   - Secondary sort by story points (smallest first)

2. **Allocate to Sprint**
   - Fill committed stories up to capacity
   - Add stretch goals up to 120% capacity
   - Calculate utilization percentage

3. **Generate Sprint Summary**
   - Total committed points
   - Stretch goal points
   - Utilization rate
   - Risk assessment

### Phase 4: Output Generation

1. **Format Output**
   - Text: Human-readable story cards with acceptance criteria
   - JSON: Structured data for API/tool integration
   - CSV: Jira/Linear import format

2. **Write Results**
   - Display to stdout (default)
   - Write to file if --file specified

## Output Examples

### Text Output (Default)

```
USER STORY: USE-001
========================================
Title: View Key Metrics
Type: story
Priority: HIGH
Points: 3

Story:
As a End User, I want to view key metrics and KPIs so that I can save time and work more efficiently

Acceptance Criteria:
  1. Given user has access, When they view key metrics and kpis, Then the view key metrics and kpis is successfully completed
  2. Should validate input before processing
  3. Must show clear error message when action fails
  4. Should complete within 2 seconds
  5. Must be accessible via keyboard navigation

INVEST Checklist:
  ✓ Independent
  ✓ Negotiable
  ✓ Valuable
  ✓ Estimable
  ✓ Small
  ✓ Testable

============================================================
BACKLOG SUMMARY
============================================================
Total Stories: 12
Total Points: 47
Average Size: 3.9 points

Priority Breakdown:
  High: 4 stories
  Medium: 5 stories
  Low: 3 stories
```

### Sprint Planning Output

```
============================================================
SPRINT PLANNING
============================================================
Sprint Capacity: 30 points
Committed: 28 points (93.3%)
Stories: 6 committed + 2 stretch

COMMITTED STORIES:

  [H] USE-001: View Key Metrics (3pts)
  [H] USE-002: Customize Dashboard Layout (5pts)
  [H] USE-003: Export Dashboard Data (5pts)
  [M] USE-004: Share Dashboard (5pts)
  [M] USE-005: Set Up Automated Reports (8pts)
  [L] USE-006: Dashboard Themes (2pts)

STRETCH GOALS:

  [M] USE-007: Advanced Filters (5pts)
  [L] USE-008: Dashboard Templates (3pts)
```

### JSON Output

```json
{
  "metadata": {
    "tool": "user_story_generator",
    "version": "1.0.0",
    "total_stories": 12
  },
  "stories": [
    {
      "id": "USE-001",
      "type": "story",
      "title": "View Key Metrics",
      "narrative": "As a End User, I want to view key metrics and KPIs so that I can save time and work more efficiently",
      "acceptance_criteria": [...],
      "estimation": 3,
      "priority": "high",
      "dependencies": [],
      "invest_check": {
        "independent": true,
        "negotiable": true,
        "valuable": true,
        "estimable": true,
        "small": true,
        "testable": true
      }
    }
  ],
  "sprint": {
    "capacity": 30,
    "committed": [...],
    "stretch": [...],
    "total_points": 28,
    "utilization": 93.3
  }
}
```

### CSV Output (Jira Import)

```csv
id,title,type,narrative,priority,estimation,invest_check
USE-001,View Key Metrics,story,"As a End User, I want to...",high,3,"independent:True,negotiable:True,..."
USE-002,Customize Dashboard Layout,story,"As a Power User, I want to...",high,5,"independent:True,..."
```

## Integration Patterns

### Pattern 1: Epic → Stories → Sprint

```bash
# 1. Define epic in JSON
cat > epic.json << 'EOF'
{
  "name": "User Authentication",
  "personas": ["end_user", "admin"],
  "scope": [
    "Login with email/password",
    "OAuth with Google",
    "OAuth with GitHub",
    "Password reset flow",
    "Two-factor authentication",
    "Session management"
  ],
  "technical_requirements": [
    "Implement JWT token handling",
    "Set up OAuth2 providers"
  ]
}
EOF

# 2. Generate and plan sprint
/generate.user-stories epic.json --sprint --capacity 30

# 3. Export to Jira
/generate.user-stories epic.json --output csv --file sprint-backlog.csv
```

### Pattern 2: Quick Story Generation

```bash
# Generate stories from description
/generate.user-stories "Search functionality with filters and sorting"

# Review and refine
# Then prioritize with RICE
/prioritize.features backlog.csv
```

### Pattern 3: Continuous Backlog Refinement

```bash
# Weekly refinement session
/generate.user-stories new-features.json --verbose

# Review INVEST compliance
# Adjust stories that fail criteria
# Add to product backlog
```

## Best Practices

### Writing Good Epic Descriptions

**Do:**
- Use clear, action-oriented scope items
- Include all relevant personas
- List technical requirements separately
- Keep scope items focused and atomic

**Don't:**
- Combine multiple features in one scope item
- Use vague language ("make it better")
- Skip technical enabler stories
- Forget edge cases and error scenarios

### Sprint Planning Tips

1. **Capacity Planning**
   - Account for meetings, reviews, and ceremonies (typically 20% reduction)
   - Leave buffer for unplanned work (10-15%)
   - Consider team velocity history

2. **Story Selection**
   - Balance quick wins with larger features
   - Don't overcommit on complex stories
   - Include at least one technical debt item

3. **Stretch Goals**
   - Keep stretch goals at 10-20% of capacity
   - Select independent stories for stretch
   - Don't count stretch in velocity

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "File not found" | Epic JSON path incorrect | Verify file path exists |
| "Invalid JSON" | Malformed epic definition | Validate JSON syntax |
| "No scope items" | Empty scope array | Add at least one scope item |
| "Capacity exceeded" | Sprint capacity too low | Increase capacity or reduce scope |

## Related Resources

- **Python Tool:** [user_story_generator.py](../../skills/product-team/agile-product-owner/scripts/user_story_generator.py)
- **Agent:** [cs-agile-product-owner](../../agents/product/cs-agile-product-owner.md)
- **Skill:** [agile-product-owner](../../skills/product-team/agile-product-owner/SKILL.md)
- **Related Command:** [/prioritize.features](../workflow/prioritize.features.md)

---

**Command Pattern:** Multi-Phase (Input → Generation → Planning → Output)
**Execution Time:** 5-15 seconds depending on epic size
**Last Updated:** November 27, 2025
