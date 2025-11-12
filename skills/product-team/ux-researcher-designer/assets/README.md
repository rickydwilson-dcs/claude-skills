# UX Researcher & Designer - Sample Assets

This directory contains sample user research data for persona generation and user insights analysis.

## Sample Files

### 1. sample-user-research.json
**Purpose:** User research data for data-driven persona generation

**Description:** Realistic research dataset from 45 users including:
- 4 detailed user profiles spanning different segments
- Usage patterns and frequency data
- Feature adoption analytics
- Satisfaction metrics (NPS, feature ratings)
- User segments (power users, business users, executives)
- Psychographic and behavioral data

**Data Structure:**
- `research_metadata`: Study context and methodology
- `users`: Individual user profiles with demographics and behavior
- `usage_patterns`: Aggregate usage insights
- `satisfaction_metrics`: Overall satisfaction and feature ratings
- `segment_insights`: Grouped analysis by user type

**How to Use:**
```bash
# Generate personas from research data
python ../scripts/persona_generator.py

# Load sample data for reference
cat sample-user-research.json | python -m json.tool
```

**What to Expect:**
- 3-5 distinct personas extracted from data patterns
- Archetype identification (power user, casual user, business user, etc.)
- Psychographic profiles (goals, frustrations, motivations)
- User scenarios for each persona
- Design implications and recommendations

---

## Using This Sample

### Quick Start

```bash
cd /Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My\ Drive/Websites/GitHub/claude-skills/product-team/ux-researcher-designer/

# Generate personas from sample research
python scripts/persona_generator.py

# Interactive mode for building custom personas
python scripts/persona_generator.py --interactive

# Export as JSON for Figma/Miro
python scripts/persona_generator.py --output json --file personas.json
```

---

## Understanding Personas

### Persona Components

**Archetype:** User category
- Power User: Advanced, frequent usage
- Casual User: Occasional, basic needs
- Business User: Professional context, ROI-focused
- Mobile First: Primarily mobile, on-the-go

**Demographics:**
- Age, location, occupation
- Income bracket, education
- Company size and industry

**Psychographics:**
- Goals and aspirations
- Frustrations and pain points
- Values and beliefs
- Motivations and drivers

**Behaviors:**
- Usage frequency (daily/weekly/monthly)
- Preferred devices and platforms
- Feature usage patterns
- Purchase decision process

### Persona Profile Template

```json
{
  "name": "Jane - Efficient Product Manager",
  "archetype": "business_user",
  "age": 28,
  "occupation": "Product Manager",
  "experience_level": "3-5 years",
  "goals": [
    "Make data-driven decisions quickly",
    "Communicate insights to executives",
    "Track metrics consistently"
  ],
  "frustrations": [
    "Manual report creation (3+ hours/month)",
    "Inconsistent data across tools",
    "Difficulty collaborating with team"
  ],
  "tech_savviness": "medium",
  "devices": ["laptop", "tablet"],
  "usage_frequency": "several_times_weekly",
  "budget_authority": "high",
  "decision_criteria": ["Ease of use", "Team collaboration", "Executive reporting"]
}
```

---

## Research Data Collection

### What to Measure

**Demographic Data:**
- Age, location, job title
- Company size and industry
- Years of experience
- Income/budget authority

**Behavioral Data:**
- Usage frequency (daily/weekly/monthly)
- Time spent per session
- Features used most/least
- Devices used
- When/where they use product

**Psychographic Data:**
- Goals with your product
- Pain points in current workflow
- What they like most
- What they wish they could do
- How they measure success

**Satisfaction Data:**
- NPS score (0-10)
- Feature satisfaction (1-5 scale)
- Likelihood to recommend
- Main reason for satisfaction/dissatisfaction

### Research Methodology

**Quantitative:**
- User surveys (50-200 responses)
- Usage analytics (page views, feature usage)
- Satisfaction metrics (NPS, CSAT)

**Qualitative:**
- User interviews (15-30 participants)
- Contextual inquiry (observe in real environment)
- User testing (watch them complete tasks)

**Recommended Approach:**
- 30-50 surveys for large companies
- 8-12 in-depth interviews
- 5-10 user testing sessions
- Ongoing analytics monitoring

---

## Creating Personas from Data

### Process

**Step 1: Collect Data**
```bash
# Run surveys and interviews
# Track analytics
# Gather feedback
```

**Step 2: Identify Patterns**
- Group users by similar characteristics
- Look for behavior clusters
- Find common pain points
- Identify distinct needs

**Step 3: Create Profiles**
```json
{
  "segment": "power_users",
  "size_percent": 20,
  "characteristics": [
    "Tech-savvy",
    "Frequent usage (daily)",
    "Explore advanced features"
  ]
}
```

**Step 4: Validate**
- Do profiles match your actual users?
- Can you find real examples?
- Do characteristics explain behaviors?

**Step 5: Use in Design**
- Create scenarios for each persona
- Design flows for different personas
- Test with representative users
- Track which personas grow/shrink

---

## Segment Analysis

### Typical User Segments

**Power Users (15-25%)**
- Characteristics: Tech-savvy, explore features, daily usage
- Primary Needs: Advanced options, customization, automation
- Frustrations: Limited customization, lack of shortcuts
- Design Focus: Expert paths, keyboard shortcuts, APIs

**Business Users (50-65%)**
- Characteristics: Task-focused, occasional usage, ROI-driven
- Primary Needs: Pre-built workflows, simplicity, business metrics
- Frustrations: Too many options, hard to demonstrate value
- Design Focus: Templates, reporting, easy setup

**Executives (5-15%)**
- Characteristics: Infrequent use, expects to "just work"
- Primary Needs: Executive dashboards, accuracy, compliance
- Frustrations: Complexity, dependency on others
- Design Focus: Dashboards, delegation, permissions

---

## Designing with Personas

### User Scenarios

Create specific scenarios for each persona:

```
Scenario: Jane (Product Manager) wants to create monthly report

Current State:
- 3 hours to manually compile data
- Copy/paste between tools
- Risk of errors

Desired State:
- Scheduled automated report
- Sent to stakeholders monthly
- Consistent, accurate format
```

### Feature Prioritization

Use personas to prioritize:

```
Feature: Export to PowerPoint

Power Users: "Nice to have" (they code their own exports)
Business Users: "Important" (key for executive sharing)
Executives: "Critical" (only way they consume reports)

Priority: HIGH (serves majority + important for business users)
```

### Testing & Validation

```
Usability Test with 5 Users:
- 2 Power Users
- 2 Business Users
- 1 Executive

Measure:
- Task completion rate by persona
- Time to complete
- Confidence level
- Follow-up questions
```

---

## Persona Updates

### When to Revisit Personas

- Quarterly with new user research
- After major feature launches
- When NPS or satisfaction changes
- If user mix shifts significantly
- When entering new market segments

### Tracking Changes

```
Q1 2025 Personas:
- 70% Business Users
- 20% Power Users
- 10% Executives

Q2 2025 Update (New Market):
- 50% Business Users
- 25% Power Users
- 15% Mobile First
- 10% Executives
```

---

## Design Implications

### Creating Actionable Personas

**Not Just Description, But Direction:**

```
❌ Generic: "Sarah is a product manager who uses dashboards"

✓ Actionable: "Sarah (Product Manager) needs to create executive
reports in <30 minutes. She's not technical and needs templates.
Design implication: Pre-built templates + export to PowerPoint"
```

### Design Principles by Persona

**For Power Users:**
- Advanced features easily accessible
- Keyboard shortcuts and APIs
- Customization and automation
- Professional tone

**For Business Users:**
- Wizards and guided workflows
- Pre-built templates
- Clear ROI metrics
- Helpful tooltips and onboarding

**For Executives:**
- Executive dashboards
- One-click insights
- Mobile-friendly summaries
- Delegation/approval workflows

---

## Creating Your Own Research File

### JSON Structure

```json
{
  "research_metadata": {
    "study_name": "Your Study Name",
    "date_conducted": "2025-10-01",
    "sample_size": 45,
    "methodology": ["surveys", "interviews", "analytics"]
  },
  "users": [
    {
      "user_id": "U001",
      "age": 32,
      "occupation": "Software Engineer",
      "usage_frequency": "daily",
      "features_used": ["feature1", "feature2"],
      "preferred_devices": ["laptop", "desktop"],
      "tech_savviness": "high",
      "goals": ["Goal 1", "Goal 2"],
      "frustrations": ["Frustration 1", "Frustration 2"],
      "nps_score": 8
    }
  ]
}
```

### Data Collection Tips

1. **Representative Sample**
   - Include mix of user types
   - Cover different industries/sizes
   - Get both new and long-term users

2. **Consistent Metrics**
   - Define "usage_frequency" levels
   - Use consistent satisfaction scales
   - Standardize job titles

3. **Rich Descriptions**
   - Quote actual users
   - Include specific examples
   - Capture real pain points

4. **Recent Data**
   - Conduct research last 3 months
   - Track changes quarterly
   - Don't rely on 1-year-old data

---

## Best Practices

1. **Avoid Stereotypes**: Make personas based on data, not assumptions
2. **Include Quotes**: Use actual user words to bring personas to life
3. **Update Regularly**: Personas drift; refresh quarterly
4. **Share Widely**: Post in Figma, Slack, wiki for team access
5. **Use in Decisions**: Reference in design reviews and prioritization
6. **Test with Personas**: Run usability tests with representative users

---

## Tools & Integration

### Figma
- Import persona data into design files
- Use as reference during design
- Share mockups mapped to personas

### Jira/Linear
- Tag features by persona benefit
- Filter roadmap by persona alignment
- Track persona-specific metrics

### Confluence/Notion
- Create persona wiki pages
- Update as research evolves
- Team reference during meetings

---

## File Specifications

**sample-user-research.json:**
- Format: JSON
- Encoding: UTF-8
- Required Fields: research_metadata, users
- Optional Fields: usage_patterns, satisfaction_metrics, segment_insights
- Size: ~20-50KB for typical 50-user study

---

## Related Documentation

- **Persona Generator:** [../scripts/persona_generator.py](../scripts/persona_generator.py)
- **UX Research Guide:** [../SKILL.md](../SKILL.md)
- **User Research Best Practices:** [../references/](../references/)

---

**Last Updated:** November 5, 2025
**Format:** Sample Assets README
**Included Files:** 1 (sample-user-research.json with 4 detailed users + aggregate data)
**Script Version:** persona_generator.py 1.0.0
