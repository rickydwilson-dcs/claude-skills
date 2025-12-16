#!/usr/bin/env python3
"""
Network Topology Analyzer

Analyze network configurations for redundancy, security, and best practices.
Supports AWS VPC, Azure VNet, and GCP VPC configurations.

Part of senior-network-infrastructure skill for engineering-team.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class NetworkTopologyAnalyzer:
    """Analyze network topology for issues and best practices"""

    # Best practice rules
    BEST_PRACTICES = {
        'redundancy': [
            {'id': 'R001', 'name': 'Multi-AZ Subnets', 'description': 'Subnets should span multiple availability zones', 'severity': 'high'},
            {'id': 'R002', 'name': 'NAT Gateway Redundancy', 'description': 'NAT Gateways should be in each AZ', 'severity': 'high'},
            {'id': 'R003', 'name': 'Load Balancer Health Checks', 'description': 'Load balancers should have health checks configured', 'severity': 'medium'},
            {'id': 'R004', 'name': 'Route Table Redundancy', 'description': 'Private subnets should have failover routes', 'severity': 'medium'},
        ],
        'security': [
            {'id': 'S001', 'name': 'No 0.0.0.0/0 to Database', 'description': 'Database subnets should not allow internet access', 'severity': 'critical'},
            {'id': 'S002', 'name': 'VPC Flow Logs', 'description': 'VPC Flow Logs should be enabled', 'severity': 'high'},
            {'id': 'S003', 'name': 'Default Security Group', 'description': 'Default security group should have no rules', 'severity': 'medium'},
            {'id': 'S004', 'name': 'SSH/RDP Restricted', 'description': 'SSH (22) and RDP (3389) should not be open to 0.0.0.0/0', 'severity': 'critical'},
            {'id': 'S005', 'name': 'Private Subnet for Databases', 'description': 'Databases should be in private subnets', 'severity': 'high'},
            {'id': 'S006', 'name': 'Encryption in Transit', 'description': 'TLS should be enabled for all public endpoints', 'severity': 'high'},
        ],
        'cost': [
            {'id': 'C001', 'name': 'NAT Gateway Optimization', 'description': 'Consider VPC endpoints to reduce NAT costs', 'severity': 'low'},
            {'id': 'C002', 'name': 'Unused Elastic IPs', 'description': 'Release unused Elastic IPs', 'severity': 'low'},
            {'id': 'C003', 'name': 'Cross-AZ Traffic', 'description': 'Minimize cross-AZ data transfer', 'severity': 'medium'},
        ],
        'compliance': {
            'pci-dss': [
                {'id': 'P001', 'name': 'Cardholder Data Isolation', 'description': 'CDE must be isolated from public networks'},
                {'id': 'P002', 'name': 'Deny All Default', 'description': 'Default deny all, explicit allow required'},
                {'id': 'P003', 'name': 'Audit Logging', 'description': 'All network access must be logged'},
            ],
            'hipaa': [
                {'id': 'H001', 'name': 'PHI Encryption', 'description': 'PHI must be encrypted in transit'},
                {'id': 'H002', 'name': 'Access Controls', 'description': 'Network access to PHI systems must be controlled'},
            ],
            'soc2': [
                {'id': 'T001', 'name': 'Logical Access', 'description': 'Logical access controls must be implemented'},
                {'id': 'T002', 'name': 'Change Management', 'description': 'Network changes must follow change management'},
            ]
        }
    }

    def __init__(self, input_path: str, check_redundancy: bool = False,
                 security_audit: bool = False, compliance: str = None,
                 verbose: bool = False):
        """
        Initialize Network Topology Analyzer

        Args:
            input_path: Path to network configuration file or directory
            check_redundancy: Run redundancy checks
            security_audit: Run security audit
            compliance: Compliance framework to check (pci-dss, hipaa, soc2)
            verbose: Enable verbose output
        """
        self.input_path = Path(input_path)
        self.check_redundancy = check_redundancy
        self.security_audit = security_audit
        self.compliance = compliance
        self.verbose = verbose
        self.findings = []
        self.network_config = {}

    def analyze(self) -> Dict:
        """Run network topology analysis"""
        if self.verbose:
            print(f"Analyzing network configuration: {self.input_path}")
            print()

        # Load configuration
        self._load_config()

        # Run checks
        results = {
            'analyzed_at': datetime.now().isoformat(),
            'input_path': str(self.input_path),
            'summary': {},
            'findings': [],
            'recommendations': []
        }

        if self.check_redundancy or not self.security_audit:
            redundancy_findings = self._check_redundancy()
            results['findings'].extend(redundancy_findings)

        if self.security_audit or not self.check_redundancy:
            security_findings = self._check_security()
            results['findings'].extend(security_findings)

        if self.compliance:
            compliance_findings = self._check_compliance()
            results['findings'].extend(compliance_findings)

        # Generate summary
        results['summary'] = self._generate_summary(results['findings'])

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results['findings'])

        return results

    def _load_config(self):
        """Load network configuration from file or directory"""
        if self.input_path.is_file():
            try:
                with open(self.input_path) as f:
                    self.network_config = json.load(f)
            except json.JSONDecodeError:
                # Try to parse as text-based config
                self.network_config = self._parse_text_config()
        elif self.input_path.is_dir():
            # Load all JSON files in directory
            self.network_config = {'files': {}}
            for json_file in self.input_path.glob('**/*.json'):
                try:
                    with open(json_file) as f:
                        self.network_config['files'][str(json_file)] = json.load(f)
                except Exception:
                    pass
        else:
            # Create sample config for demonstration
            self.network_config = self._create_sample_config()

    def _parse_text_config(self) -> Dict:
        """Parse text-based configuration"""
        return {'type': 'text', 'content': self.input_path.read_text()}

    def _create_sample_config(self) -> Dict:
        """Create sample configuration for analysis demonstration"""
        return {
            'vpc': {
                'cidr': '10.0.0.0/16',
                'name': 'main-vpc',
                'flow_logs_enabled': False,
            },
            'subnets': [
                {'name': 'public-1a', 'cidr': '10.0.1.0/24', 'az': 'us-east-1a', 'type': 'public'},
                {'name': 'public-1b', 'cidr': '10.0.2.0/24', 'az': 'us-east-1b', 'type': 'public'},
                {'name': 'private-1a', 'cidr': '10.0.10.0/24', 'az': 'us-east-1a', 'type': 'private'},
                {'name': 'private-1b', 'cidr': '10.0.11.0/24', 'az': 'us-east-1b', 'type': 'private'},
                {'name': 'database-1a', 'cidr': '10.0.20.0/24', 'az': 'us-east-1a', 'type': 'database'},
            ],
            'security_groups': [
                {
                    'name': 'sg-web',
                    'rules': [
                        {'port': 80, 'source': '0.0.0.0/0'},
                        {'port': 443, 'source': '0.0.0.0/0'},
                        {'port': 22, 'source': '0.0.0.0/0'},  # Issue: SSH open to world
                    ]
                },
                {
                    'name': 'sg-db',
                    'rules': [
                        {'port': 5432, 'source': '10.0.0.0/16'},
                    ]
                }
            ],
            'nat_gateways': [
                {'name': 'nat-1a', 'az': 'us-east-1a'}
            ],  # Issue: Only one NAT gateway
        }

    def _check_redundancy(self) -> List[Dict]:
        """Check for redundancy issues"""
        findings = []

        config = self.network_config

        # Check Multi-AZ subnets
        if 'subnets' in config:
            azs = set()
            for subnet in config['subnets']:
                if 'az' in subnet:
                    azs.add(subnet['az'])

            if len(azs) < 2:
                findings.append({
                    'rule_id': 'R001',
                    'severity': 'high',
                    'category': 'redundancy',
                    'title': 'Single Availability Zone',
                    'description': f'Subnets only span {len(azs)} AZ(s). For high availability, use at least 2 AZs.',
                    'affected_resources': [s['name'] for s in config['subnets']],
                    'remediation': 'Create subnets in additional availability zones'
                })

        # Check NAT Gateway redundancy
        if 'nat_gateways' in config:
            nat_azs = set()
            for nat in config['nat_gateways']:
                if 'az' in nat:
                    nat_azs.add(nat['az'])

            if len(nat_azs) < 2:
                findings.append({
                    'rule_id': 'R002',
                    'severity': 'high',
                    'category': 'redundancy',
                    'title': 'NAT Gateway Not Redundant',
                    'description': f'NAT Gateways only in {len(nat_azs)} AZ(s). Single point of failure for private subnet internet access.',
                    'affected_resources': [n['name'] for n in config['nat_gateways']],
                    'remediation': 'Deploy NAT Gateway in each availability zone with private subnets'
                })

        # Check for database subnet redundancy
        if 'subnets' in config:
            db_subnets = [s for s in config['subnets'] if s.get('type') == 'database']
            db_azs = set(s.get('az') for s in db_subnets if s.get('az'))

            if len(db_subnets) > 0 and len(db_azs) < 2:
                findings.append({
                    'rule_id': 'R004',
                    'severity': 'medium',
                    'category': 'redundancy',
                    'title': 'Database Subnets Not Multi-AZ',
                    'description': 'Database subnets should span multiple AZs for RDS Multi-AZ deployments.',
                    'affected_resources': [s['name'] for s in db_subnets],
                    'remediation': 'Create database subnets in at least 2 availability zones'
                })

        return findings

    def _check_security(self) -> List[Dict]:
        """Check for security issues"""
        findings = []

        config = self.network_config

        # Check VPC Flow Logs
        if 'vpc' in config:
            if not config['vpc'].get('flow_logs_enabled', False):
                findings.append({
                    'rule_id': 'S002',
                    'severity': 'high',
                    'category': 'security',
                    'title': 'VPC Flow Logs Disabled',
                    'description': 'VPC Flow Logs are not enabled. Network traffic cannot be monitored or audited.',
                    'affected_resources': [config['vpc'].get('name', 'vpc')],
                    'remediation': 'Enable VPC Flow Logs with CloudWatch or S3 destination'
                })

        # Check security group rules
        if 'security_groups' in config:
            for sg in config['security_groups']:
                for rule in sg.get('rules', []):
                    port = rule.get('port')
                    source = rule.get('source', '')

                    # Check SSH/RDP open to world
                    if port in [22, 3389] and source == '0.0.0.0/0':
                        findings.append({
                            'rule_id': 'S004',
                            'severity': 'critical',
                            'category': 'security',
                            'title': f'{"SSH" if port == 22 else "RDP"} Open to Internet',
                            'description': f'Port {port} is accessible from 0.0.0.0/0. This is a critical security risk.',
                            'affected_resources': [sg['name']],
                            'remediation': f'Restrict port {port} to specific IP ranges or use a bastion host/VPN'
                        })

                    # Check database ports open to wide ranges
                    if port in [3306, 5432, 27017, 6379] and source == '0.0.0.0/0':
                        findings.append({
                            'rule_id': 'S001',
                            'severity': 'critical',
                            'category': 'security',
                            'title': 'Database Port Open to Internet',
                            'description': f'Database port {port} is accessible from the internet.',
                            'affected_resources': [sg['name']],
                            'remediation': 'Restrict database access to application subnets only'
                        })

        # Check for private subnets for databases
        if 'subnets' in config:
            db_subnets = [s for s in config['subnets'] if s.get('type') == 'database']
            public_db_subnets = [s for s in db_subnets if s.get('type') == 'public']

            if public_db_subnets:
                findings.append({
                    'rule_id': 'S005',
                    'severity': 'high',
                    'category': 'security',
                    'title': 'Database in Public Subnet',
                    'description': 'Database subnets should be private (no direct internet access).',
                    'affected_resources': [s['name'] for s in public_db_subnets],
                    'remediation': 'Move databases to private subnets with NAT Gateway for outbound'
                })

        return findings

    def _check_compliance(self) -> List[Dict]:
        """Check compliance with specified framework"""
        findings = []

        if not self.compliance:
            return findings

        framework_rules = self.BEST_PRACTICES['compliance'].get(self.compliance, [])

        for rule in framework_rules:
            # Simplified compliance checking - in production, these would be detailed checks
            findings.append({
                'rule_id': rule['id'],
                'severity': 'medium',
                'category': 'compliance',
                'title': rule['name'],
                'description': rule['description'],
                'affected_resources': ['Review Required'],
                'remediation': f'Verify compliance with {self.compliance.upper()} requirement: {rule["name"]}'
            })

        return findings

    def _generate_summary(self, findings: List[Dict]) -> Dict:
        """Generate analysis summary"""
        summary = {
            'total_findings': len(findings),
            'by_severity': {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            },
            'by_category': {
                'redundancy': 0,
                'security': 0,
                'cost': 0,
                'compliance': 0
            }
        }

        for finding in findings:
            severity = finding.get('severity', 'medium')
            category = finding.get('category', 'other')

            if severity in summary['by_severity']:
                summary['by_severity'][severity] += 1
            if category in summary['by_category']:
                summary['by_category'][category] += 1

        # Calculate risk score (0-100)
        risk_score = (
            summary['by_severity']['critical'] * 25 +
            summary['by_severity']['high'] * 15 +
            summary['by_severity']['medium'] * 5 +
            summary['by_severity']['low'] * 1
        )
        summary['risk_score'] = min(100, risk_score)

        # Risk level
        if summary['risk_score'] >= 50:
            summary['risk_level'] = 'HIGH'
        elif summary['risk_score'] >= 25:
            summary['risk_level'] = 'MEDIUM'
        else:
            summary['risk_level'] = 'LOW'

        return summary

    def _generate_recommendations(self, findings: List[Dict]) -> List[str]:
        """Generate prioritized recommendations"""
        recommendations = []

        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_findings = sorted(findings, key=lambda x: severity_order.get(x.get('severity', 'low'), 4))

        for finding in sorted_findings[:5]:  # Top 5 recommendations
            recommendations.append(f"[{finding['severity'].upper()}] {finding['title']}: {finding['remediation']}")

        return recommendations


def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="Network Topology Analyzer - Analyze network configurations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python network_topology_analyzer.py --input vpc-config.json --check-redundancy
  python network_topology_analyzer.py --input network/ --security-audit
  python network_topology_analyzer.py --input infra.json --compliance pci-dss --output report.md

Part of senior-network-infrastructure skill.
"""
    )

    parser.add_argument(
        '--input',
        required=True,
        help='Path to network configuration file or directory'
    )

    parser.add_argument(
        '--check-redundancy',
        action='store_true',
        help='Run redundancy checks'
    )

    parser.add_argument(
        '--security-audit',
        action='store_true',
        help='Run security audit'
    )

    parser.add_argument(
        '--compliance',
        choices=['pci-dss', 'hipaa', 'soc2'],
        help='Compliance framework to check'
    )

    parser.add_argument(
        '-o', '--output',
        choices=['json', 'text', 'markdown'],
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
        version='Network Topology Analyzer v1.0.0'
    )

    args = parser.parse_args()

    # Create analyzer
    analyzer = NetworkTopologyAnalyzer(
        input_path=args.input,
        check_redundancy=args.check_redundancy,
        security_audit=args.security_audit,
        compliance=args.compliance,
        verbose=args.verbose
    )

    # Run analysis
    results = analyzer.analyze()

    # Format output
    if args.output == 'json':
        output = json.dumps(results, indent=2)
    elif args.output == 'markdown':
        output = f"""# Network Topology Analysis Report

**Analyzed:** {results['analyzed_at']}
**Input:** {results['input_path']}

## Summary

| Metric | Value |
|--------|-------|
| Total Findings | {results['summary']['total_findings']} |
| Risk Score | {results['summary']['risk_score']}/100 |
| Risk Level | {results['summary']['risk_level']} |

### Findings by Severity

| Severity | Count |
|----------|-------|
| Critical | {results['summary']['by_severity']['critical']} |
| High | {results['summary']['by_severity']['high']} |
| Medium | {results['summary']['by_severity']['medium']} |
| Low | {results['summary']['by_severity']['low']} |

## Findings

"""
        for finding in results['findings']:
            output += f"""### [{finding['severity'].upper()}] {finding['title']}

- **Rule ID:** {finding['rule_id']}
- **Category:** {finding['category']}
- **Description:** {finding['description']}
- **Affected Resources:** {', '.join(finding['affected_resources'])}
- **Remediation:** {finding['remediation']}

"""
        output += """## Top Recommendations

"""
        for i, rec in enumerate(results['recommendations'], 1):
            output += f"{i}. {rec}\n"

    else:  # text
        output = f"""
Network Topology Analysis Report
{'=' * 50}
Analyzed: {results['analyzed_at']}
Input:    {results['input_path']}

Summary
{'-' * 50}
Total Findings: {results['summary']['total_findings']}
Risk Score:     {results['summary']['risk_score']}/100
Risk Level:     {results['summary']['risk_level']}

By Severity:
  Critical: {results['summary']['by_severity']['critical']}
  High:     {results['summary']['by_severity']['high']}
  Medium:   {results['summary']['by_severity']['medium']}
  Low:      {results['summary']['by_severity']['low']}

Findings
{'-' * 50}
"""
        for finding in results['findings']:
            output += f"""
[{finding['severity'].upper()}] {finding['title']}
  Rule ID:    {finding['rule_id']}
  Category:   {finding['category']}
  Description: {finding['description']}
  Affected:   {', '.join(finding['affected_resources'])}
  Remediation: {finding['remediation']}
"""

        output += f"""
Top Recommendations
{'-' * 50}
"""
        for i, rec in enumerate(results['recommendations'], 1):
            output += f"{i}. {rec}\n"

    # Output results
    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Report saved to: {args.file}")
    else:
        print(output)


if __name__ == "__main__":
    main()
