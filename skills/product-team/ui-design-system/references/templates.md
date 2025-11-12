# UI Design System Templates

Component templates, documentation formats, and design guidelines.

## Component Documentation Template

```markdown
# [Component Name]

## Overview
[Brief description of component purpose and usage]

## Anatomy
[Visual breakdown of component parts]

## Usage

### Basic Example
` ``jsx
<ComponentName>
  Content
</ComponentName>
```

### With Props
```jsx
<ComponentName
  variant="primary"
  size="md"
  disabled={false}
>
  Content
</ComponentName>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | string | 'default' | Visual style variant |
| size | string | 'md' | Component size |
| disabled | boolean | false | Disabled state |

## Variants

### Primary
[Description and visual example]

### Secondary
[Description and visual example]

## Accessibility

- **Keyboard:** [Keyboard interaction details]
- **Screen Reader:** [ARIA attributes and labels]
- **Focus:** [Focus management approach]

## Best Practices

### Do
- [Good practice 1]
- [Good practice 2]

### Don't
- [Anti-pattern 1]
- [Anti-pattern 2]

## Related Components
- [Related component 1]
- [Related component 2]
```

## Design Token Documentation

```markdown
# Design Tokens

## Color Palette

### Primary
- **50:** `#E6F2FF` - Lightest tint
- **500:** `#0066CC` - Brand color
- **900:** `#002952` - Darkest shade

### Usage
- 50-200: Backgrounds, hover states
- 400-600: Primary UI elements
- 700-900: Text, emphasis

## Typography Scale

| Token | Size | Usage |
|-------|------|-------|
| xs | 12px | Captions, labels |
| sm | 14px | Small text |
| base | 16px | Body text |
| lg | 18px | Subheadings |
| xl | 20px | Headings |

## Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| 1 | 4px | Tight spacing |
| 2 | 8px | Default gap |
| 4 | 16px | Component padding |
| 6 | 24px | Section spacing |
```

## Component Checklist

```markdown
# Component Readiness Checklist

## Design
- [ ] Figma designs complete
- [ ] All variants designed
- [ ] Responsive behavior defined
- [ ] Dark mode designs ready
- [ ] Accessibility annotations added

## Development
- [ ] Component implemented
- [ ] Props API defined
- [ ] TypeScript types added
- [ ] Unit tests written
- [ ] Visual regression tests added

## Documentation
- [ ] Usage guidelines written
- [ ] Code examples added
- [ ] Props table complete
- [ ] Accessibility notes added
- [ ] Storybook stories created

## Quality
- [ ] WCAG 2.1 AA compliant
- [ ] Keyboard navigation working
- [ ] Screen reader tested
- [ ] Cross-browser tested
- [ ] Performance optimized
```

---

**Last Updated:** 2025-11-08
**Related Files:**
- [frameworks.md](frameworks.md) - Design system architecture
- [tools.md](tools.md) - Design token generator documentation
