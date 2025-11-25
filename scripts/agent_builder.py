#!/usr/bin/env python3
"""
Agent Builder - Interactive CLI for creating cs-* agents

This tool automates agent creation with comprehensive validation,
template population, and catalog integration.

Usage:
    python agent_builder.py                        # Interactive mode
    python agent_builder.py --config config.yaml   # Config file mode
    python agent_builder.py --validate path.md     # Validation mode
    python agent_builder.py --help                 # Show help

ARCHITECTURE NOTE - Single-File Design:
    This script is intentionally monolithic (1,188 lines) for portability.
    Users can extract this single file and run it anywhere with Python 3.8+.
    This aligns with the repository's zero-dependency, portable-skills philosophy.

    Code is organized into logical sections for maintainability:

    SECTION 1: Configuration & Constants (Lines 15-38)
        - Exit codes, imports, global configuration

    SECTION 2: YAML Parsing Utilities (Lines 40-93)
        - simple_yaml_parse() - Standard library YAML parser
        - Handles basic YAML without external dependencies

    SECTION 3: Domain Management (Lines 94-179)
        - DomainManager class
        - Dynamic domain discovery and validation

    SECTION 4: Validation Logic (Lines 180-525)
        - AgentValidator class
        - 9+ validation checks for agent structure

    SECTION 5: Template Management (Lines 526-604)
        - TemplateLoader class
        - Template file loading and generation

    SECTION 6: Catalog Integration (Lines 605-660)
        - CatalogUpdater class
        - Updates docs/AGENTS_CATALOG.md automatically

    SECTION 7: Core Agent Builder (Lines 661-1133)
        - AgentBuilder class
        - Main orchestration logic

    SECTION 8: CLI Entry Point (Lines 1134-1188)
        - main() function
        - Argument parsing and mode selection
"""

# ============================================================================
# SECTION 1: CONFIGURATION & CONSTANTS
# ============================================================================
# Import statements, exit codes, and global configuration

import os
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Try to import PyYAML, provide fallback if not available
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    # Use simple YAML parser fallback (no external dependencies)


# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_FAILED = 1
EXIT_FILE_ERROR = 2
EXIT_CONFIG_ERROR = 3
EXIT_UNKNOWN_ERROR = 99


# ============================================================================
# SECTION 2: YAML PARSING UTILITIES
# ============================================================================
# Standard library YAML parser for agent frontmatter (zero dependencies)

def simple_yaml_parse(yaml_str: str) -> Dict:
    """
    Simple YAML parser for agent frontmatter (standard library only)

    Handles basic key-value pairs and lists.
    Does NOT support nested objects or complex YAML features.
    """
    result = {}
    current_key = None
    list_items = []

    for line in yaml_str.strip().split('\n'):
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        # List item
        if line.startswith('- '):
            item = line[2:].strip()
            list_items.append(item)
            continue

        # Key-value pair
        if ':' in line:
            # Save previous list if any
            if current_key and list_items:
                result[current_key] = list_items
                list_items = []

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Handle inline lists [item1, item2]
            if value.startswith('[') and value.endswith(']'):
                items = value[1:-1].split(',')
                result[key] = [item.strip() for item in items]
                current_key = None
            # Empty value - expect list on next lines
            elif not value:
                current_key = key
            # Simple value
            else:
                result[key] = value
                current_key = None

    # Save final list if any
    if current_key and list_items:
        result[current_key] = list_items

    return result


def ensure_session_tracking() -> Optional[str]:
    """
    Check if user is in an active session, offer to create one

    Returns:
        Session ID if active session exists, None otherwise
    """
    repo_root = Path(__file__).parent.parent
    current_session_file = repo_root / "output" / ".current-session"

    # Check if there's an active session
    if current_session_file.exists():
        try:
            session_id = current_session_file.read_text().strip()
            if session_id:
                return session_id
        except Exception:
            pass

    # No active session - offer to create one
    print("\n" + "="*60)
    print("SESSION TRACKING")
    print("="*60)
    print("No active session detected.")
    print("\nSession tracking helps:")
    print("  • Attribute work to specific initiatives")
    print("  • Preserve context for collaboration")
    print("  • Track decisions and changes over time")
    print("\nCreate a new session? (y/n): ", end="")

    try:
        response = input().strip().lower()
        if response in ('y', 'yes'):
            print("\nSession ID (e.g., 'feature-name' or press Enter to skip): ", end="")
            session_desc = input().strip()

            if session_desc:
                user = os.getenv('USER', 'unknown')
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                session_id = f"{timestamp}_{session_desc}"
                session_path = repo_root / "output" / "sessions" / user / session_id

                # Create session directory
                session_path.mkdir(parents=True, exist_ok=True)

                # Update current session pointer
                current_session_file.parent.mkdir(parents=True, exist_ok=True)
                current_session_file.write_text(f"{user}/{session_id}")

                print(f"\n✓ Created session: {session_id}")
                print(f"  Location: {session_path}")
                print("\nContinuing with agent creation...\n")
                return session_id
            else:
                print("\nSkipping session creation. Continuing with agent creation...\n")
        else:
            print("\nSkipping session creation. Continuing with agent creation...\n")
    except (KeyboardInterrupt, EOFError):
        print("\n\nSkipping session creation...\n")

    return None


# ============================================================================
# SECTION 3: DOMAIN MANAGEMENT
# ============================================================================
# Dynamic domain discovery and validation

class DomainManager:
    """Manage agent domains dynamically"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.agents_dir = repo_root / "agents"

    def get_existing_domains(self) -> List[str]:
        """Discover existing agent domains from file system"""
        if not self.agents_dir.exists():
            return []
        return [d.name for d in self.agents_dir.iterdir()
                if d.is_dir() and not d.name.startswith('.')]

    def validate_domain_format(self, domain: str) -> Tuple[bool, str]:
        """Validate domain name format (kebab-case, lowercase)"""
        pattern = r'^[a-z][a-z0-9-]*$'
        if not re.match(pattern, domain):
            return False, f"Domain must be lowercase kebab-case: {domain}"
        if len(domain) < 3:
            return False, f"Domain too short (min 3 chars): {domain}"
        if len(domain) > 30:
            return False, f"Domain too long (max 30 chars): {domain}"
        if '--' in domain:
            return False, f"Domain cannot have consecutive hyphens: {domain}"
        return True, "Valid domain format"

    def map_domain_to_skill_team(self, domain: str) -> str:
        """Map agent domain to skill team directory"""
        # Known exceptions
        DOMAIN_EXCEPTIONS = {
            'c-level': 'c-level-advisor',
        }

        if domain in DOMAIN_EXCEPTIONS:
            return DOMAIN_EXCEPTIONS[domain]

        # Default pattern: append '-team'
        return f"{domain}-team"

    def get_skill_teams_for_domain(self, domain: str) -> List[str]:
        """Find all skill teams that could map to this domain"""
        skill_team = self.map_domain_to_skill_team(domain)
        skills_dir = self.repo_root / "skills"

        if not skills_dir.exists():
            return []

        # Check if default mapping exists
        if (skills_dir / skill_team).exists():
            return [skill_team]

        # Search for similar names
        all_teams = [d.name for d in skills_dir.iterdir() if d.is_dir()]
        similar = [t for t in all_teams if domain in t or t in domain]

        return similar if similar else all_teams

    def create_domain_directory(self, domain: str) -> None:
        """Create new domain directory structure"""
        domain_path = self.agents_dir / domain
        domain_path.mkdir(parents=True, exist_ok=True)

        # Create CATALOG.md
        catalog_content = f"""# {domain.replace('-', ' ').title()} Agents

This directory contains agents for the {domain} domain.

## Agents

<!-- Agents will be listed here automatically by agent_builder.py -->

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Domain:** {domain}
**Agent Count:** 0
"""

        catalog_path = domain_path / "CATALOG.md"
        catalog_path.write_text(catalog_content)

        print(f"✅ Created: {domain_path}/")
        print(f"✅ Created: {catalog_path}")


# ============================================================================
# SECTION 4: VALIDATION LOGIC
# ============================================================================
# Comprehensive validation checks for agent structure and metadata

class AgentValidator:
    """Validation logic for agent files"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def validate_name(self, name: str) -> Tuple[bool, str]:
        """Validate agent name format (cs-[a-z0-9-]+)"""
        if not name.startswith('cs-'):
            return False, "Agent name must start with 'cs-'"

        if not re.match(r'^cs-[a-z0-9-]+$', name):
            return False, "Agent name must be kebab-case (lowercase, hyphens only)"

        if '--' in name:
            return False, "Agent name cannot have consecutive hyphens"

        if name.endswith('-'):
            return False, "Agent name cannot end with hyphen"

        return True, "Valid"

    def parse_yaml_frontmatter(self, content: str) -> Tuple[Optional[Dict], str, Optional[str]]:
        """
        Extract YAML frontmatter and content body

        Returns:
            (frontmatter_dict, markdown_body, error_message)
        """
        if not content.startswith('---'):
            return None, content, "No YAML frontmatter found"

        # Split at first and second ---
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, content, "Malformed YAML frontmatter"

        yaml_str = parts[1]
        body = parts[2]

        try:
            if YAML_AVAILABLE:
                frontmatter = yaml.safe_load(yaml_str)
            else:
                # Use simple parser fallback
                frontmatter = simple_yaml_parse(yaml_str)
            return frontmatter, body, None
        except Exception as e:
            return None, body, f"Invalid YAML syntax: {e}"

    def validate_yaml_frontmatter(self, content: str) -> Tuple[bool, str]:
        """Validate YAML frontmatter is present and valid"""
        frontmatter, body, error = self.parse_yaml_frontmatter(content)

        if error:
            return False, error

        if not frontmatter:
            return False, "Missing YAML frontmatter"

        # Required fields
        required = ['name', 'description', 'skills', 'domain', 'model', 'tools']
        for field in required:
            if field not in frontmatter:
                return False, f"Missing required YAML field: {field}"

        # Field validation
        if len(frontmatter['description']) > 150:
            return False, f"Description too long: {len(frontmatter['description'])} chars (max: 150)"

        if frontmatter['model'] not in ['sonnet', 'opus', 'haiku']:
            return False, f"Invalid model: {frontmatter['model']} (must be: sonnet, opus, haiku)"

        if not isinstance(frontmatter['tools'], list):
            return False, "Tools must be a list"

        valid_tools = ['Read', 'Write', 'Bash', 'Grep', 'Glob', 'Edit', 'NotebookEdit', 'WebFetch', 'WebSearch']
        for tool in frontmatter['tools']:
            if tool not in valid_tools:
                return False, f"Invalid tool: {tool}"

        # Optional fields validation
        if 'color' in frontmatter:
            valid_colors = ['blue', 'green', 'red', 'purple', 'orange']
            if frontmatter['color'] not in valid_colors:
                return False, f"Invalid color: {frontmatter['color']} (must be: {', '.join(valid_colors)})"

        if 'field' in frontmatter:
            valid_fields = ['quality', 'frontend', 'backend', 'fullstack', 'product', 'architecture',
                          'testing', 'devops', 'data', 'ai', 'security', 'performance', 'design',
                          'research', 'content', 'finance', 'agile', 'tools']
            if frontmatter['field'] not in valid_fields:
                return False, f"Invalid field: {frontmatter['field']} (must be one of: {', '.join(valid_fields)})"

        if 'expertise' in frontmatter:
            valid_expertise = ['beginner', 'intermediate', 'expert']
            if frontmatter['expertise'] not in valid_expertise:
                return False, f"Invalid expertise: {frontmatter['expertise']} (must be: {', '.join(valid_expertise)})"

        if 'execution' in frontmatter:
            valid_execution = ['parallel', 'coordinated', 'sequential']
            if frontmatter['execution'] not in valid_execution:
                return False, f"Invalid execution: {frontmatter['execution']} (must be: {', '.join(valid_execution)})"

        if 'mcp_tools' in frontmatter:
            if not isinstance(frontmatter['mcp_tools'], list):
                return False, "mcp_tools must be a list"

        return True, "Valid"

    def validate_relative_paths(self, agent_path: Path, content: str) -> Tuple[bool, List[str]]:
        """Validate all ../../ paths resolve correctly from agent location"""
        agent_dir = agent_path.parent
        errors = []

        # Extract all relative paths (../../...)
        path_pattern = r'\.\./\.\./[a-zA-Z0-9_/-]+(?:\.[a-zA-Z]+)?'
        paths = re.findall(path_pattern, content)

        for rel_path in set(paths):  # Remove duplicates
            # Resolve from agent directory
            absolute_path = (agent_dir / rel_path).resolve()

            if not absolute_path.exists():
                errors.append(f"Path does not exist: {rel_path}")

        return len(errors) == 0, errors

    def validate_skill_integration(self, agent_path: Path, content: str) -> Tuple[bool, str]:
        """Validate skill package exists and has required files"""
        # Extract frontmatter
        frontmatter, _, error = self.parse_yaml_frontmatter(content)
        if error or not frontmatter:
            return False, "Cannot validate skill integration: invalid frontmatter"

        skill_spec = frontmatter.get('skills', '')
        domain = frontmatter.get('domain', '')

        # Handle both formats:
        # 1. Just skill name: "content-creator"
        # 2. Full path: "marketing-skill/content-creator" or "marketing-team/content-creator"
        if '/' in skill_spec:
            # Full path provided - use as-is
            skill_path = self.repo_root / 'skills' / skill_spec
        else:
            # Just skill name - construct path
            domain_manager = DomainManager(self.repo_root)
            team = domain_manager.map_domain_to_skill_team(domain)
            skill_path = self.repo_root / 'skills' / team / skill_spec

        if not skill_path.exists():
            return False, f"Skill not found: {skill_path.relative_to(self.repo_root)}/"

        # Check required files
        skill_md = skill_path / 'SKILL.md'
        if not skill_md.exists():
            return False, f"Missing SKILL.md in {skill_path.name}"

        scripts_dir = skill_path / 'scripts'
        if not scripts_dir.exists():
            return False, f"Missing scripts/ directory in {skill_path.name}"

        return True, "Valid"

    def validate_workflows(self, content: str) -> Tuple[bool, str]:
        """Ensure minimum 3 workflows documented"""
        # Count workflow sections (### Workflow N:)
        workflow_pattern = r'###\s+Workflow\s+\d+:'
        workflows = re.findall(workflow_pattern, content)

        if len(workflows) < 3:
            return False, f"Only {len(workflows)} workflows documented (minimum: 3)"

        return True, f"Valid ({len(workflows)} workflows)"

    def validate_integration_examples(self, content: str) -> Tuple[bool, str]:
        """Ensure integration examples present"""
        # Count examples in Integration Examples section
        sections = content.split('## Integration Examples')
        if len(sections) < 2:
            return False, "Integration Examples section not found"

        # Get content until next H2 section (^##\s at start of line)
        examples_section = sections[1]
        # Find next section starting with ## at beginning of line
        next_section_match = re.search(r'\n##\s', examples_section)
        if next_section_match:
            examples_section = examples_section[:next_section_match.start()]

        # Count examples (### Example N:)
        example_pattern = r'###\s+Example\s+\d+:'
        examples = re.findall(example_pattern, examples_section)

        if len(examples) < 2:
            return False, f"Only {len(examples)} integration examples found (minimum: 2)"

        return True, f"Valid ({len(examples)} examples)"

    def validate_success_metrics(self, content: str) -> Tuple[bool, str]:
        """Ensure success metrics defined"""
        if '## Success Metrics' not in content:
            return False, "Success Metrics section not found"

        sections = content.split('## Success Metrics')
        if len(sections) < 2:
            return False, "Success Metrics section is empty"

        # Get content until next H2 section
        metrics_section = sections[1]
        next_section_match = re.search(r'\n##\s', metrics_section)
        if next_section_match:
            metrics_section = metrics_section[:next_section_match.start()]

        # Count metric categories (lines starting with **)
        categories = [line for line in metrics_section.split('\n')
                     if line.strip().startswith('**') and line.strip().endswith(':**')]

        if len(categories) < 3:
            return False, f"Only {len(categories)} metric categories found (minimum: 3)"

        return True, f"Valid ({len(categories)} metric categories)"

    def validate_markdown_structure(self, content: str) -> Tuple[bool, str]:
        """Validate required markdown sections present"""
        required_sections = [
            '## Purpose',
            '## Skill Integration',
            '## Workflows',
            '## Success Metrics'
        ]

        missing = []
        for section in required_sections:
            if section not in content:
                missing.append(section)

        if missing:
            return False, f"Missing sections: {', '.join(missing)}"

        return True, "Valid"

    def validate_cross_references(self, content: str) -> Tuple[bool, str]:
        """Validate cross-references section exists"""
        if '## References' not in content and '## Related Agents' not in content:
            return False, "Missing References or Related Agents section"

        return True, "Valid"

    def run_all_checks(self, agent_path: Path) -> Dict:
        """Run all validation checks and return results"""
        if not agent_path.exists():
            return {
                'status': 'failed',
                'checks_passed': 0,
                'checks_total': 9,
                'error': f"Agent file not found: {agent_path}"
            }

        content = agent_path.read_text()

        checks = []

        # Check 1: Name format
        agent_name = agent_path.stem
        valid, msg = self.validate_name(agent_name)
        checks.append({
            'name': 'name_format',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 2: YAML frontmatter
        valid, msg = self.validate_yaml_frontmatter(content)
        checks.append({
            'name': 'yaml_frontmatter',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 3: Relative paths
        valid, errors = self.validate_relative_paths(agent_path, content)
        checks.append({
            'name': 'relative_paths',
            'status': 'passed' if valid else 'failed',
            'message': f"Valid ({len(set(re.findall(r'\.\./\.\./[a-zA-Z0-9_/-]+(?:\.[a-zA-Z]+)?', content)))} paths checked)" if valid else f"Errors: {', '.join(errors)}"
        })

        # Check 4: Skill integration
        valid, msg = self.validate_skill_integration(agent_path, content)
        checks.append({
            'name': 'skill_integration',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 5: Workflows
        valid, msg = self.validate_workflows(content)
        checks.append({
            'name': 'workflows',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 6: Integration examples
        valid, msg = self.validate_integration_examples(content)
        checks.append({
            'name': 'integration_examples',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 7: Success metrics
        valid, msg = self.validate_success_metrics(content)
        checks.append({
            'name': 'success_metrics',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 8: Markdown structure
        valid, msg = self.validate_markdown_structure(content)
        checks.append({
            'name': 'markdown_structure',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        # Check 9: Cross-references
        valid, msg = self.validate_cross_references(content)
        checks.append({
            'name': 'cross_references',
            'status': 'passed' if valid else 'failed',
            'message': msg
        })

        checks_passed = sum(1 for c in checks if c['status'] == 'passed')

        return {
            'agent': agent_name,
            'status': 'passed' if checks_passed == len(checks) else 'failed',
            'checks_passed': checks_passed,
            'checks_total': len(checks),
            'checks': checks
        }


# ============================================================================
# SECTION 5: TEMPLATE MANAGEMENT
# ============================================================================
# Template file loading and content generation

class TemplateLoader:
    """Load and populate agent template"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.template_path = repo_root / "templates" / "agent-template.md"

    def load_template(self) -> str:
        """Load agent-template.md"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        return self.template_path.read_text()

    def populate_template(self, config: Dict) -> str:
        """Replace placeholders with actual values"""
        template = self.load_template()

        # Build YAML frontmatter with optional fields
        yaml_lines = [
            '---',
            f"name: {config['name']}",
            f"description: {config['description']}",
            f"skills: {config['skills']}",
            f"domain: {config['domain']}",
            f"model: {config['model']}",
            f"tools: {config['tools']}"
        ]

        # Add optional fields if present
        if 'color' in config:
            yaml_lines.append(f"color: {config['color']}")

        if 'field' in config:
            yaml_lines.append(f"field: {config['field']}")

        if 'expertise' in config:
            yaml_lines.append(f"expertise: {config['expertise']}")

        if 'execution' in config:
            yaml_lines.append(f"execution: {config['execution']}")

        if 'mcp_tools' in config and config['mcp_tools']:
            yaml_lines.append(f"mcp_tools: {config['mcp_tools']}")

        yaml_lines.append('---')
        yaml_section = '\n'.join(yaml_lines)

        # Replace first YAML block
        template = re.sub(
            r'^---\n.*?---',
            yaml_section,
            template,
            count=1,
            flags=re.DOTALL | re.MULTILINE
        )

        # Replace agent name placeholders
        agent_title = config['name'].replace('cs-', '').replace('-', ' ').title()
        template = template.replace('# Agent Name', f"# {agent_title}")
        template = template.replace('cs-agent-name', config['name'])

        # Replace domain references
        domain_manager = DomainManager(self.repo_root)
        skill_team = domain_manager.map_domain_to_skill_team(config['domain'])

        template = template.replace('domain-skill/skill-name', f"skills/{skill_team}/{config['skills']}")
        template = template.replace('../../domain-skill/skill-name/', f"../../skills/{skill_team}/{config['skills']}/")

        # Add metadata at bottom
        today = datetime.now().strftime('%Y-%m-%d')
        template = re.sub(
            r'\*\*Last Updated:\*\* \[Date\]',
            f"**Last Updated:** {today}",
            template
        )

        return template


# ============================================================================
# SECTION 6: CATALOG INTEGRATION
# ============================================================================
# Updates docs/AGENTS_CATALOG.md with new agent entries

class CatalogUpdater:
    """Update agent catalogs"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def append_to_catalog(self, domain: str, name: str, description: str) -> None:
        """Append entry to domain catalog"""
        catalog_path = self.repo_root / "agents" / domain / "CATALOG.md"

        if not catalog_path.exists():
            print(f"⚠️  Warning: {catalog_path} not found")
            return

        # Read existing catalog
        content = catalog_path.read_text()

        # Generate entry
        entry = f"- [{name}]({name}.md) - {description}\n"

        # Find insertion point (end of agent list)
        lines = content.split('\n')
        insert_index = -1

        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith('- [cs-'):
                insert_index = i + 1
                break

        if insert_index == -1:
            # No existing agents, insert after "## Agents" heading
            for i, line in enumerate(lines):
                if 'Agents' in line and line.startswith('##'):
                    insert_index = i + 2  # Skip heading and blank line
                    break

        if insert_index == -1:
            insert_index = len(lines)

        # Insert entry
        lines.insert(insert_index, entry.rstrip('\n'))

        # Write back
        catalog_path.write_text('\n'.join(lines))

        print(f"✓ Updated {catalog_path}")

    def verify_catalog_format(self, catalog_path: Path) -> bool:
        """Validate catalog markdown format"""
        if not catalog_path.exists():
            return False

        content = catalog_path.read_text()
        return '## Agents' in content or '##' in content


# ============================================================================
# SECTION 7: CORE AGENT BUILDER
# ============================================================================
# Main orchestration logic for agent creation and validation

class AgentBuilder:
    """Main orchestrator for agent creation"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.validator = AgentValidator(repo_root)
        self.template_loader = TemplateLoader(repo_root)
        self.catalog_updater = CatalogUpdater(repo_root)
        self.domain_manager = DomainManager(repo_root)

    def interactive_mode(self) -> None:
        """Run interactive agent creation workflow"""
        print("🤖 Agent Builder")
        print("=" * 50)
        print()

        # Step 1: Agent Name
        print("Step 1/8: Agent Name")
        print("-" * 50)
        print("Enter agent name (kebab-case with cs- prefix):")
        print("Example: cs-data-analyst, cs-backend-engineer")
        print()

        while True:
            name = input("Name: ").strip()
            valid, msg = self.validator.validate_name(name)
            if valid:
                print(f"✓ Valid name format")
                break
            else:
                print(f"❌ {msg}")
                print("Try again:")

        print()

        # Step 2: Domain Selection
        print("Step 2/8: Domain")
        print("-" * 50)

        existing_domains = self.domain_manager.get_existing_domains()
        print("Select domain:")
        for idx, domain in enumerate(existing_domains, 1):
            # Count agents in domain
            agent_count = len(list((self.repo_root / "agents" / domain).glob("cs-*.md")))
            print(f"{idx}. {domain} ({agent_count} agents)")
        print(f"{len(existing_domains) + 1}. Create new domain")
        print()

        while True:
            choice = input(f"Domain (1-{len(existing_domains) + 1}): ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(existing_domains):
                domain = existing_domains[int(choice) - 1]
                print(f"✓ Domain: {domain}")
                break
            elif choice.isdigit() and int(choice) == len(existing_domains) + 1:
                domain = self.create_new_domain_interactive()
                break
            else:
                print("❌ Invalid selection")

        print()

        # Step 3: Description
        print("Step 3/8: Description")
        print("-" * 50)
        print("Enter one-line description (under 150 chars):")
        print('Example: "Data analysis and reporting for product decisions"')
        print()

        while True:
            description = input("Description: ").strip()
            if len(description) <= 150:
                print(f"✓ Length: {len(description)} chars")
                break
            else:
                print(f"❌ Description too long: {len(description)} chars (max: 150)")

        print()

        # Step 4: Skills Integration
        print("Step 4/8: Skills Integration")
        print("-" * 50)

        skill_team = self.domain_manager.map_domain_to_skill_team(domain)
        skills_path = self.repo_root / "skills" / skill_team

        if skills_path.exists():
            available_skills = [d.name for d in skills_path.iterdir()
                              if d.is_dir() and not d.name.startswith('.')]

            if available_skills:
                print(f"Available skills in {skill_team}:")
                for skill in available_skills:
                    print(f"  - {skill}")
                print()

        print(f"Enter skill folder name (from skills/{skill_team}/):")
        print("Example: data-analyst-toolkit, senior-architect")
        print()

        while True:
            skills = input("Skills: ").strip()
            skill_path = self.repo_root / "skills" / skill_team / skills

            if skill_path.exists():
                # Count Python tools
                scripts_dir = skill_path / "scripts"
                if scripts_dir.exists():
                    tool_count = len(list(scripts_dir.glob("*.py")))
                    print(f"✓ Skill exists: skills/{skill_team}/{skills}/")
                    print(f"✓ Found {tool_count} Python tools")
                    break
                else:
                    print(f"⚠️  Skill exists but has no scripts/ directory")
                    confirm = input("Continue anyway? (y/n): ").strip().lower()
                    if confirm == 'y':
                        break
            else:
                print(f"❌ Skill not found: skills/{skill_team}/{skills}/")
                print("Try again:")

        print()

        # Step 5: Model Selection
        print("Step 5/8: Model Selection")
        print("-" * 50)
        print("Select model:")
        print("1. sonnet (recommended - balanced performance)")
        print("2. opus (complex reasoning)")
        print("3. haiku (fast, simple tasks)")
        print()

        models = ['sonnet', 'opus', 'haiku']
        while True:
            choice = input("Model (1-3): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= 3:
                model = models[int(choice) - 1]
                print(f"✓ Model: {model}")
                break
            else:
                print("❌ Invalid selection")

        print()

        # Step 6: Tools Selection
        print("Step 6/8: Tools Selection")
        print("-" * 50)
        print("Select tools (comma-separated):")
        print("Available: Read, Write, Bash, Grep, Glob, Edit, NotebookEdit")
        print()
        print("Default: Read, Write, Bash, Grep, Glob")

        tools_input = input("Tools (Enter for default): ").strip()

        if tools_input:
            tools = [t.strip() for t in tools_input.split(',')]
        else:
            tools = ['Read', 'Write', 'Bash', 'Grep', 'Glob']

        print(f"✓ Tools: {tools}")
        print()

        # Step 7: Agent Type Classification
        print("Step 7/8: Agent Type Classification (Optional)")
        print("-" * 50)
        print("Configure agent type metadata for resource management and execution patterns.")
        print()

        # Determine intelligent defaults based on domain and tools
        default_color = 'blue'  # Strategic by default
        default_field = None
        default_expertise = 'intermediate'
        default_execution = 'coordinated'

        # Suggest field based on domain
        domain_to_field = {
            'engineering': 'backend',
            'product': 'product',
            'marketing': 'content',
            'c-level': 'architecture',
            'delivery': 'coordination'
        }
        if domain in domain_to_field:
            default_field = domain_to_field[domain]

        # Adjust defaults based on tools
        if 'Bash' in tools and len(tools) >= 5:
            default_color = 'green'  # Implementation agent
            default_execution = 'coordinated'
        elif 'Bash' in tools and 'Edit' in tools:
            default_color = 'red'  # Quality agent (heavy Bash usage)
            default_execution = 'sequential'
        elif len(tools) <= 3:
            default_color = 'blue'  # Strategic agent (minimal tools)
            default_execution = 'parallel'

        print(f"1. Color (agent type): blue=Strategic, green=Implementation, red=Quality, purple=Coordination")
        print(f"   Default: {default_color}")
        color_input = input(f"   Color (Enter for default): ").strip().lower()
        color = color_input if color_input in ['blue', 'green', 'red', 'purple', 'orange'] else default_color

        print()
        print(f"2. Field (specialization): quality, frontend, backend, fullstack, product, architecture,")
        print(f"                          testing, devops, data, ai, security, performance, design,")
        print(f"                          research, content, finance, agile, tools")
        if default_field:
            print(f"   Default: {default_field}")
            field_input = input(f"   Field (Enter for default): ").strip().lower()
            field = field_input if field_input else default_field
        else:
            field_input = input(f"   Field (Enter to skip): ").strip().lower()
            field = field_input if field_input else None

        print()
        print(f"3. Expertise level: beginner, intermediate, expert")
        print(f"   Default: {default_expertise}")
        expertise_input = input(f"   Expertise (Enter for default): ").strip().lower()
        expertise = expertise_input if expertise_input in ['beginner', 'intermediate', 'expert'] else default_expertise

        print()
        print(f"4. Execution pattern: parallel (4-5 agents), coordinated (2-3 agents), sequential (1 agent)")
        print(f"   Default: {default_execution}")
        execution_input = input(f"   Execution (Enter for default): ").strip().lower()
        execution = execution_input if execution_input in ['parallel', 'coordinated', 'sequential'] else default_execution

        print()
        print(f"5. MCP Tools (comma-separated, e.g., github, playwright, atlassian)")
        mcp_input = input(f"   MCP Tools (Enter to skip): ").strip()
        mcp_tools = [t.strip() for t in mcp_input.split(',')] if mcp_input else []

        print()
        print("✓ Agent type classification configured:")
        print(f"  Color: {color}")
        if field:
            print(f"  Field: {field}")
        print(f"  Expertise: {expertise}")
        print(f"  Execution: {execution}")
        if mcp_tools:
            print(f"  MCP Tools: {mcp_tools}")
        print()

        # Step 8: Preview and Confirm
        print("Step 8/8: Preview")
        print("-" * 50)
        print("Review your agent configuration:")
        print()
        print(f"Name:        {name}")
        print(f"Domain:      {domain}")
        print(f"Description: {description}")
        print(f"Skills:      {skills}")
        print(f"Model:       {model}")
        print(f"Tools:       {tools}")
        print(f"Color:       {color}")
        if field:
            print(f"Field:       {field}")
        print(f"Expertise:   {expertise}")
        print(f"Execution:   {execution}")
        if mcp_tools:
            print(f"MCP Tools:   {mcp_tools}")
        print()
        print("Files to create:")
        print(f"- agents/{domain}/{name}.md")
        print()
        print("Catalog updates:")
        print(f"- agents/{domain}/CATALOG.md (append)")
        print()

        confirm = input("Proceed? (y/n): ").strip().lower()

        if confirm != 'y':
            print("❌ Agent creation cancelled")
            sys.exit(0)

        # Generate agent
        config = {
            'name': name,
            'domain': domain,
            'description': description,
            'skills': skills,
            'model': model,
            'tools': tools,
            'color': color,
            'expertise': expertise,
            'execution': execution
        }

        # Add optional field if provided
        if field:
            config['field'] = field

        # Add MCP tools if provided
        if mcp_tools:
            config['mcp_tools'] = mcp_tools

        self.generate_agent(config)

    def create_new_domain_interactive(self) -> str:
        """Interactive workflow for creating a new domain"""
        print()
        print("🆕 Create New Domain")
        print("-" * 50)
        print("Domain names should be:")
        print("  • Lowercase kebab-case (e.g., 'sales-ops', 'finance')")
        print("  • Descriptive and concise (3-30 chars)")
        print("  • Represent a functional area")
        print()
        print("Examples: sales, finance, operations, c-level, customer-success")
        print()

        while True:
            domain = input("New domain name: ").strip().lower()

            # Validate format
            valid, message = self.domain_manager.validate_domain_format(domain)
            if not valid:
                print(f"❌ {message}")
                continue

            # Check for conflicts
            existing = self.domain_manager.get_existing_domains()
            if domain in existing:
                print(f"❌ Domain '{domain}' already exists")
                continue

            # Confirm creation
            print(f"\n✓ Domain format valid: {domain}")
            print(f"\nThis will create:")
            print(f"  • agents/{domain}/ directory")
            print(f"  • agents/{domain}/CATALOG.md file")
            print()

            confirm = input("Create this domain? (y/n): ").strip().lower()

            if confirm == 'y':
                self.domain_manager.create_domain_directory(domain)
                return domain
            else:
                print("❌ Domain creation cancelled")
                continue

    def config_mode(self, config_path: str) -> None:
        """Create agent from config file"""
        config_file = Path(config_path)

        if not config_file.exists():
            print(f"❌ Config file not found: {config_path}")
            sys.exit(EXIT_CONFIG_ERROR)

        try:
            with open(config_file, 'r') as f:
                yaml_content = f.read()

            if YAML_AVAILABLE:
                config = yaml.safe_load(yaml_content)
            else:
                # Use simple parser fallback
                config = simple_yaml_parse(yaml_content)
        except Exception as e:
            print(f"❌ Invalid YAML config: {e}")
            sys.exit(EXIT_CONFIG_ERROR)

        # Validate required fields
        required = ['name', 'domain', 'description', 'skills', 'model', 'tools']
        missing = [f for f in required if f not in config]

        if missing:
            print(f"❌ Missing required fields in config: {', '.join(missing)}")
            sys.exit(EXIT_CONFIG_ERROR)

        # Set defaults for optional fields if not provided
        if 'color' not in config:
            config['color'] = 'blue'
        if 'expertise' not in config:
            config['expertise'] = 'intermediate'
        if 'execution' not in config:
            config['execution'] = 'coordinated'
        if 'mcp_tools' not in config:
            config['mcp_tools'] = []

        # Generate agent
        self.generate_agent(config)

    def validate_existing(self, agent_path: str) -> None:
        """Validate an existing agent file"""
        path = Path(agent_path)

        print(f"✅ Validating: {agent_path}")
        print()

        result = self.validator.run_all_checks(path)

        if 'error' in result:
            print(f"❌ {result['error']}")
            sys.exit(EXIT_VALIDATION_FAILED)

        # Print results
        for check in result['checks']:
            status_icon = "✓" if check['status'] == 'passed' else "✗"
            print(f"{status_icon} {check['name'].replace('_', ' ').title()}: {check['message']}")

        print()

        if result['status'] == 'passed':
            print(f"🎉 Validation passed: {result['checks_passed']}/{result['checks_total']} checks")
            sys.exit(EXIT_SUCCESS)
        else:
            print(f"❌ Validation failed: {result['checks_passed']}/{result['checks_total']} checks passed")
            sys.exit(EXIT_VALIDATION_FAILED)

    def generate_agent(self, config: Dict) -> None:
        """Generate agent file and update catalogs"""
        # Pre-generation validation
        print()
        print("Validating configuration...")

        # Validate name
        valid, msg = self.validator.validate_name(config['name'])
        if not valid:
            print(f"❌ Invalid name: {msg}")
            sys.exit(EXIT_VALIDATION_FAILED)

        # Check if agent already exists
        agent_path = self.repo_root / "agents" / config['domain'] / f"{config['name']}.md"
        if agent_path.exists():
            print(f"❌ Agent already exists: {agent_path}")
            sys.exit(EXIT_FILE_ERROR)

        # Generate from template
        print("Generating agent from template...")
        try:
            content = self.template_loader.populate_template(config)
        except Exception as e:
            print(f"❌ Template generation failed: {e}")
            sys.exit(EXIT_UNKNOWN_ERROR)

        # Write agent file
        print("Writing agent file...")
        try:
            agent_path.parent.mkdir(parents=True, exist_ok=True)
            agent_path.write_text(content)
            print(f"✓ Created: {agent_path}")
        except Exception as e:
            print(f"❌ Failed to write agent file: {e}")
            sys.exit(EXIT_FILE_ERROR)

        # Update catalog
        print("Updating catalog...")
        try:
            self.catalog_updater.append_to_catalog(
                config['domain'],
                config['name'],
                config['description']
            )
        except Exception as e:
            print(f"⚠️  Warning: Catalog update failed: {e}")

        # Success!
        print()
        print("✅ Agent created successfully!")
        print()
        print(f"📁 Location: {agent_path}")
        print()
        print("📝 Next steps:")
        print("   1. Review workflows and customize examples")
        print(f"   2. Test relative paths: ../../skills/{self.domain_manager.map_domain_to_skill_team(config['domain'])}/{config['skills']}/")
        print("   3. Add integration examples")
        print("   4. Commit changes:")
        print(f"      git add {agent_path}")
        print(f'      git commit -m "feat(agents): implement {config["name"]}"')
        print()


# ============================================================================
# SECTION 8: CLI ENTRY POINT
# ============================================================================
# Command-line argument parsing and mode selection

def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="Agent Builder - Interactive CLI for creating cs-* agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Interactive mode
  %(prog)s --config agent-config.yaml   # Config file mode
  %(prog)s --validate agents/engineering/cs-architect.md  # Validation mode
  %(prog)s --help                       # Show this help

For more information, see docs/USAGE.md
        """
    )

    parser.add_argument(
        '--config',
        help='Config file path (YAML format)'
    )

    parser.add_argument(
        '--validate',
        help='Validate existing agent file'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be created without writing files'
    )

    args = parser.parse_args()

    # Detect repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Initialize builder
    builder = AgentBuilder(repo_root)

    # Route to appropriate mode
    if args.validate:
        builder.validate_existing(args.validate)
    elif args.config:
        if args.dry_run:
            print("Dry run mode not yet implemented")
            sys.exit(EXIT_SUCCESS)
        builder.config_mode(args.config)
    else:
        builder.interactive_mode()


if __name__ == "__main__":
    main()
