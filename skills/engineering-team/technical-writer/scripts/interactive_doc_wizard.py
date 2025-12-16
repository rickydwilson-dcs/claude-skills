#!/usr/bin/env python3
"""
Interactive Documentation Wizard - Guided workflows for documentation creation

This tool provides step-by-step interactive wizards for creating various
types of documentation including README files, API docs, changelogs,
documentation audits, and user guides.

Usage:
    python interactive_doc_wizard.py                    # Interactive menu
    python interactive_doc_wizard.py --workflow readme  # Start specific workflow
    python interactive_doc_wizard.py --config file.yaml # Non-interactive mode
    python interactive_doc_wizard.py --help             # Show help

Features:
    - 5 interactive workflows (readme, api-docs, changelog, audit, user-guide)
    - Project auto-detection (language, framework, tests, CI)
    - Multiple output formats (markdown, html, json)
    - Config file mode for automation
    - Dry-run mode for previewing output

ARCHITECTURE NOTE - Single-File Design:
    This script is intentionally monolithic for portability.
    Users can extract this single file and run it anywhere with Python 3.8+.

    Code is organized into logical sections:

    SECTION 1: Configuration & Constants
    SECTION 2: Utility Functions
    SECTION 3: Input Prompting (InteractivePrompter)
    SECTION 4: Project Detection (ProjectDetector)
    SECTION 5: Workflow Definitions
    SECTION 6: Output Generation (DocumentGenerator)
    SECTION 7: Wizard Orchestrator (InteractiveDocWizard)
    SECTION 8: CLI Entry Point
"""

# ============================================================================
# SECTION 1: CONFIGURATION & CONSTANTS
# ============================================================================
# Import statements, exit codes, workflow types, and language defaults

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime


# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_VALIDATION_ERROR = 2
EXIT_USER_CANCELLED = 130

# Version
VERSION = "1.0.0"

# Workflow type definitions
WORKFLOW_TYPES: Dict[str, Dict[str, Any]] = {
    'readme': {
        'name': 'README Generator',
        'description': 'Interactive README creation with project analysis',
        'steps': 8,
        'time_estimate': '10-15 minutes'
    },
    'api-docs': {
        'name': 'API Documentation',
        'description': 'Generate API reference from code or specs',
        'steps': 10,
        'time_estimate': '15-20 minutes'
    },
    'changelog': {
        'name': 'CHANGELOG Generator',
        'description': 'Create changelog from git history',
        'steps': 6,
        'time_estimate': '5-10 minutes'
    },
    'audit': {
        'name': 'Documentation Audit',
        'description': 'Quality assessment of existing documentation',
        'steps': 7,
        'time_estimate': '10-15 minutes'
    },
    'user-guide': {
        'name': 'User Guide Creator',
        'description': 'Interactive user guide generation',
        'steps': 12,
        'time_estimate': '20-30 minutes'
    }
}

# Language-specific defaults for project detection
LANGUAGE_DEFAULTS: Dict[str, Dict[str, str]] = {
    'python': {
        'package_manager': 'pip',
        'install_command': 'pip install {package}',
        'test_command': 'pytest',
        'config_format': 'yaml',
        'code_fence': 'python'
    },
    'javascript': {
        'package_manager': 'npm',
        'install_command': 'npm install {package}',
        'test_command': 'npm test',
        'config_format': 'json',
        'code_fence': 'javascript'
    },
    'typescript': {
        'package_manager': 'npm',
        'install_command': 'npm install {package}',
        'test_command': 'npm test',
        'config_format': 'json',
        'code_fence': 'typescript'
    },
    'go': {
        'package_manager': 'go',
        'install_command': 'go install {package}@latest',
        'test_command': 'go test ./...',
        'config_format': 'yaml',
        'code_fence': 'go'
    },
    'rust': {
        'package_manager': 'cargo',
        'install_command': 'cargo install {package}',
        'test_command': 'cargo test',
        'config_format': 'toml',
        'code_fence': 'rust'
    },
    'java': {
        'package_manager': 'maven',
        'install_command': 'mvn install',
        'test_command': 'mvn test',
        'config_format': 'xml',
        'code_fence': 'java'
    },
    'ruby': {
        'package_manager': 'gem',
        'install_command': 'gem install {package}',
        'test_command': 'rake test',
        'config_format': 'yaml',
        'code_fence': 'ruby'
    }
}

# Framework detection patterns
FRAMEWORK_PATTERNS: Dict[str, Dict[str, List[str]]] = {
    'python': {
        'fastapi': ['fastapi', 'uvicorn'],
        'django': ['django'],
        'flask': ['flask'],
        'pytest': ['pytest'],
    },
    'javascript': {
        'react': ['react', 'react-dom'],
        'nextjs': ['next'],
        'express': ['express'],
        'vue': ['vue'],
        'angular': ['@angular/core'],
    },
    'typescript': {
        'nestjs': ['@nestjs/core'],
        'nextjs': ['next'],
        'express': ['express', '@types/express'],
    }
}


# ============================================================================
# SECTION 2: UTILITY FUNCTIONS
# ============================================================================
# Display helpers, input sanitization, and path validation


def print_banner(title: str, description: str, time_estimate: str) -> None:
    """Display workflow start banner with title and description."""
    width = 60
    print()
    print("=" * width)
    print(f"  {title}")
    print(f"  {description}")
    print(f"  Estimated time: {time_estimate}")
    print("=" * width)
    print()


def print_progress(current: int, total: int, step_title: str) -> None:
    """Display step progress indicator."""
    bar_width = 20
    filled = int(bar_width * current / total)
    bar = "#" * filled + "-" * (bar_width - filled)
    print()
    print("-" * 60)
    print(f"Step {current}/{total}: {step_title}  [{bar}]")
    print("-" * 60)
    print()


def print_success(message: str) -> None:
    """Display success message with checkmark."""
    print(f"[+] {message}")


def print_error(message: str) -> None:
    """Display error message with indicator."""
    print(f"[!] Error: {message}", file=sys.stderr)


def print_info(message: str) -> None:
    """Display informational message."""
    print(f"[*] {message}")


def print_warning(message: str) -> None:
    """Display warning message."""
    print(f"[~] Warning: {message}")


def sanitize_input(text: str) -> str:
    """Clean and normalize user input."""
    if not text:
        return ""
    return text.strip()


def validate_path(path_str: str, must_exist: bool = True) -> Optional[Path]:
    """
    Validate a file or directory path.

    Returns Path object if valid, None otherwise.
    """
    if not path_str:
        return None

    path = Path(path_str).expanduser().resolve()

    if must_exist and not path.exists():
        return None

    return path


def read_file_safe(path: Path) -> Optional[str]:
    """Safely read file contents, return None on error."""
    try:
        return path.read_text(encoding='utf-8')
    except (IOError, OSError, UnicodeDecodeError):
        return None


def write_file_safe(path: Path, content: str) -> bool:
    """Safely write content to file, return success status."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return True
    except (IOError, OSError):
        return False


def format_list(items: List[str], numbered: bool = False) -> str:
    """Format a list of items for display."""
    if not items:
        return "(none)"

    if numbered:
        return "\n".join(f"  {i+1}. {item}" for i, item in enumerate(items))
    return "\n".join(f"  - {item}" for item in items)


# ============================================================================
# SECTION 3: INPUT PROMPTING
# ============================================================================
# InteractivePrompter class for handling all user input types


class InteractivePrompter:
    """Handle interactive user prompts with validation."""

    def prompt_text(
        self,
        prompt: str,
        default: Optional[str] = None,
        required: bool = True,
        validation: Optional[Callable[[str], bool]] = None,
        error_msg: str = "Invalid input"
    ) -> str:
        """
        Prompt for single-line text input.

        Args:
            prompt: The prompt message to display
            default: Default value if user presses Enter
            required: Whether input is required
            validation: Optional validation function
            error_msg: Error message if validation fails

        Returns:
            User input string
        """
        default_hint = f" [{default}]" if default else ""
        full_prompt = f"{prompt}{default_hint}: "

        while True:
            try:
                response = input(full_prompt)
                value = sanitize_input(response)

                # Use default if empty
                if not value and default:
                    return default

                # Check required
                if required and not value:
                    print_error("This field is required")
                    continue

                # Run validation
                if validation and value and not validation(value):
                    print_error(error_msg)
                    continue

                return value

            except EOFError:
                return default or ""

    def prompt_choice(
        self,
        prompt: str,
        choices: List[str],
        default: Optional[int] = None
    ) -> str:
        """
        Prompt for single choice from numbered menu.

        Args:
            prompt: The prompt message
            choices: List of choices to display
            default: Default choice index (1-based)

        Returns:
            Selected choice string
        """
        print(f"\n{prompt}")
        for i, choice in enumerate(choices, 1):
            marker = "*" if default == i else " "
            print(f"  {marker}{i}. {choice}")

        default_hint = f" [{default}]" if default else ""

        while True:
            try:
                response = input(f"Select option{default_hint}: ")
                value = sanitize_input(response)

                # Use default if empty
                if not value and default:
                    return choices[default - 1]

                # Parse selection
                try:
                    selection = int(value)
                    if 1 <= selection <= len(choices):
                        return choices[selection - 1]
                except ValueError:
                    pass

                print_error(f"Please enter a number between 1 and {len(choices)}")

            except EOFError:
                if default:
                    return choices[default - 1]
                return choices[0]

    def prompt_multiselect(
        self,
        prompt: str,
        choices: List[str],
        defaults: Optional[List[int]] = None,
        min_selections: int = 0
    ) -> List[str]:
        """
        Prompt for multiple selections.

        Args:
            prompt: The prompt message
            choices: List of choices to display
            defaults: Default selections (1-based indices)
            min_selections: Minimum required selections

        Returns:
            List of selected choice strings
        """
        defaults = defaults or []

        print(f"\n{prompt}")
        for i, choice in enumerate(choices, 1):
            marker = "*" if i in defaults else " "
            print(f"  {marker}{i}. {choice}")

        print("\n(Enter numbers separated by spaces, or 'all' for all)")
        default_str = ",".join(str(d) for d in defaults) if defaults else ""
        default_hint = f" [{default_str}]" if default_str else ""

        while True:
            try:
                response = input(f"Select options{default_hint}: ")
                value = sanitize_input(response)

                # Use defaults if empty
                if not value and defaults:
                    return [choices[i - 1] for i in defaults]

                # Handle 'all'
                if value.lower() == 'all':
                    return choices.copy()

                # Parse selections
                try:
                    selections = []
                    for part in value.replace(',', ' ').split():
                        num = int(part)
                        if 1 <= num <= len(choices):
                            if choices[num - 1] not in selections:
                                selections.append(choices[num - 1])

                    if len(selections) >= min_selections:
                        return selections

                    print_error(f"Please select at least {min_selections} option(s)")

                except ValueError:
                    print_error("Please enter valid numbers separated by spaces")

            except EOFError:
                if defaults:
                    return [choices[i - 1] for i in defaults]
                return []

    def prompt_path(
        self,
        prompt: str,
        default: Optional[str] = None,
        must_exist: bool = True,
        path_type: str = 'any'  # 'file', 'dir', 'any'
    ) -> Optional[Path]:
        """
        Prompt for file or directory path.

        Args:
            prompt: The prompt message
            default: Default path string
            must_exist: Whether path must exist
            path_type: Expected path type ('file', 'dir', 'any')

        Returns:
            Validated Path object or None
        """
        default_hint = f" [{default}]" if default else ""
        hint = "(use . for current directory)" if path_type == 'dir' else ""

        if hint:
            print(hint)

        while True:
            try:
                response = input(f"{prompt}{default_hint}: ")
                value = sanitize_input(response)

                # Use default if empty
                if not value and default:
                    value = default

                if not value:
                    print_error("Path is required")
                    continue

                path = validate_path(value, must_exist=must_exist)

                if path is None:
                    print_error(f"Path does not exist: {value}")
                    continue

                # Check path type
                if path_type == 'file' and not path.is_file():
                    print_error("Expected a file path")
                    continue

                if path_type == 'dir' and not path.is_dir():
                    print_error("Expected a directory path")
                    continue

                return path

            except EOFError:
                if default:
                    return validate_path(default, must_exist=must_exist)
                return None

    def prompt_confirm(
        self,
        prompt: str,
        default: bool = True
    ) -> bool:
        """
        Prompt for yes/no confirmation.

        Args:
            prompt: The prompt message
            default: Default value

        Returns:
            Boolean confirmation result
        """
        hint = "[Y/n]" if default else "[y/N]"

        while True:
            try:
                response = input(f"{prompt} {hint}: ")
                value = sanitize_input(response).lower()

                if not value:
                    return default

                if value in ('y', 'yes'):
                    return True
                if value in ('n', 'no'):
                    return False

                print_error("Please enter 'y' or 'n'")

            except EOFError:
                return default

    def prompt_multiline(
        self,
        prompt: str,
        end_marker: str = ""
    ) -> List[str]:
        """
        Prompt for multi-line input.

        Args:
            prompt: The prompt message
            end_marker: Text to indicate end (empty line by default)

        Returns:
            List of input lines
        """
        print(f"\n{prompt}")
        print("(Enter one item per line, empty line when done)")

        lines = []
        count = 1

        while True:
            try:
                response = input(f"  {count}. ")
                value = sanitize_input(response)

                if not value:
                    break

                lines.append(value)
                count += 1

            except EOFError:
                break

        return lines


# ============================================================================
# SECTION 4: PROJECT DETECTION
# ============================================================================
# ProjectDetector class for analyzing project structure


class ProjectDetector:
    """Detect project characteristics from file system."""

    def __init__(self, project_path: Path):
        """Initialize detector with project path."""
        self.path = project_path
        self.results: Dict[str, Any] = {}

    def detect_language(self) -> Optional[str]:
        """
        Identify primary programming language.

        Returns:
            Language name or None
        """
        # Check for language-specific files
        patterns = {
            'python': ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile'],
            'javascript': ['package.json'],
            'typescript': ['tsconfig.json'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.toml'],
            'java': ['pom.xml', 'build.gradle'],
            'ruby': ['Gemfile', 'Rakefile'],
        }

        for lang, files in patterns.items():
            for filename in files:
                if (self.path / filename).exists():
                    return lang

        # Count file extensions as fallback
        ext_counts: Dict[str, int] = {}
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.rb': 'ruby',
        }

        for file in self.path.rglob('*'):
            if file.is_file() and not self._is_ignored(file):
                ext = file.suffix.lower()
                if ext in ext_to_lang:
                    lang = ext_to_lang[ext]
                    ext_counts[lang] = ext_counts.get(lang, 0) + 1

        if ext_counts:
            return max(ext_counts, key=ext_counts.get)

        return None

    def detect_framework(self, language: str) -> Optional[str]:
        """
        Identify framework based on dependencies.

        Args:
            language: Primary language of project

        Returns:
            Framework name or None
        """
        if language not in FRAMEWORK_PATTERNS:
            return None

        deps = self._get_dependencies(language)
        if not deps:
            return None

        for framework, markers in FRAMEWORK_PATTERNS[language].items():
            if any(marker in deps for marker in markers):
                return framework

        return None

    def detect_package_manager(self, language: str) -> str:
        """
        Identify package manager for language.

        Args:
            language: Primary language

        Returns:
            Package manager name
        """
        if language in LANGUAGE_DEFAULTS:
            return LANGUAGE_DEFAULTS[language]['package_manager']
        return 'unknown'

    def detect_tests(self) -> bool:
        """
        Check if project has test setup.

        Returns:
            True if tests detected
        """
        test_indicators = [
            'tests', 'test', '__tests__', 'spec', 'specs',
            'pytest.ini', 'jest.config.js', 'jest.config.ts',
            '.pytest_cache', 'coverage', '.coverage'
        ]

        for indicator in test_indicators:
            if (self.path / indicator).exists():
                return True

        # Check for test files
        test_patterns = ['**/test_*.py', '**/*_test.py', '**/*.test.js', '**/*.spec.ts']
        for pattern in test_patterns:
            if list(self.path.glob(pattern)):
                return True

        return False

    def detect_ci(self) -> Optional[str]:
        """
        Check for CI/CD configuration.

        Returns:
            CI system name or None
        """
        ci_files = {
            '.github/workflows': 'GitHub Actions',
            '.gitlab-ci.yml': 'GitLab CI',
            'Jenkinsfile': 'Jenkins',
            '.circleci/config.yml': 'CircleCI',
            '.travis.yml': 'Travis CI',
            'azure-pipelines.yml': 'Azure Pipelines',
        }

        for path, ci_name in ci_files.items():
            if (self.path / path).exists():
                return ci_name

        return None

    def detect_existing_readme(self) -> bool:
        """Check if README already exists."""
        readme_names = ['README.md', 'README.rst', 'README.txt', 'README']
        return any((self.path / name).exists() for name in readme_names)

    def analyze_project(self) -> Dict[str, Any]:
        """
        Run all detections and return results.

        Returns:
            Dictionary with all detection results
        """
        language = self.detect_language()

        self.results = {
            'language': language,
            'framework': self.detect_framework(language) if language else None,
            'package_manager': self.detect_package_manager(language) if language else 'unknown',
            'has_tests': self.detect_tests(),
            'ci_system': self.detect_ci(),
            'has_readme': self.detect_existing_readme(),
            'project_name': self.path.name,
        }

        # Add language defaults if available
        if language and language in LANGUAGE_DEFAULTS:
            self.results['defaults'] = LANGUAGE_DEFAULTS[language]

        return self.results

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored."""
        ignore_patterns = [
            'node_modules', '__pycache__', '.git', '.venv', 'venv',
            'dist', 'build', '.tox', '.pytest_cache', '.mypy_cache'
        ]
        return any(pattern in str(path) for pattern in ignore_patterns)

    def _get_dependencies(self, language: str) -> List[str]:
        """Get list of dependencies for language."""
        deps = []

        if language in ('javascript', 'typescript'):
            pkg_json = self.path / 'package.json'
            if pkg_json.exists():
                try:
                    data = json.loads(pkg_json.read_text())
                    deps.extend(data.get('dependencies', {}).keys())
                    deps.extend(data.get('devDependencies', {}).keys())
                except (json.JSONDecodeError, IOError):
                    pass

        elif language == 'python':
            req_txt = self.path / 'requirements.txt'
            if req_txt.exists():
                content = read_file_safe(req_txt)
                if content:
                    for line in content.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Extract package name
                            pkg = re.split(r'[<>=!~\[]', line)[0].strip()
                            if pkg:
                                deps.append(pkg.lower())

        return deps


# ============================================================================
# SECTION 5: WORKFLOW DEFINITIONS
# ============================================================================
# Workflow step dataclass and individual workflow classes


@dataclass
class WorkflowStep:
    """Definition of a single workflow step."""
    id: str
    title: str
    description: str
    input_type: str  # 'text', 'choice', 'multiselect', 'path', 'confirm', 'multiline', 'auto'
    required: bool = True
    default: Optional[Any] = None
    choices: List[str] = field(default_factory=list)
    validation: Optional[str] = None
    skip_condition: Optional[str] = None
    help_text: str = ""


class BaseWorkflow:
    """Base class for all workflows."""

    def __init__(self):
        self.context: Dict[str, Any] = {}
        self.prompter = InteractivePrompter()

    def get_steps(self) -> List[WorkflowStep]:
        """Return list of workflow steps. Override in subclass."""
        raise NotImplementedError

    def execute_step(self, step: WorkflowStep) -> Any:
        """Execute a single workflow step."""
        if step.help_text:
            print(f"  {step.help_text}")

        if step.input_type == 'text':
            return self.prompter.prompt_text(
                step.description,
                default=step.default,
                required=step.required
            )

        elif step.input_type == 'choice':
            return self.prompter.prompt_choice(
                step.description,
                step.choices,
                default=step.choices.index(step.default) + 1 if step.default in step.choices else None
            )

        elif step.input_type == 'multiselect':
            return self.prompter.prompt_multiselect(
                step.description,
                step.choices
            )

        elif step.input_type == 'path':
            return self.prompter.prompt_path(
                step.description,
                default=step.default,
                path_type='dir' if 'directory' in step.description.lower() else 'any'
            )

        elif step.input_type == 'confirm':
            return self.prompter.prompt_confirm(
                step.description,
                default=step.default if step.default is not None else True
            )

        elif step.input_type == 'multiline':
            return self.prompter.prompt_multiline(step.description)

        elif step.input_type == 'auto':
            return self._execute_auto_step(step)

        return None

    def _execute_auto_step(self, step: WorkflowStep) -> Any:
        """Execute automatic step. Override in subclass."""
        return None

    def should_skip_step(self, step: WorkflowStep) -> bool:
        """Check if step should be skipped based on context."""
        if not step.skip_condition:
            return False

        # Simple condition evaluation
        condition = step.skip_condition

        # Handle negation
        if condition.startswith('not '):
            key = condition[4:]
            return bool(self.context.get(key))

        return not bool(self.context.get(condition))

    def generate_output(self) -> str:
        """Generate output from collected context. Override in subclass."""
        raise NotImplementedError


class ReadmeWorkflow(BaseWorkflow):
    """README generation workflow - 8 steps."""

    def get_steps(self) -> List[WorkflowStep]:
        """Return README workflow steps."""
        return [
            WorkflowStep(
                id='project_path',
                title='Project Location',
                description='Enter the path to your project directory',
                input_type='path',
                default='.',
                help_text='Use . for current directory'
            ),
            WorkflowStep(
                id='project_name',
                title='Project Name',
                description='Project name',
                input_type='text',
                help_text='This will be the main heading of your README'
            ),
            WorkflowStep(
                id='description',
                title='Project Description',
                description='One-line description (max 100 chars)',
                input_type='text',
                required=True
            ),
            WorkflowStep(
                id='features',
                title='Key Features',
                description='List the main features of your project',
                input_type='multiline',
                help_text='Enter one feature per line'
            ),
            WorkflowStep(
                id='installation_type',
                title='Installation Method',
                description='How should users install this project?',
                input_type='choice',
                choices=['Package manager (npm/pip/etc)', 'From source', 'Docker', 'Binary download'],
                default='Package manager (npm/pip/etc)'
            ),
            WorkflowStep(
                id='has_cli',
                title='CLI Interface',
                description='Does this project have a command-line interface?',
                input_type='confirm',
                default=False
            ),
            WorkflowStep(
                id='sections',
                title='README Sections',
                description='Select sections to include',
                input_type='multiselect',
                choices=[
                    'Installation',
                    'Usage',
                    'API Reference',
                    'Configuration',
                    'Contributing',
                    'Testing',
                    'License',
                    'Changelog'
                ],
                default=[1, 2, 5, 7]  # Installation, Usage, Contributing, License
            ),
            WorkflowStep(
                id='confirm_generate',
                title='Generate README',
                description='Generate README with these settings?',
                input_type='confirm',
                default=True
            )
        ]

    def _execute_auto_step(self, step: WorkflowStep) -> Any:
        """Execute automatic project detection."""
        if step.id == 'detect_project':
            project_path = self.context.get('project_path')
            if project_path:
                detector = ProjectDetector(project_path)
                return detector.analyze_project()
        return None

    def generate_output(self) -> str:
        """Generate README content from context."""
        lines = []

        # Title and description
        name = self.context.get('project_name', 'Project')
        desc = self.context.get('description', '')

        lines.append(f"# {name}")
        lines.append("")
        if desc:
            lines.append(desc)
            lines.append("")

        # Features
        features = self.context.get('features', [])
        if features:
            lines.append("## Features")
            lines.append("")
            for feature in features:
                lines.append(f"- {feature}")
            lines.append("")

        # Selected sections
        sections = self.context.get('sections', [])

        if 'Installation' in sections:
            lines.extend(self._generate_installation_section())

        if 'Usage' in sections:
            lines.extend(self._generate_usage_section())

        if 'API Reference' in sections:
            lines.append("## API Reference")
            lines.append("")
            lines.append("*API documentation goes here*")
            lines.append("")

        if 'Configuration' in sections:
            lines.append("## Configuration")
            lines.append("")
            lines.append("*Configuration options go here*")
            lines.append("")

        if 'Testing' in sections:
            lines.extend(self._generate_testing_section())

        if 'Contributing' in sections:
            lines.append("## Contributing")
            lines.append("")
            lines.append("Contributions are welcome! Please read the contributing guidelines first.")
            lines.append("")

        if 'License' in sections:
            lines.append("## License")
            lines.append("")
            lines.append("MIT")
            lines.append("")

        if 'Changelog' in sections:
            lines.append("## Changelog")
            lines.append("")
            lines.append("See [CHANGELOG.md](CHANGELOG.md) for release history.")
            lines.append("")

        return "\n".join(lines)

    def _generate_installation_section(self) -> List[str]:
        """Generate installation section."""
        lines = ["## Installation", ""]

        install_type = self.context.get('installation_type', '')
        detection = self.context.get('detection', {})
        pkg_mgr = detection.get('package_manager', 'npm')
        name = self.context.get('project_name', 'package')

        if 'Package manager' in install_type:
            if pkg_mgr == 'pip':
                lines.append("```bash")
                lines.append(f"pip install {name}")
                lines.append("```")
            elif pkg_mgr in ('npm', 'yarn'):
                lines.append("```bash")
                lines.append(f"npm install {name}")
                lines.append("# or")
                lines.append(f"yarn add {name}")
                lines.append("```")
            else:
                lines.append("```bash")
                lines.append(f"# Install using your package manager")
                lines.append("```")

        elif 'source' in install_type.lower():
            lines.append("```bash")
            lines.append("git clone https://github.com/user/repo.git")
            lines.append("cd repo")
            lines.append("# Follow build instructions")
            lines.append("```")

        elif 'Docker' in install_type:
            lines.append("```bash")
            lines.append(f"docker pull {name}")
            lines.append(f"docker run -it {name}")
            lines.append("```")

        lines.append("")
        return lines

    def _generate_usage_section(self) -> List[str]:
        """Generate usage section."""
        lines = ["## Usage", ""]

        has_cli = self.context.get('has_cli', False)
        detection = self.context.get('detection', {})
        lang = detection.get('language', 'javascript')
        fence = LANGUAGE_DEFAULTS.get(lang, {}).get('code_fence', 'bash')

        if has_cli:
            lines.append("### Command Line")
            lines.append("")
            lines.append("```bash")
            lines.append(f"# Basic usage")
            lines.append(f"{self.context.get('project_name', 'tool')} --help")
            lines.append("```")
            lines.append("")

        lines.append("### Basic Example")
        lines.append("")
        lines.append(f"```{fence}")
        lines.append("// Your example code here")
        lines.append("```")
        lines.append("")

        return lines

    def _generate_testing_section(self) -> List[str]:
        """Generate testing section."""
        lines = ["## Testing", ""]

        detection = self.context.get('detection', {})
        lang = detection.get('language', 'javascript')
        test_cmd = LANGUAGE_DEFAULTS.get(lang, {}).get('test_command', 'npm test')

        lines.append("```bash")
        lines.append(test_cmd)
        lines.append("```")
        lines.append("")

        return lines


class ChangelogWorkflow(BaseWorkflow):
    """CHANGELOG generation workflow - 6 steps."""

    def get_steps(self) -> List[WorkflowStep]:
        """Return CHANGELOG workflow steps."""
        return [
            WorkflowStep(
                id='project_path',
                title='Project Location',
                description='Enter the path to your project directory',
                input_type='path',
                default='.'
            ),
            WorkflowStep(
                id='version',
                title='Version',
                description='Version number for this release',
                input_type='text',
                default='1.0.0'
            ),
            WorkflowStep(
                id='format',
                title='Format Style',
                description='Changelog format to use',
                input_type='choice',
                choices=['Keep a Changelog', 'Conventional Commits', 'Simple'],
                default='Keep a Changelog'
            ),
            WorkflowStep(
                id='categories',
                title='Change Categories',
                description='Select categories to include',
                input_type='multiselect',
                choices=['Added', 'Changed', 'Deprecated', 'Removed', 'Fixed', 'Security'],
                default=[1, 2, 5]  # Added, Changed, Fixed
            ),
            WorkflowStep(
                id='changes',
                title='Changes',
                description='List the changes for this release',
                input_type='multiline'
            ),
            WorkflowStep(
                id='confirm_generate',
                title='Generate CHANGELOG',
                description='Generate CHANGELOG with these settings?',
                input_type='confirm',
                default=True
            )
        ]

    def generate_output(self) -> str:
        """Generate CHANGELOG content from context."""
        lines = []

        format_style = self.context.get('format', 'Keep a Changelog')
        version = self.context.get('version', '1.0.0')
        date = datetime.now().strftime('%Y-%m-%d')

        lines.append("# Changelog")
        lines.append("")

        if 'Keep a Changelog' in format_style:
            lines.append("All notable changes to this project will be documented in this file.")
            lines.append("")
            lines.append("The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),")
            lines.append("and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).")
            lines.append("")

        lines.append(f"## [{version}] - {date}")
        lines.append("")

        categories = self.context.get('categories', [])
        changes = self.context.get('changes', [])

        # For simplicity, put all changes under "Changed"
        if changes:
            if 'Changed' in categories:
                lines.append("### Changed")
                lines.append("")
                for change in changes:
                    lines.append(f"- {change}")
                lines.append("")

        return "\n".join(lines)


class AuditWorkflow(BaseWorkflow):
    """Documentation audit workflow - 7 steps."""

    def get_steps(self) -> List[WorkflowStep]:
        """Return audit workflow steps."""
        return [
            WorkflowStep(
                id='scope_path',
                title='Scope',
                description='Path to documentation to audit',
                input_type='path',
                default='.'
            ),
            WorkflowStep(
                id='scope_type',
                title='Scope Type',
                description='What should be audited?',
                input_type='choice',
                choices=['Full project', 'Documentation folder', 'README only', 'API docs only'],
                default='Full project'
            ),
            WorkflowStep(
                id='criteria',
                title='Audit Criteria',
                description='Select quality criteria to check',
                input_type='multiselect',
                choices=['Structure', 'Completeness', 'Readability', 'Links', 'Code examples', 'Formatting'],
                default=[1, 2, 4]  # Structure, Completeness, Links
            ),
            WorkflowStep(
                id='threshold',
                title='Quality Threshold',
                description='Minimum quality score (0-100)',
                input_type='text',
                default='75'
            ),
            WorkflowStep(
                id='run_audit',
                title='Run Audit',
                description='Running documentation audit...',
                input_type='auto'
            ),
            WorkflowStep(
                id='output_format',
                title='Report Format',
                description='Output format for audit report',
                input_type='choice',
                choices=['Markdown', 'JSON', 'Text'],
                default='Markdown'
            ),
            WorkflowStep(
                id='confirm_generate',
                title='Generate Report',
                description='Generate audit report?',
                input_type='confirm',
                default=True
            )
        ]

    def _execute_auto_step(self, step: WorkflowStep) -> Any:
        """Execute automatic audit step."""
        if step.id == 'run_audit':
            print_info("Analyzing documentation...")
            # Simplified audit - count markdown files and check for common issues
            scope_path = self.context.get('scope_path')
            if scope_path:
                results = self._run_simple_audit(scope_path)
                self.context['audit_results'] = results
                return results
        return None

    def _run_simple_audit(self, path: Path) -> Dict[str, Any]:
        """Run a simple documentation audit."""
        results = {
            'total_files': 0,
            'markdown_files': 0,
            'issues': [],
            'score': 0
        }

        md_files = list(path.rglob('*.md'))
        results['markdown_files'] = len(md_files)

        # Check for common files
        if not (path / 'README.md').exists():
            results['issues'].append('Missing README.md')
        if not (path / 'CHANGELOG.md').exists():
            results['issues'].append('Missing CHANGELOG.md')

        # Simple scoring
        base_score = 70
        if (path / 'README.md').exists():
            base_score += 15
        if (path / 'CHANGELOG.md').exists():
            base_score += 10
        if len(md_files) > 5:
            base_score += 5

        results['score'] = min(100, base_score)

        return results

    def generate_output(self) -> str:
        """Generate audit report from context."""
        lines = []

        audit_results = self.context.get('audit_results', {})
        output_format = self.context.get('output_format', 'Markdown')

        if output_format == 'JSON':
            return json.dumps(audit_results, indent=2)

        lines.append("# Documentation Audit Report")
        lines.append("")
        lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Score:** {audit_results.get('score', 0)}/100")
        lines.append("")

        lines.append("## Summary")
        lines.append("")
        lines.append(f"- Markdown files found: {audit_results.get('markdown_files', 0)}")
        lines.append("")

        issues = audit_results.get('issues', [])
        if issues:
            lines.append("## Issues Found")
            lines.append("")
            for issue in issues:
                lines.append(f"- {issue}")
            lines.append("")
        else:
            lines.append("## Issues Found")
            lines.append("")
            lines.append("No issues found!")
            lines.append("")

        return "\n".join(lines)


class ApiDocsWorkflow(BaseWorkflow):
    """API documentation workflow - 10 steps."""

    def get_steps(self) -> List[WorkflowStep]:
        """Return API docs workflow steps."""
        return [
            WorkflowStep(
                id='source_type',
                title='API Source',
                description='Where should API documentation come from?',
                input_type='choice',
                choices=['OpenAPI/Swagger spec', 'Source code', 'Manual entry'],
                default='Manual entry'
            ),
            WorkflowStep(
                id='source_path',
                title='Source Path',
                description='Path to OpenAPI spec or source code',
                input_type='path',
                default='.',
                skip_condition='manual_entry'
            ),
            WorkflowStep(
                id='api_name',
                title='API Name',
                description='Name of your API',
                input_type='text'
            ),
            WorkflowStep(
                id='base_url',
                title='Base URL',
                description='API base URL',
                input_type='text',
                default='https://api.example.com'
            ),
            WorkflowStep(
                id='version',
                title='API Version',
                description='API version',
                input_type='text',
                default='v1'
            ),
            WorkflowStep(
                id='auth_type',
                title='Authentication',
                description='Authentication method',
                input_type='choice',
                choices=['None', 'API Key', 'Bearer Token', 'OAuth2', 'Basic Auth'],
                default='Bearer Token'
            ),
            WorkflowStep(
                id='endpoints',
                title='Endpoints',
                description='List API endpoints (e.g., GET /users)',
                input_type='multiline'
            ),
            WorkflowStep(
                id='include_examples',
                title='Include Examples',
                description='Include request/response examples?',
                input_type='confirm',
                default=True
            ),
            WorkflowStep(
                id='example_languages',
                title='Example Languages',
                description='Select languages for code examples',
                input_type='multiselect',
                choices=['curl', 'JavaScript', 'Python', 'Go', 'Ruby'],
                default=[1, 2, 3],  # curl, JavaScript, Python
                skip_condition='not include_examples'
            ),
            WorkflowStep(
                id='confirm_generate',
                title='Generate API Docs',
                description='Generate API documentation?',
                input_type='confirm',
                default=True
            )
        ]

    def generate_output(self) -> str:
        """Generate API documentation from context."""
        lines = []

        api_name = self.context.get('api_name', 'API')
        base_url = self.context.get('base_url', 'https://api.example.com')
        version = self.context.get('version', 'v1')
        auth_type = self.context.get('auth_type', 'None')

        lines.append(f"# {api_name} Documentation")
        lines.append("")
        lines.append(f"**Base URL:** `{base_url}/{version}`")
        lines.append("")

        # Authentication section
        lines.append("## Authentication")
        lines.append("")
        if auth_type == 'Bearer Token':
            lines.append("This API uses Bearer token authentication.")
            lines.append("")
            lines.append("Include the token in the Authorization header:")
            lines.append("```")
            lines.append("Authorization: Bearer YOUR_TOKEN")
            lines.append("```")
        elif auth_type == 'API Key':
            lines.append("This API uses API key authentication.")
            lines.append("")
            lines.append("Include the API key in the header:")
            lines.append("```")
            lines.append("X-API-Key: YOUR_API_KEY")
            lines.append("```")
        elif auth_type == 'None':
            lines.append("This API does not require authentication.")
        lines.append("")

        # Endpoints section
        endpoints = self.context.get('endpoints', [])
        if endpoints:
            lines.append("## Endpoints")
            lines.append("")
            for endpoint in endpoints:
                lines.append(f"### {endpoint}")
                lines.append("")
                lines.append("*Description goes here*")
                lines.append("")

                if self.context.get('include_examples'):
                    lines.append("**Example Request:**")
                    lines.append("")
                    lines.append("```bash")
                    if endpoint.startswith('GET'):
                        path = endpoint.replace('GET ', '')
                        lines.append(f"curl {base_url}/{version}{path}")
                    else:
                        lines.append(f"# {endpoint}")
                    lines.append("```")
                    lines.append("")

        return "\n".join(lines)


class UserGuideWorkflow(BaseWorkflow):
    """User guide creation workflow - 12 steps."""

    def get_steps(self) -> List[WorkflowStep]:
        """Return user guide workflow steps."""
        return [
            WorkflowStep(
                id='product_name',
                title='Product Name',
                description='Name of the product/project',
                input_type='text'
            ),
            WorkflowStep(
                id='product_type',
                title='Product Type',
                description='What type of product is this?',
                input_type='choice',
                choices=['CLI Tool', 'Web Application', 'Library/SDK', 'Desktop Application', 'API'],
                default='CLI Tool'
            ),
            WorkflowStep(
                id='target_audience',
                title='Target Audience',
                description='Who is this guide for?',
                input_type='choice',
                choices=['Developers', 'End Users', 'System Administrators', 'All Users'],
                default='Developers'
            ),
            WorkflowStep(
                id='guide_sections',
                title='Guide Sections',
                description='Select sections to include',
                input_type='multiselect',
                choices=[
                    'Introduction',
                    'Getting Started',
                    'Installation',
                    'Quick Start',
                    'Core Concepts',
                    'Tutorials',
                    'Reference',
                    'Troubleshooting',
                    'FAQ',
                    'Glossary'
                ],
                default=[1, 2, 3, 4]  # Introduction, Getting Started, Installation, Quick Start
            ),
            WorkflowStep(
                id='prerequisites',
                title='Prerequisites',
                description='List any prerequisites',
                input_type='multiline'
            ),
            WorkflowStep(
                id='quick_start_steps',
                title='Quick Start Steps',
                description='List quick start steps',
                input_type='multiline'
            ),
            WorkflowStep(
                id='include_tutorials',
                title='Include Tutorials',
                description='Include tutorial section?',
                input_type='confirm',
                default=False
            ),
            WorkflowStep(
                id='tutorial_count',
                title='Number of Tutorials',
                description='How many tutorials to include?',
                input_type='choice',
                choices=['1', '2', '3', '4', '5'],
                default='2',
                skip_condition='not include_tutorials'
            ),
            WorkflowStep(
                id='tutorial_topics',
                title='Tutorial Topics',
                description='List tutorial topics',
                input_type='multiline',
                skip_condition='not include_tutorials'
            ),
            WorkflowStep(
                id='common_issues',
                title='Common Issues',
                description='List common issues and solutions',
                input_type='multiline'
            ),
            WorkflowStep(
                id='faq_items',
                title='FAQ Items',
                description='List frequently asked questions',
                input_type='multiline'
            ),
            WorkflowStep(
                id='confirm_generate',
                title='Generate User Guide',
                description='Generate user guide?',
                input_type='confirm',
                default=True
            )
        ]

    def generate_output(self) -> str:
        """Generate user guide from context."""
        lines = []

        product_name = self.context.get('product_name', 'Product')
        sections = self.context.get('guide_sections', [])

        lines.append(f"# {product_name} User Guide")
        lines.append("")

        if 'Introduction' in sections:
            lines.append("## Introduction")
            lines.append("")
            lines.append(f"Welcome to the {product_name} user guide.")
            lines.append("")

        if 'Getting Started' in sections:
            lines.append("## Getting Started")
            lines.append("")
            prereqs = self.context.get('prerequisites', [])
            if prereqs:
                lines.append("### Prerequisites")
                lines.append("")
                for prereq in prereqs:
                    lines.append(f"- {prereq}")
                lines.append("")

        if 'Installation' in sections:
            lines.append("## Installation")
            lines.append("")
            lines.append("*Installation instructions go here*")
            lines.append("")

        if 'Quick Start' in sections:
            lines.append("## Quick Start")
            lines.append("")
            steps = self.context.get('quick_start_steps', [])
            if steps:
                for i, step in enumerate(steps, 1):
                    lines.append(f"{i}. {step}")
                lines.append("")
            else:
                lines.append("*Quick start steps go here*")
                lines.append("")

        if 'Core Concepts' in sections:
            lines.append("## Core Concepts")
            lines.append("")
            lines.append("*Core concepts explanation goes here*")
            lines.append("")

        if 'Tutorials' in sections and self.context.get('include_tutorials'):
            lines.append("## Tutorials")
            lines.append("")
            topics = self.context.get('tutorial_topics', [])
            for topic in topics:
                lines.append(f"### {topic}")
                lines.append("")
                lines.append("*Tutorial content goes here*")
                lines.append("")

        if 'Reference' in sections:
            lines.append("## Reference")
            lines.append("")
            lines.append("*Reference documentation goes here*")
            lines.append("")

        if 'Troubleshooting' in sections:
            lines.append("## Troubleshooting")
            lines.append("")
            issues = self.context.get('common_issues', [])
            if issues:
                for issue in issues:
                    lines.append(f"### {issue}")
                    lines.append("")
                    lines.append("*Solution goes here*")
                    lines.append("")
            else:
                lines.append("*Troubleshooting information goes here*")
                lines.append("")

        if 'FAQ' in sections:
            lines.append("## FAQ")
            lines.append("")
            faqs = self.context.get('faq_items', [])
            if faqs:
                for faq in faqs:
                    lines.append(f"**Q: {faq}**")
                    lines.append("")
                    lines.append("A: *Answer goes here*")
                    lines.append("")
            else:
                lines.append("*FAQ items go here*")
                lines.append("")

        if 'Glossary' in sections:
            lines.append("## Glossary")
            lines.append("")
            lines.append("*Glossary terms go here*")
            lines.append("")

        return "\n".join(lines)


# ============================================================================
# SECTION 6: OUTPUT GENERATION
# ============================================================================
# DocumentGenerator class for final output formatting


class DocumentGenerator:
    """Generate formatted documentation output."""

    def __init__(self, output_format: str = 'markdown'):
        """Initialize generator with output format."""
        self.format = output_format.lower()

    def generate(self, workflow: BaseWorkflow) -> str:
        """Generate output from workflow."""
        content = workflow.generate_output()

        if self.format == 'html':
            return self._to_html(content)
        elif self.format == 'json':
            return self._to_json(workflow.context)

        return content

    def _to_html(self, markdown_content: str) -> str:
        """Convert markdown to basic HTML."""
        lines = ["<!DOCTYPE html>", "<html>", "<head>",
                 "<meta charset='utf-8'>",
                 "<style>body{font-family:system-ui;max-width:800px;margin:0 auto;padding:20px;}</style>",
                 "</head>", "<body>"]

        for line in markdown_content.split('\n'):
            if line.startswith('# '):
                lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith('## '):
                lines.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith('### '):
                lines.append(f"<h3>{line[4:]}</h3>")
            elif line.startswith('- '):
                lines.append(f"<li>{line[2:]}</li>")
            elif line.startswith('```'):
                lines.append("<pre><code>" if "```" == line else "</code></pre>")
            elif line:
                lines.append(f"<p>{line}</p>")

        lines.extend(["</body>", "</html>"])
        return "\n".join(lines)

    def _to_json(self, context: Dict[str, Any]) -> str:
        """Convert context to JSON output."""
        # Filter out non-serializable items
        safe_context = {}
        for key, value in context.items():
            if isinstance(value, (str, int, float, bool, list, dict, type(None))):
                safe_context[key] = value
            elif isinstance(value, Path):
                safe_context[key] = str(value)

        return json.dumps(safe_context, indent=2)


# ============================================================================
# SECTION 7: WIZARD ORCHESTRATOR
# ============================================================================
# InteractiveDocWizard class for workflow orchestration


class InteractiveDocWizard:
    """Main orchestrator for interactive documentation workflows."""

    WORKFLOWS = {
        'readme': ReadmeWorkflow,
        'api-docs': ApiDocsWorkflow,
        'changelog': ChangelogWorkflow,
        'audit': AuditWorkflow,
        'user-guide': UserGuideWorkflow,
    }

    def __init__(self, verbose: bool = False, output_format: str = 'markdown'):
        """Initialize wizard."""
        self.verbose = verbose
        self.output_format = output_format
        self.prompter = InteractivePrompter()

    def show_workflow_menu(self) -> Optional[str]:
        """Display workflow selection menu and return choice."""
        print()
        print("=" * 60)
        print("  Interactive Documentation Wizard")
        print("=" * 60)
        print()
        print("Available workflows:")
        print()

        choices = []
        for key, info in WORKFLOW_TYPES.items():
            choices.append(f"{info['name']} ({info['time_estimate']})")
            print(f"  {len(choices)}. {info['name']}")
            print(f"     {info['description']}")
            print(f"     Steps: {info['steps']}, Time: {info['time_estimate']}")
            print()

        choices.append("Exit")

        selection = self.prompter.prompt_choice(
            "Select a workflow:",
            choices
        )

        if selection == "Exit":
            return None

        # Map selection back to workflow key
        for key, info in WORKFLOW_TYPES.items():
            if info['name'] in selection:
                return key

        return None

    def run_workflow(self, workflow_type: str, output_path: Optional[Path] = None,
                     dry_run: bool = False) -> int:
        """
        Execute selected workflow.

        Args:
            workflow_type: Type of workflow to run
            output_path: Optional path to write output
            dry_run: If True, show output but don't write file

        Returns:
            Exit code
        """
        if workflow_type not in self.WORKFLOWS:
            print_error(f"Unknown workflow type: {workflow_type}")
            return EXIT_ERROR

        workflow_info = WORKFLOW_TYPES[workflow_type]
        workflow_class = self.WORKFLOWS[workflow_type]
        workflow = workflow_class()

        # Display banner
        print_banner(
            workflow_info['name'],
            workflow_info['description'],
            workflow_info['time_estimate']
        )

        # Get steps
        steps = workflow.get_steps()
        total_steps = len(steps)

        # Execute each step
        for i, step in enumerate(steps, 1):
            # Check skip condition
            if workflow.should_skip_step(step):
                if self.verbose:
                    print_info(f"Skipping step: {step.title}")
                continue

            # Show progress
            print_progress(i, total_steps, step.title)

            # Execute step
            try:
                result = workflow.execute_step(step)
                workflow.context[step.id] = result

                # Handle auto-detection results
                if step.id == 'project_path' and result:
                    detector = ProjectDetector(result)
                    detection = detector.analyze_project()
                    workflow.context['detection'] = detection

                    # Show detection results
                    print()
                    print_info("Project analysis:")
                    print(f"  Language: {detection.get('language', 'Unknown')}")
                    print(f"  Framework: {detection.get('framework', 'None detected')}")
                    print(f"  Tests: {'Yes' if detection.get('has_tests') else 'No'}")
                    print(f"  CI/CD: {detection.get('ci_system', 'None detected')}")

                    # Update defaults based on detection
                    if not workflow.context.get('project_name'):
                        workflow.context['project_name'] = detection.get('project_name', 'project')

                # Check for cancel
                if step.id == 'confirm_generate' and not result:
                    print()
                    print_warning("Generation cancelled by user")
                    return EXIT_USER_CANCELLED

            except KeyboardInterrupt:
                print()
                print_warning("Workflow interrupted")
                return EXIT_USER_CANCELLED

        # Generate output
        print()
        print_info("Generating documentation...")

        generator = DocumentGenerator(self.output_format)
        output = generator.generate(workflow)

        # Preview output
        print()
        print("=" * 60)
        print("  Preview")
        print("=" * 60)
        print()

        # Show truncated preview
        preview_lines = output.split('\n')[:30]
        print('\n'.join(preview_lines))
        if len(output.split('\n')) > 30:
            print("\n... (truncated)")

        # Write output
        if dry_run:
            print()
            print_info("Dry run - output not written to file")
        elif output_path:
            if write_file_safe(output_path, output):
                print()
                print_success(f"Output written to: {output_path}")
            else:
                print_error(f"Failed to write to: {output_path}")
                return EXIT_ERROR
        else:
            # Prompt for output path
            print()
            save = self.prompter.prompt_confirm("Save to file?", default=True)
            if save:
                default_name = self._get_default_filename(workflow_type)
                path_str = self.prompter.prompt_text(
                    "Output file path",
                    default=default_name
                )
                if path_str:
                    out_path = Path(path_str)
                    if write_file_safe(out_path, output):
                        print_success(f"Output written to: {out_path}")
                    else:
                        print_error(f"Failed to write to: {out_path}")
                        return EXIT_ERROR

        print()
        print_success("Workflow completed successfully!")
        return EXIT_SUCCESS

    def _get_default_filename(self, workflow_type: str) -> str:
        """Get default output filename for workflow type."""
        defaults = {
            'readme': 'README.md',
            'api-docs': 'API.md',
            'changelog': 'CHANGELOG.md',
            'audit': 'AUDIT_REPORT.md',
            'user-guide': 'USER_GUIDE.md',
        }
        return defaults.get(workflow_type, 'OUTPUT.md')


# ============================================================================
# SECTION 8: CLI ENTRY POINT
# ============================================================================
# Argument parsing and main function


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description='Interactive documentation wizard with guided workflows',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Interactive menu
  %(prog)s --workflow readme         # Start README wizard
  %(prog)s --workflow audit -o report.md  # Run audit, save to file
  %(prog)s --workflow api-docs --dry-run  # Preview API docs
  %(prog)s --config config.yaml      # Non-interactive mode

Workflows:
  readme      Interactive README creation (8 steps, ~10-15 min)
  api-docs    Generate API documentation (10 steps, ~15-20 min)
  changelog   Create CHANGELOG from history (6 steps, ~5-10 min)
  audit       Documentation quality audit (7 steps, ~10-15 min)
  user-guide  Create user guide (12 steps, ~20-30 min)
"""
    )

    # Workflow selection
    parser.add_argument(
        '-w', '--workflow',
        choices=list(WORKFLOW_TYPES.keys()),
        help='Workflow to run'
    )

    # Config file mode
    parser.add_argument(
        '-c', '--config',
        type=Path,
        help='Config file for non-interactive mode (YAML/JSON)'
    )

    # Output options
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file path'
    )

    parser.add_argument(
        '-f', '--format',
        choices=['markdown', 'html', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
    )

    # Modes
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview output without writing files'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {VERSION}'
    )

    return parser


def load_config(config_path: Path) -> Optional[Dict[str, Any]]:
    """Load configuration from file."""
    if not config_path.exists():
        print_error(f"Config file not found: {config_path}")
        return None

    content = read_file_safe(config_path)
    if not content:
        print_error(f"Failed to read config file: {config_path}")
        return None

    # Try JSON first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try simple YAML-like parsing
    config = {}
    for line in content.splitlines():
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            config[key.strip()] = value.strip()

    return config if config else None


def run_with_config(config: Dict[str, Any], args: argparse.Namespace) -> int:
    """Run workflow with config file."""
    workflow_type = config.get('workflow', args.workflow)
    if not workflow_type:
        print_error("No workflow specified in config or arguments")
        return EXIT_ERROR

    wizard = InteractiveDocWizard(
        verbose=args.verbose,
        output_format=args.format
    )

    # Create workflow and populate context from config
    if workflow_type not in wizard.WORKFLOWS:
        print_error(f"Unknown workflow: {workflow_type}")
        return EXIT_ERROR

    workflow_class = wizard.WORKFLOWS[workflow_type]
    workflow = workflow_class()
    workflow.context = config

    # Generate output
    generator = DocumentGenerator(args.format)
    output = generator.generate(workflow)

    # Write output
    output_path = args.output or Path(config.get('output', wizard._get_default_filename(workflow_type)))

    if args.dry_run:
        print(output)
        return EXIT_SUCCESS

    if write_file_safe(output_path, output):
        print_success(f"Output written to: {output_path}")
        return EXIT_SUCCESS
    else:
        print_error(f"Failed to write to: {output_path}")
        return EXIT_ERROR


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Config file mode
    if args.config:
        config = load_config(args.config)
        if config is None:
            return EXIT_ERROR
        return run_with_config(config, args)

    # Create wizard
    wizard = InteractiveDocWizard(
        verbose=args.verbose,
        output_format=args.format
    )

    # Specific workflow or interactive menu
    if args.workflow:
        return wizard.run_workflow(
            args.workflow,
            output_path=args.output,
            dry_run=args.dry_run
        )

    # Interactive menu loop
    while True:
        workflow_type = wizard.show_workflow_menu()

        if workflow_type is None:
            print()
            print("Goodbye!")
            return EXIT_SUCCESS

        result = wizard.run_workflow(
            workflow_type,
            output_path=args.output,
            dry_run=args.dry_run
        )

        if result != EXIT_SUCCESS:
            return result

        # Ask if user wants to run another workflow
        print()
        if not wizard.prompter.prompt_confirm("Run another workflow?", default=False):
            print()
            print("Goodbye!")
            return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
