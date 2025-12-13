# Installation Guide

Complete setup instructions for the Claude Skills Library.

---

## Prerequisites

Before installing, ensure you have the following:

### Required
- **Python 3.8+** - For CLI automation tools
  ```bash
  python3 --version  # Should be 3.8 or higher
  ```
- **Git** - For cloning the repository
  ```bash
  git --version
  ```

### Optional but Recommended
- **Claude Code** - For agent integration (if using agents)
- **Virtual Environment** - For isolated Python dependencies
  ```bash
  python3 -m venv --help  # Should show venv options
  ```

---

## Installation Steps

### Quick Start: Interactive Installer

The fastest way to install is using the interactive installation script:

```bash
# Clone the repository
git clone https://github.com/rickydwilson-dcs/claude-skills.git
cd claude-skills

# Run the interactive installer
./install.sh
```

The installer will:
- Check prerequisites (Python 3.8+, Git)
- Ask which agent domains you need (all, marketing, product, delivery, engineering)
- Install to `~/.claude-skills/` by default (or custom location)
- Create a quick start guide
- Backup any existing installation

### Manual Installation

If you prefer manual control, follow the steps below.

### 1. Clone the Repository

```bash
git clone https://github.com/rickydwilson-dcs/claude-skills.git
cd claude-skills
```

### 2. Verify Directory Structure

```bash
ls -la
```

You should see:
- `agents/` - Workflow orchestrator agents (cs-* prefix)
- `skills/` - All skill packages organized by domain
  - `marketing-team/` - Marketing skills and tools (3 skills)
  - `product-team/` - Product management skills (5 skills)
  - `engineering-team/` - Engineering skills including CTO advisor (15 skills)
  - `delivery-team/` - Delivery/PM and Atlassian tools (4 skills)
- `docs/` - Documentation and standards library
- `templates/` - Reusable templates for agents and skills
- `tools/` - Testing and validation scripts

### 3. Set Up Python Environment (Optional but Recommended)

```bash
# Create virtual environment
python3 -m venv claude-skills_venv

# Activate virtual environment
# On macOS/Linux:
source claude-skills_venv/bin/activate
# On Windows:
claude-skills_venv\Scripts\activate

# Your prompt should now show (claude-skills_venv)
```

### 4. Verify Python Installation

```bash
# Verify Python is working (no dependencies needed)
python3 -c "print('Python environment ready')"

# All Python tools use standard library only - no pip install required!
```

### 5. Install Agents

The repository includes 30 production agents across 4 domains. Install them to use with Claude Code:

```bash
# Interactive mode - choose which agents to install
python3 scripts/install_agents.py

# Install ALL agents at once
python3 scripts/install_agents.py --all --overwrite

# Preview what would be installed (dry run)
python3 scripts/install_agents.py --dry-run

# List available agents
python3 scripts/install_agents.py --list

# Install specific agent
python3 scripts/install_agents.py --agent cs-architect

# Install by domain (marketing, product, delivery, engineering)
python3 scripts/install_agents.py --domain engineering
```

Agents are installed to `~/.claude/agents/` (user-level, available everywhere).

### 6. Install Slash Commands

The repository includes 16 slash commands that automate common workflows. Install them to use with Claude Code:

```bash
# Interactive mode - choose which commands to install
python3 scripts/install_commands.py

# Install ALL commands at once
python3 scripts/install_commands.py --category all --overwrite

# Preview what would be installed (dry run)
python3 scripts/install_commands.py --dry-run

# List available commands
python3 scripts/install_commands.py --list

# Install specific command
python3 scripts/install_commands.py --command update.docs

# Install by category (analysis, generation, git, workflow, test)
python3 scripts/install_commands.py --category workflow
```

After installation, use commands in Claude Code:
```bash
/update.docs           # Auto-update documentation
/review.code src/      # Code review
/generate.tests        # Generate test cases
/create.pr             # Create pull request
/audit.security        # Security audit
```

Commands are installed to `~/.claude/commands/` (user-level, available everywhere).

---

### 7. Builder Tools (Optional - For Development)

The repository includes builder tools for creating and validating agents and skills.

#### Quick Start

```bash
# Create new agent (interactive mode)
python3 scripts/agent_builder.py

# Create new skill (interactive mode)
python3 scripts/skill_builder.py

# Validate existing agent
python3 scripts/agent_builder.py --validate agents/marketing/cs-content-creator.md

# Validate existing skill
python3 scripts/skill_builder.py --validate skills/marketing-team/content-creator
```

#### Features

- **Zero dependencies** - Python 3.8+ standard library only
- **Interactive workflows** - Guided 7-8 step processes
- **Config file mode** - YAML-based automation for CI/CD
- **Comprehensive validation** - 9 checks per agent/skill
- **Time savings**: 93-96% faster than manual creation

See [Builder Standards](standards/builder-standards.md) for validation criteria.

### 8. Verify Installation

#### Test Architecture Agent Tools

```bash
# Test the architecture analyzer on this codebase
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . --verbose

# Should output comprehensive architecture analysis including:
# - Project structure assessment
# - Architecture pattern detection
# - Dependency analysis
# - Optimization recommendations
```

#### Test Security Agent Tools

```bash
# Test the security auditor on this codebase
python3 skills/engineering-team/senior-security/scripts/security_auditor.py --input . --output text --verbose

# Should output security analysis covering:
# - OWASP Top 10 vulnerability scanning
# - Dependency vulnerability detection
# - Exposed secrets detection
# - Weak cryptography identification
```

#### Test Product Management Agent Tools

```bash
# Test RICE prioritizer with sample features
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  docs/examples/sample-features.csv --capacity 20

# Should output feature prioritization with:
# - RICE scores for each feature
# - Portfolio analysis (Quick Wins, Big Bets, Fill-Ins, Money Pits)
# - Quarterly roadmap recommendations

# Test customer interview analyzer
python3 skills/product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py \
  docs/examples/sample-interview.txt

# Should output interview analysis with:
# - Pain points extraction with severity ratings
# - Feature requests identified from transcript
# - Sentiment analysis and themes
```

#### Run Test Suite (Optional)

```bash
# Install pytest
pip install pytest

# Run full test suite (2,814 tests)
pytest tests/

# Or use the testing tools
chmod +x tools/test_cli_standards.sh
./tools/test_cli_standards.sh
```

---

## Global Availability (Use Across All Repos)

To make skills, agents, and commands available across **all repositories** on your machine without duplicating them, use Claude Code's user-level directories with symlinks.

### Directory Locations

| Element | User-Level (Global) | Project-Level (Team) |
|---------|---------------------|----------------------|
| **Agents** | `~/.claude/agents/` | `.claude/agents/` |
| **Skills** | `~/.claude/skills/` | `.claude/skills/` |
| **Commands** | `~/.claude/commands/` | `.claude/commands/` |
| **Memory** | `~/.claude/CLAUDE.md` | `./CLAUDE.md` |
| **MCP Servers** | `~/.claude.json` | `.mcp.json` |

### Complete Directory Structure

After setup, your `~/.claude/` will look like:

```
~/.claude/
├── CLAUDE.md       # Global instructions (optional)
├── agents/         # 30 agents (symlinked)
├── commands/       # 16 slash commands (symlinked)
└── skills/         # 31 skills (symlinked)
```

### Setup Script for Global Availability

Run this script to symlink your claude-skills library for global access:

```bash
#!/bin/bash
SKILLS_REPO="$HOME/claude-skills"  # Adjust to your clone location

# Setup user-level agents (symlinks to avoid duplication)
mkdir -p ~/.claude/agents
for agent in "$SKILLS_REPO"/agents/*/cs-*.md; do
  [ -f "$agent" ] && ln -sf "$agent" ~/.claude/agents/
done

# Setup user-level skills (symlinks to avoid duplication)
mkdir -p ~/.claude/skills
for skill_dir in "$SKILLS_REPO"/skills/*/*/; do
  skill_name=$(basename "$skill_dir")
  [ -d "$skill_dir" ] && ln -sf "$skill_dir" ~/.claude/skills/"$skill_name"
done

# Setup user-level commands (symlinks)
mkdir -p ~/.claude/commands
for cmd in "$SKILLS_REPO"/commands/**/*.md; do
  [ -f "$cmd" ] && ln -sf "$cmd" ~/.claude/commands/
done

echo "✓ Claude Skills now available globally"
echo "  Agents:   $(ls ~/.claude/agents/*.md 2>/dev/null | wc -l | xargs)"
echo "  Skills:   $(ls ~/.claude/skills 2>/dev/null | wc -l | xargs)"
echo "  Commands: $(ls ~/.claude/commands/*.md 2>/dev/null | wc -l | xargs)"
```

### Key Points

- **Single source of truth**: Keep everything in your `claude-skills` clone
- **Symlinks**: Changes to your library are immediately available everywhere
- **No duplication**: Each repo doesn't need its own copy
- **Team sharing**: Use `.claude/` directories in projects for team-shared versions

### Example: Global CLAUDE.md

Create `~/.claude/CLAUDE.md` for instructions that apply everywhere:

```markdown
# Global Development Standards

## Available Claude Skills
See ~/claude-skills/ for full library:
- cs-architect: System design and architecture decisions
- cs-code-reviewer: Code quality and best practices
- cs-devops-engineer: CI/CD and infrastructure

## My Preferences
- Use conventional commits
- Branch from develop, PR to main
```

---

## Configuration

### Claude AI Integration

1. **Copy skill documentation** to your Claude AI conversation:
   ```bash
   cat skills/marketing-team/content-creator/SKILL.md
   ```

2. **Reference** the skill in your prompts:
   ```
   Use the Content Creator skill to analyze this text for brand voice...
   ```

### Claude Code Integration

1. **Navigate to repository** in your terminal:
   ```bash
   cd /path/to/claude-skills
   ```

2. **Start Claude Code**:
   ```bash
   claude-code
   ```

3. **Use agents** for integrated workflows:
   ```
   # Architecture analysis
   I need to analyze the architecture of this codebase. Use the cs-architect agent
   to run the project_architect.py tool and provide recommendations.

   # Security audit
   Run a security audit using the cs-security-engineer agent. Scan for OWASP
   vulnerabilities, exposed secrets, and weak cryptography.

   # Feature prioritization
   Use the cs-product-manager agent to analyze docs/examples/sample-features.csv
   with the RICE framework. I have 20 person-months of capacity this quarter.
   ```

4. **Run Python tools directly** for quick analysis:
   ```bash
   # Architecture analysis
   python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . --verbose

   # Security audit
   python3 skills/engineering-team/senior-security/scripts/security_auditor.py --input . --verbose

   # RICE prioritization
   python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
     docs/examples/sample-features.csv --capacity 20
   ```

---

## Directory Reference

### Key Directories

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `agents/` | Workflow orchestrators | 27 specialized agents (cs-* prefix) |
| `skills/` | All skill packages | Organized by domain (4 teams) |
| `skills/marketing-team/` | Marketing skills | 3 skills with Python CLI tools |
| `skills/product-team/` | Product skills | 5 skills including RICE prioritizer |
| `skills/engineering-team/` | Engineering skills | 15 skills including CTO advisor |
| `skills/delivery-team/` | Delivery/PM skills | 4 skills with Atlassian tools |
| `docs/` | Documentation | Standards library and guides |
| `templates/` | Reusable templates | Agent and skill templates |
| `tools/` | Testing scripts | CLI validation tools |
| `output/` | Agent reports | Timestamped analysis outputs (gitignored) |

### Important Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation, skill catalog |
| `CLAUDE.md` | Development guide for Claude Code |
| `CHANGELOG.md` | Version history |
| `docs/INSTALL.md` | This installation guide |
| `docs/USAGE.md` | Usage examples and workflows |
| `docs/WORKFLOW.md` | Git workflow and branch strategy |

---

## Platform-Specific Notes

### macOS

```bash
# If you get permission errors:
chmod +x tools/*.sh

# If Python 3 is not default:
python3 --version
```

### Linux

```bash
# Install Python 3 if needed:
sudo apt-get update
sudo apt-get install python3 python3-pip

# Make scripts executable:
chmod +x tools/*.sh
```

### Windows

```bash
# Use Git Bash or WSL for best compatibility
# Python scripts work with:
python script.py

# Shell scripts may need WSL:
wsl ./tools/test_cli_standards.sh
```

---

## Verification Checklist

After installation, verify:

- [ ] Repository cloned successfully
- [ ] Python 3.8+ installed and accessible
- [ ] Can run `python3 --version`
- [ ] Can navigate to `claude-skills/` directory
- [ ] Directory structure matches (skills/, agents/, docs/, templates/)
- [ ] Architecture tool works: `python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . --verbose`
- [ ] Security tool works: `python3 skills/engineering-team/senior-security/scripts/security_auditor.py --input . --verbose`
- [ ] RICE prioritizer works: `python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py docs/examples/sample-features.csv --capacity 20`
- [ ] Sample data files exist: `docs/examples/sample-features.csv` and `docs/examples/sample-interview.txt`
- [ ] Optional: Virtual environment created and activated
- [ ] Optional: Virtual environment works (no dependencies to install)

---

## Troubleshooting

### Python Command Not Found

```bash
# Try different Python commands:
python --version
python3 --version
py --version  # Windows

# If none work, install Python 3.8+
```

### Permission Denied Errors

```bash
# Make scripts executable:
chmod +x tools/test_cli_standards.sh
chmod +x tools/test_single_script.sh

# Or run with bash explicitly:
bash tools/test_cli_standards.sh
```

### Module Import Errors

```bash
# Ensure you're in the repository root:
pwd  # Should end with /claude-skills

# If using virtual environment, activate it:
source claude-skills_venv/bin/activate
```

### Script Execution Fails

```bash
# Check Python version (must be 3.8+):
python3 --version

# Check file exists:
ls -la skills/engineering-team/senior-architect/scripts/project_architect.py

# Check file permissions:
ls -l skills/engineering-team/senior-architect/scripts/project_architect.py

# Test with minimal input:
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --help

# Run with full python3 path:
/usr/bin/python3 script.py
```

### Test Suite Failures

```bash
# Install test dependencies:
pip install pytest

# Run tests with verbose output:
pytest tests/ -v

# Run single test file:
pytest tests/test_cli_help.py -v

# Check Python syntax:
python3 -m compileall skills/
```

---

## Next Steps

After successful installation:

1. **Explore the skills** - Browse [README.md](../README.md#-available-skills) for skill catalog
2. **Try the agents** - Review [Agent Catalog](../README.md#-agent-catalog) (27 production agents)
3. **Run examples** - See [USAGE.md](USAGE.md) for workflow examples
4. **Read documentation** - Check [CLAUDE.md](../CLAUDE.md) for development guide
5. **Review standards** - See [standards/](standards/) for best practices

---

## Getting Help

- **Documentation Issues:** Check [CLAUDE.md](CLAUDE.md)
- **Bug Reports:** [GitHub Issues](https://github.com/rickydwilson-dcs/claude-skills/issues)
- **Questions:** [Discussions](https://github.com/rickydwilson-dcs/claude-skills/discussions)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Version:** 1.0.0
**Last Updated:** November 17, 2025
**Compatibility:** Python 3.8+, Claude AI, Claude Code
