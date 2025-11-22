---
name: skill-name
description: One-line description of what this skill provides (used in search, catalogs, and agent integration). Keep under 200 characters. Include primary use cases and key capabilities.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: domain-category
  domain: domain-name
  updated: YYYY-MM-DD
  keywords:
    - keyword1
    - keyword2
    - keyword3
    - keyword4
    - keyword5
  tech-stack:
    - Technology 1
    - Technology 2
    - Technology 3
  python-tools:
    - tool1.py
    - tool2.py
---

<!--
  INSTRUCTIONS FOR USING THIS TEMPLATE:

  1. Replace "skill-name" with your skill folder name (kebab-case, no cs- prefix)
  2. Replace "Skill Name" below with the display name (Title Case)
  3. Update all YAML frontmatter fields above
  4. Fill in all sections following the structure
  5. Create Python tools in scripts/ directory
  6. Add reference guides to references/ directory
  7. Add user templates to assets/ directory
  8. Test all commands and examples before committing

  EXAMPLES OF COMPLETED SKILLS:
  - skills/marketing-team/content-creator/SKILL.md
  - skills/engineering-team/senior-architect/SKILL.md
  - skills/product-team/business-analyst-toolkit/SKILL.md
  - skills/delivery-team/jira-expert/SKILL.md

  YAML FRONTMATTER GUIDELINES:
  - name: Match folder name exactly (kebab-case)
  - description: 150-200 chars, include use cases and keywords for search
  - keywords: 5-30 keywords (for search and categorization)
  - tech-stack: List all technologies/languages/frameworks
  - python-tools: List all .py files in scripts/ directory
-->

# Skill Name

<!--
  One-line tagline (20-50 words) describing the skill's core value proposition.
  Example: "Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks for creating high-quality marketing content."
-->

[One-line tagline describing core value proposition]

## Overview

<!--
  Write 2-3 paragraphs describing:
  - What this skill provides (tools, frameworks, templates)
  - Who should use this skill (target users)
  - When to use this skill (use cases)
  - What problems it solves

  Example structure:
  Paragraph 1: High-level overview of capabilities
  Paragraph 2: Target users and their pain points
  Paragraph 3: Core value proposition (time savings, quality improvements)
-->

[Paragraph 1: Overview of capabilities - What does this skill provide?]

[Paragraph 2: Target users and pain points - Who needs this and why?]

**Core Value:** [Quantified benefit - Example: "Save 40%+ time on content creation while improving consistency by 30% and SEO performance by 25%."]

## Core Capabilities

<!--
  List 4-6 primary capabilities this skill enables.
  Use bullet points with brief descriptions.
  Focus on outcomes, not just features.
-->

- **Capability 1** - Brief description of what users can accomplish
- **Capability 2** - Brief description of what users can accomplish
- **Capability 3** - Brief description of what users can accomplish
- **Capability 4** - Brief description of what users can accomplish
- **Capability 5** (optional) - Brief description
- **Capability 6** (optional) - Brief description

## Quick Start

<!--
  Provide copy-paste ready commands for immediate use.
  This should get users productive in under 5 minutes.
  Include 2-3 most common use cases.
-->

### [Primary Use Case]
```bash
# Quick command for most common task
python scripts/tool_name.py input.txt

# With options
python scripts/tool_name.py input.txt --option value
```

### [Secondary Use Case]
```bash
# Alternative common usage
python scripts/another_tool.py input.csv --output json
```

### Access Documentation
<!--
  Point users to reference guides and templates
-->
- Tool documentation: `references/tool_reference.md`
- Best practices: `references/best_practices.md`
- Templates: `assets/template_name.md`

## Key Workflows

<!--
  Document 2-4 complete workflows that show how to use the skill end-to-end.
  Each workflow should have: Title, Time Estimate, Steps, Expected Output

  Workflow types to consider:
  - First-time setup/onboarding
  - Primary use case (most common)
  - Advanced use case (power users)
  - Integration workflow (with other skills/tools)
-->

### 1. [Primary Workflow Name]

**Time:** [X hours/minutes for typical execution]

<!--
  Provide step-by-step instructions.
  Include commands where applicable.
  Explain the "why" not just the "what"
-->

1. **[Action Step]** - Description of first step and why it matters
2. **[Action Step]** - Description of second step
   ```bash
   # Command example if applicable
   python scripts/tool.py input.txt
   ```
3. **[Action Step]** - Description of third step
4. **[Action Step]** - Description of fourth step
5. **[Action Step]** - Description of final step

See [reference_guide.md](references/reference_guide.md) for detailed walkthrough.

### 2. [Secondary Workflow Name]

**Time:** [X hours/minutes]

1. **[Action Step]** - Description
2. **[Action Step]** - Description
3. **[Action Step]** - Description
4. **[Action Step]** - Description

### 3. [Advanced Workflow Name]

**Time:** [X hours/minutes]

1. **[Action Step]** - Description
2. **[Action Step]** - Description
3. **[Action Step]** - Description

### 4. [Optional Fourth Workflow]

<!-- Delete this section if you only have 3 workflows -->

**Time:** [X hours/minutes]

1. **[Action Step]** - Description
2. **[Action Step]** - Description

## Python Tools

<!--
  Document each Python CLI tool in scripts/ directory.
  Provide comprehensive usage documentation for each tool.
  Minimum 1 tool, ideally 2-4 tools per skill.

  For each tool document:
  - Purpose (one sentence)
  - Key features (bullet list)
  - Usage examples (bash code blocks)
  - Common use cases
-->

### tool_name.py

<!--
  Replace "tool_name" with actual tool filename
-->

[One-sentence description of what this tool does]

**Key Features:**
- Feature 1 with brief description
- Feature 2 with brief description
- Feature 3 with brief description
- Feature 4 with brief description

**Common Usage:**
```bash
# Basic usage
python scripts/tool_name.py input.txt

# With options
python scripts/tool_name.py input.txt --option value

# JSON output for automation
python scripts/tool_name.py input.txt --output json

# Save to file
python scripts/tool_name.py input.txt --file results.txt

# Help
python scripts/tool_name.py --help
```

**Use Cases:**
- When to use this tool (scenario 1)
- When to use this tool (scenario 2)
- When to use this tool (scenario 3)

See [tools.md](references/tools.md) for comprehensive documentation and advanced examples.

### second_tool.py

<!-- Repeat structure for additional tools -->

[One-sentence description]

**Key Features:**
- Feature 1
- Feature 2
- Feature 3

**Common Usage:**
```bash
python scripts/second_tool.py input.csv --flag
```

**Use Cases:**
- Use case 1
- Use case 2

### third_tool.py

<!-- Optional - add more tools as needed -->

[One-sentence description]

**Key Features:**
- Feature 1
- Feature 2

**Common Usage:**
```bash
python scripts/third_tool.py --input file.txt
```

## Reference Documentation

<!--
  Document reference guides in references/ directory.
  These are knowledge bases, frameworks, best practices.
  Point users to the right guide for their needs.
-->

### When to Use Each Reference

**[reference_guide_1.md](references/reference_guide_1.md)** - [Topic area]
- What this guide covers (bullet list)
- When to consult this guide
- Key sections and contents
- Target audience

**[reference_guide_2.md](references/reference_guide_2.md)** - [Topic area]
- What this guide covers (bullet list)
- When to consult this guide
- Key sections and contents
- Target audience

**[reference_guide_3.md](references/reference_guide_3.md)** - [Topic area] (optional)
- What this guide covers
- When to consult this guide
- Target audience

## Templates

<!--
  Optional section - only if skill has user-facing templates in assets/
  Document each template's purpose and usage
-->

### [Template Name]

**Location:** `assets/template_name.md`

**Purpose:** [What this template is used for]

**Use Cases:**
- When to use this template (scenario 1)
- When to use this template (scenario 2)
- When to use this template (scenario 3)

**Sections:** [List main sections of the template]

### [Second Template]

<!-- Repeat for additional templates -->

**Location:** `assets/second_template.md`

**Purpose:** [What this template is used for]

**Use Cases:**
- Use case 1
- Use case 2

## Best Practices

<!--
  Document quality standards, common pitfalls, and recommendations.
  Provide specific, actionable guidance.
-->

### Quality Standards

- **Standard 1:** Target value or threshold with brief explanation
- **Standard 2:** Target value or threshold with brief explanation
- **Standard 3:** Target value or threshold with brief explanation
- **Standard 4:** Target value or threshold with brief explanation

### Common Pitfalls to Avoid

- **Pitfall 1** - Why this is problematic and how to avoid it
- **Pitfall 2** - Why this is problematic and how to avoid it
- **Pitfall 3** - Why this is problematic and how to avoid it
- **Pitfall 4** - Why this is problematic and how to avoid it

See [reference_guide.md](references/reference_guide.md) for detailed guidelines.

## Performance Metrics

<!--
  Define measurable outcomes for tracking skill effectiveness.
  Group into logical categories (3-4 categories).
  Use specific, quantifiable metrics.
-->

**[Metric Category 1]:**
- Metric name (target: X% or specific value)
- Metric name (target: X% or specific value)
- Metric name (target: X% or specific value)

**[Metric Category 2]:**
- Metric name (target: X% or specific value)
- Metric name (target: X% or specific value)

**[Metric Category 3]:**
- Metric name (target: X% or specific value)
- Metric name (target: X% or specific value)

**[Metric Category 4]** (optional):
- Metric name (target: X% or specific value)

## Integration

<!--
  Document how this skill integrates with other tools, platforms, or skills.
  Optional section - remove if not applicable.
-->

This skill works best with:
- Integration 1 (description of how/why)
- Integration 2 (description of how/why)
- Integration 3 (description of how/why)
- Integration 4 (description of how/why)

See [tools.md](references/tools.md) for CI/CD and automation integration examples.

## Examples

<!--
  Optional section - provide complete, real-world usage examples.
  Show end-to-end workflows with actual commands and expected outputs.
-->

### Example 1: [Use Case Name]

**Scenario:** [Describe the problem/goal]

**Workflow:**
```bash
# Step 1: Description
python scripts/tool1.py input.txt

# Step 2: Description
python scripts/tool2.py results.json --format report

# Step 3: Description
# Review output
```

**Expected Outcome:** [What success looks like]

**Time Estimate:** [How long this typically takes]

### Example 2: [Use Case Name]

<!-- Repeat structure for additional examples -->

**Scenario:** [Describe the problem/goal]

**Workflow:**
```bash
# Commands
```

**Expected Outcome:** [What success looks like]

## Integration with Other Skills

<!--
  Optional section - document how this skill complements other skills.
  Cross-reference related skills in the same or different domains.
-->

**[Related Skill 1]:** How these skills work together

**[Related Skill 2]:** How these skills work together

**[Related Skill 3]:** How these skills work together

## Benefits

<!--
  Optional section - quantify the value this skill provides.
  Include time savings, quality improvements, business impact.
-->

**Time Savings:**
- X% faster [task] using [feature] vs. manual approach
- Y% reduction in [activity] through [capability]

**Quality Improvements:**
- Benefit 1 with quantification
- Benefit 2 with quantification

**Business Impact:**
- Impact 1 with quantification
- Impact 2 with quantification

## Next Steps

<!--
  Optional section - guide users on what to do after reviewing the skill.
  Provide clear starting points for different user types.
-->

**Getting Started:**
1. [First action - usually running a tool or reviewing a guide]
2. [Second action - trying a workflow]
3. [Third action - applying to real work]

**Advanced Usage:**
- [Advanced technique or integration]
- [Advanced technique or integration]
- [Advanced technique or integration]

## Additional Resources

<!--
  Optional section - link to related documentation.
  Remove this section if no additional resources.
-->

- **Quick commands** - See [examples.md](references/examples.md)
- **Troubleshooting** - See [tools.md](references/tools.md)
- **Advanced patterns** - See [advanced_guide.md](references/advanced_guide.md)
- **External documentation** - [Link to external resource]

---

<!--
  Update metadata when publishing or updating skill.
  Status options: Production Ready, Beta, Alpha, Deprecated
-->

**Documentation:** Full skill guide and workflows available in this file

**Support:** For issues or questions, refer to domain guide at `../{domain-team}/CLAUDE.md`

**Version:** 1.0.0 | **Last Updated:** YYYY-MM-DD | **Status:** Production Ready
