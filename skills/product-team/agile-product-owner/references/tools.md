# Agile Product Owner Tools Documentation

Complete documentation for Python automation tools.

## user_story_generator.py

INVEST-compliant user story generator with sprint planning capabilities.

### Overview

**Purpose:** Automatically generate well-formed user stories from epic descriptions, complete with acceptance criteria, story point estimates, and INVEST criteria validation.

**Key Capabilities:**
- Break down epics into deliverable user stories
- Generate acceptance criteria automatically
- Estimate story points based on complexity
- Validate INVEST criteria compliance
- Sprint planning with capacity allocation
- Multiple output formats (text, JSON, CSV)

### Installation

**Requirements:**
- Python 3.8+
- No external dependencies (uses standard library only)

**Setup:**
```bash
# No installation needed - uses Python standard library
python3 scripts/user_story_generator.py --help
```

### Usage

#### Basic Usage

**Generate stories from sample epic:**
```bash
python3 scripts/user_story_generator.py
```

**Generate stories from custom epic file:**
```bash
python3 scripts/user_story_generator.py epic.json
```

#### Sprint Planning Mode

**Plan sprint with default capacity (30 points):**
```bash
python3 scripts/user_story_generator.py --sprint
```

**Plan sprint with custom capacity:**
```bash
python3 scripts/user_story_generator.py --sprint --capacity 25
```

**Sprint planning from epic file:**
```bash
python3 scripts/user_story_generator.py epic.json --sprint --capacity 40
```

#### Output Formats

**JSON output (for tool integration):**
```bash
python3 scripts/user_story_generator.py --output json
```

**CSV output (for Jira import):**
```bash
python3 scripts/user_story_generator.py --output csv
```

**Save to file:**
```bash
python3 scripts/user_story_generator.py -o json -f stories.json
```

#### Verbose Mode

**Show all stories with full details:**
```bash
python3 scripts/user_story_generator.py -v
```

**Verbose sprint planning:**
```bash
python3 scripts/user_story_generator.py --sprint --capacity 30 -v
```

### Command-Line Options

```
usage: user_story_generator.py [-h] [--sprint] [--capacity CAPACITY]
                               [--output {text,json,csv}] [--file FILE]
                               [--verbose] [--version]
                               [input]

Generate INVEST-compliant user stories from epic requirements

positional arguments:
  input                 JSON file with epic definition (optional, uses sample
                        if not provided)

options:
  -h, --help            show this help message and exit
  --sprint              Generate sprint planning instead of just epic
                        breakdown
  --capacity CAPACITY   Sprint capacity in story points (default: 30)
  --output {text,json,csv}, -o {text,json,csv}
                        Output format (default: text)
  --file FILE, -f FILE  Write output to file instead of stdout
  --verbose, -v         Show all stories in detail (not just first 3)
  --version             show program's version number and exit
```

### Input Format

#### Epic JSON Structure

Create a JSON file defining your epic:

```json
{
  "name": "User Dashboard",
  "description": "Create a comprehensive dashboard for users to view their data",
  "personas": ["end_user", "power_user"],
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

**Field Descriptions:**

- **name** (required): Short epic name
- **description** (required): Brief epic description
- **personas** (required): List of user types
  - `end_user`: Standard users
  - `admin`: Administrators
  - `power_user`: Advanced users
  - `new_user`: First-time users
- **scope** (required): List of features/capabilities
- **technical_requirements** (optional): Technical enabler stories

### Output Formats

#### Text Output (Default)

Human-readable format with full story details:

```
USER STORY: USE-001
========================================
Title: View Key Metrics
Type: story
Priority: HIGH
Points: 5

Story:
As a End User, I want to view key metrics and kpis so that I can achieve my goals related to efficiency

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
```

#### JSON Output

Machine-readable format for tool integration:

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
      "narrative": "As a End User, I want to view key metrics and kpis so that I can achieve my goals related to efficiency",
      "acceptance_criteria": [
        "Given user has access, When they view key metrics and kpis, Then the view key metrics and kpis is successfully completed",
        "Should validate input before processing",
        "Must show clear error message when action fails",
        "Should complete within 2 seconds",
        "Must be accessible via keyboard navigation"
      ],
      "estimation": 5,
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
  ]
}
```

#### CSV Output

Spreadsheet format for Jira/tool import:

```csv
id,title,type,narrative,priority,estimation,invest_check
USE-001,View Key Metrics,story,"As a End User, I want to view key metrics...",high,5,"independent:True,negotiable:True,valuable:True,estimable:True,small:True,testable:True"
USE-002,Customize Dashboard Layout,story,"As a End User, I want to customize dashboard...",medium,8,"independent:True,negotiable:True,valuable:True,estimable:True,small:True,testable:True"
```

#### Sprint Planning Output

When using `--sprint` flag:

```
============================================================
SPRINT PLANNING
============================================================
Sprint Capacity: 30 points
Committed: 28 points (93.3%)
Stories: 5 committed + 2 stretch

COMMITTED STORIES:

  [H] USE-001: View Key Metrics (5pts)
  [H] USE-003: Export Dashboard Data (3pts)
  [M] USE-002: Customize Dashboard Layout (8pts)
  [M] USE-004: Share Dashboard With (5pts)
  [L] USE-005: Set Up Automated (3pts)

STRETCH GOALS:

  [H] USE-E01: Technical: Implement Caching (5pts)
  [H] USE-E02: Technical: Set Up Real (5pts)
```

### Story Point Estimation

The tool automatically estimates story points based on complexity indicators:

**1 Point (Trivial):**
- Keywords: simple, basic, view, display
- Example: "View user profile"
- Time: 2-4 hours

**3 Points (Simple):**
- Keywords: create, edit, update
- Example: "Edit dashboard settings"
- Time: 1 day

**5 Points (Moderate):**
- Default complexity
- Example: "Export data with filtering"
- Time: 2-3 days

**8 Points (Complex):**
- Keywords: complex, advanced, integrate, migrate
- Example: "Integrate with external API"
- Time: 3-5 days

**13 Points (Very Complex):**
- Keywords: redesign, refactor, architect
- Example: "Redesign entire dashboard system"
- Time: 1-2 weeks
- Note: Consider breaking into smaller stories

### Priority Assignment

Stories are automatically prioritized based on:

**Critical:**
- Keywords: security, fix, critical, broken
- Example: "Fix security vulnerability in auth"

**High:**
- Primary personas (end_user, admin) with core features
- Keywords: core, essential, primary
- Example: "Admin user management"

**Medium:**
- Improvement and enhancement stories
- Keywords: improve, enhance, optimize
- Example: "Optimize dashboard load time"

**Low:**
- Nice-to-have features
- Secondary personas
- Example: "Add tooltip animations"

### INVEST Criteria Validation

Each story is checked against INVEST criteria:

**Independent:**
- ✓ Pass: No dependency keywords (after, depends, requires)
- ✗ Fail: Contains dependency language

**Negotiable:**
- ✓ Pass: Most stories (default true)
- Technical details can be discussed

**Valuable:**
- ✓ Pass: All stories in backlog assumed valuable
- Provides user or business value

**Estimable:**
- ✓ Pass: Description is clear (<20 words)
- ✗ Fail: Too vague or complex to estimate

**Small:**
- ✓ Pass: Estimation ≤8 points
- ✗ Fail: >8 points, needs breakdown

**Testable:**
- ✓ Pass: Has clear success criteria
- ✗ Fail: Vague words (maybe, possibly, somehow)

### Integration Patterns

#### Jira Import Workflow

```bash
# 1. Generate stories as CSV
python3 scripts/user_story_generator.py epic.json -o csv -f stories.csv

# 2. Import to Jira
# - Open Jira project
# - Issues → Import from CSV
# - Map CSV columns to Jira fields
# - Import stories
```

**CSV to Jira Field Mapping:**
- `id` → Story ID or Summary prefix
- `title` → Summary
- `narrative` → Description
- `priority` → Priority
- `estimation` → Story Points
- `type` → Issue Type (Story or Enabler)

#### Linear Import Workflow

```bash
# 1. Generate as JSON
python3 scripts/user_story_generator.py epic.json -o json -f stories.json

# 2. Use Linear API to import
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @stories.json
```

#### ProductBoard Integration

```bash
# 1. Generate stories
python3 scripts/user_story_generator.py epic.json -v

# 2. Copy stories to ProductBoard
# - Open ProductBoard Features board
# - Create feature card per story
# - Add story narrative to description
# - Set priority and effort scores
```

### Advanced Usage

#### Custom Epic Templates

Create epic templates for common patterns:

**Feature Epic Template:**
```json
{
  "name": "New Feature Name",
  "description": "Feature description",
  "personas": ["end_user"],
  "scope": [
    "Core functionality",
    "Error handling",
    "User documentation"
  ],
  "technical_requirements": [
    "Database schema",
    "API endpoints"
  ]
}
```

**Refactor Epic Template:**
```json
{
  "name": "System Refactor",
  "description": "Technical improvement",
  "personas": ["power_user"],
  "scope": [],
  "technical_requirements": [
    "Refactor component A",
    "Update tests",
    "Performance benchmarks",
    "Migration script"
  ]
}
```

#### Batch Processing

Process multiple epics:

```bash
# Generate stories for multiple epics
for epic in epics/*.json; do
  python3 scripts/user_story_generator.py "$epic" \
    -o json \
    -f "output/$(basename "$epic" .json)_stories.json"
done
```

#### Sprint Planning Workflow

```bash
# 1. Generate all stories
python3 scripts/user_story_generator.py epic.json -o json -f backlog.json

# 2. Plan current sprint (30 points)
python3 scripts/user_story_generator.py epic.json --sprint --capacity 30 -f sprint_current.txt

# 3. Plan next sprint (remaining stories)
# Manual: Remove committed stories from epic.json
python3 scripts/user_story_generator.py epic_remaining.json --sprint --capacity 30 -f sprint_next.txt
```

### Troubleshooting

#### Issue: Stories too large (>8 points)

**Solution:** Break down epic scope into smaller pieces

```json
{
  "scope": [
    "View dashboard (basic metrics only)",
    "Add advanced filters (separate story)",
    "Export data (separate story)"
  ]
}
```

#### Issue: Generic acceptance criteria

**Problem:** Tool generates generic criteria for vague scope items

**Solution:** Use more specific scope descriptions

```json
// Instead of:
"scope": ["Dashboard improvements"]

// Use:
"scope": [
  "Add real-time data refresh every 30 seconds",
  "Filter dashboard by date range",
  "Export dashboard as PDF"
]
```

#### Issue: Wrong persona selected

**Solution:** Specify multiple personas if feature serves different users

```json
{
  "personas": ["end_user", "admin"],
  "scope": [
    "View dashboard (end_user focused)",
    "Configure dashboard defaults (admin focused)"
  ]
}
```

#### Issue: Missing technical enablers

**Solution:** Always include technical requirements for foundational work

```json
{
  "technical_requirements": [
    "Set up database indexes for dashboard queries",
    "Implement caching layer",
    "Add monitoring and alerts"
  ]
}
```

### Best Practices

**DO:**
- Keep epic scope focused (5-10 items max)
- Use specific, actionable scope descriptions
- Include technical requirements for infrastructure work
- Review and refine generated stories before sprint planning
- Use verbose mode to see all stories before committing

**DON'T:**
- Create epics with >15 scope items (break into multiple epics)
- Use vague scope like "improve dashboard" (be specific)
- Forget technical enablers (will create bottlenecks)
- Skip INVEST validation (use it to improve story quality)
- Blindly accept story point estimates (adjust based on team knowledge)

### Performance Tips

**Large Epics:**
- Break into multiple smaller epics (<10 stories each)
- Process separately to avoid overwhelming output
- Use JSON format for easier parsing

**Sprint Planning:**
- Start with realistic capacity (historical velocity)
- Leave 20% buffer for unknowns
- Review committed vs stretch goals with team

**Tool Integration:**
- Use JSON format for API integrations
- Use CSV format for spreadsheet imports
- Use text format for documentation

---

**Last Updated:** 2025-11-08
**Tool Version:** 1.0.0
**Related Files:**
- [frameworks.md](frameworks.md) - INVEST criteria, sprint planning frameworks
- [templates.md](templates.md) - User story and epic templates
