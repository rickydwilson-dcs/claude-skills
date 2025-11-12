# Python Script Testing Guide

This guide shows you how to test Python scripts in the claude-skills repository to ensure they follow CLI standards and work correctly.

---

## Quick Start - Test Any Script

### 1. Test a Single Script (Comprehensive)

```bash
# Basic test (checks syntax, argparse, --help)
./test_single_script.sh marketing-skill/content-creator/scripts/brand_voice_analyzer.py

# Full test with sample input (checks execution, JSON, file output, verbose)
./test_single_script.sh \
  marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt
```

### 2. Test All Scripts (Full Suite)

```bash
# Run the complete test suite on all 67 scripts
./test_cli_standards.sh
```

---

## Testing Tools Available

### Tool 1: `test_single_script.sh` ⭐ Recommended

**Purpose:** Comprehensive testing of a single script with detailed output

**What it tests:**
1. ✅ Python syntax validity
2. ✅ Uses argparse (not manual sys.argv)
3. ✅ Has main() function
4. ✅ `--help` flag works
5. ✅ `--version` flag (optional)
6. ✅ Standard flags documented (--output, --file, --verbose)
7. ✅ Execution with sample input (if provided)
8. ✅ JSON output validity
9. ✅ File output creation
10. ✅ Verbose mode

**Usage:**
```bash
# Test without input (checks 1-6)
./test_single_script.sh path/to/script.py

# Test with input (checks 1-10)
./test_single_script.sh path/to/script.py path/to/sample_input.txt
```

**Example:**
```bash
./test_single_script.sh \
  product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  product-team/product-manager-toolkit/assets/sample-features.csv
```

---

### Tool 2: `test_cli_standards.sh`

**Purpose:** Batch testing of all scripts in the repository

**What it tests:**
1. ✅ `--help` flag works
2. ✅ Python syntax valid
3. ✅ Uses argparse
4. ✅ Has main() function

**Usage:**
```bash
./test_cli_standards.sh
```

**Output:**
```
Testing: brand_voice_analyzer.py
  ✓ --help flag works
  ✓ Python syntax valid
  ✓ Uses argparse
  ✓ Has main() function
  PASSED (4 checks)

========================================
Test Summary:
  Total scripts tested: 67
  Passed: 56
  Failed: 11
========================================
```

**Note:** The 11 "failures" are expected (RA/QM placeholder scripts).

---

## Manual Testing Methods

### Method 1: Test Help Documentation

```bash
# View complete help for any script
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py --help

# Test version info
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py --version
```

**What to look for:**
- Clear description
- All flags documented with short/long forms
- Usage examples provided
- Default values shown

---

### Method 2: Test Basic Execution

```bash
# Run with sample input (text output)
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt

# Check exit code
echo $?  # Should be 0 for success
```

---

### Method 3: Test Output Formats

```bash
# Test JSON output
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt \
  --output json

# Validate JSON is properly formatted
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt \
  --output json | python3 -m json.tool
```

---

### Method 4: Test File Output

```bash
# Write output to file
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt \
  --output json \
  --file results.json

# Verify file was created
ls -lh results.json
cat results.json
```

---

### Method 5: Test Verbose Mode

```bash
# Enable verbose output
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt \
  --verbose
```

---

### Method 6: Test Error Handling

```bash
# Test with missing file (should fail gracefully)
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py nonexistent.txt
echo $?  # Should be 1 (error)

# Test with invalid arguments (should show help)
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py --invalid-flag
```

---

## Testing Examples by Domain

### Marketing Scripts

```bash
# Brand Voice Analyzer
./test_single_script.sh \
  marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt

# SEO Optimizer
./test_single_script.sh \
  marketing-skill/content-creator/scripts/seo_optimizer.py \
  marketing-skill/content-creator/assets/sample-article.md

# CAC Calculator
./test_single_script.sh \
  marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py \
  marketing-skill/marketing-demand-acquisition/assets/sample-channels.json
```

---

### Product Team Scripts

```bash
# RICE Prioritizer
./test_single_script.sh \
  product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  product-team/product-manager-toolkit/assets/sample-features.csv

# User Story Generator
./test_single_script.sh \
  product-team/agile-product-owner/scripts/user_story_generator.py \
  product-team/agile-product-owner/assets/sample-epic.json

# Customer Interview Analyzer
./test_single_script.sh \
  product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py \
  product-team/product-manager-toolkit/assets/sample-interview.txt
```

---

### C-Level Advisory Scripts

```bash
# Financial Scenario Analyzer
./test_single_script.sh \
  c-level-advisor/ceo-advisor/scripts/financial_scenario_analyzer.py \
  c-level-advisor/ceo-advisor/assets/sample-scenarios.json

# Strategy Analyzer
./test_single_script.sh \
  c-level-advisor/ceo-advisor/scripts/strategy_analyzer.py \
  c-level-advisor/ceo-advisor/assets/sample-company.json

# Tech Debt Analyzer
./test_single_script.sh \
  c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py \
  c-level-advisor/cto-advisor/assets/sample-system.json

# Team Scaling Calculator
./test_single_script.sh \
  c-level-advisor/cto-advisor/scripts/team_scaling_calculator.py \
  c-level-advisor/cto-advisor/assets/sample-team.json
```

---

### Engineering Scripts

```bash
# Code Quality Checker
./test_single_script.sh \
  engineering-team/code-reviewer/scripts/code_quality_checker.py

# Project Architect
./test_single_script.sh \
  engineering-team/senior-architect/scripts/project_architect.py

# Any engineering script (they all follow the same pattern)
./test_single_script.sh \
  engineering-team/senior-ml-engineer/scripts/rag_system_builder.py
```

---

## CI/CD Testing

### GitHub Actions (Automatic)

The repository has CI/CD pipeline that automatically runs on:
- Pull requests
- Push to main
- Manual trigger

**What it tests:**
- Python syntax (compileall)
- YAML linting
- Workflow validation
- Dependency audits

**Location:** `.github/workflows/ci-quality-gate.yml`

**Trigger manually:**
```bash
# Use GitHub CLI
gh workflow run ci-quality-gate.yml
```

---

## Test Results Interpretation

### Success Indicators ✅

```
✓ PASSED - Valid Python syntax
✓ PASSED - Uses argparse
✓ PASSED - Has main() function
✓ PASSED - --help flag works
✓ PASSED - Script executed successfully
✓ PASSED - Valid JSON output
✓ PASSED - File created successfully
```

### Warning Indicators ⚠️

```
⚠ WARNING - No main() function found (not critical)
⚠ SKIPPED - No --version flag (optional)
⚠ SKIPPED - No sample input provided
```

### Failure Indicators ✗

```
✗ FAILED - Syntax errors found
✗ FAILED - Does not import argparse
✗ FAILED - --help flag failed
✗ FAILED - Script execution failed
✗ FAILED - Invalid JSON output
```

---

## Troubleshooting

### Issue: Script not found

```bash
# Error
Error: Script not found: path/to/script.py

# Solution: Use correct path from repository root
cd /path/to/claude-skills
./test_single_script.sh marketing-skill/content-creator/scripts/brand_voice_analyzer.py
```

---

### Issue: Sample input file missing

```bash
# Error
✗ FAILED - Sample input file not found

# Solution: Check if assets/ directory and sample files exist
ls marketing-skill/content-creator/assets/

# Create sample file if missing (see assets/README.md)
```

---

### Issue: Invalid JSON output

```bash
# Error
✗ FAILED - Invalid JSON output

# Debug: Check what the script outputs
python3 script.py input.txt --output json

# Common causes:
# - Extra print statements mixed with JSON
# - Syntax error in JSON formatting
# - Script writing to stdout instead of returning JSON
```

---

### Issue: Permission denied

```bash
# Error
Permission denied: ./test_single_script.sh

# Solution: Make script executable
chmod +x ./test_single_script.sh
chmod +x ./test_cli_standards.sh
```

---

## Best Practices

### 1. Test After Every Change
```bash
# After modifying a script
./test_single_script.sh path/to/modified/script.py path/to/sample.txt
```

### 2. Test with Multiple Inputs
```bash
# Test with different input sizes
./test_single_script.sh script.py small_input.txt
./test_single_script.sh script.py large_input.txt
```

### 3. Test All Output Formats
```bash
# Test text output
python3 script.py input.txt

# Test JSON output
python3 script.py input.txt --output json

# Test CSV output (if supported)
python3 script.py input.txt --output csv
```

### 4. Test Error Conditions
```bash
# Missing file
python3 script.py nonexistent.txt

# Invalid format
python3 script.py --output invalid_format

# Missing required argument
python3 script.py
```

### 5. Verify Exit Codes
```bash
# Success should return 0
python3 script.py valid_input.txt
echo $?  # Should print: 0

# Error should return non-zero
python3 script.py invalid_input.txt
echo $?  # Should print: 1, 3, or 4
```

---

## Quick Reference

### Test One Script Quickly
```bash
./test_single_script.sh <script_path>
```

### Test One Script Thoroughly
```bash
./test_single_script.sh <script_path> <sample_input>
```

### Test All Scripts
```bash
./test_cli_standards.sh
```

### Test Script Manually
```bash
# Help
python3 <script> --help

# Basic run
python3 <script> <input>

# JSON output
python3 <script> <input> --output json

# Save to file
python3 <script> <input> -o json -f output.json

# Verbose
python3 <script> <input> -v
```

---

## Sample Test Session

Here's a complete test session for the brand voice analyzer:

```bash
# 1. Navigate to repository
cd "/Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My Drive/Websites/GitHub/claude-skills"

# 2. View help
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py --help

# 3. Check version
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py --version

# 4. Run basic test
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt

# 5. Test JSON output
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt \
  --output json | python3 -m json.tool

# 6. Test file output
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt \
  --output json \
  --file analysis.json

# 7. Verify file created
cat analysis.json

# 8. Test verbose mode
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt \
  --verbose

# 9. Run comprehensive automated test
./test_single_script.sh \
  marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  marketing-skill/content-creator/assets/sample-content.txt

# 10. Check exit code
echo $?  # Should be 0
```

---

## Additional Resources

- **CLI Standards:** See `documentation/standards/cli-standards.md`
- **Python Template:** See `templates/python-cli-template.py`
- **Migration Report:** See `documentation/migration/CLI_MIGRATION_COMPLETE_2025-11-05.md`
- **Sample Files:** See `*/assets/README.md` in each skill directory

---

## Support

If tests fail or you need help:

1. Check the script's `--help` output for correct usage
2. Verify sample input file exists and is valid format
3. Check `documentation/standards/cli-standards.md` for requirements
4. Review test output for specific error messages
5. Check CI/CD logs in GitHub Actions

---

**Last Updated:** November 5, 2025
**Test Tools Version:** 1.0.0
