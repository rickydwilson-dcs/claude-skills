#!/bin/bash

# Claude Skills Installation Script
# Version: 1.0.0
# Description: Interactive installation for claude-skills repository

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Installation configuration
REPO_NAME="claude-skills"
INSTALL_DIR="${HOME}/.claude-skills"
CLAUDE_CODE_DIR="${HOME}/.claude"
BACKUP_DIR="${HOME}/.claude-skills-backup-$(date +%Y%m%d-%H%M%S)"

# Helper functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    local missing_deps=()

    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python 3 found: $PYTHON_VERSION"
    else
        missing_deps+=("python3")
        print_error "Python 3 not found"
    fi

    # Check Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | awk '{print $3}')
        print_success "Git found: $GIT_VERSION"
    else
        missing_deps+=("git")
        print_error "Git not found"
    fi

    # Check if we're in a git repository
    if git rev-parse --git-dir > /dev/null 2>&1; then
        print_success "Running inside git repository"
    else
        print_warning "Not inside a git repository"
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        echo ""
        echo "Please install missing dependencies and run again."
        exit 1
    fi

    echo ""
}

# Display welcome message
display_welcome() {
    clear
    print_header "Claude Skills Installation"
    echo ""
    echo "This script will help you install the claude-skills repository"
    echo "containing 41 production agents and 40 skill packages."
    echo ""
    echo "What you'll get:"
    echo "  • 41 production agents (Marketing, Product, Delivery, Engineering)"
    echo "  • 132 Python CLI automation tools"
    echo "  • 16 slash commands"
    echo "  • Comprehensive standards library"
    echo "  • Templates and workflows"
    echo ""
    echo "Installation locations:"
    echo "  • Agents: ~/.claude/agents/ (Claude Code discovery)"
    echo "  • Skills: ~/.claude-skills/skills/"
    echo "  • Commands: ~/.claude/commands/"
    echo ""
}

# Ask installation questions
ask_questions() {
    print_header "Installation Configuration"
    echo ""

    # Question 1: Installation type
    echo "1. How do you want to use Claude Skills?"
    echo "   a) Claude Code (VSCode extension) - Recommended"
    echo "   b) Claude AI (claude.ai) - Upload to Projects"
    echo "   c) Both"
    echo ""
    read -p "Choose (a/b/c) [a]: " INSTALL_TYPE
    INSTALL_TYPE=${INSTALL_TYPE:-a}

    # Question 2: Which agents to install
    echo ""
    echo "2. Which agent domains do you need?"
    echo "   a) All agents (41 production agents) - Recommended"
    echo "   b) Marketing only (4 agents)"
    echo "   c) Product only (6 agents)"
    echo "   d) Delivery only (4 agents)"
    echo "   e) Engineering only (27 agents)"
    echo ""
    read -p "Choose (a/b/c/d/e) [a]: " AGENT_SELECTION
    AGENT_SELECTION=${AGENT_SELECTION:-a}

    # Question 3: Installation location
    echo ""
    echo "3. Installation location"
    if [ "$INSTALL_TYPE" = "a" ] || [ "$INSTALL_TYPE" = "c" ]; then
        echo "   Default: ${INSTALL_DIR}"
        echo ""
        read -p "Use default location? (y/n) [y]: " USE_DEFAULT
        USE_DEFAULT=${USE_DEFAULT:-y}

        if [ "$USE_DEFAULT" != "y" ]; then
            read -p "Enter custom path: " CUSTOM_PATH
            INSTALL_DIR="$CUSTOM_PATH"
        fi
    fi

    echo ""
}

# Confirm installation
confirm_installation() {
    print_header "Installation Summary"
    echo ""
    echo "Install Type:    $INSTALL_TYPE"
    echo "Agent Selection: $AGENT_SELECTION"
    echo "Install Path:    $INSTALL_DIR"
    echo ""
    read -p "Proceed with installation? (y/n) [y]: " CONFIRM
    CONFIRM=${CONFIRM:-y}

    if [ "$CONFIRM" != "y" ]; then
        echo "Installation cancelled."
        exit 0
    fi
    echo ""
}

# Backup existing installation
backup_existing() {
    if [ -d "$INSTALL_DIR" ]; then
        print_info "Existing installation found. Creating backup..."
        mkdir -p "$BACKUP_DIR"
        cp -r "$INSTALL_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
        print_success "Backup created: $BACKUP_DIR"
    fi
}

# Install agents
install_agents() {
    print_header "Installing Agents"

    # Create directories
    mkdir -p "$INSTALL_DIR/agents"
    mkdir -p "$CLAUDE_CODE_DIR/agents"

    case $AGENT_SELECTION in
        a) # All agents
            print_info "Installing all 41 production agents..."
            # Install to ~/.claude-skills/agents/ for reference
            cp -r agents/* "$INSTALL_DIR/agents/" 2>/dev/null || true
            # Install to ~/.claude/agents/ for Claude Code discovery (flat structure)
            for agent in agents/*/cs-*.md; do
                cp "$agent" "$CLAUDE_CODE_DIR/agents/" 2>/dev/null || true
            done
            print_success "Installed 41 agents to ~/.claude/agents/ (Claude Code)"
            print_success "Installed 41 agents to ~/.claude-skills/agents/ (reference)"
            ;;
        b) # Marketing only
            print_info "Installing marketing agents..."
            mkdir -p "$INSTALL_DIR/agents/marketing"
            cp -r agents/marketing/* "$INSTALL_DIR/agents/marketing/" 2>/dev/null || true
            for agent in agents/marketing/cs-*.md; do
                cp "$agent" "$CLAUDE_CODE_DIR/agents/" 2>/dev/null || true
            done
            print_success "Installed 4 marketing agents"
            ;;
        c) # Product only
            print_info "Installing product agents..."
            mkdir -p "$INSTALL_DIR/agents/product"
            cp -r agents/product/* "$INSTALL_DIR/agents/product/" 2>/dev/null || true
            for agent in agents/product/cs-*.md; do
                cp "$agent" "$CLAUDE_CODE_DIR/agents/" 2>/dev/null || true
            done
            print_success "Installed 6 product agents"
            ;;
        d) # Delivery only
            print_info "Installing delivery agents..."
            mkdir -p "$INSTALL_DIR/agents/delivery"
            cp -r agents/delivery/* "$INSTALL_DIR/agents/delivery/" 2>/dev/null || true
            for agent in agents/delivery/cs-*.md; do
                cp "$agent" "$CLAUDE_CODE_DIR/agents/" 2>/dev/null || true
            done
            print_success "Installed 4 delivery agents"
            ;;
        e) # Engineering only
            print_info "Installing engineering agents..."
            mkdir -p "$INSTALL_DIR/agents/engineering"
            cp -r agents/engineering/* "$INSTALL_DIR/agents/engineering/" 2>/dev/null || true
            for agent in agents/engineering/cs-*.md; do
                cp "$agent" "$CLAUDE_CODE_DIR/agents/" 2>/dev/null || true
            done
            print_success "Installed 27 engineering agents"
            ;;
    esac

    echo ""
}

# Install skills
install_skills() {
    print_header "Installing Skill Packages"

    print_info "Installing 40 skill packages..."

    # Copy skills directory (all 4 domains)
    if [ -d "skills" ]; then
        case $AGENT_SELECTION in
            a) # All skills
                cp -r skills "$INSTALL_DIR/" 2>/dev/null || true
                print_success "Installed all 40 skill packages (4 domains)"
                ;;
            b) # Marketing only
                mkdir -p "$INSTALL_DIR/skills"
                [ -d "skills/marketing-team" ] && cp -r skills/marketing-team "$INSTALL_DIR/skills/" 2>/dev/null || true
                print_success "Installed 4 marketing skill packages"
                ;;
            c) # Product only
                mkdir -p "$INSTALL_DIR/skills"
                [ -d "skills/product-team" ] && cp -r skills/product-team "$INSTALL_DIR/skills/" 2>/dev/null || true
                print_success "Installed 7 product skill packages"
                ;;
            d) # Delivery only
                mkdir -p "$INSTALL_DIR/skills"
                [ -d "skills/delivery-team" ] && cp -r skills/delivery-team "$INSTALL_DIR/skills/" 2>/dev/null || true
                print_success "Installed 4 delivery skill packages"
                ;;
            e) # Engineering only
                mkdir -p "$INSTALL_DIR/skills"
                [ -d "skills/engineering-team" ] && cp -r skills/engineering-team "$INSTALL_DIR/skills/" 2>/dev/null || true
                print_success "Installed 26 engineering skill packages"
                ;;
        esac
    else
        print_warning "Skills directory not found - skipping skill installation"
    fi

    echo ""
}

# Install slash commands
install_commands() {
    print_header "Installing Slash Commands"

    mkdir -p "$CLAUDE_CODE_DIR/commands"

    if [ -d "commands" ]; then
        print_info "Installing 16 slash commands..."

        # Find all command .md files (excluding README, CLAUDE.md, CATALOG.md)
        for cmd in commands/*/*.md; do
            filename=$(basename "$cmd")
            # Skip non-command files
            if [[ "$filename" != "README.md" && "$filename" != "CLAUDE.md" && "$filename" != "CATALOG.md" ]]; then
                cp "$cmd" "$CLAUDE_CODE_DIR/commands/" 2>/dev/null || true
            fi
        done

        cmd_count=$(ls "$CLAUDE_CODE_DIR/commands/"*.md 2>/dev/null | wc -l | xargs)
        print_success "Installed $cmd_count slash commands to ~/.claude/commands/"
    else
        print_warning "Commands directory not found - skipping command installation"
    fi

    echo ""
}

# Install standards and templates
install_resources() {
    print_header "Installing Resources"

    print_info "Installing documentation and standards..."
    [ -d "docs" ] && cp -r docs "$INSTALL_DIR/" 2>/dev/null || true
    print_success "Installed docs/ (includes standards, testing guides, workflow)"

    print_info "Installing templates..."
    [ -d "templates" ] && cp -r templates "$INSTALL_DIR/" 2>/dev/null || true
    print_success "Installed templates"

    echo ""
}

# Configure Claude Code
configure_claude_code() {
    if [ "$INSTALL_TYPE" = "a" ] || [ "$INSTALL_TYPE" = "c" ]; then
        print_header "Configuring Claude Code"

        # Check for VSCode
        if command -v code &> /dev/null; then
            print_success "VSCode found"
            print_info "Claude Code extension will auto-discover agents in:"
            echo "           $INSTALL_DIR/agents/"
        else
            print_warning "VSCode not found in PATH"
            print_info "Install VSCode and Claude Code extension manually"
        fi

        echo ""
    fi
}

# Create quick start guide
create_quick_start() {
    print_header "Creating Quick Start Guide"

    cat > "$INSTALL_DIR/QUICK_START.txt" << EOF
Claude Skills - Quick Start Guide
Generated: $(date)

Installation Complete!

AGENTS INSTALLED:
- Claude Code location: $CLAUDE_CODE_DIR/agents/
- Reference location: $INSTALL_DIR/agents/
- Count: $(find "$CLAUDE_CODE_DIR/agents" -name "cs-*.md" 2>/dev/null | wc -l | xargs) agents

SLASH COMMANDS INSTALLED:
- Location: $CLAUDE_CODE_DIR/commands/
- Count: $(ls "$CLAUDE_CODE_DIR/commands/"*.md 2>/dev/null | wc -l | xargs) commands

SKILLS INSTALLED:
- Location: $INSTALL_DIR/skills/
- Count: $(find "$INSTALL_DIR/skills" -maxdepth 2 -type d -name "senior-*" -o -name "*-toolkit" -o -name "*-expert" 2>/dev/null | wc -l | xargs) skills

USAGE:

1. Claude Code (VSCode):
   - Agents are automatically discovered from ~/.claude/agents/
   - Type: @cs-product-manager
   - Example: "@cs-content-creator help me write a blog post"
   - Use slash commands: /update.docs, /review.code, /generate.tests

2. Claude AI (claude.ai):
   - Upload agents from: $INSTALL_DIR/agents/
   - Upload skills from: $INSTALL_DIR/skills/
   - Reference in your Project

3. Python Tools (132 total):
   - All scripts in: $INSTALL_DIR/skills/*/scripts/*.py
   - Run with: python3 path/to/script.py --help

IMPORTANT DIRECTORIES:
- ~/.claude/agents/     - Claude Code agent discovery (restart VSCode after changes)
- ~/.claude/commands/   - Claude Code slash commands
- ~/.claude-skills/     - Full skill packages with Python tools

DOCUMENTATION:
- Main README: $INSTALL_DIR/README.md (if exists)
- Agent Guide: $INSTALL_DIR/agents/CLAUDE.md
- Standards: $INSTALL_DIR/docs/standards/
- Templates: $INSTALL_DIR/templates/
- Installation: $INSTALL_DIR/docs/guides/installation.md
- Usage Guide: $INSTALL_DIR/docs/guides/usage.md

NEXT STEPS:
1. RESTART VSCODE to discover new agents
2. Try an agent: @cs-product-manager (in Claude Code)
3. Try a command: /update.docs
4. Read docs for detailed examples

For help: See $INSTALL_DIR/docs/
EOF

    print_success "Quick start guide created"
    echo ""
}

# Display completion message
display_completion() {
    print_header "Installation Complete!"
    echo ""
    print_success "Claude Skills successfully installed!"
    echo ""
    echo "INSTALLATION SUMMARY:"
    echo "  Agents:   $(find "$CLAUDE_CODE_DIR/agents" -name "cs-*.md" 2>/dev/null | wc -l | xargs) installed to ~/.claude/agents/"
    echo "  Commands: $(ls "$CLAUDE_CODE_DIR/commands/"*.md 2>/dev/null | wc -l | xargs) installed to ~/.claude/commands/"
    echo "  Skills:   $(ls -d "$INSTALL_DIR/skills"/*/* 2>/dev/null | wc -l | xargs) installed to ~/.claude-skills/skills/"
    echo ""
    print_info "IMPORTANT: Restart VSCode to discover new agents"
    echo ""
    print_info "Next Steps:"
    echo "  1. RESTART VSCODE (required for agent discovery)"
    echo ""
    echo "  2. For Claude Code users:"
    echo "     - Type: @cs-product-manager to use an agent"
    echo "     - Type: /update.docs to use a command"
    echo ""
    echo "  3. For Claude AI users:"
    echo "     - Upload agents from: $INSTALL_DIR/agents/"
    echo "     - Upload skills as needed"
    echo ""
    echo "  4. View quick start guide:"
    echo "     cat $INSTALL_DIR/QUICK_START.txt"
    echo ""
    echo "  5. Explore installed agents:"
    echo "     ls ~/.claude/agents/"
    echo ""

    if [ -d "$BACKUP_DIR" ]; then
        print_info "Backup of previous installation:"
        echo "     $BACKUP_DIR"
        echo ""
    fi

    print_success "Happy coding with Claude Skills!"
    echo ""
}

# Main installation flow
main() {
    display_welcome
    check_prerequisites
    ask_questions
    confirm_installation
    backup_existing
    install_agents
    install_skills
    install_commands
    install_resources
    configure_claude_code
    create_quick_start
    display_completion
}

# Run main installation
main
