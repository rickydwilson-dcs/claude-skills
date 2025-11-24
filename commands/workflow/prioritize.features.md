---
name: prioritize.features
title: Feature Prioritization with RICE Framework
description: Analyze and prioritize feature requests using the RICE framework with automated scoring, portfolio analysis, and quarterly roadmap generation
category: product
subcategory: feature-planning
difficulty: intermediate
time-saved: "2-3 hours per prioritization session"
frequency: "Weekly per product team"
use-cases:
  - "Prioritizing quarterly roadmap with 20+ feature candidates using RICE scores"
  - "Analyzing portfolio balance between quick wins and strategic big bets"
  - "Generating quarterly roadmap with capacity planning and team allocation"
  - "Validating stakeholder requests with data-driven prioritization framework"
related-agents:
  - cs-product-manager
  - cs-agile-product-owner
  - cs-product-strategist
related-skills:
  - product-team/product-manager-toolkit
  - product-team/product-strategist
related-commands:
  - /feature-analyze
  - /roadmap-generate
  - /okr-cascade
dependencies:
  tools:
    - Read
    - Write
    - Bash
    - Grep
    - Glob
  scripts:
    - product-team/product-manager-toolkit/scripts/rice_prioritizer.py
    - product-team/product-manager-toolkit/scripts/capacity_planner.py
  python-packages: []
compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows
examples:
  - title: "Basic Feature Prioritization"
    input: "/prioritize.features features.csv"
    output: "Generated RICE scores for 15 features, top 3: API Rate Limiting (RICE: 85), User Dashboard (RICE: 78), Dark Mode (RICE: 45)"
  - title: "Prioritization with Capacity Planning"
    input: "/prioritize.features features.csv --capacity 20"
    output: "Quarterly roadmap generated: Q1 includes 5 features (18.5 person-months), 1.5 months buffer"
  - title: "Portfolio Analysis"
    input: "/prioritize.features features.csv --analysis portfolio"
    output: "Portfolio balance: 40% quick wins, 35% strategic bets, 25% technical debt. Recommended shift: +10% strategic bets"
  - title: "Advanced with Constraints"
    input: "/prioritize.features features.csv --constraints dependencies.json --teams teams.json"
    output: "Generated roadmap with dependency resolution: 18 features prioritized, 3 blocked by dependencies, 2 waiting for team capacity"
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0
version: v1.2.1
author: Claude Skills Team
contributors:
  - Product Team
  - Beta Testers
created: 2025-10-15
updated: 2025-11-24
tags:
  - product-management
  - feature-planning
  - prioritization
  - rice-framework
  - roadmap-planning
  - agile
  - capacity-planning
  - portfolio-analysis
featured: false
verified: true
license: MIT
---

## Overview

Feature prioritization is critical for product strategy. This command implements the RICE framework to systematically evaluate and rank feature requests.

### RICE Framework

**R**each: How many users will this impact?
**I**mpact: What will be the effect on each user?
**C**onfidence: How confident are we in the reach/impact estimates?
**E**ffort: How many person-months will this take?

## Usage

```bash
# Basic prioritization from CSV
/prioritize.features features.csv

# With capacity planning
/prioritize.features features.csv --capacity 20

# Portfolio analysis
/prioritize.features features.csv --analysis portfolio

# With team and dependency constraints
/prioritize.features features.csv --constraints dependencies.json --teams teams.json

# Generate quarterly roadmap
/prioritize.features features.csv --output roadmap.json --quarters 4
```

## Implementation

### Phase 1: Data Collection
- Read feature CSV with R, I, C, E values
- Parse team capacity from teams.json
- Extract dependency constraints

### Phase 2: RICE Scoring
- Calculate score = (R * I * C) / E
- Normalize scores to 0-100 scale
- Group by category/team

### Phase 3: Roadmap Generation
- Sort features by score
- Apply capacity constraints
- Handle dependencies
- Generate quarterly allocation

### Phase 4: Analysis & Report
- Calculate portfolio balance
- Identify risks and bottlenecks
- Generate recommendations
- Output JSON and markdown reports
