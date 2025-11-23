# Agile User Story Framework Reference Guide

## Overview
Comprehensive framework for writing, refining, and managing user stories in agile development. Covers INVEST criteria, acceptance criteria, story mapping, and best practices for product owners.

## User Story Fundamentals

### Standard Format
```
As a [user type/persona]
I want [goal/desire]
So that [benefit/value]
```

**Example:**
```
As a project manager
I want to export project reports to PDF
So that I can share updates with executives who prefer printed documents
```

### INVEST Criteria (Detailed)

**Independent:** Stories should stand alone
- Can be completed without depending on other stories
- Can be delivered in any order
- Enables flexible sprint planning

**Negotiable:** Details are flexible
- Story describes what, not how (implementation)
- Technical approach determined by development team
- Allows for creative solutions

**Valuable:** Delivers user/business value
- User can see the benefit
- Connects to business objectives
- Not purely technical/architectural

**Estimable:** Team can size it
- Clear enough to estimate effort
- Team understands requirements
- Known technology/approach

**Small:** Fits in one sprint
- 1-5 story points typical
- 8+ points needs breakdown
- Completable in 1-3 days

**Testable:** Has clear acceptance criteria
- Can verify completion objectively
- Acceptance tests can be written
- "Done" is unambiguous

## Acceptance Criteria

### Given-When-Then Format (Gherkin)

**Template:**
```
Given [precondition/context]
When [action/event]
Then [expected outcome]
```

**Example:**
```
Story: Export project report to PDF

Acceptance Criteria:
- Given I'm viewing a project report
  When I click "Export to PDF"
  Then a PDF file downloads with current report data

- Given the report has charts and tables
  When I export to PDF
  Then charts and tables render correctly in PDF format

- Given I export a report
  When I check the file size
  Then it's under 10MB for typical reports

- Given I'm on mobile
  When I try to export
  Then I see a message "Export available on desktop only"
```

### Checklist Format (Alternative)

**When to use:** Simple stories, internal features

**Example:**
```
Story: Add dark mode toggle

Acceptance Criteria:
- [ ] Toggle appears in user settings
- [ ] Clicking toggle switches between light and dark mode
- [ ] Dark mode persists across sessions
- [ ] All pages support dark mode
- [ ] Sufficient color contrast for accessibility (WCAG AA)
```

## Story Mapping

### Purpose
Visualize product backlog as a user journey to prioritize and plan releases

### Structure
```
                    User Activities (Epic Level)
                    ↓
          [Discover] [Evaluate] [Purchase] [Use] [Support]
             ↓          ↓          ↓        ↓       ↓
           User Tasks (Feature Level)
             ↓          ↓          ↓        ↓       ↓
          User Stories (Story Level)
───────────────────────────────────────────────────────────
Release 1:   [MVP stories - must-have]
Release 2:   [Enhanced stories - should-have]
Release 3:   [Nice-to-have stories]
```

### Example: E-commerce Checkout
```
Activities:   [Browse] → [Add to Cart] → [Checkout] → [Confirm]

MVP (Release 1):
- Browse: View product list, search, filters
- Cart: Add to cart, view cart, update quantity
- Checkout: Enter payment, submit order
- Confirm: Order confirmation email

Release 2:
- Browse: Product recommendations
- Cart: Save for later
- Checkout: Apply promo code, gift wrapping
- Confirm: Track shipment

Release 3:
- Browse: Virtual try-on
- Cart: Share cart with friend
- Checkout: One-click checkout
- Confirm: Order history and re-order
```

## Story Sizing

### Story Points (Fibonacci Scale)
```
1 point:   Trivial (2-4 hours, minimal complexity)
2 points:  Simple (4-8 hours, straightforward)
3 points:  Moderate (1 day, some complexity)
5 points:  Complex (2-3 days, multiple components)
8 points:  Very complex (3-5 days, high uncertainty)
13 points: Too large - needs breakdown
```

### T-Shirt Sizing (Alternative)
- XS: 1 point
- S: 2-3 points
- M: 5 points
- L: 8 points
- XL: 13+ points (split before sprint)

## Story Splitting Techniques

### 1. By Workflow Steps
**Original:** "User can manage their profile"
**Split:**
- User can view their profile
- User can edit their profile
- User can upload profile photo
- User can change password

### 2. By CRUD Operations
**Original:** "Admin can manage users"
**Split:**
- Admin can create new users
- Admin can view user list
- Admin can edit user details
- Admin can delete users

### 3. By Happy Path vs Edge Cases
**Original:** "User can complete checkout"
**Split:**
- User can checkout with valid payment (happy path)
- User sees error for declined card (edge case)
- User can checkout as guest (alternative path)
- User can save payment method (enhancement)

### 4. By Simple vs Complex
**Original:** "Search products with filters"
**Split:**
- Basic text search (simple)
- Filter by category (simple)
- Filter by price range (simple)
- Filter by multiple attributes + sorting (complex)

### 5. By Data Variations
**Original:** "Import customer data"
**Split:**
- Import CSV files
- Import Excel files
- Import from API
- Handle duplicate records

## Backlog Refinement

### Refinement Cycle
```
New Idea → Rough Story → Refined Story → Sprint-Ready → In Sprint
  ↓           ↓              ↓              ↓            ↓
(Backlog)  (1 week)      (2-3 weeks)    (1-2 weeks)  (Active)
```

### Definition of Ready Checklist
- [ ] Story follows INVEST criteria
- [ ] Acceptance criteria defined (Given-When-Then)
- [ ] Story estimated by team (planning poker)
- [ ] Dependencies identified
- [ ] UX/design assets available (if needed)
- [ ] Technical approach discussed
- [ ] No major unknowns or blockers

## Epic Structure

### Epic Hierarchy
```
Theme: Improve User Engagement
  ↓
Epic: Personalized Dashboard
  ↓
Feature: Customizable Widgets
  ↓
Stories:
- User can add widgets to dashboard
- User can remove widgets from dashboard
- User can rearrange widgets by drag-and-drop
- User can resize widgets
```

### Epic Template
```
Epic Title: [Name]
Goal: [Business objective]
User Persona: [Who benefits]
Success Metrics: [How to measure]

User Stories (High-level):
1. [Story 1]
2. [Story 2]
3. [Story 3]

Out of Scope:
- [What's not included]

Dependencies:
- [Other epics, teams, systems]
```

## Resources
- Story mapping tools: Miro, Mural, StoriesOnBoard
- Story templates: Jira, Linear, Shortcut
- Planning poker: PlanITPoker, Scrum Poker Online

---
**Last Updated:** November 23, 2025
**Related:** frameworks.md, templates.md, tools.md
