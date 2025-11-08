---
name: ux-researcher-designer
description: UX research and design toolkit for Senior UX Designer/Researcher including data-driven persona generation, journey mapping, usability testing frameworks, and research synthesis. Use for user research, persona creation, journey mapping, and design validation.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: product
  domain: ux-research
  updated: 2025-11-08
  keywords:
    - user research
    - persona generation
    - journey mapping
    - usability testing
    - user interviews
    - design validation
    - empathy mapping
    - user behavior
    - psychographics
    - user archetypes
    - design implications
    - research synthesis
    - user segmentation
    - accessibility research
    - qualitative research
    - design insights
  tech-stack:
    - Python 3.8+
    - CLI
    - JSON processing
    - User data analysis
    - JSON export
  python-tools:
    - persona_generator.py
---

# UX Researcher & Designer

Comprehensive toolkit for user-centered research and experience design.

## Core Capabilities
- Data-driven persona generation
- Customer journey mapping
- Usability testing frameworks
- Research synthesis and insights
- Design validation methods

## Key Scripts

### persona_generator.py
Creates research-backed personas from user data and interviews.

**Usage:**
```bash
# Basic persona generation
python3 scripts/persona_generator.py --data user_research.json

# With segment filtering
python3 scripts/persona_generator.py --data user_data.json --segment "premium"

# JSON output
python3 scripts/persona_generator.py --data user_research.json --output json

# Save to file
python3 scripts/persona_generator.py --data user_research.json -o json -f personas.json

# Verbose mode
python3 scripts/persona_generator.py --data user_research.json -v
```

**Available Options:**
- `--data`: User research data file (JSON format) - required
- `--segment`: Filter by user segment (optional)
- `--output/-o`: Output format (text, json, csv) - default: text
- `--file/-f`: Write output to file instead of stdout
- `--verbose/-v`: Enable detailed output
- `--help`: Show help message with examples

**Features**:
- Analyzes user behavior patterns
- Identifies persona archetypes
- Extracts psychographics
- Generates scenarios
- Provides design implications
- Confidence scoring based on sample size
