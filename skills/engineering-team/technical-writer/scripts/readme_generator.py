#!/usr/bin/env python3
"""
README Generator - Generates or updates README files with project statistics
"""

import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReadmeGenerator:
    def __init__(self, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("ReadmeGenerator initialized")

        # Project type indicators
        self.project_indicators = {
            'python': ['setup.py', 'pyproject.toml', 'requirements.txt', 'setup.cfg'],
            'nodejs': ['package.json', 'package-lock.json', 'yarn.lock'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.toml', 'Cargo.lock'],
            'ruby': ['Gemfile', 'Gemfile.lock'],
            'java': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
            'dotnet': ['*.csproj', '*.sln', '*.fsproj']
        }

        # File extensions to count as code
        self.code_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.go', '.rs', '.rb',
            '.java', '.cs', '.cpp', '.c', '.h', '.hpp', '.php', '.swift',
            '.kt', '.scala', '.sh', '.bash', '.zsh', '.fish'
        }

        # Files/dirs to ignore
        self.ignore_patterns = {
            '.git', '.svn', 'node_modules', '__pycache__', '.pytest_cache',
            'venv', '.venv', 'env', '.env', 'vendor', 'target', 'build',
            'dist', '.idea', '.vscode', '.DS_Store', 'coverage'
        }

    def detect_project_type(self, project_path: Path) -> Tuple[str, List[str]]:
        """Detect project type based on manifest files"""
        logger.debug(f"Detecting project type for: {project_path}")
        detected_types = []
        features = []

        for proj_type, indicators in self.project_indicators.items():
            for indicator in indicators:
                if '*' in indicator:
                    # Handle glob patterns
                    pattern = indicator
                    matches = list(project_path.glob(pattern))
                    if matches:
                        detected_types.append(proj_type)
                        features.append(indicator)
                        break
                else:
                    # Handle exact file names
                    if (project_path / indicator).exists():
                        detected_types.append(proj_type)
                        features.append(indicator)
                        break

        # Additional feature detection
        if (project_path / '.github' / 'workflows').exists():
            features.append('github-actions')

        if (project_path / 'pytest.ini').exists() or (project_path / 'setup.cfg').exists():
            features.append('pytest')

        if (project_path / 'Dockerfile').exists():
            features.append('docker')

        if (project_path / 'docker-compose.yml').exists():
            features.append('docker-compose')

        primary_type = detected_types[0] if detected_types else 'generic'
        logger.debug(f"Detected project type: {primary_type}, features: {features}")

        return primary_type, features

    def count_statistics(self, project_path: Path) -> Dict:
        """Count project statistics"""
        logger.debug(f"Counting statistics for: {project_path}")
        stats = {
            'total_files': 0,
            'total_lines': 0,
            'code_files': 0,
            'code_lines': 0,
            'agents': 0,
            'skills': 0,
            'commands': 0,
            'tests': 0,
            'docs': 0
        }

        # Check for claude-skills specific structure
        is_claude_skills = (project_path / 'agents').exists() and (project_path / 'skills').exists()

        if is_claude_skills:
            # Count agents
            agents_dir = project_path / 'agents'
            if agents_dir.exists():
                stats['agents'] = sum(1 for f in agents_dir.rglob('*.md') if f.is_file())

            # Count skills
            skills_dir = project_path / 'skills'
            if skills_dir.exists():
                stats['skills'] = sum(1 for d in skills_dir.rglob('SKILL.md') if d.is_file())

            # Count commands
            commands_dir = project_path / 'commands'
            if commands_dir.exists():
                stats['commands'] = sum(1 for f in commands_dir.rglob('*.md')
                                       if f.is_file() and f.name != 'README.md')

        # Count all files and lines
        for item in project_path.rglob('*'):
            # Skip ignored patterns
            if any(ignored in item.parts for ignored in self.ignore_patterns):
                continue

            if item.is_file():
                stats['total_files'] += 1

                # Count lines in text files
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        lines = sum(1 for _ in f)
                        stats['total_lines'] += lines

                        # Count code files
                        if item.suffix in self.code_extensions:
                            stats['code_files'] += 1
                            stats['code_lines'] += lines

                        # Count test files
                        if 'test' in item.name.lower() or 'spec' in item.name.lower():
                            stats['tests'] += 1

                        # Count documentation
                        if item.suffix in {'.md', '.rst', '.txt', '.adoc'}:
                            stats['docs'] += 1

                except (UnicodeDecodeError, PermissionError) as e:
                    # Skip binary files or files without read permission
                    logger.warning(f"Could not read file {item}: {e}")
                    pass

        logger.debug(f"Statistics: {stats['total_files']} files, {stats['total_lines']} lines")
        return stats

    def generate_badges(self, project_type: str, features: List[str]) -> List[str]:
        """Generate relevant badges for the project"""
        logger.debug(f"Generating badges for project type: {project_type}")
        badges = []

        # Language/framework badges
        badge_configs = {
            'python': ('Python', 'blue', 'https://www.python.org'),
            'nodejs': ('Node.js', 'green', 'https://nodejs.org'),
            'go': ('Go', 'blue', 'https://golang.org'),
            'rust': ('Rust', 'orange', 'https://www.rust-lang.org'),
        }

        if project_type in badge_configs:
            name, color, url = badge_configs[project_type]
            badges.append(f'![{name}](https://img.shields.io/badge/{name}-{color})')

        # Feature badges
        if 'github-actions' in features:
            badges.append('![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue)')

        if 'docker' in features:
            badges.append('![Docker](https://img.shields.io/badge/Docker-enabled-blue)')

        if 'pytest' in features:
            badges.append('![Tests](https://img.shields.io/badge/Tests-pytest-green)')

        # Generic badges
        badges.append('![License](https://img.shields.io/badge/License-MIT-green)')

        return badges

    def generate_stats_section(self, stats: Dict) -> str:
        """Generate statistics section"""
        lines = [
            '<!-- STATS_START -->',
            '## 📊 Project Statistics',
            '',
        ]

        # General stats
        if stats['total_files'] > 0:
            lines.extend([
                f"- **Total Files:** {stats['total_files']:,}",
                f"- **Total Lines:** {stats['total_lines']:,}",
            ])

        if stats['code_files'] > 0:
            lines.extend([
                f"- **Code Files:** {stats['code_files']:,}",
                f"- **Code Lines:** {stats['code_lines']:,}",
            ])

        # Claude-skills specific stats
        if stats['agents'] > 0:
            lines.append(f"- **Production Agents:** {stats['agents']}")

        if stats['skills'] > 0:
            lines.append(f"- **Skills:** {stats['skills']}")

        if stats['commands'] > 0:
            lines.append(f"- **Commands:** {stats['commands']}")

        # Other stats
        if stats['tests'] > 0:
            lines.append(f"- **Test Files:** {stats['tests']}")

        if stats['docs'] > 0:
            lines.append(f"- **Documentation Files:** {stats['docs']}")

        lines.extend(['', '<!-- STATS_END -->', ''])

        return '\n'.join(lines)

    def generate_installation_section(self, project_type: str) -> str:
        """Generate installation instructions"""
        lines = ['## 🚀 Installation', '']

        install_configs = {
            'python': [
                '```bash',
                '# Clone the repository',
                'git clone <repository-url>',
                'cd <project-name>',
                '',
                '# Create virtual environment',
                'python3 -m venv venv',
                'source venv/bin/activate  # On Windows: venv\\Scripts\\activate',
                '',
                '# Install dependencies',
                'pip install -r requirements.txt',
                '```'
            ],
            'nodejs': [
                '```bash',
                '# Clone the repository',
                'git clone <repository-url>',
                'cd <project-name>',
                '',
                '# Install dependencies',
                'npm install',
                '# or',
                'yarn install',
                '```'
            ],
            'go': [
                '```bash',
                '# Clone the repository',
                'git clone <repository-url>',
                'cd <project-name>',
                '',
                '# Install dependencies',
                'go mod download',
                '',
                '# Build',
                'go build',
                '```'
            ],
            'rust': [
                '```bash',
                '# Clone the repository',
                'git clone <repository-url>',
                'cd <project-name>',
                '',
                '# Build',
                'cargo build --release',
                '```'
            ],
            'generic': [
                '```bash',
                '# Clone the repository',
                'git clone <repository-url>',
                'cd <project-name>',
                '',
                '# Follow project-specific setup instructions',
                '```'
            ]
        }

        install_steps = install_configs.get(project_type, install_configs['generic'])
        lines.extend(install_steps)
        lines.append('')

        return '\n'.join(lines)

    def generate_usage_section(self, project_type: str) -> str:
        """Generate usage examples"""
        lines = ['## 💡 Usage', '']

        usage_configs = {
            'python': [
                '```python',
                '# Basic usage example',
                'from your_module import YourClass',
                '',
                'instance = YourClass()',
                'result = instance.method()',
                'print(result)',
                '```'
            ],
            'nodejs': [
                '```javascript',
                '// Basic usage example',
                'const { YourClass } = require(\'./your-module\');',
                '',
                'const instance = new YourClass();',
                'const result = instance.method();',
                'console.log(result);',
                '```'
            ],
            'generic': [
                '```bash',
                '# Example usage',
                './your-command --help',
                '```'
            ]
        }

        usage_steps = usage_configs.get(project_type, usage_configs['generic'])
        lines.extend(usage_steps)
        lines.append('')

        return '\n'.join(lines)

    def generate_api_section(self) -> str:
        """Generate API reference placeholder"""
        return '\n'.join([
            '## 📚 API Reference',
            '',
            '### Main Classes',
            '',
            '#### `YourClass`',
            '',
            'Description of your main class.',
            '',
            '**Methods:**',
            '',
            '- `method()` - Description of method',
            '',
            ''
        ])

    def parse_existing_readme(self, readme_path: Path) -> Dict[str, str]:
        """Parse existing README and extract sections"""
        if not readme_path.exists():
            return {}

        content = readme_path.read_text(encoding='utf-8')
        sections = {}

        # Extract content between custom markers
        custom_pattern = r'<!-- CUSTOM_START -->(.*?)<!-- CUSTOM_END -->'
        custom_matches = re.findall(custom_pattern, content, re.DOTALL)

        for i, match in enumerate(custom_matches):
            sections[f'custom_{i}'] = match

        # Extract stats section
        stats_pattern = r'<!-- STATS_START -->(.*?)<!-- STATS_END -->'
        stats_match = re.search(stats_pattern, content, re.DOTALL)
        if stats_match:
            sections['stats'] = stats_match.group(1)

        return sections

    def generate_readme(self, project_path: Path, template: str = 'standard',
                       sections: List[str] = None, merge: bool = False) -> str:
        """Generate complete README content"""
        logger.debug(f"Generating README with template: {template}")

        if sections is None:
            sections = ['all']

        # Detect project type
        project_type, features = self.detect_project_type(project_path)

        # Collect statistics
        stats = self.count_statistics(project_path)

        # Start building README
        lines = []

        # Title
        project_name = project_path.name
        lines.extend([
            f'# {project_name}',
            '',
            'Project description goes here.',
            '',
        ])

        # Badges (if standard or comprehensive)
        if template in ['standard', 'comprehensive']:
            badges = self.generate_badges(project_type, features)
            if badges:
                lines.extend(badges)
                lines.append('')

        # Stats section
        if 'all' in sections or 'stats' in sections:
            lines.append(self.generate_stats_section(stats))

        # Features section
        if template in ['standard', 'comprehensive']:
            lines.extend([
                '## ✨ Features',
                '',
                '- Feature 1',
                '- Feature 2',
                '- Feature 3',
                '',
            ])

        # Installation
        if 'all' in sections or 'install' in sections:
            lines.append(self.generate_installation_section(project_type))

        # Usage
        if 'all' in sections or 'usage' in sections:
            lines.append(self.generate_usage_section(project_type))

        # API Reference (comprehensive only)
        if template == 'comprehensive' and ('all' in sections or 'api' in sections):
            lines.append(self.generate_api_section())

        # Contributing section
        if template in ['standard', 'comprehensive']:
            lines.extend([
                '## 🤝 Contributing',
                '',
                'Contributions are welcome! Please feel free to submit a Pull Request.',
                '',
                '1. Fork the repository',
                '2. Create your feature branch (`git checkout -b feature/AmazingFeature`)',
                '3. Commit your changes (`git commit -m \'Add some AmazingFeature\'`)',
                '4. Push to the branch (`git push origin feature/AmazingFeature`)',
                '5. Open a Pull Request',
                '',
            ])

        # License section
        if template in ['standard', 'comprehensive']:
            lines.extend([
                '## 📄 License',
                '',
                'This project is licensed under the MIT License - see the LICENSE file for details.',
                '',
            ])

        # Footer
        lines.extend([
            '---',
            '',
            f'*Generated by readme_generator.py on {datetime.now().strftime("%Y-%m-%d")}*',
            ''
        ])

        return '\n'.join(lines)

    def merge_readme(self, project_path: Path, new_content: str) -> str:
        """Merge new content with existing README, preserving custom sections"""
        logger.debug("Merging with existing README")
        readme_path = project_path / 'README.md'

        if not readme_path.exists():
            logger.warning("No existing README found to merge with")
            return new_content

        existing_content = readme_path.read_text(encoding='utf-8')

        # Replace stats section if it exists
        stats_pattern = r'<!-- STATS_START -->.*?<!-- STATS_END -->'
        if re.search(stats_pattern, existing_content, re.DOTALL):
            # Extract stats from new content
            stats_match = re.search(stats_pattern, new_content, re.DOTALL)
            if stats_match:
                new_stats = stats_match.group(0)
                existing_content = re.sub(stats_pattern, new_stats, existing_content, flags=re.DOTALL)

        return existing_content


def generate_readme_file(project_path: str, template: str = 'standard',
                        sections: List[str] = None, merge: bool = False,
                        dry_run: bool = False, output_file: str = 'README.md',
                        output_format: str = 'text', verbose: bool = False) -> str:
    """Main function to generate README"""
    logger.debug(f"Starting README generation for: {project_path}")
    generator = ReadmeGenerator(verbose=verbose)

    project_path = Path(project_path).resolve()

    if not project_path.exists():
        logger.error(f"Project path not found: {project_path}")
        raise FileNotFoundError(f"Project path not found: {project_path}")

    if not project_path.is_dir():
        logger.error(f"Path is not a directory: {project_path}")
        raise NotADirectoryError(f"Path is not a directory: {project_path}")

    # Detect project
    project_type, features = generator.detect_project_type(project_path)

    # Collect stats
    stats = generator.count_statistics(project_path)

    # Generate README content
    if merge:
        readme_content = generator.generate_readme(project_path, template, sections, merge)
        readme_content = generator.merge_readme(project_path, readme_content)
    else:
        readme_content = generator.generate_readme(project_path, template, sections)

    # Prepare output
    if output_format == 'json':
        result = {
            'project_type': project_type,
            'detected_features': features,
            'stats': stats,
            'sections_generated': sections if sections else ['all'],
            'output_file': output_file,
            'dry_run': dry_run
        }
        return json.dumps(result, indent=2)

    # Text format - show preview or write
    if dry_run:
        output = [
            "📝 README Preview (Dry Run)",
            "=" * 50,
            "",
            readme_content,
            "",
            "=" * 50,
            f"✅ Preview complete. Use without --dry-run to write to {output_file}"
        ]
        return '\n'.join(output)

    # Write to file
    output_path = project_path / output_file
    output_path.write_text(readme_content, encoding='utf-8')

    output = [
        f"📊 Project Analysis:",
        f"  Type: {project_type}",
        f"  Features: {', '.join(features) if features else 'None detected'}",
        "",
        f"📈 Statistics:",
        f"  Files: {stats['total_files']:,}",
        f"  Lines: {stats['total_lines']:,}",
    ]

    if stats['agents'] > 0:
        output.append(f"  Agents: {stats['agents']}")
    if stats['skills'] > 0:
        output.append(f"  Skills: {stats['skills']}")
    if stats['commands'] > 0:
        output.append(f"  Commands: {stats['commands']}")

    output.extend([
        "",
        f"✅ README generated: {output_path}",
        ""
    ])

    return '\n'.join(output)


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='README generator with project statistics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate standard README
  %(prog)s /path/to/project

  # Generate with specific template
  %(prog)s /path/to/project --template comprehensive

  # Update only stats section
  %(prog)s /path/to/project --sections stats --merge

  # Preview without writing
  %(prog)s /path/to/project --dry-run

  # JSON output
  %(prog)s /path/to/project --format json

For more information, see the skill documentation.
        """
    )

    # Required arguments
    parser.add_argument(
        'path',
        help='Project directory to analyze'
    )

    # Optional arguments
    parser.add_argument(
        '--template', '-t',
        choices=['minimal', 'standard', 'comprehensive'],
        default='standard',
        help='Template style (default: standard)'
    )

    parser.add_argument(
        '--sections', '-s',
        choices=['stats', 'install', 'usage', 'api', 'all'],
        nargs='+',
        default=['all'],
        help='Specific sections to generate/update (default: all)'
    )

    parser.add_argument(
        '--merge', '-m',
        action='store_true',
        help='Merge with existing README (preserve custom content)'
    )

    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Preview without writing'
    )

    parser.add_argument(
        '--output', '-o',
        default='README.md',
        help='Output file (default: README.md)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json'],
        default='text',
        help='Output format: text (default) or json'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output with detailed information'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    try:
        # Verbose logging
        if args.verbose:
            print(f"🔍 Analyzing project: {args.path}", file=sys.stderr)
            print(f"   Template: {args.template}", file=sys.stderr)
            print(f"   Sections: {', '.join(args.sections)}", file=sys.stderr)
            print(f"   Merge mode: {args.merge}", file=sys.stderr)
            print(f"   Dry run: {args.dry_run}", file=sys.stderr)
            print("", file=sys.stderr)

        # Generate README
        output = generate_readme_file(
            args.path,
            template=args.template,
            sections=args.sections,
            merge=args.merge,
            dry_run=args.dry_run,
            output_file=args.output,
            output_format=args.format,
            verbose=args.verbose
        )

        print(output)
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    except NotADirectoryError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    except PermissionError as e:
        print(f"❌ Error: Permission denied: {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"❌ Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
