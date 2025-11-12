# UX Research & Design Frameworks

Comprehensive frameworks for user research, persona development, and design validation.

## User Research Methods

### Qualitative Research

**User Interviews:**
- Semi-structured format
- 30-45 minutes per session
- 5-8 interviews per cohort
- Focus on "why" not "what"

**Usability Testing:**
- Task-based scenarios
- Think-aloud protocol
- 5 users uncover 85% of issues
- Remote or in-person

**Field Studies:**
- Contextual inquiry
- Observe in natural environment
- Identify workarounds
- Understand workflows

### Quantitative Research

**Surveys:**
- Large sample sizes (100+ responses)
- Multiple choice and scales
- Statistical analysis
- Validate qualitative findings

**Analytics:**
- Behavioral data
- Funnel analysis
- Heatmaps and session recordings
- A/B testing results

**Metrics:**
- Task completion rate
- Time on task
- Error rate
- Satisfaction scores (SUS, CSAT)

## Persona Development Framework

### Jobs-to-be-Done (JTBD)

**Framework:**
```
When [situation]
I want to [motivation]
So I can [expected outcome]
```

**Example:**
```
When I'm tracking project progress
I want to see all tasks in one view
So I can identify bottlenecks quickly
```

### Persona Components

**Demographics:**
- Age, role, company size
- Technical proficiency
- Industry/vertical

**Psychographics:**
- Goals and motivations
- Pain points and frustrations
- Behaviors and patterns
- Preferences and values

**Scenarios:**
- Typical use cases
- Edge cases
- Success criteria

### Persona Validation

**Criteria:**
- Based on real user data (not assumptions)
- Represent significant user segments
- Actionable for design decisions
- Updated quarterly with new research

## Journey Mapping

### Customer Journey Stages

1. **Awareness:** User learns about product
2. **Consideration:** Evaluating alternatives
3. **Purchase:** Decision to buy/signup
4. **Onboarding:** First-time experience
5. **Usage:** Regular product use
6. **Advocacy:** Recommend to others

### Journey Map Components

**For Each Stage:**
- User actions
- Touchpoints
- Emotions (frustrated → delighted)
- Pain points
- Opportunities for improvement

**Example:**
```
Stage: Onboarding
Actions: Create account → verify email → setup profile
Touchpoints: Signup form, email, dashboard
Emotions: 😊 Excited → 😐 Confused → 😟 Frustrated
Pain Points: Too many required fields, unclear next steps
Opportunities: Reduce form fields, add progress indicator
```

## Usability Testing Framework

### Test Planning

**Define:**
- Research questions
- Success metrics
- Participant criteria
- Task scenarios

**Recruit:**
- 5-8 participants per round
- Screen for target persona
- Compensate appropriately

### Test Execution

**Script:**
1. Introduction (5 min)
2. Background questions (5 min)
3. Task scenarios (25 min)
4. Post-task questions (10 min)
5. Wrap-up (5 min)

**Facilitation:**
- Neutral tone, no leading questions
- Think-aloud protocol
- Observe, don't interrupt
- Note pain points and delights

### Analysis

**Severity Rating:**
- **Critical:** Prevents task completion
- **High:** Causes significant frustration
- **Medium:** Minor inconvenience
- **Low:** Cosmetic issue

**Prioritization:**
- Frequency × Severity = Priority
- Quick wins vs long-term fixes

## Accessibility Framework

### WCAG 2.1 Principles

**POUR:**
- **Perceivable:** Can users perceive the content?
- **Operable:** Can users operate the interface?
- **Understandable:** Can users understand the content and interface?
- **Robust:** Can content be interpreted reliably?

### Accessibility Checklist

**Visual:**
- [ ] Color contrast ratios meet WCAG AA (4.5:1 text, 3:1 UI)
- [ ] Don't rely on color alone to convey information
- [ ] Text is resizable up to 200%
- [ ] Content is readable in high contrast mode

**Keyboard:**
- [ ] All functionality available via keyboard
- [ ] Focus indicator is visible
- [ ] Tab order is logical
- [ ] No keyboard traps

**Screen Reader:**
- [ ] Semantic HTML used correctly
- [ ] Images have alt text
- [ ] Forms have labels
- [ ] ARIA attributes used appropriately

**Cognitive:**
- [ ] Consistent navigation
- [ ] Clear error messages
- [ ] Sufficient time to complete tasks
- [ ] Help is available

## Design Validation Methods

### Prototype Testing

**Fidelity Levels:**
- **Low-Fi:** Paper sketches, wireframes
- **Mid-Fi:** Clickable prototypes (Figma, Sketch)
- **High-Fi:** Interactive prototypes with real data

**When to Use:**
- Low-Fi: Early concept validation
- Mid-Fi: Flow and interaction testing
- High-Fi: Final validation before development

### A/B Testing

**Framework:**
```
Hypothesis: Changing [element] will [impact] because [reason]
Metric: [Primary success metric]
Sample Size: [Calculated for statistical significance]
Duration: [Run until significance reached]
```

**Example:**
```
Hypothesis: Adding social proof will increase signups because users trust peer recommendations
Metric: Signup conversion rate
Sample Size: 1,000 per variant
Duration: 2 weeks or significance
```

### Design Critique Framework

**Structure:**
1. **Context:** What problem are we solving?
2. **Constraints:** Time, technical, business limitations
3. **Design:** Walk through the design
4. **Feedback:** Structured critique
5. **Next Steps:** Action items

**Feedback Types:**
- **I like:** Positive reinforcement
- **I wish:** Constructive suggestions
- **I wonder:** Open questions

---

**Last Updated:** 2025-11-08
**Related Files:**
- [templates.md](templates.md) - Research scripts and persona templates
- [tools.md](tools.md) - persona_generator.py documentation
