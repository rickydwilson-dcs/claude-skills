# Session-Based Output Workflow Guide

Complete guide to using the session-based output organization system in claude-skills.

## Overview

The session-based output system organizes all agent-generated outputs into work sessions that capture:
- **User attribution** - Who created the work
- **Context tracking** - Branch, ticket, project, team
- **Lifecycle management** - Status, retention, promotion
- **Collaboration** - Git-tracked, shareable metadata

## Core Concepts

### Session
A **session** is a logical unit of work tied to:
- A git feature branch
- A Jira ticket or project
- A specific user
- A team (marketing, product, engineering, delivery)
- A time period (with retention policy)

**Example Session:**
```
output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
├── .session-metadata.yaml        # All context and tracking
├── 2025-11-22_08-15-30_invoice-process-analysis_cs-business-analyst.md
├── 2025-11-22_09-45-00_system-architecture_cs-architect.md
└── 2025-11-22_16-00-00_executive-summary_cs-business-analyst.md
```

### Session ID Format
```
{YYYY-MM-DD}_{branch-slug}_{short-hash}
```

**Components:**
- **Date**: Session creation date
- **Branch**: Sanitized git branch name (max 30 chars)
- **Hash**: 6-character random hex for uniqueness

**Examples:**
- `2025-11-22_feature-invoice-automation_a3f42c`
- `2025-11-22_bugfix-auth-timeout_7b89de`
- `2025-11-22_spike-payment-gateway_c19f03`

## Complete Workflows

### Workflow 1: Feature Development

**Scenario:** Developing a new invoice automation feature

```bash
# Step 1: Start feature branch
git checkout develop
git pull origin develop
git checkout -b feature/invoice-automation

# Step 2: Create work session
python3 scripts/session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Automation System" \
  --team engineering \
  --retention project

# Output:
# ✅ Session created: output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
# 🔗 Session ID: 2025-11-22_feature-invoice-automation_a3f42c

# Step 3: Set session directory
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)

# Step 4: Generate architecture analysis
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_architecture-review_cs-architect.md

# Step 5: Generate business analysis
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py transcript.md \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.md

# Step 6: Review session
python3 scripts/session_manager.py report

# Step 7: Commit session to git
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
git commit -m "docs(session): add invoice automation analysis outputs

- Architecture review
- Business process analysis
- Session: 2025-11-22_feature-invoice-automation_a3f42c"

# Step 8: Promote important outputs to Confluence
python3 scripts/promote_to_confluence.py \
  --session 2025-11-22_feature-invoice-automation_a3f42c \
  --file analysis/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.md \
  --confluence-url "https://company.atlassian.net/wiki/spaces/PROJ/pages/123456" \
  --notify "sarah@company.com,mike@company.com"

# Step 9: Close session
python3 scripts/session_manager.py close

# Step 10: Final commit
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/.session-metadata.yaml
git commit -m "feat(session): close invoice automation session

- Total outputs: 2
- Promoted: 1
- Status: closed"
```

### Workflow 2: Sprint Planning

**Scenario:** Product manager creating sprint planning artifacts

```bash
# Step 1: Create sprint session
python3 scripts/session_manager.py create \
  --ticket PROJ-200 \
  --project "Q4 Sprint 3 Planning" \
  --team product \
  --retention sprint \
  --sprint "2025-Q4-Sprint-3"

# Step 2: Generate user stories
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/product-manager/scripts/user_story_generator.py requirements.md \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_user-stories_cs-product-manager.md

# Step 3: Generate roadmap
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/product-manager/scripts/roadmap_prioritizer.py backlog.csv \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_roadmap-prioritization_cs-product-manager.md

# Step 4: Close and commit
python3 scripts/session_manager.py close
git add output/sessions/${USER}/$(python3 scripts/session_manager.py list | grep "2025-Q4-Sprint-3" | awk '{print $1}')
git commit -m "docs(sprint): Q4 Sprint 3 planning artifacts"
```

### Workflow 3: Security Audit

**Scenario:** Security engineer running security scan

```bash
# Step 1: Create audit session
python3 scripts/session_manager.py create \
  --ticket SEC-456 \
  --project "Q4 Security Audit" \
  --team engineering \
  --retention temporary

# Step 2: Run security scan
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/engineering-team/senior-secops/scripts/security_scanner.py --input . \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_security-scan_cs-secops.md

# Step 3: Generate remediation report
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
# ... generate report ...
echo "Remediation steps..." > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_remediation-plan_cs-secops.md

# Step 4: Close and notify stakeholders
python3 scripts/session_manager.py close
# Manual notification via email/Confluence
```

### Workflow 4: Ad-hoc Analysis

**Scenario:** Quick analysis that doesn't tie to a ticket

```bash
# Step 1: Create temporary session
python3 scripts/session_manager.py create \
  --project "Database Performance Investigation" \
  --team engineering \
  --retention temporary

# Step 2: Generate analysis
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
# ... run analysis ...
echo "Performance metrics..." > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_perf-analysis_cs-architect.md

# Step 3: Close when done (expires in 30 days)
python3 scripts/session_manager.py close
```

## Integration with Git Workflow

### Feature Branch Integration

Sessions naturally map to feature branches:

```bash
# Branch: feature/invoice-automation
# Session: 2025-11-22_feature-invoice-automation_a3f42c

# When you:
# 1. Create feature branch
git checkout -b feature/invoice-automation

# 2. Create session (automatically uses branch name)
python3 scripts/session_manager.py create --ticket PROJ-123 --project "Invoice Automation" --team engineering

# 3. Generate outputs (tied to session/branch)
# 4. Commit session (tracked with feature work)
git add output/sessions/*/2025-11-22_feature-invoice-automation_*/
git commit -m "docs(session): add analysis for invoice automation"

# 5. Merge feature branch (session comes with it)
git checkout develop
git merge feature/invoice-automation
```

### Multiple Users, Same Project

```bash
# User A (Tech Lead)
python3 scripts/session_manager.py create --ticket PROJ-123 --project "Invoice Automation" --team engineering
# Session: output/sessions/user-a/2025-11-22_feature-invoice-automation_a3f42c/

# User B (Product Manager)
python3 scripts/session_manager.py create --ticket PROJ-123 --project "Invoice Automation" --team product
# Session: output/sessions/user-b/2025-11-22_feature-invoice-automation_c4f88a/

# No collision! Different users, different hash
# Both sessions link to PROJ-123 via metadata
# Search finds both: python3 scripts/session_manager.py search --ticket PROJ-123
```

## Confluence Promotion Process

### Step-by-Step Manual Promotion

1. **Identify Output for Promotion**
   ```bash
   python3 scripts/session_manager.py report
   # Review outputs, select one for Confluence
   ```

2. **Read and Enhance Content**
   ```bash
   # Open file in editor
   code ${CLAUDE_SESSION_DIR}/analysis/2025-11-22_08-15-30_invoice-process-analysis_cs-business-analyst.md

   # Add Confluence enhancements:
   # - Table of contents: {toc}
   # - Status macro: {status:colour=Blue|title=In Review}
   # - @mentions for stakeholders
   # - Panels for callouts: {panel:title=Key Finding}...{panel}
   ```

3. **Create Confluence Page**
   - Navigate to Confluence space
   - Create new page or update existing
   - Title: Match output topic
   - Copy content from markdown
   - Apply Confluence formatting

4. **Track Promotion**
   ```bash
   python3 scripts/promote_to_confluence.py \
     --session 2025-11-22_feature-invoice-automation_a3f42c \
     --file analysis/2025-11-22_08-15-30_invoice-process-analysis_cs-business-analyst.md \
     --confluence-url "https://company.atlassian.net/wiki/spaces/PROJ/pages/123456" \
     --notify "sarah@company.com,mike@company.com"

   # This:
   # - Copies file to shared/promoted-to-confluence/PROJ/123456/
   # - Updates session metadata (promoted: true)
   # - Creates promotion metadata
   ```

5. **Commit Promotion**
   ```bash
   git add output/sessions/${USER}/2025-11-22_feature-invoice-automation_a3f42c/.session-metadata.yaml
   git add output/shared/promoted-to-confluence/PROJ/123456/
   git commit -m "docs(promotion): promote invoice analysis to Confluence

- Confluence page: PROJ/123456
- Notified: sarah@company.com, mike@company.com"
   ```

## Search and Discovery

### Find Sessions by Ticket

```bash
python3 scripts/session_manager.py search --ticket PROJ-123
```

### Find Sessions by Project

```bash
python3 scripts/session_manager.py search --project "Invoice Automation"
```

### Find Outputs by Agent

```bash
python3 scripts/session_manager.py search --agent cs-business-analyst
```

### Find Active Sessions

```bash
python3 scripts/session_manager.py list --status active
```

### Find Sessions by Team

```bash
python3 scripts/session_manager.py list --team engineering
```

### Find Expiring Sessions

```bash
python3 scripts/session_manager.py search --expiring-within 30
# Review before automatic cleanup
```

## Retention and Cleanup

### Retention Policies

**Project (6 months):**
```bash
python3 scripts/session_manager.py create \
  --project "Feature Development" \
  --team engineering \
  --retention project
# Expires: 6 months from creation
```

**Sprint (3 weeks):**
```bash
python3 scripts/session_manager.py create \
  --project "Sprint 3 Planning" \
  --team product \
  --retention sprint
# Expires: 21 days from creation
```

**Temporary (30 days):**
```bash
python3 scripts/session_manager.py create \
  --project "Quick Investigation" \
  --team engineering \
  --retention temporary
# Expires: 30 days from creation
```

### Cleanup Process

```bash
# 1. Find expiring sessions
python3 scripts/session_manager.py search --expiring-within 30

# 2. Review each session
python3 scripts/session_manager.py report {session-id}

# 3. Promote important outputs before expiration
python3 scripts/promote_to_confluence.py ...

# 4. Archive session (manual for now)
# Move to archive/ directory if needed for historical record
mv output/sessions/{user}/{session-id} output/archive/
```

## Best Practices

### 1. Create Sessions Before Work
Always create a session before generating outputs. This ensures proper context tracking.

### 2. Use Descriptive Project Names
- Good: "Invoice Automation System"
- Bad: "New Feature"

### 3. Link to Jira Tickets
Always provide `--ticket` for feature work. This enables cross-referencing.

### 4. Close Sessions When Complete
Mark sessions as closed when work is done. This signals completion.

### 5. Commit Sessions to Git
Sessions are collaboration artifacts. Commit them for team visibility.

### 6. Promote Strategic Outputs
Not everything needs Confluence. Promote:
- Stakeholder-facing analyses
- Architecture decisions
- Sprint planning artifacts
- Audit reports

### 7. Review Before Expiration
Set reminders to review sessions before retention expires.

### 8. Update Metadata Progressively
Add stakeholders, tags, and notes as work progresses.

## Troubleshooting

### Problem: No Current Session

```bash
# Check for current session
python3 scripts/session_manager.py current

# If none exists, create one
python3 scripts/session_manager.py create --project "Your Project" --team engineering
```

### Problem: Cannot Find Session

```bash
# Search by various criteria
python3 scripts/session_manager.py search --project "Your Project"
python3 scripts/session_manager.py list --user your-username
```

### Problem: Wrong Team in Metadata

```bash
# Edit metadata file directly
code output/sessions/{user}/{session-id}/.session-metadata.yaml

# Update team field:
created_by:
  team: "correct-team"  # marketing | product | engineering | delivery

# Commit change
git add output/sessions/{user}/{session-id}/.session-metadata.yaml
git commit -m "fix(session): update team metadata"
```

### Problem: Session Output Path Not Set

```bash
# Set CLAUDE_SESSION_DIR
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)

# Verify
echo $CLAUDE_SESSION_DIR
# Should output: /path/to/output/sessions/{user}/{session-id}
```

### Problem: Git Conflicts on Sessions

Sessions are user-isolated, so conflicts are rare. If they occur:

```bash
# Pull latest
git pull origin develop

# Since sessions are in {user}/ directories, conflicts are minimal
# If conflict exists, resolve normally:
git status
# Edit conflicting files
git add .
git commit
```

## Advanced Usage

### Batch Session Creation

```bash
# Create multiple sessions for sprint stories
for ticket in PROJ-123 PROJ-124 PROJ-125; do
  python3 scripts/session_manager.py create \
    --ticket $ticket \
    --project "Sprint 3 Stories" \
    --team product \
    --retention sprint
done
```

### Session Reports in CI/CD

```bash
# Generate session report in CI pipeline
python3 scripts/session_manager.py report --format json > session-report.json

# Parse and validate
jq '.outputs | length' session-report.json
```

### Custom Retention Dates

Edit `.session-metadata.yaml`:
```yaml
retention:
  policy: "project"
  expires_at: "2026-12-31"  # Custom date
  reason: "Critical project - retain until year-end retrospective"
```

## Additional Resources

- **Output README**: [output/README.md](../../output/README.md) - Complete reference
- **Metadata Template**: [templates/session-metadata-template.yaml](../../templates/session-metadata-template.yaml) - Schema
- **ADR**: Migration session in output/ - Complete design rationale
- **Python Scripts**:
  - `scripts/session_manager.py` - Core session management
  - `scripts/migrate_outputs.py` - Legacy migration
  - `scripts/promote_to_confluence.py` - Promotion tracking

---

**Version:** 1.0.0
**Last Updated:** 2025-11-22
**Status:** Production Ready
