# Command Metadata Schema Architecture

**Version:** 1.0.0
**Last Updated:** November 24, 2025

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COMMAND METADATA SCHEMA v1.0.0                    │
│                         (Website-Ready Day 1)                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ 1. CORE IDENTITY (5 required fields)                                │
│    ┌──────────────────────────────────────────────────────────┐    │
│    │ name: feature-prioritize (unique identifier)             │    │
│    │ title: Feature Prioritization with RICE Framework        │    │
│    │ description: One-sentence description (80-120 chars)     │    │
│    │ category: product | marketing | engineering | ...        │    │
│    │ subcategory: feature-planning                            │    │
│    └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2. WEBSITE DISPLAY (4 required fields)                              │
│    ┌──────────────────────────────────────────────────────────┐    │
│    │ difficulty: beginner | intermediate | advanced           │    │
│    │ time-saved: "2-3 hours per prioritization session"       │    │
│    │ frequency: "Weekly per product team"                     │    │
│    │ use-cases: [2-5 concrete scenarios]                      │    │
│    │   - "Prioritizing quarterly roadmap..."                  │    │
│    │   - "Analyzing portfolio balance..."                     │    │
│    └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3. RELATIONSHIPS (3 optional fields)                                │
│    ┌──────────────────────────────────────────────────────────┐    │
│    │ related-agents:                                           │    │
│    │   ├─ cs-product-manager ──────┐                          │    │
│    │   └─ cs-agile-product-owner ──┼─> Cross-Link to Agents  │    │
│    │                                │                          │    │
│    │ related-skills:                │                          │    │
│    │   └─ product-team/toolkit ────┼─> Cross-Link to Skills  │    │
│    │                                │                          │    │
│    │ related-commands:              │                          │    │
│    │   ├─ /feature-analyze ────────┼─> Cross-Link to Commands│    │
│    │   └─ /roadmap-generate ───────┘                          │    │
│    └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 4. TECHNICAL (2 required objects)                                   │
│    ┌──────────────────────────────────────────────────────────┐    │
│    │ dependencies:                                             │    │
│    │   tools: [Read, Write, Bash, Grep, Glob]                │    │
│    │   scripts:                                                │    │
│    │     - product-team/toolkit/scripts/rice_prioritizer.py  │    │
│    │   python-packages: []  # Standard library only           │    │
│    │                                                           │    │
│    │ compatibility:                                            │    │
│    │   claude-ai: true                                        │    │
│    │   claude-code: true                                      │    │
│    │   platforms: [macos, linux, windows]                    │    │
│    └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 5. EXAMPLES (2-5 required)                                          │
│    ┌──────────────────────────────────────────────────────────┐    │
│    │ Example 1: Basic Usage                                    │    │
│    │   input:  "/feature-prioritize features.csv"            │    │
│    │   output: "Generated RICE scores for 15 features..."    │    │
│    │                                                           │    │
│    │ Example 2: Advanced Usage                                │    │
│    │   input:  "/feature-prioritize features.csv --capacity" │    │
│    │   output: "Quarterly roadmap generated..."               │    │
│    └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 6. ANALYTICS (1 required object - placeholder)                      │
│    ┌──────────────────────────────────────────────────────────┐    │
│    │ stats:                                                    │    │
│    │   installs: 0      ─────> Future: Track usage           │    │
│    │   upvotes: 0       ─────> Future: Community voting      │    │
│    │   rating: 0.0      ─────> Future: 0.0-5.0 rating        │    │
│    │   reviews: 0       ─────> Future: Review count          │    │
│    └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 7. VERSIONING (4-5 fields)                                          │
│    ┌──────────────────────────────────────────────────────────┐    │
│    │ version: v1.2.1 (semantic versioning)                    │    │
│    │ author: Claude Skills Team                               │    │
│    │ contributors: [Product Team, Beta Testers] (optional)    │    │
│    │ created: 2025-10-15                                      │    │
│    │ updated: 2025-11-24                                      │    │
│    └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 8. DISCOVERABILITY (4 required fields)                              │
│    ┌──────────────────────────────────────────────────────────┐    │
│    │ tags: [product-management, prioritization, rice, ...]   │    │
│    │   (3-10 kebab-case keywords for search/filter)          │    │
│    │                                                           │    │
│    │ featured: false  (exceptional commands only)             │    │
│    │ verified: true   (official = true, community = false)    │    │
│    │ license: MIT     (SPDX identifier)                       │    │
│    └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Schema Flow

```
YAML Frontmatter                JSON Export                Website
─────────────────          ──────────────────        ──────────────

command.md                 API Response              UI Components
┌──────────┐              ┌──────────┐              ┌──────────┐
│   YAML   │ ──Parse────> │   JSON   │ ──Render──> │  Website │
│Frontmatter│              │  Object  │              │   Pages  │
└──────────┘              └──────────┘              └──────────┘
     │                          │                         │
     │                          │                         │
     ├─ name                    ├─ core.name              ├─ Command card
     ├─ title                   ├─ core.title             ├─ Title/description
     ├─ description             ├─ core.description       ├─ Category badge
     ├─ category                ├─ display.difficulty     ├─ Difficulty badge
     ├─ difficulty              ├─ display.time_saved     ├─ Time saved chip
     ├─ use-cases               ├─ display.use_cases      ├─ Use case list
     ├─ related-agents          ├─ relationships.*        ├─ Related items
     ├─ examples                ├─ examples[]             ├─ Example viewer
     ├─ stats                   ├─ analytics.stats        ├─ Rating/installs
     └─ tags                    └─ discoverability.tags   └─ Tag filters
```

## Website Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         WEBSITE ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 1: DATA SOURCES                                               │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│    │  Commands    │  │   Agents     │  │   Skills     │           │
│    │  *.yaml      │  │   *.md       │  │   SKILL.md   │           │
│    └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│           │                  │                  │                    │
│           └──────────────────┴──────────────────┘                    │
└─────────────────────────────────┬───────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 2: PARSING & VALIDATION                                       │
│    ┌────────────────────────────────────────────────────────┐      │
│    │ YAML Parser → JSON Validator → Schema Validation      │      │
│    └────────────────────────────────────────────────────────┘      │
└─────────────────────────────────┬───────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 3: DATABASE                                                   │
│    ┌────────────────────────────────────────────────────────┐      │
│    │ PostgreSQL / MongoDB                                    │      │
│    │  ├─ commands (main table/collection)                   │      │
│    │  ├─ agents (for cross-referencing)                     │      │
│    │  ├─ skills (for cross-referencing)                     │      │
│    │  ├─ relationships (graph edges)                        │      │
│    │  └─ analytics (stats, trends)                          │      │
│    └────────────────────────────────────────────────────────┘      │
└─────────────────────────────────┬───────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 4: SEARCH & INDEXING                                          │
│    ┌────────────────────────────────────────────────────────┐      │
│    │ ElasticSearch / Algolia / PostgreSQL Full-Text         │      │
│    │  ├─ Full-text search (title, description, use-cases)   │      │
│    │  ├─ Faceted filtering (category, difficulty, tags)     │      │
│    │  ├─ Sorting (rating, installs, updated)                │      │
│    │  └─ Related item suggestions (graph queries)           │      │
│    └────────────────────────────────────────────────────────┘      │
└─────────────────────────────────┬───────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 5: REST API                                                   │
│    ┌────────────────────────────────────────────────────────┐      │
│    │ GET  /api/v1/commands             (list with filters)  │      │
│    │ GET  /api/v1/commands/{name}      (single command)     │      │
│    │ GET  /api/v1/commands/{name}/related (related items)   │      │
│    │ POST /api/v1/commands/search      (advanced search)    │      │
│    │ GET  /api/v1/stats/trending       (trending commands)  │      │
│    │ POST /api/v1/commands/{name}/rate (future: rate)       │      │
│    └────────────────────────────────────────────────────────┘      │
└─────────────────────────────────┬───────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 6: WEBSITE UI                                                 │
│    ┌────────────────────────────────────────────────────────┐      │
│    │ Browse Page                                             │      │
│    │  ├─ Search bar (full-text)                             │      │
│    │  ├─ Category filters (faceted)                         │      │
│    │  ├─ Difficulty badges                                  │      │
│    │  ├─ Sort options (rating, installs, updated)           │      │
│    │  └─ Command cards (grid/list view)                     │      │
│    │                                                         │      │
│    │ Command Detail Page                                    │      │
│    │  ├─ Title, description, badges                         │      │
│    │  ├─ Use cases list                                     │      │
│    │  ├─ Examples with code blocks                          │      │
│    │  ├─ Dependencies and compatibility                     │      │
│    │  ├─ Related agents, skills, commands                   │      │
│    │  ├─ Analytics (installs, rating, reviews)              │      │
│    │  └─ Install/copy button                                │      │
│    │                                                         │      │
│    │ Related Items Sidebar                                  │      │
│    │  ├─ Related agents (with links)                        │      │
│    │  ├─ Related skills (with links)                        │      │
│    │  └─ Related commands (with links)                      │      │
│    └────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
```

## Field Dependencies & Relationships

```
┌─────────────────────────────────────────────────────────────────────┐
│ FIELD RELATIONSHIP MAP                                              │
└─────────────────────────────────────────────────────────────────────┘

category ──────────┐
                   ├──> Determines primary filtering bucket
subcategory ───────┘

tags ──────────────┐
                   ├──> Secondary filtering + full-text search
description ───────┘

difficulty ────────┐
time-saved ────────┤
frequency ─────────┼──> Value proposition cluster
use-cases ─────────┘

related-agents ────┐
related-skills ────┤──> Relationship graph for recommendations
related-commands ──┘

dependencies.tools ────┐
dependencies.scripts ──┼──> Technical requirements validation
compatibility.* ───────┘

examples ──────────────> Usage patterns + documentation

stats ─────────────────> Analytics + trending algorithms

version ───────────────┐
created ───────────────┼──> Change tracking + versioning
updated ───────────────┘

tags + category ───────> Search index configuration

featured + verified ───> Editorial curation + trust signals
```

## Validation Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│ VALIDATION PIPELINE                                                 │
└─────────────────────────────────────────────────────────────────────┘

YAML File
    │
    ▼
┌────────────────────────────────────┐
│ 1. SYNTAX VALIDATION               │
│    ├─ Valid YAML syntax            │
│    ├─ Proper indentation           │
│    └─ No duplicate keys            │
└─────────────┬──────────────────────┘
              ▼
┌────────────────────────────────────┐
│ 2. REQUIRED FIELDS CHECK           │
│    ├─ All 21 required fields       │
│    ├─ Correct field names          │
│    └─ No extra unknown fields      │
└─────────────┬──────────────────────┘
              ▼
┌────────────────────────────────────┐
│ 3. TYPE VALIDATION                 │
│    ├─ Strings are strings          │
│    ├─ Arrays are arrays            │
│    ├─ Objects are objects          │
│    └─ Booleans are booleans        │
└─────────────┬──────────────────────┘
              ▼
┌────────────────────────────────────┐
│ 4. PATTERN MATCHING                │
│    ├─ name: kebab-case             │
│    ├─ version: semver              │
│    ├─ dates: YYYY-MM-DD            │
│    ├─ tags: lowercase kebab-case   │
│    └─ related-*: proper format     │
└─────────────┬──────────────────────┘
              ▼
┌────────────────────────────────────┐
│ 5. CONSTRAINT VALIDATION           │
│    ├─ Min/max lengths              │
│    ├─ Array sizes (2-5, 3-10)      │
│    ├─ Enum values                  │
│    └─ Number ranges                │
└─────────────┬──────────────────────┘
              ▼
┌────────────────────────────────────┐
│ 6. REFERENCE VALIDATION            │
│    ├─ Script paths exist           │
│    ├─ Related agents exist         │
│    ├─ Related skills exist         │
│    └─ Related commands exist       │
└─────────────┬──────────────────────┘
              ▼
┌────────────────────────────────────┐
│ 7. RELATIONSHIP VALIDATION         │
│    ├─ Bidirectional links          │
│    ├─ No circular dependencies     │
│    └─ Valid cross-references       │
└─────────────┬──────────────────────┘
              ▼
┌────────────────────────────────────┐
│ 8. SEMANTIC VALIDATION             │
│    ├─ Use case quality             │
│    ├─ Example realism              │
│    ├─ Tag relevance                │
│    └─ Time saved plausibility      │
└─────────────┬──────────────────────┘
              ▼
       ✅ VALID COMMAND
```

## Schema Evolution Path

```
┌─────────────────────────────────────────────────────────────────────┐
│ SCHEMA EVOLUTION ROADMAP                                            │
└─────────────────────────────────────────────────────────────────────┘

v1.0.0 (CURRENT)
├─ Core schema with 25 fields
├─ Website-ready structure
├─ Analytics placeholder
└─ Documentation complete
    │
    ▼
v1.1.0 (Q1 2026) - COMMUNITY FEATURES
├─ Add: community_ratings object
│   ├─ user_id
│   ├─ rating (1-5)
│   ├─ review_text
│   └─ timestamp
├─ Add: contribution_info object
│   ├─ fork_count
│   ├─ remix_count
│   └─ community_edits
└─ Update: stats with real tracking
    │
    ▼
v1.2.0 (Q2 2026) - ADVANCED ANALYTICS
├─ Add: performance_metrics object
│   ├─ avg_execution_time
│   ├─ success_rate
│   ├─ error_frequency
│   └─ usage_patterns
├─ Add: ab_testing object
│   ├─ variant_id
│   ├─ test_group
│   └─ conversion_metrics
└─ Enhance: analytics with trends
    │
    ▼
v2.0.0 (Q3 2026) - MARKETPLACE
├─ Add: pricing object
│   ├─ tier (free|premium|enterprise)
│   ├─ price
│   └─ billing_frequency
├─ Add: access_control object
│   ├─ visibility
│   ├─ permissions
│   └─ subscription_required
└─ Add: monetization object
    ├─ revenue_share
    └─ payment_provider
```

## Cross-Entity Relationships

```
┌─────────────────────────────────────────────────────────────────────┐
│ ENTITY RELATIONSHIP DIAGRAM                                         │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐        related-commands        ┌──────────────┐
│   COMMAND    │◄───────────────────────────────┤   COMMAND    │
│              │                                 │              │
│ /feature-    │                                 │ /roadmap-    │
│  prioritize  │                                 │  generate    │
└──────┬───────┘                                 └──────────────┘
       │                                                  ▲
       │ related-agents                                  │
       │                                                  │
       ▼                                                  │
┌──────────────┐        uses skills            ┌────────┴──────┐
│    AGENT     │──────────────────────────────>│     SKILL     │
│              │                                │               │
│ cs-product-  │                                │ product-team/ │
│  manager     │                                │  toolkit      │
└──────────────┘                                └───────────────┘
       │                                                  ▲
       │ related-agents                                  │
       │                                                  │
       ▼                                                  │
┌──────────────┐                                         │
│    AGENT     │                                         │
│              │─────────────────────────────────────────┘
│ cs-agile-    │        related-skills
│  product-    │
│  owner       │
└──────────────┘

Legend:
─────>  One-way relationship
◄────>  Bidirectional relationship
```

## Data Flow: YAML to Website

```
┌─────────────────────────────────────────────────────────────────────┐
│ DATA TRANSFORMATION PIPELINE                                        │
└─────────────────────────────────────────────────────────────────────┘

Step 1: Parse YAML
─────────────────
feature-prioritize.yaml
├─ name: feature-prioritize
├─ title: Feature Prioritization...
├─ use-cases: [...]
└─ ...

Step 2: Transform to JSON
──────────────────────────
{
  "metadata": {...},
  "core": {
    "name": "feature-prioritize",
    "title": "Feature Prioritization..."
  },
  "display": {...},
  ...
}

Step 3: Store in Database
──────────────────────────
INSERT INTO commands (
  name, title, description, ...
) VALUES (
  'feature-prioritize', 'Feature...', ...
)

Step 4: Index for Search
─────────────────────────
Elasticsearch Document:
{
  "id": "feature-prioritize",
  "title": "Feature Prioritization...",
  "description": "...",
  "tags": [...],
  "category": "product"
}

Step 5: Render on Website
──────────────────────────
<CommandCard>
  <Title>Feature Prioritization</Title>
  <Badge category="product" />
  <Badge difficulty="intermediate" />
  <Description>...</Description>
  <UseCases>...</UseCases>
</CommandCard>
```

## Performance Considerations

```
┌─────────────────────────────────────────────────────────────────────┐
│ PERFORMANCE & SCALABILITY                                           │
└─────────────────────────────────────────────────────────────────────┘

Database Indexing Strategy
───────────────────────────
PRIMARY INDEX:  name (unique)
INDEX:          category + subcategory (faceted filtering)
INDEX:          tags (array, GIN index for PostgreSQL)
INDEX:          featured, verified (boolean filters)
INDEX:          created, updated (sorting)
INDEX:          stats.rating, stats.installs (sorting)

Full-Text Search Index
──────────────────────
WEIGHTED:       title (weight: 3.0)
WEIGHTED:       description (weight: 2.0)
WEIGHTED:       use-cases (weight: 1.0)
WEIGHTED:       tags (weight: 1.5)

Caching Strategy
────────────────
CACHE:          List all commands (5 min TTL)
CACHE:          Featured commands (10 min TTL)
CACHE:          Trending commands (15 min TTL)
CACHE:          Related items (10 min TTL)
NO CACHE:       Single command detail (always fresh)

API Rate Limiting
─────────────────
LIST:           100 requests/min per IP
DETAIL:         200 requests/min per IP
SEARCH:         50 requests/min per IP (expensive)
TRENDING:       20 requests/min per IP (expensive)
```

---

**Document Version:** 1.0.0
**Last Updated:** November 24, 2025
**Maintainer:** Claude Skills Team
