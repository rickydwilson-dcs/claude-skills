---

# === CORE IDENTITY ===
name: ux-researcher-designer
title: UX Researcher Designer Skill Package
description: UX research and design toolkit for Senior UX Designer/Researcher including data-driven persona generation, journey mapping, usability testing frameworks, and research synthesis. Use for user research, persona creation, journey mapping, and design validation.
domain: product
subdomain: ux-design

# === WEBSITE DISPLAY ===
difficulty: intermediate
time-saved: "TODO: Quantify time savings"
frequency: "TODO: Estimate usage frequency"
use-cases:
  - Primary workflow for Ux Researcher Designer
  - Analysis and recommendations for ux researcher designer tasks
  - Best practices implementation for ux researcher designer
  - Integration with related skills and workflows

# === RELATIONSHIPS ===
related-agents: []
related-skills: []
related-commands: []
orchestrated-by: []

# === TECHNICAL ===
dependencies:
  scripts: []
  references: []
  assets: []
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack:
  - Python 3.8+
  - CLI
  - JSON processing
  - User data analysis
  - JSON export

# === EXAMPLES ===
examples:
  -
    title: Example Usage
    input: "TODO: Add example input for ux-researcher-designer"
    output: "TODO: Add expected output"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-10-19
updated: 2025-11-08
license: MIT

# === DISCOVERABILITY ===
tags: [data, design, designer, product, researcher, testing]
featured: false
verified: true
---

# UX Researcher & Designer

## Overview

This skill provides [TODO: Add 2-3 sentence overview].

**Core Value:** [TODO: Add value proposition with metrics]

**Target Audience:** [TODO: Define target users]

**Use Cases:** [TODO: List 3-5 primary use cases]


## Core Capabilities

- **[Capability 1]** - [Description]
- **[Capability 2]** - [Description]
- **[Capability 3]** - [Description]
- **[Capability 4]** - [Description]


## Key Workflows

### Workflow 1: [Workflow Name]

**Time:** [Duration estimate]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Output:** [What success looks like]

### Workflow 2: [Workflow Name]

**Time:** [Duration estimate]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Output:** [What success looks like]


Comprehensive toolkit for user-centered research and experience design. This skill provides Python tools for persona generation, research frameworks for validation, and battle-tested templates for interviews and journey mapping.

**What This Skill Provides:**
- Data-driven persona generator from user research
- User research methodologies (interviews, usability testing)
- Journey mapping and Jobs-to-be-Done frameworks
- Design validation methods (prototypes, A/B tests)
- Accessibility compliance frameworks (WCAG 2.1)

**Best For:**
- Conducting user research and synthesis
- Creating research-backed personas
- Journey mapping and empathy building
- Usability testing and validation
- Ensuring accessible design

## Quick Start

### Generate Personas
```bash
# Interactive mode
python scripts/persona_generator.py

# From user data
python scripts/persona_generator.py --data user_research.json

# Filter by segment
python scripts/persona_generator.py --data user_data.json --segment "premium"
```

### Persona Components
**Demographics:** Age, role, company, technical proficiency
**Goals:** Primary objectives and motivations
**Pain Points:** Frustrations and challenges
**Behaviors:** Usage patterns and preferences
**JTBD:** Jobs-to-be-done framework

See [frameworks.md](references/frameworks.md) for complete persona development framework.

## Core Workflows

### 1. User Research Process

**Steps:**
1. Define research questions
2. Recruit participants (5-8 per cohort)
3. Conduct interviews (30-45 min each)
4. Synthesize findings
5. Generate personas: `python scripts/persona_generator.py --data research.json`
6. Validate with stakeholders

**Research Methods:**
- **Qualitative:** Interviews, usability testing, field studies
- **Quantitative:** Surveys, analytics, A/B tests
- **Mixed:** Combine both for comprehensive insights

**Interview Structure:**
- Introduction (5 min)
- Background (5 min)
- Problem exploration (20 min)
- Solution validation (10 min)
- Wrap-up (5 min)

**Detailed Methods:** See [frameworks.md](references/frameworks.md) for qualitative and quantitative research frameworks.

**Templates:** See [templates.md](references/templates.md) for interview scripts and usability test plans.

### 2. Persona Creation Process

**Steps:**
1. Collect user data (interviews, surveys, analytics)
2. Format as JSON input
3. Generate personas: `python scripts/persona_generator.py --data user_research.json`
4. Segment by user type (enterprise, SMB, individual)
5. Validate with real users
6. Update quarterly with new data

**Persona Components:**
- Demographics and psychographics
- Goals and motivations
- Pain points and frustrations
- Behavior patterns
- Jobs-to-be-done
- Representative quotes

**Confidence Scoring:**
- High: Based on 15+ interviews
- Medium: Based on 8-14 interviews
- Low: Based on <8 interviews

**Detailed Framework:** See [frameworks.md](references/frameworks.md) for persona development and Jobs-to-be-Done framework.

**Templates:** See [templates.md](references/templates.md) for persona template and journey map format.

### 3. Design Validation Process

**Methods:**
- **Prototype Testing:** Low/mid/high-fidelity testing
- **Usability Testing:** Task-based scenarios with 5-8 users
- **A/B Testing:** Quantitative validation of design decisions
- **Design Critiques:** Structured feedback sessions

**Usability Test Structure:**
1. Plan (research questions, success metrics)
2. Recruit (5-8 participants per round)
3. Execute (45-50 min sessions)
4. Analyze (severity rating, prioritization)
5. Iterate (implement fixes, retest)

**Severity Rating:**
- Critical: Prevents task completion
- High: Causes significant frustration
- Medium: Minor inconvenience
- Low: Cosmetic issue

**Detailed Frameworks:** See [frameworks.md](references/frameworks.md) for usability testing and validation methods.

**Templates:** See [templates.md](references/templates.md) for usability test plan template.

## Python Tools

### persona_generator.py
Data-driven persona generation from user research.

**Key Features:**
- Demographic and psychographic profiling
- Goals and pain points extraction
- Behavior pattern identification
- Jobs-to-be-done analysis
- Confidence scoring based on sample size
- Multiple output formats (text, JSON, CSV)

**Usage:**
```bash
# Interactive persona creation
python3 scripts/persona_generator.py

# From user research JSON
python3 scripts/persona_generator.py --data user_research.json

# Filter by segment
python3 scripts/persona_generator.py --data user_data.json --segment "enterprise"

# JSON output
python3 scripts/persona_generator.py --data user_research.json --output json

# Save to file
python3 scripts/persona_generator.py --data user_research.json -o json -f personas.json

# Verbose mode
python3 scripts/persona_generator.py --data user_research.json -v
```

**Generated Persona Includes:**
- Name and archetype
- Demographics (age, role, company, industry)
- Goals (primary objectives)
- Pain points (frustrations)
- Behaviors (usage patterns)
- Jobs-to-be-done (JTBD framework)
- Representative quote
- Confidence level (based on sample size)

**Input Format:**
- JSON file with user research data
- Demographics, behaviors, goals, pain points, quotes
- Multiple users per segment

**Complete Documentation:** See [tools.md](references/tools.md) for full usage guide, input formats, and integration patterns.

## Reference Documentation

### Frameworks ([frameworks.md](references/frameworks.md))
Comprehensive research and design frameworks:
- User Research Methods: Qualitative and quantitative approaches
- Persona Development: JTBD, persona components, validation criteria
- Journey Mapping: Customer journey stages, map components, insights
- Usability Testing: Test planning, execution, severity rating
- Accessibility Framework: WCAG 2.1 principles, compliance checklist
- Design Validation: Prototype testing, A/B testing, design critiques

### Templates ([templates.md](references/templates.md))
Ready-to-use templates:
- User Interview Script: Complete interview guide with questions
- Persona Template: Comprehensive persona format
- Journey Map Template: Multi-stage journey mapping format
- Usability Test Plan: Complete test plan with scenarios

### Tools ([tools.md](references/tools.md))
Python tool documentation:
- persona_generator.py: Complete usage guide
- Command-Line Options: All flags and parameters
- Input Format: User research JSON structure
- Generated Output: Persona format examples
- Integration Patterns: Figma, documentation, research synthesis
- Best Practices: DO/DON'T guidelines

## Integration Points

This toolkit integrates with:
- **Design Tools:** Figma, Sketch, Miro (personas and journey maps)
- **Research Tools:** Dovetail, UserVoice, Maze, Optimal Workshop
- **Analytics:** Amplitude, Mixpanel, Hotjar, FullStory
- **Testing:** UserTesting.com, Lookback, UserZoom
- **Documentation:** Confluence, Notion, Airtable

See [tools.md](references/tools.md) for detailed integration workflows.

## Quick Commands

```bash
# Interactive persona creation
python scripts/persona_generator.py

# From user research data
python scripts/persona_generator.py --data user_research.json

# By segment
python scripts/persona_generator.py --data user_data.json --segment "enterprise"
python scripts/persona_generator.py --data user_data.json --segment "smb"

# Export formats
python scripts/persona_generator.py --data research.json -o json -f personas.json
python scripts/persona_generator.py --data research.json -o csv -f personas.csv

# Verbose output
python scripts/persona_generator.py --data research.json -v
```
