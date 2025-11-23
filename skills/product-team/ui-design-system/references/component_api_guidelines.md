# Component API Guidelines Reference Guide

## Overview
Best practices and standards for designing component APIs (props, events, slots) that are flexible, intuitive, and maintainable in modern component-based UI frameworks (React, Vue, Svelte).

## API Design Principles

### 1. Simplicity
**Principle:** Simple things should be simple

**Example:**
```jsx
// Good: Simple use case is simple
<Button>Click me</Button>

// Bad: Requires configuration for basic use
<Button config={{ label: "Click me", type: "button" }} />
```

### 2. Discoverability
**Principle:** API should be self-documenting via TypeScript or clear naming

**Example:**
```typescript
// Good: Clear prop names, TypeScript autocomplete
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
}

// Bad: Unclear, inconsistent naming
interface ButtonProps {
  type?: string;  // What types are valid?
  sz?: string;    // Abbreviation unclear
  isDisabled?: boolean;  // Inconsistent 'is' prefix
}
```

### 3. Consistency
**Principle:** Similar components use similar prop names

**Example:**
```jsx
// Good: Consistent across components
<Button size="large" variant="primary" />
<Input size="large" variant="outlined" />
<Select size="large" variant="outlined" />

// Bad: Inconsistent naming
<Button size="large" type="primary" />
<Input inputSize="lg" style="outlined" />
<Select selectSize="LARGE" kind="outlined" />
```

## Prop Patterns

### Boolean Props
**Convention:** Use positive names, default to false

**Example:**
```jsx
// Good
<Button disabled />           // Clear: button is disabled
<Modal open />                // Clear: modal is open

// Bad
<Button notEnabled />         // Double negative confusing
<Modal closed={false} />      // Hard to reason about
```

### Variant Props
**Convention:** Use string unions for predefined options

**Example:**
```tsx
type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost';

<Button variant="primary">Save</Button>
<Button variant="danger">Delete</Button>
```

### Size Props
**Convention:** Standard sizes across components

**Example:**
```tsx
type Size = 'small' | 'medium' | 'large';

<Button size="small" />
<Input size="medium" />
<Avatar size="large" />
```

### Controlled vs Uncontrolled
**Pattern:** Support both modes

**Example:**
```jsx
// Uncontrolled (internal state)
<Input defaultValue="hello" />

// Controlled (external state)
const [value, setValue] = useState('');
<Input value={value} onChange={(e) => setValue(e.target.value)} />
```

## Event Handling

### Naming Convention
**Pattern:** `on[Event]` for callbacks

**Example:**
```tsx
<Button onClick={() => {}} />           // Click event
<Input onChange={(e) => {}} />          // Change event
<Modal onClose={() => {}} />            // Close event
<Form onSubmit={(data) => {}} />        // Submit event
```

### Event Payload
**Pattern:** Pass meaningful data, not raw events when possible

**Example:**
```tsx
// Good: Meaningful data
<Input onChange={(value: string) => {}} />
<DatePicker onSelect={(date: Date) => {}} />

// Less good: Raw event (forces consumer to extract value)
<Input onChange={(e: ChangeEvent) => {
  const value = e.target.value;  // Consumer has to do this
}} />
```

## Composition Patterns

### Children Prop
**Pattern:** Use for flexible content

**Example:**
```jsx
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content goes here</CardBody>
  <CardFooter><Button>Action</Button></CardFooter>
</Card>
```

### Render Props
**Pattern:** For custom rendering logic

**Example:**
```jsx
<DataTable
  data={users}
  renderRow={(user) => (
    <tr key={user.id}>
      <td>{user.name}</td>
      <td>{user.email}</td>
    </tr>
  )}
/>
```

### Slots (Vue/Svelte)
**Pattern:** Named slots for specific content areas

**Example:**
```vue
<Modal>
  <template #header>
    <h2>Confirm Delete</h2>
  </template>
  <template #body>
    <p>Are you sure?</p>
  </template>
  <template #footer>
    <Button @click="confirm">Yes</Button>
    <Button @click="cancel">No</Button>
  </template>
</Modal>
```

## Accessibility API

### Required Accessibility Props
```tsx
interface AccessibleButtonProps {
  'aria-label'?: string;        // For icon-only buttons
  'aria-describedby'?: string;  // For tooltips/help text
  'aria-pressed'?: boolean;     // For toggle buttons
  disabled?: boolean;           // Native disabled state
}

// Usage
<Button aria-label="Close dialog" />  // Icon button
<Button aria-describedby="help-text">Submit</Button>
```

### Keyboard Navigation
**Requirements:**
- All interactive components support Tab key
- Enter/Space triggers primary action
- Escape closes modals/dropdowns
- Arrow keys navigate lists/menus

## TypeScript Best Practices

### Strict Prop Types
```typescript
// Good: Specific types
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size: 'small' | 'medium' | 'large';
  disabled?: boolean;
  onClick?: () => void;
}

// Bad: Too permissive
interface ButtonProps {
  variant?: string;
  size?: any;
  props?: Record<string, unknown>;
}
```

### Generic Components
```typescript
// DataTable with generic item type
interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  renderRow: (item: T) => React.ReactNode;
}

function DataTable<T>({ data, columns, renderRow }: DataTableProps<T>) {
  // Implementation
}
```

## Documentation Standards

### Component README Template
```markdown
# Button Component

## Usage
\`\`\`jsx
<Button variant="primary" size="medium">
  Click me
</Button>
\`\`\`

## Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' \| 'danger' | 'primary' | Button style variant |
| size | 'small' \| 'medium' \| 'large' | 'medium' | Button size |
| disabled | boolean | false | Disables button interaction |
| onClick | () => void | - | Click event handler |

## Accessibility
- Uses semantic `<button>` element
- Supports keyboard navigation (Enter/Space)
- Includes focus styles for keyboard users
- Respects prefers-reduced-motion for animations

## Examples
[Link to Storybook]
\`\`\`

## Resources
- TypeScript component templates
- Accessibility checklist
- Component API documentation generator
- Storybook setup guide

---
**Last Updated:** November 23, 2025
**Related:** design_system_principles.md, design_token_standards.md
