---
name: create.pr
title: Create Pull Request with Auto-Generated Description
description: Creates a pull request with automatically generated description from commit history and diff analysis
category: create
subcategory: pull-requests
pattern: simple
difficulty: beginner
time-saved: "10 minutes per PR"
frequency: "Weekly per developer"
use-cases:
  - "Creating PR with formatted description auto-generated from commit messages"
  - "Generating professional PR body with summary, changes breakdown, and test plan"
  - "Standardizing PR format across team contributions with consistent structure"
  - "Creating draft PRs for early feedback before marking ready for review"
version: v1.0.0
author: Claude Skills Team
contributors:
  - Engineering Team
created: 2025-11-24
updated: 2025-11-24
example_usage: "/pr-create"
requires_input: false
requires_context: true
estimated_time: "1-2 minutes"
model_preference: sonnet
tools_required: [Bash, Read, Write, Grep]
output_format: markdown
interactive: false
dangerous: false
tags:
  - pull-requests
  - git-workflow
  - automation
  - github
  - productivity
  - development
  - feature-branch
  - conventional-commits
related-commands:
  - /workflow.create-branch
  - /code.review-pr
  - /workflow.sync-develop
related-agents:
  - cs-pull-request-manager
related-skills:
  - engineering-team/code-reviewer
dependencies:
  tools:
    - Bash
    - Read
    - Write
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
  - title: "Basic PR Creation"
    input: "/pr-create"
    output: "Created PR #42: feat(agents): implement cs-content-creator\nhttps://github.com/repo/pull/42"
  - title: "PR with Custom Title"
    input: "/pr-create --title 'Add dark mode support'"
    output: "Created PR #43: Add dark mode support\nhttps://github.com/repo/pull/43"
  - title: "PR with Specific Base Branch"
    input: "/pr-create --base main"
    output: "Created PR #44: Target branch set to main\nhttps://github.com/repo/pull/44"
  - title: "Draft PR"
    input: "/pr-create --draft"
    output: "Created draft PR #45: Ready for review when marked ready\nhttps://github.com/repo/pull/45"
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0
featured: false
verified: true
license: MIT
---

# Create Pull Request with Auto-Generated Description

This command automates pull request creation by gathering commit history, analyzing diffs, and generating a well-formatted PR description. Perfect for developers who want to maintain consistent, professional PR standards across their team.

**When to use:** After completing work on a feature branch and ready to merge back to develop/main.

**What it saves:** Eliminates manual PR description writing - saves 10 minutes per PR while ensuring consistent formatting and completeness.

---

## What This Command Does

### Context Gathering

The command starts by analyzing your feature branch:

1. **Branch Analysis**
   - Get current branch name
   - Determine target base branch (defaults to `develop`)
   - Verify branch has commits ahead of base
   - List all commits between branches

2. **Commit History**
   - Parse commit messages using conventional commit format
   - Extract type (feat, fix, docs, refactor, test, etc.)
   - Count commits by type
   - Identify scope/domain from messages

3. **Diff Analysis**
   - Get file diff statistics
   - Categorize changes by file type
   - Detect modified skills/agents/scripts
   - Identify test file changes

### Task Execution

The command generates a professional PR with:

1. **PR Title** - Extracted from first commit message
2. **Summary** - Synthesized from all commit messages
3. **Changes** - Organized by file type and domain
4. **Test Plan** - Recommendations based on changes
5. **Related Items** - Links to skills/agents if modified
6. **Labels** - Automatically applied based on commit types

### Expected Output

- Created pull request with GitHub URL
- Formatted markdown description
- Applicable labels (feat, fix, docs, etc.)
- PR number and link for verification
- Success confirmation message

## Usage

```bash
# Basic usage - creates PR from current branch to develop
/pr-create

# With custom title
/pr-create --title "Custom PR Title"

# Specify base branch (defaults to develop)
/pr-create --base main

# Create as draft PR
/pr-create --draft

# Add specific labels
/pr-create --labels "enhancement,documentation"

# Set assignees
/pr-create --assignees "user1,user2"

# Dry run - preview without creating
/pr-create --dry-run
```

### Arguments

- `--title` - Custom PR title (optional, defaults to first commit message)
- `--base` - Target branch for PR (optional, defaults to `develop`)
- `--draft` - Create as draft PR, not ready for review (optional)
- `--labels` - Comma-separated labels to apply (optional, auto-applied if not specified)
- `--assignees` - Comma-separated GitHub usernames to assign (optional)
- `--dry-run` - Preview changes without creating PR (optional)
- `--force` - Create PR even if one already exists from this branch (optional)

## Examples

### Example 1: Basic PR Creation
```bash
/pr-create
```
**Result:** Creates PR from feature branch to develop with auto-generated description including commits, changes summary, and test plan.

### Example 2: Draft PR for Early Review
```bash
/pr-create --draft
```
**Result:** Creates draft PR, useful when seeking feedback before marking ready for team review.

### Example 3: Custom Title and Base Branch
```bash
/pr-create --title "Add user authentication" --base main
```
**Result:** Creates PR with custom title targeting main branch instead of develop.

### Example 4: Preview Before Creating
```bash
/pr-create --dry-run
```
**Result:** Shows formatted PR description without creating PR, allowing review before committing.

---

## Pattern Type: Simple (Context → Task)

**Complexity:** Low
**Execution Time:** 1-2 minutes
**Destructive:** Yes (creates PR - requires confirmation)
**Requires Authentication:** Yes (GitHub CLI - `gh`)

---

## Implementation Notes

### Phase 1: Discovery
1. Validate current git repository
2. Get current branch name
3. Determine base branch (develop by default)
4. Verify branch has commits ahead of base
5. List all commits between branches

### Phase 2: Context Analysis
1. Parse commit messages using conventional commit format
2. Extract type (feat, fix, docs, etc.)
3. Count commits by type
4. Identify scope/domain from messages
5. Get file diff statistics
6. Detect modified skills/agents/scripts

### Phase 3: Description Generation
1. Format PR title from first commit
2. Create Summary section from commit history
3. Generate Changes section by file type
4. Build Test Plan from commit types
5. Add Related Skills/Agents if modified
6. Format complete markdown description

### Phase 4: PR Creation
1. Use `gh pr create` to create PR
2. Pass formatted description
3. Apply labels based on commit types
4. Set assignees if provided
5. Mark as draft if requested
6. Return PR URL and number

## Success Criteria

This command is successful when:
- [ ] Current branch has commits ahead of base branch
- [ ] PR is successfully created in GitHub
- [ ] Description is properly formatted markdown
- [ ] All commit messages included in summary
- [ ] Test plan section is actionable
- [ ] Related skills/agents are identified
- [ ] Labels are automatically applied based on commit types
- [ ] PR URL returned to user
- [ ] PR number and link are clickable

## Error Handling

### Common Issues and Solutions

**Issue:** "No commits found between branches"
- **Cause:** Current branch has no unpushed commits or is not ahead of base
- **Solution:** Run `/workflow.sync-develop` first to ensure branch is properly set up
- **Prevention:** Always create feature branches from develop with `git checkout -b`

**Issue:** "Not in a git repository"
- **Cause:** Command run outside a git repository
- **Solution:** Navigate to repository root and try again
- **Prevention:** Check `git status` before running command

**Issue:** "GitHub CLI not authenticated"
- **Cause:** `gh` CLI not authenticated with GitHub
- **Solution:** Run `gh auth login` and follow prompts
- **Prevention:** Ensure GitHub CLI is installed and authenticated

**Issue:** "PR already exists"
- **Cause:** PR already created from this branch
- **Solution:** Use `--force` to recreate or check existing PR with `gh pr view`
- **Prevention:** Delete old PR or use different branch name

**Issue:** "Remote not found"
- **Cause:** Remote repository not configured or not accessible
- **Solution:** Verify remote: `git remote -v`, set if needed: `git remote add origin <url>`
- **Prevention:** Clone repositories with HTTPS/SSH configured

## Advanced Usage

### Customize PR Template

Edit PR body with custom sections:

```bash
/pr-create --template "## Breaking Changes\n\n## Migration Guide\n\n## Review Checklist"
```

### Link Related Issues

Auto-link related GitHub issues:

```bash
/pr-create --closes "123,124" --related "125,126"
```

### Team Workflow

Add reviewers and auto-assign:

```bash
/pr-create --assignees "@frontend-team" --reviewers "@code-reviewers"
```

### CI/CD Integration

Request review from specific teams:

```bash
/pr-create --request-teams "backend,devops"
```
