#!/usr/bin/env python3
"""
Regenerate HOW_TO_USE.md files with actual skill-specific content

This script reads each SKILL.md file and generates a customized HOW_TO_USE.md
with real examples, actual Python tools, and concrete related skills.
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

def simple_yaml_parse(yaml_str: str) -> Dict:
    """Simple YAML parser for skill frontmatter"""
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
            # Top-level key
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

    # Save final list if any
    if current_key and list_items:
        if in_nested:
            nested_dict[current_key] = list_items
        else:
            result[current_key] = list_items

    # Save final nested dict if any
    if in_nested and nested_key:
        result[nested_key] = nested_dict

    return result

def extract_skill_metadata(skill_md_path: Path) -> Dict:
    """Extract metadata and content from SKILL.md"""
    content = skill_md_path.read_text()

    # Extract YAML frontmatter
    if not content.startswith('---'):
        return {}

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    yaml_content = parts[1]
    body_content = parts[2]

    metadata = simple_yaml_parse(yaml_content)

    # Extract description from Overview section
    overview_match = re.search(r'## Overview\n\n(.+?)(?=\n##|\Z)', body_content, re.DOTALL)
    overview = overview_match.group(1).strip() if overview_match else metadata.get('description', '')

    # Extract key workflows
    workflows = []
    workflow_section = re.search(r'## Key Workflows\n\n(.+?)(?=\n##|\Z)', body_content, re.DOTALL)
    if workflow_section:
        workflow_matches = re.findall(r'###\s+(.+?)\n', workflow_section.group(1))
        workflows = [w.strip() for w in workflow_matches[:3]]  # Take first 3

    return {
        'metadata': metadata,
        'overview': overview,
        'workflows': workflows,
        'body': body_content
    }

def get_python_tools(skill_path: Path) -> List[Tuple[str, str]]:
    """Get list of Python tools with descriptions"""
    scripts_dir = skill_path / 'scripts'
    if not scripts_dir.exists():
        return []

    tools = []
    for py_file in sorted(scripts_dir.glob('*.py')):
        # Read first few lines to get docstring
        try:
            content = py_file.read_text()
            docstring_match = re.search(r'"""(.+?)"""', content, re.DOTALL)
            if docstring_match:
                desc = docstring_match.group(1).strip().split('\n')[0]
            else:
                # Generate description from filename
                desc = py_file.stem.replace('_', ' ').title()
            tools.append((py_file.name, desc))
        except Exception:
            tools.append((py_file.name, py_file.stem.replace('_', ' ').title()))

    return tools

def get_related_skills(skill_path: Path, domain: str) -> List[Tuple[str, str]]:
    """Find related skills from same and adjacent domains"""
    skills_dir = skill_path.parent.parent
    related = []

    # Get all skills from same domain
    same_domain_skills = []
    if (skills_dir / domain).exists():
        for skill_dir in (skills_dir / domain).iterdir():
            if skill_dir.is_dir() and skill_dir != skill_path and (skill_dir / 'SKILL.md').exists():
                skill_name = skill_dir.name
                same_domain_skills.append((skill_name, f'../../{domain}/{skill_name}/'))

    # Take up to 3 from same domain
    related.extend(same_domain_skills[:3])

    # If we have less than 3, add from other domains
    if len(related) < 3:
        for team_dir in skills_dir.iterdir():
            if team_dir.is_dir() and team_dir.name != domain and not team_dir.name.startswith('.'):
                for skill_dir in team_dir.iterdir():
                    if skill_dir.is_dir() and (skill_dir / 'SKILL.md').exists():
                        skill_name = skill_dir.name
                        related.append((skill_name, f'../../{team_dir.name}/{skill_name}/'))
                        if len(related) >= 3:
                            break
            if len(related) >= 3:
                break

    return related[:3]

def clean_workflow_text(workflow: str) -> str:
    """Strip numbering and parenthetical from workflow titles"""
    # Remove leading 'Workflow N: ' (e.g., "Workflow 1: ")
    workflow = re.sub(r'^Workflow\s+\d+:\s+', '', workflow, flags=re.IGNORECASE)
    # Remove leading numbers and dots (e.g., "1. ")
    workflow = re.sub(r'^\d+\.\s+', '', workflow)
    # Remove parenthetical expressions (e.g., "(first time)")
    workflow = re.sub(r'\s*\([^)]*\)', '', workflow)
    return workflow.strip()

def generate_example_invocations(skill_name: str, workflows: List[str], overview: str) -> List[str]:
    """Generate realistic example invocations based on skill type"""
    examples = []

    # Generate skill-type-specific examples
    if 'review' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you review this pull request?')
    elif 'architect' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you help me design a scalable architecture?')
    elif 'security' in skill_name or 'secops' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you perform a security assessment?')
    elif 'data' in skill_name or 'analyst' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you analyze this dataset?')
    elif 'content' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you create SEO-optimized content?')
    elif 'jira' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you set up a custom workflow?')
    elif 'confluence' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you organize our documentation?')
    elif 'scrum' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you facilitate sprint planning?')
    elif 'qa' in skill_name or 'test' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you create a test strategy?')
    elif 'devops' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you set up a CI/CD pipeline?')
    elif 'marketing' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you plan a demand generation campaign?')
    elif 'product' in skill_name or 'pm' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you help prioritize features?')
    elif 'design' in skill_name or 'ux' in skill_name or 'ui' in skill_name:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you design a user-friendly interface?')
    else:
        # Generic fallback
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you analyze my current codebase?')

    # Example 2: From first workflow (cleaned)
    if workflows:
        workflow = clean_workflow_text(workflows[0].lower())
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you help me with {workflow}?')
    else:
        examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you provide a comprehensive analysis?')

    # Example 3: Integration
    examples.append(f'Hey Claude—I just added the "{skill_name}" skill. Can you use it together with related skills to deliver a complete solution?')

    return examples

def generate_what_to_provide(skill_name: str, overview: str) -> List[str]:
    """Generate what user should provide based on skill type"""
    items = []

    # Determine skill type from name/overview
    if 'data' in skill_name or 'analyst' in skill_name:
        items.append('**Dataset**: Your data files (CSV, JSON, Excel) or database connection details')
        items.append('**Context** (optional): Business objectives, key metrics of interest')
        items.append('**Constraints** (optional): Performance requirements, data privacy considerations')
    elif 'security' in skill_name or 'secops' in skill_name:
        items.append('**System Details**: Infrastructure overview, technology stack')
        items.append('**Context** (optional): Compliance requirements, threat model')
        items.append('**Scope** (optional): Specific areas to focus on, known vulnerabilities')
    elif 'architect' in skill_name:
        items.append('**Requirements**: Functional and non-functional requirements')
        items.append('**Context** (optional): Technical constraints, existing architecture')
        items.append('**Preferences** (optional): Technology preferences, scalability needs')
    elif 'frontend' in skill_name or 'backend' in skill_name or 'fullstack' in skill_name:
        items.append('**Codebase**: Link to repository or description of application')
        items.append('**Context** (optional): Project goals, technology stack')
        items.append('**Focus Areas** (optional): Specific features or problems to address')
    elif 'ml' in skill_name or 'ai' in skill_name or 'computer-vision' in skill_name:
        items.append('**Problem Statement**: What you want to achieve with ML/AI')
        items.append('**Dataset** (optional): Available data or data collection approach')
        items.append('**Constraints** (optional): Compute resources, latency requirements')
    elif 'qa' in skill_name or 'test' in skill_name:
        items.append('**Application Details**: What needs to be tested')
        items.append('**Context** (optional): Test coverage goals, known issues')
        items.append('**Preferences** (optional): Testing frameworks, automation level')
    elif 'devops' in skill_name or 'infrastructure' in skill_name:
        items.append('**Infrastructure Details**: Current setup, cloud provider')
        items.append('**Context** (optional): Scale requirements, budget constraints')
        items.append('**Goals** (optional): What you want to optimize or automate')
    elif 'product' in skill_name or 'pm' in skill_name:
        items.append('**Product Context**: Product vision, target users')
        items.append('**Goals** (optional): What you want to achieve')
        items.append('**Constraints** (optional): Timeline, resources, market conditions')
    elif 'design' in skill_name or 'ux' in skill_name or 'ui' in skill_name:
        items.append('**Design Problem**: What needs to be designed or improved')
        items.append('**Context** (optional): User research findings, brand guidelines')
        items.append('**Constraints** (optional): Technical limitations, timeline')
    elif 'content' in skill_name or 'marketing' in skill_name:
        items.append('**Content Brief**: Topic, audience, goals')
        items.append('**Brand Context** (optional): Brand voice, messaging guidelines')
        items.append('**Requirements** (optional): Length, format, SEO keywords')
    elif 'jira' in skill_name or 'confluence' in skill_name or 'scrum' in skill_name:
        items.append('**Project Context**: Team structure, workflow needs')
        items.append('**Current Setup** (optional): Existing configurations')
        items.append('**Goals** (optional): What you want to optimize')
    else:
        # Generic fallback
        items.append('**Primary Input**: Describe what you need help with')
        items.append('**Context** (optional): Background information, constraints')
        items.append('**Preferences** (optional): Specific approaches or requirements')

    return items

def generate_what_youll_get(skill_name: str, python_tools: List[Tuple[str, str]]) -> List[str]:
    """Generate what user will get from the skill"""
    items = []

    # Determine skill type
    if 'data' in skill_name or 'analyst' in skill_name:
        items.append('**Analysis Reports**: Statistical summaries, trend analysis, insights')
        items.append('**Visualizations**: Charts and graphs showing key findings')
        items.append('**Recommendations**: Data-driven action items')
    elif 'security' in skill_name or 'secops' in skill_name:
        items.append('**Security Assessment**: Vulnerability analysis, risk assessment')
        items.append('**Remediation Plan**: Prioritized action items with implementation guidance')
        items.append('**Compliance Report**: Gap analysis against security standards')
    elif 'architect' in skill_name:
        items.append('**Architecture Design**: System diagrams, component specifications')
        items.append('**Technical Documentation**: Architecture decision records (ADRs)')
        items.append('**Implementation Roadmap**: Phased approach with milestones')
    elif 'review' in skill_name:
        items.append('**Code Review**: Detailed analysis of code quality, patterns, issues')
        items.append('**Improvement Suggestions**: Specific recommendations with examples')
        items.append('**Best Practices**: Guidance on industry standards')
    elif 'ml' in skill_name or 'ai' in skill_name:
        items.append('**Model Recommendations**: Suggested algorithms and architectures')
        items.append('**Implementation Plan**: Step-by-step development approach')
        items.append('**Evaluation Strategy**: Metrics and validation approaches')
    elif 'qa' in skill_name:
        items.append('**Test Strategy**: Comprehensive testing approach')
        items.append('**Test Cases**: Specific test scenarios and acceptance criteria')
        items.append('**Automation Plan**: Framework recommendations and implementation guidance')
    elif 'devops' in skill_name:
        items.append('**Infrastructure Design**: CI/CD pipelines, deployment strategies')
        items.append('**Automation Scripts**: Configuration files, deployment scripts')
        items.append('**Monitoring Setup**: Observability and alerting recommendations')
    elif 'product' in skill_name:
        items.append('**Product Strategy**: Roadmap, prioritization, success metrics')
        items.append('**User Stories**: Well-defined requirements with acceptance criteria')
        items.append('**Documentation**: PRDs, specifications, stakeholder communications')
    elif 'design' in skill_name or 'ux' in skill_name or 'ui' in skill_name:
        items.append('**Design Deliverables**: Wireframes, mockups, prototypes')
        items.append('**User Flows**: Journey maps, interaction patterns')
        items.append('**Design System**: Components, patterns, guidelines')
    elif 'content' in skill_name or 'marketing' in skill_name:
        items.append('**Content**: Polished copy aligned with brand voice')
        items.append('**SEO Optimization**: Keyword integration, meta descriptions')
        items.append('**Performance Metrics**: Analytics setup and tracking recommendations')
    else:
        items.append('**Analysis**: Comprehensive evaluation of your request')
        items.append('**Recommendations**: Actionable guidance and best practices')
        items.append('**Deliverables**: Formatted outputs and documentation')

    # Add Python tools mention if they exist
    if python_tools:
        items.append(f'**Automated Tools**: {len(python_tools)} Python scripts for data processing and analysis')

    return items

def generate_how_to_use(skill_path: Path) -> str:
    """Generate customized HOW_TO_USE.md content"""
    skill_md_path = skill_path / 'SKILL.md'

    if not skill_md_path.exists():
        return None

    # Extract skill information
    skill_data = extract_skill_metadata(skill_md_path)
    if not skill_data:
        return None

    metadata = skill_data['metadata']
    skill_name = metadata.get('name', skill_path.name)
    # Use skill_path.parent.name for domain (e.g., "marketing-team", "engineering-team")
    domain = skill_path.parent.name
    skill_display = skill_name.replace('-', ' ').title()

    # Get Python tools
    python_tools = get_python_tools(skill_path)

    # Get related skills
    related_skills = get_related_skills(skill_path, domain)

    # Generate examples
    examples = generate_example_invocations(skill_name, skill_data['workflows'], skill_data['overview'])

    # Generate what to provide
    what_to_provide = generate_what_to_provide(skill_name, skill_data['overview'])

    # Generate what you'll get
    what_youll_get = generate_what_youll_get(skill_name, python_tools)

    # Build content
    content = f"""# How to Use the {skill_display} Skill

## Quick Start

{examples[0]}

## Example Invocations

### Example 1: Basic Usage
```
{examples[0]}
```

### Example 2: Specific Workflow
```
{examples[1]}
```

### Example 3: Integration with Other Skills
```
{examples[2]}
```

## What to Provide

When using this skill, provide:

"""

    for item in what_to_provide:
        content += f"- {item}\n"

    content += f"""
## What You'll Get

This skill will provide:

"""

    for item in what_youll_get:
        content += f"- {item}\n"

    # Python Tools section
    content += f"""
## Python Tools Available

"""

    if python_tools:
        content += "This skill includes the following Python tools:\n\n"
        for tool_name, tool_desc in python_tools:
            content += f"- **{tool_name}**: {tool_desc}\n"

        content += f"""
You can run these tools directly:

```bash
python skills/{domain}/{skill_name}/scripts/{python_tools[0][0]} --help
```
"""
    else:
        content += "This skill focuses on strategic guidance and frameworks rather than automated tools.\n"
        content += "The value comes from expert analysis, recommendations, and structured approaches.\n"

    # Tips section
    domain_display = domain.replace('-team', '').replace('-', ' ')
    content += f"""
## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements for better results
2. **Provide Context**: Include relevant background information about your project
3. **Iterate**: Start with a focused request, then refine based on initial results
4. **Combine Skills**: This skill works well with other {domain_display} skills for comprehensive solutions

## Related Skills

Consider using these skills together:

"""

    if related_skills:
        for related_name, related_path in related_skills:
            related_display = related_name.replace('-', ' ').title()
            content += f"- **[{related_display}]({related_path})**: Complementary expertise for {related_display.lower()} tasks\n"
    else:
        content += f"- Explore other skills in the {domain_display} domain for complementary capabilities\n"

    # Footer
    updated_date = metadata.get('metadata', {}).get('updated', datetime.now().strftime('%Y-%m-%d'))
    content += f"""
---

**Skill**: {skill_name}
**Domain**: {domain}
**Version**: 1.0.0
**Last Updated**: {updated_date}
"""

    return content

def main():
    """Main entry point"""
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / 'skills'

    print("Regenerating HOW_TO_USE.md files for all skills")
    print("=" * 60)
    print()

    updated_count = 0
    failed_count = 0

    # Find all skills
    for team_dir in skills_dir.iterdir():
        if not team_dir.is_dir() or team_dir.name.startswith('.'):
            continue

        for skill_dir in team_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            if not (skill_dir / 'SKILL.md').exists():
                continue

            skill_name = skill_dir.name
            print(f"Processing {team_dir.name}/{skill_name}...", end=' ')

            try:
                content = generate_how_to_use(skill_dir)
                if content:
                    how_to_use_path = skill_dir / 'HOW_TO_USE.md'
                    how_to_use_path.write_text(content)
                    print("✓ Updated")
                    updated_count += 1
                else:
                    print("✗ Failed (could not extract metadata)")
                    failed_count += 1
            except Exception as e:
                print(f"✗ Failed ({e})")
                failed_count += 1

    print()
    print("=" * 60)
    print(f"Results: {updated_count} updated, {failed_count} failed")
    print()

    if failed_count > 0:
        print("⚠️  Some files failed to update. Review errors above.")
        return 1
    else:
        print("✅ All HOW_TO_USE.md files successfully regenerated!")
        return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
