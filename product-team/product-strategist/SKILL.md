---
name: product-strategist
description: Strategic product leadership toolkit for Head of Product including OKR cascade generation, market analysis, vision setting, and team scaling. Use for strategic planning, goal alignment, competitive analysis, and organizational design.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: product
  domain: product-strategy
  updated: 2025-11-08
  keywords:
    - OKR framework
    - strategic planning
    - goal alignment
    - market analysis
    - competitive analysis
    - vision setting
    - team scaling
    - organizational design
    - strategy cascade
    - key results
    - alignment tracking
    - metrics definition
    - KPI development
    - strategic roadmap
    - business strategy
    - market positioning
  tech-stack:
    - Python 3.8+
    - CLI
    - JSON export
    - Alignment scoring
  python-tools:
    - okr_cascade_generator.py
---

# Product Strategist

Strategic toolkit for Head of Product to drive vision, alignment, and organizational excellence.

## Core Capabilities
- OKR cascade generation and alignment
- Market and competitive analysis
- Product vision and strategy frameworks
- Team scaling and organizational design
- Metrics and KPI definition

## Key Scripts

### okr_cascade_generator.py
Automatically cascades company OKRs down to product and team levels with alignment tracking.

**Usage:**
```bash
# Growth strategy OKRs
python3 scripts/okr_cascade_generator.py growth

# Retention strategy
python3 scripts/okr_cascade_generator.py retention

# Revenue strategy
python3 scripts/okr_cascade_generator.py revenue

# JSON output
python3 scripts/okr_cascade_generator.py growth --output json

# Save to file
python3 scripts/okr_cascade_generator.py growth -o json -f okrs.json

# Verbose mode with metrics
python3 scripts/okr_cascade_generator.py growth --metrics -v
```

**Available Options:**
- `strategy_type`: Strategy type (growth, retention, revenue, innovation, operational) - required
- `--output/-o`: Output format (text, json, csv) - default: text
- `--file/-f`: Write output to file instead of stdout
- `--metrics`: Include detailed metric definitions
- `--verbose/-v`: Enable detailed output
- `--help`: Show help message with examples

**Features:**
- Strategies: growth, retention, revenue, innovation, operational
- Generates company → product → team OKR cascade
- Calculates alignment scores
- Tracks contribution percentages
