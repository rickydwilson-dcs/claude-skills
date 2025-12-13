# How to Use Senior Mobile Skill

Quick start guide for cross-platform mobile development with React Native, Flutter, and Expo.

## Quick Start

### 1. Generate a New Project

```bash
# React Native with TypeScript and Redux
python3 scripts/mobile_scaffolder.py \
  --framework react-native \
  --platforms ios,android \
  --navigation react-navigation \
  --state redux \
  --output ./my-app

# Flutter with Riverpod
python3 scripts/mobile_scaffolder.py \
  --framework flutter \
  --navigation go-router \
  --state riverpod \
  --output ./my-flutter-app

# Expo with Zustand
python3 scripts/mobile_scaffolder.py \
  --framework expo \
  --navigation expo-router \
  --state zustand \
  --output ./my-expo-app
```

### 2. Analyze Existing Project

```bash
# Full analysis
python3 scripts/platform_detector.py --check all --depth full

# iOS-only
python3 scripts/platform_detector.py --check ios --output json

# Android signing
python3 scripts/platform_detector.py --check android --depth signing
```

### 3. Validate for App Stores

```bash
# Apple App Store
python3 scripts/app_store_validator.py --store apple --strict

# Google Play Store
python3 scripts/app_store_validator.py --store google --strict

# Both stores
python3 scripts/app_store_validator.py --store both --output markdown > report.md
```

## Common Tasks

### Framework Selection

Use `references/frameworks.md` to compare React Native vs Flutter:

| Factor | React Native | Flutter |
|--------|-------------|---------|
| Team has JS experience | Choose RN | - |
| UI consistency critical | - | Choose Flutter |
| Need web support | - | Choose Flutter |
| Existing native modules | Choose RN | - |

### Pre-Release Checklist

1. Run validation: `python3 scripts/app_store_validator.py --store both --strict`
2. Fix all critical and high-priority issues
3. Re-validate until clean
4. Build release versions
5. Submit to stores

### CI/CD Setup

Generate project with CI:
```bash
python3 scripts/mobile_scaffolder.py \
  --framework react-native \
  --ci github-actions \
  --output ./my-app
```

Configure secrets in GitHub:
- `APPLE_CERTIFICATE_BASE64`
- `APPLE_PROVISIONING_PROFILE_BASE64`
- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

## Tool Reference

| Tool | Purpose | Key Options |
|------|---------|-------------|
| `mobile_scaffolder.py` | Generate projects | `--framework`, `--platforms`, `--state` |
| `platform_detector.py` | Analyze projects | `--check`, `--depth`, `--output` |
| `app_store_validator.py` | Validate builds | `--store`, `--strict`, `--output` |

## Related Skills

- **senior-ios** - Deep Swift/SwiftUI expertise
- **senior-flutter** - Deep Dart/Flutter expertise
- **senior-frontend** - Web frontend patterns

## Need More?

See `SKILL.md` for complete workflows and detailed documentation.
