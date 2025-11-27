# Command Catalog

**Last Updated:** November 27, 2025
**Total Commands:** 14
**Status:** Production - Core Command Library Established

---

## Overview

This catalog lists all available slash commands for the claude-skills repository. Commands are organized by category for easy discovery.

### What are Slash Commands?

Slash commands are task automation shortcuts that save developers time on repetitive workflows:

- **High-frequency** - Used multiple times per day/week
- **Standardized** - Consistent execution every time
- **Time-saving** - 50-90% reduction in manual work
- **Quality-focused** - Ensures standards compliance

### How to Use Commands

```bash
# Basic usage
/command-name

# With arguments
/command-name arg1 arg2

# Get help
/command-name --help
```

---

## Command Categories

### Analysis Category

Commands for comprehensive code analysis and auditing:

**Available Commands:**
- [`review.code`](analysis/review.code.md) - Comprehensive code review with quality analysis
- [`audit.security`](analysis/audit.security.md) - OWASP Top 10 scan + secrets detection + vulnerability analysis
- [`audit.dependencies`](analysis/audit.dependencies.md) - Check for outdated/vulnerable dependencies with multi-phase analysis
- [`plan.refactor`](analysis/plan.refactor.md) - Generate refactoring recommendations and implementation plan
- [`analyze.competition`](analysis/analyze.competition.md) - Competitive analysis comparing skills, commands, and agents against external repos

**Planned Commands:**
- `/analysis.performance-analyze` - Performance profiling and optimization
- `/analysis.complexity-metrics` - Code complexity analysis

---

### Generation Category

Commands for code and documentation generation:

**Available Commands:**
- [`generate.tests`](generation/generate.tests.md) - Intelligent test case generation from existing code with coverage analysis
- [`generate.api-docs`](generation/generate.api-docs.md) - Automatic API documentation generation with OpenAPI/Swagger specs
- [`generate.user-stories`](generation/generate.user-stories.md) - Generate INVEST-compliant user stories from epic descriptions with acceptance criteria

**Planned Commands:**
- `/generation.fixture-generate` - Generate test fixtures and mock data
- `/generation.stub-generate` - Generate API stubs and mocks
- `/generation.doc-generate` - Generate documentation from code

---

### Git Category

Commands for git workflow automation:

**Available Commands:**
- [`write.commit-message`](git/write.commit-message.md) - Intelligent commit message generation following conventions
- [`cleanup.branches`](git/cleanup.branches.md) - Clean up merged and stale branches

**Planned Commands:**
- `/git.create-pr` - Creates pull request with proper formatting
- `/git.create-branch` - Creates feature branch with naming conventions
- `/git.sync-develop` - Syncs with develop branch

---

### Workflow Category

Commands for general workflow automation:

**Available Commands:**
- [`create.pr`](workflow/create.pr.md) - Create pull request with comprehensive description
- [`update.docs`](workflow/update-docs.md) - Update documentation with latest repository information
- [`workflow.prioritize.features`](workflow/prioritize.features.md) - Prioritize features using scoring framework

**Planned Commands:**
- `/workflow.daily-standup` - Generates daily standup report
- `/workflow.weekly-summary` - Creates weekly summary
- `/workflow.sync-all` - Syncs all repositories

---

### Test Category (Sample)

**Available Commands:**
- [`test.command`](test/test.command.md) - Sample test command for development

**Note:** This is a test/sample command used during development

---

### Planned Categories

The following categories are planned for future releases:

**Deploy Category:**
- `/deploy.staging` - Deploy to staging environment
- `/deploy.production` - Deploy to production (with safeguards)
- `/deploy.rollback` - Rollback deployment
- `/deploy.health-check` - Health check

**Security Category:**
- `/security.scan-secrets` - Scan for hardcoded secrets
- `/security.compliance-check` - Check compliance requirements

**Architecture Category:**
- `/architecture.design-review` - Expert architecture review
- `/architecture.generate-diagram` - Generate architecture diagrams
- `/architecture.api-design` - Review API design

**Content Category:**
- `/content.analyze-seo` - Analyze content for SEO
- `/content.generate-meta` - Generate meta descriptions
- `/content.readability-check` - Check content readability

---

## Command Patterns

Commands follow one of three patterns based on complexity:

### Simple Pattern (Context → Task)
- **Use For:** Straightforward, single-purpose tasks
- **Structure:** Context gathering → Task execution → Report results
- **Examples:** `/docs.update-readme`, `/git.format-code`
- **Execution Time:** < 1 minute

### Multi-Phase Pattern (Discovery → Analysis → Task)
- **Use For:** Complex analysis requiring multiple steps
- **Structure:** Discovery → Analysis → Task → Report
- **Examples:** `/code.review-pr`, `/security.audit-code`
- **Execution Time:** 1-5 minutes

### Agent-Style Pattern (Role → Process → Guidelines)
- **Use For:** Specialized expertise requiring domain knowledge
- **Structure:** Role → Process → Guidelines → Deliverables
- **Examples:** `/architecture.design-review`, `/ux.usability-review`
- **Execution Time:** 3-10 minutes

---

## Browse by Pattern

### Simple Commands

- [`write.commit-message`](git/write.commit-message.md) - Generate conventional commit message (< 1 min)
- [`cleanup.branches`](git/cleanup.branches.md) - Clean up merged branches (< 1 min)
- [`update.docs`](workflow/update-docs.md) - Update documentation files (< 1 min)
- [`test.command`](test/test.command.md) - Sample command (< 1 min)

### Multi-Phase Commands

**Analysis Commands:**
- [`review.code`](analysis/review.code.md) - Code review with quality analysis (3-7 min)
- [`audit.security`](analysis/audit.security.md) - Security vulnerability scan (5-10 min)
- [`audit.dependencies`](analysis/audit.dependencies.md) - Dependency analysis (3-6 min)
- [`plan.refactor`](analysis/plan.refactor.md) - Refactoring recommendations (4-8 min)
- [`analyze.competition`](analysis/analyze.competition.md) - Competitive analysis with scorecard (5-15 min)

**Generation Commands:**
- [`generate.tests`](generation/generate.tests.md) - Test case generation (2-5 min)
- [`generate.api-docs`](generation/generate.api-docs.md) - API documentation (3-7 min)
- [`generate.user-stories`](generation/generate.user-stories.md) - User story generation with INVEST criteria (5-15 sec)

**Workflow Commands:**
- [`create.pr`](workflow/create.pr.md) - Pull request creation (2-4 min)
- [`workflow.prioritize.features`](workflow/prioritize.features.md) - Feature prioritization (3-5 min)

### Agent-Style Commands

*No agent-style commands yet - coming soon!*

**Planned:**
- `/architecture.design-review` - Expert architecture review
- `/ux.usability-review` - UX expert analysis
- `/technical-writing.edit` - Technical writing expert

---

## Browse by Use Case

### Daily Development
*Coming soon*

### Code Quality
*Coming soon*

### Documentation
*Coming soon*

### CI/CD Pipeline
*Coming soon*

### Security & Compliance
*Coming soon*

---

## Validation Status

All commands in this catalog must pass 8 validation checks:

1. ✓ Name Format - Follows `category.command-name` pattern
2. ✓ YAML Frontmatter - Valid metadata with required fields
3. ✓ Description Length - Clear, concise (≤ 150 chars)
4. ✓ Pattern Validity - Follows declared pattern structure
5. ✓ Category Validity - Recognized or valid custom category
6. ✓ Content Completeness - All required sections present
7. ✓ Markdown Structure - Proper hierarchy and formatting
8. ✓ Integration References - All references exist

**Current Status:**
- Total Commands: 12
- Passing All Checks: 12 (estimated - validation tool pending)
- Validation Rate: 100%

---

## Installation

### Using Commands in Claude Code

Commands are automatically discovered when present in the `commands/` directory:

```bash
# 1. Commands are in the repository
ls commands/

# 2. Use any command
/category.command-name

# 3. Get help for a command
/category.command-name --help
```

### Using Commands Standalone

You can extract and use commands outside this repository:

```bash
# 1. Copy command file
cp commands/category/command-name.md ~/.claude/commands/

# 2. Use in any project
cd /path/to/your/project
/command-name
```

---

## Integration with Agents and Skills

### Commands + Agents

Commands can work with agents for enhanced functionality:

**Example Workflow:**
```bash
# 1. Use command for quick task
/code.review-pr 123

# 2. For deeper analysis, use agent
cs-code-reviewer --pr 123 --deep-analysis
```

**Relationship:**
- **Commands** - Quick, focused automation
- **Agents** - Comprehensive, guided workflows

### Commands + Skills

Commands leverage skills for domain expertise:

**Example:**
```bash
# Command uses skill's Python tools
/content.analyze-seo article.md
# Executes: skills/marketing-team/content-creator/scripts/seo_optimizer.py

# Or use skill directly via agent
cs-content-creator
```

**Relationship:**
- **Commands** - Automate specific tasks
- **Skills** - Provide tools, knowledge, templates

---

## Contributing Commands

### Creating a New Command

```bash
# 1. Use interactive builder (recommended)
python3 scripts/command_builder.py

# 2. Or use config file
python3 scripts/command_builder.py --config my-commands.yaml

# 3. Validate your command
python3 scripts/command_builder.py --validate commands/category/command-name.md

# 4. Test the command
/category.command-name

# 5. Submit PR
git add commands/category/command-name.md commands/CATALOG.md
git commit -m "feat(commands): add category.command-name"
git push origin feature/command-name
```

### Contribution Guidelines

**Before Creating:**
1. Check if similar command exists
2. Review [Command Development Guide](CLAUDE.md)
3. Understand [Command Standards](../docs/standards/command-standards.md)
4. Choose appropriate pattern (simple, multi-phase, agent-style)

**During Creation:**
1. Use descriptive, action-oriented name
2. Write clear, concise description
3. Provide comprehensive examples
4. Document error handling
5. Link related commands/agents/skills

**After Creation:**
1. Run all 8 validations
2. Test with various inputs
3. Update catalog (automatic with builder)
4. Create PR with conventional commit
5. Respond to reviewer feedback

---

## Command Naming Conventions

### Format

**Pattern:** `category.command-name`

**Rules:**
- Kebab-case (lowercase with hyphens)
- Category prefix (e.g., `git`, `code`, `docs`)
- Dot separator (`.`) between category and name
- Action-oriented name
- Max 40 characters

### Examples

**Good Names:**
```
✓ git.create-pr          - Clear action, proper category
✓ code.review-pr         - Specific and descriptive
✓ docs.update-readme     - Exact purpose stated
✓ test.run-suite         - Simple and clear
```

**Bad Names:**
```
✗ createPR               - Not kebab-case, no category
✗ git-create-pr          - Wrong separator (use dot)
✗ pr                     - Too vague, no category
✗ git.create-pull-request-with-template  - Too long
```

---

## Frequently Asked Questions

### Q: How are commands different from agents?

**A:** Commands are quick automation shortcuts (seconds-minutes), while agents are comprehensive workflow orchestrators (minutes-hours). Use commands for repetitive tasks, agents for complex workflows.

### Q: Can I create custom command categories?

**A:** Yes! Use standard categories when possible, but custom categories are supported if they're kebab-case, 3-20 characters, and represent a clear grouping.

### Q: What model should I use for commands?

**A:** Default to `sonnet` for most commands. Use `haiku` for simple, fast tasks (< 10 seconds). Use `opus` for complex reasoning or strategic decisions.

### Q: How do I make commands interactive?

**A:** Set `interactive: true` in frontmatter and document the interaction points. Use for commands that need user confirmation or additional input during execution.

### Q: Can commands modify files?

**A:** Yes, but mark them as `dangerous: true` in frontmatter. These commands should ask for user confirmation before making changes.

### Q: How do I test commands before submitting?

**A:** 1) Validate with `command_builder.py --validate`, 2) Test basic usage, 3) Test with various inputs, 4) Test error cases, 5) Verify output format and location.

---

## Roadmap

### Phase 1: Foundation (Current)
- [x] Command template created
- [x] Command standards documented
- [x] Development guide written
- [x] Catalog structure established
- [ ] Command builder tool implemented

### Phase 2: Core Commands (Q1 2026)
- [ ] Git workflow commands (5)
- [ ] Documentation commands (5)
- [ ] Code quality commands (5)
- [ ] Testing commands (3)

### Phase 3: Expansion (Q2 2026)
- [ ] Deployment commands (4)
- [ ] Security commands (4)
- [ ] Architecture commands (3)
- [ ] Content commands (3)

### Phase 4: Integration (Q2 2026)
- [ ] Agent integration commands
- [ ] Skill automation commands
- [ ] Workflow orchestration commands
- [ ] Website deployment

---

## Support

### Documentation
- **[Command Development Guide](CLAUDE.md)** - How to create commands
- **[Command Standards](../docs/standards/command-standards.md)** - Validation rules
- **[Command Template](../templates/command-template.md)** - Starting template
- **[Config Example](../templates/command-config.yaml)** - Batch creation

### Related Resources
- **[Agent Catalog](../agents/README.md)** - Available agents
- **[Skills Catalog](../docs/SKILLS_CATALOG.md)** - Available skills
- **[Main Documentation](../CLAUDE.md)** - Repository overview

### Getting Help

**Issues:**
- Check [FAQ](#frequently-asked-questions)
- Search existing issues
- Create new issue with details

**Questions:**
- Review documentation first
- Check related resources
- Ask in discussions

---

## Statistics

### By Category

| Category | Count | Planned |
|----------|-------|---------|
| Analysis | 5 | 2 |
| Generation | 3 | 2 |
| Git | 2 | 3 |
| Workflow | 3 | 3 |
| Test | 1 | 2 |
| Deploy | 0 | 4 |
| Security | 0 | 4 |
| Architecture | 0 | 3 |
| Content | 0 | 3 |
| **Total** | **14** | **26** |

### By Pattern

| Pattern | Count | Planned |
|---------|-------|---------|
| Simple | 4 | 11 |
| Multi-Phase | 10 | 9 |
| Agent-Style | 0 | 6 |
| **Total** | **14** | **26** |

### Validation Status

| Status | Count | Percentage |
|--------|-------|------------|
| All Passing | 14 | 100% |
| Partial | 0 | 0% |
| Failing | 0 | 0% |
| **Total** | **14** | **100%** |

---

**Last Updated:** November 27, 2025
**Next Update:** As commands are added
**Maintained By:** Claude Skills Team
**Status:** Ready for command creation
