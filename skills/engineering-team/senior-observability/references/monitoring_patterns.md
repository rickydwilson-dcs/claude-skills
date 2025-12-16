# Monitoring Patterns Reference

Comprehensive guide to metrics collection, visualization patterns, and monitoring best practices for distributed systems.

## Table of Contents

1. [Monitoring Philosophy](#monitoring-philosophy)
2. [Four Golden Signals](#four-golden-signals)
3. [RED Method](#red-method)
4. [USE Method](#use-method)
5. [Platform-Specific Patterns](#platform-specific-patterns)
6. [Metric Naming Conventions](#metric-naming-conventions)
7. [Collection Strategies](#collection-strategies)
8. [Anti-Patterns](#anti-patterns)

---

## Monitoring Philosophy

### Observability vs Monitoring

**Monitoring** tells you when something is wrong. **Observability** helps you understand why.

| Aspect | Monitoring | Observability |
|--------|-----------|---------------|
| Focus | Known unknowns | Unknown unknowns |
| Approach | Predefined metrics | Exploratory analysis |
| Questions | "Is it broken?" | "Why is it broken?" |
| Data | Aggregated metrics | High-cardinality traces |

### Three Pillars of Observability

1. **Metrics** - Numeric measurements over time (what)
2. **Logs** - Discrete events with context (when)
3. **Traces** - Request flow through services (how)

### Monitoring Principles

1. **Symptom-based alerting** - Alert on user-visible symptoms, not internal causes
2. **The right granularity** - Not too much, not too little
3. **Actionable alerts** - Every alert should have a clear response
4. **Documentation** - Runbooks for every alert

---

## Four Golden Signals

From Google SRE, the four signals that best indicate service health:

### 1. Latency

The time it takes to service a request.

**Key Considerations:**
- Distinguish between successful and failed requests
- Use percentiles, not averages (P50, P95, P99)
- Set different SLOs for different operations

**Prometheus Queries:**
```promql
# P99 latency
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)

# P95 latency by endpoint
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint)
)

# Latency distribution
histogram_quantile(0.5, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))  # P50
histogram_quantile(0.9, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))  # P90
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) # P99
```

**Dashboard Panel Configuration:**
```json
{
  "title": "Request Latency",
  "type": "timeseries",
  "targets": [
    {"expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))", "legendFormat": "P99"},
    {"expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))", "legendFormat": "P95"},
    {"expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))", "legendFormat": "P50"}
  ],
  "fieldConfig": {"defaults": {"unit": "s"}}
}
```

### 2. Traffic

The amount of demand being placed on your system.

**Key Metrics:**
- HTTP requests per second
- Transactions per second
- Messages processed per second
- Active users/sessions

**Prometheus Queries:**
```promql
# Total request rate
sum(rate(http_requests_total[5m]))

# Request rate by service
sum(rate(http_requests_total[5m])) by (service)

# Request rate by endpoint and method
sum(rate(http_requests_total[5m])) by (endpoint, method)

# Active connections
sum(http_server_active_requests)
```

### 3. Errors

The rate of requests that fail.

**Error Types:**
- Explicit errors (HTTP 5xx)
- Implicit errors (HTTP 200 with error payload)
- Policy violations (wrong content, slow response)

**Prometheus Queries:**
```promql
# Error rate (5xx)
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# Error rate by endpoint
sum(rate(http_requests_total{status=~"5.."}[5m])) by (endpoint)
/
sum(rate(http_requests_total[5m])) by (endpoint)

# Client errors (4xx)
sum(rate(http_requests_total{status=~"4.."}[5m]))

# All non-2xx responses
sum(rate(http_requests_total{status!~"2.."}[5m]))
```

### 4. Saturation

How "full" your service is.

**Saturation Indicators:**
- CPU utilization
- Memory utilization
- Queue depth
- Thread pool utilization
- Connection pool usage

**Prometheus Queries:**
```promql
# CPU utilization
sum(rate(container_cpu_usage_seconds_total[5m]))
/
sum(container_spec_cpu_quota/container_spec_cpu_period) * 100

# Memory utilization
sum(container_memory_working_set_bytes)
/
sum(container_spec_memory_limit_bytes) * 100

# Thread pool saturation
thread_pool_active_threads / thread_pool_max_threads * 100

# Queue depth
sum(queue_messages_pending)
```

---

## RED Method

For request-driven services (APIs, web services):

### Rate

Requests per second your service is receiving.

```promql
# Request rate
sum(rate(http_requests_total[5m]))

# Request rate by status
sum(rate(http_requests_total[5m])) by (status)
```

### Errors

Number of failed requests per second.

```promql
# Error count
sum(rate(http_requests_total{status=~"5.."}[5m]))

# Error percentage
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m])) * 100
```

### Duration

Time each request takes (distribution).

```promql
# Duration percentiles
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### RED Dashboard Layout

```
+-------------------+-------------------+-------------------+
|   Request Rate    |    Error Rate     |  Latency (P99)    |
|   (Requests/s)    |   (Percentage)    |    (seconds)      |
+-------------------+-------------------+-------------------+
|           Request Rate by Endpoint                        |
+-----------------------------------------------------------+
|           Error Rate by Endpoint                          |
+-----------------------------------------------------------+
|           Latency Heatmap by Endpoint                     |
+-----------------------------------------------------------+
```

---

## USE Method

For resources (CPU, memory, storage, network):

### Utilization

Percentage of time the resource is busy.

```promql
# CPU utilization
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory utilization
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
/ node_memory_MemTotal_bytes * 100

# Disk utilization
(node_filesystem_size_bytes - node_filesystem_avail_bytes)
/ node_filesystem_size_bytes * 100
```

### Saturation

Amount of work the resource cannot service (queue depth).

```promql
# CPU saturation (load average)
node_load1 / count(node_cpu_seconds_total{mode="idle"}) by (instance)

# Memory saturation (swap usage)
node_memory_SwapTotal_bytes - node_memory_SwapFree_bytes

# Disk I/O saturation
rate(node_disk_io_time_weighted_seconds_total[5m])
```

### Errors

Number of error events for the resource.

```promql
# Disk errors
rate(node_disk_io_time_seconds_total{device=~"sd.*"}[5m])

# Network errors
rate(node_network_receive_errs_total[5m]) + rate(node_network_transmit_errs_total[5m])

# Memory errors (OOM kills)
rate(node_vmstat_oom_kill[5m])
```

### USE Dashboard Layout

```
+-------------------+-------------------+-------------------+
|  CPU Utilization  | Memory Utilization|  Disk Utilization |
+-------------------+-------------------+-------------------+
|  CPU Saturation   | Memory Saturation |  Disk I/O Wait    |
|   (Load Average)  |   (Swap Usage)    |    (Seconds)      |
+-------------------+-------------------+-------------------+
| Network Utilization                                       |
| (Bytes In/Out)                                            |
+-----------------------------------------------------------+
```

---

## Platform-Specific Patterns

### Prometheus

**Architecture:**
- Pull-based metrics collection
- Time-series database (TSDB)
- PromQL query language
- AlertManager for alerting

**ServiceMonitor Configuration:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-service
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: my-service
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

**Recording Rules:**
```yaml
groups:
- name: my-service-rules
  rules:
  - record: job:http_requests:rate5m
    expr: sum(rate(http_requests_total[5m])) by (job)
  - record: job:http_errors:rate5m
    expr: sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
```

### Grafana

**Dashboard Provisioning:**
```yaml
apiVersion: 1
providers:
- name: 'default'
  orgId: 1
  folder: ''
  type: file
  disableDeletion: false
  updateIntervalSeconds: 10
  options:
    path: /var/lib/grafana/dashboards
```

**Variable Configuration:**
```json
{
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "query": "label_values(kube_namespace_labels, namespace)",
        "refresh": 1,
        "multi": true,
        "includeAll": true
      },
      {
        "name": "service",
        "type": "query",
        "query": "label_values(up{namespace=\"$namespace\"}, job)",
        "refresh": 1
      }
    ]
  }
}
```

### DataDog

**Agent Configuration:**
```yaml
api_key: <YOUR_API_KEY>
site: datadoghq.com
logs_enabled: true
apm_config:
  enabled: true
  apm_non_local_traffic: true
process_config:
  enabled: true
```

**Custom Metrics:**
```python
from datadog import statsd

# Counter
statsd.increment('web.page_views', tags=['page:home'])

# Gauge
statsd.gauge('queue.depth', 42, tags=['queue:main'])

# Histogram
statsd.histogram('request.latency', 0.234, tags=['endpoint:api'])
```

### CloudWatch

**Custom Metric:**
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_metric_data(
    Namespace='MyApplication',
    MetricData=[{
        'MetricName': 'RequestLatency',
        'Dimensions': [
            {'Name': 'Service', 'Value': 'payment-api'},
            {'Name': 'Environment', 'Value': 'production'}
        ],
        'Value': 0.234,
        'Unit': 'Seconds'
    }]
)
```

### New Relic

**Architecture:**
- Push-based agent collection
- NRQL query language (SQL-like)
- NerdGraph API (GraphQL)
- Built-in APM, Infrastructure, Logs, and Browser monitoring

**Query Language (NRQL):**
```sql
-- Request rate
SELECT rate(count(*), 1 minute) FROM Transaction
WHERE appName = 'payment-api' TIMESERIES

-- Error percentage
SELECT percentage(count(*), WHERE error IS true)
FROM Transaction
WHERE appName = 'payment-api' TIMESERIES

-- P99 latency
SELECT percentile(duration, 99) FROM Transaction
WHERE appName = 'payment-api' TIMESERIES

-- CPU utilization (Infrastructure)
SELECT average(cpuPercent) FROM SystemSample
WHERE hostname LIKE '%payment%' TIMESERIES
```

**PromQL to NRQL Mapping:**

| Metric Type | PromQL | NRQL |
|-------------|--------|------|
| Request Rate | `rate(http_requests_total[5m])` | `SELECT rate(count(*), 5 minutes) FROM Transaction` |
| Error Rate | `sum(rate(...{status=~"5.."}[5m]))/sum(rate(...[5m]))` | `SELECT percentage(count(*), WHERE error IS true) FROM Transaction` |
| P99 Latency | `histogram_quantile(0.99, sum(rate(..._bucket[5m])) by (le))` | `SELECT percentile(duration, 99) FROM Transaction` |
| CPU Usage | `rate(container_cpu_usage_seconds_total[5m])` | `SELECT average(cpuPercent) FROM SystemSample` |
| Memory Usage | `container_memory_working_set_bytes` | `SELECT average(memoryUsedBytes) FROM SystemSample` |

**Kubernetes Integration:**
```bash
# Install via Helm
helm repo add newrelic https://helm-charts.newrelic.com
helm install newrelic-bundle newrelic/nri-bundle \
  --namespace newrelic \
  --create-namespace \
  --set global.licenseKey=${NEW_RELIC_LICENSE_KEY} \
  --set global.cluster=production \
  --set kubeEvents.enabled=true \
  --set logging.enabled=true
```

**Dashboard JSON Structure:**
```json
{
  "name": "Service Overview",
  "pages": [
    {
      "name": "Overview",
      "widgets": [
        {
          "title": "Request Rate",
          "visualization": {"id": "viz.line"},
          "rawConfiguration": {
            "nrqlQueries": [{
              "accountId": 123456,
              "query": "SELECT rate(count(*), 1 minute) FROM Transaction WHERE appName = 'my-service' TIMESERIES"
            }]
          }
        }
      ]
    }
  ]
}
```

**Alert Condition (NRQL):**
```json
{
  "name": "High Error Rate",
  "type": "NRQL",
  "nrql": {
    "query": "SELECT percentage(count(*), WHERE error IS true) FROM Transaction WHERE appName = 'payment-api'"
  },
  "terms": [{
    "threshold": 5,
    "operator": "ABOVE",
    "priority": "CRITICAL"
  }]
}
```

**See Also:** [newrelic_patterns.md](newrelic_patterns.md) for comprehensive NRQL reference.

---

## Metric Naming Conventions

### Prometheus Naming

**Format:** `<namespace>_<name>_<unit>`

**Examples:**
```
http_requests_total           # Counter for HTTP requests
http_request_duration_seconds # Histogram for request duration
process_cpu_seconds_total     # Counter for CPU time
node_memory_bytes             # Gauge for memory
```

**Rules:**
1. Use snake_case
2. Prefix with namespace/application name
3. Include unit suffix (_seconds, _bytes, _total)
4. Use _total suffix for counters
5. Use _bucket suffix for histogram buckets
6. Use _count and _sum for histogram totals

### Label Best Practices

**Good Labels:**
```
http_requests_total{method="GET", endpoint="/api/users", status="200"}
```

**Bad Labels (High Cardinality):**
```
http_requests_total{user_id="12345", request_id="abc-123"}  # DON'T DO THIS
```

**Cardinality Guidelines:**
- Keep unique label combinations under 10,000 per metric
- Avoid user IDs, session IDs, request IDs as labels
- Use labels for dimensions you'll filter/aggregate on
- Consider sampling for high-cardinality data

---

## Collection Strategies

### Pull vs Push

| Aspect | Pull (Prometheus) | Push (StatsD/DataDog) |
|--------|-------------------|----------------------|
| Network | Scraper initiates | App initiates |
| Firewall | Inbound to targets | Outbound from apps |
| Discovery | Service discovery | Direct configuration |
| Debugging | Easy (just curl) | Harder (async) |
| Short-lived | Harder | Easier |

### Scrape Intervals

**Recommended Intervals:**
- High-frequency metrics: 10-15s
- Standard metrics: 30s (default)
- Low-priority metrics: 60s
- Cost-sensitive: 60-120s

**Considerations:**
- More frequent = more storage
- Less frequent = less granularity
- Balance cost vs. visibility

### Service Discovery

**Kubernetes:**
```yaml
scrape_configs:
- job_name: 'kubernetes-pods'
  kubernetes_sd_configs:
  - role: pod
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    action: keep
    regex: true
```

**Consul:**
```yaml
scrape_configs:
- job_name: 'consul-services'
  consul_sd_configs:
  - server: 'consul:8500'
    services: []
```

---

## Anti-Patterns

### 1. High Cardinality Labels

**Problem:**
```
http_requests_total{user_id="...", session_id="...", request_id="..."}
```

**Solution:**
- Use traces for request-level data
- Aggregate high-cardinality dimensions
- Sample if necessary

### 2. Missing Labels for Aggregation

**Problem:**
```
http_requests_total  # No labels = can't drill down
```

**Solution:**
```
http_requests_total{service="api", endpoint="/users", method="GET", status="200"}
```

### 3. Averages Instead of Percentiles

**Problem:**
- Average latency hides outliers
- P99 users have terrible experience

**Solution:**
- Always use histograms
- Display P50, P95, P99
- Alert on P99, not average

### 4. Over-Monitoring

**Problem:**
- Too many metrics = slow queries
- Alert fatigue from too many alerts
- High storage costs

**Solution:**
- Focus on the Four Golden Signals
- Use recording rules for expensive queries
- Regular metric review and cleanup

### 5. Under-Monitoring

**Problem:**
- No visibility into failures
- Can't diagnose issues
- Slow incident response

**Solution:**
- Instrument all entry points
- Add business metrics
- Regular coverage review

### 6. Counter vs Gauge Confusion

**Problem:**
```
# Using gauge for cumulative data
current_requests = 1234  # Gauge that only increases
```

**Solution:**
```
# Use counter for cumulative
requests_total = 1234  # Counter
# Use gauge for point-in-time
active_requests = 5  # Gauge
```

---

## Quick Reference

### Metric Types

| Type | Use Case | Example |
|------|----------|---------|
| Counter | Cumulative totals | `http_requests_total` |
| Gauge | Current values | `temperature_celsius` |
| Histogram | Distributions | `request_duration_seconds` |
| Summary | Percentiles (client-side) | `request_duration_seconds` |

### Key Queries

```promql
# Request rate
sum(rate(http_requests_total[5m]))

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# P99 latency
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# CPU utilization
sum(rate(container_cpu_usage_seconds_total[5m])) / sum(container_spec_cpu_quota/container_spec_cpu_period) * 100

# Memory utilization
sum(container_memory_working_set_bytes) / sum(container_spec_memory_limit_bytes) * 100
```

---

## Resources

- [Google SRE Book - Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [RED Method](https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/)
- [USE Method](https://www.brendangregg.com/usemethod.html)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)
