# Network Security Guide

Comprehensive guide to network security implementation across AWS, Azure, and GCP.

## Overview

This reference covers network security controls, from foundational security groups to advanced zero-trust architectures. Includes compliance mappings, implementation patterns, and best practices for enterprise deployments.

## Security Group Best Practices

### Principle of Least Privilege

**Core Rule:** Only allow traffic that is explicitly required.

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Group Design                     │
├─────────────────────────────────────────────────────────────┤
│  ✓ Specific source IPs/CIDRs (not 0.0.0.0/0)               │
│  ✓ Specific ports (not all ports)                           │
│  ✓ Specific protocols (TCP/UDP, not all)                    │
│  ✓ Reference other security groups (not CIDRs when possible)│
│  ✓ Descriptive names and comments                           │
│  ✗ Avoid wildcards in production                            │
│  ✗ Avoid overly permissive rules                            │
└─────────────────────────────────────────────────────────────┘
```

### Security Group Naming Convention

```
{env}-{tier}-{application}-{purpose}-sg
```

**Examples:**
- `prod-web-api-alb-sg` - Production web tier ALB
- `prod-app-api-ecs-sg` - Production application tier ECS
- `prod-db-api-rds-sg` - Production database tier RDS
- `dev-mgmt-bastion-sg` - Development management bastion

### 3-Tier Application Security Groups

**Web Tier (ALB):**
```hcl
# Inbound
- HTTPS (443) from 0.0.0.0/0 (or CloudFront IPs)
- HTTP (80) from 0.0.0.0/0 (redirect to HTTPS)

# Outbound
- App port to Application SG
- HTTPS (443) to 0.0.0.0/0 (health checks, webhooks)
```

**Application Tier (ECS/EC2):**
```hcl
# Inbound
- App port (8080) from Web Tier SG only
- SSH (22) from Bastion SG (if needed)

# Outbound
- Database port (5432/3306) to Database SG
- HTTPS (443) to 0.0.0.0/0 (external APIs)
- Cache port (6379) to Cache SG
```

**Database Tier (RDS):**
```hcl
# Inbound
- Database port from Application SG only
- Database port from Bastion SG (for admin)

# Outbound
- None (stateful - responses allowed automatically)
```

### Security Group vs NACL

| Feature | Security Group | Network ACL |
|---------|----------------|-------------|
| **Level** | Instance/ENI | Subnet |
| **State** | Stateful | Stateless |
| **Rules** | Allow only | Allow and Deny |
| **Evaluation** | All rules | Rules in order |
| **Default** | Deny all inbound | Allow all |
| **Use Case** | Primary control | Defense in depth |

**Best Practice:** Use Security Groups as primary control, NACLs for subnet-level blocking (e.g., known bad IPs, emergency blocks).

## Network ACL Patterns

### Standard NACL Configuration

**Inbound Rules:**
| Rule # | Type | Protocol | Port Range | Source | Allow/Deny |
|--------|------|----------|------------|--------|------------|
| 100 | HTTPS | TCP | 443 | 0.0.0.0/0 | ALLOW |
| 110 | HTTP | TCP | 80 | 0.0.0.0/0 | ALLOW |
| 120 | Ephemeral | TCP | 1024-65535 | 0.0.0.0/0 | ALLOW |
| 130 | SSH | TCP | 22 | 10.0.0.0/8 | ALLOW |
| * | All | All | All | 0.0.0.0/0 | DENY |

**Outbound Rules:**
| Rule # | Type | Protocol | Port Range | Destination | Allow/Deny |
|--------|------|----------|------------|-------------|------------|
| 100 | HTTPS | TCP | 443 | 0.0.0.0/0 | ALLOW |
| 110 | HTTP | TCP | 80 | 0.0.0.0/0 | ALLOW |
| 120 | Ephemeral | TCP | 1024-65535 | 0.0.0.0/0 | ALLOW |
| 130 | PostgreSQL | TCP | 5432 | 10.0.0.0/8 | ALLOW |
| * | All | All | All | 0.0.0.0/0 | DENY |

### Emergency Block Pattern

When you need to immediately block malicious traffic:

```hcl
# Add at lowest rule number to ensure evaluation first
resource "aws_network_acl_rule" "block_bad_actor" {
  network_acl_id = aws_network_acl.main.id
  rule_number    = 10
  egress         = false
  protocol       = "-1"
  rule_action    = "deny"
  cidr_block     = "203.0.113.50/32"  # Bad actor IP
}
```

## Zero-Trust Architecture

### Core Principles

1. **Never Trust, Always Verify** - Authenticate and authorize every request
2. **Assume Breach** - Minimize blast radius through segmentation
3. **Verify Explicitly** - Use all available data points for access decisions
4. **Least Privilege Access** - Just-in-time and just-enough access

### Zero-Trust Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Zero-Trust Network                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User/Device                                                │
│       │                                                      │
│       ▼                                                      │
│   ┌───────────────┐                                         │
│   │   Identity    │  ← MFA, Device Trust, Risk Score        │
│   │   Provider    │                                         │
│   └───────┬───────┘                                         │
│           │                                                  │
│           ▼                                                  │
│   ┌───────────────┐                                         │
│   │   Policy      │  ← Context-aware access policies        │
│   │   Engine      │                                         │
│   └───────┬───────┘                                         │
│           │                                                  │
│           ▼                                                  │
│   ┌───────────────┐                                         │
│   │   Proxy/      │  ← TLS inspection, logging              │
│   │   Gateway     │                                         │
│   └───────┬───────┘                                         │
│           │                                                  │
│           ▼                                                  │
│   ┌───────────────┐                                         │
│   │   Micro-      │  ← Service mesh, mTLS                   │
│   │   Segments    │                                         │
│   └───────────────┘                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Components

**Identity Layer:**
- AWS IAM Identity Center / Azure AD / Google Cloud Identity
- MFA enforcement (hardware keys preferred)
- Device trust verification
- Session management

**Network Layer:**
- Micro-segmentation (security groups per service)
- Service mesh (Istio, AWS App Mesh, Linkerd)
- mTLS for service-to-service communication
- Network policies in Kubernetes

**Application Layer:**
- API authentication (OAuth 2.0, JWT)
- Request signing (AWS SigV4)
- Rate limiting and throttling
- Input validation

**Data Layer:**
- Encryption at rest and in transit
- Key management (KMS, Vault)
- Data classification and DLP
- Audit logging

## DDoS Mitigation

### AWS DDoS Protection Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    DDoS Protection Layers                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Layer 7 (Application)                                      │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  AWS WAF                                             │   │
│   │  - Rate limiting rules                               │   │
│   │  - Bot control                                       │   │
│   │  - SQL injection / XSS protection                    │   │
│   │  - Geo-blocking                                      │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
│   Layer 3/4 (Network)                                        │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  AWS Shield                                          │   │
│   │  - Standard: Automatic (free)                        │   │
│   │  - Advanced: 24/7 DRT, cost protection               │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
│   Edge (Global)                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  CloudFront                                          │   │
│   │  - Global edge network                               │   │
│   │  - TLS termination                                   │   │
│   │  - Origin protection                                 │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### WAF Rule Examples

**Rate Limiting:**
```json
{
  "Name": "RateLimitRule",
  "Priority": 1,
  "Action": { "Block": {} },
  "Statement": {
    "RateBasedStatement": {
      "Limit": 2000,
      "AggregateKeyType": "IP"
    }
  }
}
```

**Geo-Blocking:**
```json
{
  "Name": "GeoBlockRule",
  "Priority": 2,
  "Action": { "Block": {} },
  "Statement": {
    "GeoMatchStatement": {
      "CountryCodes": ["CN", "RU", "KP"]
    }
  }
}
```

**SQL Injection Protection:**
```json
{
  "Name": "SQLiProtection",
  "Priority": 3,
  "Action": { "Block": {} },
  "Statement": {
    "SqliMatchStatement": {
      "FieldToMatch": { "AllQueryArguments": {} },
      "TextTransformations": [
        { "Priority": 0, "Type": "URL_DECODE" },
        { "Priority": 1, "Type": "HTML_ENTITY_DECODE" }
      ]
    }
  }
}
```

## Compliance Frameworks

### PCI-DSS Network Requirements

**Requirement 1: Firewall Configuration**
- [ ] 1.1 - Document firewall standards and procedures
- [ ] 1.2 - Restrict connections between untrusted networks and CDE
- [ ] 1.3 - Prohibit direct public access to CDE
- [ ] 1.4 - Install personal firewall on mobile devices

**Requirement 2: Security Configurations**
- [ ] 2.1 - Change vendor defaults
- [ ] 2.2 - Configuration standards for all components
- [ ] 2.3 - Encrypt non-console admin access

**Network Segmentation:**
```
┌─────────────────────────────────────────────────────────────┐
│                    PCI-DSS Network Zones                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────────┐     ┌─────────────────┐              │
│   │  Corporate      │     │  DMZ            │              │
│   │  Network        │     │  (Web Servers)  │              │
│   │  (Out of Scope) │     │                 │              │
│   └────────┬────────┘     └────────┬────────┘              │
│            │                       │                        │
│            │    ┌─────────────┐    │                        │
│            └────►  Firewall   ◄────┘                        │
│                 └──────┬──────┘                             │
│                        │                                    │
│            ┌───────────▼───────────┐                        │
│            │  Cardholder Data      │                        │
│            │  Environment (CDE)    │                        │
│            │  ┌─────────────────┐  │                        │
│            │  │ Payment Systems │  │                        │
│            │  └─────────────────┘  │                        │
│            └───────────────────────┘                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### SOC 2 Network Controls

**CC6.1 - Logical Access Security**
- Network segmentation implementation
- Firewall rule documentation
- Access control lists

**CC6.6 - Security Event Monitoring**
- VPC Flow Logs enabled
- SIEM integration
- Alerting on anomalies

**CC6.7 - Transmission Security**
- TLS 1.2+ enforcement
- Certificate management
- Encryption in transit

### HIPAA Network Requirements

**164.312(e)(1) - Transmission Security**
- Encryption of ePHI in transit
- Integrity controls
- Network access controls

**Implementation:**
```hcl
# Enforce TLS 1.2 minimum on ALB
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = aws_acm_certificate.main.arn
}
```

## Network Monitoring

### VPC Flow Logs

**Enable for all VPCs:**
```hcl
resource "aws_flow_log" "main" {
  vpc_id                   = aws_vpc.main.id
  traffic_type             = "ALL"
  log_destination_type     = "cloud-watch-logs"
  log_destination          = aws_cloudwatch_log_group.flow_logs.arn
  iam_role_arn             = aws_iam_role.flow_logs.arn
  max_aggregation_interval = 60

  tags = {
    Name = "vpc-flow-logs"
  }
}
```

**Custom Log Format (recommended):**
```
${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status} ${vpc-id} ${subnet-id} ${instance-id} ${tcp-flags} ${type} ${pkt-srcaddr} ${pkt-dstaddr}
```

### Traffic Analysis Queries

**Find Rejected Traffic:**
```sql
SELECT srcaddr, dstaddr, dstport, COUNT(*) as count
FROM vpc_flow_logs
WHERE action = 'REJECT'
AND start >= now() - interval '1' hour
GROUP BY srcaddr, dstaddr, dstport
ORDER BY count DESC
LIMIT 20
```

**Detect Port Scanning:**
```sql
SELECT srcaddr, COUNT(DISTINCT dstport) as port_count
FROM vpc_flow_logs
WHERE action = 'REJECT'
AND start >= now() - interval '1' hour
GROUP BY srcaddr
HAVING COUNT(DISTINCT dstport) > 100
ORDER BY port_count DESC
```

**Unusual Outbound Traffic:**
```sql
SELECT dstaddr, SUM(bytes) as total_bytes
FROM vpc_flow_logs
WHERE srcaddr LIKE '10.%'
AND NOT dstaddr LIKE '10.%'
AND start >= now() - interval '1' hour
GROUP BY dstaddr
ORDER BY total_bytes DESC
LIMIT 20
```

## Security Incident Response

### Network Isolation Runbook

**Step 1: Identify Compromised Resource**
```bash
# Get instance details
aws ec2 describe-instances --instance-ids i-1234567890abcdef0

# Get current security groups
aws ec2 describe-instance-attribute \
  --instance-id i-1234567890abcdef0 \
  --attribute groupSet
```

**Step 2: Create Isolation Security Group**
```bash
# Create quarantine security group
aws ec2 create-security-group \
  --group-name quarantine-sg \
  --description "Quarantine - No traffic allowed" \
  --vpc-id vpc-12345678

# No inbound or outbound rules = complete isolation
```

**Step 3: Apply Isolation**
```bash
# Replace security groups with quarantine
aws ec2 modify-instance-attribute \
  --instance-id i-1234567890abcdef0 \
  --groups sg-quarantine12345
```

**Step 4: Preserve Evidence**
```bash
# Create snapshot for forensics
aws ec2 create-snapshot \
  --volume-id vol-1234567890abcdef0 \
  --description "Forensic snapshot - incident 2024-001"

# Enable termination protection
aws ec2 modify-instance-attribute \
  --instance-id i-1234567890abcdef0 \
  --disable-api-termination
```

### Network Forensics Checklist

- [ ] Capture VPC Flow Logs for affected time period
- [ ] Export DNS query logs
- [ ] Collect WAF logs if applicable
- [ ] Snapshot network interfaces
- [ ] Document security group rules at time of incident
- [ ] Preserve load balancer access logs
- [ ] Export CloudTrail network-related events

## Best Practices Summary

### Security Group Rules

1. **Use security group references** instead of CIDR when possible
2. **Document all rules** with descriptions
3. **Review quarterly** for unused rules
4. **Separate by function** (one SG per service tier)
5. **Never use 0.0.0.0/0** for SSH/RDP

### Network Architecture

1. **Multi-AZ deployment** for high availability
2. **Private subnets** for application and database
3. **NAT Gateway per AZ** for resilience
4. **VPC endpoints** for AWS service access
5. **Transit Gateway** for multi-VPC connectivity

### Monitoring and Logging

1. **Enable VPC Flow Logs** on all VPCs
2. **Centralize logs** in SIEM
3. **Alert on rejected traffic** spikes
4. **Regular traffic analysis** for anomalies
5. **Automate incident response** where possible

## Resources

- AWS Security Best Practices: https://docs.aws.amazon.com/security/
- Azure Network Security: https://docs.microsoft.com/azure/security/
- GCP VPC Security: https://cloud.google.com/vpc/docs/firewalls
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
