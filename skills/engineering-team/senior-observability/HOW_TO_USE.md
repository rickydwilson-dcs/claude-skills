# How to Use Senior Observability Skill

## Quick Start

```bash
# Generate a Grafana dashboard for your API service
python3 scripts/dashboard_generator.py --service my-api --type api --platform grafana --output json

# Generate a NewRelic dashboard for your API service
python3 scripts/dashboard_generator.py --service my-api --type api --platform newrelic --output json

# Create SLO-based alerts with 99.9% availability target (Prometheus)
python3 scripts/alert_rule_generator.py --service my-api --slo-target 99.9 --platform prometheus --output yaml

# Create SLO-based alerts with 99.9% availability target (NewRelic)
python3 scripts/alert_rule_generator.py --service my-api --slo-target 99.9 --platform newrelic --output json

# Calculate error budget from your metrics
python3 scripts/slo_calculator.py --input metrics.csv --slo-type availability --target 99.9 --output json

# Analyze metrics for anomalies
python3 scripts/metrics_analyzer.py --input metrics.csv --analysis-type anomaly --output json
```

## Example Invocations

### 1. Full Observability Setup for Microservice

```bash
# Step 1: Generate dashboards for each service type
python3 scripts/dashboard_generator.py -s payment-api -t api -p grafana -o json -f dashboards/payment-api.json
python3 scripts/dashboard_generator.py -s postgres-main -t database -p grafana -o json -f dashboards/postgres.json
python3 scripts/dashboard_generator.py -s redis-cache -t cache -p grafana -o json -f dashboards/redis.json

# Step 2: Create alert rules with runbook links
python3 scripts/alert_rule_generator.py -s payment-api --slo-target 99.9 -p prometheus --runbook-url https://runbooks.example.com -o yaml -f alerts/payment-api.yaml

# Step 3: Set up SLO tracking
python3 scripts/slo_calculator.py -i payment-api-metrics.csv --target 99.9 --window 30d -o markdown -f slo-report.md
```

### 2. SLO Framework Definition

```bash
# Calculate baseline from historical data
python3 scripts/slo_calculator.py -i historical-metrics.csv --slo-type availability --window 90d -o json

# Get recommendations for achievable SLO target
python3 scripts/slo_calculator.py -i historical-metrics.csv --slo-type latency --target 95 --window 30d -o markdown

# Generate multi-burn-rate alerts based on SLO
python3 scripts/alert_rule_generator.py -s critical-service --slo-target 99.95 --severity critical,warning -p prometheus -o yaml
```

### 3. Metrics Analysis and Optimization

```bash
# Detect anomalies in the last export
python3 scripts/metrics_analyzer.py -i prometheus-export.csv --analysis-type anomaly --threshold 2.5 -o json

# Analyze trends over time
python3 scripts/metrics_analyzer.py -i weekly-metrics.csv --analysis-type trend -o markdown

# Find high-cardinality metrics causing performance issues
python3 scripts/metrics_analyzer.py -i metrics-inventory.csv --analysis-type cardinality -o text
```

### 4. NewRelic Observability Setup

```bash
# Step 1: Generate NewRelic dashboards with NRQL queries
python3 scripts/dashboard_generator.py -s payment-api -t api -p newrelic -o json -f dashboards/payment-api-newrelic.json
python3 scripts/dashboard_generator.py -s postgres-main -t database -p newrelic -o json -f dashboards/postgres-newrelic.json

# Step 2: Create NewRelic alert policies with multi-burn-rate alerting
python3 scripts/alert_rule_generator.py -s payment-api --slo-target 99.9 -p newrelic -o json -f alerts/payment-api-newrelic.json

# Step 3: Review generated NRQL queries
# The dashboard JSON contains NRQL queries like:
# - SELECT rate(count(*), 1 minute) FROM Transaction WHERE appName = 'payment-api'
# - SELECT percentage(count(*), WHERE error IS true) FROM Transaction WHERE appName = 'payment-api'
# - SELECT percentile(duration, 50, 95, 99) FROM Transaction WHERE appName = 'payment-api'

# Step 4: Import to NewRelic via NerdGraph API or UI
# See references/newrelic_patterns.md for detailed import instructions
```

## What to Provide

### For Dashboard Generator
- **Service name**: The name of your service (e.g., `payment-api`, `user-service`)
- **Service type**: One of `api`, `database`, `queue`, `cache`, `web`
- **Platform**: Target platform - `grafana`, `datadog`, `cloudwatch`, or `newrelic`

### For Alert Rule Generator
- **Service name**: The service to create alerts for
- **SLO target**: Your availability target (e.g., 99.9, 99.99)
- **Platform**: Alert platform - `prometheus`, `datadog`, `cloudwatch`, `newrelic`, `pagerduty`

### For SLO Calculator
- **Metrics file**: CSV or JSON with timestamp, total_requests, successful_requests (for availability) or latency values
- **SLO type**: `availability`, `latency`, or `throughput`
- **Target**: Your SLO target percentage

### For Metrics Analyzer
- **Metrics file**: CSV or JSON with timestamp and metric values
- **Analysis type**: `anomaly`, `trend`, `correlation`, `baseline`, or `cardinality`

## What You'll Get

### Dashboard Generator Output
- Complete dashboard configuration (JSON for Grafana, YAML for CloudWatch)
- RED method panels (Rate, Errors, Duration)
- USE method panels (Utilization, Saturation, Errors)
- Variable templating for multi-instance views
- Threshold annotations for at-a-glance health

### Alert Rule Generator Output
- Production-ready alert rules in platform-specific format
- Multi-window, multi-burn-rate alerts for SLO violations
- Runbook links embedded in alert annotations
- Inhibition rules to prevent alert storms
- Severity-based classification and routing

### SLO Calculator Output
- Current SLI value and SLO compliance status
- Error budget (total, consumed, remaining percentage)
- Burn rate analysis (1h, 6h, 24h windows)
- Recommendations for SLO targets based on historical performance
- Alert threshold suggestions

### Metrics Analyzer Output
- Statistical baselines (mean, median, percentiles)
- Detected anomalies with severity and timestamps
- Trend direction and strength
- Cardinality counts and optimization recommendations
- Actionable improvement suggestions

## Python Tools Available

| Tool | Path | Purpose |
|------|------|---------|
| Dashboard Generator | `scripts/dashboard_generator.py` | Generate monitoring dashboards |
| Alert Rule Generator | `scripts/alert_rule_generator.py` | Create alerting rules |
| SLO Calculator | `scripts/slo_calculator.py` | Calculate error budgets |
| Metrics Analyzer | `scripts/metrics_analyzer.py` | Analyze metric patterns |

## Tips for Best Results

1. **Start with baselines**: Use `slo_calculator.py` to understand your current performance before setting SLO targets
2. **Match dashboard to service type**: API services need RED dashboards, databases need USE dashboards
3. **Use multi-burn-rate alerting**: Catches both fast burns (incidents) and slow burns (degradation)
4. **Review cardinality regularly**: High cardinality is the #1 cause of monitoring performance issues
5. **Keep runbooks updated**: Every alert should have a corresponding, tested runbook

## Related Skills

- **[senior-devops](../senior-devops/)** - Deploy and manage the monitoring infrastructure
- **[senior-backend](../senior-backend/)** - Application instrumentation for custom metrics
- **[senior-secops](../senior-secops/)** - Security monitoring and compliance alerting
