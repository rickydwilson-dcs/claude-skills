# Slash Command Metadata Schema

**Version:** 1.0.0
**Status:** Production Ready
**Last Updated:** November 24, 2025

## Overview

This directory contains the comprehensive metadata schema for slash commands in the claude-skills repository. The schema is designed to be **website-ready from Day 1**, enabling rich discovery, cross-referencing, analytics tracking, and future community contributions.

## Schema Files

### 1. [command-metadata-schema.md](./command-metadata-schema.md)
**Full specification and field documentation**

- Complete field-by-field documentation (21 required, 4 optional fields)
- Validation rules for each field type
- Examples for all field types
- Migration strategy for retrofitting existing agents/skills
- Best practices and patterns

**Key Sections:**
- Core Identity (name, title, description, category, subcategory)
- Website Display (difficulty, time-saved, frequency, use-cases)
- Relationships (related-agents, related-skills, related-commands)
- Technical (dependencies, compatibility, examples)
- Analytics (stats placeholder for future tracking)
- Versioning (version, author, contributors, dates)
- Discoverability (tags, featured, verified, license)

**Use this when:**
- Creating new slash commands
- Understanding field requirements
- Validating command metadata
- Planning schema extensions

### 2. [command-metadata-example.yaml](./command-metadata-example.yaml)
**Complete working example with realistic data**

A fully populated example showing the `/feature-prioritize` command with:
- All 25 fields populated with realistic data
- Inline comments explaining each section
- Actual command documentation below YAML frontmatter
- Demonstrates proper formatting and structure

**Use this when:**
- Creating your first slash command
- Need a template to copy and customize
- Validating your YAML syntax
- Understanding field relationships

### 3. [json-export-schema.json](./json-export-schema.json)
**JSON Schema for website API**

JSON Schema (draft-07) defining:
- How YAML frontmatter translates to JSON
- API response format and structure
- Field types, constraints, and validation rules
- Example API endpoints and query parameters
- Search indexing strategy recommendations

**Use this when:**
- Building the website API
- Implementing search/filter functionality
- Validating JSON exports programmatically
- Planning database schema for website

### 4. [README.md](./README.md)
**This file - Overview and quick start guide**

## Quick Start

### Creating a New Slash Command

**Step 1:** Copy the example template
```bash
cp schema/command-metadata-example.yaml .claude/commands/my-command.md
```

**Step 2:** Update the YAML frontmatter
- Change `name` to your command name (kebab-case)
- Update all core identity fields
- Fill in realistic time-saved and frequency
- Add 2-5 concrete use cases
- List dependencies (tools, scripts, packages)
- Create 2-5 examples showing usage
- Add 3-10 relevant tags

**Step 3:** Write the command documentation
Below the YAML frontmatter, document:
- Purpose and overview
- Usage examples
- Input/output formats
- Workflows
- Success metrics

**Step 4:** Validate your command
```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('.claude/commands/my-command.md'))"

# Validate against schema
# (validation tool to be created)
```

## Schema Structure Overview

```yaml
---
# Core Identity (5 fields)
name: command-name
title: Human-Readable Title
description: One-sentence description
category: primary-category
subcategory: specific-subcategory

# Website Display (4 fields)
difficulty: beginner|intermediate|advanced
time-saved: "X hours per use"
frequency: "Weekly per team"
use-cases: [2-5 concrete scenarios]

# Relationships (3 optional fields)
related-agents: [cs-agent-list]
related-skills: [domain/skill-list]
related-commands: [/command-list]

# Technical (2 objects)
dependencies:
  tools: [Claude Code tools]
  scripts: [Python script paths]
  python-packages: []
compatibility:
  claude-ai: true
  claude-code: true
  platforms: [macos, linux, windows]

# Examples (2-5 required)
examples:
  - title: "Example Title"
    input: "/command args"
    output: "Expected output"

# Analytics (1 object - placeholder)
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0

# Versioning (5 fields)
version: v1.0.0
author: Author Name
contributors: []
created: 2025-11-24
updated: 2025-11-24

# Discoverability (4 fields)
tags: [3-10 keywords]
featured: false
verified: true
license: MIT
---
```

## Design Principles

### 1. Universal Schema
Works for commands, agents, and skills - we'll retrofit agents/skills later

### 2. Website-First
All fields designed for rich discovery:
- Browse/filter/search functionality
- Cross-referencing between entities
- Analytics tracking (placeholder)
- Version management

### 3. Validation-Friendly
Clear types, patterns, and constraints enable:
- Automated validation tools
- JSON Schema validation
- Pre-commit hooks
- CI/CD checks

### 4. Extensible
Schema designed to grow:
- v1.1.0: Community features (ratings, reviews, contributions)
- v1.2.0: Advanced analytics (usage tracking, performance metrics)
- v2.0.0: Marketplace features (pricing, subscriptions)

### 5. Consistent with Repository
Follows existing patterns from:
- Agent YAML frontmatter (name, description, domain, tools)
- Skill YAML frontmatter (metadata, keywords, tech-stack)
- Repository standards (kebab-case, semantic versioning)

## Field Requirements

### Required Fields (21)
Must be present in every command:
- Core Identity: name, title, description, category, subcategory
- Website Display: difficulty, time-saved, frequency, use-cases
- Technical: dependencies, compatibility, examples
- Analytics: stats
- Versioning: version, author, created, updated
- Discoverability: tags, featured, verified, license

### Optional Fields (4)
Include when relevant:
- Relationships: related-agents, related-skills, related-commands
- Versioning: contributors

### Minimum Requirements
- At least 2 use cases
- At least 2 examples
- At least 3 tags
- At least 1 compatible platform

## Validation Rules

### Automated Checks
The schema enables automated validation:

```python
# Example validation (future tool)
from schema_validator import validate_command

result = validate_command('.claude/commands/my-command.md')
if result.is_valid:
    print("✓ Command metadata is valid")
else:
    for error in result.errors:
        print(f"✗ {error.field}: {error.message}")
```

**Validation Categories:**
1. **Syntax**: Valid YAML, proper formatting
2. **Required Fields**: All 21 required fields present
3. **Field Types**: Correct types (string, array, object, boolean)
4. **Patterns**: Matches regex patterns (dates, versions, names)
5. **Constraints**: Min/max lengths, array sizes, enum values
6. **References**: Paths exist, related entities exist
7. **Relationships**: Bidirectional links verified

### Manual Review
Human review required for:
- Use case quality and specificity
- Example realism and clarity
- Tag relevance and accuracy
- Time-saved estimates
- Difficulty classification

## Website Integration

### API Endpoints (Planned)

**List Commands**
```http
GET /api/v1/commands?category=product&difficulty=intermediate&page=1
```

**Get Single Command**
```http
GET /api/v1/commands/feature-prioritize
```

**Search Commands**
```http
POST /api/v1/commands/search
{
  "query": "feature planning",
  "filters": {
    "categories": ["product"],
    "tags": ["roadmap-planning"]
  }
}
```

**Get Related Items**
```http
GET /api/v1/commands/feature-prioritize/related
```

**Trending Commands**
```http
GET /api/v1/stats/trending?period=week&limit=10
```

### Search Features

**Full-Text Search:**
- Title (high weight)
- Description (medium weight)
- Use cases (low weight)

**Faceted Filtering:**
- Category (10 options)
- Subcategory (dynamic)
- Difficulty (3 levels)
- Tags (all unique tags)
- Platforms (3 options)
- Compatibility (Claude AI/Code)

**Sorting:**
- Name (A-Z, Z-A)
- Rating (high to low)
- Installs (most to least)
- Updated (newest first)

### Analytics Tracking

**Placeholder fields (v1.0.0):**
- `stats.installs`: Command usage count
- `stats.upvotes`: Community upvotes
- `stats.rating`: Average rating (0.0-5.0)
- `stats.reviews`: Number of reviews

**Future implementation (v1.1.0+):**
- Track installs via website API
- Enable community ratings/reviews
- Generate trending algorithms
- Provide usage analytics dashboard

## Migration Strategy

### Retrofitting Existing Agents

To add command metadata to existing agents:

**Step 1:** Extract existing YAML frontmatter
```yaml
# Current agent frontmatter
name: cs-product-manager
description: Product management agent...
skills: product-team/product-manager-toolkit
domain: product
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
```

**Step 2:** Map to command schema
```yaml
# New command metadata
name: product-manager
title: Product Manager Workflow Assistant
description: Feature prioritization, customer discovery, PRD development, and roadmap planning
category: product
subcategory: product-management
# ... add remaining fields
```

**Step 3:** Generate missing fields
- Extract use-cases from "Purpose" section
- Create examples from "Workflows" section
- Generate tags from domain, skills, and expertise
- Estimate time-saved from workflow time estimates

**Step 4:** Establish relationships
- Link to related agents from same domain
- Reference skills used by agent
- Suggest related workflow commands

### Retrofitting Existing Skills

To add command metadata to existing skills:

**Step 1:** Extract skill metadata
```yaml
# Current skill frontmatter
name: content-creator
description: Create SEO-optimized marketing content...
metadata:
  category: marketing
  domain: content-marketing
  keywords: [content creation, SEO, brand voice]
  python-tools: [brand_voice_analyzer.py, seo_optimizer.py]
```

**Step 2:** Map to command schema
```yaml
# New command metadata
name: content-creator
title: SEO-Optimized Content Creation
description: Brand voice analysis and SEO optimization for marketing content
category: marketing
subcategory: content-creation
# ... add remaining fields
```

**Step 3:** Generate skill-specific fields
- Create use-cases from key workflows
- Generate examples from tool usage
- Map python-tools to dependencies.scripts
- Extract tags from keywords

## Best Practices

### Writing Descriptions
✓ **Good:** "Analyze and prioritize feature requests using RICE framework with automated scoring"
✗ **Bad:** "A tool for features" (too vague)
✗ **Bad:** "The best, most amazing feature prioritization system ever created" (marketing fluff)

### Defining Use Cases
✓ **Good:** "Prioritizing quarterly roadmap with 20+ feature candidates using RICE scores"
✗ **Bad:** "Feature planning" (too generic)
✗ **Bad:** "When you need to prioritize features" (not specific enough)

### Creating Examples
✓ **Good:**
```yaml
- title: "Prioritization with Capacity Planning"
  input: "/feature-prioritize features.csv --capacity 20"
  output: "Quarterly roadmap: Q1 includes 5 features (18.5 person-months)"
```
✗ **Bad:**
```yaml
- title: "Example"
  input: "/command"
  output: "Output"
```

### Choosing Tags
✓ **Good:** `[product-management, feature-planning, prioritization, rice-framework]`
✗ **Bad:** `[good, useful, best, awesome]` (not descriptive)
✗ **Bad:** `[Product Management, RICE Framework]` (not kebab-case)

### Estimating Time Saved
✓ **Good:** "2-3 hours per prioritization session" (specific, measurable, realistic)
✗ **Bad:** "Saves lots of time" (not quantified)
✗ **Bad:** "10 hours per day" (unrealistic)

## Roadmap

### v1.0.0 (Current)
- ✅ Core schema specification
- ✅ Complete example command
- ✅ JSON export schema
- ✅ Documentation and README
- 🔄 Validation tool (in progress)

### v1.1.0 (Q1 2026)
- Community ratings system
- User reviews and feedback
- Contribution guidelines
- Fork/remix tracking
- Enhanced search algorithms

### v1.2.0 (Q2 2026)
- Advanced analytics dashboard
- Usage tracking integration
- Performance metrics
- A/B testing support
- Recommendation engine

### v2.0.0 (Q3 2026)
- Marketplace features
- Premium commands
- Subscription tiers
- Payment integration
- Advanced licensing

## Contributing

### Creating New Commands
1. Copy `command-metadata-example.yaml`
2. Update all fields with your command details
3. Validate YAML syntax
4. Test command functionality
5. Submit PR with conventional commit: `feat(commands): add /command-name`

### Updating Schema
1. Propose changes in GitHub issue
2. Discuss with maintainers
3. Update schema documentation
4. Update example file
5. Update JSON schema
6. Increment version (semver)

### Reporting Issues
Found a problem with the schema?
1. Check existing issues
2. Create new issue with label `schema`
3. Provide specific examples
4. Suggest solution if possible

## Resources

- **Full Specification:** [command-metadata-schema.md](./command-metadata-schema.md)
- **Working Example:** [command-metadata-example.yaml](./command-metadata-example.yaml)
- **JSON Schema:** [json-export-schema.json](./json-export-schema.json)
- **Agent Architecture:** [../agents/CLAUDE.md](../agents/CLAUDE.md)
- **Repository Guide:** [../CLAUDE.md](../CLAUDE.md)

## FAQ

### Q: Why YAML frontmatter instead of JSON?
**A:** YAML is more human-readable and widely used in documentation systems. The JSON export schema enables programmatic access while keeping the source files readable.

### Q: Can I add custom fields?
**A:** The schema is strict for v1.0.0 to ensure consistency. Propose new fields via GitHub issues for future versions.

### Q: How do I validate my command metadata?
**A:** Currently manual validation against schema. Automated validation tool coming in v1.0.1.

### Q: What if my command doesn't fit the categories?
**A:** Use the closest category and specific subcategory. Propose new categories via GitHub issue if needed.

### Q: Should every Python script become a command?
**A:** No. Commands should represent complete workflows, not individual scripts. Scripts are referenced in `dependencies.scripts`.

### Q: How do I handle breaking changes?
**A:** Increment major version (v2.0.0) and document migration path. Maintain backward compatibility when possible.

### Q: Can commands span multiple categories?
**A:** No, choose the primary category. Use tags to indicate cross-category applicability.

### Q: What's the difference between agents and commands?
**A:** Agents are workflow orchestrators (cs-* prefix), commands are executable workflows (/command syntax). Commands may use agents internally.

## Support

- **Questions:** Open GitHub issue with label `question`
- **Bugs:** Open GitHub issue with label `bug`
- **Feature Requests:** Open GitHub issue with label `enhancement`
- **Documentation:** See [../docs/](../docs/)

---

**Schema Version:** v1.0.0
**Status:** Production Ready
**Maintainer:** Claude Skills Team
**Last Updated:** November 24, 2025
