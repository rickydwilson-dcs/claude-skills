# Code Reviewer Scripts Implementation Plan

**Session:** 2025-12-02_code-reviewer-implementation-plan
**Status:** Ready for Implementation
**Backlog Reference:** Priority 1: Code Quality & Review (3 scripts)

---

## Executive Summary

This plan details the implementation of three placeholder Python scripts for the code-reviewer skill. All implementations use **Python standard library only** (no pip dependencies).

| Script | Current State | Target Size | Priority |
|--------|---------------|-------------|----------|
| `code_quality_checker.py` | 160 lines (placeholder) | ~500 lines | HIGH |
| `pr_analyzer.py` | 140 lines (placeholder) | ~400 lines | HIGH |
| `review_report_generator.py` | 140 lines (placeholder) | ~350 lines | MEDIUM |

**Total Effort:** ~1,250 lines of production code
**Reference Implementation:** `sprint_metrics_calculator.py` (476 lines) - shows expected quality level

---

## Current State Analysis

### What Exists (Placeholder Pattern)

All three scripts share identical boilerplate:

```python
class [ScriptName]:
    def __init__(self, target_path: str, verbose: bool = False)
    def run(self) -> Dict
    def validate_target(self)
    def analyze(self)  # Empty stub - just sets status='success'
    def generate_report(self)  # Generic template output
```

**What's Implemented (~10%):**
- CLI argument parsing (complete)
- Basic file path validation (complete)
- Report generation skeleton (template only)
- Output formatting structure (JSON/CSV/text)

**What's Missing (~90%):**
- No actual code analysis logic
- No file parsing or scanning
- No anti-pattern detection
- No quality metrics calculation
- No language-specific checks
- No severity scoring

### Reference Documentation (Excellent Quality)

The `references/` folder contains production-ready guidance:
- **common_antipatterns.md** (724 lines) - 50+ anti-patterns across 6 languages
- **coding_standards.md** - Language-specific standards with examples
- **code_review_checklist.md** - 300+ review items with severity

---

## Architecture Design

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    PatternRegistry                          │
│  - 100+ detection patterns organized by category            │
│  - Language-specific pattern activation                     │
│  - Severity classification (CRITICAL/HIGH/MEDIUM/LOW)       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ code_quality  │   │   pr_analyzer   │   │ review_report   │
│ _checker.py   │   │      .py        │   │ _generator.py   │
├───────────────┤   ├─────────────────┤   ├─────────────────┤
│ - File scan   │   │ - Git diff      │   │ - Aggregate     │
│ - AST parse   │   │ - Change impact │   │ - Categorize    │
│ - Regex match │   │ - Risk assess   │   │ - Format output │
│ - Score calc  │   │ - Time estimate │   │ - Markdown/JSON │
└───────────────┘   └─────────────────┘   └─────────────────┘
```

### Shared Data Structures

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional
import re

class Severity(Enum):
    CRITICAL = 4  # Block merge - security vulnerabilities, data loss
    HIGH = 3      # Fix before merge - major bugs, significant debt
    MEDIUM = 2    # Plan to fix - code smells, minor issues
    LOW = 1       # Consider fixing - style, minor improvements

@dataclass
class Pattern:
    id: str                    # e.g., "SEC-001"
    name: str                  # e.g., "SQL Injection"
    regex: str                 # Detection pattern
    severity: Severity
    languages: List[str]       # ["all"] or ["python", "typescript"]
    category: str              # "security", "performance", etc.
    message: str               # User-facing description
    suggestion: str            # How to fix
    compiled: re.Pattern = None

@dataclass
class Finding:
    pattern_id: str
    file_path: str
    line_number: int
    line_content: str
    severity: Severity
    category: str
    message: str
    suggestion: str
```

---

## Script 1: code_quality_checker.py

### Purpose

Static analysis tool that scans source files for anti-patterns, code smells, and quality issues across multiple languages.

### Features to Implement

| Feature | Method | Standard Library |
|---------|--------|------------------|
| Multi-language file discovery | `discover_files()` | `pathlib`, `os` |
| Language detection | `detect_language()` | Extension mapping |
| Python AST analysis | `analyze_python_ast()` | `ast` |
| Regex pattern matching | `match_patterns()` | `re` |
| Cyclomatic complexity | `calculate_complexity()` | AST node counting |
| Code duplication | `detect_duplication()` | Content hashing |
| Quality scoring | `calculate_score()` | Weighted formula |

### Detection Patterns by Category

#### Security Patterns (20 patterns) - CRITICAL Priority

| ID | Pattern | Regex | Severity |
|----|---------|-------|----------|
| SEC-001 | SQL Injection | `".*SELECT.*\$\{` | CRITICAL |
| SEC-002 | SQL Concat | `"SELECT.*"\s*\+\s*\w+` | CRITICAL |
| SEC-003 | Command Injection | `exec\(.*\$\{\|subprocess.*shell=True` | CRITICAL |
| SEC-004 | Hardcoded Password | `password\s*=\s*['"][^'"]+['"]` | CRITICAL |
| SEC-005 | Hardcoded API Key | `(api[_-]?key)\s*[:=]\s*['"][^'"]+` | CRITICAL |
| SEC-006 | AWS Credentials | `AKIA[0-9A-Z]{16}` | CRITICAL |
| SEC-007 | Private Key | `-----BEGIN.*PRIVATE KEY-----` | CRITICAL |
| SEC-008 | eval() Usage | `\beval\s*\(` | CRITICAL |
| SEC-009 | innerHTML XSS | `\.innerHTML\s*=.*\$\{` | HIGH |
| SEC-010 | document.write | `document\.write\(` | HIGH |

#### Python-Specific Patterns (15 patterns) - AST-based

| ID | Pattern | Detection Method | Severity |
|----|---------|-----------------|----------|
| PY-001 | Mutable Default Arg | AST: default is List/Dict/Set | HIGH |
| PY-002 | Bare Except | AST: ExceptHandler with type=None | HIGH |
| PY-003 | Except Pass | Regex: `except.*:\s*pass` | HIGH |
| PY-004 | Broad Exception | Regex: `except\s+Exception\s*:` | MEDIUM |
| PY-005 | Using 'is' for Value | AST: Is with Constant | HIGH |
| PY-006 | Missing Context Manager | AST: open() not in with | MEDIUM |
| PY-007 | Import Star | Regex: `from\s+\w+\s+import\s+\*` | MEDIUM |
| PY-008 | Global Variable | Regex: `\bglobal\s+\w+` | MEDIUM |
| PY-009 | No Type Hints | AST: FunctionDef without returns | LOW |
| PY-010 | Print Statement | Regex: `\bprint\s*\(` | LOW |

#### TypeScript/JavaScript Patterns (18 patterns)

| ID | Pattern | Regex | Severity |
|----|---------|-------|----------|
| TS-001 | Using 'any' Type | `: any\b` | HIGH |
| TS-002 | Any in Generic | `<any>\|any\[\]` | HIGH |
| TS-003 | Type Assertion to Any | `as any\b` | HIGH |
| TS-004 | Empty Catch | `catch\s*\([^)]*\)\s*\{\s*\}` | HIGH |
| TS-005 | Ignoring Promise | `.catch\(\(\)\s*=>\s*\{\s*\}\)` | HIGH |
| TS-006 | Props Mutation | `props\.\w+\s*=` | CRITICAL |
| TS-007 | Var Usage | `\bvar\s+` | MEDIUM |
| TS-008 | == Instead of === | `[^!=!]==[^=]` | MEDIUM |
| TS-009 | Console Log | `console\.(log\|debug)\(` | LOW |

#### Go Patterns (10 patterns)

| ID | Pattern | Regex | Severity |
|----|---------|-------|----------|
| GO-001 | Ignored Error | `,\s*_\s*:?=\s*\w+\(` | HIGH |
| GO-002 | Missing Defer | `os\.Open` without defer | MEDIUM |
| GO-003 | Goroutine Leak | `go\s+func.*for\s*\{` | HIGH |
| GO-004 | Panic in Library | `\bpanic\(` | HIGH |

#### General Patterns (12 patterns)

| ID | Pattern | Regex | Severity |
|----|---------|-------|----------|
| GEN-001 | Magic Numbers | `(?<![a-zA-Z_])\d{3,}(?![a-zA-Z_\d.])` | MEDIUM |
| GEN-002 | Long Line | Line > 120 chars | LOW |
| GEN-003 | Deep Nesting | 4+ indentation levels | MEDIUM |
| GEN-004 | TODO/FIXME | `TODO\|FIXME\|HACK\|XXX` | LOW |
| GEN-005 | Long Function | Function > 50 lines | MEDIUM |
| GEN-006 | God Class | Class > 300 lines or > 20 methods | HIGH |

### Method Signatures

```python
class CodeQualityChecker:
    def __init__(self, target_path: str, language: str = 'auto',
                 min_severity: str = 'LOW', verbose: bool = False):
        self.target_path = Path(target_path)
        self.language = language
        self.min_severity = Severity[min_severity]
        self.verbose = verbose
        self.patterns = self._load_patterns()
        self.findings: List[Finding] = []

    # File discovery
    def discover_files(self) -> List[Path]
    def detect_language(self, file_path: Path) -> str
    def read_file_safe(self, file_path: Path) -> Optional[str]

    # Pattern matching
    def _load_patterns(self) -> Dict[str, List[Pattern]]
    def match_patterns(self, content: str, language: str, file_path: str) -> List[Finding]

    # Python-specific (AST)
    def analyze_python_ast(self, content: str, file_path: str) -> List[Finding]
    def _check_mutable_defaults(self, tree: ast.AST) -> List[Finding]
    def _check_bare_excepts(self, tree: ast.AST) -> List[Finding]
    def _check_missing_context_managers(self, tree: ast.AST) -> List[Finding]

    # Metrics
    def calculate_complexity(self, content: str, language: str) -> int
    def detect_long_functions(self, content: str, language: str) -> List[Finding]
    def detect_deep_nesting(self, lines: List[str]) -> List[Finding]

    # Scoring
    def calculate_quality_score(self) -> Dict
    def get_grade(self, score: int) -> str

    # Output
    def run(self) -> Dict
    def generate_report(self) -> None
    def format_json(self) -> str
    def format_csv(self) -> str
    def format_text(self) -> str
```

### Quality Score Formula

```python
def calculate_quality_score(self) -> Dict:
    """Calculate weighted quality score (0-100)"""
    critical_count = sum(1 for f in self.findings if f.severity == Severity.CRITICAL)
    high_count = sum(1 for f in self.findings if f.severity == Severity.HIGH)
    medium_count = sum(1 for f in self.findings if f.severity == Severity.MEDIUM)

    # Penalty system
    penalty = (critical_count * 20) + (high_count * 10) + (medium_count * 3)
    score = max(0, min(100, 100 - penalty))

    return {
        'score': score,
        'grade': self.get_grade(score),
        'breakdown': {
            'critical': critical_count,
            'high': high_count,
            'medium': medium_count,
            'low': sum(1 for f in self.findings if f.severity == Severity.LOW)
        }
    }

def get_grade(self, score: int) -> str:
    if score >= 90: return 'A'
    if score >= 80: return 'B'
    if score >= 70: return 'C'
    if score >= 60: return 'D'
    return 'F'
```

### Output Structure

```json
{
  "status": "success",
  "target": "./src",
  "analyzed_at": "2025-12-02T10:00:00",
  "files_analyzed": 15,
  "quality_score": {
    "score": 78,
    "grade": "B",
    "breakdown": {
      "critical": 0,
      "high": 3,
      "medium": 12,
      "low": 8
    }
  },
  "findings": [
    {
      "file": "src/user_service.py",
      "line": 45,
      "severity": "HIGH",
      "category": "anti-pattern",
      "pattern_id": "PY-001",
      "message": "Mutable default argument: items=[]",
      "suggestion": "Use None as default and initialize inside function"
    }
  ],
  "recommendations": [
    "Fix 3 high-severity issues before merging",
    "Add type hints to functions lacking return annotations"
  ]
}
```

---

## Script 2: pr_analyzer.py

### Purpose

Analyze pull request changes by examining git diff output. Calculate metrics, identify risk areas, and estimate review effort.

### Features to Implement

| Feature | Method | Standard Library |
|---------|--------|------------------|
| Git diff parsing | `get_diff_output()` | `subprocess` |
| Change metrics | `count_changes()` | Line counting |
| File categorization | `categorize_files()` | Path pattern matching |
| Risk assessment | `identify_risks()` | Pattern matching |
| Security scan of changes | `scan_security()` | Regex on diff |
| Review time estimation | `estimate_review_time()` | Formula |

### Risk Detection Patterns

```python
SECURITY_SENSITIVE_PATHS = [
    r'auth|authentication|login|password',
    r'payment|billing|stripe|paypal',
    r'crypto|encrypt|decrypt|hash',
    r'secret|token|credential|api.?key',
]

BREAKING_CHANGE_PATTERNS = [
    (r'export\s+(interface|type|class)', 'API/Interface change'),
    (r'ALTER\s+TABLE|DROP\s+COLUMN', 'Database schema change'),
    (r'@deprecated', 'Deprecation added'),
]

CONFIG_FILES = [
    r'package\.json|requirements\.txt|go\.mod',
    r'\.env|config\.(yaml|yml|json)',
    r'Dockerfile|docker-compose',
]
```

### Method Signatures

```python
class PrAnalyzer:
    def __init__(self, target_path: str, base_branch: str = 'main',
                 head_branch: str = 'HEAD', verbose: bool = False):
        self.target_path = Path(target_path)
        self.base_branch = base_branch
        self.head_branch = head_branch
        self.verbose = verbose

    # Git operations
    def get_diff_output(self) -> str
    def get_changed_files(self) -> List[str]
    def get_commit_messages(self) -> List[str]

    # Parsing
    def parse_diff(self, diff_output: str) -> Dict
    def count_changes(self) -> Dict[str, int]

    # Analysis
    def categorize_files(self, files: List[str]) -> Dict[str, List[str]]
    def identify_risks(self, files: List[str]) -> List[Dict]
    def scan_security(self, diff_output: str) -> List[Finding]
    def detect_breaking_changes(self, diff_output: str) -> List[Dict]

    # Estimation
    def calculate_complexity_score(self) -> int
    def estimate_review_time(self) -> int
    def determine_priority(self) -> str

    # Output
    def run(self) -> Dict
    def generate_report(self) -> None
```

### Review Time Formula

```python
def estimate_review_time(self) -> int:
    """Estimate review time in minutes"""
    changes = self.count_changes()
    files = len(self.get_changed_files())
    risks = len(self.identify_risks(self.get_changed_files()))

    # Base: 2 min per file + 1 min per 50 lines
    base_time = (files * 2) + (changes['total'] // 50)

    # Risk multiplier
    if risks > 3:
        base_time *= 1.5
    elif risks > 0:
        base_time *= 1.2

    return max(10, min(120, int(base_time)))
```

### Output Structure

```json
{
  "status": "success",
  "pr_info": {
    "base_branch": "main",
    "head_branch": "feature/user-auth",
    "commits": 5
  },
  "summary": {
    "files_changed": 12,
    "lines_added": 245,
    "lines_removed": 87,
    "net_change": 158
  },
  "file_breakdown": {
    "source": ["src/auth.py", "src/user.py"],
    "test": ["tests/test_auth.py"],
    "config": ["config/settings.yaml"],
    "documentation": ["README.md"]
  },
  "risk_assessment": {
    "risk_score": 7,
    "risk_level": "medium",
    "flags": [
      {"type": "security", "file": "src/auth.py", "reason": "Authentication logic modified"},
      {"type": "config", "file": "config/settings.yaml", "reason": "Configuration changed"}
    ]
  },
  "security_findings": [],
  "breaking_changes": [],
  "review_recommendation": {
    "priority": "high",
    "estimated_time_minutes": 45,
    "focus_areas": ["Authentication changes in src/auth.py"]
  }
}
```

---

## Script 3: review_report_generator.py

### Purpose

Generate comprehensive, human-readable review reports combining quality analysis with PR context. Produce actionable feedback with proper categorization.

### Features to Implement

| Feature | Method | Standard Library |
|---------|--------|------------------|
| Finding aggregation | `aggregate_findings()` | Data structures |
| Issue categorization | `categorize_by_severity()` | Enum sorting |
| Markdown generation | `format_markdown()` | String formatting |
| JSON output | `format_json()` | `json` |
| CSV output | `format_csv()` | `csv` |

### Issue Categories

| Category | Description | Action |
|----------|-------------|--------|
| **Blocking** | Security issues, critical bugs | Must fix before merge |
| **Major** | Performance, architecture, maintainability | Should fix before merge |
| **Minor** | Style, naming, comments | Consider fixing |
| **Nitpick** | Personal preferences | Optional |

### Method Signatures

```python
class ReviewReportGenerator:
    def __init__(self, findings: List[Finding] = None,
                 pr_metrics: Dict = None, output_format: str = 'markdown',
                 verbose: bool = False):
        self.findings = findings or []
        self.pr_metrics = pr_metrics or {}
        self.output_format = output_format
        self.verbose = verbose

    # Categorization
    def categorize_by_severity(self) -> Dict[str, List[Finding]]
    def categorize_by_file(self) -> Dict[str, List[Finding]]
    def prioritize_findings(self) -> List[Finding]

    # Content generation
    def generate_summary(self) -> str
    def generate_blocking_section(self) -> str
    def generate_major_section(self) -> str
    def generate_minor_section(self) -> str
    def generate_recommendations(self) -> List[str]
    def generate_positive_notes(self) -> List[str]

    # Formatting
    def format_markdown(self) -> str
    def format_json(self) -> str
    def format_csv(self) -> str
    def format_text(self) -> str

    # Output
    def run(self) -> str
    def write_report(self, output_path: str) -> None
```

### Markdown Template

```markdown
# Code Review Report

## Summary

| Metric | Value |
|--------|-------|
| Quality Score | 78/100 (B) |
| Files Analyzed | 12 |
| Total Findings | 23 |
| Critical Issues | 0 |
| High Issues | 3 |

## Blocking Issues (Must Fix)

> No blocking issues found.

## High Priority Issues (Should Fix)

### PY-001: Mutable Default Argument
- **File:** `src/user_service.py` (line 45)
- **Code:** `def add_item(item, items=[]):`
- **Fix:** Use `None` as default and initialize inside function

## Minor Issues (Consider)

- **GEN-004** `src/utils.py:34` - TODO comment without ticket reference

## Positive Notes

- Good test coverage on authentication module
- Consistent use of type hints

## Recommendations

1. Address 3 high-severity issues before merge
2. Add integration tests for new API endpoints

---
*Generated by code-reviewer skill*
```

---

## Implementation Phases

### Phase 1: code_quality_checker.py (Week 1)

**Day 1-2: Core Infrastructure**
- [ ] Create Severity enum and Finding/Pattern dataclasses
- [ ] Implement PatternRegistry with all detection patterns
- [ ] Implement LanguageDetector (extension mapping)
- [ ] File discovery with filtering

**Day 3-4: Detection Engine**
- [ ] Regex-based pattern matching for all languages
- [ ] Python AST analysis (mutable defaults, bare excepts, etc.)
- [ ] Line-based detection (long lines, deep nesting)
- [ ] Function/class length analysis

**Day 5: Scoring & Output**
- [ ] Quality score calculation with weighted formula
- [ ] JSON/CSV/text output formatters
- [ ] CLI interface with all options
- [ ] Testing with sample codebases

### Phase 2: pr_analyzer.py (Week 2)

**Day 1-2: Git Integration**
- [ ] subprocess calls for git diff, log
- [ ] Diff output parsing (hunks, files)
- [ ] Changed file extraction

**Day 3: Analysis**
- [ ] File categorization (source/test/config/docs)
- [ ] Risk pattern detection
- [ ] Security scan on diff content
- [ ] Breaking change detection

**Day 4: Estimation & Scoring**
- [ ] Complexity score calculation
- [ ] Review time estimation formula
- [ ] Priority determination

**Day 5: Output**
- [ ] JSON output structure
- [ ] CLI interface
- [ ] Integration testing

### Phase 3: review_report_generator.py (Week 2-3)

**Day 1-2: Aggregation**
- [ ] Finding collection from files/input
- [ ] Severity categorization
- [ ] File-based grouping

**Day 3-4: Report Generation**
- [ ] Markdown template implementation
- [ ] Section generators (blocking, major, minor)
- [ ] Recommendations engine
- [ ] Positive feedback detection

**Day 5: Finalization**
- [ ] JSON/CSV output formats
- [ ] CLI interface
- [ ] Documentation updates
- [ ] SKILL.md accuracy verification

---

## Testing Strategy

### Manual Testing

```bash
# Test code_quality_checker.py
python code_quality_checker.py --input ./skills/engineering-team --output json

# Test pr_analyzer.py
python pr_analyzer.py --input . --base main --head HEAD

# Test review_report_generator.py
python review_report_generator.py --input ./analysis.json --format markdown
```

### Validation Criteria

1. **--help works** for all scripts
2. **JSON output is valid** and parseable
3. **Findings are accurate** (no false positives on reference code)
4. **Score calculation is consistent**
5. **All languages detected correctly**

---

## Files Modified

| File | Action |
|------|--------|
| `skills/engineering-team/code-reviewer/scripts/code_quality_checker.py` | Rewrite |
| `skills/engineering-team/code-reviewer/scripts/pr_analyzer.py` | Rewrite |
| `skills/engineering-team/code-reviewer/scripts/review_report_generator.py` | Rewrite |
| `skills/engineering-team/code-reviewer/SKILL.md` | Update if needed |
| `BACKLOG.md` | Mark Priority 1 complete |

---

## Success Criteria

- [ ] All 3 scripts have substantive implementation (300-500 lines each)
- [ ] 50+ anti-patterns detectable across 6 languages
- [ ] Quality score calculation working with weighted formula
- [ ] All output formats (JSON, CSV, text, markdown) functional
- [ ] CLI matches existing patterns in repository
- [ ] No external dependencies (standard library only)
- [ ] Passes `--help` validation
- [ ] Accurate detection on test files

---

## Reference Files

| File | Purpose |
|------|---------|
| `skills/delivery-team/scrum-master/scripts/sprint_metrics_calculator.py` | Quality reference (476 lines) |
| `skills/engineering-team/code-reviewer/references/common_antipatterns.md` | Anti-pattern catalog (724 lines) |
| `skills/engineering-team/code-reviewer/references/coding_standards.md` | Language standards |
| `skills/engineering-team/code-reviewer/references/code_review_checklist.md` | Review checklist |

---

**Plan Created:** 2025-12-02
**Ready for Implementation:** Yes
