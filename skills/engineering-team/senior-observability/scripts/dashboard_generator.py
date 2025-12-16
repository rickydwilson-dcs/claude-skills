#!/usr/bin/env python3
"""
Dashboard Generator
Generate monitoring dashboard configurations for Grafana, DataDog, CloudWatch, and New Relic.

Features:
- Multi-platform support (Grafana, DataDog, CloudWatch, New Relic)
- Service type templates (API, Database, Queue, Cache, Web)
- RED method panels (Rate, Errors, Duration)
- USE method panels (Utilization, Saturation, Errors)
- Variable templating for multi-service views
- Threshold configurations and annotations
- PromQL to NRQL query translation for New Relic

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
    """Supported dashboard platforms"""
    GRAFANA = "grafana"
    DATADOG = "datadog"
    CLOUDWATCH = "cloudwatch"
    NEWRELIC = "newrelic"


class ServiceType(Enum):
    """Service types with specific dashboard patterns"""
    API = "api"
    DATABASE = "database"
    QUEUE = "queue"
    CACHE = "cache"
    WEB = "web"


class PanelType(Enum):
    """Types of dashboard panels"""
    GRAPH = "graph"
    STAT = "stat"
    GAUGE = "gauge"
    TABLE = "table"
    HEATMAP = "heatmap"
    TEXT = "text"


@dataclass
class Panel:
    """Dashboard panel configuration"""
    title: str
    panel_type: PanelType
    query: str
    unit: str = ""
    thresholds: List[Dict[str, Any]] = field(default_factory=list)
    legend: bool = True
    description: str = ""
    grid_pos: Dict[str, int] = field(default_factory=dict)


@dataclass
class Variable:
    """Dashboard variable for templating"""
    name: str
    label: str
    query: str
    var_type: str = "query"
    multi: bool = False
    include_all: bool = True


@dataclass
class DashboardConfig:
    """Complete dashboard configuration"""
    title: str
    service: str
    service_type: ServiceType
    platform: Platform
    panels: List[Panel] = field(default_factory=list)
    variables: List[Variable] = field(default_factory=list)
    annotations: List[Dict[str, Any]] = field(default_factory=list)
    refresh: str = "30s"
    time_from: str = "now-1h"
    time_to: str = "now"
    tags: List[str] = field(default_factory=list)


class REDMethodPanels:
    """Generate RED method panels (Rate, Errors, Duration)"""

    @staticmethod
    def rate_panel(service: str, namespace: str = "") -> Panel:
        """Request rate panel"""
        ns_filter = f'namespace="{namespace}",' if namespace else ""
        return Panel(
            title="Request Rate",
            panel_type=PanelType.GRAPH,
            query=f'sum(rate(http_requests_total{{{ns_filter}service="{service}"}}[5m]))',
            unit="reqps",
            description="Requests per second",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 100, "color": "yellow"},
                {"value": 500, "color": "red"}
            ],
            grid_pos={"x": 0, "y": 0, "w": 8, "h": 8}
        )

    @staticmethod
    def error_rate_panel(service: str, namespace: str = "") -> Panel:
        """Error rate panel"""
        ns_filter = f'namespace="{namespace}",' if namespace else ""
        return Panel(
            title="Error Rate",
            panel_type=PanelType.GRAPH,
            query=f'sum(rate(http_requests_total{{{ns_filter}service="{service}",status=~"5.."}}[5m])) / sum(rate(http_requests_total{{{ns_filter}service="{service}"}}[5m])) * 100',
            unit="percent",
            description="Percentage of requests resulting in 5xx errors",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 1, "color": "yellow"},
                {"value": 5, "color": "red"}
            ],
            grid_pos={"x": 8, "y": 0, "w": 8, "h": 8}
        )

    @staticmethod
    def duration_panel(service: str, namespace: str = "") -> Panel:
        """Request duration panel with percentiles"""
        ns_filter = f'namespace="{namespace}",' if namespace else ""
        return Panel(
            title="Request Duration",
            panel_type=PanelType.GRAPH,
            query=f'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{{{ns_filter}service="{service}"}}[5m])) by (le))',
            unit="s",
            description="P99 request latency",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 0.5, "color": "yellow"},
                {"value": 1, "color": "red"}
            ],
            grid_pos={"x": 16, "y": 0, "w": 8, "h": 8}
        )

    @staticmethod
    def get_all_panels(service: str, namespace: str = "") -> List[Panel]:
        """Get all RED method panels"""
        return [
            REDMethodPanels.rate_panel(service, namespace),
            REDMethodPanels.error_rate_panel(service, namespace),
            REDMethodPanels.duration_panel(service, namespace)
        ]


class USEMethodPanels:
    """Generate USE method panels (Utilization, Saturation, Errors)"""

    @staticmethod
    def cpu_utilization_panel(service: str, namespace: str = "") -> Panel:
        """CPU utilization panel"""
        ns_filter = f'namespace="{namespace}",' if namespace else ""
        return Panel(
            title="CPU Utilization",
            panel_type=PanelType.GRAPH,
            query=f'sum(rate(container_cpu_usage_seconds_total{{{ns_filter}container="{service}"}}[5m])) / sum(container_spec_cpu_quota{{{ns_filter}container="{service}"}}/container_spec_cpu_period{{{ns_filter}container="{service}"}}) * 100',
            unit="percent",
            description="CPU usage as percentage of limit",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 70, "color": "yellow"},
                {"value": 90, "color": "red"}
            ],
            grid_pos={"x": 0, "y": 8, "w": 8, "h": 8}
        )

    @staticmethod
    def memory_utilization_panel(service: str, namespace: str = "") -> Panel:
        """Memory utilization panel"""
        ns_filter = f'namespace="{namespace}",' if namespace else ""
        return Panel(
            title="Memory Utilization",
            panel_type=PanelType.GRAPH,
            query=f'sum(container_memory_working_set_bytes{{{ns_filter}container="{service}"}}) / sum(container_spec_memory_limit_bytes{{{ns_filter}container="{service}"}}) * 100',
            unit="percent",
            description="Memory usage as percentage of limit",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 70, "color": "yellow"},
                {"value": 90, "color": "red"}
            ],
            grid_pos={"x": 8, "y": 8, "w": 8, "h": 8}
        )

    @staticmethod
    def saturation_panel(service: str, namespace: str = "") -> Panel:
        """Saturation panel (queue depth, thread pool)"""
        ns_filter = f'namespace="{namespace}",' if namespace else ""
        return Panel(
            title="Saturation (Queue Depth)",
            panel_type=PanelType.GRAPH,
            query=f'sum(http_server_active_requests{{{ns_filter}service="{service}"}})',
            unit="short",
            description="Number of requests currently being processed",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 50, "color": "yellow"},
                {"value": 100, "color": "red"}
            ],
            grid_pos={"x": 16, "y": 8, "w": 8, "h": 8}
        )

    @staticmethod
    def get_all_panels(service: str, namespace: str = "") -> List[Panel]:
        """Get all USE method panels"""
        return [
            USEMethodPanels.cpu_utilization_panel(service, namespace),
            USEMethodPanels.memory_utilization_panel(service, namespace),
            USEMethodPanels.saturation_panel(service, namespace)
        ]


class DatabasePanels:
    """Generate database-specific panels"""

    @staticmethod
    def connections_panel(service: str) -> Panel:
        """Active connections panel"""
        return Panel(
            title="Active Connections",
            panel_type=PanelType.GRAPH,
            query=f'pg_stat_activity_count{{datname="{service}"}}',
            unit="short",
            description="Number of active database connections",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 80, "color": "yellow"},
                {"value": 100, "color": "red"}
            ],
            grid_pos={"x": 0, "y": 16, "w": 8, "h": 8}
        )

    @staticmethod
    def query_duration_panel(service: str) -> Panel:
        """Query duration panel"""
        return Panel(
            title="Query Duration (P99)",
            panel_type=PanelType.GRAPH,
            query=f'histogram_quantile(0.99, sum(rate(pg_stat_statements_seconds_total_bucket{{datname="{service}"}}[5m])) by (le))',
            unit="s",
            description="P99 query execution time",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 0.1, "color": "yellow"},
                {"value": 1, "color": "red"}
            ],
            grid_pos={"x": 8, "y": 16, "w": 8, "h": 8}
        )

    @staticmethod
    def replication_lag_panel(service: str) -> Panel:
        """Replication lag panel"""
        return Panel(
            title="Replication Lag",
            panel_type=PanelType.GRAPH,
            query=f'pg_replication_lag{{datname="{service}"}}',
            unit="s",
            description="Replication lag in seconds",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 1, "color": "yellow"},
                {"value": 5, "color": "red"}
            ],
            grid_pos={"x": 16, "y": 16, "w": 8, "h": 8}
        )

    @staticmethod
    def disk_usage_panel(service: str) -> Panel:
        """Disk usage panel"""
        return Panel(
            title="Disk Usage",
            panel_type=PanelType.GAUGE,
            query=f'pg_database_size_bytes{{datname="{service}"}} / pg_tablespace_size_bytes * 100',
            unit="percent",
            description="Database disk usage percentage",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 70, "color": "yellow"},
                {"value": 90, "color": "red"}
            ],
            grid_pos={"x": 0, "y": 24, "w": 8, "h": 8}
        )

    @staticmethod
    def cache_hit_ratio_panel(service: str) -> Panel:
        """Cache hit ratio panel"""
        return Panel(
            title="Cache Hit Ratio",
            panel_type=PanelType.STAT,
            query=f'pg_stat_database_blks_hit{{datname="{service}"}} / (pg_stat_database_blks_hit{{datname="{service}"}} + pg_stat_database_blks_read{{datname="{service}"}}) * 100',
            unit="percent",
            description="Buffer cache hit ratio",
            thresholds=[
                {"value": 0, "color": "red"},
                {"value": 90, "color": "yellow"},
                {"value": 99, "color": "green"}
            ],
            grid_pos={"x": 8, "y": 24, "w": 8, "h": 8}
        )

    @staticmethod
    def get_all_panels(service: str) -> List[Panel]:
        """Get all database panels"""
        return [
            DatabasePanels.connections_panel(service),
            DatabasePanels.query_duration_panel(service),
            DatabasePanels.replication_lag_panel(service),
            DatabasePanels.disk_usage_panel(service),
            DatabasePanels.cache_hit_ratio_panel(service)
        ]


class QueuePanels:
    """Generate queue-specific panels"""

    @staticmethod
    def queue_depth_panel(service: str) -> Panel:
        """Queue depth panel"""
        return Panel(
            title="Queue Depth",
            panel_type=PanelType.GRAPH,
            query=f'rabbitmq_queue_messages{{queue="{service}"}}',
            unit="short",
            description="Number of messages in queue",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 1000, "color": "yellow"},
                {"value": 10000, "color": "red"}
            ],
            grid_pos={"x": 0, "y": 16, "w": 8, "h": 8}
        )

    @staticmethod
    def publish_rate_panel(service: str) -> Panel:
        """Message publish rate panel"""
        return Panel(
            title="Publish Rate",
            panel_type=PanelType.GRAPH,
            query=f'rate(rabbitmq_queue_messages_published_total{{queue="{service}"}}[5m])',
            unit="short",
            description="Messages published per second",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 100, "color": "yellow"},
                {"value": 500, "color": "red"}
            ],
            grid_pos={"x": 8, "y": 16, "w": 8, "h": 8}
        )

    @staticmethod
    def consume_rate_panel(service: str) -> Panel:
        """Message consume rate panel"""
        return Panel(
            title="Consume Rate",
            panel_type=PanelType.GRAPH,
            query=f'rate(rabbitmq_queue_messages_delivered_total{{queue="{service}"}}[5m])',
            unit="short",
            description="Messages consumed per second",
            thresholds=[
                {"value": 0, "color": "green"}
            ],
            grid_pos={"x": 16, "y": 16, "w": 8, "h": 8}
        )

    @staticmethod
    def consumer_count_panel(service: str) -> Panel:
        """Consumer count panel"""
        return Panel(
            title="Active Consumers",
            panel_type=PanelType.STAT,
            query=f'rabbitmq_queue_consumers{{queue="{service}"}}',
            unit="short",
            description="Number of active consumers",
            thresholds=[
                {"value": 0, "color": "red"},
                {"value": 1, "color": "yellow"},
                {"value": 2, "color": "green"}
            ],
            grid_pos={"x": 0, "y": 24, "w": 8, "h": 8}
        )

    @staticmethod
    def get_all_panels(service: str) -> List[Panel]:
        """Get all queue panels"""
        return [
            QueuePanels.queue_depth_panel(service),
            QueuePanels.publish_rate_panel(service),
            QueuePanels.consume_rate_panel(service),
            QueuePanels.consumer_count_panel(service)
        ]


class CachePanels:
    """Generate cache-specific panels (Redis)"""

    @staticmethod
    def hit_rate_panel(service: str) -> Panel:
        """Cache hit rate panel"""
        return Panel(
            title="Cache Hit Rate",
            panel_type=PanelType.GRAPH,
            query=f'redis_keyspace_hits_total{{instance=~".*{service}.*"}} / (redis_keyspace_hits_total{{instance=~".*{service}.*"}} + redis_keyspace_misses_total{{instance=~".*{service}.*"}}) * 100',
            unit="percent",
            description="Cache hit ratio",
            thresholds=[
                {"value": 0, "color": "red"},
                {"value": 80, "color": "yellow"},
                {"value": 95, "color": "green"}
            ],
            grid_pos={"x": 0, "y": 16, "w": 8, "h": 8}
        )

    @staticmethod
    def memory_usage_panel(service: str) -> Panel:
        """Memory usage panel"""
        return Panel(
            title="Memory Usage",
            panel_type=PanelType.GRAPH,
            query=f'redis_memory_used_bytes{{instance=~".*{service}.*"}} / redis_memory_max_bytes{{instance=~".*{service}.*"}} * 100',
            unit="percent",
            description="Memory usage as percentage of maxmemory",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 70, "color": "yellow"},
                {"value": 90, "color": "red"}
            ],
            grid_pos={"x": 8, "y": 16, "w": 8, "h": 8}
        )

    @staticmethod
    def connections_panel(service: str) -> Panel:
        """Connected clients panel"""
        return Panel(
            title="Connected Clients",
            panel_type=PanelType.GRAPH,
            query=f'redis_connected_clients{{instance=~".*{service}.*"}}',
            unit="short",
            description="Number of connected clients",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 100, "color": "yellow"},
                {"value": 500, "color": "red"}
            ],
            grid_pos={"x": 16, "y": 16, "w": 8, "h": 8}
        )

    @staticmethod
    def evictions_panel(service: str) -> Panel:
        """Key evictions panel"""
        return Panel(
            title="Key Evictions",
            panel_type=PanelType.GRAPH,
            query=f'rate(redis_evicted_keys_total{{instance=~".*{service}.*"}}[5m])',
            unit="short",
            description="Keys evicted per second",
            thresholds=[
                {"value": 0, "color": "green"},
                {"value": 1, "color": "yellow"},
                {"value": 10, "color": "red"}
            ],
            grid_pos={"x": 0, "y": 24, "w": 8, "h": 8}
        )

    @staticmethod
    def get_all_panels(service: str) -> List[Panel]:
        """Get all cache panels"""
        return [
            CachePanels.hit_rate_panel(service),
            CachePanels.memory_usage_panel(service),
            CachePanels.connections_panel(service),
            CachePanels.evictions_panel(service)
        ]


class GrafanaGenerator:
    """Generate Grafana dashboard JSON"""

    @staticmethod
    def generate_panel(panel: Panel, panel_id: int) -> Dict[str, Any]:
        """Convert Panel to Grafana panel JSON"""
        base_panel = {
            "id": panel_id,
            "title": panel.title,
            "type": panel.panel_type.value if panel.panel_type != PanelType.GRAPH else "timeseries",
            "description": panel.description,
            "gridPos": panel.grid_pos,
            "targets": [
                {
                    "expr": panel.query,
                    "legendFormat": "{{instance}}",
                    "refId": "A"
                }
            ],
            "fieldConfig": {
                "defaults": {
                    "unit": panel.unit,
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"value": t["value"], "color": t["color"]}
                            for t in panel.thresholds
                        ]
                    }
                }
            },
            "options": {
                "legend": {
                    "displayMode": "list" if panel.legend else "hidden",
                    "placement": "bottom"
                }
            }
        }
        return base_panel

    @staticmethod
    def generate_variable(var: Variable) -> Dict[str, Any]:
        """Convert Variable to Grafana variable JSON"""
        return {
            "name": var.name,
            "label": var.label,
            "type": var.var_type,
            "query": var.query,
            "multi": var.multi,
            "includeAll": var.include_all,
            "refresh": 1
        }

    @staticmethod
    def generate_dashboard(config: DashboardConfig) -> Dict[str, Any]:
        """Generate complete Grafana dashboard JSON"""
        panels = []
        for i, panel in enumerate(config.panels):
            panels.append(GrafanaGenerator.generate_panel(panel, i + 1))

        variables = []
        for var in config.variables:
            variables.append(GrafanaGenerator.generate_variable(var))

        dashboard = {
            "title": config.title,
            "uid": f"{config.service}-dashboard",
            "tags": config.tags + [config.service_type.value, "observability"],
            "timezone": "browser",
            "refresh": config.refresh,
            "time": {
                "from": config.time_from,
                "to": config.time_to
            },
            "templating": {
                "list": variables
            },
            "annotations": {
                "list": config.annotations or [
                    {
                        "name": "Deployments",
                        "datasource": "Prometheus",
                        "enable": True,
                        "expr": f'changes(kube_deployment_status_observed_generation{{deployment="{config.service}"}}[1m]) > 0',
                        "titleFormat": "Deployment",
                        "textFormat": "New deployment detected"
                    }
                ]
            },
            "panels": panels,
            "schemaVersion": 38,
            "version": 1
        }
        return dashboard


class DataDogGenerator:
    """Generate DataDog dashboard JSON"""

    @staticmethod
    def generate_widget(panel: Panel) -> Dict[str, Any]:
        """Convert Panel to DataDog widget JSON"""
        widget_type_map = {
            PanelType.GRAPH: "timeseries",
            PanelType.STAT: "query_value",
            PanelType.GAUGE: "gauge",
            PanelType.TABLE: "query_table",
            PanelType.HEATMAP: "heatmap"
        }

        return {
            "definition": {
                "title": panel.title,
                "type": widget_type_map.get(panel.panel_type, "timeseries"),
                "requests": [
                    {
                        "q": panel.query.replace("{", "(").replace("}", ")"),  # DataDog syntax
                        "display_type": "line"
                    }
                ],
                "yaxis": {
                    "scale": "linear"
                }
            },
            "layout": {
                "x": panel.grid_pos.get("x", 0),
                "y": panel.grid_pos.get("y", 0),
                "width": panel.grid_pos.get("w", 4),
                "height": panel.grid_pos.get("h", 2)
            }
        }

    @staticmethod
    def generate_dashboard(config: DashboardConfig) -> Dict[str, Any]:
        """Generate complete DataDog dashboard JSON"""
        widgets = []
        for panel in config.panels:
            widgets.append(DataDogGenerator.generate_widget(panel))

        dashboard = {
            "title": config.title,
            "description": f"Dashboard for {config.service} ({config.service_type.value})",
            "widgets": widgets,
            "template_variables": [
                {
                    "name": var.name,
                    "prefix": var.name,
                    "available_values": [],
                    "default": "*"
                }
                for var in config.variables
            ],
            "layout_type": "ordered",
            "is_read_only": False,
            "notify_list": [],
            "reflow_type": "fixed"
        }
        return dashboard


class CloudWatchGenerator:
    """Generate CloudWatch dashboard JSON"""

    @staticmethod
    def generate_widget(panel: Panel, region: str = "us-east-1") -> Dict[str, Any]:
        """Convert Panel to CloudWatch widget JSON"""
        widget_type_map = {
            PanelType.GRAPH: "metric",
            PanelType.STAT: "metric",
            PanelType.GAUGE: "metric",
            PanelType.TEXT: "text"
        }

        return {
            "type": widget_type_map.get(panel.panel_type, "metric"),
            "x": panel.grid_pos.get("x", 0),
            "y": panel.grid_pos.get("y", 0),
            "width": panel.grid_pos.get("w", 6),
            "height": panel.grid_pos.get("h", 6),
            "properties": {
                "title": panel.title,
                "view": "timeSeries" if panel.panel_type == PanelType.GRAPH else "singleValue",
                "stacked": False,
                "region": region,
                "metrics": [
                    # CloudWatch metrics would need to be adapted from Prometheus queries
                    ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", panel.query]
                ],
                "period": 300
            }
        }

    @staticmethod
    def generate_dashboard(config: DashboardConfig) -> Dict[str, Any]:
        """Generate complete CloudWatch dashboard JSON"""
        widgets = []
        for panel in config.panels:
            widgets.append(CloudWatchGenerator.generate_widget(panel))

        dashboard = {
            "widgets": widgets
        }
        return dashboard


class NewRelicGenerator:
    """Generate New Relic dashboard JSON using NerdGraph API format"""

    # PromQL to NRQL query translation patterns
    QUERY_TRANSLATIONS = {
        # RED Method translations
        "http_requests_total": "Transaction",
        "http_request_duration_seconds": "Transaction",
        "container_cpu_usage_seconds_total": "SystemSample",
        "container_memory_working_set_bytes": "SystemSample",
        "container_spec_memory_limit_bytes": "SystemSample",
        "container_spec_cpu_quota": "SystemSample",
        "http_server_active_requests": "Transaction",
        # Database translations
        "pg_stat_activity_count": "PostgresqlDatabaseSample",
        "pg_replication_lag": "PostgresqlDatabaseSample",
        "pg_database_size_bytes": "PostgresqlDatabaseSample",
        # Queue translations
        "rabbitmq_queue_messages": "RabbitmqQueueSample",
        "rabbitmq_queue_consumers": "RabbitmqQueueSample",
        # Cache translations
        "redis_keyspace_hits_total": "RedisSample",
        "redis_memory_used_bytes": "RedisSample",
        "redis_connected_clients": "RedisSample",
    }

    @staticmethod
    def translate_promql_to_nrql(promql: str, service: str) -> str:
        """
        Translate PromQL query to NRQL.

        This handles common patterns:
        - rate(metric[5m]) -> rate(count(*), 5 minutes)
        - sum(rate(...)) -> SELECT sum(count(*)) ... TIMESERIES
        - histogram_quantile(0.99, ...) -> percentile(duration, 99)
        - Label filters {service="x"} -> WHERE appName = 'x'
        """
        # Determine the event type based on metric patterns
        event_type = "Transaction"
        for metric, event in NewRelicGenerator.QUERY_TRANSLATIONS.items():
            if metric in promql:
                event_type = event
                break

        # Handle different query patterns
        if "histogram_quantile" in promql:
            # P99/P95 latency queries
            if "0.99" in promql:
                return f"SELECT percentile(duration, 99) FROM {event_type} WHERE appName = '{service}' TIMESERIES"
            elif "0.95" in promql:
                return f"SELECT percentile(duration, 95) FROM {event_type} WHERE appName = '{service}' TIMESERIES"
            elif "0.50" in promql or "0.5" in promql:
                return f"SELECT percentile(duration, 50) FROM {event_type} WHERE appName = '{service}' TIMESERIES"
            else:
                return f"SELECT percentile(duration, 99) FROM {event_type} WHERE appName = '{service}' TIMESERIES"

        elif 'status=~"5.."' in promql or "status=~'5..'" in promql:
            # Error rate queries
            if "/" in promql and "* 100" in promql:
                return f"SELECT percentage(count(*), WHERE error IS true) FROM {event_type} WHERE appName = '{service}' TIMESERIES"
            else:
                return f"SELECT filter(count(*), WHERE httpResponseCode LIKE '5%') FROM {event_type} WHERE appName = '{service}' TIMESERIES"

        elif "rate(" in promql and "http_requests" in promql:
            # Request rate queries
            return f"SELECT rate(count(*), 5 minutes) FROM {event_type} WHERE appName = '{service}' TIMESERIES"

        elif "container_cpu_usage" in promql:
            # CPU utilization
            return f"SELECT average(cpuPercent) FROM {event_type} WHERE appName = '{service}' OR hostname LIKE '%{service}%' TIMESERIES"

        elif "container_memory" in promql or "memory_working_set" in promql:
            # Memory utilization
            return f"SELECT average(memoryUsedPercent) FROM {event_type} WHERE appName = '{service}' OR hostname LIKE '%{service}%' TIMESERIES"

        elif "http_server_active_requests" in promql:
            # Active requests / saturation
            return f"SELECT average(duration) * rate(count(*), 1 minute) as 'concurrent_requests' FROM {event_type} WHERE appName = '{service}' TIMESERIES"

        elif "pg_stat_activity" in promql:
            # PostgreSQL connections
            return f"SELECT latest(postgresql.connections) FROM PostgresqlDatabaseSample WHERE database = '{service}' TIMESERIES"

        elif "pg_replication_lag" in promql:
            # PostgreSQL replication lag
            return f"SELECT latest(postgresql.replication.lagBytes) FROM PostgresqlDatabaseSample WHERE database = '{service}' TIMESERIES"

        elif "pg_database_size" in promql:
            # PostgreSQL disk usage
            return f"SELECT latest(postgresql.database.sizeBytes) FROM PostgresqlDatabaseSample WHERE database = '{service}' TIMESERIES"

        elif "rabbitmq_queue_messages" in promql:
            # RabbitMQ queue depth
            return f"SELECT latest(queue.messages) FROM RabbitmqQueueSample WHERE queue.name = '{service}' TIMESERIES"

        elif "rabbitmq_queue_consumers" in promql:
            # RabbitMQ consumers
            return f"SELECT latest(queue.consumers) FROM RabbitmqQueueSample WHERE queue.name = '{service}' TIMESERIES"

        elif "redis_keyspace_hits" in promql:
            # Redis hit rate
            return f"SELECT (latest(db.keyspace.hits) / (latest(db.keyspace.hits) + latest(db.keyspace.misses))) * 100 as 'hit_rate' FROM RedisSample WHERE instance LIKE '%{service}%' TIMESERIES"

        elif "redis_memory_used" in promql:
            # Redis memory usage
            return f"SELECT latest(redis.memoryUsedBytes) / latest(redis.memoryMaxBytes) * 100 as 'memory_percent' FROM RedisSample WHERE instance LIKE '%{service}%' TIMESERIES"

        elif "redis_connected_clients" in promql:
            # Redis connections
            return f"SELECT latest(redis.connectedClients) FROM RedisSample WHERE instance LIKE '%{service}%' TIMESERIES"

        elif "redis_evicted_keys" in promql:
            # Redis evictions
            return f"SELECT rate(sum(redis.evictedKeys), 5 minutes) FROM RedisSample WHERE instance LIKE '%{service}%' TIMESERIES"

        else:
            # Fallback: generic transaction query
            return f"SELECT count(*) FROM {event_type} WHERE appName = '{service}' TIMESERIES"

    @staticmethod
    def generate_widget(panel: Panel, service: str) -> Dict[str, Any]:
        """Convert Panel to New Relic widget JSON"""
        # Map panel types to New Relic visualization IDs
        viz_type_map = {
            PanelType.GRAPH: "viz.line",
            PanelType.STAT: "viz.billboard",
            PanelType.GAUGE: "viz.bullet",
            PanelType.TABLE: "viz.table",
            PanelType.HEATMAP: "viz.heatmap",
            PanelType.TEXT: "viz.markdown"
        }

        # Translate PromQL to NRQL
        nrql_query = NewRelicGenerator.translate_promql_to_nrql(panel.query, service)

        # Build widget configuration
        widget = {
            "title": panel.title,
            "visualization": {
                "id": viz_type_map.get(panel.panel_type, "viz.line")
            },
            "configuration": {
                "nrqlQueries": [
                    {
                        "accountIds": ["{{ACCOUNT_ID}}"],
                        "query": nrql_query
                    }
                ]
            },
            "rawConfiguration": {
                "nrqlQueries": [
                    {
                        "accountId": "{{ACCOUNT_ID}}",
                        "query": nrql_query
                    }
                ],
                "legend": {
                    "enabled": panel.legend
                },
                "yAxisLeft": {
                    "zero": True
                }
            },
            "layout": {
                "column": (panel.grid_pos.get("x", 0) // 8) + 1,  # Convert to 1-indexed columns
                "row": (panel.grid_pos.get("y", 0) // 8) + 1,    # Convert to 1-indexed rows
                "width": min(panel.grid_pos.get("w", 4) // 2, 12),  # Scale to 12-column grid
                "height": max(panel.grid_pos.get("h", 3) // 2, 3)   # Minimum height of 3
            }
        }

        # Add thresholds for billboard/gauge widgets
        if panel.panel_type in [PanelType.STAT, PanelType.GAUGE] and panel.thresholds:
            widget["rawConfiguration"]["thresholds"] = []
            for threshold in panel.thresholds:
                widget["rawConfiguration"]["thresholds"].append({
                    "value": threshold.get("value", 0),
                    "severity": "critical" if threshold.get("color") == "red" else "warning" if threshold.get("color") == "yellow" else "normal"
                })

        return widget

    @staticmethod
    def generate_dashboard(config: DashboardConfig) -> Dict[str, Any]:
        """Generate complete New Relic dashboard JSON (NerdGraph API format)"""
        widgets = []
        for panel in config.panels:
            widgets.append(NewRelicGenerator.generate_widget(panel, config.service))

        dashboard = {
            "__comment": "New Relic Dashboard - Import via NerdGraph API or UI",
            "__usage": "Replace {{ACCOUNT_ID}} with your New Relic account ID",
            "name": config.title,
            "description": f"Observability dashboard for {config.service} ({config.service_type.value})",
            "permissions": "PUBLIC_READ_WRITE",
            "pages": [
                {
                    "name": f"{config.service} Overview",
                    "description": f"Service health metrics using {config.service_type.value.upper()} patterns",
                    "widgets": widgets
                }
            ],
            "variables": [
                {
                    "name": var.name,
                    "title": var.label,
                    "type": "NRQL",
                    "nrqlQuery": {
                        "accountIds": ["{{ACCOUNT_ID}}"],
                        "query": f"SELECT uniques({var.name}) FROM Transaction WHERE appName = '{config.service}'"
                    },
                    "isMultiSelection": var.multi,
                    "defaultValues": [{"value": {"string": "*"}}] if var.include_all else []
                }
                for var in config.variables
            ]
        }

        return dashboard


class DashboardBuilder:
    """Build dashboards for different service types"""

    def __init__(self, service: str, service_type: ServiceType, platform: Platform):
        self.service = service
        self.service_type = service_type
        self.platform = platform
        self.config = DashboardConfig(
            title=f"{service} Dashboard",
            service=service,
            service_type=service_type,
            platform=platform,
            tags=[service, service_type.value]
        )

    def add_red_panels(self, namespace: str = "") -> "DashboardBuilder":
        """Add RED method panels"""
        self.config.panels.extend(REDMethodPanels.get_all_panels(self.service, namespace))
        return self

    def add_use_panels(self, namespace: str = "") -> "DashboardBuilder":
        """Add USE method panels"""
        self.config.panels.extend(USEMethodPanels.get_all_panels(self.service, namespace))
        return self

    def add_database_panels(self) -> "DashboardBuilder":
        """Add database-specific panels"""
        self.config.panels.extend(DatabasePanels.get_all_panels(self.service))
        return self

    def add_queue_panels(self) -> "DashboardBuilder":
        """Add queue-specific panels"""
        self.config.panels.extend(QueuePanels.get_all_panels(self.service))
        return self

    def add_cache_panels(self) -> "DashboardBuilder":
        """Add cache-specific panels"""
        self.config.panels.extend(CachePanels.get_all_panels(self.service))
        return self

    def add_standard_variables(self) -> "DashboardBuilder":
        """Add standard dashboard variables"""
        self.config.variables = [
            Variable(
                name="namespace",
                label="Namespace",
                query='label_values(kube_namespace_labels, namespace)',
                multi=True
            ),
            Variable(
                name="instance",
                label="Instance",
                query=f'label_values(up{{job="{self.service}"}}, instance)',
                multi=True
            )
        ]
        return self

    def build_for_service_type(self) -> "DashboardBuilder":
        """Add panels appropriate for the service type"""
        self.add_standard_variables()

        if self.service_type == ServiceType.API:
            self.add_red_panels()
            self.add_use_panels()
        elif self.service_type == ServiceType.DATABASE:
            self.add_use_panels()
            self.add_database_panels()
        elif self.service_type == ServiceType.QUEUE:
            self.add_use_panels()
            self.add_queue_panels()
        elif self.service_type == ServiceType.CACHE:
            self.add_use_panels()
            self.add_cache_panels()
        elif self.service_type == ServiceType.WEB:
            self.add_red_panels()
            self.add_use_panels()

        return self

    def generate(self) -> Dict[str, Any]:
        """Generate the dashboard in the target platform format"""
        if self.platform == Platform.GRAFANA:
            return GrafanaGenerator.generate_dashboard(self.config)
        elif self.platform == Platform.DATADOG:
            return DataDogGenerator.generate_dashboard(self.config)
        elif self.platform == Platform.CLOUDWATCH:
            return CloudWatchGenerator.generate_dashboard(self.config)
        elif self.platform == Platform.NEWRELIC:
            return NewRelicGenerator.generate_dashboard(self.config)
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")


def format_output(dashboard: Dict[str, Any], output_format: str) -> str:
    """Format dashboard output"""
    if output_format == "json":
        return json.dumps(dashboard, indent=2)
    elif output_format == "yaml":
        # Simple YAML-like output without external dependency
        def to_yaml(obj: Any, indent: int = 0) -> str:
            prefix = "  " * indent
            if isinstance(obj, dict):
                lines = []
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        lines.append(f"{prefix}{k}:")
                        lines.append(to_yaml(v, indent + 1))
                    else:
                        lines.append(f"{prefix}{k}: {json.dumps(v)}")
                return "\n".join(lines)
            elif isinstance(obj, list):
                lines = []
                for item in obj:
                    if isinstance(item, (dict, list)):
                        lines.append(f"{prefix}-")
                        lines.append(to_yaml(item, indent + 1))
                    else:
                        lines.append(f"{prefix}- {json.dumps(item)}")
                return "\n".join(lines)
            else:
                return f"{prefix}{json.dumps(obj)}"
        return to_yaml(dashboard)
    else:  # text
        # Detect platform from dashboard structure
        is_newrelic = "pages" in dashboard
        is_grafana = "uid" in dashboard
        is_datadog = "layout_type" in dashboard

        if is_newrelic:
            platform_name = "New Relic"
            title = dashboard.get("name", "Unknown")
        else:
            platform_name = "Grafana" if is_grafana else "DataDog" if is_datadog else "CloudWatch"
            title = dashboard.get("title", "Unknown")

        lines = [
            "=" * 60,
            f"Dashboard: {title}",
            "=" * 60,
            "",
            f"Platform: {platform_name}",
            f"Tags: {', '.join(dashboard.get('tags', []))}",
            f"Refresh: {dashboard.get('refresh', 'N/A')}",
            "",
            "-" * 60,
            "Panels/Widgets:",
            "-" * 60
        ]

        # Handle New Relic page-based structure
        if is_newrelic:
            for page in dashboard.get("pages", []):
                lines.append(f"  Page: {page.get('name', 'Unknown')}")
                for i, widget in enumerate(page.get("widgets", []), 1):
                    lines.append(f"    {i}. {widget.get('title', 'Unknown')}")
        else:
            panels = dashboard.get("panels", dashboard.get("widgets", []))
            for i, panel in enumerate(panels, 1):
                title = panel.get("title") or panel.get("definition", {}).get("title", "Unknown")
                lines.append(f"  {i}. {title}")

        lines.extend([
            "",
            "-" * 60,
            "Variables:",
            "-" * 60
        ])

        # Handle New Relic variables structure
        if is_newrelic:
            variables = dashboard.get("variables", [])
            for var in variables:
                lines.append(f"  - {var.get('name', 'Unknown')}: {var.get('title', '')}")
        else:
            variables = dashboard.get("templating", {}).get("list", [])
            variables = variables or dashboard.get("template_variables", [])
            for var in variables:
                lines.append(f"  - {var.get('name', 'Unknown')}: {var.get('label', var.get('prefix', ''))}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate monitoring dashboards for Grafana, DataDog, CloudWatch, or New Relic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Grafana dashboard for API service
  %(prog)s --service payment-api --type api --platform grafana --output json

  # Generate DataDog dashboard for database
  %(prog)s --service postgres-main --type database --platform datadog --output json

  # Generate CloudWatch dashboard for cache
  %(prog)s --service redis-cache --type cache --platform cloudwatch --output json

  # Generate New Relic dashboard for API service (NRQL)
  %(prog)s --service pandora-api --type api --platform newrelic --output json

  # Save dashboard to file
  %(prog)s --service my-api --type api --platform grafana --output json --file dashboard.json

Service Types:
  api       - HTTP/REST API services (RED method)
  database  - PostgreSQL, MySQL, etc. (USE method + DB metrics)
  queue     - RabbitMQ, Kafka, SQS (queue depth, throughput)
  cache     - Redis, Memcached (hit rate, memory)
  web       - Frontend applications (RED method)

Platforms:
  grafana   - Grafana dashboards with PromQL queries
  datadog   - DataDog dashboards with custom metrics
  cloudwatch - AWS CloudWatch dashboards
  newrelic  - New Relic One dashboards with NRQL queries
        """
    )

    parser.add_argument(
        "--service", "-s",
        required=True,
        help="Service name for the dashboard"
    )

    parser.add_argument(
        "--type", "-t",
        choices=[t.value for t in ServiceType],
        default="api",
        help="Service type (default: api)"
    )

    parser.add_argument(
        "--platform", "-p",
        choices=[p.value for p in Platform],
        default="grafana",
        help="Target dashboard platform (default: grafana)"
    )

    parser.add_argument(
        "--output", "-o",
        choices=["json", "yaml", "text"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--file", "-f",
        help="Write output to file instead of stdout"
    )

    parser.add_argument(
        "--namespace", "-n",
        default="",
        help="Kubernetes namespace filter (optional)"
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
        # Build dashboard
        logger.info(f"Generating {args.platform} dashboard for {args.service} ({args.type})")

        builder = DashboardBuilder(
            service=args.service,
            service_type=ServiceType(args.type),
            platform=Platform(args.platform)
        )

        builder.build_for_service_type()
        dashboard = builder.generate()

        # Format output
        output = format_output(dashboard, args.output)

        # Write output
        if args.file:
            with open(args.file, "w") as f:
                f.write(output)
            logger.info(f"Dashboard written to {args.file}")
        else:
            print(output)

        logger.info("Dashboard generation complete")
        return 0

    except Exception as e:
        logger.error(f"Error generating dashboard: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
