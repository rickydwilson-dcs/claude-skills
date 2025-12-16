#!/usr/bin/env python3
"""
VPN Configurator

Generate production-ready VPN configurations for AWS, Azure, and GCP.
Supports site-to-site VPN, point-to-site VPN, and HA VPN configurations.

Part of senior-network-infrastructure skill for engineering-team.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class VPNConfigurator:
    """Generate VPN configurations for multi-cloud environments"""

    # Default configurations per provider
    PROVIDER_DEFAULTS = {
        'aws': {
            'tunnel_inside_cidr_1': '169.254.100.0/30',
            'tunnel_inside_cidr_2': '169.254.100.4/30',
            'ike_versions': ['ikev2'],
            'phase1_encryption': 'AES256',
            'phase1_integrity': 'SHA256',
            'phase1_dh_group': 14,
            'phase2_encryption': 'AES256',
            'phase2_integrity': 'SHA256',
            'phase2_dh_group': 14,
            'phase1_lifetime': 28800,
            'phase2_lifetime': 3600,
        },
        'azure': {
            'vpn_type': 'RouteBased',
            'sku': 'VpnGw1',
            'generation': 'Generation1',
            'ike_encryption': 'AES256',
            'ike_integrity': 'SHA256',
            'dh_group': 'DHGroup14',
            'ipsec_encryption': 'AES256',
            'ipsec_integrity': 'SHA256',
            'pfs_group': 'PFS14',
            'sa_lifetime': 27000,
        },
        'gcp': {
            'vpn_gateway_region': 'us-central1',
            'peer_gateway_redundancy_type': 'TWO_IPS_REDUNDANCY',
            'ike_version': 2,
            'shared_secret_type': 'GENERATED',
        }
    }

    def __init__(self, provider: str, vpn_type: str, remote_ip: Optional[str] = None,
                 remote_cidr: Optional[str] = None, ha: bool = False, verbose: bool = False):
        """
        Initialize VPN Configurator

        Args:
            provider: Cloud provider (aws, azure, gcp)
            vpn_type: VPN type (site-to-site, point-to-site, ha-vpn)
            remote_ip: Remote gateway IP address
            remote_cidr: Remote network CIDR block
            ha: Enable high availability with redundant tunnels
            verbose: Enable verbose output
        """
        self.provider = provider.lower()
        self.vpn_type = vpn_type.lower()
        self.remote_ip = remote_ip
        self.remote_cidr = remote_cidr or '10.0.0.0/8'
        self.ha = ha
        self.verbose = verbose
        self.config = {}

    def generate(self) -> Dict:
        """Generate VPN configuration based on provider and type"""
        if self.verbose:
            print(f"Generating {self.vpn_type} VPN configuration for {self.provider.upper()}")
            print(f"Remote IP: {self.remote_ip or 'Not specified'}")
            print(f"Remote CIDR: {self.remote_cidr}")
            print(f"High Availability: {'Enabled' if self.ha else 'Disabled'}")
            print()

        if self.provider == 'aws':
            return self._generate_aws_config()
        elif self.provider == 'azure':
            return self._generate_azure_config()
        elif self.provider == 'gcp':
            return self._generate_gcp_config()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _generate_aws_config(self) -> Dict:
        """Generate AWS VPN Gateway configuration"""
        defaults = self.PROVIDER_DEFAULTS['aws']

        config = {
            'provider': 'aws',
            'vpn_type': self.vpn_type,
            'generated_at': datetime.now().isoformat(),
            'resources': {
                'customer_gateway': {
                    'name': 'cgw-customer',
                    'bgp_asn': 65000,
                    'ip_address': self.remote_ip or 'REPLACE_WITH_REMOTE_IP',
                    'type': 'ipsec.1',
                },
                'vpn_gateway': {
                    'name': 'vgw-main',
                    'amazon_side_asn': 64512,
                },
                'vpn_connection': {
                    'name': 'vpn-to-customer',
                    'type': 'ipsec.1',
                    'static_routes_only': False,
                    'tunnel1_inside_cidr': defaults['tunnel_inside_cidr_1'],
                    'tunnel2_inside_cidr': defaults['tunnel_inside_cidr_2'],
                    'tunnel1_preshared_key': 'REPLACE_WITH_PSK_1',
                    'tunnel2_preshared_key': 'REPLACE_WITH_PSK_2',
                },
            },
            'tunnel_options': {
                'ike_versions': defaults['ike_versions'],
                'phase1_encryption_algorithms': [defaults['phase1_encryption']],
                'phase1_integrity_algorithms': [defaults['phase1_integrity']],
                'phase1_dh_group_numbers': [defaults['phase1_dh_group']],
                'phase2_encryption_algorithms': [defaults['phase2_encryption']],
                'phase2_integrity_algorithms': [defaults['phase2_integrity']],
                'phase2_dh_group_numbers': [defaults['phase2_dh_group']],
                'phase1_lifetime_seconds': defaults['phase1_lifetime'],
                'phase2_lifetime_seconds': defaults['phase2_lifetime'],
            },
            'routes': [
                {'destination_cidr_block': self.remote_cidr}
            ]
        }

        if self.ha:
            config['high_availability'] = {
                'enabled': True,
                'tunnels': 2,
                'description': 'AWS provides 2 tunnels by default for HA'
            }

        return config

    def _generate_azure_config(self) -> Dict:
        """Generate Azure VPN Gateway configuration"""
        defaults = self.PROVIDER_DEFAULTS['azure']

        config = {
            'provider': 'azure',
            'vpn_type': self.vpn_type,
            'generated_at': datetime.now().isoformat(),
            'resources': {
                'virtual_network_gateway': {
                    'name': 'vng-main',
                    'type': 'Vpn',
                    'vpn_type': defaults['vpn_type'],
                    'sku': defaults['sku'] if not self.ha else 'VpnGw1AZ',
                    'generation': defaults['generation'],
                    'enable_bgp': True,
                    'active_active': self.ha,
                    'bgp_settings': {
                        'asn': 65515,
                    }
                },
                'local_network_gateway': {
                    'name': 'lng-customer',
                    'gateway_ip_address': self.remote_ip or 'REPLACE_WITH_REMOTE_IP',
                    'address_prefixes': [self.remote_cidr],
                    'bgp_settings': {
                        'asn': 65000,
                        'bgp_peering_address': 'REPLACE_WITH_BGP_PEER_IP'
                    }
                },
                'vpn_connection': {
                    'name': 'conn-to-customer',
                    'connection_type': 'IPsec',
                    'shared_key': 'REPLACE_WITH_PSK',
                    'enable_bgp': True,
                }
            },
            'ipsec_policy': {
                'ike_encryption': defaults['ike_encryption'],
                'ike_integrity': defaults['ike_integrity'],
                'dh_group': defaults['dh_group'],
                'ipsec_encryption': defaults['ipsec_encryption'],
                'ipsec_integrity': defaults['ipsec_integrity'],
                'pfs_group': defaults['pfs_group'],
                'sa_lifetime_seconds': defaults['sa_lifetime'],
                'sa_data_size_kilobytes': 102400000,
            }
        }

        if self.ha:
            config['high_availability'] = {
                'enabled': True,
                'active_active': True,
                'zone_redundant': True,
                'description': 'Active-Active configuration with zone redundancy'
            }

        return config

    def _generate_gcp_config(self) -> Dict:
        """Generate GCP Cloud VPN configuration"""
        defaults = self.PROVIDER_DEFAULTS['gcp']

        config = {
            'provider': 'gcp',
            'vpn_type': self.vpn_type,
            'generated_at': datetime.now().isoformat(),
            'resources': {
                'ha_vpn_gateway': {
                    'name': 'ha-vpn-gateway',
                    'region': defaults['vpn_gateway_region'],
                    'network': 'REPLACE_WITH_VPC_NAME',
                },
                'external_vpn_gateway': {
                    'name': 'external-vpn-gateway',
                    'redundancy_type': defaults['peer_gateway_redundancy_type'] if self.ha else 'SINGLE_IP_INTERNALLY_REDUNDANT',
                    'interfaces': [
                        {'id': 0, 'ip_address': self.remote_ip or 'REPLACE_WITH_REMOTE_IP_1'},
                    ] if not self.ha else [
                        {'id': 0, 'ip_address': self.remote_ip or 'REPLACE_WITH_REMOTE_IP_1'},
                        {'id': 1, 'ip_address': 'REPLACE_WITH_REMOTE_IP_2'},
                    ]
                },
                'vpn_tunnels': [
                    {
                        'name': 'vpn-tunnel-0',
                        'vpn_gateway_interface': 0,
                        'peer_external_gateway_interface': 0,
                        'shared_secret': 'REPLACE_WITH_PSK',
                        'ike_version': defaults['ike_version'],
                        'router': 'REPLACE_WITH_ROUTER_NAME',
                    }
                ],
                'cloud_router': {
                    'name': 'router-vpn',
                    'region': defaults['vpn_gateway_region'],
                    'network': 'REPLACE_WITH_VPC_NAME',
                    'bgp': {
                        'asn': 64512,
                        'advertise_mode': 'CUSTOM',
                    }
                }
            }
        }

        if self.ha:
            # Add second tunnel for HA
            config['resources']['vpn_tunnels'].append({
                'name': 'vpn-tunnel-1',
                'vpn_gateway_interface': 1,
                'peer_external_gateway_interface': 1,
                'shared_secret': 'REPLACE_WITH_PSK_2',
                'ike_version': defaults['ike_version'],
                'router': 'REPLACE_WITH_ROUTER_NAME',
            })
            config['high_availability'] = {
                'enabled': True,
                'tunnels': 2,
                'description': 'HA VPN with 2 tunnels across gateway interfaces'
            }

        return config

    def to_terraform(self) -> str:
        """Convert configuration to Terraform format"""
        config = self.generate()

        if self.provider == 'aws':
            return self._aws_to_terraform(config)
        elif self.provider == 'azure':
            return self._azure_to_terraform(config)
        elif self.provider == 'gcp':
            return self._gcp_to_terraform(config)

        return ""

    def _aws_to_terraform(self, config: Dict) -> str:
        """Generate AWS Terraform configuration"""
        cgw = config['resources']['customer_gateway']
        vgw = config['resources']['vpn_gateway']
        vpn = config['resources']['vpn_connection']
        tunnel = config['tunnel_options']

        tf = f'''# AWS VPN Configuration
# Generated: {config['generated_at']}

# Customer Gateway (remote site)
resource "aws_customer_gateway" "{cgw['name'].replace('-', '_')}" {{
  bgp_asn    = {cgw['bgp_asn']}
  ip_address = "{cgw['ip_address']}"
  type       = "{cgw['type']}"

  tags = {{
    Name = "{cgw['name']}"
  }}
}}

# Virtual Private Gateway
resource "aws_vpn_gateway" "{vgw['name'].replace('-', '_')}" {{
  amazon_side_asn = {vgw['amazon_side_asn']}

  tags = {{
    Name = "{vgw['name']}"
  }}
}}

# VPN Gateway Attachment (attach to your VPC)
resource "aws_vpn_gateway_attachment" "vpn_attachment" {{
  vpc_id         = var.vpc_id  # Replace with your VPC ID
  vpn_gateway_id = aws_vpn_gateway.{vgw['name'].replace('-', '_')}.id
}}

# VPN Connection
resource "aws_vpn_connection" "{vpn['name'].replace('-', '_')}" {{
  vpn_gateway_id      = aws_vpn_gateway.{vgw['name'].replace('-', '_')}.id
  customer_gateway_id = aws_customer_gateway.{cgw['name'].replace('-', '_')}.id
  type                = "{vpn['type']}"
  static_routes_only  = {str(vpn['static_routes_only']).lower()}

  tunnel1_inside_cidr   = "{vpn['tunnel1_inside_cidr']}"
  tunnel2_inside_cidr   = "{vpn['tunnel2_inside_cidr']}"
  tunnel1_preshared_key = var.tunnel1_psk  # Use variable for security
  tunnel2_preshared_key = var.tunnel2_psk  # Use variable for security

  tunnel1_ike_versions                 = {json.dumps(tunnel['ike_versions'])}
  tunnel1_phase1_encryption_algorithms = {json.dumps(tunnel['phase1_encryption_algorithms'])}
  tunnel1_phase1_integrity_algorithms  = {json.dumps(tunnel['phase1_integrity_algorithms'])}
  tunnel1_phase1_dh_group_numbers      = {json.dumps(tunnel['phase1_dh_group_numbers'])}
  tunnel1_phase2_encryption_algorithms = {json.dumps(tunnel['phase2_encryption_algorithms'])}
  tunnel1_phase2_integrity_algorithms  = {json.dumps(tunnel['phase2_integrity_algorithms'])}
  tunnel1_phase2_dh_group_numbers      = {json.dumps(tunnel['phase2_dh_group_numbers'])}
  tunnel1_phase1_lifetime_seconds      = {tunnel['phase1_lifetime_seconds']}
  tunnel1_phase2_lifetime_seconds      = {tunnel['phase2_lifetime_seconds']}

  tunnel2_ike_versions                 = {json.dumps(tunnel['ike_versions'])}
  tunnel2_phase1_encryption_algorithms = {json.dumps(tunnel['phase1_encryption_algorithms'])}
  tunnel2_phase1_integrity_algorithms  = {json.dumps(tunnel['phase1_integrity_algorithms'])}
  tunnel2_phase1_dh_group_numbers      = {json.dumps(tunnel['phase1_dh_group_numbers'])}
  tunnel2_phase2_encryption_algorithms = {json.dumps(tunnel['phase2_encryption_algorithms'])}
  tunnel2_phase2_integrity_algorithms  = {json.dumps(tunnel['phase2_integrity_algorithms'])}
  tunnel2_phase2_dh_group_numbers      = {json.dumps(tunnel['phase2_dh_group_numbers'])}
  tunnel2_phase1_lifetime_seconds      = {tunnel['phase1_lifetime_seconds']}
  tunnel2_phase2_lifetime_seconds      = {tunnel['phase2_lifetime_seconds']}

  tags = {{
    Name = "{vpn['name']}"
  }}
}}

# Route to remote network
resource "aws_vpn_connection_route" "remote_route" {{
  destination_cidr_block = "{config['routes'][0]['destination_cidr_block']}"
  vpn_connection_id      = aws_vpn_connection.{vpn['name'].replace('-', '_')}.id
}}

# Variables
variable "vpc_id" {{
  description = "VPC ID to attach VPN Gateway"
  type        = string
}}

variable "tunnel1_psk" {{
  description = "Pre-shared key for tunnel 1"
  type        = string
  sensitive   = true
}}

variable "tunnel2_psk" {{
  description = "Pre-shared key for tunnel 2"
  type        = string
  sensitive   = true
}}

# Outputs
output "vpn_connection_id" {{
  value = aws_vpn_connection.{vpn['name'].replace('-', '_')}.id
}}

output "tunnel1_address" {{
  value = aws_vpn_connection.{vpn['name'].replace('-', '_')}.tunnel1_address
}}

output "tunnel2_address" {{
  value = aws_vpn_connection.{vpn['name'].replace('-', '_')}.tunnel2_address
}}
'''
        return tf

    def _azure_to_terraform(self, config: Dict) -> str:
        """Generate Azure Terraform configuration"""
        vng = config['resources']['virtual_network_gateway']
        lng = config['resources']['local_network_gateway']
        conn = config['resources']['vpn_connection']
        ipsec = config['ipsec_policy']

        tf = f'''# Azure VPN Configuration
# Generated: {config['generated_at']}

# Virtual Network Gateway
resource "azurerm_virtual_network_gateway" "{vng['name'].replace('-', '_')}" {{
  name                = "{vng['name']}"
  location            = var.location
  resource_group_name = var.resource_group_name

  type     = "{vng['type']}"
  vpn_type = "{vng['vpn_type']}"
  sku      = "{vng['sku']}"
  generation = "{vng['generation']}"

  active_active = {str(vng['active_active']).lower()}
  enable_bgp    = {str(vng['enable_bgp']).lower()}

  bgp_settings {{
    asn = {vng['bgp_settings']['asn']}
  }}

  ip_configuration {{
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.vpn_gateway_ip.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = var.gateway_subnet_id
  }}
}}

# Public IP for VPN Gateway
resource "azurerm_public_ip" "vpn_gateway_ip" {{
  name                = "pip-vpn-gateway"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
}}

# Local Network Gateway (remote site)
resource "azurerm_local_network_gateway" "{lng['name'].replace('-', '_')}" {{
  name                = "{lng['name']}"
  location            = var.location
  resource_group_name = var.resource_group_name

  gateway_address = "{lng['gateway_ip_address']}"
  address_space   = {json.dumps(lng['address_prefixes'])}

  bgp_settings {{
    asn                 = {lng['bgp_settings']['asn']}
    bgp_peering_address = "{lng['bgp_settings']['bgp_peering_address']}"
  }}
}}

# VPN Connection
resource "azurerm_virtual_network_gateway_connection" "{conn['name'].replace('-', '_')}" {{
  name                = "{conn['name']}"
  location            = var.location
  resource_group_name = var.resource_group_name

  type                       = "{conn['connection_type']}"
  virtual_network_gateway_id = azurerm_virtual_network_gateway.{vng['name'].replace('-', '_')}.id
  local_network_gateway_id   = azurerm_local_network_gateway.{lng['name'].replace('-', '_')}.id

  shared_key = var.vpn_shared_key
  enable_bgp = {str(conn['enable_bgp']).lower()}

  ipsec_policy {{
    ike_encryption   = "{ipsec['ike_encryption']}"
    ike_integrity    = "{ipsec['ike_integrity']}"
    dh_group         = "{ipsec['dh_group']}"
    ipsec_encryption = "{ipsec['ipsec_encryption']}"
    ipsec_integrity  = "{ipsec['ipsec_integrity']}"
    pfs_group        = "{ipsec['pfs_group']}"
    sa_lifetime      = {ipsec['sa_lifetime_seconds']}
    sa_datasize      = {ipsec['sa_data_size_kilobytes']}
  }}
}}

# Variables
variable "location" {{
  description = "Azure region"
  type        = string
  default     = "eastus"
}}

variable "resource_group_name" {{
  description = "Resource group name"
  type        = string
}}

variable "gateway_subnet_id" {{
  description = "Gateway subnet ID (must be named GatewaySubnet)"
  type        = string
}}

variable "vpn_shared_key" {{
  description = "VPN pre-shared key"
  type        = string
  sensitive   = true
}}

# Outputs
output "vpn_gateway_public_ip" {{
  value = azurerm_public_ip.vpn_gateway_ip.ip_address
}}

output "vpn_connection_id" {{
  value = azurerm_virtual_network_gateway_connection.{conn['name'].replace('-', '_')}.id
}}
'''
        return tf

    def _gcp_to_terraform(self, config: Dict) -> str:
        """Generate GCP Terraform configuration"""
        ha_gw = config['resources']['ha_vpn_gateway']
        ext_gw = config['resources']['external_vpn_gateway']
        tunnels = config['resources']['vpn_tunnels']
        router = config['resources']['cloud_router']

        tf = f'''# GCP Cloud VPN Configuration
# Generated: {config['generated_at']}

# HA VPN Gateway
resource "google_compute_ha_vpn_gateway" "{ha_gw['name'].replace('-', '_')}" {{
  name    = "{ha_gw['name']}"
  region  = "{ha_gw['region']}"
  network = var.network_name
}}

# External VPN Gateway (peer)
resource "google_compute_external_vpn_gateway" "{ext_gw['name'].replace('-', '_')}" {{
  name            = "{ext_gw['name']}"
  redundancy_type = "{ext_gw['redundancy_type']}"

'''
        # Add interfaces
        for iface in ext_gw['interfaces']:
            tf += f'''  interface {{
    id         = {iface['id']}
    ip_address = "{iface['ip_address']}"
  }}

'''

        tf += f'''}}

# Cloud Router
resource "google_compute_router" "{router['name'].replace('-', '_')}" {{
  name    = "{router['name']}"
  region  = "{router['region']}"
  network = var.network_name

  bgp {{
    asn            = {router['bgp']['asn']}
    advertise_mode = "{router['bgp']['advertise_mode']}"
  }}
}}

'''
        # Add VPN tunnels
        for i, tunnel in enumerate(tunnels):
            tf += f'''# VPN Tunnel {i}
resource "google_compute_vpn_tunnel" "{tunnel['name'].replace('-', '_')}" {{
  name                            = "{tunnel['name']}"
  region                          = "{ha_gw['region']}"
  vpn_gateway                     = google_compute_ha_vpn_gateway.{ha_gw['name'].replace('-', '_')}.id
  vpn_gateway_interface           = {tunnel['vpn_gateway_interface']}
  peer_external_gateway           = google_compute_external_vpn_gateway.{ext_gw['name'].replace('-', '_')}.id
  peer_external_gateway_interface = {tunnel['peer_external_gateway_interface']}
  shared_secret                   = var.vpn_shared_secret_{i}
  ike_version                     = {tunnel['ike_version']}
  router                          = google_compute_router.{router['name'].replace('-', '_')}.id
}}

# Router Interface for Tunnel {i}
resource "google_compute_router_interface" "router_interface_{i}" {{
  name       = "interface-{i}"
  router     = google_compute_router.{router['name'].replace('-', '_')}.name
  region     = "{ha_gw['region']}"
  ip_range   = "169.254.{i}.1/30"
  vpn_tunnel = google_compute_vpn_tunnel.{tunnel['name'].replace('-', '_')}.name
}}

# BGP Peer for Tunnel {i}
resource "google_compute_router_peer" "router_peer_{i}" {{
  name            = "peer-{i}"
  router          = google_compute_router.{router['name'].replace('-', '_')}.name
  region          = "{ha_gw['region']}"
  peer_ip_address = "169.254.{i}.2"
  peer_asn        = 65000
  interface       = google_compute_router_interface.router_interface_{i}.name
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
        for i in range(len(tunnels)):
            tf += f'''variable "vpn_shared_secret_{i}" {{
  description = "VPN shared secret for tunnel {i}"
  type        = string
  sensitive   = true
}}

'''

        tf += f'''# Outputs
output "ha_vpn_gateway_ip_0" {{
  value = google_compute_ha_vpn_gateway.{ha_gw['name'].replace('-', '_')}.vpn_interfaces[0].ip_address
}}

output "ha_vpn_gateway_ip_1" {{
  value = google_compute_ha_vpn_gateway.{ha_gw['name'].replace('-', '_')}.vpn_interfaces[1].ip_address
}}
'''
        return tf


def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="VPN Configurator - Generate VPN configurations for AWS, Azure, GCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python vpn_configurator.py --provider aws --type site-to-site --remote-ip 203.0.113.1 --output terraform
  python vpn_configurator.py --provider azure --type site-to-site --ha --output json
  python vpn_configurator.py --provider gcp --type ha-vpn --output terraform

Part of senior-network-infrastructure skill.
"""
    )

    parser.add_argument(
        '--provider',
        required=True,
        choices=['aws', 'azure', 'gcp'],
        help='Cloud provider (aws, azure, gcp)'
    )

    parser.add_argument(
        '--type',
        required=True,
        choices=['site-to-site', 'point-to-site', 'ha-vpn'],
        help='VPN type'
    )

    parser.add_argument(
        '--remote-ip',
        help='Remote gateway IP address'
    )

    parser.add_argument(
        '--remote-cidr',
        default='10.0.0.0/8',
        help='Remote network CIDR block (default: 10.0.0.0/8)'
    )

    parser.add_argument(
        '--ha',
        action='store_true',
        help='Enable high availability configuration'
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
        version='VPN Configurator v1.0.0'
    )

    args = parser.parse_args()

    # Create configurator
    configurator = VPNConfigurator(
        provider=args.provider,
        vpn_type=args.type,
        remote_ip=args.remote_ip,
        remote_cidr=args.remote_cidr,
        ha=args.ha,
        verbose=args.verbose
    )

    # Generate output
    if args.output == 'terraform':
        output = configurator.to_terraform()
    elif args.output == 'json':
        config = configurator.generate()
        output = json.dumps(config, indent=2)
    else:
        config = configurator.generate()
        output = f"""
VPN Configuration Summary
{'=' * 50}
Provider:     {config['provider'].upper()}
VPN Type:     {config['vpn_type']}
Generated:    {config['generated_at']}

Resources:
"""
        for resource_type, resource in config['resources'].items():
            output += f"  {resource_type}:\n"
            if isinstance(resource, dict):
                for key, value in resource.items():
                    output += f"    {key}: {value}\n"
            elif isinstance(resource, list):
                for item in resource:
                    output += f"    - {item}\n"

        if 'high_availability' in config:
            output += f"\nHigh Availability:\n"
            for key, value in config['high_availability'].items():
                output += f"  {key}: {value}\n"

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
