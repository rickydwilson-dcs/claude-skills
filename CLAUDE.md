# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 28 production agents, 28 skills across 4 domains with 60 Python automation tools, 20 slash commands.

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be extracted and deployed by users into their own Claude workflows.

## Quick Start for Development

```bash
# Setup Python environment (optional - no dependencies needed)
python3 -m venv claude-skills_venv
source claude-skills_venv/bin/activate  # On Windows: claude-skills_venv\Scripts\activate

# Test a Python tool - works immediately, no pip install needed!
python skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py --help
python skills/marketing-team/content-creator/scripts/seo_optimizer.py --help

# Create new agent (interactive mode - 96% faster than manual)
python3 scripts/agent_builder.py

# Create new skill (interactive mode - 93% faster than manual)
python3 scripts/skill_builder.py

# Validate existing agent
python3 scripts/agent_builder.py --validate agents/marketing/cs-content-creator.md

# Validate existing skill
python3 scripts/skill_builder.py --validate skills/marketing-team/content-creator

# Install slash commands
python3 scripts/install_commands.py

# Use installed commands
/speckit.specify "Add user authentication"
```

## Navigation Map

This repository uses **modular documentation**. For domain-specific guidance, see:

| Domain | CLAUDE.md Location | Focus |
|--------|-------------------|-------|
| **Agent Development** | [agents/CLAUDE.md](agents/CLAUDE.md) | cs-* agent creation, YAML frontmatter, relative paths |
| **Slash Commands** | [commands/CLAUDE.md](commands/CLAUDE.md) | Command creation, patterns, validation |
| **Marketing Skills** | [skills/marketing-team/CLAUDE.md](skills/marketing-team/CLAUDE.md) | Content creation, SEO, demand gen Python tools |
| **Product Team** | [skills/product-team/CLAUDE.md](skills/product-team/CLAUDE.md) | RICE, OKRs, user stories, UX research tools |
| **Engineering** | [skills/engineering-team/CLAUDE.md](skills/engineering-team/CLAUDE.md) | Scaffolding, fullstack, AI/ML, data tools, CTO strategy |
| **Delivery Team** | [skills/delivery-team/CLAUDE.md](skills/delivery-team/CLAUDE.md) | Atlassian MCP, Jira/Confluence integration |
| **Standards Library** | [docs/standards/CLAUDE.md](docs/standards/CLAUDE.md) | Communication, quality, git, security standards |
| **Templates** | [templates/CLAUDE.md](templates/CLAUDE.md) | Template system usage |

## Architecture Overview

### Repository Structure

```
claude-skills/
├── skills/                    # All skill packages organized by domain
│   ├── marketing-team/        # 3 marketing skills + Python tools
│   ├── product-team/          # 6 product skills + Python tools
│   ├── engineering-team/      # 15 engineering skills + Python tools
│   └── delivery-team/         # 4 delivery/PM skills + Atlassian MCP
├── agents/                    # Workflow orchestrator agents (cs-* prefix)
│   ├── marketing/            # 3 agents
│   ├── product/              # 6 agents
│   ├── delivery/             # 4 agents
│   └── engineering/          # 15 agents
├── commands/                  # Slash commands library
│   ├── analysis/             # Analysis commands (4)
│   ├── generation/           # Code generation (2)
│   ├── git/                  # Git workflow (2)
│   ├── workflow/             # Team workflow (3)
│   └── .claude/commands/     # Speckit workflow (8)
├── docs/                      # Documentation and standards
├── scripts/                   # Builder tools and utilities
├── templates/                 # Reusable templates
└── output/                    # Session-based outputs (git-tracked)
```

### Skill Package Pattern

Each skill follows this structure:
```
skill-name/
├── SKILL.md              # Master documentation
├── scripts/              # Python CLI tools (no ML/LLM calls)
├── references/           # Expert knowledge bases
└── assets/               # User templates
```

**Design Philosophy**: Skills are self-contained packages. Each includes executable tools (Python scripts), knowledge bases (markdown references), and user-facing templates. Teams can extract a skill folder and use it immediately.

**Key Pattern**: Knowledge flows from `references/` → into `SKILL.md` workflows → executed via `scripts/` → applied using `assets/` templates.

### Agent Architecture

**28 production agents** orchestrate skills through guided workflows across 4 domains (marketing, product, engineering, delivery).

**Key Principles:**
- **cs-* Prefix Convention** - All agents use `cs-` prefix (claude-skills)
- **Workflow Orchestration** - Agents guide multi-step processes
- **Relative Path Integration** - Agents use `../../skill-package/` paths
- **YAML Frontmatter** - Structured metadata (name, description, skills, domain, model, tools)
- **4+ Workflows Minimum** - Production agents document at least 4 complete workflows

**Agent vs. Skill Distinction:**
- **Skills** = Tools + Knowledge + Templates (the "what")
- **Agents** = Workflow Orchestrators (the "how")

**Learn More:** See [agents/CLAUDE.md](agents/CLAUDE.md) for complete agent architecture and [docs/AGENTS_CATALOG.md](docs/AGENTS_CATALOG.md) for full agent list.

### Slash Commands Architecture

**20 production commands** automate high-frequency developer workflows across 6 categories (general/speckit, analysis, generation, git, workflow, test).

**Key Principles:**
- **category.command-name Pattern** - All commands use kebab-case with category prefix
- **Task Automation** - Commands execute focused, repetitive tasks
- **3 Official Patterns** - Simple, Multi-Phase, Agent-Style (Anthropic standards)
- **YAML Frontmatter** - Structured metadata (name, description, category, pattern, tools)
- **50%+ Time Savings** - Commands save significant time on repetitive work

**Command vs. Agent vs. Skill Distinction:**
- **Commands** = Quick task automation (seconds-minutes)
- **Agents** = Workflow orchestrators (minutes-hours)
- **Skills** = Tools + Knowledge + Templates

**Available Command Categories:**
- **General (Speckit)** - 8 commands for specification-driven development workflow
- **Analysis** - 4 commands for code review, security, dependencies, refactoring
- **Generation** - 2 commands for test generation and API documentation
- **Git** - 2 commands for commit assistance and branch cleanup
- **Workflow** - 3 commands for PRs, docs, feature prioritization
- **Test** - 1 sample command for development

**Learn More:** See [commands/README.md](commands/README.md) for complete command library, [commands/CLAUDE.md](commands/CLAUDE.md) for development guide, and [commands/CATALOG.md](commands/CATALOG.md) for full command list.

**Quick Start:**
```bash
# Install commands
python3 scripts/install_commands.py

# Use commands
/speckit.specify "Add user authentication"
/analysis.code-review src/
/generation.test-generate
```

## Git Workflow

**Branch Strategy:** develop → staging → main (quality gates)

**Branch Protection Active:** Main branch requires PR approval. Direct pushes blocked.

### Quick Start

```bash
# 1. Work on develop branch (or create feature branch)
git checkout develop
git pull origin develop

# 2. Create feature branch (optional, for large features)
git checkout -b feature/agents-{name}

# 3. Work and commit (conventional commits)
feat(agents): implement cs-{agent-name}
fix(tool): correct calculation logic
docs(workflow): update branch strategy

# 4. Merge feature to develop (if using feature branch)
git checkout develop
git merge feature/agents-{name}
git push origin develop

# 5. Promote to staging
git checkout staging
git merge develop
git push origin staging

# 6. Deploy to production
git checkout main
git merge staging
git push origin main
```

**Branch Protection Rules:**
- ✅ Main: Production-ready code only, requires validation
- ✅ Staging: Pre-production validation environment
- ✅ Develop: Primary development branch
- ✅ All: Conventional commits enforced

See [docs/WORKFLOW.md](docs/WORKFLOW.md) for complete workflow guide.

## Session Tracking

**All work is tracked in session-based output directories** for attribution, context, and collaboration.

### Session Structure

```
output/sessions/{user}/{session-id}/
├── .session-metadata.yaml    # YAML tracking (REQUIRED)
├── SESSION_METADATA.md        # Human-readable summary
├── COMPLETION_SUMMARY.md      # Executive summary
└── *.md                       # All work outputs
```

### Creating Sessions

**Always create a session before starting work:**

```bash
# Get username (use system username or identifier)
USER=$(whoami)

# Create timestamp-based session ID
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
SESSION_ID="${TIMESTAMP}_${description}"

# Create session directory
mkdir -p "output/sessions/${USER}/${SESSION_ID}"

# Create .session-metadata.yaml with required fields:
# - session_id, created_at, user, team, status
# - work_context (branch, project, description)
# - outputs (list of files created)
# - retention policy and expiration

# Update current session pointer
echo "${USER}/${SESSION_ID}" > output/.current-session
```

**Session Naming Convention:**
- Format: `{YYYY-MM-DD}_{HH-MM-SS}_{description}`
- Description: kebab-case, concise (e.g., `command-verb-object-renaming`)
- Examples:
  - `2025-11-24_21-34-54_command-verb-object-renaming`
  - `2025-11-22_14-30-00_skill-builder-enhancement`
  - `2025-11-20_09-15-00_agent-validation-fixes`

### Session Metadata Requirements

Every session MUST include `.session-metadata.yaml`:

```yaml
session_id: 2025-11-24_21-34-54_command-verb-object-renaming
created_at: 2025-11-24T21:34:54
user: rickywilson
team: engineering
status: active  # or closed

work_context:
  branch: feature/slash-commands-library
  project: Command Naming Standardization
  description: Complete migration to verb.object pattern

outputs:
  - file: COMPLETION_SUMMARY.md
    type: summary
    created_at: 2025-11-24T21:34:54

retention:
  policy: project  # or sprint, temporary
  expires_at: 2026-05-24

tags:
  - command-naming
  - standardization
```

### Why Sessions Matter

1. **Attribution** - Know who did what and when
2. **Context** - Understand the purpose of each piece of work
3. **Searchability** - Find work by user, date, or project
4. **Collaboration** - Git-tracked sessions enable team review
5. **Retention** - Automatic cleanup based on policies

### Quick Reference

```bash
# Current session
cat output/.current-session

# List user sessions
ls -la output/sessions/${USER}/

# View session metadata
cat output/sessions/${USER}/${SESSION_ID}/.session-metadata.yaml
```

**Learn More:** See [output/README.md](output/README.md) for complete session management guide.

## Builder Tools (Automated Creation)

The repository includes **zero-dependency builder tools** that automate agent and skill creation:

### Agent Builder
```bash
# Create new agent interactively (96% faster: 2 days → 1 hour)
python3 scripts/agent_builder.py

# Validate existing agent
python3 scripts/agent_builder.py --validate agents/marketing/cs-content-creator.md
```

**Features**: 9 validation checks, dynamic domain discovery, template-based generation
**Time Savings**: 2 days → 1 hour (96% faster)

### Skill Builder
```bash
# Create new skill interactively (93% faster: 3 days → 2 hours)
python3 scripts/skill_builder.py

# Validate existing skill
python3 scripts/skill_builder.py --validate skills/marketing-team/content-creator
```

**Features**: Full directory scaffolding, extended metadata YAML, placeholder generation
**Time Savings**: 3 days → 2 hours (93% faster)

### Validation
- **All agents**: 28/28 passing (100%)
- **All skills**: 28/28 passing (100%)
- **Zero external dependencies** for builders
- **Standards**: See [docs/standards/builder-standards.md](docs/standards/builder-standards.md)

## Development Environment

**No build system or test frameworks** - intentional design choice for portability.

**Python Environment Setup:**
```bash
# Create virtual environment (recommended)
python3 -m venv claude-skills_venv
source claude-skills_venv/bin/activate

# No dependencies needed - all scripts use standard library only
python3 -c "print('Python environment ready')"
```

**Python Scripts:**
- Use standard library only (minimal dependencies)
- CLI-first design for easy automation
- Support both JSON and human-readable output
- No ML/LLM calls (keeps skills portable and fast)

## Key Principles

1. **Skills are products** - Each skill deployable as standalone package
2. **Documentation-driven** - Success depends on clear, actionable docs
3. **Algorithm over AI** - Use deterministic analysis (code) vs LLM calls
4. **Template-heavy** - Provide ready-to-use templates users customize
5. **Platform-specific** - Specific best practices > generic advice

## Anti-Patterns to Avoid

- Creating dependencies between skills (keep each self-contained)
- Adding complex build systems or test frameworks (maintain simplicity)
- Generic advice (focus on specific, actionable frameworks)
- LLM calls in scripts (defeats portability and speed)
- Hardcoding absolute paths in agents (always use `../../` pattern)
- Committing directly to main (use develop → staging → main)

## Working with This Repository

**Creating New Skills:** Use `python3 scripts/skill_builder.py` for 93% time savings. See domain CLAUDE.md for guidance.

**Creating New Agents:** Use `python3 scripts/agent_builder.py` for 96% time savings. See [agents/CLAUDE.md](agents/CLAUDE.md) for details.

**Editing Existing Skills:** Maintain consistency across markdown files. Use the same voice, formatting, and structure patterns.

**Quality Standard:** Each skill should save users 40%+ time while improving consistency/quality by 30%+.

## Additional Resources

### Documentation
- **[docs/WORKFLOW.md](docs/WORKFLOW.md)** - Branch strategy and deployment pipeline
- **[docs/INSTALL.md](docs/INSTALL.md)** - Setup instructions
- **[docs/USAGE.md](docs/USAGE.md)** - Usage examples and workflows
- **[docs/AGENTS_CATALOG.md](docs/AGENTS_CATALOG.md)** - Complete agent list with validation status
- **[docs/SKILLS_CATALOG.md](docs/SKILLS_CATALOG.md)** - Complete skill list with validation status
- **[commands/CATALOG.md](commands/CATALOG.md)** - Complete command list with patterns and categories
- **[docs/standards/](docs/standards/)** - Communication, quality, git, documentation, security standards

### Slash Commands
- **[commands/README.md](commands/README.md)** - Slash commands library overview and quick start
- **[commands/CLAUDE.md](commands/CLAUDE.md)** - Command development guide and patterns
- **[commands/CATALOG.md](commands/CATALOG.md)** - All 20 commands with categories and statistics
- **[docs/COMMANDS_INSTALLATION.md](docs/COMMANDS_INSTALLATION.md)** - Installation guide and troubleshooting
- **[docs/COMMANDS_CREATION.md](docs/COMMANDS_CREATION.md)** - Step-by-step command creation tutorial
- Install commands: `python3 scripts/install_commands.py`

### Output Directory
- **[output/README.md](output/README.md)** - Session-based output organization system
- Git-tracked sessions for collaboration
- User-isolated directories with rich metadata

### Testing
- **[docs/testing/](docs/testing/)** - Testing guides and quick starts
- Validate all agents: `python3 scripts/validate_all_agents.sh`
- Test Python tools: All must support `--help` flag

### Troubleshooting
Common issues and solutions documented in domain-specific CLAUDE.md files:
- Python tools: See [skills/CLAUDE.md](skills/marketing-team/CLAUDE.md)
- Agent paths: See [agents/CLAUDE.md](agents/CLAUDE.md)
- Command installation: See [docs/COMMANDS_INSTALLATION.md#troubleshooting](docs/COMMANDS_INSTALLATION.md#troubleshooting)
- Git workflow: See [docs/WORKFLOW.md](docs/WORKFLOW.md)

---

**Last Updated:** November 24, 2025
**Current Status:** 28 production agents, 28 skills across 4 domains, 20 slash commands
**Python Version:** 3.8+ required
**Dependencies:** None - all tools use Python standard library only
