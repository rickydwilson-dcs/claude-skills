#!/usr/bin/env python3
"""
Code Quality Analyzer - Cross-Stack Quality Analysis Tool

A comprehensive code quality analysis tool for fullstack projects that:
- Validates frontend/backend consistency
- Checks API contract compliance
- Scans for security vulnerabilities
- Assesses test coverage
- Evaluates documentation quality
- Analyzes dependencies

Part of the senior-fullstack skill package.
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# Enums and Data Classes
# =============================================================================

class QualityCategory(Enum):
    """Categories of quality checks"""
    CONSISTENCY = "Frontend/Backend Consistency"
    API_CONTRACT = "API Contract Validation"
    SECURITY = "Security Vulnerability"
    TEST_COVERAGE = "Test Coverage"
    DOCUMENTATION = "Documentation Quality"
    DEPENDENCIES = "Dependency Analysis"


class Severity(Enum):
    """Severity levels for findings"""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    INFO = 0


@dataclass
class QualityCheck:
    """Definition of a quality check"""
    id: str
    category: QualityCategory
    name: str
    description: str
    patterns: List[str]
    severity: Severity
    recommendation: str
    file_types: List[str] = field(default_factory=list)


@dataclass
class QualityFinding:
    """A quality issue found during analysis"""
    check: QualityCheck
    file_path: str
    line_number: int
    line_content: str
    details: str


@dataclass
class CoverageData:
    """Test coverage information"""
    total_lines: int = 0
    covered_lines: int = 0
    coverage_percent: float = 0.0
    uncovered_files: List[str] = field(default_factory=list)


# =============================================================================
# Quality Check Definitions
# =============================================================================

class CheckDefinitions:
    """Factory for quality check definitions"""

    @staticmethod
    def security_checks() -> List[QualityCheck]:
        """Security vulnerability checks"""
        return [
            QualityCheck(
                id='SEC001',
                category=QualityCategory.SECURITY,
                name='Hardcoded Credentials',
                description='Hardcoded passwords, API keys, or secrets in code',
                patterns=[
                    r'(?i)(?:password|passwd|pwd)\s*[=:]\s*["\'][^"\']{8,}["\']',
                    r'(?i)(?:api[_-]?key|apikey)\s*[=:]\s*["\'][A-Za-z0-9_\-]{16,}["\']',
                    r'(?i)(?:secret[_-]?key|secretkey)\s*[=:]\s*["\'][A-Za-z0-9_\-]{16,}["\']',
                    r'(?i)(?:auth[_-]?token|authtoken)\s*[=:]\s*["\'][A-Za-z0-9_\-\.]{20,}["\']',
                    r'(?i)(?:private[_-]?key)\s*[=:]\s*["\']-----BEGIN',
                    r'(?i)Bearer\s+[A-Za-z0-9_\-\.]{20,}',
                ],
                severity=Severity.CRITICAL,
                recommendation='Store credentials in environment variables or a secure vault',
                file_types=['.js', '.ts', '.jsx', '.tsx', '.py', '.go', '.java', '.env']
            ),
            QualityCheck(
                id='SEC002',
                category=QualityCategory.SECURITY,
                name='SQL Injection Risk',
                description='Potential SQL injection vulnerability from string concatenation',
                patterns=[
                    r'(?i)(?:execute|query|raw)\s*\(\s*[f"\'].*\+.*(?:SELECT|INSERT|UPDATE|DELETE)',
                    r'(?i)(?:execute|query)\s*\(\s*f["\'].*\{.*\}.*(?:SELECT|INSERT|UPDATE|DELETE)',
                    r'(?i)cursor\.execute\s*\([^,]*\+',
                    r'(?i)\.query\s*\([^,]*\$\{',
                ],
                severity=Severity.CRITICAL,
                recommendation='Use parameterized queries or an ORM',
                file_types=['.js', '.ts', '.py', '.go', '.java']
            ),
            QualityCheck(
                id='SEC003',
                category=QualityCategory.SECURITY,
                name='XSS Vulnerability',
                description='Potential cross-site scripting vulnerability',
                patterns=[
                    r'(?i)dangerouslySetInnerHTML',
                    r'(?i)innerHTML\s*=',
                    r'(?i)v-html\s*=',
                    r'(?i)document\.write\s*\(',
                    r'(?i)\{\s*\{\s*\{.*\}\s*\}\s*\}',  # Triple mustache in templates
                ],
                severity=Severity.HIGH,
                recommendation='Sanitize user input before rendering; use safe DOM methods',
                file_types=['.js', '.ts', '.jsx', '.tsx', '.vue', '.html']
            ),
            QualityCheck(
                id='SEC004',
                category=QualityCategory.SECURITY,
                name='Insecure Random',
                description='Use of insecure random number generation',
                patterns=[
                    r'Math\.random\s*\(\)',
                    r'random\.random\s*\(\)',
                    r'(?i)rand\s*\(\)',
                ],
                severity=Severity.MEDIUM,
                recommendation='Use crypto.randomBytes() or secrets module for security-sensitive operations',
                file_types=['.js', '.ts', '.jsx', '.tsx', '.py']
            ),
            QualityCheck(
                id='SEC005',
                category=QualityCategory.SECURITY,
                name='Disabled Security',
                description='Security features explicitly disabled',
                patterns=[
                    r'(?i)verify\s*=\s*False',
                    r'(?i)ssl\s*:\s*false',
                    r'(?i)secure\s*:\s*false',
                    r'(?i)rejectUnauthorized\s*:\s*false',
                    r'(?i)CSRF.*disable',
                ],
                severity=Severity.HIGH,
                recommendation='Enable security features in production environments',
                file_types=['.js', '.ts', '.py', '.json', '.yaml', '.yml']
            ),
            QualityCheck(
                id='SEC006',
                category=QualityCategory.SECURITY,
                name='Exposed Debug Mode',
                description='Debug mode enabled or exposed in code',
                patterns=[
                    r'(?i)DEBUG\s*=\s*True',
                    r'(?i)debug\s*:\s*true',
                    r'(?i)NODE_ENV.*development',
                    r'console\.(log|debug|info)\s*\(',
                ],
                severity=Severity.LOW,
                recommendation='Disable debug mode and remove console statements in production',
                file_types=['.js', '.ts', '.jsx', '.tsx', '.py', '.env']
            ),
        ]

    @staticmethod
    def consistency_checks() -> List[QualityCheck]:
        """Frontend/backend consistency checks"""
        return [
            QualityCheck(
                id='CON001',
                category=QualityCategory.CONSISTENCY,
                name='Inconsistent Naming Convention',
                description='Mixed naming conventions (camelCase vs snake_case)',
                patterns=[
                    r'(?<![a-z])([a-z]+_[a-z]+)\s*[=:]',  # snake_case
                    r'(?<![A-Z])([a-z]+[A-Z][a-z]+)\s*[=:]',  # camelCase
                ],
                severity=Severity.LOW,
                recommendation='Establish and enforce consistent naming conventions across the stack',
                file_types=['.js', '.ts', '.jsx', '.tsx', '.py']
            ),
            QualityCheck(
                id='CON002',
                category=QualityCategory.CONSISTENCY,
                name='Hardcoded API URL',
                description='API URLs hardcoded instead of using environment variables',
                patterns=[
                    r'(?i)(?:fetch|axios|http)\s*\(\s*["\']https?://(?!localhost)',
                    r'(?i)baseURL\s*:\s*["\']https?://(?!localhost)',
                    r'(?i)api[_-]?url\s*=\s*["\']https?://',
                ],
                severity=Severity.MEDIUM,
                recommendation='Use environment variables for API URLs (e.g., process.env.API_URL)',
                file_types=['.js', '.ts', '.jsx', '.tsx']
            ),
            QualityCheck(
                id='CON003',
                category=QualityCategory.CONSISTENCY,
                name='Missing Error Handling',
                description='API calls without proper error handling',
                patterns=[
                    r'(?i)await\s+fetch\s*\([^)]+\)\s*(?!\.catch|;|\s*\.\s*then)',
                    r'(?i)axios\.[a-z]+\s*\([^)]+\)\s*(?!\.catch)',
                ],
                severity=Severity.MEDIUM,
                recommendation='Add try-catch blocks or .catch() handlers for async operations',
                file_types=['.js', '.ts', '.jsx', '.tsx']
            ),
        ]

    @staticmethod
    def api_checks() -> List[QualityCheck]:
        """API contract validation checks"""
        return [
            QualityCheck(
                id='API001',
                category=QualityCategory.API_CONTRACT,
                name='Missing API Response Types',
                description='API endpoints without TypeScript response types',
                patterns=[
                    r'(?i)app\.(get|post|put|delete|patch)\s*\([^)]+,\s*(?:async\s*)?\([^:)]+\)\s*=>',
                    r'(?i)router\.(get|post|put|delete|patch)\s*\([^)]+,\s*(?:async\s*)?\([^:)]+\)\s*=>',
                ],
                severity=Severity.MEDIUM,
                recommendation='Add TypeScript types for request/response in API handlers',
                file_types=['.ts', '.tsx']
            ),
            QualityCheck(
                id='API002',
                category=QualityCategory.API_CONTRACT,
                name='Inconsistent HTTP Status Codes',
                description='Non-standard HTTP status codes in responses',
                patterns=[
                    r'(?i)res\.status\s*\(\s*(?!200|201|204|301|302|304|400|401|403|404|409|422|500|502|503)\d{3}\s*\)',
                    r'(?i)status_code\s*=\s*(?!200|201|204|301|302|304|400|401|403|404|409|422|500|502|503)\d{3}',
                ],
                severity=Severity.LOW,
                recommendation='Use standard HTTP status codes for consistent API behavior',
                file_types=['.js', '.ts', '.py']
            ),
            QualityCheck(
                id='API003',
                category=QualityCategory.API_CONTRACT,
                name='Missing Input Validation',
                description='API endpoints without input validation',
                patterns=[
                    r'(?i)req\.body\.[a-zA-Z]+(?!\s*\?\s*\.)',
                    r'(?i)req\.params\.[a-zA-Z]+(?!\s*\?\s*\.)',
                    r'(?i)req\.query\.[a-zA-Z]+(?!\s*\?\s*\.)',
                ],
                severity=Severity.HIGH,
                recommendation='Validate all user input with a schema validation library (Zod, Joi, etc.)',
                file_types=['.js', '.ts']
            ),
        ]

    @staticmethod
    def documentation_checks() -> List[QualityCheck]:
        """Documentation quality checks"""
        return [
            QualityCheck(
                id='DOC001',
                category=QualityCategory.DOCUMENTATION,
                name='Missing Function Documentation',
                description='Public functions without JSDoc/docstring comments',
                patterns=[
                    r'(?i)^(?!\s*/\*\*).*export\s+(?:async\s+)?function\s+[A-Z]',
                    r'(?i)^(?!\s*#).*def\s+[a-z_]+\s*\([^)]*\)\s*:',
                ],
                severity=Severity.LOW,
                recommendation='Add JSDoc comments for exported functions',
                file_types=['.js', '.ts', '.jsx', '.tsx', '.py']
            ),
            QualityCheck(
                id='DOC002',
                category=QualityCategory.DOCUMENTATION,
                name='TODO/FIXME Comment',
                description='Unresolved TODO or FIXME comments in code',
                patterns=[
                    r'(?i)//\s*TODO\s*:',
                    r'(?i)//\s*FIXME\s*:',
                    r'(?i)#\s*TODO\s*:',
                    r'(?i)#\s*FIXME\s*:',
                ],
                severity=Severity.INFO,
                recommendation='Resolve or track TODO/FIXME items in issue tracker',
                file_types=['.js', '.ts', '.jsx', '.tsx', '.py', '.go']
            ),
        ]

    @staticmethod
    def dependency_checks() -> List[QualityCheck]:
        """Dependency analysis checks"""
        return [
            QualityCheck(
                id='DEP001',
                category=QualityCategory.DEPENDENCIES,
                name='Wildcard Version',
                description='Dependency version using wildcard or latest',
                patterns=[
                    r'"[^"]+"\s*:\s*"\*"',
                    r'"[^"]+"\s*:\s*"latest"',
                    r'"[^"]+"\s*:\s*">=',
                ],
                severity=Severity.MEDIUM,
                recommendation='Pin dependency versions for reproducible builds',
                file_types=['package.json']
            ),
            QualityCheck(
                id='DEP002',
                category=QualityCategory.DEPENDENCIES,
                name='Deprecated Package Pattern',
                description='Usage of commonly deprecated packages',
                patterns=[
                    r'"request"\s*:',
                    r'"moment"\s*:',
                    r'"node-sass"\s*:',
                    r'"tslint"\s*:',
                ],
                severity=Severity.LOW,
                recommendation='Consider migrating to modern alternatives (axios, date-fns, sass, eslint)',
                file_types=['package.json']
            ),
        ]


# =============================================================================
# Main Analyzer Class
# =============================================================================

class CodeQualityAnalyzer:
    """Cross-stack code quality analyzer for fullstack projects"""

    SKIP_DIRS = {
        'node_modules', '__pycache__', '.git', '.svn', '.hg',
        'venv', 'env', '.venv', 'dist', 'build', '.tox',
        'vendor', 'third_party', '.idea', '.vscode', '.next',
        'coverage', '.nyc_output', '.pytest_cache', 'target'
    }

    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.vue', '.go',
        '.java', '.rb', '.php', '.html', '.css', '.scss'
    }

    CONFIG_FILES = {
        'package.json', 'requirements.txt', 'pyproject.toml',
        'tsconfig.json', '.eslintrc.js', '.eslintrc.json',
        'docker-compose.yml', 'Dockerfile'
    }

    def __init__(self, target_path: str, config: Optional[Dict] = None,
                 verbose: bool = False, checks: Optional[List[str]] = None):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        self.target_path = Path(target_path).resolve()
        self.config = config or {}
        self.verbose = verbose
        self.enabled_checks = checks  # None means all checks

        self.findings: List[QualityFinding] = []
        self.files_analyzed = 0
        self.lines_analyzed = 0
        self.coverage_data = CoverageData()

        # Load all check definitions
        self.checks = self._load_checks()

        # Track project structure
        self.has_frontend = False
        self.has_backend = False
        self.frontend_dir: Optional[Path] = None
        self.backend_dir: Optional[Path] = None

        logger.debug("CodeQualityAnalyzer initialized")

    def _load_checks(self) -> List[QualityCheck]:
        """Load all quality check definitions"""
        all_checks = []
        all_checks.extend(CheckDefinitions.security_checks())
        all_checks.extend(CheckDefinitions.consistency_checks())
        all_checks.extend(CheckDefinitions.api_checks())
        all_checks.extend(CheckDefinitions.documentation_checks())
        all_checks.extend(CheckDefinitions.dependency_checks())

        # Filter by enabled checks if specified
        if self.enabled_checks:
            enabled_categories = {c.upper() for c in self.enabled_checks}
            all_checks = [
                c for c in all_checks
                if c.category.name in enabled_categories
            ]

        return all_checks

    def run(self) -> Dict:
        """Execute the full quality analysis"""
        logger.debug("Starting quality analysis run")
        if self.verbose:
            print(f"Analyzing: {self.target_path}", file=sys.stderr)

        # Detect project structure
        self._detect_project_structure()

        # Run pattern-based checks
        self._scan_files()

        # Check test coverage if available
        self._analyze_coverage()

        # Check documentation
        self._analyze_documentation()

        # Build results
        return self._build_results()

    def _detect_project_structure(self):
        """Detect frontend/backend directories"""
        logger.debug("Detecting project structure")
        common_frontend = ['frontend', 'client', 'web', 'app', 'src/app', 'src/pages']
        common_backend = ['backend', 'server', 'api', 'src/api', 'src/server']

        for name in common_frontend:
            path = self.target_path / name
            if path.is_dir():
                self.has_frontend = True
                self.frontend_dir = path
                break

        for name in common_backend:
            path = self.target_path / name
            if path.is_dir():
                self.has_backend = True
                self.backend_dir = path
                break

        # Check for fullstack frameworks (Next.js, Nuxt, etc.)
        if (self.target_path / 'pages').is_dir() or (self.target_path / 'app').is_dir():
            # Likely Next.js or similar
            if (self.target_path / 'pages' / 'api').is_dir():
                self.has_backend = True
            self.has_frontend = True

        if self.verbose:
            print(f"Frontend detected: {self.has_frontend}", file=sys.stderr)
            print(f"Backend detected: {self.has_backend}", file=sys.stderr)

    def _should_skip_dir(self, path: Path) -> bool:
        """Check if directory should be skipped"""
        return path.name in self.SKIP_DIRS or path.name.startswith('.')

    def _scan_files(self):
        """Scan all files and run pattern checks"""
        for root, dirs, files in os.walk(self.target_path):
            # Filter directories in-place
            dirs[:] = [d for d in dirs if not self._should_skip_dir(Path(root) / d)]

            for filename in files:
                file_path = Path(root) / filename
                suffix = file_path.suffix.lower()

                # Check if file should be analyzed
                if suffix not in self.CODE_EXTENSIONS and filename not in self.CONFIG_FILES:
                    continue

                self._analyze_file(file_path)

    def _analyze_file(self, file_path: Path):
        """Analyze a single file for quality issues"""
        logger.debug(f"Analyzing file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except (IOError, OSError) as e:
            logger.error(f"Could not read {file_path}: {e}")
            if self.verbose:
                print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
            return

        self.files_analyzed += 1
        self.lines_analyzed += len(lines)

        rel_path = str(file_path.relative_to(self.target_path))
        suffix = file_path.suffix.lower()
        filename = file_path.name.lower()

        # Run applicable checks
        for check in self.checks:
            # Check if this check applies to this file type
            if check.file_types:
                applicable = any(
                    suffix == ft or filename == ft.lower()
                    for ft in check.file_types
                )
                if not applicable:
                    continue

            # Run pattern matching
            for pattern in check.patterns:
                try:
                    regex = re.compile(pattern, re.MULTILINE)
                    for i, line in enumerate(lines, 1):
                        if regex.search(line):
                            finding = QualityFinding(
                                check=check,
                                file_path=rel_path,
                                line_number=i,
                                line_content=line.strip()[:100],
                                details=f"Pattern matched: {check.name}"
                            )
                            self.findings.append(finding)
                except re.error as e:
                    if self.verbose:
                        print(f"Warning: Invalid regex pattern: {e}", file=sys.stderr)

    def _analyze_coverage(self):
        """Analyze test coverage if coverage files exist"""
        # Check for lcov.info
        lcov_path = self.target_path / 'coverage' / 'lcov.info'
        if lcov_path.exists():
            self._parse_lcov(lcov_path)
            return

        # Check for coverage.xml (cobertura format)
        coverage_xml = self.target_path / 'coverage.xml'
        if coverage_xml.exists():
            self._parse_cobertura(coverage_xml)
            return

        # Check for pytest coverage
        pytest_cov = self.target_path / '.coverage'
        if pytest_cov.exists():
            # Just note that coverage exists but can't be parsed without sqlite3
            if self.verbose:
                print("Found .coverage file (pytest)", file=sys.stderr)

    def _parse_lcov(self, lcov_path: Path):
        """Parse lcov.info coverage file"""
        try:
            with open(lcov_path, 'r') as f:
                content = f.read()

            total_lines = 0
            covered_lines = 0
            current_file = None
            uncovered_files = []

            for line in content.split('\n'):
                if line.startswith('SF:'):
                    current_file = line[3:]
                elif line.startswith('LF:'):
                    total_lines += int(line[3:])
                elif line.startswith('LH:'):
                    file_covered = int(line[3:])
                    covered_lines += file_covered
                    if current_file and file_covered == 0:
                        uncovered_files.append(current_file)

            if total_lines > 0:
                self.coverage_data = CoverageData(
                    total_lines=total_lines,
                    covered_lines=covered_lines,
                    coverage_percent=round(covered_lines / total_lines * 100, 2),
                    uncovered_files=uncovered_files[:10]  # Top 10
                )

                # Add finding if coverage is low
                if self.coverage_data.coverage_percent < 50:
                    self.findings.append(QualityFinding(
                        check=QualityCheck(
                            id='COV001',
                            category=QualityCategory.TEST_COVERAGE,
                            name='Low Test Coverage',
                            description='Test coverage below 50%',
                            patterns=[],
                            severity=Severity.HIGH,
                            recommendation='Increase test coverage to at least 70%'
                        ),
                        file_path='coverage/lcov.info',
                        line_number=0,
                        line_content=f'Coverage: {self.coverage_data.coverage_percent}%',
                        details=f'Current coverage: {self.coverage_data.coverage_percent}%'
                    ))
        except Exception as e:
            if self.verbose:
                print(f"Warning: Could not parse lcov: {e}", file=sys.stderr)

    def _parse_cobertura(self, xml_path: Path):
        """Parse cobertura XML coverage file"""
        try:
            with open(xml_path, 'r') as f:
                content = f.read()

            # Simple regex parsing (avoiding xml.etree for simplicity)
            line_rate_match = re.search(r'line-rate="([0-9.]+)"', content)
            if line_rate_match:
                coverage_percent = float(line_rate_match.group(1)) * 100
                self.coverage_data.coverage_percent = round(coverage_percent, 2)

                if coverage_percent < 50:
                    self.findings.append(QualityFinding(
                        check=QualityCheck(
                            id='COV001',
                            category=QualityCategory.TEST_COVERAGE,
                            name='Low Test Coverage',
                            description='Test coverage below 50%',
                            patterns=[],
                            severity=Severity.HIGH,
                            recommendation='Increase test coverage to at least 70%'
                        ),
                        file_path='coverage.xml',
                        line_number=0,
                        line_content=f'Coverage: {coverage_percent:.1f}%',
                        details=f'Current coverage: {coverage_percent:.1f}%'
                    ))
        except Exception as e:
            if self.verbose:
                print(f"Warning: Could not parse cobertura: {e}", file=sys.stderr)

    def _analyze_documentation(self):
        """Check documentation quality"""
        # Check for README
        readme_files = ['README.md', 'README.rst', 'README.txt', 'readme.md']
        has_readme = any((self.target_path / f).exists() for f in readme_files)

        if not has_readme:
            self.findings.append(QualityFinding(
                check=QualityCheck(
                    id='DOC003',
                    category=QualityCategory.DOCUMENTATION,
                    name='Missing README',
                    description='Project lacks a README file',
                    patterns=[],
                    severity=Severity.MEDIUM,
                    recommendation='Add a README.md with project overview and setup instructions'
                ),
                file_path='.',
                line_number=0,
                line_content='',
                details='No README file found'
            ))
        else:
            # Check README completeness
            self._check_readme_quality()

        # Check for API documentation
        api_docs = ['openapi.yaml', 'openapi.json', 'swagger.yaml', 'swagger.json']
        has_api_docs = any((self.target_path / f).exists() for f in api_docs)
        docs_dir = self.target_path / 'docs'

        if self.has_backend and not has_api_docs and not docs_dir.exists():
            self.findings.append(QualityFinding(
                check=QualityCheck(
                    id='DOC004',
                    category=QualityCategory.DOCUMENTATION,
                    name='Missing API Documentation',
                    description='Backend project lacks OpenAPI/Swagger documentation',
                    patterns=[],
                    severity=Severity.LOW,
                    recommendation='Add OpenAPI specification for API endpoints'
                ),
                file_path='.',
                line_number=0,
                line_content='',
                details='No OpenAPI/Swagger documentation found'
            ))

    def _check_readme_quality(self):
        """Check README file quality"""
        logger.debug("Checking README quality")
        readme_path = None
        for name in ['README.md', 'readme.md', 'README.rst']:
            path = self.target_path / name
            if path.exists():
                readme_path = path
                break

        if not readme_path:
            logger.warning("No README file found")
            return

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            # Check for essential sections
            essential_sections = {
                'installation': ['install', 'setup', 'getting started'],
                'usage': ['usage', 'how to use', 'example'],
                'license': ['license', 'mit', 'apache', 'gpl'],
            }

            missing_sections = []
            for section, keywords in essential_sections.items():
                if not any(kw in content for kw in keywords):
                    missing_sections.append(section)

            if missing_sections:
                self.findings.append(QualityFinding(
                    check=QualityCheck(
                        id='DOC005',
                        category=QualityCategory.DOCUMENTATION,
                        name='Incomplete README',
                        description='README missing essential sections',
                        patterns=[],
                        severity=Severity.INFO,
                        recommendation=f'Add sections for: {", ".join(missing_sections)}'
                    ),
                    file_path='README.md',
                    line_number=0,
                    line_content='',
                    details=f'Missing: {", ".join(missing_sections)}'
                ))
        except Exception as e:
            if self.verbose:
                print(f"Warning: Could not analyze README: {e}", file=sys.stderr)

    def _build_results(self) -> Dict:
        """Build the final results dictionary"""
        # Count findings by severity and category
        by_severity = defaultdict(int)
        by_category = defaultdict(int)

        for finding in self.findings:
            by_severity[finding.check.severity.name] += 1
            by_category[finding.check.category.value] += 1

        # Calculate quality score (0-100)
        # Deduct points based on severity
        score = 100
        score -= by_severity.get('CRITICAL', 0) * 15
        score -= by_severity.get('HIGH', 0) * 10
        score -= by_severity.get('MEDIUM', 0) * 5
        score -= by_severity.get('LOW', 0) * 2
        score -= by_severity.get('INFO', 0) * 0.5
        score = max(0, min(100, score))

        # Generate recommendations
        recommendations = self._generate_recommendations()

        return {
            'timestamp': datetime.now().isoformat(),
            'target': str(self.target_path),
            'project_structure': {
                'has_frontend': self.has_frontend,
                'has_backend': self.has_backend,
                'frontend_dir': str(self.frontend_dir) if self.frontend_dir else None,
                'backend_dir': str(self.backend_dir) if self.backend_dir else None,
            },
            'scan_stats': {
                'files_analyzed': self.files_analyzed,
                'lines_analyzed': self.lines_analyzed,
                'checks_run': len(self.checks),
            },
            'coverage': {
                'total_lines': self.coverage_data.total_lines,
                'covered_lines': self.coverage_data.covered_lines,
                'coverage_percent': self.coverage_data.coverage_percent,
                'uncovered_files': self.coverage_data.uncovered_files,
            },
            'summary': {
                'quality_score': round(score, 1),
                'total_findings': len(self.findings),
                'critical': by_severity.get('CRITICAL', 0),
                'high': by_severity.get('HIGH', 0),
                'medium': by_severity.get('MEDIUM', 0),
                'low': by_severity.get('LOW', 0),
                'info': by_severity.get('INFO', 0),
            },
            'by_category': dict(by_category),
            'findings': [
                {
                    'check_id': f.check.id,
                    'category': f.check.category.value,
                    'name': f.check.name,
                    'severity': f.check.severity.name,
                    'file': f.file_path,
                    'line': f.line_number,
                    'content': f.line_content,
                    'description': f.check.description,
                    'recommendation': f.check.recommendation,
                }
                for f in sorted(
                    self.findings,
                    key=lambda x: (x.check.severity.value, x.file_path),
                    reverse=True
                )
            ],
            'recommendations': recommendations,
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []

        # Group findings by check ID to avoid duplicates
        check_counts = defaultdict(int)
        for finding in self.findings:
            check_counts[finding.check.id] += 1

        # Sort by severity and count
        severity_order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
            Severity.INFO: 4,
        }

        seen_recs = set()
        for finding in sorted(
            self.findings,
            key=lambda x: (severity_order[x.check.severity], -check_counts[x.check.id])
        ):
            rec = f"[{finding.check.severity.name}] {finding.check.recommendation}"
            if rec not in seen_recs:
                recommendations.append(rec)
                seen_recs.add(rec)

        return recommendations[:15]  # Top 15 recommendations


# =============================================================================
# Output Formatting
# =============================================================================

class OutputFormatter:
    """Format analysis results for output"""

    @staticmethod
    def format_text(results: Dict, verbose: bool = False) -> str:
        """Format results as human-readable text"""
        lines = []
        lines.append("=" * 80)
        lines.append("CODE QUALITY ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"Timestamp: {results['timestamp']}")
        lines.append(f"Target: {results['target']}")
        lines.append("")

        # Project Structure
        ps = results['project_structure']
        lines.append("PROJECT STRUCTURE")
        lines.append("-" * 40)
        lines.append(f"  Frontend detected: {'Yes' if ps['has_frontend'] else 'No'}")
        lines.append(f"  Backend detected: {'Yes' if ps['has_backend'] else 'No'}")
        lines.append("")

        # Scan Stats
        stats = results['scan_stats']
        lines.append("SCAN STATISTICS")
        lines.append("-" * 40)
        lines.append(f"  Files analyzed: {stats['files_analyzed']}")
        lines.append(f"  Lines analyzed: {stats['lines_analyzed']:,}")
        lines.append(f"  Checks run: {stats['checks_run']}")
        lines.append("")

        # Coverage
        cov = results['coverage']
        if cov['total_lines'] > 0:
            lines.append("TEST COVERAGE")
            lines.append("-" * 40)
            lines.append(f"  Coverage: {cov['coverage_percent']}%")
            lines.append(f"  Lines: {cov['covered_lines']:,} / {cov['total_lines']:,}")
            lines.append("")

        # Summary
        summary = results['summary']
        lines.append("QUALITY SUMMARY")
        lines.append("-" * 40)

        # Score with color indicator
        score = summary['quality_score']
        if score >= 80:
            grade = "EXCELLENT"
        elif score >= 60:
            grade = "GOOD"
        elif score >= 40:
            grade = "NEEDS IMPROVEMENT"
        else:
            grade = "POOR"

        lines.append(f"  Quality Score: {score}/100 ({grade})")
        lines.append(f"  Total Findings: {summary['total_findings']}")
        lines.append(f"    Critical: {summary['critical']}")
        lines.append(f"    High: {summary['high']}")
        lines.append(f"    Medium: {summary['medium']}")
        lines.append(f"    Low: {summary['low']}")
        lines.append(f"    Info: {summary['info']}")
        lines.append("")

        # Findings by category
        if results['by_category']:
            lines.append("FINDINGS BY CATEGORY")
            lines.append("-" * 40)
            for category, count in sorted(
                results['by_category'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                lines.append(f"  {category}: {count}")
            lines.append("")

        # Detailed findings (if verbose or few findings)
        findings = results['findings']
        if findings:
            show_count = len(findings) if verbose else min(10, len(findings))
            lines.append(f"TOP FINDINGS ({show_count} of {len(findings)})")
            lines.append("-" * 40)

            for finding in findings[:show_count]:
                lines.append(f"  [{finding['severity']}] {finding['name']}")
                lines.append(f"    File: {finding['file']}:{finding['line']}")
                if finding['content']:
                    lines.append(f"    Code: {finding['content'][:60]}...")
                lines.append(f"    Fix: {finding['recommendation']}")
                lines.append("")

        # Recommendations
        if results['recommendations']:
            lines.append("RECOMMENDATIONS")
            lines.append("-" * 40)
            for i, rec in enumerate(results['recommendations'][:10], 1):
                lines.append(f"  {i}. {rec}")
            lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)

    @staticmethod
    def format_json(results: Dict) -> str:
        """Format results as JSON"""
        return json.dumps(results, indent=2)

    @staticmethod
    def format_csv(results: Dict) -> str:
        """Format findings as CSV"""
        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            'check_id', 'category', 'name', 'severity',
            'file', 'line', 'description', 'recommendation'
        ])

        # Data rows
        for finding in results['findings']:
            writer.writerow([
                finding['check_id'],
                finding['category'],
                finding['name'],
                finding['severity'],
                finding['file'],
                finding['line'],
                finding['description'],
                finding['recommendation']
            ])

        return output.getvalue()


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Code Quality Analyzer - Cross-stack quality analysis tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a project directory
  %(prog)s --input /path/to/project

  # Generate JSON report
  %(prog)s --input ./project --output json --file report.json

  # Run only security checks
  %(prog)s --input ./project --checks security

  # Run multiple check categories
  %(prog)s --input ./project --checks security,api_contract,consistency

Check Categories:
  - security: Hardcoded credentials, SQL injection, XSS vulnerabilities
  - consistency: Naming conventions, hardcoded URLs, error handling
  - api_contract: Response types, status codes, input validation
  - documentation: README, JSDoc, TODO comments
  - dependencies: Version pinning, deprecated packages
  - test_coverage: Coverage analysis from lcov/cobertura

Quality Score:
  - 80-100: EXCELLENT - Well-maintained codebase
  - 60-79: GOOD - Minor improvements needed
  - 40-59: NEEDS IMPROVEMENT - Significant issues present
  - 0-39: POOR - Critical issues requiring immediate attention
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Project directory to analyze'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )

    parser.add_argument(
        '--config', '-c',
        help='Configuration file path (JSON)'
    )

    parser.add_argument(
        '--checks',
        help='Comma-separated list of check categories to run'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Validate input
    if not os.path.exists(args.target):
        print(f"Error: Target path does not exist: {args.target}", file=sys.stderr)
        sys.exit(1)

    # Load config if provided
    config = {}
    if args.config and os.path.exists(args.config):
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid config file: {e}", file=sys.stderr)
            sys.exit(1)

    # Parse checks filter
    checks = None
    if args.checks:
        checks = [c.strip().upper() for c in args.checks.split(',')]

    try:
        # Run analysis
        analyzer = CodeQualityAnalyzer(
            target_path=args.target,
            config=config,
            verbose=args.verbose,
            checks=checks
        )
        results = analyzer.run()

        # Format output
        formatter = OutputFormatter()
        if args.output == 'json':
            output_text = formatter.format_json(results)
        elif args.output == 'csv':
            output_text = formatter.format_csv(results)
        else:
            output_text = formatter.format_text(results, verbose=args.verbose)

        # Write output
        if args.file:
            with open(args.file, 'w') as f:
                f.write(output_text)
            if args.verbose:
                print(f"Report saved to: {args.file}", file=sys.stderr)
        else:
            print(output_text)

        # Exit code based on findings
        if results['summary']['critical'] > 0:
            sys.exit(2)
        elif results['summary']['high'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\nAnalysis interrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
