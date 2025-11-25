#!/bin/bash
# Docs Reorganization Script
# Session: 2025-11-24_20-33-06
# Purpose: Reorganize docs/ directory into clear logical hierarchy

set -e  # Exit on error

SESSION_DIR="output/2025-11-24_20-33-06_docs-reorganization"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

echo "=== Docs Reorganization Started ==="
echo "Session: $SESSION_DIR"
echo "Timestamp: $TIMESTAMP"
echo ""

# Create log file
LOG_FILE="$SESSION_DIR/execution-log.txt"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "Step 1: Create new directory structure"
mkdir -p docs/guides
mkdir -p docs/development/agents
mkdir -p docs/development/skills
mkdir -p docs/development/commands
mkdir -p docs/development/testing
mkdir -p docs/catalogs
mkdir -p docs/architecture
mkdir -p docs/reference/roadmap
mkdir -p docs/reference/examples

echo "Step 2: Move implementation docs to session output"
# These were session-specific progress docs - belong in output/
if [ -f "docs/implementation/commands-implementation.md" ]; then
    mv docs/implementation/commands-implementation.md "$SESSION_DIR/commands-implementation-original.md"
fi
if [ -f "docs/implementation/commands-documentation-summary.md" ]; then
    mv docs/implementation/commands-documentation-summary.md "$SESSION_DIR/commands-documentation-summary-original.md"
fi
if [ -f "docs/implementation/qa-validation-report.md" ]; then
    mv docs/implementation/qa-validation-report.md "$SESSION_DIR/qa-validation-report-original.md"
fi
if [ -d "docs/implementation" ]; then
    rmdir docs/implementation 2>/dev/null || echo "  Note: implementation/ not empty or already removed"
fi

echo "Step 3: Reorganize user guides"
# Move user guides to guides/
[ -f "docs/INSTALL.md" ] && mv docs/INSTALL.md docs/guides/installation.md
[ -f "docs/QUICK_START.md" ] && mv docs/QUICK_START.md docs/guides/quick-start.md
[ -f "docs/USAGE.md" ] && mv docs/USAGE.md docs/guides/usage.md
[ -f "docs/WORKFLOW.md" ] && mv docs/WORKFLOW.md docs/guides/workflow.md

# Keep existing guides
[ -f "docs/guides/skill-to-agent-flow.md" ] && mv docs/guides/skill-to-agent-flow.md docs/reference/skill-to-agent-flow.md

echo "Step 4: Reorganize development guides"
# Agent development
if [ -d "docs/agent-development" ]; then
    [ -f "docs/agent-development/README.md" ] && mv docs/agent-development/README.md docs/development/agents/README.md
    [ -f "docs/agent-development/AGENT_QUICK_START.md" ] && mv docs/agent-development/AGENT_QUICK_START.md docs/development/agents/quick-start.md
    [ -f "docs/agent-development/AGENT_DEVELOPMENT_GUIDE.md" ] && mv docs/agent-development/AGENT_DEVELOPMENT_GUIDE.md docs/development/agents/guide.md
    [ -f "docs/agent-development/COMPLETENESS_CHECKLIST.md" ] && mv docs/agent-development/COMPLETENESS_CHECKLIST.md docs/development/agents/completeness-checklist.md
    rmdir docs/agent-development 2>/dev/null || echo "  Note: agent-development/ not empty"
fi

# Command development
[ -f "docs/COMMANDS_INSTALLATION.md" ] && mv docs/COMMANDS_INSTALLATION.md docs/development/commands/installation.md
[ -f "docs/COMMANDS_CREATION.md" ] && mv docs/COMMANDS_CREATION.md docs/development/commands/creation.md

# Testing
if [ -d "docs/testing" ]; then
    [ -f "docs/testing/TESTING_QUICK_START.md" ] && mv docs/testing/TESTING_QUICK_START.md docs/development/testing/quick-start.md
    [ -f "docs/testing/TESTING_GUIDE.md" ] && mv docs/testing/TESTING_GUIDE.md docs/development/testing/guide.md
    [ -f "docs/testing/README.md" ] && mv docs/testing/README.md docs/development/testing/README.md
    rmdir docs/testing 2>/dev/null || echo "  Note: testing/ not empty"
fi

echo "Step 5: Reorganize catalogs"
[ -f "docs/AGENTS_CATALOG.md" ] && mv docs/AGENTS_CATALOG.md docs/catalogs/agents.md
[ -f "docs/SKILLS_CATALOG.md" ] && mv docs/SKILLS_CATALOG.md docs/catalogs/skills.md
# commands catalog stays in commands/CATALOG.md

echo "Step 6: Rename standards files (remove -standards suffix)"
cd docs/standards
[ -f "documentation-standards.md" ] && mv documentation-standards.md documentation.md
[ -f "communication-standards.md" ] && mv communication-standards.md communication.md
[ -f "quality-standards.md" ] && mv quality-standards.md quality.md
[ -f "security-standards.md" ] && mv security-standards.md security.md
[ -f "git-workflow-standards.md" ] && mv git-workflow-standards.md git-workflow.md
[ -f "cli-standards.md" ] && mv cli-standards.md cli.md
[ -f "builder-standards.md" ] && mv builder-standards.md builders.md
[ -f "command-standards.md" ] && mv command-standards.md commands.md
[ -f "anthropic-skill-validation.md" ] && mv anthropic-skill-validation.md anthropic-validation.md
cd ../..

echo "Step 7: Move architecture and reference docs"
[ -f "docs/workflows/session-based-outputs.md" ] && mv docs/workflows/session-based-outputs.md docs/architecture/session-outputs.md
[ -d "docs/workflows" ] && rmdir docs/workflows 2>/dev/null

if [ -d "docs/roadmap" ]; then
    [ -f "docs/roadmap/slash-commands-roadmap.md" ] && mv docs/roadmap/slash-commands-roadmap.md docs/reference/roadmap/commands-roadmap.md
    [ -f "docs/roadmap/slash-commands-decisions.md" ] && mv docs/roadmap/slash-commands-decisions.md docs/reference/roadmap/commands-decisions.md
    rmdir docs/roadmap 2>/dev/null
fi

if [ -d "docs/examples" ]; then
    [ -f "docs/examples/README.md" ] && mv docs/examples/README.md docs/reference/examples/README.md
    rmdir docs/examples 2>/dev/null
fi

echo ""
echo "=== Reorganization Complete ==="
echo "Check $LOG_FILE for full details"
echo ""
echo "Next steps:"
echo "1. Create README files for navigation"
echo "2. Update all cross-references"
echo "3. Update documentation standards"
echo "4. Test all links"
