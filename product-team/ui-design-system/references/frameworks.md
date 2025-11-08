# UI Design System Frameworks

Comprehensive frameworks for building and maintaining scalable design systems.

## Design Token Architecture

Design tokens are the atomic building blocks of design systems - named entities that store visual design attributes.

### Token Types

**Color Tokens:**
```
primary-500: #0066CC
primary-600: #0052A3
primary-700: #003D7A

semantic:
  success: primary-600
  error: error-600
  warning: warning-600
```

**Typography Tokens:**
```
font-size-base: 16px
font-size-lg: 20px
line-height-base: 1.5
font-weight-normal: 400
font-weight-bold: 700
```

**Spacing Tokens:**
```
space-1: 4px
space-2: 8px
space-3: 12px
space-4: 16px
(8pt grid system)
```

**Shadow Tokens:**
```
shadow-sm: 0 1px 2px rgba(0,0,0,0.05)
shadow-md: 0 4px 6px rgba(0,0,0,0.1)
shadow-lg: 0 10px 15px rgba(0,0,0,0.15)
```

### Token Naming Conventions

**Tiered Naming (Recommended):**
```
[category]-[property]-[variant]-[state]

Examples:
color-background-primary-default
color-background-primary-hover
color-text-heading-default
spacing-padding-inline-sm
```

**Semantic Naming:**
```
[purpose]-[element]-[property]

Examples:
button-primary-background
input-border-color
card-shadow
```

## Color System Design

### Color Palette Generation

**Primary Color Scale (50-900):**
- 50: Lightest tint (backgrounds)
- 100-300: Light variants (hover states, borders)
- 400-600: Core brand colors
- 700-900: Dark variants (text, emphasis)

**Generation Algorithm:**
```
Base color: #0066CC

Lighter:
- Tint with white: mix(base, white, percentage)
- 50: 95% white
- 100: 90% white
- 200: 75% white

Darker:
- Shade with black: mix(base, black, percentage)
- 700: 15% black
- 800: 30% black
- 900: 45% black
```

### Semantic Color Mapping

**UI State Colors:**
- Success: Green (#10B981)
- Warning: Amber (#F59E0B)
- Error: Red (#EF4444)
- Info: Blue (#3B82F6)

**Neutral Scale:**
- Gray-50 to Gray-900
- Used for text, borders, backgrounds
- Ensures contrast ratios

### Color Contrast Standards

**WCAG 2.1 AA Requirements:**
- Normal text (16px+): 4.5:1 contrast ratio
- Large text (24px+): 3:1 contrast ratio
- UI components: 3:1 contrast ratio

**Contrast Testing:**
```
Foreground: #333333 (text)
Background: #FFFFFF (white)
Ratio: 12.6:1 (AAA compliant)

Foreground: #757575 (gray text)
Background: #FFFFFF
Ratio: 4.6:1 (AA compliant)
```

## Typography System

### Type Scale

**Modular Scale (1.250 ratio):**
```
font-size-xs: 0.64rem (10px)
font-size-sm: 0.8rem (13px)
font-size-base: 1rem (16px)
font-size-lg: 1.25rem (20px)
font-size-xl: 1.563rem (25px)
font-size-2xl: 1.953rem (31px)
font-size-3xl: 2.441rem (39px)
```

**Line Height Scale:**
```
line-height-tight: 1.25 (headings)
line-height-normal: 1.5 (body text)
line-height-relaxed: 1.75 (long-form content)
```

**Font Weight Scale:**
```
font-weight-light: 300
font-weight-normal: 400
font-weight-medium: 500
font-weight-semibold: 600
font-weight-bold: 700
```

### Typography Hierarchy

**Heading Levels:**
```
h1: 3xl / tight / bold
h2: 2xl / tight / bold
h3: xl / tight / semibold
h4: lg / normal / semibold
h5: base / normal / semibold
h6: sm / normal / semibold
```

**Body Text:**
```
body-lg: lg / relaxed / normal
body: base / normal / normal
body-sm: sm / normal / normal
caption: xs / normal / normal
```

### Web Font Loading

**Font Display Strategy:**
```css
@font-face {
  font-family: 'Inter';
  font-display: swap; /* Show fallback immediately */
  src: url('/fonts/inter.woff2') format('woff2');
}
```

**Performance Tips:**
- Use variable fonts (single file, multiple weights)
- Subset fonts (remove unused characters)
- Preload critical fonts
- Limit font weights (3-4 max)

## Spacing System

### 8pt Grid System

**Base Unit:** 8px

**Spacing Scale:**
```
space-0: 0px
space-1: 4px (0.5× base)
space-2: 8px (1× base)
space-3: 12px (1.5× base)
space-4: 16px (2× base)
space-5: 20px (2.5× base)
space-6: 24px (3× base)
space-8: 32px (4× base)
space-10: 40px (5× base)
space-12: 48px (6× base)
space-16: 64px (8× base)
space-20: 80px (10× base)
```

**Usage Guidelines:**
- Component padding: 12px, 16px, 24px
- Element spacing: 8px, 16px, 32px
- Section spacing: 48px, 64px, 80px

### Responsive Spacing

**Scale by Breakpoint:**
```
mobile: space-4 (16px)
tablet: space-6 (24px)
desktop: space-8 (32px)

Example:
margin-top: var(--space-4);
@media (min-width: 768px) {
  margin-top: var(--space-6);
}
```

## Component Architecture

### Component Library Structure

```
components/
├── primitives/          # Atomic components
│   ├── Button
│   ├── Input
│   ├── Checkbox
│   └── Radio
├── patterns/            # Composite components
│   ├── FormGroup
│   ├── Card
│   ├── Modal
│   └── Dropdown
└── layouts/             # Layout components
    ├── Container
    ├── Grid
    └── Stack
```

### Component Variants

**Size Variants:**
```
button-sm: 32px height
button-md: 40px height (default)
button-lg: 48px height
```

**Style Variants:**
```
button-primary: Brand color, solid
button-secondary: Gray, solid
button-outline: Transparent, bordered
button-ghost: Transparent, no border
button-link: Text only
```

**State Variants:**
```
default
hover
active (pressed)
focus
disabled
loading
```

### Component API Design

**Props Pattern:**
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: ReactNode;
  children: ReactNode;
  onClick?: () => void;
}
```

## Responsive Design System

### Breakpoint System

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
.container {
  padding: 16px;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 24px;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
  }
}
```

### Grid System

**12-Column Grid:**
```
col-1: 8.333%
col-2: 16.666%
col-3: 25%
col-4: 33.333%
col-6: 50%
col-12: 100%
```

**Responsive Columns:**
```
<div class="col-12 md:col-6 lg:col-4">
  <!-- Full width on mobile -->
  <!-- Half width on tablet -->
  <!-- Third width on desktop -->
</div>
```

## Accessibility Standards

### WCAG 2.1 AA Compliance

**Color Contrast:**
- Normal text: 4.5:1 minimum
- Large text: 3:1 minimum
- UI components: 3:1 minimum

**Focus Indicators:**
```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

**Keyboard Navigation:**
- Tab order follows visual order
- All interactive elements focusable
- Skip links for navigation
- Escape key closes modals

**Screen Reader Support:**
```html
<button aria-label="Close dialog">
  <svg aria-hidden="true">...</svg>
</button>

<div role="alert" aria-live="polite">
  Form submitted successfully
</div>
```

### Semantic HTML

**Correct Element Usage:**
```html
<!-- Good -->
<button onClick={handleClick}>Submit</button>
<nav>...</nav>
<main>...</main>

<!-- Bad -->
<div onClick={handleClick}>Submit</div>
<div class="nav">...</div>
<div class="content">...</div>
```

## Design System Governance

### Version Control

**Semantic Versioning:**
```
Major.Minor.Patch

1.0.0: Initial release
1.1.0: New component (minor)
1.1.1: Bug fix (patch)
2.0.0: Breaking change (major)
```

**Change Log:**
```markdown
## [1.2.0] - 2025-11-08

### Added
- New `Toast` notification component
- Dark mode support for all components

### Changed
- Updated button padding from 12px to 16px
- Improved focus states for better accessibility

### Fixed
- Modal scroll lock on iOS
- Input border color in dark mode
```

### Documentation Standards

**Component Documentation:**
```markdown
# Button Component

## Usage
[Code example]

## Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | string | 'primary' | Button style variant |
| size | string | 'md' | Button size |

## Examples
[Visual examples with code]

## Accessibility
- Uses semantic `<button>` element
- Includes focus visible styles
- Supports keyboard navigation

## Guidelines
- Use primary for main actions
- Use secondary for alternative actions
- Avoid more than 2 buttons per screen section
```

### Design Tokens Distribution

**Format Options:**
- JSON (for JavaScript/TypeScript)
- CSS Custom Properties (for web)
- SCSS Variables (for Sass)
- iOS/Android (for native mobile)

**JSON Format:**
```json
{
  "color": {
    "primary": {
      "500": "#0066CC"
    }
  },
  "spacing": {
    "4": "16px"
  }
}
```

**CSS Custom Properties:**
```css
:root {
  --color-primary-500: #0066CC;
  --spacing-4: 16px;
}
```

---

**Last Updated:** 2025-11-08
**Related Files:**
- [templates.md](templates.md) - Component templates and examples
- [tools.md](tools.md) - design_token_generator.py documentation
