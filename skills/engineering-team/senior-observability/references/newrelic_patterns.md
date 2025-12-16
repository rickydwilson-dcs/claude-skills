# New Relic Observability Patterns

## Overview

New Relic is a comprehensive observability platform that provides APM (Application Performance Monitoring), infrastructure monitoring, log management, and distributed tracing in a unified experience. This guide covers NRQL query patterns, dashboard design, alerting strategies, and best practices for New Relic implementations.

---

## Architecture

### New Relic Components

| Component | Purpose | Data Sources |
|-----------|---------|--------------|
| **APM** | Application performance | APM agents (Java, Node.js, Python, .NET, Go, Ruby, PHP) |
| **Infrastructure** | Host/container metrics | Infrastructure agent, cloud integrations |
| **Logs** | Centralized logging | Log forwarders, APM context |
| **Browser** | Frontend RUM | Browser agent (JavaScript) |
| **Mobile** | Mobile app monitoring | iOS/Android SDKs |
| **Synthetics** | Uptime monitoring | Synthetic monitors |
| **Distributed Tracing** | Request tracing | APM agents with trace context |

### Data Model

New Relic stores data as **events** in NRDB (New Relic Database):

```
Event Types:
├── Transaction         # APM web/background transactions
├── TransactionError    # Application errors
├── Span               # Distributed trace spans
├── SystemSample       # Infrastructure host metrics
├── ProcessSample      # Process-level metrics
├── ContainerSample    # Container metrics
├── K8sClusterSample   # Kubernetes cluster metrics
├── Log                # Log events
└── Custom Events      # Application-specific events
```

---

## NRQL Query Language

### Basic Syntax

```sql
SELECT [aggregation] FROM [event_type]
WHERE [conditions]
SINCE [time_range]
FACET [grouping]
TIMESERIES [bucket_size]
```

### Core Functions

| Function | Description | Example |
|----------|-------------|---------|
| `count(*)` | Count events | `SELECT count(*) FROM Transaction` |
| `average(attr)` | Average value | `SELECT average(duration) FROM Transaction` |
| `sum(attr)` | Sum values | `SELECT sum(totalTime) FROM Transaction` |
| `max(attr)` / `min(attr)` | Max/min values | `SELECT max(duration) FROM Transaction` |
| `percentile(attr, N)` | Nth percentile | `SELECT percentile(duration, 99) FROM Transaction` |
| `rate(count(*), N)` | Rate per time | `SELECT rate(count(*), 1 minute) FROM Transaction` |
| `percentage(count(*), WHERE)` | Percentage with filter | `SELECT percentage(count(*), WHERE error IS true)` |
| `filter(count(*), WHERE)` | Filtered count | `SELECT filter(count(*), WHERE httpResponseCode >= 500)` |
| `uniqueCount(attr)` | Distinct count | `SELECT uniqueCount(userId) FROM Transaction` |
| `latest(attr)` | Most recent value | `SELECT latest(cpuPercent) FROM SystemSample` |

### Time Functions

```sql
-- Relative time ranges
SINCE 1 hour ago
SINCE 30 minutes ago UNTIL 15 minutes ago
SINCE '2024-01-15 09:00:00'

-- Time series bucketing
TIMESERIES              -- Auto bucket
TIMESERIES 1 minute     -- 1-minute buckets
TIMESERIES AUTO         -- Automatic bucketing
TIMESERIES MAX          -- Maximum data points
```

---

## Four Golden Signals in NRQL

### 1. Latency (Request Duration)

```sql
-- Average latency
SELECT average(duration) FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES

-- P99 latency
SELECT percentile(duration, 99) FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES

-- Latency distribution
SELECT histogram(duration, 10, 20) FROM Transaction
WHERE appName = 'pandora-api' SINCE 1 hour ago

-- Latency by endpoint
SELECT average(duration), percentile(duration, 99)
FROM Transaction
WHERE appName = 'pandora-api'
FACET request.uri SINCE 1 hour ago
```

### 2. Traffic (Request Rate)

```sql
-- Requests per minute
SELECT rate(count(*), 1 minute) FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES

-- Requests by endpoint
SELECT count(*) FROM Transaction
WHERE appName = 'pandora-api'
FACET request.uri TIMESERIES

-- Throughput by response code
SELECT count(*) FROM Transaction
WHERE appName = 'pandora-api'
FACET httpResponseCode TIMESERIES

-- Peak traffic hours
SELECT count(*) FROM Transaction
WHERE appName = 'pandora-api'
FACET hourOf(timestamp) SINCE 7 days ago
```

### 3. Errors (Error Rate)

```sql
-- Error percentage
SELECT percentage(count(*), WHERE error IS true)
FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES

-- Error count by type
SELECT count(*) FROM TransactionError
WHERE appName = 'pandora-api'
FACET error.class TIMESERIES

-- 5xx error rate
SELECT filter(count(*), WHERE httpResponseCode >= 500) / count(*) * 100
AS 'Error Rate %'
FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES

-- Error details
SELECT count(*), latest(error.message) FROM TransactionError
WHERE appName = 'pandora-api'
FACET error.class, error.message
SINCE 1 hour ago LIMIT 20
```

### 4. Saturation (Resource Utilization)

```sql
-- CPU utilization
SELECT average(cpuPercent) FROM SystemSample
WHERE hostname LIKE '%pandora%' TIMESERIES

-- Memory utilization
SELECT average(memoryUsedPercent) FROM SystemSample
WHERE hostname LIKE '%pandora%' TIMESERIES

-- Disk utilization
SELECT average(diskUsedPercent) FROM SystemSample
WHERE hostname LIKE '%pandora%' FACET device TIMESERIES

-- Container CPU
SELECT average(cpuLimitPercent) FROM ContainerSample
WHERE containerName LIKE '%pandora%' TIMESERIES

-- Connection pool saturation
SELECT average(databaseCallCount) FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES
```

---

## RED Method Queries

### Rate

```sql
-- Overall request rate
SELECT rate(count(*), 1 minute) as 'Requests/min'
FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES

-- Rate by transaction type
SELECT rate(count(*), 1 minute) FROM Transaction
WHERE appName = 'pandora-api'
FACET transactionType TIMESERIES
```

### Errors

```sql
-- Error rate percentage
SELECT percentage(count(*), WHERE error IS true) as 'Error Rate %'
FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES

-- Apdex score (combines errors and latency)
SELECT apdex(duration, 0.5) FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES
```

### Duration

```sql
-- Response time percentiles
SELECT percentile(duration, 50, 90, 95, 99)
FROM Transaction
WHERE appName = 'pandora-api' TIMESERIES

-- Slowest transactions
SELECT average(duration), count(*) FROM Transaction
WHERE appName = 'pandora-api'
FACET name
SINCE 1 hour ago
ORDER BY average(duration) DESC LIMIT 10
```

---

## USE Method Queries

### Utilization

```sql
-- CPU utilization
SELECT average(cpuPercent) as 'CPU %'
FROM SystemSample
WHERE hostname LIKE '%pandora%' TIMESERIES

-- Memory utilization
SELECT average(memoryUsedBytes) / average(memoryTotalBytes) * 100 as 'Memory %'
FROM SystemSample
WHERE hostname LIKE '%pandora%' TIMESERIES

-- Disk I/O utilization
SELECT average(diskUtilizationPercent) FROM SystemSample
WHERE hostname LIKE '%pandora%' FACET device TIMESERIES

-- Network utilization
SELECT average(receiveBytesPerSecond) + average(transmitBytesPerSecond)
as 'Network Bytes/s'
FROM SystemSample
WHERE hostname LIKE '%pandora%' TIMESERIES
```

### Saturation

```sql
-- CPU saturation (load average vs cores)
SELECT average(loadAverageOneMinute) / uniqueCount(coreCount) as 'Load per Core'
FROM SystemSample
WHERE hostname LIKE '%pandora%' TIMESERIES

-- Memory pressure (swap usage)
SELECT average(swapUsedBytes) / average(swapTotalBytes) * 100 as 'Swap %'
FROM SystemSample
WHERE hostname LIKE '%pandora%' TIMESERIES

-- Disk queue depth
SELECT average(diskQueueDepth) FROM SystemSample
WHERE hostname LIKE '%pandora%' FACET device TIMESERIES
```

### Errors

```sql
-- System errors from logs
SELECT count(*) FROM Log
WHERE hostname LIKE '%pandora%' AND level = 'ERROR'
FACET message TIMESERIES

-- Disk errors
SELECT count(*) FROM SystemSample
WHERE hostname LIKE '%pandora%' AND diskReadUtilizationPercent > 90
TIMESERIES
```

---

## Dashboard Design

### Widget Types

| Widget | Visualization ID | Use Case |
|--------|-----------------|----------|
| Line chart | `viz.line` | Time series trends |
| Area chart | `viz.area` | Stacked metrics |
| Billboard | `viz.billboard` | Single KPI values |
| Table | `viz.table` | Detailed breakdowns |
| Bar chart | `viz.bar` | Comparisons |
| Pie chart | `viz.pie` | Distribution |
| Heatmap | `viz.heatmap` | Density visualization |
| Histogram | `viz.histogram` | Distribution analysis |
| Markdown | `viz.markdown` | Documentation/notes |
| Bullet | `viz.bullet` | Progress toward target |

### Dashboard JSON Structure

```json
{
  "name": "Service Overview",
  "description": "RED method metrics for service",
  "permissions": "PUBLIC_READ_WRITE",
  "pages": [
    {
      "name": "Overview",
      "widgets": [
        {
          "title": "Request Rate",
          "visualization": { "id": "viz.line" },
          "rawConfiguration": {
            "nrqlQueries": [
              {
                "accountId": 123456,
                "query": "SELECT rate(count(*), 1 minute) FROM Transaction WHERE appName = 'my-service' TIMESERIES"
              }
            ],
            "yAxisLeft": { "zero": true },
            "legend": { "enabled": true }
          },
          "layout": {
            "column": 1,
            "row": 1,
            "width": 4,
            "height": 3
          }
        }
      ]
    }
  ],
  "variables": [
    {
      "name": "environment",
      "title": "Environment",
      "type": "NRQL",
      "nrqlQuery": {
        "accountIds": [123456],
        "query": "SELECT uniques(tags.env) FROM Transaction"
      },
      "isMultiSelection": false
    }
  ]
}
```

### Dashboard Best Practices

1. **Layout**: Use 12-column grid, group related metrics
2. **Colors**: Use consistent color schemes for severity
3. **Thresholds**: Configure billboard thresholds for at-a-glance status
4. **Variables**: Add filter variables for environment, service, region
5. **Time picker**: Enable time range selection
6. **Annotations**: Add deployment markers

---

## Alerting Strategies

### Alert Condition Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Static** | Fixed threshold | CPU > 80%, Error rate > 5% |
| **Baseline** | Anomaly detection | Unusual traffic patterns |
| **Outlier** | Group comparison | Instance behaving differently |
| **NRQL** | Custom queries | Complex business logic |

### NRQL Alert Examples

```sql
-- High error rate alert
SELECT percentage(count(*), WHERE error IS true)
FROM Transaction
WHERE appName = 'pandora-api'

-- Latency degradation
SELECT percentile(duration, 99)
FROM Transaction
WHERE appName = 'pandora-api'

-- Traffic drop (potential outage)
SELECT count(*)
FROM Transaction
WHERE appName = 'pandora-api'

-- Apdex below target
SELECT apdex(duration, 0.5)
FROM Transaction
WHERE appName = 'pandora-api'
```

### Multi-Burn-Rate SLO Alerts

```sql
-- Fast burn (2% of 30-day budget in 1 hour) - Critical
SELECT percentage(count(*), WHERE error IS true)
FROM Transaction
WHERE appName = 'pandora-api'
-- Threshold: 14.4 * (100 - 99.9) / 100 = 0.144% error rate

-- Slow burn (10% of 30-day budget in 3 days) - Warning
SELECT percentage(count(*), WHERE error IS true)
FROM Transaction
WHERE appName = 'pandora-api'
-- Threshold: 1.0 * (100 - 99.9) / 100 = 0.1% error rate
```

### Alert Policy Configuration

```json
{
  "policy": {
    "name": "pandora-api SLO Alerts",
    "incident_preference": "PER_CONDITION_AND_TARGET"
  },
  "conditions": [
    {
      "name": "High Error Rate",
      "type": "NRQL",
      "enabled": true,
      "nrql": {
        "query": "SELECT percentage(count(*), WHERE error IS true) FROM Transaction WHERE appName = 'pandora-api'"
      },
      "signal": {
        "aggregation_window": 60,
        "aggregation_method": "EVENT_FLOW"
      },
      "terms": [
        {
          "threshold": 1,
          "threshold_duration": 300,
          "operator": "ABOVE",
          "priority": "CRITICAL"
        }
      ]
    }
  ]
}
```

---

## Service Level Management

### SLI Definitions

```sql
-- Availability SLI (successful requests / total requests)
SELECT percentage(count(*), WHERE error IS false) as 'Availability %'
FROM Transaction
WHERE appName = 'pandora-api'
SINCE 30 days ago

-- Latency SLI (requests under threshold / total requests)
SELECT percentage(count(*), WHERE duration < 0.5) as 'Fast Requests %'
FROM Transaction
WHERE appName = 'pandora-api'
SINCE 30 days ago

-- Throughput SLI
SELECT count(*) as 'Total Requests'
FROM Transaction
WHERE appName = 'pandora-api'
SINCE 30 days ago
```

### Error Budget Calculation

```sql
-- Error budget remaining
SELECT
  (1 - percentage(count(*), WHERE error IS true) / 100) as 'Current SLI',
  0.999 as 'SLO Target',
  ((1 - percentage(count(*), WHERE error IS true) / 100) - 0.999) / 0.001 * 100 as 'Budget Remaining %'
FROM Transaction
WHERE appName = 'pandora-api'
SINCE 30 days ago
```

---

## Kubernetes Monitoring

### Cluster Health

```sql
-- Pod status
SELECT latest(status) FROM K8sPodSample
WHERE clusterName = 'production'
FACET podName, namespace LIMIT 100

-- Container restarts
SELECT sum(restartCount) FROM K8sContainerSample
WHERE clusterName = 'production'
FACET containerName TIMESERIES

-- Node capacity
SELECT average(allocatableCpuCores), average(allocatableMemoryBytes)
FROM K8sNodeSample
WHERE clusterName = 'production'
FACET nodeName
```

### Deployment Tracking

```sql
-- Deployment changes
SELECT count(*) FROM K8sDeploymentSample
WHERE clusterName = 'production'
FACET deploymentName, updatedReplicas TIMESERIES

-- ReplicaSet availability
SELECT latest(availableReplicas), latest(desiredReplicas)
FROM K8sReplicaSetSample
WHERE clusterName = 'production'
FACET replicaSetName
```

---

## Database Monitoring

### PostgreSQL

```sql
-- Connection count
SELECT latest(postgresql.connections) FROM PostgresqlDatabaseSample
WHERE database = 'pandora_db' TIMESERIES

-- Query duration
SELECT average(postgresql.queryDurationMs) FROM PostgresqlDatabaseSample
WHERE database = 'pandora_db' TIMESERIES

-- Cache hit ratio
SELECT latest(postgresql.buffers.hit) /
       (latest(postgresql.buffers.hit) + latest(postgresql.buffers.read)) * 100
       as 'Cache Hit %'
FROM PostgresqlDatabaseSample
WHERE database = 'pandora_db' TIMESERIES
```

### Redis

```sql
-- Hit rate
SELECT latest(redis.keyspaceHits) /
       (latest(redis.keyspaceHits) + latest(redis.keyspaceMisses)) * 100
       as 'Hit Rate %'
FROM RedisSample TIMESERIES

-- Memory usage
SELECT latest(redis.usedMemoryBytes) / latest(redis.maxMemoryBytes) * 100
       as 'Memory %'
FROM RedisSample TIMESERIES

-- Connected clients
SELECT latest(redis.connectedClients) FROM RedisSample TIMESERIES
```

---

## Integration Patterns

### OpenTelemetry Integration

New Relic supports OTLP (OpenTelemetry Protocol):

```yaml
# otel-collector-config.yaml
exporters:
  otlp:
    endpoint: otlp.nr-data.net:4317
    headers:
      api-key: ${NEW_RELIC_LICENSE_KEY}

service:
  pipelines:
    traces:
      exporters: [otlp]
    metrics:
      exporters: [otlp]
```

### Prometheus Integration

```yaml
# prometheus-remote-write.yaml
remote_write:
  - url: https://metric-api.newrelic.com/prometheus/v1/write?prometheus_server=pandora
    bearer_token: ${NEW_RELIC_LICENSE_KEY}
```

### Kubernetes Agent Deployment

```bash
# Install New Relic Kubernetes integration
helm repo add newrelic https://helm-charts.newrelic.com
helm install newrelic-bundle newrelic/nri-bundle \
  --namespace newrelic \
  --create-namespace \
  --set global.licenseKey=${NEW_RELIC_LICENSE_KEY} \
  --set global.cluster=pandora-production \
  --set kubeEvents.enabled=true \
  --set logging.enabled=true \
  --set prometheus.enabled=true
```

---

## Best Practices

### Query Optimization

1. **Use specific WHERE clauses** - Narrow down data early
2. **Avoid SELECT *** - Select only needed attributes
3. **Use LIMIT** - Cap result sets
4. **Prefer TIMESERIES** for trending - More efficient than raw events
5. **Use FACET wisely** - High cardinality slows queries

### Dashboard Guidelines

1. **One purpose per dashboard** - SLO, Operations, Debugging
2. **Top-down layout** - Summary at top, details below
3. **Consistent time ranges** - Use variables or linked time
4. **Mobile-friendly** - Consider different screen sizes
5. **Documentation** - Include markdown widgets explaining metrics

### Alerting Best Practices

1. **Alert on symptoms, not causes** - Users experience latency, not CPU
2. **Use multi-window burn rates** - Avoid alert fatigue
3. **Include runbook links** - Speed up incident response
4. **Test alerts regularly** - Validate thresholds quarterly
5. **Escalation policies** - Route by severity and time

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| Alerting on every metric | Alert fatigue | Focus on user-facing SLIs |
| No time range in queries | Slow, unpredictable | Always use SINCE clause |
| Hardcoded account IDs | Breaks portability | Use variables |
| Single burn-rate alerts | Too sensitive/slow | Multi-window burn rates |
| Polling for real-time | Inefficient | Use streaming/NerdGraph subscriptions |
| Monolithic dashboards | Hard to navigate | Split by domain/team |

---

## References

- [NRQL Reference](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/get-started/introduction-nrql-new-relics-query-language/)
- [NerdGraph API](https://docs.newrelic.com/docs/apis/nerdgraph/get-started/introduction-new-relic-nerdgraph/)
- [Alert Conditions](https://docs.newrelic.com/docs/alerts-applied-intelligence/new-relic-alerts/alert-conditions/)
- [Service Level Management](https://docs.newrelic.com/docs/service-level-management/intro-slm/)
- [Kubernetes Integration](https://docs.newrelic.com/docs/kubernetes-pixie/kubernetes-integration/get-started/introduction-kubernetes-integration/)
