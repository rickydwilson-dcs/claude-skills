# Slash Command Metadata Schema Specification

**Version:** 1.0.0
**Last Updated:** November 24, 2025
**Status:** Production Ready

## Overview

This schema defines the comprehensive YAML frontmatter structure for slash commands in the claude-skills repository. The schema is designed to be website-ready from Day 1, enabling rich discovery, cross-referencing, analytics tracking, and community engagement.

**Design Principles:**
- Universal schema that works for commands, agents, and skills
- Website-first approach for browse/filter/search functionality
- Extensible for future features (analytics, community contributions)
- Consistent with existing repository patterns
- Validation-friendly structure

## Schema Structure

### Complete Schema Template

```yaml
---
# === CORE IDENTITY ===
name: command-name
title: Human-Readable Command Title
description: One-sentence description of what this command does (80-120 chars)
category: primary-category
subcategory: specific-subcategory

# === WEBSITE DISPLAY ===
difficulty: beginner|intermediate|advanced
time-saved: "15 minutes per use"
frequency: "Weekly per developer"
use-cases:
  - "Primary use case description"
  - "Secondary use case description"
  - "Additional use case (min 2 total)"

# === RELATIONSHIPS (Cross-linking) ===
related-agents:
  - cs-agent-name-1
  - cs-agent-name-2
related-skills:
  - domain-team/skill-name
  - domain-team/another-skill
related-commands:
  - /related-command-1
  - /related-command-2

# === TECHNICAL ===
dependencies:
  tools:
    - Read
    - Write
    - Bash
  scripts:
    - domain-team/skill-name/scripts/tool.py
    - domain-team/skill-name/scripts/another-tool.py
  python-packages: []  # Empty if using stdlib only

compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows

# === EXAMPLES (Min 2) ===
examples:
  - title: "Basic Usage Example"
    input: "/command-name basic-argument"
    output: "Expected output description or actual output"

  - title: "Advanced Usage Example"
    input: "/command-name --flag advanced-argument"
    output: "Expected output description or actual output"

# === ANALYTICS (Placeholder for future) ===
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Author Name or Team
contributors:
  - Contributor Name 1
  - Contributor Name 2
created: 2025-11-24
updated: 2025-11-24

# === DISCOVERABILITY ===
tags:
  - primary-tag
  - secondary-tag
  - tertiary-tag
  - additional-tags
featured: false
verified: true
license: MIT
---
```

## Field Specifications

### Core Identity Fields

#### `name` (Required)
- **Type:** String (kebab-case)
- **Pattern:** `^[a-z0-9]+(-[a-z0-9]+)*$`
- **Example:** `feature-analyzer`, `code-review-assistant`
- **Description:** Unique identifier for the command
- **Validation Rules:**
  - Must be lowercase
  - Use hyphens for word separation
  - No special characters except hyphens
  - Must be unique across all commands
  - 3-50 characters length

#### `title` (Required)
- **Type:** String
- **Example:** "Feature Analysis and Planning Assistant"
- **Description:** Human-readable display name
- **Validation Rules:**
  - 10-80 characters
  - Title case preferred
  - Clear and descriptive
  - Can include special characters

#### `description` (Required)
- **Type:** String
- **Example:** "Analyze feature requirements and generate implementation plans with effort estimates"
- **Description:** One-sentence summary of command functionality
- **Validation Rules:**
  - 80-120 characters recommended
  - Must be a complete sentence
  - Action-oriented language
  - Should answer "What does this command do?"

#### `category` (Required)
- **Type:** Enum String
- **Allowed Values:**
  - `development` - Code-related commands
  - `product` - Product management commands
  - `marketing` - Marketing and content commands
  - `engineering` - Infrastructure and DevOps
  - `quality` - Testing and QA commands
  - `documentation` - Docs and technical writing
  - `design` - UI/UX and design commands
  - `analytics` - Data analysis commands
  - `automation` - Workflow automation
  - `collaboration` - Team coordination
- **Description:** Primary category for filtering
- **Validation Rules:**
  - Must be one of allowed values
  - Single category only

#### `subcategory` (Required)
- **Type:** String
- **Example:** `feature-planning`, `code-review`, `seo-optimization`
- **Description:** Specific subcategory within primary category
- **Validation Rules:**
  - 3-30 characters
  - kebab-case format
  - Should be specific and descriptive
  - Related to parent category

### Website Display Fields

#### `difficulty` (Required)
- **Type:** Enum String
- **Allowed Values:**
  - `beginner` - No prerequisites, simple to use
  - `intermediate` - Some domain knowledge required
  - `advanced` - Expert-level, complex workflows
- **Description:** Skill level required to use command
- **Validation Rules:**
  - Must be one of three values
  - Consider user's technical background
  - Assess complexity of inputs required

#### `time-saved` (Required)
- **Type:** String (duration format)
- **Pattern:** `^\d+(-\d+)?\s+(minutes?|hours?|days?)(\s+per\s+.+)?$`
- **Examples:**
  - "15 minutes per use"
  - "2-3 hours per sprint"
  - "1 day per quarter"
- **Description:** Quantified time savings
- **Validation Rules:**
  - Must include number and unit
  - Can include range (5-10 minutes)
  - Should specify frequency context
  - Be realistic and measurable

#### `frequency` (Required)
- **Type:** String
- **Pattern:** `^(Daily|Weekly|Monthly|Quarterly|As-needed)(\s+per\s+.+)?$`
- **Examples:**
  - "Weekly per developer"
  - "Daily during sprints"
  - "As-needed for releases"
- **Description:** How often command is typically used
- **Validation Rules:**
  - Start with frequency term
  - Include context (per developer, per team, etc.)
  - Should reflect realistic usage patterns

#### `use-cases` (Required)
- **Type:** Array of Strings
- **Min Items:** 2
- **Max Items:** 5
- **Example:**
  ```yaml
  use-cases:
    - "Planning new feature development with RICE prioritization"
    - "Analyzing existing feature requests for roadmap planning"
    - "Generating quarterly OKRs from strategic initiatives"
  ```
- **Description:** Concrete scenarios where command provides value
- **Validation Rules:**
  - Minimum 2 use cases required
  - Each 40-120 characters
  - Start with action verbs
  - Be specific, not generic
  - Different use cases, not variations

### Relationships Fields

#### `related-agents` (Optional)
- **Type:** Array of Strings
- **Pattern:** Each item matches `^cs-[a-z0-9-]+$`
- **Example:**
  ```yaml
  related-agents:
    - cs-product-manager
    - cs-agile-product-owner
  ```
- **Description:** Agents that integrate with this command
- **Validation Rules:**
  - Agent must exist in repository
  - Use cs-* prefix format
  - Verify bidirectional relationships
  - 0-10 related agents max

#### `related-skills` (Optional)
- **Type:** Array of Strings
- **Pattern:** `^[a-z-]+/[a-z-]+$`
- **Example:**
  ```yaml
  related-skills:
    - product-team/product-manager-toolkit
    - product-team/agile-product-owner
  ```
- **Description:** Skills that this command leverages
- **Validation Rules:**
  - Skill path must exist
  - Format: domain/skill-name
  - Verify skill exists in repository
  - 0-10 related skills max

#### `related-commands` (Optional)
- **Type:** Array of Strings
- **Pattern:** `^/[a-z0-9-]+$`
- **Example:**
  ```yaml
  related-commands:
    - /feature-prioritize
    - /roadmap-generate
  ```
- **Description:** Other commands that complement this one
- **Validation Rules:**
  - Must start with /
  - Commands should exist
  - Suggest logical workflow sequences
  - 0-8 related commands max

### Technical Fields

#### `dependencies` (Required)
- **Type:** Object with nested arrays
- **Structure:**
  ```yaml
  dependencies:
    tools: [String]        # Claude Code tools
    scripts: [String]      # Python scripts used
    python-packages: [String]  # External packages (or empty)
  ```
- **Example:**
  ```yaml
  dependencies:
    tools:
      - Read
      - Write
      - Bash
      - Grep
    scripts:
      - product-team/product-manager-toolkit/scripts/rice_prioritizer.py
    python-packages: []  # Standard library only
  ```
- **Validation Rules:**
  - `tools`: Must be valid Claude Code tools
  - `scripts`: Paths must exist in repository
  - `python-packages`: Empty array preferred (stdlib only)
  - All arrays can be empty if no dependencies

#### `compatibility` (Required)
- **Type:** Object with boolean and array fields
- **Structure:**
  ```yaml
  compatibility:
    claude-ai: Boolean
    claude-code: Boolean
    platforms: [String]
  ```
- **Example:**
  ```yaml
  compatibility:
    claude-ai: true
    claude-code: true
    platforms:
      - macos
      - linux
      - windows
  ```
- **Validation Rules:**
  - `claude-ai`: Boolean (works in Claude.ai interface)
  - `claude-code`: Boolean (works in Claude Code CLI)
  - `platforms`: Array of [macos, linux, windows]
  - At least one platform required

### Examples Fields

#### `examples` (Required)
- **Type:** Array of Objects
- **Min Items:** 2
- **Max Items:** 5
- **Object Structure:**
  ```yaml
  - title: String (20-80 chars)
    input: String (actual command)
    output: String (expected result)
  ```
- **Example:**
  ```yaml
  examples:
    - title: "Basic Feature Prioritization"
      input: "/prioritize-features features.csv"
      output: "Generated RICE scores for 15 features, top 3: API Rate Limiting (RICE: 85), User Dashboard (RICE: 78), Dark Mode (RICE: 45)"

    - title: "Prioritization with Capacity Planning"
      input: "/prioritize-features features.csv --capacity 20"
      output: "Quarterly roadmap generated: Q1 includes 5 features (18.5 person-months), 1.5 months buffer"
  ```
- **Validation Rules:**
  - Minimum 2 examples required
  - Examples should progress from simple to complex
  - Input must be realistic command syntax
  - Output should be specific, not generic
  - Each example demonstrates different capability

### Analytics Fields (Placeholder)

#### `stats` (Required)
- **Type:** Object with numeric fields
- **Structure:**
  ```yaml
  stats:
    installs: Integer (default: 0)
    upvotes: Integer (default: 0)
    rating: Float (default: 0.0, range: 0.0-5.0)
    reviews: Integer (default: 0)
  ```
- **Description:** Placeholder for future analytics tracking
- **Validation Rules:**
  - All fields initialize to 0
  - `rating`: 0.0-5.0 range
  - Will be populated by website backend
  - Do not manually edit

### Versioning Fields

#### `version` (Required)
- **Type:** String (Semantic Versioning)
- **Pattern:** `^v\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$`
- **Example:** `v1.0.0`, `v2.1.3`, `v1.0.0-beta`
- **Description:** Semantic version of command
- **Validation Rules:**
  - Must follow semver format
  - Start with 'v' prefix
  - Format: vMAJOR.MINOR.PATCH
  - Optional pre-release suffix

#### `author` (Required)
- **Type:** String
- **Example:** "Claude Skills Team", "John Doe"
- **Description:** Original author or team
- **Validation Rules:**
  - 2-50 characters
  - Person name or team name
  - Can include organization

#### `contributors` (Optional)
- **Type:** Array of Strings
- **Example:**
  ```yaml
  contributors:
    - Jane Smith
    - Engineering Team
    - Community Contributor
  ```
- **Description:** Additional contributors
- **Validation Rules:**
  - Each 2-50 characters
  - Can be empty if single author
  - List significant contributors only

#### `created` (Required)
- **Type:** Date String
- **Pattern:** `^\d{4}-\d{2}-\d{2}$`
- **Example:** `2025-11-24`
- **Description:** Date command was created
- **Validation Rules:**
  - ISO 8601 date format (YYYY-MM-DD)
  - Must be valid date
  - Cannot be future date

#### `updated` (Required)
- **Type:** Date String
- **Pattern:** `^\d{4}-\d{2}-\d{2}$`
- **Example:** `2025-11-24`
- **Description:** Date of last update
- **Validation Rules:**
  - ISO 8601 date format (YYYY-MM-DD)
  - Must be >= created date
  - Update when making changes

### Discoverability Fields

#### `tags` (Required)
- **Type:** Array of Strings
- **Min Items:** 3
- **Max Items:** 10
- **Example:**
  ```yaml
  tags:
    - feature-planning
    - product-management
    - prioritization
    - roadmap
    - agile
  ```
- **Description:** Search and filter keywords
- **Validation Rules:**
  - Minimum 3 tags
  - Maximum 10 tags
  - kebab-case format
  - Lowercase only
  - Relevant to command functionality
  - Include domain, use-case, and technology tags

#### `featured` (Required)
- **Type:** Boolean
- **Default:** `false`
- **Description:** Whether command appears in featured section
- **Validation Rules:**
  - Must be boolean
  - Reserved for exceptional commands
  - Requires maintainer approval

#### `verified` (Required)
- **Type:** Boolean
- **Default:** `true` for official commands
- **Description:** Official/verified status
- **Validation Rules:**
  - Must be boolean
  - `true` for repository maintainers
  - `false` for community contributions (future)

#### `license` (Required)
- **Type:** String
- **Allowed Values:** `MIT`, `Apache-2.0`, `GPL-3.0`, `BSD-3-Clause`
- **Default:** `MIT`
- **Description:** Software license
- **Validation Rules:**
  - Must be standard SPDX license identifier
  - Match repository license (MIT)

## Validation Rules Summary

### Required Fields (18)
1. name
2. title
3. description
4. category
5. subcategory
6. difficulty
7. time-saved
8. frequency
9. use-cases
10. dependencies
11. compatibility
12. examples
13. stats
14. version
15. author
16. created
17. updated
18. tags
19. featured
20. verified
21. license

### Optional Fields (3)
1. related-agents
2. related-skills
3. related-commands
4. contributors

### Minimum Viable Command

A command must include at minimum:
- All 21 required fields
- At least 2 use cases
- At least 2 examples
- At least 3 tags
- Valid compatibility for at least 1 platform

### Maximum Complexity

Upper bounds for scalability:
- use-cases: 5 max
- related-agents: 10 max
- related-skills: 10 max
- related-commands: 8 max
- examples: 5 max
- tags: 10 max
- contributors: 20 max

## Migration Strategy

### Retrofitting Existing Agents

To retrofit existing agents with this schema:

1. **Add new fields incrementally**
   - Start with core identity and technical
   - Add relationships based on existing docs
   - Fill analytics with placeholder values

2. **Extract from existing content**
   - Parse YAML frontmatter for base fields
   - Extract use cases from "Purpose" section
   - Generate examples from "Workflows" section
   - Create tags from domain and expertise

3. **Validate completeness**
   - Ensure all required fields present
   - Verify paths and references exist
   - Check relationship bidirectionality

### Retrofitting Existing Skills

To retrofit existing skills:

1. **Map skill metadata to command schema**
   - Skill name → command name
   - Description → description + title
   - Keywords → tags
   - Tools → dependencies

2. **Generate command-specific fields**
   - Create use-cases from skill workflows
   - Generate examples from usage patterns
   - Estimate time-saved from skill metrics

3. **Establish relationships**
   - Link to agents that use this skill
   - Cross-reference related skills
   - Suggest workflow commands

## Best Practices

### Writing Descriptions
- Start with action verb
- Be specific about outcomes
- Avoid marketing language
- 80-120 characters ideal
- One complete sentence

### Defining Use Cases
- Start with gerund (action + -ing)
- Be concrete and specific
- Include context and benefit
- 40-120 characters each
- Show diverse applications

### Creating Examples
- Progress from simple to complex
- Use realistic data and arguments
- Show actual expected output
- Demonstrate key features
- 2-5 examples per command

### Choosing Tags
- Include domain (product, engineering, etc.)
- Add use-case tags (planning, analysis, etc.)
- Include technology (python, api, etc.)
- Use common search terms
- 3-10 tags per command

### Estimating Time Saved
- Be conservative and realistic
- Include context (per use, per sprint, etc.)
- Consider learning curve
- Base on actual measurements
- Use ranges for variability

## Schema Evolution

### Version History

**v1.0.0** (2025-11-24)
- Initial schema release
- Universal for commands, agents, skills
- Website-ready Day 1
- Analytics placeholder structure

### Future Enhancements (Planned)

**v1.1.0** - Community features
- Community ratings integration
- User reviews structure
- Contribution guidelines field
- Fork/remix tracking

**v1.2.0** - Advanced analytics
- Usage tracking integration
- Performance metrics
- Success rate tracking
- A/B testing support

**v2.0.0** - Marketplace features
- Pricing/monetization support
- Premium command fields
- Subscription tiers
- Payment integration

## References

- **Agent Schema:** [agents/CLAUDE.md](../agents/CLAUDE.md)
- **Skill Schema:** [skills/marketing-team/CLAUDE.md](../skills/marketing-team/CLAUDE.md)
- **Builder Standards:** [docs/standards/builder-standards.md](../docs/standards/builder-standards.md)
- **Example Implementation:** [command-metadata-example.yaml](./command-metadata-example.yaml)
- **JSON Export Schema:** [json-export-schema.json](./json-export-schema.json)

---

**Schema Version:** v1.0.0
**Status:** Production Ready
**Maintainer:** Claude Skills Team
**Last Updated:** November 24, 2025
