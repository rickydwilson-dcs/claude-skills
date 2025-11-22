# Architecture Decision Record: Session-Based Output Organization System

**Status:** Proposed
**Date:** 2025-11-22
**Author:** cs-architect
**Repository:** claude-skills
**Branch:** develop

---

## Executive Summary

This ADR proposes migrating from a flat, timestamped file organization system to a session-based output hierarchy that provides user attribution, work context tracking, and integration with Pandora's knowledge management systems (OneDrive/Confluence). The new system addresses critical limitations discovered after 13 outputs were generated: lack of user identification, no work session context, namespace collisions at scale, and unclear lifecycle management.

**Key Decision:** Implement session-based directory structure with YAML metadata, git-tracked outputs, and manual Confluence promotion workflow.

**Impact:** All 27 agents, 50+ anticipated users, 4 teams (Marketing, Product, Engineering, Delivery)

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Architecture Decision](#2-architecture-decision)
3. [Session Directory Structure](#3-session-directory-structure)
4. [Metadata Schema Design](#4-metadata-schema-design)
5. [Implementation Requirements](#5-implementation-requirements)
6. [Manual Confluence Promotion Workflow](#6-manual-confluence-promotion-workflow)
7. [Migration Strategy](#7-migration-strategy)
8. [Testing & Validation](#8-testing--validation)
9. [Appendices](#9-appendices)

---

## 1. Problem Statement

### 1.1 Current System Analysis

**Current Structure:**
```
output/
├── architecture/
├── reviews/
├── analysis/          # 13 files, flat namespace
│   ├── 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
│   ├── 2025-11-19_12-19-45_roadmap-prioritization_cs-product-manager.md
│   └── ...
└── reports/
```

**Naming Convention:**
```
YYYY-MM-DD_HH-MM-SS_<topic>_<agent-name>.md
```

### 1.2 Critical Limitations

#### 1.2.1 No User Attribution
**Problem:** Cannot identify who created outputs or for what purpose.

**Evidence from existing files:**
- `2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md` - Who analyzed the invoice process?
- `2025-11-19_12-19-45_roadmap-prioritization_cs-product-manager.md` - Which PM created this roadmap?

**Impact:**
- Cannot answer "Who worked on the invoice process analysis?"
- No accountability trail for recommendations
- Impossible to contact creators for clarification
- Cannot track individual productivity or contributions

**Scale Problem:** With 50+ users across 4 teams, this becomes critical.

#### 1.2.2 No Work Session Context
**Problem:** Cannot link outputs to feature branches, Jira tickets, or projects.

**Questions we cannot answer:**
- Which feature branch was active when this analysis was created?
- What Jira ticket is this output associated with?
- Is this part of a sprint, release, or one-off investigation?
- Who are the stakeholders for this work?

**Impact:**
- Outputs become orphaned over time
- Cannot reconstruct decision-making context
- Difficult to find related outputs (e.g., "show me all business-analyst outputs for the invoice automation project")
- No integration path to Pandora's project tracking systems

#### 1.2.3 Flat Namespace Collision
**Problem:** All outputs stored in category-only directories causes collisions at scale.

**Current collision risk:**
```
output/analysis/
├── 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md  # User A
├── 2025-11-22_07-15-22_invoice-process-analysis_cs-business-analyst.md  # User B (same day!)
└── 2025-11-22_14-30-10_invoice-process-analysis_cs-business-analyst.md  # User A (iteration 2)
```

**Which is the "correct" analysis?**
- Timestamp alone doesn't provide context
- No way to distinguish between users
- Cannot tell if these are iterations or competing analyses

**Scale Problem:** With 50 users × 27 agents × 4 categories = potential for thousands of files in single directories.

#### 1.2.4 No Lifecycle Management
**Problem:** Unclear what to keep, promote to Confluence, or delete.

**Current README.md suggests:**
```bash
# Remove reports older than 30 days
find output/ -name "*.md" -mtime +30 -delete
```

**Questions:**
- Which outputs are "important" and should be preserved?
- Which have been promoted to Confluence?
- Which are drafts vs. final versions?
- When is it safe to delete?

**Impact:**
- Risk deleting work-in-progress before promotion
- No tracking of what's been shared with stakeholders
- Cannot implement retention policies (e.g., keep sprint planning outputs for 6 months, ad-hoc analyses for 30 days)

#### 1.2.5 No Integration Path
**Problem:** No documented workflow for promoting outputs to Pandora's systems.

**Pandora's Knowledge Management:**
- **OneDrive:** Team-level file storage (Marketing, Product, Engineering, Delivery)
- **Confluence:** Project documentation, decision records, meeting notes
- **Jira:** Ticket attachments, sprint artifacts

**Current system cannot:**
- Track which outputs have been promoted
- Maintain links between git repository and Confluence pages
- Provide search across both systems
- Support team-specific organization

### 1.3 Scale Analysis

**Current State:**
- 27 agents
- 13 outputs generated (small sample)
- 1 primary user (rickydwilson-dcs)

**Target State (6 months):**
- 27 agents
- 50+ users across 4 teams
- 10 outputs/user/week = 500 outputs/week = 26,000 outputs/year

**Collision Probability:**
With flat namespace and timestamp-only differentiation:
- Same-second collision: Low (but possible with automation)
- Same-topic-same-day collision: HIGH (multiple users analyzing same feature)
- Same-category collision: CERTAIN (hundreds of analysis files in single directory)

**Search Performance:**
- 26,000 files in 4 directories = 6,500 files per directory
- `ls output/analysis/` becomes unusable
- `grep` searches become slow
- Git performance degrades with large flat directories

### 1.4 Requirements for New System

Based on limitations analysis, the new system must provide:

1. **User Attribution** - Every output linked to creator (git user identity)
2. **Session Context** - Link outputs to feature branches, tickets, projects, teams
3. **Namespace Isolation** - Prevent collisions between users and sessions
4. **Lifecycle Tracking** - Metadata for status (draft/final), promotion tracking, retention
5. **Integration Path** - Manual workflow for Confluence promotion with bidirectional links
6. **Backward Compatibility** - Migrate existing 13 outputs without data loss
7. **Git-Tracked** - All sessions committed (NOT gitignored) for history preservation
8. **Team Organization** - Support Marketing, Product, Engineering, Delivery team separation
9. **Scalability** - Support 50+ users, 500+ outputs/week without degradation
10. **Developer Experience** - Simple Python utilities for session creation and management

---

## 2. Architecture Decision

### 2.1 Options Considered

#### Option 1: Session-Based Hierarchy (RECOMMENDED)
```
output/
├── sessions/
│   ├── {user}/
│   │   ├── {session-id}/
│   │   │   ├── .session-metadata.yaml
│   │   │   ├── architecture/
│   │   │   ├── analysis/
│   │   │   ├── reviews/
│   │   │   └── reports/
│   └── ...
└── shared/
    ├── promoted-to-confluence/
    └── team-resources/
```

**Pros:**
- Complete user and session isolation
- All context captured in metadata
- Scalable to thousands of sessions
- Clear lifecycle management
- Git-tracked with full history
- Supports multi-team organization

**Cons:**
- Deeper directory nesting (4-5 levels)
- Requires Python utilities for session management
- Migration effort for existing outputs
- Learning curve for new structure

#### Option 2: Enhanced Flat Structure (Current + Metadata)
```
output/
├── architecture/
│   ├── 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
│   └── 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.yaml
├── analysis/
└── ...
```

**Pros:**
- Minimal disruption to current system
- No directory restructuring needed
- Simpler implementation

**Cons:**
- Does NOT solve namespace collision problem
- Does NOT provide session-based organization
- Metadata files double the file count
- Still difficult to find related outputs
- Does NOT scale to 50+ users

#### Option 3: Database-Backed System
Use SQLite database to track metadata with files stored by hash.

**Pros:**
- Powerful querying capabilities
- Excellent scalability

**Cons:**
- Requires database management
- Breaks git-based workflow
- Not portable (database file conflicts in git)
- Overly complex for the use case
- Violates "simple skills library" philosophy

### 2.2 Decision: Session-Based Hierarchy

**Selected:** Option 1 - Session-Based Hierarchy

**Rationale:**

1. **Solves All Five Limitations:**
   - User attribution: User directory level
   - Session context: Session-level metadata
   - Namespace isolation: User/session/category hierarchy
   - Lifecycle management: Metadata status and promotion tracking
   - Integration path: Shared/promoted-to-confluence directory

2. **Scalability:**
   - 50 users × 20 sessions/user = 1,000 session directories
   - Each session contains 1-20 outputs in categorized subdirectories
   - No single directory exceeds 100 files
   - `ls` and `grep` remain performant

3. **Git-Friendly:**
   - Each session is a commit-worthy unit of work
   - Clear boundaries for feature branch → develop → main promotion
   - Session directories map naturally to feature branches
   - Metadata files are small YAML (git-friendly format)

4. **Team Organization:**
   - User directories naturally group by team (git user naming conventions)
   - Shared directory provides cross-team resources
   - Metadata captures team affiliation explicitly

5. **Developer Experience:**
   - Python utilities abstract complexity
   - Simple commands: `create-session`, `close-session`, `list-sessions`
   - Agents can automatically infer context from git

6. **Pandora Integration:**
   - Session metadata includes Confluence links
   - Promoted outputs copied to shared/promoted-to-confluence/
   - Clear audit trail of what's been shared

### 2.3 Trade-offs Accepted

1. **Deeper Nesting:** 4-5 directory levels vs. 2 levels
   - **Mitigation:** Python utilities provide shortcuts
   - **Benefit:** Outweighed by organization gains

2. **Migration Effort:** Must migrate 13 existing outputs
   - **Mitigation:** One-time migration script
   - **Benefit:** Clean slate for scalable future

3. **Learning Curve:** New structure for users to learn
   - **Mitigation:** Comprehensive documentation + CLI utilities
   - **Benefit:** Self-documenting structure once learned

4. **Python Dependency:** Requires Python utilities
   - **Mitigation:** Python already required (53 existing tools)
   - **Benefit:** Consistent with repository patterns

---

## 3. Session Directory Structure

### 3.1 Complete Hierarchy

```
output/
├── sessions/                                    # All user session outputs
│   ├── {user}/                                  # User identity (git user.name, sanitized)
│   │   ├── {session-id}/                        # Unique session identifier
│   │   │   ├── .session-metadata.yaml           # Session context and tracking
│   │   │   ├── architecture/                    # Architecture outputs for this session
│   │   │   │   └── {timestamp}_{topic}_{agent}.md
│   │   │   ├── analysis/                        # Analysis outputs for this session
│   │   │   │   └── {timestamp}_{topic}_{agent}.md
│   │   │   ├── reviews/                         # Review outputs for this session
│   │   │   │   └── {timestamp}_{topic}_{agent}.md
│   │   │   ├── reports/                         # Report outputs for this session
│   │   │   │   └── {timestamp}_{topic}_{agent}.md
│   │   │   └── artifacts/                       # Supporting files (JSON, diagrams, CSVs)
│   │   │       └── {timestamp}_{artifact-name}.{ext}
│   │   ├── {another-session-id}/
│   │   └── ...
│   ├── {another-user}/
│   └── ...
├── shared/                                      # Cross-user shared resources
│   ├── promoted-to-confluence/                  # Outputs promoted to Confluence
│   │   ├── {space-key}/                         # Confluence space (e.g., PROD, ENG, MKT)
│   │   │   ├── {page-id}/                       # Confluence page ID
│   │   │   │   ├── .promotion-metadata.yaml     # Promotion details
│   │   │   │   └── {filename}.md                # Copy of promoted output
│   │   │   └── ...
│   │   └── ...
│   ├── team-resources/                          # Team-level shared resources
│   │   ├── marketing/
│   │   ├── product/
│   │   ├── engineering/
│   │   └── delivery/
│   └── templates/                               # Output templates (optional)
│       ├── architecture-review-template.md
│       ├── code-review-template.md
│       └── ...
└── README.md                                    # Updated system documentation
```

### 3.2 Naming Conventions

#### 3.2.1 User Directory (`{user}`)

**Format:** Sanitized git user name (lowercase, hyphens, alphanumeric only)

**Examples:**
```
rickydwilson-dcs              # From: rickydwilson-dcs
sarah-chen                    # From: Sarah Chen
john-smith-eng                # From: John Smith (Engineering)
```

**Generation Rule:**
```python
import re

def sanitize_username(git_user_name: str) -> str:
    """Convert git user.name to directory-safe format."""
    # Lowercase, replace spaces/underscores with hyphens, remove special chars
    sanitized = git_user_name.lower()
    sanitized = re.sub(r'[\s_]+', '-', sanitized)
    sanitized = re.sub(r'[^a-z0-9-]', '', sanitized)
    sanitized = re.sub(r'-+', '-', sanitized)  # Collapse multiple hyphens
    sanitized = sanitized.strip('-')
    return sanitized or 'unknown-user'

# Examples:
# "rickydwilson-dcs" → "rickydwilson-dcs"
# "Sarah Chen" → "sarah-chen"
# "John_Smith (Engineering)" → "john-smith-engineering"
```

**User Lookup:**
```bash
git config user.name  # Returns: "rickydwilson-dcs"
```

#### 3.2.2 Session ID (`{session-id}`)

**Format:** `{YYYY-MM-DD}_{branch-slug}_{short-hash}`

**Components:**
1. **Date:** Session creation date (YYYY-MM-DD)
2. **Branch Slug:** Current git branch (sanitized, max 30 chars)
3. **Short Hash:** 6-character random hex for uniqueness

**Examples:**
```
2025-11-22_feature-invoice-automation_a3f42c
2025-11-22_bugfix-auth-timeout_7b89de
2025-11-22_spike-new-payment-gateway_c19f03
2025-11-22_develop_8e4a21
```

**Generation Rule:**
```python
import re
import secrets
from datetime import datetime

def generate_session_id(branch_name: str) -> str:
    """Generate unique session identifier."""
    # Get current date
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Sanitize branch name
    branch_slug = branch_name.lower()
    branch_slug = re.sub(r'[^a-z0-9-]', '-', branch_slug)
    branch_slug = re.sub(r'-+', '-', branch_slug)
    branch_slug = branch_slug.strip('-')
    branch_slug = branch_slug[:30]  # Limit length

    # Generate random hash
    short_hash = secrets.token_hex(3)  # 6 characters

    return f"{date_str}_{branch_slug}_{short_hash}"

# Examples:
# "feature/invoice-automation" → "2025-11-22_feature-invoice-automation_a3f42c"
# "bugfix/auth-timeout" → "2025-11-22_bugfix-auth-timeout_7b89de"
```

**Branch Lookup:**
```bash
git rev-parse --abbrev-ref HEAD  # Returns: "feature/invoice-automation"
```

#### 3.2.3 Output Filenames (within session)

**Format:** `{YYYY-MM-DD}_{HH-MM-SS}_{topic}_{agent-name}.md`

**No change from current system** - timestamps remain within session for:
- Chronological ordering within session
- Multiple outputs from same agent in one session
- Compatibility with existing agent output patterns

**Examples within session:**
```
2025-11-22_feature-invoice-automation_a3f42c/
├── analysis/
│   ├── 2025-11-22_08-15-30_invoice-process-analysis_cs-business-analyst.md
│   └── 2025-11-22_14-22-10_revised-analysis_cs-business-analyst.md
├── architecture/
│   └── 2025-11-22_09-45-00_system-architecture_cs-architect.md
└── reports/
    └── 2025-11-22_16-00-00_executive-summary_cs-business-analyst.md
```

### 3.3 Example: Multi-User, Multi-Team Scenario

**Scenario:** Pandora's invoice automation project with 3 users across 2 teams

```
output/
├── sessions/
│   ├── rickydwilson-dcs/                        # Technical Lead (Engineering)
│   │   ├── 2025-11-22_feature-invoice-automation_a3f42c/
│   │   │   ├── .session-metadata.yaml
│   │   │   │   # team: engineering
│   │   │   │   # ticket: PROJ-123
│   │   │   │   # project: Invoice Automation
│   │   │   ├── architecture/
│   │   │   │   └── 2025-11-22_09-45-00_system-architecture_cs-architect.md
│   │   │   └── analysis/
│   │   │       └── 2025-11-22_10-30-00_tech-stack-evaluation_cs-cto-advisor.md
│   │   └── 2025-11-23_spike-ocr-integration_b8d39e/
│   │       └── ...
│   ├── sarah-chen/                              # Product Manager (Product Team)
│   │   └── 2025-11-22_feature-invoice-automation_c4f88a/
│   │       ├── .session-metadata.yaml
│   │       │   # team: product
│   │       │   # ticket: PROJ-123
│   │       │   # project: Invoice Automation
│   │       ├── analysis/
│   │       │   ├── 2025-11-22_08-00-00_user-stories_cs-product-manager.md
│   │       │   └── 2025-11-22_11-15-00_roadmap-prioritization_cs-product-manager.md
│   │       └── reports/
│   │           └── 2025-11-22_15-30-00_sprint-planning_cs-agile-product-owner.md
│   └── mike-johnson/                            # Business Analyst (Delivery Team)
│       └── 2025-11-22_feature-invoice-automation_d9e21f/
│           ├── .session-metadata.yaml
│           │   # team: delivery
│           │   # ticket: PROJ-123
│           │   # project: Invoice Automation
│           ├── analysis/
│           │   ├── 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
│           │   └── 2025-11-22_07-00-00_stakeholder-mapping_cs-business-analyst.json
│           └── reports/
│               └── 2025-11-22_16-00-00_executive-recommendations_cs-business-analyst.md
├── shared/
│   ├── promoted-to-confluence/
│   │   └── PROJ/                                # Project space
│   │       └── 123456/                          # Page ID
│   │           ├── .promotion-metadata.yaml
│   │           └── invoice-process-analysis.md  # Promoted from mike-johnson session
│   └── team-resources/
│       ├── product/
│       │   └── sprint-planning-template.md
│       └── engineering/
│           └── architecture-review-checklist.md
└── README.md
```

**Key Benefits Illustrated:**

1. **User Isolation:** 3 users work on same project without file collisions
2. **Session Uniqueness:** Each user has unique session ID (different hash) even on same branch/day
3. **Team Attribution:** Metadata clearly shows team affiliation
4. **Project Linking:** All sessions link to PROJ-123 via metadata
5. **Shared Resources:** Promoted outputs in centralized location
6. **Searchability:**
   ```bash
   # Find all outputs for PROJ-123
   grep -r "ticket: PROJ-123" output/sessions/*/*/. session-metadata.yaml

   # Find all business analyst outputs
   find output/sessions -name "*_cs-business-analyst.md"

   # Find all outputs by mike-johnson
   ls output/sessions/mike-johnson/
   ```

### 3.4 Collision Prevention

**Scenario: Same user, same branch, same day, multiple sessions**

**Problem:** User wants to start fresh session after closing previous one.

**Solution: Random short hash ensures uniqueness:**
```
output/sessions/rickydwilson-dcs/
├── 2025-11-22_feature-invoice-automation_a3f42c/   # Session 1 (morning work)
├── 2025-11-22_feature-invoice-automation_f7b91d/   # Session 2 (afternoon work)
└── 2025-11-22_feature-invoice-automation_c8e43a/   # Session 3 (evening work)
```

**Collision Probability:**
- 6-character hex = 16^6 = 16,777,216 possible combinations
- Birthday paradox: 50% collision after ~4,800 sessions
- Per-user collision: 50% after 4,800 sessions by SAME USER on SAME BRANCH on SAME DAY
- **Verdict:** Negligible risk (average user creates 2-5 sessions per day)

**Mitigation if collision occurs:**
- Session creation script checks for existing directory
- If collision detected (rare), regenerate hash
- Log warning for monitoring

---

## 4. Metadata Schema Design

### 4.1 Session Metadata Schema

**File:** `.session-metadata.yaml` (stored in each session directory)

**Purpose:** Capture all context needed for:
- User attribution
- Work context (branch, ticket, project)
- Lifecycle tracking (status, retention, promotion)
- Team organization
- Stakeholder communication

#### 4.1.1 Complete Schema

```yaml
# Session Identity
session_id: "2025-11-22_feature-invoice-automation_a3f42c"
created_at: "2025-11-22T08:00:00Z"
created_by:
  user: "rickydwilson-dcs"
  email: "webmaster@digitalconsultingservices.co.uk"
  team: "engineering"

# Work Context
context:
  branch: "feature/invoice-automation"
  ticket: "PROJ-123"  # Jira ticket
  project: "Invoice Automation System"
  sprint: "2025-Q4-Sprint-3"  # Optional
  epic: "PROJ-100"  # Optional
  release: "v2.1.0"  # Optional

# Session Status
status:
  current: "active"  # active | closed | archived
  closed_at: null  # Set when session closed
  archived_at: null  # Set when moved to archive

# Outputs Tracking
outputs:
  - file: "analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md"
    agent: "cs-business-analyst"
    type: "analysis"
    created_at: "2025-11-22T06:58:38Z"
    promoted: false
    promoted_to: null
  - file: "architecture/2025-11-22_09-45-00_system-architecture_cs-architect.md"
    agent: "cs-architect"
    type: "architecture"
    created_at: "2025-11-22T09:45:00Z"
    promoted: true
    promoted_to: "confluence://PROJ/123456"

# Stakeholders
stakeholders:
  - name: "Sarah Chen"
    role: "Product Manager"
    email: "sarah.chen@pandora.com"
  - name: "Mike Johnson"
    role: "Business Analyst"
    email: "mike.johnson@pandora.com"

# Retention Policy
retention:
  policy: "project"  # project | sprint | temporary
  expires_at: "2026-05-22"  # 6 months from creation
  reason: "Project documentation - retain until post-launch retrospective"

# Integration Links
links:
  jira: "https://pandora.atlassian.net/browse/PROJ-123"
  confluence: "https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456"
  onedrive: "https://pandora.sharepoint.com/sites/Engineering/InvoiceAutomation"
  github_pr: "https://github.com/pandora/invoice-system/pull/42"

# Tags for searchability
tags:
  - "invoice-automation"
  - "process-improvement"
  - "business-analysis"
  - "architecture"

# Notes (free-form)
notes: |
  Initial analysis session for invoice automation project.
  Stakeholder walkthrough meeting on 2025-11-22 revealed significant
  pain points in current manual process. This session captures
  process analysis, architecture design, and executive recommendations.
```

#### 4.1.2 Field Definitions

##### Session Identity
- **session_id**: Unique identifier (matches directory name)
- **created_at**: ISO 8601 timestamp (UTC) when session created
- **created_by.user**: Git user.name (sanitized to match directory name)
- **created_by.email**: Git user.email
- **created_by.team**: Team affiliation (marketing | product | engineering | delivery)

##### Work Context
- **context.branch**: Git branch name (feature/*, bugfix/*, develop, etc.)
- **context.ticket**: Jira ticket ID (REQUIRED for feature work, optional for spikes)
- **context.project**: Human-readable project name
- **context.sprint**: Sprint identifier (optional, for Scrum teams)
- **context.epic**: Parent epic ticket (optional)
- **context.release**: Target release version (optional)

##### Session Status
- **status.current**: Enum: `active` | `closed` | `archived`
  - `active`: Session in progress, outputs being added
  - `closed`: Work complete, no more outputs expected
  - `archived`: Moved to archive (if implemented), metadata preserved
- **status.closed_at**: Timestamp when session closed
- **status.archived_at**: Timestamp when session archived

##### Outputs Tracking
Array of all outputs generated in this session:
- **file**: Relative path from session directory
- **agent**: Agent that created output (cs-* name)
- **type**: Category (architecture | analysis | reviews | reports | artifacts)
- **created_at**: Output creation timestamp
- **promoted**: Boolean - has this been promoted to Confluence?
- **promoted_to**: Confluence URL or null

##### Stakeholders
Array of people involved or notified:
- **name**: Full name
- **role**: Job title or role in project
- **email**: Email address

##### Retention Policy
- **retention.policy**: Enum: `project` | `sprint` | `temporary`
  - `project`: Keep until project complete + retrospective (default 6 months)
  - `sprint`: Keep until sprint complete + 1 sprint (default 3 weeks)
  - `temporary`: Ad-hoc analysis (default 30 days)
- **retention.expires_at**: ISO 8601 date when eligible for deletion
- **retention.reason**: Human-readable explanation

##### Integration Links
- **links.jira**: Direct link to Jira ticket
- **links.confluence**: Direct link to Confluence page
- **links.onedrive**: OneDrive folder/file link
- **links.github_pr**: GitHub pull request link

##### Tags
Array of searchable keywords (kebab-case)

##### Notes
Free-form markdown text for additional context

#### 4.1.3 Minimal Required Schema

For quick session creation, only these fields are REQUIRED:

```yaml
session_id: "2025-11-22_feature-invoice-automation_a3f42c"
created_at: "2025-11-22T08:00:00Z"
created_by:
  user: "rickydwilson-dcs"
  email: "webmaster@digitalconsultingservices.co.uk"
  team: "engineering"
context:
  branch: "feature/invoice-automation"
  ticket: "PROJ-123"  # Optional for spikes/experiments
  project: "Invoice Automation System"
status:
  current: "active"
outputs: []
retention:
  policy: "project"
  expires_at: "2026-05-22"
```

All other fields are optional and can be populated over time.

### 4.2 Promotion Metadata Schema

**File:** `.promotion-metadata.yaml` (stored in shared/promoted-to-confluence/{space}/{page}/)

**Purpose:** Track what has been promoted to Confluence, when, and by whom.

```yaml
# Promotion Details
promoted_at: "2025-11-22T16:00:00Z"
promoted_by:
  user: "rickydwilson-dcs"
  email: "webmaster@digitalconsultingservices.co.uk"

# Source Information
source:
  session_id: "2025-11-22_feature-invoice-automation_a3f42c"
  user: "mike-johnson"  # Original creator
  file: "analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md"
  agent: "cs-business-analyst"

# Confluence Details
confluence:
  space_key: "PROJ"
  space_name: "Project Documentation"
  page_id: "123456"
  page_title: "Invoice Process Analysis - November 2025"
  page_url: "https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456"
  parent_page_id: "100000"  # Optional
  version: 1  # Page version after promotion

# Distribution
notified:
  - "sarah.chen@pandora.com"
  - "mike.johnson@pandora.com"
  - "exec-team@pandora.com"

# Notes
notes: |
  Promoted to Confluence for stakeholder review.
  This analysis formed the basis for the invoice automation project approval.
```

### 4.3 Metadata Usage Examples

#### 4.3.1 Creating a Session
```bash
# Python utility creates session and metadata
python3 tools/session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Automation System"

# Output:
# ✅ Session created: output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
# 📝 Metadata: output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/.session-metadata.yaml
# 🔗 Current session set to: 2025-11-22_feature-invoice-automation_a3f42c
```

#### 4.3.2 Adding an Output
```bash
# Agent generates output (automatically registered)
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py \
  transcript.md \
  --output $CLAUDE_SESSION_DIR/analysis/

# session_manager.py automatically updates metadata:
# outputs:
#   - file: "analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md"
#     agent: "cs-business-analyst"
#     type: "analysis"
#     created_at: "2025-11-22T06:58:38Z"
#     promoted: false
```

#### 4.3.3 Searching Sessions
```bash
# Find all sessions for ticket PROJ-123
python3 tools/session_manager.py search --ticket PROJ-123

# Output:
# Found 3 sessions for ticket PROJ-123:
# 1. rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c (active)
# 2. sarah-chen/2025-11-22_feature-invoice-automation_c4f88a (closed)
# 3. mike-johnson/2025-11-22_feature-invoice-automation_d9e21f (active)

# Find all outputs by agent
python3 tools/session_manager.py search --agent cs-business-analyst

# Find all sessions expiring in 30 days
python3 tools/session_manager.py search --expiring-within 30
```

#### 4.3.4 Closing a Session
```bash
# Close session when work complete
python3 tools/session_manager.py close

# Updates metadata:
# status:
#   current: "closed"
#   closed_at: "2025-11-22T18:00:00Z"
```

---

## 5. Implementation Requirements

### 5.1 Python Utilities

#### 5.1.1 Core Utility: `tools/session_manager.py`

**Purpose:** Central CLI tool for session lifecycle management

**Commands:**
```bash
# Create new session
session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Automation" \
  [--team engineering] \
  [--retention project] \
  [--stakeholder "Sarah Chen <sarah@pandora.com>"]

# List sessions
session_manager.py list \
  [--user rickydwilson-dcs] \
  [--status active] \
  [--team engineering]

# Get current active session
session_manager.py current

# Set active session (for agent outputs)
session_manager.py use {session-id}

# Add output to current session (called by agents)
session_manager.py add-output \
  --file analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md \
  --agent cs-business-analyst \
  --type analysis

# Search sessions
session_manager.py search \
  [--ticket PROJ-123] \
  [--project "Invoice Automation"] \
  [--agent cs-business-analyst] \
  [--tag invoice-automation] \
  [--expiring-within 30]

# Close session
session_manager.py close [session-id]

# Archive old sessions
session_manager.py archive [session-id]

# Generate session report
session_manager.py report {session-id} \
  [--format markdown|json]
```

**Implementation Notes:**
- Uses Python standard library only (os, pathlib, yaml, datetime, secrets)
- Stores current session ID in `.current-session` file in output/ directory
- Agents read `CLAUDE_SESSION_DIR` environment variable (set by session_manager)
- Validates metadata schema on create/update
- Provides helpful error messages with suggestions

#### 5.1.2 Migration Utility: `tools/migrate_outputs.py`

**Purpose:** One-time migration of existing 13 outputs to new structure

**Command:**
```bash
# Migrate all existing outputs
python3 tools/migrate_outputs.py \
  --dry-run  # Preview migration without changes

python3 tools/migrate_outputs.py \
  --execute  # Perform migration

# Options:
# --user rickydwilson-dcs       # Override detected git user
# --default-ticket PROJ-999     # Default ticket for outputs without context
# --default-project "Legacy"    # Default project name
```

**Migration Logic:**

1. **Scan existing outputs:**
   ```
   output/
   ├── analysis/
   │   ├── 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
   │   └── ...
   ```

2. **Extract metadata from filename:**
   - Timestamp → `created_at`
   - Topic → `project` (best guess) and `tags`
   - Agent → `agent`

3. **Create migration session for each user:**
   ```
   output/sessions/rickydwilson-dcs/
   └── 2025-11-22_migration-legacy-outputs_000000/
       ├── .session-metadata.yaml
       │   # project: "Legacy Outputs Migration"
       │   # ticket: "MIGRATION-001"
       │   # retention: temporary (30 days)
       ├── analysis/
       │   └── 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
       └── ...
   ```

4. **Handle unknowns:**
   - User: Use current git user.name (or --user flag)
   - Team: Use "unknown" (can be updated later)
   - Ticket: Use "MIGRATION-001" (or --default-ticket flag)
   - Project: Use "Legacy Outputs Migration" (or --default-project flag)

5. **Generate migration report:**
   ```markdown
   # Migration Report

   ## Summary
   - Total outputs migrated: 13
   - Users identified: 1 (rickydwilson-dcs)
   - Sessions created: 1 (migration session)
   - Errors: 0

   ## Migrated Outputs

   ### rickydwilson-dcs / 2025-11-22_migration-legacy-outputs_000000

   1. analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
      - Agent: cs-business-analyst
      - Original: output/analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md

   [... list continues ...]

   ## Next Steps

   1. Review migration session metadata: output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/.session-metadata.yaml
   2. Update ticket/project fields if known
   3. Promote important outputs to Confluence
   4. Archive or delete legacy migration session after 30 days
   ```

6. **Backup original structure:**
   ```bash
   # Before migration, create backup
   cp -r output/ output.backup-2025-11-22/
   ```

**Dry-Run Output:**
```
🔍 Scanning existing outputs...
   Found 13 outputs in 4 categories

📊 Migration Plan:

   User: rickydwilson-dcs
   Session: 2025-11-22_migration-legacy-outputs_000000

   To Migrate:
   ✓ analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
   ✓ analysis/2025-11-19_12-19-45_roadmap-prioritization_cs-product-manager.md
   [... 11 more ...]

   New Structure:
   output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/
   ├── .session-metadata.yaml
   ├── analysis/ (10 files)
   ├── architecture/ (2 files)
   └── reports/ (1 file)

⚠️  Dry-run mode - no changes made
🔁 Run with --execute to perform migration
💾 Backup will be created: output.backup-2025-11-22/
```

#### 5.1.3 Promotion Utility: `tools/promote_to_confluence.py`

**Purpose:** Track Confluence promotions and copy outputs to shared directory

**Command:**
```bash
# Promote output to Confluence
python3 tools/promote_to_confluence.py \
  --session {session-id} \
  --file analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md \
  --confluence-url "https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456" \
  [--notify "sarah.chen@pandora.com,mike.johnson@pandora.com"]

# Output:
# ✅ Output promoted to Confluence
# 📋 Copied to: output/shared/promoted-to-confluence/PROJ/123456/invoice-process-analysis.md
# 📝 Metadata: output/shared/promoted-to-confluence/PROJ/123456/.promotion-metadata.yaml
# 🔗 Session metadata updated
# ✉️  Notifications sent to: sarah.chen@pandora.com, mike.johnson@pandora.com
```

**Implementation Notes:**
- Does NOT automatically upload to Confluence (manual copy-paste for now)
- Copies file to shared/promoted-to-confluence/ directory
- Creates .promotion-metadata.yaml
- Updates session metadata (promoted: true, promoted_to: URL)
- Optionally sends notification emails (requires SMTP configuration)

### 5.2 Agent Integration Updates

**Change Required:** Agents must write outputs to current session directory

#### 5.2.1 Current Agent Pattern
```bash
# Current: Agents write directly to output/category/
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py \
  transcript.md \
  > output/analysis/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.md
```

#### 5.2.2 New Agent Pattern (Option 1: Environment Variable)
```bash
# New: Agents write to $CLAUDE_SESSION_DIR (set by session_manager)
export CLAUDE_SESSION_DIR="output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py \
  transcript.md \
  > ${CLAUDE_SESSION_DIR}/analysis/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.md

# Session manager automatically registers output in metadata
```

#### 5.2.3 New Agent Pattern (Option 2: Wrapper Script)
```bash
# Wrapper script handles session directory
python3 tools/agent_runner.py cs-business-analyst process_analyzer.py transcript.md

# agent_runner.py:
# 1. Gets current session from .current-session
# 2. Sets CLAUDE_SESSION_DIR environment variable
# 3. Runs agent script
# 4. Registers output in session metadata
```

**Recommended:** Option 1 (environment variable) for simplicity

#### 5.2.4 Agent Documentation Updates

Each agent's SKILL.md must be updated with new output pattern:

```markdown
## Workflow: Process Analysis

### Setup Session
```bash
# Create session for this work
python3 tools/session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Automation"

# Session directory automatically set in $CLAUDE_SESSION_DIR
```

### Run Analysis
```bash
# Generate analysis (outputs to current session)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py \
  transcript.md \
  > ${CLAUDE_SESSION_DIR}/analysis/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.md
```

### Review Output
```bash
# View session outputs
python3 tools/session_manager.py report
```
```

### 5.3 Git Configuration Changes

#### 5.3.1 Update .gitignore

**Current:**
```
# .gitignore (relevant section)
output/*
```

**New:**
```
# .gitignore (updated)
# Output directory - SESSION-BASED (git-tracked by default)
# Only ignore temporary files and working directories
output/.current-session
output/**/.DS_Store
output/**/tmp/
output/**/*.swp
output/**/*.swo
output/**/*.bak

# Legacy output structure (if migration incomplete)
output/architecture/*.md
output/analysis/*.md
output/reviews/*.md
output/reports/*.md
```

**Rationale:**
- Sessions ARE git-tracked (intentional design decision)
- Only ignore ephemeral files (.DS_Store, vim swaps, etc.)
- Legacy flat structure ignored during migration period

#### 5.3.2 Git Commit Pattern

**Session Creation:**
```bash
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
git commit -m "feat(sessions): create session for invoice automation analysis

- Ticket: PROJ-123
- Project: Invoice Automation System
- Team: Engineering"
```

**Adding Outputs to Session:**
```bash
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/analysis/
git commit -m "docs(analysis): add invoice process analysis

- Agent: cs-business-analyst
- Session: 2025-11-22_feature-invoice-automation_a3f42c
- Output: invoice-process-analysis_cs-business-analyst.md"
```

**Closing Session:**
```bash
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/.session-metadata.yaml
git commit -m "feat(sessions): close invoice automation analysis session

- Total outputs: 4
- Promoted to Confluence: 2
- Status: closed"
```

### 5.4 Documentation Updates

#### 5.4.1 Update output/README.md
- Replace current content with session-based system documentation
- Include Python utility usage examples
- Add search and discovery patterns
- Document promotion workflow

#### 5.4.2 Update CLAUDE.md (Repository Root)
- Update "Agent Output Directory" section
- Reference new session-based system
- Add quickstart examples

#### 5.4.3 Update agents/CLAUDE.md
- Update agent output pattern examples
- Document $CLAUDE_SESSION_DIR usage
- Add session creation step to workflow templates

#### 5.4.4 Create New Docs
- `docs/sessions/SESSION_GUIDE.md` - Comprehensive session management guide
- `docs/sessions/PROMOTION_WORKFLOW.md` - Confluence promotion process
- `docs/sessions/MIGRATION_GUIDE.md` - Legacy output migration instructions

### 5.5 Testing & Validation Requirements

See [Section 8: Testing & Validation](#8-testing--validation) for complete test plan.

---

## 6. Manual Confluence Promotion Workflow

### 6.1 Workflow Overview

**Design Principle:** Manual promotion maintains control and quality. Automatic promotion risks:
- Publishing draft/incomplete work
- Breaking Confluence page structure
- Losing formatting/context
- Overwriting collaborative edits

**Process:** Human reviews, enhances, and manually copies to Confluence, then tracks promotion in git.

### 6.2 Step-by-Step Process

#### Step 1: Identify Output for Promotion

**Criteria for Promotion:**
- Output is finalized (not draft)
- Stakeholders need access (broader than just git users)
- Content has long-term value (not ephemeral analysis)
- Needs discoverability in Confluence search

**Example:**
```bash
# Review session outputs
python3 tools/session_manager.py report

# Output:
# Session: 2025-11-22_feature-invoice-automation_a3f42c
# Outputs:
#   1. analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
#      Status: finalized, ready for promotion
#   2. analysis/2025-11-22_14-22-10_revised-analysis_cs-business-analyst.md
#      Status: draft, not ready
```

**Decision:** Promote output #1 to Confluence for stakeholder review.

#### Step 2: Prepare Content for Confluence

**Review and enhance markdown:**
```bash
# Open output in editor
code output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
```

**Make Confluence-specific enhancements:**
- Add table of contents (Confluence macro)
- Convert diagrams to Confluence format (or embed images)
- Add @mentions for stakeholders
- Add page labels for discoverability
- Format callouts using Confluence panels
- Add status macro (e.g., "In Review")

**Example Enhancements:**
```markdown
<!-- Original (git) -->
# Invoice Process Analysis

## Key Findings
- Finding 1
- Finding 2

<!-- Enhanced (Confluence) -->
{toc}

{status:colour=Blue|title=In Review|subtle=false}

# Invoice Process Analysis

*Prepared by:* @rickydwilson-dcs
*Review by:* @sarah.chen, @mike.johnson
*Date:* November 22, 2025

{info}
This analysis is based on stakeholder walkthrough meeting on 2025-11-22.
See [PROJ-123](jira:PROJ-123) for project details.
{info}

## Key Findings

{panel:title=Finding 1: Manual Data Entry|borderColor=#ccc|titleBGColor=#F7D6C4}
Current process requires 100% manual data entry...
{panel}

[... continues ...]
```

#### Step 3: Create/Update Confluence Page

**Option A: Create New Page**
1. Navigate to Confluence space (e.g., PROJ - Project Documentation)
2. Click "Create" button
3. Select "Blank Page" template
4. Set page title (e.g., "Invoice Process Analysis - November 2025")
5. Paste enhanced markdown (Confluence auto-converts)
6. Add page labels: `invoice-automation`, `business-analysis`, `proj-123`
7. Set parent page (e.g., "Invoice Automation Project")
8. Publish page

**Option B: Update Existing Page**
1. Navigate to existing page
2. Click "Edit" button
3. Update content (append or replace sections)
4. Add comment: "Updated from git session: 2025-11-22_feature-invoice-automation_a3f42c"
5. Publish changes

**Copy Confluence URL:** `https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456`

#### Step 4: Track Promotion in Git

**Use promotion utility:**
```bash
python3 tools/promote_to_confluence.py \
  --session 2025-11-22_feature-invoice-automation_a3f42c \
  --file analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md \
  --confluence-url "https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456" \
  --notify "sarah.chen@pandora.com,mike.johnson@pandora.com"
```

**What this does:**
1. **Copies file to shared directory:**
   ```
   output/shared/promoted-to-confluence/PROJ/123456/
   ├── .promotion-metadata.yaml
   └── invoice-process-analysis.md
   ```

2. **Creates promotion metadata:**
   ```yaml
   promoted_at: "2025-11-22T16:00:00Z"
   promoted_by:
     user: "rickydwilson-dcs"
     email: "webmaster@digitalconsultingservices.co.uk"
   source:
     session_id: "2025-11-22_feature-invoice-automation_a3f42c"
     user: "rickydwilson-dcs"
     file: "analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md"
     agent: "cs-business-analyst"
   confluence:
     space_key: "PROJ"
     page_id: "123456"
     page_title: "Invoice Process Analysis - November 2025"
     page_url: "https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456"
     version: 1
   ```

3. **Updates session metadata:**
   ```yaml
   outputs:
     - file: "analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md"
       agent: "cs-business-analyst"
       type: "analysis"
       created_at: "2025-11-22T06:58:38Z"
       promoted: true
       promoted_to: "confluence://PROJ/123456"
   ```

4. **Optionally sends notifications:**
   ```
   To: sarah.chen@pandora.com, mike.johnson@pandora.com
   Subject: [Confluence] New Page: Invoice Process Analysis

   A new analysis has been published to Confluence:

   Title: Invoice Process Analysis - November 2025
   URL: https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456
   Created by: rickydwilson-dcs
   Agent: cs-business-analyst

   This page documents the invoice process analysis for PROJ-123.
   Please review and provide feedback by [date].
   ```

#### Step 5: Commit Promotion to Git

```bash
git add output/shared/promoted-to-confluence/PROJ/123456/
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/.session-metadata.yaml
git commit -m "docs(confluence): promote invoice process analysis to Confluence

- Page: Invoice Process Analysis - November 2025
- URL: https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456
- Session: 2025-11-22_feature-invoice-automation_a3f42c
- Notified: sarah.chen@pandora.com, mike.johnson@pandora.com"
```

#### Step 6: Add Bidirectional Link (Confluence → Git)

**In Confluence page, add footer section:**
```markdown
---

## Document History

**Source:** Git Repository - claude-skills
**Session:** `2025-11-22_feature-invoice-automation_a3f42c`
**Path:** `output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md`
**Promoted:** 2025-11-22 by @rickydwilson-dcs

For version history and related outputs, see git repository.
```

**Benefits:**
- Confluence readers know where to find technical details
- Git session provides full context (other outputs, metadata)
- Bidirectional traceability maintained

### 6.3 Promotion Tracking & Discovery

#### 6.3.1 Find Promoted Outputs

**By session:**
```bash
# List promoted outputs in session
python3 tools/session_manager.py report 2025-11-22_feature-invoice-automation_a3f42c --promoted-only

# Output:
# Promoted Outputs:
#   1. analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
#      Confluence: https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456
#      Promoted: 2025-11-22T16:00:00Z by rickydwilson-dcs
```

**By Confluence space:**
```bash
# List all outputs promoted to PROJ space
ls output/shared/promoted-to-confluence/PROJ/

# Output:
# 123456/  (Invoice Process Analysis)
# 123457/  (System Architecture)
# 123458/  (Executive Recommendations)
```

**Search by metadata:**
```bash
# Find all promoted outputs by agent
grep -r "agent: cs-business-analyst" output/shared/promoted-to-confluence/*/*/. promotion-metadata.yaml
```

#### 6.3.2 Prevent Duplicate Promotions

**Check before promoting:**
```bash
# Promotion utility checks session metadata
python3 tools/promote_to_confluence.py \
  --session 2025-11-22_feature-invoice-automation_a3f42c \
  --file analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md \
  --confluence-url "https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456"

# Output:
# ⚠️  Warning: This output has already been promoted!
#    Previous promotion: 2025-11-22T16:00:00Z
#    Confluence page: https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456
#
# Options:
#   1. Abort (recommended if this is a mistake)
#   2. Continue (will update promotion metadata to version 2)
#   3. Promote to different page (provide new URL)
#
# Choice: _
```

### 6.4 Lifecycle Management Post-Promotion

#### 6.4.1 Retention Policy After Promotion

**Question:** Can we delete session outputs after Confluence promotion?

**Answer:** Depends on retention policy and context:

**Scenario A: Promoted Output is Self-Contained**
- Confluence page is complete record
- No additional context needed from session
- **Action:** Safe to delete session after retention period

**Scenario B: Promoted Output Requires Session Context**
- Confluence page is summary; session has detailed analysis
- Related outputs in session provide supporting evidence
- **Action:** Keep session until project/sprint complete

**Best Practice:** Set retention policy based on promotion:
```yaml
# In .session-metadata.yaml
retention:
  policy: "project"  # Keep until project complete
  expires_at: "2026-05-22"
  reason: "Promoted to Confluence but session contains detailed analysis referenced in page"
```

#### 6.4.2 Updating Promoted Content

**Scenario:** Need to update Confluence page with revised analysis.

**Workflow:**

1. **Create new output in session:**
   ```bash
   # Generate revised analysis
   python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py \
     updated-transcript.md \
     > ${CLAUDE_SESSION_DIR}/analysis/2025-11-23_10-00-00_revised-invoice-process-analysis_cs-business-analyst.md
   ```

2. **Update Confluence page manually:**
   - Edit page with new findings
   - Add comment: "Updated based on revised analysis (2025-11-23)"

3. **Track update in promotion metadata:**
   ```bash
   python3 tools/promote_to_confluence.py \
     --session 2025-11-22_feature-invoice-automation_a3f42c \
     --file analysis/2025-11-23_10-00-00_revised-invoice-process-analysis_cs-business-analyst.md \
     --confluence-url "https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456" \
     --update-existing

   # Updates promotion metadata to version 2:
   # confluence:
   #   version: 2
   #   updated_at: "2025-11-23T10:00:00Z"
   ```

### 6.5 Integration with OneDrive (Future Enhancement)

**Current Scope:** Confluence promotion only.

**Future Enhancement:** Add OneDrive integration for team-level file sharing.

**Potential Workflow:**
```bash
# Promote to OneDrive
python3 tools/promote_to_onedrive.py \
  --session 2025-11-22_feature-invoice-automation_a3f42c \
  --file analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md \
  --onedrive-path "/Engineering/Invoice Automation/Analysis/"

# Copies to:
# output/shared/promoted-to-onedrive/engineering/invoice-automation/
```

**Not implementing in initial version** - focus on Confluence as primary knowledge system.

---

## 7. Migration Strategy

### 7.1 Migration Approach

**Philosophy:** Pragmatic migration with minimal disruption to ongoing work.

**Approach:**
1. **Preserve existing outputs** - No data loss
2. **One-time batch migration** - All 13 outputs moved at once
3. **Create migration session** - Legacy outputs grouped together
4. **Update metadata** - Minimal context (user, timestamp, agent)
5. **Allow incremental enhancement** - Users can update metadata later
6. **Archive old structure** - Keep backup for rollback

### 7.2 Pre-Migration Checklist

**Before running migration:**

- [ ] **Backup current state:**
  ```bash
  cp -r output/ output.backup-2025-11-22/
  tar -czf output.backup-2025-11-22.tar.gz output.backup-2025-11-22/
  ```

- [ ] **Install Python utilities:**
  ```bash
  # Verify utilities exist
  ls tools/migrate_outputs.py
  ls tools/session_manager.py

  # Test dry-run
  python3 tools/migrate_outputs.py --dry-run
  ```

- [ ] **Review output inventory:**
  ```bash
  find output/ -name "*.md" -type f | grep -v README.md
  # Expected: 13 files across architecture/, analysis/, reviews/, reports/
  ```

- [ ] **Identify git user:**
  ```bash
  git config user.name  # Should return: rickydwilson-dcs
  git config user.email  # Should return: webmaster@digitalconsultingservices.co.uk
  ```

- [ ] **Create feature branch:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/session-based-output-system
  ```

### 7.3 Migration Execution

#### Step 1: Run Dry-Run Migration

```bash
python3 tools/migrate_outputs.py --dry-run
```

**Expected Output:**
```
🔍 Scanning existing outputs...
   Found 13 outputs across 4 categories:
   - architecture/ (2 files)
   - analysis/ (10 files)
   - reviews/ (1 file)
   - reports/ (0 files)

📊 Migration Plan:

   User: rickydwilson-dcs (from git config)
   Email: webmaster@digitalconsultingservices.co.uk
   Team: unknown (update manually after migration)

   Migration Session:
   └── output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/

   Outputs to Migrate:

   ✓ analysis/2025-11-13_14-22-25_security-review_cs-secops.md
     → sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/analysis/
     Agent: cs-secops | Created: 2025-11-13T14:22:25Z

   ✓ analysis/2025-11-19_12-19-45_roadmap-prioritization_cs-product-manager.md
     → sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/analysis/
     Agent: cs-product-manager | Created: 2025-11-19T12:19:45Z

   [... 11 more files ...]

   Session Metadata:
   - session_id: 2025-11-22_migration-legacy-outputs_000000
   - created_at: 2025-11-22T08:00:00Z
   - project: "Legacy Outputs Migration"
   - ticket: "MIGRATION-001"
   - retention: temporary (expires 2025-12-22)
   - outputs: 13 files

⚠️  Dry-run mode - no changes made

Actions:
1. Review migration plan above
2. Run with --execute to perform migration
3. Backup created at: output.backup-2025-11-22/

💡 Tips:
- Update team/project/ticket in session metadata after migration
- Promote important outputs to Confluence
- Archive or delete migration session after 30 days
```

**Review:**
- Verify all 13 files identified
- Confirm user/email correct
- Check migration session structure

#### Step 2: Execute Migration

```bash
python3 tools/migrate_outputs.py --execute
```

**Expected Output:**
```
🔍 Scanning existing outputs...
   Found 13 outputs

💾 Creating backup...
   ✅ Backup created: output.backup-2025-11-22/

🚀 Executing migration...

1. Creating migration session...
   ✅ Created: output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/
   ✅ Metadata: .session-metadata.yaml

2. Migrating outputs...
   ✓ analysis/2025-11-13_14-22-25_security-review_cs-secops.md
   ✓ analysis/2025-11-19_12-19-45_roadmap-prioritization_cs-product-manager.md
   ✓ analysis/2025-11-19_13-21-38_user-stories-quick-wins-sprint_cs-product-manager.md
   [... progress continues ...]
   ✅ Migrated 13 files

3. Updating session metadata...
   ✅ Registered 13 outputs in .session-metadata.yaml

4. Cleaning up legacy structure...
   ⚠️  Legacy files left in place (use --remove-legacy to delete)
   ℹ️  Git still tracks: output/architecture/, output/analysis/, etc.

✅ Migration Complete!

📊 Summary:
   - Total outputs migrated: 13
   - Sessions created: 1
   - Errors: 0
   - Duration: 0.3 seconds

📂 New Structure:
   output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/
   ├── .session-metadata.yaml
   ├── analysis/ (10 files)
   ├── architecture/ (2 files)
   └── reviews/ (1 file)

📝 Migration Report:
   Saved to: output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/MIGRATION_REPORT.md

Next Steps:
1. Review migration session: python3 tools/session_manager.py report 2025-11-22_migration-legacy-outputs_000000
2. Update metadata (team, project, tickets) as needed
3. Promote important outputs to Confluence
4. Commit migration: git add output/sessions/ && git commit -m "feat(sessions): migrate legacy outputs to session-based system"
5. Remove legacy structure: python3 tools/migrate_outputs.py --remove-legacy
```

#### Step 3: Review Migration Results

```bash
# View migration session
python3 tools/session_manager.py report 2025-11-22_migration-legacy-outputs_000000

# Output:
# Session Report: 2025-11-22_migration-legacy-outputs_000000
#
# Identity:
#   User: rickydwilson-dcs
#   Email: webmaster@digitalconsultingservices.co.uk
#   Team: unknown
#
# Context:
#   Branch: feature/session-based-output-system
#   Project: Legacy Outputs Migration
#   Ticket: MIGRATION-001
#
# Status: active
# Created: 2025-11-22T08:00:00Z
# Retention: temporary (expires 2025-12-22)
#
# Outputs (13):
#   1. analysis/2025-11-13_14-22-25_security-review_cs-secops.md
#      Agent: cs-secops | Created: 2025-11-13T14:22:25Z | Promoted: No
#   [... 12 more ...]
#
# Next Steps:
#   1. Update team field in metadata (currently: unknown)
#   2. Update ticket/project for each output if known
#   3. Promote important outputs to Confluence
#   4. Archive migration session after 30 days
```

**Manually inspect files:**
```bash
# Check session directory structure
tree output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/

# Read migration report
cat output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/MIGRATION_REPORT.md

# Verify metadata
cat output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/.session-metadata.yaml
```

#### Step 4: Enhance Metadata (Optional)

**For important migrated outputs, add context:**

```bash
# Edit session metadata directly
code output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/.session-metadata.yaml

# Update fields:
# - created_by.team: "engineering" (instead of "unknown")
# - context.ticket: "PROJ-123" (for invoice automation outputs)
# - context.project: "Invoice Automation System" (specific project name)
# - tags: ["invoice-automation", "business-analysis"]
```

**Or use utility (if implemented):**
```bash
python3 tools/session_manager.py update 2025-11-22_migration-legacy-outputs_000000 \
  --team engineering \
  --ticket PROJ-123 \
  --project "Invoice Automation System" \
  --add-tag invoice-automation
```

#### Step 5: Commit Migration

```bash
# Stage migration session
git add output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/

# Commit
git commit -m "feat(sessions): migrate legacy outputs to session-based system

- Migrated 13 outputs from flat structure
- Created migration session: 2025-11-22_migration-legacy-outputs_000000
- User: rickydwilson-dcs
- Retention: temporary (30 days)
- All files preserved with original timestamps

Details:
- analysis/ (10 files)
- architecture/ (2 files)
- reviews/ (1 file)

Next steps:
- Update metadata with project/ticket context
- Promote important outputs to Confluence
- Remove legacy structure after verification"
```

#### Step 6: Update .gitignore

```bash
# Update .gitignore to track sessions
code .gitignore

# Change from:
# output/*

# To:
# output/.current-session
# output/**/.DS_Store
# output/**/tmp/

# Commit
git add .gitignore
git commit -m "chore(git): update .gitignore to track session-based outputs"
```

#### Step 7: Remove Legacy Structure (After Verification)

**Wait 1-2 days to ensure migration successful, then:**

```bash
# Remove legacy flat directories
python3 tools/migrate_outputs.py --remove-legacy

# Output:
# ⚠️  This will remove legacy output directories:
#    - output/architecture/
#    - output/analysis/
#    - output/reviews/
#    - output/reports/
#
# Backup exists at: output.backup-2025-11-22/
#
# Are you sure? (yes/no): yes
#
# 🗑️  Removing legacy directories...
#    ✅ Removed: output/architecture/
#    ✅ Removed: output/analysis/
#    ✅ Removed: output/reviews/
#    ✅ Removed: output/reports/
#
# ✅ Legacy structure removed
#
# Git status:
#    deleted: output/architecture/*.md (2 files)
#    deleted: output/analysis/*.md (10 files)
#    deleted: output/reviews/*.md (1 file)

# Commit deletion
git add output/
git commit -m "chore(cleanup): remove legacy flat output structure

- Deleted legacy directories (architecture/, analysis/, reviews/, reports/)
- All outputs preserved in session-based structure
- Backup retained at: output.backup-2025-11-22/"
```

### 7.4 Post-Migration Validation

**Checklist:**

- [ ] **All 13 files migrated:**
  ```bash
  find output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/ -name "*.md" | wc -l
  # Expected: 13 (excluding MIGRATION_REPORT.md)
  ```

- [ ] **No data loss:**
  ```bash
  # Compare file counts
  find output.backup-2025-11-22/ -name "*.md" | grep -v README.md | wc -l
  find output/sessions/ -name "*.md" | grep -v README.md | grep -v MIGRATION_REPORT.md | wc -l
  # Should match: 13
  ```

- [ ] **Metadata valid:**
  ```bash
  # Validate YAML syntax
  python3 -c "import yaml; yaml.safe_load(open('output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/.session-metadata.yaml'))"
  # No errors = valid
  ```

- [ ] **Session utilities work:**
  ```bash
  python3 tools/session_manager.py list
  python3 tools/session_manager.py report 2025-11-22_migration-legacy-outputs_000000
  python3 tools/session_manager.py search --user rickydwilson-dcs
  ```

- [ ] **Git tracking correct:**
  ```bash
  git status
  # Should show: new files in output/sessions/ (tracked)
  # Should NOT show: output/sessions/ as untracked
  ```

- [ ] **Backup preserved:**
  ```bash
  ls output.backup-2025-11-22/
  # Should contain: architecture/, analysis/, reviews/, reports/, README.md
  ```

### 7.5 Rollback Plan

**If migration fails or issues discovered:**

```bash
# 1. Discard migration
git reset --hard HEAD

# 2. Restore from backup
rm -rf output/
cp -r output.backup-2025-11-22/ output/

# 3. Verify restoration
git status
# Should show: no changes

# 4. Investigate issue
python3 tools/migrate_outputs.py --dry-run --debug
```

**Common Issues & Fixes:**

| Issue | Cause | Fix |
|-------|-------|-----|
| File count mismatch | Script missed files | Update glob pattern in migrate_outputs.py |
| Invalid YAML | Metadata generation bug | Fix schema generation logic |
| Permission errors | File ownership issues | `chmod -R u+rw output/` |
| Git tracking wrong | .gitignore misconfigured | Update .gitignore patterns |

### 7.6 Migration Timeline

**Recommended Schedule:**

| Day | Activity | Duration |
|-----|----------|----------|
| Day 1 | Implement Python utilities (session_manager.py, migrate_outputs.py) | 4 hours |
| Day 1 | Test utilities with mock data | 1 hour |
| Day 1 | Run dry-run migration, review plan | 30 min |
| Day 1 | Execute migration, verify results | 1 hour |
| Day 2 | Update documentation (README.md, CLAUDE.md, etc.) | 2 hours |
| Day 2 | Create feature branch PR, request review | 30 min |
| Day 3 | Address PR feedback, merge to develop | 1 hour |
| Day 4 | Monitor for issues, rollback if needed | Ongoing |
| Day 5+ | Enhance metadata, promote to Confluence | Ongoing |

**Total Implementation Time:** ~10 hours over 3-5 days

---

## 8. Testing & Validation

### 8.1 Test Plan Overview

**Testing Phases:**
1. **Unit Tests** - Python utilities in isolation
2. **Integration Tests** - Utilities + git + file system
3. **Migration Tests** - Legacy → new structure
4. **Agent Integration Tests** - Agents write to sessions
5. **Workflow Tests** - End-to-end user workflows
6. **Scale Tests** - Performance with 50+ users, 1000+ sessions

### 8.2 Unit Tests

#### 8.2.1 session_manager.py Tests

```python
# Test file: tests/test_session_manager.py

def test_sanitize_username():
    """Test username sanitization for directory names."""
    assert sanitize_username("rickydwilson-dcs") == "rickydwilson-dcs"
    assert sanitize_username("Sarah Chen") == "sarah-chen"
    assert sanitize_username("John_Smith (Engineering)") == "john-smith-engineering"
    assert sanitize_username("Test@User!123") == "testuser123"
    assert sanitize_username("") == "unknown-user"

def test_generate_session_id():
    """Test session ID generation."""
    session_id = generate_session_id("feature/invoice-automation")

    # Format: YYYY-MM-DD_branch-slug_hash
    assert len(session_id.split("_")) == 3
    assert session_id.startswith("2025-11-22")  # Today's date
    assert "feature-invoice-automation" in session_id
    assert len(session_id.split("_")[-1]) == 6  # 6-char hash

def test_create_session():
    """Test session creation."""
    # Setup
    temp_dir = "/tmp/test-output-sessions"
    os.makedirs(temp_dir, exist_ok=True)

    # Create session
    session = create_session(
        output_dir=temp_dir,
        user="test-user",
        email="test@example.com",
        team="engineering",
        branch="feature/test",
        ticket="TEST-123",
        project="Test Project"
    )

    # Assertions
    assert session.session_id is not None
    assert os.path.exists(session.directory)
    assert os.path.exists(session.metadata_file)

    # Validate metadata
    metadata = yaml.safe_load(open(session.metadata_file))
    assert metadata["session_id"] == session.session_id
    assert metadata["created_by"]["user"] == "test-user"
    assert metadata["context"]["ticket"] == "TEST-123"
    assert metadata["status"]["current"] == "active"

    # Cleanup
    shutil.rmtree(temp_dir)

def test_add_output_to_session():
    """Test adding output to existing session."""
    # Setup: create session
    session = create_session(...)

    # Create output file
    output_path = os.path.join(session.directory, "analysis", "test-output.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("# Test Output")

    # Register output
    add_output(
        session_id=session.session_id,
        file_path="analysis/test-output.md",
        agent="cs-test-agent",
        type="analysis"
    )

    # Validate metadata updated
    metadata = yaml.safe_load(open(session.metadata_file))
    assert len(metadata["outputs"]) == 1
    assert metadata["outputs"][0]["file"] == "analysis/test-output.md"
    assert metadata["outputs"][0]["agent"] == "cs-test-agent"
    assert metadata["outputs"][0]["promoted"] is False

def test_search_sessions():
    """Test session search functionality."""
    # Setup: create multiple sessions
    session1 = create_session(ticket="PROJ-123", project="Project A")
    session2 = create_session(ticket="PROJ-456", project="Project B")
    session3 = create_session(ticket="PROJ-123", project="Project A")

    # Search by ticket
    results = search_sessions(ticket="PROJ-123")
    assert len(results) == 2

    # Search by project
    results = search_sessions(project="Project A")
    assert len(results) == 2

    # Search by user
    results = search_sessions(user="test-user")
    assert len(results) == 3
```

#### 8.2.2 migrate_outputs.py Tests

```python
# Test file: tests/test_migrate_outputs.py

def test_scan_legacy_outputs():
    """Test scanning legacy output directory."""
    # Setup legacy structure
    legacy_dir = "/tmp/test-legacy-output"
    create_legacy_structure(legacy_dir)  # Helper to create mock files

    # Scan
    outputs = scan_legacy_outputs(legacy_dir)

    # Assertions
    assert len(outputs) == 13
    assert any(o["category"] == "analysis" for o in outputs)
    assert any(o["agent"] == "cs-business-analyst" for o in outputs)

def test_extract_metadata_from_filename():
    """Test extracting metadata from legacy filename."""
    filename = "2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md"

    metadata = extract_metadata_from_filename(filename)

    assert metadata["timestamp"] == "2025-11-22T06:58:38Z"
    assert metadata["topic"] == "invoice-process-analysis"
    assert metadata["agent"] == "cs-business-analyst"

def test_migration_dry_run():
    """Test dry-run migration (no file changes)."""
    # Setup
    legacy_dir = "/tmp/test-legacy"
    output_dir = "/tmp/test-new-output"
    create_legacy_structure(legacy_dir)

    # Run dry-run
    plan = migrate_outputs(
        legacy_dir=legacy_dir,
        output_dir=output_dir,
        dry_run=True
    )

    # Assertions
    assert plan["total_files"] == 13
    assert not os.path.exists(output_dir)  # No changes made
    assert os.path.exists(legacy_dir)  # Original preserved

def test_migration_execute():
    """Test actual migration execution."""
    # Setup
    legacy_dir = "/tmp/test-legacy"
    output_dir = "/tmp/test-new-output"
    create_legacy_structure(legacy_dir)

    # Execute migration
    result = migrate_outputs(
        legacy_dir=legacy_dir,
        output_dir=output_dir,
        dry_run=False
    )

    # Assertions
    assert result["success"] is True
    assert result["migrated_count"] == 13
    assert os.path.exists(output_dir + "/sessions/test-user/")

    # Verify metadata
    migration_session = find_migration_session(output_dir)
    metadata = yaml.safe_load(open(migration_session + "/.session-metadata.yaml"))
    assert len(metadata["outputs"]) == 13
```

### 8.3 Integration Tests

#### 8.3.1 Git Integration Test

```bash
# Test: Session creation integrates with git

# Setup
cd /tmp/test-repo
git init
git config user.name "test-user"
git config user.email "test@example.com"
git checkout -b feature/test-session

# Create session (should read git config)
python3 tools/session_manager.py create \
  --ticket TEST-123 \
  --project "Test Project"

# Verify session uses git context
SESSION_DIR=$(python3 tools/session_manager.py current --path)
cat $SESSION_DIR/.session-metadata.yaml | grep "branch: feature/test-session"
cat $SESSION_DIR/.session-metadata.yaml | grep "user: test-user"

# Verify git tracks session
git add output/sessions/
git status | grep "new file.*output/sessions/"

# Cleanup
cd /tmp && rm -rf test-repo
```

#### 8.3.2 Agent Output Integration Test

```bash
# Test: Agent outputs write to current session

# Setup
python3 tools/session_manager.py create \
  --ticket TEST-123 \
  --project "Test Project"

# Verify environment variable set
echo $CLAUDE_SESSION_DIR
# Expected: output/sessions/test-user/2025-11-22_feature-test-session_abc123/

# Generate agent output
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
echo "# Test Analysis" > ${CLAUDE_SESSION_DIR}/analysis/${TIMESTAMP}_test-analysis_cs-test-agent.md

# Verify output registered
python3 tools/session_manager.py report | grep "test-analysis_cs-test-agent.md"

# Cleanup
python3 tools/session_manager.py close
```

### 8.4 Migration Tests

#### 8.4.1 Full Migration Test

```bash
# Test: Complete migration of actual 13 outputs

# Setup: Create test copy of current output
cp -r output/ test-output-backup/

# Run migration
python3 tools/migrate_outputs.py \
  --input test-output-backup/ \
  --output test-output-migrated/ \
  --dry-run

# Review plan, then execute
python3 tools/migrate_outputs.py \
  --input test-output-backup/ \
  --output test-output-migrated/ \
  --execute

# Validate results
# 1. File count matches
ORIGINAL=$(find test-output-backup/ -name "*.md" | grep -v README | wc -l)
MIGRATED=$(find test-output-migrated/sessions/ -name "*.md" | grep -v MIGRATION_REPORT | wc -l)
test $ORIGINAL -eq $MIGRATED || echo "❌ File count mismatch"

# 2. Metadata valid
python3 -c "import yaml; yaml.safe_load(open('test-output-migrated/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/.session-metadata.yaml'))"

# 3. Outputs registered
python3 tools/session_manager.py --output-dir test-output-migrated/ report 2025-11-22_migration-legacy-outputs_000000

# Cleanup
rm -rf test-output-backup/ test-output-migrated/
```

### 8.5 Workflow Tests

#### 8.5.1 Complete User Workflow Test

```bash
# Test: User creates session, generates outputs, promotes to Confluence, closes session

# Step 1: Create session
python3 tools/session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Automation System"

SESSION_ID=$(python3 tools/session_manager.py current)
echo "Created session: $SESSION_ID"

# Step 2: Generate multiple outputs (simulate agent work)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
echo "# Process Analysis" > ${CLAUDE_SESSION_DIR}/analysis/${TIMESTAMP}_process-analysis_cs-business-analyst.md
sleep 2
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
echo "# Architecture Design" > ${CLAUDE_SESSION_DIR}/architecture/${TIMESTAMP}_architecture-design_cs-architect.md

# Step 3: Review session
python3 tools/session_manager.py report
# Expected: Shows 2 outputs

# Step 4: Promote one output to Confluence
python3 tools/promote_to_confluence.py \
  --session $SESSION_ID \
  --file "analysis/${TIMESTAMP}_process-analysis_cs-business-analyst.md" \
  --confluence-url "https://test.atlassian.net/wiki/spaces/TEST/pages/123456"

# Verify promotion tracked
python3 tools/session_manager.py report | grep "promoted: true"
test -f "output/shared/promoted-to-confluence/TEST/123456/.promotion-metadata.yaml"

# Step 5: Close session
python3 tools/session_manager.py close

# Verify status
python3 tools/session_manager.py report $SESSION_ID | grep "Status: closed"

# Step 6: Commit to git
git add output/
git commit -m "test: complete workflow test session"

# Cleanup
git reset --hard HEAD~1
```

### 8.6 Scale Tests

#### 8.6.1 Multi-User Collision Test

```bash
# Test: Multiple users create sessions on same branch/day without collisions

# Simulate 10 users
for i in {1..10}; do
  USER="test-user-$i"

  # Override git config temporarily
  export GIT_AUTHOR_NAME=$USER
  export GIT_COMMITTER_NAME=$USER

  python3 tools/session_manager.py create \
    --user $USER \
    --email "${USER}@example.com" \
    --ticket PROJ-123 \
    --project "Test Project"
done

# Verify 10 unique sessions created
SESSIONS=$(find output/sessions/ -name ".session-metadata.yaml" | wc -l)
test $SESSIONS -eq 10 || echo "❌ Collision detected!"

# Verify unique session IDs
SESSION_IDS=$(find output/sessions -maxdepth 2 -type d | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}_" | wc -l)
test $SESSION_IDS -eq 10 || echo "❌ Duplicate session IDs!"

# Cleanup
rm -rf output/sessions/test-user-*
```

#### 8.6.2 Large Directory Performance Test

```bash
# Test: Search performance with 1000+ sessions

# Generate 1000 mock sessions
for i in {1..1000}; do
  SESSION_ID=$(python3 -c "import secrets; print(f'2025-11-22_test-session_{secrets.token_hex(3)}')")
  mkdir -p "output/sessions/perf-test-user/$SESSION_ID"

  cat > "output/sessions/perf-test-user/$SESSION_ID/.session-metadata.yaml" <<EOF
session_id: "$SESSION_ID"
created_at: "2025-11-22T08:00:00Z"
created_by:
  user: "perf-test-user"
  email: "perf@example.com"
  team: "engineering"
context:
  branch: "feature/test"
  ticket: "TEST-$i"
  project: "Test Project"
status:
  current: "active"
outputs: []
EOF
done

# Test search performance
time python3 tools/session_manager.py search --user perf-test-user
# Expected: < 2 seconds

time python3 tools/session_manager.py search --ticket "TEST-500"
# Expected: < 2 seconds

# Test list performance
time python3 tools/session_manager.py list
# Expected: < 3 seconds

# Cleanup
rm -rf output/sessions/perf-test-user/
```

### 8.7 Validation Checklist

Before production deployment:

- [ ] All unit tests pass
- [ ] Git integration works (reads config, tracks sessions)
- [ ] Agent integration works (CLAUDE_SESSION_DIR)
- [ ] Migration completes without errors
- [ ] Complete workflow test succeeds
- [ ] No collisions with 50 concurrent sessions
- [ ] Search/list performs well with 1000+ sessions
- [ ] Documentation updated (README.md, CLAUDE.md)
- [ ] Python utilities have --help documentation
- [ ] Backup/rollback process tested
- [ ] Team members reviewed and approved design

---

## 9. Appendices

### 9.1 Appendix A: Python Utility Reference

#### session_manager.py CLI Reference

```bash
# Create session
session_manager.py create \
  --ticket <TICKET-ID> \
  --project "<PROJECT-NAME>" \
  [--team <TEAM>] \
  [--sprint <SPRINT>] \
  [--epic <EPIC-ID>] \
  [--release <VERSION>] \
  [--retention <project|sprint|temporary>] \
  [--stakeholder "<NAME> <EMAIL>"]

# List sessions
session_manager.py list \
  [--user <USERNAME>] \
  [--status <active|closed|archived>] \
  [--team <TEAM>]

# Get current session
session_manager.py current [--path]

# Set active session
session_manager.py use <SESSION-ID>

# Add output to session
session_manager.py add-output \
  --file <RELATIVE-PATH> \
  --agent <AGENT-NAME> \
  --type <architecture|analysis|reviews|reports|artifacts>

# Search sessions
session_manager.py search \
  [--ticket <TICKET-ID>] \
  [--project "<PROJECT-NAME>"] \
  [--agent <AGENT-NAME>] \
  [--tag <TAG>] \
  [--user <USERNAME>] \
  [--expiring-within <DAYS>]

# Close session
session_manager.py close [<SESSION-ID>]

# Archive session
session_manager.py archive <SESSION-ID>

# Generate report
session_manager.py report [<SESSION-ID>] \
  [--format <markdown|json>] \
  [--promoted-only]

# Update metadata
session_manager.py update <SESSION-ID> \
  [--team <TEAM>] \
  [--ticket <TICKET-ID>] \
  [--project "<PROJECT-NAME>"] \
  [--add-tag <TAG>] \
  [--add-stakeholder "<NAME> <EMAIL>"]
```

#### migrate_outputs.py CLI Reference

```bash
# Dry-run migration
migrate_outputs.py \
  [--input <LEGACY-OUTPUT-DIR>] \
  [--output <NEW-OUTPUT-DIR>] \
  --dry-run

# Execute migration
migrate_outputs.py \
  [--input <LEGACY-OUTPUT-DIR>] \
  [--output <NEW-OUTPUT-DIR>] \
  --execute \
  [--user <USERNAME>] \
  [--default-ticket <TICKET-ID>] \
  [--default-project "<PROJECT-NAME>"]

# Remove legacy structure (after migration)
migrate_outputs.py --remove-legacy
```

#### promote_to_confluence.py CLI Reference

```bash
# Promote output
promote_to_confluence.py \
  --session <SESSION-ID> \
  --file <RELATIVE-PATH> \
  --confluence-url <CONFLUENCE-URL> \
  [--notify <EMAIL1,EMAIL2,...>] \
  [--update-existing]
```

### 9.2 Appendix B: Metadata Schema Quick Reference

#### Session Metadata (.session-metadata.yaml)

```yaml
session_id: string (REQUIRED)
created_at: ISO8601 timestamp (REQUIRED)
created_by:
  user: string (REQUIRED)
  email: string (REQUIRED)
  team: string (REQUIRED) # marketing|product|engineering|delivery
context:
  branch: string (REQUIRED)
  ticket: string (optional, but recommended)
  project: string (REQUIRED)
  sprint: string (optional)
  epic: string (optional)
  release: string (optional)
status:
  current: enum (REQUIRED) # active|closed|archived
  closed_at: ISO8601 timestamp (optional)
  archived_at: ISO8601 timestamp (optional)
outputs: array (REQUIRED, can be empty)
  - file: string
    agent: string
    type: enum # architecture|analysis|reviews|reports|artifacts
    created_at: ISO8601 timestamp
    promoted: boolean
    promoted_to: string|null
stakeholders: array (optional)
  - name: string
    role: string
    email: string
retention:
  policy: enum (REQUIRED) # project|sprint|temporary
  expires_at: ISO8601 date (REQUIRED)
  reason: string (optional)
links: object (optional)
  jira: URL
  confluence: URL
  onedrive: URL
  github_pr: URL
tags: array of strings (optional)
notes: string (optional, markdown)
```

#### Promotion Metadata (.promotion-metadata.yaml)

```yaml
promoted_at: ISO8601 timestamp (REQUIRED)
promoted_by:
  user: string (REQUIRED)
  email: string (REQUIRED)
source:
  session_id: string (REQUIRED)
  user: string (REQUIRED)
  file: string (REQUIRED)
  agent: string (REQUIRED)
confluence:
  space_key: string (REQUIRED)
  space_name: string (optional)
  page_id: string (REQUIRED)
  page_title: string (REQUIRED)
  page_url: URL (REQUIRED)
  parent_page_id: string (optional)
  version: integer (REQUIRED)
notified: array of emails (optional)
notes: string (optional, markdown)
```

### 9.3 Appendix C: Directory Structure Comparison

#### Current (Flat) Structure

```
output/
├── architecture/
│   ├── 2025-11-22_09-45-00_system-architecture_cs-architect.md
│   └── 2025-11-23_10-30-00_system-architecture_cs-architect.md  # Collision risk!
├── analysis/
│   ├── 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
│   ├── 2025-11-22_08-15-30_invoice-process-analysis_cs-business-analyst.md  # Same topic, same day!
│   └── ... (10 more files)
├── reviews/
│   └── 2025-11-13_14-22-25_security-review_cs-secops.md
├── reports/
└── README.md

Problems:
❌ No user attribution
❌ No session context
❌ Flat namespace (collision risk)
❌ No lifecycle tracking
❌ No Confluence integration
```

#### New (Session-Based) Structure

```
output/
├── sessions/
│   ├── rickydwilson-dcs/
│   │   ├── 2025-11-22_feature-invoice-automation_a3f42c/
│   │   │   ├── .session-metadata.yaml  ✅ Full context
│   │   │   ├── architecture/
│   │   │   │   └── 2025-11-22_09-45-00_system-architecture_cs-architect.md
│   │   │   └── analysis/
│   │   │       └── 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md
│   │   └── 2025-11-23_spike-ocr-integration_b8d39e/
│   │       └── ...
│   ├── sarah-chen/
│   │   └── 2025-11-22_feature-invoice-automation_c4f88a/  ✅ No collision
│   │       ├── .session-metadata.yaml
│   │       └── analysis/
│   │           └── 2025-11-22_08-15-30_invoice-process-analysis_cs-business-analyst.md
│   └── mike-johnson/
│       └── ...
├── shared/
│   ├── promoted-to-confluence/  ✅ Confluence integration
│   │   └── PROJ/
│   │       └── 123456/
│   │           ├── .promotion-metadata.yaml
│   │           └── invoice-process-analysis.md
│   └── team-resources/
│       └── ...
└── README.md

Benefits:
✅ User attribution (user directories)
✅ Session context (metadata)
✅ Namespace isolation (user/session/category)
✅ Lifecycle tracking (status, retention, promotion)
✅ Confluence integration (shared/promoted-to-confluence/)
✅ Scalable to 50+ users, 1000+ sessions
```

### 9.4 Appendix D: Search & Discovery Patterns

#### Find all outputs for a ticket

```bash
# Method 1: Using session_manager utility
python3 tools/session_manager.py search --ticket PROJ-123

# Method 2: Using grep
grep -r "ticket: PROJ-123" output/sessions/*/*/.session-metadata.yaml
```

#### Find all outputs by agent

```bash
# Method 1: Using session_manager utility
python3 tools/session_manager.py search --agent cs-business-analyst

# Method 2: Using find
find output/sessions -name "*_cs-business-analyst.md"
```

#### Find all active sessions

```bash
# Method 1: Using session_manager utility
python3 tools/session_manager.py list --status active

# Method 2: Using grep
grep -l "current: active" output/sessions/*/*/.session-metadata.yaml
```

#### Find sessions expiring soon

```bash
# Method 1: Using session_manager utility
python3 tools/session_manager.py search --expiring-within 30

# Method 2: Manual (more complex)
find output/sessions -name ".session-metadata.yaml" -exec grep -l "expires_at: 2025-12-" {} \;
```

#### Find all promoted outputs

```bash
# Method 1: List shared directory
ls output/shared/promoted-to-confluence/

# Method 2: Search session metadata
grep -r "promoted: true" output/sessions/*/*/.session-metadata.yaml

# Method 3: Using session_manager utility
python3 tools/session_manager.py report --promoted-only
```

#### Find all outputs for a user

```bash
# Method 1: List user directory
ls output/sessions/rickydwilson-dcs/

# Method 2: Using session_manager utility
python3 tools/session_manager.py search --user rickydwilson-dcs
```

#### Find outputs by tag

```bash
# Method 1: Using session_manager utility
python3 tools/session_manager.py search --tag invoice-automation

# Method 2: Using grep
grep -r "- invoice-automation" output/sessions/*/*/.session-metadata.yaml
```

### 9.5 Appendix E: Git Workflow Integration

#### Feature Branch → Develop → Main Flow

**Scenario:** User works on feature/invoice-automation, creates outputs, merges to develop.

```bash
# 1. Start feature branch
git checkout develop
git pull origin develop
git checkout -b feature/invoice-automation

# 2. Create session
python3 tools/session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Automation System"

# Session automatically linked to feature/invoice-automation branch (from git)

# 3. Generate outputs during feature work
# (Agents write to $CLAUDE_SESSION_DIR)

# 4. Commit session outputs as work progresses
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
git commit -m "docs(analysis): add invoice process analysis for PROJ-123"

# 5. Close session when feature complete
python3 tools/session_manager.py close
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/.session-metadata.yaml
git commit -m "feat(sessions): close invoice automation analysis session"

# 6. Create PR to develop
git push origin feature/invoice-automation
gh pr create --base develop --title "Add invoice automation analysis"

# 7. After PR merged, session is in develop branch
# Session metadata shows: branch: feature/invoice-automation (historical record)

# 8. Later, promote important outputs to Confluence
python3 tools/promote_to_confluence.py \
  --session 2025-11-22_feature-invoice-automation_a3f42c \
  --file analysis/2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md \
  --confluence-url "https://pandora.atlassian.net/wiki/spaces/PROJ/pages/123456"

git add output/shared/promoted-to-confluence/
git commit -m "docs(confluence): promote invoice analysis to Confluence"
```

**Key Benefits:**
- Session metadata captures feature branch context
- Outputs versioned with feature code
- PR reviewers see outputs alongside code changes
- Historical record of which branch created which outputs
- Confluence promotion tracked in git

---

## Conclusion

This session-based output organization system addresses all five critical limitations of the current flat structure:

1. **User Attribution** - User directories + metadata capture git user identity
2. **Session Context** - Metadata links outputs to branches, tickets, projects, teams
3. **Namespace Isolation** - User/session/category hierarchy prevents collisions
4. **Lifecycle Management** - Status tracking, retention policies, promotion tracking
5. **Integration Path** - Manual Confluence promotion workflow with bidirectional links

**Implementation Path:**
1. Implement Python utilities (~4 hours)
2. Execute migration (~1 hour)
3. Update documentation (~2 hours)
4. Test workflows (~2 hours)
5. Deploy to develop branch (~1 hour)

**Total Implementation Time:** ~10 hours over 3-5 days

**Next Steps:**
1. Review this ADR with stakeholders
2. Get approval for implementation
3. Assign implementation to cs-fullstack-engineer
4. Track progress via Jira ticket
5. Deploy and monitor

---

**Document Version:** 1.0
**Last Updated:** 2025-11-22T07:53:43Z
**Author:** cs-architect
**Review Status:** Awaiting Stakeholder Review
**Implementation Status:** Not Started

**Reviewers:**
- [ ] Technical Lead (rickydwilson-dcs)
- [ ] Product Manager (if applicable)
- [ ] Team Leads (Marketing, Product, Engineering, Delivery)

**Related Documents:**
- output/README.md (current system documentation)
- CLAUDE.md (repository instructions)
- docs/WORKFLOW.md (git workflow)

**References:**
- [Architecture Decision Records (ADR) Pattern](https://adr.github.io/)
- [Git Workflow Best Practices](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [YAML Schema Specification](https://yaml.org/spec/1.2/spec.html)
