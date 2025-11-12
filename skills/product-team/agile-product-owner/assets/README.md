# Agile Product Owner - Sample Assets

This directory contains sample input files for the User Story Generator and sprint planning tools.

## Sample Files

### 1. sample-epic.json
**Purpose:** Epic definition for user story generation and sprint planning

**Description:** Realistic product epic "Advanced Reporting Dashboard" with:
- Epic metadata (ID, dates, priorities)
- Scope items broken down into user story candidates
- Technical requirements for enabler stories
- Success criteria and business impact
- Dependencies and related initiatives

**Key Fields:**
- `name`: Epic title
- `scope`: List of features/capabilities to build
- `personas`: Who benefits from this epic
- `technical_requirements`: Backend/infrastructure work needed
- `success_criteria`: How to measure success

**How to Use:**
```bash
# Generate user stories from epic
python ../scripts/user_story_generator.py sample-epic.json

# With sprint planning (30 story point capacity)
python ../scripts/user_story_generator.py sample-epic.json --sprint --capacity 30

# Export as JSON for Jira integration
python ../scripts/user_story_generator.py sample-epic.json --output json

# Export as CSV
python ../scripts/user_story_generator.py sample-epic.json --output csv --file backlog.csv
```

**What to Expect:**
- Generated user stories with INVEST criteria checks
- Acceptance criteria for each story
- Story point estimates
- Priority levels
- Enabler stories for technical work

---

## Using This Sample

### Quick Start

```bash
cd /Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My\ Drive/Websites/GitHub/claude-skills/product-team/agile-product-owner/

# Generate stories from epic
python scripts/user_story_generator.py assets/sample-epic.json

# Sprint planning with 30 point capacity
python scripts/user_story_generator.py assets/sample-epic.json --sprint --capacity 30

# Full JSON export for tool integration
python scripts/user_story_generator.py assets/sample-epic.json --output json -f stories.json
```

### Understanding Generated Stories

Each story includes:

1. **Story ID**: Unique identifier (e.g., RPT-001)
2. **Title**: Concise description of the feature
3. **Narrative**: "As a [persona], I want to [action] so that [benefit]"
4. **Acceptance Criteria**: 5-7 specific testable conditions
5. **Story Points**: Complexity estimate (1, 3, 5, 8, 13 Fibonacci)
6. **Priority**: Critical, High, Medium, or Low
7. **INVEST Check**: Completeness metrics

---

## Creating Your Own Epic

### Epic Structure

```json
{
  "name": "Your Epic Title",
  "description": "2-3 sentence description of the epic's purpose",
  "personas": ["end_user", "power_user"],
  "scope": [
    "Specific feature or capability 1",
    "Specific feature or capability 2"
  ],
  "technical_requirements": [
    "Infrastructure work needed",
    "Integration work needed"
  ]
}
```

### Epic Definition Tips

1. **Name**: Clear, outcome-focused (Dashboard, Integration, Mobile App)
2. **Description**: Why we're building it, business value
3. **Personas**: Who benefits (end_user, admin, power_user, new_user)
4. **Scope**: 4-8 specific features, not vague
5. **Technical Requirements**: Backend work, integrations, platform changes
6. **Success Criteria**: Measurable outcomes
7. **Priority**: Usually "high" for approved epics
8. **Estimated Effort**: Total story points for planning

### Good Scope Item Examples
- "Create customizable dashboard with drag-and-drop widgets"
- "Build real-time data refresh capability"
- "Implement role-based access control"
- "Export reports to PDF and Excel formats"

### Avoid These
- "Improve dashboard" (too vague)
- "Make it better" (unmeasurable)
- "User experience enhancements" (no acceptance criteria possible)

---

## Story Point Guidelines

| Points | Complexity | Examples |
|--------|-----------|----------|
| 1 | Trivial | UI text change, button rename |
| 3 | Small | Simple form, basic validation |
| 5 | Medium | Dashboard widget, basic feature |
| 8 | Large | Complex feature, multiple components |
| 13 | Extra Large | Major feature, significant integration |

---

## Sprint Planning

### Capacity Planning Formula

```
Sprint Capacity = Team Size × Velocity × Duration

Example:
5 engineers × 10 pts/engineer × 2 weeks = 100 point capacity
```

### Allocating Stories

The script generates:
1. **Committed**: Stories fitting within capacity
2. **Stretch**: Stories reaching to 120% of capacity
3. **Backlog**: Remaining stories for future sprints

### Sprint Utilization
- 80-100%: Healthy commitment
- <80%: Under-committed (risks)
- >120%: Over-committed (burndown issues)

---

## INVEST Criteria Explained

Each story should be:

| Criterion | What It Means | How to Check |
|-----------|--------------|-------------|
| Independent | Can be developed without others | No "depends on STORY-X" |
| Negotiable | Details can change, outcome is fixed | Some flexibility on implementation |
| Valuable | Delivers business value | Clear ROI or user benefit |
| Estimable | Team can estimate effort | Not too vague or complex |
| Small | Completable in one sprint | 8 points or less ideally |
| Testable | Acceptance criteria are verifiable | Can automated/manual test it |

---

## Output Formats

### Text Format (Default)
Human-readable story details, good for discussion

### JSON Format
Machine-readable, integrates with:
- Jira (via custom importers)
- Azure DevOps
- Linear
- Notion
- Spreadsheets

### CSV Format
Importable to Excel/Sheets, useful for:
- Quick browsing in spreadsheet
- Jira bulk import
- Pivot table analysis
- Stakeholder sharing

---

## Integration with Other Tools

### Jira Integration
```bash
# Export stories as JSON
python scripts/user_story_generator.py epic.json --output json > stories.json

# Import via Jira API or bulk import tool
```

### Confluence Documentation
```bash
# Generate detailed stories for wiki
python scripts/user_story_generator.py epic.json --verbose > epic-stories.md
```

### Spreadsheet Collaboration
```bash
# Export to CSV for team discussion
python scripts/user_story_generator.py epic.json --output csv --file backlog.csv
```

---

## Troubleshooting

**Issue:** "PersonaError: Unknown persona"
- Use valid personas: end_user, admin, power_user, new_user
- Or add custom personas in the script

**Issue:** "Stories seem too vague"
- Scope items need to be specific
- Use action verbs: "Create", "Build", "Implement", "Add"
- Include the "what" and "why"

**Issue:** "Story points seem high/low"
- Complexity estimation depends on team experience
- Adjust if consistently different from actual velocity
- Compare to similar past stories

**Issue:** "CSV export looks odd"
- Use a proper CSV parser
- Some fields may contain commas (quoted properly)
- Ensure UTF-8 encoding in spreadsheet

---

## Best Practices

1. **Validate with Team**: Have engineers estimate before committing
2. **Keep Stories Small**: Easier to complete, easier to test
3. **Clear Acceptance Criteria**: Remove ambiguity
4. **Break Down Epics**: Aim for 8-15 stories per epic
5. **Technical Stories**: Include equal priority to user-facing stories
6. **Regular Refinement**: Review before sprint planning

---

## File Specifications

- **File Format:** JSON
- **Encoding:** UTF-8
- **Required Fields:** name, personas, scope, technical_requirements
- **Optional Fields:** epic_id, dates, dependencies, business_impact
- **Max Size:** 10MB (easily handles 100+ epics)

---

## Related Documentation

- **User Story Generator:** [../scripts/user_story_generator.py](../scripts/user_story_generator.py)
- **RICE Prioritizer:** [../product-manager-toolkit/scripts/rice_prioritizer.py](../product-manager-toolkit/scripts/rice_prioritizer.py)
- **Agile Best Practices:** [../SKILL.md](../SKILL.md)

---

**Last Updated:** November 5, 2025
**Format:** Sample Assets README
**Included Files:** 1 (sample-epic.json)
**Script Version:** user_story_generator.py 1.0.0
