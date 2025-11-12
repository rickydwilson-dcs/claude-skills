# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **comprehensive skills library** for Claude AI - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks. The repository provides modular skills that teams can download and use directly in their workflows.

**Current Scope:** 26 production-ready skills across 4 domains with 77 Python automation tools.

**Key Distinction**: This is NOT a traditional application. It's a library of skill packages meant to be extracted and deployed by users into their own Claude workflows.

## Quick Start for Development

```bash
# Setup Python environment
python3 -m venv claude-skills_venv
source claude-skills_venv/bin/activate  # On Windows: claude-skills_venv\Scripts\activate
pip install -r requirements.txt

# Test a Python tool
python skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py --help
python skills/marketing-team/content-creator/scripts/seo_optimizer.py --help

# Run agent validation (if available)
find agents -name "cs-*.md" -exec echo "Validating: {}" \;
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

**Current Sprint:** See [docs/delivery/sprint-11-05-2025/](docs/delivery/sprint-11-05-2025/) for active sprint context and progress.

## Architecture Overview

### Repository Structure

```
claude-code-skills/
├── skills/                    # All skill packages organized by domain
│   ├── marketing-team/        # 3 marketing skills + Python tools
│   ├── product-team/          # 5 product skills + Python tools
│   ├── engineering-team/      # 15 engineering skills + Python tools (includes cto-advisor)
│   └── delivery-team/         # 6 delivery/PM skills + Atlassian MCP
├── agents/                    # Workflow orchestrator agents (cs-* prefix)
│   ├── marketing/            # Marketing domain agents
│   └── product/              # Product management agents
├── docs/                      # Standards, migration docs, sprints
│   ├── standards/            # CLI, git, quality, security standards
│   ├── implementation/       # Implementation plans
│   └── delivery/             # Sprint tracking
├── templates/                 # Reusable templates (agent, CLI, etc.)
├── tools/                     # Testing and validation scripts
└── tests/                     # Automated pytest tests
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

### Agent Architecture (v1.0)

**3 production agents** orchestrate skills through guided workflows:

```
agents/
├── marketing/
│   ├── cs-content-creator.md         # SEO-optimized content creation
│   └── cs-demand-gen-specialist.md   # Lead gen & conversion funnel
└── product/
    └── cs-product-manager.md         # RICE prioritization & roadmaps
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

**Branch Strategy:** feature → dev → main (PR only)

**Branch Protection Active:** Main branch requires PR approval. Direct pushes blocked.

### Quick Start

```bash
# 1. Always start from dev
git checkout dev
git pull origin dev

# 2. Create feature branch
git checkout -b feature/agents-{name}

# 3. Work and commit (conventional commits)
feat(agents): implement cs-{agent-name}
fix(tool): correct calculation logic
docs(workflow): update branch strategy

# 4. Push and create PR to dev
git push origin feature/agents-{name}
gh pr create --base dev --head feature/agents-{name}

# 5. After approval, PR merges to dev
# 6. Periodically, dev merges to main via PR
```

**Branch Protection Rules:**
- ✅ Main: Requires PR approval, no direct push
- ✅ Dev: Unprotected, but PRs recommended
- ✅ All: Conventional commits enforced

See [documentation/WORKFLOW.md](documentation/WORKFLOW.md) for complete workflow guide.
See [standards/git/git-workflow-standards.md](standards/git/git-workflow-standards.md) for commit standards.

## Development Environment

**No build system or test frameworks** - intentional design choice for portability.

**Python Environment Setup:**
```bash
# Create virtual environment (recommended)
python3 -m venv claude-skills_venv
source claude-skills_venv/bin/activate

# Install dependencies (minimal - only pyyaml currently)
pip install -r requirements.txt

# Verify setup
python -c "import yaml; print('Environment ready')"
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

**If adding dependencies:**
- Keep scripts runnable with minimal setup (`pip install package` at most)
- Document all dependencies in SKILL.md and update requirements.txt
- Prefer standard library implementations

## Current Sprint

**Active Sprint:** sprint-11-05-2025 (Nov 5-19, 2025)
**Goal:** Skill-Agent Integration Phase 1-2
**Status:** ✅ COMPLETE - All 6 days finished, 3 agents deployed

**Deliverables:**
- 3 production agents: cs-content-creator, cs-demand-gen-specialist, cs-product-manager
- 1 agent template for future development
- Modular documentation structure (main + domain CLAUDE.md files)
- Three-tier deployment pipeline (develop → staging → main)

**Progress Tracking:**
- [Sprint Plan](docs/delivery/sprint-11-05-2025/plan.md) - Day-by-day execution plan
- [Sprint Context](docs/delivery/sprint-11-05-2025/context.md) - Goals, scope, risks
- [Sprint Progress](docs/delivery/sprint-11-05-2025/PROGRESS.md) - Real-time auto-updating tracker

## Roadmap

**Phase 1 Complete:** 26 Pandora-focused skills deployed
- Marketing (3), Product (5), Delivery/PM (6), Engineering (15 including CTO advisor)
- 77 Python automation tools, 60+ reference guides
- Complete coverage for Pandora's marketing, product, engineering, and delivery teams

**Next Priorities:**
- **Phase 2 (Q1 2026):** Marketing expansion - SEO optimizer, social media manager, campaign analytics
- **Phase 3 (Q2 2026):** Business & growth - Sales engineer, customer success, growth marketer
- **Phase 4 (Q3 2026):** Specialized domains - Mobile, blockchain, web3, finance

**Target:** 35+ Pandora-focused skills by Q3 2026

See domain-specific roadmaps in each skill folder's README.md or roadmap files.

## Common Development Tasks

### Creating a New Skill

```bash
# 1. Create skill directory structure
mkdir -p skills/<domain-team>/<skill-name>/{scripts,references,assets}

# 2. Create SKILL.md from template
cp templates/skill-template.md skills/<domain-team>/<skill-name>/SKILL.md

# 3. Add Python tools to scripts/
# All tools must:
# - Support --help flag
# - Accept JSON output mode
# - Use standard library (or update requirements.txt)
# - Follow CLI-first design

# 4. Add knowledge bases to references/
# - Markdown format
# - Expert-level content
# - Platform-specific guidance

# 5. Add templates to assets/
# - User-customizable
# - Copy-paste ready

# 6. Test skill integration
python skills/<domain-team>/<skill-name>/scripts/<tool>.py --help
```

### Creating a New Agent

```bash
# 1. Use agent template
cp templates/agent-template.md agents/<domain>/cs-<agent-name>.md

# 2. Update YAML frontmatter
# - name: cs-<agent-name>
# - description: One-line purpose
# - skills: skill-folder-name
# - domain: marketing|product|engineering|delivery
# - model: sonnet|opus|haiku
# - tools: [Read, Write, Bash, Grep, Glob]

# 3. Document workflows (minimum 3)
# - Clear step-by-step instructions
# - Specific tool/command references
# - Expected outputs
# - Time estimates

# 4. Test relative paths (CRITICAL)
cd agents/<domain>/
ls ../../skills/<domain-team>/<skill-name>/  # Must resolve correctly

# 5. Test Python tool execution
python ../../skills/<domain-team>/<skill-name>/scripts/<tool>.py --help
```

### Testing Changes

```bash
# Validate Python syntax
find . -name "*.py" -type f -exec python3 -m py_compile {} \;

# Test Python tools
for tool in $(find . -name "*.py" -path "*/scripts/*"); do
    echo "Testing: $tool"
    python "$tool" --help || echo "FAILED: $tool"
done

# Validate markdown files
find . -name "*.md" -type f -exec echo "Checking: {}" \;

# Check for secrets (pre-commit check)
git diff --cached | grep -iE '(api[_-]?key|secret|password|token).*=.*[^x{5}]' && echo "⚠️  Potential secret detected"

# Validate relative paths in agents
find agents -name "cs-*.md" -exec grep -l "../../" {} \; | while read file; do
    echo "Validating paths in: $file"
    grep -o "\.\./\.\./[a-z-]*/[a-z-]*/" "$file" | sort -u
done
```

### Slash Commands

Available slash commands (from `.claude/commands/`):

```bash
# Git and commit workflows
/git:cm     # Stage changes and create conventional commit (no push)
/git:cp     # Stage, commit, and push following git governance
/git:pr     # Create pull request from current branch

# Quality gates
/review           # Run local review gate before pushing
/security-scan    # Run security scan gate
```

**Usage Example:**
```bash
# Make changes
vim skills/marketing-team/content-creator/SKILL.md

# Review changes
/review

# Commit with conventional format
/git:cm

# Create pull request
/git:pr develop
```

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
# Issue: Module not found
# Solution: Activate virtual environment
source claude-skills_venv/bin/activate
pip install -r requirements.txt

# Issue: Permission denied
# Solution: Make script executable
chmod +x <domain-skill>/<skill-name>/scripts/<tool>.py

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
pip install -r requirements.txt

# Issue: Wrong Python version in venv
# Solution: Specify Python version
python3.9 -m venv claude-skills_venv
# or
python3.11 -m venv claude-skills_venv
```

## Additional Resources

- **.gitignore:** Excludes .vscode/, .DS_Store, AGENTS.md, PROMPTS.md, .env*, *_venv/
- **Standards Library:** [docs/standards/](docs/standards/) - Communication, quality, git, documentation, security
- **Implementation Plans:** [docs/implementation/](docs/implementation/)
- **Sprint Delivery:** [docs/delivery/](docs/delivery/)
- **Workflow Guide:** [docs/WORKFLOW.md](docs/WORKFLOW.md)
- **Git Standards:** [docs/standards/git/git-workflow-standards.md](docs/standards/git/git-workflow-standards.md)

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
├── docs/                          # Implementation docs
│   ├── WORKFLOW.md                # Git workflow guide
│   ├── implementation/            # Implementation plans
│   ├── delivery/                  # Sprint tracking
│   └── standards/                 # Quality standards
│       ├── communication/
│       ├── quality/
│       ├── git/
│       ├── documentation/
│       └── security/
├── templates/                     # Templates
│   ├── agent-template.md          # Agent creation template
│   └── skill-template.md          # Skill creation template
├── requirements.txt               # Python dependencies
└── CLAUDE.md                      # This file
```

---

**Last Updated:** November 12, 2025
**Current Focus:** Clean Break restructuring for Pandora-specific deployment
**Status:** 26 Pandora-focused skills across 4 domains, 3 production agents
**Python Version:** 3.8+ required
**Dependencies:** pyyaml>=6.0.3 (see requirements.txt)
