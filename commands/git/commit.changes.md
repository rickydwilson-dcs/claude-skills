---
name: commit.changes
title: Commit and Promote Through Workflow
description: Always commit and push to develop branch first, then optionally promote through staging to main - enforces proper git workflow
category: git
subcategory: workflow
pattern: multi-phase
difficulty: intermediate
time-saved: "10 minutes per commit cycle"
frequency: "Daily per developer"
version: 1.0.0
author: Claude Skills Team
contributors:
  - Git Workflow Team
created: 2025-11-25
updated: 2025-11-28
example_usage: "/commit.changes"
requires_input: false
requires_context: true
estimated_time: "2-5 minutes"
model_preference: opus
tools_required: [Bash, Read, Grep]
output_format: text
interactive: true
dangerous: true
tags:
  - git
  - commit
  - workflow
  - develop
  - staging
  - main
  - promotion
  - branch-strategy
related-commands:
  - /write.commit-message
  - /cleanup.branches
  - /create.pr
related-agents:
  - cs-git-workflow-master
related-skills:
  - engineering-team/code-reviewer
dependencies:
  tools:
    - Bash
    - Read
    - Grep
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
  - title: "Basic Commit to Develop"
    input: "/commit.changes"
    output: "Staged 5 files, created commit 'feat(commands): add commit workflow command', pushed to develop"
  - title: "Commit and Promote to Staging"
    input: "/commit.changes --promote staging"
    output: "Committed to develop, merged to staging, all checks passed"
  - title: "Full Promotion to Main"
    input: "/commit.changes --promote main"
    output: "Committed to develop → staging → main, all validation passed"
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

This command **enforces the proper git workflow** by always committing and pushing to the **develop branch first**, then optionally promoting through staging to main.

**Key Principle:** All changes MUST go through develop first. Never commit directly to staging or main.

**Workflow:** `develop` → `staging` → `main`

**When to use:** After making changes that you want to commit to the repository following the standard workflow.

**What it saves:** Eliminates manual branch switching, merging, and validation - saves 10 minutes per commit cycle.

**⚠️ Important:** This command modifies git state and pushes to remote branches. Changes are ALWAYS pushed to develop first, regardless of promotion level.

---

## Usage

```bash
# Commit and push to develop branch (REQUIRED first step)
/commit.changes

# Commit to develop THEN promote to staging
/commit.changes --promote staging

# Full workflow: commit to develop → merge to staging → merge to main
/commit.changes --promote main

# Dry run - preview what would happen
/commit.changes --dry-run

# Skip validation checks (use with caution)
/commit.changes --no-validate
```

**Note:** All commands ALWAYS push to develop first. The `--promote` flag adds additional promotion steps AFTER the develop commit.

### Arguments

- `--promote [staging|main]` - Promote changes beyond develop (optional)
- `--dry-run` - Preview actions without executing (optional)
- `--no-validate` - Skip validation checks (dangerous, optional)
- `--message "text"` - Provide commit message directly instead of generating (optional)

---

## Pattern Type: Multi-Phase (Validation → Execution → Verification)

**Complexity:** Medium
**Execution Time:** 2-5 minutes
**Destructive:** Yes (commits and pushes to git branches)

---

## What This Command Does

### Phase 1: Pre-Commit Validation

Before making any commits, the command validates:

1. **Git Status Check**
   - Verify you're in a git repository
   - Check current branch (should be on develop or feature branch)
   - Identify staged and unstaged changes
   - Warn if working directory is dirty

2. **Branch State Validation**
   - Verify develop branch exists and is up to date
   - Check if staging and main branches exist
   - Ensure no merge conflicts exist
   - Validate branch protection rules

3. **Change Analysis**
   - Read git diff for staged changes
   - Analyze file types modified
   - Check for common issues (secrets, large files, .DS_Store)
   - Count lines added/removed

4. **Generate Commit Message**
   - Analyze changes to determine type (feat, fix, docs, etc.)
   - Generate conventional commit message
   - Present message for user approval
   - Allow user to edit if needed

### Phase 2: Commit and Push to Develop (ALWAYS REQUIRED)

After validation passes, changes are ALWAYS committed and pushed to develop first:

1. **Stage Changes**
   - Add all relevant files to staging area
   - Exclude ignored files and patterns
   - Confirm files to be committed with user

2. **Create Commit**
   - Commit with conventional commit message
   - Include co-authored-by Claude Code
   - Add commit signature if configured
   - Store commit SHA for tracking

3. **Push to Develop (MANDATORY)**
   - Push commit to origin/develop
   - Verify push succeeded
   - Report commit details (SHA, files changed, insertions/deletions)
   - **This step is NEVER skipped** - all changes must go through develop first

### Phase 3: Optional Promotion to Staging

If `--promote staging` is specified:

1. **Pre-Promotion Validation**
   - Run validation checks (if not skipped)
   - Verify all tests pass
   - Check code quality metrics
   - Ensure no blocking issues

2. **Merge to Staging**
   - Switch to staging branch
   - Pull latest changes
   - Merge develop into staging
   - Resolve any conflicts (abort if conflicts exist)

3. **Push and Verify**
   - Push staging branch to remote
   - Trigger CI/CD pipelines
   - Wait for basic checks to pass
   - Report staging status

### Phase 4: Optional Promotion to Main

If `--promote main` is specified:

1. **Production-Ready Validation**
   - All staging checks must pass
   - Verify no critical issues
   - Check deployment readiness
   - Confirm with user (extra safety)

2. **Merge to Main**
   - Switch to main branch
   - Pull latest changes
   - Merge staging into main (fast-forward if possible)
   - Tag release if appropriate

3. **Deploy and Verify**
   - Push main branch to remote
   - Trigger production deployment (if configured)
   - Verify deployment succeeded
   - Report final status

### Expected Output

You will receive:

- **Commit Details** - SHA, message, files changed, insertions/deletions
- **Branch Status** - Current state of develop, staging, main branches
- **Validation Results** - All checks performed and their outcomes
- **Next Steps** - Recommended actions based on promotion level

**Output Format:** Text with color-coded status indicators (✓, ⚠️, ✗)

---

## Error Handling

### Common Issues

**Issue:** "You are not on develop or feature branch"
**Cause:** Currently on staging or main branch
**Solution:** Switch to develop: `git checkout develop`
**Prevention:** Always work on develop or feature branches

---

**Issue:** "Uncommitted changes detected"
**Cause:** Working directory has unstaged changes
**Solution:** Stage changes: `git add .` or stash: `git stash`
**Prevention:** Stage changes before running command

---

**Issue:** "Branch protection prevents direct push"
**Cause:** Main or staging branch requires PR
**Solution:** Use `/create.pr` command instead
**Prevention:** Check branch protection rules in repository settings

---

**Issue:** "Merge conflict detected during promotion"
**Cause:** Conflicting changes between branches
**Solution:** Manually resolve conflicts, then rerun command
**Prevention:** Keep develop, staging, main synchronized regularly

---

**Issue:** "Validation checks failed"
**Cause:** Tests failing, code quality issues, or security problems
**Solution:** Fix reported issues, commit fixes, then retry
**Prevention:** Run validation locally before committing: `python3 scripts/validate_all_agents.sh`

---

## Success Criteria

This command is successful when:

- [ ] All validation checks pass (unless skipped)
- [ ] Commit created with proper conventional commit message
- [ ] Changes pushed to develop branch
- [ ] If promoted to staging: staging branch updated and verified
- [ ] If promoted to main: main branch updated and deployment initiated
- [ ] No merge conflicts occurred
- [ ] All CI/CD pipelines succeeded
- [ ] Repository state is consistent

### Quality Metrics

**Expected Outcomes:**
- Commit follows conventional commit format: `type(scope): description`
- Branch history is clean (no merge commits unless necessary)
- All automated checks pass
- Changes are traceable through commit history

---

## Git Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  PROPER WORKFLOW: develop → staging → main                  │
│  ALL changes MUST go through develop first!                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────┐
│   DEVELOP   │  ← ALL commits go here FIRST (mandatory)
└──────┬──────┘
       │ /commit.changes (always pushes here)
       ▼
┌─────────────┐
│   STAGING   │  ← Pre-production validation
└──────┬──────┘
       │ --promote staging (merges from develop)
       ▼
┌─────────────┐
│    MAIN     │  ← Production-ready code
└─────────────┘
       │ --promote main (merges from staging)
       ▼
   PRODUCTION

⚠️  NEVER commit directly to staging or main!
```

---

## Integration with Agents & Skills

### Related Commands

This command works well with:

- **[/write.commit-message](./write.commit-message.md)** - Generates conventional commit messages
- **[/create.pr](../workflow/create.pr.md)** - Creates pull request for code review
- **[/cleanup.branches](./cleanup.branches.md)** - Cleans up merged feature branches

### Related Agents

- **cs-git-workflow-master** - Orchestrates complex git workflows and branch strategies

### Related Skills

- **[code-reviewer](../../skills/engineering-team/code-reviewer/)** - Validates code quality before committing

---

## Tips for Best Results

1. **Always Start on Develop**
   - Work on develop or feature branches
   - Never commit directly to staging or main
   - Use feature branches for larger changes

2. **Review Changes Before Committing**
   - Run `git diff` to review your changes
   - Ensure you're not committing debug code or secrets
   - Check that all files are intentionally modified

3. **Use Dry Run First**
   - Test with `--dry-run` to preview actions
   - Verify commit message is appropriate
   - Ensure correct files will be committed

4. **Promote Incrementally**
   - Commit to develop first, verify it works
   - Then promote to staging, run validation
   - Only promote to main after thorough testing

5. **Keep Commits Atomic**
   - One logical change per commit
   - Don't mix unrelated changes
   - Write clear, descriptive commit messages

6. **Validate Before Promoting**
   - Run tests locally before promoting
   - Check that documentation is updated
   - Ensure no breaking changes without migration path

---

## Branch Protection Rules

This repository has the following protections:

- **Main branch:** Requires PR approval, no direct pushes
- **Staging branch:** Requires validation checks to pass
- **Develop branch:** Direct pushes allowed, conventional commits enforced

If you try to push directly to main, the command will recommend using `/create.pr` instead.

---

## Related Commands

- `/write.commit-message` - Generate conventional commit message only
- `/create.pr` - Create pull request after committing
- `/cleanup.branches` - Clean up merged feature branches
- `/update.docs` - Update documentation before committing

---

## References

- [Git Workflow Guide](../../docs/WORKFLOW.md) - Complete branch strategy documentation
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message format
- [Branch Protection](../../docs/GIT_WORKFLOW.md) - Branch rules and requirements

---

**Last Updated:** November 28, 2025
**Version:** 1.0.0
**Maintained By:** Claude Skills Team
**Feedback:** Create an issue in the repository or contact @claude-skills-team
