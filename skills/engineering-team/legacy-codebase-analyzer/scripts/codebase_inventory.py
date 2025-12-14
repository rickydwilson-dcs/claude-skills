#!/usr/bin/env python3
"""
Codebase Inventory - Foundation Analysis Tool

Scans and catalogs a codebase to create a comprehensive inventory of files,
languages, frameworks, dependencies, and structural patterns. This foundational
tool provides the baseline data that all other legacy analysis tools consume.

Part of the legacy-codebase-analyzer skill package.
"""

from dataclasses import dataclass, field
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import argparse
import csv
import json
import logging
import os
import re
import sys


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class FileInfo:
    """Information about a single source file"""
    path: str
    language: str
    extension: str
    lines_total: int
    lines_code: int
    lines_comment: int
    lines_blank: int
    size_bytes: int
    last_modified: str
    encoding: str = 'utf-8'


@dataclass
class LanguageStats:
    """Statistics for a programming language"""
    language: str
    file_count: int
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    percentage: float
    extensions: List[str] = field(default_factory=list)


@dataclass
class Framework:
    """Detected framework or library"""
    name: str
    version: Optional[str]
    category: str  # web, testing, orm, cli, data, etc.
    detection_source: str  # package.json, requirements.txt, imports, etc.
    confidence: str  # high, medium, low


@dataclass
class Dependency:
    """Project dependency"""
    name: str
    version: str
    version_constraint: str
    source: str  # requirements.txt, package.json, go.mod, etc.
    is_dev_dependency: bool
    ecosystem: str  # python, node, go, java, etc.


class CodebaseInventory:
    """Comprehensive codebase scanning and cataloging tool"""

    LANGUAGE_EXTENSIONS = {
        # Python
        '.py': 'python',
        '.pyw': 'python',
        '.pyx': 'python',
        # JavaScript/TypeScript
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.mjs': 'javascript',
        '.cjs': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        # Web
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        # Backend
        '.go': 'go',
        '.java': 'java',
        '.kt': 'kotlin',
        '.kts': 'kotlin',
        '.scala': 'scala',
        '.rb': 'ruby',
        '.php': 'php',
        '.cs': 'csharp',
        '.fs': 'fsharp',
        '.vb': 'visualbasic',
        # Systems
        '.rs': 'rust',
        '.c': 'c',
        '.h': 'c',
        '.cpp': 'cpp',
        '.hpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        # Data/Config
        '.sql': 'sql',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.xml': 'xml',
        '.graphql': 'graphql',
        '.gql': 'graphql',
        # Shell
        '.sh': 'shell',
        '.bash': 'shell',
        '.zsh': 'shell',
        '.fish': 'shell',
        '.ps1': 'powershell',
        # Other
        '.md': 'markdown',
        '.rst': 'restructuredtext',
        '.r': 'r',
        '.R': 'r',
        '.swift': 'swift',
        '.m': 'objectivec',
        '.mm': 'objectivec',
        '.dart': 'dart',
        '.lua': 'lua',
        '.pl': 'perl',
        '.pm': 'perl',
        '.ex': 'elixir',
        '.exs': 'elixir',
        '.erl': 'erlang',
        '.hrl': 'erlang',
        '.clj': 'clojure',
        '.cljs': 'clojure',
        '.hs': 'haskell',
        '.vue': 'vue',
        '.svelte': 'svelte',
    }

    SKIP_DIRS = {
        'node_modules', '__pycache__', '.git', '.svn', '.hg',
        'venv', 'env', '.venv', '.env', 'virtualenv',
        'dist', 'build', 'out', 'target', 'bin', 'obj',
        '.tox', '.pytest_cache', '.mypy_cache', '.ruff_cache',
        'coverage', '.coverage', 'htmlcov', '.nyc_output',
        'vendor', 'third_party', 'external', 'deps',
        '.idea', '.vscode', '.vs', '.eclipse',
        '.next', '.nuxt', '.output', '.cache',
        'bower_components', 'jspm_packages',
        'eggs', '*.egg-info', '.eggs',
    }

    SKIP_FILES = {
        '.DS_Store', 'Thumbs.db', '.gitignore', '.gitattributes',
        'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
        'Pipfile.lock', 'poetry.lock', 'Cargo.lock',
        'go.sum', 'composer.lock', 'Gemfile.lock',
    }

    COMMENT_PATTERNS = {
        'python': (r'^\s*#', r'^\s*"""', r"^\s*'''"),
        'javascript': (r'^\s*//', r'^\s*/\*', r'\*/\s*$'),
        'typescript': (r'^\s*//', r'^\s*/\*', r'\*/\s*$'),
        'java': (r'^\s*//', r'^\s*/\*', r'\*/\s*$'),
        'go': (r'^\s*//', r'^\s*/\*', r'\*/\s*$'),
        'ruby': (r'^\s*#', r'^\s*=begin', r'^\s*=end'),
        'shell': (r'^\s*#',),
        'c': (r'^\s*//', r'^\s*/\*', r'\*/\s*$'),
        'cpp': (r'^\s*//', r'^\s*/\*', r'\*/\s*$'),
        'csharp': (r'^\s*//', r'^\s*/\*', r'\*/\s*$'),
        'rust': (r'^\s*//', r'^\s*/\*', r'\*/\s*$'),
        'php': (r'^\s*//', r'^\s*#', r'^\s*/\*', r'\*/\s*$'),
        'sql': (r'^\s*--', r'^\s*/\*', r'\*/\s*$'),
        'html': (r'^\s*<!--', r'-->\s*$'),
        'css': (r'^\s*/\*', r'\*/\s*$'),
    }

    FRAMEWORK_PATTERNS = {
        # Python Web Frameworks
        'django': {'files': ['manage.py', 'settings.py'], 'imports': ['django'], 'packages': ['django']},
        'flask': {'imports': ['flask'], 'packages': ['flask']},
        'fastapi': {'imports': ['fastapi'], 'packages': ['fastapi']},
        'tornado': {'imports': ['tornado'], 'packages': ['tornado']},
        'pyramid': {'imports': ['pyramid'], 'packages': ['pyramid']},
        # JavaScript Frameworks
        'react': {'packages': ['react'], 'files': [], 'imports': ['react']},
        'vue': {'packages': ['vue'], 'files': ['vue.config.js'], 'imports': ['vue']},
        'angular': {'packages': ['@angular/core'], 'files': ['angular.json']},
        'svelte': {'packages': ['svelte'], 'files': ['svelte.config.js']},
        'next.js': {'packages': ['next'], 'files': ['next.config.js', 'next.config.mjs']},
        'nuxt': {'packages': ['nuxt'], 'files': ['nuxt.config.js', 'nuxt.config.ts']},
        'express': {'packages': ['express'], 'imports': ['express']},
        'nestjs': {'packages': ['@nestjs/core'], 'imports': ['@nestjs']},
        # Testing Frameworks
        'pytest': {'packages': ['pytest'], 'imports': ['pytest']},
        'jest': {'packages': ['jest'], 'files': ['jest.config.js', 'jest.config.ts']},
        'mocha': {'packages': ['mocha'], 'files': ['.mocharc.js', '.mocharc.json']},
        'unittest': {'imports': ['unittest']},
        'rspec': {'packages': ['rspec'], 'files': ['.rspec']},
        # ORM/Database
        'sqlalchemy': {'packages': ['sqlalchemy'], 'imports': ['sqlalchemy']},
        'django-orm': {'imports': ['django.db']},
        'prisma': {'packages': ['@prisma/client'], 'files': ['prisma/schema.prisma']},
        'sequelize': {'packages': ['sequelize'], 'imports': ['sequelize']},
        'typeorm': {'packages': ['typeorm'], 'imports': ['typeorm']},
        # Build Tools
        'webpack': {'packages': ['webpack'], 'files': ['webpack.config.js']},
        'vite': {'packages': ['vite'], 'files': ['vite.config.js', 'vite.config.ts']},
        'rollup': {'packages': ['rollup'], 'files': ['rollup.config.js']},
        'esbuild': {'packages': ['esbuild']},
        # Other
        'celery': {'packages': ['celery'], 'imports': ['celery']},
        'redis': {'packages': ['redis', 'ioredis'], 'imports': ['redis']},
        'graphql': {'packages': ['graphql', 'apollo-server'], 'imports': ['graphql']},
    }

    def __init__(self, target_path: str, exclude_patterns: List[str] = None,
                 max_depth: int = None, verbose: bool = False):
        self.target_path = Path(target_path).resolve()
        self.exclude_patterns = exclude_patterns or []
        self.max_depth = max_depth
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("CodebaseInventory initialized")

        self.files: List[FileInfo] = []
        self.languages: Dict[str, LanguageStats] = {}
        self.frameworks: List[Framework] = []
        self.dependencies: List[Dependency] = []
        self.results: Dict = {}

    def discover_files(self) -> List[Path]:
        """Recursively find source files to catalog"""
        files = []
        base_depth = len(self.target_path.parts)

        if self.target_path.is_file():
            return [self.target_path] if self._is_source_file(self.target_path) else []

        for root, dirs, filenames in os.walk(self.target_path):
            root_path = Path(root)

            # Check depth limit
            if self.max_depth:
                current_depth = len(root_path.parts) - base_depth
                if current_depth >= self.max_depth:
                    dirs[:] = []
                    continue

            # Filter directories
            dirs[:] = [d for d in dirs if not self._should_skip_dir(d)]

            for filename in filenames:
                if filename in self.SKIP_FILES:
                    continue
                if self._matches_exclude_pattern(filename):
                    continue

                file_path = root_path / filename
                if self._is_source_file(file_path):
                    files.append(file_path)

        return sorted(files)

    def _should_skip_dir(self, dirname: str) -> bool:
        """Check if directory should be skipped"""
        if dirname in self.SKIP_DIRS:
            return True
        if dirname.startswith('.'):
            return True
        if self._matches_exclude_pattern(dirname):
            return True
        return False

    def _matches_exclude_pattern(self, name: str) -> bool:
        """Check if name matches any exclude pattern"""
        import fnmatch
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        return False

    def _is_source_file(self, path: Path) -> bool:
        """Check if file is a recognized source file"""
        return path.suffix.lower() in self.LANGUAGE_EXTENSIONS

    def detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        return self.LANGUAGE_EXTENSIONS.get(file_path.suffix.lower(), 'unknown')

    def read_file_safe(self, file_path: Path) -> Optional[str]:
        """Read file with graceful encoding error handling"""
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                content = file_path.read_text(encoding=encoding)
                return content
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                if self.verbose:
                    print(f"  Warning: Could not read {file_path}: {e}", file=sys.stderr)
                return None
        return None

    def count_lines(self, content: str, language: str) -> Tuple[int, int, int, int]:
        """Count total, code, comment, and blank lines"""
        lines = content.split('\n')
        total = len(lines)
        blank = sum(1 for line in lines if not line.strip())

        comment_patterns = self.COMMENT_PATTERNS.get(language, ())
        in_multiline_comment = False
        comments = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Simple comment detection
            is_comment = False
            for pattern in comment_patterns:
                if re.match(pattern, line):
                    is_comment = True
                    break

            if is_comment:
                comments += 1

        code = total - blank - comments
        return total, max(0, code), comments, blank

    def analyze_file(self, file_path: Path) -> Optional[FileInfo]:
        """Analyze a single file"""
        try:
            stat = file_path.stat()
            language = self.detect_language(file_path)

            content = self.read_file_safe(file_path)
            if content is None:
                return None

            total, code, comments, blank = self.count_lines(content, language)

            rel_path = str(file_path.relative_to(self.target_path))

            return FileInfo(
                path=rel_path,
                language=language,
                extension=file_path.suffix.lower(),
                lines_total=total,
                lines_code=code,
                lines_comment=comments,
                lines_blank=blank,
                size_bytes=stat.st_size,
                last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                encoding='utf-8'
            )
        except Exception as e:
            if self.verbose:
                print(f"  Warning: Could not analyze {file_path}: {e}", file=sys.stderr)
            return None

    def calculate_language_stats(self) -> Dict[str, LanguageStats]:
        """Calculate statistics per language"""
        lang_data: Dict[str, Dict] = {}

        for file_info in self.files:
            lang = file_info.language
            if lang not in lang_data:
                lang_data[lang] = {
                    'file_count': 0,
                    'total_lines': 0,
                    'code_lines': 0,
                    'comment_lines': 0,
                    'blank_lines': 0,
                    'extensions': set()
                }

            lang_data[lang]['file_count'] += 1
            lang_data[lang]['total_lines'] += file_info.lines_total
            lang_data[lang]['code_lines'] += file_info.lines_code
            lang_data[lang]['comment_lines'] += file_info.lines_comment
            lang_data[lang]['blank_lines'] += file_info.lines_blank
            lang_data[lang]['extensions'].add(file_info.extension)

        total_lines = sum(d['total_lines'] for d in lang_data.values())

        stats = {}
        for lang, data in lang_data.items():
            percentage = (data['total_lines'] / total_lines * 100) if total_lines > 0 else 0
            stats[lang] = LanguageStats(
                language=lang,
                file_count=data['file_count'],
                total_lines=data['total_lines'],
                code_lines=data['code_lines'],
                comment_lines=data['comment_lines'],
                blank_lines=data['blank_lines'],
                percentage=round(percentage, 2),
                extensions=sorted(data['extensions'])
            )

        return dict(sorted(stats.items(), key=lambda x: -x[1].total_lines))

    def parse_requirements_txt(self, file_path: Path) -> List[Dependency]:
        """Parse Python requirements.txt"""
        deps = []
        content = self.read_file_safe(file_path)
        if not content:
            return deps

        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('-'):
                continue

            # Parse package==version or package>=version etc.
            match = re.match(r'^([a-zA-Z0-9_-]+)\s*([<>=!~]+)?\s*([a-zA-Z0-9._-]+)?', line)
            if match:
                name = match.group(1)
                constraint = match.group(2) or ''
                version = match.group(3) or ''
                deps.append(Dependency(
                    name=name,
                    version=version,
                    version_constraint=f"{constraint}{version}",
                    source=str(file_path.relative_to(self.target_path)),
                    is_dev_dependency='dev' in str(file_path).lower(),
                    ecosystem='python'
                ))

        return deps

    def parse_package_json(self, file_path: Path) -> List[Dependency]:
        """Parse Node.js package.json"""
        deps = []
        content = self.read_file_safe(file_path)
        if not content:
            return deps

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return deps

        for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
            is_dev = dep_type != 'dependencies'
            for name, version in data.get(dep_type, {}).items():
                deps.append(Dependency(
                    name=name,
                    version=version.lstrip('^~>=<'),
                    version_constraint=version,
                    source=str(file_path.relative_to(self.target_path)),
                    is_dev_dependency=is_dev,
                    ecosystem='node'
                ))

        return deps

    def parse_go_mod(self, file_path: Path) -> List[Dependency]:
        """Parse Go go.mod"""
        deps = []
        content = self.read_file_safe(file_path)
        if not content:
            return deps

        in_require = False
        for line in content.split('\n'):
            line = line.strip()

            if line.startswith('require ('):
                in_require = True
                continue
            if line == ')':
                in_require = False
                continue

            if in_require or line.startswith('require '):
                line = line.replace('require ', '')
                match = re.match(r'^([^\s]+)\s+([^\s]+)', line)
                if match:
                    deps.append(Dependency(
                        name=match.group(1),
                        version=match.group(2),
                        version_constraint=match.group(2),
                        source=str(file_path.relative_to(self.target_path)),
                        is_dev_dependency=False,
                        ecosystem='go'
                    ))

        return deps

    def discover_dependencies(self) -> List[Dependency]:
        """Discover all project dependencies from manifest files"""
        deps = []

        # Python
        for req_file in self.target_path.rglob('requirements*.txt'):
            if any(skip in str(req_file) for skip in self.SKIP_DIRS):
                continue
            deps.extend(self.parse_requirements_txt(req_file))

        # Node.js
        for pkg_file in self.target_path.rglob('package.json'):
            if any(skip in str(pkg_file) for skip in self.SKIP_DIRS):
                continue
            deps.extend(self.parse_package_json(pkg_file))

        # Go
        for go_file in self.target_path.rglob('go.mod'):
            if any(skip in str(go_file) for skip in self.SKIP_DIRS):
                continue
            deps.extend(self.parse_go_mod(go_file))

        return deps

    def detect_frameworks(self) -> List[Framework]:
        """Detect frameworks and libraries used in the project"""
        frameworks = []
        detected: Set[str] = set()

        # Get all package names from dependencies
        dep_names = {d.name.lower() for d in self.dependencies}

        # Check for framework indicators
        for name, indicators in self.FRAMEWORK_PATTERNS.items():
            if name in detected:
                continue

            confidence = 'low'
            detection_source = ''

            # Check packages
            packages = indicators.get('packages', [])
            for pkg in packages:
                if pkg.lower() in dep_names:
                    confidence = 'high'
                    detection_source = 'package manifest'
                    break

            # Check for config files
            if confidence != 'high':
                files = indicators.get('files', [])
                for f in files:
                    if (self.target_path / f).exists():
                        confidence = 'high'
                        detection_source = f'config file ({f})'
                        break

            if confidence != 'low':
                # Try to get version from dependencies
                version = None
                for pkg in packages:
                    for dep in self.dependencies:
                        if dep.name.lower() == pkg.lower():
                            version = dep.version
                            break
                    if version:
                        break

                # Determine category
                category = self._categorize_framework(name)

                frameworks.append(Framework(
                    name=name,
                    version=version,
                    category=category,
                    detection_source=detection_source,
                    confidence=confidence
                ))
                detected.add(name)

        return sorted(frameworks, key=lambda f: (f.category, f.name))

    def _categorize_framework(self, name: str) -> str:
        """Categorize a framework by type"""
        web_frameworks = {'django', 'flask', 'fastapi', 'express', 'nestjs', 'react',
                        'vue', 'angular', 'svelte', 'next.js', 'nuxt', 'tornado', 'pyramid'}
        testing = {'pytest', 'jest', 'mocha', 'unittest', 'rspec'}
        orm = {'sqlalchemy', 'django-orm', 'prisma', 'sequelize', 'typeorm'}
        build = {'webpack', 'vite', 'rollup', 'esbuild'}

        name_lower = name.lower()
        if name_lower in web_frameworks:
            return 'web'
        if name_lower in testing:
            return 'testing'
        if name_lower in orm:
            return 'orm'
        if name_lower in build:
            return 'build'
        return 'other'

    def calculate_age_analysis(self) -> Dict:
        """Analyze file age distribution"""
        if not self.files:
            return {}

        dates = []
        for f in self.files:
            try:
                dt = datetime.fromisoformat(f.last_modified)
                dates.append(dt)
            except (ValueError, TypeError):
                continue

        if not dates:
            return {}

        oldest = min(dates)
        newest = max(dates)
        now = datetime.now()

        # Calculate age buckets
        buckets = {
            'last_30_days': 0,
            'last_90_days': 0,
            'last_year': 0,
            'older': 0
        }

        for dt in dates:
            age_days = (now - dt).days
            if age_days <= 30:
                buckets['last_30_days'] += 1
            elif age_days <= 90:
                buckets['last_90_days'] += 1
            elif age_days <= 365:
                buckets['last_year'] += 1
            else:
                buckets['older'] += 1

        avg_age = sum((now - dt).days for dt in dates) / len(dates)

        return {
            'oldest_file': {
                'date': oldest.isoformat(),
                'age_days': (now - oldest).days
            },
            'newest_file': {
                'date': newest.isoformat(),
                'age_days': (now - newest).days
            },
            'average_age_days': round(avg_age, 1),
            'distribution': buckets
        }

    def run(self) -> Dict:
        """Execute the inventory scan"""
        if self.verbose:
            print(f"Scanning: {self.target_path}")

        if not self.target_path.exists():
            return {
                'status': 'error',
                'error': f"Target path does not exist: {self.target_path}"
            }

        # Discover and analyze files
        files = self.discover_files()
        if self.verbose:
            print(f"Found {len(files)} source files")

        for file_path in files:
            if self.verbose:
                print(f"  Analyzing: {file_path}")
            file_info = self.analyze_file(file_path)
            if file_info:
                self.files.append(file_info)

        # Calculate language statistics
        self.languages = self.calculate_language_stats()

        # Discover dependencies
        if self.verbose:
            print("Discovering dependencies...")
        self.dependencies = self.discover_dependencies()

        # Detect frameworks
        if self.verbose:
            print("Detecting frameworks...")
        self.frameworks = self.detect_frameworks()

        # Calculate metrics
        total_lines = sum(f.lines_total for f in self.files)
        total_code = sum(f.lines_code for f in self.files)
        total_comments = sum(f.lines_comment for f in self.files)
        total_blank = sum(f.lines_blank for f in self.files)
        total_size = sum(f.size_bytes for f in self.files)

        # Age analysis
        age_analysis = self.calculate_age_analysis()

        # Build results
        self.results = {
            'status': 'success',
            'target': str(self.target_path),
            'analyzed_at': datetime.now().isoformat(),
            'summary': {
                'total_files': len(self.files),
                'total_lines': total_lines,
                'code_lines': total_code,
                'comment_lines': total_comments,
                'blank_lines': total_blank,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'languages_detected': len(self.languages),
                'frameworks_detected': len(self.frameworks),
                'dependencies_count': len(self.dependencies)
            },
            'languages': [
                {
                    'language': stats.language,
                    'file_count': stats.file_count,
                    'total_lines': stats.total_lines,
                    'code_lines': stats.code_lines,
                    'comment_lines': stats.comment_lines,
                    'blank_lines': stats.blank_lines,
                    'percentage': stats.percentage,
                    'extensions': stats.extensions
                }
                for stats in self.languages.values()
            ],
            'frameworks': [
                {
                    'name': fw.name,
                    'version': fw.version,
                    'category': fw.category,
                    'detection_source': fw.detection_source,
                    'confidence': fw.confidence
                }
                for fw in self.frameworks
            ],
            'dependencies': [
                {
                    'name': dep.name,
                    'version': dep.version,
                    'version_constraint': dep.version_constraint,
                    'source': dep.source,
                    'is_dev_dependency': dep.is_dev_dependency,
                    'ecosystem': dep.ecosystem
                }
                for dep in self.dependencies
            ],
            'age_analysis': age_analysis,
            'files': [
                {
                    'path': f.path,
                    'language': f.language,
                    'lines': f.lines_total,
                    'size_bytes': f.size_bytes,
                    'last_modified': f.last_modified
                }
                for f in sorted(self.files, key=lambda x: -x.lines_total)[:100]  # Top 100 by lines
            ]
        }

        return self.results

    def format_json(self) -> str:
        """Format results as JSON"""
        return json.dumps(self.results, indent=2)

    def format_csv(self) -> str:
        """Format file list as CSV"""
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['path', 'language', 'lines_total', 'lines_code',
                        'lines_comment', 'lines_blank', 'size_bytes', 'last_modified'])

        for f in self.files:
            writer.writerow([
                f.path, f.language, f.lines_total, f.lines_code,
                f.lines_comment, f.lines_blank, f.size_bytes, f.last_modified
            ])

        return output.getvalue()

    def format_text(self) -> str:
        """Format results as human-readable text"""
        lines = []
        lines.append("=" * 70)
        lines.append("CODEBASE INVENTORY REPORT")
        lines.append("=" * 70)
        lines.append(f"Target: {self.results.get('target')}")
        lines.append(f"Analyzed At: {self.results.get('analyzed_at')}")
        lines.append("")

        summary = self.results.get('summary', {})
        lines.append("SUMMARY")
        lines.append("-" * 40)
        lines.append(f"  Total Files:       {summary.get('total_files', 0):,}")
        lines.append(f"  Total Lines:       {summary.get('total_lines', 0):,}")
        lines.append(f"  Code Lines:        {summary.get('code_lines', 0):,}")
        lines.append(f"  Comment Lines:     {summary.get('comment_lines', 0):,}")
        lines.append(f"  Blank Lines:       {summary.get('blank_lines', 0):,}")
        lines.append(f"  Total Size:        {summary.get('total_size_mb', 0)} MB")
        lines.append(f"  Languages:         {summary.get('languages_detected', 0)}")
        lines.append(f"  Frameworks:        {summary.get('frameworks_detected', 0)}")
        lines.append(f"  Dependencies:      {summary.get('dependencies_count', 0)}")
        lines.append("")

        # Languages
        languages = self.results.get('languages', [])
        if languages:
            lines.append("LANGUAGES")
            lines.append("-" * 40)
            for lang in languages[:10]:
                lines.append(f"  {lang['language']:<15} {lang['file_count']:>5} files  "
                           f"{lang['total_lines']:>8} lines  ({lang['percentage']:>5.1f}%)")
            if len(languages) > 10:
                lines.append(f"  ... and {len(languages) - 10} more")
            lines.append("")

        # Frameworks
        frameworks = self.results.get('frameworks', [])
        if frameworks:
            lines.append("FRAMEWORKS DETECTED")
            lines.append("-" * 40)
            for fw in frameworks:
                version = fw['version'] or 'unknown'
                lines.append(f"  {fw['name']:<20} v{version:<12} [{fw['category']}]")
            lines.append("")

        # Dependencies summary
        deps = self.results.get('dependencies', [])
        if deps:
            by_ecosystem = {}
            for d in deps:
                eco = d['ecosystem']
                by_ecosystem[eco] = by_ecosystem.get(eco, 0) + 1

            lines.append("DEPENDENCIES BY ECOSYSTEM")
            lines.append("-" * 40)
            for eco, count in sorted(by_ecosystem.items(), key=lambda x: -x[1]):
                lines.append(f"  {eco:<15} {count:>5} packages")
            lines.append("")

        # Age analysis
        age = self.results.get('age_analysis', {})
        if age:
            lines.append("AGE ANALYSIS")
            lines.append("-" * 40)
            if age.get('oldest_file'):
                lines.append(f"  Oldest File:    {age['oldest_file']['age_days']} days old")
            if age.get('newest_file'):
                lines.append(f"  Newest File:    {age['newest_file']['age_days']} days old")
            lines.append(f"  Average Age:    {age.get('average_age_days', 0)} days")
            dist = age.get('distribution', {})
            if dist:
                lines.append(f"  Last 30 days:   {dist.get('last_30_days', 0)} files")
                lines.append(f"  Last 90 days:   {dist.get('last_90_days', 0)} files")
                lines.append(f"  Last year:      {dist.get('last_year', 0)} files")
                lines.append(f"  Older:          {dist.get('older', 0)} files")
            lines.append("")

        # Largest files
        files = self.results.get('files', [])
        if files:
            lines.append("LARGEST FILES (by lines)")
            lines.append("-" * 40)
            for f in files[:10]:
                lines.append(f"  {f['path'][:50]:<50} {f['lines']:>6} lines")
            lines.append("")

        lines.append("=" * 70)
        return '\n'.join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Codebase Inventory - Comprehensive codebase scanning and cataloging",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input ./legacy-app
  %(prog)s --input ./src --output json --file inventory.json
  %(prog)s --input . --exclude "*.test.js" --exclude "docs/*" -v
  %(prog)s --input ./project --depth 5 --output csv

Output Formats:
  text  - Human-readable summary (default)
  json  - Complete structured data
  csv   - File list for spreadsheet analysis
        """
    )

    parser.add_argument(
        '--input', '-i', required=True,
        help='Target directory to scan'
    )
    parser.add_argument(
        '--output', '-o', choices=['text', 'json', 'csv'], default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )
    parser.add_argument(
        '--exclude', '-e', action='append', default=[],
        help='Glob pattern to exclude (can be repeated)'
    )
    parser.add_argument(
        '--depth', '-d', type=int,
        help='Maximum directory depth to scan'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    inventory = CodebaseInventory(
        target_path=args.input,
        exclude_patterns=args.exclude,
        max_depth=args.depth,
        verbose=args.verbose
    )

    results = inventory.run()

    if results.get('status') == 'error':
        print(f"Error: {results.get('error')}", file=sys.stderr)
        sys.exit(1)

    if args.output == 'json':
        output = inventory.format_json()
    elif args.output == 'csv':
        output = inventory.format_csv()
    else:
        output = inventory.format_text()

    if args.file:
        Path(args.file).write_text(output)
        if args.verbose:
            print(f"Results written to {args.file}")
    else:
        print(output)


if __name__ == '__main__':
    main()
