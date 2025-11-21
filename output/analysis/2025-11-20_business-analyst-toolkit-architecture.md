# Business Analyst Toolkit - Architecture Design

**Created:** November 20, 2025
**Status:** Design Complete → Ready for Implementation
**Architecture Type:** Modular CLI Tool Suite with Shared Data Model
**Based On:** PRD (2025-11-20_business-analyst-toolkit-PRD.md)

---

## Architecture Overview

### Design Philosophy

**Principles:**
1. **CLI-First**: Every tool is a standalone CLI script with --help and JSON output
2. **Data-Driven**: Central JSON schema enables tool composition and piping
3. **Standard Library**: Core functionality uses Python stdlib only (graceful fallbacks for optional features)
4. **Modular**: Each tool does one thing well, composable via Unix pipes or sequential execution
5. **Portable**: No external dependencies for core features, runs anywhere Python 3.8+ exists

**Architecture Pattern:** Pipeline Architecture with Shared Data Model

```
Input Sources              Core Tools                  Output Formats
┌──────────────┐          ┌──────────────┐           ┌──────────────┐
│ URLs         │──────┐   │  Parser      │──────┬───→│ JSON         │
│ Text Files   │──────┤   ├──────────────┤      │    │ CSV          │
│ Images       │──────┼──→│  Mapper      │──────┼───→│ Markdown     │
│ Transcripts  │──────┘   ├──────────────┤      │    │ SVG/PNG      │
└──────────────┘          │  Analyzer    │──────┤    │ HTML         │
                           ├──────────────┤      │    │ Mermaid      │
                           │  Comparator  │──────┴───→│ Lucidchart   │
                           ├──────────────┤           │ Miro         │
                           │  Prioritizer │           └──────────────┘
                           └──────────────┘
```

---

## Data Model: Central JSON Schema

### Core Schema (v1.0)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["process_name", "steps"],
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "1.0",
      "description": "Schema version for compatibility"
    },
    "process_name": {
      "type": "string",
      "description": "Human-readable process name"
    },
    "process_id": {
      "type": "string",
      "description": "Unique process identifier (auto-generated UUID)"
    },
    "process_owner": {
      "type": "string",
      "description": "Person or role responsible for process"
    },
    "process_description": {
      "type": "string",
      "description": "Brief process overview"
    },
    "source": {
      "type": "object",
      "properties": {
        "type": {"enum": ["url", "file", "image", "transcript"]},
        "location": {"type": "string"},
        "parsed_at": {"type": "string", "format": "date-time"}
      }
    },
    "confidence_score": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Overall confidence in parsed process (0.0-1.0)"
    },
    "steps": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^step_[0-9]{3}$",
            "description": "Unique step identifier (step_001, step_002, ...)"
          },
          "name": {
            "type": "string",
            "description": "Step name/title"
          },
          "description": {
            "type": "string",
            "description": "Detailed step description"
          },
          "role": {
            "type": "string",
            "description": "Role or person responsible for this step"
          },
          "duration_minutes": {
            "type": "number",
            "minimum": 0,
            "description": "Average duration in minutes"
          },
          "effort_hours": {
            "type": "number",
            "minimum": 0,
            "description": "Person-hours required"
          },
          "inputs": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Required inputs/artifacts"
          },
          "outputs": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Produced outputs/artifacts"
          },
          "decisions": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "question": {"type": "string"},
                "criteria": {"type": "string"},
                "options": {"type": "array", "items": {"type": "string"}}
              }
            },
            "description": "Decision points in this step"
          },
          "handoffs": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "to_role": {"type": "string"},
                "artifact": {"type": "string"}
              }
            },
            "description": "Handoffs to other roles/teams"
          },
          "automation_potential": {
            "type": "string",
            "enum": ["high", "medium", "low", "none"],
            "description": "Potential for automation"
          },
          "confidence": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Confidence in this step's data (0.0-1.0)"
          },
          "sequence": {
            "type": "integer",
            "description": "Step order in process"
          },
          "parallel_steps": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Step IDs that can run in parallel"
          }
        }
      }
    },
    "roles": {
      "type": "array",
      "items": {"type": "string"},
      "description": "All roles involved in process"
    },
    "metrics": {
      "type": "object",
      "properties": {
        "total_cycle_time_minutes": {"type": "number"},
        "total_processing_time_minutes": {"type": "number"},
        "total_wait_time_minutes": {"type": "number"},
        "total_handoffs": {"type": "integer"},
        "process_efficiency_percent": {"type": "number"}
      }
    },
    "gaps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type", "severity", "description"],
        "properties": {
          "type": {
            "type": "string",
            "enum": [
              "missing_info",
              "undefined_role",
              "missing_decision",
              "unclear_handoff",
              "incomplete_step",
              "contradiction",
              "missing_sla"
            ]
          },
          "severity": {
            "type": "string",
            "enum": ["critical", "high", "medium", "low"]
          },
          "step_id": {"type": "string"},
          "description": {"type": "string"},
          "impact": {"type": "string"},
          "suggested_questions": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "version": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "category": {"type": "string"}
      }
    }
  }
}
```

### Schema Design Rationale

**Why JSON?**
- Universal format (language-agnostic)
- Human-readable and machine-parseable
- Easy to validate, transform, and extend
- Native Python support (json module)

**Why This Structure?**
- **Flat steps array**: Easy to iterate, filter, map
- **Confidence scores**: Transparency about data quality
- **Embedded gaps**: Self-documenting issues
- **Extensible metadata**: Future-proof for V2 features

**Migration Strategy:**
- V1.0 schema is stable (no breaking changes in V1.x)
- V2.0 will add fields (backward compatible)
- Tools validate schema version and fail gracefully

---

## Module Architecture

### 1. process_parser.py

**Purpose:** Universal process parser supporting multiple input formats

**Architecture:**

```
┌──────────────────────────────────────┐
│      process_parser.py (Main)       │
└──────────────┬───────────────────────┘
               │
       ┌───────┴────────┐
       │  Input Router  │ (detect format, route to handler)
       └───┬────────┬───┴─────┬────────┐
           │        │         │        │
      ┌────▼───┐ ┌─▼────┐ ┌──▼───┐ ┌─▼─────┐
      │ Text   │ │ URL  │ │Image │ │Trans- │
      │Handler │ │Handler│ │Handler│ │cript │
      └────┬───┘ └─┬────┘ └──┬───┘ └─┬─────┘
           │       │         │       │
           └───────┴─────┬───┴───────┘
                         │
                   ┌─────▼──────┐
                   │  Process   │
                   │ Normalizer │
                   └─────┬──────┘
                         │
                   ┌─────▼──────┐
                   │   JSON     │
                   │ Generator  │
                   └────────────┘
```

**Key Classes/Functions:**

```python
# parser_core.py
class ProcessParser:
    def __init__(self, input_source, input_type=None):
        self.source = input_source
        self.type = input_type or self._detect_type()

    def parse(self):
        handler = self._get_handler()
        raw_data = handler.parse()
        normalized = self._normalize(raw_data)
        return self._to_json(normalized)

# handlers/text_handler.py
class TextHandler:
    def parse(self, content):
        # Extract steps using regex patterns
        # Identify roles, durations, decisions
        # Return structured dict

# handlers/url_handler.py
class URLHandler:
    def parse(self, url):
        # Fetch HTML content
        # Convert to text (BeautifulSoup-style parsing)
        # Delegate to TextHandler

# handlers/image_handler.py (optional dependencies)
class ImageHandler:
    def parse(self, image_path):
        # OCR with pytesseract
        # Clean OCR output
        # Delegate to TextHandler
        # Graceful fallback if OCR unavailable

# handlers/transcript_handler.py
class TranscriptHandler:
    def parse(self, transcript):
        # NLP parsing for conversation structure
        # Extract actions, actors, timing
        # Return structured dict
```

**Dependencies:**
- **Core:** `json`, `argparse`, `re`, `urllib.request`, `html.parser`
- **Optional:** `pytesseract`, `Pillow` (OCR)
- **Fallback:** Skip image parsing or prompt for manual text extraction

**CLI Interface:**

```bash
python process_parser.py --input FILE_OR_DIR [--url URL] [--type TYPE] [--output FILE] [--format json|yaml] [--verbose]

# Examples:
python process_parser.py --input process.md --output process.json
python process_parser.py --url "https://confluence.company.com/process" --output process.json
python process_parser.py --input sketch.png --type image --output process.json
python process_parser.py --input transcript.txt --type transcript --output process.json
```

---

### 2. process_mapper.py

**Purpose:** Generate visual process diagrams in multiple formats

**Architecture:**

```
┌──────────────────────────────────────┐
│      process_mapper.py (Main)        │
└──────────────┬───────────────────────┘
               │
       ┌───────▼────────┐
       │  JSON Loader   │ (validate schema, load process)
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │ Diagram Type   │ (flowchart, swimlane, BPMN)
       │   Selector     │
       └───┬────────┬───┴───────┐
           │        │           │
      ┌────▼───┐ ┌─▼────┐ ┌────▼───┐
      │Flowchart│ │Swimlane│ │ BPMN │
      │Generator│ │Generator│ │Generator│
      └────┬───┘ └─┬────┘ └────┬───┘
           │       │           │
           └───────┴─────┬─────┘
                         │
                   ┌─────▼──────┐
                   │  Mermaid   │
                   │  Renderer  │
                   └─────┬──────┘
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
  ┌────▼───┐      ┌──────▼──────┐   ┌────▼────┐
  │  SVG   │      │     PNG     │   │  HTML   │
  │Exporter│      │  Exporter   │   │Exporter │
  └────────┘      └─────────────┘   └─────────┘
```

**Key Classes/Functions:**

```python
# mapper_core.py
class ProcessMapper:
    def __init__(self, process_json, diagram_type, output_format):
        self.process = self._load_and_validate(process_json)
        self.type = diagram_type
        self.format = output_format

    def generate(self):
        generator = self._get_generator()
        mermaid = generator.to_mermaid()
        return self._export(mermaid)

# generators/flowchart_generator.py
class FlowchartGenerator:
    def to_mermaid(self, process):
        # Generate Mermaid flowchart syntax
        # graph TD format
        # Handle decisions, branches, loops

# generators/swimlane_generator.py
class SwimlaneGenerator:
    def to_mermaid(self, process):
        # Generate Mermaid swimlane (sequenceDiagram or graph with subgraphs)
        # Group by role
        # Show handoffs between lanes

# generators/bpmn_generator.py
class BPMNGenerator:
    def to_mermaid(self, process):
        # Generate BPMN-style Mermaid diagram
        # Use proper BPMN notation (events, tasks, gateways)

# exporters/svg_exporter.py
class SVGExporter:
    def export(self, mermaid_syntax):
        # Use mermaid-cli if available
        # Fallback: return Mermaid markdown with instructions
```

**Dependencies:**
- **Core:** `json`, `argparse`
- **Optional:** `mermaid-cli` (npm package for SVG/PNG rendering)
- **Fallback:** Mermaid markdown output (users render themselves)

**CLI Interface:**

```bash
python process_mapper.py --input process.json --type TYPE --format FORMAT --output FILE [--theme THEME] [--complexity LEVEL]

# Examples:
python process_mapper.py --input process.json --type flowchart --format mermaid --output diagram.md
python process_mapper.py --input process.json --type swimlane --format svg --output diagram.svg
python process_mapper.py --input process.json --type bpmn --format html --output diagram.html
```

---

### 3. gap_analyzer.py

**Purpose:** Identify missing information and problems in process definition

**Architecture:**

```
┌──────────────────────────────────────┐
│      gap_analyzer.py (Main)          │
└──────────────┬───────────────────────┘
               │
       ┌───────▼────────┐
       │  JSON Loader   │
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │   Gap Detector │ (run all checks)
       └───┬────────┬───┴───┬───┬───┬───┐
           │        │       │   │   │   │
      ┌────▼──┐ ┌──▼──┐ ┌──▼─┐│   │   │
      │Missing│ │Role │ │Dec-││   │   │
      │ Info  │ │Check│ │ision││   │   │
      └───────┘ └─────┘ └────┘│   │   │
                       More checks...
                               │
                         ┌─────▼──────┐
                         │  Severity  │
                         │  Scorer    │
                         └─────┬──────┘
                               │
                         ┌─────▼──────┐
                         │  Question  │
                         │ Generator  │
                         └─────┬──────┘
                               │
                         ┌─────▼──────┐
                         │   Report   │
                         │ Formatter  │
                         └────────────┘
```

**Gap Detection Rules:**

```python
# checkers/missing_info_checker.py
def check_missing_info(process):
    gaps = []
    for step in process['steps']:
        if not step.get('role'):
            gaps.append({
                'type': 'undefined_role',
                'severity': 'high',
                'step_id': step['id'],
                'description': f"Step '{step['name']}' has no assigned role",
                'impact': 'Unclear accountability',
                'suggested_questions': [
                    f"Who is responsible for {step['name']}?",
                    f"Which team owns this step?"
                ]
            })
        if not step.get('duration_minutes'):
            gaps.append({
                'type': 'missing_info',
                'severity': 'medium',
                'step_id': step['id'],
                'description': f"Step '{step['name']}' has no duration estimate",
                'impact': 'Cannot calculate cycle time',
                'suggested_questions': [
                    f"How long does {step['name']} typically take?",
                    f"What is the SLA for this step?"
                ]
            })
    return gaps

# Severity scoring algorithm
def calculate_severity(gap_type, step_importance):
    # Critical: Process cannot execute
    # High: Process will likely fail or produce poor results
    # Medium: Process may be inefficient or unclear
    # Low: Minor improvements or clarifications
```

**CLI Interface:**

```bash
python gap_analyzer.py --input process.json --output gaps.md [--format json|markdown|html] [--severity LEVEL] [--questions]

# Examples:
python gap_analyzer.py --input process.json --output gaps.md
python gap_analyzer.py --input process.json --severity high --output critical-gaps.json
python gap_analyzer.py --input process.json --questions --output questions.md
```

---

### 4. efficiency_analyzer.py

**Purpose:** Calculate process efficiency metrics and identify bottlenecks

**Architecture:**

```
┌──────────────────────────────────────┐
│   efficiency_analyzer.py (Main)      │
└──────────────┬───────────────────────┘
               │
       ┌───────▼────────┐
       │  JSON Loader   │
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │ Metrics Engine │
       └───┬────────┬───┴───┬────┐
           │        │       │    │
      ┌────▼───┐ ┌─▼────┐ ┌▼──┐ │
      │ Time   │ │Waste │ │Bot-││
      │Metrics │ │Analysis│ │tleneck││
      └────────┘ └──────┘ └───┘│
                         More analyzers...
                               │
                         ┌─────▼──────┐
                         │Recommendation│
                         │  Generator │
                         └─────┬──────┘
                               │
                         ┌─────▼──────┐
                         │   Report   │
                         │ Formatter  │
                         └────────────┘
```

**Metrics Calculations:**

```python
# metrics/time_metrics.py
def calculate_cycle_time(process):
    # Sum of all step durations (sequential)
    # Account for parallel steps (max duration)
    total_minutes = 0
    for step in process['steps']:
        if not step.get('parallel_steps'):
            total_minutes += step.get('duration_minutes', 0)
        else:
            # Parallel steps: use max duration
            parallel_durations = [
                s.get('duration_minutes', 0)
                for s in process['steps']
                if s['id'] in step['parallel_steps']
            ]
            total_minutes += max(parallel_durations) if parallel_durations else 0
    return total_minutes

def calculate_process_efficiency(processing_time, cycle_time):
    # Efficiency = Processing Time / Cycle Time
    # High efficiency = less waiting, more value-added work
    if cycle_time == 0:
        return 0
    return (processing_time / cycle_time) * 100

# metrics/waste_analysis.py
def identify_waste(process):
    # Lean 7 Wastes
    waste = {
        'waiting': calculate_wait_time(process),
        'transportation': count_handoffs(process),
        'motion': calculate_context_switches(process),
        'defects': identify_rework_loops(process),
        'overprocessing': identify_unnecessary_steps(process),
        'overproduction': identify_early_work(process),
        'inventory': calculate_wip(process)
    }
    return waste

# metrics/bottleneck_detection.py
def identify_bottlenecks(process):
    bottlenecks = []
    avg_duration = mean([s.get('duration_minutes', 0) for s in process['steps']])

    for step in process['steps']:
        duration = step.get('duration_minutes', 0)
        handoffs = len(step.get('handoffs', []))

        # Bottleneck criteria
        if duration > avg_duration * 2:
            bottlenecks.append({
                'step_id': step['id'],
                'reason': 'long_duration',
                'severity': 'high',
                'recommendation': 'Consider parallelization or automation'
            })
        if handoffs > 2:
            bottlenecks.append({
                'step_id': step['id'],
                'reason': 'too_many_handoffs',
                'severity': 'medium',
                'recommendation': 'Reduce handoffs or consolidate ownership'
            })

    return sorted(bottlenecks, key=lambda x: x['severity'], reverse=True)
```

**CLI Interface:**

```bash
python efficiency_analyzer.py --input process.json --output metrics.json [--format json|markdown|csv|html] [--historical FILE]

# Examples:
python efficiency_analyzer.py --input process.json --output metrics.json
python efficiency_analyzer.py --input process.json --historical historical.csv --output metrics.md
python efficiency_analyzer.py --input process.json --format html --output dashboard.html
```

---

### 5. metrics_builder.py

**Purpose:** Define success metrics and KPIs for process

**Architecture:** Similar to efficiency_analyzer.py but focuses on KPI definition vs calculation

**CLI Interface:**

```bash
python metrics_builder.py --input process.json --output metrics-plan.md [--format json|markdown|yaml] [--objectives FILE] [--focus AREA]
```

---

### 6. process_comparator.py

**Purpose:** Compare as-is vs to-be processes

**Architecture:**

```
┌──────────────────────────────────────┐
│   process_comparator.py (Main)       │
└──────────────┬───────────────────────┘
               │
       ┌───────▼────────┐
       │ Load 2 Processes│
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │   Diff Engine  │
       └───┬────────┬───┴──────┐
           │        │          │
      ┌────▼───┐ ┌─▼────┐ ┌───▼──┐
      │ Added  │ │Modified│ │Removed│
      │ Steps  │ │ Steps  │ │ Steps │
      └────┬───┘ └─┬────┘ └───┬──┘
           │       │          │
           └───────┴─────┬────┘
                         │
                   ┌─────▼──────┐
                   │   Impact   │
                   │  Analyzer  │
                   └─────┬──────┘
                         │
                   ┌─────▼──────┐
                   │   Report   │
                   │ Generator  │
                   └────────────┘
```

**CLI Interface:**

```bash
python process_comparator.py --current as-is.json --proposed to-be.json --output comparison.md [--format json|markdown|html] [--impact]
```

---

### 7. improvement_prioritizer.py

**Purpose:** Prioritize process improvements using RICE framework

**Architecture:**

```
┌──────────────────────────────────────┐
│  improvement_prioritizer.py (Main)   │
└──────────────┬───────────────────────┘
               │
       ┌───────▼────────┐
       │ Load Gap + Metrics│
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │  Improvement   │
       │  Generator     │
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │ RICE Calculator│
       └───┬────────────┘
           │
      ┌────▼───────────┐
      │  Categorizer   │ (quick wins, big bets, fill-ins)
      └───┬────────────┘
          │
      ┌───▼────────────┐
      │   Roadmap      │
      │   Generator    │
      └────────────────┘
```

**RICE Calculation:**

```python
def calculate_rice(improvement):
    reach = improvement['reach']  # Number of process executions affected
    impact = improvement['impact']  # 3=Massive, 2=High, 1=Medium, 0.5=Low
    confidence = improvement['confidence']  # 1.0=High, 0.8=Medium, 0.5=Low
    effort = improvement['effort']  # Person-weeks

    rice_score = (reach * impact * confidence) / effort
    return rice_score

def categorize_improvement(rice_score, effort):
    if rice_score > 10:
        return 'quick_win' if effort < 2 else 'big_bet'
    elif rice_score > 5:
        return 'big_bet'
    elif rice_score > 2:
        return 'fill_in'
    else:
        return 'money_pit'
```

**CLI Interface:**

```bash
python improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --output priorities.md [--format json|markdown|csv] [--priorities FILE] [--threshold SCORE]
```

---

## Integration Architecture

### Cross-Tool Workflows

**Workflow 1: Process Discovery**

```bash
# Step 1: Parse Confluence page
python process_parser.py --url "https://company.com/process" --output process.json

# Step 2: Generate swimlane diagram
python process_mapper.py --input process.json --type swimlane --format svg --output diagram.svg

# Step 3: Identify gaps
python gap_analyzer.py --input process.json --output gaps.md
```

**Workflow 2: Process Optimization**

```bash
# Step 1: Analyze efficiency
python efficiency_analyzer.py --input process.json --output metrics.json

# Step 2: Prioritize improvements
python improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --output priorities.md

# Step 3: Compare as-is vs to-be
# (after manually creating improved process)
python process_comparator.py --current as-is.json --proposed to-be.json --output comparison.md
```

**Workflow 3: Cross-Skill Integration**

```bash
# Step 1: Generate improvement CSV
python improvement_prioritizer.py --gaps gaps.json --metrics metrics.json --format csv --output improvements.csv

# Step 2: Use product-manager RICE prioritizer
python ../product-manager-toolkit/scripts/rice_prioritizer.py --input improvements.csv --output prioritized.csv

# Step 3: Generate user stories for automation
python ../agile-product-owner/scripts/user_story_generator.py --input prioritized.csv --output stories.md
```

### Data Flow Diagram

```
┌─────────────┐
│   Input     │
│   Source    │
└──────┬──────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  process_    │────→│  process_    │────→│     SVG/     │
│  parser.py   │     │  mapper.py   │     │   PNG File   │
└──────┬───────┘     └──────────────┘     └──────────────┘
       │
       │ process.json
       │
       ├──────────────→┌──────────────┐
       │               │     gap_     │
       │               │  analyzer.py │
       │               └──────┬───────┘
       │                      │ gaps.json
       │                      │
       ├──────────────→┌──────▼───────┐
       │               │ efficiency_  │
       │               │analyzer.py   │
       │               └──────┬───────┘
       │                      │ metrics.json
       │                      │
       └──────────────→┌──────▼───────┐
                       │improvement_  │
                       │prioritizer.py│
                       └──────────────┘
```

---

## Error Handling Strategy

### Graceful Degradation

```python
# Example: Optional OCR dependency
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

def parse_image(image_path):
    if not OCR_AVAILABLE:
        print("⚠️  OCR not available (pip install pytesseract Pillow)")
        print("📝 Please extract text manually and save as .txt file")
        return None

    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        print("📝 Please extract text manually")
        return None
```

### Input Validation

```python
def validate_process_json(process):
    errors = []

    # Required fields
    if 'process_name' not in process:
        errors.append("Missing required field: process_name")
    if 'steps' not in process or not process['steps']:
        errors.append("Process must have at least one step")

    # Schema validation
    for step in process.get('steps', []):
        if 'id' not in step:
            errors.append(f"Step missing required field: id")
        if 'name' not in step:
            errors.append(f"Step {step.get('id')} missing required field: name")

    if errors:
        raise ValueError(f"Invalid process JSON: {', '.join(errors)}")

    return True
```

### User-Friendly Error Messages

```python
# Good error messages
✅ "Invalid JSON file: process.json (line 42: missing comma)"
✅ "URL not accessible: https://company.com/process (404 Not Found)"
✅ "Image parsing failed: sketch.png (OCR not installed)"

# Bad error messages
❌ "JSONDecodeError: Expecting ',' delimiter"
❌ "HTTPError: 404"
❌ "ModuleNotFoundError: No module named 'pytesseract'"
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_process_parser.py
def test_parse_text_file():
    parser = ProcessParser('sample-process.txt', 'text')
    result = parser.parse()
    assert result['process_name'] == 'Sample Process'
    assert len(result['steps']) > 0
    assert result['steps'][0]['name'] is not None

def test_parse_invalid_input():
    parser = ProcessParser('invalid.txt', 'text')
    with pytest.raises(ValueError):
        parser.parse()
```

### Integration Tests

```bash
# tests/integration_test.sh
#!/bin/bash

# Test end-to-end workflow
python process_parser.py --input test-process.txt --output /tmp/process.json
python process_mapper.py --input /tmp/process.json --type swimlane --format mermaid --output /tmp/diagram.md
python gap_analyzer.py --input /tmp/process.json --output /tmp/gaps.md

# Verify outputs
if [ -f /tmp/process.json ] && [ -f /tmp/diagram.md ] && [ -f /tmp/gaps.md ]; then
    echo "✅ Integration test passed"
else
    echo "❌ Integration test failed"
    exit 1
fi
```

---

## Performance Considerations

### Optimization Targets

- **Parse time**: <5 seconds for 100-line text document
- **Map generation**: <2 seconds for 50-step process
- **Gap analysis**: <1 second for any process
- **Efficiency analysis**: <3 seconds for 100-step process

### Scaling Strategy

- **Small processes** (1-20 steps): Optimal performance target
- **Medium processes** (21-50 steps): Still performant
- **Large processes** (51-100 steps): Acceptable performance
- **Very large processes** (100+ steps): May require optimization

**If performance issues arise:**
- Implement caching for repeated operations
- Use streaming JSON parsing for large files
- Add --limit flag to process subset of steps

---

## Security Considerations

### Input Sanitization

```python
# Sanitize URLs
def sanitize_url(url):
    # Block file:// and javascript: protocols
    if url.startswith(('file://', 'javascript:')):
        raise ValueError("Invalid URL protocol")
    return url

# Sanitize file paths
def sanitize_path(path):
    # Prevent path traversal
    if '..' in path:
        raise ValueError("Invalid file path (contains '..')")
    return os.path.abspath(path)
```

### No Remote Code Execution

- Never use `eval()` or `exec()` on user input
- Use JSON parsing only (no YAML which supports arbitrary objects)
- Subprocess calls only for known safe commands (mermaid-cli)

---

## Deployment & Distribution

### Installation

```bash
# No installation needed (standard library only)
cd skills/product-team/business-analyst-toolkit/
python scripts/process_parser.py --help

# Optional: Install enhanced features
pip install pytesseract Pillow  # OCR support
npm install -g @mermaid-js/mermaid-cli  # SVG/PNG rendering
```

### Packaging (Future)

```bash
# Optional: Create Python package
pip install business-analyst-toolkit

# Command-line interface
batools parse --input process.md --output process.json
batools map --input process.json --type swimlane --output diagram.svg
```

---

## Documentation Architecture

### SKILL.md Structure

```markdown
# Business Analyst Toolkit

## Quick Start (Copy-paste commands)
## Core Workflows (3+ end-to-end examples)
## Python Tools (7 tools documented)
## Reference Documentation (links to 3 reference files)
## Integration Examples (cross-skill workflows)
## Troubleshooting (common issues + solutions)
```

### Reference Documents

1. **frameworks.md** (500+ lines)
   - BPMN, swimlanes, VSM, Lean, Six Sigma
2. **templates.md** (400+ lines)
   - Process docs, RACI, charters, proposals
3. **tools.md** (300+ lines)
   - Lucidchart, Miro, Confluence, Jira integration

---

## Success Metrics (Architecture Quality)

**Code Quality:**
- ✅ 100% of tools support --help flag
- ✅ 100% of tools handle errors gracefully
- ✅ 0 external dependencies for core features
- ✅ <1000 lines per tool (maintainability)

**Performance:**
- ✅ Parse 100-line doc in <5 seconds
- ✅ Generate diagram in <2 seconds
- ✅ Gap analysis in <1 second

**Extensibility:**
- ✅ Add new parser (URL, text, image, transcript, **NEW**)
- ✅ Add new diagram type (flowchart, swimlane, BPMN, **NEW**)
- ✅ Add new metric (cycle time, efficiency, **NEW**)

---

## Next Steps: Implementation Roadmap

**Week 1:**
1. Implement process_parser.py (text + URL support)
2. Define JSON schema (v1.0)
3. Create basic unit tests

**Week 2:**
4. Implement process_mapper.py (Mermaid generation)
5. Implement gap_analyzer.py
6. Add image parsing (OCR)

**Week 3:**
7. Implement efficiency_analyzer.py
8. Implement metrics_builder.py
9. Create reference documentation

**Week 4:**
10. Implement process_comparator.py
11. Implement improvement_prioritizer.py
12. Create asset templates

**Week 5:**
13. Create cs-business-analyst agent
14. Test integration workflows
15. Update documentation

**Week 6:**
16. Comprehensive testing
17. Code review
18. Documentation polish

---

**Architecture Status:** ✅ DESIGN COMPLETE
**Next Action:** Begin implementation (process_parser.py)
**Created By:** Architecture design workflow
**Reviewed By:** (pending)
**Last Updated:** November 20, 2025
