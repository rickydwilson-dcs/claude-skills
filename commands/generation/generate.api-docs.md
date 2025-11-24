---
name: generate.api-docs
title: Generate API Documentation from Code
description: Automatic API documentation generation with OpenAPI/Swagger specs, endpoint discovery, and interactive examples
category: generate
subcategory: documentation
pattern: multi-phase
difficulty: intermediate
time-saved: 20 minutes per update
frequency: After API changes
use-cases:
  - Generate comprehensive API documentation from source code automatically
  - Create OpenAPI/Swagger specifications from REST endpoint definitions
  - Produce interactive API documentation with executable examples
  - Generate client SDK documentation and integration guides
  - Maintain up-to-date API docs synchronized with code changes
dependencies:
  tools:
    - Read
    - Bash
    - Grep
    - Glob
    - Write
  scripts:
    - api_endpoint_extractor.py
    - openapi_generator.py
    - documentation_formatter.py
  python-packages: []
related-agents:
  - cs-backend-engineer
  - cs-senior-architect
  - cs-devops-engineer
related-skills:
  - senior-backend
  - senior-architect
  - senior-devops
related-commands:
  - generation.swagger-spec
  - generation.endpoint-catalog
  - docs.update-readme
compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows
examples:
  - title: "Generate Full API Documentation"
    input: "/generate.api-docs /path/to/api/src"
    output: "Complete API documentation with OpenAPI spec, endpoint list, and examples"
  - title: "Generate for Specific Framework"
    input: "/generate.api-docs /path/to/api/src --framework fastapi"
    output: "Framework-optimized documentation with FastAPI-specific patterns"
  - title: "Include Authentication Details"
    input: "/generate.api-docs /path/to/api/src --auth-schemes oauth2,api-key"
    output: "Documentation with security schemes and authentication flow examples"
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0
version: v1.0.0
author: Claude Skills Team
created: 2025-11-24
updated: 2025-11-24
tags:
  - api-documentation
  - openapi
  - swagger
  - endpoint-discovery
  - code-analysis
  - documentation-generation
  - rest-api
  - interactive-docs
featured: false
verified: true
license: MIT
---

# Generate API Documentation from Code

Automatically generates comprehensive API documentation from your codebase with OpenAPI/Swagger specifications, endpoint discovery, interactive examples, and formatted markdown docs. This multi-phase command analyzes your API source code and produces production-ready documentation that stays synchronized with code changes.

**When to use:** After implementing new API endpoints, before API releases, or to update documentation when code changes.

**What it saves:** Eliminates manual API documentation writing - saves 20 minutes per update while ensuring accuracy and completeness.

---

## Pattern Type: Multi-Phase

**Complexity:** Intermediate
**Execution Time:** 3-8 minutes (depends on API size)
**Destructive:** No (generates new files, doesn't modify existing code)

---

## Usage

```bash
/generate.api-docs [api-source-path] [options]
```

### Arguments

- `api-source-path` - Absolute or relative path to API source code directory (required)
- `--framework` - API framework: `fastapi`, `flask`, `django`, `express`, `go-gin`, `spring-boot` (optional, auto-detected)
- `--auth-schemes` - Comma-separated authentication schemes: `oauth2`, `api-key`, `jwt`, `basic` (optional)
- `--output` - Output directory for generated documentation (optional, default: `./api-docs`)
- `--format` - Output format: `markdown`, `html`, `openapi`, `all` (optional, default: all)
- `--include-examples` - Include executable code examples (optional, default: true)
- `--base-url` - Base URL for API endpoints in documentation (optional)
- `--version` - API version string (optional, auto-detected from package.json/setup.py)

### Examples

```bash
# Generate complete documentation from FastAPI project
/generate.api-docs ./src --framework fastapi

# Generate with OAuth2 authentication scheme
/generate.api-docs ./src --auth-schemes oauth2,api-key

# Output to specific directory
/generate.api-docs ./src --output ./docs/api-v2

# Generate only OpenAPI specification
/generate.api-docs ./src --format openapi

# With custom base URL and version
/generate.api-docs ./src --base-url https://api.example.com --version 2.1.0

# Generate all formats including interactive HTML
/generate.api-docs ./src --format all --include-examples true
```

---

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Scan codebase and identify all API endpoints, frameworks, and patterns

**Steps:**

1. Scan source directory for API-related files (.py, .js, .go, .java files)
2. Detect API framework type (FastAPI, Flask, Django, Express, etc.)
3. Locate endpoint definitions and route configurations
4. Identify HTTP methods (GET, POST, PUT, DELETE, PATCH)
5. Extract path parameters, query parameters, request bodies
6. Scan for authentication/authorization patterns
7. Find request/response models and schemas
8. Catalog error responses and status codes
9. Locate API documentation comments/docstrings
10. Identify rate limiting and deprecation notices

**Tools Used:** Glob (file scanning), Grep (pattern matching), Read (code analysis)

**Discovery Checklist:**
- [ ] API framework detected
- [ ] All endpoints identified
- [ ] Request/response models found
- [ ] Authentication methods located
- [ ] Error handling identified
- [ ] Documentation comments parsed
- [ ] Version information found

### Phase 2: Analysis

**Goal:** Analyze endpoints and generate structured API specification

**Steps:**

1. Parse endpoint definitions and extract metadata
2. Analyze function signatures and type hints
3. Extract parameter information (name, type, required, default, description)
4. Parse request body schemas and validation rules
5. Extract response models and status codes
6. Identify authentication requirements per endpoint
7. Categorize endpoints by resource/tag
8. Build OpenAPI specification components
9. Generate code examples for each endpoint
10. Create authentication flow diagrams
11. Calculate documentation completeness metrics
12. Cross-reference related endpoints

**Analysis Criteria:**

- **Framework Detection** - Identify API framework and version
- **Endpoint Completeness** - Ensure all parameters documented
- **Schema Validation** - Verify request/response schemas are valid
- **Authentication Coverage** - All protected endpoints documented
- **Error Handling** - All status codes and errors documented
- **Example Quality** - Examples are executable and realistic
- **Documentation Quality** - Clear descriptions and explanations

**Output Includes:**

- Structured endpoint catalog with all metadata
- OpenAPI 3.0 specification
- Authentication schemes definition
- Request/response schemas
- Code examples per endpoint
- Error responses catalog

### Phase 3: Generation

**Goal:** Create formatted documentation in multiple output formats

**Steps:**

1. Generate OpenAPI specification (JSON/YAML)
2. Create markdown documentation with sections:
   - API overview and description
   - Authentication and authorization
   - Base URLs and versions
   - Endpoints organized by resource/tag
   - Request/response examples
   - Error codes and handling
   - Rate limiting information
   - Deprecation notices
   - Integration guides
3. Generate interactive HTML documentation (Swagger UI)
4. Create client SDK documentation
5. Generate changelog/API updates
6. Create quick start guide
7. Generate authentication flow diagrams
8. Build integration examples

**Generation Details:**

- **OpenAPI Spec** - Valid OpenAPI 3.0 specification
- **Markdown Docs** - Human-readable endpoint documentation
- **Interactive HTML** - Swagger UI for testing endpoints
- **Code Examples** - cURL, Python, JavaScript, Go examples
- **Integration Guide** - Step-by-step integration instructions

### Phase 4: Validation & Reporting

**Goal:** Validate generated documentation and provide quality report

**Steps:**

1. Validate OpenAPI specification syntax
2. Verify all endpoints documented
3. Check for missing descriptions
4. Validate request/response examples
5. Verify authentication configurations
6. Check for broken links and references
7. Generate completeness score (0-100)
8. Identify missing documentation
9. Create validation report
10. Suggest improvements

**Report Includes:**

- Validation status (pass/fail)
- Documentation completeness score
- Endpoint coverage summary
- Missing descriptions count
- Authentication configuration status
- Example quality assessment
- Recommendations for improvement
- File locations of generated docs

---

## What This Command Does

### Context Gathering

The command will:

1. Scan the specified directory recursively for API source files
2. Detect the API framework (FastAPI, Flask, Django, Express, etc.)
3. Parse route/endpoint definitions and decorators
4. Extract parameter information from function signatures
5. Read documentation comments and docstrings
6. Identify authentication mechanisms
7. Locate request/response schema definitions
8. Determine API version and metadata

### Task Execution

Then it will:

1. Generate comprehensive OpenAPI 3.0 specification
2. Create human-readable markdown documentation
3. Generate interactive HTML documentation (Swagger UI)
4. Produce executable code examples (cURL, Python, JS, Go)
5. Create authentication flow documentation
6. Generate integration guides and quick start
7. Validate all documentation for completeness
8. Generate quality and completeness report

### Expected Output

You will receive:

- OpenAPI specification file (api-spec.json or openapi.yaml)
- Comprehensive markdown documentation (API.md)
- Interactive Swagger UI HTML file
- Code examples for each endpoint (examples/ directory)
- Quick start guide
- Integration guide
- Validation report with completeness metrics
- Optional: Client SDK documentation

**Output Location:** `./api-docs/` (configurable with `--output`)
**Output Format:** Markdown, JSON (OpenAPI), HTML, Python/JavaScript/Go code examples

**Generated Files:**
```
api-docs/
├── openapi.yaml              # OpenAPI specification
├── API.md                     # Comprehensive markdown docs
├── QUICK_START.md            # Quick start guide
├── INTEGRATION.md            # Integration guide
├── AUTHENTICATION.md         # Auth flow documentation
├── index.html                # Interactive Swagger UI
├── examples/
│   ├── curl-examples.sh      # cURL command examples
│   ├── python-examples.py    # Python code examples
│   ├── javascript-examples.js # Node.js examples
│   └── go-examples.go        # Go code examples
└── VALIDATION_REPORT.md      # Quality and completeness report
```

---

## Error Handling

### Common Issues

**Issue:** "No API framework detected"
**Cause:** Unsupported framework or incorrect directory structure
**Solution:** Specify framework with `--framework` option, check directory contains API files
**Prevention:** Ensure API code is in provided directory, use standard framework patterns

---

**Issue:** "No endpoints found"
**Cause:** Framework detection incorrect or endpoints not using standard patterns
**Solution:** Verify framework is correct, check endpoint definitions follow conventions
**Prevention:** Use standard framework decorators (@app.route, @router.get, etc.)

---

**Issue:** "Missing type hints or annotations"
**Cause:** API code lacks type hints for parameters/responses
**Solution:** Documentation generated with available info, add type hints for better docs
**Prevention:** Use type hints in function definitions, document with docstrings

---

**Issue:** "Authentication schemes not detected"
**Cause:** Authorization checks not in standard location or using custom patterns
**Solution:** Specify schemes with `--auth-schemes` option, review generated docs
**Prevention:** Use framework's standard auth mechanisms (Flask-Login, FastAPI Security, etc.)

---

**Issue:** "OpenAPI validation fails"
**Cause:** Generated specification has schema errors
**Solution:** Review validation report, check endpoint definitions in source
**Prevention:** Use proper type hints, ensure request/response models are valid

---

### Validation Failures

If the command reports validation errors:

1. **Missing Endpoints**
   - Check: All endpoints present in source
   - Fix: Scan full directory, check naming conventions match
   - Verify: Endpoints using standard framework patterns

2. **Incomplete Descriptions**
   - Check: Docstrings present in source code
   - Fix: Add descriptions to endpoint functions
   - Verify: Documentation comments are clear

3. **Invalid Schemas**
   - Check: Request/response models are properly defined
   - Fix: Ensure type hints and validation rules are correct
   - Verify: Models match actual code implementation

4. **Auth Configuration**
   - Check: Authentication is properly configured
   - Fix: Specify auth schemes with `--auth-schemes` option
   - Verify: Security definitions in OpenAPI spec

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-backend-engineer](../../agents/engineering/cs-backend-engineer.md)** - Updates docs during API development
- **[cs-senior-architect](../../agents/engineering/cs-senior-architect.md)** - Reviews API design and architecture
- **[cs-devops-engineer](../../agents/engineering/cs-devops-engineer.md)** - Deploys docs alongside API releases

### Related Skills

This command leverages:

- **[senior-backend](../../skills/engineering-team/senior-backend/)** - Backend development and API design
- **[senior-architect](../../skills/engineering-team/senior-architect/)** - System architecture and design patterns
- **[senior-devops](../../skills/engineering-team/senior-devops/)** - Deployment and documentation pipelines

### Python Tools

This command may leverage Python tools from related skills for:

- API endpoint analysis and extraction
- OpenAPI specification generation
- Documentation formatting and validation

**Note:** Python tool integration is planned for future versions

---

## Success Criteria

This command is successful when:

- [ ] API framework correctly identified
- [ ] All endpoints discovered and documented
- [ ] OpenAPI specification is valid and complete
- [ ] Request/response examples are executable
- [ ] Authentication schemes properly documented
- [ ] Error responses documented for each endpoint
- [ ] Markdown documentation is clear and complete
- [ ] Interactive HTML documentation renders correctly
- [ ] Code examples work without modification
- [ ] Documentation completeness score >= 85%
- [ ] Validation report shows no critical issues
- [ ] Generated files ready for publication

### Quality Metrics

**Expected Outcomes:**

- **Endpoint Coverage:** 100% of endpoints documented
- **Documentation Completeness:** >= 85% score (complete descriptions, parameters, examples)
- **Example Accuracy:** All code examples are executable and tested
- **Specification Validity:** OpenAPI spec passes validator.swagger.io
- **Type Coverage:** >= 95% of parameters have type information
- **Error Coverage:** All HTTP status codes documented

---

## Tips for Best Results

1. **Prepare Source Code**
   - Use proper type hints in function signatures
   - Add docstrings with descriptions and examples
   - Follow framework conventions for routing
   - Use standard authentication patterns

2. **Framework Selection**
   - Specify framework explicitly if auto-detection fails
   - Use framework-specific decorators and patterns
   - Ensure code follows framework best practices
   - Keep endpoint definitions in standard locations

3. **Documentation Quality**
   - Write clear, concise endpoint descriptions
   - Include business context in docstrings
   - Document error conditions and edge cases
   - Provide realistic request/response examples
   - Keep descriptions updated with code changes

4. **Integration Guidance**
   - Include base URL and authentication info
   - Document rate limits and quotas
   - Provide integration step-by-step guide
   - Include common use cases and workflows
   - Add troubleshooting section

5. **Maintenance & Updates**
   - Re-run after significant API changes
   - Review and validate generated docs
   - Update docstrings when endpoints change
   - Version documentation with API versions
   - Track changes in changelog/INTEGRATION.md

6. **CI/CD Integration**
   - Run during build process to validate API docs
   - Generate docs on every API commit
   - Publish to API portal or documentation site
   - Compare docs against deployed API
   - Alert on breaking changes or deprecations

---

## Related Commands

- `/generation.swagger-spec` - Generate Swagger specification directly
- `/generation.endpoint-catalog` - List all API endpoints in catalog format
- `/docs.update-readme` - Update README with API documentation link
- `/analysis.code-review` - Review API code for best practices
- `/architecture.design-review` - Review API architecture design

---

## References

- [OpenAPI Specification 3.0](https://spec.openapis.org/oas/v3.0.3) - Official OpenAPI 3.0 specification
- [REST API Best Practices](https://restfulapi.net/) - Comprehensive REST API design guidelines
- [JSON Schema Specification](https://json-schema.org/) - Schema validation standards
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/) - Interactive documentation tool
- [API Documentation Guide](https://developer.mozilla.org/en-US/docs/Glossary/API) - MDN API documentation guide

---

**Last Updated:** 2025-11-24
**Version:** v1.0.0
**Maintained By:** Claude Skills Team
**Feedback:** Report issues via GitHub Issues with `[api-document]` tag
