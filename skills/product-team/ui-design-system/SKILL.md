---

# === CORE IDENTITY ===
name: ui-design-system
title: UI Design System Skill Package
description: UI design system toolkit for Senior UI Designer including design token generation, component documentation, responsive design calculations, and developer handoff tools. Use for creating design systems, maintaining visual consistency, and facilitating design-dev collaboration.
domain: product
subdomain: ux-design

# === WEBSITE DISPLAY ===
difficulty: intermediate
time-saved: """TODO: Quantify time savings"""
frequency: """TODO: Estimate usage frequency"""
use-cases:
  - Primary workflow for Ui Design System
  - Analysis and recommendations for ui design system tasks
  - Best practices implementation for ui design system
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
  - JSON export
  - CSS/SCSS generation
  - Color processing

# === EXAMPLES ===
examples:
  -
    title: Example Usage
    input: "TODO: Add example input for ui-design-system"
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
tags: [design, product, system]
featured: false
verified: true
---

# UI Design System

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


Professional toolkit for creating and maintaining scalable design systems. This skill provides Python tools for token generation, comprehensive frameworks for design system architecture, and battle-tested templates for component documentation.

**What This Skill Provides:**
- Design token generator from brand colors
- Complete color, typography, and spacing systems
- Component architecture patterns
- Accessibility compliance frameworks (WCAG 2.1 AA)
- Developer handoff documentation

**Best For:**
- Building new design systems from scratch
- Standardizing existing design patterns
- Generating design tokens programmatically
- Ensuring accessibility compliance
- Facilitating design-development collaboration

## Quick Start

### Generate Design Tokens
```bash
# Modern style
python scripts/design_token_generator.py --brand "#0066CC" --style modern

# Export as CSS
python scripts/design_token_generator.py --brand "#0066CC" --output css

# Export as JSON for Figma
python scripts/design_token_generator.py --brand "#0066CC" -o json -f tokens.json
```

### Design Token Structure
**Color System:** 50-900 scale (primary, secondary, neutral)
**Typography:** Modular scale (xs to 3xl)
**Spacing:** 8pt grid system
**Shadows:** 5 elevation levels
**Animation:** Duration and easing tokens

See [frameworks.md](references/frameworks.md) for complete token architecture.

## Core Workflows

### 1. Design System Creation Process

**Steps:**
1. Define brand color: `#0066CC`
2. Choose style: modern, classic, or playful
3. Generate tokens: `python scripts/design_token_generator.py --brand "#0066CC" --style modern`
4. Export format: JSON (Figma), CSS (web), SCSS (Sass)
5. Import to design tools and codebase
6. Document component guidelines

**Token Generation:**
```bash
python scripts/design_token_generator.py --brand "#0066CC" --style modern -o json -f tokens.json
```

**Style Presets:**
- **Modern:** Clean, minimalist, sans-serif
- **Classic:** Traditional, serif, formal
- **Playful:** Vibrant, rounded, casual

**Detailed Process:** See [frameworks.md](references/frameworks.md) for design token architecture and color system design.

**Templates:** See [templates.md](references/templates.md) for token documentation format.

### 2. Component System Design

**Component Hierarchy:**
```
Primitives → Patterns → Layouts

Primitives: Button, Input, Checkbox
Patterns: FormGroup, Card, Modal
Layouts: Container, Grid, Stack
```

**Component Variants:**
- **Size:** sm, md, lg
- **Style:** primary, secondary, outline, ghost
- **State:** default, hover, active, focus, disabled

**Component Props API:**
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: ReactNode;
}
```

**Detailed Framework:** See [frameworks.md](references/frameworks.md) for component architecture and API design patterns.

**Templates:** See [templates.md](references/templates.md) for component documentation template.

### 3. Responsive Design Implementation

**Breakpoint System:**
```
xs: 0px (mobile)
sm: 640px (large mobile)
md: 768px (tablet)
lg: 1024px (laptop)
xl: 1280px (desktop)
2xl: 1536px (large desktop)
```

**Mobile-First Approach:**
```css
/* Default: mobile */
padding: 16px;

/* Tablet and up */
@media (min-width: 768px) {
  padding: 24px;
}
```

**Grid System:**
- 12-column grid
- Responsive columns (col-12 md:col-6 lg:col-4)
- Fluid containers

**Detailed Framework:** See [frameworks.md](references/frameworks.md) for responsive design system and grid implementation.

## Python Tools

### design_token_generator.py
Generate complete design token systems from brand color.

**Key Features:**
- Color palette generation (50-900 scale)
- Modular typography scale
- 8pt spacing grid
- Shadow and animation tokens
- Multiple export formats (JSON, CSS, SCSS)
- Three style presets

**Usage:**
```bash
# Modern style, JSON output
python3 scripts/design_token_generator.py --brand "#0066CC" --style modern

# CSS export
python3 scripts/design_token_generator.py --brand "#0066CC" --output css -f tokens.css

# SCSS export
python3 scripts/design_token_generator.py --brand "#0066CC" --output scss -f tokens.scss

# JSON for Figma
python3 scripts/design_token_generator.py --brand "#0066CC" -o json -f figma-tokens.json

# Verbose mode
python3 scripts/design_token_generator.py --brand "#0066CC" -v
```

**Generated Tokens:**
- **Color:** Primary, secondary, neutral scales (50-900)
- **Typography:** Font sizes (xs-3xl), line heights, weights
- **Spacing:** 8pt grid (0-20)
- **Shadows:** 5 elevation levels
- **Animation:** Durations and easing functions

**Export Formats:**
- JSON (React, Tailwind, Figma)
- CSS Custom Properties (web)
- SCSS Variables (Sass)

**Complete Documentation:** See [tools.md](references/tools.md) for full usage guide, integration patterns, and customization options.

## Reference Documentation

### Frameworks ([frameworks.md](references/frameworks.md))
Comprehensive design system frameworks:
- Design Token Architecture: Token types, naming conventions, distribution
- Color System Design: Palette generation, semantic mapping, contrast standards
- Typography System: Type scale, hierarchy, font loading
- Spacing System: 8pt grid, responsive spacing
- Component Architecture: Component library structure, variants, API design
- Responsive Design: Breakpoints, grid system, mobile-first approach
- Accessibility Standards: WCAG 2.1 AA compliance, semantic HTML
- Design System Governance: Versioning, documentation, token distribution

### Templates ([templates.md](references/templates.md))
Ready-to-use templates:
- Component Documentation: Complete component doc template with examples
- Design Token Documentation: Token reference format
- Component Checklist: Readiness checklist for design and development

### Tools ([tools.md](references/tools.md))
Python tool documentation:
- design_token_generator.py: Complete usage guide
- Command-Line Options: All flags and parameters
- Generated Tokens: Full list of token types
- Export Formats: JSON, CSS, SCSS examples
- Integration Patterns: React/Tailwind, Figma, CSS frameworks
- Best Practices: DO/DON'T guidelines

## Integration Points

This toolkit integrates with:
- **Design Tools:** Figma, Sketch, Adobe XD (via JSON tokens)
- **CSS Frameworks:** Tailwind CSS, Styled Components, Emotion
- **Build Tools:** Webpack, Vite, Rollup
- **Documentation:** Storybook, Docz, Styleguidist
- **Testing:** Chromatic, Percy (visual regression)

See [tools.md](references/tools.md) for detailed integration workflows.

## Quick Commands

```bash
# Generate tokens (modern style)
python scripts/design_token_generator.py --brand "#0066CC" --style modern

# Different styles
python scripts/design_token_generator.py --brand "#0066CC" --style classic
python scripts/design_token_generator.py --brand "#8B5CF6" --style playful

# Export formats
python scripts/design_token_generator.py --brand "#0066CC" -o json -f tokens.json
python scripts/design_token_generator.py --brand "#0066CC" -o css -f tokens.css
python scripts/design_token_generator.py --brand "#0066CC" -o scss -f tokens.scss

# Verbose output
python scripts/design_token_generator.py --brand "#0066CC" -v
```
