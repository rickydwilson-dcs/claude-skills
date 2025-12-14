#!/usr/bin/env python3
"""
Compliance Checker - Framework Compliance Validation Tool

Automated compliance checking against industry security frameworks:
- SOC 2 Type II controls (CC6, CC7, CC8)
- HIPAA Security Rule requirements
- GDPR data protection requirements
- PCI-DSS payment security controls
- OWASP ASVS application security

Generates compliance checklists, identifies gaps, and provides remediation guidance.

Part of the senior-secops skill package.
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ComplianceStatus(Enum):
    """Compliance check status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"
    NOT_APPLICABLE = "not_applicable"
    NOT_ASSESSED = "not_assessed"


class Severity(Enum):
    """Gap severity levels"""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class ComplianceControl:
    """A compliance control requirement"""
    id: str
    framework: str
    category: str
    name: str
    description: str
    check_patterns: List[str]
    required_evidence: List[str]
    severity: Severity
    remediation: str


@dataclass
class ComplianceResult:
    """Result of a compliance check"""
    control_id: str
    framework: str
    category: str
    name: str
    status: ComplianceStatus
    findings: List[str]
    evidence: List[str]
    gaps: List[str]
    remediation: str
    severity: Severity


class ComplianceChecker:
    """Compliance validation against security frameworks"""

    SUPPORTED_FRAMEWORKS = ['SOC2', 'HIPAA', 'GDPR', 'PCI-DSS', 'OWASP-ASVS']

    SKIP_DIRS = {
        'node_modules', '__pycache__', '.git', '.svn', '.hg',
        'venv', 'env', '.venv', 'dist', 'build', '.tox',
        'vendor', 'third_party', '.idea', '.vscode'
    }

    def __init__(self, target_path: str, frameworks: List[str] = None,
                 config: Optional[Dict] = None, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.target_path = Path(target_path)
        self.frameworks = frameworks or ['SOC2']
        self.config = config or {}
        self.verbose = verbose
        self.results: List[ComplianceResult] = []
        self.files_analyzed = 0
        self.controls = self._load_controls()
        logger.debug("ComplianceChecker initialized")

    def _load_controls(self) -> List[ComplianceControl]:
        """Load compliance controls for selected frameworks"""
        logger.debug(f"Loading controls for frameworks: {self.frameworks}")
        controls = []
        for framework in self.frameworks:
            if framework == 'SOC2':
                controls.extend(self._soc2_controls())
            elif framework == 'HIPAA':
                controls.extend(self._hipaa_controls())
            elif framework == 'GDPR':
                controls.extend(self._gdpr_controls())
            elif framework == 'PCI-DSS':
                controls.extend(self._pci_dss_controls())
            elif framework == 'OWASP-ASVS':
                controls.extend(self._owasp_asvs_controls())
        return controls

    def _soc2_controls(self) -> List[ComplianceControl]:
        """SOC 2 Type II Trust Services Criteria controls"""
        return [
            # CC6 - Logical and Physical Access Controls
            ComplianceControl(
                id='CC6.1', framework='SOC2', category='Access Control',
                name='Logical Access Controls',
                description='The entity implements logical access security software and infrastructure '
                           'to protect against threats to system components.',
                check_patterns=[
                    r'(?i)(?:authentication|auth|login|session)',
                    r'(?i)(?:jwt|oauth|bearer|token)',
                    r'(?i)(?:role|permission|rbac|acl)'
                ],
                required_evidence=['Authentication implementation', 'Authorization checks', 'Session management'],
                severity=Severity.HIGH,
                remediation='Implement proper authentication, authorization, and session management controls'
            ),
            ComplianceControl(
                id='CC6.6', framework='SOC2', category='Access Control',
                name='System Boundary Protection',
                description='The entity implements security measures to protect external access points.',
                check_patterns=[
                    r'(?i)(?:cors|Content-Security-Policy|X-Frame-Options)',
                    r'(?i)(?:rate.?limit|throttle)',
                    r'(?i)(?:firewall|waf|api.?gateway)'
                ],
                required_evidence=['CORS configuration', 'Rate limiting', 'API security headers'],
                severity=Severity.HIGH,
                remediation='Configure security headers, implement rate limiting, and API boundary controls'
            ),
            ComplianceControl(
                id='CC6.7', framework='SOC2', category='Encryption',
                name='Data Encryption',
                description='The entity encrypts data at rest and in transit.',
                check_patterns=[
                    r'(?i)(?:https|tls|ssl)',
                    r'(?i)(?:encrypt|aes|rsa|cipher)',
                    r'(?i)(?:bcrypt|argon|scrypt|pbkdf)'
                ],
                required_evidence=['TLS configuration', 'Encryption at rest', 'Password hashing'],
                severity=Severity.CRITICAL,
                remediation='Implement TLS for all connections, encrypt sensitive data at rest, use secure password hashing'
            ),
            # CC7 - System Operations
            ComplianceControl(
                id='CC7.2', framework='SOC2', category='Monitoring',
                name='Security Monitoring',
                description='The entity monitors system components for anomalies and security events.',
                check_patterns=[
                    r'(?i)(?:log|logging|logger)',
                    r'(?i)(?:audit|monitor|alert)',
                    r'(?i)(?:sentry|datadog|newrelic|cloudwatch)'
                ],
                required_evidence=['Logging implementation', 'Monitoring setup', 'Alert configuration'],
                severity=Severity.HIGH,
                remediation='Implement comprehensive logging, monitoring, and alerting systems'
            ),
            ComplianceControl(
                id='CC7.3', framework='SOC2', category='Vulnerability Management',
                name='Vulnerability Management',
                description='The entity evaluates and remediates vulnerabilities in a timely manner.',
                check_patterns=[
                    r'(?i)(?:npm.audit|yarn.audit|pip-audit|snyk|dependabot)',
                    r'(?i)(?:security.?scan|vulnerability)',
                    r'(?i)(?:cve|nvd|advisory)'
                ],
                required_evidence=['Dependency scanning', 'Vulnerability tracking', 'Patch management'],
                severity=Severity.HIGH,
                remediation='Implement automated vulnerability scanning and establish patch management process'
            ),
            # CC8 - Change Management
            ComplianceControl(
                id='CC8.1', framework='SOC2', category='Change Management',
                name='Change Authorization',
                description='The entity authorizes, designs, develops, and implements changes to infrastructure.',
                check_patterns=[
                    r'(?i)(?:github|gitlab|bitbucket)',
                    r'(?i)(?:pull.?request|merge.?request|code.?review)',
                    r'(?i)(?:ci/cd|pipeline|deployment)'
                ],
                required_evidence=['Version control', 'Code review process', 'CI/CD pipeline'],
                severity=Severity.MEDIUM,
                remediation='Implement version control, code review requirements, and automated deployment pipelines'
            ),
        ]

    def _hipaa_controls(self) -> List[ComplianceControl]:
        """HIPAA Security Rule controls"""
        return [
            ComplianceControl(
                id='HIPAA-164.312(a)(1)', framework='HIPAA', category='Access Control',
                name='Unique User Identification',
                description='Assign a unique name and/or number for identifying and tracking user identity.',
                check_patterns=[
                    r'(?i)(?:user.?id|username|user_identifier)',
                    r'(?i)(?:authentication|identity)',
                ],
                required_evidence=['User identification system', 'Authentication mechanism'],
                severity=Severity.HIGH,
                remediation='Implement unique user identification and authentication for all users'
            ),
            ComplianceControl(
                id='HIPAA-164.312(a)(2)(iv)', framework='HIPAA', category='Encryption',
                name='Encryption and Decryption',
                description='Implement a mechanism to encrypt and decrypt ePHI.',
                check_patterns=[
                    r'(?i)(?:encrypt|decrypt|aes|cipher)',
                    r'(?i)(?:phi|pii|health.?data|patient)',
                ],
                required_evidence=['Encryption implementation', 'Key management'],
                severity=Severity.CRITICAL,
                remediation='Encrypt all ePHI at rest and in transit using approved algorithms'
            ),
            ComplianceControl(
                id='HIPAA-164.312(b)', framework='HIPAA', category='Audit Controls',
                name='Audit Controls',
                description='Implement hardware, software, and/or procedural mechanisms for audit trails.',
                check_patterns=[
                    r'(?i)(?:audit|log|trail)',
                    r'(?i)(?:access.?log|activity.?log)',
                ],
                required_evidence=['Audit logging', 'Log retention policy'],
                severity=Severity.HIGH,
                remediation='Implement comprehensive audit logging for all ePHI access and changes'
            ),
            ComplianceControl(
                id='HIPAA-164.312(c)(1)', framework='HIPAA', category='Integrity',
                name='Data Integrity',
                description='Implement policies and procedures to protect ePHI from improper alteration.',
                check_patterns=[
                    r'(?i)(?:checksum|hash|signature)',
                    r'(?i)(?:integrity|validation)',
                ],
                required_evidence=['Data integrity checks', 'Input validation'],
                severity=Severity.HIGH,
                remediation='Implement data integrity controls including checksums and input validation'
            ),
            ComplianceControl(
                id='HIPAA-164.312(e)(1)', framework='HIPAA', category='Transmission Security',
                name='Transmission Security',
                description='Implement technical security measures to guard against unauthorized access to ePHI.',
                check_patterns=[
                    r'(?i)(?:https|tls|ssl)',
                    r'(?i)(?:secure.?transport|encrypted.?channel)',
                ],
                required_evidence=['TLS configuration', 'Secure transmission'],
                severity=Severity.CRITICAL,
                remediation='Ensure all ePHI transmissions use TLS 1.2 or higher'
            ),
        ]

    def _gdpr_controls(self) -> List[ComplianceControl]:
        """GDPR data protection controls"""
        return [
            ComplianceControl(
                id='GDPR-Art.5', framework='GDPR', category='Data Principles',
                name='Data Processing Principles',
                description='Personal data shall be processed lawfully, fairly and transparently.',
                check_patterns=[
                    r'(?i)(?:consent|opt.?in|gdpr)',
                    r'(?i)(?:privacy.?policy|data.?protection)',
                ],
                required_evidence=['Consent mechanism', 'Privacy policy'],
                severity=Severity.HIGH,
                remediation='Implement consent management and transparent data processing practices'
            ),
            ComplianceControl(
                id='GDPR-Art.17', framework='GDPR', category='Data Subject Rights',
                name='Right to Erasure',
                description='Data subjects have the right to have their personal data erased.',
                check_patterns=[
                    r'(?i)(?:delete|erase|remove).*(user|data|account)',
                    r'(?i)(?:right.?to.?be.?forgotten|data.?deletion)',
                ],
                required_evidence=['Data deletion capability', 'Erasure procedures'],
                severity=Severity.HIGH,
                remediation='Implement data deletion functionality and procedures for handling erasure requests'
            ),
            ComplianceControl(
                id='GDPR-Art.20', framework='GDPR', category='Data Subject Rights',
                name='Data Portability',
                description='Data subjects have the right to receive their personal data in a portable format.',
                check_patterns=[
                    r'(?i)(?:export|download).*(data|profile)',
                    r'(?i)(?:data.?portability|json|csv)',
                ],
                required_evidence=['Data export functionality'],
                severity=Severity.MEDIUM,
                remediation='Implement data export functionality in machine-readable format'
            ),
            ComplianceControl(
                id='GDPR-Art.25', framework='GDPR', category='Privacy by Design',
                name='Data Protection by Design',
                description='Implement appropriate technical measures to protect personal data.',
                check_patterns=[
                    r'(?i)(?:anonymiz|pseudonymiz|mask)',
                    r'(?i)(?:data.?minim|privacy)',
                ],
                required_evidence=['Data minimization', 'Privacy controls'],
                severity=Severity.HIGH,
                remediation='Implement privacy by design principles including data minimization'
            ),
            ComplianceControl(
                id='GDPR-Art.32', framework='GDPR', category='Security',
                name='Security of Processing',
                description='Implement appropriate security measures for personal data protection.',
                check_patterns=[
                    r'(?i)(?:encrypt|secure|protect)',
                    r'(?i)(?:access.?control|authentication)',
                ],
                required_evidence=['Security measures', 'Access controls'],
                severity=Severity.CRITICAL,
                remediation='Implement appropriate technical and organizational security measures'
            ),
        ]

    def _pci_dss_controls(self) -> List[ComplianceControl]:
        """PCI-DSS payment security controls"""
        return [
            ComplianceControl(
                id='PCI-DSS-3.4', framework='PCI-DSS', category='Cardholder Data',
                name='PAN Protection',
                description='Render PAN unreadable anywhere it is stored.',
                check_patterns=[
                    r'(?i)(?:card.?number|pan|credit.?card)',
                    r'(?i)(?:mask|truncat|encrypt).*(?:card|pan)',
                ],
                required_evidence=['PAN encryption/masking', 'Key management'],
                severity=Severity.CRITICAL,
                remediation='Encrypt or mask all stored PAN data'
            ),
            ComplianceControl(
                id='PCI-DSS-4.1', framework='PCI-DSS', category='Transmission',
                name='Transmission Encryption',
                description='Use strong cryptography to safeguard sensitive cardholder data during transmission.',
                check_patterns=[
                    r'(?i)(?:https|tls|ssl)',
                    r'(?i)(?:payment|stripe|braintree|paypal)',
                ],
                required_evidence=['TLS for payment data', 'Secure payment gateway'],
                severity=Severity.CRITICAL,
                remediation='Use TLS 1.2+ for all payment data transmission'
            ),
            ComplianceControl(
                id='PCI-DSS-6.5', framework='PCI-DSS', category='Secure Development',
                name='Secure Coding Practices',
                description='Address common coding vulnerabilities in software-development processes.',
                check_patterns=[
                    r'(?i)(?:injection|xss|csrf)',
                    r'(?i)(?:parameterized|prepared.?statement)',
                ],
                required_evidence=['Secure coding guidelines', 'Vulnerability prevention'],
                severity=Severity.HIGH,
                remediation='Follow secure coding practices to prevent OWASP Top 10 vulnerabilities'
            ),
            ComplianceControl(
                id='PCI-DSS-8.2', framework='PCI-DSS', category='Authentication',
                name='User Authentication',
                description='Implement proper user identification and authentication management.',
                check_patterns=[
                    r'(?i)(?:password.?policy|strong.?password)',
                    r'(?i)(?:mfa|2fa|two.?factor)',
                ],
                required_evidence=['Strong authentication', 'MFA implementation'],
                severity=Severity.HIGH,
                remediation='Implement strong password policies and multi-factor authentication'
            ),
            ComplianceControl(
                id='PCI-DSS-10.2', framework='PCI-DSS', category='Logging',
                name='Audit Trail',
                description='Implement automated audit trails for all system components.',
                check_patterns=[
                    r'(?i)(?:audit|log|trail)',
                    r'(?i)(?:payment.?log|transaction.?log)',
                ],
                required_evidence=['Audit logging', 'Log review process'],
                severity=Severity.HIGH,
                remediation='Implement comprehensive audit logging for all cardholder data access'
            ),
        ]

    def _owasp_asvs_controls(self) -> List[ComplianceControl]:
        """OWASP Application Security Verification Standard controls"""
        return [
            ComplianceControl(
                id='ASVS-2.1', framework='OWASP-ASVS', category='Authentication',
                name='Password Security',
                description='Verify that user set passwords are at least 12 characters in length.',
                check_patterns=[
                    r'(?i)(?:min.?length|password.?length)',
                    r'(?i)(?:bcrypt|argon|scrypt)',
                ],
                required_evidence=['Password policy', 'Secure password storage'],
                severity=Severity.HIGH,
                remediation='Enforce minimum 12 character passwords and use secure hashing'
            ),
            ComplianceControl(
                id='ASVS-3.3', framework='OWASP-ASVS', category='Session Management',
                name='Session Logout',
                description='Verify that logout and expiration invalidate the session token.',
                check_patterns=[
                    r'(?i)(?:logout|signout|session.?destroy)',
                    r'(?i)(?:session.?expir|token.?invalidat)',
                ],
                required_evidence=['Session invalidation', 'Logout functionality'],
                severity=Severity.MEDIUM,
                remediation='Implement proper session logout and token invalidation'
            ),
            ComplianceControl(
                id='ASVS-4.1', framework='OWASP-ASVS', category='Access Control',
                name='Access Control Design',
                description='Verify the application enforces access control rules on a trusted service layer.',
                check_patterns=[
                    r'(?i)(?:authorize|permission|role)',
                    r'(?i)(?:middleware|guard|interceptor)',
                ],
                required_evidence=['Authorization checks', 'Access control layer'],
                severity=Severity.HIGH,
                remediation='Implement server-side access control on a trusted layer'
            ),
            ComplianceControl(
                id='ASVS-5.1', framework='OWASP-ASVS', category='Input Validation',
                name='Input Validation',
                description='Verify that the application validates all input.',
                check_patterns=[
                    r'(?i)(?:validat|sanitiz|escape)',
                    r'(?i)(?:input|param|query)',
                ],
                required_evidence=['Input validation', 'Output encoding'],
                severity=Severity.HIGH,
                remediation='Implement comprehensive input validation and output encoding'
            ),
            ComplianceControl(
                id='ASVS-9.1', framework='OWASP-ASVS', category='Communications',
                name='TLS Requirement',
                description='Verify that TLS is used for all client connectivity.',
                check_patterns=[
                    r'(?i)(?:https|tls|ssl)',
                    r'(?i)(?:hsts|secure.?cookie)',
                ],
                required_evidence=['TLS configuration', 'HSTS header'],
                severity=Severity.HIGH,
                remediation='Enforce TLS for all connections and implement HSTS'
            ),
        ]

    def run(self) -> Dict:
        """Execute compliance check"""
        logger.debug("Starting compliance check execution")
        if self.verbose:
            print(f"Starting compliance check: {self.target_path}")
            print(f"Frameworks: {', '.join(self.frameworks)}")

        if not self.target_path.exists():
            logger.error(f"Target path does not exist: {self.target_path}")
            raise ValueError(f"Target path does not exist: {self.target_path}")

        # Scan codebase for compliance evidence
        self._scan_codebase()

        # Evaluate each control
        for control in self.controls:
            result = self._evaluate_control(control)
            self.results.append(result)

        return self._generate_results()

    def _scan_codebase(self):
        """Scan codebase to collect compliance evidence"""
        logger.debug("Starting codebase scan for compliance evidence")
        self.evidence_cache: Dict[str, List[str]] = {}

        if self.target_path.is_file():
            self._scan_file(self.target_path)
        else:
            for root, dirs, files in os.walk(self.target_path):
                dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]
                for file_name in files:
                    file_path = Path(root) / file_name
                    self._scan_file(file_path)

    def _scan_file(self, file_path: Path):
        """Scan file for compliance evidence"""
        try:
            # Skip binary files
            if self._is_binary(file_path):
                return

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            self.files_analyzed += 1

            # Check each control's patterns
            for control in self.controls:
                for pattern in control.check_patterns:
                    if re.search(pattern, content):
                        if control.id not in self.evidence_cache:
                            self.evidence_cache[control.id] = []
                        self.evidence_cache[control.id].append(str(file_path))

        except Exception as e:
            logger.warning(f"Error scanning {file_path}: {e}")
            if self.verbose:
                print(f"  Error scanning {file_path}: {e}")

    def _is_binary(self, file_path: Path) -> bool:
        """Check if file is binary"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(512)
                return b'\x00' in chunk
        except Exception:
            return True

    def _evaluate_control(self, control: ComplianceControl) -> ComplianceResult:
        """Evaluate a single compliance control"""
        logger.debug(f"Evaluating control: {control.id}")
        evidence = self.evidence_cache.get(control.id, [])
        unique_evidence = list(set(evidence))[:5]  # Limit evidence list

        gaps = []
        findings = []

        if evidence:
            # Found some evidence - determine if partial or compliant
            if len(evidence) >= len(control.required_evidence):
                status = ComplianceStatus.COMPLIANT
                findings.append(f"Found evidence in {len(unique_evidence)} file(s)")
            else:
                status = ComplianceStatus.PARTIAL
                findings.append(f"Partial evidence found in {len(unique_evidence)} file(s)")
                gaps.append("Additional evidence may be needed for full compliance")
        else:
            status = ComplianceStatus.NON_COMPLIANT
            gaps = [f"No evidence found for: {req}" for req in control.required_evidence]

        return ComplianceResult(
            control_id=control.id,
            framework=control.framework,
            category=control.category,
            name=control.name,
            status=status,
            findings=findings,
            evidence=unique_evidence,
            gaps=gaps,
            remediation=control.remediation,
            severity=control.severity
        )

    def _generate_results(self) -> Dict:
        """Generate comprehensive compliance results"""
        logger.debug("Generating compliance results")
        # Calculate compliance score
        total = len(self.results)
        compliant = sum(1 for r in self.results if r.status == ComplianceStatus.COMPLIANT)
        partial = sum(1 for r in self.results if r.status == ComplianceStatus.PARTIAL)
        non_compliant = sum(1 for r in self.results if r.status == ComplianceStatus.NON_COMPLIANT)

        compliance_score = int((compliant + (partial * 0.5)) / max(total, 1) * 100)

        # Framework breakdown
        framework_scores = {}
        for framework in self.frameworks:
            fw_results = [r for r in self.results if r.framework == framework]
            fw_compliant = sum(1 for r in fw_results if r.status == ComplianceStatus.COMPLIANT)
            fw_partial = sum(1 for r in fw_results if r.status == ComplianceStatus.PARTIAL)
            fw_total = len(fw_results)
            framework_scores[framework] = int((fw_compliant + (fw_partial * 0.5)) / max(fw_total, 1) * 100)

        # Categorize gaps by severity
        critical_gaps = [r for r in self.results
                        if r.status == ComplianceStatus.NON_COMPLIANT and r.severity == Severity.CRITICAL]
        high_gaps = [r for r in self.results
                    if r.status == ComplianceStatus.NON_COMPLIANT and r.severity == Severity.HIGH]

        results = {
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'target': str(self.target_path),
            'frameworks_assessed': self.frameworks,
            'files_analyzed': self.files_analyzed,
            'summary': {
                'total_controls': total,
                'compliant': compliant,
                'partial': partial,
                'non_compliant': non_compliant,
                'compliance_score': compliance_score,
                'critical_gaps': len(critical_gaps),
                'high_gaps': len(high_gaps)
            },
            'framework_scores': framework_scores,
            'compliance_results': [self._result_to_dict(r) for r in self.results],
            'gaps': [self._result_to_dict(r) for r in self.results
                    if r.status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.PARTIAL]],
            'recommendations': self._generate_recommendations(critical_gaps, high_gaps)
        }

        return results

    def _result_to_dict(self, result: ComplianceResult) -> Dict:
        """Convert result to dictionary"""
        return {
            'control_id': result.control_id,
            'framework': result.framework,
            'category': result.category,
            'name': result.name,
            'status': result.status.value,
            'severity': result.severity.name,
            'findings': result.findings,
            'evidence': result.evidence,
            'gaps': result.gaps,
            'remediation': result.remediation
        }

    def _generate_recommendations(self, critical_gaps: List, high_gaps: List) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []

        if critical_gaps:
            recommendations.append(
                f"CRITICAL: {len(critical_gaps)} critical compliance gaps found. "
                "Address these immediately to meet regulatory requirements."
            )
            for gap in critical_gaps[:3]:
                recommendations.append(f"  - {gap.control_id}: {gap.remediation}")

        if high_gaps:
            recommendations.append(
                f"HIGH: {len(high_gaps)} high-priority gaps require attention."
            )

        if not recommendations:
            recommendations.append(
                "Good compliance posture. Continue monitoring for regulatory changes."
            )

        return recommendations


class OutputFormatter:
    """Format compliance results for output"""

    @staticmethod
    def format_text(results: Dict, verbose: bool = False) -> str:
        """Format results as human-readable text"""
        output = []
        output.append("=" * 80)
        output.append("COMPLIANCE CHECK REPORT")
        output.append("=" * 80)
        output.append(f"Timestamp: {results['timestamp']}")
        output.append(f"Target: {results['target']}")
        output.append(f"Frameworks: {', '.join(results['frameworks_assessed'])}")
        output.append(f"Files Analyzed: {results['files_analyzed']}")
        output.append("")

        summary = results['summary']
        output.append("SUMMARY")
        output.append("-" * 80)
        output.append(f"Overall Compliance Score: {summary['compliance_score']}%")
        output.append(f"Total Controls: {summary['total_controls']}")
        output.append(f"  Compliant: {summary['compliant']}")
        output.append(f"  Partial: {summary['partial']}")
        output.append(f"  Non-Compliant: {summary['non_compliant']}")
        output.append(f"Critical Gaps: {summary['critical_gaps']}")
        output.append(f"High Gaps: {summary['high_gaps']}")
        output.append("")

        output.append("FRAMEWORK SCORES")
        output.append("-" * 80)
        for fw, score in results['framework_scores'].items():
            status = "PASS" if score >= 80 else "NEEDS WORK" if score >= 50 else "FAIL"
            output.append(f"  {fw}: {score}% [{status}]")
        output.append("")

        if results['gaps']:
            output.append("COMPLIANCE GAPS")
            output.append("-" * 80)
            for gap in results['gaps'][:20]:
                output.append(f"[{gap['severity']}] {gap['control_id']}: {gap['name']}")
                output.append(f"  Status: {gap['status']}")
                output.append(f"  Remediation: {gap['remediation']}")
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
        writer.writerow(['control_id', 'framework', 'category', 'name', 'status',
                        'severity', 'remediation'])
        for result in results['compliance_results']:
            writer.writerow([
                result['control_id'], result['framework'], result['category'],
                result['name'], result['status'], result['severity'],
                result['remediation']
            ])
        return output.getvalue()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Compliance Checker - Framework Compliance Validation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check SOC2 compliance
  %(prog)s --input /path/to/project

  # Check multiple frameworks
  %(prog)s --input /path/to/project --frameworks SOC2 HIPAA GDPR

  # Generate JSON report
  %(prog)s --input /path/to/project --output json --file compliance.json

Supported Frameworks:
  SOC2       - SOC 2 Type II Trust Services Criteria
  HIPAA      - HIPAA Security Rule requirements
  GDPR       - GDPR data protection requirements
  PCI-DSS    - PCI-DSS payment security controls
  OWASP-ASVS - OWASP Application Security Verification Standard
        """
    )

    parser.add_argument('--input', '-i', required=True, help='File or directory to check')
    parser.add_argument('--frameworks', nargs='+', default=['SOC2'],
                       choices=['SOC2', 'HIPAA', 'GDPR', 'PCI-DSS', 'OWASP-ASVS'],
                       help='Compliance frameworks to check (default: SOC2)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--config', '-c', help='Configuration file path (JSON)')
    parser.add_argument('--file', '-f', help='Write output to file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

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
        # Run compliance check
        checker = ComplianceChecker(
            target_path=args.input,
            frameworks=args.frameworks,
            config=config,
            verbose=args.verbose
        )
        results = checker.run()

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

        # Exit code based on compliance score
        if results['summary']['critical_gaps'] > 0:
            sys.exit(2)
        elif results['summary']['compliance_score'] < 80:
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\nCheck interrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
