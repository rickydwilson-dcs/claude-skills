#!/usr/bin/env python3
"""
ServiceNow Status Sync

Bi-directional status synchronization between monitoring alerts and ServiceNow incidents.
Generates status update payloads for keeping systems in sync.

Features:
- Map alert states to ServiceNow incident states
- Generate status update payloads
- Support work notes and resolution details
- Parse ServiceNow webhook responses
- Track incident lifecycle

Usage:
    python servicenow_status_sync.py --action update --snow-number INC0012345 --status in_progress
    python servicenow_status_sync.py --action resolve --snow-number INC0012345 --notes "Fixed by rollback"
    python servicenow_status_sync.py --help

Author: Claude Skills Team
Version: 1.0.0
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Version info
__version__ = "1.0.0"

# ServiceNow incident states
SNOW_STATES = {
    'new': 1,
    'in_progress': 2,
    'on_hold': 3,
    'resolved': 6,
    'closed': 7,
    'canceled': 8,
}

# Alert state to ServiceNow state mapping
ALERT_TO_SNOW_STATE = {
    'firing': 'new',
    'triggered': 'new',
    'acknowledged': 'in_progress',
    'investigating': 'in_progress',
    'contained': 'on_hold',
    'pending': 'on_hold',
    'resolved': 'resolved',
    'ok': 'resolved',
    'closed': 'closed',
}

# Resolution codes
RESOLUTION_CODES = {
    'fixed': 'Resolved',
    'workaround': 'Workaround',
    'duplicate': 'Duplicate',
    'not_reproducible': 'Not Reproducible',
    'known_error': 'Known Error',
    'user_error': 'User Error',
    'no_fault_found': 'No Fault Found',
}

# Close codes
CLOSE_CODES = {
    'resolved': 'Solved (Permanently)',
    'workaround': 'Solved (Work Around)',
    'not_solved': 'Not Solved (Not Reproducible)',
    'duplicate': 'Not Solved (Duplicate)',
    'known_error': 'Solved Remotely (Workaround)',
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if config_path is None:
        script_dir = Path(__file__).parent.parent
        possible_paths = [
            script_dir / "assets" / "servicenow-config.yaml",
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
                    config[key] = {} if not value else value
                elif indent == 2 and current_section:
                    if isinstance(config.get(current_section), dict):
                        if value.lower() == 'true':
                            value = True
                        elif value.lower() == 'false':
                            value = False
                        elif value.isdigit():
                            value = int(value)
                        config[current_section][key] = value

    return config


def map_alert_state_to_snow(alert_state: str) -> str:
    """Map alert state to ServiceNow incident state."""
    normalized = alert_state.lower().replace('-', '_').replace(' ', '_')
    return ALERT_TO_SNOW_STATE.get(normalized, 'new')


def generate_status_update_payload(
    action: str,
    status: Optional[str] = None,
    notes: Optional[str] = None,
    assigned_to: Optional[str] = None,
    resolution_code: Optional[str] = None,
    close_code: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Generate ServiceNow status update payload."""
    config = config or {}
    payload = {}
    timestamp = datetime.utcnow().isoformat() + 'Z'

    if action == 'acknowledge':
        payload['state'] = str(SNOW_STATES['in_progress'])
        payload['work_notes'] = notes or f"Incident acknowledged at {timestamp}"
        if assigned_to:
            payload['assigned_to'] = assigned_to

    elif action == 'update':
        if status:
            snow_state = map_alert_state_to_snow(status)
            payload['state'] = str(SNOW_STATES.get(snow_state, SNOW_STATES['in_progress']))
        if notes:
            payload['work_notes'] = notes
        if assigned_to:
            payload['assigned_to'] = assigned_to

    elif action == 'hold':
        payload['state'] = str(SNOW_STATES['on_hold'])
        payload['hold_reason'] = notes or "Awaiting additional information"
        payload['work_notes'] = f"Incident placed on hold at {timestamp}\nReason: {notes or 'Pending investigation'}"

    elif action == 'resolve':
        payload['state'] = str(SNOW_STATES['resolved'])
        payload['resolution_code'] = RESOLUTION_CODES.get(resolution_code, 'Resolved')
        payload['close_notes'] = notes or f"Incident resolved at {timestamp}"
        payload['resolved_at'] = timestamp
        if close_code:
            payload['close_code'] = CLOSE_CODES.get(close_code, 'Solved (Permanently)')

    elif action == 'close':
        payload['state'] = str(SNOW_STATES['closed'])
        payload['close_code'] = CLOSE_CODES.get(close_code, 'Solved (Permanently)')
        payload['close_notes'] = notes or f"Incident closed at {timestamp}"
        payload['closed_at'] = timestamp

    elif action == 'reopen':
        payload['state'] = str(SNOW_STATES['in_progress'])
        payload['work_notes'] = notes or f"Incident reopened at {timestamp}"
        payload['reopen_count'] = '+1'  # Increment reopen counter

    return payload


def generate_work_note(
    note_type: str,
    content: str,
    author: Optional[str] = None,
    metrics: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate formatted work note."""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    lines = [f"[{timestamp}]"]

    if author:
        lines.append(f"Author: {author}")

    if note_type == 'investigation':
        lines.extend([
            "",
            "=== Investigation Update ===",
            content,
        ])

    elif note_type == 'resolution':
        lines.extend([
            "",
            "=== Resolution Details ===",
            content,
        ])
        if metrics:
            lines.extend([
                "",
                "Metrics:",
                f"  - Time to Detect (MTTD): {metrics.get('mttd', 'N/A')}",
                f"  - Time to Respond (MTTR): {metrics.get('mttr', 'N/A')}",
                f"  - Time to Contain (MTTC): {metrics.get('mttc', 'N/A')}",
            ])

    elif note_type == 'escalation':
        lines.extend([
            "",
            "=== Escalation Notice ===",
            content,
            "",
            "Escalation requested due to:",
            "  - SLA breach risk",
            "  - Requires additional expertise",
        ])

    elif note_type == 'handoff':
        lines.extend([
            "",
            "=== Handoff Notes ===",
            content,
        ])

    else:
        lines.extend(["", content])

    return '\n'.join(lines)


def parse_snow_webhook(webhook_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse ServiceNow webhook payload for bi-directional sync."""
    return {
        'incident_number': webhook_data.get('number', ''),
        'sys_id': webhook_data.get('sys_id', ''),
        'state': webhook_data.get('state', ''),
        'state_name': get_state_name(webhook_data.get('state', '')),
        'priority': webhook_data.get('priority', ''),
        'assigned_to': webhook_data.get('assigned_to', {}).get('display_value', ''),
        'assignment_group': webhook_data.get('assignment_group', {}).get('display_value', ''),
        'short_description': webhook_data.get('short_description', ''),
        'updated_on': webhook_data.get('sys_updated_on', ''),
        'work_notes': webhook_data.get('work_notes', ''),
        'close_notes': webhook_data.get('close_notes', ''),
    }


def get_state_name(state_value: str) -> str:
    """Convert state value to name."""
    state_names = {v: k for k, v in SNOW_STATES.items()}
    try:
        return state_names.get(int(state_value), 'unknown')
    except (ValueError, TypeError):
        return 'unknown'


def format_as_curl(
    payload: Dict[str, Any],
    incident_number: str,
    config: Dict[str, Any],
) -> str:
    """Format payload as curl command."""
    instance_url = config.get('servicenow', {}).get('instance_url', 'https://your-instance.service-now.com')

    curl_cmd = f'''curl -X PUT "{instance_url}/api/now/table/incident/{incident_number}" \\
  -H "Content-Type: application/json" \\
  -H "Accept: application/json" \\
  -H "Authorization: Basic $(echo -n "$SNOW_USERNAME:$SNOW_PASSWORD" | base64)" \\
  -d '{json.dumps(payload, indent=2)}'
'''
    return curl_cmd


def format_output(
    payload: Dict[str, Any],
    output_format: str,
    incident_number: str,
    config: Dict[str, Any],
) -> str:
    """Format output based on requested format."""
    if output_format == 'json':
        return json.dumps(payload, indent=2)
    elif output_format == 'curl':
        return format_as_curl(payload, incident_number, config)
    elif output_format == 'text':
        lines = [
            f"ServiceNow Status Update for {incident_number}",
            "=" * 50,
        ]
        for key, value in payload.items():
            lines.append(f"{key}: {value}")
        return '\n'.join(lines)
    else:
        return json.dumps(payload, indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Bi-directional status sync between alerts and ServiceNow incidents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Acknowledge incident
  python servicenow_status_sync.py --action acknowledge --snow-number INC0012345

  # Update with work notes
  python servicenow_status_sync.py --action update --snow-number INC0012345 \\
    --status investigating --notes "Root cause identified: memory leak"

  # Resolve incident
  python servicenow_status_sync.py --action resolve --snow-number INC0012345 \\
    --notes "Fixed by deploying hotfix v2.3.2" --resolution-code fixed

  # Close incident
  python servicenow_status_sync.py --action close --snow-number INC0012345 \\
    --close-code resolved

  # Generate curl command
  python servicenow_status_sync.py --action resolve --snow-number INC0012345 \\
    --output curl
'''
    )

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    # Required arguments
    parser.add_argument('--action', '-a', required=True,
                       choices=['acknowledge', 'update', 'hold', 'resolve', 'close', 'reopen'],
                       help='Action to perform')
    parser.add_argument('--snow-number', '-n', required=True,
                       help='ServiceNow incident number (INC...)')

    # Optional arguments
    parser.add_argument('--status', '-s',
                       choices=['firing', 'acknowledged', 'investigating', 'contained', 'resolved', 'closed'],
                       help='New status (for update action)')
    parser.add_argument('--notes', help='Work notes or resolution details')
    parser.add_argument('--assigned-to', help='User to assign incident to')
    parser.add_argument('--resolution-code',
                       choices=['fixed', 'workaround', 'duplicate', 'not_reproducible', 'known_error'],
                       help='Resolution code (for resolve action)')
    parser.add_argument('--close-code',
                       choices=['resolved', 'workaround', 'not_solved', 'duplicate', 'known_error'],
                       help='Close code (for close action)')

    # Configuration
    parser.add_argument('--config', help='Path to servicenow-config.yaml')

    # Output options
    parser.add_argument('--output', '-o',
                       choices=['json', 'text', 'curl'],
                       default='json',
                       help='Output format (default: json)')
    parser.add_argument('--file', '-f', help='Write output to file')

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Generate payload
    payload = generate_status_update_payload(
        action=args.action,
        status=args.status,
        notes=args.notes,
        assigned_to=args.assigned_to,
        resolution_code=args.resolution_code,
        close_code=args.close_code,
        config=config,
    )

    # Format output
    output = format_output(payload, args.output, args.snow_number, config)

    # Write or print output
    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Status update payload written to: {args.file}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
