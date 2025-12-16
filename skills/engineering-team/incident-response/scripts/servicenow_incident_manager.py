#!/usr/bin/env python3
"""
ServiceNow Incident Manager

Generate ServiceNow incident payloads from observability alerts.
Supports Prometheus AlertManager, NewRelic, DataDog, and custom alert formats.

Features:
- Maps P0-P3 severity to ServiceNow impact/urgency/priority
- Generates complete incident payload JSON
- Includes runbook URLs in description
- Outputs curl commands for testing
- Reads configuration from servicenow-config.yaml
- Supports CMDB CI linking

Usage:
    python servicenow_incident_manager.py --alert-file alert.json --output json
    python servicenow_incident_manager.py --severity P1 --service payment-api --output curl
    python servicenow_incident_manager.py --help

Author: Claude Skills Team
Version: 1.0.0
"""

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Version info
__version__ = "1.0.0"

# Default severity mapping (can be overridden by config)
DEFAULT_SEVERITY_MAPPING = {
    "P0": {"impact": 1, "urgency": 1, "priority": 1},
    "P1": {"impact": 2, "urgency": 1, "priority": 2},
    "P2": {"impact": 2, "urgency": 2, "priority": 3},
    "P3": {"impact": 3, "urgency": 3, "priority": 4},
    "critical": {"impact": 1, "urgency": 1, "priority": 1},
    "high": {"impact": 2, "urgency": 1, "priority": 2},
    "warning": {"impact": 2, "urgency": 2, "priority": 3},
    "low": {"impact": 3, "urgency": 3, "priority": 4},
    "info": {"impact": 3, "urgency": 3, "priority": 5},
}

# Default assignment groups
DEFAULT_ASSIGNMENT_GROUPS = {
    "default": "Platform Engineering",
    "infrastructure": "Infrastructure Team",
    "application": "Application Support",
    "security": "Security Operations",
    "database": "Database Administration",
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if config_path is None:
        # Look for config in standard locations
        script_dir = Path(__file__).parent.parent
        possible_paths = [
            script_dir / "assets" / "servicenow-config.yaml",
            Path.cwd() / "servicenow-config.yaml",
            Path.home() / ".servicenow-config.yaml",
        ]
        for path in possible_paths:
            if path.exists():
                config_path = str(path)
                break

    if config_path and Path(config_path).exists():
        try:
            # Simple YAML parsing without external dependency
            config = parse_simple_yaml(config_path)
            return config
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}", file=sys.stderr)

    return {}


def parse_simple_yaml(file_path: str) -> Dict[str, Any]:
    """Simple YAML parser for basic config files (no external deps)."""
    config = {}
    current_section = None
    current_subsection = None

    with open(file_path, 'r') as f:
        for line in f:
            # Skip comments and empty lines
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # Count indentation
            indent = len(line) - len(line.lstrip())

            # Handle key-value pairs
            if ':' in stripped:
                key, _, value = stripped.partition(':')
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                if indent == 0:
                    current_section = key
                    current_subsection = None
                    if value:
                        config[key] = value
                    else:
                        config[key] = {}
                elif indent == 2 and current_section:
                    current_subsection = key
                    if isinstance(config.get(current_section), dict):
                        if value:
                            config[current_section][key] = value
                        else:
                            config[current_section][key] = {}
                elif indent == 4 and current_section and current_subsection:
                    if isinstance(config.get(current_section), dict):
                        if isinstance(config[current_section].get(current_subsection), dict):
                            # Convert value types
                            if value.lower() == 'true':
                                value = True
                            elif value.lower() == 'false':
                                value = False
                            elif value.isdigit():
                                value = int(value)
                            config[current_section][current_subsection][key] = value

    return config


def load_alert_file(file_path: str) -> Dict[str, Any]:
    """Load alert data from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def parse_prometheus_alert(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse Prometheus AlertManager webhook format."""
    labels = alert_data.get('labels', {})
    annotations = alert_data.get('annotations', {})

    return {
        'alert_name': labels.get('alertname', 'Unknown Alert'),
        'severity': labels.get('severity', 'warning'),
        'service': labels.get('service', labels.get('job', 'unknown')),
        'namespace': labels.get('namespace', 'default'),
        'description': annotations.get('description', annotations.get('summary', '')),
        'runbook_url': annotations.get('runbook_url', ''),
        'source': 'Prometheus',
        'status': alert_data.get('status', 'firing'),
        'starts_at': alert_data.get('startsAt', ''),
        'labels': labels,
    }


def parse_newrelic_alert(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse NewRelic webhook format."""
    return {
        'alert_name': alert_data.get('condition_name', 'Unknown Alert'),
        'severity': alert_data.get('severity', 'WARNING').lower(),
        'service': alert_data.get('entity', {}).get('name', 'unknown'),
        'namespace': alert_data.get('account_name', ''),
        'description': alert_data.get('details', ''),
        'runbook_url': alert_data.get('runbook_url', alert_data.get('violation_url', '')),
        'source': 'NewRelic',
        'status': 'firing' if alert_data.get('current_state') == 'open' else 'resolved',
        'labels': {},
    }


def parse_datadog_alert(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse DataDog webhook format."""
    return {
        'alert_name': alert_data.get('alert_title', 'Unknown Alert'),
        'severity': alert_data.get('alert_type', 'warning'),
        'service': alert_data.get('hostname', alert_data.get('host', 'unknown')),
        'namespace': alert_data.get('scope', ''),
        'description': alert_data.get('body', alert_data.get('alert_metric', '')),
        'runbook_url': alert_data.get('link', ''),
        'source': 'DataDog',
        'status': 'firing' if alert_data.get('alert_transition') == 'Triggered' else 'resolved',
        'labels': alert_data.get('tags', {}),
    }


def parse_generic_alert(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse generic alert format."""
    return {
        'alert_name': alert_data.get('alert_name', alert_data.get('name', 'Unknown Alert')),
        'severity': alert_data.get('severity', alert_data.get('priority', 'warning')),
        'service': alert_data.get('service', alert_data.get('affected_service', 'unknown')),
        'namespace': alert_data.get('namespace', alert_data.get('environment', '')),
        'description': alert_data.get('description', alert_data.get('message', '')),
        'runbook_url': alert_data.get('runbook_url', alert_data.get('runbook', '')),
        'source': alert_data.get('source', 'Custom'),
        'status': alert_data.get('status', 'firing'),
        'labels': alert_data.get('labels', {}),
    }


def detect_and_parse_alert(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """Auto-detect alert format and parse accordingly."""
    # Prometheus format detection
    if 'labels' in alert_data and 'alertname' in alert_data.get('labels', {}):
        return parse_prometheus_alert(alert_data)

    # NewRelic format detection
    if 'condition_name' in alert_data or 'violation_url' in alert_data:
        return parse_newrelic_alert(alert_data)

    # DataDog format detection
    if 'alert_title' in alert_data or 'alert_type' in alert_data:
        return parse_datadog_alert(alert_data)

    # Fall back to generic format
    return parse_generic_alert(alert_data)


def map_severity_to_priority(severity: str, config: Dict[str, Any]) -> Dict[str, int]:
    """Map alert severity to ServiceNow impact/urgency/priority."""
    severity_mapping = config.get('servicenow', {}).get('severity_mapping', DEFAULT_SEVERITY_MAPPING)

    # Normalize severity string
    severity_normalized = severity.upper().replace('-', '').replace('_', '')

    # Try exact match first
    if severity in severity_mapping:
        mapping = severity_mapping[severity]
    elif severity_normalized in severity_mapping:
        mapping = severity_mapping[severity_normalized]
    elif severity.lower() in severity_mapping:
        mapping = severity_mapping[severity.lower()]
    else:
        # Default to medium priority
        mapping = DEFAULT_SEVERITY_MAPPING.get('P2', {"impact": 2, "urgency": 2, "priority": 3})

    return {
        'impact': str(mapping.get('impact', 2)),
        'urgency': str(mapping.get('urgency', 2)),
        'priority': str(mapping.get('priority', 3)),
    }


def get_assignment_group(service: str, severity: str, config: Dict[str, Any]) -> str:
    """Determine assignment group based on service and severity."""
    groups = config.get('servicenow', {}).get('assignment_groups', DEFAULT_ASSIGNMENT_GROUPS)

    # P0/Critical goes to escalation group if configured
    if severity.upper() in ['P0', 'CRITICAL']:
        if 'p0_escalation' in groups:
            return groups['p0_escalation']

    # P1/High goes to on-call group if configured
    if severity.upper() in ['P1', 'HIGH']:
        if 'p1_escalation' in groups:
            return groups['p1_escalation']

    # Try to match service type to group
    service_lower = service.lower()
    if any(kw in service_lower for kw in ['db', 'database', 'postgres', 'mysql', 'redis']):
        return groups.get('database', groups.get('default', 'Platform Engineering'))
    if any(kw in service_lower for kw in ['network', 'dns', 'load-balancer', 'lb']):
        return groups.get('network', groups.get('default', 'Platform Engineering'))
    if any(kw in service_lower for kw in ['security', 'auth', 'firewall', 'waf']):
        return groups.get('security', groups.get('default', 'Platform Engineering'))

    return groups.get('default', 'Platform Engineering')


def build_description(alert: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Build formatted incident description."""
    lines = [
        f"Alert: {alert['alert_name']}",
        f"Severity: {alert['severity'].upper()}",
        f"Source: {alert['source']}",
        f"Timestamp: {datetime.utcnow().isoformat()}Z",
        "",
        "Affected Systems:",
        f"  - Service: {alert['service']}",
    ]

    if alert.get('namespace'):
        lines.append(f"  - Environment: {alert['namespace']}")

    if alert.get('description'):
        lines.extend(["", "Details:", alert['description']])

    if alert.get('runbook_url'):
        lines.extend(["", f"Runbook: {alert['runbook_url']}"])

    if alert.get('labels'):
        lines.extend(["", "Labels:"])
        for key, value in alert['labels'].items():
            lines.append(f"  - {key}: {value}")

    return '\n'.join(lines)


def generate_incident_payload(
    alert: Dict[str, Any],
    config: Dict[str, Any],
    assignment_group: Optional[str] = None,
    ci_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate ServiceNow incident payload."""
    priority_mapping = map_severity_to_priority(alert['severity'], config)

    if assignment_group is None:
        assignment_group = get_assignment_group(alert['service'], alert['severity'], config)

    incident_config = config.get('servicenow', {}).get('incident', {})
    custom_fields = config.get('servicenow', {}).get('custom_fields', {})

    payload = {
        'short_description': f"{alert['alert_name']} - {alert['service']}",
        'description': build_description(alert, config),
        'category': incident_config.get('category', 'Software'),
        'subcategory': incident_config.get('subcategory', 'Application'),
        'impact': priority_mapping['impact'],
        'urgency': priority_mapping['urgency'],
        'priority': priority_mapping['priority'],
        'assignment_group': assignment_group,
        'caller_id': incident_config.get('caller_id', 'monitoring-system'),
        'contact_type': incident_config.get('contact_type', 'Monitoring'),
    }

    # Add CI reference if provided
    if ci_name:
        payload['cmdb_ci'] = ci_name
    elif alert.get('service'):
        payload['cmdb_ci'] = alert['service']

    # Add custom fields
    for field, value in custom_fields.items():
        payload[field] = value

    # Add correlation ID for tracking
    payload['correlation_id'] = f"{alert['source'].lower()}-{alert['alert_name']}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    return payload


def format_as_curl(payload: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Format payload as curl command for testing."""
    instance_url = config.get('servicenow', {}).get('instance_url', 'https://your-instance.service-now.com')

    curl_cmd = f'''curl -X POST "{instance_url}/api/now/table/incident" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  -H "Authorization: Basic $(echo -n "$SNOW_USERNAME:$SNOW_PASSWORD" | base64)" \\
  -d '{json.dumps(payload, indent=2)}'
'''
    return curl_cmd


def format_output(payload: Dict[str, Any], output_format: str, config: Dict[str, Any]) -> str:
    """Format output based on requested format."""
    if output_format == 'json':
        return json.dumps(payload, indent=2)
    elif output_format == 'curl':
        return format_as_curl(payload, config)
    elif output_format == 'text':
        lines = ["ServiceNow Incident Payload", "=" * 40]
        for key, value in payload.items():
            if key == 'description':
                lines.append(f"\n{key}:")
                lines.append("-" * 20)
                lines.append(value)
                lines.append("-" * 20)
            else:
                lines.append(f"{key}: {value}")
        return '\n'.join(lines)
    else:
        return json.dumps(payload, indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate ServiceNow incident payloads from observability alerts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # From alert file
  python servicenow_incident_manager.py --alert-file alert.json --output json

  # Manual incident creation
  python servicenow_incident_manager.py --severity P1 --service payment-api \\
    --alert-name "High Latency" --output curl

  # With custom assignment group
  python servicenow_incident_manager.py --alert-file alert.json \\
    --assignment-group "Database Team" --output json

  # Output to file
  python servicenow_incident_manager.py --alert-file alert.json \\
    --output json --file incident-payload.json
'''
    )

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    # Input options
    input_group = parser.add_argument_group('Input Options')
    input_group.add_argument('--alert-file', '-a', help='Path to alert JSON file')
    input_group.add_argument('--alert-name', help='Alert name (manual mode)')
    input_group.add_argument('--severity', '-s',
                            choices=['P0', 'P1', 'P2', 'P3', 'critical', 'high', 'warning', 'low', 'info'],
                            help='Alert severity')
    input_group.add_argument('--service', help='Affected service name')
    input_group.add_argument('--description', '-d', help='Alert description')
    input_group.add_argument('--runbook-url', help='Runbook URL')
    input_group.add_argument('--source', default='Custom', help='Alert source system')

    # ServiceNow options
    snow_group = parser.add_argument_group('ServiceNow Options')
    snow_group.add_argument('--assignment-group', '-g', help='Override assignment group')
    snow_group.add_argument('--ci-name', '-c', help='CMDB Configuration Item name')
    snow_group.add_argument('--config', help='Path to servicenow-config.yaml')

    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('--output', '-o',
                             choices=['json', 'text', 'curl'],
                             default='json',
                             help='Output format (default: json)')
    output_group.add_argument('--file', '-f', help='Write output to file')
    output_group.add_argument('--dry-run', action='store_true',
                             help='Generate payload without suggestions to send')

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Parse alert data
    if args.alert_file:
        alert_data = load_alert_file(args.alert_file)
        alert = detect_and_parse_alert(alert_data)
    elif args.alert_name and args.severity and args.service:
        # Manual mode
        alert = {
            'alert_name': args.alert_name,
            'severity': args.severity,
            'service': args.service,
            'namespace': '',
            'description': args.description or '',
            'runbook_url': args.runbook_url or '',
            'source': args.source,
            'status': 'firing',
            'labels': {},
        }
    else:
        parser.error('Either --alert-file or (--alert-name, --severity, --service) required')

    # Generate incident payload
    payload = generate_incident_payload(
        alert=alert,
        config=config,
        assignment_group=args.assignment_group,
        ci_name=args.ci_name,
    )

    # Format output
    output = format_output(payload, args.output, config)

    # Write or print output
    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Incident payload written to: {args.file}", file=sys.stderr)
    else:
        print(output)

    # Show dry-run message
    if args.dry_run:
        print("\n[DRY RUN] Payload generated but not sent to ServiceNow", file=sys.stderr)


if __name__ == '__main__':
    main()
