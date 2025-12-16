# ServiceNow Change Management Integration

Comprehensive guide for integrating deployment pipelines with ServiceNow Change Management for audit compliance, ITIL workflows, and deployment tracking.

## Table of Contents

1. [Change Management Overview](#change-management-overview)
2. [Change Request Types](#change-request-types)
3. [Deployment-to-Change Workflow](#deployment-to-change-workflow)
4. [Change Request API](#change-request-api)
5. [CAB Approval Workflows](#cab-approval-workflows)
6. [CI/CD Pipeline Integration](#cicd-pipeline-integration)
7. [Best Practices](#best-practices)

---

## Change Management Overview

### Why Integrate Deployments with Change Management?

1. **Audit Compliance**: Track all production changes for regulatory requirements (SOX, PCI-DSS, HIPAA)
2. **Risk Management**: Assess and document deployment risks before execution
3. **Change Visibility**: Provide stakeholders visibility into upcoming changes
4. **Incident Correlation**: Link incidents to recent changes for faster RCA
5. **CAB Oversight**: Enable Change Advisory Board review when required

### Change Request Lifecycle

```
New → Assess → Authorize → Scheduled → Implement → Review → Closed
 │       │         │           │           │         │
 └───────┴─────────┴───────────┴───────────┴─────────┴── Canceled (at any stage)
```

---

## Change Request Types

### Standard Changes

Pre-approved, low-risk changes that follow a documented procedure.

**Characteristics:**
- No CAB approval required
- Uses pre-approved templates
- Low risk and well-understood
- Commonly recurring

**Examples:**
- Routine deployments to non-production
- Scheduled maintenance windows
- Pre-approved security patches
- Configuration file updates

**ServiceNow Template Usage:**
```json
{
  "type": "Standard",
  "std_change_producer_version": "{{template_sys_id}}",
  "risk": 4,
  "category": "Software"
}
```

### Normal Changes

Standard changes requiring CAB review and approval.

**Characteristics:**
- Requires CAB approval
- Risk assessment mandatory
- Implementation and backout plans required
- Scheduled change window

**Examples:**
- Production feature deployments
- Infrastructure changes
- Database schema migrations
- Network configuration updates

**Approval Workflow:**
```
Create → Assess → Technical Review → CAB Review → Approve → Schedule → Implement
```

### Emergency Changes

Urgent changes that bypass normal approval processes.

**Characteristics:**
- Expedited approval (single approver)
- Post-implementation review required
- Used for critical fixes only
- Higher scrutiny after implementation

**Examples:**
- Security vulnerability patches
- Critical production bug fixes
- Service restoration after outage
- Data breach remediation

**When to Use:**
- Active security incident
- Service availability below SLA
- Data integrity at risk
- Customer-impacting issue

---

## Deployment-to-Change Workflow

### Pre-Deployment (Change Creation)

```bash
# 1. Generate deployment configuration
python deployment_manager.py \
  --input config.yaml \
  --output json \
  --file deploy-config.json

# 2. Create change request from deployment
python servicenow_change_manager.py \
  --deployment-file deploy-config.json \
  --change-type normal \
  --output curl > create-change.sh

# 3. Submit change request
bash create-change.sh
# Response: {"result": {"sys_id": "abc123", "number": "CHG0012345"}}

# 4. Store change number for pipeline
echo "CHG0012345" > change-number.txt
```

### During Deployment (Status Updates)

```bash
# Update change status to "Implement"
curl -X PUT "https://instance.service-now.com/api/now/table/change_request/CHG0012345" \
  -H "Authorization: Basic $SNOW_AUTH" \
  -d '{"state": "-1", "work_notes": "Deployment started at $(date)"}'

# Add work notes during deployment
curl -X PUT "https://instance.service-now.com/api/now/table/change_request/CHG0012345" \
  -d '{"work_notes": "Step 1/5: Image pulled successfully"}'
```

### Post-Deployment (Closure)

```bash
# Successful deployment
curl -X PUT "https://instance.service-now.com/api/now/table/change_request/CHG0012345" \
  -d '{
    "state": "0",
    "close_code": "successful",
    "close_notes": "Deployment completed successfully. Version 2.3.1 now running."
  }'

# Failed deployment (with rollback)
curl -X PUT "https://instance.service-now.com/api/now/table/change_request/CHG0012345" \
  -d '{
    "state": "0",
    "close_code": "unsuccessful",
    "close_notes": "Deployment failed. Rollback executed. Previous version restored."
  }'
```

---

## Change Request API

### Create Change Request

**Endpoint:** `POST /api/now/table/change_request`

**Required Fields:**
```json
{
  "short_description": "Deployment: payment-service v2.3.1",
  "description": "Production deployment of payment-service",
  "type": "Normal",
  "category": "Software",
  "start_date": "2024-01-15 10:00:00",
  "end_date": "2024-01-15 12:00:00",
  "assignment_group": "Platform Engineering",
  "cmdb_ci": "payment-service-prod"
}
```

**Recommended Additional Fields:**
```json
{
  "risk": 3,
  "impact": 2,
  "backout_plan": "kubectl rollout undo deployment/payment-service",
  "test_plan": "1. Health check\n2. API tests\n3. Metrics validation",
  "justification": "New feature release per roadmap",
  "correlation_id": "deploy-payment-service-2.3.1-20240115"
}
```

### Update Change Request

**Endpoint:** `PUT /api/now/table/change_request/{number_or_sys_id}`

**State Values:**
| State | Value | Description |
|-------|-------|-------------|
| New | -5 | Initial state |
| Assess | -4 | Under assessment |
| Authorize | -3 | Awaiting authorization |
| Scheduled | -2 | Approved and scheduled |
| Implement | -1 | Implementation in progress |
| Review | 0 | Post-implementation review |
| Closed | 3 | Change completed |
| Canceled | 4 | Change canceled |

### Query Change Requests

**Endpoint:** `GET /api/now/table/change_request`

**Query Examples:**
```
# Open changes for a service
?sysparm_query=cmdb_ci.name=payment-service^state!=-3^state!=3

# Changes in implementation
?sysparm_query=state=-1

# Recent closed changes
?sysparm_query=state=3^sys_updated_on>javascript:gs.daysAgoStart(7)&sysparm_orderby=sys_updated_on
```

---

## CAB Approval Workflows

### Standard CAB Process

```
1. Change Owner creates change request
   ↓
2. Technical Reviewer assesses risk
   ↓
3. CAB meeting reviews change
   ↓
4. CAB votes (approve/reject/defer)
   ↓
5. Approved changes scheduled
   ↓
6. Implementation during change window
   ↓
7. Post-implementation review
```

### Emergency CAB (ECAB)

```
1. Change Owner creates emergency change
   ↓
2. Single manager approval (phone/email)
   ↓
3. Implementation immediately
   ↓
4. Post-implementation ECAB review
   ↓
5. Document lessons learned
```

### Automated Approval Rules

Configure ServiceNow to auto-approve standard changes:

```javascript
// ServiceNow Business Rule: Auto-approve standard changes
if (current.type == 'Standard' && current.std_change_producer_version != '') {
    current.state = -2;  // Scheduled
    current.approval = 'approved';
    current.work_notes = 'Auto-approved via standard change template';
}
```

---

## CI/CD Pipeline Integration

### GitHub Actions Example

```yaml
name: Deploy with Change Management

on:
  push:
    branches: [main]

jobs:
  create-change:
    runs-on: ubuntu-latest
    outputs:
      change_number: ${{ steps.create.outputs.change_number }}
    steps:
      - name: Create Change Request
        id: create
        run: |
          CHANGE=$(curl -X POST "${{ secrets.SNOW_INSTANCE }}/api/now/table/change_request" \
            -H "Authorization: Basic ${{ secrets.SNOW_AUTH }}" \
            -H "Content-Type: application/json" \
            -d '{
              "short_description": "Deploy ${{ github.repository }} ${{ github.sha }}",
              "type": "Standard",
              "category": "Software",
              "assignment_group": "Platform Engineering"
            }' | jq -r '.result.number')
          echo "change_number=$CHANGE" >> $GITHUB_OUTPUT

  deploy:
    needs: create-change
    runs-on: ubuntu-latest
    steps:
      - name: Update Change to Implement
        run: |
          curl -X PUT "${{ secrets.SNOW_INSTANCE }}/api/now/table/change_request/${{ needs.create-change.outputs.change_number }}" \
            -H "Authorization: Basic ${{ secrets.SNOW_AUTH }}" \
            -d '{"state": "-1"}'

      - name: Deploy Application
        run: |
          # Your deployment steps here
          kubectl apply -f k8s/

      - name: Close Change Request
        if: success()
        run: |
          curl -X PUT "${{ secrets.SNOW_INSTANCE }}/api/now/table/change_request/${{ needs.create-change.outputs.change_number }}" \
            -H "Authorization: Basic ${{ secrets.SNOW_AUTH }}" \
            -d '{"state": "0", "close_code": "successful"}'

      - name: Mark Change Failed
        if: failure()
        run: |
          curl -X PUT "${{ secrets.SNOW_INSTANCE }}/api/now/table/change_request/${{ needs.create-change.outputs.change_number }}" \
            -H "Authorization: Basic ${{ secrets.SNOW_AUTH }}" \
            -d '{"state": "0", "close_code": "unsuccessful", "close_notes": "Deployment failed"}'
```

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any

    environment {
        SNOW_INSTANCE = credentials('servicenow-instance')
        SNOW_AUTH = credentials('servicenow-auth')
    }

    stages {
        stage('Create Change') {
            steps {
                script {
                    def response = httpRequest(
                        url: "${SNOW_INSTANCE}/api/now/table/change_request",
                        httpMode: 'POST',
                        authentication: 'servicenow-auth',
                        contentType: 'APPLICATION_JSON',
                        requestBody: """
                        {
                            "short_description": "Deploy ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                            "type": "Normal"
                        }
                        """
                    )
                    def json = readJSON text: response.content
                    env.CHANGE_NUMBER = json.result.number
                }
            }
        }

        stage('Wait for Approval') {
            when { environment name: 'CHANGE_TYPE', value: 'Normal' }
            steps {
                script {
                    // Poll for approval status
                    timeout(time: 24, unit: 'HOURS') {
                        waitUntil {
                            def response = httpRequest(
                                url: "${SNOW_INSTANCE}/api/now/table/change_request/${env.CHANGE_NUMBER}",
                                authentication: 'servicenow-auth'
                            )
                            def json = readJSON text: response.content
                            return json.result.state == '-2'  // Scheduled = approved
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Update change to implement
                httpRequest(
                    url: "${SNOW_INSTANCE}/api/now/table/change_request/${env.CHANGE_NUMBER}",
                    httpMode: 'PUT',
                    authentication: 'servicenow-auth',
                    requestBody: '{"state": "-1"}'
                )

                // Your deployment steps
                sh 'kubectl apply -f k8s/'
            }
        }
    }

    post {
        success {
            httpRequest(
                url: "${SNOW_INSTANCE}/api/now/table/change_request/${env.CHANGE_NUMBER}",
                httpMode: 'PUT',
                authentication: 'servicenow-auth',
                requestBody: '{"state": "0", "close_code": "successful"}'
            )
        }
        failure {
            httpRequest(
                url: "${SNOW_INSTANCE}/api/now/table/change_request/${env.CHANGE_NUMBER}",
                httpMode: 'PUT',
                authentication: 'servicenow-auth',
                requestBody: '{"state": "0", "close_code": "unsuccessful"}'
            )
        }
    }
}
```

---

## Best Practices

### 1. Use Standard Change Templates

Pre-create templates for common deployment scenarios:
- Standard application deployment
- Configuration file updates
- Database migration
- Infrastructure scaling

### 2. Include Correlation IDs

Always include correlation IDs to link changes to:
- CI/CD pipeline runs
- Git commits/tags
- Jira tickets
- Deployment logs

### 3. Automate Risk Assessment

Calculate risk programmatically based on:
- Environment (prod vs non-prod)
- Service criticality
- Change scope
- Historical failure rate

### 4. Link to CMDB

Always link changes to Configuration Items:
- Primary CI (service being deployed)
- Related CIs (dependent services)
- Business service (for impact analysis)

### 5. Document Rollback Plans

Every change must include:
- Step-by-step rollback procedure
- Previous version information
- Estimated rollback time
- Rollback decision criteria

### 6. Schedule Change Windows

Align deployments with:
- Maintenance windows
- Low-traffic periods
- Team availability
- Dependent team schedules

### 7. Post-Implementation Review

For all changes, document:
- Actual implementation time
- Issues encountered
- Lessons learned
- Process improvements

---

## Quick Reference

### curl: Create Normal Change

```bash
curl -X POST "https://instance.service-now.com/api/now/table/change_request" \
  -H "Authorization: Basic $(echo -n 'user:pass' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "short_description": "Deploy payment-service v2.3.1",
    "type": "Normal",
    "category": "Software",
    "start_date": "2024-01-15 10:00:00",
    "end_date": "2024-01-15 12:00:00",
    "assignment_group": "Platform Engineering",
    "cmdb_ci": "payment-service-prod",
    "backout_plan": "kubectl rollout undo deployment/payment-service"
  }'
```

### curl: Emergency Change

```bash
curl -X POST "https://instance.service-now.com/api/now/table/change_request" \
  -H "Authorization: Basic $(echo -n 'user:pass' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "short_description": "EMERGENCY: Security patch for CVE-2024-1234",
    "type": "Emergency",
    "reason": "Critical security vulnerability requires immediate patching",
    "risk": 2,
    "assignment_group": "Security Operations"
  }'
```

---

## Related Resources

- [servicenow_change_manager.py](../scripts/servicenow_change_manager.py) - Python tool for generating change request payloads
- [servicenow-change-template.json](../assets/servicenow-change-template.json) - JSON template for change requests
- [ServiceNow Change Management Docs](https://docs.servicenow.com/bundle/tokyo-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html)
