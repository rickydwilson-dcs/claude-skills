# Command Installation Tool (`install_commands.py`)

Interactive command installation tool for Claude Code slash commands. Easily discover, select, and install slash commands from the claude-skills library to your `.claude/commands/` directory.

## Quick Start

```bash
# Interactive mode (recommended)
python3 scripts/install_commands.py

# List all available commands
python3 scripts/install_commands.py --list

# Install specific command
python3 scripts/install_commands.py --command workflow.update-docs

# Install all in category
python3 scripts/install_commands.py --category workflow

# Search for commands
python3 scripts/install_commands.py --search "specification"

# Preview before installing (dry-run)
python3 scripts/install_commands.py --dry-run

# Overwrite existing commands
python3 scripts/install_commands.py --command workflow.update-docs --overwrite

# Get help
python3 scripts/install_commands.py --help
```

## Features

### Interactive Selection
- Browse available categories
- View command descriptions and metadata
- Multi-select commands to install
- Detailed command previews with version info
- Clear installation summary with results

### Installation Management
- Copy command files to `.claude/commands/` directory
- Create/update manifest.json with installation tracking
- Check for conflicts and offer to overwrite
- Support for custom target directories
- Dry-run mode to preview changes

### Discovery
- Discover commands from both `commands/` and `.claude/commands/` directories
- Organize commands by category
- Search commands by name or description
- Display installed status for each command

### Manifest Tracking
Automatically creates and maintains `manifest.json`:

```json
{
  "installed": [
    {
      "name": "workflow.update-docs",
      "version": "1.0.0",
      "category": "workflow",
      "installedAt": "2025-11-24T19:44:10.241333Z",
      "source": "claude-skills",
      "description": "Update documentation files..."
    }
  ],
  "lastSync": "2025-11-24T19:44:10.241353Z",
  "version": "1.0.0"
}
```

## CLI Usage

### Mode 1: Interactive Mode (Default)

```bash
python3 scripts/install_commands.py
```

**Flow:**
1. Select category to browse
2. View available commands
3. Multi-select commands to install
4. Review installation summary
5. Confirm and proceed

**Example:**
```
============================================================
COMMAND INSTALLATION TOOL
============================================================

Step 1: Select category to browse:
  1. All Commands
  2. workflow
  3. code

Your selection: 2

Step 2: Select commands to install (3 available)
  1. workflow.update-docs - Update documentation files
  2. workflow.daily-standup - Generate daily standup report
  3. workflow.cleanup-branches - Clean up merged branches

Your selection: 1,3
[Enter]

============================================================
INSTALLATION SUMMARY
============================================================
Commands to install: 2
  • workflow.update-docs (new)
  • workflow.cleanup-branches (new)

Target directory: ~/.claude/commands/

Proceed with installation? (y/n): y

✓ Installing workflow.update-docs → workflow.update-docs.md
✓ Installing workflow.cleanup-branches → workflow.cleanup-branches.md
✓ Updated manifest: ~/.claude/commands/manifest.json

============================================================
INSTALLATION SUMMARY
============================================================

✓ Successfully installed (2):
  • workflow.update-docs
  • workflow.cleanup-branches

============================================================
```

### Mode 2: List Available Commands

```bash
# List all commands
python3 scripts/install_commands.py --list

# List by category
python3 scripts/install_commands.py --list --category workflow

# Search for commands
python3 scripts/install_commands.py --search "specification"
```

**Output:**
```
============================================================
AVAILABLE COMMANDS
============================================================

WORKFLOW (3):
  [ ] workflow.update-docs         - Update documentation files
  [✓] workflow.daily-standup       - Generate daily standup report
  [ ] workflow.cleanup-branches    - Clean up merged branches

CODE (5):
  [ ] code.review-pr               - Comprehensive code review
  [✓] code.format-check            - Validates code formatting
  ...

[✓] = Already installed
```

### Mode 3: Install Specific Command

```bash
# Install single command
python3 scripts/install_commands.py --command workflow.update-docs

# Overwrite if already installed
python3 scripts/install_commands.py --command workflow.update-docs --overwrite

# Install to custom directory
python3 scripts/install_commands.py --command workflow.update-docs --target ~/my-commands/
```

### Mode 4: Install Category

```bash
# Install all in category
python3 scripts/install_commands.py --category workflow

# Overwrite existing
python3 scripts/install_commands.py --category workflow --overwrite
```

### Mode 5: Dry-Run (Preview)

```bash
# Preview what would be installed
python3 scripts/install_commands.py --dry-run

# Preview specific command
python3 scripts/install_commands.py --command workflow.update-docs --dry-run

# Preview category
python3 scripts/install_commands.py --category workflow --dry-run
```

**Output:**
```
Installing all 3 commands in 'workflow'...
✓ Installing [DRY RUN] workflow.update-docs → workflow.update-docs.md
✓ Installing [DRY RUN] workflow.daily-standup → workflow.daily-standup.md
✓ Installing [DRY RUN] workflow.cleanup-branches → workflow.cleanup-branches.md

============================================================
INSTALLATION SUMMARY
============================================================

✓ Would install (3):
  • workflow.update-docs
  • workflow.daily-standup
  • workflow.cleanup-branches

============================================================
```

## Command Metadata

Each command's metadata is parsed from YAML frontmatter:

```yaml
---
name: workflow.update-docs
description: Update documentation files with latest information
category: workflow
version: 1.0.0
pattern: simple
tools_required: [Read, Write, Bash]
estimated_time: 5m
requires_input: false
requires_context: false
dangerous: false
interactive: false
model_preference: sonnet
---
```

**Metadata fields displayed:**
- `name` - Command identifier
- `category` - Category for organization
- `version` - Semantic version
- `description` - One-line description
- `pattern` - Command pattern (simple, multi-phase, agent-style)
- `tools_required` - Required Claude Code tools
- `estimated_time` - Typical execution time
- `requires_input` - Requires command arguments
- `requires_context` - Requires specific project structure
- `dangerous` - File-modifying operations
- `interactive` - Prompts during execution
- `model_preference` - Preferred Claude model

## Target Directory

### Default Behavior
```bash
# Installs to ~/.claude/commands/
python3 scripts/install_commands.py --command workflow.update-docs
```

### Custom Target
```bash
# Install to specific directory
python3 scripts/install_commands.py --command workflow.update-docs --target ~/my-claude-commands/

# Install to project-specific directory
python3 scripts/install_commands.py --command workflow.update-docs --target ./.claude/commands/
```

### Directory Creation
The tool automatically creates the target directory if it doesn't exist:
```
~/.claude/commands/
├── manifest.json              # Installation tracking
├── workflow.update-docs.md    # Installed command
├── code.review-pr.md          # Installed command
└── ...
```

## Manifest Management

### Automatic Tracking
The tool maintains `manifest.json` in the target directory:

- **installed** - Array of installed commands with metadata
- **lastSync** - Last installation/update timestamp (ISO 8601)
- **version** - Manifest format version

### Usage Examples

**Check installed commands:**
```bash
cat ~/.claude/commands/manifest.json | jq '.installed[].name'
```

**Track installation dates:**
```bash
cat ~/.claude/commands/manifest.json | jq '.installed[] | {name, installedAt}'
```

**Find commands by source:**
```bash
cat ~/.claude/commands/manifest.json | jq '.installed[] | select(.source == "claude-skills")'
```

## Error Handling

### Conflict Detection
```bash
# File already installed
$ python3 scripts/install_commands.py --command workflow.update-docs
Error: Already installed: workflow.update-docs (use --overwrite to update)
```

**Resolution:**
```bash
# Use --overwrite flag to update
python3 scripts/install_commands.py --command workflow.update-docs --overwrite
```

### Missing Commands
```bash
# Command not found
$ python3 scripts/install_commands.py --command nonexistent.command
Error: Command not found: nonexistent.command
```

**Resolution:**
```bash
# List available commands
python3 scripts/install_commands.py --list

# Search for similar commands
python3 scripts/install_commands.py --search "keyword"
```

### Permission Errors
```bash
# Cannot write to target directory
Error: Failed to create target directory: Permission denied
```

**Resolution:**
```bash
# Use alternative target directory
python3 scripts/install_commands.py --target ~/my-commands/

# Or create directory with proper permissions first
mkdir -p ~/.claude/commands/
chmod 755 ~/.claude/commands/
```

## Exit Codes

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | Installation completed |
| 1 | Validation failed | Command not found |
| 2 | File error | Cannot create directory |
| 3 | User cancelled | User pressed Ctrl+C |
| 99 | Unknown error | Unexpected exception |

**Check exit code:**
```bash
python3 scripts/install_commands.py --command workflow.update-docs
echo $?  # Prints exit code
```

## Performance

- **Command discovery:** < 100ms (scans markdown files)
- **Interactive selection:** Instant (memory-based)
- **Installation:** < 1s per command (file copy + manifest update)
- **Manifest update:** < 50ms (JSON serialization)

**Example timing:**
```bash
# Install 8 commands
$ time python3 scripts/install_commands.py --category workflow

real    0m0.847s
user    0m0.612s
sys     0m0.201s
```

## Advanced Usage

### Batch Installation via Scripts

```bash
#!/bin/bash
# Install all workflow commands to custom location

TARGET="${HOME}/.claude/workflow-commands"
CATEGORY="workflow"

python3 scripts/install_commands.py \
  --category "$CATEGORY" \
  --target "$TARGET" \
  --overwrite

echo "Installation complete. Commands available at: $TARGET"
```

### Integration with CI/CD

```yaml
# .github/workflows/setup-commands.yml
name: Setup Claude Commands

on: [push, pull_request]

jobs:
  install:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install commands
        run: |
          python3 scripts/install_commands.py \
            --category workflow \
            --target ~/.claude/commands/
```

### Programmatic Usage

```python
#!/usr/bin/env python3
from pathlib import Path
from scripts.install_commands import CommandCatalog, CommandInstaller

# Discover commands
repo_root = Path(".")
catalog = CommandCatalog(repo_root)

# Get all commands
all_commands = catalog.get_all_commands()
print(f"Found {len(all_commands)} commands")

# Install specific category
workflow_commands = catalog.get_category_commands("workflow")
installer = CommandInstaller(Path.home() / ".claude" / "commands")

success, installed, errors = installer.install_commands(workflow_commands)
print(f"Installed: {success}, Errors: {len(errors)}")
```

## Troubleshooting

### Commands Not Discovered
**Problem:** `No commands available`

**Causes:**
1. Running outside repository directory
2. Commands directory structure is incorrect
3. Command files don't have proper YAML frontmatter

**Solution:**
```bash
# Verify you're in repo root
ls commands/CATALOG.md

# Verify command files exist
ls .claude/commands/*.md

# Check YAML frontmatter
head -10 .claude/commands/speckit.specify.md
```

### Interactive Mode Doesn't Work
**Problem:** `--list` shows no commands but interactive mode starts

**Causes:**
1. Terminal doesn't support interactive input
2. Running in non-interactive shell

**Solution:**
```bash
# Use non-interactive mode with --command flag
python3 scripts/install_commands.py --command workflow.update-docs

# Or list first, then install
python3 scripts/install_commands.py --list
python3 scripts/install_commands.py --command <name>
```

### Manifest Corruption
**Problem:** `Error loading manifest: ...`

**Solution:**
```bash
# Backup corrupted manifest
mv ~/.claude/commands/manifest.json ~/.claude/commands/manifest.json.bak

# Reinstall commands (new manifest will be created)
python3 scripts/install_commands.py --list
```

### Path Issues on Windows
**Problem:** Paths not working correctly on Windows

**Solution:**
```bash
# Use forward slashes or raw strings
python3 scripts/install_commands.py --target "C:/Users/User/.claude/commands"

# Or use environment variable
set TARGET=%USERPROFILE%\.claude\commands
python3 scripts/install_commands.py --target %TARGET%
```

## Development

### Architecture

**Class Structure:**
- `CommandMetadata` - Parse YAML frontmatter from .md files
- `CommandCatalog` - Discover and organize commands
- `CommandInstaller` - Manage installation and manifest
- `InteractiveUI` - Provide user prompts and displays
- `CommandInstallationFlow` - Orchestrate installation flows

**Data Flow:**
```
Repository/
├── commands/              (template library)
└── .claude/commands/      (source)
    ↓
CommandCatalog (discovers + organizes)
    ↓
CommandInstallationFlow (orchestrates modes)
    ↓
CommandInstaller (copies files + manifest)
    ↓
~/.claude/commands/       (target)
├── manifest.json
└── *.md
```

### Testing Commands
```bash
# List mode
python3 scripts/install_commands.py --list

# Search mode
python3 scripts/install_commands.py --search test

# Single install
python3 scripts/install_commands.py --command speckit.specify --target /tmp/test

# Dry-run
python3 scripts/install_commands.py --dry-run --target /tmp/test

# Verify manifest
cat /tmp/test/manifest.json | python3 -m json.tool
```

## Future Enhancements

Potential improvements:
- [ ] Auto-update installed commands
- [ ] Version conflict resolution
- [ ] Dependency management between commands
- [ ] Command grouping/collections
- [ ] Uninstall functionality
- [ ] Command usage tracking
- [ ] Integration with command builder

## Support

For issues or questions:
1. Check [troubleshooting](#troubleshooting) section
2. Review command metadata with `--list`
3. Search for similar issues in repository
4. Create new issue with details

## License

Same as claude-skills repository

---

**Last Updated:** November 24, 2025
**Status:** Production-ready
**Dependencies:** None (Python stdlib only)
**Python Version:** 3.8+
