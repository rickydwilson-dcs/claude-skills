---
name: update.docs
title: Auto-Update Documentation After Code Changes
description: Auto-updates README, CHANGELOG, and documentation after code changes by scanning repository state and syncing statistics
category: update
subcategory: documentation
pattern: simple
difficulty: beginner
time-saved: "15 minutes per use"
frequency: "Weekly per developer"
version: 1.0.0
author: Claude Skills Team
contributors:
  - Documentation Team
  - Workflow Team
created: 2025-11-24
updated: 2025-11-24
example_usage: "/update.docs"
requires_input: false
requires_context: false
estimated_time: "2-3 minutes"
model_preference: sonnet
tools_required: [Read, Write, Glob, Bash]
output_format: markdown
interactive: false
dangerous: false
tags:
  - documentation
  - automation
  - maintenance
related-commands:
  - /workflow.validate-docs
  - /workflow.generate-catalog
related-agents:
  - cs-documentation-manager
  - cs-agile-product-owner
related-skills:
  - engineering-team/code-reviewer
  - product-team/product-manager-toolkit
dependencies:
  tools:
    - Read
    - Write
    - Glob
    - Bash
  scripts: []
  python-packages: []
compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows
examples:
  - title: "Basic Documentation Update"
    input: "/update.docs"
    output: "Updated README.md: 28 agents, 28 skills. Updated CHANGELOG.md with latest commits. All counts synchronized."
  - title: "Verbose Mode with Progress"
    input: "/update.docs --verbose"
    output: "Scanning agents/ directory (found 28 cs-* agents). Scanning skills/ directory (found 28 skill packages). Updated README.md counts. Updated CHANGELOG.md with 5 new entries. Validation passed. All files synchronized."
  - title: "Dry Run Preview"
    input: "/update.docs --dry-run"
    output: "Would update: README.md (agent count: 28, skill count: 28). Would update: CHANGELOG.md (5 new entries). Would add to docs/AGENTS_CATALOG.md and docs/SKILLS_CATALOG.md. Use /update.docs to apply changes."
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0
featured: false
verified: true
license: MIT
---

## Overview

Documentation drift is a common problem in rapidly evolving repositories. This command keeps your README, CHANGELOG, and catalog files automatically synchronized with your actual codebase state by scanning for agents, skills, and recent commits.

**When to use:** After creating new agents, skills, or making significant code changes that should be documented.

**What it saves:** Eliminates manual counting and changelog maintenance - saves 15 minutes per update cycle across a team.

---

## Usage

```bash
/update.docs                              # Basic usage - update all documentation
/update.docs --verbose                    # Verbose mode - show scanning details
/update.docs --dry-run                    # Dry run - preview changes
/update.docs --sections readme changelog  # Update specific sections
/update.docs --force                      # Force update even if current
```

### Arguments

- `--verbose` - Display detailed progress for each scanning phase (optional)
- `--dry-run` - Preview all changes without writing to disk (optional)
- `--sections` - Limit updates to specific documentation files: `readme`, `changelog`, `agents-catalog`, `skills-catalog` (optional, default: all)
- `--force` - Rewrite documentation even if counts haven't changed (optional)

---

## Examples

### Basic Documentation Update

```bash
/update.docs
```

**Output:**
```
Scanning repository...
✓ Found 28 agents in agents/ directory
✓ Found 28 skills in skills/ directory
✓ Found 67 Python tools
✓ Found 5 new commits since last update

Updating documentation...
✓ Updated README.md (agent count: 28, skill count: 28)
✓ Updated CHANGELOG.md (5 new entries)
✓ Updated docs/AGENTS_CATALOG.md
✓ Updated docs/SKILLS_CATALOG.md

All documentation synchronized successfully.
```

### Dry Run Preview

```bash
/update.docs --dry-run
```

**Output:**
```
Scanning repository (dry run)...
✓ Found 28 agents in agents/ directory
✓ Found 28 skills in skills/ directory

Would update:
- README.md (agent count: 28, skill count: 28)
- CHANGELOG.md (5 new entries)
- docs/AGENTS_CATALOG.md
- docs/SKILLS_CATALOG.md

Use /update.docs to apply changes.
```

---

## Pattern Type: Simple (Context → Task)

**Complexity:** Low
**Execution Time:** 2-3 minutes
**Destructive:** No (read-only scanning, safe file writes with validation)

---

## What This Command Does

### Context Gathering

The command starts by scanning your repository structure:

1. **Agent Discovery**
   - Glob `agents/**/*.md` for files matching `cs-*.md` pattern
   - Count agents by domain (marketing, product, engineering, delivery)
   - Capture agent metadata from YAML frontmatter

2. **Skill Discovery**
   - Glob `skills/**` for skill packages
   - Count skills by team (marketing-team, product-team, engineering-team, delivery-team)
   - Identify Python tools and references in each skill

3. **Recent Changes**
   - Read git log for recent commits
   - Parse conventional commit messages (feat, fix, docs, etc.)
   - Group commits by domain and type

4. **Current Documentation**
   - Read README.md to identify current statistics
   - Read CHANGELOG.md to find last documented entry
   - Check docs/AGENTS_CATALOG.md and docs/SKILLS_CATALOG.md

### Task Execution

Based on discovered state, the command:

1. **Update Statistics Sections**
   - Calculate total agents and skills
   - Break down by domain/team
   - Calculate Python tools count
   - Update "Current Scope" and "Status" sections in README.md

2. **Update CHANGELOG.md**
   - Add new commit entries in reverse chronological order
   - Group by conventional commit type (feat, fix, docs, etc.)
   - Link to relevant agents/skills when applicable
   - Preserve existing changelog entries

3. **Regenerate Catalog Files**
   - Update docs/AGENTS_CATALOG.md with complete agent listing
   - Update docs/SKILLS_CATALOG.md with complete skill listing
   - Include validation status for each entry
   - Add metadata (created date, author, version)

4. **Validate All Changes**
   - Verify markdown syntax is valid
   - Check that all counts are reasonable (not impossible numbers)
   - Confirm all referenced agents/skills actually exist
   - Validate YAML frontmatter in catalog entries

### Expected Output

You will receive:

- **Updated README.md** - Current scope, statistics, and status sections
- **Updated CHANGELOG.md** - New entries for recent commits
- **Updated Catalog Files** - Complete agent and skill listings with metadata
- **Summary Report** - What was changed, counts updated, validation results

**Output Location:** Files are updated in place (README.md, CHANGELOG.md, docs/ directory)
**Output Format:** Markdown files, human-readable summary report

---

## Error Handling

### Common Issues

**Issue:** "No agents found in agents/ directory"
**Cause:** Directory structure changed or agents aren't using `cs-*.md` naming
**Solution:** Verify agents exist: `ls agents/**/cs-*.md` - check file naming
**Prevention:** Always use `cs-` prefix for agent filenames

---

**Issue:** "Git log parsing failed"
**Cause:** Unconventional commit messages or git repository issues
**Solution:** Check git status is healthy: `git status && git log --oneline | head -10`
**Prevention:** Use conventional commits: `feat(domain): description`

---

**Issue:** "Markdown validation failed after update"
**Cause:** Malformed YAML frontmatter or syntax errors
**Solution:** Check file with markdown parser, review recent changes
**Prevention:** Validate frontmatter with `command_builder.py --validate`

---

**Issue:** "Permission denied writing to documentation files"
**Cause:** File permissions or git branch restrictions
**Solution:** Check file permissions: `ls -la README.md CHANGELOG.md`
**Prevention:** Ensure you have write access, work on develop branch

---

## Success Criteria

This command is successful when:

- [ ] All agent/skill counts are accurate and match repository state
- [ ] README.md updated with current scope statistics
- [ ] CHANGELOG.md contains entries for recent commits
- [ ] All catalog files regenerated with complete listings
- [ ] All markdown files pass syntax validation
- [ ] No existing content was corrupted
- [ ] All referenced agents/skills actually exist in repository
- [ ] File write operations completed successfully

### Quality Metrics

**Expected Outcomes:**
- Agent count matches: `find agents -name "cs-*.md" | wc -l`
- Skill count matches: `find skills -type d -mindepth 2 -maxdepth 2 | wc -l`
- Changelog entries match: Recent commits in last N days
- No validation errors reported

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-documentation-manager](../../agents/delivery/cs-documentation-manager.md)** - Orchestrates comprehensive documentation updates and maintenance
- **[cs-agile-product-owner](../../agents/product/cs-agile-product-owner.md)** - Uses updated docs for roadmap and backlog management

### Related Skills

This command leverages:

- **[code-reviewer](../../skills/engineering-team/code-reviewer/)** - Validates markdown syntax and documentation quality
- **[product-manager-toolkit](../../skills/product-team/product-manager-toolkit/)** - Helps organize statistics and metrics

### Python Tools

This command may execute:

```bash
python skills/engineering-team/code-reviewer/scripts/validate_markdown.py README.md
python skills/engineering-team/code-reviewer/scripts/validate_markdown.py CHANGELOG.md
```

---

## Tips for Best Results

1. **Run After Major Changes**
   - Create new agents or skills? Run `/update.docs` immediately
   - Ensures documentation stays current and accurate

2. **Use Verbose Mode for Learning**
   - First time? Run `/update.docs --verbose`
   - Understand what the command is discovering and updating
   - Good for debugging if something seems wrong

3. **Dry Run Before Committing**
   - Use `--dry-run` to preview changes
   - Review the output before files are modified
   - Ensures you're comfortable with the updates

4. **Commit Documentation Separately**
   - After `/update.docs` completes, commit documentation changes
   - Use commit message: `docs(repo): update README, CHANGELOG, and catalogs`
   - Keeps documentation commits separate from code changes

5. **Keep Conventional Commits**
   - Command parses `feat()`, `fix()`, `docs()`, etc.
   - Use proper formatting for meaningful changelogs
   - Better changelog = better communication with team

---

## Related Commands

- `/workflow.validate-docs` - Validates all documentation without updating
- `/workflow.generate-catalog` - Generates catalog files in isolation
- `/git.create-pr` - Creates PR after running this command to commit docs

---

## References

- [CHANGELOG.md Format](../../CHANGELOG.md) - See current changelog structure
- [README.md](../../README.md) - See what statistics are updated
- [Git Workflow Guide](../../docs/WORKFLOW.md) - Conventional commit standards
- [Command Development Guide](../CLAUDE.md) - Understanding slash commands

---

**Last Updated:** November 24, 2025
**Version:** 1.0.0
**Maintained By:** Claude Skills Team
**Feedback:** Create an issue in the repository or contact @claude-skills-team
