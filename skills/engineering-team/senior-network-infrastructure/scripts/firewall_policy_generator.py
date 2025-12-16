#!/usr/bin/env python3
"""
Firewall Policy Generator

Generate security groups, NACLs, and firewall rules for AWS, Azure, and GCP.
Supports 3-tier applications, microservices, and compliance-ready configurations.

Part of senior-network-infrastructure skill for engineering-team.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class FirewallPolicyGenerator:
    """Generate firewall policies for multi-cloud environments"""

    # Common service ports
    COMMON_PORTS = {
        'ssh': 22,
        'http': 80,
        'https': 443,
        'mysql': 3306,
        'postgres': 5432,
        'redis': 6379,
        'mongodb': 27017,
        'elasticsearch': 9200,
        'kafka': 9092,
    }

    # 3-tier application template
    THREE_TIER_TEMPLATE = {
        'web': {
            'inbound': [
                {'port': 80, 'protocol': 'tcp', 'source': '0.0.0.0/0', 'description': 'HTTP from internet'},
                {'port': 443, 'protocol': 'tcp', 'source': '0.0.0.0/0', 'description': 'HTTPS from internet'},
            ],
            'outbound': [
                {'port': 'app_port', 'protocol': 'tcp', 'destination': 'app_tier', 'description': 'To application tier'},
                {'port': 443, 'protocol': 'tcp', 'destination': '0.0.0.0/0', 'description': 'HTTPS outbound'},
            ]
        },
        'app': {
            'inbound': [
                {'port': 'app_port', 'protocol': 'tcp', 'source': 'web_tier', 'description': 'From web tier'},
            ],
            'outbound': [
                {'port': 'db_port', 'protocol': 'tcp', 'destination': 'db_tier', 'description': 'To database tier'},
                {'port': 443, 'protocol': 'tcp', 'destination': '0.0.0.0/0', 'description': 'HTTPS outbound'},
            ]
        },
        'db': {
            'inbound': [
                {'port': 'db_port', 'protocol': 'tcp', 'source': 'app_tier', 'description': 'From application tier'},
            ],
            'outbound': []
        }
    }

    # Compliance requirements
    COMPLIANCE_RULES = {
        'pci-dss': {
            'requirements': [
                'No direct internet access to cardholder data environment',
                'Deny all by default, allow specific traffic',
                'Log all network access to critical systems',
                'Segregate cardholder data environment',
            ],
            'additional_rules': [
                {'description': 'Block all inbound from internet to DB tier', 'action': 'deny'},
            ]
        },
        'hipaa': {
            'requirements': [
                'Encrypt data in transit',
                'Access controls for PHI systems',
                'Audit logging for all access',
            ],
            'additional_rules': []
        },
        'soc2': {
            'requirements': [
                'Logical access controls',
                'Network segmentation',
                'Change management for firewall rules',
            ],
            'additional_rules': []
        }
    }

    def __init__(self, cloud: str, tier: str = '3-tier', pattern: str = None,
                 app_port: int = 8080, db_port: int = 5432,
                 services: List[str] = None, compliance: str = None,
                 verbose: bool = False):
        """
        Initialize Firewall Policy Generator

        Args:
            cloud: Cloud provider (aws, azure, gcp)
            tier: Application tier pattern (3-tier, microservices, custom)
            pattern: Architecture pattern (microservices, lambda, etc.)
            app_port: Application tier port (default: 8080)
            db_port: Database port (default: 5432)
            services: List of services for microservices pattern
            compliance: Compliance framework (pci-dss, hipaa, soc2)
            verbose: Enable verbose output
        """
        self.cloud = cloud.lower()
        self.tier = tier
        self.pattern = pattern
        self.app_port = app_port
        self.db_port = db_port
        self.services = services or []
        self.compliance = compliance
        self.verbose = verbose
        self.rules = {}

    def generate(self) -> Dict:
        """Generate firewall policy based on configuration"""
        if self.verbose:
            print(f"Generating firewall policies for {self.cloud.upper()}")
            print(f"Pattern: {self.tier}")
            print(f"App Port: {self.app_port}, DB Port: {self.db_port}")
            if self.compliance:
                print(f"Compliance: {self.compliance.upper()}")
            print()

        if self.tier == '3-tier':
            return self._generate_three_tier()
        elif self.pattern == 'microservices':
            return self._generate_microservices()
        else:
            return self._generate_custom()

    def _generate_three_tier(self) -> Dict:
        """Generate 3-tier application security groups"""
        config = {
            'cloud': self.cloud,
            'pattern': '3-tier',
            'generated_at': datetime.now().isoformat(),
            'security_groups': {}
        }

        for tier_name, tier_rules in self.THREE_TIER_TEMPLATE.items():
            sg_name = f"sg-{tier_name}"
            sg_config = {
                'name': sg_name,
                'description': f"Security group for {tier_name} tier",
                'inbound_rules': [],
                'outbound_rules': []
            }

            # Process inbound rules
            for rule in tier_rules['inbound']:
                port = rule['port']
                if port == 'app_port':
                    port = self.app_port
                elif port == 'db_port':
                    port = self.db_port

                source = rule['source']
                if source == 'web_tier':
                    source = 'sg-web'
                elif source == 'app_tier':
                    source = 'sg-app'

                sg_config['inbound_rules'].append({
                    'port': port,
                    'protocol': rule['protocol'],
                    'source': source,
                    'description': rule['description']
                })

            # Process outbound rules
            for rule in tier_rules['outbound']:
                port = rule['port']
                if port == 'app_port':
                    port = self.app_port
                elif port == 'db_port':
                    port = self.db_port

                destination = rule['destination']
                if destination == 'app_tier':
                    destination = 'sg-app'
                elif destination == 'db_tier':
                    destination = 'sg-db'

                sg_config['outbound_rules'].append({
                    'port': port,
                    'protocol': rule['protocol'],
                    'destination': destination,
                    'description': rule['description']
                })

            config['security_groups'][tier_name] = sg_config

        # Add compliance requirements if specified
        if self.compliance:
            config['compliance'] = {
                'framework': self.compliance,
                'requirements': self.COMPLIANCE_RULES.get(self.compliance, {}).get('requirements', [])
            }

        return config

    def _generate_microservices(self) -> Dict:
        """Generate microservices security groups"""
        config = {
            'cloud': self.cloud,
            'pattern': 'microservices',
            'generated_at': datetime.now().isoformat(),
            'security_groups': {}
        }

        # Default services if none provided
        services = self.services or ['web', 'api', 'worker', 'db']

        for service in services:
            sg_name = f"sg-{service}"
            sg_config = {
                'name': sg_name,
                'description': f"Security group for {service} service",
                'inbound_rules': [],
                'outbound_rules': []
            }

            # Service-specific rules
            if service == 'web':
                sg_config['inbound_rules'] = [
                    {'port': 80, 'protocol': 'tcp', 'source': '0.0.0.0/0', 'description': 'HTTP'},
                    {'port': 443, 'protocol': 'tcp', 'source': '0.0.0.0/0', 'description': 'HTTPS'},
                ]
            elif service == 'api':
                sg_config['inbound_rules'] = [
                    {'port': self.app_port, 'protocol': 'tcp', 'source': 'sg-web', 'description': 'From web'},
                    {'port': self.app_port, 'protocol': 'tcp', 'source': 'sg-worker', 'description': 'From worker'},
                ]
            elif service == 'worker':
                sg_config['inbound_rules'] = []  # Workers typically don't accept inbound
            elif service == 'db':
                sg_config['inbound_rules'] = [
                    {'port': self.db_port, 'protocol': 'tcp', 'source': 'sg-api', 'description': 'From API'},
                    {'port': self.db_port, 'protocol': 'tcp', 'source': 'sg-worker', 'description': 'From worker'},
                ]

            # Common outbound rules
            sg_config['outbound_rules'] = [
                {'port': 443, 'protocol': 'tcp', 'destination': '0.0.0.0/0', 'description': 'HTTPS outbound'},
            ]

            config['security_groups'][service] = sg_config

        return config

    def _generate_custom(self) -> Dict:
        """Generate custom security group configuration"""
        return {
            'cloud': self.cloud,
            'pattern': 'custom',
            'generated_at': datetime.now().isoformat(),
            'security_groups': {
                'default': {
                    'name': 'sg-default',
                    'description': 'Default security group - customize as needed',
                    'inbound_rules': [
                        {'port': 443, 'protocol': 'tcp', 'source': '0.0.0.0/0', 'description': 'HTTPS'},
                    ],
                    'outbound_rules': [
                        {'port': 443, 'protocol': 'tcp', 'destination': '0.0.0.0/0', 'description': 'HTTPS'},
                    ]
                }
            }
        }

    def to_terraform(self) -> str:
        """Convert configuration to Terraform format"""
        config = self.generate()

        if self.cloud == 'aws':
            return self._aws_to_terraform(config)
        elif self.cloud == 'azure':
            return self._azure_to_terraform(config)
        elif self.cloud == 'gcp':
            return self._gcp_to_terraform(config)

        return ""

    def _aws_to_terraform(self, config: Dict) -> str:
        """Generate AWS Security Groups Terraform"""
        tf = f'''# AWS Security Groups
# Generated: {config['generated_at']}
# Pattern: {config['pattern']}

'''
        for tier_name, sg in config['security_groups'].items():
            resource_name = sg['name'].replace('-', '_')
            tf += f'''# Security Group: {sg['name']}
resource "aws_security_group" "{resource_name}" {{
  name        = "{sg['name']}"
  description = "{sg['description']}"
  vpc_id      = var.vpc_id

'''
            # Inbound rules
            for rule in sg['inbound_rules']:
                source_key = 'cidr_blocks' if '/' in str(rule['source']) else 'security_groups'
                source_value = f'["{rule["source"]}"]' if '/' in str(rule['source']) else f'[aws_security_group.{rule["source"].replace("-", "_")}.id]'

                tf += f'''  ingress {{
    description     = "{rule['description']}"
    from_port       = {rule['port']}
    to_port         = {rule['port']}
    protocol        = "{rule['protocol']}"
    {source_key} = {source_value}
  }}

'''
            # Outbound rules
            for rule in sg['outbound_rules']:
                dest_key = 'cidr_blocks' if '/' in str(rule['destination']) else 'security_groups'
                dest_value = f'["{rule["destination"]}"]' if '/' in str(rule['destination']) else f'[aws_security_group.{rule["destination"].replace("-", "_")}.id]'

                tf += f'''  egress {{
    description     = "{rule['description']}"
    from_port       = {rule['port']}
    to_port         = {rule['port']}
    protocol        = "{rule['protocol']}"
    {dest_key} = {dest_value}
  }}

'''
            tf += f'''  tags = {{
    Name        = "{sg['name']}"
    Environment = var.environment
    ManagedBy   = "terraform"
  }}
}}

'''
        tf += '''# Variables
variable "vpc_id" {
  description = "VPC ID for security groups"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# Outputs
'''
        for tier_name, sg in config['security_groups'].items():
            resource_name = sg['name'].replace('-', '_')
            tf += f'''output "{resource_name}_id" {{
  value = aws_security_group.{resource_name}.id
}}

'''
        return tf

    def _azure_to_terraform(self, config: Dict) -> str:
        """Generate Azure NSGs Terraform"""
        tf = f'''# Azure Network Security Groups
# Generated: {config['generated_at']}
# Pattern: {config['pattern']}

'''
        priority = 100
        for tier_name, sg in config['security_groups'].items():
            resource_name = sg['name'].replace('-', '_')
            tf += f'''# NSG: {sg['name']}
resource "azurerm_network_security_group" "{resource_name}" {{
  name                = "{sg['name']}"
  location            = var.location
  resource_group_name = var.resource_group_name

'''
            # Inbound rules
            for i, rule in enumerate(sg['inbound_rules']):
                rule_priority = priority + i
                tf += f'''  security_rule {{
    name                       = "{sg['name']}-inbound-{i}"
    priority                   = {rule_priority}
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "{rule['protocol'].title()}"
    source_port_range          = "*"
    destination_port_range     = "{rule['port']}"
    source_address_prefix      = "{rule['source']}"
    destination_address_prefix = "*"
    description                = "{rule['description']}"
  }}

'''
            # Outbound rules
            for i, rule in enumerate(sg['outbound_rules']):
                rule_priority = priority + len(sg['inbound_rules']) + i
                tf += f'''  security_rule {{
    name                       = "{sg['name']}-outbound-{i}"
    priority                   = {rule_priority}
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "{rule['protocol'].title()}"
    source_port_range          = "*"
    destination_port_range     = "{rule['port']}"
    source_address_prefix      = "*"
    destination_address_prefix = "{rule['destination']}"
    description                = "{rule['description']}"
  }}

'''
            tf += f'''  tags = {{
    Environment = var.environment
    ManagedBy   = "terraform"
  }}
}}

'''
        tf += '''# Variables
variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}
'''
        return tf

    def _gcp_to_terraform(self, config: Dict) -> str:
        """Generate GCP Firewall Rules Terraform"""
        tf = f'''# GCP Firewall Rules
# Generated: {config['generated_at']}
# Pattern: {config['pattern']}

'''
        priority = 1000
        for tier_name, sg in config['security_groups'].items():
            # Inbound rules
            for i, rule in enumerate(sg['inbound_rules']):
                resource_name = f"{sg['name']}_allow_{rule['port']}_{i}".replace('-', '_')
                source_ranges = f'["{rule["source"]}"]' if '/' in str(rule['source']) else 'null'
                source_tags = '[]' if '/' in str(rule['source']) else f'["{rule["source"]}"]'

                tf += f'''# Firewall: {sg['name']} - {rule['description']}
resource "google_compute_firewall" "{resource_name}" {{
  name    = "{sg['name']}-allow-{rule['port']}-{i}"
  network = var.network_name

  allow {{
    protocol = "{rule['protocol']}"
    ports    = ["{rule['port']}"]
  }}

  source_ranges = {source_ranges}
  source_tags   = {source_tags}
  target_tags   = ["{tier_name}"]

  priority    = {priority + i}
  direction   = "INGRESS"
  description = "{rule['description']}"
}}

'''
        tf += '''# Variables
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "network_name" {
  description = "VPC network name"
  type        = string
}
'''
        return tf


def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="Firewall Policy Generator - Generate security groups for AWS, Azure, GCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python firewall_policy_generator.py --cloud aws --tier 3-tier --output terraform
  python firewall_policy_generator.py --cloud azure --tier 3-tier --app-port 8080 --db-port 5432
  python firewall_policy_generator.py --cloud gcp --pattern microservices --services web,api,db
  python firewall_policy_generator.py --cloud aws --tier 3-tier --compliance pci-dss

Part of senior-network-infrastructure skill.
"""
    )

    parser.add_argument(
        '--cloud',
        required=True,
        choices=['aws', 'azure', 'gcp'],
        help='Cloud provider (aws, azure, gcp)'
    )

    parser.add_argument(
        '--tier',
        choices=['3-tier', 'custom'],
        default='3-tier',
        help='Application tier pattern (default: 3-tier)'
    )

    parser.add_argument(
        '--pattern',
        choices=['microservices', 'serverless', 'custom'],
        help='Architecture pattern'
    )

    parser.add_argument(
        '--app-port',
        type=int,
        default=8080,
        help='Application tier port (default: 8080)'
    )

    parser.add_argument(
        '--db-port',
        type=int,
        default=5432,
        help='Database port (default: 5432)'
    )

    parser.add_argument(
        '--services',
        help='Comma-separated list of services for microservices pattern'
    )

    parser.add_argument(
        '--compliance',
        choices=['pci-dss', 'hipaa', 'soc2'],
        help='Compliance framework to apply'
    )

    parser.add_argument(
        '-o', '--output',
        choices=['json', 'terraform', 'text'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '-f', '--file',
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Firewall Policy Generator v1.0.0'
    )

    args = parser.parse_args()

    # Parse services if provided
    services = args.services.split(',') if args.services else None

    # Create generator
    generator = FirewallPolicyGenerator(
        cloud=args.cloud,
        tier=args.tier,
        pattern=args.pattern,
        app_port=args.app_port,
        db_port=args.db_port,
        services=services,
        compliance=args.compliance,
        verbose=args.verbose
    )

    # Generate output
    if args.output == 'terraform':
        output = generator.to_terraform()
    elif args.output == 'json':
        config = generator.generate()
        output = json.dumps(config, indent=2)
    else:
        config = generator.generate()
        output = f"""
Firewall Policy Summary
{'=' * 50}
Cloud:        {config['cloud'].upper()}
Pattern:      {config['pattern']}
Generated:    {config['generated_at']}

Security Groups:
"""
        for tier_name, sg in config['security_groups'].items():
            output += f"\n  {sg['name']}:\n"
            output += f"    Description: {sg['description']}\n"
            output += f"    Inbound Rules: {len(sg['inbound_rules'])}\n"
            for rule in sg['inbound_rules']:
                output += f"      - Port {rule['port']}/{rule['protocol']} from {rule['source']}: {rule['description']}\n"
            output += f"    Outbound Rules: {len(sg['outbound_rules'])}\n"
            for rule in sg['outbound_rules']:
                output += f"      - Port {rule['port']}/{rule['protocol']} to {rule['destination']}: {rule['description']}\n"

        if 'compliance' in config:
            output += f"\nCompliance Framework: {config['compliance']['framework'].upper()}\n"
            output += "Requirements:\n"
            for req in config['compliance']['requirements']:
                output += f"  - {req}\n"

        output += f"\nUse --output terraform for Terraform configuration\n"

    # Output results
    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Configuration saved to: {args.file}")
    else:
        print(output)


if __name__ == "__main__":
    main()
