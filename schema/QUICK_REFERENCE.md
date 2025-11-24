# Command Metadata Schema - Quick Reference

**Version:** 1.0.0 | **Last Updated:** November 24, 2025

## TL;DR

Copy `command-metadata-example.yaml`, fill in 25 fields, validate, ship.

## Minimal Valid Command

```yaml
---
# === REQUIRED: 21 fields minimum ===

# Core (5)
name: my-command
title: My Command Title
description: One-sentence description of what this command does (80-120 chars)
category: product
subcategory: feature-planning

# Display (4)
difficulty: intermediate
time-saved: "2 hours per use"
frequency: "Weekly per team"
use-cases:
  - "First concrete use case scenario"
  - "Second concrete use case scenario"

# Technical (2 objects)
dependencies:
  tools: [Read, Write, Bash]
  scripts: []
  python-packages: []
compatibility:
  claude-ai: true
  claude-code: true
  platforms: [macos, linux, windows]

# Examples (min 2)
examples:
  - title: "Basic Usage"
    input: "/my-command input.txt"
    output: "Expected output here"
  - title: "Advanced Usage"
    input: "/my-command input.txt --flag"
    output: "Expected output here"

# Analytics (placeholder)
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0

# Versioning (4)
version: v1.0.0
author: Your Name
created: 2025-11-24
updated: 2025-11-24

# Discoverability (4)
tags:
  - primary-tag
  - secondary-tag
  - tertiary-tag
featured: false
verified: true
license: MIT
---

# Your command documentation goes here
```

## Field Cheat Sheet

| Field | Type | Required | Pattern | Min/Max | Example |
|-------|------|----------|---------|---------|---------|
| **name** | string | ✅ | kebab-case | 3-50 | `feature-prioritize` |
| **title** | string | ✅ | Title Case | 10-80 | `Feature Prioritization` |
| **description** | string | ✅ | sentence | 80-120 | `Analyze and prioritize...` |
| **category** | enum | ✅ | 10 options | - | `product` |
| **subcategory** | string | ✅ | kebab-case | 3-30 | `feature-planning` |
| **difficulty** | enum | ✅ | 3 levels | - | `intermediate` |
| **time-saved** | string | ✅ | N units per X | - | `2 hours per use` |
| **frequency** | string | ✅ | When per who | - | `Weekly per team` |
| **use-cases** | array | ✅ | strings | 2-5 | `["Use case 1", ...]` |
| **related-agents** | array | ❌ | cs-* | 0-10 | `["cs-product-manager"]` |
| **related-skills** | array | ❌ | domain/skill | 0-10 | `["product-team/toolkit"]` |
| **related-commands** | array | ❌ | /command | 0-8 | `["/related-command"]` |
| **dependencies** | object | ✅ | 3 arrays | - | `{tools: [], scripts: [], python-packages: []}` |
| **compatibility** | object | ✅ | 2 bool + array | - | `{claude-ai: true, claude-code: true, platforms: [...]}` |
| **examples** | array | ✅ | objects | 2-5 | `[{title, input, output}]` |
| **stats** | object | ✅ | 4 numbers | - | `{installs: 0, upvotes: 0, rating: 0.0, reviews: 0}` |
| **version** | string | ✅ | semver | - | `v1.0.0` |
| **author** | string | ✅ | name | 2-50 | `Claude Skills Team` |
| **contributors** | array | ❌ | names | 0-20 | `["Person 1", "Person 2"]` |
| **created** | string | ✅ | YYYY-MM-DD | - | `2025-11-24` |
| **updated** | string | ✅ | YYYY-MM-DD | - | `2025-11-24` |
| **tags** | array | ✅ | kebab-case | 3-10 | `["product", "planning"]` |
| **featured** | boolean | ✅ | true/false | - | `false` |
| **verified** | boolean | ✅ | true/false | - | `true` |
| **license** | string | ✅ | SPDX | - | `MIT` |

## Categories Reference

```yaml
category: one-of-these
  - development      # Code-related commands
  - product          # Product management
  - marketing        # Marketing and content
  - engineering      # Infrastructure/DevOps
  - quality          # Testing and QA
  - documentation    # Docs and tech writing
  - design           # UI/UX and design
  - analytics        # Data analysis
  - automation       # Workflow automation
  - collaboration    # Team coordination
```

## Common Patterns

### Time Saved Patterns
```yaml
time-saved: "15 minutes per use"
time-saved: "2-3 hours per sprint"
time-saved: "1 day per quarter"
time-saved: "30 minutes per feature"
```

### Frequency Patterns
```yaml
frequency: "Daily per developer"
frequency: "Weekly per product team"
frequency: "Monthly per manager"
frequency: "Quarterly per organization"
frequency: "As-needed for releases"
```

### Use Case Patterns
```yaml
use-cases:
  - "Planning new feature with RICE prioritization and capacity constraints"
  - "Analyzing existing backlog for quarterly roadmap generation"
  - "Validating stakeholder requests with data-driven framework"
```

### Dependency Patterns
```yaml
# Minimal dependencies (preferred)
dependencies:
  tools: [Read, Write]
  scripts: []
  python-packages: []

# Full tool access
dependencies:
  tools: [Read, Write, Bash, Grep, Glob]
  scripts:
    - product-team/toolkit/scripts/analyzer.py
  python-packages: []  # Still prefer stdlib only
```

### Example Patterns
```yaml
examples:
  # Basic example - always first
  - title: "Basic Usage"
    input: "/command input.txt"
    output: "Simple output showing core functionality"

  # Advanced example - show flags/options
  - title: "Advanced Usage with Options"
    input: "/command input.txt --flag --option value"
    output: "Enhanced output showing additional features"

  # JSON output - if supported
  - title: "JSON Output for Automation"
    input: "/command input.txt --format json"
    output: '{"result": "structured data"}'
```

### Tag Patterns
```yaml
tags:
  # Domain tag (always include)
  - product-management

  # Use case tags
  - feature-planning
  - prioritization

  # Technology/methodology tags
  - rice-framework
  - agile

  # Tool/platform tags
  - roadmap-planning
  - capacity-planning
```

## Validation Checklist

### Pre-Submission Checklist

- [ ] All 21 required fields present
- [ ] YAML syntax valid (no tabs, proper indentation)
- [ ] `name` is unique and kebab-case
- [ ] `description` is 80-120 characters
- [ ] `category` is one of 10 allowed values
- [ ] `difficulty` is beginner|intermediate|advanced
- [ ] `use-cases` has 2-5 items, each 40-120 chars
- [ ] `dependencies.tools` contains valid Claude Code tools
- [ ] `dependencies.scripts` paths exist in repository
- [ ] `dependencies.python-packages` is empty (or justified)
- [ ] `compatibility` has at least 1 platform
- [ ] `examples` has 2-5 items with title/input/output
- [ ] `stats` all set to 0 (placeholder)
- [ ] `version` follows semver (vX.Y.Z)
- [ ] `created` and `updated` are valid dates (YYYY-MM-DD)
- [ ] `tags` has 3-10 items, all lowercase kebab-case
- [ ] `featured` is false (unless exceptional)
- [ ] `verified` is true (official commands only)
- [ ] `license` is MIT (match repository)

### Optional Field Checklist

- [ ] `related-agents` lists exist and use cs-* prefix
- [ ] `related-skills` paths exist in repository
- [ ] `related-commands` start with /
- [ ] `contributors` lists additional authors (if any)

## Quick Commands

### Validate YAML Syntax
```bash
# Check YAML is valid
python3 -c "import yaml; yaml.safe_load(open('command.yaml'))"

# Pretty print YAML
python3 -c "import yaml; print(yaml.dump(yaml.safe_load(open('command.yaml')), default_flow_style=False))"
```

### Count Fields
```bash
# Count top-level fields
grep -E "^[a-z-]+:" command.yaml | wc -l

# Should be 21+ for required fields
```

### Extract Fields
```bash
# Get all tags
yq '.tags[]' command.yaml

# Get category and subcategory
yq '.category, .subcategory' command.yaml

# Get all related entities
yq '.related-agents[], .related-skills[], .related-commands[]' command.yaml
```

### Validate Patterns
```bash
# Check name is kebab-case
echo "feature-prioritize" | grep -E '^[a-z0-9]+(-[a-z0-9]+)*$'

# Check version is semver
echo "v1.0.0" | grep -E '^v\d+\.\d+\.\d+$'

# Check date format
echo "2025-11-24" | grep -E '^\d{4}-\d{2}-\d{2}$'
```

## Common Mistakes

### ❌ WRONG
```yaml
name: Feature Prioritize  # Not kebab-case
category: Product        # Not lowercase
difficulty: easy         # Not valid enum (use beginner)
time-saved: saves time   # Not quantified
use-cases: "Planning"    # Too generic, not array
examples: []             # Empty (need min 2)
tags: [Good, Useful]     # Not kebab-case
version: 1.0             # Missing 'v' prefix
created: Nov 24, 2025    # Not ISO format
```

### ✅ CORRECT
```yaml
name: feature-prioritize
category: product
difficulty: beginner
time-saved: "2 hours per use"
use-cases:
  - "Prioritizing quarterly roadmap with RICE scores"
  - "Analyzing portfolio balance for strategic planning"
examples:
  - title: "Basic Usage"
    input: "/feature-prioritize features.csv"
    output: "Generated RICE scores for 15 features"
  - title: "Advanced Usage"
    input: "/feature-prioritize features.csv --capacity 20"
    output: "Quarterly roadmap with capacity planning"
tags:
  - product-management
  - feature-planning
  - rice-framework
version: v1.0.0
created: 2025-11-24
```

## JSON Export Example

YAML → JSON transformation:

```yaml
# YAML
name: feature-prioritize
title: Feature Prioritization
category: product
use-cases:
  - "Use case 1"
  - "Use case 2"
```

Becomes:

```json
{
  "core": {
    "name": "feature-prioritize",
    "title": "Feature Prioritization",
    "category": "product"
  },
  "display": {
    "use_cases": [
      "Use case 1",
      "Use case 2"
    ]
  }
}
```

Note: Hyphens become underscores in JSON.

## File Locations

```
Repository Structure:
claude-skills/
├── schema/
│   ├── README.md                        # Overview
│   ├── QUICK_REFERENCE.md              # This file
│   ├── SCHEMA_ARCHITECTURE.md          # Visual diagrams
│   ├── command-metadata-schema.md      # Full spec
│   ├── command-metadata-example.yaml   # Working example
│   └── json-export-schema.json         # JSON schema
└── .claude/
    └── commands/
        └── your-command.md              # Your commands go here
```

## Help & Support

- **Full Spec:** [command-metadata-schema.md](./command-metadata-schema.md)
- **Example:** [command-metadata-example.yaml](./command-metadata-example.yaml)
- **Architecture:** [SCHEMA_ARCHITECTURE.md](./SCHEMA_ARCHITECTURE.md)
- **Issues:** Open GitHub issue with label `schema`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2025-11-24 | Initial schema release |

---

**Quick Reference Version:** 1.0.0
**Schema Version:** 1.0.0
**Last Updated:** November 24, 2025
