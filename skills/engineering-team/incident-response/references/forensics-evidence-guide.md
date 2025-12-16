# Forensics and Evidence Collection Guide

## Overview

This guide provides comprehensive procedures for collecting, preserving, and managing digital evidence during security incident response. Proper evidence handling ensures forensic integrity, maintains chain of custody, and supports potential legal proceedings.

## Evidence Collection Principles

### Order of Volatility

Evidence must be collected in order of volatility - most volatile first:

| Priority | Evidence Type | Volatility | Collection Window |
|----------|--------------|------------|-------------------|
| 1 | Memory (RAM) | Very High | Seconds-minutes |
| 2 | Network connections | High | Minutes |
| 3 | Running processes | High | Minutes |
| 4 | Swap/page files | Medium | Hours |
| 5 | Temporary files | Medium | Hours |
| 6 | System logs | Low | Days-weeks |
| 7 | Disk contents | Very Low | Persistent |

### Chain of Custody Requirements

Every piece of evidence must have documented chain of custody:

```
EVIDENCE CHAIN OF CUSTODY LOG

Evidence ID: EVD-INC-001-001
Description: Memory dump from server-prod-01
Collection Date: 2025-12-16 14:30:00 UTC
Collected By: John Smith (Security Analyst)
Hash (SHA-256): abc123...

Transfer Log:
| Date/Time | From | To | Purpose | Signature |
|-----------|------|-----|---------|-----------|
| 2025-12-16 14:35 | Collection | Secure Storage | Initial storage | JS |
| 2025-12-16 16:00 | Secure Storage | Forensics Lab | Analysis | JS→ML |
```

### Hash Verification

All evidence must be hashed immediately upon collection:

```bash
# Calculate SHA-256 hash
sha256sum evidence_file.raw > evidence_file.sha256

# Verify hash integrity
sha256sum -c evidence_file.sha256
```

**Integration with incident_responder.py:**
```bash
# Automatic hash calculation during evidence collection
python incident_responder.py \
  --incident INC-001 \
  --collect-evidence \
  --paths /var/log/auth.log /var/log/syslog \
  --output-dir ./evidence

# Output includes hash verification in manifest
```

## Evidence Types and Collection Methods

### 1. Memory (RAM) Collection

**Why:** Contains decrypted data, running processes, network connections, malware in memory.

**Tools:**
- Linux: LiME (Linux Memory Extractor)
- Windows: WinPMem, Magnet RAM Capture
- macOS: MacQuisition

**Linux Memory Acquisition:**
```bash
# Using LiME
insmod lime.ko "path=/evidence/memory.lime format=lime"

# Verify acquisition
sha256sum /evidence/memory.lime > /evidence/memory.sha256
```

**Windows Memory Acquisition:**
```cmd
# Using WinPMem
winpmem_mini_x64.exe memory.raw

# Using Magnet RAM Capture (GUI)
# Export to .raw format
```

**Analysis Tools:**
- Volatility Framework (volatility3)
- Rekall
- Strings analysis

### 2. Disk Image Collection

**Why:** Contains file system, deleted files, application data, logs.

**Tools:**
- Linux: dd, dc3dd, dcfldd
- Windows: FTK Imager, EnCase
- Cross-platform: Guymager

**Linux Disk Imaging:**
```bash
# Full disk image with dd
dd if=/dev/sda of=/evidence/disk.raw bs=4M status=progress

# With hash verification (dc3dd)
dc3dd if=/dev/sda of=/evidence/disk.raw hash=sha256 log=/evidence/disk.log

# Compressed image
dd if=/dev/sda | gzip > /evidence/disk.raw.gz
```

**Mount for Analysis (Read-Only):**
```bash
# Create loop device (read-only)
losetup -r /dev/loop0 /evidence/disk.raw

# Mount read-only
mount -o ro,noexec /dev/loop0 /mnt/evidence
```

### 3. Log File Collection

**Why:** Contains authentication events, application activity, system events, audit trails.

**Critical Log Locations:**

| System | Log Path | Contents |
|--------|----------|----------|
| Linux Auth | /var/log/auth.log | Authentication events |
| Linux Syslog | /var/log/syslog | System events |
| Linux Audit | /var/log/audit/audit.log | Security audit |
| Windows Security | Security.evtx | Security events |
| Windows System | System.evtx | System events |
| Apache | /var/log/apache2/access.log | Web access |
| Nginx | /var/log/nginx/access.log | Web access |

**Collection Script:**
```bash
#!/bin/bash
# collect_logs.sh - Comprehensive log collection

EVIDENCE_DIR="/evidence/$INCIDENT_ID/logs"
mkdir -p "$EVIDENCE_DIR"

# System logs
cp -p /var/log/auth.log* "$EVIDENCE_DIR/"
cp -p /var/log/syslog* "$EVIDENCE_DIR/"
cp -p /var/log/kern.log* "$EVIDENCE_DIR/"

# Application logs
cp -rp /var/log/apache2/ "$EVIDENCE_DIR/apache2/"
cp -rp /var/log/nginx/ "$EVIDENCE_DIR/nginx/"

# Audit logs
cp -p /var/log/audit/* "$EVIDENCE_DIR/audit/"

# Generate manifest with hashes
find "$EVIDENCE_DIR" -type f -exec sha256sum {} \; > "$EVIDENCE_DIR/manifest.sha256"
```

**Integration with incident_responder.py:**
```bash
python incident_responder.py \
  --incident INC-001 \
  --collect-evidence \
  --paths /var/log/auth.log /var/log/syslog /var/log/audit/ \
  --output-dir ./evidence/INC-001
```

### 4. Network Capture Collection

**Why:** Contains network traffic, connections, potential C2 communication.

**Tools:**
- tcpdump
- Wireshark/tshark
- Zeek (Bro)

**Live Capture:**
```bash
# Capture all traffic on interface
tcpdump -i eth0 -w /evidence/capture.pcap

# Capture specific host
tcpdump -i eth0 host 192.168.1.100 -w /evidence/host_traffic.pcap

# Capture with rotation (1 hour files)
tcpdump -i eth0 -w /evidence/capture_%Y%m%d_%H%M%S.pcap -G 3600
```

**Analysis:**
```bash
# Extract connections
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e tcp.port

# Extract HTTP requests
tshark -r capture.pcap -Y "http.request" -T fields -e http.host -e http.request.uri

# Extract DNS queries
tshark -r capture.pcap -Y "dns.qry.name" -T fields -e dns.qry.name
```

### 5. Cloud Evidence Collection

**AWS:**
```bash
# CloudTrail logs
aws cloudtrail lookup-events \
  --start-time 2025-12-15T00:00:00Z \
  --end-time 2025-12-16T23:59:59Z \
  --output json > /evidence/cloudtrail.json

# S3 access logs
aws s3 cp s3://bucket-logs/ /evidence/s3-logs/ --recursive

# VPC Flow Logs
aws logs filter-log-events \
  --log-group-name vpc-flow-logs \
  --start-time 1702598400000 \
  --output json > /evidence/vpc-flow.json
```

**Azure:**
```bash
# Activity logs
az monitor activity-log list \
  --start-time 2025-12-15T00:00:00Z \
  --end-time 2025-12-16T23:59:59Z \
  --output json > /evidence/activity-log.json

# Sign-in logs
az ad sign-in list \
  --filter "createdDateTime ge 2025-12-15" \
  --output json > /evidence/signin-logs.json
```

**GCP:**
```bash
# Audit logs
gcloud logging read \
  'timestamp>="2025-12-15T00:00:00Z" AND timestamp<="2025-12-16T23:59:59Z"' \
  --format=json > /evidence/gcp-audit.json
```

### 6. Application-Specific Evidence

**Database Logs:**
```sql
-- PostgreSQL query log
SHOW log_directory;
SHOW log_filename;

-- MySQL general query log
SHOW VARIABLES LIKE 'general_log%';
```

**Container Logs:**
```bash
# Docker container logs
docker logs --since 24h container_name > /evidence/container.log

# Kubernetes pod logs
kubectl logs pod_name --since=24h > /evidence/pod.log

# All pods in namespace
kubectl logs -l app=myapp --all-containers --since=24h > /evidence/pods.log
```

## Evidence Storage Requirements

### Secure Storage

Evidence must be stored securely:

```
/evidence/
├── INC-001/
│   ├── .evidence-manifest.json     # Master manifest
│   ├── memory/
│   │   ├── server01.lime           # Memory dump
│   │   └── server01.lime.sha256    # Hash
│   ├── disk/
│   │   ├── server01.raw.gz         # Disk image
│   │   └── server01.raw.sha256     # Hash
│   ├── logs/
│   │   ├── auth.log
│   │   ├── syslog
│   │   └── manifest.sha256
│   └── network/
│       ├── capture.pcap
│       └── capture.pcap.sha256
```

### Encryption Requirements

Sensitive evidence should be encrypted at rest:

```bash
# Encrypt evidence archive
gpg --symmetric --cipher-algo AES256 evidence.tar.gz

# Decrypt for analysis
gpg --decrypt evidence.tar.gz.gpg > evidence.tar.gz
```

### Retention Periods

| Evidence Type | Minimum Retention | Notes |
|---------------|-------------------|-------|
| P0 Incidents | 7 years | Legal/compliance requirements |
| P1 Incidents | 3 years | Potential legal proceedings |
| P2/P3 Incidents | 1 year | Internal review |
| Regulatory (HIPAA) | 6 years | HHS requirement |
| Regulatory (PCI) | 1 year | PCI DSS requirement |

## Legal Considerations

### Admissibility Requirements

For evidence to be admissible in legal proceedings:

1. **Authenticity:** Can prove evidence is what it claims to be
2. **Integrity:** No tampering (verified by hashes)
3. **Chain of Custody:** Complete documentation of handling
4. **Relevance:** Evidence relates to the case
5. **Completeness:** Full context preserved

### Privacy Regulations

| Regulation | Evidence Handling Requirements |
|------------|-------------------------------|
| GDPR | Minimize personal data collection, document legal basis |
| CCPA | Notify affected individuals if PII involved |
| HIPAA | Special handling for PHI, BAA requirements |

### Cross-Border Considerations

When evidence spans jurisdictions:
- Document data location and applicable laws
- Consider MLAT (Mutual Legal Assistance Treaty) requirements
- Engage legal counsel for international incidents

## Evidence Validation

### Integrity Verification

```bash
# Verify all evidence hashes
find /evidence/INC-001 -name "*.sha256" -exec sha256sum -c {} \;

# Using incident_responder.py manifest
python -c "
import json
with open('evidence_manifest.json') as f:
    manifest = json.load(f)
for item in manifest['evidence_items']:
    print(f'{item[\"evidence_id\"]}: {item[\"hash_sha256\"][:16]}...')
"
```

### Documentation Checklist

For each piece of evidence, document:

- [ ] Evidence ID (unique identifier)
- [ ] Description (what is it)
- [ ] Source system (where collected from)
- [ ] Collection timestamp (when collected)
- [ ] Collector name (who collected it)
- [ ] Collection method (how collected)
- [ ] Hash value (SHA-256)
- [ ] Storage location (where stored)
- [ ] Chain of custody entries

## Evidence Analysis Workflow

### Analysis Environment Setup

```bash
# Create isolated analysis environment
# Use dedicated forensics workstation or VM

# Mount evidence read-only
mount -o ro,noexec /evidence/disk.raw /mnt/analysis

# Never modify original evidence
# Work on copies for analysis
```

### Timeline Reconstruction

```bash
# Using incident_analyzer.py
python incident_analyzer.py \
  --incident INC-001 \
  --evidence-dir /evidence/INC-001 \
  --rca \
  --output json

# Manual timeline from logs
grep -h "Dec 16" /evidence/logs/*.log | sort -k3 > timeline.txt
```

### IOC Extraction

```bash
# Extract IP addresses
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' /evidence/logs/* | sort -u

# Extract domains
grep -oE '[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,}' /evidence/logs/* | sort -u

# Extract file hashes from logs
grep -oE '[a-fA-F0-9]{32}|[a-fA-F0-9]{64}' /evidence/logs/* | sort -u
```

## Quick Reference

### Collection Commands Summary

```bash
# Memory
insmod lime.ko "path=/evidence/mem.lime format=lime"

# Disk
dd if=/dev/sda of=/evidence/disk.raw bs=4M

# Logs
tar czvf /evidence/logs.tar.gz /var/log/

# Network
tcpdump -i eth0 -w /evidence/capture.pcap

# Hash everything
find /evidence -type f ! -name "*.sha256" -exec sha256sum {} \; > /evidence/manifest.sha256
```

### incident_responder.py Integration

```bash
# Automated evidence collection
python incident_responder.py \
  --incident INC-001 \
  --collect-evidence \
  --paths /var/log/ /etc/ /home/user/.ssh/ \
  --output-dir /evidence/INC-001

# View manifest
cat /evidence/INC-001/INC-001_evidence_manifest.json
```

---
**Last Updated:** December 16, 2025
**Related:** incident-response-playbooks.md, communication-templates.md
**Tools:** incident_responder.py (--collect-evidence), incident_analyzer.py (--evidence-dir)
