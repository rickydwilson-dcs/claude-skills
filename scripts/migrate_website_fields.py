#!/usr/bin/env python3
"""
Website Fields Migration Script

Migrates agents and skills to website-ready frontmatter format with full parity
to the slash commands structure.

Usage:
    python migrate_website_fields.py --type agents --phase 1 --dry-run
    python migrate_website_fields.py --type skills --phase 1 --dry-run
    python migrate_website_fields.py --type all --phase 1 --execute
    python migrate_website_fields.py --report

ARCHITECTURE NOTE - Single-File Design:
    This script follows the repository's zero-dependency, portable philosophy.
    It can be extracted and run anywhere with Python 3.8+.

    Code is organized into logical sections:

    SECTION 1: Configuration & Constants
    SECTION 2: YAML Parsing Utilities
    SECTION 3: Field Derivation Logic
    SECTION 4: Agent Migration
    SECTION 5: Skill Migration (with flattening)
    SECTION 6: Reporting & Validation
    SECTION 7: CLI Entry Point
"""

# ============================================================================
# SECTION 1: CONFIGURATION & CONSTANTS
# ============================================================================

import os
import sys
import re
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

# Try to import PyYAML, provide fallback if not available
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_FAILED = 1
EXIT_FILE_ERROR = 2
EXIT_CONFIG_ERROR = 3

# Phase definitions
PHASE_1_FIELDS = {
    'agents': ['title', 'subdomain', 'version', 'author', 'contributors', 'created', 'updated', 'license'],
    'skills': ['title', 'subdomain', 'contributors', 'created']  # Skills flatten existing metadata
}

PHASE_2_FIELDS = {
    'agents': ['difficulty', 'time-saved', 'frequency', 'use-cases', 'tags', 'featured', 'verified'],
    'skills': ['difficulty', 'time-saved', 'frequency', 'use-cases', 'featured', 'verified']
}

PHASE_3_FIELDS = {
    'agents': ['related-agents', 'related-skills', 'related-commands', 'orchestrates', 'dependencies', 'compatibility'],
    'skills': ['related-agents', 'related-skills', 'related-commands', 'orchestrated-by', 'dependencies', 'compatibility']
}

PHASE_4_FIELDS = {
    'agents': ['examples', 'stats'],
    'skills': ['examples', 'stats']
}

# Expertise to difficulty mapping
EXPERTISE_TO_DIFFICULTY = {
    'expert': 'advanced',
    'senior': 'advanced',
    'intermediate': 'intermediate',
    'beginner': 'beginner'
}

# Domain to subdomain mapping (defaults)
DOMAIN_SUBDOMAINS = {
    'engineering': {
        'backend': 'backend-development',
        'frontend': 'frontend-development',
        'fullstack': 'fullstack-development',
        'devops': 'devops-operations',
        'architecture': 'system-architecture',
        'data': 'data-engineering',
        'ai': 'ai-ml-engineering',
        'security': 'security-engineering',
        'quality': 'quality-assurance',
        'testing': 'quality-assurance'
    },
    'product': {
        'product': 'product-management',
        'design': 'ux-design',
        'research': 'user-research',
        'agile': 'agile-methodology'
    },
    'marketing': {
        'content': 'content-marketing',
        'demand': 'demand-generation',
        'strategy': 'marketing-strategy'
    },
    'delivery': {
        'agile': 'agile-delivery',
        'tools': 'delivery-tools',
        'coordination': 'project-coordination'
    }
}


# ============================================================================
# SECTION 2: YAML PARSING UTILITIES
# ============================================================================

def parse_yaml_frontmatter(content: str) -> Tuple[Optional[Dict], str, Optional[str]]:
    """
    Extract YAML frontmatter and content body from markdown file.

    Returns:
        (frontmatter_dict, markdown_body, error_message)
    """
    if not content.startswith('---'):
        return None, content, "No YAML frontmatter found"

    # Find the end of frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content, "Malformed YAML frontmatter (no closing ---)"

    yaml_str = parts[1]
    body = '---'.join(parts[2:])  # Preserve any other --- in content

    try:
        if YAML_AVAILABLE:
            frontmatter = yaml.safe_load(yaml_str)
        else:
            frontmatter = simple_yaml_parse(yaml_str)
        return frontmatter, body, None
    except Exception as e:
        return None, body, f"Invalid YAML syntax: {e}"


def simple_yaml_parse(yaml_str: str) -> Dict:
    """Simple YAML parser for frontmatter (standard library only)"""
    result = {}
    current_key = None
    list_items = []
    in_nested = False
    nested_key = None
    nested_dict = {}

    for line in yaml_str.strip().split('\n'):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())

        if not stripped or stripped.startswith('#'):
            continue

        # List item
        if stripped.startswith('- '):
            item = stripped[2:].strip()
            list_items.append(item)
            continue

        # Key-value pair
        if ':' in stripped:
            # Save previous list if any
            if current_key and list_items:
                if in_nested:
                    nested_dict[current_key] = list_items
                else:
                    result[current_key] = list_items
                list_items = []

            key, value = stripped.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Nested object (indented with 2+ spaces)
            if indent >= 2:
                in_nested = True
                if value.startswith('[') and value.endswith(']'):
                    if value == '[]':
                        nested_dict[key] = []
                    else:
                        items = value[1:-1].split(',')
                        nested_dict[key] = [item.strip() for item in items]
                    current_key = None
                elif not value:
                    current_key = key
                else:
                    nested_dict[key] = value
                    current_key = None
            else:
                if in_nested and nested_key:
                    result[nested_key] = nested_dict
                    nested_dict = {}

                in_nested = False

                if value.startswith('[') and value.endswith(']'):
                    if value == '[]':
                        result[key] = []
                    else:
                        items = value[1:-1].split(',')
                        result[key] = [item.strip() for item in items]
                    current_key = None
                elif not value:
                    current_key = key
                    nested_key = key
                    in_nested = False
                else:
                    result[key] = value
                    current_key = None

    if current_key and list_items:
        if in_nested:
            nested_dict[current_key] = list_items
        else:
            result[current_key] = list_items

    if in_nested and nested_key:
        result[nested_key] = nested_dict

    return result


def format_yaml_frontmatter(data: Dict, section_comments: bool = True) -> str:
    """
    Format dictionary as YAML frontmatter with optional section comments.

    Args:
        data: Dictionary to format
        section_comments: Whether to add # === SECTION === comments

    Returns:
        YAML-formatted string with --- delimiters
    """
    lines = ['---']

    # Define section ordering and comments
    sections = [
        ('CORE IDENTITY', ['name', 'title', 'description', 'domain', 'subdomain', 'skills', 'model']),
        ('WEBSITE DISPLAY', ['difficulty', 'time-saved', 'frequency', 'use-cases']),
        ('AGENT CLASSIFICATION', ['classification']),
        ('RELATIONSHIPS', ['related-agents', 'related-skills', 'related-commands', 'orchestrates', 'orchestrated-by']),
        ('TECHNICAL', ['tools', 'dependencies', 'compatibility', 'tech-stack']),
        ('EXAMPLES', ['examples']),
        ('ANALYTICS', ['stats']),
        ('VERSIONING', ['version', 'author', 'contributors', 'created', 'updated', 'license']),
        ('DISCOVERABILITY', ['tags', 'keywords', 'featured', 'verified']),
        ('LEGACY', ['color', 'field', 'expertise', 'execution', 'mcp_tools'])  # Keep legacy fields
    ]

    used_keys = set()

    for section_name, section_keys in sections:
        section_lines = []
        for key in section_keys:
            if key in data:
                section_lines.extend(_format_yaml_value(key, data[key]))
                used_keys.add(key)

        if section_lines:
            if section_comments:
                lines.append(f'\n# === {section_name} ===')
            lines.extend(section_lines)

    # Add any remaining keys not in sections
    for key in data:
        if key not in used_keys:
            lines.extend(_format_yaml_value(key, data[key]))

    lines.append('---')
    return '\n'.join(lines)


def _format_yaml_value(key: str, value: Any, indent: int = 0) -> List[str]:
    """Format a single YAML key-value pair"""
    prefix = '  ' * indent
    lines = []

    if value is None:
        lines.append(f'{prefix}{key}:')
    elif isinstance(value, bool):
        lines.append(f'{prefix}{key}: {str(value).lower()}')
    elif isinstance(value, str):
        if '\n' in value:
            lines.append(f'{prefix}{key}: |')
            for line in value.split('\n'):
                lines.append(f'{prefix}  {line}')
        elif ':' in value or '"' in value or "'" in value:
            lines.append(f'{prefix}{key}: "{value}"')
        else:
            lines.append(f'{prefix}{key}: {value}')
    elif isinstance(value, (int, float)):
        lines.append(f'{prefix}{key}: {value}')
    elif isinstance(value, list):
        if not value:
            lines.append(f'{prefix}{key}: []')
        elif all(isinstance(item, str) and len(item) < 40 for item in value):
            # Short list - inline format
            items_str = ', '.join(str(item) for item in value)
            if len(items_str) < 60:
                lines.append(f'{prefix}{key}: [{items_str}]')
            else:
                lines.append(f'{prefix}{key}:')
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f'{prefix}  - ')
                        for k, v in item.items():
                            lines.extend(_format_yaml_value(k, v, indent + 2))
                    else:
                        lines.append(f'{prefix}  - {item}')
        else:
            lines.append(f'{prefix}{key}:')
            for item in value:
                if isinstance(item, dict):
                    lines.append(f'{prefix}  -')
                    for k, v in item.items():
                        sub_lines = _format_yaml_value(k, v, indent + 2)
                        lines.extend(sub_lines)
                else:
                    lines.append(f'{prefix}  - {item}')
    elif isinstance(value, dict):
        lines.append(f'{prefix}{key}:')
        for k, v in value.items():
            lines.extend(_format_yaml_value(k, v, indent + 1))
    else:
        lines.append(f'{prefix}{key}: {value}')

    return lines


# ============================================================================
# SECTION 3: FIELD DERIVATION LOGIC
# ============================================================================

def derive_title(name: str, asset_type: str) -> str:
    """
    Derive human-readable title from name.

    Examples:
        cs-architect -> System Architecture Specialist
        senior-backend -> Senior Backend Development Skill
    """
    # Remove cs- prefix for agents
    clean_name = name.replace('cs-', '').replace('-', ' ')

    # Title case with common acronym handling
    words = clean_name.split()
    title_words = []
    acronyms = {'ai', 'ml', 'api', 'ui', 'ux', 'qa', 'ci', 'cd', 'pm', 'cto'}

    for word in words:
        if word.lower() in acronyms:
            title_words.append(word.upper())
        else:
            title_words.append(word.capitalize())

    title = ' '.join(title_words)

    # Add appropriate suffix
    if asset_type == 'agent':
        if 'engineer' not in title.lower() and 'specialist' not in title.lower():
            title = f"{title} Specialist"
    elif asset_type == 'skill':
        if 'skill' not in title.lower() and 'toolkit' not in title.lower():
            title = f"{title} Skill Package"

    return title


def derive_subdomain(name: str, domain: str, field: Optional[str] = None) -> str:
    """Derive subdomain from name, domain, and field"""
    # Try to get from domain -> field mapping
    if domain in DOMAIN_SUBDOMAINS and field:
        if field in DOMAIN_SUBDOMAINS[domain]:
            return DOMAIN_SUBDOMAINS[domain][field]

    # Extract from name
    clean_name = name.replace('cs-', '').replace('senior-', '')

    # Common patterns
    if 'backend' in clean_name:
        return 'backend-development'
    elif 'frontend' in clean_name:
        return 'frontend-development'
    elif 'fullstack' in clean_name:
        return 'fullstack-development'
    elif 'architect' in clean_name:
        return 'system-architecture'
    elif 'devops' in clean_name:
        return 'devops-operations'
    elif 'security' in clean_name or 'secops' in clean_name:
        return 'security-engineering'
    elif 'data' in clean_name:
        return 'data-engineering'
    elif 'ml' in clean_name or 'ai' in clean_name:
        return 'ai-ml-engineering'
    elif 'qa' in clean_name or 'quality' in clean_name:
        return 'quality-assurance'
    elif 'prompt' in clean_name:
        return 'prompt-engineering'
    elif 'computer-vision' in clean_name or 'vision' in clean_name:
        return 'computer-vision'
    elif 'product' in clean_name:
        return 'product-management'
    elif 'ux' in clean_name or 'design' in clean_name:
        return 'ux-design'
    elif 'ui' in clean_name:
        return 'ui-design'
    elif 'content' in clean_name:
        return 'content-marketing'
    elif 'demand' in clean_name:
        return 'demand-generation'
    elif 'scrum' in clean_name or 'agile' in clean_name:
        return 'agile-methodology'
    elif 'jira' in clean_name or 'confluence' in clean_name:
        return 'delivery-tools'

    # Default: use domain + general
    return f"{domain}-general"


def derive_difficulty(expertise: Optional[str], name: str) -> str:
    """Derive difficulty level from expertise field or name"""
    if expertise:
        return EXPERTISE_TO_DIFFICULTY.get(expertise.lower(), 'intermediate')

    # Infer from name
    if 'senior' in name.lower() or 'cto' in name.lower():
        return 'advanced'
    elif 'junior' in name.lower() or 'beginner' in name.lower():
        return 'beginner'

    return 'intermediate'


def derive_tags(name: str, description: str, domain: str, field: Optional[str] = None) -> List[str]:
    """Derive searchable tags from name, description, and domain"""
    tags = set()

    # Add domain
    tags.add(domain)

    # Add field if present
    if field:
        tags.add(field)

    # Extract from name
    clean_name = name.replace('cs-', '').replace('-', ' ')
    for word in clean_name.split():
        if len(word) >= 3 and word.lower() not in ['the', 'and', 'for']:
            tags.add(word.lower())

    # Extract keywords from description
    keywords = ['architecture', 'design', 'development', 'engineering', 'analysis',
                'automation', 'testing', 'security', 'performance', 'optimization',
                'api', 'database', 'cloud', 'microservices', 'devops', 'ci/cd',
                'machine learning', 'data', 'analytics', 'product', 'agile', 'scrum']

    desc_lower = description.lower()
    for keyword in keywords:
        if keyword in desc_lower:
            tags.add(keyword.replace(' ', '-'))

    return sorted(list(tags))[:10]  # Limit to 10 tags


def derive_use_cases(name: str, description: str, asset_type: str) -> List[str]:
    """Generate placeholder use cases based on name and description"""
    clean_name = name.replace('cs-', '').replace('-', ' ').title()

    # Default use cases based on patterns
    use_cases = []

    if 'architect' in name.lower():
        use_cases = [
            "Designing scalable system architectures for cloud-native applications",
            "Evaluating technology stacks and making evidence-based decisions",
            "Creating comprehensive architecture documentation with diagrams",
            "Reviewing existing architectures for performance and security"
        ]
    elif 'backend' in name.lower():
        use_cases = [
            "Building robust API services with proper authentication and authorization",
            "Designing database schemas and optimizing query performance",
            "Implementing microservices patterns and service communication",
            "Setting up CI/CD pipelines for backend applications"
        ]
    elif 'frontend' in name.lower():
        use_cases = [
            "Building responsive user interfaces with modern frameworks",
            "Implementing state management and component architecture",
            "Optimizing frontend performance and bundle sizes",
            "Creating accessible and user-friendly web experiences"
        ]
    elif 'devops' in name.lower():
        use_cases = [
            "Setting up infrastructure as code with Terraform or CloudFormation",
            "Implementing CI/CD pipelines with automated testing and deployment",
            "Configuring container orchestration with Kubernetes",
            "Monitoring and alerting setup for production systems"
        ]
    elif 'security' in name.lower() or 'secops' in name.lower():
        use_cases = [
            "Conducting security audits and vulnerability assessments",
            "Implementing authentication and authorization patterns",
            "Setting up security monitoring and incident response",
            "Reviewing code for OWASP Top 10 vulnerabilities"
        ]
    elif 'qa' in name.lower() or 'testing' in name.lower():
        use_cases = [
            "Designing comprehensive test strategies and test plans",
            "Implementing automated testing frameworks",
            "Setting up continuous testing in CI/CD pipelines",
            "Conducting performance and load testing"
        ]
    elif 'data' in name.lower():
        use_cases = [
            "Designing data pipelines for ETL/ELT processes",
            "Building data warehouses and data lakes",
            "Implementing data quality and governance frameworks",
            "Creating analytics dashboards and reporting"
        ]
    elif 'product' in name.lower():
        use_cases = [
            "Defining product roadmaps and feature prioritization",
            "Writing user stories and acceptance criteria",
            "Conducting competitive analysis and market research",
            "Stakeholder communication and alignment"
        ]
    elif 'content' in name.lower():
        use_cases = [
            "Creating engaging content for target audiences",
            "Optimizing content for SEO and discoverability",
            "Developing brand voice and messaging guidelines",
            "Planning content calendars and campaigns"
        ]
    else:
        # Generic use cases
        use_cases = [
            f"Primary workflow for {clean_name}",
            f"Analysis and recommendations for {clean_name.lower()} tasks",
            f"Best practices implementation for {clean_name.lower()}",
            f"Integration with related {asset_type}s and workflows"
        ]

    return use_cases


def get_git_created_date(file_path: Path) -> str:
    """Get file creation date from git, fallback to current date"""
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'log', '--follow', '--format=%aI', '--', str(file_path)],
            capture_output=True,
            text=True,
            cwd=file_path.parent
        )
        if result.returncode == 0 and result.stdout.strip():
            dates = result.stdout.strip().split('\n')
            if dates:
                # Get earliest date
                earliest = dates[-1]
                return earliest.split('T')[0]
    except Exception:
        pass

    return datetime.now().strftime('%Y-%m-%d')


# ============================================================================
# SECTION 4: AGENT MIGRATION
# ============================================================================

class AgentMigrator:
    """Handles migration of agent files to website-ready format"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.agents_dir = repo_root / "agents"
        self.backup_dir = repo_root / "output" / "backups" / f"migration-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    def get_all_agents(self) -> List[Path]:
        """Get all agent files"""
        agents = []
        for domain_dir in self.agents_dir.iterdir():
            if domain_dir.is_dir() and not domain_dir.name.startswith('.'):
                for agent_file in domain_dir.glob("cs-*.md"):
                    agents.append(agent_file)
        return sorted(agents)

    def migrate_agent(self, agent_path: Path, phase: int, dry_run: bool = True) -> Dict:
        """
        Migrate a single agent file.

        Returns:
            Dictionary with migration results
        """
        result = {
            'file': str(agent_path.relative_to(self.repo_root)),
            'status': 'pending',
            'changes': [],
            'errors': []
        }

        try:
            content = agent_path.read_text()
            frontmatter, body, error = parse_yaml_frontmatter(content)

            if error:
                result['status'] = 'error'
                result['errors'].append(error)
                return result

            # Create backup
            if not dry_run:
                self.backup_dir.mkdir(parents=True, exist_ok=True)
                backup_path = self.backup_dir / agent_path.relative_to(self.repo_root)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(agent_path, backup_path)

            # Apply phase-specific migrations
            updated_frontmatter = self._apply_phase_migrations(frontmatter, agent_path, phase, result)

            if not dry_run and result['changes']:
                # Generate new content
                new_yaml = format_yaml_frontmatter(updated_frontmatter)
                new_content = new_yaml + body
                agent_path.write_text(new_content)
                result['status'] = 'migrated'
            else:
                result['status'] = 'dry_run' if result['changes'] else 'no_changes'

        except Exception as e:
            result['status'] = 'error'
            result['errors'].append(str(e))

        return result

    def _apply_phase_migrations(self, frontmatter: Dict, agent_path: Path, phase: int, result: Dict) -> Dict:
        """Apply phase-specific field migrations"""
        updated = dict(frontmatter)
        name = frontmatter.get('name', agent_path.stem)
        description = frontmatter.get('description', '')
        domain = frontmatter.get('domain', 'engineering')
        field = frontmatter.get('field')
        expertise = frontmatter.get('expertise')

        if phase >= 1:
            # Phase 1: Core Identity + Versioning
            if 'title' not in updated:
                updated['title'] = derive_title(name, 'agent')
                result['changes'].append(f"Added title: {updated['title']}")

            if 'subdomain' not in updated:
                updated['subdomain'] = derive_subdomain(name, domain, field)
                result['changes'].append(f"Added subdomain: {updated['subdomain']}")

            if 'version' not in updated:
                updated['version'] = 'v1.0.0'
                result['changes'].append("Added version: v1.0.0")

            if 'author' not in updated:
                updated['author'] = 'Claude Skills Team'
                result['changes'].append("Added author: Claude Skills Team")

            if 'contributors' not in updated:
                updated['contributors'] = []
                result['changes'].append("Added contributors: []")

            if 'created' not in updated:
                updated['created'] = get_git_created_date(agent_path)
                result['changes'].append(f"Added created: {updated['created']}")

            if 'updated' not in updated:
                updated['updated'] = datetime.now().strftime('%Y-%m-%d')
                result['changes'].append(f"Added updated: {updated['updated']}")

            if 'license' not in updated:
                updated['license'] = 'MIT'
                result['changes'].append("Added license: MIT")

        if phase >= 2:
            # Phase 2: Website Display + Discoverability
            if 'difficulty' not in updated:
                updated['difficulty'] = derive_difficulty(expertise, name)
                result['changes'].append(f"Added difficulty: {updated['difficulty']}")

            if 'time-saved' not in updated:
                updated['time-saved'] = "TODO: Quantify time savings"
                result['changes'].append("Added time-saved placeholder")

            if 'frequency' not in updated:
                updated['frequency'] = "TODO: Estimate usage frequency"
                result['changes'].append("Added frequency placeholder")

            if 'use-cases' not in updated:
                updated['use-cases'] = derive_use_cases(name, description, 'agent')
                result['changes'].append(f"Added {len(updated['use-cases'])} use-cases")

            if 'tags' not in updated:
                updated['tags'] = derive_tags(name, description, domain, field)
                result['changes'].append(f"Added {len(updated['tags'])} tags")

            if 'featured' not in updated:
                updated['featured'] = False
                result['changes'].append("Added featured: false")

            if 'verified' not in updated:
                updated['verified'] = True
                result['changes'].append("Added verified: true")

        if phase >= 3:
            # Phase 3: Relationships + Technical
            if 'related-agents' not in updated:
                updated['related-agents'] = []
                result['changes'].append("Added related-agents: []")

            if 'related-skills' not in updated:
                skill = frontmatter.get('skills', '')
                if skill:
                    team = f"{domain}-team"
                    updated['related-skills'] = [f"{team}/{skill}"]
                else:
                    updated['related-skills'] = []
                result['changes'].append(f"Added related-skills: {updated['related-skills']}")

            if 'related-commands' not in updated:
                updated['related-commands'] = []
                result['changes'].append("Added related-commands: []")

            if 'orchestrates' not in updated:
                skill = frontmatter.get('skills', '')
                if skill:
                    team = f"{domain}-team"
                    updated['orchestrates'] = {'skill': f"{team}/{skill}"}
                    result['changes'].append(f"Added orchestrates: {updated['orchestrates']}")

            # Restructure tools to dependencies if not already done
            if 'dependencies' not in updated and 'tools' in updated:
                tools = updated.get('tools', [])
                mcp_tools = updated.get('mcp_tools', [])
                updated['dependencies'] = {
                    'tools': tools if isinstance(tools, list) else [tools],
                    'mcp-tools': mcp_tools if isinstance(mcp_tools, list) else [],
                    'scripts': []
                }
                result['changes'].append("Restructured tools into dependencies")

            if 'compatibility' not in updated:
                updated['compatibility'] = {
                    'claude-ai': True,
                    'claude-code': True,
                    'platforms': ['macos', 'linux', 'windows']
                }
                result['changes'].append("Added compatibility")

        if phase >= 4:
            # Phase 4: Examples + Analytics
            if 'examples' not in updated:
                updated['examples'] = [
                    {
                        'title': 'Example Workflow',
                        'input': f'TODO: Add example input for {name}',
                        'output': 'TODO: Add expected output'
                    }
                ]
                result['changes'].append("Added examples placeholder")

            if 'stats' not in updated:
                updated['stats'] = {
                    'installs': 0,
                    'upvotes': 0,
                    'rating': 0.0,
                    'reviews': 0
                }
                result['changes'].append("Added stats placeholder")

            # Group existing agent classification fields
            if 'classification' not in updated:
                classification = {}
                for key in ['color', 'field', 'expertise', 'execution', 'model']:
                    if key in updated:
                        if key == 'color':
                            classification['type'] = self._color_to_type(updated[key])
                        classification[key] = updated[key]

                if classification:
                    updated['classification'] = classification
                    result['changes'].append("Grouped classification fields")

        return updated

    def _color_to_type(self, color: str) -> str:
        """Map color to agent type"""
        mapping = {
            'blue': 'strategic',
            'green': 'implementation',
            'red': 'quality',
            'purple': 'coordination',
            'orange': 'domain-specific'
        }
        return mapping.get(color, 'strategic')


# ============================================================================
# SECTION 5: SKILL MIGRATION (WITH FLATTENING)
# ============================================================================

class SkillMigrator:
    """Handles migration of skill files with metadata flattening"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.skills_dir = repo_root / "skills"
        self.backup_dir = repo_root / "output" / "backups" / f"migration-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    def get_all_skills(self) -> List[Path]:
        """Get all SKILL.md files"""
        skills = []
        for team_dir in self.skills_dir.iterdir():
            if team_dir.is_dir() and not team_dir.name.startswith('.'):
                for skill_dir in team_dir.iterdir():
                    if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                        skill_md = skill_dir / "SKILL.md"
                        if skill_md.exists():
                            skills.append(skill_md)
        return sorted(skills)

    def migrate_skill(self, skill_path: Path, phase: int, dry_run: bool = True) -> Dict:
        """
        Migrate a single skill file with metadata flattening.

        Returns:
            Dictionary with migration results
        """
        result = {
            'file': str(skill_path.relative_to(self.repo_root)),
            'status': 'pending',
            'changes': [],
            'errors': []
        }

        try:
            content = skill_path.read_text()
            frontmatter, body, error = parse_yaml_frontmatter(content)

            if error:
                result['status'] = 'error'
                result['errors'].append(error)
                return result

            # Check for duplicate frontmatter (known issue in some skills)
            if body.strip().startswith('license:') or body.strip().startswith('metadata:'):
                result['errors'].append("Warning: Possible duplicate metadata in body - manual review needed")

            # Create backup
            if not dry_run:
                self.backup_dir.mkdir(parents=True, exist_ok=True)
                backup_path = self.backup_dir / skill_path.relative_to(self.repo_root)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(skill_path, backup_path)

            # Apply phase-specific migrations with flattening
            updated_frontmatter = self._apply_phase_migrations(frontmatter, skill_path, phase, result)

            if not dry_run and result['changes']:
                # Generate new content
                new_yaml = format_yaml_frontmatter(updated_frontmatter)

                # Clean up body if it starts with duplicate metadata
                clean_body = self._clean_duplicate_metadata(body)

                new_content = new_yaml + clean_body
                skill_path.write_text(new_content)
                result['status'] = 'migrated'
            else:
                result['status'] = 'dry_run' if result['changes'] else 'no_changes'

        except Exception as e:
            result['status'] = 'error'
            result['errors'].append(str(e))

        return result

    def _clean_duplicate_metadata(self, body: str) -> str:
        """Remove duplicate metadata block from body if present"""
        # Look for patterns that indicate duplicate metadata
        lines = body.split('\n')
        clean_lines = []
        skip_until_content = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Skip duplicate license/metadata lines at the start
            if i < 50 and stripped.startswith(('license:', 'metadata:')):
                skip_until_content = True
                continue

            if skip_until_content:
                # Look for actual content (headers, significant text)
                if stripped.startswith('#') or (len(stripped) > 50 and not stripped.startswith('-')):
                    skip_until_content = False
                    clean_lines.append(line)
                continue

            clean_lines.append(line)

        return '\n'.join(clean_lines)

    def _apply_phase_migrations(self, frontmatter: Dict, skill_path: Path, phase: int, result: Dict) -> Dict:
        """Apply phase-specific field migrations with flattening"""
        updated = {}

        # Extract nested metadata if present
        metadata = frontmatter.get('metadata', {})
        if not isinstance(metadata, dict):
            metadata = {}

        name = frontmatter.get('name', skill_path.parent.name)
        description = frontmatter.get('description', '')

        # Always flatten to top-level
        updated['name'] = name
        updated['description'] = description

        # Get domain from metadata or derive from path
        domain = metadata.get('domain', metadata.get('category', ''))
        if not domain:
            # Derive from path: skills/engineering-team/skill-name
            team_dir = skill_path.parent.parent.name
            domain = team_dir.replace('-team', '')
        updated['domain'] = domain.lower()

        if phase >= 1:
            # Phase 1: Flatten metadata + Core Identity + Versioning
            if 'title' not in frontmatter:
                updated['title'] = derive_title(name, 'skill')
                result['changes'].append(f"Added title: {updated['title']}")
            else:
                updated['title'] = frontmatter['title']

            if 'subdomain' not in frontmatter:
                updated['subdomain'] = derive_subdomain(name, updated['domain'])
                result['changes'].append(f"Added subdomain: {updated['subdomain']}")
            else:
                updated['subdomain'] = frontmatter['subdomain']

            # Flatten version from metadata
            version = metadata.get('version', frontmatter.get('version', '1.0.0'))
            updated['version'] = f"v{version}" if not str(version).startswith('v') else version
            if 'version' not in frontmatter:
                result['changes'].append(f"Flattened version: {updated['version']}")

            # Flatten author from metadata
            updated['author'] = metadata.get('author', frontmatter.get('author', 'Claude Skills Team'))
            if 'author' not in frontmatter:
                result['changes'].append(f"Flattened author: {updated['author']}")

            # Add contributors
            updated['contributors'] = frontmatter.get('contributors', [])
            if 'contributors' not in frontmatter:
                result['changes'].append("Added contributors: []")

            # Add/flatten created date
            if 'created' not in frontmatter:
                updated['created'] = get_git_created_date(skill_path)
                result['changes'].append(f"Added created: {updated['created']}")
            else:
                updated['created'] = frontmatter['created']

            # Flatten updated from metadata
            updated['updated'] = metadata.get('updated', frontmatter.get('updated', datetime.now().strftime('%Y-%m-%d')))
            if 'updated' not in frontmatter:
                result['changes'].append(f"Flattened updated: {updated['updated']}")

            # Keep license at top level
            updated['license'] = frontmatter.get('license', 'MIT')

            # Flatten tech-stack from metadata
            tech_stack = metadata.get('tech-stack', frontmatter.get('tech-stack', []))
            if tech_stack:
                updated['tech-stack'] = tech_stack
                if 'tech-stack' not in frontmatter:
                    result['changes'].append(f"Flattened tech-stack: {len(tech_stack)} items")

            # Mark as flattened if metadata was nested
            if metadata:
                result['changes'].append("Flattened nested metadata to top-level")

        if phase >= 2:
            # Phase 2: Website Display + Discoverability
            if 'difficulty' not in frontmatter:
                # Infer from name
                updated['difficulty'] = derive_difficulty(None, name)
                result['changes'].append(f"Added difficulty: {updated['difficulty']}")
            else:
                updated['difficulty'] = frontmatter['difficulty']

            if 'time-saved' not in frontmatter:
                updated['time-saved'] = "TODO: Quantify time savings"
                result['changes'].append("Added time-saved placeholder")
            else:
                updated['time-saved'] = frontmatter['time-saved']

            if 'frequency' not in frontmatter:
                updated['frequency'] = "TODO: Estimate usage frequency"
                result['changes'].append("Added frequency placeholder")
            else:
                updated['frequency'] = frontmatter['frequency']

            if 'use-cases' not in frontmatter:
                updated['use-cases'] = derive_use_cases(name, description, 'skill')
                result['changes'].append(f"Added {len(updated['use-cases'])} use-cases")
            else:
                updated['use-cases'] = frontmatter['use-cases']

            # Rename keywords to tags or use existing
            keywords = metadata.get('keywords', frontmatter.get('keywords', []))
            tags = frontmatter.get('tags', [])

            if not tags and keywords:
                updated['tags'] = keywords[:10]  # Limit to 10
                result['changes'].append(f"Renamed keywords to tags: {len(updated['tags'])} items")
            elif tags:
                updated['tags'] = tags
            else:
                updated['tags'] = derive_tags(name, description, updated['domain'])
                result['changes'].append(f"Derived {len(updated['tags'])} tags")

            # Keep keywords for skills (they have both)
            if keywords:
                updated['keywords'] = keywords

            if 'featured' not in frontmatter:
                updated['featured'] = False
                result['changes'].append("Added featured: false")
            else:
                updated['featured'] = frontmatter['featured']

            if 'verified' not in frontmatter:
                updated['verified'] = True
                result['changes'].append("Added verified: true")
            else:
                updated['verified'] = frontmatter['verified']

        if phase >= 3:
            # Phase 3: Relationships + Technical
            if 'related-agents' not in frontmatter:
                # Find agents that reference this skill
                updated['related-agents'] = []
                result['changes'].append("Added related-agents: []")
            else:
                updated['related-agents'] = frontmatter['related-agents']

            if 'related-skills' not in frontmatter:
                updated['related-skills'] = []
                result['changes'].append("Added related-skills: []")
            else:
                updated['related-skills'] = frontmatter['related-skills']

            if 'related-commands' not in frontmatter:
                updated['related-commands'] = []
                result['changes'].append("Added related-commands: []")
            else:
                updated['related-commands'] = frontmatter['related-commands']

            if 'orchestrated-by' not in frontmatter:
                updated['orchestrated-by'] = []
                result['changes'].append("Added orchestrated-by: []")
            else:
                updated['orchestrated-by'] = frontmatter['orchestrated-by']

            # Build dependencies from metadata
            python_tools = metadata.get('python-tools', frontmatter.get('python-tools', []))
            if 'dependencies' not in frontmatter:
                updated['dependencies'] = {
                    'scripts': python_tools,
                    'references': [],
                    'assets': []
                }
                result['changes'].append("Built dependencies from python-tools")
            else:
                updated['dependencies'] = frontmatter['dependencies']

            if 'compatibility' not in frontmatter:
                updated['compatibility'] = {
                    'python-version': '3.8+',
                    'platforms': ['macos', 'linux', 'windows']
                }
                result['changes'].append("Added compatibility")
            else:
                updated['compatibility'] = frontmatter['compatibility']

        if phase >= 4:
            # Phase 4: Examples + Analytics
            if 'examples' not in frontmatter:
                updated['examples'] = [
                    {
                        'title': 'Example Usage',
                        'input': f'TODO: Add example input for {name}',
                        'output': 'TODO: Add expected output'
                    }
                ]
                result['changes'].append("Added examples placeholder")
            else:
                updated['examples'] = frontmatter['examples']

            if 'stats' not in frontmatter:
                updated['stats'] = {
                    'downloads': 0,
                    'stars': 0,
                    'rating': 0.0,
                    'reviews': 0
                }
                result['changes'].append("Added stats placeholder")
            else:
                updated['stats'] = frontmatter['stats']

        return updated


# ============================================================================
# SECTION 6: REPORTING & VALIDATION
# ============================================================================

def generate_migration_report(results: List[Dict], output_path: Optional[Path] = None) -> str:
    """Generate migration report from results"""
    report_lines = [
        "# Website Fields Migration Report",
        f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n## Summary\n"
    ]

    # Calculate stats
    total = len(results)
    migrated = sum(1 for r in results if r['status'] == 'migrated')
    dry_run = sum(1 for r in results if r['status'] == 'dry_run')
    no_changes = sum(1 for r in results if r['status'] == 'no_changes')
    errors = sum(1 for r in results if r['status'] == 'error')

    report_lines.extend([
        f"| Status | Count |",
        f"|--------|-------|",
        f"| Total Files | {total} |",
        f"| Migrated | {migrated} |",
        f"| Dry Run | {dry_run} |",
        f"| No Changes | {no_changes} |",
        f"| Errors | {errors} |",
        "\n"
    ])

    # List changes by file
    report_lines.append("## Changes by File\n")

    for result in results:
        status_icon = {
            'migrated': '✅',
            'dry_run': '🔍',
            'no_changes': '⏭️',
            'error': '❌'
        }.get(result['status'], '❓')

        report_lines.append(f"### {status_icon} {result['file']}\n")

        if result['changes']:
            for change in result['changes']:
                report_lines.append(f"- {change}")
        else:
            report_lines.append("- No changes")

        if result['errors']:
            report_lines.append("\n**Errors:**")
            for error in result['errors']:
                report_lines.append(f"- ⚠️ {error}")

        report_lines.append("")

    report = '\n'.join(report_lines)

    if output_path:
        output_path.write_text(report)
        print(f"📄 Report saved to: {output_path}")

    return report


# ============================================================================
# SECTION 7: CLI ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Migrate agents and skills to website-ready frontmatter format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python migrate_website_fields.py --type agents --phase 1 --dry-run
  python migrate_website_fields.py --type skills --phase 1 --dry-run
  python migrate_website_fields.py --type all --phase 1 --execute
  python migrate_website_fields.py --report

Phases:
  1: Core Identity + Versioning (+ flatten for skills)
  2: Website Display + Discoverability
  3: Relationships + Technical
  4: Examples + Analytics
"""
    )

    parser.add_argument(
        '--type',
        choices=['agents', 'skills', 'all'],
        help='Type of assets to migrate'
    )

    parser.add_argument(
        '--phase',
        type=int,
        choices=[1, 2, 3, 4],
        default=1,
        help='Migration phase (1-4)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without writing files'
    )

    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually write changes to files'
    )

    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate migration status report'
    )

    parser.add_argument(
        '--file',
        help='Migrate a single file (for testing)'
    )

    args = parser.parse_args()

    # Determine repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Initialize migrators
    agent_migrator = AgentMigrator(repo_root)
    skill_migrator = SkillMigrator(repo_root)

    results = []

    if args.report:
        # Generate status report
        print("📊 Generating migration status report...\n")

        # Collect all agents
        agents = agent_migrator.get_all_agents()
        print(f"Found {len(agents)} agents")

        # Collect all skills
        skills = skill_migrator.get_all_skills()
        print(f"Found {len(skills)} skills")

        # Quick check of each file's current state
        for agent in agents:
            content = agent.read_text()
            frontmatter, _, _ = parse_yaml_frontmatter(content)
            has_title = frontmatter and 'title' in frontmatter
            has_version = frontmatter and 'version' in frontmatter

            results.append({
                'file': str(agent.relative_to(repo_root)),
                'status': 'migrated' if (has_title and has_version) else 'pending',
                'changes': [],
                'errors': []
            })

        for skill in skills:
            content = skill.read_text()
            frontmatter, _, _ = parse_yaml_frontmatter(content)
            has_title = frontmatter and 'title' in frontmatter
            is_flat = frontmatter and 'metadata' not in frontmatter

            results.append({
                'file': str(skill.relative_to(repo_root)),
                'status': 'migrated' if (has_title and is_flat) else 'pending',
                'changes': [],
                'errors': []
            })

        report_path = repo_root / "output" / f"migration-report-{datetime.now().strftime('%Y%m%d')}.md"
        generate_migration_report(results, report_path)
        return

    if not args.type and not args.file:
        parser.print_help()
        return

    # Determine if we're doing dry run or execute
    dry_run = not args.execute
    if dry_run and not args.dry_run:
        print("⚠️  No --execute flag provided. Running in dry-run mode.")
        print("   Add --execute to actually write changes.\n")

    print(f"🚀 Migration Phase {args.phase}")
    print(f"   Mode: {'DRY RUN' if dry_run else 'EXECUTE'}")
    print()

    if args.file:
        # Migrate single file
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = repo_root / file_path

        if 'agents' in str(file_path):
            result = agent_migrator.migrate_agent(file_path, args.phase, dry_run)
        else:
            result = skill_migrator.migrate_skill(file_path, args.phase, dry_run)

        results.append(result)
    else:
        # Migrate by type
        if args.type in ['agents', 'all']:
            print("📦 Migrating agents...")
            agents = agent_migrator.get_all_agents()
            for agent in agents:
                result = agent_migrator.migrate_agent(agent, args.phase, dry_run)
                results.append(result)

                status_icon = '✅' if result['status'] in ['migrated', 'dry_run'] else '❌'
                print(f"   {status_icon} {result['file']}: {len(result['changes'])} changes")

        if args.type in ['skills', 'all']:
            print("\n📦 Migrating skills...")
            skills = skill_migrator.get_all_skills()
            for skill in skills:
                result = skill_migrator.migrate_skill(skill, args.phase, dry_run)
                results.append(result)

                status_icon = '✅' if result['status'] in ['migrated', 'dry_run'] else '❌'
                print(f"   {status_icon} {result['file']}: {len(result['changes'])} changes")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total = len(results)
    success = sum(1 for r in results if r['status'] in ['migrated', 'dry_run', 'no_changes'])
    errors = sum(1 for r in results if r['status'] == 'error')
    total_changes = sum(len(r['changes']) for r in results)

    print(f"Files processed: {total}")
    print(f"Successful: {success}")
    print(f"Errors: {errors}")
    print(f"Total changes: {total_changes}")

    if dry_run:
        print("\n💡 Run with --execute to apply these changes")
    else:
        print(f"\n✅ Changes applied. Backups saved to output/backups/")

    # Generate report
    report_path = repo_root / "output" / f"migration-report-phase{args.phase}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    generate_migration_report(results, report_path)


if __name__ == "__main__":
    main()
