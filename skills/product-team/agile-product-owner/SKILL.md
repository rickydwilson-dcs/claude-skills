---
name: agile-product-owner
description: Agile product ownership toolkit for Senior Product Owner including INVEST-compliant user story generation, sprint planning, backlog management, and velocity tracking. Use for story writing, sprint planning, stakeholder communication, and agile ceremonies.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: product
  domain: agile
  updated: 2025-11-08
  keywords:
    - agile product ownership
    - user story generation
    - sprint planning
    - INVEST criteria
    - backlog prioritization
    - acceptance criteria
    - velocity tracking
    - story points estimation
    - agile ceremonies
    - product backlog
    - sprint capacity
    - burndown charts
    - retrospectives
    - daily standups
    - release planning
  tech-stack:
    - Python 3.8+
    - CLI
    - CSV processing
    - JSON export
  python-tools:
    - user_story_generator.py
---

# Agile Product Owner

Complete toolkit for agile product ownership - from backlog refinement to sprint delivery. This skill provides Python tools for story generation, comprehensive frameworks for agile ceremonies, and battle-tested templates for user stories and epics.

**What This Skill Provides:**
- INVEST-compliant user story generator with sprint planning
- Complete agile ceremony frameworks (planning, review, retro)
- Velocity tracking and capacity planning methods
- Story estimation and backlog refinement processes

**Best For:**
- Breaking epics into deliverable user stories
- Sprint planning and capacity allocation
- Running effective agile ceremonies
- Tracking team velocity and burndown

## Quick Start

### Generate User Stories
```bash
# From sample epic
python scripts/user_story_generator.py

# From custom epic
python scripts/user_story_generator.py epic.json

# Sprint planning (30 points)
python scripts/user_story_generator.py --sprint --capacity 30
```

### Story Quality Check
Use INVEST criteria to validate stories:
- **I**ndependent: Can complete without dependencies
- **N**egotiable: Flexible on implementation
- **V**aluable: Delivers user/business value
- **E**stimable: Team can size it
- **S**mall: Fits in one sprint
- **T**estable: Clear success criteria

See [frameworks.md](references/frameworks.md) for complete INVEST guidelines.

## Core Workflows

### 1. Epic Breakdown Process

**Steps:**
1. Define epic with scope and personas
2. Generate stories: `python scripts/user_story_generator.py epic.json`
3. Review INVEST criteria compliance
4. Refine acceptance criteria
5. Prioritize and estimate with team

**Epic JSON Format:**
```json
{
  "name": "User Dashboard",
  "description": "Create dashboard for users",
  "personas": ["end_user", "power_user"],
  "scope": [
    "View key metrics and KPIs",
    "Customize dashboard layout",
    "Export dashboard data"
  ],
  "technical_requirements": [
    "Implement caching for performance"
  ]
}
```

**Detailed Process:** See [frameworks.md](references/frameworks.md) for INVEST criteria and backlog refinement.

**Templates:** See [templates.md](references/templates.md) for epic and user story templates.

### 2. Sprint Planning Process

**Part 1: What Will We Build? (2 hours)**
1. Set sprint goal aligned with quarterly OKRs
2. Calculate team capacity (velocity × sprint days)
3. Pull stories from backlog until capacity reached
4. Identify dependencies and risks

**Part 2: How Will We Build It? (2 hours)**
1. Break stories into technical tasks
2. Estimate task hours
3. Assign initial owners
4. Commit to sprint scope

**Sprint Planning Tool:**
```bash
python scripts/user_story_generator.py epic.json --sprint --capacity 30
```

**Detailed Framework:** See [frameworks.md](references/frameworks.md) for complete sprint planning guide.

**Templates:** See [templates.md](references/templates.md) for sprint planning agenda.

### 3. Backlog Refinement Process

**Weekly Activity (1 hour mid-sprint):**
1. Review upcoming epics
2. Break into user stories
3. Write acceptance criteria
4. Estimate with planning poker
5. Ensure 2-3 sprints of refined backlog

**Estimation Scale:**
- 1-2 points: Simple (2-4 hours)
- 3-5 points: Moderate (1-3 days)
- 8 points: Complex (3-5 days)
- 13+ points: Too large - needs breakdown

**Detailed Process:** See [frameworks.md](references/frameworks.md) for refinement and estimation methods.

**Templates:** See [templates.md](references/templates.md) for story templates and splitting techniques.

## Python Tools

### user_story_generator.py
INVEST-compliant story generator with sprint planning.

**Key Features:**
- Epic breakdown into user stories
- Automatic acceptance criteria generation
- Story point estimation
- INVEST criteria validation
- Sprint capacity planning
- Multiple output formats (text, JSON, CSV)

**Usage:**
```bash
# Basic story generation
python3 scripts/user_story_generator.py epic.json

# Sprint planning
python3 scripts/user_story_generator.py --sprint --capacity 30

# JSON output for Jira import
python3 scripts/user_story_generator.py -o json -f stories.json

# CSV for spreadsheet import
python3 scripts/user_story_generator.py -o csv -f backlog.csv

# Verbose mode (show all stories)
python3 scripts/user_story_generator.py -v
```

**Story Point Estimation:**
- 1 pt: Simple, basic, view (2-4 hours)
- 3 pts: Create, edit, update (1 day)
- 5 pts: Moderate complexity (2-3 days)
- 8 pts: Complex, integrate (3-5 days)
- 13 pts: Redesign, refactor (1-2 weeks, needs breakdown)

**Complete Documentation:** See [tools.md](references/tools.md) for full usage guide, input formats, and integration patterns.

## Reference Documentation

### Frameworks ([frameworks.md](references/frameworks.md))
Comprehensive agile methodologies:
- INVEST Criteria: Detailed guidelines for each criterion
- Sprint Planning: Two-part planning framework
- Sprint Review & Retrospective: Complete ceremony guides
- Daily Standup: Three questions format and anti-patterns
- Backlog Refinement: Estimation and prioritization
- Velocity Tracking: Calculation, trends, burndown charts
- Release Planning: Capacity and timeline forecasting

### Templates ([templates.md](references/templates.md))
Ready-to-use templates:
- User Story Templates: Standard, feature, technical, bug fix formats
- Epic Templates: Complete epic structure with examples
- Sprint Ceremony Agendas: Planning, review, retrospective formats
- Story Splitting Techniques: By workflow, business rules, data entry
- Best Practices: Writing effective stories and avoiding pitfalls

### Tools ([tools.md](references/tools.md))
Python tool documentation:
- user_story_generator.py: Complete usage guide
- Input Formats: Epic JSON structure
- Output Formats: Text, JSON, CSV examples
- Command-Line Options: All flags and parameters
- Integration Patterns: Jira, Linear, ProductBoard workflows
- Troubleshooting: Common issues and solutions
- Best Practices: DO/DON'T guidelines

## Integration Points

This toolkit integrates with:
- **Project Management:** Jira, Linear, Azure DevOps, Asana
- **Collaboration:** Confluence, Notion, Miro
- **Version Control:** GitHub Issues, GitLab Issues
- **Roadmapping:** ProductBoard, Aha!, Roadmunk

See [tools.md](references/tools.md) for detailed integration workflows.

## Quick Commands

```bash
# Generate stories from sample
python scripts/user_story_generator.py

# Generate from custom epic
python scripts/user_story_generator.py epic.json

# Sprint planning (30 points)
python scripts/user_story_generator.py --sprint --capacity 30

# Export as JSON
python scripts/user_story_generator.py -o json -f stories.json

# Export as CSV
python scripts/user_story_generator.py -o csv -f backlog.csv

# Verbose output (all stories)
python scripts/user_story_generator.py -v
```
