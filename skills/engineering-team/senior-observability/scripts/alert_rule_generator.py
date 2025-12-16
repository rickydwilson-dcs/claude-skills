#!/usr/bin/env python3
"""
Alert Rule Generator
Generate alerting rules for Prometheus AlertManager, DataDog, CloudWatch, PagerDuty, and New Relic.

Features:
- Multi-platform support (Prometheus, DataDog, CloudWatch, PagerDuty, New Relic)
- SLO-based alerting (error budget consumption)
- Multi-window, multi-burn-rate alerting patterns
- Severity classification (critical, warning, info)
- Runbook link generation
- Inhibition rules to reduce alert noise
- NRQL-based alert conditions for New Relic

Standard library only - no external dependencies required.
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

__version__ = "1.0.0"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Platform(Enum):
    """Supported alerting platforms"""
    PROMETHEUS = "prometheus"
    DATADOG = "datadog"
    CLOUDWATCH = "cloudwatch"
    PAGERDUTY = "pagerduty"
    NEWRELIC = "newrelic"


class Severity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class AlertType(Enum):
    """Types of alerts"""
    AVAILABILITY = "availability"
    LATENCY = "latency"
    ERROR_RATE = "error_rate"
    SATURATION = "saturation"
    BURN_RATE = "burn_rate"
    RESOURCE = "resource"


@dataclass
class AlertRule:
    """Alert rule configuration"""
    name: str
    alert_type: AlertType
    severity: Severity
    expression: str
    duration: str  # e.g., "5m", "15m"
    summary: str
    description: str
    runbook_url: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)


@dataclass
class AlertConfig:
    """Complete alert configuration"""
    service: str
    slo_target: float  # e.g., 99.9
    rules: List[AlertRule] = field(default_factory=list)
    inhibit_rules: List[Dict[str, Any]] = field(default_factory=list)


class BurnRateCalculator:
    """Calculate burn rates for SLO-based alerting"""

    # Multi-window, multi-burn-rate thresholds based on Google SRE guidelines
    # Format: (short_window, long_window, burn_rate, severity)
    BURN_RATE_WINDOWS = [
        ("1h", "5m", 14.4, Severity.CRITICAL),    # 2% of 30-day budget in 1 hour
        ("6h", "30m", 6.0, Severity.CRITICAL),    # 5% of 30-day budget in 6 hours
        ("1d", "2h", 3.0, Severity.WARNING),      # 10% of 30-day budget in 1 day
        ("3d", "6h", 1.0, Severity.WARNING),      # 10% of 30-day budget in 3 days
    ]

    @staticmethod
    def error_budget_percent(slo_target: float) -> float:
        """Calculate error budget as percentage"""
        return 100 - slo_target

    @staticmethod
    def burn_rate_threshold(slo_target: float, window_hours: float, budget_consumption: float = 0.02) -> float:
        """
        Calculate burn rate threshold

        Args:
            slo_target: Target SLO (e.g., 99.9)
            window_hours: Alert window in hours
            budget_consumption: Fraction of monthly budget to consume (default 2%)

        Returns:
            Burn rate threshold
        """
        error_budget = 100 - slo_target
        monthly_hours = 30 * 24  # 720 hours
        burn_rate = (budget_consumption * monthly_hours) / (window_hours * (error_budget / 100))
        return round(burn_rate, 2)


class PrometheusAlertGenerator:
    """Generate Prometheus AlertManager rules"""

    @staticmethod
    def availability_alerts(service: str, slo_target: float, runbook_base: str) -> List[AlertRule]:
        """Generate availability-based alerts"""
        error_budget = 100 - slo_target
        rules = []

        for short_window, long_window, burn_rate, severity in BurnRateCalculator.BURN_RATE_WINDOWS:
            rule = AlertRule(
                name=f"{service}_high_error_rate_{short_window}",
                alert_type=AlertType.BURN_RATE,
                severity=severity,
                expression=f"""
(
  sum(rate(http_requests_total{{service="{service}",status=~"5.."}}[{long_window}]))
  /
  sum(rate(http_requests_total{{service="{service}"}}[{long_window}]))
) > ({burn_rate} * {error_budget / 100})
and
(
  sum(rate(http_requests_total{{service="{service}",status=~"5.."}}[{short_window}]))
  /
  sum(rate(http_requests_total{{service="{service}"}}[{short_window}]))
) > ({burn_rate} * {error_budget / 100})
""".strip(),
                duration="2m",
                summary=f"High error rate burning {slo_target}% SLO budget",
                description=f"Service {service} is consuming error budget at {burn_rate}x the sustainable rate over {short_window}",
                runbook_url=f"{runbook_base}/high-error-rate" if runbook_base else "",
                labels={
                    "service": service,
                    "slo": f"{slo_target}",
                    "burn_rate": str(burn_rate),
                    "window": short_window
                }
            )
            rules.append(rule)

        return rules

    @staticmethod
    def latency_alerts(service: str, slo_target: float, runbook_base: str) -> List[AlertRule]:
        """Generate latency-based alerts"""
        rules = []

        # P99 latency alert
        rules.append(AlertRule(
            name=f"{service}_high_latency_p99",
            alert_type=AlertType.LATENCY,
            severity=Severity.WARNING,
            expression=f"""
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket{{service="{service}"}}[5m])) by (le)
) > 1.0
""".strip(),
            duration="5m",
            summary=f"High P99 latency for {service}",
            description=f"P99 latency for {service} is above 1 second",
            runbook_url=f"{runbook_base}/high-latency" if runbook_base else "",
            labels={"service": service, "percentile": "99"}
        ))

        # P95 latency alert
        rules.append(AlertRule(
            name=f"{service}_high_latency_p95",
            alert_type=AlertType.LATENCY,
            severity=Severity.INFO,
            expression=f"""
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket{{service="{service}"}}[5m])) by (le)
) > 0.5
""".strip(),
            duration="10m",
            summary=f"Elevated P95 latency for {service}",
            description=f"P95 latency for {service} is above 500ms",
            runbook_url=f"{runbook_base}/high-latency" if runbook_base else "",
            labels={"service": service, "percentile": "95"}
        ))

        return rules

    @staticmethod
    def resource_alerts(service: str, runbook_base: str) -> List[AlertRule]:
        """Generate resource utilization alerts"""
        rules = []

        # CPU alert
        rules.append(AlertRule(
            name=f"{service}_high_cpu",
            alert_type=AlertType.RESOURCE,
            severity=Severity.WARNING,
            expression=f"""
sum(rate(container_cpu_usage_seconds_total{{container="{service}"}}[5m]))
/
sum(container_spec_cpu_quota{{container="{service}"}}/container_spec_cpu_period{{container="{service}"}})
* 100 > 80
""".strip(),
            duration="10m",
            summary=f"High CPU usage for {service}",
            description=f"CPU usage for {service} is above 80% for 10 minutes",
            runbook_url=f"{runbook_base}/high-cpu" if runbook_base else "",
            labels={"service": service, "resource": "cpu"}
        ))

        # Memory alert
        rules.append(AlertRule(
            name=f"{service}_high_memory",
            alert_type=AlertType.RESOURCE,
            severity=Severity.WARNING,
            expression=f"""
sum(container_memory_working_set_bytes{{container="{service}"}})
/
sum(container_spec_memory_limit_bytes{{container="{service}"}})
* 100 > 85
""".strip(),
            duration="10m",
            summary=f"High memory usage for {service}",
            description=f"Memory usage for {service} is above 85% for 10 minutes",
            runbook_url=f"{runbook_base}/high-memory" if runbook_base else "",
            labels={"service": service, "resource": "memory"}
        ))

        # Critical memory alert
        rules.append(AlertRule(
            name=f"{service}_critical_memory",
            alert_type=AlertType.RESOURCE,
            severity=Severity.CRITICAL,
            expression=f"""
sum(container_memory_working_set_bytes{{container="{service}"}})
/
sum(container_spec_memory_limit_bytes{{container="{service}"}})
* 100 > 95
""".strip(),
            duration="5m",
            summary=f"Critical memory usage for {service}",
            description=f"Memory usage for {service} is above 95% - OOM risk",
            runbook_url=f"{runbook_base}/critical-memory" if runbook_base else "",
            labels={"service": service, "resource": "memory"}
        ))

        return rules

    @staticmethod
    def saturation_alerts(service: str, runbook_base: str) -> List[AlertRule]:
        """Generate saturation alerts"""
        rules = []

        rules.append(AlertRule(
            name=f"{service}_high_saturation",
            alert_type=AlertType.SATURATION,
            severity=Severity.WARNING,
            expression=f"""
sum(http_server_active_requests{{service="{service}"}}) > 100
""".strip(),
            duration="5m",
            summary=f"High request saturation for {service}",
            description=f"Active requests for {service} exceeds 100",
            runbook_url=f"{runbook_base}/high-saturation" if runbook_base else "",
            labels={"service": service}
        ))

        return rules

    @staticmethod
    def service_down_alert(service: str, runbook_base: str) -> AlertRule:
        """Generate service down alert"""
        return AlertRule(
            name=f"{service}_down",
            alert_type=AlertType.AVAILABILITY,
            severity=Severity.CRITICAL,
            expression=f'up{{job="{service}"}} == 0',
            duration="1m",
            summary=f"Service {service} is down",
            description=f"Service {service} has been down for more than 1 minute",
            runbook_url=f"{runbook_base}/service-down" if runbook_base else "",
            labels={"service": service}
        )

    @staticmethod
    def format_rule(rule: AlertRule) -> Dict[str, Any]:
        """Format a single alert rule for Prometheus"""
        formatted = {
            "alert": rule.name,
            "expr": rule.expression,
            "for": rule.duration,
            "labels": {
                "severity": rule.severity.value,
                "alert_type": rule.alert_type.value,
                **rule.labels
            },
            "annotations": {
                "summary": rule.summary,
                "description": rule.description,
                **rule.annotations
            }
        }

        if rule.runbook_url:
            formatted["annotations"]["runbook_url"] = rule.runbook_url

        return formatted

    @staticmethod
    def generate_inhibit_rules(service: str) -> List[Dict[str, Any]]:
        """Generate inhibition rules to prevent alert storms"""
        return [
            {
                "source_match": {
                    "alertname": f"{service}_down"
                },
                "target_match_re": {
                    "alertname": f"{service}_.*"
                },
                "equal": ["service"]
            },
            {
                "source_match": {
                    "severity": "critical"
                },
                "target_match": {
                    "severity": "warning"
                },
                "equal": ["alertname", "service"]
            }
        ]

    @staticmethod
    def generate_config(config: AlertConfig) -> Dict[str, Any]:
        """Generate complete Prometheus alerting config"""
        formatted_rules = [PrometheusAlertGenerator.format_rule(r) for r in config.rules]

        return {
            "groups": [
                {
                    "name": f"{config.service}-alerts",
                    "rules": formatted_rules
                }
            ]
        }


class DataDogAlertGenerator:
    """Generate DataDog monitor configurations"""

    @staticmethod
    def format_rule(rule: AlertRule, service: str) -> Dict[str, Any]:
        """Format a single alert rule for DataDog"""
        # Convert Prometheus expression to DataDog query (simplified)
        query = rule.expression.replace("{", "(").replace("}", ")")
        query = query.replace("rate(", "avg:").replace("[5m]", ".rollup(avg, 300)")

        return {
            "name": f"[{service}] {rule.summary}",
            "type": "metric alert",
            "query": query,
            "message": f"""
{rule.description}

Severity: {rule.severity.value}
Runbook: {rule.runbook_url}

@pagerduty
""".strip(),
            "tags": [f"service:{service}", f"severity:{rule.severity.value}"],
            "options": {
                "thresholds": {
                    "critical": 1,
                    "warning": 0.5
                },
                "notify_no_data": True,
                "no_data_timeframe": 10,
                "renotify_interval": 60
            }
        }

    @staticmethod
    def generate_config(config: AlertConfig) -> Dict[str, Any]:
        """Generate complete DataDog alerting config"""
        monitors = [DataDogAlertGenerator.format_rule(r, config.service) for r in config.rules]

        return {
            "monitors": monitors
        }


class CloudWatchAlertGenerator:
    """Generate CloudWatch alarm configurations"""

    @staticmethod
    def format_rule(rule: AlertRule, service: str) -> Dict[str, Any]:
        """Format a single alert rule for CloudWatch"""
        return {
            "AlarmName": f"{service}-{rule.name}",
            "AlarmDescription": rule.description,
            "MetricName": rule.alert_type.value,
            "Namespace": f"Custom/{service}",
            "Statistic": "Average",
            "Period": 300,
            "EvaluationPeriods": 3,
            "Threshold": 1,
            "ComparisonOperator": "GreaterThanThreshold",
            "TreatMissingData": "breaching",
            "AlarmActions": [
                f"arn:aws:sns:us-east-1:123456789:alerts-{rule.severity.value}"
            ],
            "Tags": [
                {"Key": "Service", "Value": service},
                {"Key": "Severity", "Value": rule.severity.value}
            ]
        }

    @staticmethod
    def generate_config(config: AlertConfig) -> Dict[str, Any]:
        """Generate complete CloudWatch alerting config"""
        alarms = [CloudWatchAlertGenerator.format_rule(r, config.service) for r in config.rules]

        return {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": f"CloudWatch alarms for {config.service}",
            "Resources": {
                f"{config.service}Alarm{i}": {
                    "Type": "AWS::CloudWatch::Alarm",
                    "Properties": alarm
                }
                for i, alarm in enumerate(alarms)
            }
        }


class PagerDutyAlertGenerator:
    """Generate PagerDuty event rules"""

    @staticmethod
    def generate_config(config: AlertConfig) -> Dict[str, Any]:
        """Generate PagerDuty routing and event rules"""
        rules = []

        for rule in config.rules:
            urgency = "high" if rule.severity == Severity.CRITICAL else "low"
            rules.append({
                "condition": {
                    "expression": {
                        "field": "details.alert_type",
                        "operation": "equals",
                        "value": rule.alert_type.value
                    }
                },
                "actions": {
                    "severity": {
                        "value": rule.severity.value
                    },
                    "urgency": {
                        "value": urgency
                    },
                    "route": {
                        "value": config.service
                    },
                    "annotate": {
                        "value": rule.runbook_url
                    }
                }
            })

        return {
            "service": config.service,
            "event_rules": rules
        }


class NewRelicAlertGenerator:
    """Generate New Relic NRQL alert conditions"""

    # Window duration mapping (Prometheus to minutes)
    WINDOW_MAP = {
        "1m": 1, "2m": 2, "5m": 5, "10m": 10, "15m": 15,
        "30m": 30, "1h": 60, "2h": 120, "6h": 360, "1d": 1440, "3d": 4320
    }

    @staticmethod
    def translate_promql_to_nrql(promql: str, service: str) -> str:
        """
        Translate PromQL expression to NRQL query.

        Handles common alerting patterns:
        - Error rate calculations
        - Latency percentiles
        - Resource utilization
        - Service availability
        """
        # Service availability check
        if "up{" in promql and "== 0" in promql:
            return f"SELECT count(*) FROM Transaction WHERE appName = '{service}' AND error IS false"

        # Error rate / burn rate alerts
        if 'status=~"5.."' in promql or "status=~'5..'" in promql:
            if "/" in promql:  # Error rate percentage
                return f"SELECT percentage(count(*), WHERE error IS true) FROM Transaction WHERE appName = '{service}'"
            else:  # Error count
                return f"SELECT filter(count(*), WHERE httpResponseCode LIKE '5%') FROM Transaction WHERE appName = '{service}'"

        # Latency percentile alerts
        if "histogram_quantile" in promql:
            if "0.99" in promql:
                return f"SELECT percentile(duration, 99) FROM Transaction WHERE appName = '{service}'"
            elif "0.95" in promql:
                return f"SELECT percentile(duration, 95) FROM Transaction WHERE appName = '{service}'"
            else:
                return f"SELECT percentile(duration, 99) FROM Transaction WHERE appName = '{service}'"

        # CPU utilization
        if "container_cpu_usage" in promql:
            return f"SELECT average(cpuPercent) FROM SystemSample WHERE hostname LIKE '%{service}%' OR appName = '{service}'"

        # Memory utilization
        if "container_memory" in promql or "memory_working_set" in promql:
            return f"SELECT average(memoryUsedPercent) FROM SystemSample WHERE hostname LIKE '%{service}%' OR appName = '{service}'"

        # Active requests / saturation
        if "http_server_active_requests" in promql:
            return f"SELECT average(duration) * rate(count(*), 1 minute) FROM Transaction WHERE appName = '{service}'"

        # Fallback: generic query
        return f"SELECT count(*) FROM Transaction WHERE appName = '{service}'"

    @staticmethod
    def extract_threshold(promql: str) -> float:
        """Extract numeric threshold from PromQL expression"""
        import re
        # Look for comparison operators with numbers
        patterns = [
            r'>\s*([\d.]+)',      # > threshold
            r'>=\s*([\d.]+)',     # >= threshold
            r'<\s*([\d.]+)',      # < threshold
            r'<=\s*([\d.]+)',     # <= threshold
            r'==\s*([\d.]+)',     # == threshold
        ]
        for pattern in patterns:
            match = re.search(pattern, promql)
            if match:
                return float(match.group(1))
        return 1.0  # Default threshold

    @staticmethod
    def format_rule(rule: AlertRule, service: str, slo_target: float) -> Dict[str, Any]:
        """Format a single alert rule for New Relic NRQL condition"""
        # Translate the query
        nrql_query = NewRelicAlertGenerator.translate_promql_to_nrql(rule.expression, service)

        # Extract threshold from the original expression
        threshold = NewRelicAlertGenerator.extract_threshold(rule.expression)

        # Parse duration to minutes
        duration_mins = NewRelicAlertGenerator.WINDOW_MAP.get(rule.duration, 5)

        # Map severity to New Relic priority
        priority_map = {
            Severity.CRITICAL: "CRITICAL",
            Severity.WARNING: "WARNING",
            Severity.INFO: "LOW"
        }

        # Determine condition type based on alert type
        if rule.alert_type == AlertType.AVAILABILITY:
            condition_type = "static"
            operator = "BELOW"
            threshold = 1  # At least 1 transaction expected
        elif rule.alert_type in [AlertType.ERROR_RATE, AlertType.BURN_RATE]:
            condition_type = "static"
            operator = "ABOVE"
            # Convert error budget threshold
            if "* 100" in rule.expression or "percent" in rule.description.lower():
                threshold = max(threshold, (100 - slo_target) * 2)  # 2x error budget
            else:
                threshold = max(threshold, 0.01)  # 1% default
        elif rule.alert_type == AlertType.LATENCY:
            condition_type = "static"
            operator = "ABOVE"
            threshold = threshold if threshold > 0 else 1.0  # Default 1 second
        elif rule.alert_type == AlertType.RESOURCE:
            condition_type = "static"
            operator = "ABOVE"
            threshold = threshold if threshold > 0 else 80  # Default 80%
        else:
            condition_type = "static"
            operator = "ABOVE"

        return {
            "name": rule.name.replace("_", " ").title(),
            "type": "NRQL",
            "enabled": True,
            "nrql": {
                "query": nrql_query
            },
            "signal": {
                "aggregation_window": duration_mins * 60,  # Convert to seconds
                "aggregation_method": "EVENT_FLOW",
                "aggregation_delay": 120,
                "fill_option": "NONE"
            },
            "terms": [
                {
                    "threshold": threshold,
                    "threshold_duration": duration_mins * 60,
                    "threshold_occurrences": "ALL",
                    "operator": operator,
                    "priority": priority_map.get(rule.severity, "WARNING")
                }
            ],
            "violation_time_limit_seconds": 86400,  # 24 hours
            "runbook_url": rule.runbook_url,
            "description": rule.description,
            "tags": {
                "service": service,
                "alert_type": rule.alert_type.value,
                "severity": rule.severity.value,
                "slo_target": str(slo_target)
            }
        }

    @staticmethod
    def generate_config(config: AlertConfig) -> Dict[str, Any]:
        """Generate complete New Relic alerting policy configuration"""
        conditions = []
        for rule in config.rules:
            conditions.append(
                NewRelicAlertGenerator.format_rule(rule, config.service, config.slo_target)
            )

        return {
            "__comment": "New Relic Alert Policy - Import via NerdGraph API",
            "__usage": "Use NerdGraph mutation alertsPolicyCreate and alertsNrqlConditionCreate",
            "policy": {
                "name": f"{config.service} SLO Alerts",
                "incident_preference": "PER_CONDITION_AND_TARGET"
            },
            "conditions": conditions,
            "notification_channels": [
                {
                    "type": "PAGERDUTY",
                    "name": f"{config.service}-pagerduty",
                    "config": {
                        "service_key": "{{PAGERDUTY_SERVICE_KEY}}"
                    }
                },
                {
                    "type": "SLACK",
                    "name": f"{config.service}-slack",
                    "config": {
                        "channel": "#alerts-{config.service}",
                        "webhook_url": "{{SLACK_WEBHOOK_URL}}"
                    }
                }
            ]
        }


def generate_all_alerts(service: str, slo_target: float, severities: List[Severity],
                        runbook_base: str) -> AlertConfig:
    """Generate all alert rules for a service"""
    config = AlertConfig(service=service, slo_target=slo_target)

    # Service down alert (always critical)
    config.rules.append(PrometheusAlertGenerator.service_down_alert(service, runbook_base))

    # Availability/burn rate alerts
    availability_rules = PrometheusAlertGenerator.availability_alerts(service, slo_target, runbook_base)
    for rule in availability_rules:
        if rule.severity in severities:
            config.rules.append(rule)

    # Latency alerts
    latency_rules = PrometheusAlertGenerator.latency_alerts(service, slo_target, runbook_base)
    for rule in latency_rules:
        if rule.severity in severities:
            config.rules.append(rule)

    # Resource alerts
    resource_rules = PrometheusAlertGenerator.resource_alerts(service, runbook_base)
    for rule in resource_rules:
        if rule.severity in severities:
            config.rules.append(rule)

    # Saturation alerts
    saturation_rules = PrometheusAlertGenerator.saturation_alerts(service, runbook_base)
    for rule in saturation_rules:
        if rule.severity in severities:
            config.rules.append(rule)

    # Inhibition rules
    config.inhibit_rules = PrometheusAlertGenerator.generate_inhibit_rules(service)

    return config


def format_output(config: Dict[str, Any], output_format: str, platform: str) -> str:
    """Format alert configuration output"""
    if output_format == "json":
        return json.dumps(config, indent=2)
    elif output_format == "yaml":
        # Simple YAML-like output for Prometheus
        def to_yaml(obj: Any, indent: int = 0) -> str:
            prefix = "  " * indent
            if isinstance(obj, dict):
                lines = []
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        lines.append(f"{prefix}{k}:")
                        lines.append(to_yaml(v, indent + 1))
                    elif isinstance(v, str) and "\n" in v:
                        # Multi-line string
                        lines.append(f"{prefix}{k}: |")
                        for line in v.split("\n"):
                            lines.append(f"{prefix}  {line}")
                    else:
                        val = v if isinstance(v, (int, float, bool)) else f'"{v}"' if v else '""'
                        if isinstance(v, bool):
                            val = str(v).lower()
                        lines.append(f"{prefix}{k}: {val}")
                return "\n".join(lines)
            elif isinstance(obj, list):
                lines = []
                for item in obj:
                    if isinstance(item, dict):
                        first = True
                        for k, v in item.items():
                            pref = f"{prefix}- " if first else f"{prefix}  "
                            first = False
                            if isinstance(v, (dict, list)):
                                lines.append(f"{pref}{k}:")
                                lines.append(to_yaml(v, indent + 2))
                            elif isinstance(v, str) and "\n" in v:
                                lines.append(f"{pref}{k}: |")
                                for line in v.split("\n"):
                                    lines.append(f"{prefix}    {line}")
                            else:
                                val = v if isinstance(v, (int, float, bool)) else f'"{v}"' if v else '""'
                                if isinstance(v, bool):
                                    val = str(v).lower()
                                lines.append(f"{pref}{k}: {val}")
                    else:
                        lines.append(f"{prefix}- {json.dumps(item)}")
                return "\n".join(lines)
            else:
                return f"{prefix}{json.dumps(obj)}"
        return to_yaml(config)
    else:  # text
        lines = [
            "=" * 60,
            f"Alert Rules for {platform.upper()}",
            "=" * 60,
            ""
        ]

        if platform == "prometheus":
            groups = config.get("groups", [])
            for group in groups:
                lines.append(f"Group: {group.get('name', 'Unknown')}")
                lines.append("-" * 40)
                for rule in group.get("rules", []):
                    severity = rule.get("labels", {}).get("severity", "unknown")
                    lines.append(f"  [{severity.upper()}] {rule.get('alert', 'Unknown')}")
                    lines.append(f"    Duration: {rule.get('for', 'N/A')}")
                    lines.append(f"    Summary: {rule.get('annotations', {}).get('summary', 'N/A')}")
                    if rule.get('annotations', {}).get('runbook_url'):
                        lines.append(f"    Runbook: {rule['annotations']['runbook_url']}")
                    lines.append("")
        elif platform == "datadog":
            for monitor in config.get("monitors", []):
                lines.append(f"  {monitor.get('name', 'Unknown')}")
                lines.append(f"    Type: {monitor.get('type', 'N/A')}")
                lines.append("")
        elif platform == "cloudwatch":
            for name, resource in config.get("Resources", {}).items():
                props = resource.get("Properties", {})
                lines.append(f"  {props.get('AlarmName', name)}")
                lines.append(f"    Metric: {props.get('MetricName', 'N/A')}")
                lines.append("")
        elif platform == "newrelic":
            policy = config.get("policy", {})
            lines.append(f"Policy: {policy.get('name', 'Unknown')}")
            lines.append(f"Incident Preference: {policy.get('incident_preference', 'N/A')}")
            lines.append("-" * 40)
            for condition in config.get("conditions", []):
                severity = condition.get("tags", {}).get("severity", "unknown")
                lines.append(f"  [{severity.upper()}] {condition.get('name', 'Unknown')}")
                lines.append(f"    Type: {condition.get('type', 'N/A')}")
                lines.append(f"    NRQL: {condition.get('nrql', {}).get('query', 'N/A')[:60]}...")
                if condition.get('runbook_url'):
                    lines.append(f"    Runbook: {condition['runbook_url']}")
                lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate alerting rules for Prometheus, DataDog, CloudWatch, PagerDuty, or New Relic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Prometheus alerts for 99.9% SLO
  %(prog)s --service payment-api --slo-target 99.9 --platform prometheus --output yaml

  # Generate DataDog monitors
  %(prog)s --service payment-api --slo-target 99.9 --platform datadog --output json

  # Generate New Relic NRQL alert conditions
  %(prog)s --service pandora-api --slo-target 99.9 --platform newrelic --output json

  # Generate critical alerts only
  %(prog)s --service payment-api --severity critical --platform prometheus --output yaml

  # Include runbook links
  %(prog)s --service payment-api --runbook-url https://runbooks.example.com --output yaml

Alert Types Generated:
  - Service down (critical)
  - Multi-burn-rate SLO alerts (critical/warning)
  - Latency percentile alerts (warning/info)
  - Resource utilization alerts (critical/warning)
  - Saturation alerts (warning)

Platforms:
  prometheus  - Prometheus AlertManager rules (YAML)
  datadog     - DataDog monitors (JSON)
  cloudwatch  - AWS CloudWatch alarms (CloudFormation)
  pagerduty   - PagerDuty event rules (JSON)
  newrelic    - New Relic NRQL conditions (NerdGraph API)
        """
    )

    parser.add_argument(
        "--service", "-s",
        required=True,
        help="Service name for alerts"
    )

    parser.add_argument(
        "--slo-target",
        type=float,
        default=99.9,
        help="SLO availability target percentage (default: 99.9)"
    )

    parser.add_argument(
        "--platform", "-p",
        choices=[p.value for p in Platform],
        default="prometheus",
        help="Target alerting platform (default: prometheus)"
    )

    parser.add_argument(
        "--severity",
        default="critical,warning",
        help="Comma-separated severity levels to generate (default: critical,warning)"
    )

    parser.add_argument(
        "--output", "-o",
        choices=["yaml", "json", "text"],
        default="yaml",
        help="Output format (default: yaml)"
    )

    parser.add_argument(
        "--file", "-f",
        help="Write output to file instead of stdout"
    )

    parser.add_argument(
        "--runbook-url",
        default="",
        help="Base URL for runbook links"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Parse severity levels
        severities = []
        for sev in args.severity.split(","):
            sev = sev.strip().lower()
            try:
                severities.append(Severity(sev))
            except ValueError:
                logger.warning(f"Unknown severity: {sev}, skipping")

        if not severities:
            severities = [Severity.CRITICAL, Severity.WARNING]

        # Generate alerts
        logger.info(f"Generating {args.platform} alerts for {args.service} (SLO: {args.slo_target}%)")

        config = generate_all_alerts(
            service=args.service,
            slo_target=args.slo_target,
            severities=severities,
            runbook_base=args.runbook_url
        )

        # Generate platform-specific output
        platform = Platform(args.platform)
        if platform == Platform.PROMETHEUS:
            output_config = PrometheusAlertGenerator.generate_config(config)
        elif platform == Platform.DATADOG:
            output_config = DataDogAlertGenerator.generate_config(config)
        elif platform == Platform.CLOUDWATCH:
            output_config = CloudWatchAlertGenerator.generate_config(config)
        elif platform == Platform.PAGERDUTY:
            output_config = PagerDutyAlertGenerator.generate_config(config)
        elif platform == Platform.NEWRELIC:
            output_config = NewRelicAlertGenerator.generate_config(config)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        # Format output
        output = format_output(output_config, args.output, args.platform)

        # Write output
        if args.file:
            with open(args.file, "w") as f:
                f.write(output)
            logger.info(f"Alert rules written to {args.file}")
        else:
            print(output)

        logger.info(f"Generated {len(config.rules)} alert rules")
        return 0

    except Exception as e:
        logger.error(f"Error generating alerts: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
