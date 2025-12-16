# Alerting and Runbooks Reference

Comprehensive guide to alert design, SLI/SLO frameworks, and incident response runbooks.

## Table of Contents

1. [Alert Design Principles](#alert-design-principles)
2. [SLI/SLO/SLA Framework](#slislosla-framework)
3. [Multi-Burn-Rate Alerting](#multi-burn-rate-alerting)
4. [Escalation Policies](#escalation-policies)
5. [Runbook Structure](#runbook-structure)
6. [Common Runbooks](#common-runbooks)
7. [Alert Fatigue Prevention](#alert-fatigue-prevention)
8. [Incident Response Integration](#incident-response-integration)

---

## Alert Design Principles

### Symptom-Based vs Cause-Based

**Symptom-based (Preferred):**
- Alert on user-visible impact
- "Error rate is high" rather than "Database is slow"
- Fewer alerts, more actionable

**Cause-based (Use Sparingly):**
- Alert on internal component failure
- Useful for preventive alerting
- Can cause alert noise

### The 3 A's of Alerts

1. **Actionable** - Someone can do something about it
2. **Accurate** - Low false positive rate
3. **Appropriate** - Right urgency level

### Alert Categories

| Category | Example | Page? | Timing |
|----------|---------|-------|--------|
| **Critical** | Service down, data loss risk | Yes | Immediate |
| **Warning** | Degraded performance, approaching limits | Maybe | Business hours |
| **Info** | Non-urgent, tracked | No | Async review |

### What NOT to Alert On

- Things that auto-recover (use metrics instead)
- Internal metrics without user impact
- Things no one can fix
- Duplicate alerts for same issue

---

## SLI/SLO/SLA Framework

### Definitions

| Term | Definition | Owner | Example |
|------|------------|-------|---------|
| **SLI** | Service Level Indicator - measured metric | Engineering | 99.95% requests < 200ms |
| **SLO** | Service Level Objective - target for SLI | Engineering | 99.9% availability |
| **SLA** | Service Level Agreement - contract | Business | 99.5% with penalties |

### SLI Types

**Availability SLI:**
```
successful_requests / total_requests * 100

PromQL:
sum(rate(http_requests_total{status!~"5.."}[30d]))
/
sum(rate(http_requests_total[30d])) * 100
```

**Latency SLI:**
```
requests_below_threshold / total_requests * 100

PromQL:
sum(rate(http_request_duration_seconds_bucket{le="0.2"}[30d]))
/
sum(rate(http_request_duration_seconds_count[30d])) * 100
```

**Throughput SLI:**
```
periods_meeting_rps_target / total_periods * 100
```

### Error Budget

**Calculation:**
```
Error Budget = 100% - SLO Target

Example:
SLO = 99.9%
Error Budget = 0.1% = 43.2 minutes/month
```

**Error Budget Policy:**

| Budget Remaining | Action |
|-----------------|--------|
| > 50% | Normal development velocity |
| 25-50% | Reduce risky deployments |
| 10-25% | Focus on reliability work |
| < 10% | Feature freeze, all hands on reliability |
| Exhausted | Incident review, postmortem required |

### SLO Examples by Service Tier

| Tier | Availability | Latency (P99) | Use Case |
|------|-------------|---------------|----------|
| **Tier 0** | 99.99% | < 100ms | Payment, Auth |
| **Tier 1** | 99.9% | < 200ms | Core API |
| **Tier 2** | 99.5% | < 500ms | Internal tools |
| **Tier 3** | 99% | < 1s | Batch jobs |

---

## Multi-Burn-Rate Alerting

### Concept

Alert based on how fast you're consuming error budget, not just current error rate.

**Burn Rate = Actual Error Rate / Allowed Error Rate**

### Standard Windows

| Alert | Short Window | Long Window | Burn Rate | Budget Consumed |
|-------|-------------|-------------|-----------|-----------------|
| Critical | 5m | 1h | 14.4x | 2% in 1 hour |
| Critical | 30m | 6h | 6x | 5% in 6 hours |
| Warning | 2h | 1d | 3x | 10% in 1 day |
| Warning | 6h | 3d | 1x | 10% in 3 days |

### Prometheus Alert Rules

```yaml
groups:
- name: slo-alerts
  rules:
  # Critical: Fast burn (2% budget in 1 hour)
  - alert: SLOHighBurnRate1h
    expr: |
      (
        sum(rate(http_requests_total{status=~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m]))
      ) > (14.4 * 0.001)  # 14.4x burn rate for 99.9% SLO
      and
      (
        sum(rate(http_requests_total{status=~"5.."}[1h]))
        /
        sum(rate(http_requests_total[1h]))
      ) > (14.4 * 0.001)
    for: 2m
    labels:
      severity: critical
      slo: availability
    annotations:
      summary: "High error rate burning SLO budget fast"
      description: "Error budget being consumed at 14.4x sustainable rate"
      runbook_url: "https://runbooks.example.com/slo-burn"

  # Warning: Slow burn (10% budget in 3 days)
  - alert: SLOSlowBurnRate3d
    expr: |
      (
        sum(rate(http_requests_total{status=~"5.."}[6h]))
        /
        sum(rate(http_requests_total[6h]))
      ) > (1.0 * 0.001)
      and
      (
        sum(rate(http_requests_total{status=~"5.."}[3d]))
        /
        sum(rate(http_requests_total[3d]))
      ) > (1.0 * 0.001)
    for: 1h
    labels:
      severity: warning
      slo: availability
    annotations:
      summary: "Sustained elevated error rate"
      description: "Error rate consistently above SLO threshold"
```

### Why Multi-Window?

| Scenario | Short Window Only | Multi-Window |
|----------|-------------------|--------------|
| Brief spike, recovered | Alert! (noise) | No alert (correct) |
| Sustained issue | Alert! | Alert! |
| Slow degradation | May miss | Alert! |

---

## Escalation Policies

### Escalation Tiers

| Tier | Response Time | Who | Authority |
|------|---------------|-----|-----------|
| **L1** | 5 min | On-call engineer | Restart, scale, rollback |
| **L2** | 15 min | Team lead/senior | Code fixes, config changes |
| **L3** | 30 min | Architect/principal | Major decisions, vendor contact |
| **Incident Commander** | As needed | Manager | Communication, coordination |

### On-Call Rotation

**Schedule Template:**
```yaml
schedule:
  name: payment-team-oncall
  timezone: America/New_York
  rotation:
    type: weekly
    handoff_time: "09:00"
    handoff_day: Monday
  layers:
    - primary:
        rotation_length: 7 days
        participants:
          - alice@company.com
          - bob@company.com
          - carol@company.com
    - secondary:
        rotation_length: 7 days
        start_offset: 3 days
        participants:
          - dave@company.com
          - eve@company.com
```

### PagerDuty Integration

```yaml
# AlertManager config
receivers:
- name: 'pagerduty-critical'
  pagerduty_configs:
  - service_key: '<YOUR_SERVICE_KEY>'
    severity: critical
    description: '{{ .CommonAnnotations.summary }}'
    details:
      firing: '{{ template "pagerduty.default.instances" .Alerts.Firing }}'
      runbook_url: '{{ .CommonAnnotations.runbook_url }}'

- name: 'pagerduty-warning'
  pagerduty_configs:
  - service_key: '<YOUR_SERVICE_KEY>'
    severity: warning
    description: '{{ .CommonAnnotations.summary }}'

route:
  receiver: 'pagerduty-warning'
  routes:
  - match:
      severity: critical
    receiver: 'pagerduty-critical'
    repeat_interval: 5m
  - match:
      severity: warning
    receiver: 'pagerduty-warning'
    repeat_interval: 30m
```

---

## Runbook Structure

### Standard Template

```markdown
# Alert: [Alert Name]

## Overview
- **Severity:** Critical/Warning/Info
- **Service:** [Service name]
- **SLO Impact:** [Which SLO is affected]
- **Last Updated:** [Date]

## Alert Meaning
[What this alert indicates in plain language]

## Impact Assessment
- [ ] Who is affected? (All users / Specific region / Specific feature)
- [ ] What functionality is degraded?
- [ ] Is there data loss risk?

## Diagnostic Steps

### 1. Verify the Alert
```bash
# Check current metric value
curl -s "http://prometheus:9090/api/v1/query?query=<metric>" | jq
```

### 2. Check Service Health
```bash
# Check pod status
kubectl get pods -l app=<service>

# Check recent logs
kubectl logs -l app=<service> --tail=100 --since=10m
```

### 3. Check Dependencies
- [ ] Database connectivity
- [ ] Redis cache
- [ ] External APIs

## Remediation Steps

### Quick Fixes (Try First)
1. **Restart the service**
   ```bash
   kubectl rollout restart deployment/<service>
   ```

2. **Scale up**
   ```bash
   kubectl scale deployment/<service> --replicas=5
   ```

3. **Rollback recent deployment**
   ```bash
   kubectl rollout undo deployment/<service>
   ```

### If Quick Fixes Don't Work
1. Check recent changes in deployment history
2. Review error logs for root cause
3. Escalate to L2 if not resolved in 15 minutes

## Escalation

### When to Escalate
- Quick fixes not working after 15 minutes
- Data loss suspected
- Multiple services affected
- Customer-reported widespread outage

### Escalation Contacts
- **L2:** @oncall-senior (Slack)
- **L3:** @team-lead (Slack)
- **Incident Commander:** Page via PagerDuty

## Post-Incident

- [ ] Update incident timeline
- [ ] Collect relevant logs and metrics
- [ ] Schedule postmortem if > 15 min duration
- [ ] Update this runbook if needed
```

---

## Common Runbooks

### High Error Rate

**Alert:** `ServiceHighErrorRate`

**Quick Diagnosis:**
```bash
# Get error breakdown
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (endpoint)" | jq

# Check recent deployments
kubectl rollout history deployment/api-service

# Check logs for errors
kubectl logs -l app=api-service --tail=500 | grep -i error | tail -50
```

**Common Causes & Fixes:**

| Cause | Indicator | Fix |
|-------|-----------|-----|
| Bad deployment | Started after deploy | Rollback |
| Dependency down | Timeout errors | Check dependency |
| Resource exhaustion | OOMKilled, CPU throttle | Scale up |
| Traffic spike | Request rate spike | Scale up, rate limit |

### High Latency

**Alert:** `ServiceHighLatency`

**Quick Diagnosis:**
```bash
# Check latency by endpoint
curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))" | jq

# Check database query times
kubectl logs -l app=api-service | grep "query_time" | sort -t= -k2 -rn | head -10
```

**Common Causes & Fixes:**

| Cause | Indicator | Fix |
|-------|-----------|-----|
| Slow queries | DB metrics high | Add indexes, optimize |
| Cache miss | Cache hit rate low | Warm cache, check eviction |
| Cold start | After deployment | Pre-warm, increase instances |
| External API slow | Trace shows external latency | Add timeout, fallback |

### Service Down

**Alert:** `ServiceDown`

**Immediate Actions:**
```bash
# 1. Check pod status
kubectl get pods -l app=<service> -o wide

# 2. Check events
kubectl get events --sort-by='.lastTimestamp' | tail -20

# 3. Check node status
kubectl get nodes

# 4. Check for OOM
kubectl describe pod <pod-name> | grep -A5 "Last State"
```

**Recovery Steps:**
1. If CrashLoopBackOff: Check logs, likely app bug or config issue
2. If Pending: Check resource availability, node capacity
3. If OOMKilled: Increase memory limits
4. If ImagePullBackOff: Check image exists, registry credentials

### Database Connection Issues

**Alert:** `DatabaseConnectionErrors`

**Diagnosis:**
```bash
# Check connection count
kubectl exec -it <db-pod> -- psql -c "SELECT count(*) FROM pg_stat_activity;"

# Check for locks
kubectl exec -it <db-pod> -- psql -c "SELECT * FROM pg_locks WHERE NOT granted;"

# Check replication lag
kubectl exec -it <db-pod> -- psql -c "SELECT * FROM pg_stat_replication;"
```

**Common Fixes:**
1. Connection pool exhausted → Restart app or increase pool size
2. Too many connections → Kill idle connections
3. Replication lag → Check network, disk I/O

---

## Alert Fatigue Prevention

### Monthly Alert Review

**Questions to Ask:**

1. **Is this alert actionable?**
   - Can someone do something about it?
   - If auto-resolves, maybe it shouldn't page

2. **Is the threshold correct?**
   - Too sensitive = noise
   - Not sensitive enough = missed incidents

3. **Does this still matter?**
   - Services change, alerts should too

4. **Is there a better signal?**
   - Maybe a symptom rather than cause

### Metrics to Track

```promql
# Alert frequency
sum(increase(ALERTS{alertstate="firing"}[30d])) by (alertname)

# Mean time to acknowledge
avg(alertmanager_notification_latency_seconds) by (alertname)

# False positive rate (manual tracking)
# Target: < 5% of pages should be false positives
```

### Silencing vs Fixing

**When to Silence:**
- Known maintenance window
- Known bug with fix in progress
- Temporary condition

**When to Fix:**
- Same alert firing repeatedly
- Alert never acted upon
- Alert conditions changed

### Alert Hygiene Checklist

- [ ] Every alert has a runbook
- [ ] Runbooks are up to date
- [ ] Thresholds reviewed quarterly
- [ ] Unused alerts removed
- [ ] Alert ownership is clear
- [ ] Escalation paths documented

---

## Incident Response Integration

### Incident Lifecycle

```
Alert → Acknowledge → Diagnose → Mitigate → Resolve → Postmortem
  │          │           │           │          │          │
  │          │           │           │          │          └── Learn
  │          │           │           │          └── Verify fix
  │          │           │           └── Stop bleeding
  │          │           └── Find root cause
  │          └── Take ownership
  └── Detection
```

### Incident Severity Levels

| Level | Definition | Response | Communication |
|-------|------------|----------|---------------|
| **SEV1** | Total outage | All hands | Exec + customers |
| **SEV2** | Major degradation | Team + escalation | Management |
| **SEV3** | Minor issue | On-call | Team |
| **SEV4** | No impact | Next business day | None |

### Incident Communication Template

```markdown
## Incident Update - [Service Name] - [Timestamp]

**Status:** Investigating / Identified / Monitoring / Resolved

**Impact:**
- [X users/customers affected]
- [X% of requests failing]
- [Specific feature unavailable]

**Current Understanding:**
[Brief description of what we know]

**Actions Taken:**
1. [Action 1]
2. [Action 2]

**Next Steps:**
1. [Planned action]
2. [Planned action]

**Next Update:** [Time] or when status changes

---
Incident Commander: [Name]
Technical Lead: [Name]
```

### Postmortem Trigger Criteria

**Always postmortem if:**
- SEV1 or SEV2 incident
- Customer-reported outage
- Data loss or security issue
- Same alert fired 3+ times in a week

**Postmortem Template:**
```markdown
# Incident Postmortem: [Title]

**Date:** [Incident date]
**Duration:** [Start to resolution]
**Severity:** SEV[1-4]
**Author:** [Name]

## Summary
[2-3 sentence summary of what happened]

## Impact
- Users affected: [Number]
- Duration: [Minutes]
- Revenue impact: [If applicable]

## Timeline
| Time | Event |
|------|-------|
| HH:MM | Alert fired |
| HH:MM | On-call acknowledged |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Full resolution |

## Root Cause
[Detailed explanation of what caused the incident]

## What Went Well
- [Good thing 1]
- [Good thing 2]

## What Went Poorly
- [Problem 1]
- [Problem 2]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | Open |

## Lessons Learned
[Key takeaways for the team]
```

---

## Quick Reference

### Alert Severity Decision Tree

```
Is there user-visible impact?
├─ Yes → Is data at risk?
│        ├─ Yes → CRITICAL (page immediately)
│        └─ No → Is it widespread?
│                ├─ Yes → CRITICAL
│                └─ No → WARNING (page business hours)
└─ No → Is it likely to cause impact soon?
         ├─ Yes → WARNING
         └─ No → INFO (no page)
```

### Essential Prometheus Alerts

```yaml
# Service down
- alert: ServiceDown
  expr: up == 0
  for: 1m
  labels:
    severity: critical

# High error rate
- alert: HighErrorRate
  expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
  for: 5m
  labels:
    severity: critical

# High latency
- alert: HighLatency
  expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 1
  for: 5m
  labels:
    severity: warning

# Low disk space
- alert: LowDiskSpace
  expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
  for: 10m
  labels:
    severity: warning
```

---

## Resources

- [Google SRE Book - Alerting](https://sre.google/sre-book/alerting-on-slos/)
- [Alerting on SLOs (Google)](https://sre.google/workbook/alerting-on-slos/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Atlassian Incident Management](https://www.atlassian.com/incident-management)
- [Blameless Postmortems](https://www.blameless.com/sre/what-are-blameless-postmortems)
