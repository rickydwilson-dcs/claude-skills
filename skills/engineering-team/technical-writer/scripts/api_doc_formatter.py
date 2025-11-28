#!/usr/bin/env python3
"""
API Documentation Formatter - Generates formatted API documentation from structured input
"""

import json
import re
import os
from typing import Dict, List, Any
from pathlib import Path


class ApiDocFormatter:
    def __init__(self, base_url: str = None, include_examples: bool = True):
        self.base_url = base_url or "https://api.example.com"
        self.include_examples = include_examples

        # HTTP method colors/badges
        self.method_badges = {
            'GET': '🟢',
            'POST': '🔵',
            'PUT': '🟠',
            'PATCH': '🟡',
            'DELETE': '🔴'
        }

    def parse_json_spec(self, json_path: str) -> Dict:
        """Parse API specification from JSON file"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                spec = json.load(f)
            return spec
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except Exception as e:
            raise ValueError(f"Error reading JSON file: {e}")

    def parse_code_directory(self, directory: str) -> Dict:
        """Parse API endpoints from Python/JavaScript code files"""
        endpoints = []
        dir_path = Path(directory)

        if not dir_path.exists():
            raise ValueError(f"Directory not found: {directory}")

        # Find Python and JavaScript files
        py_files = list(dir_path.rglob('*.py'))
        js_files = list(dir_path.rglob('*.js'))

        # Parse Python files for Flask/FastAPI routes
        for file in py_files:
            endpoints.extend(self._parse_python_file(file))

        # Parse JavaScript files for Express routes
        for file in js_files:
            endpoints.extend(self._parse_javascript_file(file))

        return {'endpoints': endpoints}

    def _parse_python_file(self, file_path: Path) -> List[Dict]:
        """Extract API endpoints from Python files"""
        endpoints = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Pattern for Flask routes: @app.route('/path', methods=['GET'])
            flask_pattern = r"@app\.route\(['\"]([^'\"]+)['\"](?:,\s*methods=\[([^\]]+)\])?\)"

            # Pattern for FastAPI: @app.get('/path')
            fastapi_patterns = [
                (r"@app\.get\(['\"]([^'\"]+)['\"]\)", 'GET'),
                (r"@app\.post\(['\"]([^'\"]+)['\"]\)", 'POST'),
                (r"@app\.put\(['\"]([^'\"]+)['\"]\)", 'PUT'),
                (r"@app\.patch\(['\"]([^'\"]+)['\"]\)", 'PATCH'),
                (r"@app\.delete\(['\"]([^'\"]+)['\"]\)", 'DELETE')
            ]

            # Find Flask routes
            for match in re.finditer(flask_pattern, content):
                path = match.group(1)
                methods = match.group(2) if match.group(2) else "'GET'"
                methods = [m.strip().strip("'\"") for m in methods.split(',')]

                for method in methods:
                    endpoints.append({
                        'method': method.upper(),
                        'path': path,
                        'description': f'{method.upper()} {path}',
                        'source': str(file_path)
                    })

            # Find FastAPI routes
            for pattern, method in fastapi_patterns:
                for match in re.finditer(pattern, content):
                    path = match.group(1)
                    endpoints.append({
                        'method': method,
                        'path': path,
                        'description': f'{method} {path}',
                        'source': str(file_path)
                    })

        except Exception:
            pass  # Skip files that can't be parsed

        return endpoints

    def _parse_javascript_file(self, file_path: Path) -> List[Dict]:
        """Extract API endpoints from JavaScript files"""
        endpoints = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Pattern for Express routes: app.get('/path', ...)
            patterns = [
                (r"app\.get\(['\"]([^'\"]+)['\"]", 'GET'),
                (r"app\.post\(['\"]([^'\"]+)['\"]", 'POST'),
                (r"app\.put\(['\"]([^'\"]+)['\"]", 'PUT'),
                (r"app\.patch\(['\"]([^'\"]+)['\"]", 'PATCH'),
                (r"app\.delete\(['\"]([^'\"]+)['\"]", 'DELETE'),
                (r"router\.get\(['\"]([^'\"]+)['\"]", 'GET'),
                (r"router\.post\(['\"]([^'\"]+)['\"]", 'POST'),
                (r"router\.put\(['\"]([^'\"]+)['\"]", 'PUT'),
                (r"router\.patch\(['\"]([^'\"]+)['\"]", 'PATCH'),
                (r"router\.delete\(['\"]([^'\"]+)['\"]", 'DELETE')
            ]

            for pattern, method in patterns:
                for match in re.finditer(pattern, content):
                    path = match.group(1)
                    endpoints.append({
                        'method': method,
                        'path': path,
                        'description': f'{method} {path}',
                        'source': str(file_path)
                    })

        except Exception:
            pass  # Skip files that can't be parsed

        return endpoints

    def format_markdown(self, spec: Dict, template_path: str = None) -> str:
        """Format API specification as Markdown documentation"""
        output = []

        # Use custom template if provided
        if template_path and Path(template_path).exists():
            return self._apply_template(spec, template_path)

        # Default template
        output.append("# API Documentation\n")

        # Get endpoints
        endpoints = spec.get('endpoints', [])

        if not endpoints:
            output.append("_No endpoints found._\n")
            return '\n'.join(output)

        # Group endpoints by path prefix
        grouped = self._group_endpoints(endpoints)

        for group_name, group_endpoints in grouped.items():
            if group_name:
                output.append(f"\n## {group_name}\n")

            for endpoint in group_endpoints:
                output.append(self._format_endpoint_markdown(endpoint))

        return '\n'.join(output)

    def _group_endpoints(self, endpoints: List[Dict]) -> Dict[str, List[Dict]]:
        """Group endpoints by path prefix"""
        groups = {}

        for endpoint in endpoints:
            path = endpoint.get('path', '')

            # Extract first path segment as group
            parts = [p for p in path.split('/') if p]
            group_name = parts[0].capitalize() if parts else 'Root'

            if group_name not in groups:
                groups[group_name] = []
            groups[group_name].append(endpoint)

        return groups

    def _format_endpoint_markdown(self, endpoint: Dict) -> str:
        """Format a single endpoint as Markdown"""
        output = []

        method = endpoint.get('method', 'GET')
        path = endpoint.get('path', '/')
        description = endpoint.get('description', f'{method} {path}')

        # Endpoint header
        badge = self.method_badges.get(method, '⚪')
        output.append(f"### {badge} `{method}` {path}\n")
        output.append(f"{description}\n")

        # Parameters
        parameters = endpoint.get('parameters', [])
        if parameters:
            output.append("#### Parameters\n")
            output.append("| Name | In | Type | Required | Description |")
            output.append("|------|-----|------|----------|-------------|")

            for param in parameters:
                name = param.get('name', '')
                location = param.get('in', 'query')
                param_type = param.get('type', 'string')
                required = 'Yes' if param.get('required', False) else 'No'
                desc = param.get('description', '')

                output.append(f"| {name} | {location} | {param_type} | {required} | {desc} |")

            output.append("")

        # Request body
        request_body = endpoint.get('requestBody')
        if request_body:
            output.append("#### Request Body\n")
            content_type = request_body.get('contentType', 'application/json')
            output.append(f"**Content-Type:** `{content_type}`\n")

            schema = request_body.get('schema')
            if schema:
                output.append("```json")
                output.append(json.dumps(schema, indent=2))
                output.append("```\n")

        # Examples
        if self.include_examples:
            output.append(self._generate_examples(endpoint))

        # Responses
        responses = endpoint.get('responses', {})
        if responses:
            output.append("#### Responses\n")

            for status_code, response in responses.items():
                desc = response.get('description', '')
                schema = response.get('schema')

                output.append(f"**{status_code}** {desc}\n")

                if schema:
                    output.append("```json")
                    output.append(json.dumps(schema, indent=2))
                    output.append("```\n")

        # Authentication
        auth = endpoint.get('authentication')
        if auth:
            output.append(f"#### Authentication\n")
            output.append(f"🔒 {auth}\n")

        output.append("---\n")

        return '\n'.join(output)

    def _generate_examples(self, endpoint: Dict) -> str:
        """Generate code examples for an endpoint"""
        output = []

        method = endpoint.get('method', 'GET')
        path = endpoint.get('path', '/')
        full_url = f"{self.base_url}{path}"

        # Replace path parameters with example values
        full_url = re.sub(r'\{([^}]+)\}', r'123', full_url)

        output.append("#### Examples\n")

        # cURL example
        output.append("**cURL**\n")
        output.append("```bash")

        curl_cmd = f'curl -X {method} "{full_url}"'

        # Add headers
        if endpoint.get('authentication'):
            curl_cmd += ' \\\n  -H "Authorization: Bearer $TOKEN"'

        if method in ['POST', 'PUT', 'PATCH']:
            curl_cmd += ' \\\n  -H "Content-Type: application/json"'

            # Add sample body
            request_body = endpoint.get('requestBody', {})
            schema = request_body.get('schema')
            if schema:
                body_json = json.dumps(schema, indent=2)
                curl_cmd += f" \\\n  -d '{body_json}'"

        output.append(curl_cmd)
        output.append("```\n")

        # Python example
        output.append("**Python**\n")
        output.append("```python")
        output.append("import requests\n")

        py_code = f'url = "{full_url}"'

        if endpoint.get('authentication'):
            py_code += '\nheaders = {"Authorization": "Bearer YOUR_TOKEN"}'
        else:
            py_code += '\nheaders = {}'

        if method == 'GET':
            py_code += f'\nresponse = requests.get(url, headers=headers)'
        elif method in ['POST', 'PUT', 'PATCH']:
            request_body = endpoint.get('requestBody', {})
            schema = request_body.get('schema', {})
            py_code += f'\ndata = {json.dumps(schema)}'
            py_code += f'\nresponse = requests.{method.lower()}(url, json=data, headers=headers)'
        elif method == 'DELETE':
            py_code += f'\nresponse = requests.delete(url, headers=headers)'

        py_code += '\nprint(response.json())'

        output.append(py_code)
        output.append("```\n")

        # JavaScript example
        output.append("**JavaScript**\n")
        output.append("```javascript")

        js_code = f'const url = "{full_url}";'

        js_options = '{\n  method: "' + method + '"'

        if endpoint.get('authentication'):
            js_options += ',\n  headers: {\n    "Authorization": "Bearer YOUR_TOKEN"'
            if method in ['POST', 'PUT', 'PATCH']:
                js_options += ',\n    "Content-Type": "application/json"'
            js_options += '\n  }'
        elif method in ['POST', 'PUT', 'PATCH']:
            js_options += ',\n  headers: {\n    "Content-Type": "application/json"\n  }'

        if method in ['POST', 'PUT', 'PATCH']:
            request_body = endpoint.get('requestBody', {})
            schema = request_body.get('schema', {})
            js_options += ',\n  body: JSON.stringify(' + json.dumps(schema) + ')'

        js_options += '\n}'

        js_code += f'\nconst options = {js_options};'
        js_code += '\n\nfetch(url, options)'
        js_code += '\n  .then(response => response.json())'
        js_code += '\n  .then(data => console.log(data))'
        js_code += '\n  .catch(error => console.error("Error:", error));'

        output.append(js_code)
        output.append("```\n")

        return '\n'.join(output)

    def _apply_template(self, spec: Dict, template_path: str) -> str:
        """Apply custom template to API spec"""
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # Simple variable replacement
        endpoints = spec.get('endpoints', [])

        # Replace {{endpoint_count}}
        template = template.replace('{{endpoint_count}}', str(len(endpoints)))

        # Generate endpoint documentation
        endpoint_docs = []
        for endpoint in endpoints:
            endpoint_docs.append(self._format_endpoint_markdown(endpoint))

        # Replace {{endpoints}}
        template = template.replace('{{endpoints}}', '\n'.join(endpoint_docs))

        return template

    def format_openapi_yaml(self, spec: Dict) -> str:
        """Format API specification as OpenAPI YAML"""
        output = []

        output.append("openapi: 3.0.0")
        output.append("info:")
        output.append(f"  title: {spec.get('title', 'API Documentation')}")
        output.append(f"  version: {spec.get('version', '1.0.0')}")
        output.append(f"  description: {spec.get('description', 'API documentation')}")
        output.append("")
        output.append("servers:")
        output.append(f"  - url: {self.base_url}")
        output.append(f"    description: API server")
        output.append("")
        output.append("paths:")

        endpoints = spec.get('endpoints', [])

        for endpoint in endpoints:
            path = endpoint.get('path', '/')
            method = endpoint.get('method', 'GET').lower()

            output.append(f"  {path}:")
            output.append(f"    {method}:")
            output.append(f"      summary: {endpoint.get('description', f'{method.upper()} {path}')}")

            # Parameters
            parameters = endpoint.get('parameters', [])
            if parameters:
                output.append("      parameters:")
                for param in parameters:
                    output.append(f"        - name: {param.get('name', '')}")
                    output.append(f"          in: {param.get('in', 'query')}")
                    output.append(f"          required: {str(param.get('required', False)).lower()}")
                    output.append("          schema:")
                    output.append(f"            type: {param.get('type', 'string')}")
                    if param.get('description'):
                        output.append(f"          description: {param.get('description')}")

            # Responses
            responses = endpoint.get('responses', {})
            if responses:
                output.append("      responses:")
                for status_code, response in responses.items():
                    output.append(f"        '{status_code}':")
                    output.append(f"          description: {response.get('description', '')}")

                    if response.get('schema'):
                        output.append("          content:")
                        output.append("            application/json:")
                        output.append("              schema:")
                        output.append(f"                type: object")

            output.append("")

        return '\n'.join(output)


def format_api_docs(source: str, output_format: str = 'markdown',
                   include_examples: bool = True, base_url: str = None,
                   template: str = None, verbose: bool = False) -> str:
    """Main function to format API documentation"""

    formatter = ApiDocFormatter(base_url=base_url, include_examples=include_examples)

    # Determine source type
    source_path = Path(source)

    if not source_path.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    # Parse source
    if source_path.is_file() and source_path.suffix == '.json':
        if verbose:
            print(f"📚 Parsing JSON specification: {source}")
        spec = formatter.parse_json_spec(source)
    elif source_path.is_dir():
        if verbose:
            print(f"📚 Scanning directory for API endpoints: {source}")
        spec = formatter.parse_code_directory(source)
    else:
        raise ValueError(f"Source must be a JSON file or directory: {source}")

    if verbose:
        endpoint_count = len(spec.get('endpoints', []))
        print(f"✅ Found {endpoint_count} API endpoint(s)")

    # Format output
    if output_format == 'markdown':
        if verbose:
            print("📋 Generating Markdown documentation...")
        return formatter.format_markdown(spec, template)
    elif output_format == 'openapi-yaml':
        if verbose:
            print("📋 Generating OpenAPI YAML specification...")
        return formatter.format_openapi_yaml(spec)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Format API documentation from structured input or code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Format from JSON spec
  %(prog)s api-spec.json

  # Format with code examples
  %(prog)s api-spec.json --include-examples

  # Generate OpenAPI YAML
  %(prog)s api-spec.json --format openapi-yaml

  # Scan Python/JS code directory
  %(prog)s src/api/

  # Custom base URL
  %(prog)s api-spec.json --base-url https://api.myapp.com

  # Output to file
  %(prog)s api-spec.json --output docs/api.md

  # Use custom template
  %(prog)s api-spec.json --template my-template.md

For more information, see the skill documentation.
        """
    )

    # Required arguments
    parser.add_argument(
        'source',
        help='JSON file with API spec OR directory with Python/JS files'
    )

    # Optional arguments
    parser.add_argument(
        '--format', '-f',
        choices=['markdown', 'openapi-yaml'],
        default='markdown',
        help='Output format: markdown (default) or openapi-yaml'
    )

    parser.add_argument(
        '--include-examples', '-e',
        action='store_true',
        default=True,
        help='Generate code examples (curl, Python, JavaScript) - enabled by default'
    )

    parser.add_argument(
        '--no-examples',
        action='store_true',
        help='Disable code examples generation'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout)'
    )

    parser.add_argument(
        '--base-url', '-b',
        default='https://api.example.com',
        help='API base URL for examples (default: https://api.example.com)'
    )

    parser.add_argument(
        '--template', '-t',
        help='Use custom template file'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Detailed output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    try:
        # Handle --no-examples flag
        include_examples = args.include_examples and not args.no_examples

        # Generate documentation
        if args.verbose:
            print("📚 API Documentation Formatter")
            print(f"🔗 Base URL: {args.base_url}")
            print(f"📋 Format: {args.format}")
            print()

        output = format_api_docs(
            source=args.source,
            output_format=args.format,
            include_examples=include_examples,
            base_url=args.base_url,
            template=args.template,
            verbose=args.verbose
        )

        # Write output
        if args.output:
            try:
                output_path = Path(args.output)

                # Create parent directories if needed
                output_path.parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output)

                if args.verbose:
                    print(f"✅ Documentation written to: {args.output}")
                else:
                    print(f"✅ Output saved to: {args.output}")

            except PermissionError:
                print(f"❌ Error: Permission denied writing to: {args.output}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"❌ Error writing output file: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(output)

        sys.exit(0)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"❌ Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
