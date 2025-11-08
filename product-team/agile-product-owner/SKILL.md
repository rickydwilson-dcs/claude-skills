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

Complete toolkit for Product Owners to excel at backlog management and sprint execution.

## Core Capabilities
- INVEST-compliant user story generation
- Automatic acceptance criteria creation
- Sprint capacity planning
- Backlog prioritization
- Velocity tracking and metrics

## Key Scripts

### user_story_generator.py
Generates well-formed user stories with acceptance criteria from epics.

**Usage:**
```bash
# Basic usage
python3 scripts/user_story_generator.py input_epic.txt

# JSON output
python3 scripts/user_story_generator.py input_epic.txt --output json

# Save to file
python3 scripts/user_story_generator.py input_epic.txt -o json -f stories.json

# Sprint planning with capacity
python3 scripts/user_story_generator.py input_epic.txt --sprint --capacity 30

# Verbose mode
python3 scripts/user_story_generator.py input_epic.txt -v
```

**Available Options:**
- `input`: Input file path (required)
- `--output/-o`: Output format (text, json, csv) - default: text
- `--file/-f`: Write output to file instead of stdout
- `--sprint`: Enable sprint planning mode
- `--capacity`: Sprint capacity in story points (default: 30)
- `--verbose/-v`: Enable detailed output
- `--help`: Show help message with examples

**Features**:
- Breaks epics into stories
- INVEST criteria validation
- Automatic point estimation
- Priority assignment
- Sprint planning with capacity
