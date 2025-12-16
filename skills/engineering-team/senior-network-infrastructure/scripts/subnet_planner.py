#!/usr/bin/env python3
"""
Subnet Planner

Calculate CIDR allocations and plan subnet layouts for optimal IP utilization.
Supports multi-AZ planning, tier-based allocation, and IP inventory generation.

Part of senior-network-infrastructure skill for engineering-team.
"""

import os
import sys
import json
import argparse
import ipaddress
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class SubnetPlanner:
    """Plan subnet allocations and CIDR blocks"""

    # Default subnet sizes (CIDR suffix)
    DEFAULT_SUBNET_SIZES = {
        'public': 24,      # 251 usable IPs per subnet
        'private': 22,     # 1019 usable IPs per subnet
        'database': 26,    # 59 usable IPs per subnet
        'cache': 27,       # 27 usable IPs per subnet
        'management': 28,  # 11 usable IPs per subnet
    }

    # AWS reserves 5 IPs per subnet
    # Azure reserves 5 IPs per subnet
    # GCP reserves 4 IPs per subnet
    RESERVED_IPS = {
        'aws': 5,
        'azure': 5,
        'gcp': 4
    }

    def __init__(self, vpc_cidr: str, azs: int = 3, tiers: int = 3,
                 subnets: str = None, reserve_future: int = 0,
                 cloud: str = 'aws', verbose: bool = False):
        """
        Initialize Subnet Planner

        Args:
            vpc_cidr: VPC CIDR block (e.g., 10.0.0.0/16)
            azs: Number of availability zones
            tiers: Number of tiers (3 = public, private, database)
            subnets: Custom subnet specification (e.g., "public:24,private:22,db:26")
            reserve_future: Percentage of address space to reserve for future use
            cloud: Cloud provider for reserved IP calculation
            verbose: Enable verbose output
        """
        self.vpc_cidr = vpc_cidr
        self.vpc_network = ipaddress.ip_network(vpc_cidr, strict=False)
        self.azs = azs
        self.tiers = tiers
        self.subnets = self._parse_subnets(subnets) if subnets else None
        self.reserve_future = reserve_future
        self.cloud = cloud.lower()
        self.verbose = verbose

    def _parse_subnets(self, subnets_str: str) -> Dict[str, int]:
        """Parse custom subnet specification"""
        result = {}
        for spec in subnets_str.split(','):
            parts = spec.strip().split(':')
            if len(parts) == 2:
                name = parts[0].strip()
                size = int(parts[1].strip())
                result[name] = size
        return result

    def plan(self) -> Dict:
        """Generate subnet plan"""
        if self.verbose:
            print(f"Planning subnets for VPC: {self.vpc_cidr}")
            print(f"Availability Zones: {self.azs}")
            print(f"Cloud Provider: {self.cloud.upper()}")
            print()

        # Calculate available space
        vpc_size = self.vpc_network.prefixlen
        total_ips = 2 ** (32 - vpc_size)

        # Calculate space to reserve
        reserved_ips = int(total_ips * self.reserve_future / 100) if self.reserve_future else 0

        # Determine subnet configuration
        if self.subnets:
            subnet_config = self.subnets
        else:
            subnet_config = self._get_tier_config()

        # Calculate subnets
        subnets = self._calculate_subnets(subnet_config)

        # Generate plan
        plan = {
            'vpc': {
                'cidr': self.vpc_cidr,
                'total_ips': total_ips,
                'usable_ips': total_ips - 2,  # Network and broadcast
                'reserved_for_future': reserved_ips,
            },
            'configuration': {
                'availability_zones': self.azs,
                'cloud_provider': self.cloud,
                'reserved_ips_per_subnet': self.RESERVED_IPS.get(self.cloud, 5),
            },
            'subnets': subnets,
            'summary': self._generate_summary(subnets, total_ips),
            'generated_at': datetime.now().isoformat()
        }

        return plan

    def _get_tier_config(self) -> Dict[str, int]:
        """Get default tier configuration"""
        if self.tiers == 3:
            return {
                'public': self.DEFAULT_SUBNET_SIZES['public'],
                'private': self.DEFAULT_SUBNET_SIZES['private'],
                'database': self.DEFAULT_SUBNET_SIZES['database'],
            }
        elif self.tiers == 2:
            return {
                'public': self.DEFAULT_SUBNET_SIZES['public'],
                'private': self.DEFAULT_SUBNET_SIZES['private'],
            }
        elif self.tiers == 4:
            return {
                'public': self.DEFAULT_SUBNET_SIZES['public'],
                'private': self.DEFAULT_SUBNET_SIZES['private'],
                'database': self.DEFAULT_SUBNET_SIZES['database'],
                'cache': self.DEFAULT_SUBNET_SIZES['cache'],
            }
        else:
            return {
                'default': 24,
            }

    def _calculate_subnets(self, config: Dict[str, int]) -> List[Dict]:
        """Calculate subnet allocations"""
        subnets = []
        reserved_per_subnet = self.RESERVED_IPS.get(self.cloud, 5)

        # Sort tiers by size (largest first for efficient allocation)
        sorted_tiers = sorted(config.items(), key=lambda x: x[1])

        # Calculate required bits for all subnets
        total_subnets_needed = len(config) * self.azs
        vpc_prefix = self.vpc_network.prefixlen

        # Start allocating from the beginning of the VPC
        current_offset = 0

        for tier_name, subnet_size in sorted_tiers:
            tier_subnets = []

            for az_num in range(self.azs):
                # Calculate subnet CIDR
                subnet_ips = 2 ** (32 - subnet_size)

                # Calculate the subnet network
                subnet_start = int(self.vpc_network.network_address) + current_offset
                subnet_network = ipaddress.ip_network(f"{ipaddress.ip_address(subnet_start)}/{subnet_size}", strict=False)

                # AZ naming (a, b, c, etc.)
                az_letter = chr(ord('a') + az_num)

                subnet_info = {
                    'name': f"{tier_name}-{az_letter}",
                    'tier': tier_name,
                    'availability_zone': f"az-{az_letter}",
                    'cidr': str(subnet_network),
                    'network_address': str(subnet_network.network_address),
                    'broadcast_address': str(subnet_network.broadcast_address),
                    'first_usable': str(subnet_network.network_address + reserved_per_subnet),
                    'last_usable': str(subnet_network.broadcast_address - 1),
                    'total_ips': subnet_ips,
                    'usable_ips': subnet_ips - reserved_per_subnet - 1,  # -1 for broadcast
                    'reserved_ips': reserved_per_subnet,
                }

                tier_subnets.append(subnet_info)
                current_offset += subnet_ips

            subnets.extend(tier_subnets)

        return subnets

    def _generate_summary(self, subnets: List[Dict], total_vpc_ips: int) -> Dict:
        """Generate allocation summary"""
        allocated_ips = sum(s['total_ips'] for s in subnets)
        usable_ips = sum(s['usable_ips'] for s in subnets)
        remaining_ips = total_vpc_ips - allocated_ips

        # Group by tier
        by_tier = {}
        for subnet in subnets:
            tier = subnet['tier']
            if tier not in by_tier:
                by_tier[tier] = {'count': 0, 'total_ips': 0, 'usable_ips': 0}
            by_tier[tier]['count'] += 1
            by_tier[tier]['total_ips'] += subnet['total_ips']
            by_tier[tier]['usable_ips'] += subnet['usable_ips']

        return {
            'total_subnets': len(subnets),
            'total_allocated_ips': allocated_ips,
            'total_usable_ips': usable_ips,
            'remaining_ips': remaining_ips,
            'utilization_percentage': round((allocated_ips / total_vpc_ips) * 100, 2),
            'by_tier': by_tier
        }

    def to_terraform(self) -> str:
        """Generate Terraform subnet configuration"""
        plan = self.plan()
        tf = f'''# Subnet Plan for VPC {plan['vpc']['cidr']}
# Generated: {plan['generated_at']}
# Cloud: {plan['configuration']['cloud_provider'].upper()}

locals {{
  vpc_cidr = "{plan['vpc']['cidr']}"
  azs      = {json.dumps([f"az-{chr(ord('a') + i)}" for i in range(self.azs)])}
}}

'''
        # Group subnets by tier
        by_tier = {}
        for subnet in plan['subnets']:
            tier = subnet['tier']
            if tier not in by_tier:
                by_tier[tier] = []
            by_tier[tier].append(subnet)

        for tier, tier_subnets in by_tier.items():
            tf += f'''# {tier.title()} Subnets
'''
            for i, subnet in enumerate(tier_subnets):
                resource_name = subnet['name'].replace('-', '_')
                tf += f'''resource "aws_subnet" "{resource_name}" {{
  vpc_id            = var.vpc_id
  cidr_block        = "{subnet['cidr']}"
  availability_zone = "${{var.region}}{subnet['availability_zone'].replace('az-', '')}"

  tags = {{
    Name        = "{subnet['name']}"
    Tier        = "{tier}"
    Environment = var.environment
    ManagedBy   = "terraform"
  }}
}}

'''

        tf += '''# Variables
variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# Outputs
'''
        for tier in by_tier.keys():
            tier_var = tier.replace('-', '_')
            tf += f'''output "{tier_var}_subnet_ids" {{
  value = [
'''
            for subnet in by_tier[tier]:
                resource_name = subnet['name'].replace('-', '_')
                tf += f'    aws_subnet.{resource_name}.id,\n'
            tf += '''  ]
}

'''

        return tf

    def to_csv(self) -> str:
        """Generate CSV inventory"""
        plan = self.plan()
        csv_lines = ['Name,Tier,AZ,CIDR,Network Address,First Usable,Last Usable,Total IPs,Usable IPs']

        for subnet in plan['subnets']:
            csv_lines.append(
                f"{subnet['name']},{subnet['tier']},{subnet['availability_zone']},"
                f"{subnet['cidr']},{subnet['network_address']},{subnet['first_usable']},"
                f"{subnet['last_usable']},{subnet['total_ips']},{subnet['usable_ips']}"
            )

        return '\n'.join(csv_lines)


def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="Subnet Planner - Calculate CIDR allocations and plan subnet layouts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python subnet_planner.py --vpc-cidr 10.0.0.0/16 --azs 3 --tiers 3
  python subnet_planner.py --vpc-cidr 172.16.0.0/12 --subnets public:24,private:22,database:26
  python subnet_planner.py --vpc-cidr 10.0.0.0/16 --inventory --output csv

Part of senior-network-infrastructure skill.
"""
    )

    parser.add_argument(
        '--vpc-cidr',
        required=True,
        help='VPC CIDR block (e.g., 10.0.0.0/16)'
    )

    parser.add_argument(
        '--azs',
        type=int,
        default=3,
        help='Number of availability zones (default: 3)'
    )

    parser.add_argument(
        '--tiers',
        type=int,
        default=3,
        choices=[1, 2, 3, 4],
        help='Number of tiers (default: 3 = public, private, database)'
    )

    parser.add_argument(
        '--subnets',
        help='Custom subnet specification (e.g., "public:24,private:22,db:26")'
    )

    parser.add_argument(
        '--reserve-future',
        type=int,
        default=0,
        help='Percentage of space to reserve for future use (default: 0)'
    )

    parser.add_argument(
        '--cloud',
        choices=['aws', 'azure', 'gcp'],
        default='aws',
        help='Cloud provider for reserved IP calculation (default: aws)'
    )

    parser.add_argument(
        '--inventory',
        action='store_true',
        help='Generate IP inventory'
    )

    parser.add_argument(
        '-o', '--output',
        choices=['json', 'text', 'terraform', 'csv'],
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
        version='Subnet Planner v1.0.0'
    )

    args = parser.parse_args()

    # Validate CIDR
    try:
        ipaddress.ip_network(args.vpc_cidr, strict=False)
    except ValueError as e:
        print(f"Error: Invalid CIDR block: {e}", file=sys.stderr)
        sys.exit(1)

    # Create planner
    planner = SubnetPlanner(
        vpc_cidr=args.vpc_cidr,
        azs=args.azs,
        tiers=args.tiers,
        subnets=args.subnets,
        reserve_future=args.reserve_future,
        cloud=args.cloud,
        verbose=args.verbose
    )

    # Generate output
    if args.output == 'terraform':
        output = planner.to_terraform()
    elif args.output == 'csv':
        output = planner.to_csv()
    elif args.output == 'json':
        plan = planner.plan()
        output = json.dumps(plan, indent=2)
    else:  # text
        plan = planner.plan()
        output = f"""
Subnet Plan
{'=' * 60}
VPC CIDR:         {plan['vpc']['cidr']}
Total IPs:        {plan['vpc']['total_ips']:,}
Usable IPs:       {plan['vpc']['usable_ips']:,}
Cloud Provider:   {plan['configuration']['cloud_provider'].upper()}
Reserved/Subnet:  {plan['configuration']['reserved_ips_per_subnet']} IPs

Configuration
{'-' * 60}
Availability Zones: {plan['configuration']['availability_zones']}
Total Subnets:      {plan['summary']['total_subnets']}

Allocation Summary
{'-' * 60}
Allocated IPs:      {plan['summary']['total_allocated_ips']:,}
Usable IPs:         {plan['summary']['total_usable_ips']:,}
Remaining IPs:      {plan['summary']['remaining_ips']:,}
Utilization:        {plan['summary']['utilization_percentage']}%

By Tier:
"""
        for tier, stats in plan['summary']['by_tier'].items():
            output += f"  {tier.title()}: {stats['count']} subnets, {stats['usable_ips']:,} usable IPs\n"

        output += f"""
Subnet Details
{'-' * 60}
"""
        # Group by tier for display
        current_tier = None
        for subnet in plan['subnets']:
            if subnet['tier'] != current_tier:
                current_tier = subnet['tier']
                output += f"\n{current_tier.upper()} TIER:\n"

            output += f"""  {subnet['name']}:
    CIDR:         {subnet['cidr']}
    AZ:           {subnet['availability_zone']}
    Usable Range: {subnet['first_usable']} - {subnet['last_usable']}
    Usable IPs:   {subnet['usable_ips']:,}
"""

        output += f"""
Generated: {plan['generated_at']}

Use --output terraform for Terraform configuration
Use --output csv for IP inventory spreadsheet
"""

    # Output results
    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Plan saved to: {args.file}")
    else:
        print(output)


if __name__ == "__main__":
    main()
