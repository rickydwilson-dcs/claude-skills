# Mobile Python Tools Documentation

Complete reference for the Python CLI tools included in the senior-mobile skill package.

## Overview

| Tool | Purpose | Primary Use Case |
|------|---------|------------------|
| `mobile_scaffolder.py` | Generate project structures | New project setup |
| `platform_detector.py` | Analyze project configuration | Project audit and debugging |
| `app_store_validator.py` | Pre-submission validation | Release preparation |

All tools:
- Use Python standard library only (no pip dependencies)
- Support `--help` for usage information
- Output in multiple formats (text, JSON, CSV, markdown)
- Work cross-platform (macOS, Linux, Windows)

---

## mobile_scaffolder.py

Generate complete mobile project structures with best practices baked in.

### Usage

```bash
python3 scripts/mobile_scaffolder.py [options]
```

### Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--framework` | react-native, flutter, expo | Required | Target framework |
| `--platforms` | ios, android, web | ios,android | Target platforms |
| `--navigation` | react-navigation, expo-router, go-router, auto-route | auto | Navigation library |
| `--state` | redux, zustand, mobx, riverpod, bloc, provider | auto | State management |
| `--ci` | github-actions, gitlab-ci, bitrise, none | none | CI/CD configuration |
| `--output` | path | ./new-app | Output directory |
| `--dry-run` | flag | false | Preview without creating |
| `--verbose` | flag | false | Detailed output |

### Examples

```bash
# React Native with full configuration
python3 scripts/mobile_scaffolder.py \
  --framework react-native \
  --platforms ios,android \
  --navigation react-navigation \
  --state redux \
  --ci github-actions \
  --output ./my-app

# Flutter clean architecture
python3 scripts/mobile_scaffolder.py \
  --framework flutter \
  --platforms ios,android,web \
  --navigation go-router \
  --state riverpod \
  --ci github-actions \
  --output ./my-flutter-app

# Expo managed workflow
python3 scripts/mobile_scaffolder.py \
  --framework expo \
  --platforms ios,android \
  --navigation expo-router \
  --state zustand \
  --output ./my-expo-app

# Preview what would be created
python3 scripts/mobile_scaffolder.py \
  --framework flutter \
  --dry-run
```

### Generated Structure

**React Native:**
```
my-app/
├── src/
│   ├── components/
│   ├── screens/
│   ├── navigation/
│   ├── services/
│   ├── store/
│   ├── hooks/
│   └── utils/
├── ios/
├── android/
├── __tests__/
├── .github/workflows/      # If --ci github-actions
├── tsconfig.json
├── babel.config.js
└── package.json
```

**Flutter:**
```
my-flutter-app/
├── lib/
│   ├── core/
│   ├── features/
│   └── shared/
├── test/
├── ios/
├── android/
├── web/                    # If web in platforms
├── .github/workflows/
└── pubspec.yaml
```

---

## platform_detector.py

Analyze mobile projects to detect framework type, platform capabilities, and configuration status.

### Usage

```bash
python3 scripts/platform_detector.py [options]
```

### Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--check` | ios, android, all | all | Platforms to check |
| `--depth` | quick, standard, full, signing | standard | Analysis depth |
| `--output` | text, json, csv | text | Output format |
| `--project-path` | path | . | Project root path |

### Examples

```bash
# Full analysis of current directory
python3 scripts/platform_detector.py --check all --depth full

# iOS-only with JSON output
python3 scripts/platform_detector.py --check ios --output json

# Android signing analysis
python3 scripts/platform_detector.py --check android --depth signing

# Analyze specific project
python3 scripts/platform_detector.py --project-path /path/to/app --check all
```

### Output

**Text Output:**
```
=== Mobile Project Analysis ===

Project Type: React Native
Version: 0.73.0

--- iOS Configuration ---
Bundle ID: com.example.myapp
Minimum iOS: 13.0
Provisioning: ✓ Found (Development)
Entitlements: Push Notifications, Background Modes
Info.plist: ✓ Complete

--- Android Configuration ---
Package: com.example.myapp
Min SDK: 24
Target SDK: 34
Signing: ✓ Configured (release keystore)
Manifest: ✓ Complete

Health Score: 92/100
```

**JSON Output:**
```json
{
  "project_type": "react-native",
  "version": "0.73.0",
  "ios": {
    "bundle_id": "com.example.myapp",
    "min_version": "13.0",
    "provisioning": "development",
    "entitlements": ["push", "background-modes"],
    "info_plist_complete": true
  },
  "android": {
    "package": "com.example.myapp",
    "min_sdk": 24,
    "target_sdk": 34,
    "signing_configured": true,
    "manifest_complete": true
  },
  "health_score": 92
}
```

### Detection Capabilities

**Project Type Detection:**
- React Native (package.json with react-native)
- Flutter (pubspec.yaml)
- Expo (app.json with expo)
- Native iOS (*.xcodeproj or *.xcworkspace)
- Native Android (build.gradle with com.android.application)

**iOS Checks:**
- Bundle identifier
- Minimum iOS version
- Provisioning profiles
- Entitlements
- Info.plist completeness
- Code signing configuration

**Android Checks:**
- Package name
- Min/Target SDK versions
- Signing configuration
- Manifest permissions
- ProGuard/R8 setup
- 64-bit support

---

## app_store_validator.py

Validate mobile app builds against Apple App Store and Google Play Store requirements.

### Usage

```bash
python3 scripts/app_store_validator.py [options]
```

### Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--store` | apple, google, both | Required | Target store(s) |
| `--build-path` | path | auto-detect | Path to build artifacts |
| `--check` | all, icons, manifest, signing, privacy | all | Specific checks |
| `--strict` | flag | false | Fail on warnings |
| `--output` | text, json, markdown | text | Output format |

### Examples

```bash
# Apple App Store validation
python3 scripts/app_store_validator.py --store apple --strict

# Google Play Store validation
python3 scripts/app_store_validator.py --store google --build-path ./android/app/build

# Both stores with markdown report
python3 scripts/app_store_validator.py --store both --output markdown > report.md

# Specific check only
python3 scripts/app_store_validator.py --store apple --check icons
```

### Validation Checks

**Apple App Store:**

| Check | Severity | Description |
|-------|----------|-------------|
| Info.plist | Critical | Required keys present |
| Privacy Manifest | Critical | PrivacyInfo.xcprivacy for required APIs |
| App Icons | High | All required sizes (1024x1024, etc.) |
| Launch Screen | High | Launch storyboard or image set |
| Entitlements | High | Valid entitlement keys |
| Permissions | Medium | Usage descriptions for all permissions |
| Min iOS Version | Low | iOS 13+ recommended |
| Swift Version | Low | Current Swift version |

**Google Play Store:**

| Check | Severity | Description |
|-------|----------|-------------|
| Target SDK | Critical | Must meet Play Store requirements |
| 64-bit Support | Critical | arm64-v8a required |
| Signing | Critical | Release keystore configured |
| Manifest | High | Required permissions declared |
| Icons | High | Adaptive icons recommended |
| ProGuard | Medium | Obfuscation enabled |
| Min SDK | Low | SDK 24+ recommended |

### Output

**Text Output:**
```
=== App Store Validation Report ===

Target: Apple App Store
Status: PASS (with warnings)

✓ Info.plist complete
✓ App icons present (all sizes)
✓ Launch screen configured
✓ Privacy manifest present
⚠ NSLocationWhenInUseUsageDescription could be more specific
✓ Entitlements valid
✓ Minimum iOS version: 14.0

Summary:
  Critical: 0
  High: 0
  Medium: 1
  Low: 0

Recommendation: Ready for submission (address warning for best experience)
```

**Markdown Output:**
```markdown
# App Store Validation Report

**Store:** Apple App Store
**Status:** ✅ PASS (with warnings)
**Date:** 2025-12-13

## Checks

| Check | Status | Severity | Details |
|-------|--------|----------|---------|
| Info.plist | ✅ | Critical | All required keys present |
| App Icons | ✅ | High | 1024x1024, 180x180, etc. |
| Launch Screen | ✅ | High | LaunchScreen.storyboard |
| Privacy Manifest | ✅ | Critical | PrivacyInfo.xcprivacy present |
| Permissions | ⚠️ | Medium | Location description vague |

## Summary

- **Critical Issues:** 0
- **High Priority:** 0
- **Medium Priority:** 1
- **Low Priority:** 0

## Recommendations

1. Update `NSLocationWhenInUseUsageDescription` to be more specific
```

---

## Integration Examples

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running mobile validation..."
python3 scripts/app_store_validator.py --store both --strict

if [ $? -ne 0 ]; then
  echo "❌ Validation failed. Please fix issues before committing."
  exit 1
fi

echo "✅ Validation passed"
```

### CI/CD Integration

```yaml
# .github/workflows/validate.yml
name: Mobile Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Detect Platform
        run: |
          python3 scripts/platform_detector.py --output json > platform-info.json

      - name: Validate for Stores
        run: |
          python3 scripts/app_store_validator.py --store both --strict --output markdown > validation-report.md

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: validation-report
          path: validation-report.md
```

### Scripted Project Setup

```bash
#!/bin/bash
# setup-new-project.sh

PROJECT_NAME=$1
FRAMEWORK=${2:-react-native}

echo "Creating $PROJECT_NAME with $FRAMEWORK..."

# Generate project
python3 scripts/mobile_scaffolder.py \
  --framework $FRAMEWORK \
  --platforms ios,android \
  --ci github-actions \
  --output ./$PROJECT_NAME

# Verify setup
cd $PROJECT_NAME
python3 ../scripts/platform_detector.py --check all

echo "✅ Project $PROJECT_NAME created successfully"
```

---

## Troubleshooting

### Common Issues

**"Project type not detected"**
- Ensure you're in the project root directory
- Check that package.json, pubspec.yaml, or app.json exists
- Use `--project-path` to specify exact location

**"Validation warnings for missing icons"**
- Generate all required icon sizes
- Use tools like app-icon or flutter_launcher_icons
- Verify icon locations match expected paths

**"Signing not configured"**
- iOS: Check Xcode signing settings
- Android: Verify keystore in build.gradle
- Use `--depth signing` for detailed analysis

### Getting Help

```bash
# Full help for any tool
python3 scripts/mobile_scaffolder.py --help
python3 scripts/platform_detector.py --help
python3 scripts/app_store_validator.py --help
```
