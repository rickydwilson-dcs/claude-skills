# Command Installation Guide

This guide provides step-by-step instructions for installing and using slash commands from the claude-skills library.

---

## Table of Contents

- [Quick Start](#quick-start)
- [What are Slash Commands?](#what-are-slash-commands)
- [Installation Methods](#installation-methods)
- [Using Commands](#using-commands)
- [Managing Commands](#managing-commands)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

---

## Quick Start

Get started with commands in under 2 minutes:

```bash
# 1. Navigate to claude-skills repository
cd /path/to/claude-skills

# 2. Run interactive installer
python3 scripts/install_commands.py

# 3. Follow the prompts to select commands

# 4. Start using commands
/review.code "Add user authentication"
```

---

## What are Slash Commands?

**Slash commands** are task automation shortcuts that save time on repetitive developer workflows:

### Key Benefits

- **Fast** - Execute in seconds to minutes
- **Consistent** - Same quality every time
- **Automated** - No manual steps
- **Integrated** - Works with your project context

### Example Use Cases

```bash
# Specification workflow
/review.code "Add payment processing"
/audit.security
/generate.tests

# Code analysis
/review.code src/
/audit.security
/analysis.dependency-audit

# Code generation
/generate.tests src/utils.js
/generation.api-document

# Git workflow
/write.commit-message
/cleanup.branches
/create.pr
```

### Time Savings

| Task | Manual | With Command | Savings |
|------|--------|--------------|---------|
| Write specification | 2 hours | 30 min | 75% |
| Create implementation plan | 1.5 hours | 20 min | 78% |
| Security audit | 45 min | 10 min | 78% |
| Generate tests | 1 hour | 15 min | 75% |
| Code review | 30 min | 5 min | 83% |

---

## Installation Methods

### Method 1: Interactive Installation (Recommended)

The easiest way to install commands:

```bash
# Run interactive installer
python3 scripts/install_commands.py
```

**Steps:**
1. View available categories
2. Browse commands in each category
3. Select commands to install (multi-select with space bar)
4. Review and confirm installation
5. Commands are installed to `~/.claude/commands/`

**Benefits:**
- User-friendly interface
- Preview commands before installing
- Multi-select for batch installation
- Conflict detection
- Automatic manifest tracking

---

### Method 2: Category Installation

Install all commands in a category at once:

```bash
# Install all analysis commands (analysis.*)
python3 scripts/install_commands.py --category general

# Install all analysis commands
python3 scripts/install_commands.py --category analysis

# Install all generation commands
python3 scripts/install_commands.py --category generation
```

**Use When:**
- You want a complete workflow (e.g., all analysis commands)
- Setting up a new environment
- Installing for a team

---

### Method 3: Direct Command Installation

Install specific commands by name:

```bash
# Install single command
python3 scripts/install_commands.py --command review.code

# Install multiple commands (run multiple times)
python3 scripts/install_commands.py --command review.code
python3 scripts/install_commands.py --command audit.security
python3 scripts/install_commands.py --command generate.tests
```

**Use When:**
- You know exactly which command you need
- Updating a specific command
- Scripting/automation

---

### Method 4: Custom Target Directory

Install to a custom location:

```bash
# Install to custom directory
python3 scripts/install_commands.py --target ~/my-commands/

# With specific command
python3 scripts/install_commands.py --command review.code --target ~/.claude/commands/

# With category
python3 scripts/install_commands.py --category general --target /custom/path/
```

**Use When:**
- Non-standard setup
- Multiple Claude Code installations
- Testing commands before installing to default location

---

### Method 5: Dry-Run Mode

Preview what would be installed without making changes:

```bash
# Preview interactive installation
python3 scripts/install_commands.py --dry-run

# Preview category installation
python3 scripts/install_commands.py --category general --dry-run

# Preview specific command
python3 scripts/install_commands.py --command review.code --dry-run
```

**Use When:**
- Testing the installer
- Verifying command selection
- Checking for conflicts
- Reviewing before batch install

---

## Using Commands

### Basic Usage

Once installed, commands are available in any project:

```bash
# Navigate to your project
cd /path/to/your/project

# Use any installed command
/review.code "Add user authentication feature"

# Commands work with Claude Code context
/review.code src/
```

### Command Discovery

List installed commands:

```bash
# List all installed commands
python3 scripts/install_commands.py --list

# List commands by category
python3 scripts/install_commands.py --list --category analysis

# Search for commands
python3 scripts/install_commands.py --search "specification"
```

### Getting Help

Each command includes documentation:

```bash
# Most commands provide context-aware help
/review.code --help

# Or review the command file
cat ~/.claude/commands/review.code.md
```

---

## Managing Commands

### Updating Commands

Update installed commands with newer versions:

```bash
# Update single command (use --overwrite)
python3 scripts/install_commands.py --command review.code --overwrite

# Update entire category
python3 scripts/install_commands.py --category general --overwrite

# Update all (interactive mode)
python3 scripts/install_commands.py --overwrite
```

**Note:** The `--overwrite` flag is required to replace existing commands.

---

### Viewing Installed Commands

Check what's currently installed:

```bash
# View manifest
cat ~/.claude/commands/manifest.json

# List installed commands
python3 scripts/install_commands.py --list
```

**Manifest Format:**
```json
{
  "installed": [
    {
      "name": "review.code",
      "version": "1.0.0",
      "category": "general",
      "installedAt": "2025-11-24T19:44:10.241333Z",
      "source": "claude-skills",
      "description": "Create or update the feature specification..."
    }
  ],
  "lastSync": "2025-11-24T19:44:10.241353Z",
  "version": "1.0.0"
}
```

---

### Uninstalling Commands

Remove commands manually:

```bash
# Remove single command
rm ~/.claude/commands/review.code.md

# Remove all commands
rm -rf ~/.claude/commands/

# Remove manifest
rm ~/.claude/commands/manifest.json
```

**Note:** Uninstall functionality is not currently automated but planned for future releases.

---

## Troubleshooting

### Installation Issues

#### Issue: Command already installed

**Error Message:**
```
Error: Command 'review.code' is already installed.
Use --overwrite to replace it.
```

**Solution:**
```bash
# Add --overwrite flag
python3 scripts/install_commands.py --command review.code --overwrite
```

---

#### Issue: Target directory doesn't exist

**Error Message:**
```
Error: Target directory does not exist: /custom/path/
```

**Solution:**
```bash
# Create directory first
mkdir -p /custom/path/

# Or use default location (auto-created)
python3 scripts/install_commands.py  # Uses ~/.claude/commands/
```

---

#### Issue: Permission denied

**Error Message:**
```
Error: Permission denied: ~/.claude/commands/
```

**Solution:**
```bash
# Check directory permissions
ls -la ~/.claude/

# Create with proper permissions
mkdir -p ~/.claude/commands/
chmod 755 ~/.claude/commands/

# Or use custom location
python3 scripts/install_commands.py --target ~/my-commands/
```

---

### Usage Issues

#### Issue: Command not found

**Problem:** Command installed but not recognized

**Solution:**
1. Check installation location:
   ```bash
   ls ~/.claude/commands/review.code.md
   ```

2. Verify Claude Code is looking in correct directory:
   ```bash
   # Claude Code looks in ~/.claude/commands/ by default
   # Ensure commands are installed there
   ```

3. Restart Claude Code to reload commands

---

#### Issue: Command fails to execute

**Problem:** Command runs but produces errors

**Checklist:**
- [ ] Are you in a project directory?
- [ ] Does command require specific input?
- [ ] Are required tools available?
- [ ] Check command requirements in metadata

**Debug Steps:**
```bash
# Read command file to check requirements
cat ~/.claude/commands/review.code.md

# Check YAML frontmatter for:
# - requires_input: true/false
# - requires_context: true/false
# - tools_required: [...]
```

---

#### Issue: Outdated command version

**Problem:** Installed command is older than repository version

**Solution:**
```bash
# Update to latest version
cd /path/to/claude-skills
git pull origin main

# Reinstall with --overwrite
python3 scripts/install_commands.py --command review.code --overwrite
```

---

## Advanced Usage

### Batch Installation Script

Install multiple commands programmatically:

```bash
#!/bin/bash
# install-workflow-commands.sh

COMMANDS=(
  "review.code"
  "audit.security"
  "generate.tests"
  "create.pr"
)

for cmd in "${COMMANDS[@]}"; do
  python3 scripts/install_commands.py --command "$cmd"
done

echo "Installed ${#COMMANDS[@]} commands"
```

---

### CI/CD Integration

Install commands in CI/CD pipeline:

```yaml
# .github/workflows/setup-commands.yml
name: Install Claude Commands

on: [push]

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install commands
        run: |
          python3 scripts/install_commands.py \
            --category general \
            --target ~/.claude/commands/
```

---

### Team Setup

Install standardized commands for team:

```bash
# team-setup.sh
#!/bin/bash

# Required commands for all team members
REQUIRED_COMMANDS=(
  "review.code"
  "audit.security"
  "generate.tests"
  "review.code"
  "write.commit-message"
)

echo "Installing required team commands..."

for cmd in "${REQUIRED_COMMANDS[@]}"; do
  python3 scripts/install_commands.py \
    --command "$cmd" \
    --target ~/.claude/commands/

  if [ $? -eq 0 ]; then
    echo "✓ Installed: $cmd"
  else
    echo "✗ Failed: $cmd"
  fi
done

echo "Team setup complete!"
```

---

### Programmatic Usage

Use installer as Python library:

```python
#!/usr/bin/env python3
"""Install commands programmatically."""

from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from install_commands import CommandCatalog, CommandInstaller

def install_workflow_commands():
    """Install all workflow commands."""

    # Initialize
    repo_root = Path.cwd()
    target_dir = Path.home() / ".claude" / "commands"

    catalog = CommandCatalog(repo_root)
    installer = CommandInstaller(target_dir)

    # Get workflow commands
    commands = catalog.get_category_commands("general")

    # Install
    success, installed, errors = installer.install_commands(
        commands=commands,
        overwrite=False,
        dry_run=False
    )

    # Report
    print(f"Installed: {len(installed)} commands")
    if errors:
        print(f"Errors: {len(errors)}")
        for error in errors:
            print(f"  - {error}")

    return success

if __name__ == "__main__":
    success = install_workflow_commands()
    sys.exit(0 if success else 1)
```

---

### Custom Command Repository

Create your own command repository:

```bash
# 1. Create repository structure
mkdir my-commands
cd my-commands
mkdir -p commands/custom/

# 2. Copy template
cp /path/to/claude-skills/templates/command-template.md \
   commands/custom/my-command.md

# 3. Edit command
vim commands/custom/my-command.md

# 4. Install from custom location
python3 /path/to/claude-skills/scripts/install_commands.py \
  --command custom.my-command \
  --target ~/.claude/commands/
```

---

## Available Command Categories

### General Workflow (Speckit)

Complete specification-driven development workflow:

```bash
/review.code       # Create feature specification
/plan.refactor       # Ask clarification questions
/audit.security          # Generate implementation plan
/generate.tests         # Create task list
/create.pr     # Execute tasks
/analysis.dependency-audit       # Cross-artifact analysis
/write.commit-message     # Generate custom checklist
/update.docs  # Project principles
```

**Install All:**
```bash
python3 scripts/install_commands.py --category general
```

---

### Analysis Commands

Code quality and security analysis:

```bash
/review.code      # Comprehensive code review
/audit.security   # Security vulnerability scan
/analysis.dependency-audit # Dependency analysis
/plan.refactor    # Refactoring suggestions
```

**Install All:**
```bash
python3 scripts/install_commands.py --category analysis
```

---

### Generation Commands

Automated code generation:

```bash
/generate.tests  # Generate test cases
/generation.api-document   # API documentation
```

**Install All:**
```bash
python3 scripts/install_commands.py --category generation
```

---

### Git Commands

Git workflow automation:

```bash
/write.commit-message     # Conventional commit helper
/cleanup.branches    # Clean up merged branches
```

**Install All:**
```bash
python3 scripts/install_commands.py --category git
```

---

### Workflow Commands

General workflow automation:

```bash
/create.pr       # Create pull request
/update.docs     # Update documentation
/workflow.prioritize.features  # Prioritize features
```

**Install All:**
```bash
python3 scripts/install_commands.py --category workflow
```

---

## Next Steps

### After Installation

1. **Try Basic Commands**
   ```bash
   /review.code "Add user profile page"
   ```

2. **Explore Command Catalog**
   - Read [commands/CATALOG.md](../commands/CATALOG.md)
   - Browse commands by category
   - Learn command patterns

3. **Learn Command Creation**
   - Read [commands/CLAUDE.md](../commands/CLAUDE.md)
   - Review [docs/COMMANDS_CREATION.md](COMMANDS_CREATION.md)
   - Use `scripts/command_builder.py` (coming soon)

4. **Integrate with Workflow**
   - Map commands to daily tasks
   - Create team conventions
   - Automate repetitive work

---

## Additional Resources

### Documentation

- **[Command Catalog](../commands/CATALOG.md)** - All available commands
- **[Command Development Guide](../commands/CLAUDE.md)** - Create commands
- **[Command Creation Guide](COMMANDS_CREATION.md)** - Detailed creation steps
- **[Main Documentation](../CLAUDE.md)** - Repository overview

### Tools

- **[install_commands.py](../scripts/install_commands.py)** - Installation tool
- **[command_builder.py](../scripts/command_builder.py)** - Creation tool (planned)
- **[Agent Catalog](AGENTS_CATALOG.md)** - Available agents
- **[Skills Catalog](SKILLS_CATALOG.md)** - Available skills

### Support

**Issues:**
- Check [Troubleshooting](#troubleshooting)
- Search existing GitHub issues
- Create new issue with details

**Questions:**
- Review documentation first
- Check [FAQ in CATALOG.md](../commands/CATALOG.md#frequently-asked-questions)
- Ask in discussions

---

## Summary

### Installation Quick Reference

```bash
# Interactive (recommended)
python3 scripts/install_commands.py

# Install category
python3 scripts/install_commands.py --category general

# Install specific command
python3 scripts/install_commands.py --command review.code

# Preview (dry-run)
python3 scripts/install_commands.py --dry-run

# Update existing
python3 scripts/install_commands.py --command review.code --overwrite

# Custom location
python3 scripts/install_commands.py --target ~/my-commands/

# List installed
python3 scripts/install_commands.py --list
```

---

**Last Updated:** November 24, 2025
**Status:** Production-ready
**Installer Version:** 1.0.0
**Maintained By:** Claude Skills Team
