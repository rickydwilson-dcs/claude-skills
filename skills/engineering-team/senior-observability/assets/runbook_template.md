# Runbook Template: {{ALERT_NAME}}

## Overview

| Field | Value |
|-------|-------|
| **Alert Name** | {{ALERT_NAME}} |
| **Severity** | {{SEVERITY}} (critical/high/warning/info) |
| **Service** | {{SERVICE_NAME}} |
| **Team** | {{TEAM_NAME}} |
| **Last Updated** | {{DATE}} |
| **Author** | {{AUTHOR}} |

## Alert Description

{{DESCRIPTION}}

### When This Alert Fires

This alert fires when:
- {{CONDITION_1}}
- {{CONDITION_2}}

### Impact

**User Impact:**
- {{USER_IMPACT}}

**Business Impact:**
- {{BUSINESS_IMPACT}}

---

## Quick Reference

### Key Metrics

| Metric | PromQL Query | Expected Range |
|--------|--------------|----------------|
| {{METRIC_1}} | `{{QUERY_1}}` | {{RANGE_1}} |
| {{METRIC_2}} | `{{QUERY_2}}` | {{RANGE_2}} |

### Key Dashboards

| Dashboard | Link |
|-----------|------|
| Service Overview | [Link]({{DASHBOARD_URL_1}}) |
| SLO Dashboard | [Link]({{DASHBOARD_URL_2}}) |
| Trace View | [Link]({{TRACE_URL}}) |

### Key Logs

```
# Kibana/Loki query
{{LOG_QUERY}}
```

---

## Diagnosis Steps

### Step 1: Assess Severity

```bash
# Check current error rate
curl -s "http://prometheus:9090/api/v1/query?query={{ERROR_RATE_QUERY}}" | jq '.data.result[0].value[1]'

# Check number of affected instances
kubectl get pods -l app={{SERVICE_NAME}} -o wide
```

**Questions to answer:**
- [ ] How many users are affected?
- [ ] What is the geographic scope?
- [ ] When did the issue start?

### Step 2: Gather Context

```bash
# Recent deployments
kubectl rollout history deployment/{{SERVICE_NAME}}

# Recent changes
git log --oneline --since="2 hours ago" -- path/to/service

# Pod events
kubectl describe pod -l app={{SERVICE_NAME}} | grep -A 10 "Events:"
```

### Step 3: Check Dependencies

```bash
# Database connectivity
kubectl exec -it {{SERVICE_NAME}}-pod -- curl -s http://database:5432/health

# External service status
curl -s "https://status.external-api.com/api/v2/status.json"
```

### Step 4: Review Logs

```bash
# Recent errors
kubectl logs -l app={{SERVICE_NAME}} --since=30m | grep -i error | tail -50

# Structured log search (Loki)
logcli query '{app="{{SERVICE_NAME}}"} |= "error"' --limit 100

# Full context around errors
kubectl logs -l app={{SERVICE_NAME}} --since=30m | grep -A 5 -B 5 "{{ERROR_PATTERN}}"
```

### Step 5: Review Traces

1. Open [Jaeger/Tempo]({{TRACE_URL}})
2. Filter by service: `{{SERVICE_NAME}}`
3. Filter by status: `error`
4. Look for:
   - Slow spans
   - Error spans
   - Missing spans (dropped requests)

---

## Common Causes and Resolutions

### Cause 1: {{CAUSE_1}}

**Symptoms:**
- {{SYMPTOM_1}}
- {{SYMPTOM_2}}

**Resolution:**

```bash
# Step 1
{{RESOLUTION_STEP_1}}

# Step 2
{{RESOLUTION_STEP_2}}
```

**Verification:**
```bash
# Verify the fix
{{VERIFICATION_COMMAND}}
```

---

### Cause 2: {{CAUSE_2}}

**Symptoms:**
- {{SYMPTOM_3}}
- {{SYMPTOM_4}}

**Resolution:**

```bash
# Resolution steps
{{RESOLUTION_STEPS}}
```

---

### Cause 3: Dependency Failure

**Symptoms:**
- Timeout errors in logs
- Increased latency
- Connection refused errors

**Resolution:**

1. Identify failing dependency from traces
2. Check dependency health:
   ```bash
   kubectl get pods -l app={{DEPENDENCY_NAME}}
   ```
3. If dependency is unhealthy, escalate to dependency team
4. Consider enabling circuit breaker:
   ```bash
   kubectl set env deployment/{{SERVICE_NAME}} ENABLE_CIRCUIT_BREAKER=true
   ```

---

## Mitigation Strategies

### Immediate Mitigation

**Option A: Scale Up**
```bash
kubectl scale deployment/{{SERVICE_NAME}} --replicas=10
```

**Option B: Rollback**
```bash
kubectl rollout undo deployment/{{SERVICE_NAME}}
```

**Option C: Feature Flag**
```bash
# Disable problematic feature
kubectl set env deployment/{{SERVICE_NAME}} FEATURE_{{FEATURE_NAME}}_ENABLED=false
```

**Option D: Traffic Shifting**
```bash
# Shift traffic to healthy region
kubectl patch virtualservice {{SERVICE_NAME}} --type=merge -p '{"spec":{"http":[{"route":[{"destination":{"host":"{{SERVICE_NAME}}","subset":"stable"},"weight":100}]}]}}'
```

### Communication

**For Critical Alerts:**

1. Post to #incidents Slack channel:
   ```
   :rotating_light: INCIDENT: {{SERVICE_NAME}} {{ALERT_NAME}}
   Impact: {{IMPACT_SUMMARY}}
   Status: Investigating
   Lead: @{{YOUR_NAME}}
   ```

2. Update status page if user-facing

3. Start incident call if needed:
   - Zoom: {{INCIDENT_CALL_LINK}}
   - Bridge: {{BRIDGE_NUMBER}}

---

## Escalation

### Escalation Path

| Level | Team | Contact | When to Escalate |
|-------|------|---------|------------------|
| L1 | On-Call Engineer | PagerDuty | First response |
| L2 | {{TEAM_NAME}} Lead | @{{LEAD_SLACK}} | After 15 min without progress |
| L3 | Engineering Manager | @{{EM_SLACK}} | Major incident / customer impact |
| L4 | VP Engineering | @{{VP_SLACK}} | SEV1 / revenue impact |

### When to Escalate

- [ ] Issue persists > 15 minutes without progress
- [ ] Need access to systems you don't have
- [ ] Customer-reported issues
- [ ] Multiple services affected
- [ ] Data integrity concerns

### External Escalation

| Dependency | Contact | SLA |
|------------|---------|-----|
| {{EXTERNAL_SERVICE_1}} | {{CONTACT_1}} | {{SLA_1}} |
| {{EXTERNAL_SERVICE_2}} | {{CONTACT_2}} | {{SLA_2}} |

---

## Post-Incident

### Verification Checklist

After resolving the issue, verify:

- [ ] Error rate returned to baseline
- [ ] Latency returned to baseline
- [ ] No alert still firing
- [ ] Customer impact confirmed resolved
- [ ] All pods healthy

```bash
# Verification commands
kubectl get pods -l app={{SERVICE_NAME}} | grep -v Running
curl -s "http://prometheus:9090/api/v1/query?query={{ERROR_RATE_QUERY}}" | jq '.data.result[0].value[1]'
```

### Documentation

- [ ] Update incident timeline
- [ ] Create incident report (for SEV1/SEV2)
- [ ] Update this runbook if needed
- [ ] Create follow-up tickets for improvements

---

## Related Documentation

- [Service Architecture]({{ARCHITECTURE_DOC_URL}})
- [Deployment Guide]({{DEPLOYMENT_DOC_URL}})
- [API Documentation]({{API_DOC_URL}})
- [Previous Incidents]({{INCIDENT_HISTORY_URL}})

---

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| {{DATE}} | {{AUTHOR}} | Initial version |

---

## Template Usage Notes

Replace the following placeholders when creating a new runbook:

| Placeholder | Description |
|-------------|-------------|
| `{{ALERT_NAME}}` | Name of the alert this runbook covers |
| `{{SEVERITY}}` | Alert severity level |
| `{{SERVICE_NAME}}` | Name of the affected service |
| `{{TEAM_NAME}}` | Owning team name |
| `{{DATE}}` | Current date (YYYY-MM-DD) |
| `{{AUTHOR}}` | Your name |
| `{{DESCRIPTION}}` | Brief description of the alert |
| `{{CONDITION_*}}` | Alert firing conditions |
| `{{*_IMPACT}}` | Impact descriptions |
| `{{METRIC_*}}` | Key metric names |
| `{{QUERY_*}}` | PromQL queries |
| `{{RANGE_*}}` | Expected value ranges |
| `{{DASHBOARD_URL_*}}` | Dashboard links |
| `{{LOG_QUERY}}` | Log search query |
| `{{ERROR_RATE_QUERY}}` | PromQL for error rate |
| `{{ERROR_PATTERN}}` | Error message pattern to search |
| `{{TRACE_URL}}` | Tracing UI URL |
| `{{CAUSE_*}}` | Common causes |
| `{{SYMPTOM_*}}` | Observable symptoms |
| `{{RESOLUTION_*}}` | Resolution steps |
| `{{VERIFICATION_COMMAND}}` | Command to verify fix |
| `{{DEPENDENCY_NAME}}` | Name of dependency service |
| `{{FEATURE_NAME}}` | Feature flag name |
| `{{INCIDENT_CALL_LINK}}` | Video call link |
| `{{BRIDGE_NUMBER}}` | Phone bridge number |
| `{{*_SLACK}}` | Slack handles |
| `{{EXTERNAL_SERVICE_*}}` | External dependency names |
| `{{CONTACT_*}}` | Contact information |
| `{{SLA_*}}` | SLA terms |
| `{{*_DOC_URL}}` | Documentation links |
