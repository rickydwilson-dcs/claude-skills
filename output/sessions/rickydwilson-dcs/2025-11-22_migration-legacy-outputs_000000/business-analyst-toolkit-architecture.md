# Business Analyst Toolkit - Technical Architecture

**Version:** 1.0
**Date:** 2025-11-21
**Architect:** cs-architect
**Skill Location:** `skills/product-team/business-analyst-toolkit/`

## Executive Summary

This document defines the technical architecture for the business-analyst-toolkit skill, which provides 7 Python CLI tools for process analysis, documentation, and improvement. The architecture emphasizes:

- **Standard library only** (Python 3.8+, no external dependencies)
- **JSON-based data model** for process representation
- **CLI-first design** with argparse
- **Security patterns** for input validation and file handling
- **Tool chaining** through standard input/output streams

**Tools Overview:**
1. `process_parser.py` - Parse process docs from multiple formats
2. `gap_analyzer.py` - Identify process gaps and improvement opportunities
3. `raci_generator.py` - Generate RACI matrices from process definitions
4. `stakeholder_mapper.py` - Map stakeholder relationships and influence
5. `charter_builder.py` - Create process charters with governance
6. `improvement_planner.py` - Generate improvement roadmaps
7. `kpi_calculator.py` - Calculate process KPIs and metrics

---

## 1. Data Model

### 1.1 Core JSON Schema

All tools operate on a standardized JSON schema representing process definitions:

```json
{
  "schema_version": "1.0",
  "process_id": "proc_12345678",
  "process_name": "Purchase Order Processing",
  "process_description": "End-to-end workflow for purchase order creation, approval, and fulfillment",
  "process_owner": "Finance Director",
  "source": {
    "type": "text|url|image|transcript|directory",
    "location": "/path/to/source.md",
    "parsed_at": "2025-11-21T10:30:00Z"
  },
  "metadata": {
    "created_at": "2025-11-21T10:30:00Z",
    "updated_at": "2025-11-21T10:30:00Z",
    "version": "1.0",
    "tags": ["finance", "procurement", "approval-workflow"]
  },
  "steps": [
    {
      "id": "step_001",
      "name": "Create Purchase Requisition",
      "description": "Employee submits purchase requisition in procurement system",
      "sequence": 1,
      "role": "Requester",
      "duration_minutes": 15,
      "effort_hours": 0.25,
      "inputs": ["Business need", "Budget code", "Vendor information"],
      "outputs": ["Purchase requisition ID", "Approval request"],
      "decisions": [
        {
          "question": "Is purchase amount > $5,000?",
          "criteria": "Dollar threshold policy",
          "options": ["Route to Director", "Route to Manager"]
        }
      ],
      "confidence": 0.85
    }
  ],
  "roles": ["Requester", "Manager", "Director", "Finance", "Vendor"],
  "gaps": [
    {
      "type": "undefined_role|missing_decision|missing_info|bottleneck",
      "severity": "critical|high|medium|low",
      "step_id": "step_003",
      "description": "Step 'Approve Request' has no decision criteria",
      "impact": "Inconsistent approval decisions",
      "recommendation": "Define approval criteria based on amount, category, urgency"
    }
  ],
  "confidence_score": 0.78
}
```

### 1.2 Extended Schemas

**RACI Matrix Schema:**
```json
{
  "schema_version": "1.0",
  "process_id": "proc_12345678",
  "raci_matrix": [
    {
      "step_id": "step_001",
      "step_name": "Create Purchase Requisition",
      "responsible": ["Requester"],
      "accountable": ["Manager"],
      "consulted": ["Finance"],
      "informed": ["Director"]
    }
  ],
  "roles_summary": {
    "Requester": {
      "responsible_count": 2,
      "accountable_count": 0,
      "consulted_count": 1,
      "informed_count": 0,
      "workload_score": 0.65
    }
  },
  "conflicts": [
    {
      "type": "multiple_accountable|no_accountable|overloaded_role",
      "severity": "high",
      "step_id": "step_005",
      "description": "Multiple roles accountable for final approval",
      "recommendation": "Designate single accountable party"
    }
  ]
}
```

**Stakeholder Map Schema:**
```json
{
  "schema_version": "1.0",
  "process_id": "proc_12345678",
  "stakeholders": [
    {
      "name": "Finance Director",
      "role": "Process Owner",
      "influence": "high",
      "interest": "high",
      "category": "key_player",
      "concerns": ["Budget compliance", "Audit requirements"],
      "engagement_strategy": "Involve in all major decisions"
    }
  ],
  "relationships": [
    {
      "from": "Finance Director",
      "to": "Procurement Manager",
      "type": "reports_to|collaborates_with|approves|informs",
      "strength": "strong|moderate|weak"
    }
  ],
  "engagement_plan": [
    {
      "stakeholder": "Finance Director",
      "frequency": "weekly",
      "method": "status_report|meeting|email",
      "topics": ["Budget tracking", "Exception reports"]
    }
  ]
}
```

**Process Charter Schema:**
```json
{
  "schema_version": "1.0",
  "process_id": "proc_12345678",
  "charter": {
    "purpose": "Ensure timely, compliant purchase order processing",
    "scope": {
      "included": ["PO creation", "Approval workflow", "Vendor communication"],
      "excluded": ["Contract negotiation", "Invoice processing"]
    },
    "success_criteria": [
      "95% of POs approved within 24 hours",
      "100% compliance with approval policies",
      "90% first-time accuracy"
    ],
    "kpis": [
      {
        "name": "Cycle Time",
        "target": "24 hours",
        "frequency": "daily"
      }
    ],
    "governance": {
      "owner": "Finance Director",
      "review_frequency": "quarterly",
      "approval_authority": "CFO"
    },
    "assumptions": ["Budget codes are current", "Vendors respond within SLA"],
    "constraints": ["SOX compliance required", "SAP system limitations"],
    "risks": [
      {
        "description": "Approval delays during vacation periods",
        "likelihood": "medium",
        "impact": "high",
        "mitigation": "Designate backup approvers"
      }
    ]
  }
}
```

**Improvement Plan Schema:**
```json
{
  "schema_version": "1.0",
  "process_id": "proc_12345678",
  "improvement_plan": {
    "current_state": {
      "cycle_time_hours": 72,
      "first_time_accuracy": 0.65,
      "manual_steps": 12,
      "bottlenecks": ["Manager approval queue", "Vendor response time"]
    },
    "target_state": {
      "cycle_time_hours": 24,
      "first_time_accuracy": 0.90,
      "manual_steps": 5,
      "automation_opportunities": ["Auto-routing", "Status notifications"]
    },
    "initiatives": [
      {
        "id": "imp_001",
        "title": "Implement automated approval routing",
        "description": "Route based on amount, category, requester level",
        "priority": "high",
        "effort_weeks": 4,
        "impact_score": 0.85,
        "dependencies": [],
        "assigned_to": "IT Project Manager"
      }
    ],
    "roadmap": [
      {
        "phase": "Phase 1: Quick Wins",
        "duration_weeks": 8,
        "initiatives": ["imp_001", "imp_003"],
        "expected_impact": "30% cycle time reduction"
      }
    ],
    "investment": {
      "total_effort_weeks": 24,
      "estimated_cost_usd": 120000,
      "expected_annual_savings_usd": 240000,
      "roi_months": 6
    }
  }
}
```

**KPI Schema:**
```json
{
  "schema_version": "1.0",
  "process_id": "proc_12345678",
  "kpis": {
    "efficiency_metrics": {
      "cycle_time": {
        "value": 48.5,
        "unit": "hours",
        "target": 24.0,
        "variance": -102.1,
        "trend": "improving"
      },
      "throughput": {
        "value": 145,
        "unit": "transactions_per_day",
        "target": 200,
        "variance": -27.5,
        "trend": "stable"
      }
    },
    "quality_metrics": {
      "first_time_accuracy": {
        "value": 0.78,
        "unit": "percentage",
        "target": 0.90,
        "variance": -13.3,
        "trend": "declining"
      },
      "error_rate": {
        "value": 0.12,
        "unit": "percentage",
        "target": 0.05,
        "variance": 140.0,
        "trend": "worsening"
      }
    },
    "compliance_metrics": {
      "policy_adherence": {
        "value": 0.94,
        "unit": "percentage",
        "target": 1.00,
        "variance": -6.0,
        "trend": "stable"
      }
    },
    "cost_metrics": {
      "cost_per_transaction": {
        "value": 12.50,
        "unit": "usd",
        "target": 8.00,
        "variance": 56.3,
        "trend": "increasing"
      }
    },
    "summary": {
      "overall_health": "amber",
      "critical_issues": 2,
      "attention_needed": ["cycle_time", "error_rate"],
      "on_track": ["policy_adherence"]
    }
  }
}
```

---

## 2. Tool Architecture

### 2.1 Tool Design Principles

All tools follow consistent design patterns:

1. **CLI-First**: argparse-based command-line interface
2. **Standard Library Only**: No external dependencies (except optional OCR)
3. **Input Flexibility**: Accept file paths, stdin, or inline arguments
4. **Output Formats**: JSON (machine-readable) and human-readable text
5. **Error Handling**: Graceful failures with clear error messages
6. **Chainable**: Tools consume and produce standardized JSON schemas
7. **Documented**: Complete docstrings, --help text, usage examples

### 2.2 Tool Specifications

#### Tool 1: process_parser.py

**Status:** ✅ IMPLEMENTED (see existing file)

**Purpose:** Parse process documentation from multiple input formats

**Inputs:**
- Text files (.txt, .md)
- URLs (HTML content extraction)
- Images (OCR, optional)
- Transcripts (conversation analysis)
- Directories (multiple files)

**Outputs:**
- Process JSON schema
- Confidence scores for extracted data
- Gap identification (basic)

**Key Functions:**
- Auto-detect input type
- Extract process name, description, owner
- Parse steps with sequence, role, duration, inputs/outputs
- Identify decision points
- Generate unique process ID

**Already Implemented** - Reference implementation complete

---

#### Tool 2: gap_analyzer.py

**Purpose:** Identify process gaps and improvement opportunities

**Usage:**
```bash
# From process JSON
python gap_analyzer.py --input process.json --output gaps.json

# Direct from text (chains with parser)
python process_parser.py --input process.md | python gap_analyzer.py --stdin

# Verbose output
python gap_analyzer.py --input process.json --verbose
```

**Analysis Categories:**
1. **Missing Information**: Undefined roles, missing durations, no decision criteria
2. **Bottlenecks**: Steps with long durations, high effort, single point of failure
3. **Inefficiencies**: Manual work, redundant steps, unnecessary handoffs
4. **Compliance Risks**: No audit trails, approval bypasses, policy violations
5. **Quality Issues**: Error-prone steps, rework loops, no validation

**Output:**
- Gap list with severity (critical/high/medium/low)
- Impact analysis for each gap
- Prioritized recommendations
- Estimated improvement potential

---

#### Tool 3: raci_generator.py

**Purpose:** Generate RACI (Responsible, Accountable, Consulted, Informed) matrices

**Usage:**
```bash
# Generate RACI from process JSON
python raci_generator.py --input process.json --output raci.json

# Generate RACI and export to CSV
python raci_generator.py --input process.json --format csv --output raci.csv

# Interactive mode (prompts for missing RACI assignments)
python raci_generator.py --input process.json --interactive
```

**Logic:**
1. Extract roles from process steps
2. Assign initial RACI based on step role (R by default)
3. Infer Accountable from process owner + role hierarchy
4. Identify Consulted from inputs/outputs between steps
5. Determine Informed from stakeholder map (if available)
6. Validate RACI rules (one A per step, no missing R, etc.)

**Output:**
- RACI matrix JSON
- Role workload analysis
- Conflict detection (multiple A, no A, overloaded roles)
- Recommendations for RACI corrections

---

#### Tool 4: stakeholder_mapper.py

**Purpose:** Map stakeholder relationships and influence

**Usage:**
```bash
# Generate stakeholder map from process JSON
python stakeholder_mapper.py --input process.json --output stakeholders.json

# Add stakeholder manually
python stakeholder_mapper.py --input process.json --add-stakeholder \
  --name "CFO" --influence high --interest medium

# Generate influence/interest grid visualization (text-based)
python stakeholder_mapper.py --input process.json --grid
```

**Analysis:**
1. Extract stakeholders from process roles + owner
2. Calculate influence score (based on role level, approval authority)
3. Calculate interest score (based on process touchpoints, KPI ownership)
4. Categorize: Key Players, Keep Satisfied, Keep Informed, Monitor
5. Identify relationships (reports to, collaborates with, approves, informs)

**Output:**
- Stakeholder list with influence/interest scores
- Power/interest grid categorization
- Relationship map
- Engagement recommendations

---

#### Tool 5: charter_builder.py

**Purpose:** Create process charters with governance structure

**Usage:**
```bash
# Generate charter from process JSON
python charter_builder.py --input process.json --output charter.json

# Generate charter with template
python charter_builder.py --input process.json \
  --template ../assets/process-charter-template.md \
  --output charter.md

# Interactive mode (prompts for charter sections)
python charter_builder.py --input process.json --interactive
```

**Charter Sections:**
1. **Purpose**: Why this process exists
2. **Scope**: What's included/excluded
3. **Success Criteria**: Measurable outcomes
4. **KPIs**: Metrics and targets
5. **Governance**: Owner, review frequency, approval authority
6. **Assumptions**: What must be true for success
7. **Constraints**: Limitations and boundaries
8. **Risks**: Potential issues and mitigations

**Logic:**
- Extract purpose from process description
- Infer scope from step boundaries
- Suggest KPIs based on process type
- Identify risks from gaps analysis

**Output:**
- Charter JSON
- Charter markdown (formatted document)
- Checklist for charter review

---

#### Tool 6: improvement_planner.py

**Purpose:** Generate improvement roadmaps based on gap analysis

**Usage:**
```bash
# Generate improvement plan from gaps
python improvement_planner.py --input gaps.json --output improvement-plan.json

# Prioritize by ROI
python improvement_planner.py --input gaps.json --prioritize roi

# Quick wins only (< 4 weeks effort)
python improvement_planner.py --input gaps.json --quick-wins

# Full roadmap with phases
python improvement_planner.py --input gaps.json --phases 3 --output roadmap.json
```

**Analysis:**
1. Parse gaps from gap_analyzer output
2. Convert gaps to improvement initiatives
3. Estimate effort (person-weeks) and impact (% improvement)
4. Calculate priority score (impact / effort)
5. Group initiatives into phases (Quick Wins, Medium-term, Long-term)
6. Estimate investment and ROI

**Prioritization Methods:**
- **ROI**: Return on investment (savings / cost)
- **Impact**: Largest improvement potential
- **Effort**: Quickest wins (lowest effort)
- **Risk**: Address critical/high severity first

**Output:**
- Improvement plan JSON with initiatives
- Phased roadmap
- Investment and ROI estimates
- Success metrics for each initiative

---

#### Tool 7: kpi_calculator.py

**Purpose:** Calculate process KPIs and metrics

**Usage:**
```bash
# Calculate KPIs from process JSON and transaction data
python kpi_calculator.py --process process.json --data transactions.csv

# Calculate specific KPI
python kpi_calculator.py --process process.json --data transactions.csv \
  --kpi cycle_time

# Trend analysis (compare against historical data)
python kpi_calculator.py --process process.json \
  --current transactions-current.csv \
  --historical transactions-last-month.csv

# Generate dashboard (text-based)
python kpi_calculator.py --process process.json --data transactions.csv --dashboard
```

**KPI Categories:**
1. **Efficiency**: Cycle time, throughput, resource utilization
2. **Quality**: First-time accuracy, error rate, rework percentage
3. **Compliance**: Policy adherence, audit findings, SLA compliance
4. **Cost**: Cost per transaction, total process cost, waste

**Calculations:**
- **Cycle Time**: Sum of step durations (from process JSON)
- **Throughput**: Transactions per time period (from data CSV)
- **First-Time Accuracy**: (Successful / Total) from data
- **Error Rate**: (Errors / Total) from data
- **Cost Per Transaction**: Total cost / transaction count

**Output:**
- KPI JSON with values, targets, variance, trends
- Health summary (red/amber/green)
- Critical issues list
- Recommendations based on KPI analysis

---

## 3. Security Patterns

### 3.1 Input Validation

All tools implement strict input validation:

```python
def validate_filepath(filepath: str, allowed_extensions: List[str] = None) -> str:
    """
    Validate file path for security issues.

    Args:
        filepath: User-provided file path
        allowed_extensions: List of allowed file extensions (e.g., ['.json', '.txt'])

    Returns:
        Validated absolute path

    Raises:
        ValueError: If path is invalid or unsafe
    """
    from pathlib import Path

    # Reject if empty
    if not filepath or not filepath.strip():
        raise ValueError("File path cannot be empty")

    # Reject path traversal attempts
    if '..' in filepath:
        raise ValueError("Path traversal not allowed (..) ")

    # Convert to Path object for safe manipulation
    path = Path(filepath).resolve()

    # Ensure file exists
    if not path.exists():
        raise ValueError(f"File not found: {filepath}")

    # Ensure it's a file, not directory
    if not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    # Validate extension if specified
    if allowed_extensions:
        if path.suffix.lower() not in allowed_extensions:
            raise ValueError(f"Invalid file type. Allowed: {', '.join(allowed_extensions)}")

    return str(path)


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize filename for safe file system operations.

    Args:
        filename: User-provided filename
        max_length: Maximum filename length

    Returns:
        Sanitized filename
    """
    import re

    # Remove path separators and null bytes
    safe = re.sub(r'[/\\:\0]', '', filename)

    # Remove leading/trailing dots and spaces
    safe = safe.strip('. ')

    # Replace unsafe characters with underscore
    safe = re.sub(r'[<>"|?*]', '_', safe)

    # Limit length
    if len(safe) > max_length:
        name, ext = os.path.splitext(safe)
        safe = name[:max_length - len(ext)] + ext

    # Ensure not empty
    if not safe:
        safe = 'output'

    return safe


def validate_json_schema(data: dict, schema: dict) -> bool:
    """
    Validate JSON data against schema (basic validation without external libs).

    Args:
        data: JSON data to validate
        schema: Schema definition dict

    Returns:
        True if valid, raises ValueError otherwise
    """
    # Check required top-level fields
    required_fields = schema.get('required', [])
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Check schema version
    if 'schema_version' not in data:
        raise ValueError("Missing schema_version field")

    # Validate specific field types
    field_types = schema.get('field_types', {})
    for field, expected_type in field_types.items():
        if field in data:
            if expected_type == 'string' and not isinstance(data[field], str):
                raise ValueError(f"Field '{field}' must be string")
            elif expected_type == 'array' and not isinstance(data[field], list):
                raise ValueError(f"Field '{field}' must be array")
            elif expected_type == 'object' and not isinstance(data[field], dict):
                raise ValueError(f"Field '{field}' must be object")

    return True
```

### 3.2 File Handling

Safe file operations:

```python
def safe_read_file(filepath: str, max_size_mb: int = 10) -> str:
    """
    Safely read file with size limits.

    Args:
        filepath: Validated file path
        max_size_mb: Maximum file size in MB

    Returns:
        File contents

    Raises:
        ValueError: If file too large or read error
    """
    import os

    # Check file size
    file_size = os.path.getsize(filepath)
    max_size_bytes = max_size_mb * 1024 * 1024

    if file_size > max_size_bytes:
        raise ValueError(f"File too large: {file_size / 1024 / 1024:.1f}MB (max: {max_size_mb}MB)")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        raise ValueError("File is not valid UTF-8 text")
    except Exception as e:
        raise ValueError(f"Failed to read file: {str(e)}")


def safe_write_file(filepath: str, content: str, overwrite: bool = False) -> None:
    """
    Safely write file with overwrite protection.

    Args:
        filepath: Output file path
        content: Content to write
        overwrite: Allow overwriting existing files

    Raises:
        ValueError: If file exists and overwrite=False
    """
    import os

    # Check if file exists
    if os.path.exists(filepath) and not overwrite:
        raise ValueError(f"File exists (use --overwrite to replace): {filepath}")

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise ValueError(f"Failed to write file: {str(e)}")
```

### 3.3 Command Injection Prevention

No shell execution - use safe subprocess calls:

```python
# ❌ NEVER DO THIS
def run_command_unsafe(command: str):
    import subprocess
    subprocess.run(command, shell=True)  # DANGEROUS!

# ✅ SAFE APPROACH (if subprocess needed)
def run_command_safe(args: List[str], timeout: int = 30):
    import subprocess
    result = subprocess.run(
        args,  # List, not string
        capture_output=True,
        text=True,
        check=True,
        timeout=timeout,
        shell=False  # IMPORTANT!
    )
    return result.stdout
```

### 3.4 Error Handling

Secure error messages without information disclosure:

```python
def handle_error(error: Exception, verbose: bool = False) -> None:
    """
    Handle errors securely without exposing sensitive information.

    Args:
        error: Exception to handle
        verbose: Include stack trace
    """
    import sys

    # User-friendly error message
    if isinstance(error, ValueError):
        print(f"Error: {str(error)}", file=sys.stderr)
    elif isinstance(error, FileNotFoundError):
        print(f"Error: File not found", file=sys.stderr)
    elif isinstance(error, PermissionError):
        print(f"Error: Permission denied", file=sys.stderr)
    else:
        # Generic error for unknown exceptions
        print(f"Error: An unexpected error occurred", file=sys.stderr)

    # Optional stack trace for debugging
    if verbose:
        import traceback
        traceback.print_exc(file=sys.stderr)

    sys.exit(1)
```

---

## 4. Integration Points

### 4.1 Tool Chaining

Tools chain together via JSON input/output:

```bash
# Example: Full analysis pipeline
python process_parser.py --input process.md --output process.json && \
python gap_analyzer.py --input process.json --output gaps.json && \
python improvement_planner.py --input gaps.json --output plan.json && \
python kpi_calculator.py --process process.json --data transactions.csv

# Example: Using pipes (stdin/stdout)
python process_parser.py --input process.md | \
python gap_analyzer.py --stdin | \
python improvement_planner.py --stdin --format human
```

### 4.2 Data Flow

```
┌─────────────────────┐
│  process_parser.py  │
│  (parse docs)       │
└──────────┬──────────┘
           │ process.json
           ▼
┌─────────────────────┐
│  gap_analyzer.py    │
│  (find gaps)        │
└──────────┬──────────┘
           │ gaps.json
           ▼
┌─────────────────────┐
│ improvement_planner │
│  (create roadmap)   │
└──────────┬──────────┘
           │ plan.json
           ▼
┌─────────────────────┐
│  kpi_calculator.py  │
│  (measure impact)   │
└─────────────────────┘

Parallel Tools (operate on process.json):
├── raci_generator.py → raci.json
├── stakeholder_mapper.py → stakeholders.json
└── charter_builder.py → charter.json
```

### 4.3 Integration with Templates

Tools reference templates from `assets/` directory:

```python
def load_template(template_name: str) -> str:
    """
    Load template from assets directory.

    Args:
        template_name: Template filename

    Returns:
        Template content
    """
    from pathlib import Path

    # Get path relative to script location
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / 'assets' / template_name

    if not template_path.exists():
        raise ValueError(f"Template not found: {template_name}")

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()
```

### 4.4 CSV Import/Export

Tools support CSV for spreadsheet integration:

```python
def export_to_csv(data: dict, output_file: str) -> None:
    """
    Export JSON data to CSV format.

    Args:
        data: JSON data structure
        output_file: Output CSV path
    """
    import csv

    # Example: Export RACI matrix to CSV
    if 'raci_matrix' in data:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header row
            roles = list(data['roles_summary'].keys())
            writer.writerow(['Step'] + roles)

            # Data rows
            for item in data['raci_matrix']:
                row = [item['step_name']]
                for role in roles:
                    raci_code = []
                    if role in item.get('responsible', []):
                        raci_code.append('R')
                    if role in item.get('accountable', []):
                        raci_code.append('A')
                    if role in item.get('consulted', []):
                        raci_code.append('C')
                    if role in item.get('informed', []):
                        raci_code.append('I')
                    row.append(','.join(raci_code))
                writer.writerow(row)
```

---

## 5. Error Handling Strategy

### 5.1 Error Hierarchy

```python
class ProcessToolError(Exception):
    """Base exception for all process tools."""
    pass

class ValidationError(ProcessToolError):
    """Input validation failed."""
    pass

class ParseError(ProcessToolError):
    """Failed to parse input."""
    pass

class SchemaError(ProcessToolError):
    """JSON schema validation failed."""
    pass

class FileOperationError(ProcessToolError):
    """File operation failed."""
    pass
```

### 5.2 Error Handling Pattern

Consistent error handling across all tools:

```python
def main():
    parser = argparse.ArgumentParser(
        description='Tool description',
        epilog='Usage examples...'
    )
    # ... argument setup ...

    args = parser.parse_args()

    try:
        # Validate inputs
        validate_inputs(args)

        # Process data
        result = process_data(args)

        # Output results
        output_results(result, args)

        return 0  # Success

    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1

    except ParseError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        return 2

    except SchemaError as e:
        print(f"Schema error: {e}", file=sys.stderr)
        return 3

    except FileOperationError as e:
        print(f"File error: {e}", file=sys.stderr)
        return 4

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 99

if __name__ == '__main__':
    sys.exit(main())
```

### 5.3 Logging Strategy

Optional verbose logging for debugging:

```python
def log(message: str, level: str = 'INFO', verbose: bool = False) -> None:
    """
    Log message if verbose mode enabled.

    Args:
        message: Log message
        level: Log level (INFO, WARNING, ERROR)
        verbose: Enable logging
    """
    if verbose:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {level}: {message}", file=sys.stderr)
```

---

## 6. Code Templates

### 6.1 Standard Tool Template

Base template for all tools:

```python
#!/usr/bin/env python3
"""
Tool Name - Brief description

Detailed description of what this tool does.

Usage:
    python tool_name.py --input FILE [OPTIONS]

Author: Claude Skills - Business Analyst Toolkit
Version: 1.0.0
License: MIT
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Schema version
SCHEMA_VERSION = "1.0"


class ToolNameProcessor:
    """Main processing class for tool functionality."""

    def __init__(self, verbose: bool = False):
        """
        Initialize processor.

        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose

    def process(self, input_data: Dict) -> Dict:
        """
        Main processing method.

        Args:
            input_data: Input JSON data

        Returns:
            Processed output data

        Raises:
            ValueError: If input invalid
        """
        # Validate schema
        self._validate_schema(input_data)

        # Process data
        result = self._process_internal(input_data)

        # Add metadata
        result['schema_version'] = SCHEMA_VERSION
        result['processed_at'] = datetime.utcnow().isoformat() + 'Z'

        return result

    def _validate_schema(self, data: Dict) -> None:
        """Validate input data schema."""
        required_fields = ['process_id', 'process_name']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

    def _process_internal(self, data: Dict) -> Dict:
        """Internal processing logic."""
        # TODO: Implement tool-specific logic
        return {}

    def _log(self, message: str, level: str = 'INFO') -> None:
        """Log message if verbose enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] {level}: {message}", file=sys.stderr)


def validate_filepath(filepath: str, must_exist: bool = True) -> str:
    """
    Validate file path for security.

    Args:
        filepath: User-provided file path
        must_exist: Require file to exist

    Returns:
        Validated absolute path

    Raises:
        ValueError: If path invalid
    """
    if not filepath or not filepath.strip():
        raise ValueError("File path cannot be empty")

    if '..' in filepath:
        raise ValueError("Path traversal not allowed")

    path = Path(filepath).resolve()

    if must_exist and not path.exists():
        raise ValueError(f"File not found: {filepath}")

    if must_exist and not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    return str(path)


def read_json_file(filepath: str) -> Dict:
    """
    Read and parse JSON file safely.

    Args:
        filepath: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        ValueError: If file invalid or parse error
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    except Exception as e:
        raise ValueError(f"Failed to read file: {e}")


def write_json_file(filepath: str, data: Dict, overwrite: bool = False) -> None:
    """
    Write JSON data to file safely.

    Args:
        filepath: Output file path
        data: Data to write
        overwrite: Allow overwriting existing files

    Raises:
        ValueError: If file exists and overwrite=False
    """
    path = Path(filepath)

    if path.exists() and not overwrite:
        raise ValueError(f"File exists (use --overwrite): {filepath}")

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Failed to write file: {e}")


def format_human_readable(data: Dict) -> str:
    """
    Format data for human-readable output.

    Args:
        data: Data to format

    Returns:
        Formatted string
    """
    # TODO: Implement tool-specific formatting
    output = []
    output.append("=" * 80)
    output.append(f"Tool Output: {data.get('process_name', 'Unknown')}")
    output.append("=" * 80)
    # Add more formatting...
    return '\n'.join(output)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Tool Name - Brief description',
        epilog='Examples:\n'
               '  python tool_name.py --input process.json\n'
               '  python tool_name.py --input process.json --output result.json\n'
               '  python tool_name.py --stdin --format human\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Input arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', type=str, help='Input JSON file path')
    input_group.add_argument('--stdin', action='store_true', help='Read from stdin')

    # Output arguments
    parser.add_argument('--output', type=str, help='Output file path (default: stdout)')
    parser.add_argument('--format', type=str, default='json',
                       choices=['json', 'human'],
                       help='Output format (default: json)')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing output file')

    # Options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    try:
        # Read input
        if args.stdin:
            input_data = json.load(sys.stdin)
        else:
            input_path = validate_filepath(args.input, must_exist=True)
            input_data = read_json_file(input_path)

        # Process
        processor = ToolNameProcessor(verbose=args.verbose)
        result = processor.process(input_data)

        # Format output
        if args.format == 'json':
            output_text = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output_text = format_human_readable(result)

        # Write output
        if args.output:
            output_path = validate_filepath(args.output, must_exist=False)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_text)
            if args.verbose:
                print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(output_text)

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 99


if __name__ == '__main__':
    sys.exit(main())
```

### 6.2 Argparse Pattern

Consistent CLI structure:

```python
def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Setup command-line argument parser.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description='Tool description',
        epilog='Examples:\n'
               '  Example 1\n'
               '  Example 2\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Required arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', type=str,
                            help='Input file path')
    input_group.add_argument('--stdin', action='store_true',
                            help='Read from stdin')

    # Optional arguments
    parser.add_argument('--output', type=str,
                       help='Output file path (default: stdout)')
    parser.add_argument('--format', type=str, default='json',
                       choices=['json', 'human', 'csv'],
                       help='Output format (default: json)')

    # Flags
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing files')

    return parser
```

### 6.3 JSON Schema Validation

Schema validation without external dependencies:

```python
def validate_process_schema(data: Dict) -> None:
    """
    Validate process JSON schema.

    Args:
        data: Process JSON data

    Raises:
        ValueError: If schema invalid
    """
    # Required top-level fields
    required_fields = ['schema_version', 'process_id', 'process_name', 'steps']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Validate schema version
    if data['schema_version'] != SCHEMA_VERSION:
        raise ValueError(f"Unsupported schema version: {data['schema_version']}")

    # Validate steps array
    if not isinstance(data['steps'], list):
        raise ValueError("Field 'steps' must be an array")

    if len(data['steps']) == 0:
        raise ValueError("Process must have at least one step")

    # Validate each step
    for i, step in enumerate(data['steps']):
        if not isinstance(step, dict):
            raise ValueError(f"Step {i} must be an object")

        step_required = ['id', 'name', 'sequence']
        for field in step_required:
            if field not in step:
                raise ValueError(f"Step {i} missing required field: {field}")
```

---

## 7. Testing Strategy

### 7.1 Unit Testing

Each tool should have basic unit tests:

```python
def test_validate_filepath():
    """Test file path validation."""
    # Valid path
    try:
        result = validate_filepath('/tmp/test.json', must_exist=False)
        assert isinstance(result, str)
    except ValueError:
        assert False, "Valid path rejected"

    # Invalid path (traversal)
    try:
        validate_filepath('../etc/passwd')
        assert False, "Path traversal not blocked"
    except ValueError:
        pass  # Expected

    # Empty path
    try:
        validate_filepath('')
        assert False, "Empty path not rejected"
    except ValueError:
        pass  # Expected


def test_process_parser():
    """Test process parser basic functionality."""
    parser = ProcessParser('/path/to/test.md', 'text', verbose=False)
    # Add assertions...
```

### 7.2 Integration Testing

Test tool chaining:

```bash
#!/bin/bash
# test-integration.sh - Test tool integration

set -e  # Exit on error

echo "Testing tool integration..."

# Create test data
cat > test-process.md <<EOF
# Purchase Order Process

1. Create requisition (Manager, 15 min)
2. Approve request (Director, 30 min)
3. Create PO (Finance, 20 min)
EOF

# Test parser
echo "Testing process_parser..."
python scripts/process_parser.py --input test-process.md --output test-process.json

# Test gap analyzer
echo "Testing gap_analyzer..."
python scripts/gap_analyzer.py --input test-process.json --output test-gaps.json

# Test RACI generator
echo "Testing raci_generator..."
python scripts/raci_generator.py --input test-process.json --output test-raci.json

# Verify outputs exist
test -f test-process.json || { echo "process.json not created"; exit 1; }
test -f test-gaps.json || { echo "gaps.json not created"; exit 1; }
test -f test-raci.json || { echo "raci.json not created"; exit 1; }

# Cleanup
rm -f test-process.md test-process.json test-gaps.json test-raci.json

echo "✅ All integration tests passed"
```

### 7.3 Manual Testing Checklist

```yaml
tool_testing:
  basic_functionality:
    - [ ] --help flag displays usage
    - [ ] --input processes valid JSON file
    - [ ] --stdin reads from pipe
    - [ ] --output writes to file
    - [ ] --format json outputs valid JSON
    - [ ] --format human outputs readable text
    - [ ] --verbose shows debug information

  error_handling:
    - [ ] Invalid file path shows clear error
    - [ ] Missing required argument shows usage
    - [ ] Invalid JSON shows parse error
    - [ ] File not found shows clear message
    - [ ] Permission denied handled gracefully

  security:
    - [ ] Path traversal attempts blocked
    - [ ] Large files rejected
    - [ ] Invalid characters in filenames sanitized
    - [ ] No shell injection vulnerabilities

  integration:
    - [ ] Output compatible with next tool in chain
    - [ ] JSON schema validated by downstream tools
    - [ ] Templates referenced correctly
    - [ ] CSV export/import works
```

---

## 8. Implementation Roadmap

### Phase 1: Core Tools (Weeks 1-2)
- ✅ `process_parser.py` (COMPLETE)
- 🔨 `gap_analyzer.py` (implement)
- 🔨 `kpi_calculator.py` (implement)

### Phase 2: Collaboration Tools (Weeks 3-4)
- 🔨 `raci_generator.py` (implement)
- 🔨 `stakeholder_mapper.py` (implement)

### Phase 3: Planning Tools (Weeks 5-6)
- 🔨 `charter_builder.py` (implement)
- 🔨 `improvement_planner.py` (implement)

### Phase 4: Integration & Testing (Week 7)
- Integration testing
- Documentation completion
- Example workflows
- Template updates

---

## 9. Success Metrics

**Tool Quality:**
- 100% of tools execute without errors
- All tools support --help, --stdin, --output
- All tools handle errors gracefully
- All tools follow security patterns

**Integration:**
- Tools chain correctly via JSON schemas
- Templates referenced without errors
- CSV import/export validated

**Documentation:**
- Complete docstrings for all functions
- Usage examples for all tools
- Integration workflows documented

**Security:**
- No path traversal vulnerabilities
- Input validation on all user inputs
- No shell injection risks
- File size limits enforced

---

## 10. Dependencies

**Required:**
- Python 3.8+
- Standard library only (json, argparse, sys, pathlib, re, datetime, typing)

**Optional:**
- PIL (Pillow) - For image OCR in process_parser
- pytesseract - For OCR functionality
- If OCR not available, process_parser gracefully degrades

**No External Dependencies:**
All tools must work with standard library only. Optional features (like OCR) can require external packages but must fail gracefully if unavailable.

---

## 11. Architecture Decisions

### Decision 1: Standard Library Only
**Rationale:** Portability, simplicity, no dependency management
**Trade-off:** Some advanced features require more code (e.g., JSON schema validation)
**Impact:** Minimal - standard library provides all essential functionality

### Decision 2: JSON as Universal Format
**Rationale:** Widely supported, easy to parse, human-readable
**Trade-off:** Larger file sizes than binary formats
**Impact:** Acceptable - process definitions are typically small (<1MB)

### Decision 3: CLI-First Design
**Rationale:** Easy automation, composability, UNIX philosophy
**Trade-off:** No GUI for non-technical users
**Impact:** Acceptable - target audience is technical business analysts

### Decision 4: No Database
**Rationale:** Simplicity, portability, version control friendly
**Trade-off:** No centralized storage or multi-user access
**Impact:** Acceptable - users can store JSON in version control

### Decision 5: Text-Based Visualization
**Rationale:** No GUI dependencies, works in terminals
**Trade-off:** Less visually appealing than graphical tools
**Impact:** Acceptable - users can export to CSV for visualization in Excel/Tableau

---

## 12. Future Enhancements

**Potential Additions (Post-v1.0):**
1. **Web Interface:** Simple Flask/FastAPI UI for non-technical users
2. **Database Backend:** Optional SQLite storage for large process libraries
3. **Graph Visualization:** Export to Graphviz/Mermaid formats
4. **Process Mining:** Import from event logs (CSV)
5. **AI Integration:** Claude API integration for process recommendations
6. **Simulation:** Monte Carlo simulation for process performance
7. **Collaboration:** Multi-user features, comments, versioning
8. **Integration:** Export to BPMN, PowerPoint, Confluence

---

## Appendix A: File Structure

```
business-analyst-toolkit/
├── scripts/                    # Python CLI tools
│   ├── process_parser.py      # ✅ Implemented
│   ├── gap_analyzer.py        # 🔨 To implement
│   ├── raci_generator.py      # 🔨 To implement
│   ├── stakeholder_mapper.py  # 🔨 To implement
│   ├── charter_builder.py     # 🔨 To implement
│   ├── improvement_planner.py # 🔨 To implement
│   └── kpi_calculator.py      # 🔨 To implement
├── assets/                     # User templates
│   ├── process-charter-template.md
│   ├── raci-matrix-template.md
│   ├── stakeholder-analysis-template.md
│   └── improvement-proposal-template.md
├── references/                 # Knowledge bases
│   ├── process-analysis-guide.md
│   ├── gap-analysis-framework.md
│   └── improvement-methodologies.md
└── SKILL.md                   # Master documentation
```

---

## Appendix B: Code Quality Checklist

```yaml
python_quality:
  pep8_compliance:
    - [ ] 4-space indentation
    - [ ] Max line length 100 characters
    - [ ] Two blank lines between functions
    - [ ] Lowercase with underscores for function names

  documentation:
    - [ ] Module docstring at top
    - [ ] Docstrings for all public functions
    - [ ] Type hints for all function parameters
    - [ ] Usage examples in docstrings

  error_handling:
    - [ ] Try/except for all I/O operations
    - [ ] Clear error messages
    - [ ] Proper exception types
    - [ ] No bare except clauses

  security:
    - [ ] Path validation on all file operations
    - [ ] No shell=True in subprocess
    - [ ] Input validation on user data
    - [ ] No hardcoded credentials

  testing:
    - [ ] --help flag implemented
    - [ ] Basic unit tests written
    - [ ] Integration tests pass
    - [ ] Manual testing completed
```

---

**Document Status:** FINAL
**Review Date:** 2025-11-21
**Next Review:** After Phase 1 implementation
**Approved By:** cs-architect
