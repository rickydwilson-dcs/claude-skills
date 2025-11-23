# Design Token Standards Reference Guide

## Overview
Comprehensive standards for defining, naming, organizing, and implementing design tokens in modern design systems. Design tokens are the visual atoms of a design system - named entities that store design decisions.

## Token Categories

### Color Tokens

**Base Palette (Raw Colors):**
```
--color-blue-100: #E6F2FF
--color-blue-200: #BFDDFF
--color-blue-300: #99C9FF
--color-blue-500: #0066CC (primary)
--color-blue-700: #004C99
--color-blue-900: #003366
```

**Semantic Tokens (Meaningful Names):**
```
--color-primary: var(--color-blue-500)
--color-primary-hover: var(--color-blue-700)
--color-success: #10B981
--color-warning: #F59E0B
--color-danger: #EF4444
--color-text-primary: #000000
--color-text-secondary: #666666
--color-background: #FFFFFF
```

**Component Tokens (Specific Usage):**
```
--button-background-primary: var(--color-primary)
--button-text-primary: var(--color-text-inverse)
--input-border-default: var(--color-neutral-300)
--input-border-focus: var(--color-primary)
```

### Typography Tokens

**Font Family:**
```
--font-family-primary: 'Inter', -apple-system, system-ui, sans-serif
--font-family-mono: 'SF Mono', 'Consolas', monospace
```

**Font Sizes (Scale):**
```
--font-size-xs: 0.75rem    (12px)
--font-size-sm: 0.875rem   (14px)
--font-size-base: 1rem     (16px)
--font-size-lg: 1.125rem   (18px)
--font-size-xl: 1.25rem    (20px)
--font-size-2xl: 1.5rem    (24px)
--font-size-3xl: 2rem      (32px)
--font-size-4xl: 2.5rem    (40px)
```

**Font Weights:**
```
--font-weight-normal: 400
--font-weight-medium: 500
--font-weight-semibold: 600
--font-weight-bold: 700
```

**Line Heights:**
```
--line-height-tight: 1.2
--line-height-normal: 1.5
--line-height-relaxed: 1.8
```

### Spacing Tokens (8px Grid)

**Base Scale:**
```
--space-1: 0.25rem   (4px)
--space-2: 0.5rem    (8px)
--space-3: 0.75rem   (12px)
--space-4: 1rem      (16px)
--space-5: 1.5rem    (24px)
--space-6: 2rem      (32px)
--space-8: 3rem      (48px)
--space-10: 4rem     (64px)
```

**Component Spacing:**
```
--button-padding-x: var(--space-4)
--button-padding-y: var(--space-2)
--card-padding: var(--space-6)
--section-margin: var(--space-10)
```

### Shadow Tokens (Elevation)

```
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1)
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1)
```

### Border Tokens

**Border Widths:**
```
--border-width-thin: 1px
--border-width-medium: 2px
--border-width-thick: 4px
```

**Border Radius:**
```
--border-radius-none: 0
--border-radius-sm: 0.125rem  (2px)
--border-radius-md: 0.25rem   (4px)
--border-radius-lg: 0.5rem    (8px)
--border-radius-full: 9999px  (circular)
```

## Naming Conventions

### Token Naming Pattern
```
[category]-[property]-[variant]-[state]

Examples:
--color-background-primary
--color-text-secondary
--button-background-primary-hover
--input-border-error
```

### Naming Rules
1. Use lowercase with hyphens (kebab-case)
2. Be specific but not overly verbose
3. Use semantic names for component tokens
4. Include state (hover, focus, active, disabled)
5. Group related tokens with prefixes

## Token Organization

### File Structure
```
tokens/
├─ colors.json           (all color tokens)
├─ typography.json       (font tokens)
├─ spacing.json          (spacing scale)
├─ shadows.json          (elevation tokens)
├─ borders.json          (border tokens)
└─ components/
   ├─ button.json        (button-specific tokens)
   ├─ input.json         (input-specific tokens)
   └─ card.json          (card-specific tokens)
```

### JSON Format (Style Dictionary)
```json
{
  "color": {
    "primary": {
      "value": "#0066CC",
      "type": "color",
      "description": "Primary brand color"
    },
    "background": {
      "default": {
        "value": "#FFFFFF",
        "type": "color"
      },
      "subtle": {
        "value": "#F5F5F5",
        "type": "color"
      }
    }
  }
}
```

## Token Implementation

### CSS Custom Properties
```css
:root {
  /* Colors */
  --color-primary: #0066CC;
  --color-text-primary: #000000;
  
  /* Typography */
  --font-family-primary: 'Inter', sans-serif;
  --font-size-base: 1rem;
  
  /* Spacing */
  --space-4: 1rem;
}

/* Usage */
.button {
  background-color: var(--color-primary);
  font-family: var(--font-family-primary);
  padding: var(--space-4);
}
```

### JavaScript/TypeScript
```typescript
export const tokens = {
  color: {
    primary: '#0066CC',
    textPrimary: '#000000',
  },
  fontSize: {
    base: '1rem',
    lg: '1.125rem',
  },
  spacing: {
    4: '1rem',
    6: '2rem',
  },
};

// Usage in React
<Button style={{ backgroundColor: tokens.color.primary }} />
```

### Figma Variables
1. Create variable collection: "Design Tokens"
2. Add color variables: `color/primary`, `color/text/primary`
3. Add number variables: `spacing/4`, `fontSize/base`
4. Apply to components
5. Sync with code via Figma Tokens plugin

## Resources
- Style Dictionary (token build tool)
- Figma Tokens plugin
- Token naming generator
- Token documentation template

---
**Last Updated:** November 23, 2025
**Related:** design_system_principles.md, component_api_guidelines.md
