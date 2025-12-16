#!/usr/bin/env python3
"""
Incident Detector - Alert Triage and Severity Classification Tool

Automated alert triage, severity classification, and indicator of compromise (IOC)
correlation for security incident detection.

Features:
- Severity classification (P0-P3) based on incident type and scope
- Pattern detection (brute force, data exfiltration, lateral movement)
- IOC correlation with known threat indicators
- Alert aggregation and deduplication
- Multiple log format support (JSON, syslog, auth.log)

Usage:
    python incident_detector.py --input /var/log/auth.log
    python incident_detector.py --input logs/ --ioc-file iocs.txt --output json
    python incident_detector.py --input alerts.json --severity P1 --file report.json

Author: Claude Skills Team
Version: 1.0.0
License: MIT
"""

import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

__version__ = "1.0.0"


# =============================================================================
# ENUMS AND DATA CLASSES
# =============================================================================

class Severity(Enum):
    """Incident severity levels following industry standards."""
    P0 = 4  # Critical - active breach, data exfiltration confirmed
    P1 = 3  # High - potential breach, suspicious privileged activity
    P2 = 2  # Medium - anomalies, policy violations, failed attacks
    P3 = 1  # Low - informational alerts, blocked attempts

    @classmethod
    def from_string(cls, value: str) -> 'Severity':
        """Convert string to Severity enum."""
        mapping = {'P0': cls.P0, 'P1': cls.P1, 'P2': cls.P2, 'P3': cls.P3}
        return mapping.get(value.upper(), cls.P3)


class IncidentType(Enum):
    """Classification of incident types."""
    BRUTE_FORCE = "brute_force"
    CREDENTIAL_STUFFING = "credential_stuffing"
    DATA_EXFILTRATION = "data_exfiltration"
    LATERAL_MOVEMENT = "lateral_movement"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    MALWARE = "malware"
    PHISHING = "phishing"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    POLICY_VIOLATION = "policy_violation"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    RANSOMWARE = "ransomware"
    DATA_BREACH = "data_breach"
    CLOUD_COMPROMISE = "cloud_compromise"
    INSIDER_THREAT = "insider_threat"
    UNKNOWN = "unknown"


@dataclass
class Alert:
    """Represents a single security alert."""
    alert_id: str
    timestamp: str
    source: str
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    user: Optional[str] = None
    event_type: str = ""
    description: str = ""
    raw_data: str = ""
    severity: Severity = Severity.P3
    confidence: float = 0.0
    iocs_matched: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "alert_id": self.alert_id,
            "timestamp": self.timestamp,
            "source": self.source,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "user": self.user,
            "event_type": self.event_type,
            "description": self.description,
            "severity": self.severity.name,
            "confidence": self.confidence,
            "iocs_matched": self.iocs_matched
        }


@dataclass
class TriageResult:
    """Result of incident triage analysis."""
    incident_id: str
    severity: Severity
    incident_type: IncidentType
    classification: str
    affected_systems: List[str] = field(default_factory=list)
    affected_users: List[str] = field(default_factory=list)
    iocs_matched: List[str] = field(default_factory=list)
    alerts: List[Alert] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    first_seen: str = ""
    last_seen: str = ""
    event_count: int = 0

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "incident_id": self.incident_id,
            "severity": self.severity.name,
            "incident_type": self.incident_type.value,
            "classification": self.classification,
            "affected_systems": self.affected_systems,
            "affected_users": self.affected_users,
            "iocs_matched": self.iocs_matched,
            "alert_count": len(self.alerts),
            "recommended_actions": self.recommended_actions,
            "confidence_score": self.confidence_score,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "event_count": self.event_count
        }


@dataclass
class DetectionPattern:
    """Definition of a detection pattern."""
    name: str
    pattern: str
    incident_type: IncidentType
    base_severity: Severity
    description: str
    threshold: int = 1  # Events needed to trigger
    timeframe_minutes: int = 60  # Timeframe for threshold


# =============================================================================
# DETECTION PATTERNS
# =============================================================================

DETECTION_PATTERNS = [
    # Brute Force Detection
    DetectionPattern(
        name="ssh_brute_force",
        pattern=r"(Failed password|authentication failure|failed login).*(ssh|sshd)",
        incident_type=IncidentType.BRUTE_FORCE,
        base_severity=Severity.P2,
        description="SSH brute force attack detected",
        threshold=10,
        timeframe_minutes=5
    ),
    DetectionPattern(
        name="auth_brute_force",
        pattern=r"(authentication fail|invalid (user|password)|login fail)",
        incident_type=IncidentType.BRUTE_FORCE,
        base_severity=Severity.P2,
        description="Authentication brute force attempt",
        threshold=10,
        timeframe_minutes=5
    ),

    # Credential Stuffing
    DetectionPattern(
        name="credential_stuffing",
        pattern=r"(multiple account|different user).*(same (ip|source)|single source)",
        incident_type=IncidentType.CREDENTIAL_STUFFING,
        base_severity=Severity.P1,
        description="Credential stuffing attack detected",
        threshold=5,
        timeframe_minutes=10
    ),

    # Data Exfiltration
    DetectionPattern(
        name="large_data_transfer",
        pattern=r"(large (file|data) transfer|unusual (upload|download)|exfil)",
        incident_type=IncidentType.DATA_EXFILTRATION,
        base_severity=Severity.P0,
        description="Potential data exfiltration detected",
        threshold=1,
        timeframe_minutes=60
    ),
    DetectionPattern(
        name="sensitive_file_access",
        pattern=r"(access|read|copy).*(passwd|shadow|credentials|secret|key|token)",
        incident_type=IncidentType.DATA_EXFILTRATION,
        base_severity=Severity.P1,
        description="Sensitive file access detected",
        threshold=1,
        timeframe_minutes=60
    ),

    # Lateral Movement
    DetectionPattern(
        name="internal_scan",
        pattern=r"(port scan|network scan).*(internal|10\.|192\.168|172\.(1[6-9]|2[0-9]|3[01]))",
        incident_type=IncidentType.LATERAL_MOVEMENT,
        base_severity=Severity.P1,
        description="Internal network scanning detected",
        threshold=1,
        timeframe_minutes=30
    ),
    DetectionPattern(
        name="smb_lateral",
        pattern=r"(smb|cifs|windows share).*(remote|lateral|spread)",
        incident_type=IncidentType.LATERAL_MOVEMENT,
        base_severity=Severity.P1,
        description="SMB lateral movement detected",
        threshold=3,
        timeframe_minutes=30
    ),

    # Privilege Escalation
    DetectionPattern(
        name="sudo_abuse",
        pattern=r"(sudo|su ).*(fail|incorrect|NOT in sudoers)",
        incident_type=IncidentType.PRIVILEGE_ESCALATION,
        base_severity=Severity.P2,
        description="Sudo privilege escalation attempt",
        threshold=5,
        timeframe_minutes=10
    ),
    DetectionPattern(
        name="admin_escalation",
        pattern=r"(admin|administrator|root).*(grant|elevat|promot|add.*group)",
        incident_type=IncidentType.PRIVILEGE_ESCALATION,
        base_severity=Severity.P1,
        description="Administrative privilege escalation",
        threshold=1,
        timeframe_minutes=60
    ),

    # Malware Indicators
    DetectionPattern(
        name="malware_execution",
        pattern=r"(malware|trojan|virus|worm|ransomware).*(detect|found|execute)",
        incident_type=IncidentType.MALWARE,
        base_severity=Severity.P0,
        description="Malware execution detected",
        threshold=1,
        timeframe_minutes=60
    ),
    DetectionPattern(
        name="suspicious_process",
        pattern=r"(powershell.*-enc|cmd.*/c|bash.*-c|curl.*\|.*sh)",
        incident_type=IncidentType.MALWARE,
        base_severity=Severity.P1,
        description="Suspicious process execution",
        threshold=1,
        timeframe_minutes=30
    ),

    # Ransomware
    DetectionPattern(
        name="ransomware_activity",
        pattern=r"(\.encrypted|\.locked|ransom|decrypt|bitcoin|monero).*file",
        incident_type=IncidentType.RANSOMWARE,
        base_severity=Severity.P0,
        description="Ransomware activity detected",
        threshold=1,
        timeframe_minutes=15
    ),
    DetectionPattern(
        name="mass_file_encryption",
        pattern=r"(mass|bulk|multiple).*(encrypt|modify|rename).*file",
        incident_type=IncidentType.RANSOMWARE,
        base_severity=Severity.P0,
        description="Mass file encryption detected",
        threshold=1,
        timeframe_minutes=15
    ),

    # Unauthorized Access
    DetectionPattern(
        name="after_hours_access",
        pattern=r"(access|login).*(after hours|weekend|holiday|unusual time)",
        incident_type=IncidentType.UNAUTHORIZED_ACCESS,
        base_severity=Severity.P2,
        description="After-hours system access",
        threshold=1,
        timeframe_minutes=60
    ),
    DetectionPattern(
        name="geographic_anomaly",
        pattern=r"(login|access).*(different country|unusual location|impossible travel)",
        incident_type=IncidentType.UNAUTHORIZED_ACCESS,
        base_severity=Severity.P1,
        description="Geographic access anomaly",
        threshold=1,
        timeframe_minutes=60
    ),

    # Cloud Compromise
    DetectionPattern(
        name="cloud_credential_abuse",
        pattern=r"(aws|azure|gcp|cloud).*(credential|key|token).*(abuse|compromise|leak)",
        incident_type=IncidentType.CLOUD_COMPROMISE,
        base_severity=Severity.P0,
        description="Cloud credential abuse detected",
        threshold=1,
        timeframe_minutes=60
    ),
    DetectionPattern(
        name="unusual_cloud_activity",
        pattern=r"(ec2|lambda|s3|azure|gcp).*(unusual|anomal|unauthor)",
        incident_type=IncidentType.CLOUD_COMPROMISE,
        base_severity=Severity.P1,
        description="Unusual cloud activity detected",
        threshold=3,
        timeframe_minutes=30
    ),

    # Insider Threat
    DetectionPattern(
        name="data_hoarding",
        pattern=r"(mass download|bulk export|data hoard)",
        incident_type=IncidentType.INSIDER_THREAT,
        base_severity=Severity.P1,
        description="Potential data hoarding by insider",
        threshold=1,
        timeframe_minutes=60
    ),
    DetectionPattern(
        name="policy_bypass",
        pattern=r"(bypass|circumvent|disable).*(policy|security|control|dlp)",
        incident_type=IncidentType.INSIDER_THREAT,
        base_severity=Severity.P1,
        description="Security policy bypass attempt",
        threshold=1,
        timeframe_minutes=60
    ),
]


# =============================================================================
# IOC PATTERNS
# =============================================================================

class IOCType(Enum):
    """Types of Indicators of Compromise."""
    IP_ADDRESS = "ip_address"
    DOMAIN = "domain"
    URL = "url"
    FILE_HASH_MD5 = "md5"
    FILE_HASH_SHA1 = "sha1"
    FILE_HASH_SHA256 = "sha256"
    EMAIL = "email"
    FILENAME = "filename"
    REGISTRY_KEY = "registry_key"
    USER_AGENT = "user_agent"


IOC_PATTERNS = {
    IOCType.IP_ADDRESS: re.compile(
        r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    ),
    IOCType.DOMAIN: re.compile(
        r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    ),
    IOCType.FILE_HASH_MD5: re.compile(r'\b[a-fA-F0-9]{32}\b'),
    IOCType.FILE_HASH_SHA1: re.compile(r'\b[a-fA-F0-9]{40}\b'),
    IOCType.FILE_HASH_SHA256: re.compile(r'\b[a-fA-F0-9]{64}\b'),
    IOCType.EMAIL: re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'),
}


# =============================================================================
# LOG PARSERS
# =============================================================================

class LogParser:
    """Base class for log parsers."""

    def parse_line(self, line: str, source: str) -> Optional[Alert]:
        """Parse a single log line into an Alert."""
        raise NotImplementedError

    def _generate_alert_id(self, line: str) -> str:
        """Generate unique alert ID from line content."""
        return hashlib.md5(line.encode()).hexdigest()[:12]

    def _extract_timestamp(self, line: str) -> str:
        """Extract timestamp from log line."""
        # Common timestamp patterns
        patterns = [
            # ISO 8601
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)',
            # Syslog format
            r'([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',
            # Common log format
            r'\[(\d{2}/[A-Z][a-z]{2}/\d{4}:\d{2}:\d{2}:\d{2}\s+[+-]\d{4})\]',
            # Simple date
            r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',
        ]

        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                return match.group(1)

        return datetime.now().isoformat()

    def _extract_ip(self, line: str) -> Optional[str]:
        """Extract IP address from log line."""
        match = IOC_PATTERNS[IOCType.IP_ADDRESS].search(line)
        return match.group(0) if match else None

    def _extract_user(self, line: str) -> Optional[str]:
        """Extract username from log line."""
        patterns = [
            r'user[=:\s]+([a-zA-Z0-9_.-]+)',
            r'for\s+([a-zA-Z0-9_.-]+)\s+from',
            r'account[=:\s]+([a-zA-Z0-9_.-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1)
        return None


class SyslogParser(LogParser):
    """Parser for syslog format logs."""

    def parse_line(self, line: str, source: str) -> Optional[Alert]:
        if not line.strip():
            return None

        return Alert(
            alert_id=self._generate_alert_id(line),
            timestamp=self._extract_timestamp(line),
            source=source,
            source_ip=self._extract_ip(line),
            user=self._extract_user(line),
            event_type="syslog",
            description=line[:200],
            raw_data=line
        )


class JSONLogParser(LogParser):
    """Parser for JSON format logs."""

    def parse_line(self, line: str, source: str) -> Optional[Alert]:
        if not line.strip():
            return None

        try:
            data = json.loads(line)
            return Alert(
                alert_id=data.get('id', self._generate_alert_id(line)),
                timestamp=data.get('timestamp', data.get('@timestamp', datetime.now().isoformat())),
                source=source,
                source_ip=data.get('source_ip', data.get('src_ip', data.get('client_ip'))),
                destination_ip=data.get('destination_ip', data.get('dst_ip', data.get('server_ip'))),
                user=data.get('user', data.get('username', data.get('user_name'))),
                event_type=data.get('event_type', data.get('type', 'json')),
                description=data.get('message', data.get('description', str(data)[:200])),
                raw_data=line
            )
        except json.JSONDecodeError:
            return None


class AuthLogParser(LogParser):
    """Parser for auth.log format logs (Linux authentication logs)."""

    def parse_line(self, line: str, source: str) -> Optional[Alert]:
        if not line.strip():
            return None

        # Determine event type
        event_type = "auth"
        if "Failed password" in line or "authentication failure" in line:
            event_type = "auth_failure"
        elif "Accepted" in line:
            event_type = "auth_success"
        elif "sudo" in line:
            event_type = "sudo"
        elif "session opened" in line:
            event_type = "session_open"
        elif "session closed" in line:
            event_type = "session_close"

        return Alert(
            alert_id=self._generate_alert_id(line),
            timestamp=self._extract_timestamp(line),
            source=source,
            source_ip=self._extract_ip(line),
            user=self._extract_user(line),
            event_type=event_type,
            description=line[:200],
            raw_data=line
        )


# =============================================================================
# INCIDENT DETECTOR
# =============================================================================

class IncidentDetector:
    """Main incident detection engine."""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.alerts: List[Alert] = []
        self.iocs: Set[str] = set()
        self.results: List[TriageResult] = []
        self.stats = {
            'logs_processed': 0,
            'alerts_generated': 0,
            'iocs_matched': 0,
            'patterns_matched': 0
        }

    def load_iocs(self, ioc_file: str) -> None:
        """Load IOCs from file (one per line)."""
        try:
            path = Path(ioc_file)
            if path.exists():
                with open(path, 'r') as f:
                    for line in f:
                        ioc = line.strip()
                        if ioc and not ioc.startswith('#'):
                            self.iocs.add(ioc.lower())
        except Exception as e:
            print(f"Warning: Failed to load IOC file: {e}", file=sys.stderr)

    def _get_parser(self, filepath: str) -> LogParser:
        """Select appropriate parser based on file type."""
        filepath_lower = filepath.lower()

        if filepath_lower.endswith('.json') or filepath_lower.endswith('.jsonl'):
            return JSONLogParser()
        elif 'auth' in filepath_lower or 'secure' in filepath_lower:
            return AuthLogParser()
        else:
            return SyslogParser()

    def parse_logs(self, input_path: str) -> List[Alert]:
        """Parse log files from input path."""
        path = Path(input_path)
        files_to_process = []

        if path.is_file():
            files_to_process.append(path)
        elif path.is_dir():
            for ext in ['*.log', '*.json', '*.jsonl', '*.txt']:
                files_to_process.extend(path.glob(ext))
                files_to_process.extend(path.glob(f'**/{ext}'))

        for filepath in files_to_process:
            parser = self._get_parser(str(filepath))
            try:
                with open(filepath, 'r', errors='ignore') as f:
                    for line in f:
                        self.stats['logs_processed'] += 1
                        alert = parser.parse_line(line, str(filepath))
                        if alert:
                            self.alerts.append(alert)
            except Exception as e:
                print(f"Warning: Failed to parse {filepath}: {e}", file=sys.stderr)

        return self.alerts

    def _check_iocs(self, alert: Alert) -> List[str]:
        """Check alert against loaded IOCs."""
        matched = []
        text = f"{alert.raw_data} {alert.source_ip or ''} {alert.user or ''}".lower()

        for ioc in self.iocs:
            if ioc in text:
                matched.append(ioc)
                self.stats['iocs_matched'] += 1

        # Also extract and check embedded IOCs
        for ioc_type, pattern in IOC_PATTERNS.items():
            for match in pattern.findall(text):
                if match.lower() in self.iocs:
                    if match not in matched:
                        matched.append(match)

        return matched

    def _classify_severity(self, alert: Alert, pattern: Optional[DetectionPattern],
                          ioc_matches: List[str]) -> Severity:
        """Classify alert severity based on pattern and IOC matches."""
        severity = Severity.P3

        if pattern:
            severity = pattern.base_severity

        # Escalate if IOCs matched
        if ioc_matches:
            if severity == Severity.P3:
                severity = Severity.P2
            elif severity == Severity.P2:
                severity = Severity.P1

        # Escalate for certain keywords
        critical_keywords = ['breach', 'exfiltration', 'ransomware', 'confirmed', 'active attack']
        if any(kw in alert.raw_data.lower() for kw in critical_keywords):
            if severity.value < Severity.P0.value:
                severity = Severity(min(severity.value + 1, 4))

        return severity

    def detect_patterns(self, alerts: List[Alert]) -> Dict[str, List[Alert]]:
        """Detect security patterns in alerts."""
        pattern_matches: Dict[str, List[Alert]] = defaultdict(list)

        for alert in alerts:
            ioc_matches = self._check_iocs(alert)
            alert.iocs_matched = ioc_matches

            for pattern in DETECTION_PATTERNS:
                if re.search(pattern.pattern, alert.raw_data, re.IGNORECASE):
                    alert.severity = self._classify_severity(alert, pattern, ioc_matches)
                    alert.confidence = 0.7 + (0.1 * len(ioc_matches))
                    pattern_matches[pattern.name].append(alert)
                    self.stats['patterns_matched'] += 1
                    break
            else:
                # No pattern matched, check for IOCs only
                if ioc_matches:
                    alert.severity = Severity.P2
                    alert.confidence = 0.5
                    pattern_matches['ioc_match'].append(alert)

        return pattern_matches

    def _get_recommended_actions(self, incident_type: IncidentType, severity: Severity) -> List[str]:
        """Get recommended actions based on incident type and severity."""
        actions = []

        # Severity-based actions
        if severity in [Severity.P0, Severity.P1]:
            actions.append("Notify security team immediately")
            actions.append("Initiate incident response process")

        # Type-specific actions
        action_map = {
            IncidentType.BRUTE_FORCE: [
                "Block source IP address",
                "Implement account lockout policy",
                "Review failed authentication logs",
                "Consider implementing MFA"
            ],
            IncidentType.DATA_EXFILTRATION: [
                "Isolate affected systems immediately",
                "Preserve evidence and logs",
                "Identify scope of data exposure",
                "Notify legal and compliance teams"
            ],
            IncidentType.RANSOMWARE: [
                "Isolate infected systems from network",
                "Do NOT pay ransom",
                "Verify backup integrity",
                "Contact law enforcement (FBI IC3)"
            ],
            IncidentType.LATERAL_MOVEMENT: [
                "Segment network to contain spread",
                "Identify all affected systems",
                "Reset credentials for compromised accounts",
                "Review network logs for full scope"
            ],
            IncidentType.PRIVILEGE_ESCALATION: [
                "Disable compromised accounts",
                "Review sudo/admin access logs",
                "Audit group memberships",
                "Rotate credentials"
            ],
            IncidentType.MALWARE: [
                "Quarantine affected systems",
                "Collect memory and disk forensics",
                "Identify malware family and IOCs",
                "Scan all systems for indicators"
            ],
            IncidentType.CLOUD_COMPROMISE: [
                "Rotate compromised credentials immediately",
                "Review CloudTrail/Activity logs",
                "Terminate unauthorized resources",
                "Enable enhanced logging"
            ],
            IncidentType.INSIDER_THREAT: [
                "Preserve evidence without alerting subject",
                "Involve HR and legal teams",
                "Review access logs and data movement",
                "Document all findings"
            ]
        }

        actions.extend(action_map.get(incident_type, [
            "Investigate alert details",
            "Review related logs",
            "Determine scope of activity"
        ]))

        return actions

    def correlate_alerts(self, pattern_matches: Dict[str, List[Alert]]) -> List[TriageResult]:
        """Correlate alerts into incidents."""
        incidents = []

        for pattern_name, alerts in pattern_matches.items():
            if not alerts:
                continue

            # Group by source IP or user
            groups: Dict[str, List[Alert]] = defaultdict(list)
            for alert in alerts:
                key = alert.source_ip or alert.user or 'unknown'
                groups[key].append(alert)

            # Find the pattern definition
            pattern_def = next(
                (p for p in DETECTION_PATTERNS if p.name == pattern_name),
                None
            )

            for key, group_alerts in groups.items():
                # Check if threshold is met
                threshold = pattern_def.threshold if pattern_def else 1
                if len(group_alerts) < threshold:
                    continue

                # Determine highest severity in group
                max_severity = max(a.severity for a in group_alerts)

                # Collect unique IOCs
                all_iocs = set()
                for a in group_alerts:
                    all_iocs.update(a.iocs_matched)

                # Collect affected systems and users
                systems = list(set(a.source for a in group_alerts))
                users = list(set(a.user for a in group_alerts if a.user))

                # Determine incident type
                incident_type = pattern_def.incident_type if pattern_def else IncidentType.SUSPICIOUS_ACTIVITY

                # Calculate confidence
                confidence = sum(a.confidence for a in group_alerts) / len(group_alerts)
                if all_iocs:
                    confidence = min(confidence + 0.15, 1.0)

                # Generate incident ID
                incident_id = f"INC-{datetime.now().strftime('%Y-%m-%d')}-{len(incidents)+1:03d}"

                # Get timestamps
                timestamps = [a.timestamp for a in group_alerts]

                result = TriageResult(
                    incident_id=incident_id,
                    severity=max_severity,
                    incident_type=incident_type,
                    classification=pattern_def.description if pattern_def else "Suspicious Activity",
                    affected_systems=systems[:10],  # Limit for readability
                    affected_users=users[:10],
                    iocs_matched=list(all_iocs),
                    alerts=group_alerts,
                    recommended_actions=self._get_recommended_actions(incident_type, max_severity),
                    confidence_score=round(confidence, 2),
                    first_seen=min(timestamps) if timestamps else "",
                    last_seen=max(timestamps) if timestamps else "",
                    event_count=len(group_alerts)
                )
                incidents.append(result)

        # Sort by severity (highest first)
        incidents.sort(key=lambda x: x.severity.value, reverse=True)
        self.results = incidents

        return incidents

    def run(self, input_path: str, min_severity: Optional[Severity] = None) -> Dict:
        """Run full detection pipeline."""
        # Parse logs
        self.parse_logs(input_path)
        self.stats['alerts_generated'] = len(self.alerts)

        # Detect patterns
        pattern_matches = self.detect_patterns(self.alerts)

        # Correlate into incidents
        incidents = self.correlate_alerts(pattern_matches)

        # Filter by severity if requested
        if min_severity:
            incidents = [i for i in incidents if i.severity.value >= min_severity.value]

        # Generate summary
        severity_counts = defaultdict(int)
        for incident in incidents:
            severity_counts[incident.severity.name] += 1

        return {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "scan_stats": self.stats,
            "summary": {
                "P0_critical": severity_counts.get('P0', 0),
                "P1_high": severity_counts.get('P1', 0),
                "P2_medium": severity_counts.get('P2', 0),
                "P3_low": severity_counts.get('P3', 0),
                "total_incidents": len(incidents)
            },
            "incidents": [i.to_dict() for i in incidents],
            "recommendations": self._generate_recommendations(incidents)
        }

    def _generate_recommendations(self, incidents: List[TriageResult]) -> List[str]:
        """Generate overall recommendations based on incidents."""
        recommendations = []

        p0_count = sum(1 for i in incidents if i.severity == Severity.P0)
        p1_count = sum(1 for i in incidents if i.severity == Severity.P1)

        if p0_count > 0:
            recommendations.append(f"CRITICAL: {p0_count} P0 incident(s) require immediate attention")
        if p1_count > 0:
            recommendations.append(f"HIGH: {p1_count} P1 incident(s) should be investigated within 30 minutes")

        # Check for patterns suggesting broader compromise
        incident_types = [i.incident_type for i in incidents]
        if IncidentType.LATERAL_MOVEMENT in incident_types and IncidentType.DATA_EXFILTRATION in incident_types:
            recommendations.append("ALERT: Lateral movement combined with data exfiltration suggests active breach")

        if not recommendations:
            recommendations.append("No critical incidents detected. Continue monitoring.")

        return recommendations


# =============================================================================
# OUTPUT FORMATTERS
# =============================================================================

def format_text(results: Dict) -> str:
    """Format results as human-readable text."""
    lines = []
    lines.append("=" * 70)
    lines.append("INCIDENT DETECTION REPORT")
    lines.append("=" * 70)
    lines.append(f"Timestamp: {results['timestamp']}")
    lines.append(f"Status: {results['status']}")
    lines.append("")

    # Stats
    stats = results['scan_stats']
    lines.append("SCAN STATISTICS")
    lines.append("-" * 40)
    lines.append(f"  Logs Processed:    {stats['logs_processed']:,}")
    lines.append(f"  Alerts Generated:  {stats['alerts_generated']:,}")
    lines.append(f"  IOCs Matched:      {stats['iocs_matched']:,}")
    lines.append(f"  Patterns Matched:  {stats['patterns_matched']:,}")
    lines.append("")

    # Summary
    summary = results['summary']
    lines.append("SEVERITY SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  P0 (Critical):  {summary['P0_critical']}")
    lines.append(f"  P1 (High):      {summary['P1_high']}")
    lines.append(f"  P2 (Medium):    {summary['P2_medium']}")
    lines.append(f"  P3 (Low):       {summary['P3_low']}")
    lines.append(f"  Total:          {summary['total_incidents']}")
    lines.append("")

    # Incidents
    if results['incidents']:
        lines.append("INCIDENTS DETECTED")
        lines.append("-" * 40)
        for incident in results['incidents']:
            lines.append("")
            lines.append(f"  [{incident['severity']}] {incident['incident_id']}")
            lines.append(f"  Type: {incident['incident_type']}")
            lines.append(f"  Classification: {incident['classification']}")
            lines.append(f"  Confidence: {incident['confidence_score']*100:.0f}%")
            lines.append(f"  Events: {incident['event_count']}")
            if incident['affected_systems']:
                lines.append(f"  Affected Systems: {', '.join(incident['affected_systems'][:3])}")
            if incident['affected_users']:
                lines.append(f"  Affected Users: {', '.join(incident['affected_users'][:3])}")
            if incident['iocs_matched']:
                lines.append(f"  IOCs Matched: {', '.join(incident['iocs_matched'][:3])}")
            lines.append("  Recommended Actions:")
            for action in incident['recommended_actions'][:3]:
                lines.append(f"    - {action}")

    # Recommendations
    lines.append("")
    lines.append("RECOMMENDATIONS")
    lines.append("-" * 40)
    for rec in results['recommendations']:
        lines.append(f"  * {rec}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def format_csv(results: Dict) -> str:
    """Format results as CSV."""
    lines = []
    headers = [
        "incident_id", "severity", "incident_type", "classification",
        "confidence", "event_count", "affected_systems", "affected_users",
        "iocs_matched", "first_seen", "last_seen"
    ]
    lines.append(",".join(headers))

    for incident in results['incidents']:
        row = [
            incident['incident_id'],
            incident['severity'],
            incident['incident_type'],
            f'"{incident["classification"]}"',
            str(incident['confidence_score']),
            str(incident['event_count']),
            f'"{";".join(incident["affected_systems"])}"',
            f'"{";".join(incident["affected_users"])}"',
            f'"{";".join(incident["iocs_matched"])}"',
            incident['first_seen'],
            incident['last_seen']
        ]
        lines.append(",".join(row))

    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='incident_detector',
        description="""
Incident Detector - Alert Triage and Severity Classification

Automated tool for security alert triage, severity classification, and
indicator of compromise (IOC) correlation.

Features:
  - Severity classification (P0-P3) based on incident type
  - Pattern detection (brute force, exfiltration, lateral movement)
  - IOC correlation with known threat indicators
  - Multiple log format support (JSON, syslog, auth.log)

Examples:
  %(prog)s --input /var/log/auth.log
  %(prog)s --input logs/ --ioc-file iocs.txt --output json
  %(prog)s --input alerts.json --severity P1 --file report.json
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to log file or directory to analyze'
    )

    parser.add_argument(
        '--ioc-file',
        help='Path to IOC file (one indicator per line)'
    )

    parser.add_argument(
        '--severity', '-s',
        choices=['P0', 'P1', 'P2', 'P3'],
        help='Minimum severity level to report (default: all)'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Validate input path
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path does not exist: {args.input}", file=sys.stderr)
        sys.exit(2)

    # Initialize detector
    detector = IncidentDetector()

    # Load IOCs if provided
    if args.ioc_file:
        detector.load_iocs(args.ioc_file)
        if args.verbose:
            print(f"Loaded {len(detector.iocs)} IOCs from {args.ioc_file}", file=sys.stderr)

    # Run detection
    min_severity = Severity.from_string(args.severity) if args.severity else None

    if args.verbose:
        print(f"Analyzing logs from: {args.input}", file=sys.stderr)

    results = detector.run(args.input, min_severity)

    # Format output
    if args.output == 'json':
        output = json.dumps(results, indent=2)
    elif args.output == 'csv':
        output = format_csv(results)
    else:
        output = format_text(results)

    # Write output
    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        if args.verbose:
            print(f"Results written to: {args.file}", file=sys.stderr)
    else:
        print(output)

    # Exit with appropriate code
    summary = results['summary']
    if summary['P0_critical'] > 0:
        sys.exit(2)  # Critical incidents found
    elif summary['P1_high'] > 0:
        sys.exit(1)  # High severity incidents found
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
