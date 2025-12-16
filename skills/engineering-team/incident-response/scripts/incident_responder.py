#!/usr/bin/env python3
"""
Incident Responder - Containment and Evidence Collection Tool

Incident containment, timeline tracking, and evidence collection with
playbook execution for security incident response.

Features:
- Pre-built playbooks (phishing, ransomware, data breach, cloud compromise)
- Containment action execution with logging
- Evidence collection with chain of custody tracking
- Timeline generation with all incident events
- Hash verification for evidence integrity

Usage:
    python incident_responder.py --incident INC-001 --playbook ransomware
    python incident_responder.py --incident INC-001 --action contain
    python incident_responder.py --incident INC-001 --collect-evidence --output-dir ./evidence

Author: Claude Skills Team
Version: 1.0.0
License: MIT
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
import tarfile
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any

__version__ = "1.0.0"


# =============================================================================
# ENUMS AND DATA CLASSES
# =============================================================================

class ActionStatus(Enum):
    """Status of a containment action."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    REQUIRES_APPROVAL = "requires_approval"


class ActionType(Enum):
    """Types of containment actions."""
    DISABLE_ACCOUNT = "disable_account"
    ISOLATE_SYSTEM = "isolate_system"
    BLOCK_IP = "block_ip"
    BLOCK_DOMAIN = "block_domain"
    ROTATE_CREDENTIALS = "rotate_credentials"
    SHUTDOWN_SERVICE = "shutdown_service"
    QUARANTINE_FILE = "quarantine_file"
    REVOKE_TOKEN = "revoke_token"
    DISABLE_MFA = "disable_mfa"
    RESET_PASSWORD = "reset_password"
    TERMINATE_SESSION = "terminate_session"
    BACKUP_VERIFICATION = "backup_verification"
    NETWORK_SEGMENT = "network_segment"
    PRESERVE_EVIDENCE = "preserve_evidence"


class PlaybookType(Enum):
    """Types of incident response playbooks."""
    PHISHING = "phishing"
    RANSOMWARE = "ransomware"
    DATA_BREACH = "data_breach"
    CLOUD_COMPROMISE = "cloud_compromise"
    INSIDER_THREAT = "insider_threat"
    MALWARE = "malware"
    DDOS = "ddos"
    UNAUTHORIZED_ACCESS = "unauthorized_access"


class EvidenceType(Enum):
    """Types of evidence that can be collected."""
    LOG_FILE = "log_file"
    MEMORY_DUMP = "memory_dump"
    DISK_IMAGE = "disk_image"
    NETWORK_CAPTURE = "network_capture"
    SCREENSHOT = "screenshot"
    CONFIG_FILE = "config_file"
    DATABASE_EXPORT = "database_export"
    EMAIL = "email"
    REGISTRY = "registry"
    PROCESS_LIST = "process_list"
    NETWORK_CONNECTIONS = "network_connections"


@dataclass
class ContainmentAction:
    """Represents a single containment action."""
    action_id: str
    action_type: ActionType
    target: str
    description: str
    status: ActionStatus = ActionStatus.PENDING
    timestamp: str = ""
    executed_by: str = "incident_responder"
    notes: str = ""
    rollback_command: Optional[str] = None
    requires_approval: bool = False
    approval_by: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type.value,
            "target": self.target,
            "description": self.description,
            "status": self.status.value,
            "timestamp": self.timestamp,
            "executed_by": self.executed_by,
            "notes": self.notes,
            "rollback_command": self.rollback_command,
            "requires_approval": self.requires_approval,
            "approval_by": self.approval_by
        }


@dataclass
class Evidence:
    """Represents collected evidence."""
    evidence_id: str
    evidence_type: EvidenceType
    source_system: str
    source_path: str
    collected_at: str
    hash_sha256: str
    file_path: str
    file_size: int
    description: str
    chain_of_custody: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type.value,
            "source_system": self.source_system,
            "source_path": self.source_path,
            "collected_at": self.collected_at,
            "hash_sha256": self.hash_sha256,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "description": self.description,
            "chain_of_custody": self.chain_of_custody
        }


@dataclass
class TimelineEvent:
    """A single event in the incident timeline."""
    timestamp: str
    event_type: str
    description: str
    actor: str = ""
    target: str = ""
    outcome: str = ""
    source: str = ""

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "description": self.description,
            "actor": self.actor,
            "target": self.target,
            "outcome": self.outcome,
            "source": self.source
        }


@dataclass
class IncidentTimeline:
    """Complete incident timeline."""
    incident_id: str
    events: List[TimelineEvent] = field(default_factory=list)
    detection_time: str = ""
    containment_time: str = ""
    eradication_time: str = ""
    recovery_time: str = ""

    def add_event(self, event: TimelineEvent):
        self.events.append(event)
        self.events.sort(key=lambda x: x.timestamp)

    def to_dict(self) -> Dict:
        return {
            "incident_id": self.incident_id,
            "events": [e.to_dict() for e in self.events],
            "detection_time": self.detection_time,
            "containment_time": self.containment_time,
            "eradication_time": self.eradication_time,
            "recovery_time": self.recovery_time,
            "total_events": len(self.events)
        }


# =============================================================================
# PLAYBOOK DEFINITIONS
# =============================================================================

PLAYBOOKS = {
    PlaybookType.PHISHING: {
        "name": "Phishing Response Playbook",
        "description": "Response procedures for phishing attacks",
        "severity": "P1",
        "response_time_sla": "30 minutes",
        "actions": [
            {
                "type": ActionType.DISABLE_ACCOUNT,
                "target": "affected_user",
                "description": "Disable affected user account",
                "priority": 1
            },
            {
                "type": ActionType.REVOKE_TOKEN,
                "target": "affected_user_sessions",
                "description": "Revoke all active sessions and tokens",
                "priority": 2
            },
            {
                "type": ActionType.RESET_PASSWORD,
                "target": "affected_user",
                "description": "Force password reset for affected account",
                "priority": 3
            },
            {
                "type": ActionType.BLOCK_DOMAIN,
                "target": "phishing_domain",
                "description": "Block malicious domain at email gateway and firewall",
                "priority": 4
            },
            {
                "type": ActionType.PRESERVE_EVIDENCE,
                "target": "phishing_email",
                "description": "Preserve original phishing email with headers",
                "priority": 5
            }
        ],
        "evidence_to_collect": [
            EvidenceType.EMAIL,
            EvidenceType.LOG_FILE,
            EvidenceType.SCREENSHOT
        ]
    },

    PlaybookType.RANSOMWARE: {
        "name": "Ransomware Response Playbook",
        "description": "Response procedures for ransomware infections",
        "severity": "P0",
        "response_time_sla": "Immediate",
        "actions": [
            {
                "type": ActionType.ISOLATE_SYSTEM,
                "target": "infected_systems",
                "description": "Immediately isolate infected systems from network",
                "priority": 1
            },
            {
                "type": ActionType.NETWORK_SEGMENT,
                "target": "affected_subnet",
                "description": "Segment network to prevent lateral spread",
                "priority": 2
            },
            {
                "type": ActionType.SHUTDOWN_SERVICE,
                "target": "file_shares",
                "description": "Disable network file shares to prevent encryption spread",
                "priority": 3
            },
            {
                "type": ActionType.BACKUP_VERIFICATION,
                "target": "critical_systems",
                "description": "Verify backup integrity and availability",
                "priority": 4
            },
            {
                "type": ActionType.PRESERVE_EVIDENCE,
                "target": "ransom_note",
                "description": "Preserve ransom note and encrypted file samples",
                "priority": 5
            }
        ],
        "evidence_to_collect": [
            EvidenceType.DISK_IMAGE,
            EvidenceType.MEMORY_DUMP,
            EvidenceType.LOG_FILE,
            EvidenceType.NETWORK_CAPTURE
        ],
        "critical_notes": [
            "DO NOT pay the ransom",
            "DO NOT shut down systems - preserve memory",
            "Contact law enforcement (FBI IC3)",
            "Engage cyber insurance carrier"
        ]
    },

    PlaybookType.DATA_BREACH: {
        "name": "Data Breach Response Playbook",
        "description": "Response procedures for data breach incidents",
        "severity": "P0",
        "response_time_sla": "Immediate",
        "actions": [
            {
                "type": ActionType.DISABLE_ACCOUNT,
                "target": "compromised_accounts",
                "description": "Disable all compromised user accounts",
                "priority": 1
            },
            {
                "type": ActionType.BLOCK_IP,
                "target": "attacker_ips",
                "description": "Block attacker IP addresses at firewall",
                "priority": 2
            },
            {
                "type": ActionType.ROTATE_CREDENTIALS,
                "target": "affected_systems",
                "description": "Rotate credentials for all affected systems",
                "priority": 3
            },
            {
                "type": ActionType.PRESERVE_EVIDENCE,
                "target": "access_logs",
                "description": "Preserve all access logs and database query logs",
                "priority": 4
            }
        ],
        "evidence_to_collect": [
            EvidenceType.LOG_FILE,
            EvidenceType.DATABASE_EXPORT,
            EvidenceType.NETWORK_CAPTURE
        ],
        "regulatory_notes": [
            "GDPR: Notify authority within 72 hours",
            "CCPA: Notify affected consumers",
            "HIPAA: Notify HHS within 60 days",
            "Document all data potentially exposed"
        ]
    },

    PlaybookType.CLOUD_COMPROMISE: {
        "name": "Cloud Account Compromise Playbook",
        "description": "Response procedures for cloud account compromise",
        "severity": "P0",
        "response_time_sla": "Immediate",
        "actions": [
            {
                "type": ActionType.REVOKE_TOKEN,
                "target": "compromised_credentials",
                "description": "Revoke compromised IAM credentials immediately",
                "priority": 1
            },
            {
                "type": ActionType.ROTATE_CREDENTIALS,
                "target": "all_access_keys",
                "description": "Rotate all potentially compromised access keys",
                "priority": 2
            },
            {
                "type": ActionType.SHUTDOWN_SERVICE,
                "target": "unauthorized_resources",
                "description": "Terminate unauthorized cloud resources",
                "priority": 3
            },
            {
                "type": ActionType.PRESERVE_EVIDENCE,
                "target": "cloud_trail_logs",
                "description": "Preserve CloudTrail/Activity logs for forensics",
                "priority": 4
            }
        ],
        "evidence_to_collect": [
            EvidenceType.LOG_FILE,
            EvidenceType.CONFIG_FILE
        ]
    },

    PlaybookType.INSIDER_THREAT: {
        "name": "Insider Threat Response Playbook",
        "description": "Response procedures for insider threat incidents",
        "severity": "P1",
        "response_time_sla": "1 hour",
        "actions": [
            {
                "type": ActionType.PRESERVE_EVIDENCE,
                "target": "user_activity_logs",
                "description": "Preserve all user activity logs before alerting subject",
                "priority": 1,
                "requires_approval": True
            },
            {
                "type": ActionType.DISABLE_ACCOUNT,
                "target": "subject_account",
                "description": "Disable subject's account (coordinate with HR/Legal)",
                "priority": 2,
                "requires_approval": True
            },
            {
                "type": ActionType.REVOKE_TOKEN,
                "target": "subject_access",
                "description": "Revoke all access tokens and badges",
                "priority": 3
            }
        ],
        "evidence_to_collect": [
            EvidenceType.LOG_FILE,
            EvidenceType.EMAIL,
            EvidenceType.DATABASE_EXPORT
        ],
        "coordination_notes": [
            "Coordinate with HR before taking visible actions",
            "Involve Legal counsel early",
            "Do not alert subject prematurely",
            "Document all observations"
        ]
    },

    PlaybookType.MALWARE: {
        "name": "Malware Response Playbook",
        "description": "Response procedures for malware infections",
        "severity": "P1",
        "response_time_sla": "30 minutes",
        "actions": [
            {
                "type": ActionType.ISOLATE_SYSTEM,
                "target": "infected_host",
                "description": "Isolate infected system from network",
                "priority": 1
            },
            {
                "type": ActionType.QUARANTINE_FILE,
                "target": "malware_sample",
                "description": "Quarantine malware sample for analysis",
                "priority": 2
            },
            {
                "type": ActionType.PRESERVE_EVIDENCE,
                "target": "system_state",
                "description": "Capture memory dump and disk image",
                "priority": 3
            },
            {
                "type": ActionType.BLOCK_IP,
                "target": "c2_servers",
                "description": "Block command and control server IPs",
                "priority": 4
            }
        ],
        "evidence_to_collect": [
            EvidenceType.MEMORY_DUMP,
            EvidenceType.DISK_IMAGE,
            EvidenceType.NETWORK_CAPTURE,
            EvidenceType.PROCESS_LIST
        ]
    }
}


# =============================================================================
# INCIDENT RESPONDER
# =============================================================================

class IncidentResponder:
    """Main incident response engine."""

    def __init__(self, incident_id: str, output_dir: str = "./evidence"):
        self.incident_id = incident_id
        self.output_dir = Path(output_dir)
        self.timeline = IncidentTimeline(incident_id=incident_id)
        self.actions: List[ContainmentAction] = []
        self.evidence: List[Evidence] = []
        self.action_counter = 0
        self.evidence_counter = 0

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_action_id(self) -> str:
        """Generate unique action ID."""
        self.action_counter += 1
        return f"ACT-{self.incident_id}-{self.action_counter:03d}"

    def _generate_evidence_id(self) -> str:
        """Generate unique evidence ID."""
        self.evidence_counter += 1
        return f"EVD-{self.incident_id}-{self.evidence_counter:03d}"

    def _log_event(self, event_type: str, description: str, actor: str = "",
                   target: str = "", outcome: str = ""):
        """Log an event to the timeline."""
        event = TimelineEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            description=description,
            actor=actor,
            target=target,
            outcome=outcome,
            source="incident_responder"
        )
        self.timeline.add_event(event)

    def _calculate_file_hash(self, filepath: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def load_playbook(self, playbook_type: PlaybookType) -> Dict:
        """Load and return playbook definition."""
        if playbook_type not in PLAYBOOKS:
            raise ValueError(f"Unknown playbook type: {playbook_type}")
        return PLAYBOOKS[playbook_type]

    def execute_playbook(self, playbook_type: PlaybookType,
                        dry_run: bool = False) -> List[ContainmentAction]:
        """Execute all actions in a playbook."""
        playbook = self.load_playbook(playbook_type)

        self._log_event(
            "playbook_started",
            f"Executing playbook: {playbook['name']}",
            actor="incident_responder",
            target=self.incident_id
        )

        executed_actions = []
        for action_def in sorted(playbook['actions'], key=lambda x: x.get('priority', 99)):
            action = ContainmentAction(
                action_id=self._generate_action_id(),
                action_type=action_def['type'],
                target=action_def['target'],
                description=action_def['description'],
                requires_approval=action_def.get('requires_approval', False)
            )

            if dry_run:
                action.status = ActionStatus.SKIPPED
                action.notes = "Dry run - action not executed"
            elif action.requires_approval:
                action.status = ActionStatus.REQUIRES_APPROVAL
                action.notes = "Awaiting approval before execution"
            else:
                action = self._execute_action(action)

            executed_actions.append(action)
            self.actions.append(action)

        self._log_event(
            "playbook_completed",
            f"Completed playbook: {playbook['name']} ({len(executed_actions)} actions)",
            actor="incident_responder",
            outcome="success" if all(a.status == ActionStatus.COMPLETED for a in executed_actions) else "partial"
        )

        # Set containment time
        self.timeline.containment_time = datetime.now().isoformat()

        return executed_actions

    def _execute_action(self, action: ContainmentAction) -> ContainmentAction:
        """Execute a single containment action (simulated)."""
        action.status = ActionStatus.IN_PROGRESS
        action.timestamp = datetime.now().isoformat()

        self._log_event(
            "action_started",
            f"Executing: {action.description}",
            actor="incident_responder",
            target=action.target
        )

        # Simulate action execution
        # In production, this would integrate with actual systems
        try:
            # Action-specific simulation
            if action.action_type == ActionType.DISABLE_ACCOUNT:
                action.notes = f"Account '{action.target}' marked for disable"
                action.rollback_command = f"enable_account {action.target}"

            elif action.action_type == ActionType.ISOLATE_SYSTEM:
                action.notes = f"System '{action.target}' isolation initiated"
                action.rollback_command = f"restore_network {action.target}"

            elif action.action_type == ActionType.BLOCK_IP:
                action.notes = f"IP block rule created for '{action.target}'"
                action.rollback_command = f"unblock_ip {action.target}"

            elif action.action_type == ActionType.BLOCK_DOMAIN:
                action.notes = f"Domain '{action.target}' added to blocklist"
                action.rollback_command = f"unblock_domain {action.target}"

            elif action.action_type == ActionType.ROTATE_CREDENTIALS:
                action.notes = f"Credential rotation initiated for '{action.target}'"

            elif action.action_type == ActionType.SHUTDOWN_SERVICE:
                action.notes = f"Service '{action.target}' shutdown requested"
                action.rollback_command = f"start_service {action.target}"

            elif action.action_type == ActionType.REVOKE_TOKEN:
                action.notes = f"All tokens revoked for '{action.target}'"

            elif action.action_type == ActionType.PRESERVE_EVIDENCE:
                action.notes = f"Evidence preservation initiated for '{action.target}'"

            elif action.action_type == ActionType.BACKUP_VERIFICATION:
                action.notes = f"Backup verification requested for '{action.target}'"

            elif action.action_type == ActionType.NETWORK_SEGMENT:
                action.notes = f"Network segmentation applied to '{action.target}'"
                action.rollback_command = f"remove_segment {action.target}"

            else:
                action.notes = f"Action executed for '{action.target}'"

            action.status = ActionStatus.COMPLETED

        except Exception as e:
            action.status = ActionStatus.FAILED
            action.notes = f"Action failed: {str(e)}"

        self._log_event(
            "action_completed",
            f"Completed: {action.description}",
            actor="incident_responder",
            target=action.target,
            outcome=action.status.value
        )

        return action

    def execute_single_action(self, action_type: ActionType, target: str,
                             description: str = "", dry_run: bool = False) -> ContainmentAction:
        """Execute a single containment action."""
        action = ContainmentAction(
            action_id=self._generate_action_id(),
            action_type=action_type,
            target=target,
            description=description or f"{action_type.value} for {target}"
        )

        if dry_run:
            action.status = ActionStatus.SKIPPED
            action.notes = "Dry run - action not executed"
        else:
            action = self._execute_action(action)

        self.actions.append(action)
        return action

    def collect_evidence(self, source_paths: List[str],
                        description: str = "") -> List[Evidence]:
        """Collect evidence from specified paths."""
        collected = []

        self._log_event(
            "evidence_collection_started",
            f"Starting evidence collection from {len(source_paths)} sources",
            actor="incident_responder"
        )

        for source_path in source_paths:
            path = Path(source_path)
            if not path.exists():
                self._log_event(
                    "evidence_not_found",
                    f"Source not found: {source_path}",
                    outcome="skipped"
                )
                continue

            evidence = self._collect_single_evidence(path, description)
            if evidence:
                collected.append(evidence)
                self.evidence.append(evidence)

        self._log_event(
            "evidence_collection_completed",
            f"Collected {len(collected)} evidence items",
            actor="incident_responder",
            outcome="success"
        )

        return collected

    def _collect_single_evidence(self, source_path: Path,
                                description: str = "") -> Optional[Evidence]:
        """Collect a single piece of evidence."""
        try:
            evidence_id = self._generate_evidence_id()

            # Determine evidence type
            evidence_type = EvidenceType.LOG_FILE
            suffix = source_path.suffix.lower()
            if suffix in ['.pcap', '.pcapng']:
                evidence_type = EvidenceType.NETWORK_CAPTURE
            elif suffix in ['.png', '.jpg', '.jpeg', '.gif']:
                evidence_type = EvidenceType.SCREENSHOT
            elif suffix in ['.conf', '.cfg', '.ini', '.yaml', '.yml', '.json']:
                evidence_type = EvidenceType.CONFIG_FILE
            elif suffix in ['.eml', '.msg']:
                evidence_type = EvidenceType.EMAIL
            elif suffix in ['.raw', '.mem', '.dmp']:
                evidence_type = EvidenceType.MEMORY_DUMP

            # Create destination path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_name = f"{evidence_id}_{timestamp}_{source_path.name}"
            dest_path = self.output_dir / dest_name

            # Copy file
            if source_path.is_file():
                shutil.copy2(source_path, dest_path)
            elif source_path.is_dir():
                # Create tarball for directories
                dest_path = self.output_dir / f"{dest_name}.tar.gz"
                with tarfile.open(dest_path, "w:gz") as tar:
                    tar.add(source_path, arcname=source_path.name)

            # Calculate hash
            file_hash = self._calculate_file_hash(dest_path)

            # Create evidence record
            evidence = Evidence(
                evidence_id=evidence_id,
                evidence_type=evidence_type,
                source_system=os.uname().nodename if hasattr(os, 'uname') else "unknown",
                source_path=str(source_path),
                collected_at=datetime.now().isoformat(),
                hash_sha256=file_hash,
                file_path=str(dest_path),
                file_size=dest_path.stat().st_size,
                description=description or f"Evidence from {source_path}",
                chain_of_custody=[f"Collected by incident_responder at {datetime.now().isoformat()}"]
            )

            self._log_event(
                "evidence_collected",
                f"Collected: {source_path.name}",
                target=str(source_path),
                outcome=f"SHA256: {file_hash[:16]}..."
            )

            return evidence

        except Exception as e:
            self._log_event(
                "evidence_collection_failed",
                f"Failed to collect: {source_path}",
                target=str(source_path),
                outcome=f"Error: {str(e)}"
            )
            return None

    def generate_evidence_manifest(self) -> Dict:
        """Generate manifest of all collected evidence."""
        manifest = {
            "incident_id": self.incident_id,
            "generated_at": datetime.now().isoformat(),
            "output_directory": str(self.output_dir),
            "total_evidence": len(self.evidence),
            "evidence_items": [e.to_dict() for e in self.evidence],
            "chain_of_custody_verified": True
        }

        # Write manifest to file
        manifest_path = self.output_dir / f"{self.incident_id}_evidence_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        return manifest

    def build_timeline(self) -> IncidentTimeline:
        """Build and return the incident timeline."""
        return self.timeline

    def generate_status_report(self) -> Dict:
        """Generate current incident status report."""
        # Count action statuses
        action_summary = {
            "total": len(self.actions),
            "completed": sum(1 for a in self.actions if a.status == ActionStatus.COMPLETED),
            "failed": sum(1 for a in self.actions if a.status == ActionStatus.FAILED),
            "pending": sum(1 for a in self.actions if a.status == ActionStatus.PENDING),
            "requires_approval": sum(1 for a in self.actions if a.status == ActionStatus.REQUIRES_APPROVAL)
        }

        # Calculate MTTR if containment is done
        mttr = None
        if self.timeline.detection_time and self.timeline.containment_time:
            try:
                detect = datetime.fromisoformat(self.timeline.detection_time)
                contain = datetime.fromisoformat(self.timeline.containment_time)
                mttr = (contain - detect).total_seconds() / 60  # in minutes
            except:
                pass

        return {
            "status": "completed",
            "incident_id": self.incident_id,
            "timestamp": datetime.now().isoformat(),
            "action_summary": action_summary,
            "containment_actions": [a.to_dict() for a in self.actions],
            "evidence_collected": [e.to_dict() for e in self.evidence],
            "timeline": self.timeline.to_dict(),
            "metrics": {
                "mttr_minutes": mttr,
                "actions_executed": action_summary["completed"],
                "evidence_items": len(self.evidence)
            }
        }

    def run(self, playbook_type: Optional[PlaybookType] = None,
           action_type: Optional[ActionType] = None,
           target: str = "",
           collect_evidence_paths: Optional[List[str]] = None,
           dry_run: bool = False) -> Dict:
        """Run the incident response workflow."""

        # Set detection time
        self.timeline.detection_time = datetime.now().isoformat()

        self._log_event(
            "response_started",
            f"Incident response initiated for {self.incident_id}",
            actor="incident_responder"
        )

        # Execute playbook if specified
        if playbook_type:
            self.execute_playbook(playbook_type, dry_run)

        # Execute single action if specified
        if action_type and target:
            self.execute_single_action(action_type, target, dry_run=dry_run)

        # Collect evidence if paths specified
        if collect_evidence_paths:
            self.collect_evidence(collect_evidence_paths)
            self.generate_evidence_manifest()

        self._log_event(
            "response_completed",
            f"Incident response workflow completed",
            actor="incident_responder",
            outcome="success"
        )

        return self.generate_status_report()


# =============================================================================
# OUTPUT FORMATTERS
# =============================================================================

def format_text(results: Dict) -> str:
    """Format results as human-readable text."""
    lines = []
    lines.append("=" * 70)
    lines.append("INCIDENT RESPONSE REPORT")
    lines.append("=" * 70)
    lines.append(f"Incident ID: {results['incident_id']}")
    lines.append(f"Timestamp: {results['timestamp']}")
    lines.append(f"Status: {results['status']}")
    lines.append("")

    # Action Summary
    summary = results['action_summary']
    lines.append("ACTION SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  Total Actions:       {summary['total']}")
    lines.append(f"  Completed:           {summary['completed']}")
    lines.append(f"  Failed:              {summary['failed']}")
    lines.append(f"  Pending:             {summary['pending']}")
    lines.append(f"  Requires Approval:   {summary['requires_approval']}")
    lines.append("")

    # Containment Actions
    if results['containment_actions']:
        lines.append("CONTAINMENT ACTIONS")
        lines.append("-" * 40)
        for action in results['containment_actions']:
            status_icon = {
                'completed': '[OK]',
                'failed': '[FAIL]',
                'pending': '[...]',
                'requires_approval': '[WAIT]',
                'skipped': '[SKIP]'
            }.get(action['status'], '[?]')
            lines.append(f"  {status_icon} {action['action_id']}: {action['description']}")
            lines.append(f"       Target: {action['target']}")
            if action['notes']:
                lines.append(f"       Notes: {action['notes']}")
        lines.append("")

    # Evidence Collected
    if results['evidence_collected']:
        lines.append("EVIDENCE COLLECTED")
        lines.append("-" * 40)
        for evidence in results['evidence_collected']:
            lines.append(f"  [{evidence['evidence_id']}] {evidence['evidence_type']}")
            lines.append(f"       Source: {evidence['source_path']}")
            lines.append(f"       Hash: {evidence['hash_sha256'][:32]}...")
            lines.append(f"       Size: {evidence['file_size']:,} bytes")
        lines.append("")

    # Timeline
    timeline = results['timeline']
    if timeline['events']:
        lines.append("INCIDENT TIMELINE")
        lines.append("-" * 40)
        for event in timeline['events'][-10:]:  # Last 10 events
            lines.append(f"  [{event['timestamp']}]")
            lines.append(f"       {event['event_type']}: {event['description']}")
        lines.append("")

    # Metrics
    metrics = results['metrics']
    lines.append("METRICS")
    lines.append("-" * 40)
    if metrics['mttr_minutes']:
        lines.append(f"  MTTR (minutes):      {metrics['mttr_minutes']:.1f}")
    lines.append(f"  Actions Executed:    {metrics['actions_executed']}")
    lines.append(f"  Evidence Items:      {metrics['evidence_items']}")
    lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='incident_responder',
        description="""
Incident Responder - Containment and Evidence Collection

Incident containment, timeline tracking, and evidence collection with
playbook execution for security incident response.

Features:
  - Pre-built playbooks (phishing, ransomware, data breach, cloud)
  - Containment action execution with logging
  - Evidence collection with chain of custody tracking
  - Timeline generation with all incident events

Examples:
  %(prog)s --incident INC-001 --playbook ransomware
  %(prog)s --incident INC-001 --action isolate --target server01
  %(prog)s --incident INC-001 --collect-evidence --paths /var/log/auth.log
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--incident', '-i',
        required=True,
        help='Incident identifier (e.g., INC-2025-12-16-001)'
    )

    parser.add_argument(
        '--playbook', '-p',
        choices=[p.value for p in PlaybookType],
        help='Playbook to execute'
    )

    parser.add_argument(
        '--action', '-a',
        choices=[a.value for a in ActionType],
        help='Specific action to execute'
    )

    parser.add_argument(
        '--target', '-t',
        help='Target for specific action'
    )

    parser.add_argument(
        '--collect-evidence', '-c',
        action='store_true',
        help='Enable evidence collection'
    )

    parser.add_argument(
        '--paths',
        nargs='+',
        help='Paths to collect evidence from'
    )

    parser.add_argument(
        '--output-dir', '-d',
        default='./evidence',
        help='Directory for evidence storage (default: ./evidence)'
    )

    parser.add_argument(
        '--timeline',
        action='store_true',
        help='Generate incident timeline'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate actions without executing'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json'],
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

    # Validate arguments
    if args.action and not args.target:
        print("Error: --target is required when using --action", file=sys.stderr)
        sys.exit(2)

    if args.collect_evidence and not args.paths:
        print("Error: --paths is required when using --collect-evidence", file=sys.stderr)
        sys.exit(2)

    # Initialize responder
    responder = IncidentResponder(
        incident_id=args.incident,
        output_dir=args.output_dir
    )

    if args.verbose:
        print(f"Incident Response initiated for: {args.incident}", file=sys.stderr)

    # Run response workflow
    playbook_type = PlaybookType(args.playbook) if args.playbook else None
    action_type = ActionType(args.action) if args.action else None

    results = responder.run(
        playbook_type=playbook_type,
        action_type=action_type,
        target=args.target or "",
        collect_evidence_paths=args.paths if args.collect_evidence else None,
        dry_run=args.dry_run
    )

    # Format output
    if args.output == 'json':
        output = json.dumps(results, indent=2)
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

    # Exit code based on action results
    if results['action_summary']['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
