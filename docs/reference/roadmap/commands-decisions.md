# Slash Commands - Key Decisions Log

**Purpose:** Document critical decisions made during slash commands library implementation to provide context for future contributors and prevent re-litigating settled questions.

**Status:** Living document
**Started:** 2025-01-24

---

## Strategic Decisions

### Decision 1: Pandora Internal-First, Community-Ready Architecture

**Date:** 2025-01-24
**Decision:** Build for Pandora internal employees first, but with website-ready infrastructure from Day 1.

**Context:**
- Primary purpose: Serve Pandora SDLC teams with high-frequency task automation
- Secondary opportunity: Position for future community expansion and public website
- Balance: Immediate internal value vs. long-term scalability

**Rationale:**
- Avoid costly retrofitting later
- Extended metadata enables rich website features (browse, filter, search, stats)
- Can "flip a switch" to enable community when ready
- Demonstrates Pandora thought leadership externally

**Implications:**
- All commands include rich metadata beyond minimum requirements
- JSON export infrastructure built from Phase 1
- Analytics hooks included (even if not capturing data yet)
- Documentation written for both internal and external audiences

**Alternatives Considered:**
- Internal-only: Simpler but requires rebuild for community
- Community-first: Premature, internal validation needed first

**Status:** Approved

---

### Decision 2: Commands as Peer to Agents and Skills

**Date:** 2025-01-24
**Decision:** Position slash commands as a peer offering alongside agents (28) and skills (28), targeting 28-30 production commands.

**Context:**
- Agents = Workflow orchestrators (guides multi-step processes)
- Skills = Tools + Knowledge (analysis, generation)
- Commands = Task automation (frequent, specific shortcuts)

**Rationale:**
- Clear differentiation based on **frequency of use**
- Commands solve "I do this every week" problem
- Agents/Skills solve "I need expertise for this complex task"
- Parity (28-30 each) signals equal importance

**Key Distinction:**

| Type | Invocation | Use Case | Example |
|------|------------|----------|---------|
| Commands | Intentional shortcut | Daily/weekly tasks | `/update-docs` |
| Agents | Explicit mention | Complex workflows | `@cs-architect` |
| Skills | Natural conversation | Accidental discovery | "Can you review architecture?" |

**Status:** Approved

---

### Decision 3: Exclude Speckit Commands from Library

**Date:** 2025-01-24
**Decision:** Keep speckit.* commands in `.claude/commands/` as personal workflow tools, exclude from production library and catalogs.

**Context:**
- 8 existing speckit.* commands (speckit.analyze, speckit.plan, etc.)
- Designed for specific personal workflow
- Not intended as shareable library offering

**Rationale:**
- Speckit = personal tools, not production offering
- Library commands = vetted, documented, shareable
- Keeps library focused on universal use cases
- Avoids confusion about what's "official"

**Implications:**
- `.claude/commands/speckit.*` ignored in validation
- Not included in COMMANDS_CATALOG.md
- Not exported to api/commands.json
- Can coexist with production library

**Status:** Approved

---

## Technical Decisions

### Decision 4: Extended YAML Frontmatter (Website-Ready Metadata)

**Date:** 2025-01-24
**Decision:** All commands, agents, and skills use extended YAML frontmatter with website-ready metadata.

**Required Fields:**
```yaml
# Core
name, title, description, category, subcategory

# Website Display
difficulty, time-saved, frequency, use-cases (min 2)

# Relationships
related-agents, related-skills, related-commands

# Technical
dependencies, compatibility, examples (min 2)

# Analytics (placeholder)
stats (installs, upvotes, rating)

# Versioning
version, author, created, updated

# Discoverability
tags (min 3), featured, verified, license
```

**Rationale:**
- Enables rich website features (browse, filter, search)
- Supports cross-referencing (agents ↔ skills ↔ commands)
- Analytics-ready for future tracking
- SEO and discoverability optimization

**Implications:**
- Command builder must prompt for all fields
- Validation requires metadata completeness
- Retrofit agents/skills to add new fields
- JSON export includes all metadata

**Alternatives Considered:**
- Minimal frontmatter: Simpler but limits website features
- Separate metadata file: More complex to maintain

**Status:** Approved

---

### Decision 5: Quality Gate - GitHub PR Review Required (ALL Contributions)

**Date:** 2025-01-24
**Decision:** All contributions (internal Pandora team or future community) flow through GitHub PR with automated validation + manual review.

**Workflow:**
1. Submit GitHub PR (fork/branch)
2. Automated validation (command_builder.py --validate)
3. Manual code review (safety, quality, use case validation)
4. Approval → Merge → Auto-deploy (catalog.json regeneration)

**Rationale:**
- **Quality Control:** 100% validation passing maintained
- **Security:** Manual review catches malicious code
- **Consistency:** Same standards for all contributors
- **Transparency:** Public review process (when community-ready)

**Implications:**
- Even internal Pandora developers use PR workflow
- No direct commits to main/develop with commands
- CI/CD pipeline validates automatically
- Rejected PRs provide clear feedback

**No exceptions rationale:**
- Protects repository quality
- Ensures safety for all users (internal and future community)
- Establishes precedent for community contributions

**Status:** Approved

---

### Decision 6: Both Formats (Markdown + JSON)

**Date:** 2025-01-24
**Decision:** Generate both .md command files (for Claude Code) AND JSON exports (for website API).

**Outputs:**
- **Primary:** `commands/category/command-name.md` (source of truth)
- **Derived:** `api/commands.json`, `api/catalog.json` (website consumption)

**Rationale:**
- Markdown = Claude Code native format, human-readable, git-friendly
- JSON = Website API format, machine-readable, queryable
- Single source of truth (markdown) prevents drift
- Auto-generation ensures consistency

**Implications:**
- `export_catalog_json.py` parses .md → generates JSON
- Website consumes JSON (static files or API)
- Changes to .md automatically reflected in JSON (via CI/CD)

**Status:** Approved

---

### Decision 7: Semantic Versioning (v1.0.0)

**Date:** 2025-01-24
**Decision:** Use semantic versioning (MAJOR.MINOR.PATCH) for all commands, agents, and skills.

**Format:** `v1.0.0`
- **MAJOR:** Breaking changes (incompatible with previous version)
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes, documentation updates

**Rationale:**
- Industry standard
- Clear upgrade path
- Website can show "Update Available"
- Users can choose when to upgrade

**Implications:**
- Command builder prompts for version
- Manifest tracks installed versions
- Validation checks version format
- Website displays version and changelog

**Alternatives Considered:**
- Date-based versioning: Less clear semantically
- Simple incremental: Doesn't convey change significance

**Status:** Approved

---

### Decision 8: All Installation Methods Supported

**Date:** 2025-01-24
**Decision:** Support multiple installation methods to accommodate different user types.

**Methods:**
1. **Copy to Clipboard** (website button) - Non-technical users
2. **Download .md File** (direct download) - Simplest
3. **CLI Tool** (`install_commands.py`) - Developers
4. **curl Command** (one-liner) - Advanced users
5. **Manual Copy** (cp command) - Traditional

**Rationale:**
- Different users have different skill levels
- No single method fits all use cases
- Flexibility increases adoption
- Each method documented clearly

**Implications:**
- Install script supports interactive selection
- Website provides multiple install options
- Documentation covers all methods
- No "preferred" method prescribed

**Status:** Approved

---

### Decision 9: Community via GitHub PR Only

**Date:** 2025-01-24
**Decision:** Community contributions ONLY via GitHub PR, not website form submission.

**Workflow:**
1. Community member forks repository
2. Creates command using command_builder.py
3. Submits GitHub PR
4. Automated validation + manual review
5. Approval → Merge

**Rationale:**
- **Quality Control:** PR review process ensures standards
- **Security:** Manual review catches malicious code
- **Transparency:** Public review history
- **Git History:** Proper attribution and change tracking

**Alternatives Considered:**
- **Website Form → Auto PR:** Complex to build, security concerns
- **Email Submission:** Doesn't scale, manual process
- **GitHub Issues Only:** Doesn't include code, requires manual implementation

**Implications:**
- No website submission form (Phase 1-4)
- CONTRIBUTING.md includes command contribution guide
- PR template for command submissions
- Requires GitHub account (acceptable barrier)

**Status:** Approved

---

## Naming and Organization Decisions

### Decision 10: Command Naming Convention

**Date:** 2025-01-24
**Decision:** Support both standalone kebab-case and category.command-name formats.

**Formats:**
- **Standalone:** `/update-docs` (for high-frequency, well-known commands)
- **Categorized:** `/workflow.branch-create` (for organization, less common commands)

**Rationale:**
- Flexibility for different use cases
- Standalone for frequent tasks (shorter to type)
- Categorized for discovery and organization
- Both validated and supported

**Examples:**
- `/update-docs` (standalone, everyone knows what it does)
- `/code-review` (standalone, universal task)
- `/workflow.branch-create` (categorized, specific workflow)
- `/analysis.performance-audit` (categorized, specific analysis type)

**Validation:**
- Both formats pass name validation
- Standalone: 2-4 words, kebab-case
- Categorized: category.command-name, both kebab-case

**Status:** Approved

---

### Decision 11: Directory Structure (Category Folders)

**Date:** 2025-01-24
**Decision:** Organize commands in category folders: `commands/category/command-name.md`

**Structure:**
```
commands/
├── workflow/
│   ├── update-docs.md
│   ├── pr-create.md
│   └── CATALOG.md
├── analysis/
│   ├── code-review.md
│   └── CATALOG.md
├── generation/
│   └── CATALOG.md
├── git/
│   └── CATALOG.md
└── CATALOG.md (master)
```

**Rationale:**
- Mirrors agents/domain/ and skills/team/ patterns
- Easy browsing by category
- Sub-catalogs enable focused documentation
- Scalable (can add categories without cluttering)

**Status:** Approved

---

## Builder Tool Decisions

### Decision 12: Zero Dependencies (Python 3.8+ Stdlib Only)

**Date:** 2025-01-24
**Decision:** All builder tools use Python 3.8+ standard library only, no external dependencies.

**Rationale:**
- **Consistency:** Matches agent_builder.py and skill_builder.py pattern
- **Portability:** Works everywhere Python is installed
- **Security:** No supply chain risk from dependencies
- **Simplicity:** No pip install needed

**Implications:**
- Custom YAML parser (no PyYAML)
- Standard library file operations
- No third-party CLI frameworks (argparse only)
- Manual implementations where needed

**Proven Success:**
- agent_builder.py: 96% time savings, zero dependencies
- skill_builder.py: 93% time savings, zero dependencies

**Status:** Approved

---

### Decision 13: Command Builder Pattern (Follow Agent/Skill Builders)

**Date:** 2025-01-24
**Decision:** command_builder.py follows proven patterns from agent_builder.py (1,188 lines) and skill_builder.py (1,621 lines).

**Architecture:**
- **CategoryManager:** Dynamic category discovery (no hardcoded lists)
- **CommandValidator:** 8 validation checks (100% passing requirement)
- **TemplateLoader:** Populate command-template.md with user input
- **CommandBuilder:** Orchestrator (interactive + config + validate modes)

**Modes:**
1. **Interactive Mode:** Guided prompts for all metadata
2. **Config Mode:** YAML config file input (batch generation)
3. **Validate Mode:** Check existing command file

**Exit Codes:**
- 0 = Success
- 1 = Validation failed
- 2 = File error
- 3 = Config error

**Rationale:**
- Proven pattern (96% and 93% time savings)
- Consistent user experience
- Reliable validation framework
- Zero dependencies

**Status:** Approved

---

## Validation Decisions

### Decision 14: 8 Validation Checks (100% Passing Required)

**Date:** 2025-01-24
**Decision:** All commands must pass 8 validation checks. No merge without 100% passing.

**Checks:**
1. Name format (kebab-case or category.command-name)
2. YAML frontmatter validity
3. Extended metadata completeness (website fields)
4. Argument handling ($ARGUMENTS)
5. Execution steps present
6. Usage examples (min 2)
7. Dependencies documented
8. Markdown structure

**Rationale:**
- **Quality:** Maintains consistency with agents (28/28) and skills (28/28)
- **Website-Ready:** Ensures all metadata present for website features
- **User Experience:** Complete documentation guarantees usability
- **Automation:** CI/CD enforces automatically

**Enforcement:**
- `command_builder.py --validate` checks all 8
- GitHub Actions blocks merge if validation fails
- Batch validation: `validate_all_commands.py`

**Target:** 100% passing (consistent with agents: 28/28, skills: 28/28)

**Status:** Approved

---

## Future-Proofing Decisions

### Decision 15: Analytics Hooks (Placeholders)

**Date:** 2025-01-24
**Decision:** Include analytics structure in metadata (stats field) even though not actively tracked initially.

**Placeholder Fields:**
```yaml
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: []
```

**Rationale:**
- Website-ready when tracking implemented
- No schema changes needed later
- Encourages thinking about metrics
- Easy to activate tracking later

**Future Activation:**
- Website logs installs (API endpoint)
- Users upvote/rate commands
- Reviews collected and moderated
- Stats displayed on command detail pages

**Status:** Approved

---

### Decision 16: Featured Commands Rotation

**Date:** 2025-01-24
**Decision:** Support featured commands (featured: true|false in metadata) for homepage/landing page highlighting.

**Purpose:**
- Showcase high-value commands
- Rotate seasonally or based on trends
- Manually curated initially
- Data-driven later (most popular, highest rated)

**Implementation:**
- Metadata includes featured field
- `api/featured.json` exports featured commands
- Website homepage displays carousel

**Status:** Approved

---

## Documentation Decisions

### Decision 17: Modular CLAUDE.md Pattern

**Date:** 2025-01-24
**Decision:** Follow existing modular documentation pattern with domain-specific CLAUDE.md files.

**Structure:**
```
CLAUDE.md (root) - Project overview
├── commands/CLAUDE.md - Command development
├── agents/CLAUDE.md - Agent development
├── skills/marketing-team/CLAUDE.md
├── skills/product-team/CLAUDE.md
├── skills/engineering-team/CLAUDE.md
└── docs/standards/CLAUDE.md
```

**Rationale:**
- Consistency with existing structure
- Domain-specific guidance
- Avoids single massive file
- Easy to maintain

**Status:** Approved

---

## Timeline and Scope Decisions

### Decision 18: 8-Week Timeline, 4 Phases

**Date:** 2025-01-24
**Decision:** Phased rollout over 8 weeks to balance speed and quality.

**Phases:**
- **Phase 1 (Weeks 1-2):** Foundation + Top 10 commands
- **Phase 2 (Weeks 3-4):** Expand to 20 + Retrofit agents/skills
- **Phase 3 (Weeks 5-6):** Scale to 28-30 commands
- **Phase 4 (Weeks 7-8):** Polish + Community readiness

**Rationale:**
- Incremental value delivery (10 commands usable after 2 weeks)
- Time for feedback and iteration
- Parallel work (agents retrofit while building commands)
- Achieves "leader" positioning (28-30 commands, comprehensive)

**Alternative Considered:**
- Faster timeline (4 weeks): Risks quality
- Longer timeline (12+ weeks): Delays value delivery

**Status:** Approved

---

### Decision 19: Target 28-30 Commands (Parity with Agents/Skills)

**Date:** 2025-01-24
**Decision:** Target 28-30 production commands to achieve parity with agents (28) and skills (28).

**Rationale:**
- **Leadership Positioning:** Signals equal investment and importance
- **Comprehensive Coverage:** Enough commands for all major use cases
- **Psychological Parity:** Users see consistency across offerings
- **Scalable:** Room to grow beyond 30 based on demand

**Milestone:** 84 total artifacts (28 commands + 28 agents + 28 skills)

**Status:** Approved

---

## Risk Management Decisions

### Decision 20: Parallel Agent Execution for Speed

**Date:** 2025-01-24
**Decision:** Use parallel agent execution (multiple Task tool calls) to accelerate development.

**Wave Strategy:**
- **Wave 1:** Schema + Templates (parallel, no dependencies)
- **Wave 2:** Core tools (parallel, schema-dependent)
- **Wave 3:** 10 commands (parallel, tools-dependent)
- **Wave 4:** Integration (sequential, requires all previous)

**Time Savings:**
- **Traditional Sequential:** ~20 hours
- **Parallel Agents:** ~4.5 hours
- **Savings:** 78% reduction

**Rationale:**
- Maximize Claude Code parallel agent capabilities
- Reduce time to value
- Maintain quality through clear task boundaries
- Each agent has independent deliverables

**Status:** Approved

---

## Decisions Summary

| # | Decision | Status | Impact |
|---|----------|--------|--------|
| 1 | Pandora internal-first, community-ready | Approved | Strategic |
| 2 | Commands as peer to agents/skills | Approved | Strategic |
| 3 | Exclude speckit from library | Approved | Scope |
| 4 | Extended YAML frontmatter | Approved | Technical |
| 5 | GitHub PR review required (ALL) | Approved | Quality |
| 6 | Both formats (Markdown + JSON) | Approved | Technical |
| 7 | Semantic versioning | Approved | Technical |
| 8 | All installation methods | Approved | UX |
| 9 | Community via GitHub PR only | Approved | Quality |
| 10 | Flexible command naming | Approved | UX |
| 11 | Category folders organization | Approved | Structure |
| 12 | Zero dependencies | Approved | Technical |
| 13 | Follow agent/skill builder pattern | Approved | Technical |
| 14 | 8 validation checks, 100% passing | Approved | Quality |
| 15 | Analytics hooks (placeholders) | Approved | Future-proof |
| 16 | Featured commands rotation | Approved | Future-proof |
| 17 | Modular CLAUDE.md pattern | Approved | Documentation |
| 18 | 8-week timeline, 4 phases | Approved | Timeline |
| 19 | Target 28-30 commands | Approved | Scope |
| 20 | Parallel agent execution | Approved | Efficiency |

---

**Document Status:** Active
**Last Updated:** 2025-01-24
**Next Review:** After Phase 1 completion
**Owner:** Ricky Wilson
