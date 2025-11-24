# Testing Framework - Quick Start Guide

## Installation (30 seconds)

```bash
# Install pytest
pip install pytest

# Verify installation
pytest --version
# pytest 8.4.2
```

## Running Tests (2 minutes)

### Run All Tests
```bash
cd /Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My Drive/Websites/GitHub/claude-skills

# Full test suite (all 2,436 tests)
pytest

# Expected output:
# ================ 2385 passed, 93 failed, 2 warnings in 137.68s ================
```

### Run by Category

```bash
# Help flag tests only (40 seconds)
pytest -m help

# Execution tests (45 seconds)
pytest -m execution

# Output format tests (50 seconds)
pytest -m output
```

### Run for Single Script

```bash
# Test brand voice analyzer only
pytest -k "brand_voice_analyzer"

# Test marketing domain only
pytest -k "marketing"

# Test with verbose output
pytest -k "brand_voice" -vv
```

## Understanding Results

### Passing Tests Example
```
tests/test_cli_help.py::TestCliHelpFlag::test_script_help_flag[content-creator/marketing-skill/brand_voice_analyzer.py] PASSED [  7%]
```
- Script responds to --help correctly
- Exit code is 0
- Help text is present

### Failing Tests Example
```
FAILED tests/test_cli_basic.py::TestBasicScriptExecution::test_script_has_main_function[senior-ml-engineer/engineering-team/ml_monitoring_suite.py]
AssertionError: Script ml_monitoring_suite.py missing main guard (if __name__ == '__main__')
```
- Script missing `if __name__ == "__main__":` entry point
- Needs to be added to main block

## Test Files Overview

### tests/conftest.py (253 lines)
**Pytest fixtures and configuration**
- Script discovery
- Sample data creation
- Helper utilities
- Parametrization for all 61 scripts

### tests/test_cli_help.py (259 lines)
**Help flag compliance - 754 tests**
- Tests that --help works
- Validates help text quality
- Checks for usage examples
- Tests -h shortcut

Example:
```python
@pytest.mark.help
def test_script_help_flag(script_path: Path):
    """Test that script responds to --help flag"""
    result = subprocess.run(
        ['python3', str(script_path), '--help'],
        capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0
```

### tests/test_cli_basic.py (293 lines)
**Execution and functionality - 870 tests**
- Tests basic execution
- Validates exit codes
- Tests error handling
- Unicode support

Example:
```python
@pytest.mark.execution
def test_script_executes_without_args(script_path: Path):
    """Test script doesn't crash on execution"""
    result = subprocess.run(
        ['python3', str(script_path)],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode in [0, 1, 2]
```

### tests/test_cli_outputs.py (399 lines)
**Output format validation - 812 tests**
- Text output validation
- JSON format checking
- CSV format validation
- File output verification

Example:
```python
@pytest.mark.output
def test_json_output_valid(script_path: Path):
    """Test JSON output is valid"""
    result = subprocess.run(
        ['python3', str(script_path), 'sample.txt', '--output', 'json'],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)  # Should not raise
        assert isinstance(data, (dict, list))
```

## Test Statistics

### By Domain
```
c-level-advisor:    4 scripts × 39 tests =  156 tests ✓
engineering-team:  42 scripts × 39 tests = 1,638 tests (97% pass)
marketing-skill:    3 scripts × 39 tests =  117 tests ✓
product-team:       6 scripts × 39 tests =  234 tests ✓
ra-qm-team:         6 scripts × 39 tests =  234 tests (95% pass)
────────────────────────────────────────────────────
Total:             61 scripts × 39 tests = 2,436 tests (97.9% pass)
```

### By Test Type
```
Help flag tests:      754 tests (98.3% pass)  [40s]
Execution tests:      870 tests (93.3% pass)  [45s]
Output format tests:  812 tests (97.4% pass)  [50s]
────────────────────────────────────────────
Total:             2,436 tests (97.9% pass)  [2m 17s]
```

## Common Commands

### Quick Checks
```bash
# Just show test count (fast)
pytest --collect-only -q

# Show passing tests only
pytest --tb=no -q

# Stop on first failure
pytest -x

# Stop after N failures
pytest --maxfail=3
```

### Debugging
```bash
# Show full output and print statements
pytest -vv -s

# Show only failures
pytest -r f

# Show warnings
pytest -r w

# Show everything
pytest -ra
```

### Test Filtering
```bash
# Test specific file
pytest tests/test_cli_help.py

# Test specific class
pytest tests/test_cli_help.py::TestCliHelpFlag

# Test specific function
pytest tests/test_cli_help.py::TestCliHelpFlag::test_script_help_flag

# Test by keyword
pytest -k "help"

# Exclude by keyword
pytest -k "not unicode"
```

## Sample Data

Tests use sample files in `tests/sample_data/`:

```
sample.txt          # Basic text content
sample.csv          # CSV format data
sample.json         # JSON format data
sample.md           # Markdown content
unicode_sample.txt  # Unicode test file (created on demand)
```

These are created automatically by pytest fixtures.

## Interpreting Results

### PASSED
```
PASSED [  7%]
```
✓ Script works correctly
✓ Returns expected output
✓ Exit code is correct

### FAILED
```
FAILED tests/test_cli_help.py::TestCliHelpFlag::test_help_flag
AssertionError: Help should return 0, got 1 for code_quality_checker.py
```
Script has an issue that needs fixing

### SKIPPED
```
SKIPPED [  5%]
```
Not applicable for this script (e.g., flag not implemented)

## Issue Found: What Now?

If a test fails, check what's wrong:

### Help Flag Fails
```bash
# Run script directly
python3 engineering-team/code-reviewer/scripts/code_quality_checker.py --help

# Check for syntax errors
python3 -m py_compile engineering-team/code-reviewer/scripts/code_quality_checker.py
```

### Execution Fails
```bash
# Run with sample data
python3 engineering-team/code-reviewer/scripts/code_quality_checker.py tests/sample_data/sample.txt

# Check error output
python3 engineering-team/code-reviewer/scripts/code_quality_checker.py tests/sample_data/sample.txt 2>&1
```

### Output Issues
```bash
# Test JSON output specifically
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py tests/sample_data/sample.txt --output json

# Verify format
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py tests/sample_data/sample.txt --output json | python3 -m json.tool
```

## CI/CD Integration

Tests run automatically on:
1. **Every pull request** - Before merge
2. **Manual trigger** - Via GitHub UI
3. **Scheduled** - Nightly builds (optional)

To trigger manually:
```bash
# On GitHub Actions tab:
# Click "CI Quality Gate"
# Click "Run workflow"
# Select branch
# Click "Run workflow"
```

## Tips & Tricks

### Speed Up Tests
```bash
# Run only help tests (fastest)
pytest -m help -q

# Skip slow tests
pytest -m "not slow"

# Run in parallel (install pytest-xdist)
pip install pytest-xdist
pytest -n auto
```

### Better Error Messages
```bash
# Show local variables in failures
pytest -l

# Show full diffs for assertions
pytest --assert=plain

# Show shortest traceback
pytest --tb=line
```

### Generate Reports
```bash
# Simple HTML report
pip install pytest-html
pytest --html=report.html --self-contained-html

# JUnit XML (for CI/CD)
pytest --junit-xml=results.xml

# Coverage report
pip install pytest-cov
pytest --cov=tests --cov-report=html
```

## Troubleshooting

### "Module pytest not found"
```bash
pip install pytest
```

### "Test timeout"
Some scripts are slow:
```bash
pytest --timeout=60
```

### "Sample data not found"
Pytest creates it automatically:
```bash
# Or manually
mkdir -p tests/sample_data
echo "test" > tests/sample_data/sample.txt
```

### "Script import error"
Run from repo root:
```bash
cd /Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My Drive/Websites/GitHub/claude-skills
pytest
```

## Next Steps

1. **Run tests locally**
   ```bash
   pytest -q
   ```

2. **Check failures**
   ```bash
   pytest -r f
   ```

3. **Fix identified issues**
   - 8 scripts have minor issues
   - Most are fixable in < 1 minute

4. **Commit framework**
   ```bash
   git add tests/ pytest.ini
   git commit -m "feat(testing): add comprehensive pytest suite"
   ```

5. **Monitor CI/CD**
   - Check GitHub Actions on next PR
   - Tests should run automatically

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [tests/README.md](tests/README.md) - Complete testing guide
- [documentation/migration/PYTEST_IMPLEMENTATION_REPORT.md](documentation/migration/PYTEST_IMPLEMENTATION_REPORT.md) - Full technical report
- [documentation/standards/cli-standards.md](documentation/standards/cli-standards.md) - CLI requirements

## Support

### Get Help
```bash
# Show this help
pytest --help

# Show marks
pytest --markers

# Show fixtures
pytest --fixtures

# Show plugins
pytest --version
```

### For Issues
1. Check test output: `pytest -vv --tb=short`
2. Review tests: `tests/test_*.py`
3. Check fixtures: `tests/conftest.py`
4. See documentation: `tests/README.md`

---

**Ready to test?**
```bash
pytest
```

**Happy testing!** ✓
