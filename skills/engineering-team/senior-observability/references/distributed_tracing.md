# Distributed Tracing Reference

Comprehensive guide to distributed tracing implementation with OpenTelemetry, Jaeger, and production best practices.

## Table of Contents

1. [Tracing Fundamentals](#tracing-fundamentals)
2. [OpenTelemetry](#opentelemetry)
3. [Trace Context Propagation](#trace-context-propagation)
4. [Instrumentation Patterns](#instrumentation-patterns)
5. [Sampling Strategies](#sampling-strategies)
6. [Tracing Backends](#tracing-backends)
7. [Trace Analysis](#trace-analysis)
8. [Production Considerations](#production-considerations)

---

## Tracing Fundamentals

### Key Concepts

**Trace:** A complete request flow through a distributed system.

**Span:** A single operation within a trace (e.g., HTTP request, database query).

**Context:** Metadata that links spans together across services.

### Trace Structure

```
Trace ID: abc123
├── Span A: API Gateway (0-100ms)
│   └── Span B: Auth Service (10-30ms)
│       └── Span C: Redis Cache (12-15ms)
│   └── Span D: Order Service (35-90ms)
│       └── Span E: Database Query (40-60ms)
│       └── Span F: Payment Service (65-85ms)
```

### Span Anatomy

```json
{
  "trace_id": "abc123def456",
  "span_id": "span789",
  "parent_span_id": "parentspan123",
  "operation_name": "HTTP GET /api/orders",
  "service_name": "order-service",
  "start_time": "2025-01-15T10:23:45.123Z",
  "duration_ms": 234,
  "status": "OK",
  "tags": {
    "http.method": "GET",
    "http.url": "/api/orders/123",
    "http.status_code": 200,
    "db.type": "postgresql",
    "db.statement": "SELECT * FROM orders WHERE id = ?"
  },
  "logs": [
    {
      "timestamp": "2025-01-15T10:23:45.200Z",
      "event": "cache_miss",
      "message": "Order not found in cache"
    }
  ]
}
```

---

## OpenTelemetry

### Architecture

```
+-------------+     +-------------+     +----------+
| Application | --> | OTel SDK    | --> | Exporter |
| Code        |     | (Auto/Manual|     | (OTLP,   |
|             |     |  Instrument)|     |  Jaeger) |
+-------------+     +-------------+     +----------+
                                              |
                                              v
                                        +-----------+
                                        | Collector |
                                        +-----------+
                                              |
                    +-------------------------+-------------------------+
                    v                         v                         v
              +-----------+            +-----------+            +-----------+
              | Jaeger    |            | Zipkin    |            | Tempo     |
              +-----------+            +-----------+            +-----------+
```

### Python Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Configure resource
resource = Resource.create({
    "service.name": "order-service",
    "service.version": "1.2.3",
    "deployment.environment": "production"
})

# Configure tracer provider
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://otel-collector:4317")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrument libraries
FlaskInstrumentor().instrument()
RequestsInstrumentor().instrument()
SQLAlchemyInstrumentor().instrument()

# Manual instrumentation
tracer = trace.get_tracer(__name__)

@app.route('/orders/<order_id>')
def get_order(order_id):
    with tracer.start_as_current_span("fetch_order") as span:
        span.set_attribute("order.id", order_id)

        # Business logic
        order = fetch_from_database(order_id)

        span.add_event("order_fetched", {"items_count": len(order.items)})

        return jsonify(order)
```

### Node.js Setup

```javascript
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'order-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.2.3',
  }),
  traceExporter: new OTLPTraceExporter({
    url: 'http://otel-collector:4317',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

// Manual spans
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('order-service');

async function processOrder(orderId) {
  const span = tracer.startSpan('process_order');
  span.setAttribute('order.id', orderId);

  try {
    // Business logic
    const result = await doProcessing(orderId);
    span.setStatus({ code: SpanStatusCode.OK });
    return result;
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
    span.recordException(error);
    throw error;
  } finally {
    span.end();
  }
}
```

### Go Setup

```go
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
    "go.opentelemetry.io/otel/trace"
)

func initTracer() (*sdktrace.TracerProvider, error) {
    ctx := context.Background()

    exporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    res, err := resource.New(ctx,
        resource.WithAttributes(
            semconv.ServiceName("order-service"),
            semconv.ServiceVersion("1.2.3"),
        ),
    )

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(res),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}

func processOrder(ctx context.Context, orderID string) error {
    tracer := otel.Tracer("order-service")

    ctx, span := tracer.Start(ctx, "process_order")
    defer span.End()

    span.SetAttributes(
        attribute.String("order.id", orderID),
    )

    // Business logic
    return nil
}
```

### OpenTelemetry Collector Configuration

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

  memory_limiter:
    check_interval: 1s
    limit_mib: 1000

  # Sampling
  probabilistic_sampler:
    sampling_percentage: 10

  # Add attributes
  attributes:
    actions:
      - key: environment
        value: production
        action: upsert

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

  otlp:
    endpoint: tempo:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [jaeger, otlp]
```

---

## Trace Context Propagation

### W3C Trace Context (Standard)

**Headers:**
```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
tracestate: vendor1=value1,vendor2=value2
```

**Format:**
```
traceparent: {version}-{trace-id}-{parent-id}-{flags}

version:   00 (always)
trace-id:  32 hex characters (16 bytes)
parent-id: 16 hex characters (8 bytes)
flags:     01 = sampled, 00 = not sampled
```

### B3 Propagation (Zipkin)

**Single Header:**
```
b3: 80f198ee56343ba864fe8b2a57d3eff7-e457b5a2e4d86bd1-1
```

**Multi Header:**
```
X-B3-TraceId: 80f198ee56343ba864fe8b2a57d3eff7
X-B3-SpanId: e457b5a2e4d86bd1
X-B3-ParentSpanId: 05e3ac9a4f6e3b90
X-B3-Sampled: 1
```

### Propagation Implementation

**Python:**
```python
from opentelemetry.propagate import inject, extract
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

propagator = TraceContextTextMapPropagator()

# Inject context into outgoing request
def make_request(url):
    headers = {}
    inject(headers)  # Adds traceparent header
    return requests.get(url, headers=headers)

# Extract context from incoming request
def handle_request(request):
    context = extract(request.headers)
    with tracer.start_as_current_span("handle", context=context):
        # Process request
        pass
```

**Node.js:**
```javascript
const { context, propagation } = require('@opentelemetry/api');
const { W3CTraceContextPropagator } = require('@opentelemetry/core');

// Set propagator
propagation.setGlobalPropagator(new W3CTraceContextPropagator());

// Inject into outgoing request
async function makeRequest(url) {
  const headers = {};
  propagation.inject(context.active(), headers);
  return fetch(url, { headers });
}

// Extract from incoming request
function handleRequest(req, res) {
  const extractedContext = propagation.extract(context.active(), req.headers);
  context.with(extractedContext, () => {
    // Handle request with context
  });
}
```

---

## Instrumentation Patterns

### Auto-Instrumentation

Libraries that automatically instrument common frameworks:

| Language | Libraries |
|----------|-----------|
| Python | Flask, Django, FastAPI, requests, SQLAlchemy, Redis |
| Node.js | Express, Fastify, pg, mysql, redis, mongodb |
| Go | net/http, gRPC, database/sql |
| Java | Spring, Servlet, JDBC, gRPC |

### Manual Instrumentation

**Creating spans:**
```python
with tracer.start_as_current_span("operation_name") as span:
    span.set_attribute("key", "value")
    span.add_event("event_name", {"data": "value"})

    # Do work
    result = do_work()

    if error:
        span.record_exception(error)
        span.set_status(StatusCode.ERROR, str(error))
```

**Nested spans:**
```python
with tracer.start_as_current_span("parent") as parent:
    parent.set_attribute("type", "parent")

    with tracer.start_as_current_span("child") as child:
        child.set_attribute("type", "child")
        # Child automatically linked to parent
```

### Semantic Conventions

Standard attribute names for common operations:

**HTTP:**
```python
span.set_attribute("http.method", "GET")
span.set_attribute("http.url", "https://api.example.com/users")
span.set_attribute("http.status_code", 200)
span.set_attribute("http.request_content_length", 1024)
```

**Database:**
```python
span.set_attribute("db.system", "postgresql")
span.set_attribute("db.name", "orders")
span.set_attribute("db.statement", "SELECT * FROM users WHERE id = ?")
span.set_attribute("db.operation", "SELECT")
```

**Messaging:**
```python
span.set_attribute("messaging.system", "rabbitmq")
span.set_attribute("messaging.destination", "orders-queue")
span.set_attribute("messaging.operation", "publish")
```

---

## Sampling Strategies

### Head-Based Sampling

Decision made at trace start.

**Probabilistic:**
```yaml
# Sample 10% of traces
processors:
  probabilistic_sampler:
    sampling_percentage: 10
```

**Rate Limiting:**
```yaml
# Sample max 100 traces per second
processors:
  rate_limiting_sampler:
    rate: 100
```

### Tail-Based Sampling

Decision made after trace completes (requires buffering).

```yaml
processors:
  tail_sampling:
    decision_wait: 10s
    num_traces: 100000
    policies:
      # Always sample errors
      - name: errors
        type: status_code
        status_code: {status_codes: [ERROR]}

      # Always sample slow traces
      - name: slow
        type: latency
        latency: {threshold_ms: 1000}

      # Sample 10% of everything else
      - name: probabilistic
        type: probabilistic
        probabilistic: {sampling_percentage: 10}
```

### Adaptive Sampling

Adjust sampling rate based on traffic.

```yaml
processors:
  adaptive_sampler:
    target_traces_per_second: 100
    min_sampling_percentage: 1
    max_sampling_percentage: 100
```

### Sampling Decision Tree

```
Is this an error trace?
  └─ Yes → Sample 100%
  └─ No → Is latency > threshold?
           └─ Yes → Sample 100%
           └─ No → Is this a critical path?
                    └─ Yes → Sample 50%
                    └─ No → Sample 10%
```

---

## Tracing Backends

### Jaeger

**Architecture:**
```
+--------+    +-----------+    +----------+    +-----------+
| Client | -> | Collector | -> | Storage  | -> | Query     |
|        |    |           |    | (ES/     |    | Service   |
|        |    |           |    |  Cassandra)   |           |
+--------+    +-----------+    +----------+    +-----------+
                                                     |
                                                     v
                                               +-----------+
                                               | Jaeger UI |
                                               +-----------+
```

**Kubernetes Deployment:**
```yaml
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: production
spec:
  strategy: production
  storage:
    type: elasticsearch
    elasticsearch:
      nodeCount: 3
      storage:
        size: 200Gi
  collector:
    replicas: 3
    resources:
      limits:
        cpu: 1
        memory: 2Gi
  query:
    replicas: 2
```

### Grafana Tempo

**Architecture:**
- No indexing (like Loki for logs)
- Uses object storage (S3, GCS)
- Integrates with Grafana

**Configuration:**
```yaml
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        grpc:

ingester:
  trace_idle_period: 10s
  max_block_bytes: 1_000_000
  max_block_duration: 5m

compactor:
  compaction:
    block_retention: 48h

storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-traces
      endpoint: s3.amazonaws.com
```

### Zipkin

**Simple deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zipkin
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: zipkin
        image: openzipkin/zipkin:latest
        ports:
        - containerPort: 9411
        env:
        - name: STORAGE_TYPE
          value: elasticsearch
        - name: ES_HOSTS
          value: elasticsearch:9200
```

---

## Trace Analysis

### Critical Path Analysis

Identify the longest path through a trace:

```
Total: 500ms
├── API Gateway: 20ms (4%)
├── Auth Service: 50ms (10%)
├── Order Service: 200ms (40%) ← Bottleneck
│   ├── DB Query: 150ms (30%)  ← Root cause
│   └── Validation: 50ms (10%)
└── Payment: 230ms (46%)
```

### Service Dependency Mapping

```
           ┌─────────────────┐
           │   API Gateway   │
           └────────┬────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │  Auth   │ │  Order  │ │ Payment │
   └────┬────┘ └────┬────┘ └────┬────┘
        │           │           │
        ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │  Redis  │ │ Postgres│ │  Stripe │
   └─────────┘ └─────────┘ └─────────┘
```

### Error Analysis

Query traces with errors:

**Jaeger Query:**
```
service=order-service error=true
```

**Tempo TraceQL:**
```
{status=error} | duration > 1s
{resource.service.name="order-service" && status=error}
```

---

## Production Considerations

### Performance Overhead

| Operation | Typical Overhead |
|-----------|-----------------|
| Span creation | 1-5 μs |
| Context propagation | 0.5-2 μs |
| Span export (async) | Negligible |
| Total per request | < 1% |

### Resource Planning

**Collector sizing:**
- 1 CPU core per 10,000 spans/second
- 2GB RAM per 10,000 spans/second (with batching)

**Storage estimation:**
- ~1KB per span (compressed)
- 1M spans/day = ~1GB/day storage
- Plan for 3-7 day hot retention

### High Availability

```yaml
# Collector deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: otel-collector
spec:
  replicas: 3
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: otel-collector
            topologyKey: kubernetes.io/hostname
```

### Monitoring the Monitoring

Key metrics to watch:

```promql
# Spans received rate
sum(rate(otelcol_receiver_accepted_spans[5m])) by (receiver)

# Spans dropped
sum(rate(otelcol_processor_dropped_spans[5m])) by (processor)

# Export failures
sum(rate(otelcol_exporter_send_failed_spans[5m])) by (exporter)

# Queue depth
otelcol_exporter_queue_size
```

---

## Quick Reference

### Essential Span Attributes

```python
# HTTP
span.set_attribute("http.method", "POST")
span.set_attribute("http.url", "/api/orders")
span.set_attribute("http.status_code", 201)

# Database
span.set_attribute("db.system", "postgresql")
span.set_attribute("db.statement", "INSERT INTO orders...")

# Error
span.record_exception(exception)
span.set_status(StatusCode.ERROR, "Failed to process")

# Custom business logic
span.set_attribute("order.id", "12345")
span.set_attribute("order.total", 99.99)
span.add_event("payment_processed", {"provider": "stripe"})
```

### Sampling Configuration

```yaml
# Development: 100%
sampling_percentage: 100

# Staging: 50%
sampling_percentage: 50

# Production: 10% + 100% errors
tail_sampling:
  policies:
    - type: status_code
      status_codes: [ERROR]
    - type: probabilistic
      sampling_percentage: 10
```

---

## Resources

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Grafana Tempo](https://grafana.com/docs/tempo/latest/)
- [Distributed Tracing in Practice (O'Reilly)](https://www.oreilly.com/library/view/distributed-tracing-in/9781492056621/)
