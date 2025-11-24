---
name: cleanup.branches
title: Branch Cleanup
description: Remove stale local and remote git branches that have been merged or deleted upstream
category: cleanup
subcategory: maintenance
difficulty: beginner
time-saved: "10 minutes per cleanup"
frequency: "Monthly"
pattern: simple
version: 1.0.0
author: Claude Skills Team
tags: [git, branches, maintenance, cleanup, housekeeping, remote, automation]
example_usage: /cleanup.branches
requires_input: false
requires_context: true
estimated_time: 2m
model_preference: haiku
tools_required: [Bash, Read]
output_format: text
interactive: true
dangerous: true
related_commands:
  - git.commit-assist
  - git.create-branch
related_agents:
  - cs-git-workflow-master
related_skills:
  - engineering-team/code-reviewer
use-cases:
  - "Removing stale branches after pull request merges"
  - "Cleaning up local branches that were deleted on remote"
  - "Maintaining a clean branch list across team"
  - "Automating monthly repository hygiene"
dependencies:
  tools:
    - Bash
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
  - title: "Basic Branch Cleanup"
    input: "/cleanup.branches"
    output: "Found 5 stale local branches\nFound 3 deleted remote branches\nProceed with cleanup? (y/n)"
  - title: "Cleanup with Dry Run"
    input: "/cleanup.branches --dry-run"
    output: "Branches that would be deleted:\nlocal: feature/old-feature\nremote: origin/archived-branch\n... (showing what would happen)"
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

# Branch Cleanup

## What This Command Does

This command removes stale local and remote git branches that have been merged or deleted upstream, saving 10 minutes per cleanup while maintaining a clean, organized branch structure.

**Pattern Type:** Simple (Context → Task)

**Complexity:** Low
**Execution Time:** ~2 minutes
**Destructive:** Yes (deletes branches; confirms before executing)

---

## Usage

```bash
# Run interactive cleanup
/cleanup.branches

# Dry run - show what would be deleted without making changes
/cleanup.branches --dry-run

# Only cleanup local branches
/cleanup.branches --local-only

# Only cleanup remote branches
/cleanup.branches --remote-only

# Force deletion without confirmation
/cleanup.branches --force

# View help
/cleanup.branches --help
```

### Arguments

This command takes no required arguments. It automatically analyzes your git repository for stale branches.

### Options

- `--dry-run` - Show which branches would be deleted without deleting (optional, default: false)
- `--local-only` - Only cleanup local branches (optional, default: false)
- `--remote-only` - Only cleanup remote branches (optional, default: false)
- `--force` - Skip confirmation prompts (optional, default: false)
- `--help` - Display help information (optional)

### Interactive Prompts

After analysis, you'll see:
- List of stale branches found (local and remote)
- Count of branches that will be deleted
- Confirmation prompt before deletion
- Summary of deletions performed
- Recommendations for next steps

### Examples

```bash
# Basic usage - analyze and confirm before cleanup
/cleanup.branches

# Output example:
# ─────────────────────────────────────────────────────
# Branch Cleanup Analysis
# ─────────────────────────────────────────────────────
# Local Branches (5 stale found):
# • feature/old-feature (merged 45 days ago)
# • bugfix/fixed-issue-123 (merged 30 days ago)
# • experimental/new-approach (deleted on remote)
# • wip/incomplete-work (stale, no activity)
# • archive/legacy-code (merged 60 days ago)
#
# Remote Branches (3 deleted upstream):
# • origin/feature/archived-task
# • origin/hotfix/resolved-incident
# • origin/docs/outdated-guide
#
# Ready to delete 8 branches total?
# This action cannot be undone. Continue? (y/n)

# Dry run first to see what would happen
/cleanup.branches --dry-run

# Output example:
# ─────────────────────────────────────────────────────
# DRY RUN - No branches will be deleted
# ─────────────────────────────────────────────────────
# Would delete local branch: feature/old-feature
# Would delete local branch: bugfix/fixed-issue-123
# Would delete remote tracking: origin/archived-task
# ...
# Total: 8 branches would be deleted
```

---

## What This Command Does in Detail

### Context Gathering

The command will:

1. **Check Repository Status**
   - Verify you're in a git repository
   - Confirm current branch and working directory is clean
   - Fetch latest remote tracking information

2. **Analyze Local Branches**
   - List all local branches
   - Identify merged branches (already integrated)
   - Detect branches deleted on remote but still local
   - Find stale branches with no recent activity
   - Calculate days since last commit per branch

3. **Analyze Remote Branches**
   - List remote-tracking branches (origin/*, etc.)
   - Identify deleted remote branches (local copies exist)
   - Check if remote branch still exists on server
   - Calculate branch age and merge status

### Task Execution

Then it will:

1. **Determine Cleanup Candidates**
   - Branches fully merged into main/master
   - Branches fully merged into develop
   - Remote-tracking branches where remote was deleted
   - Branches with no commits in 60+ days (optional)

2. **Present Findings**
   - Display list of local branches to delete
   - Display list of remote-tracking branches to clean up
   - Show merge status and age for each
   - Ask for confirmation before proceeding

3. **Execute Cleanup**
   - Delete confirmed local branches with `git branch -d`
   - Prune remote-tracking branches with `git remote prune`
   - Handle any conflicts or locked refs gracefully
   - Provide summary of deletions

### Expected Output

You will receive:

- **Branch Analysis** - List of stale branches with metadata (merge status, age)
- **Deletion Summary** - Count of branches deleted (local and remote)
- **Success Confirmation** - Confirmation that cleanup completed successfully
- **Recommendations** - Suggestions for next cleanup or maintenance tasks

**Output Location:** Displayed in terminal (no files created)
**Output Format:** Human-readable text with formatting and confirmation prompts

---

## Branch Stale Criteria

This command identifies branches as "stale" when they meet these conditions:

### Merged Local Branches

Branches where all commits have been integrated into main/master:

```bash
# Detected via:
git branch --merged main

# Safe to delete - all work is preserved in main
```

### Deleted Remote Branches

Local branches that track remotes that no longer exist:

```bash
# Example: origin/old-feature still exists locally
# but was deleted on the remote server
# git remote prune origin cleans these up
```

### Inactive Branches

Branches with no commits in the last 60 days:

```bash
# Detected via: comparing commit dates
# Criteria: Last commit > 60 days ago
# Reason: Likely abandoned or completed work
```

### Orphaned Remote Branches

Remote-tracking branches where the actual branch was deleted:

```bash
# Example: origin/archived-branch deleted but
# .git/refs/remotes/origin/archived-branch still exists
```

---

## Detailed Workflow

### Step 1: Pre-Flight Checks

Before analyzing branches, the command verifies:

```
✓ Inside a git repository
✓ Working directory is clean (no uncommitted changes)
✓ Not in middle of merge/rebase/conflict
✓ Current branch is valid and accessible
✓ Remote connectivity (if checking remote branches)
```

**What to do if checks fail:**
- Not a git repo: Run `git init` in project directory
- Uncommitted changes: Commit or stash changes with `git stash`
- In merge state: Complete/abort merge with `git merge --abort`
- Remote unreachable: Check internet connection or VPN

### Step 2: Fetch Remote Updates

The command fetches latest remote information:

```bash
# Updates remote-tracking branches
git fetch --prune --all

# Shows current state of all remotes
# Removes stale remote-tracking references
```

**Why this step:**
- Ensures accurate remote branch status
- Removes dangling references automatically
- Shows which remote branches still exist

### Step 3: Analyze Local Branches

The command checks each local branch:

```bash
# Get all local branches
git branch -a

# For each branch, check:
1. Is it fully merged into main/master?
   → git branch --merged main

2. When was the last commit?
   → git log -1 --format='%ci' branch-name

3. Does the remote tracking branch exist?
   → git rev-parse origin/branch-name
```

**Information gathered:**
- Branch name and merge status
- Last commit date and author
- Commits ahead/behind main
- Remote tracking status

### Step 4: Analyze Remote Branches

The command checks remote-tracking branches:

```bash
# List all remote branches
git branch -r

# For each, check:
1. Does remote branch still exist on server?
2. Is it merged into remote main?
3. When was it last updated?
```

**Information gathered:**
- Remote branch names
- Merge status on remote
- Age of remote branch
- Active vs. abandoned status

### Step 5: Present Findings

The command displays branches categorized by type:

```
LOCAL BRANCHES (6 found):
├─ Merged into main
│  ├─ feature/completed-work (45 days ago)
│  └─ bugfix/fixed-issue (30 days ago)
├─ Merged into develop
│  └─ feature/integrated-feature (20 days ago)
├─ No remote tracking
│  └─ experimental/local-only (60+ days)
└─ Deleted on remote
   └─ backup/old-branch (exists locally only)

REMOTE BRANCHES (3 found):
├─ Deleted on server
│  ├─ origin/archived-task
│  └─ origin/old-docs
└─ Active on remote
   └─ origin/main-branch (recent activity)
```

### Step 6: Confirm Before Deletion

Command asks for explicit confirmation:

```
IMPORTANT: This action cannot be undone!
Review the branches listed above carefully.

Delete 6 local branches? (y/n)
Delete 3 remote-tracking branches? (y/n)
```

**Why we confirm:**
- Deletion is permanent
- Prevents accidental data loss
- Allows user to cancel before execution
- Forces deliberate action

### Step 7: Execute Cleanup

If confirmed, the command performs:

```bash
# Delete merged local branches
git branch -d feature/completed-work
git branch -d bugfix/fixed-issue

# Prune deleted remote branches
git remote prune origin

# Clean up garbage references
git gc --prune=now
```

**Deletion strategy:**
- Uses `-d` flag (safe: only deletes merged branches)
- Falls back to `-D` only for branches marked for force deletion
- Prunes remote tracking after deletions
- Handles errors gracefully

### Step 8: Report Results

Command provides summary:

```
─────────────────────────────────────────────────────
Branch Cleanup Complete!
─────────────────────────────────────────────────────
✓ Deleted 6 local branches
✓ Cleaned 3 remote-tracking branches
✓ Recovered ~2.5 MB of local storage
─────────────────────────────────────────────────────

Branches remaining: 8 (main, develop, + 6 active)
Next cleanup recommended: 30 days (Jan 24, 2026)

Pro tip: Run 'git branch -vv' to see branch status
```

---

## Success Criteria

This command is successful when:

- [x] Correctly identifies stale local branches
- [x] Correctly identifies deleted remote branches
- [x] Displays clear list of branches for deletion
- [x] Requests explicit user confirmation before deletion
- [x] Successfully deletes all confirmed branches
- [x] Cleans up remote-tracking references
- [x] Provides accurate summary of deletions
- [x] Handles errors gracefully without data loss

### Quality Metrics

**Expected Outcomes:**
- **Accuracy**: Identifies stale branches 95%+ correctly
- **Time Saved**: 10 minutes manual cleanup vs 2 minutes automated
- **Safety**: Zero accidental deletions (must confirm)
- **Efficiency**: Cleans up 5-10 branches per cleanup on average

---

## Tips for Best Results

1. **Review Before Confirming**
   - Always review the branch list before confirming deletion
   - Pay special attention to branches with unusual names
   - Check that no active work branches are listed

2. **Use Dry Run First**
   - Run with `--dry-run` flag to preview changes
   - Verify all branches shown are actually stale
   - Proceed to real cleanup only if results look correct

3. **Clean Working Directory**
   - Commit or stash any uncommitted changes first
   - Ensures accurate merge status detection
   - Prevents conflicts during cleanup

4. **Run Regularly**
   - Schedule monthly cleanup
   - Prevents branch list from becoming unwieldy
   - Keeps git repository organized and performant

5. **After Cleanup**
   - Run `git branch -vv` to verify remaining branches
   - Check `git log --graph --oneline` to see history
   - Consider running `git gc` for optimization

---

## Common Issues

### Issue: "Not a git repository"
**Cause:** Command is being run outside a git repo
**Solution:** Navigate to a git repository first
**Example:**
```bash
cd /path/to/repo
/cleanup.branches
```
**Prevention:** Always use this command in git repositories only

---

### Issue: "Working directory not clean"
**Cause:** You have uncommitted changes that must be committed or stashed
**Solution:** Commit changes or stash them temporarily
**Example:**
```bash
git status              # See uncommitted changes
git add .              # Stage changes
git commit -m "wip"    # Commit temporarily
/cleanup.branches    # Now cleanup is safe
```
**Prevention:** Commit all work before cleanup, then amend commits later if needed

---

### Issue: "Merge in progress"
**Cause:** Repository is in the middle of a merge/rebase/conflict
**Solution:** Complete or abort the merge operation first
**Example:**
```bash
git merge --abort      # Abort ongoing merge
/cleanup.branches    # Then try again
```
**Prevention:** Resolve conflicts before cleanup operations

---

### Issue: "Permission denied" or "remote refused"
**Cause:** Insufficient permissions to delete remote-tracking branches
**Solution:** Check SSH keys or git credentials
**Example:**
```bash
# Check SSH key works
ssh -T git@github.com

# Try cleanup with local-only flag
/cleanup.branches --local-only
```
**Prevention:** Ensure you have write access to repository

---

### Issue: "Branch won't delete - not fully merged"
**Cause:** Branch contains commits not in main/develop
**Solution:** Either merge the branch or use force flag (use with caution!)
**Example:**
```bash
# Review branch first
git log branch-name --not main

# Merge it if needed
git checkout main
git merge branch-name

# Then cleanup again
/cleanup.branches
```
**Prevention:** Only delete branches that are truly complete

---

### Issue: "Remote prune fails"
**Cause:** Remote connectivity issue or git permissions problem
**Solution:** Verify remote access and retry
**Example:**
```bash
# Verify remote connection
git remote -v

# Fetch to update remote info
git fetch --prune origin

# Try cleanup again
/cleanup.branches --remote-only
```
**Prevention:** Ensure network connectivity before cleanup

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-git-workflow-master](../../agents/engineering/cs-git-workflow-master.md)** - Complete git workflow orchestration
- **[cs-code-reviewer](../../agents/engineering/cs-code-reviewer.md)** - Reviews code and manages branches

### Related Commands

- `/git.commit-assist` - Generate conventional commit messages
- `/git.create-branch` - Create new feature branches with proper naming
- `/workflow.create-pr` - Create pull requests (after cleanup)

### Related Standards

- **[Git Workflow Standards](../../docs/standards/git-standards.md)** - Project git standards
- **[Branch Naming Standards](../../docs/standards/git-standards.md#branch-naming)** - Naming conventions
- **[Merge Strategy Standards](../../docs/standards/git-standards.md#merge-strategy)** - Merge best practices

---

## Error Handling Reference

### Validation Errors

If the command reports validation errors:

1. **Invalid Repository State**
   - Check: `git status` shows clean state or valid staging
   - Fix: Resolve any conflicts or stash changes first

2. **Insufficient Permissions**
   - Check: `git remote -v` shows accessible remotes
   - Fix: Verify SSH keys or credentials are configured

3. **Network Issues**
   - Check: `ping github.com` or test remote connectivity
   - Fix: Ensure you're connected to internet/VPN

---

## Advanced Usage

### Scheduled Cleanup

Set up automatic monthly cleanup with cron/scheduler:

```bash
# macOS/Linux - add to crontab
0 0 1 * * cd /path/to/repo && /cleanup.branches --force

# Runs on 1st of month at midnight, auto-confirms
```

### Integration with CI/CD

Use in deployment pipelines:

```bash
# In CI/CD script before deploying
/cleanup.branches --local-only --force
git fetch --prune origin

# Clean state before operations
```

### Custom Branch Patterns

For repositories with non-standard branch patterns:

```bash
# Run with local-only to be conservative
/cleanup.branches --local-only

# Then manually clean remotes
git remote prune origin
```

---

## Environment Requirements

### Minimum Requirements

- Git 2.0+
- Bash/Shell environment
- Claude Code with terminal access
- Write permissions to repository

### Platform Support

- **macOS**: Full support (tested on 10.15+)
- **Linux**: Full support (Ubuntu 18.04+, CentOS 7+)
- **Windows**: Full support (PowerShell or WSL, Git Bash)

### Remote Support

- **GitHub**: Full support
- **GitLab**: Full support
- **Bitbucket**: Full support
- **Self-hosted**: Full support (all standard git servers)

---

## Success Stories

**Common Use Cases:**

1. **Team Hygiene**
   - Team runs monthly cleanup
   - Reduces branch list from 50+ to 8-10 active
   - Improves team clarity on what's in progress

2. **Repository Performance**
   - Cleanup removes unused references
   - Improves git command speed
   - Reduces local storage usage by 5-10%

3. **Onboarding New Developers**
   - New team members see clean branch list
   - Easier to understand active projects
   - Reduced confusion about branch status

---

## Related Documentation

- **[Git Book - Branching](https://git-scm.com/book/en/v2/Git-Branching-Branch-Management)** - Branch management guide
- **[Git Best Practices](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)** - Branching workflows
- **[GitHub Branch Management](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository)** - GitHub-specific guidance
- **[Project Git Standards](../../docs/standards/git-standards.md)** - This project's standards

---

## Validation Checklist

Before using this command, ensure:

- [x] You're in a git repository (`git status` works)
- [x] Working directory is clean (`git status` shows no uncommitted changes)
- [x] No merge/rebase in progress (`git status` shows normal state)
- [x] You have write access to repository
- [x] Terminal/shell is accessible

---

**Last Updated:** November 24, 2025
**Version:** 1.0.0
**Status:** Production Ready
**Maintained By:** Claude Skills Team
**Feedback:** Report issues or suggest improvements via GitHub issues
