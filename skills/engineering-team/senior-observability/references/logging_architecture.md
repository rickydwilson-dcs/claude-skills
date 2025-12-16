# Logging Architecture Reference

Comprehensive guide to structured logging, log aggregation, and centralized logging architectures for distributed systems.

## Table of Contents

1. [Structured Logging](#structured-logging)
2. [Log Levels](#log-levels)
3. [ELK Stack Architecture](#elk-stack-architecture)
4. [Loki Architecture](#loki-architecture)
5. [Log Aggregation Patterns](#log-aggregation-patterns)
6. [Correlation and Context](#correlation-and-context)
7. [Retention and Cost](#retention-and-cost)
8. [Security Considerations](#security-considerations)

---

## Structured Logging

### Why Structured Logging?

Unstructured logs are hard to parse, search, and analyze at scale.

**Unstructured (Bad):**
```
2025-01-15 10:23:45 INFO User john@example.com logged in from 192.168.1.1
```

**Structured (Good):**
```json
{
  "timestamp": "2025-01-15T10:23:45.123Z",
  "level": "INFO",
  "message": "User logged in",
  "user_email": "john@example.com",
  "source_ip": "192.168.1.1",
  "service": "auth-service",
  "trace_id": "abc123",
  "span_id": "def456"
}
```

### JSON Log Format

**Standard Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 | Event time with timezone |
| `level` | string | Log level (DEBUG, INFO, WARN, ERROR, FATAL) |
| `message` | string | Human-readable message |
| `service` | string | Service/application name |
| `version` | string | Service version |
| `environment` | string | Environment (dev, staging, prod) |
| `host` | string | Hostname/pod name |
| `trace_id` | string | Distributed trace ID |
| `span_id` | string | Current span ID |

**Python Example:**
```python
import json
import logging
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "service": "my-service",
            "environment": os.getenv("ENVIRONMENT", "development")
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra"):
            log_entry.update(record.extra)

        return json.dumps(log_entry)

# Usage
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("User logged in", extra={"user_id": "123", "ip": "192.168.1.1"})
```

**Node.js Example (Winston):**
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'my-service',
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.Console()
  ]
});

logger.info('User logged in', { userId: '123', ip: '192.168.1.1' });
```

---

## Log Levels

### Standard Levels

| Level | Value | Use Case |
|-------|-------|----------|
| **FATAL** | 60 | System is unusable, immediate action required |
| **ERROR** | 50 | Error occurred, operation failed |
| **WARN** | 40 | Warning, potential issue |
| **INFO** | 30 | Normal operation, state changes |
| **DEBUG** | 20 | Detailed debugging information |
| **TRACE** | 10 | Very detailed tracing |

### When to Use Each Level

**FATAL:**
- Database connection permanently lost
- Out of memory
- Security breach detected
- Critical configuration missing

**ERROR:**
- Request failed due to internal error
- External API call failed after retries
- Data validation failed
- Unhandled exception

**WARN:**
- Deprecated API called
- Retry attempt for external service
- Resource usage approaching limit
- Non-critical validation issue

**INFO:**
- Request received/completed
- User logged in/out
- Configuration loaded
- Service started/stopped
- Scheduled job completed

**DEBUG:**
- SQL queries executed
- Cache hits/misses
- Function entry/exit
- Variable values

**TRACE:**
- Every function call
- Loop iterations
- Wire-level data

### Level Configuration by Environment

| Environment | Console Level | File Level | Aggregator Level |
|-------------|--------------|------------|------------------|
| Development | DEBUG | DEBUG | - |
| Staging | INFO | DEBUG | DEBUG |
| Production | INFO | INFO | INFO |

---

## ELK Stack Architecture

### Components

```
+------------+    +-------------+    +---------------+    +---------+
|  App Logs  | -> | Filebeat/   | -> | Logstash      | -> | Elastic |
|            |    | Fluentd     |    | (Processing)  |    | search  |
+------------+    +-------------+    +---------------+    +---------+
                                                               |
                                                               v
                                                         +---------+
                                                         | Kibana  |
                                                         +---------+
```

### Elasticsearch Index Strategy

**Index Naming:**
```
logs-{service}-{environment}-{date}

Examples:
logs-payment-api-production-2025.01.15
logs-user-service-staging-2025.01.15
```

**Index Template:**
```json
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy",
      "index.lifecycle.rollover_alias": "logs"
    },
    "mappings": {
      "properties": {
        "timestamp": { "type": "date" },
        "level": { "type": "keyword" },
        "message": { "type": "text" },
        "service": { "type": "keyword" },
        "environment": { "type": "keyword" },
        "trace_id": { "type": "keyword" },
        "user_id": { "type": "keyword" }
      }
    }
  }
}
```

### Logstash Pipeline

```ruby
input {
  beats {
    port => 5044
  }
}

filter {
  json {
    source => "message"
    target => "log"
  }

  date {
    match => ["[log][timestamp]", "ISO8601"]
    target => "@timestamp"
  }

  mutate {
    add_field => {
      "service" => "%{[log][service]}"
      "level" => "%{[log][level]}"
    }
  }

  # Mask sensitive data
  mutate {
    gsub => [
      "[log][message]", "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]",
      "[log][message]", "\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[REDACTED_CARD]"
    ]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{[log][service]}-%{[log][environment]}-%{+YYYY.MM.dd}"
  }
}
```

### Filebeat Configuration

```yaml
filebeat.inputs:
- type: container
  paths:
    - '/var/lib/docker/containers/*/*.log'
  processors:
    - add_kubernetes_metadata:
        host: ${NODE_NAME}
        matchers:
        - logs_path:
            logs_path: "/var/lib/docker/containers/"

output.logstash:
  hosts: ["logstash:5044"]

logging.level: info
logging.to_files: true
```

---

## Loki Architecture

### Overview

Loki is a log aggregation system designed for efficiency - it indexes only metadata (labels), not the log content.

```
+------------+    +-----------+    +-------+    +---------+
|  App Logs  | -> | Promtail  | -> | Loki  | -> | Grafana |
+------------+    +-----------+    +-------+    +---------+
```

### Promtail Configuration

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
    pipeline_stages:
      - json:
          expressions:
            level: level
            message: message
            trace_id: trace_id
      - labels:
          level:
          trace_id:
```

### LogQL Queries

```logql
# Find all errors in payment-service
{app="payment-service"} |= "error"

# Parse JSON and filter by level
{app="payment-service"} | json | level="ERROR"

# Count errors per service
sum(count_over_time({level="ERROR"}[5m])) by (app)

# Search for specific trace
{app=~".*"} |= "trace_id=abc123"

# Calculate error rate
sum(rate({app="payment-service"} |= "error" [5m]))
/
sum(rate({app="payment-service"} [5m]))
```

### Loki vs Elasticsearch

| Feature | Loki | Elasticsearch |
|---------|------|---------------|
| Indexing | Labels only | Full text |
| Storage | Very efficient | Higher |
| Query Language | LogQL | Lucene/KQL |
| Cost | Lower | Higher |
| Search Speed | Slower for text | Faster |
| Integration | Native Grafana | Kibana |

---

## Log Aggregation Patterns

### Sidecar Pattern

Each pod has a logging sidecar that ships logs.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: app
    image: my-app:latest
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  - name: log-shipper
    image: fluent/fluent-bit:latest
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
      readOnly: true
    - name: fluent-bit-config
      mountPath: /fluent-bit/etc/
  volumes:
  - name: logs
    emptyDir: {}
  - name: fluent-bit-config
    configMap:
      name: fluent-bit-config
```

**Pros:**
- Isolated from application
- Can handle app crashes
- Consistent across services

**Cons:**
- More resource overhead
- More complexity

### DaemonSet Pattern

A single log collector per node.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
spec:
  selector:
    matchLabels:
      app: fluent-bit
  template:
    metadata:
      labels:
        app: fluent-bit
    spec:
      containers:
      - name: fluent-bit
        image: fluent/fluent-bit:latest
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: containers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: containers
        hostPath:
          path: /var/lib/docker/containers
```

**Pros:**
- Efficient resource usage
- Simpler to manage
- Node-level logging

**Cons:**
- Single point of failure per node
- Less isolation

### Direct Push Pattern

Application pushes logs directly to aggregator.

```python
import logging
from fluent import handler

fluent_handler = handler.FluentHandler(
    'my-app',
    host='fluentd.logging.svc.cluster.local',
    port=24224
)
logging.getLogger().addHandler(fluent_handler)
```

**Pros:**
- No additional containers
- Lower latency
- Fine-grained control

**Cons:**
- Application dependency
- Lost logs on crash
- Network dependency

---

## Correlation and Context

### Trace Context Propagation

**W3C Trace Context Headers:**
```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
tracestate: vendor1=value1,vendor2=value2
```

**OpenTelemetry Integration:**
```python
from opentelemetry import trace
from opentelemetry.trace import SpanContext

class ContextLogger:
    def __init__(self, logger):
        self.logger = logger

    def _add_trace_context(self, extra):
        span = trace.get_current_span()
        if span.is_recording():
            ctx = span.get_span_context()
            extra["trace_id"] = format(ctx.trace_id, "032x")
            extra["span_id"] = format(ctx.span_id, "016x")
        return extra

    def info(self, message, **extra):
        extra = self._add_trace_context(extra)
        self.logger.info(message, extra=extra)
```

### Request Context

**Middleware Example (Express.js):**
```javascript
const { v4: uuidv4 } = require('uuid');
const asyncLocalStorage = require('async_hooks').AsyncLocalStorage;

const requestContext = new AsyncLocalStorage();

app.use((req, res, next) => {
  const context = {
    requestId: req.headers['x-request-id'] || uuidv4(),
    traceId: req.headers['traceparent']?.split('-')[1],
    userId: req.user?.id
  };

  requestContext.run(context, next);
});

// In your logger
function log(level, message, data = {}) {
  const context = requestContext.getStore() || {};
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level,
    message,
    ...context,
    ...data
  }));
}
```

### Correlation ID Best Practices

1. **Generate at entry point** - First service creates correlation ID
2. **Propagate through headers** - Pass to downstream services
3. **Log on every entry/exit** - Include in all log entries
4. **Store in thread/async context** - Automatically include

---

## Retention and Cost

### Retention Policies

| Environment | Hot Storage | Warm Storage | Cold/Archive | Total |
|-------------|-------------|--------------|--------------|-------|
| Production | 7 days | 30 days | 1 year | 1 year |
| Staging | 3 days | 14 days | - | 14 days |
| Development | 1 day | 7 days | - | 7 days |

### Index Lifecycle Management (Elasticsearch)

```json
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50gb",
            "max_age": "1d"
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {},
          "set_priority": {
            "priority": 0
          }
        }
      },
      "delete": {
        "min_age": "365d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### Cost Optimization Strategies

1. **Sample debug logs** - Log 10% of debug in production
2. **Use appropriate levels** - Don't log DEBUG in production
3. **Compress archived logs** - Use gzip/zstd compression
4. **Drop unnecessary fields** - Remove verbose stack traces after analysis
5. **Use cheaper storage tiers** - Move old logs to S3/GCS
6. **Set retention limits** - Auto-delete old logs

---

## Security Considerations

### PII Redaction

**Common PII Patterns:**
```python
import re

REDACTION_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
}

def redact_pii(text):
    for name, pattern in REDACTION_PATTERNS.items():
        text = re.sub(pattern, f'[REDACTED_{name.upper()}]', text)
    return text
```

### Log Encryption

**At Rest:**
- Enable encryption for Elasticsearch indices
- Use encrypted S3 buckets for archives
- Encrypt Loki chunks in object storage

**In Transit:**
- TLS for all log shipping
- mTLS between components
- VPN for cross-region replication

### Access Control

```yaml
# Elasticsearch role-based access
{
  "security_role": {
    "cluster": ["monitor"],
    "indices": [
      {
        "names": ["logs-payment-*"],
        "privileges": ["read"],
        "field_security": {
          "except": ["user_email", "credit_card"]
        }
      }
    ]
  }
}
```

### Audit Logging

Log access to sensitive logs:
```json
{
  "timestamp": "2025-01-15T10:23:45Z",
  "event": "log_access",
  "user": "analyst@company.com",
  "action": "search",
  "index": "logs-payment-production-*",
  "query": "error AND user_id:123",
  "results_count": 42
}
```

---

## Quick Reference

### Essential Log Fields

```json
{
  "timestamp": "2025-01-15T10:23:45.123Z",
  "level": "INFO",
  "message": "Request completed",
  "service": "payment-api",
  "version": "1.2.3",
  "environment": "production",
  "host": "payment-api-5d4f8b7c9d-x7k2m",
  "trace_id": "abc123",
  "span_id": "def456",
  "request_id": "req-789",
  "user_id": "user-456",
  "duration_ms": 234,
  "status_code": 200
}
```

### Log Level Decision Tree

```
Is the system unusable?
  └─ Yes → FATAL
  └─ No → Did an operation fail?
           └─ Yes → ERROR
           └─ No → Is this a potential issue?
                    └─ Yes → WARN
                    └─ No → Is this a state change?
                             └─ Yes → INFO
                             └─ No → DEBUG/TRACE
```

---

## Resources

- [The Twelve-Factor App - Logs](https://12factor.net/logs)
- [Elastic Stack Documentation](https://www.elastic.co/guide/index.html)
- [Grafana Loki Documentation](https://grafana.com/docs/loki/latest/)
- [OpenTelemetry Logging](https://opentelemetry.io/docs/concepts/signals/logs/)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
