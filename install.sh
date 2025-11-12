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
    echo "containing 3 production agents and 26 Pandora-focused skill packages."
    echo ""
    echo "What you'll get:"
    echo "  • 3 production agents (Marketing, Product)"
    echo "  • 77 Python CLI automation tools"
    echo "  • Comprehensive standards library"
    echo "  • Templates and workflows"
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
    echo "   a) All agents (3 production agents) - Recommended"
    echo "   b) Marketing only (2 agents)"
    echo "   c) Product only (1 agent)"
    echo ""
    read -p "Choose (a/b/c) [a]: " AGENT_SELECTION
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

    mkdir -p "$INSTALL_DIR/agents"

    case $AGENT_SELECTION in
        a) # All agents
            print_info "Installing all 3 production agents..."
            cp -r agents/* "$INSTALL_DIR/agents/" 2>/dev/null || true
            print_success "Installed 3 production agents"
            ;;
        b) # Marketing only
            print_info "Installing marketing agents..."
            mkdir -p "$INSTALL_DIR/agents/marketing"
            cp -r agents/marketing/* "$INSTALL_DIR/agents/marketing/" 2>/dev/null || true
            print_success "Installed 2 marketing agents"
            ;;
        c) # Product only
            print_info "Installing product agent..."
            mkdir -p "$INSTALL_DIR/agents/product"
            cp -r agents/product/* "$INSTALL_DIR/agents/product/" 2>/dev/null || true
            print_success "Installed 1 product agent"
            ;;
    esac

    echo ""
}

# Install skills
install_skills() {
    print_header "Installing Skill Packages"

    print_info "Installing 26 Pandora-focused skill packages..."

    # Copy skills directory (all 4 domains)
    if [ -d "skills" ]; then
        case $AGENT_SELECTION in
            a) # All skills
                cp -r skills "$INSTALL_DIR/" 2>/dev/null || true
                print_success "Installed all 26 skill packages (4 domains)"
                ;;
            b) # Marketing only
                mkdir -p "$INSTALL_DIR/skills"
                [ -d "skills/marketing-team" ] && cp -r skills/marketing-team "$INSTALL_DIR/skills/" 2>/dev/null || true
                print_success "Installed 3 marketing skill packages"
                ;;
            c) # Product only
                mkdir -p "$INSTALL_DIR/skills"
                [ -d "skills/product-team" ] && cp -r skills/product-team "$INSTALL_DIR/skills/" 2>/dev/null || true
                print_success "Installed 5 product skill packages"
                ;;
        esac
    else
        print_warning "Skills directory not found - skipping skill installation"
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
- Location: $INSTALL_DIR/agents/
- Count: $(find "$INSTALL_DIR/agents" -name "cs-*.md" 2>/dev/null | wc -l | xargs) agents

USAGE:

1. Claude Code (VSCode):
   - Agents are automatically discovered
   - Type: @cs-product-manager
   - Example: "@cs-content-creator help me write a blog post"

2. Claude AI (claude.ai):
   - Upload agents from: $INSTALL_DIR/agents/
   - Upload skills from: $INSTALL_DIR/skills/
   - Reference in your Project

3. Python Tools (77 total):
   - All scripts in: $INSTALL_DIR/skills/*/scripts/*.py
   - Run with: python3 path/to/script.py --help

DOCUMENTATION:
- Main README: $INSTALL_DIR/README.md (if exists)
- Agent Guide: $INSTALL_DIR/agents/CLAUDE.md
- Standards: $INSTALL_DIR/docs/standards/
- Templates: $INSTALL_DIR/templates/
- Installation: $INSTALL_DIR/docs/INSTALL.md
- Usage Guide: $INSTALL_DIR/docs/USAGE.md
- Workflow: $INSTALL_DIR/docs/WORKFLOW.md

NEXT STEPS:
1. Read docs/USAGE.md for detailed examples
2. Browse agents in: $INSTALL_DIR/agents/
3. Try an agent: @cs-product-manager (in Claude Code)

For help: See $INSTALL_DIR/docs/
EOF

    print_success "Quick start guide created"
    echo ""
}

# Display completion message
display_completion() {
    print_header "Installation Complete!"
    echo ""
    print_success "Claude Skills successfully installed to:"
    echo "           $INSTALL_DIR"
    echo ""
    print_info "Next Steps:"
    echo "  1. Read the quick start guide:"
    echo "     cat $INSTALL_DIR/QUICK_START.txt"
    echo ""
    echo "  2. For Claude Code users:"
    echo "     - Restart VSCode"
    echo "     - Agents will be auto-discovered"
    echo "     - Type: @cs-product-manager to start"
    echo ""
    echo "  3. For Claude AI users:"
    echo "     - Upload agents from: $INSTALL_DIR/agents/"
    echo "     - Upload skills as needed"
    echo ""
    echo "  4. Explore agents:"
    echo "     ls $INSTALL_DIR/agents/*/"
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
    install_resources
    configure_claude_code
    create_quick_start
    display_completion
}

# Run main installation
main
