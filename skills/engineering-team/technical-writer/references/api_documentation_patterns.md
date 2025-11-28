# API Documentation Patterns

## Documentation Types

### 1. Reference Documentation

**Purpose:** Complete, systematic coverage of all API endpoints, parameters, and responses.

**Characteristics:**
- Comprehensive and exhaustive
- Structured and predictable layout
- Searchable and scannable
- Often auto-generated from code

**When to use:**
- Documenting all endpoints
- Providing complete parameter lists
- Listing all response codes
- Serving as source of truth

**Example structure:**
```
API Reference
├── Authentication
├── Endpoints
│   ├── Users
│   │   ├── GET /users
│   │   ├── POST /users
│   │   ├── GET /users/{id}
│   │   └── DELETE /users/{id}
│   └── Products
├── Error Codes
└── Rate Limits
```

### 2. Conceptual Documentation

**Purpose:** Explain how the API works, key concepts, and architectural decisions.

**Characteristics:**
- Educational and explanatory
- Context and background
- "Why" not just "what"
- Narrative flow

**When to use:**
- Explaining authentication flows
- Describing rate limiting strategies
- Documenting pagination approaches
- Clarifying design decisions

**Topics to cover:**
- Authentication and authorization
- Resource relationships
- Data models and schemas
- Versioning strategy
- Rate limiting and quotas
- Webhooks and events
- Error handling philosophy

### 3. Tutorial Documentation

**Purpose:** Step-by-step guides to accomplish specific tasks.

**Characteristics:**
- Task-oriented
- Sequential steps
- Working code examples
- Expected outcomes at each step

**When to use:**
- Getting started guides
- Common use case walkthroughs
- Integration guides
- Migration guides

**Tutorial structure:**
1. **Goal statement:** "In this tutorial, you'll build a user authentication system"
2. **Prerequisites:** Required tools, accounts, knowledge
3. **Time estimate:** "Estimated time: 15 minutes"
4. **Step-by-step instructions:** Numbered, actionable steps
5. **Verification:** How to know it worked
6. **Next steps:** Related tutorials or topics

### 4. Quick Start Guide

**Purpose:** Get developers to first successful API call as fast as possible.

**Characteristics:**
- Minimal, essential steps only
- Copy-paste ready code
- Immediate gratification
- 5-10 minutes to complete

**Quick start template:**
```markdown
# Quick Start

Get your first API response in 5 minutes.

## 1. Get your API key
[Sign up](https://dashboard.example.com) and copy your API key from the dashboard.

## 2. Make your first request

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.example.com/v1/hello
```

## 3. You should see

```json
{
  "message": "Hello, World!",
  "status": "success"
}
```

## Next steps
- [Explore the full API reference](#)
- [Learn about authentication](#)
- [Try the tutorials](#)
```

## Endpoint Documentation Format

### 1. Method + Resource + Outcome Pattern

**Format:** `[METHOD] [Resource] - [What it does]`

**Examples:**
- `GET /users` - List all users
- `POST /users` - Create a new user
- `GET /users/{id}` - Retrieve a specific user
- `PUT /users/{id}` - Update a user
- `DELETE /users/{id}` - Delete a user

### 2. Complete Endpoint Documentation Template

```markdown
## Create User

Creates a new user account.

### HTTP Request

`POST https://api.example.com/v1/users`

### Authentication

Requires a valid API key with `users:write` permission.

### Request Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email address. Must be unique. |
| name | string | Yes | User's full name. 2-100 characters. |
| role | string | No | User role. One of: `admin`, `user`, `guest`. Default: `user` |
| metadata | object | No | Custom key-value pairs. Max 10 keys. |

### Example Request

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "name": "Jane Doe",
    "role": "user",
    "metadata": {
      "department": "Engineering"
    }
  }'
```

### Success Response

**Code:** `201 Created`

```json
{
  "id": "usr_abc123",
  "email": "jane@example.com",
  "name": "Jane Doe",
  "role": "user",
  "created_at": "2025-11-28T10:30:00Z",
  "metadata": {
    "department": "Engineering"
  }
}
```

### Error Responses

**Code:** `400 Bad Request`

```json
{
  "error": {
    "code": "invalid_email",
    "message": "Email address is not valid",
    "field": "email"
  }
}
```

**Code:** `409 Conflict`

```json
{
  "error": {
    "code": "email_exists",
    "message": "A user with this email already exists"
  }
}
```

**Code:** `401 Unauthorized`

```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid or missing API key"
  }
}
```

### Rate Limiting

This endpoint is rate-limited to 100 requests per hour per API key.

### Notes

- Email addresses are case-insensitive and stored in lowercase
- User IDs are prefixed with `usr_` for easy identification
- Metadata keys must be strings; values can be strings, numbers, or booleans
```

## Parameter Documentation

### 1. Path Parameters

Document parameters that appear in the URL path.

**Format:**
```markdown
### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| id | string | Unique identifier for the user. Format: `usr_[a-z0-9]+` |
```

**Best practices:**
- Specify format or pattern
- Note if case-sensitive
- Provide example value

### 2. Query Parameters

Document parameters passed in the URL query string.

**Format:**
```markdown
### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| limit | integer | No | 20 | Number of results to return. Range: 1-100 |
| offset | integer | No | 0 | Number of results to skip for pagination |
| sort | string | No | created_at | Field to sort by. Options: `created_at`, `name`, `email` |
| order | string | No | desc | Sort order. Options: `asc`, `desc` |
| filter | string | No | - | Filter results by field. Format: `field:value` |
```

**Best practices:**
- Show default values
- Specify allowed values or ranges
- Indicate which parameters can be combined

### 3. Request Body Parameters

Document parameters sent in the request body.

**For JSON bodies:**
```markdown
### Request Body

```json
{
  "email": "string (required)",
  "name": "string (required)",
  "role": "string (optional, default: 'user')",
  "metadata": {
    "key": "value (optional)"
  }
}
```

**Detailed table:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| email | string | Yes | Valid email format | User's email address |
| name | string | Yes | 2-100 chars | User's full name |
| role | string | No | Enum: admin, user, guest | User's role |
| metadata | object | No | Max 10 keys | Custom key-value pairs |
```

**Best practices:**
- Show nested object structure
- Specify validation rules
- Include examples of valid values
- Note any interdependencies

### 4. Response Fields

Document fields in the response body.

```markdown
### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique user identifier. Format: `usr_[a-z0-9]+` |
| email | string | User's email address |
| name | string | User's full name |
| role | string | User's role: `admin`, `user`, or `guest` |
| created_at | string | ISO 8601 timestamp of user creation |
| updated_at | string | ISO 8601 timestamp of last update |
| metadata | object | Custom key-value pairs |
```

## Request and Response Examples

### 1. Multiple Example Scenarios

Provide examples for different use cases.

**Pattern:**
```markdown
### Example 1: Create basic user

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "name": "Jane Doe"
  }'
```

### Example 2: Create admin user with metadata

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "name": "Admin User",
    "role": "admin",
    "metadata": {
      "department": "IT",
      "location": "HQ"
    }
  }'
```
```

### 2. Realistic Data

Use realistic, representative data in examples.

**Bad example:**
```json
{
  "name": "test",
  "email": "test@test.com",
  "id": "123"
}
```

**Good example:**
```json
{
  "id": "usr_7f8a9b2c3d4e5f6",
  "name": "Sarah Johnson",
  "email": "sarah.johnson@example.com",
  "created_at": "2025-11-28T14:30:00Z"
}
```

### 3. Success Examples

Show complete, successful responses.

```markdown
### Success Response (200 OK)

```json
{
  "data": [
    {
      "id": "usr_abc123",
      "name": "Alice Smith",
      "email": "alice@example.com",
      "role": "admin"
    },
    {
      "id": "usr_def456",
      "name": "Bob Jones",
      "email": "bob@example.com",
      "role": "user"
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```
```

### 4. Error Examples

Document all possible error responses with realistic scenarios.

```markdown
### Error Responses

**Validation Error (400 Bad Request)**

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "error": "Email address is required"
      },
      {
        "field": "name",
        "error": "Name must be at least 2 characters"
      }
    ]
  }
}
```

**Not Found (404 Not Found)**

```json
{
  "error": {
    "code": "user_not_found",
    "message": "User with ID 'usr_invalid' does not exist"
  }
}
```

**Rate Limited (429 Too Many Requests)**

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Try again in 3600 seconds",
    "retry_after": 3600
  }
}
```
```

### 5. Language-Specific Examples

Provide examples in multiple programming languages.

```markdown
### Code Examples

#### JavaScript (Node.js)

```javascript
const fetch = require('node-fetch');

async function createUser() {
  const response = await fetch('https://api.example.com/v1/users', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: 'jane@example.com',
      name: 'Jane Doe'
    })
  });

  const data = await response.json();
  return data;
}
```

#### Python

```python
import requests

def create_user():
    response = requests.post(
        'https://api.example.com/v1/users',
        headers={
            'Authorization': 'Bearer YOUR_API_KEY',
            'Content-Type': 'application/json'
        },
        json={
            'email': 'jane@example.com',
            'name': 'Jane Doe'
        }
    )
    return response.json()
```

#### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "net/http"
)

func createUser() (map[string]interface{}, error) {
    body := map[string]string{
        "email": "jane@example.com",
        "name": "Jane Doe",
    }

    jsonBody, _ := json.Marshal(body)

    req, _ := http.NewRequest("POST",
        "https://api.example.com/v1/users",
        bytes.NewBuffer(jsonBody))

    req.Header.Set("Authorization", "Bearer YOUR_API_KEY")
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    var result map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&result)
    return result, nil
}
```
```

## Authentication Documentation

### 1. Authentication Overview

```markdown
# Authentication

The API uses API key authentication. All requests must include your API key in the `Authorization` header.

## Getting Your API Key

1. Sign up for an account at [dashboard.example.com](https://dashboard.example.com)
2. Navigate to Settings → API Keys
3. Click "Generate New Key"
4. Copy the key and store it securely

**Important:** Your API key provides access to your account. Never share it publicly or commit it to version control.

## Making Authenticated Requests

Include your API key in the `Authorization` header with the `Bearer` scheme:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.example.com/v1/resource
```

## Authentication Errors

If authentication fails, you'll receive a `401 Unauthorized` response:

```json
{
  "error": {
    "code": "unauthorized",
    "message": "Invalid or missing API key"
  }
}
```
```

### 2. OAuth 2.0 Documentation

```markdown
# OAuth 2.0 Authentication

The API supports OAuth 2.0 for user authorization.

## Authorization Flow

1. **Redirect user to authorization URL:**
   ```
   https://auth.example.com/oauth/authorize?
     client_id=YOUR_CLIENT_ID&
     redirect_uri=YOUR_REDIRECT_URI&
     response_type=code&
     scope=read write
   ```

2. **User grants permission**

3. **Receive authorization code at redirect URI:**
   ```
   https://yourapp.com/callback?code=AUTH_CODE
   ```

4. **Exchange code for access token:**
   ```bash
   curl -X POST https://auth.example.com/oauth/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=authorization_code" \
     -d "code=AUTH_CODE" \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET" \
     -d "redirect_uri=YOUR_REDIRECT_URI"
   ```

5. **Use access token in API requests:**
   ```bash
   curl -H "Authorization: Bearer ACCESS_TOKEN" \
     https://api.example.com/v1/resource
   ```

## Scopes

| Scope | Description |
|-------|-------------|
| read | Read access to user data |
| write | Create and update resources |
| delete | Delete resources |
| admin | Full administrative access |

## Token Refresh

Access tokens expire after 1 hour. Use the refresh token to get a new access token:

```bash
curl -X POST https://auth.example.com/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=REFRESH_TOKEN" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```
```

### 3. JWT Authentication

```markdown
# JWT Authentication

The API uses JSON Web Tokens (JWT) for stateless authentication.

## Obtaining a JWT

Send your credentials to the authentication endpoint:

```bash
curl -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your-password"
  }'
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-11-28T14:30:00Z"
}
```

## Using the JWT

Include the token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  https://api.example.com/v1/resource
```

## Token Expiration

JWTs expire after 1 hour. When a token expires, you'll receive a `401 Unauthorized` response. Obtain a new token by logging in again.
```

## Error Documentation

### 1. HTTP Status Codes

```markdown
# Error Codes

The API uses standard HTTP status codes to indicate success or failure.

## Success Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request succeeded, no content to return |

## Client Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 400 | Bad Request | Invalid request format or parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Request conflicts with current state |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |

## Server Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | Invalid response from upstream |
| 503 | Service Unavailable | Temporary server overload |
| 504 | Gateway Timeout | Request timeout |
```

### 2. Error Response Format

```markdown
# Error Response Format

All errors follow a consistent JSON structure:

```json
{
  "error": {
    "code": "error_code",
    "message": "Human-readable error message",
    "details": [] // Optional: Additional context
  }
}
```

## Error Fields

| Field | Type | Description |
|-------|------|-------------|
| error.code | string | Machine-readable error code |
| error.message | string | Human-readable description |
| error.details | array | Optional: Additional error information |
| error.field | string | Optional: Field that caused the error |
```

### 3. Common Error Codes

```markdown
# Common Error Codes

## Authentication Errors

| Code | HTTP Status | Description | Solution |
|------|-------------|-------------|----------|
| invalid_api_key | 401 | API key is invalid | Check your API key is correct |
| missing_api_key | 401 | No API key provided | Include Authorization header |
| expired_token | 401 | JWT has expired | Obtain a new token |
| insufficient_permissions | 403 | Missing required permissions | Request appropriate access level |

## Validation Errors

| Code | HTTP Status | Description | Solution |
|------|-------------|-------------|----------|
| missing_field | 400 | Required field is missing | Include all required fields |
| invalid_format | 400 | Field format is incorrect | Check field format requirements |
| value_too_long | 400 | Value exceeds maximum length | Reduce field length |
| invalid_email | 400 | Email format is invalid | Use valid email address |

## Resource Errors

| Code | HTTP Status | Description | Solution |
|------|-------------|-------------|----------|
| not_found | 404 | Resource does not exist | Verify resource ID |
| already_exists | 409 | Resource already exists | Use unique identifier |
| cannot_delete | 409 | Resource cannot be deleted | Check dependencies |
```

## Versioning Documentation

### 1. URL Versioning

```markdown
# API Versioning

The API uses URL-based versioning. The version is included in the request path.

## Current Version

The current API version is **v1**. All requests should use:

```
https://api.example.com/v1/resource
```

## Versioning Policy

- **Major versions** (v1, v2) introduce breaking changes
- **Minor updates** within a version are backward-compatible
- Deprecated endpoints remain available for 12 months
- Version sunset dates are announced 6 months in advance

## Version History

| Version | Release Date | Status | End of Life |
|---------|--------------|--------|-------------|
| v1 | 2024-01-01 | Current | - |
| v0 (beta) | 2023-06-01 | Deprecated | 2025-01-01 |
```

### 2. Header Versioning

```markdown
# API Versioning

The API uses header-based versioning. Specify the version in the `API-Version` header.

## Current Version

```bash
curl -H "API-Version: 2025-11-28" \
  https://api.example.com/resource
```

## Version Format

Versions use ISO date format: `YYYY-MM-DD`

## Default Behavior

If no version header is provided, the API uses the latest stable version. However, we recommend always specifying a version for consistency.
```

## OpenAPI/Swagger Integration

### 1. OpenAPI Annotations

```yaml
openapi: 3.0.0
info:
  title: Example API
  description: API for managing users and resources
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
    url: https://example.com/support

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging.example.com/v1
    description: Staging server

paths:
  /users:
    get:
      summary: List users
      description: Returns a paginated list of users
      tags:
        - Users
      parameters:
        - name: limit
          in: query
          description: Number of results to return
          required: false
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/UnauthorizedError'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: string
          example: usr_abc123
        email:
          type: string
          format: email
          example: jane@example.com
        name:
          type: string
          example: Jane Doe
          minLength: 2
          maxLength: 100

  responses:
    UnauthorizedError:
      description: Authentication failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

### 2. Generation Best Practices

**From code annotations:**
- Document inline with code for accuracy
- Use detailed descriptions
- Include examples for complex types
- Keep annotations up-to-date

**From specification:**
- Write OpenAPI spec first for API-first development
- Generate server stubs and client SDKs
- Validate requests/responses against spec
- Use spec as single source of truth

---

**Last Updated:** November 28, 2025
**Applies To:** REST APIs, GraphQL APIs, SDK documentation
**Related:** technical_writing_standards.md, developer_documentation_guide.md
