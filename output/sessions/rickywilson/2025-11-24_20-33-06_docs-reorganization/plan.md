# Docs Directory Reorganization Plan

## Problem Statement

Current `docs/` structure is inconsistent:
- Mix of different content types (guides, standards, catalogs, implementation)
- Inconsistent naming (UPPERCASE vs lowercase)
- Implementation docs don't belong in docs/ (should be in output/)
- agent-development/ is special but guides/ and testing/ aren't consistent
- No clear hierarchy or navigation

## Proposed Structure

```
docs/
├── README.md                          # Navigation hub for all documentation
│
├── guides/                            # User-facing guides (how to use)
│   ├── installation.md                # How to install and set up
│   ├── quick-start.md                 # Get started in 5 minutes
│   ├── using-agents.md                # How to use agents
│   ├── using-skills.md                # How to use skills
│   ├── using-commands.md              # How to use slash commands
│   ├── understanding-skills.md        # Concept explanation
│   └── workflow.md                    # Git workflow and best practices
│
├── development/                       # Developer guides (how to create)
│   ├── agents/                        # Agent development
│   │   ├── README.md                  # Agent development overview
│   │   ├── quick-start.md             # Quick start for agents
│   │   ├── guide.md                   # Complete development guide
│   │   └── completeness-checklist.md  # Quality checklist
│   ├── skills/                        # Skill development
│   │   ├── README.md                  # Skill development overview
│   │   ├── quick-start.md             # Quick start for skills
│   │   └── guide.md                   # Complete development guide
│   ├── commands/                      # Command development
│   │   ├── README.md                  # Command development overview
│   │   ├── installation.md            # How to install commands
│   │   └── creation.md                # How to create commands
│   └── testing/                       # Testing guides
│       ├── README.md                  # Testing overview
│       ├── quick-start.md             # Quick testing guide
│       └── guide.md                   # Complete testing guide
│
├── catalogs/                          # Reference catalogs
│   ├── agents.md                      # All agents catalog
│   ├── skills.md                      # All skills catalog
│   ├── commands.md                    # All commands catalog
│   └── tools.md                       # Python tools catalog
│
├── standards/                         # Standards and conventions
│   ├── README.md                      # Standards overview
│   ├── documentation.md               # Documentation standards
│   ├── communication.md               # Communication standards
│   ├── quality.md                     # Quality standards
│   ├── security.md                    # Security standards
│   ├── git-workflow.md                # Git workflow standards
│   ├── cli.md                         # CLI tool standards
│   ├── builders.md                    # Builder tool standards
│   ├── commands.md                    # Command standards
│   └── anthropic-validation.md        # Anthropic validation standards
│
├── architecture/                      # Architecture documentation
│   ├── overview.md                    # System architecture
│   ├── agents.md                      # Agent architecture
│   ├── skills.md                      # Skill architecture
│   ├── commands.md                    # Command architecture
│   └── session-outputs.md             # Output system architecture
│
└── reference/                         # Reference documentation
    ├── roadmap/                       # Project roadmap
    │   ├── commands-roadmap.md        # Commands roadmap
    │   └── commands-decisions.md      # Decision log
    └── examples/                      # Usage examples
        └── README.md                  # Examples index
```

## Migration Plan

### Move Implementation Docs to Output

```bash
# Implementation summaries don't belong in docs/
mv docs/implementation/commands-implementation.md output/2025-11-24_commands/implementation-summary.md
mv docs/implementation/commands-documentation-summary.md output/2025-11-24_commands/documentation-summary.md
mv docs/implementation/qa-validation-report.md output/2025-11-24_commands/qa-validation-report.md
rmdir docs/implementation/
```

### Reorganize User Guides

```bash
mkdir -p docs/guides

# Move/rename user guides
mv docs/INSTALL.md docs/guides/installation.md
mv docs/QUICK_START.md docs/guides/quick-start.md
mv docs/USAGE.md docs/guides/usage.md
mv docs/WORKFLOW.md docs/guides/workflow.md
mv docs/guides/using-skills.md docs/guides/using-skills.md
mv docs/guides/understanding-skills.md docs/guides/understanding-skills.md

# Keep skill-to-agent-flow as reference
mv docs/guides/skill-to-agent-flow.md docs/reference/skill-to-agent-flow.md
```

### Reorganize Development Guides

```bash
mkdir -p docs/development/{agents,skills,commands,testing}

# Agent development
mv docs/agent-development/README.md docs/development/agents/README.md
mv docs/agent-development/AGENT_QUICK_START.md docs/development/agents/quick-start.md
mv docs/agent-development/AGENT_DEVELOPMENT_GUIDE.md docs/development/agents/guide.md
mv docs/agent-development/COMPLETENESS_CHECKLIST.md docs/development/agents/completeness-checklist.md
rmdir docs/agent-development/

# Command development
mkdir -p docs/development/commands
mv docs/COMMANDS_INSTALLATION.md docs/development/commands/installation.md
mv docs/COMMANDS_CREATION.md docs/development/commands/creation.md

# Testing
mv docs/testing/TESTING_QUICK_START.md docs/development/testing/quick-start.md
mv docs/testing/TESTING_GUIDE.md docs/development/testing/guide.md
```

### Reorganize Catalogs

```bash
mkdir -p docs/catalogs

mv docs/AGENTS_CATALOG.md docs/catalogs/agents.md
mv docs/SKILLS_CATALOG.md docs/catalogs/skills.md
# Commands catalog stays in commands/CATALOG.md (it's part of the command system)
```

### Reorganize Standards

```bash
# Standards already in good location, just rename for consistency
cd docs/standards/
mv documentation-standards.md documentation.md
mv communication-standards.md communication.md
mv quality-standards.md quality.md
mv security-standards.md security.md
mv git-workflow-standards.md git-workflow.md
mv cli-standards.md cli.md
mv builder-standards.md builders.md
mv command-standards.md commands.md
mv anthropic-skill-validation.md anthropic-validation.md
```

### Create Architecture Docs

```bash
mkdir -p docs/architecture

# Create new architecture overview (extract from CLAUDE.md)
# Move session outputs doc
mv docs/workflows/session-based-outputs.md docs/architecture/session-outputs.md
rmdir docs/workflows/
```

### Create Reference Section

```bash
mkdir -p docs/reference/{roadmap,examples}

mv docs/roadmap/slash-commands-roadmap.md docs/reference/roadmap/commands-roadmap.md
mv docs/roadmap/slash-commands-decisions.md docs/reference/roadmap/commands-decisions.md
rmdir docs/roadmap/

mv docs/examples/README.md docs/reference/examples/README.md
```

## Naming Convention

### Directories
- **All lowercase** - `guides/`, `development/`, `catalogs/`, `standards/`
- **Hyphen-separated** for multi-word - `git-workflow.md`
- **Plural for collections** - `guides/`, `catalogs/`, `standards/`

### Files
- **All lowercase** - `installation.md`, `quick-start.md`
- **Hyphen-separated** - `quick-start.md`, `git-workflow.md`
- **No UPPERCASE** except for special root files (README.md, CLAUDE.md)
- **Descriptive names** - `using-agents.md` not `agents.md` in guides/

### Special Cases
- **README.md** - Always UPPERCASE, navigation/overview for directory
- **CLAUDE.md** - Root-level context file (UPPERCASE, special case)

## Benefits

### Clear Hierarchy
- **guides/** - "How do I use X?"
- **development/** - "How do I create X?"
- **catalogs/** - "What's available?"
- **standards/** - "What are the rules?"
- **architecture/** - "How does it work?"
- **reference/** - "Background information"

### Consistent Navigation
- Every major directory has README.md
- Clear parent-child relationships
- Easy to find what you need

### Proper Separation
- Implementation docs → output/
- User docs → docs/guides/
- Developer docs → docs/development/
- Reference → docs/catalogs/ and docs/reference/

### Scalable
- Easy to add new guides
- Easy to add new development docs
- Easy to add new standards
- Doesn't clutter as it grows

## Updated Documentation Standards

The key principles:

1. **Implementation Progress** → `output/{session}/` (git-tracked, session-specific)
2. **User Guides** → `docs/guides/` (how to use)
3. **Developer Guides** → `docs/development/` (how to create)
4. **Reference Material** → `docs/catalogs/`, `docs/reference/`
5. **Standards** → `docs/standards/`
6. **Architecture** → `docs/architecture/`

## Migration Checklist

- [ ] Create new directory structure
- [ ] Move implementation docs to output/
- [ ] Move and rename user guides
- [ ] Reorganize development docs
- [ ] Move catalogs
- [ ] Rename standards (remove -standards suffix)
- [ ] Create architecture section
- [ ] Create reference section
- [ ] Create README.md for each major directory
- [ ] Update all internal links
- [ ] Update CLAUDE.md navigation map
- [ ] Update documentation-standards.md
- [ ] Test all links
- [ ] Commit changes

## Next Steps

1. Review this plan
2. Execute migration (scripted for safety)
3. Update all cross-references
4. Create directory README files
5. Update main CLAUDE.md
6. Test navigation
7. Commit

---

**Status:** Planning
**Priority:** High (blocks clear documentation)
**Effort:** 1-2 hours (mostly automated)
