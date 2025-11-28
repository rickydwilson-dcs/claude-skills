# {HTTP_METHOD} {endpoint_path}

## Description

{endpoint_description}

## Authentication

**Required:** {yes/no}

**Type:** {auth_type}

```http
Authorization: {auth_scheme} {token_format}
```

## Request

### Endpoint

```
{HTTP_METHOD} {base_url}{endpoint_path}
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| {path_param_1} | {type} | {yes/no} | {description} |
| {path_param_2} | {type} | {yes/no} | {description} |

### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| {query_param_1} | {type} | {yes/no} | {default} | {description} |
| {query_param_2} | {type} | {yes/no} | {default} | {description} |
| {query_param_3} | {type} | {yes/no} | {default} | {description} |

### Request Headers

| Header | Type | Required | Description |
|--------|------|----------|-------------|
| Content-Type | string | Yes | application/json |
| Authorization | string | {yes/no} | {auth_description} |
| {custom_header_1} | {type} | {yes/no} | {description} |

### Request Body

```json
{
  "{field_1}": "{type} - {description}",
  "{field_2}": "{type} - {description}",
  "{field_3}": {
    "{nested_field_1}": "{type} - {description}",
    "{nested_field_2}": "{type} - {description}"
  },
  "{field_4}": [
    "{array_item_type} - {description}"
  ]
}
```

**Schema:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| {field_1} | {type} | {yes/no} | {constraints} | {description} |
| {field_2} | {type} | {yes/no} | {constraints} | {description} |
| {field_3} | {type} | {yes/no} | {constraints} | {description} |
| {field_4} | {type} | {yes/no} | {constraints} | {description} |

## Request Examples

### cURL

```bash
curl -X {HTTP_METHOD} \
  '{base_url}{endpoint_path}?{query_params}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: {auth_scheme} {token}' \
  -d '{
    "{field_1}": "{example_value_1}",
    "{field_2}": "{example_value_2}",
    "{field_3}": {
      "{nested_field_1}": "{example_value_3}",
      "{nested_field_2}": "{example_value_4}"
    }
  }'
```

### JavaScript (fetch)

```javascript
const response = await fetch('{base_url}{endpoint_path}?{query_params}', {
  method: '{HTTP_METHOD}',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': '{auth_scheme} {token}'
  },
  body: JSON.stringify({
    {field_1}: '{example_value_1}',
    {field_2}: '{example_value_2}',
    {field_3}: {
      {nested_field_1}: '{example_value_3}',
      {nested_field_2}: '{example_value_4}'
    }
  })
});

const data = await response.json();
```

### Python (requests)

```python
import requests

url = '{base_url}{endpoint_path}'
headers = {
    'Content-Type': 'application/json',
    'Authorization': '{auth_scheme} {token}'
}
params = {
    '{query_param_1}': '{value_1}',
    '{query_param_2}': '{value_2}'
}
data = {
    '{field_1}': '{example_value_1}',
    '{field_2}': '{example_value_2}',
    '{field_3}': {
        '{nested_field_1}': '{example_value_3}',
        '{nested_field_2}': '{example_value_4}'
    }
}

response = requests.{method_lowercase}(url, headers=headers, params=params, json=data)
result = response.json()
```

## Response

### Success Response

**Code:** `{success_code}`

**Content:**

```json
{
  "{response_field_1}": "{type} - {description}",
  "{response_field_2}": "{type} - {description}",
  "{response_field_3}": {
    "{nested_response_field_1}": "{type} - {description}",
    "{nested_response_field_2}": "{type} - {description}"
  },
  "{response_field_4}": [
    {
      "{array_item_field_1}": "{type} - {description}",
      "{array_item_field_2}": "{type} - {description}"
    }
  ]
}
```

**Schema:**

| Field | Type | Description |
|-------|------|-------------|
| {response_field_1} | {type} | {description} |
| {response_field_2} | {type} | {description} |
| {response_field_3} | {type} | {description} |
| {response_field_4} | {type} | {description} |

### Response Headers

| Header | Description |
|--------|-------------|
| Content-Type | application/json |
| X-RateLimit-Limit | {description} |
| X-RateLimit-Remaining | {description} |
| X-RateLimit-Reset | {description} |

### Success Example

```json
{
  "{response_field_1}": "{example_value_1}",
  "{response_field_2}": "{example_value_2}",
  "{response_field_3}": {
    "{nested_response_field_1}": "{example_value_3}",
    "{nested_response_field_2}": "{example_value_4}"
  },
  "{response_field_4}": [
    {
      "{array_item_field_1}": "{example_value_5}",
      "{array_item_field_2}": "{example_value_6}"
    }
  ]
}
```

## Error Responses

### Error Response Format

```json
{
  "error": {
    "code": "{error_code}",
    "message": "{error_message}",
    "details": [
      {
        "field": "{field_name}",
        "issue": "{issue_description}"
      }
    ]
  }
}
```

### Common Error Codes

#### 400 Bad Request

**Description:** {error_description}

**Example:**

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "{error_message}",
    "details": [
      {
        "field": "{field_name}",
        "issue": "{issue_description}"
      }
    ]
  }
}
```

#### 401 Unauthorized

**Description:** {error_description}

**Example:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or missing authentication token"
  }
}
```

#### 403 Forbidden

**Description:** {error_description}

**Example:**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions to access this resource"
  }
}
```

#### 404 Not Found

**Description:** {error_description}

**Example:**

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "{resource_type} not found"
  }
}
```

#### 429 Too Many Requests

**Description:** {error_description}

**Example:**

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please retry after {seconds} seconds"
  }
}
```

#### 500 Internal Server Error

**Description:** {error_description}

**Example:**

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred. Please try again later"
  }
}
```

## Rate Limiting

**Limit:** {rate_limit_value} requests per {time_period}

**Headers:**
- `X-RateLimit-Limit`: Maximum number of requests allowed
- `X-RateLimit-Remaining`: Number of requests remaining
- `X-RateLimit-Reset`: Timestamp when the rate limit resets

## Pagination

**Supported:** {yes/no}

**Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: {default_limit}, max: {max_limit})

**Response includes:**
- `total`: Total number of items
- `page`: Current page number
- `limit`: Items per page
- `pages`: Total number of pages

## Filtering and Sorting

### Filtering

**Supported Fields:**
- {filterable_field_1}: {filter_operators}
- {filterable_field_2}: {filter_operators}
- {filterable_field_3}: {filter_operators}

**Example:**
```
{endpoint_path}?{field}={value}&{field}[operator]={value}
```

### Sorting

**Supported Fields:**
- {sortable_field_1}
- {sortable_field_2}
- {sortable_field_3}

**Example:**
```
{endpoint_path}?sort={field}&order={asc|desc}
```

## Webhooks

**Supported:** {yes/no}

**Events triggered:**
- {event_1}: {event_description_1}
- {event_2}: {event_description_2}

## Versioning

**Current Version:** {api_version}

**Version Header:**
```
Accept: application/vnd.{api_name}.{version}+json
```

## Related Endpoints

- [{related_endpoint_1_description}]({related_endpoint_1_path})
- [{related_endpoint_2_description}]({related_endpoint_2_path})
- [{related_endpoint_3_description}]({related_endpoint_3_path})

## Notes

{additional_notes}

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| {version_1} | {date_1} | {changes_1} |
| {version_2} | {date_2} | {changes_2} |
