# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 27 production-ready skills across 4 domains with 60 Python automation tools.

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
```

## Navigation Map

This repository uses **modular documentation**. For domain-specific guidance, see:

| Domain | CLAUDE.md Location | Focus |
|--------|-------------------|-------|
| **Agent Development** | [agents/CLAUDE.md](agents/CLAUDE.md) | cs-* agent creation, YAML frontmatter, relative paths |
| **Marketing Skills** | [skills/marketing-team/CLAUDE.md](skills/marketing-team/CLAUDE.md) | Content creation, SEO, demand gen Python tools |
| **Product Team** | [skills/product-team/CLAUDE.md](skills/product-team/CLAUDE.md) | RICE, OKRs, user stories, UX research tools |
| **Engineering** | [skills/engineering-team/CLAUDE.md](skills/engineering-team/CLAUDE.md) | Scaffolding, fullstack, AI/ML, data tools, CTO strategy |
| **Delivery Team** | [skills/delivery-team/CLAUDE.md](skills/delivery-team/CLAUDE.md) | Atlassian MCP, Jira/Confluence integration |
| **Standards Library** | [docs/standards/CLAUDE.md](docs/standards/CLAUDE.md) | Communication, quality, git, security standards |
| **Templates** | [templates/CLAUDE.md](templates/CLAUDE.md) | Template system usage |

## Architecture Overview

### Repository Structure

```
claude-code-skills/
├── skills/                    # All skill packages organized by domain
│   ├── marketing-team/        # 3 marketing skills + Python tools
│   ├── product-team/          # 6 product skills + Python tools
│   ├── engineering-team/      # 15 engineering skills + Python tools (includes cto-advisor)
│   └── delivery-team/         # 4 delivery/PM skills + Atlassian MCP
├── agents/                    # Workflow orchestrator agents (cs-* prefix)
│   ├── marketing/            # Marketing domain agents (3 agents)
│   ├── product/              # Product management agents (6 agents)
│   ├── delivery/             # Delivery/PM agents (4 agents)
│   └── engineering/          # Engineering domain agents (15 agents)
├── docs/                      # Documentation and standards
│   ├── standards/            # CLI, git, quality, security standards
│   ├── testing/              # Testing guides and quick starts
│   ├── INSTALL.md            # Installation guide
│   ├── USAGE.md              # Usage examples and workflows
│   └── WORKFLOW.md           # Git workflow guide
├── templates/                 # Reusable templates (agent, CLI, etc.)
├── tools/                     # Testing and validation scripts
└── tests/                     # Test suite (optional)
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

### Agent Architecture (v2.0)

**28 production agents** orchestrate skills through guided workflows:

```
agents/
├── marketing/              # 3 agents
│   ├── cs-content-creator.md
│   ├── cs-demand-gen-specialist.md
│   └── cs-product-marketer.md
├── product/                # 6 agents
│   ├── cs-product-manager.md
│   ├── cs-agile-product-owner.md
│   ├── cs-product-strategist.md
│   ├── cs-ux-researcher.md
│   ├── cs-ui-designer.md
│   └── cs-business-analyst.md
├── delivery/               # 4 agents
│   ├── cs-jira-expert.md
│   ├── cs-confluence-expert.md
│   ├── cs-scrum-master.md
│   └── cs-senior-pm.md
└── engineering/            # 15 agents
    ├── cs-code-reviewer.md
    ├── cs-architect.md
    ├── cs-backend-engineer.md
    ├── cs-frontend-engineer.md
    ├── cs-fullstack-engineer.md
    ├── cs-devops-engineer.md
    ├── cs-security-engineer.md
    ├── cs-secops-engineer.md
    ├── cs-qa-engineer.md
    ├── cs-ml-engineer.md
    ├── cs-data-engineer.md
    ├── cs-data-scientist.md
    ├── cs-computer-vision.md
    ├── cs-prompt-engineer.md
    └── cs-cto-advisor.md
```

**Agent Design Principles:**

1. **cs-* Prefix Convention** - All agents use `cs-` prefix (claude-skills) to distinguish from other agent types
2. **Workflow Orchestration** - Agents guide multi-step processes, invoking skills and tools intelligently
3. **Relative Path Integration** - Agents use `../../skill-package/` paths to access skills from their location
4. **YAML Frontmatter** - Each agent has structured metadata (name, description, skills, domain, model, tools)
5. **4+ Workflows Minimum** - Production agents document at least 4 complete workflows
6. **Tool Integration** - Agents invoke Python CLI tools using bash commands with proper paths

**Agent Structure:**
```markdown
---
name: cs-agent-name
description: What this agent does
skills: skill-package-name
domain: marketing|product|engineering|delivery
model: sonnet|opus
tools: [Read, Write, Bash, Grep, Glob]
---

# Agent Name

## Purpose
[Description]

## Skill Integration
**Skill Location:** `../../skills/domain-team/skill-package/`

### Python Tools
```bash
python ../../skills/domain-team/skill-package/scripts/tool.py input.txt
```

## Workflows
### Workflow 1: [Name]
[Step-by-step guide]

## Success Metrics
[How to measure effectiveness]
```

**Agent vs. Skill Distinction:**
- **Skills** = Tools + Knowledge + Templates (the "what")
- **Agents** = Workflow Orchestrators (the "how")
- Agents invoke skills intelligently based on context and guide users through complex processes

**Learn More:** See [agents/CLAUDE.md](agents/CLAUDE.md) for agent development guide and [templates/agent-template.md](templates/agent-template.md) for the creation template.

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
See [docs/standards/git/git-workflow-standards.md](docs/standards/git/git-workflow-standards.md) for commit standards.

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

**Testing Python Tools:**
```bash
# Test with --help flag (all tools must support this)
python <domain-skill>/<skill-name>/scripts/<tool>.py --help

# Test execution with sample data
echo "Sample content for testing" > test-input.txt
python skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py test-input.txt
python skills/marketing-team/content-creator/scripts/seo_optimizer.py test-input.txt "test keyword"
rm test-input.txt

# Test JSON output format
python skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py content.txt json
```

**If adding dependencies in the future:**
- Keep scripts runnable with minimal setup (`pip install package` at most)
- Create a requirements.txt file and document all dependencies in SKILL.md
- Prefer standard library implementations whenever possible

## Roadmap

**Phase 1 Complete:** 26 Pandora-focused skills deployed
- Marketing (3), Product (6), Delivery/PM (4), Engineering (15 including CTO advisor)
- 60 Python automation tools, 60+ reference guides
- Complete coverage for Pandora's marketing, product, engineering, and delivery teams

**Next Priorities:**
- **Phase 2 (Q1 2026):** Marketing expansion - SEO optimizer, social media manager, campaign analytics
- **Phase 3 (Q2 2026):** Business & growth - Sales engineer, customer success, growth marketer
- **Phase 4 (Q3 2026):** Specialized domains - Mobile, blockchain, web3, finance

**Target:** 35+ Pandora-focused skills by Q3 2026

See domain-specific roadmaps in each skill folder's README.md or roadmap files.

## Builder Tools (Automated Creation & Validation)

The repository includes **zero-dependency builder tools** that automate agent and skill creation, reducing development time by 93-96%.

### Agent Builder

**Purpose**: Create and validate cs-* agents with guided workflows

```bash
# Interactive mode (recommended for new agents)
python3 scripts/agent_builder.py

# Config file mode (for automation)
python3 scripts/agent_builder.py --config examples/agent-config-example.yaml

# Validate existing agent
python3 scripts/agent_builder.py --validate agents/marketing/cs-content-creator.md
```

**Features**:
- 9 validation checks (YAML, paths, workflows, examples, metrics, structure)
- Dynamic domain discovery (create custom domains on-the-fly)
- Template-based generation with placeholder replacement
- Zero external dependencies (custom YAML parser)
- Time savings: **2 days → 1 hour (96% faster)**

**Validation Criteria**:
- ✓ Valid YAML frontmatter (name, description, skills, domain, model, tools)
- ✓ Correct relative paths (`../../skills/`)
- ✓ 4+ documented workflows
- ✓ 2+ integration examples
- ✓ 3+ success metric categories
- ✓ Complete markdown structure

### Skill Builder

**Purpose**: Create and validate skill packages with full directory scaffolding

```bash
# Interactive mode (recommended for new skills)
python3 scripts/skill_builder.py

# Config file mode (for automation)
python3 scripts/skill_builder.py --config skill-config.yaml

# Validate existing skill
python3 scripts/skill_builder.py --validate skills/marketing-team/content-creator
```

**Features**:
- 9 validation checks (structure, metadata, sections, tools, references)
- Full directory scaffolding (scripts/, references/, assets/)
- Placeholder Python tool generation
- Extended metadata YAML support
- Zero external dependencies
- Time savings: **3 days → 2 hours (93% faster)**

**Validation Criteria**:
- ✓ Valid directory structure (scripts/, references/, assets/)
- ✓ SKILL.md with required sections (Overview, Core Capabilities, Key Workflows)
- ✓ Extended metadata YAML (version, author, category, keywords, tech-stack)
- ✓ Python tools marked executable (chmod +x)
- ✓ Valid YAML frontmatter

### Skill Upgrade Tool

**Purpose**: Batch upgrade existing skills to new validation standards

```bash
# Dry run (preview changes)
python3 scripts/upgrade_skills_to_new_standards.py

# Execute upgrades
python3 scripts/upgrade_skills_to_new_standards.py --execute

# Upgrade specific skill
python3 scripts/upgrade_skills_to_new_standards.py --skill content-creator --execute
```

**Automated Fixes**:
- Makes Python tools executable (chmod +x)
- Creates missing directories (assets/, scripts/)
- Adds extended metadata YAML
- Adds missing SKILL.md sections (Overview, Core Capabilities, Key Workflows)

**Result**: Upgraded all 28 skills from 5.5/9 average to 7.5/9 (36% improvement)

## Common Development Tasks

### Creating a New Skill (Automated)

```bash
# Use the skill builder for 93% time savings (3 days → 2 hours)
python3 scripts/skill_builder.py

# Follow 8-step interactive workflow:
# 1. Choose team (marketing-team, product-team, engineering-team, delivery-team, or create new)
# 2. Enter skill name (lowercase-with-hyphens)
# 3. Enter description (1-2 sentences)
# 4. Enter category (domain area)
# 5. List Python tools (comma-separated)
# 6. List reference files (comma-separated)
# 7. Enter tech stack (comma-separated)
# 8. Enter keywords (comma-separated)

# Builder creates complete skill structure with:
# - SKILL.md with extended metadata
# - scripts/ with placeholder Python tools
# - references/ with placeholder markdown files
# - assets/ with .gitkeep

# Validate before committing
python3 scripts/skill_builder.py --validate skills/<team>/<skill-name>
```

### Creating a New Agent (Automated)

```bash
# Use the agent builder for 96% time savings (2 days → 1 hour)
python3 scripts/agent_builder.py

# Follow 7-step interactive workflow:
# 1. Enter agent name (cs-prefix, lowercase-with-hyphens)
# 2. Choose domain (marketing, product, engineering, delivery, or create new)
# 3. Enter description (under 150 chars)
# 4. Enter skill package reference (team/skill-name)
# 5. Choose model (sonnet, opus, haiku)
# 6. Select tools (Read, Write, Bash, Grep, Glob, etc.)
# 7. Review and confirm

# Builder creates complete agent with:
# - Valid YAML frontmatter
# - Skill Integration section with correct relative paths
# - 4 workflow templates
# - 2 integration example templates
# - Success Metrics template
# - Related Agents template
# - References template

# Validate before committing
python3 scripts/agent_builder.py --validate agents/<domain>/cs-<agent-name>.md
```

**Config File Mode** (for automation/CI):
```bash
# Create config file
cat > agent-config.yaml << EOF
name: cs-data-analyst
domain: engineering
description: Data analysis and reporting for product decisions
skills: data-analyst-toolkit
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
EOF

# Generate agent from config
python3 scripts/agent_builder.py --config agent-config.yaml
```

### Testing and Validation

```bash
# Validate all agents (recommended before committing)
for agent in agents/**/cs-*.md; do
    python3 scripts/agent_builder.py --validate "$agent"
done

# Validate all skills (recommended before committing)
for team in skills/*/; do
    for skill in $team*/; do
        [ -f "$skill/SKILL.md" ] && python3 scripts/skill_builder.py --validate "$skill"
    done
done

# Validate Python syntax
find . -name "*.py" -type f -exec python3 -m py_compile {} \;

# Test Python tools with --help flag
for tool in $(find skills -name "*.py" -path "*/scripts/*"); do
    echo "Testing: $tool"
    python3 "$tool" --help || echo "❌ FAILED: $tool"
done

# Check for secrets (pre-commit check)
git diff --cached | grep -iE '(api[_-]?key|secret|password|token).*=.*[^x{5}]' && echo "⚠️  Potential secret detected"
```

**Validation Success Metrics**:
- All agents: 28/28 passing (100% as of Nov 2025)
- All skills: 28/28 passing validation (100% as of Nov 2025)
- Zero external dependencies for builders
- Average validation time: < 2 seconds per agent/skill

### Slash Commands

Available slash commands (from `.claude/commands/`):

See `.claude/commands/` directory for available slash commands. The repository uses custom slash commands for workflow automation.

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
- Over-documenting file structure (skills are simple by design)
- Hardcoding absolute paths in agents (always use `../../` pattern)
- Committing directly to main (use feature branches and PRs)

## Working with This Repository

**Creating New Skills:** Follow the appropriate domain's roadmap and CLAUDE.md guide (see Navigation Map above).

**Editing Existing Skills:** Maintain consistency across markdown files. Use the same voice, formatting, and structure patterns.

**Quality Standard:** Each skill should save users 40%+ time while improving consistency/quality by 30%+.

## Troubleshooting

### Python Tools Not Working

```bash
# Issue: Module not found (shouldn't happen with standard library)
# Solution: Verify Python version
python3 --version  # Should be 3.8+

# Issue: Permission denied
# Solution: Make script executable
chmod +x skills/<domain-team>/<skill-name>/scripts/<tool>.py

# Issue: Tool returns unexpected output
# Solution: Test with --help first
python <tool>.py --help

# Solution: Check Python version (requires 3.8+)
python --version
```

### Agent Relative Paths Failing

```bash
# Issue: Agent can't find skill files
# Solution: Verify path resolution from agent location
cd agents/<domain>/
ls ../../skills/<domain-team>/<skill-name>/  # Should list files

# Issue: Path works locally but not in Claude Code
# Solution: Always use ../../skills/ pattern, never absolute paths
# Wrong: /Users/name/claude-skills/marketing-team/
# Right: ../../skills/marketing-team/
```

### Git Workflow Issues

```bash
# Issue: Can't push to main
# Solution: Main is protected - use PRs
git checkout dev
git checkout -b feature/my-changes
# ... make changes ...
git push origin feature/my-changes
gh pr create --base dev

# Issue: Commit rejected (conventional commits)
# Solution: Use correct format
# Wrong: "updated files"
# Right: "feat(agents): implement cs-new-agent"

# Issue: Merge conflicts
# Solution: Sync with dev first
git checkout feature/my-branch
git pull origin dev
# ... resolve conflicts ...
git add .
git commit -m "chore: resolve merge conflicts"
```

### Virtual Environment Issues

```bash
# Issue: Virtual environment not activating
# Solution: Recreate it
rm -rf claude-skills_venv
python3 -m venv claude-skills_venv
source claude-skills_venv/bin/activate
# No pip install needed - all tools use standard library

# Issue: Wrong Python version in venv
# Solution: Specify Python version (3.8+ required)
python3.9 -m venv claude-skills_venv
# or
python3.11 -m venv claude-skills_venv
```

## Agent Output Directory

All agent-generated reports, analyses, and outputs are saved using a **session-based organization system** that provides user attribution, work context tracking, and integration with knowledge management systems (Confluence, Jira).

### Session-Based System (v2.0)

**Key Features:**
- User-isolated session directories
- Rich metadata (ticket, project, team, stakeholders)
- Git-tracked for collaboration
- Manual Confluence promotion workflow
- Retention policies (project, sprint, temporary)

**Quick Start:**
```bash
# 1. Create a work session
python3 scripts/session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Automation" \
  --team engineering

# 2. Generate outputs to session (flat structure)
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py transcript.md \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.md

# 3. Close session when complete
python3 scripts/session_manager.py close
```

**Directory Structure:**
```
output/
├── sessions/                           # User session outputs (git-tracked)
│   └── {user}/
│       └── {session-id}/
│           ├── .session-metadata.yaml  # Session context
│           └── *.md                    # All outputs (flat structure, categorized via metadata)
├── shared/
│   ├── promoted-to-confluence/         # Manually promoted outputs
│   └── team-resources/                 # Team-shared resources
└── archive/                            # Archived sessions
```

**Session Management:**
```bash
# List sessions
python3 scripts/session_manager.py list --status active

# Search sessions
python3 scripts/session_manager.py search --ticket PROJ-123

# Generate report
python3 scripts/session_manager.py report
```

**Git Workflow:** Sessions are **git-tracked** (unlike old system). Commit sessions for collaboration:
```bash
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
git commit -m "feat(sessions): create session for invoice automation analysis"
```

**Migration:** All previous outputs migrated to `output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/`

See [output/README.md](output/README.md) for complete session-based workflow guide.

## Additional Resources

- **.gitignore:** Excludes .vscode/, .DS_Store, AGENTS.md, PROMPTS.md, .env*, *_venv/, output/*
- **Output Directory:** [output/README.md](output/README.md) - Agent output naming conventions and guidelines
- **Standards Library:** [docs/standards/](docs/standards/) - Communication, quality, git, documentation, security
- **Workflow Guide:** [docs/WORKFLOW.md](docs/WORKFLOW.md) - Branch strategy and deployment pipeline
- **Installation Guide:** [docs/INSTALL.md](docs/INSTALL.md) - Setup instructions
- **Usage Guide:** [docs/USAGE.md](docs/USAGE.md) - Examples and workflows
- **Testing Guides:** [docs/testing/](docs/testing/) - Testing documentation

## File Locations Quick Reference

```
claude-skills/
├── skills/                        # All skill packages organized by domain
│   ├── marketing-team/            # Marketing skills
│   ├── product-team/              # Product skills
│   ├── engineering-team/          # Engineering skills (includes cto-advisor)
│   └── delivery-team/             # Delivery/PM skills
│   └── <skill-name>/
│       ├── SKILL.md               # Master documentation
│       ├── scripts/               # Python tools (executable)
│       ├── references/            # Knowledge bases
│       └── assets/                # User templates
├── agents/                        # cs-* agents (orchestrate skills)
│   ├── marketing/                 # Marketing agents
│   ├── product/                   # Product agents
│   └── CLAUDE.md                  # Agent development guide
├── docs/                          # Documentation and standards
│   ├── WORKFLOW.md                # Git workflow guide
│   ├── INSTALL.md                 # Installation guide
│   ├── USAGE.md                   # Usage examples
│   ├── testing/                   # Testing guides
│   └── standards/                 # All standards (communication, quality, git, documentation, security)
├── output/                        # Agent-generated reports (gitignored by default)
│   ├── architecture/              # Architecture reviews, diagrams, design docs
│   ├── reviews/                   # Code reviews, quality assessments
│   ├── analysis/                  # Dependency, performance, security analysis
│   ├── reports/                   # General reports and summaries
│   └── README.md                  # Output directory guidelines
├── templates/                     # Templates
│   ├── agent-template.md          # Agent creation template
│   └── skill-template.md          # Skill creation template
└── CLAUDE.md                      # This file
```

---

**Last Updated:** November 22, 2025
**Current Focus:** Agent completion - 28 production agents for 27 Pandora skills
**Status:** 27 Pandora-focused skills across 4 domains, 28 production agents (v2.0)
**Python Version:** 3.8+ required
**Dependencies:** None - all tools use Python standard library only
