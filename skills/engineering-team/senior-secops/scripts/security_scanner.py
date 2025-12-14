#!/usr/bin/env python3
"""
Security Scanner - SAST-lite Static Application Security Testing

Automated security scanning tool that detects:
- Secret detection (API keys, passwords, tokens, credentials)
- Hardcoded credentials and sensitive data exposure
- Unsafe code patterns (eval, exec, shell injection vectors)
- OWASP Top 10 vulnerability patterns

Part of the senior-secops skill package.
"""

import argparse
import csv
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class Severity(Enum):
    """Security issue severity levels"""
    CRITICAL = 4  # Immediate security risk - secrets, RCE
    HIGH = 3      # Significant security risk - injection, auth issues
    MEDIUM = 2    # Moderate security risk - weak patterns
    LOW = 1       # Minor security risk - best practice violation
    INFO = 0      # Informational findings


@dataclass
class SecurityPattern:
    """Pattern definition for security scanning"""
    id: str
    name: str
    regex: str
    severity: Severity
    category: str
    description: str
    recommendation: str
    owasp: Optional[str] = None
    cwe_id: Optional[str] = None


@dataclass
class Finding:
    """A security finding from the scan"""
    finding_id: str
    pattern_id: str
    severity: str
    category: str
    type: str
    file_path: str
    line_number: int
    line_content: str
    description: str
    recommendation: str
    owasp: Optional[str] = None
    cwe_id: Optional[str] = None


class SecurityScanner:
    """SAST-lite security scanner for codebases"""

    # File extensions to scan
    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.rb', '.php',
        '.go', '.cs', '.c', '.cpp', '.h', '.hpp', '.rs', '.swift',
        '.kt', '.scala', '.sql', '.sh', '.bash', '.ps1', '.psm1'
    }

    CONFIG_EXTENSIONS = {
        '.env', '.ini', '.cfg', '.conf', '.config', '.yaml', '.yml',
        '.json', '.xml', '.properties', '.toml'
    }

    SKIP_DIRS = {
        'node_modules', '__pycache__', '.git', '.svn', '.hg',
        'venv', 'env', '.venv', 'dist', 'build', '.tox',
        '.pytest_cache', '.mypy_cache', 'coverage', 'vendor',
        'third_party', '.idea', '.vscode', '.next', '.nuxt'
    }

    SKIP_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.tar',
        '.gz', '.rar', '.7z', '.mp3', '.mp4', '.avi', '.mov',
        '.exe', '.dll', '.so', '.dylib', '.pyc', '.pyo', '.class',
        '.jar', '.war', '.woff', '.woff2', '.ttf', '.eot', '.lock'
    }

    def __init__(self, target_path: str, config: Optional[Dict] = None,
                 verbose: bool = False):
        self.target_path = Path(target_path)
        self.config = config or {}
        self.verbose = verbose
        self.findings: List[Finding] = []
        self.files_scanned = 0
        self.lines_scanned = 0
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> List[SecurityPattern]:
        """Load all security detection patterns"""
        patterns = []
        patterns.extend(self._secret_patterns())
        patterns.extend(self._injection_patterns())
        patterns.extend(self._owasp_patterns())
        patterns.extend(self._unsafe_patterns())
        return patterns

    def _secret_patterns(self) -> List[SecurityPattern]:
        """Patterns for detecting hardcoded secrets"""
        return [
            # AWS Credentials
            SecurityPattern(
                id='SEC001', name='AWS Access Key ID',
                regex=r'(?i)(?:aws_access_key_id|aws_access_key)\s*[=:]\s*["\']?(AKIA[0-9A-Z]{16})["\']?',
                severity=Severity.CRITICAL, category='Secrets',
                description='AWS Access Key ID detected in code',
                recommendation='Move AWS credentials to environment variables or AWS Secrets Manager',
                cwe_id='CWE-798'
            ),
            SecurityPattern(
                id='SEC002', name='AWS Secret Access Key',
                regex=r'(?i)(?:aws_secret_access_key|aws_secret_key)\s*[=:]\s*["\']?([A-Za-z0-9/+=]{40})["\']?',
                severity=Severity.CRITICAL, category='Secrets',
                description='AWS Secret Access Key detected in code',
                recommendation='Move AWS credentials to environment variables or AWS Secrets Manager',
                cwe_id='CWE-798'
            ),
            # API Keys
            SecurityPattern(
                id='SEC003', name='Generic API Key',
                regex=r'(?i)(?:api[_-]?key|apikey|api[_-]?secret)\s*[=:]\s*["\']([A-Za-z0-9_\-]{20,})["\']',
                severity=Severity.HIGH, category='Secrets',
                description='API key detected in code',
                recommendation='Store API keys in environment variables or secret management system',
                cwe_id='CWE-798'
            ),
            # Private Keys
            SecurityPattern(
                id='SEC004', name='Private Key',
                regex=r'-----BEGIN\s+(?:RSA\s+|EC\s+|DSA\s+|OPENSSH\s+)?PRIVATE\s+KEY-----',
                severity=Severity.CRITICAL, category='Secrets',
                description='Private key detected in code',
                recommendation='Remove private keys from codebase, use secure key management',
                cwe_id='CWE-321'
            ),
            # Passwords
            SecurityPattern(
                id='SEC005', name='Hardcoded Password',
                regex=r'(?i)(?:password|passwd|pwd|secret)\s*[=:]\s*["\']([^"\'\s]{8,})["\']',
                severity=Severity.HIGH, category='Secrets',
                description='Hardcoded password detected',
                recommendation='Use environment variables or secure credential storage',
                cwe_id='CWE-798'
            ),
            # Database Connection Strings
            SecurityPattern(
                id='SEC006', name='Database Connection String',
                regex=r'(?i)(?:mongodb|mysql|postgresql|postgres|redis|mssql)://[a-zA-Z0-9_\-]+:[^@\s]+@',
                severity=Severity.HIGH, category='Secrets',
                description='Database connection string with credentials detected',
                recommendation='Use environment variables for database credentials',
                cwe_id='CWE-798'
            ),
            # JWT Secrets
            SecurityPattern(
                id='SEC007', name='JWT Secret',
                regex=r'(?i)(?:jwt[_-]?secret|jwt[_-]?key|token[_-]?secret)\s*[=:]\s*["\']([A-Za-z0-9_\-]{16,})["\']',
                severity=Severity.CRITICAL, category='Secrets',
                description='JWT secret key detected',
                recommendation='Store JWT secrets in environment variables',
                cwe_id='CWE-798'
            ),
            # GitHub Tokens
            SecurityPattern(
                id='SEC008', name='GitHub Token',
                regex=r'gh[pousr]_[A-Za-z0-9_]{36,}',
                severity=Severity.HIGH, category='Secrets',
                description='GitHub personal access token detected',
                recommendation='Use GitHub Actions secrets or environment variables',
                cwe_id='CWE-798'
            ),
            # Slack Tokens
            SecurityPattern(
                id='SEC009', name='Slack Token',
                regex=r'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,}',
                severity=Severity.HIGH, category='Secrets',
                description='Slack API token detected',
                recommendation='Use environment variables for Slack tokens',
                cwe_id='CWE-798'
            ),
            # Google API Key
            SecurityPattern(
                id='SEC010', name='Google API Key',
                regex=r'AIza[0-9A-Za-z\-_]{35}',
                severity=Severity.HIGH, category='Secrets',
                description='Google API key detected',
                recommendation='Use environment variables and restrict API key scope',
                cwe_id='CWE-798'
            ),
            # Stripe Keys
            SecurityPattern(
                id='SEC011', name='Stripe API Key',
                regex=r'(?:sk|pk|rk)_(?:live|test)_[0-9a-zA-Z]{24,}',
                severity=Severity.CRITICAL, category='Secrets',
                description='Stripe API key detected',
                recommendation='Store Stripe keys in environment variables',
                cwe_id='CWE-798'
            ),
            # SendGrid API Key
            SecurityPattern(
                id='SEC012', name='SendGrid API Key',
                regex=r'SG\.[a-zA-Z0-9]{22}\.[a-zA-Z0-9]{43}',
                severity=Severity.HIGH, category='Secrets',
                description='SendGrid API key detected',
                recommendation='Store SendGrid keys in environment variables',
                cwe_id='CWE-798'
            ),
        ]

    def _injection_patterns(self) -> List[SecurityPattern]:
        """Patterns for detecting injection vulnerabilities"""
        return [
            # SQL Injection
            SecurityPattern(
                id='INJ001', name='SQL Injection - String Concatenation',
                regex=r'(?i)(?:execute|exec|query|cursor\.execute)\s*\([^)]*["\'].*?\s*\+\s*',
                severity=Severity.CRITICAL, category='Injection',
                description='Potential SQL injection - string concatenation in query',
                recommendation='Use parameterized queries or prepared statements',
                owasp='A03:2021', cwe_id='CWE-89'
            ),
            SecurityPattern(
                id='INJ002', name='SQL Injection - Format String',
                regex=r'(?i)(?:execute|cursor\.execute)\s*\(\s*["\'].*?%s.*?["\'].*?%\s*\(',
                severity=Severity.CRITICAL, category='Injection',
                description='Potential SQL injection - using format strings',
                recommendation='Use parameterized queries with proper escaping',
                owasp='A03:2021', cwe_id='CWE-89'
            ),
            SecurityPattern(
                id='INJ003', name='SQL Injection - f-string',
                regex=r'(?i)(?:execute|cursor\.execute)\s*\(\s*f["\'].*?\{.*?\}',
                severity=Severity.CRITICAL, category='Injection',
                description='Potential SQL injection - f-string in query',
                recommendation='Use parameterized queries instead of f-strings',
                owasp='A03:2021', cwe_id='CWE-89'
            ),
            # Command Injection
            SecurityPattern(
                id='INJ004', name='Command Injection - os.system',
                regex=r'(?i)os\.system\s*\([^)]*["\'].*?\+|os\.system\s*\(\s*f["\']',
                severity=Severity.CRITICAL, category='Injection',
                description='Potential command injection via os.system',
                recommendation='Use subprocess with shell=False and argument list',
                owasp='A03:2021', cwe_id='CWE-78'
            ),
            SecurityPattern(
                id='INJ005', name='Command Injection - subprocess shell',
                regex=r'(?i)subprocess\.(?:call|run|Popen)\s*\([^)]*shell\s*=\s*True',
                severity=Severity.HIGH, category='Injection',
                description='Subprocess with shell=True can be dangerous',
                recommendation='Use shell=False with proper argument list',
                owasp='A03:2021', cwe_id='CWE-78'
            ),
            # XSS
            SecurityPattern(
                id='INJ006', name='XSS - innerHTML',
                regex=r'(?i)\.innerHTML\s*=\s*[^"\']*(?:request|input|params)',
                severity=Severity.HIGH, category='Injection',
                description='Potential XSS via innerHTML assignment',
                recommendation='Use textContent or sanitize HTML with DOMPurify',
                owasp='A03:2021', cwe_id='CWE-79'
            ),
            SecurityPattern(
                id='INJ007', name='XSS - React dangerouslySetInnerHTML',
                regex=r'dangerouslySetInnerHTML\s*=\s*\{',
                severity=Severity.HIGH, category='Injection',
                description='dangerouslySetInnerHTML can lead to XSS',
                recommendation='Sanitize HTML with DOMPurify before use',
                owasp='A03:2021', cwe_id='CWE-79'
            ),
            # LDAP Injection
            SecurityPattern(
                id='INJ008', name='LDAP Injection',
                regex=r'(?i)ldap_search\s*\([^)]*\+',
                severity=Severity.HIGH, category='Injection',
                description='Potential LDAP injection',
                recommendation='Sanitize LDAP query inputs',
                owasp='A03:2021', cwe_id='CWE-90'
            ),
            # XPath Injection
            SecurityPattern(
                id='INJ009', name='XPath Injection',
                regex=r'(?i)xpath\s*\([^)]*\+',
                severity=Severity.HIGH, category='Injection',
                description='Potential XPath injection',
                recommendation='Use parameterized XPath queries',
                owasp='A03:2021', cwe_id='CWE-643'
            ),
        ]

    def _owasp_patterns(self) -> List[SecurityPattern]:
        """Patterns for OWASP Top 10 issues"""
        return [
            # A01:2021 - Broken Access Control
            SecurityPattern(
                id='OWA001', name='Open Redirect',
                regex=r'(?i)(?:redirect|location\.href|window\.location)\s*=\s*[^"\']*(?:request|params|query)',
                severity=Severity.MEDIUM, category='Access Control',
                description='Potential open redirect vulnerability',
                recommendation='Validate redirect URLs against whitelist',
                owasp='A01:2021', cwe_id='CWE-601'
            ),
            SecurityPattern(
                id='OWA002', name='Path Traversal',
                regex=r'(?i)(?:open|fopen|readFile|file_get_contents)\s*\([^)]*(?:request|params|input)',
                severity=Severity.HIGH, category='Access Control',
                description='Potential path traversal vulnerability',
                recommendation='Validate and sanitize file paths, use whitelisting',
                owasp='A01:2021', cwe_id='CWE-22'
            ),
            # A02:2021 - Cryptographic Failures
            SecurityPattern(
                id='OWA003', name='Weak Hash - MD5',
                regex=r'(?i)(?:md5|hashlib\.md5)\s*\(',
                severity=Severity.MEDIUM, category='Cryptography',
                description='MD5 is cryptographically broken',
                recommendation='Use SHA-256 or better for hashing, bcrypt/argon2 for passwords',
                owasp='A02:2021', cwe_id='CWE-327'
            ),
            SecurityPattern(
                id='OWA004', name='Weak Hash - SHA1',
                regex=r'(?i)(?:sha1|hashlib\.sha1)\s*\(',
                severity=Severity.MEDIUM, category='Cryptography',
                description='SHA1 is cryptographically weak',
                recommendation='Use SHA-256 or SHA-3 for hashing',
                owasp='A02:2021', cwe_id='CWE-327'
            ),
            SecurityPattern(
                id='OWA005', name='Weak Random',
                regex=r'(?i)(?:random\.random|Math\.random|rand\(\))',
                severity=Severity.MEDIUM, category='Cryptography',
                description='Weak random number generator for security contexts',
                recommendation='Use secrets module (Python) or crypto.randomBytes (Node.js)',
                owasp='A02:2021', cwe_id='CWE-338'
            ),
            SecurityPattern(
                id='OWA006', name='SSL Verification Disabled',
                regex=r'(?i)(?:verify\s*[=:]\s*False|ssl_verify\s*=\s*false|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*["\']0["\']|rejectUnauthorized\s*:\s*false)',
                severity=Severity.HIGH, category='Cryptography',
                description='SSL/TLS certificate verification disabled',
                recommendation='Enable SSL verification to prevent MITM attacks',
                owasp='A02:2021', cwe_id='CWE-295'
            ),
            # A05:2021 - Security Misconfiguration
            SecurityPattern(
                id='OWA007', name='Debug Mode Enabled',
                regex=r'(?i)(?:DEBUG|debug)\s*[=:]\s*(?:true|True|TRUE|1|["\']true["\'])',
                severity=Severity.MEDIUM, category='Configuration',
                description='Debug mode enabled - information disclosure risk',
                recommendation='Disable debug mode in production',
                owasp='A05:2021', cwe_id='CWE-489'
            ),
            SecurityPattern(
                id='OWA008', name='CORS Wildcard',
                regex=r'(?i)Access-Control-Allow-Origin\s*[=:]\s*[\'"]\*[\'"]',
                severity=Severity.MEDIUM, category='Configuration',
                description='CORS allows all origins (*)',
                recommendation='Restrict CORS to specific trusted origins',
                owasp='A05:2021', cwe_id='CWE-942'
            ),
            # A07:2021 - Authentication Failures
            SecurityPattern(
                id='OWA009', name='Hardcoded Admin Credentials',
                regex=r'(?i)(?:admin|root|administrator)\s*[=:]\s*["\'][^"\']+["\']',
                severity=Severity.HIGH, category='Authentication',
                description='Hardcoded admin credentials detected',
                recommendation='Use environment variables for credentials',
                owasp='A07:2021', cwe_id='CWE-798'
            ),
            SecurityPattern(
                id='OWA010', name='Plain Text Password Comparison',
                regex=r'(?i)password\s*==\s*["\'][^"\']+["\']',
                severity=Severity.CRITICAL, category='Authentication',
                description='Plain text password comparison',
                recommendation='Hash passwords with bcrypt, argon2, or scrypt',
                owasp='A07:2021', cwe_id='CWE-916'
            ),
            # A08:2021 - Software and Data Integrity
            SecurityPattern(
                id='OWA011', name='Insecure Deserialization - pickle',
                regex=r'(?i)pickle\.(?:load|loads)\s*\(',
                severity=Severity.CRITICAL, category='Deserialization',
                description='Insecure deserialization - pickle can execute arbitrary code',
                recommendation='Use json.loads or implement input validation',
                owasp='A08:2021', cwe_id='CWE-502'
            ),
            SecurityPattern(
                id='OWA012', name='Insecure Deserialization - yaml',
                regex=r'(?i)yaml\.(?:load|unsafe_load)\s*\([^)]*(?:Loader\s*=\s*yaml\.(?:Loader|UnsafeLoader|FullLoader))?',
                severity=Severity.CRITICAL, category='Deserialization',
                description='yaml.load without safe_load can execute arbitrary code',
                recommendation='Use yaml.safe_load() instead',
                owasp='A08:2021', cwe_id='CWE-502'
            ),
            # A10:2021 - SSRF
            SecurityPattern(
                id='OWA013', name='Server-Side Request Forgery',
                regex=r'(?i)(?:requests\.get|urllib\.request\.urlopen|fetch)\s*\([^)]*(?:request|params|input)',
                severity=Severity.HIGH, category='SSRF',
                description='Potential SSRF - user input in URL request',
                recommendation='Validate and whitelist allowed URLs/domains',
                owasp='A10:2021', cwe_id='CWE-918'
            ),
        ]

    def _unsafe_patterns(self) -> List[SecurityPattern]:
        """Patterns for unsafe code practices"""
        return [
            SecurityPattern(
                id='UNS001', name='Eval Usage',
                regex=r'(?i)(?<!\.)\beval\s*\(',
                severity=Severity.HIGH, category='Unsafe Code',
                description='eval() can execute arbitrary code',
                recommendation='Avoid eval(), use safe alternatives like ast.literal_eval',
                cwe_id='CWE-95'
            ),
            SecurityPattern(
                id='UNS002', name='Exec Usage',
                regex=r'(?i)(?<!\.)\bexec\s*\(',
                severity=Severity.HIGH, category='Unsafe Code',
                description='exec() can execute arbitrary code',
                recommendation='Avoid exec(), use safer alternatives',
                cwe_id='CWE-95'
            ),
            SecurityPattern(
                id='UNS003', name='Compile with exec mode',
                regex=r'(?i)compile\s*\([^)]*,\s*["\']exec["\']',
                severity=Severity.HIGH, category='Unsafe Code',
                description='compile() with exec mode can be dangerous',
                recommendation='Avoid dynamic code compilation',
                cwe_id='CWE-95'
            ),
            SecurityPattern(
                id='UNS004', name='Assert Statement',
                regex=r'(?i)^\s*assert\s+',
                severity=Severity.LOW, category='Unsafe Code',
                description='Assert statements are removed in optimized mode',
                recommendation='Use proper validation instead of assert for security checks',
                cwe_id='CWE-617'
            ),
            SecurityPattern(
                id='UNS005', name='Unrestricted File Upload',
                regex=r'(?i)(?:upload|save|write).*?filename.*?(?:request|params)',
                severity=Severity.HIGH, category='File Handling',
                description='Potential unrestricted file upload',
                recommendation='Validate file types, size, and use secure storage',
                cwe_id='CWE-434'
            ),
            SecurityPattern(
                id='UNS006', name='Temporary File Insecure',
                regex=r'(?i)tempfile\.mktemp\s*\(',
                severity=Severity.MEDIUM, category='File Handling',
                description='mktemp is insecure, race condition vulnerability',
                recommendation='Use tempfile.mkstemp() or tempfile.NamedTemporaryFile()',
                cwe_id='CWE-377'
            ),
            SecurityPattern(
                id='UNS007', name='Hardcoded IP Address',
                regex=r'\b(?:192\.168|10\.\d+|172\.(?:1[6-9]|2[0-9]|3[01]))\.\d+\.\d+\b',
                severity=Severity.LOW, category='Configuration',
                description='Hardcoded internal IP address',
                recommendation='Use configuration files or environment variables',
                cwe_id='CWE-547'
            ),
            SecurityPattern(
                id='UNS008', name='TODO/FIXME Security',
                regex=r'(?i)(?:TODO|FIXME|XXX).*?(?:security|auth|password|secret|token|credential)',
                severity=Severity.INFO, category='Code Quality',
                description='Security-related TODO/FIXME comment',
                recommendation='Address security-related TODOs before deployment'
            ),
        ]

    def run(self) -> Dict:
        """Execute the security scan"""
        if self.verbose:
            print(f"Starting security scan: {self.target_path}")

        if self.target_path.is_file():
            self._scan_file(self.target_path)
        elif self.target_path.is_dir():
            self._scan_directory(self.target_path)
        else:
            raise ValueError(f"Target path does not exist: {self.target_path}")

        return self._generate_results()

    def _scan_directory(self, directory: Path):
        """Recursively scan directory"""
        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]

            for file_name in files:
                file_path = Path(root) / file_name

                # Skip binary/media files
                if file_path.suffix.lower() in self.SKIP_EXTENSIONS:
                    continue

                # Only scan code and config files
                if file_path.suffix.lower() not in (self.CODE_EXTENSIONS | self.CONFIG_EXTENSIONS):
                    continue

                self._scan_file(file_path)

    def _scan_file(self, file_path: Path):
        """Scan single file for security issues"""
        try:
            # Check if text file
            if not self._is_text_file(file_path):
                return

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            self.files_scanned += 1
            self.lines_scanned += len(lines)

            for line_num, line in enumerate(lines, start=1):
                self._scan_line(file_path, line_num, line)

            if self.verbose and self.files_scanned % 50 == 0:
                print(f"  Scanned {self.files_scanned} files...")

        except Exception as e:
            if self.verbose:
                print(f"  Error scanning {file_path}: {e}")

    def _is_text_file(self, file_path: Path) -> bool:
        """Check if file is text file"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(512)
                if b'\x00' in chunk:
                    return False
            return True
        except:
            return False

    def _scan_line(self, file_path: Path, line_num: int, line: str):
        """Scan single line for security patterns"""
        for pattern in self.patterns:
            if re.search(pattern.regex, line):
                # Redact sensitive content
                redacted_line = self._redact_sensitive(line, pattern)

                finding = Finding(
                    finding_id=f"{pattern.id}-{self.files_scanned}-{line_num}",
                    pattern_id=pattern.id,
                    severity=pattern.severity.name,
                    category=pattern.category,
                    type=pattern.name,
                    file_path=str(file_path),
                    line_number=line_num,
                    line_content=redacted_line[:200],
                    description=pattern.description,
                    recommendation=pattern.recommendation,
                    owasp=pattern.owasp,
                    cwe_id=pattern.cwe_id
                )
                self.findings.append(finding)

    def _redact_sensitive(self, line: str, pattern: SecurityPattern) -> str:
        """Redact sensitive data from line content"""
        if pattern.category == 'Secrets':
            # Redact the matched secret value
            match = re.search(pattern.regex, line)
            if match and match.groups():
                for group in match.groups():
                    if group and len(group) > 4:
                        redacted = group[:4] + '*' * (len(group) - 4)
                        line = line.replace(group, redacted)
        return line.strip()

    def _generate_results(self) -> Dict:
        """Generate comprehensive scan results"""
        # Count by severity
        severity_counts = {s.name: 0 for s in Severity}
        for finding in self.findings:
            severity_counts[finding.severity] += 1

        # Count by category
        category_counts: Dict[str, int] = {}
        for finding in self.findings:
            category_counts[finding.category] = category_counts.get(finding.category, 0) + 1

        # Calculate security score
        security_score = self._calculate_score(severity_counts)

        results = {
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'target': str(self.target_path),
            'scan_stats': {
                'files_scanned': self.files_scanned,
                'lines_scanned': self.lines_scanned,
                'patterns_checked': len(self.patterns)
            },
            'summary': {
                'total_findings': len(self.findings),
                'critical': severity_counts['CRITICAL'],
                'high': severity_counts['HIGH'],
                'medium': severity_counts['MEDIUM'],
                'low': severity_counts['LOW'],
                'info': severity_counts['INFO'],
                'security_score': security_score,
                'categories': category_counts
            },
            'findings': [self._finding_to_dict(f) for f in self.findings],
            'recommendations': self._generate_recommendations()
        }

        return results

    def _calculate_score(self, severity_counts: Dict[str, int]) -> int:
        """Calculate security score (0-100)"""
        if self.files_scanned == 0:
            return 0

        # Weighted deductions
        deduction = (
            severity_counts['CRITICAL'] * 25 +
            severity_counts['HIGH'] * 10 +
            severity_counts['MEDIUM'] * 3 +
            severity_counts['LOW'] * 1
        )

        # Normalize by files analyzed
        issues_per_file = deduction / max(self.files_scanned, 1)
        score = max(0, int(100 * (0.9 ** issues_per_file)))
        return score

    def _finding_to_dict(self, finding: Finding) -> Dict:
        """Convert finding to dictionary"""
        result = {
            'finding_id': finding.finding_id,
            'severity': finding.severity,
            'type': finding.type,
            'category': finding.category,
            'file': finding.file_path,
            'line': finding.line_number,
            'content': finding.line_content,
            'description': finding.description,
            'recommendation': finding.recommendation
        }
        if finding.owasp:
            result['owasp'] = finding.owasp
        if finding.cwe_id:
            result['cwe'] = finding.cwe_id
        return result

    def _generate_recommendations(self) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []

        # Count by category
        critical_count = sum(1 for f in self.findings if f.severity == 'CRITICAL')
        secrets_count = sum(1 for f in self.findings if f.category == 'Secrets')
        injection_count = sum(1 for f in self.findings if f.category == 'Injection')

        if critical_count > 0:
            recommendations.append(
                f"CRITICAL: {critical_count} critical security issues found. "
                "Address these immediately before deployment."
            )

        if secrets_count > 0:
            recommendations.append(
                f"Found {secrets_count} hardcoded secrets. "
                "Move all secrets to environment variables or a secrets manager."
            )

        if injection_count > 0:
            recommendations.append(
                f"Found {injection_count} potential injection vulnerabilities. "
                "Use parameterized queries and input validation."
            )

        if not recommendations:
            recommendations.append(
                "No significant security issues detected. "
                "Continue following security best practices."
            )

        return recommendations


class OutputFormatter:
    """Format scan results for output"""

    @staticmethod
    def format_text(results: Dict, verbose: bool = False) -> str:
        """Format results as human-readable text"""
        output = []
        output.append("=" * 80)
        output.append("SECURITY SCAN REPORT")
        output.append("=" * 80)
        output.append(f"Timestamp: {results['timestamp']}")
        output.append(f"Target: {results['target']}")
        output.append(f"Files Scanned: {results['scan_stats']['files_scanned']}")
        output.append(f"Lines Scanned: {results['scan_stats']['lines_scanned']}")
        output.append("")

        summary = results['summary']
        output.append("SUMMARY")
        output.append("-" * 80)
        output.append(f"Security Score: {summary['security_score']}/100")
        output.append(f"Total Findings: {summary['total_findings']}")
        output.append(f"  Critical: {summary['critical']}")
        output.append(f"  High: {summary['high']}")
        output.append(f"  Medium: {summary['medium']}")
        output.append(f"  Low: {summary['low']}")
        output.append(f"  Info: {summary['info']}")
        output.append("")

        if results['findings']:
            output.append("FINDINGS")
            output.append("-" * 80)
            for finding in results['findings'][:50]:  # Limit output
                output.append(f"[{finding['severity']}] {finding['type']}")
                output.append(f"  File: {finding['file']}:{finding['line']}")
                output.append(f"  Description: {finding['description']}")
                output.append(f"  Recommendation: {finding['recommendation']}")
                if finding.get('owasp'):
                    output.append(f"  OWASP: {finding['owasp']}")
                output.append("")

        output.append("RECOMMENDATIONS")
        output.append("-" * 80)
        for i, rec in enumerate(results['recommendations'], 1):
            output.append(f"{i}. {rec}")

        output.append("=" * 80)
        return "\n".join(output)

    @staticmethod
    def format_json(results: Dict) -> str:
        """Format results as JSON"""
        return json.dumps(results, indent=2)

    @staticmethod
    def format_csv(results: Dict) -> str:
        """Format results as CSV"""
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['finding_id', 'severity', 'type', 'category', 'file', 'line',
                        'description', 'recommendation', 'owasp', 'cwe'])
        for finding in results['findings']:
            writer.writerow([
                finding['finding_id'], finding['severity'], finding['type'],
                finding['category'], finding['file'], finding['line'],
                finding['description'], finding['recommendation'],
                finding.get('owasp', ''), finding.get('cwe', '')
            ])
        return output.getvalue()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Security Scanner - SAST-lite Static Application Security Testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a directory for security issues
  %(prog)s --input /path/to/project

  # Generate JSON report
  %(prog)s --input /path/to/project --output json --file report.json

  # Verbose output with progress
  %(prog)s --input /path/to/project --verbose

Detection Categories:
  - Secrets: API keys, passwords, tokens, credentials
  - Injection: SQL, command, XSS, LDAP, XPath
  - OWASP Top 10: A01-A10 vulnerability patterns
  - Cryptography: Weak hashing, SSL issues
  - Unsafe Code: eval, exec, insecure patterns

Severity Levels:
  CRITICAL - Immediate security risk (secrets, RCE)
  HIGH     - Significant risk (injection, auth bypass)
  MEDIUM   - Moderate risk (weak crypto, config issues)
  LOW      - Minor risk (best practice violations)
  INFO     - Informational findings
        """
    )

    parser.add_argument('--input', '-i', required=True, help='File or directory to scan')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--config', '-c', help='Configuration file path (JSON)')
    parser.add_argument('--file', '-f', help='Write output to file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Validate input
    if not os.path.exists(args.input):
        print(f"Error: Input path does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Load config if provided
    config = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)

    try:
        # Run scan
        scanner = SecurityScanner(
            target_path=args.input,
            config=config,
            verbose=args.verbose
        )
        results = scanner.run()

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
                print(f"\nReport saved to: {args.file}")
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
        print("\nScan interrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
