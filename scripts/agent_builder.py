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

# Validation limits
MAX_DESCRIPTION_LENGTH = 300       # Maximum description length in YAML
MAX_DESCRIPTION_INPUT = 150        # Maximum for interactive input (user-friendly)
MAX_TITLE_LENGTH = 100             # Maximum title length


# ============================================================================
# SECTION 2: YAML PARSING UTILITIES
# ============================================================================
# Standard library YAML parser for agent frontmatter (zero dependencies)

def simple_yaml_parse(yaml_str: str) -> Dict:
    """
    Simple YAML parser for agent frontmatter (standard library only)

    Handles:
    - Basic key-value pairs
    - Lists (both inline [...] and multi-line with -)
    - Single-level nested objects (like stats, classification, dependencies)

    Does NOT support deeply nested structures (3+ levels).
    """
    result: Dict = {}
    current_key: Optional[str] = None
    current_dict: Optional[Dict] = None
    list_items: List = []
    lines = yaml_str.strip().split('\n')

    i = 0
    while i < len(lines):
        raw_line = lines[i]
        stripped = raw_line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            i += 1
            continue

        # Calculate indentation (2 spaces = 1 level)
        indent = len(raw_line) - len(raw_line.lstrip())
        is_indented = indent >= 2

        # List item (either top-level or nested)
        if stripped.startswith('- '):
            item = stripped[2:].strip()
            # Handle list item with nested dict (- title: "...", etc.)
            if ':' in item and not item.startswith('"') and not item.startswith("'"):
                # This is a dict item in a list (like examples)
                dict_item = {}
                key, value = item.split(':', 1)
                dict_item[key.strip()] = value.strip().strip('"\'')
                # Look ahead for more keys in this dict item
                j = i + 1
                while j < len(lines):
                    next_raw = lines[j]
                    next_stripped = next_raw.strip()
                    next_indent = len(next_raw) - len(next_raw.lstrip())
                    # Same or deeper indent and has key-value
                    if next_indent >= indent + 2 and ':' in next_stripped and not next_stripped.startswith('-'):
                        k, v = next_stripped.split(':', 1)
                        dict_item[k.strip()] = v.strip().strip('"\'')
                        j += 1
                    else:
                        break
                list_items.append(dict_item)
                i = j
                continue
            else:
                list_items.append(item)
            i += 1
            continue

        # Key-value pair
        if ':' in stripped:
            # Save previous collection if any
            if current_key and list_items:
                result[current_key] = list_items
                list_items = []
            if current_key and current_dict:
                result[current_key] = current_dict
                current_dict = None

            key, value = stripped.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Handle indented key (part of nested dict)
            if is_indented and current_key and current_dict is not None:
                # Convert value types
                if value.lower() == 'true':
                    current_dict[key] = True
                elif value.lower() == 'false':
                    current_dict[key] = False
                elif value.replace('.', '', 1).replace('-', '', 1).isdigit():
                    current_dict[key] = float(value) if '.' in value else int(value)
                elif value.startswith('[') and value.endswith(']'):
                    items = value[1:-1].split(',')
                    current_dict[key] = [item.strip() for item in items if item.strip()]
                else:
                    current_dict[key] = value.strip('"\'')
                i += 1
                continue

            # Handle inline lists [item1, item2]
            if value.startswith('[') and value.endswith(']'):
                items = value[1:-1].split(',')
                result[key] = [item.strip() for item in items if item.strip()]
                current_key = None
                current_dict = None
            # Empty value - could be list or nested dict
            elif not value:
                current_key = key
                # Check next line to determine if list or dict
                if i + 1 < len(lines):
                    next_stripped = lines[i + 1].strip()
                    if next_stripped.startswith('- '):
                        current_dict = None  # It's a list
                    else:
                        current_dict = {}  # It's a nested dict
                else:
                    current_dict = None
            # Simple value
            else:
                # Convert value types
                if value.lower() == 'true':
                    result[key] = True
                elif value.lower() == 'false':
                    result[key] = False
                elif value.replace('.', '', 1).replace('-', '', 1).isdigit():
                    result[key] = float(value) if '.' in value else int(value)
                else:
                    result[key] = value.strip('"\'')
                current_key = None
                current_dict = None

        i += 1

    # Save final collection if any
    if current_key:
        if list_items:
            result[current_key] = list_items
        elif current_dict is not None:
            result[current_key] = current_dict

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

    # Valid values for validation
    VALID_MODELS = ['sonnet', 'opus', 'haiku']
    VALID_TOOLS = ['Read', 'Write', 'Bash', 'Grep', 'Glob', 'Edit', 'NotebookEdit', 'WebFetch', 'WebSearch']
    VALID_COLORS = ['blue', 'green', 'red', 'purple', 'orange']
    VALID_FIELDS = ['quality', 'frontend', 'backend', 'fullstack', 'product', 'architecture',
                    'testing', 'devops', 'data', 'ai', 'security', 'performance', 'design',
                    'research', 'content', 'finance', 'agile', 'tools', 'coordination']
    VALID_DIFFICULTY = ['beginner', 'intermediate', 'advanced']
    VALID_EXPERTISE = ['beginner', 'intermediate', 'expert']
    VALID_EXECUTION = ['parallel', 'coordinated', 'sequential']
    VALID_CLASSIFICATION_TYPES = ['strategic', 'implementation', 'quality', 'coordination', 'domain-specific']

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    # -------------------------------------------------------------------------
    # Validation Helper Methods (extracted for reduced complexity)
    # -------------------------------------------------------------------------

    def _validate_required_fields(self, frontmatter: Dict) -> Optional[str]:
        """Validate required YAML fields are present. Returns error message or None."""
        required = ['name', 'description', 'domain', 'model', 'tools']
        for field in required:
            if field not in frontmatter:
                return f"Missing required YAML field: {field}"
        return None

    def _validate_core_fields(self, frontmatter: Dict) -> Optional[str]:
        """Validate core field values (description, model, tools). Returns error message or None."""
        if len(frontmatter['description']) > MAX_DESCRIPTION_LENGTH:
            return f"Description too long: {len(frontmatter['description'])} chars (max: {MAX_DESCRIPTION_LENGTH})"

        if frontmatter['model'] not in self.VALID_MODELS:
            return f"Invalid model: {frontmatter['model']} (must be: {', '.join(self.VALID_MODELS)})"

        if not isinstance(frontmatter['tools'], list):
            return "Tools must be a list"

        for tool in frontmatter['tools']:
            if tool not in self.VALID_TOOLS:
                return f"Invalid tool: {tool}"

        return None

    def _validate_string_field(self, frontmatter: Dict, field: str, max_len: int,
                                pattern: Optional[str] = None, pattern_desc: str = "") -> Optional[str]:
        """Validate optional string field. Returns error message or None."""
        if field not in frontmatter:
            return None

        value = frontmatter[field]
        if max_len > 0 and len(value) > max_len:
            return f"{field.title()} too long: {len(value)} chars (max: {max_len})"

        if pattern and not re.match(pattern, value):
            return f"Invalid {field} format: {value} ({pattern_desc})"

        return None

    def _validate_enum_field(self, frontmatter: Dict, field: str, valid_values: List[str]) -> Optional[str]:
        """Validate optional enum field. Returns error message or None."""
        if field not in frontmatter:
            return None

        value = frontmatter[field]
        if value not in valid_values:
            return f"Invalid {field}: {value} (must be: {', '.join(valid_values)})"

        return None

    def _validate_list_field(self, frontmatter: Dict, field: str) -> Optional[str]:
        """Validate optional list field. Returns error message or None."""
        if field not in frontmatter:
            return None

        if not isinstance(frontmatter[field], list):
            return f"{field} must be a list"

        return None

    def _validate_website_ready_fields(self, frontmatter: Dict) -> Optional[str]:
        """Validate Phase 1-4 website-ready fields. Returns error message or None."""
        # Phase 1: Core Identity + Versioning
        error = self._validate_string_field(frontmatter, 'title', 100)
        if error:
            return error

        error = self._validate_string_field(frontmatter, 'subdomain', 0,
                                            r'^[a-z][a-z0-9-]*$', "must be kebab-case")
        if error:
            return error

        error = self._validate_string_field(frontmatter, 'version', 0,
                                            r'^v?\d+\.\d+\.\d+$', "must be vX.Y.Z or X.Y.Z")
        if error:
            return error

        # Phase 2: Website Display + Discoverability
        error = self._validate_enum_field(frontmatter, 'difficulty', self.VALID_DIFFICULTY)
        if error:
            return error

        for list_field in ['use-cases', 'tags', 'related-agents', 'related-skills', 'related-commands']:
            error = self._validate_list_field(frontmatter, list_field)
            if error:
                return error

        # Phase 3: Classification
        if 'classification' in frontmatter:
            if isinstance(frontmatter['classification'], dict):
                if 'type' in frontmatter['classification']:
                    if frontmatter['classification']['type'] not in self.VALID_CLASSIFICATION_TYPES:
                        return f"Invalid classification type: {frontmatter['classification']['type']}"

        # Dependencies validation
        if 'dependencies' in frontmatter:
            deps = frontmatter['dependencies']
            if isinstance(deps, dict):
                if 'tools' in deps and not isinstance(deps['tools'], list):
                    return "dependencies.tools must be a list"
                if 'mcp-tools' in deps and not isinstance(deps['mcp-tools'], list):
                    return "dependencies.mcp-tools must be a list"

        # Phase 4: Examples + Analytics
        error = self._validate_list_field(frontmatter, 'examples')
        if error:
            return error

        if 'stats' in frontmatter and not isinstance(frontmatter['stats'], dict):
            return "stats must be a dictionary"

        return None

    def _validate_legacy_fields(self, frontmatter: Dict) -> Optional[str]:
        """Validate legacy fields for backward compatibility. Returns error message or None."""
        error = self._validate_enum_field(frontmatter, 'color', self.VALID_COLORS)
        if error:
            return error

        error = self._validate_enum_field(frontmatter, 'field', self.VALID_FIELDS)
        if error:
            return error

        error = self._validate_enum_field(frontmatter, 'expertise', self.VALID_EXPERTISE)
        if error:
            return error

        error = self._validate_enum_field(frontmatter, 'execution', self.VALID_EXECUTION)
        if error:
            return error

        return None

    def _validate_collaborates_with(self, frontmatter: Dict) -> Optional[str]:
        """
        Validate collaborates-with structure for agent dependencies.

        Expected format:
        collaborates-with:
          - agent: cs-technical-writer
            purpose: Description of collaboration
            required: optional|recommended|required
            features-enabled:
              - feature-1
              - feature-2
            without-collaborator: "What doesn't work without this"

        Returns error message or None.
        """
        if 'collaborates-with' not in frontmatter:
            return None

        collaborations = frontmatter['collaborates-with']

        if not isinstance(collaborations, list):
            return "collaborates-with must be a list"

        valid_required_values = ['optional', 'recommended', 'required']

        for idx, collab in enumerate(collaborations):
            if not isinstance(collab, dict):
                return f"collaborates-with[{idx}] must be a dictionary"

            # Required fields
            if 'agent' not in collab:
                return f"collaborates-with[{idx}] missing required 'agent' field"

            if 'purpose' not in collab:
                return f"collaborates-with[{idx}] missing required 'purpose' field"

            # Validate agent name format
            agent_name = collab.get('agent', '')
            if not agent_name.startswith('cs-'):
                return f"collaborates-with[{idx}].agent must start with 'cs-': {agent_name}"

            # Validate required field if present
            if 'required' in collab:
                if collab['required'] not in valid_required_values:
                    return f"collaborates-with[{idx}].required must be one of: {', '.join(valid_required_values)}"

            # Validate features-enabled if present (accept list or string for parser compatibility)
            if 'features-enabled' in collab:
                features = collab['features-enabled']
                if not isinstance(features, (list, str)):
                    return f"collaborates-with[{idx}].features-enabled must be a list or string"

            # Validate without-collaborator if present
            if 'without-collaborator' in collab:
                if not isinstance(collab['without-collaborator'], str):
                    return f"collaborates-with[{idx}].without-collaborator must be a string"

        return None

    # -------------------------------------------------------------------------
    # Public Validation Methods
    # -------------------------------------------------------------------------

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

        # Required fields validation
        error = self._validate_required_fields(frontmatter)
        if error:
            return False, error

        # Core field values validation
        error = self._validate_core_fields(frontmatter)
        if error:
            return False, error

        # Website-ready fields validation (Phase 1-4)
        error = self._validate_website_ready_fields(frontmatter)
        if error:
            return False, error

        # Legacy fields validation (backward compatibility)
        error = self._validate_legacy_fields(frontmatter)
        if error:
            return False, error

        # Collaborates-with validation (agent dependencies)
        error = self._validate_collaborates_with(frontmatter)
        if error:
            return False, error

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
        path_pattern = r'\.\./\.\./[a-zA-Z0-9_/-]+(?:\.[a-zA-Z]+)?'
        path_count = len(set(re.findall(path_pattern, content)))
        checks.append({
            'name': 'relative_paths',
            'status': 'passed' if valid else 'failed',
            'message': f"Valid ({path_count} paths checked)" if valid else f"Errors: {', '.join(errors)}"
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

        # Add dependencies section with nested mcp-tools
        tools_list = config.get('tools', ['Read', 'Write', 'Bash', 'Grep', 'Glob'])
        mcp_tools = config.get('mcp_tools', [])
        scripts = config.get('scripts', [])
        yaml_lines.append("dependencies:")
        yaml_lines.append(f"  tools: {tools_list}")
        yaml_lines.append(f"  mcp-tools: {mcp_tools}")
        yaml_lines.append(f"  scripts: {scripts}")

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

    # Domain to field mapping for intelligent defaults
    DOMAIN_TO_FIELD = {
        'engineering': 'backend',
        'product': 'product',
        'marketing': 'content',
        'c-level': 'architecture',
        'delivery': 'coordination'
    }

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.validator = AgentValidator(repo_root)
        self.template_loader = TemplateLoader(repo_root)
        self.catalog_updater = CatalogUpdater(repo_root)
        self.domain_manager = DomainManager(repo_root)

    # -------------------------------------------------------------------------
    # Interactive Mode Helper Methods (extracted for reduced complexity)
    # -------------------------------------------------------------------------

    def _prompt_agent_name(self) -> str:
        """Prompt for and validate agent name (Step 1)"""
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
                print()
                return name
            print(f"❌ {msg}")
            print("Try again:")

    def _prompt_domain_selection(self) -> str:
        """Prompt for domain selection (Step 2)"""
        print("Step 2/8: Domain")
        print("-" * 50)

        existing_domains = self.domain_manager.get_existing_domains()
        print("Select domain:")
        for idx, domain in enumerate(existing_domains, 1):
            agent_count = len(list((self.repo_root / "agents" / domain).glob("cs-*.md")))
            print(f"{idx}. {domain} ({agent_count} agents)")
        print(f"{len(existing_domains) + 1}. Create new domain")
        print()

        while True:
            choice = input(f"Domain (1-{len(existing_domains) + 1}): ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(existing_domains):
                domain = existing_domains[int(choice) - 1]
                print(f"✓ Domain: {domain}")
                print()
                return domain

            if choice.isdigit() and int(choice) == len(existing_domains) + 1:
                domain = self.create_new_domain_interactive()
                print()
                return domain

            print("❌ Invalid selection")

    def _prompt_description(self) -> str:
        """Prompt for agent description (Step 3)"""
        print("Step 3/8: Description")
        print("-" * 50)
        print(f"Enter one-line description (under {MAX_DESCRIPTION_INPUT} chars):")
        print('Example: "Data analysis and reporting for product decisions"')
        print()

        while True:
            description = input("Description: ").strip()
            if len(description) <= MAX_DESCRIPTION_INPUT:
                print(f"✓ Length: {len(description)} chars")
                print()
                return description
            print(f"❌ Description too long: {len(description)} chars (max: {MAX_DESCRIPTION_INPUT})")

    def _prompt_skills_integration(self, domain: str) -> str:
        """Prompt for skills integration (Step 4)"""
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

            if not skill_path.exists():
                print(f"❌ Skill not found: skills/{skill_team}/{skills}/")
                print("Try again:")
                continue

            scripts_dir = skill_path / "scripts"
            if scripts_dir.exists():
                tool_count = len(list(scripts_dir.glob("*.py")))
                print(f"✓ Skill exists: skills/{skill_team}/{skills}/")
                print(f"✓ Found {tool_count} Python tools")
                print()
                return skills

            print(f"⚠️  Skill exists but has no scripts/ directory")
            confirm = input("Continue anyway? (y/n): ").strip().lower()
            if confirm == 'y':
                print()
                return skills

    def _prompt_model_selection(self) -> str:
        """Prompt for model selection (Step 5)"""
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
                print()
                return model
            print("❌ Invalid selection")

    def _prompt_tools_selection(self) -> List[str]:
        """Prompt for tools selection (Step 6)"""
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
        return tools

    def _compute_classification_defaults(self, domain: str, tools: List[str]) -> Dict:
        """Compute intelligent defaults for agent classification based on domain and tools"""
        defaults = {
            'color': 'blue',
            'field': self.DOMAIN_TO_FIELD.get(domain),
            'expertise': 'intermediate',
            'execution': 'coordinated'
        }

        # Adjust based on tools
        if 'Bash' in tools and len(tools) >= 5:
            defaults['color'] = 'green'  # Implementation agent
            defaults['execution'] = 'coordinated'
        elif 'Bash' in tools and 'Edit' in tools:
            defaults['color'] = 'red'  # Quality agent
            defaults['execution'] = 'sequential'
        elif len(tools) <= 3:
            defaults['color'] = 'blue'  # Strategic agent
            defaults['execution'] = 'parallel'

        return defaults

    def _prompt_agent_classification(self, domain: str, tools: List[str]) -> Dict:
        """Prompt for agent classification (Step 7)"""
        print("Step 7/8: Agent Type Classification (Optional)")
        print("-" * 50)
        print("Configure agent type metadata for resource management and execution patterns.")
        print()

        defaults = self._compute_classification_defaults(domain, tools)

        # Color
        print(f"1. Color (agent type): blue=Strategic, green=Implementation, red=Quality, purple=Coordination")
        print(f"   Default: {defaults['color']}")
        color_input = input(f"   Color (Enter for default): ").strip().lower()
        color = color_input if color_input in ['blue', 'green', 'red', 'purple', 'orange'] else defaults['color']

        print()

        # Field
        print(f"2. Field (specialization): quality, frontend, backend, fullstack, product, architecture,")
        print(f"                          testing, devops, data, ai, security, performance, design,")
        print(f"                          research, content, finance, agile, tools")
        if defaults['field']:
            print(f"   Default: {defaults['field']}")
            field_input = input(f"   Field (Enter for default): ").strip().lower()
            field = field_input if field_input else defaults['field']
        else:
            field_input = input(f"   Field (Enter to skip): ").strip().lower()
            field = field_input if field_input else None

        print()

        # Expertise
        print(f"3. Expertise level: beginner, intermediate, expert")
        print(f"   Default: {defaults['expertise']}")
        expertise_input = input(f"   Expertise (Enter for default): ").strip().lower()
        expertise = expertise_input if expertise_input in ['beginner', 'intermediate', 'expert'] else defaults['expertise']

        print()

        # Execution
        print(f"4. Execution pattern: parallel (4-5 agents), coordinated (2-3 agents), sequential (1 agent)")
        print(f"   Default: {defaults['execution']}")
        execution_input = input(f"   Execution (Enter for default): ").strip().lower()
        execution = execution_input if execution_input in ['parallel', 'coordinated', 'sequential'] else defaults['execution']

        print()

        # MCP Tools
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

        return {
            'color': color,
            'field': field,
            'expertise': expertise,
            'execution': execution,
            'mcp_tools': mcp_tools
        }

    def _preview_and_confirm(self, config: Dict) -> bool:
        """Preview configuration and confirm (Step 8)"""
        print("Step 8/8: Preview")
        print("-" * 50)
        print("Review your agent configuration:")
        print()
        print(f"Name:        {config['name']}")
        print(f"Domain:      {config['domain']}")
        print(f"Description: {config['description']}")
        print(f"Skills:      {config['skills']}")
        print(f"Model:       {config['model']}")
        print(f"Tools:       {config['tools']}")
        print(f"Color:       {config['color']}")
        if config.get('field'):
            print(f"Field:       {config['field']}")
        print(f"Expertise:   {config['expertise']}")
        print(f"Execution:   {config['execution']}")
        if config.get('mcp_tools'):
            print(f"MCP Tools:   {config['mcp_tools']}")
        print()
        print("Files to create:")
        print(f"- agents/{config['domain']}/{config['name']}.md")
        print()
        print("Catalog updates:")
        print(f"- agents/{config['domain']}/CATALOG.md (append)")
        print()

        confirm = input("Proceed? (y/n): ").strip().lower()
        return confirm == 'y'

    # -------------------------------------------------------------------------
    # Public Methods
    # -------------------------------------------------------------------------

    def interactive_mode(self) -> None:
        """Run interactive agent creation workflow"""
        print("🤖 Agent Builder")
        print("=" * 50)
        print()

        # Collect configuration through step prompts
        name = self._prompt_agent_name()
        domain = self._prompt_domain_selection()
        description = self._prompt_description()
        skills = self._prompt_skills_integration(domain)
        model = self._prompt_model_selection()
        tools = self._prompt_tools_selection()
        classification = self._prompt_agent_classification(domain, tools)

        # Build configuration
        config = {
            'name': name,
            'domain': domain,
            'description': description,
            'skills': skills,
            'model': model,
            'tools': tools,
            'color': classification['color'],
            'expertise': classification['expertise'],
            'execution': classification['execution']
        }

        # Add optional fields if provided
        if classification['field']:
            config['field'] = classification['field']
        if classification['mcp_tools']:
            config['mcp_tools'] = classification['mcp_tools']

        # Preview and confirm
        if not self._preview_and_confirm(config):
            print("❌ Agent creation cancelled")
            sys.exit(0)

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
