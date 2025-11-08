# Development Workflow & CI/CD Guide

**Repository:** claude-skills
**CI/CD System:** GitHub Actions
**Development Model:** Solo development with feature branches
**Version:** 1.0
**Last Updated:** November 7, 2025

---

## Table of Contents

- [Branch Strategy](#branch-strategy)
- [Development Workflow](#development-workflow)
- [CI/CD Pipeline](#cicd-pipeline)
- [Workflow Files](#workflow-files)
- [Common Operations](#common-operations)
- [Troubleshooting](#troubleshooting)

---

## Branch Strategy

### Branches

| Branch | Purpose | Protected | CI Runs On |
|--------|---------|-----------|------------|
| **main** | Production-ready code | Yes (recommended) | Push, PR |
| **develop** | Integration and testing | No | Push, PR |
| **feature/** | Feature development | No | PR only |
| **fix/** | Bug fixes | No | PR only |
| **refactor/** | Code refactoring | No | PR only |

### Branch Lifecycle

```
develop (integration) ──┐
                        ├──> main (production)
feature/* ─────────────┘
fix/* ─────────────────┘
refactor/* ────────────┘
```

---

## Development Workflow

### Solo Development Pattern (Current)

Since you cannot self-approve PRs, we use direct pushes with a feature branch workflow:

#### Pattern 1: Quick Changes (Documentation, Minor Fixes)

```bash
# Work directly on develop
git checkout develop
git pull origin develop

# Make changes
# ... edit files ...

# Commit and push
git add .
git commit -m "docs: update documentation"
git push origin develop

# Merge to main when ready
git checkout main
git merge develop
git push origin main
```

#### Pattern 2: Feature Development (Larger Changes)

```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Make changes
# ... develop feature ...

# Commit frequently
git add .
git commit -m "feat: implement feature X"

# Push to remote (CI runs on develop merge)
git push origin feature/my-feature

# Merge to develop for testing
git checkout develop
git merge feature/my-feature
git push origin develop

# CI runs automatically on develop
# If tests pass, merge to main

git checkout main
git merge develop
git push origin main

# Delete feature branch
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

#### Pattern 3: Hotfix (Critical Production Fix)

```bash
# Create fix branch from main
git checkout main
git pull origin main
git checkout -b fix/critical-bug

# Make fix
# ... fix the bug ...

# Commit
git add .
git commit -m "fix: resolve critical bug"

# Push to develop first for CI validation
git checkout develop
git merge fix/critical-bug
git push origin develop

# Wait for CI to pass
# Then merge to main

git checkout main
git merge fix/critical-bug
git push origin main

# Cleanup
git branch -d fix/critical-bug
git push origin --delete fix/critical-bug
```

---

## CI/CD Pipeline

### Automated Tests on Push

The **CI Quality Gate** runs automatically on every push to `main` and `develop`:

#### What Gets Tested

1. **YAML Lint**
   - Validates GitHub workflow files
   - Checks: `.github/workflows/*.yml`
   - Tool: `yamllint`

2. **Workflow Schema Validation**
   - Ensures workflows follow GitHub Actions schema
   - Tool: `check-jsonschema`

3. **Python Syntax Check**
   - Validates all Python scripts compile
   - Domains: marketing-skill, product-team, c-level-advisor, engineering-team, ra-qm-team
   - Tool: `python -m compileall`

4. **Security Audit**
   - Scans dependencies for known vulnerabilities
   - Files: All `requirements*.txt`
   - Tool: `safety`

5. **Markdown Link Check**
   - Validates links in README.md
   - Tool: `markdown-link-check`

6. **Pytest Suite**
   - Runs all 2,814 automated tests
   - Coverage: CLI tools, scripts, integrations
   - Command: `pytest tests/ -v --tb=short -x`

### CI Triggers

```yaml
'on':
  push:
    branches:
      - main       # Runs on direct push to main
      - develop    # Runs on direct push to develop
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  workflow_dispatch:  # Manual trigger
  repository_dispatch:  # API trigger
```

### CI Status

Check CI status:

```bash
# View recent runs
gh run list --limit 10

# View CI Quality Gate runs
gh run list --workflow="CI Quality Gate" --limit 5

# Watch latest run
gh run watch

# View logs for specific run
gh run view <run-id> --log
```

---

## Workflow Files

### Active Workflows

#### 1. CI Quality Gate (`.github/workflows/ci-quality-gate.yml`)

**Triggers:** Push to main/develop, Pull requests, Manual dispatch
**Duration:** ~25 minutes timeout
**Purpose:** Comprehensive quality checks

**Jobs:**
- Lint YAML and workflows
- Validate Python syntax
- Security audit
- Run pytest suite (2,814 tests)
- Markdown link validation

**Concurrency:** Cancels previous runs on same PR

#### 2. Auto-Close Issues on PR Merge (`.github/workflows/pr-issue-auto-close.yml`)

**Triggers:** Pull request closed (merged)
**Duration:** ~5 seconds
**Purpose:** Automate issue closure when PRs merge

**Features:**
- Extracts linked issues from PR body, title, commits
- Supports: Fixes #123, Closes #456, Resolves #789
- Adds comment explaining closure
- Updates project board status
- Closes linked issues automatically

**Note:** Only runs on PR merge events (not direct pushes)

#### 3. Smart Bidirectional Sync (`.github/workflows/smart-sync.yml`)

**Triggers:** Issue labeled, closed, reopened
**Duration:** Varies
**Purpose:** Sync issues with project boards

**Features:**
- Bidirectional sync between issues and projects
- Label-based status updates
- Prevents sync loops with debouncing

#### 4. Claude Code Review (`.github/workflows/claude-code-review.yml`)

**Triggers:** Pull request events
**Duration:** ~2 minutes
**Purpose:** AI-powered code review

**Features:**
- Automated code review comments
- Security and quality suggestions
- Best practices recommendations

#### 5. Claude Code (`.github/workflows/claude.yml`)

**Triggers:** Issue comments, Pull request comments
**Duration:** Varies
**Purpose:** Claude AI integration

**Features:**
- AI-powered issue assistance
- Automated responses to queries

### Workflow Control

#### Kill Switch

Emergency disable for all workflows:

```bash
# Disable workflows
echo "STATUS: DISABLED" > .github/WORKFLOW_KILLSWITCH
git add .github/WORKFLOW_KILLSWITCH
git commit -m "chore: disable workflows via kill switch"
git push origin main

# Re-enable workflows
echo "STATUS: ENABLED" > .github/WORKFLOW_KILLSWITCH
git add .github/WORKFLOW_KILLSWITCH
git commit -m "chore: re-enable workflows"
git push origin main
```

---

## Common Operations

### Starting New Work

```bash
# Always start from develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/new-feature

# Work on feature
# ... make changes ...

# Commit frequently
git add .
git commit -m "feat: add new functionality"
git push origin feature/new-feature
```

### Testing Before Merge to Main

```bash
# Merge to develop first
git checkout develop
git merge feature/new-feature
git push origin develop

# CI runs automatically
# Wait for green checkmark in GitHub Actions tab

# If CI passes, merge to main
git checkout main
git merge develop
git push origin main
```

### Checking CI Status

```bash
# From command line
gh run list --limit 5

# Or visit GitHub Actions tab
open https://github.com/rickydwilson-dcs/claude-skills/actions

# Watch live run
gh run watch
```

### Viewing Test Results

```bash
# Clone and run locally
cd "/Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My Drive/Websites/GitHub/claude-skills"

# Activate test environment
source /tmp/test_venv/bin/activate

# Run pytest
pytest tests/ -v

# Run specific test file
pytest tests/test_cli_help.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Manual Workflow Trigger

```bash
# Trigger CI Quality Gate manually
gh workflow run "CI Quality Gate" --ref develop

# Note: Requires admin rights on repository
# Alternative: Make trivial commit and push
```

---

## Troubleshooting

### CI Not Running After Push

**Problem:** Pushed to main/develop but CI didn't trigger

**Solutions:**

1. **Check workflow file is valid:**
   ```bash
   cat .github/workflows/ci-quality-gate.yml | head -20
   # Verify 'on: push:' section includes your branch
   ```

2. **Check kill switch:**
   ```bash
   cat .github/WORKFLOW_KILLSWITCH
   # Should show: STATUS: ENABLED
   ```

3. **Wait 1-2 minutes:** GitHub Actions can be delayed

4. **Check GitHub Actions tab:**
   ```bash
   open https://github.com/rickydwilson-dcs/claude-skills/actions
   ```

5. **Verify branch name:**
   ```bash
   git branch --show-current
   # Should be 'main' or 'develop'
   ```

### CI Failing on Specific Test

**Problem:** CI shows red X, specific test failing

**Solutions:**

1. **View logs:**
   ```bash
   gh run list --limit 1
   gh run view <run-id> --log
   ```

2. **Run locally:**
   ```bash
   source /tmp/test_venv/bin/activate
   pytest tests/test_specific.py -v
   ```

3. **Check for environment differences:**
   - Python version (CI uses 3.11)
   - Dependencies versions
   - File permissions

4. **Fix and re-push:**
   ```bash
   # Make fix
   git add .
   git commit -m "fix: resolve test failure"
   git push origin develop
   ```

### YAML Syntax Errors

**Problem:** Workflow file has YAML syntax error

**Solutions:**

1. **Validate locally:**
   ```bash
   yamllint .github/workflows/ci-quality-gate.yml
   ```

2. **Check for common issues:**
   - Incorrect indentation (use spaces, not tabs)
   - Missing quotes around strings with special characters
   - Template literals (backticks) in JavaScript blocks

3. **Use string concatenation instead of template literals:**
   ```javascript
   // Instead of:
   const msg = `Hello ${name}`;

   // Use:
   const msg = 'Hello ' + name;
   ```

### Cannot Self-Approve PRs

**Problem:** Created PR but cannot merge (need approval)

**Solution:** Use direct push workflow (Pattern 1 above)

```bash
# Work on develop
git checkout develop
# ... make changes ...
git push origin develop

# If tests pass, merge to main
git checkout main
git merge develop
git push origin main
```

### CI Tests Pass Locally But Fail on GitHub

**Problem:** Tests work on your machine but fail in CI

**Common Causes:**

1. **Path differences:**
   - CI uses Linux paths (`/`)
   - Local might use Windows paths (`\`)

2. **Environment variables:**
   - CI has different env vars
   - Check workflow file for `env:` sections

3. **Timing issues:**
   - Tests might be time-dependent
   - CI might be slower/faster

4. **File permissions:**
   - CI might not have write permissions
   - Check for hardcoded paths

**Debug approach:**
```bash
# Add debug output to workflow
- name: Debug info
  run: |
    pwd
    ls -la
    python --version
    pip list
```

---

## Best Practices

### Commit Messages

Follow conventional commits:

```
feat: add new feature
fix: resolve bug
docs: update documentation
test: add test coverage
refactor: improve code structure
chore: maintenance tasks
ci: update workflows
```

### Testing Locally Before Push

```bash
# Always run tests locally first
source /tmp/test_venv/bin/activate
pytest tests/ -v

# Run linting
yamllint .github/workflows/

# Check Python syntax
python -m compileall marketing-skill product-team c-level-advisor
```

### Branch Hygiene

```bash
# Delete merged feature branches
git branch -d feature/old-feature
git push origin --delete feature/old-feature

# Keep develop synced with main
git checkout develop
git merge main
git push origin develop
```

### Monitoring CI

```bash
# Watch for CI status before merging
gh run list --workflow="CI Quality Gate" --limit 1

# Only merge to main if CI passes on develop
```

---

## Quick Reference

### Essential Commands

```bash
# Create feature branch
git checkout develop && git pull origin develop
git checkout -b feature/my-feature

# Commit and push to develop
git checkout develop
git merge feature/my-feature
git push origin develop

# Merge to main (after CI passes)
git checkout main
git merge develop
git push origin main

# Check CI status
gh run list --limit 5
gh run watch

# View workflow logs
gh run view --log

# Manual trigger (if needed)
gh workflow run "CI Quality Gate" --ref develop
```

### CI Workflow Files

```
.github/workflows/
├── ci-quality-gate.yml          # Main CI pipeline (25 min)
├── pr-issue-auto-close.yml      # PR automation
├── smart-sync.yml               # Issue/Project sync
├── claude-code-review.yml       # AI code review
└── claude.yml                   # Claude integration
```

### Status Check URLs

- **Actions:** https://github.com/rickydwilson-dcs/claude-skills/actions
- **Branches:** https://github.com/rickydwilson-dcs/claude-skills/branches
- **Workflows:** https://github.com/rickydwilson-dcs/claude-skills/actions/workflows

---

## Summary

**Current Setup:**
- ✅ CI runs on push to `main` and `develop`
- ✅ 2,814 automated tests
- ✅ Comprehensive quality checks (YAML, Python, security, links)
- ✅ Solo development workflow (direct pushes, no self-approval needed)
- ✅ Feature branch workflow for larger changes
- ✅ Emergency kill switch available

**Recommended Workflow:**
1. Work on `develop` or feature branches
2. Push to `develop` (CI runs automatically)
3. Wait for CI to pass (green checkmark)
4. Merge `develop` to `main`
5. Push `main` (CI runs again for production validation)

**Next Steps:**
- Monitor CI runs after each push
- Address any failing tests immediately
- Keep `develop` synced with `main` regularly
- Use feature branches for larger work

---

**Questions?** Check the [GitHub Actions documentation](https://docs.github.com/en/actions) or review workflow logs with `gh run view --log`.
