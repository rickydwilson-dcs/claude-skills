# ServiceNow ITSM Integration Patterns

Comprehensive guide for integrating observability tools with ServiceNow for incident management, CMDB linking, and change request automation.

## Table of Contents

1. [ServiceNow REST API Overview](#servicenow-rest-api-overview)
2. [Incident Management API](#incident-management-api)
3. [Event Management Integration](#event-management-integration)
4. [CMDB Configuration Items](#cmdb-configuration-items)
5. [Status Synchronization](#status-synchronization)
6. [Alert-to-Incident Mapping](#alert-to-incident-mapping)
7. [Authentication Methods](#authentication-methods)
8. [Error Handling Patterns](#error-handling-patterns)
9. [Best Practices](#best-practices)

---

## ServiceNow REST API Overview

### Base URL Structure
```
https://<instance>.service-now.com/api/now/<version>/<resource>
```

### Common Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/now/table/incident` | POST | Create incident |
| `/api/now/table/incident/{sys_id}` | PUT | Update incident |
| `/api/now/table/incident/{sys_id}` | GET | Get incident details |
| `/api/now/table/change_request` | POST | Create change request |
| `/api/now/table/cmdb_ci` | GET | Query Configuration Items |
| `/api/global/em/jsonv2` | POST | Create event (Event Management) |

### Required Headers

```http
Content-Type: application/json
Accept: application/json
Authorization: Basic <base64(username:password)>
```

Or with OAuth:
```http
Authorization: Bearer <access_token>
```

---

## Incident Management API

### Create Incident

**Endpoint:** `POST /api/now/table/incident`

**Request Body:**
```json
{
  "short_description": "High CPU on payment-service-prod",
  "description": "Alert: CPU usage exceeded 90% threshold\nSeverity: P1\nSource: Prometheus AlertManager\nRunbook: https://runbooks.example.com/high-cpu\n\nAffected Service: payment-service\nEnvironment: production\nCluster: anz-prod-1",
  "category": "Software",
  "subcategory": "Application",
  "impact": "2",
  "urgency": "1",
  "priority": "2",
  "assignment_group": "Platform Engineering",
  "cmdb_ci": "payment-service-prod",
  "caller_id": "monitoring-system",
  "contact_type": "Monitoring",
  "u_source_system": "Pandora",
  "u_environment": "production"
}
```

**Response (201 Created):**
```json
{
  "result": {
    "sys_id": "abc123def456",
    "number": "INC0012345",
    "short_description": "High CPU on payment-service-prod",
    "state": "1",
    "priority": "2"
  }
}
```

### Update Incident Status

**Endpoint:** `PUT /api/now/table/incident/{sys_id}`

**Request Body (Acknowledge):**
```json
{
  "state": "2",
  "work_notes": "Incident acknowledged. Investigating root cause.\n\nAssigned engineer: John Smith\nETA for initial assessment: 30 minutes"
}
```

**Request Body (Resolve):**
```json
{
  "state": "6",
  "close_code": "Resolved",
  "close_notes": "Root cause identified: Memory leak in payment service v2.3.1\n\nResolution: Rolled back to v2.3.0 and scheduled hotfix deployment.\n\nTime to detect: 5 minutes\nTime to resolve: 45 minutes",
  "resolution_code": "Resolved",
  "resolved_by": "monitoring-system"
}
```

### Query Incidents

**Endpoint:** `GET /api/now/table/incident`

**Query Parameters:**
```
?sysparm_query=active=true^priority<=2^assignment_group=Platform Engineering
&sysparm_display_value=true
&sysparm_limit=100
&sysparm_fields=number,short_description,state,priority,sys_id
```

**Common Query Operators:**

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `state=1` | Equals |
| `!=` | `state!=7` | Not equals |
| `STARTSWITH` | `numberSTARTSWITHINC` | Starts with |
| `CONTAINS` | `short_descriptionCONTAINScpu` | Contains |
| `^` | `state=1^priority=1` | AND |
| `^OR` | `state=1^ORstate=2` | OR |
| `ORDERBY` | `ORDERBYpriority` | Sort ascending |
| `ORDERBYDESC` | `ORDERBYDESCsys_created_on` | Sort descending |

---

## Event Management Integration

If your ServiceNow instance has Event Management licensed, use the Event API for better alert correlation and deduplication.

### Create Event

**Endpoint:** `POST /api/global/em/jsonv2`

**Request Body:**
```json
{
  "records": [
    {
      "source": "Prometheus",
      "event_class": "prometheus_alert",
      "node": "payment-service-pod-abc123",
      "resource": "payment-service",
      "type": "High CPU Usage",
      "severity": "2",
      "description": "CPU usage at 95% on payment-service-pod-abc123",
      "additional_info": {
        "alertname": "HighCPU",
        "namespace": "production",
        "pod": "payment-service-pod-abc123",
        "threshold": "90%",
        "current_value": "95%",
        "runbook_url": "https://runbooks.example.com/high-cpu"
      },
      "ci_identifier": {
        "name": "payment-service-prod"
      }
    }
  ]
}
```

### Event Severity Mapping

| Alert Severity | ServiceNow Event Severity | Value |
|----------------|---------------------------|-------|
| Critical (P0) | Critical | 1 |
| High (P1) | Major | 2 |
| Medium (P2) | Minor | 3 |
| Low (P3) | Warning | 4 |
| Info | Info | 5 |

### Event-to-Incident Correlation

ServiceNow Event Management can automatically:
1. **Deduplicate** events from the same source/CI
2. **Correlate** related events into a single incident
3. **Auto-resolve** incidents when OK events are received
4. **Enrich** events with CMDB data

**Alert Rule Example (for auto-incident creation):**
```
IF event.severity <= 2 AND event.resource IN cmdb_ci
THEN create incident WITH priority = event.severity
```

---

## CMDB Configuration Items

### Query CI by Name

**Endpoint:** `GET /api/now/table/cmdb_ci_appl`

**Query:**
```
?sysparm_query=name=payment-service-prod
&sysparm_fields=sys_id,name,operational_status,business_criticality,supported_by
```

**Response:**
```json
{
  "result": [
    {
      "sys_id": "ci_abc123",
      "name": "payment-service-prod",
      "operational_status": "1",
      "business_criticality": "1 - most critical",
      "supported_by": {
        "display_value": "Platform Engineering",
        "value": "group_sys_id_123"
      }
    }
  ]
}
```

### CI Classes by Type

| Service Type | CI Class | Table Name |
|-------------|----------|------------|
| Application | Application | cmdb_ci_appl |
| Server | Server | cmdb_ci_server |
| Database | Database | cmdb_ci_database |
| Kubernetes Cluster | Kubernetes Cluster | cmdb_ci_kubernetes_cluster |
| Docker Container | Docker Container | cmdb_ci_docker_container |
| Network Device | Network Gear | cmdb_ci_netgear |
| Cloud Service | Cloud Service | cmdb_ci_cloud_service |

### Link Incident to CI

Include the CI reference when creating an incident:
```json
{
  "cmdb_ci": "ci_sys_id_or_name",
  "business_service": "related_business_service_sys_id"
}
```

Or use CI identifier for auto-lookup:
```json
{
  "cmdb_ci.name": "payment-service-prod"
}
```

---

## Status Synchronization

### State Flow: Alert → ServiceNow

```
Alert Firing     →  Incident New (1)
Alert Acknowledged →  Incident In Progress (2)
Alert Investigating →  Incident In Progress (2)
Alert Contained  →  Incident On Hold (3)
Alert Resolved   →  Incident Resolved (6)
Alert Closed     →  Incident Closed (7)
```

### ServiceNow Incident States

| State | Value | Description |
|-------|-------|-------------|
| New | 1 | Incident just created, not yet worked |
| In Progress | 2 | Being actively worked |
| On Hold | 3 | Waiting for customer/vendor/change |
| Resolved | 6 | Issue fixed, pending confirmation |
| Closed | 7 | Confirmed resolved, no further action |
| Canceled | 8 | Incident canceled/duplicate |

### Bi-directional Sync Webhook

Configure ServiceNow Business Rule to send updates back to monitoring:

```javascript
// ServiceNow Business Rule (After Update)
(function executeRule(current, previous) {
    var request = new sn_ws.RESTMessageV2('AlertSync', 'UpdateAlert');
    request.setRequestBody(JSON.stringify({
        incident_number: current.number.toString(),
        state: current.state.toString(),
        assigned_to: current.assigned_to.getDisplayValue(),
        work_notes: current.work_notes.getJournalEntry(1)
    }));
    request.execute();
})(current, previous);
```

---

## Alert-to-Incident Mapping

### Prometheus AlertManager → ServiceNow

**AlertManager Webhook Config:**
```yaml
receivers:
  - name: servicenow
    webhook_configs:
      - url: 'https://instance.service-now.com/api/now/table/incident'
        http_config:
          basic_auth:
            username: 'monitoring_user'
            password_file: '/etc/alertmanager/snow_password'
        send_resolved: true
```

**Field Mapping:**

| Prometheus Label/Annotation | ServiceNow Field |
|----------------------------|------------------|
| `alertname` | `short_description` |
| `severity` (critical/warning/info) | `priority` (mapped) |
| `description` (annotation) | `description` |
| `namespace` | `u_environment` |
| `service` | `cmdb_ci` |
| `runbook_url` (annotation) | Included in `description` |

### NewRelic → ServiceNow

**NewRelic Webhook Payload:**
```json
{
  "condition_name": "High Error Rate",
  "current_state": "open",
  "details": "Error rate above 5%",
  "severity": "CRITICAL",
  "entity": {
    "name": "payment-service",
    "type": "APPLICATION"
  },
  "violation_url": "https://one.newrelic.com/..."
}
```

**Field Mapping:**

| NewRelic Field | ServiceNow Field |
|---------------|------------------|
| `condition_name` | `short_description` |
| `severity` | `priority` (mapped) |
| `details` | `description` |
| `entity.name` | `cmdb_ci` |
| `violation_url` | Included in `description` |

### PagerDuty → ServiceNow (Bi-directional)

PagerDuty has native ServiceNow integration. Key mappings:

| PagerDuty | ServiceNow |
|-----------|------------|
| Incident triggered | Incident created |
| Incident acknowledged | State → In Progress |
| Incident resolved | State → Resolved |
| Priority (P1-P5) | Priority (1-5) |

---

## Authentication Methods

### Basic Authentication

```bash
# Generate base64 encoded credentials
echo -n "username:password" | base64

# Use in header
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

### OAuth 2.0

**Token Request:**
```bash
curl -X POST "https://instance.service-now.com/oauth_token.do" \
  -d "grant_type=password" \
  -d "client_id=<client_id>" \
  -d "client_secret=<client_secret>" \
  -d "username=<username>" \
  -d "password=<password>"
```

**Response:**
```json
{
  "access_token": "abc123...",
  "refresh_token": "def456...",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

### API Key (Scoped Application)

For server-to-server integrations, create a scoped application with an API key:
```
Authorization: Bearer <api_key>
```

---

## Error Handling Patterns

### Common Error Responses

**401 Unauthorized:**
```json
{
  "error": {
    "message": "User Not Authenticated",
    "detail": "Required to provide Auth information"
  },
  "status": "failure"
}
```

**403 Forbidden:**
```json
{
  "error": {
    "message": "Insufficient rights to create incident",
    "detail": "User does not have the 'itil' role"
  },
  "status": "failure"
}
```

**400 Bad Request:**
```json
{
  "error": {
    "message": "Invalid value",
    "detail": "priority: Invalid value 'critical' for field priority"
  },
  "status": "failure"
}
```

### Retry Strategy

```python
# Recommended retry pattern
MAX_RETRIES = 3
RETRY_DELAYS = [1, 5, 15]  # seconds

for attempt in range(MAX_RETRIES):
    response = make_request()
    if response.status_code == 429:  # Rate limited
        time.sleep(RETRY_DELAYS[attempt])
        continue
    elif response.status_code >= 500:  # Server error
        time.sleep(RETRY_DELAYS[attempt])
        continue
    else:
        break
```

### Rate Limiting

ServiceNow default rate limits:
- **REST API:** 100 requests/minute per user
- **Event API:** 500 events/minute

Handle `429 Too Many Requests` with exponential backoff.

---

## Best Practices

### 1. Use Display Values for Readability

Add `sysparm_display_value=true` to get human-readable values:
```
GET /api/now/table/incident?sysparm_display_value=true
```

### 2. Limit Fields Returned

Reduce payload size by specifying needed fields:
```
&sysparm_fields=number,short_description,state,priority
```

### 3. Use Batch Operations

For multiple incidents, use batch API:
```
POST /api/now/v2/table/incident/batch
```

### 4. Include Correlation IDs

Always include external alert IDs for traceability:
```json
{
  "correlation_id": "prometheus-alert-12345",
  "u_external_ref": "PD-incident-67890"
}
```

### 5. Structure Descriptions

Use consistent formatting in descriptions:
```
Alert: {alert_name}
Severity: {severity}
Source: {source_system}
Timestamp: {timestamp}

Affected Systems:
- {service_name} ({environment})

Metrics:
- Current Value: {current}
- Threshold: {threshold}

Runbook: {runbook_url}
```

### 6. Test in Sub-Production

Always test integrations in ServiceNow sub-production instance first:
```
https://instance-dev.service-now.com
```

### 7. Monitor Integration Health

Track these metrics:
- API response times
- Error rates by type
- Incident creation latency
- Event-to-incident conversion rate

---

## Quick Reference: curl Examples

### Create Incident
```bash
curl -X POST "https://instance.service-now.com/api/now/table/incident" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'user:pass' | base64)" \
  -d '{
    "short_description": "Test alert",
    "priority": "3",
    "assignment_group": "Platform Engineering"
  }'
```

### Update Incident
```bash
curl -X PUT "https://instance.service-now.com/api/now/table/incident/INC0012345" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'user:pass' | base64)" \
  -d '{
    "state": "2",
    "work_notes": "Investigating..."
  }'
```

### Query CI
```bash
curl -G "https://instance.service-now.com/api/now/table/cmdb_ci_appl" \
  -H "Authorization: Basic $(echo -n 'user:pass' | base64)" \
  --data-urlencode "sysparm_query=name=payment-service" \
  --data-urlencode "sysparm_fields=sys_id,name"
```

---

## Related Resources

- [ServiceNow REST API Documentation](https://docs.servicenow.com/bundle/tokyo-application-development/page/integrate/inbound-rest/concept/c_RESTAPI.html)
- [Event Management Best Practices](https://docs.servicenow.com/bundle/tokyo-it-operations-management/page/product/event-management/concept/c_EventManagement.html)
- [CMDB API Guide](https://docs.servicenow.com/bundle/tokyo-servicenow-platform/page/product/configuration-management/concept/c_ITILConfigurationManagement.html)
