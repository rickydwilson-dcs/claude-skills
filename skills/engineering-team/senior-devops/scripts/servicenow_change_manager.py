#!/usr/bin/env python3
"""
ServiceNow Change Manager

Generate ServiceNow change request payloads from deployment configurations.
Links deployments to change tickets for audit compliance and ITIL workflows.

Features:
- Generate standard, normal, and emergency change requests
- Link deployments to CMDB Configuration Items
- Include rollback plans as backout instructions
- Support CAB approval workflow metadata
- Output curl commands for testing

Usage:
    python servicenow_change_manager.py --deployment-file deploy.json --change-type normal
    python servicenow_change_manager.py --service payment-api --version 2.3.1 --output curl
    python servicenow_change_manager.py --help

Author: Claude Skills Team
Version: 1.0.0
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List

# Version info
__version__ = "1.0.0"

# Change request types
CHANGE_TYPES = {
    'standard': 'Standard',
    'normal': 'Normal',
    'emergency': 'Emergency',
}

# Change states
CHANGE_STATES = {
    'new': -5,
    'assess': -4,
    'authorize': -3,
    'scheduled': -2,
    'implement': -1,
    'review': 0,
    'closed': 3,
    'canceled': 4,
}

# Risk levels
RISK_LEVELS = {
    'low': 4,
    'moderate': 3,
    'high': 2,
    'very_high': 1,
}

# Impact levels
IMPACT_LEVELS = {
    'low': 3,
    'medium': 2,
    'high': 1,
}

# Change categories
CHANGE_CATEGORIES = {
    'deployment': 'Software',
    'infrastructure': 'Hardware',
    'configuration': 'Configuration',
    'database': 'Database',
    'network': 'Network',
    'security': 'Security',
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if config_path is None:
        script_dir = Path(__file__).parent.parent
        # Check both incident-response and devops config locations
        possible_paths = [
            script_dir / "assets" / "servicenow-config.yaml",
            script_dir.parent / "incident-response" / "assets" / "servicenow-config.yaml",
            Path.cwd() / "servicenow-config.yaml",
        ]
        for path in possible_paths:
            if path.exists():
                config_path = str(path)
                break

    if config_path and Path(config_path).exists():
        try:
            return parse_simple_yaml(config_path)
        except Exception as e:
            print(f"Warning: Could not load config: {e}", file=sys.stderr)

    return {}


def parse_simple_yaml(file_path: str) -> Dict[str, Any]:
    """Simple YAML parser for basic config files."""
    config = {}
    current_section = None
    current_subsection = None

    with open(file_path, 'r') as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            indent = len(line) - len(line.lstrip())

            if ':' in stripped:
                key, _, value = stripped.partition(':')
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                if indent == 0:
                    current_section = key
                    current_subsection = None
                    config[key] = {} if not value else value
                elif indent == 2 and current_section:
                    current_subsection = key
                    if isinstance(config.get(current_section), dict):
                        if value.lower() == 'true':
                            value = True
                        elif value.lower() == 'false':
                            value = False
                        elif value.isdigit():
                            value = int(value)
                        config[current_section][key] = value if value else {}
                elif indent == 4 and current_section and current_subsection:
                    if isinstance(config.get(current_section), dict):
                        if isinstance(config[current_section].get(current_subsection), dict):
                            config[current_section][current_subsection][key] = value

    return config


def load_deployment_file(file_path: str) -> Dict[str, Any]:
    """Load deployment configuration from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def parse_deployment_config(deployment_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse deployment configuration into standardized format."""
    return {
        'service_name': deployment_data.get('service', deployment_data.get('name', 'unknown-service')),
        'version': deployment_data.get('version', deployment_data.get('tag', 'latest')),
        'environment': deployment_data.get('environment', deployment_data.get('env', 'production')),
        'strategy': deployment_data.get('strategy', deployment_data.get('deployment_strategy', 'rolling')),
        'replicas': deployment_data.get('replicas', deployment_data.get('scale', 1)),
        'namespace': deployment_data.get('namespace', 'default'),
        'cluster': deployment_data.get('cluster', ''),
        'image': deployment_data.get('image', ''),
        'changes': deployment_data.get('changes', deployment_data.get('changelog', [])),
        'rollback': deployment_data.get('rollback', deployment_data.get('rollback_plan', {})),
        'health_checks': deployment_data.get('health_checks', []),
        'ci_names': deployment_data.get('ci_names', deployment_data.get('affected_cis', [])),
        'owner': deployment_data.get('owner', deployment_data.get('deployed_by', '')),
        'jira_tickets': deployment_data.get('jira_tickets', deployment_data.get('tickets', [])),
    }


def calculate_risk_level(
    deployment: Dict[str, Any],
    change_type: str,
) -> str:
    """Calculate risk level based on deployment characteristics."""
    # Emergency changes are always high risk
    if change_type == 'emergency':
        return 'high'

    risk_score = 0

    # Production environment increases risk
    if deployment['environment'].lower() in ['production', 'prod', 'prd']:
        risk_score += 2

    # Large replica count increases risk
    if deployment['replicas'] > 5:
        risk_score += 1

    # Non-rolling strategy increases risk
    if deployment['strategy'].lower() in ['recreate', 'replace']:
        risk_score += 1

    # Database changes are higher risk
    if 'database' in deployment['service_name'].lower() or 'db' in deployment['service_name'].lower():
        risk_score += 2

    # Map score to risk level
    if risk_score >= 4:
        return 'high'
    elif risk_score >= 2:
        return 'moderate'
    else:
        return 'low'


def calculate_impact(deployment: Dict[str, Any]) -> str:
    """Calculate impact level based on deployment scope."""
    # Check for critical services
    critical_keywords = ['payment', 'auth', 'checkout', 'core', 'gateway', 'api']
    service_lower = deployment['service_name'].lower()

    if any(kw in service_lower for kw in critical_keywords):
        return 'high'

    # Check replica count as proxy for importance
    if deployment['replicas'] > 10:
        return 'high'
    elif deployment['replicas'] > 3:
        return 'medium'

    return 'low'


def build_change_description(deployment: Dict[str, Any]) -> str:
    """Build formatted change request description."""
    lines = [
        "Deployment Details:",
        "=" * 40,
        f"Service: {deployment['service_name']}",
        f"Version: {deployment['version']}",
        f"Environment: {deployment['environment']}",
        f"Strategy: {deployment['strategy']}",
        f"Replicas: {deployment['replicas']}",
    ]

    if deployment.get('namespace'):
        lines.append(f"Namespace: {deployment['namespace']}")

    if deployment.get('cluster'):
        lines.append(f"Cluster: {deployment['cluster']}")

    if deployment.get('image'):
        lines.append(f"Image: {deployment['image']}")

    if deployment.get('changes'):
        lines.extend(["", "Changes Included:", "-" * 20])
        for change in deployment['changes'][:10]:  # Limit to 10 items
            if isinstance(change, str):
                lines.append(f"  - {change}")
            elif isinstance(change, dict):
                lines.append(f"  - {change.get('description', change.get('message', str(change)))}")

    if deployment.get('jira_tickets'):
        lines.extend(["", "Related Tickets:", "-" * 20])
        for ticket in deployment['jira_tickets']:
            lines.append(f"  - {ticket}")

    return '\n'.join(lines)


def build_backout_plan(deployment: Dict[str, Any]) -> str:
    """Build rollback/backout plan from deployment config."""
    rollback = deployment.get('rollback', {})

    if isinstance(rollback, str):
        return rollback

    lines = [
        "Rollback Plan:",
        "=" * 40,
    ]

    # Default rollback steps based on strategy
    strategy = deployment['strategy'].lower()

    if strategy in ['rolling', 'rollingupdate']:
        lines.extend([
            "1. Execute: kubectl rollout undo deployment/{service}",
            "2. Verify: kubectl rollout status deployment/{service}",
            "3. Monitor: Check service health endpoints",
            "4. Validate: Confirm previous version running",
        ])
    elif strategy in ['blue-green', 'bluegreen']:
        lines.extend([
            "1. Switch traffic: Update service selector to blue/green",
            "2. Verify: Check traffic routing",
            "3. Cleanup: Remove failed deployment",
            "4. Validate: Confirm service restored",
        ])
    elif strategy == 'canary':
        lines.extend([
            "1. Scale down: Set canary replicas to 0",
            "2. Verify: Confirm canary pods terminated",
            "3. Restore: Scale up stable deployment",
            "4. Validate: Check service health",
        ])
    else:
        lines.extend([
            "1. Revert: Deploy previous version",
            "2. Verify: Check deployment status",
            "3. Monitor: Validate service health",
            "4. Notify: Inform stakeholders",
        ])

    # Add custom rollback info if provided
    if rollback.get('commands'):
        lines.extend(["", "Custom Rollback Commands:", "-" * 20])
        for cmd in rollback['commands']:
            lines.append(f"  $ {cmd}")

    if rollback.get('previous_version'):
        lines.append(f"\nPrevious Version: {rollback['previous_version']}")

    if rollback.get('estimated_time'):
        lines.append(f"Estimated Rollback Time: {rollback['estimated_time']}")

    # Replace placeholders
    result = '\n'.join(lines)
    result = result.replace('{service}', deployment['service_name'])

    return result


def build_test_plan(deployment: Dict[str, Any]) -> str:
    """Build test plan for change validation."""
    lines = [
        "Test Plan:",
        "=" * 40,
        "",
        "Pre-Implementation Tests:",
        "  [ ] Verify deployment configuration",
        "  [ ] Confirm CI pipeline passed",
        "  [ ] Check target environment status",
        "",
        "Implementation Tests:",
        "  [ ] Verify pods/containers started",
        "  [ ] Check resource utilization",
        "  [ ] Validate service connectivity",
        "",
        "Post-Implementation Tests:",
    ]

    # Add health check tests
    if deployment.get('health_checks'):
        for check in deployment['health_checks']:
            if isinstance(check, str):
                lines.append(f"  [ ] {check}")
            elif isinstance(check, dict):
                lines.append(f"  [ ] {check.get('name', 'Health check')}: {check.get('endpoint', '')}")
    else:
        lines.extend([
            f"  [ ] Verify /{deployment['service_name']}/health endpoint",
            "  [ ] Check application logs for errors",
            "  [ ] Validate API responses",
            "  [ ] Confirm metrics collection",
        ])

    return '\n'.join(lines)


def generate_change_payload(
    deployment: Dict[str, Any],
    change_type: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    assignment_group: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Generate ServiceNow change request payload."""
    config = config or {}
    change_config = config.get('servicenow', {}).get('change_management', {})
    custom_fields = config.get('servicenow', {}).get('custom_fields', {})

    # Calculate times if not provided
    if start_time is None:
        start_time = datetime.utcnow() + timedelta(hours=1)
    if end_time is None:
        end_time = start_time + timedelta(hours=2)

    # Calculate risk and impact
    risk = calculate_risk_level(deployment, change_type)
    impact = calculate_impact(deployment)

    # Build payload
    payload = {
        'short_description': f"Deployment: {deployment['service_name']} v{deployment['version']}",
        'description': build_change_description(deployment),
        'type': CHANGE_TYPES.get(change_type, 'Normal'),
        'category': CHANGE_CATEGORIES.get('deployment', 'Software'),
        'risk': RISK_LEVELS.get(risk, 3),
        'impact': IMPACT_LEVELS.get(impact, 2),
        'start_date': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_date': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'assignment_group': assignment_group or change_config.get('assignment_group', 'Change Management'),
        'backout_plan': build_backout_plan(deployment),
        'test_plan': build_test_plan(deployment),
        'justification': f"Deploy {deployment['service_name']} version {deployment['version']} to {deployment['environment']}",
    }

    # Add CI references
    if deployment.get('ci_names'):
        # ServiceNow typically takes first CI as primary
        payload['cmdb_ci'] = deployment['ci_names'][0] if isinstance(deployment['ci_names'], list) else deployment['ci_names']
    else:
        payload['cmdb_ci'] = deployment['service_name']

    # Add custom fields
    for field, value in custom_fields.items():
        payload[field] = value

    # Add correlation ID
    payload['correlation_id'] = f"deploy-{deployment['service_name']}-{deployment['version']}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    # Add owner/requested by
    if deployment.get('owner'):
        payload['requested_by'] = deployment['owner']

    # For emergency changes, add expedited flag
    if change_type == 'emergency':
        payload['reason'] = 'Emergency deployment required'
        payload['expedite'] = True

    return payload


def format_as_curl(
    payload: Dict[str, Any],
    config: Dict[str, Any],
) -> str:
    """Format payload as curl command."""
    instance_url = config.get('servicenow', {}).get('instance_url', 'https://your-instance.service-now.com')

    curl_cmd = f'''curl -X POST "{instance_url}/api/now/table/change_request" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  -H "Authorization: Basic $(echo -n "$SNOW_USERNAME:$SNOW_PASSWORD" | base64)" \\
  -d '{json.dumps(payload, indent=2)}'
'''
    return curl_cmd


def format_output(
    payload: Dict[str, Any],
    output_format: str,
    config: Dict[str, Any],
) -> str:
    """Format output based on requested format."""
    if output_format == 'json':
        return json.dumps(payload, indent=2)
    elif output_format == 'curl':
        return format_as_curl(payload, config)
    elif output_format == 'text':
        lines = [
            "ServiceNow Change Request Payload",
            "=" * 50,
        ]
        for key, value in payload.items():
            if key in ['description', 'backout_plan', 'test_plan']:
                lines.extend([f"\n{key}:", "-" * 30, str(value), "-" * 30])
            else:
                lines.append(f"{key}: {value}")
        return '\n'.join(lines)
    else:
        return json.dumps(payload, indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate ServiceNow change request payloads from deployments',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # From deployment file
  python servicenow_change_manager.py --deployment-file deploy.json --change-type normal

  # Manual change request
  python servicenow_change_manager.py --service payment-api --version 2.3.1 \\
    --environment production --change-type normal --output curl

  # Emergency change
  python servicenow_change_manager.py --deployment-file deploy.json \\
    --change-type emergency --output json

  # With custom timing
  python servicenow_change_manager.py --deployment-file deploy.json \\
    --start-time "2024-01-15 10:00:00" --end-time "2024-01-15 12:00:00"

  # Output to file
  python servicenow_change_manager.py --deployment-file deploy.json \\
    --output json --file change-request.json
'''
    )

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    # Input options
    input_group = parser.add_argument_group('Input Options')
    input_group.add_argument('--deployment-file', '-d', help='Path to deployment config JSON')
    input_group.add_argument('--service', '-s', help='Service name (manual mode)')
    input_group.add_argument('--service-version', dest='version', help='Service version')
    input_group.add_argument('--environment', '-e', default='production', help='Target environment')
    input_group.add_argument('--strategy', default='rolling',
                            choices=['rolling', 'blue-green', 'canary', 'recreate'],
                            help='Deployment strategy')

    # Change options
    change_group = parser.add_argument_group('Change Options')
    change_group.add_argument('--change-type', '-t', required=True,
                             choices=['standard', 'normal', 'emergency'],
                             help='Change request type')
    change_group.add_argument('--start-time', help='Planned start time (YYYY-MM-DD HH:MM:SS)')
    change_group.add_argument('--end-time', help='Planned end time (YYYY-MM-DD HH:MM:SS)')
    change_group.add_argument('--assignment-group', '-g', help='Assignment group')
    change_group.add_argument('--ci-names', help='Comma-separated CI names')

    # Configuration
    parser.add_argument('--config', help='Path to servicenow-config.yaml')

    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('--output', '-o',
                             choices=['json', 'text', 'curl'],
                             default='json',
                             help='Output format (default: json)')
    output_group.add_argument('--file', '-f', help='Write output to file')

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Parse deployment data
    if args.deployment_file:
        deployment_data = load_deployment_file(args.deployment_file)
        deployment = parse_deployment_config(deployment_data)
    elif args.service and args.version:
        deployment = {
            'service_name': args.service,
            'version': args.version,
            'environment': args.environment,
            'strategy': args.strategy,
            'replicas': 1,
            'namespace': 'default',
            'cluster': '',
            'image': '',
            'changes': [],
            'rollback': {},
            'health_checks': [],
            'ci_names': args.ci_names.split(',') if args.ci_names else [],
            'owner': '',
            'jira_tickets': [],
        }
    else:
        parser.error('Either --deployment-file or (--service, --service-version) required')

    # Override CI names if provided
    if args.ci_names:
        deployment['ci_names'] = [ci.strip() for ci in args.ci_names.split(',')]

    # Parse times
    start_time = None
    end_time = None
    if args.start_time:
        start_time = datetime.strptime(args.start_time, '%Y-%m-%d %H:%M:%S')
    if args.end_time:
        end_time = datetime.strptime(args.end_time, '%Y-%m-%d %H:%M:%S')

    # Generate payload
    payload = generate_change_payload(
        deployment=deployment,
        change_type=args.change_type,
        start_time=start_time,
        end_time=end_time,
        assignment_group=args.assignment_group,
        config=config,
    )

    # Format output
    output = format_output(payload, args.output, config)

    # Write or print output
    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Change request payload written to: {args.file}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
