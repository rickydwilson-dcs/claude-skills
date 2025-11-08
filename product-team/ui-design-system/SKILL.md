---
name: ui-design-system
description: UI design system toolkit for Senior UI Designer including design token generation, component documentation, responsive design calculations, and developer handoff tools. Use for creating design systems, maintaining visual consistency, and facilitating design-dev collaboration.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: product
  domain: design
  updated: 2025-11-08
  keywords:
    - design systems
    - design tokens
    - color palette
    - typography scale
    - spacing system
    - component documentation
    - responsive design
    - design handoff
    - visual consistency
    - Figma integration
    - CSS tokens
    - SCSS variables
    - accessibility standards
    - design patterns
    - brand guidelines
    - design tooling
  tech-stack:
    - Python 3.8+
    - CLI
    - JSON export
    - CSS/SCSS generation
    - Color processing
  python-tools:
    - design_token_generator.py
---

# UI Design System

Professional toolkit for creating and maintaining scalable design systems.

## Core Capabilities
- Design token generation (colors, typography, spacing)
- Component system architecture
- Responsive design calculations
- Accessibility compliance
- Developer handoff documentation

## Key Scripts

### design_token_generator.py
Generates complete design system tokens from brand colors.

**Usage:**
```bash
# Modern style, JSON output
python3 scripts/design_token_generator.py --brand "#0066CC" --style modern

# CSS export
python3 scripts/design_token_generator.py --brand "#0066CC" --style modern --output css

# Save to file
python3 scripts/design_token_generator.py --brand "#0066CC" --style modern -o json -f tokens.json

# SCSS format
python3 scripts/design_token_generator.py --brand "#0066CC" --style classic --output scss

# Verbose mode
python3 scripts/design_token_generator.py --brand "#0066CC" --style playful -v
```

**Available Options:**
- `--brand`: Brand color in hex format (required) - e.g., "#0066CC"
- `--style`: Design style (modern, classic, playful) - default: modern
- `--output/-o`: Output format (json, css, scss) - default: json
- `--file/-f`: Write output to file instead of stdout
- `--verbose/-v`: Enable detailed output
- `--help`: Show help message with examples

**Features**:
- Complete color palette generation
- Modular typography scale
- 8pt spacing grid system
- Shadow and animation tokens
- Responsive breakpoints
- Multiple export formats
