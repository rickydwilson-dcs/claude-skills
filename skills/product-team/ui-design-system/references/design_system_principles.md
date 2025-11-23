# Design System Principles Reference Guide

## Overview
Core principles and best practices for building, maintaining, and scaling design systems that enable consistent, accessible, and efficient product development.

## Design System Fundamentals

### Definition
A design system is the single source of truth for product design, combining:
- **Design tokens:** Colors, typography, spacing
- **Components:** Reusable UI elements (buttons, inputs, cards)
- **Patterns:** Common workflows and interactions
- **Guidelines:** Usage documentation and principles
- **Code:** React/Vue components matching designs

### Benefits
- **Consistency:** Same look/feel across product
- **Efficiency:** Designers and engineers reuse vs rebuild
- **Quality:** Accessibility and performance baked in
- **Scale:** New features ship faster with existing components
- **Alignment:** Single source of truth for design decisions

## Core Principles

### 1. Consistency
**Principle:** Same things look and behave the same way everywhere

**Application:**
- Button styles consistent (primary, secondary, danger)
- Spacing follows 8px grid system
- Colors from defined palette only
- Icons from single library (Heroicons, Material, etc.)

**Example:**
```
✓ Good: All primary buttons use same color, padding, hover state
✗ Bad: Each page designs buttons slightly differently
```

### 2. Accessibility
**Principle:** Design system components meet WCAG 2.1 AA standards by default

**Requirements:**
- Color contrast: 4.5:1 for normal text, 3:1 for large text
- Keyboard navigation: All interactive elements accessible via keyboard
- Screen reader support: Semantic HTML, ARIA labels
- Focus indicators: Visible focus states for keyboard users

**Example:**
```
✓ Good: Button has 4.5:1 contrast ratio, works with Tab key, announces "Submit form"
✗ Bad: Low contrast text, requires mouse, unclear to screen readers
```

### 3. Flexibility
**Principle:** Components adapt to different contexts without breaking

**Techniques:**
- Props for variants (size, color, state)
- Composition over inheritance
- Layout primitives (Stack, Grid, Flex)
- Responsive by default

**Example:**
```
<Button size="small" variant="primary">Save</Button>
<Button size="large" variant="secondary">Cancel</Button>
```

### 4. Documentation
**Principle:** Every component has clear usage guidelines

**Required Docs:**
- When to use (and when not to)
- Props/API reference
- Code examples
- Accessibility notes
- Design specs (Figma links)

**Example:**
```
## Button Component

**When to use:** Primary actions (form submit, confirm)
**Don't use for:** Navigation (use Link), destructive actions (use Button variant="danger")

**Props:**
- size: "small" | "medium" | "large"
- variant: "primary" | "secondary" | "danger"
- disabled: boolean

**Accessibility:** Includes focus styles, works with keyboard, announces action to screen readers
```

## Design System Structure

### Token Layer (Foundation)
```
Colors:
├─ Primary: #0066CC
├─ Secondary: #FF6B00
├─ Neutral: #000, #333, #666, #999, #CCC, #F5F5F5, #FFF
├─ Semantic: Success (#10B981), Warning (#F59E0B), Danger (#EF4444)

Typography:
├─ Font Family: Inter, system-ui
├─ Font Sizes: 12px, 14px, 16px, 18px, 24px, 32px
├─ Font Weights: 400, 500, 600, 700
├─ Line Heights: 1.2, 1.5, 1.8

Spacing:
├─ 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px (8px grid system)

Shadows:
├─ Elevation 1: 0 1px 3px rgba(0,0,0,0.12)
├─ Elevation 2: 0 4px 6px rgba(0,0,0,0.16)
├─ Elevation 3: 0 10px 20px rgba(0,0,0,0.20)
```

### Component Layer
```
Atoms (Basic):
├─ Button, Input, Label, Icon, Badge, Avatar

Molecules (Combined):
├─ Form Field (Label + Input + Error), Card, Tooltip

Organisms (Complex):
├─ Navbar, Sidebar, Modal, Data Table, Form
```

### Pattern Layer
```
Common Workflows:
├─ Authentication (login, signup, password reset)
├─ Forms (validation, submission, error handling)
├─ Data Display (tables, lists, cards)
├─ Navigation (tabs, breadcrumbs, pagination)
```

## Governance

### Contribution Process
1. **Proposal:** Submit design/component proposal (Figma + rationale)
2. **Review:** Design system team reviews (weekly meeting)
3. **Approval:** Approved, rejected, or needs revision
4. **Implementation:** Designer creates Figma component, engineer builds React component
5. **Documentation:** Write usage guidelines, accessibility notes
6. **Release:** Version bump, changelog, announce to team

### Versioning
**Semantic Versioning (semver):**
- **Major (1.0.0 → 2.0.0):** Breaking changes (component API changed)
- **Minor (1.0.0 → 1.1.0):** New features (new component added)
- **Patch (1.0.0 → 1.0.1):** Bug fixes (no API changes)

### Maintenance
- **Weekly:** Review contribution proposals
- **Monthly:** Component usage analytics, identify gaps
- **Quarterly:** Accessibility audit, design system health check
- **Annual:** Major version with breaking changes consolidated

## Adoption Strategies

### Phase 1: Foundation (Month 1-3)
- Establish design tokens
- Build 10-15 core components (Button, Input, Card, etc.)
- Document in Storybook
- Pilot with 1 team

### Phase 2: Scale (Month 4-6)
- Add 20-30 more components
- Migrate 2-3 product areas
- Train designers and engineers
- Measure adoption (% of UI using design system)

### Phase 3: Maturity (Month 7-12)
- 80%+ product coverage
- Contribution process established
- Regular releases (bi-weekly)
- Governance board formed

## Resources
- Design token generator tool
- Storybook setup guide
- Accessibility testing checklist
- Component contribution template

---
**Last Updated:** November 23, 2025
**Related:** design_token_standards.md, component_api_guidelines.md
