---
name: write.commit-message
title: Commit Message Assistant
description: Generate conventional commit messages from staged changes following project standards
category: write
subcategory: commits
difficulty: beginner
time-saved: "5 minutes per commit"
frequency: "Multiple daily"
pattern: simple
version: 1.0.0
author: Claude Skills Team
tags: [git, commits, conventional-commits, automation, productivity]
example_usage: /write.commit-message
requires_input: false
requires_context: true
estimated_time: 30s
model_preference: haiku
tools_required: [Bash, Grep, Read]
output_format: text
interactive: true
dangerous: false
related_commands:
  - git.create-branch
  - git.sync-develop
related_agents:
  - cs-git-workflow-master
related_skills:
  - engineering-team/code-reviewer
use-cases:
  - "Generating conventional commit messages from staged git changes"
  - "Ensuring consistent commit message format across team"
  - "Accelerating commit workflow with standardized messages"
  - "Following project's git commit standards automatically"
dependencies:
  tools:
    - Bash
    - Grep
    - Read
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
  - title: "Basic Commit Message Generation"
    input: "/write.commit-message"
    output: "Generated commit message: feat(agents): implement cs-git-workflow-master agent\n\nCopy to clipboard? (y/n)"
  - title: "Review and Edit Message"
    input: "/write.commit-message"
    output: "Generated message displayed, allow user to edit before committing"
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0
created: 2025-11-24
updated: 2025-11-24
verified: true
license: MIT
---

# Commit Message Assistant

## What This Command Does

This command generates conventional commit messages automatically from your staged git changes, saving you 5 minutes per commit while ensuring consistent formatting across your team.

**Pattern Type:** Simple (Context → Task)

**Complexity:** Low
**Execution Time:** ~30 seconds
**Destructive:** No (generates message only, doesn't commit unless approved)

---

## Usage

```bash
# Generate commit message from staged changes
/write.commit-message

# View help
/write.commit-message --help
```

### Arguments

This command takes no required arguments. It automatically analyzes your current staged changes.

### Interactive Options

After generating the message, you'll see:
- Generated commit message
- Breakdown of changes by type
- Option to copy to clipboard
- Option to edit before committing
- Option to reject and try again

### Examples

```bash
# Basic usage - generate and review
/write.commit-message

# The command will output something like:
# ─────────────────────────────────────────────────────
# Generated Commit Message:
# ─────────────────────────────────────────────────────
# feat(agents): implement cs-git-workflow-master agent
#
# Add comprehensive git workflow orchestration agent with
# support for conventional commits, branch management, and
# pull request automation.
# ─────────────────────────────────────────────────────
# Changes Summary:
# • 1 new file (agents/engineering/cs-git-workflow-master.md)
# • Features: 1 | Fixes: 0 | Docs: 0
# ─────────────────────────────────────────────────────
# Copy to clipboard? (y/n)
```

---

## What This Command Does in Detail

### Context Gathering

The command will:

1. **Check Git Status**
   - Verify you're in a git repository
   - Check for staged changes (required)
   - Detect if working tree is clean

2. **Analyze Staged Changes**
   - Parse git diff for staged modifications
   - Categorize changes by type (feat, fix, docs, style, refactor, test, chore)
   - Identify affected domains and components
   - Extract key modification patterns

3. **Examine Project Standards**
   - Check for `.claudemd` or similar config
   - Look for existing conventional commit patterns in recent commits
   - Identify project-specific naming conventions

### Task Execution

Then it will:

1. **Determine Commit Type**
   - Analyze change patterns to classify as feat, fix, docs, etc.
   - Consider file paths and extension types
   - Match against domain structure (agents/, skills/, etc.)

2. **Generate Conventional Message**
   - Format: `type(scope): subject`
   - Include descriptive body if changes are substantial
   - Add footer references if applicable (fixes #123, etc.)

3. **Validate Against Standards**
   - Check message follows conventional commit format
   - Verify scope matches known domains/components
   - Ensure subject line < 50 characters
   - Check body line wrapping (72 characters)

### Expected Output

You will receive:

- **Generated Commit Message** - Full formatted message following conventional commits
- **Changes Summary** - Breakdown of what's being committed (files, types, count)
- **Validation Status** - Confirms message meets project standards
- **Interactive Options** - Copy to clipboard, edit, or regenerate

**Output Location:** Displayed in terminal (no files created)
**Output Format:** Human-readable text with formatting

---

## Conventional Commit Format

This command generates messages following the standard format:

```
type(scope): subject

optional body explaining changes

optional footer (Fixes #123, Closes #456)
```

### Supported Types

- **feat** - New feature or capability
- **fix** - Bug fix or defect resolution
- **docs** - Documentation changes only
- **style** - Code style changes (formatting, semicolons, etc.)
- **refactor** - Code restructuring without feature/fix changes
- **test** - Test additions or modifications
- **chore** - Build, dependencies, or configuration changes
- **ci** - CI/CD pipeline configuration

### Project-Specific Scopes

Based on this repository's structure:

- **agents** - Agent development (cs-* prefix)
- **skills** - Skill package creation/updates
- **tools** - Python CLI tools in scripts/
- **commands** - Slash command development
- **docs** - Documentation updates
- **standards** - Standards and best practices
- **workflow** - Git workflow and CI/CD

### Examples

```
feat(agents): implement cs-content-creator agent
fix(tools): correct calculation in seo_optimizer.py
docs(skills): update README for marketing-team
chore(deps): update Python version requirement
```

---

## Detailed Workflow

### Step 1: Pre-Flight Checks

Before generating a message, the command verifies:

```
✓ Inside a git repository
✓ Staged changes exist (git add required)
✓ Not in middle of merge/rebase/conflict
✓ Working tree state is valid
```

**What to do if checks fail:**
- Not a git repo: Run `git init` in project directory
- No staged changes: Run `git add` to stage changes first
- In merge state: Complete/abort merge with `git merge --abort`

### Step 2: Change Analysis

The command analyzes staged changes by:

1. Running `git diff --cached --stat` to see what's staged
2. Running `git diff --cached` to understand nature of changes
3. Categorizing changes by file type and modification pattern
4. Identifying primary domain/component affected

**Detection Logic:**
- New `agents/*/cs-*.md` file → `feat(agents):`
- Multiple `skills/*/` changes → `feat(skills):`
- Modified `*.py` file → `fix(tools):` or `feat(tools):`
- Updated `.md` files → `docs(scope):`

### Step 3: Message Generation

The command creates a message by:

1. Selecting appropriate commit type based on change patterns
2. Identifying affected scope from file paths
3. Generating subject line (descriptive, < 50 chars)
4. Adding body if changes are substantial (> 50 lines)
5. Including footer references if commits mention issues

**Subject Generation:**
- Uses action verbs: "implement", "fix", "update", "add"
- Describes what/why not how
- Maintains lowercase (except proper nouns)
- Avoids vague phrases like "stuff", "things", "update"

### Step 4: Interactive Review

After generation, you can:

- **Copy to Clipboard** - Ready to use in your commit
- **Edit Message** - Refine the generated message
- **Regenerate** - Try a different approach
- **Reject** - Cancel and try again with new changes

---

## Success Criteria

This command is successful when:

- [x] Correctly identifies commit type from staged changes
- [x] Generates message in conventional commit format
- [x] Subject line follows < 50 character limit
- [x] Scope matches known project domains
- [x] Output is immediately usable in git commit
- [x] Message accurately describes changes staged
- [x] Interactive review allows refinement
- [x] No files are modified or committed without user action

### Quality Metrics

**Expected Outcomes:**
- **Accuracy**: Generated message matches staged changes 95%+
- **Time Saved**: 5 minutes per commit vs manual composition
- **Usability**: Message ready to commit without editing 80%+
- **Consistency**: Messages follow project standards 100%

---

## Tips for Best Results

1. **Stage Changes First**
   - Use `git add` to stage changes before running command
   - Command only analyzes staged changes
   - Use `git add .` for all changes or `git add path/` for specific

2. **Logical Change Grouping**
   - Group related changes in one commit
   - Separate different concerns into different commits
   - Avoid mixing features, fixes, and docs in one commit

3. **Clear Commit History**
   - One logical change per commit
   - Each commit should be independently understandable
   - Easier to bisect and revert when needed

---

## Common Issues

### Issue: "No staged changes found"
**Cause:** Command requires staged changes to analyze
**Solution:** Run `git add` to stage changes first
**Example:**
```bash
git add .
/write.commit-message
```
**Prevention:** Always stage changes before running command

---

### Issue: "Not a git repository"
**Cause:** Command is being run outside a git repo
**Solution:** Initialize or navigate to existing git repository
**Example:**
```bash
cd /path/to/repo  # Navigate to repo
/write.commit-message
```
**Prevention:** Always use this command in git repositories only

---

### Issue: "Merge in progress"
**Cause:** Repository is in the middle of a merge/rebase/conflict
**Solution:** Complete or abort the merge operation first
**Example:**
```bash
git merge --abort      # Abort ongoing merge
/write.commit-message     # Then try again
```
**Prevention:** Resolve conflicts before generating new commits

---

### Issue: "Generated message seems inaccurate"
**Cause:** Changes are complex or span multiple domains
**Solution:** Use interactive edit option to refine message
**Example:**
```bash
/write.commit-message
# Review message
# Select "Edit" option
# Refine message manually
```
**Prevention:** Group related changes, avoid mixing concerns

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-git-workflow-master](../../agents/engineering/cs-git-workflow-master.md)** - Complete git workflow orchestration
- **[cs-code-reviewer](../../agents/engineering/cs-code-reviewer.md)** - Reviews code before committing

### Related Commands

- `/git.create-branch` - Create feature branch with conventional naming
- `/git.sync-develop` - Sync current branch with develop
- `/workflow.create-pr` - Create PR with commit summary

### Related Standards

- **[Conventional Commits](https://www.conventionalcommits.org/)** - Official spec this follows
- **[Git Workflow Standards](../../docs/standards/git-standards.md)** - Project git standards
- **[Commit Message Standards](../../docs/standards/commit-standards.md)** - Message formatting guide

---

## Error Handling Reference

### Validation Errors

If the command reports validation errors:

1. **Invalid Repository State**
   - Check: `git status` shows clean state or valid staging
   - Fix: Resolve any conflicts or aborts first

2. **Insufficient Changes**
   - Check: `git diff --cached` shows staged modifications
   - Fix: Use `git add` to stage changes before running

3. **Unsupported Change Types**
   - Check: Command recognizes your change patterns
   - Fix: Use manual message if pattern not recognized

---

## Advanced Usage

### Custom Scopes

For changes to non-standard components:

```bash
/write.commit-message
# Select "Edit" when prompted
# Change scope to custom value
# Example: fix(custom-component): description
```

### Integration with Git Hooks

This command works well with pre-commit hooks:

```bash
# In your git hooks, you could use:
/write.commit-message --format json  # Get machine-readable output
```

### Batch Processing

For multiple commits in workflow:

```bash
# After each logical set of changes:
git add <related-files>
/write.commit-message
# Review and confirm

# Repeat for next logical group
git add <related-files>
/write.commit-message
```

---

## Environment Requirements

### Minimum Requirements

- Git 2.0+
- Bash/Shell environment
- Claude Code with access to terminal

### Platform Support

- **macOS**: Full support (tested on 10.15+)
- **Linux**: Full support (Ubuntu 18.04+, CentOS 7+)
- **Windows**: Full support (PowerShell or WSL)

---

## Success Stories

**Common Use Cases:**

1. **Accelerating Daily Commits**
   - Team saves ~30 minutes per day on commit messages
   - Improves consistency across all commits

2. **Onboarding New Developers**
   - New team members learn conventional commits quickly
   - Reduced review feedback on commit message format

3. **Maintaining Project History**
   - Clear commit messages help with blame/bisect
   - Future developers understand change history

---

## Related Documentation

- **[Conventional Commits Specification](https://www.conventionalcommits.org/)** - Official format spec
- **[Git Book - Commit Best Practices](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)** - Git fundamentals
- **[Angular Commit Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-guidelines)** - Popular variant
- **[Project Git Standards](../../docs/standards/git-standards.md)** - This project's standards

---

## Validation Checklist

Before using this command, ensure:

- [x] You're in a git repository (`git status` works)
- [x] Changes are staged (`git diff --cached` shows changes)
- [x] Repository is in valid state (no ongoing merge/rebase)
- [x] You have write access to repository
- [x] Terminal/shell is accessible

---

**Last Updated:** November 24, 2025
**Version:** 1.0.0
**Status:** Production Ready
**Maintained By:** Claude Skills Team
**Feedback:** Report issues or suggest improvements via GitHub issues

