# Python CLI Standards

## Overview

This document defines the standard patterns for Python command-line interface (CLI) implementations across all claude-skills tools. These standards ensure consistency, usability, and maintainability across 67+ Python scripts.

**Version:** 1.0.0
**Last Updated:** 2025-11-05
**Scope:** All Python scripts in claude-skills repository

---

## Core Principles

### 1. Consistency
- All scripts follow the same argument parsing pattern
- Users learn once, use everywhere
- Predictable behavior across all tools

### 2. User Experience
- Automatic `--help` / `-h` support
- Clear, actionable error messages
- Intuitive flag naming
- Comprehensive usage examples

### 3. Integration-Friendly
- Multiple output formats (text, JSON, CSV)
- File output support for pipelines
- Proper exit codes
- Machine-readable structured output

### 4. Maintainability
- Use `argparse` (never manual `sys.argv` parsing)
- Type hints and validation
- Automatic documentation generation
- Easy to extend

---

## Required Components

### 1. Argument Parser

All scripts **MUST** use Python's `argparse.ArgumentParser`:

```python
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Clear, concise description of tool purpose',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.txt
  %(prog)s input.txt --output json
  %(prog)s input.txt -o json --file results.json

For more information, see the skill documentation.
        """
    )
```

**Rationale:**
- Automatic `--help` generation
- Built-in validation
- Consistent UX
- No manual parsing errors

**❌ Never Do This:**
```python
# WRONG - Manual sys.argv parsing
if len(sys.argv) > 1:
    file = sys.argv[1]
    format = sys.argv[2] if len(sys.argv) > 2 else 'text'
```

---

### 2. Standard Flags

#### Required Flags (All Scripts)

##### Input Argument
```python
parser.add_argument(
    'input',
    help='Input file path, data source, or target'
)
```
- Position: First positional argument
- Type: String (file path or identifier)
- Required: Yes (or use `nargs='?'` for optional)

##### Output Format Flag
```python
parser.add_argument(
    '--output', '-o',
    choices=['text', 'json', 'csv'],
    default='text',
    help='Output format (default: text)'
)
```
- Short form: `-o`
- Long form: `--output`
- Valid choices: `text`, `json`, `csv` (minimum: text + json)
- Default: `text`

#### Optional Flags (Recommended)

##### Verbose Flag
```python
parser.add_argument(
    '--verbose', '-v',
    action='store_true',
    help='Enable verbose output with detailed information'
)
```

##### File Output Flag
```python
parser.add_argument(
    '--file', '-f',
    help='Write output to file instead of stdout'
)
```

##### Version Flag
```python
parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s 1.0.0'
)
```

---

### 3. Argument Naming Conventions

| Purpose | Short | Long | Type | Notes |
|---------|-------|------|------|-------|
| Input file/target | (positional) | - | string | Required |
| Output format | `-o` | `--output` | choice | text/json/csv |
| Verbose mode | `-v` | `--verbose` | flag | Boolean |
| Output file | `-f` | `--file` | string | File path |
| Configuration | `-c` | `--config` | string | Config file |
| Input path | `-i` | `--input` | string | When multiple inputs |
| Help | `-h` | `--help` | flag | Automatic |
| Version | - | `--version` | flag | Show version |

**Consistency Rules:**
- Always provide both short (`-x`) and long (`--xxx`) forms
- Use lowercase for all flags
- Use hyphens (not underscores) in long forms
- Boolean flags use `action='store_true'`

---

## Output Format Standards

### Text Output (Default)

**Purpose:** Human-readable output for interactive use

**Format Requirements:**
```
=== Section Header ===

Key Information:
- Bullet point 1
- Bullet point 2

Subsection:
  Indented details
  Additional context

--- Separator ---

Summary or Next Steps
```

**Guidelines:**
- Use `===` for major section headers
- Use `---` for separators
- Indent for hierarchy (2 spaces)
- Bullet points for lists
- Clear, scannable layout

### JSON Output

**Purpose:** Machine-readable, structured data for tool integration

**Format Requirements:**
```json
{
  "metadata": {
    "tool": "script_name",
    "version": "1.0.0",
    "timestamp": "2025-11-05T10:30:00Z",
    "execution_time_ms": 1250
  },
  "results": {
    "key_metric": "value",
    "data": [...]
  },
  "errors": [],
  "warnings": []
}
```

**Guidelines:**
- Use `json.dumps(data, indent=2)` for formatting
- Always include metadata section
- ISO 8601 timestamps
- Include all information from text output
- Preserve numeric types (don't stringify)

### CSV Output

**Purpose:** Tabular data for spreadsheet import

**Format Requirements:**
```csv
column1,column2,column3
value1,value2,value3
value4,value5,value6
```

**Guidelines:**
- Header row with column names
- Standard comma delimiter
- Quote fields containing commas
- One record per line
- No empty lines

---

## Error Handling

### File Validation

```python
import sys
from pathlib import Path

try:
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not input_path.is_file():
        print(f"Error: Path is not a file: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, 'r') as f:
        content = f.read()

except PermissionError:
    print(f"Error: Permission denied reading file: {args.input}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error reading file: {e}", file=sys.stderr)
    sys.exit(1)
```

### Exit Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 0 | Success | Normal completion |
| 1 | General error | File not found, invalid input |
| 2 | Invalid arguments | Missing required args (argparse handles) |
| 3 | Processing error | Business logic failure |
| 4 | Output error | Cannot write output file |

### Error Message Format

```python
# Good error messages
print(f"Error: Input file not found: {filename}", file=sys.stderr)
print(f"Error: Invalid format '{fmt}'. Expected: text, json, or csv", file=sys.stderr)

# Bad error messages (don't do this)
print("Error")  # Not descriptive
print("File not found")  # Missing context
raise Exception("error")  # Use sys.exit() instead
```

**Guidelines:**
- Prefix with "Error: " for clarity
- Include specific details (filename, value, etc.)
- Suggest fixes when possible
- Write to stderr using `file=sys.stderr`
- Use appropriate exit code

---

## Complete Template

See [`templates/python-cli-template.py`](../templates/python-cli-template.py) for a complete, copy-paste ready template implementing all standards.

---

## Migration Checklist

When updating existing scripts to these standards:

### Pre-Migration
- [ ] Read and understand existing script functionality
- [ ] Identify all current command-line arguments
- [ ] Note any custom output formats
- [ ] Check for dependencies on current CLI

### Implementation
- [ ] Replace manual `sys.argv` with `argparse.ArgumentParser`
- [ ] Add required flags: input, --output
- [ ] Add optional flags: --verbose, --file
- [ ] Implement all output formats (text, json minimum)
- [ ] Add file validation and error handling
- [ ] Include usage examples in epilog
- [ ] Add type hints to functions
- [ ] Update docstrings

### Testing
- [ ] Test `python script.py --help`
- [ ] Test with valid input file
- [ ] Test with missing file (should error gracefully)
- [ ] Test `--output json` format
- [ ] Test `--output text` format (default)
- [ ] Test `--file output.txt` writing
- [ ] Test `--verbose` mode
- [ ] Test all error conditions

### Documentation
- [ ] Update SKILL.md with new usage examples
- [ ] Document all flags and options
- [ ] Include JSON output schema examples
- [ ] Add common workflow examples
- [ ] Note any breaking changes

---

## Examples

### Simple Script (Single Input File)

```python
#!/usr/bin/env python3
"""
Analyzes content for brand voice consistency.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

def analyze_content(content: str) -> Dict[str, Any]:
    """Analyze content and return results."""
    # Implementation here
    return {
        "tone": "professional",
        "score": 85,
        "recommendations": ["Use more active voice"]
    }

def format_text_output(results: Dict[str, Any]) -> str:
    """Format results as human-readable text."""
    output = "=== Brand Voice Analysis ===\n\n"
    output += f"Tone: {results['tone']}\n"
    output += f"Score: {results['score']}/100\n\n"
    output += "Recommendations:\n"
    for rec in results['recommendations']:
        output += f"- {rec}\n"
    return output

def main():
    parser = argparse.ArgumentParser(
        description='Analyze content for brand voice consistency',
        epilog="""
Examples:
  %(prog)s content.txt
  %(prog)s content.txt --output json
  %(prog)s content.txt -o json -f results.json
        """
    )

    parser.add_argument('input', help='Content file to analyze')
    parser.add_argument('--output', '-o', choices=['text', 'json'],
                       default='text', help='Output format')
    parser.add_argument('--file', '-f', help='Write output to file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')

    args = parser.parse_args()

    try:
        # Validate input
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Read content
        with open(input_path, 'r') as f:
            content = f.read()

        if args.verbose:
            print(f"Analyzing {len(content)} characters...", file=sys.stderr)

        # Process
        results = analyze_content(content)

        # Format output
        if args.output == 'json':
            output = json.dumps(results, indent=2)
        else:
            output = format_text_output(results)

        # Write output
        if args.file:
            with open(args.file, 'w') as f:
                f.write(output)
            if args.verbose:
                print(f"Results written to {args.file}", file=sys.stderr)
        else:
            print(output)

        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Complex Script (Multiple Options)

```python
def main():
    parser = argparse.ArgumentParser(
        description='SEO content optimizer with keyword analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  %(prog)s content.txt

  # With keyword targeting
  %(prog)s content.txt --keyword "python programming"

  # With secondary keywords
  %(prog)s content.txt -k "python" -s "coding,development,tutorial"

  # JSON output to file
  %(prog)s content.txt -k "python" -o json -f results.json
        """
    )

    parser.add_argument('input', help='Content file to optimize')

    parser.add_argument('--keyword', '-k',
                       help='Primary keyword for optimization')

    parser.add_argument('--secondary', '-s',
                       help='Comma-separated secondary keywords')

    parser.add_argument('--output', '-o',
                       choices=['text', 'json'],
                       default='text',
                       help='Output format (default: text)')

    parser.add_argument('--file', '-f',
                       help='Write output to file')

    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Show detailed analysis steps')

    parser.add_argument('--min-score', type=int, default=60,
                       help='Minimum SEO score threshold (default: 60)')

    args = parser.parse_args()

    # Implementation...
```

---

## Best Practices

### 1. Type Hints
```python
from typing import Dict, List, Any, Optional

def process_content(content: str, keyword: Optional[str] = None) -> Dict[str, Any]:
    """Process content with optional keyword targeting."""
    pass
```

### 2. Docstrings
```python
def main():
    """
    Main entry point for the script.

    Parses command-line arguments, validates input, processes content,
    and writes output in the specified format.
    """
    pass
```

### 3. Separate Concerns
```python
# Good: Separate parsing, processing, and output
def main():
    args = parse_arguments()
    data = load_input(args.input)
    results = process_data(data)
    output = format_output(results, args.output)
    write_output(output, args.file)

# Bad: Everything in main()
def main():
    # 200 lines of mixed logic
```

### 4. Testability
```python
# Good: Functions can be tested independently
def analyze_content(content: str) -> Dict[str, Any]:
    return {"score": 85}

# Can test: analyze_content("test content")

# Bad: Everything depends on sys.argv
def main():
    if len(sys.argv) > 1:
        # Can't test without mocking sys.argv
```

---

## Common Patterns

### Optional Input with Sample Data
```python
parser.add_argument('input', nargs='?',
                   help='CSV file with data or "sample" to create sample')

args = parser.parse_args()

if args.input == 'sample':
    create_sample_file('sample.csv')
    sys.exit(0)

if not args.input:
    # Use built-in sample data
    data = get_sample_data()
else:
    data = load_from_file(args.input)
```

### Multiple Input Files
```python
parser.add_argument('inputs', nargs='+',
                   help='One or more input files to process')

# Usage: script.py file1.txt file2.txt file3.txt
```

### Config File Support
```python
parser.add_argument('--config', '-c',
                   help='Configuration file (JSON)')

if args.config:
    with open(args.config) as f:
        config = json.load(f)
else:
    config = get_default_config()
```

---

## Anti-Patterns to Avoid

### ❌ Manual Argument Parsing
```python
# WRONG
if len(sys.argv) > 1:
    file = sys.argv[1]
```

### ❌ Hardcoded Values
```python
# WRONG
output_format = 'json'  # Should be configurable
```

### ❌ Poor Error Messages
```python
# WRONG
print("Error")

# RIGHT
print(f"Error: Input file not found: {filename}", file=sys.stderr)
```

### ❌ Silent Failures
```python
# WRONG
try:
    data = load_file(file)
except:
    pass  # Silently fails

# RIGHT
try:
    data = load_file(file)
except FileNotFoundError:
    print(f"Error: File not found: {file}", file=sys.stderr)
    sys.exit(1)
```

### ❌ No Exit Codes
```python
# WRONG
print("Error occurred")
# Continues with exit code 0

# RIGHT
print(f"Error: {message}", file=sys.stderr)
sys.exit(1)
```

---

## Backward Compatibility

When migrating scripts that users may have integrated:

### Maintain Basic Usage
```python
# Old: python script.py file.txt
# New: python script.py file.txt (still works!)
```

### Add New Features as Optional
```python
# Old behavior preserved
parser.add_argument('input')  # Required positional

# New features are optional
parser.add_argument('--output', '-o', default='text')
```

### Deprecation Warnings
```python
if old_arg_detected:
    print("Warning: This argument format is deprecated. "
          "Use --new-format instead.", file=sys.stderr)
```

---

## Validation

All scripts must pass these checks:

```bash
# 1. Help flag works
python script.py --help

# 2. Version flag works (if implemented)
python script.py --version

# 3. JSON output works
python script.py input.txt --output json

# 4. File output works
python script.py input.txt --file output.txt

# 5. Error handling works
python script.py nonexistent.txt  # Should exit 1 with clear error
```

---

## Related Documentation

- [Quality Standards](quality/quality-standards.md) - Overall code quality requirements
- [Python CLI Template](../templates/python-cli-template.py) - Ready-to-use template
- [Documentation Standards](docs/documentation-standards.md) - How to document CLIs

---

## Questions & Support

For questions about these standards:
1. Review the template: `templates/python-cli-template.py`
2. Check existing implementations: Look at `skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py`
3. See SKILL.md files for usage examples

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-05
**Maintained By:** claude-skills project
