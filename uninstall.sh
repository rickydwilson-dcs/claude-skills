#!/bin/bash

# Claude Skills Uninstallation Script
# Version: 1.0.0
# Description: Safe removal of claude-skills installation

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Installation configuration
INSTALL_DIR="${HOME}/.claude-skills"
BACKUP_DIR="${HOME}/.claude-skills-uninstall-backup-$(date +%Y%m%d-%H%M%S)"

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

# Display welcome message
display_welcome() {
    clear
    print_header "Claude Skills Uninstallation"
    echo ""
    echo "This script will help you safely remove claude-skills from your system."
    echo ""
}

# Check if installation exists
check_installation() {
    print_header "Checking Installation"
    echo ""

    if [ -d "$INSTALL_DIR" ]; then
        print_success "Installation found: $INSTALL_DIR"

        # Count agents
        AGENT_COUNT=$(find "$INSTALL_DIR/agents" -name "cs-*.md" 2>/dev/null | wc -l | xargs)
        print_info "Agents installed: $AGENT_COUNT"

        # Calculate size
        SIZE=$(du -sh "$INSTALL_DIR" 2>/dev/null | awk '{print $1}')
        print_info "Disk space: $SIZE"
    else
        print_warning "No installation found at: $INSTALL_DIR"
        echo ""
        echo "Nothing to uninstall."
        exit 0
    fi

    echo ""
}

# Ask confirmation
confirm_uninstall() {
    print_header "Uninstall Options"
    echo ""
    echo "What would you like to do?"
    echo ""
    echo "1) Complete removal (delete everything)"
    echo "2) Create backup before removal"
    echo "3) Archive installation (move to backup location)"
    echo "4) Cancel uninstallation"
    echo ""
    read -p "Choose option (1-4) [2]: " UNINSTALL_OPTION
    UNINSTALL_OPTION=${UNINSTALL_OPTION:-2}

    if [ "$UNINSTALL_OPTION" = "4" ]; then
        echo ""
        echo "Uninstallation cancelled."
        exit 0
    fi

    echo ""

    if [ "$UNINSTALL_OPTION" = "1" ]; then
        print_warning "⚠️  WARNING: Complete removal will permanently delete all files!"
        print_warning "This cannot be undone."
        echo ""
        read -p "Are you absolutely sure? Type 'DELETE' to confirm: " CONFIRM

        if [ "$CONFIRM" != "DELETE" ]; then
            echo ""
            echo "Uninstallation cancelled."
            exit 0
        fi
    fi

    echo ""
}

# Create backup
create_backup() {
    if [ "$UNINSTALL_OPTION" = "2" ] || [ "$UNINSTALL_OPTION" = "3" ]; then
        print_header "Creating Backup"
        echo ""

        print_info "Backing up installation..."
        mkdir -p "$BACKUP_DIR"
        cp -r "$INSTALL_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true

        BACKUP_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | awk '{print $1}')
        print_success "Backup created: $BACKUP_DIR ($BACKUP_SIZE)"
        echo ""
    fi
}

# Remove installation
remove_installation() {
    if [ "$UNINSTALL_OPTION" = "1" ] || [ "$UNINSTALL_OPTION" = "2" ]; then
        print_header "Removing Installation"
        echo ""

        print_info "Removing: $INSTALL_DIR"
        rm -rf "$INSTALL_DIR"
        print_success "Installation removed"

        # Remove symlinks if they exist
        if [ -L "${HOME}/.claude-skills" ]; then
            rm -f "${HOME}/.claude-skills"
            print_success "Removed symlink: ${HOME}/.claude-skills"
        fi

        echo ""
    fi
}

# Archive installation
archive_installation() {
    if [ "$UNINSTALL_OPTION" = "3" ]; then
        print_header "Archiving Installation"
        echo ""

        ARCHIVE_DIR="${HOME}/claude-skills-archive-$(date +%Y%m%d-%H%M%S)"

        print_info "Moving installation to: $ARCHIVE_DIR"
        mv "$INSTALL_DIR" "$ARCHIVE_DIR"

        ARCHIVE_SIZE=$(du -sh "$ARCHIVE_DIR" 2>/dev/null | awk '{print $1}')
        print_success "Installation archived: $ARCHIVE_DIR ($ARCHIVE_SIZE)"

        echo ""
    fi
}

# Clean up VSCode/Claude Code references
cleanup_vscode() {
    print_header "Cleaning Up References"
    echo ""

    print_info "Checking for VSCode/Claude Code references..."

    # This is informational - actual cleanup depends on Claude Code extension
    print_info "Note: Claude Code agents are auto-discovered"
    print_info "Restart VSCode to refresh agent list"

    echo ""
}

# Display completion message
display_completion() {
    print_header "Uninstallation Complete"
    echo ""

    case $UNINSTALL_OPTION in
        1)
            print_success "Claude Skills completely removed from your system"
            ;;
        2)
            print_success "Claude Skills removed with backup"
            echo ""
            print_info "Backup location: $BACKUP_DIR"
            print_info "To restore: mv $BACKUP_DIR $INSTALL_DIR"
            ;;
        3)
            print_success "Claude Skills archived"
            echo ""
            print_info "Archive location: $(ls -d ~/claude-skills-archive-* 2>/dev/null | tail -1)"
            print_info "To restore: mv ~/claude-skills-archive-* $INSTALL_DIR"
            ;;
    esac

    echo ""
    print_info "Additional Cleanup Steps (Optional):"
    echo ""
    echo "  For Claude AI Users:"
    echo "  - Delete Projects containing agents from claude.ai"
    echo ""
    echo "  For Claude Code Users:"
    echo "  - Restart VSCode to refresh agent list"
    echo ""
    echo "  To reinstall:"
    echo "  - Run: ./install.sh"
    echo ""
}

# Main uninstallation flow
main() {
    display_welcome
    check_installation
    confirm_uninstall
    create_backup
    remove_installation
    archive_installation
    cleanup_vscode
    display_completion
}

# Run main uninstallation
main
