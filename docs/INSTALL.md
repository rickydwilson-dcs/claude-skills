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

### 1. Clone the Repository

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
```

### 2. Verify Directory Structure

```bash
ls -la
```

You should see:
- `agents/` - Workflow orchestrator agents
- `marketing-skill/` - Marketing skills and tools
- `c-level-advisor/` - Executive advisory skills
- `product-team/` - Product management skills
- `engineering-team/` - Engineering skills
- `ra-qm-team/` - Regulatory affairs & quality management
- `project-management/` - PM and Atlassian tools
- `tools/` - Testing and validation scripts
- `documentation/` - Standards and migration docs

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

### 4. Install Python Dependencies (if using automation tools)

```bash
# Most scripts have no external dependencies
# If a script requires packages, it will have a requirements.txt in its directory

# Example for scripts with dependencies:
pip install -r product-team/product-manager-toolkit/requirements.txt
```

### 5. Verify Installation

#### Test CLI Tools

```bash
# Test a Python CLI tool
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py --help

# Should display help text with usage examples
```

#### Test with Sample Data

```bash
# Run with sample input
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt

# Should output brand voice analysis
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

## Configuration

### Claude AI Integration

1. **Copy skill documentation** to your Claude AI conversation:
   ```bash
   cat marketing-skill/content-creator/SKILL.md
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

3. **Use agents**:
   ```
   @cs-content-creator help me create a blog post about AI
   ```

---

## Directory Reference

### Key Directories

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `agents/` | Workflow orchestrators | 5 specialized agents (cs-*) |
| `marketing-skill/` | Marketing tools | 3 skills, Python CLI tools |
| `c-level-advisor/` | Executive advisory | 2 skills, strategy tools |
| `product-team/` | Product management | 5 skills, RICE prioritizer |
| `engineering-team/` | Engineering tools | 15 skills, architecture tools |
| `ra-qm-team/` | Compliance tools | 12 skills, regulatory tools |
| `delivery-team/` | PM & Atlassian | 4 skills, Jira/Confluence |
| `tools/` | Testing scripts | CLI validation tools |
| `documentation/` | Standards & guides | CLI standards, migration docs |
| `templates/` | Reusable templates | Agent template, Python CLI template |

### Important Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation, skill catalog |
| `TESTING_GUIDE.md` | Complete testing documentation |
| `CHANGELOG.md` | Version history |
| `CLAUDE.md` | Development guide for Claude |
| `USAGE.md` | Usage examples and workflows |

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
- [ ] Can view help: `python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py --help`
- [ ] Can run sample: `python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py marketing-skill/content-creator/assets/sample-content.txt`
- [ ] Test scripts executable: `chmod +x tools/*.sh && ./tools/test_cli_standards.sh`
- [ ] Optional: Virtual environment created and activated
- [ ] Optional: Pytest installed and tests passing

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
ls -la marketing-skill/content-creator/scripts/brand_voice_analyzer.py

# Check file permissions:
ls -l marketing-skill/content-creator/scripts/brand_voice_analyzer.py

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
python3 -m compileall marketing-skill/
```

---

## Next Steps

After successful installation:

1. **Explore the skills** - Browse [README.md](README.md#-available-skills) for skill catalog
2. **Try the agents** - Review [Agent Catalog](README.md#-agent-catalog)
3. **Run examples** - See [USAGE.md](USAGE.md) for workflow examples
4. **Read documentation** - Check [CLAUDE.md](CLAUDE.md) for development guide
5. **Run tests** - Validate installation with [TESTING_GUIDE.md](TESTING_GUIDE.md)

---

## Getting Help

- **Documentation Issues:** Check [CLAUDE.md](CLAUDE.md)
- **Bug Reports:** [GitHub Issues](https://github.com/alirezarezvani/claude-skills/issues)
- **Questions:** [Discussions](https://github.com/alirezarezvani/claude-skills/discussions)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Version:** 1.0.0
**Last Updated:** November 17, 2025
**Compatibility:** Python 3.8+, Claude AI, Claude Code
