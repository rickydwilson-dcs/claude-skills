# Agent Output Directory - Session-Based Organization

This directory stores all agent-generated reports, analyses, and outputs from the claude-skills repository using a **session-based organization system** that provides user attribution, work context tracking, and integration with knowledge management systems.

## Directory Structure

```
output/
├── sessions/                           # User session outputs (git-tracked)
│   └── {user}/                         # User-specific directory
│       └── {session-id}/               # Unique work session
│           ├── .session-metadata.yaml  # Session context and tracking
│           └── *.md                    # All outputs (flat structure, categorized via metadata)
├── shared/                            # Cross-user shared resources
│   ├── promoted-to-confluence/        # Outputs promoted to Confluence
│   │   └── {space-key}/              # Confluence space
│   │       └── {page-id}/            # Confluence page
│   └── team-resources/               # Team-level shared resources
│       ├── marketing/
│       ├── product/
│       ├── engineering/
│       └── delivery/
├── archive/                           # Archived sessions
│   └── legacy-outputs/               # Migration from old system
└── README.md                          # This file
```

## Quick Start

### 1. Create a Session

```bash
# Create a new work session
python3 scripts/session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Automation" \
  --team engineering

# Output: Session created at output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
# Environment variable set: CLAUDE_SESSION_DIR
```

### 2. Generate Agent Outputs

```bash
# Get current session directory
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)

# Generate outputs to current session (flat structure)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py transcript.md \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.md
```

### 3. Close Session

```bash
# Close when work is complete
python3 scripts/session_manager.py close

# Generates report and updates metadata
```

## Session Management

### Create New Session

```bash
python3 scripts/session_manager.py create \
  --ticket PROJ-123 \
  --project "Invoice Automation" \
  --team engineering \
  [--retention project|sprint|temporary] \
  [--sprint "2025-Q4-Sprint-3"] \
  [--epic PROJ-100] \
  [--release v2.1.0]
```

**Required Fields:**
- `--project`: Human-readable project name
- `--team`: One of: marketing, product, engineering, delivery

**Optional Fields:**
- `--ticket`: Jira ticket ID (recommended)
- `--retention`: Retention policy (default: project = 6 months)
- `--sprint`, `--epic`, `--release`: Additional context

### List Sessions

```bash
# List all sessions
python3 scripts/session_manager.py list

# Filter by status
python3 scripts/session_manager.py list --status active

# Filter by team
python3 scripts/session_manager.py list --team engineering

# Filter by user
python3 scripts/session_manager.py list --user rickydwilson-dcs
```

### Search Sessions

```bash
# Search by ticket
python3 scripts/session_manager.py search --ticket PROJ-123

# Search by project name
python3 scripts/session_manager.py search --project "Invoice Automation"

# Search by agent
python3 scripts/session_manager.py search --agent cs-business-analyst

# Search by tag
python3 scripts/session_manager.py search --tag invoice-automation
```

### Generate Reports

```bash
# Report on current session
python3 scripts/session_manager.py report

# Report on specific session
python3 scripts/session_manager.py report 2025-11-22_feature-invoice-automation_a3f42c

# JSON format
python3 scripts/session_manager.py report --format json
```

### Close Session

```bash
# Close current session
python3 scripts/session_manager.py close

# Close specific session
python3 scripts/session_manager.py close 2025-11-22_feature-invoice-automation_a3f42c
```

## Session Metadata

Each session includes a `.session-metadata.yaml` file with:

- **Session Identity**: ID, creation time, user, team
- **Work Context**: Branch, ticket, project, sprint, epic, release
- **Outputs Tracking**: List of all generated files with promotion status
- **Stakeholders**: People involved or notified
- **Retention Policy**: Expiration date and reason
- **Integration Links**: Jira, Confluence, OneDrive, GitHub PR
- **Tags**: Searchable keywords
- **Notes**: Free-form context

See `templates/session-metadata-template.yaml` for complete schema.

## Confluence Promotion Workflow

### Manual Promotion Process

1. **Identify Output for Promotion**
   ```bash
   python3 scripts/session_manager.py report
   ```

2. **Review and Enhance Content**
   - Add Confluence-specific formatting (macros, @mentions)
   - Add table of contents
   - Add status indicators

3. **Manually Copy to Confluence**
   - Open Confluence page
   - Paste content
   - Enhance formatting
   - Save page

4. **Track Promotion**
   ```bash
   python3 scripts/promote_to_confluence.py \
     --session 2025-11-22_feature-invoice-automation_a3f42c \
     --file 2025-11-22_06-58-38_invoice-process-analysis_cs-business-analyst.md \
     --confluence-url "https://company.atlassian.net/wiki/spaces/PROJ/pages/123456" \
     --notify "sarah@company.com,mike@company.com"
   ```

This updates:
- Session metadata (marks output as promoted)
- Copies file to `shared/promoted-to-confluence/`
- Creates promotion metadata for tracking

## File Naming Convention

Within sessions, outputs still use timestamped filenames:

```
YYYY-MM-DD_HH-MM-SS_<topic>_<agent-name>.md
```

**Examples:**
- `2025-11-22_08-30-45_invoice-process-analysis_cs-business-analyst.md`
- `2025-11-22_14-22-10_architecture-review_cs-architect.md`
- `2025-11-22_16-45-30_security-scan_cs-secops.md`

## Git Workflow

### Sessions Are Git-Tracked

Unlike the old system where outputs were gitignored, **sessions are committed to git** for:
- Complete work history
- User attribution
- Context preservation
- Collaboration support

### Committing Sessions

```bash
# After creating session
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
git commit -m "feat(sessions): create session for invoice automation analysis

- Ticket: PROJ-123
- Project: Invoice Automation System
- Team: Engineering"

# After adding outputs
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/
git commit -m "docs(analysis): add invoice process analysis

- Agent: cs-business-analyst
- Session: 2025-11-22_feature-invoice-automation_a3f42c
- Output: invoice-process-analysis_cs-business-analyst.md"

# After closing session
git add output/sessions/rickydwilson-dcs/2025-11-22_feature-invoice-automation_a3f42c/.session-metadata.yaml
git commit -m "feat(sessions): close invoice automation analysis session

- Total outputs: 4
- Promoted to Confluence: 2
- Status: closed"
```

## Integration with Agents

### Updated Agent Pattern

Agents now write to `$CLAUDE_SESSION_DIR` instead of flat directories:

```bash
# Old pattern (deprecated)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py transcript.md \
  > output/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.md

# New pattern (session-based)
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py transcript.md \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_invoice-process-analysis_cs-business-analyst.md
```

### Agent Examples

#### Business Analyst (cs-business-analyst)
```bash
# Create session
python3 scripts/session_manager.py create --ticket PROJ-123 --project "Invoice Process" --team delivery

# Run analysis
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/product-team/business-analyst-toolkit/scripts/process_analyzer.py transcript.md \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_process-analysis_cs-business-analyst.md

# Close session
python3 scripts/session_manager.py close
```

#### Architect (cs-architect)
```bash
# Create session
python3 scripts/session_manager.py create --ticket PROJ-123 --project "System Architecture" --team engineering

# Generate architecture review
export CLAUDE_SESSION_DIR=$(python3 scripts/session_manager.py current | grep "Path:" | cut -d' ' -f2)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . \
  > ${CLAUDE_SESSION_DIR}/${TIMESTAMP}_architecture-review_cs-architect.md

# Close session
python3 scripts/session_manager.py close
```

## Migration from Legacy System

All previous outputs have been migrated to:
```
output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/
```

This migration session contains all 10 files from the old flat structure with preserved timestamps and names.

## Retention Policies

### Policy Types

1. **project** (default) - 6 months
   - For project-related work
   - Keep until post-launch retrospective

2. **sprint** - 3 weeks
   - For sprint-specific work
   - Keep until sprint complete + 1 sprint buffer

3. **temporary** - 30 days
   - For ad-hoc analyses
   - Short-term investigations

### Cleanup

```bash
# Find expired sessions
python3 scripts/session_manager.py search --expiring-within 30

# Archive old sessions (manual process)
# Review outputs before archiving
python3 scripts/session_manager.py archive {session-id}
```

## Best Practices

1. **Create Sessions Before Work** - Always start with session creation
2. **Descriptive Project Names** - Use clear, searchable project names
3. **Add Ticket Numbers** - Link to Jira tickets for context
4. **Close When Complete** - Mark sessions as closed when work is done
5. **Promote Important Outputs** - Use promotion workflow for Confluence
6. **Commit to Git** - Commit sessions for history and collaboration
7. **Update Metadata** - Add stakeholders, tags, and notes as work progresses
8. **Review Before Expiration** - Check expiring sessions periodically

## Troubleshooting

### No Current Session

```bash
# Check if session exists
python3 scripts/session_manager.py current

# If none, create one
python3 scripts/session_manager.py create --project "Your Project" --team engineering
```

### Cannot Find Session

```bash
# Search for session
python3 scripts/session_manager.py search --project "Your Project"

# List all sessions
python3 scripts/session_manager.py list
```

### Git Conflicts

Sessions are user-isolated, so conflicts are rare. If they occur:
```bash
# Pull latest
git pull origin develop

# Sessions are in separate user directories, so conflicts are minimal
```

## Additional Resources

- **Session Guide**: `docs/workflows/session-based-outputs.md`
- **Metadata Template**: `templates/session-metadata-template.yaml`
- **ADR**: `output/sessions/rickydwilson-dcs/2025-11-22_migration-legacy-outputs_000000/2025-11-22_07-53-43_session-based-output-adr_cs-architect.md`

---

**Last Updated:** 2025-11-22
**Version:** 2.0.0 (Session-Based)
**Status:** ✅ Production Ready

**Organize your work with sessions!** 🚀
