# How to Use: Senior Network Infrastructure

Quick reference guide for the senior-network-infrastructure skill package.

## Quick Start

```bash
# VPN Configuration - Generate site-to-site VPN
python scripts/vpn_configurator.py --provider aws --type site-to-site --remote-ip 203.0.113.1 --output terraform

# Firewall Rules - Generate 3-tier security groups
python scripts/firewall_policy_generator.py --cloud aws --tier 3-tier --output terraform

# Network Analysis - Check configuration for issues
python scripts/network_topology_analyzer.py --input vpc-config.json --check-redundancy --security-audit

# Subnet Planning - Plan CIDR allocation for VPC
python scripts/subnet_planner.py --vpc-cidr 10.0.0.0/16 --azs 3 --tiers 3
```

## Tool Reference

### 1. VPN Configurator

Generate VPN configurations for AWS, Azure, and GCP.

```bash
# AWS Site-to-Site VPN
python scripts/vpn_configurator.py --provider aws --type site-to-site --remote-ip 203.0.113.1

# Azure VPN Gateway
python scripts/vpn_configurator.py --provider azure --type site-to-site --remote-ip 198.51.100.1

# GCP HA VPN
python scripts/vpn_configurator.py --provider gcp --type ha-vpn --output terraform

# Point-to-Site (Client VPN)
python scripts/vpn_configurator.py --provider aws --type point-to-site --client-cidr 10.200.0.0/16

# Full options
python scripts/vpn_configurator.py --help
```

**Output Formats:** `json`, `terraform`, `text`

### 2. Firewall Policy Generator

Create security groups and firewall rules.

```bash
# 3-tier application (web, app, database)
python scripts/firewall_policy_generator.py --cloud aws --tier 3-tier

# Microservices pattern
python scripts/firewall_policy_generator.py --cloud gcp --pattern microservices --services web,api,db

# Compliance-ready rules
python scripts/firewall_policy_generator.py --cloud azure --compliance pci-dss

# Custom application ports
python scripts/firewall_policy_generator.py --cloud aws --tier 3-tier --app-port 8080 --db-port 5432

# Full options
python scripts/firewall_policy_generator.py --help
```

**Output Formats:** `json`, `terraform`, `text`

### 3. Network Topology Analyzer

Analyze network configurations for issues.

```bash
# Redundancy check
python scripts/network_topology_analyzer.py --input vpc-config.json --check-redundancy

# Security audit
python scripts/network_topology_analyzer.py --input network-export.json --security-audit

# Compliance check
python scripts/network_topology_analyzer.py --input infra/ --compliance pci-dss

# Full analysis with markdown report
python scripts/network_topology_analyzer.py --input vpc-config.json --check-redundancy --security-audit --output report.md

# Full options
python scripts/network_topology_analyzer.py --help
```

**Output Formats:** `json`, `text`, `markdown`

### 4. Subnet Planner

Plan subnet allocations and CIDR blocks.

```bash
# Standard 3-tier, 3-AZ
python scripts/subnet_planner.py --vpc-cidr 10.0.0.0/16 --azs 3 --tiers 3

# Custom subnet sizes
python scripts/subnet_planner.py --vpc-cidr 172.16.0.0/12 --subnets public:24,private:22,database:26

# Reserve space for growth
python scripts/subnet_planner.py --vpc-cidr 10.0.0.0/16 --azs 3 --tiers 3 --reserve-future 20

# Generate IP inventory
python scripts/subnet_planner.py --vpc-cidr 10.0.0.0/16 --inventory --output csv

# Generate Terraform
python scripts/subnet_planner.py --vpc-cidr 10.0.0.0/16 --azs 3 --output terraform

# Full options
python scripts/subnet_planner.py --help
```

**Output Formats:** `json`, `terraform`, `csv`, `text`

## Common Workflows

### New VPC Design

```bash
# 1. Plan subnets
python scripts/subnet_planner.py --vpc-cidr 10.0.0.0/16 --azs 3 --tiers 3 --output terraform > subnets.tf

# 2. Generate security groups
python scripts/firewall_policy_generator.py --cloud aws --tier 3-tier --output terraform > security.tf

# 3. Validate design
python scripts/network_topology_analyzer.py --input . --check-redundancy
```

### VPN Setup

```bash
# 1. Generate VPN config
python scripts/vpn_configurator.py --provider aws --type site-to-site --remote-ip 203.0.113.1 --ha --output terraform > vpn.tf

# 2. Get customer gateway config
python scripts/vpn_configurator.py --provider aws --type site-to-site --remote-ip 203.0.113.1 --output text
```

### Security Audit

```bash
# 1. Export current config (from AWS/Azure/GCP)
# 2. Run analysis
python scripts/network_topology_analyzer.py --input network-export.json --security-audit --compliance pci-dss --output audit-report.md

# 3. Review findings and remediate
```

## Reference Guides

| Guide | Content |
|-------|---------|
| [vpc_design_patterns.md](references/vpc_design_patterns.md) | VPC architecture patterns, hub-spoke, multi-region |
| [network_security_guide.md](references/network_security_guide.md) | Security groups, NACLs, zero-trust, compliance |
| [cloud_networking.md](references/cloud_networking.md) | Direct Connect, ExpressRoute, Cloud Interconnect, VPN |

## Best Practices

1. **Use Private Subnets** - Place applications and databases in private subnets
2. **NAT per AZ** - Deploy NAT Gateway in each AZ for resilience
3. **Least Privilege** - Only allow required traffic in security groups
4. **Document Rules** - Add descriptions to all security group rules
5. **Enable Flow Logs** - Monitor all VPC traffic for security analysis
6. **Plan CIDR Carefully** - Use non-overlapping blocks across environments

## Troubleshooting

**VPN not connecting:**
- Check security group allows UDP 500, 4500, and ESP (protocol 50)
- Verify pre-shared key matches on both ends
- Confirm remote IP address is correct

**Security group not working:**
- Remember security groups are stateful (return traffic auto-allowed)
- Check NACL rules (stateless, must allow return traffic)
- Verify source/destination CIDR blocks

**Subnet out of IPs:**
- Review allocation with subnet_planner.py
- Check for unused ENIs and Elastic IPs
- Consider larger CIDR for high-density workloads

## Support

- Full documentation: [SKILL.md](SKILL.md)
- Reference guides: [references/](references/)
- Tool help: `python scripts/<tool>.py --help`
