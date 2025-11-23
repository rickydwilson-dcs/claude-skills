#!/usr/bin/env python3
"""
Agent YAML Updater

Intelligently updates all 28 existing agents with new YAML fields:
- color: Agent type classification (blue, green, red, purple, orange)
- field: Primary domain focus (frontend, backend, product, etc.)
- expertise: Skill level (beginner, intermediate, expert)
- execution: Work pattern (parallel, coordinated, sequential)
- mcp_tools: MCP server integrations (github, playwright, atlassian)

Usage:
    python update_agent_yaml.py --dry-run  # Preview changes
    python update_agent_yaml.py            # Apply updates
    python update_agent_yaml.py --agent agents/marketing/cs-content-creator.md  # Update single agent
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse


class AgentYAMLUpdater:
    """Intelligent YAML updater for Claude Skills agents"""

    # Color assignment based on agent role
    COLOR_MAPPING = {
        # Strategic (Blue): Research, analysis, planning
        'blue': [
            'product-strategist', 'ceo-advisor', 'ux-researcher',
            'business-analyst', 'product-marketer'
        ],
        # Implementation (Green): Active development
        'green': [
            'backend-engineer', 'frontend-engineer', 'fullstack-engineer',
            'devops-engineer', 'ml-engineer', 'data-engineer', 'prompt-engineer'
        ],
        # Quality (Red): Testing, review, security
        'red': [
            'code-reviewer', 'qa-engineer', 'security-engineer', 'secops-engineer'
        ],
        # Coordination (Purple): Architecture, orchestration
        'purple': [
            'architect', 'cto-advisor', 'scrum-master', 'senior-pm',
            'agile-product-owner'
        ],
        # Domain (Orange): Specialized expertise
        'orange': [
            'content-creator', 'demand-gen-specialist', 'ui-designer',
            'data-scientist', 'computer-vision', 'confluence-expert', 'jira-expert'
        ]
    }

    # Field assignment based on agent name
    FIELD_MAPPING = {
        'code-reviewer': 'quality',
        'qa-engineer': 'testing',
        'security-engineer': 'security',
        'secops-engineer': 'security',
        'frontend-engineer': 'frontend',
        'backend-engineer': 'backend',
        'fullstack-engineer': 'fullstack',
        'product-strategist': 'product',
        'product-manager': 'product',
        'agile-product-owner': 'product',
        'senior-pm': 'product',
        'architect': 'architecture',
        'cto-advisor': 'architecture',
        'devops-engineer': 'devops',
        'data-engineer': 'data',
        'data-scientist': 'data',
        'ml-engineer': 'ai',
        'computer-vision': 'ai',
        'prompt-engineer': 'ai',
        'ui-designer': 'design',
        'ux-researcher': 'research',
        'content-creator': 'content',
        'demand-gen-specialist': 'content',
        'product-marketer': 'content',
        'business-analyst': 'product',
        'scrum-master': 'agile',
        'jira-expert': 'tools',
        'confluence-expert': 'tools',
        'ceo-advisor': 'strategy'
    }

    # MCP tools assignment
    MCP_MAPPING = {
        'code-reviewer': ['mcp__github'],
        'qa-engineer': ['mcp__github', 'mcp__playwright'],
        'security-engineer': ['mcp__github'],
        'jira-expert': ['mcp__atlassian'],
        'confluence-expert': ['mcp__atlassian'],
        'scrum-master': ['mcp__atlassian'],
        'agile-product-owner': ['mcp__atlassian'],
        'senior-pm': ['mcp__atlassian']
    }

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.stats = {
            'total': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0,
            'by_color': {},
            'by_field': {},
            'by_expertise': {},
            'by_execution': {}
        }

    def determine_color(self, agent_name: str, description: str) -> str:
        """Determine agent color based on name and description"""
        agent_slug = agent_name.replace('cs-', '')

        # Direct mapping
        for color, agents in self.COLOR_MAPPING.items():
            if agent_slug in agents:
                return color

        # Keyword-based fallback
        description_lower = description.lower()

        if any(word in description_lower for word in ['strategy', 'planning', 'research', 'analysis']):
            return 'blue'
        elif any(word in description_lower for word in ['engineer', 'development', 'implementation']):
            return 'green'
        elif any(word in description_lower for word in ['quality', 'testing', 'security', 'review']):
            return 'red'
        elif any(word in description_lower for word in ['architect', 'coordination', 'orchestrat']):
            return 'purple'
        else:
            return 'orange'

    def determine_field(self, agent_name: str) -> str:
        """Determine primary field based on agent name"""
        agent_slug = agent_name.replace('cs-', '')
        return self.FIELD_MAPPING.get(agent_slug, 'general')

    def determine_expertise(self, agent_name: str, description: str) -> str:
        """Determine expertise level"""
        description_lower = description.lower()

        # Check for explicit mentions
        if 'junior' in agent_name.lower() or 'beginner' in description_lower:
            return 'beginner'
        elif 'intermediate' in description_lower:
            return 'intermediate'
        else:
            # All current production agents are expert level
            return 'expert'

    def determine_execution(self, tools: List[str], agent_name: str) -> str:
        """Determine execution pattern based on tools and agent type"""
        agent_slug = agent_name.replace('cs-', '')

        # Quality agents run sequentially (heavy Bash usage)
        if agent_slug in ['code-reviewer', 'qa-engineer', 'security-engineer', 'secops-engineer']:
            return 'sequential'

        # Implementation agents use coordinated execution (active development)
        if agent_slug in ['backend-engineer', 'frontend-engineer', 'fullstack-engineer',
                          'devops-engineer', 'ml-engineer', 'data-engineer', 'prompt-engineer',
                          'computer-vision', 'data-scientist']:
            return 'coordinated'

        # Strategic, coordination, and domain-specific agents can run in parallel
        if agent_slug in ['product-strategist', 'ceo-advisor', 'ux-researcher',
                          'architect', 'cto-advisor', 'scrum-master', 'senior-pm',
                          'agile-product-owner', 'business-analyst', 'product-manager',
                          'content-creator', 'demand-gen-specialist', 'product-marketer',
                          'ui-designer', 'jira-expert', 'confluence-expert']:
            return 'parallel'

        # Default based on tool count
        if len(tools) >= 5:
            return 'coordinated'
        else:
            return 'parallel'

    def determine_mcp_tools(self, agent_name: str) -> List[str]:
        """Determine MCP tools for agent"""
        agent_slug = agent_name.replace('cs-', '')
        return self.MCP_MAPPING.get(agent_slug, [])

    def parse_yaml_frontmatter(self, content: str) -> Tuple[Optional[Dict], str, str]:
        """
        Parse YAML frontmatter from markdown file

        Returns:
            (yaml_dict, yaml_text, remaining_content)
        """
        # Match YAML frontmatter
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)

        if not match:
            return None, '', content

        yaml_text = match.group(1)
        remaining_content = match.group(2)

        try:
            # Simple YAML parser for our use case
            yaml_dict = {}
            for line in yaml_text.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Handle key-value pairs
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()

                    # Parse arrays [item1, item2]
                    if value.startswith('[') and value.endswith(']'):
                        # Remove brackets and split
                        value = value[1:-1].strip()
                        if value:
                            yaml_dict[key] = [item.strip() for item in value.split(',')]
                        else:
                            yaml_dict[key] = []
                    else:
                        yaml_dict[key] = value

            return yaml_dict, yaml_text, remaining_content
        except Exception as e:
            print(f"Warning: YAML parsing error: {e}")
            return None, yaml_text, remaining_content

    def update_yaml_fields(self, yaml_dict: Dict, yaml_text: str) -> Tuple[Dict, str]:
        """
        Add new fields to YAML dict and text

        Returns:
            (updated_dict, updated_text)
        """
        agent_name = yaml_dict.get('name', '')
        description = yaml_dict.get('description', '')
        tools = yaml_dict.get('tools', [])

        # Determine new fields
        new_fields = {
            'color': self.determine_color(agent_name, description),
            'field': self.determine_field(agent_name),
            'expertise': self.determine_expertise(agent_name, description),
            'execution': self.determine_execution(tools, agent_name),
            'mcp_tools': self.determine_mcp_tools(agent_name)
        }

        # Update dict
        updated_dict = yaml_dict.copy()
        updated_dict.update(new_fields)

        # Update text - add fields after tools
        lines = yaml_text.split('\n')
        new_lines = []
        tools_found = False

        for line in lines:
            new_lines.append(line)

            # Add new fields after tools line
            if line.startswith('tools:') and not tools_found:
                tools_found = True
                new_lines.append(f"color: {new_fields['color']}")
                new_lines.append(f"field: {new_fields['field']}")
                new_lines.append(f"expertise: {new_fields['expertise']}")
                new_lines.append(f"execution: {new_fields['execution']}")

                # Format mcp_tools as array
                if new_fields['mcp_tools']:
                    mcp_str = '[' + ', '.join(new_fields['mcp_tools']) + ']'
                else:
                    mcp_str = '[]'
                new_lines.append(f"mcp_tools: {mcp_str}")

        updated_text = '\n'.join(new_lines)

        # Update stats
        self.stats['by_color'][new_fields['color']] = self.stats['by_color'].get(new_fields['color'], 0) + 1
        self.stats['by_field'][new_fields['field']] = self.stats['by_field'].get(new_fields['field'], 0) + 1
        self.stats['by_expertise'][new_fields['expertise']] = self.stats['by_expertise'].get(new_fields['expertise'], 0) + 1
        self.stats['by_execution'][new_fields['execution']] = self.stats['by_execution'].get(new_fields['execution'], 0) + 1

        return updated_dict, updated_text

    def update_agent_file(self, file_path: Path) -> bool:
        """
        Update a single agent file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse YAML
            yaml_dict, yaml_text, remaining_content = self.parse_yaml_frontmatter(content)

            if yaml_dict is None:
                print(f"  ❌ No valid YAML frontmatter found")
                self.stats['errors'] += 1
                return False

            # Check if already updated
            if 'color' in yaml_dict:
                print(f"  ⏭️  Already updated (color field exists)")
                self.stats['skipped'] += 1
                return True

            # Update YAML
            updated_dict, updated_text = self.update_yaml_fields(yaml_dict, yaml_text)

            # Construct new content
            new_content = f"---\n{updated_text}\n---\n{remaining_content}"

            # Display changes
            print(f"  📝 New fields:")
            print(f"     Color: {updated_dict['color']}")
            print(f"     Field: {updated_dict['field']}")
            print(f"     Expertise: {updated_dict['expertise']}")
            print(f"     Execution: {updated_dict['execution']}")
            print(f"     MCP Tools: {updated_dict['mcp_tools']}")

            # Write file (if not dry run)
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ✅ Updated successfully")
            else:
                print(f"  🔍 Dry run - no changes written")

            self.stats['updated'] += 1
            return True

        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.stats['errors'] += 1
            return False

    def find_agent_files(self, base_path: Path) -> List[Path]:
        """Find all agent markdown files"""
        agent_files = []

        # Search in agents directory
        agents_dir = base_path / 'agents'

        if not agents_dir.exists():
            print(f"❌ Agents directory not found: {agents_dir}")
            return []

        # Find all .md files, excluding CLAUDE.md
        for md_file in agents_dir.rglob('*.md'):
            if md_file.name != 'CLAUDE.md':
                agent_files.append(md_file)

        return sorted(agent_files)

    def update_all_agents(self, base_path: Path, single_agent: Optional[Path] = None):
        """Update all agent files or a single agent"""

        if single_agent:
            print(f"\n🎯 Updating single agent: {single_agent.name}\n")
            print("=" * 80)
            self.stats['total'] = 1
            print(f"\n📄 {single_agent.name}")
            self.update_agent_file(single_agent)
        else:
            # Find all agent files
            agent_files = self.find_agent_files(base_path)

            if not agent_files:
                print("❌ No agent files found")
                return

            self.stats['total'] = len(agent_files)

            print(f"\n🚀 Agent YAML Updater")
            print("=" * 80)
            print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE UPDATE'}")
            print(f"Found {len(agent_files)} agent files\n")

            # Update each agent
            for agent_file in agent_files:
                print(f"\n📄 {agent_file.relative_to(base_path)}")
                self.update_agent_file(agent_file)

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print update summary"""
        print("\n" + "=" * 80)
        print("📊 Update Summary")
        print("=" * 80)

        print(f"\nTotal agents: {self.stats['total']}")
        print(f"  ✅ Updated: {self.stats['updated']}")
        print(f"  ⏭️  Skipped: {self.stats['skipped']}")
        print(f"  ❌ Errors: {self.stats['errors']}")

        if self.stats['by_color']:
            print(f"\n🎨 By Color:")
            for color, count in sorted(self.stats['by_color'].items()):
                emoji = {'blue': '🔵', 'green': '🟢', 'red': '🔴', 'purple': '🟣', 'orange': '🟠'}.get(color, '⚪')
                print(f"  {emoji} {color}: {count}")

        if self.stats['by_field']:
            print(f"\n🏷️  By Field:")
            for field, count in sorted(self.stats['by_field'].items()):
                print(f"  • {field}: {count}")

        if self.stats['by_expertise']:
            print(f"\n🎓 By Expertise:")
            for expertise, count in sorted(self.stats['by_expertise'].items()):
                print(f"  • {expertise}: {count}")

        if self.stats['by_execution']:
            print(f"\n⚙️  By Execution:")
            for execution, count in sorted(self.stats['by_execution'].items()):
                print(f"  • {execution}: {count}")

        if self.dry_run:
            print(f"\n⚠️  DRY RUN MODE - No changes written")
            print(f"   Run without --dry-run to apply updates")
        else:
            print(f"\n✅ Updates applied successfully")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Intelligently update agent YAML frontmatter with new fields',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes without writing
  python update_agent_yaml.py --dry-run

  # Apply updates to all agents
  python update_agent_yaml.py

  # Update single agent
  python update_agent_yaml.py --agent agents/marketing/cs-content-creator.md
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without writing files'
    )

    parser.add_argument(
        '--agent',
        type=str,
        help='Update a single agent file (path relative to repository root)'
    )

    args = parser.parse_args()

    # Determine base path (repository root)
    base_path = Path(__file__).parent.parent

    # Handle single agent update
    single_agent = None
    if args.agent:
        single_agent = base_path / args.agent
        if not single_agent.exists():
            print(f"❌ Agent file not found: {single_agent}")
            sys.exit(1)

    # Create updater and run
    updater = AgentYAMLUpdater(dry_run=args.dry_run)
    updater.update_all_agents(base_path, single_agent=single_agent)


if __name__ == '__main__':
    main()
