# Senior Mobile Scripts

Production-ready Python automation tools for mobile app development workflows.

## Tools

### app_store_validator.py

Pre-submission validation for Apple App Store and Google Play Store requirements.

**Purpose:** Catch common app store submission issues before uploading, reducing rejection risk and saving time.

**Features:**
- Apple App Store validation (Info.plist, icons, launch screens, privacy manifest)
- Google Play Store validation (AndroidManifest.xml, Gradle config, 64-bit support)
- Multiple output formats (text, JSON, markdown)
- Strict mode for CI/CD integration
- Actionable recommendations for each issue
- Cross-platform asset validation

**Usage:**
```bash
# Validate both stores
python app_store_validator.py ./my-app

# Apple App Store only
python app_store_validator.py ./my-app --store apple

# Google Play Store with markdown report
python app_store_validator.py ./my-app --store google --output markdown --file report.md

# Strict mode (fail on warnings) for CI/CD
python app_store_validator.py ./my-app --strict

# Verbose output for debugging
python app_store_validator.py ./my-app --verbose
```

**Exit Codes:**
- `0` - Success (ready for submission)
- `1` - Unexpected error
- `2` - Validation errors found
- `3` - Warnings in strict mode
- `4` - File I/O error

**Output Formats:**

*Text (default):*
```
=== Apple App Store Validation Results ===

Passed: 12
Errors: 1
Warnings: 2
Info: 0

--- Passed Checks ---
  ✓ Info.plist contains all required keys
  ✓ Launch screen configured

--- Errors (Must Fix) ---
  ✗ [Apple/Assets] Missing 1024x1024 App Store icon
    → Add 1024x1024 icon to AppIcon.appiconset/

--- Warnings (Should Fix) ---
  ⚠ [Apple/Privacy] PrivacyInfo.xcprivacy not found
    → Add PrivacyInfo.xcprivacy for iOS 17+ compliance
```

*JSON:*
```json
{
  "metadata": {
    "tool": "app_store_validator.py",
    "version": "1.0.0",
    "timestamp": "2025-12-13T20:00:00Z",
    "project": "my-app"
  },
  "validation": {
    "apple_app_store": {
      "summary": {
        "passed": 12,
        "errors": 1,
        "warnings": 2,
        "info": 0
      },
      "passed_checks": [...],
      "issues": [...]
    }
  }
}
```

*Markdown:*
```markdown
# App Store Validation Report

**Project:** my-app
**Store:** Apple App Store
**Generated:** 2025-12-13T20:00:00Z

## Summary
| Metric | Count |
|--------|-------|
| Passed Checks | 12 |
| Errors | 1 |
| Warnings | 2 |

## Errors (Must Fix)
### ❌ Missing 1024x1024 App Store icon
**Category:** Apple/Assets
**Recommendation:** Add 1024x1024 icon to AppIcon.appiconset/
```

**Apple App Store Checks:**
- ✓ Info.plist required keys (CFBundleIdentifier, CFBundleVersion, etc.)
- ✓ App icon sizes (20, 29, 40, 60, 76, 83.5, 1024)
- ✓ Launch screen configuration
- ✓ Privacy manifest (PrivacyInfo.xcprivacy for iOS 17+)
- ✓ Usage description strings (camera, location, photos, etc.)
- ✓ App Transport Security configuration
- ✓ Minimum deployment target (iOS 12+ recommended)
- ✓ App size estimation

**Google Play Store Checks:**
- ✓ AndroidManifest.xml required elements
- ✓ Package name format validation
- ✓ Target SDK version (34+ required for new apps in 2024)
- ✓ Minimum SDK version
- ✓ 64-bit support (arm64-v8a)
- ✓ Version code and version name
- ✓ App icon mipmaps (all densities)
- ✓ Adaptive icon support
- ✓ Permissions audit
- ✓ Code minification (ProGuard/R8)

**CI/CD Integration:**
```yaml
# GitHub Actions example
- name: Validate App Store Requirements
  run: |
    python scripts/app_store_validator.py . --strict --output json --file validation-report.json

- name: Upload Validation Report
  uses: actions/upload-artifact@v3
  with:
    name: app-store-validation
    path: validation-report.json
```

**Best Practices:**
1. Run validator before every app store submission
2. Use `--strict` mode in CI/CD pipelines
3. Generate markdown reports for PR reviews
4. Keep validation report history to track improvements
5. Address all errors and warnings before submission

**Common Issues Detected:**
- Missing required Info.plist keys
- Incomplete app icon sets
- Missing privacy manifest (iOS 17+)
- Target SDK version too low (Android)
- Missing 64-bit support
- Missing usage description strings
- Invalid package name format

**Requirements:**
- Python 3.8+
- No external dependencies (uses standard library only)
- Works on macOS, Linux, Windows

**Line Count:** 981 lines
**Version:** 1.0.0
**Last Updated:** 2025-12-13

---

## Development

All tools follow claude-skills standards:
- Standard library only (no pip dependencies)
- Support `--help` flag
- Multiple output formats
- Proper exit codes
- Verbose mode for debugging
- Comprehensive error handling

For more information, see:
- [Senior Mobile Skill Documentation](../SKILL.md)
- [Python CLI Template](/templates/python-cli-template.py)
- [CLI Standards](/docs/standards/cli-standards.md)
