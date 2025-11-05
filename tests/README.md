# Claude Skills Test Suite

Automated pytest-based testing framework for validating Python CLI scripts across the Claude Skills library.

## Overview

This test suite ensures all 67 production Python scripts follow CLI standards and maintain high quality:

- **CLI Compliance:** --help flag, usage information, argument parsing
- **Execution:** Successful runs, proper exit codes, error handling
- **Output Quality:** Text/JSON/CSV format validation, consistent output
- **Performance:** Quick execution, no timeouts, reasonable output sizes

## Quick Start

```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run tests for specific marker
pytest -m help              # --help flag tests only
pytest -m execution         # Execution tests only
pytest -m output            # Output format tests only

# Run tests for specific script
pytest -k "brand_voice_analyzer"

# Run with coverage report
pytest --cov=tests --cov-report=term-missing

# Run with verbose output
pytest -vv

# Run specific test file
pytest tests/test_cli_help.py
```

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Pytest fixtures & configuration
│
├── test_cli_help.py              # --help flag tests (67+ tests)
│   ├── TestCliHelpFlag           # Basic help flag functionality
│   ├── TestCliStandardFlags      # Standard flag documentation
│   ├── TestCliHelpEdgeCases      # Edge cases and robustness
│   └── TestCliVersionFlag        # Version flag (optional)
│
├── test_cli_basic.py             # Execution tests (70+ tests)
│   ├── TestBasicScriptExecution  # Basic execution, file handling
│   ├── TestExitCodes             # Exit code validation
│   ├── TestOutputFormatFlags     # Output format flags
│   └── TestErrorHandling         # Error handling, edge cases
│
├── test_cli_outputs.py           # Output format tests (60+ tests)
│   ├── TestTextOutput            # Text output validation
│   ├── TestJsonOutput            # JSON format validation
│   ├── TestCsvOutput             # CSV format validation
│   ├── TestFileOutput            # File output creation
│   └── TestOutputConsistency     # Consistency checks
│
└── README.md                      # This file
```

## Test Markers

Use pytest markers to run specific test categories:

```bash
# Help flag compliance
pytest -m help

# Execution and functionality
pytest -m execution

# Output format validation
pytest -m output

# Slow tests (if any)
pytest -m slow

# Integration tests
pytest -m integration
```

## Sample Data

The test suite automatically creates sample data files in `tests/sample_data/`:

- `sample.txt` - Text content for analysis
- `sample.csv` - CSV data for processing
- `sample.json` - JSON data for processing
- `sample.md` - Markdown content for SEO testing

These are created automatically by the `setup_sample_data` fixture.

## Test Coverage

### Help Flag Tests (test_cli_help.py)

Tests that all 67 scripts respond properly to --help:

- Help flag returns exit code 0
- Help output contains usage information
- Help output includes description
- Help documents all arguments
- -h shortcut works
- Help text is well-formatted
- Standard flags are documented (--output, --verbose, etc.)
- Usage examples included
- Help goes to stdout, not stderr
- --version flag handled gracefully

**Expected:** 67+ tests (1 per script)

### Execution Tests (test_cli_basic.py)

Tests basic script functionality:

- Scripts execute without crashing
- Proper exit codes (0 for success, non-zero for errors)
- Missing files handled gracefully
- Timeout checks (30 second limit)
- Valid Python syntax
- Uses argparse for CLI
- Error messages are clear
- Unicode input handled
- Working directory not modified

**Expected:** 70+ tests

### Output Tests (test_cli_outputs.py)

Tests output format and quality:

- Text output is readable
- JSON output is valid
- CSV output is properly formatted
- File output creates valid files
- Output encoding is UTF-8
- No excessive output (>1MB sanity check)
- Output is consistent across runs
- Verbose mode works
- stderr for errors, stdout for output

**Expected:** 60+ tests

## Performance

Tests are designed for speed:

- Individual script tests: <1 second
- All tests: ~5-10 minutes on standard hardware
- No external dependencies required
- Local-only execution (no network calls)

Expected total runtime: **< 15 minutes**

## Fixtures

### conftest.py Provides

**Script Discovery:**
- `all_scripts` - List of all discovered scripts
- `base_path` - Base repository path

**Test Data:**
- `sample_data_dir` - Directory with sample data files
- `temp_output_dir` - Temporary directory for test outputs

**Utilities:**
- `run_script()` - Helper to run scripts
- `CLITestHelper` - Common CLI testing assertions

**Auto-fixtures:**
- `setup_sample_data` - Creates sample files automatically

## Running in CI/CD

The test suite integrates with GitHub Actions:

```yaml
- name: Run pytest
  run: |
    pip install pytest
    pytest tests/ -v --tb=short --junit-xml=test-results.xml

- name: Publish test results
  uses: EnricoMi/publish-unit-test-result-action@v2
  if: always()
  with:
    files: test-results.xml
```

## Adding New Tests

To add tests for a new script:

1. **Test automatically parametrized** - Just update script discovery
2. **Add custom test** - Create test function with `script_path` parameter
3. **Example:**

```python
@pytest.mark.help
def test_my_custom_requirement(script_path: Path):
    """Test custom requirement for all scripts"""
    result = subprocess.run(
        ['python3', str(script_path), '--help'],
        capture_output=True,
        text=True,
        timeout=10
    )
    assert result.returncode == 0
    # Your assertions here
```

## Known Limitations

1. **Script Discovery:** Only finds scripts in standard domain directories
2. **Sample Data:** Uses same sample data for all scripts
3. **Timeout:** 30 second timeout - may be too short for long-running tasks
4. **Example.py:** Skips example.py files (templates)

## Troubleshooting

### Tests fail with "module not found"

```bash
# Install dependencies
pip install -r requirements.txt

# Or run from repo root
cd /path/to/claude-skills
pytest
```

### Tests timeout

Some scripts may be slower:

```bash
# Increase timeout
pytest --timeout=60
```

### Specific script tests fail

```bash
# Run just that script
pytest -k "script_name" -vv

# See full output
pytest -k "script_name" -vv -s
```

### Sample data missing

```bash
# Fixtures create it automatically
# Or manually:
mkdir -p tests/sample_data
echo "test content" > tests/sample_data/sample.txt
```

## Test Statistics

- **Total Scripts:** 67 production Python scripts
- **Test Modules:** 3 (help, execution, output)
- **Test Classes:** 13
- **Test Functions:** 197+ individual tests
- **Test Coverage:** 100% of scripts tested
- **Expected Runtime:** < 15 minutes

## Integration with CI/CD

See [.github/workflows/ci-quality-gate.yml](../.github/workflows/ci-quality-gate.yml) for full CI integration.

The test suite runs on:
- Every pull request (before merge)
- Workflow dispatch (manual trigger)
- Schedule (nightly builds possible)

## Best Practices

### When Writing Tests

1. **Use markers** - `@pytest.mark.help`, `@pytest.mark.execution`, etc.
2. **Clear assertions** - Include script name in failure messages
3. **Fast execution** - 30 second timeout per test
4. **Parametrized** - Use script_path fixture for all scripts
5. **Helpful errors** - Show what went wrong and why

### For Test Maintenance

1. **Keep sample data small** - < 1KB files for speed
2. **Test one thing** - Each test should have one assertion focus
3. **Use fixtures** - Don't duplicate setup code
4. **Document markers** - Keep markers section updated
5. **Fix flaky tests** - No random failures

## Related Documentation

- [CLI Standards](../standards/cli/cli-standards.md) - What all CLI scripts must do
- [Python Scripts Guide](../TESTING_GUIDE.md) - Testing guidelines
- [Contributing Guide](../CONTRIBUTING.md) - Development standards

## Future Enhancements

- [ ] Performance benchmarking tests
- [ ] Memory usage validation
- [ ] Integration tests between scripts
- [ ] Cross-platform testing (Windows, Mac, Linux)
- [ ] Test report generation (HTML)
- [ ] Coverage reports with badges

## Support

For issues or questions:

1. Check existing test output: `pytest -vv`
2. Review test code: `tests/test_*.py`
3. Check fixture definitions: `tests/conftest.py`
4. See CI logs: `.github/workflows/ci-quality-gate.yml`

---

**Last Updated:** November 5, 2025
**Test Suite Version:** 1.0.0
**Pytest Minimum:** 3.8+
**Status:** Production Ready
