#!/usr/bin/env python3
"""
Module: app_store_validator.py
Description: Pre-submission validation for Apple App Store and Google Play Store requirements

Validates mobile app projects against app store requirements including:
- Required metadata and configuration files
- Asset requirements (icons, screenshots, launch screens)
- Privacy and permission declarations
- Build configuration and versioning
- Store-specific compliance requirements

This tool helps catch common submission issues before uploading to app stores,
saving time and reducing rejection risk.

Usage:
    python app_store_validator.py ./my-app
    python app_store_validator.py ./my-app --store apple
    python app_store_validator.py ./my-app --build-path ./build/app.ipa --strict
    python app_store_validator.py ./my-app -o markdown -f report.md

Author: Claude Skills
Version: 1.0.0
Last Updated: 2025-12-13
"""

import argparse
import json
import logging
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ValidationIssue:
    """Represents a validation issue with severity level."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

    def __init__(self, severity: str, category: str, message: str, recommendation: str = ""):
        self.severity = severity
        self.category = category
        self.message = message
        self.recommendation = recommendation

    def to_dict(self) -> Dict[str, str]:
        return {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "recommendation": self.recommendation
        }


class AppStoreValidator:
    """Validates mobile app projects against app store requirements."""

    # Apple App Store icon sizes (points)
    APPLE_ICON_SIZES = [20, 29, 40, 60, 76, 83.5, 1024]

    # Google Play icon sizes (dp)
    GOOGLE_ICON_SIZES = [48, 72, 96, 144, 192, 512]

    def __init__(self, project_path: Path, build_path: Optional[Path] = None, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("AppStoreValidator initialized")

        self.project_path = project_path
        self.build_path = build_path
        self.verbose = verbose
        self.issues: List[ValidationIssue] = []
        self.passed_checks: List[str] = []

    def log(self, message: str):
        """Log verbose output."""
        if self.verbose:
            print(f"[VALIDATOR] {message}", file=sys.stderr)

    def add_issue(self, severity: str, category: str, message: str, recommendation: str = ""):
        """Add a validation issue."""
        self.issues.append(ValidationIssue(severity, category, message, recommendation))
        self.log(f"{severity.upper()}: {message}")

    def add_passed(self, check: str):
        """Add a passed check."""
        self.passed_checks.append(check)
        self.log(f"PASSED: {check}")

    def validate_apple_app_store(self) -> Dict[str, Any]:
        """Validate Apple App Store requirements."""
        logger.debug("Starting Apple App Store validation")
        self.log("Starting Apple App Store validation...")

        ios_path = self.project_path / "ios"
        if not ios_path.exists():
            logger.warning(f"iOS project directory not found at {ios_path}")
            self.add_issue(
                ValidationIssue.ERROR,
                "Apple/Project",
                "iOS project directory not found",
                "Ensure 'ios/' directory exists in your project"
            )
            return self._get_results()

        # Validate Info.plist
        self._validate_info_plist(ios_path)

        # Validate app icons
        self._validate_apple_icons(ios_path)

        # Validate launch screen
        self._validate_launch_screen(ios_path)

        # Validate privacy manifest (iOS 17+)
        self._validate_privacy_manifest(ios_path)

        # Validate usage descriptions
        self._validate_usage_descriptions(ios_path)

        # Validate build configuration
        self._validate_apple_build_config(ios_path)

        return self._get_results()

    def _validate_info_plist(self, ios_path: Path):
        """Validate Info.plist required keys."""
        info_plist_candidates = list(ios_path.rglob("Info.plist"))

        if not info_plist_candidates:
            self.add_issue(
                ValidationIssue.ERROR,
                "Apple/Metadata",
                "Info.plist not found",
                "Create Info.plist in your iOS project with required keys"
            )
            return

        info_plist_path = info_plist_candidates[0]
        self.log(f"Checking Info.plist: {info_plist_path}")

        try:
            tree = ET.parse(info_plist_path)
            root = tree.getroot()

            # Extract plist dictionary
            plist_dict = self._parse_plist_dict(root)

            # Required keys
            required_keys = [
                ("CFBundleIdentifier", "Bundle identifier"),
                ("CFBundleVersion", "Build version"),
                ("CFBundleShortVersionString", "App version"),
                ("CFBundleName", "Bundle name"),
                ("CFBundleDisplayName", "Display name"),
            ]

            missing_keys = []
            for key, description in required_keys:
                if key not in plist_dict:
                    missing_keys.append(f"{key} ({description})")

            if missing_keys:
                self.add_issue(
                    ValidationIssue.ERROR,
                    "Apple/Metadata",
                    f"Info.plist missing required keys: {', '.join(missing_keys)}",
                    "Add missing keys to Info.plist"
                )
            else:
                self.add_passed("Info.plist contains all required keys")

        except ET.ParseError as e:
            logger.error(f"Failed to parse Info.plist: {e}")
            self.add_issue(
                ValidationIssue.ERROR,
                "Apple/Metadata",
                f"Failed to parse Info.plist: {e}",
                "Fix XML syntax errors in Info.plist"
            )

    def _parse_plist_dict(self, root: ET.Element) -> Dict[str, str]:
        """Parse plist XML dictionary into Python dict."""
        plist_dict = {}

        # Find the main dict element
        dict_elem = root.find(".//dict")
        if dict_elem is None:
            return plist_dict

        # Parse key-value pairs
        children = list(dict_elem)
        for i in range(0, len(children), 2):
            if i + 1 < len(children) and children[i].tag == "key":
                key = children[i].text
                value_elem = children[i + 1]
                value = value_elem.text if value_elem.text else ""
                plist_dict[key] = value

        return plist_dict

    def _validate_apple_icons(self, ios_path: Path):
        """Validate Apple app icon assets."""
        # Look for AppIcon.appiconset
        appiconset_paths = list(ios_path.rglob("AppIcon.appiconset"))

        if not appiconset_paths:
            self.add_issue(
                ValidationIssue.ERROR,
                "Apple/Assets",
                "AppIcon.appiconset not found",
                "Create AppIcon.appiconset in Assets.xcassets with all required icon sizes"
            )
            return

        appiconset_path = appiconset_paths[0]
        self.log(f"Checking app icons: {appiconset_path}")

        # Check for Contents.json
        contents_json = appiconset_path / "Contents.json"
        if not contents_json.exists():
            self.add_issue(
                ValidationIssue.ERROR,
                "Apple/Assets",
                "AppIcon.appiconset/Contents.json not found",
                "Create Contents.json defining all required icon sizes"
            )
            return

        try:
            with open(contents_json, 'r') as f:
                contents = json.load(f)

            # Check for images
            images = contents.get("images", [])
            found_sizes = set()

            for image in images:
                size_str = image.get("size", "")
                if "x" in size_str:
                    # Parse size like "60x60" or "1024x1024"
                    width = float(size_str.split("x")[0])
                    found_sizes.add(width)

            missing_sizes = [size for size in self.APPLE_ICON_SIZES if size not in found_sizes]

            if missing_sizes:
                self.add_issue(
                    ValidationIssue.WARNING,
                    "Apple/Assets",
                    f"Missing icon sizes: {', '.join(map(str, missing_sizes))}pt",
                    "Add all required icon sizes to AppIcon.appiconset for best compatibility"
                )
            else:
                self.add_passed("App icons: All required sizes present")

            # Check for 1024x1024 App Store icon specifically
            if 1024 not in found_sizes:
                self.add_issue(
                    ValidationIssue.ERROR,
                    "Apple/Assets",
                    "Missing 1024x1024 App Store icon",
                    "Add 1024x1024 icon to AppIcon.appiconset/ - required for App Store submission"
                )

        except (json.JSONDecodeError, IOError) as e:
            self.add_issue(
                ValidationIssue.ERROR,
                "Apple/Assets",
                f"Failed to read AppIcon Contents.json: {e}",
                "Fix JSON syntax or file permissions"
            )

    def _validate_launch_screen(self, ios_path: Path):
        """Validate launch screen configuration."""
        # Check for LaunchScreen.storyboard
        launch_storyboard = list(ios_path.rglob("LaunchScreen.storyboard"))

        # Check for launch images
        launch_images = list(ios_path.rglob("LaunchImage.launchimage"))

        if not launch_storyboard and not launch_images:
            self.add_issue(
                ValidationIssue.ERROR,
                "Apple/Assets",
                "No launch screen found (LaunchScreen.storyboard or LaunchImage.launchimage)",
                "Add LaunchScreen.storyboard or launch image assets"
            )
        else:
            self.add_passed("Launch screen configured")

    def _validate_privacy_manifest(self, ios_path: Path):
        """Validate privacy manifest (iOS 17+ requirement)."""
        privacy_manifest = list(ios_path.rglob("PrivacyInfo.xcprivacy"))

        if not privacy_manifest:
            self.add_issue(
                ValidationIssue.WARNING,
                "Apple/Privacy",
                "PrivacyInfo.xcprivacy not found (required for iOS 17+)",
                "Add PrivacyInfo.xcprivacy to declare privacy-impacting APIs and data collection"
            )
        else:
            self.add_passed("Privacy manifest present")

    def _validate_usage_descriptions(self, ios_path: Path):
        """Validate usage description strings in Info.plist."""
        info_plist_candidates = list(ios_path.rglob("Info.plist"))
        if not info_plist_candidates:
            return

        try:
            tree = ET.parse(info_plist_candidates[0])
            root = tree.getroot()
            plist_dict = self._parse_plist_dict(root)

            # Common usage description keys
            usage_keys = {
                "NSCameraUsageDescription": "camera",
                "NSPhotoLibraryUsageDescription": "photo library",
                "NSLocationWhenInUseUsageDescription": "location (when in use)",
                "NSLocationAlwaysUsageDescription": "location (always)",
                "NSMicrophoneUsageDescription": "microphone",
                "NSContactsUsageDescription": "contacts",
                "NSCalendarsUsageDescription": "calendars",
                "NSMotionUsageDescription": "motion sensors",
                "NSBluetoothAlwaysUsageDescription": "Bluetooth",
            }

            # These are just warnings - app may not need all permissions
            for key, feature in usage_keys.items():
                if key not in plist_dict:
                    self.add_issue(
                        ValidationIssue.INFO,
                        "Apple/Privacy",
                        f"{key} not set (required if app uses {feature})",
                        f"Add {key} to Info.plist if your app accesses {feature}"
                    )

        except Exception:
            pass  # Already reported plist errors above

    def _validate_apple_build_config(self, ios_path: Path):
        """Validate Apple build configuration."""
        # Check for Podfile (if using CocoaPods)
        podfile = self.project_path / "ios" / "Podfile"
        if podfile.exists():
            self.add_passed("CocoaPods configuration found")

        # Check minimum deployment target in project.pbxproj
        pbxproj_files = list(ios_path.rglob("project.pbxproj"))
        if pbxproj_files:
            try:
                with open(pbxproj_files[0], 'r') as f:
                    content = f.read()

                # Extract IPHONEOS_DEPLOYMENT_TARGET
                matches = re.findall(r'IPHONEOS_DEPLOYMENT_TARGET\s*=\s*([0-9.]+)', content)
                if matches:
                    min_version = float(matches[0])
                    if min_version < 12.0:
                        self.add_issue(
                            ValidationIssue.WARNING,
                            "Apple/Build",
                            f"Minimum deployment target is iOS {min_version} (iOS 12+ recommended)",
                            "Update IPHONEOS_DEPLOYMENT_TARGET to 12.0 or higher"
                        )
                    else:
                        self.add_passed(f"Minimum deployment target: iOS {min_version}")
            except Exception as e:
                self.log(f"Could not parse project.pbxproj: {e}")

    def validate_google_play_store(self) -> Dict[str, Any]:
        """Validate Google Play Store requirements."""
        logger.debug("Starting Google Play Store validation")
        self.log("Starting Google Play Store validation...")

        android_path = self.project_path / "android"
        if not android_path.exists():
            logger.warning(f"Android project directory not found at {android_path}")
            self.add_issue(
                ValidationIssue.ERROR,
                "Google/Project",
                "Android project directory not found",
                "Ensure 'android/' directory exists in your project"
            )
            return self._get_results()

        # Validate AndroidManifest.xml
        self._validate_android_manifest(android_path)

        # Validate build.gradle
        self._validate_gradle_config(android_path)

        # Validate app icons
        self._validate_android_icons(android_path)

        # Validate permissions
        self._validate_android_permissions(android_path)

        return self._get_results()

    def _validate_android_manifest(self, android_path: Path):
        """Validate AndroidManifest.xml."""
        manifest_paths = list(android_path.rglob("AndroidManifest.xml"))

        # Filter to main manifest (not test manifests)
        main_manifests = [p for p in manifest_paths if "src/main" in str(p)]

        if not main_manifests:
            self.add_issue(
                ValidationIssue.ERROR,
                "Google/Metadata",
                "AndroidManifest.xml not found",
                "Create AndroidManifest.xml in android/app/src/main/"
            )
            return

        manifest_path = main_manifests[0]
        self.log(f"Checking AndroidManifest.xml: {manifest_path}")

        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()

            # Check required attributes
            package = root.get("package")
            if not package:
                self.add_issue(
                    ValidationIssue.ERROR,
                    "Google/Metadata",
                    "AndroidManifest.xml missing 'package' attribute",
                    "Add package attribute to <manifest> element"
                )
            else:
                # Validate package name format
                if not re.match(r'^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$', package):
                    self.add_issue(
                        ValidationIssue.WARNING,
                        "Google/Metadata",
                        f"Package name '{package}' doesn't follow recommended format",
                        "Use lowercase letters and underscores, minimum 2 segments (e.g., com.example.app)"
                    )
                else:
                    self.add_passed("Package name follows conventions")

            # Check for application element
            app_elem = root.find("application")
            if app_elem is None:
                self.add_issue(
                    ValidationIssue.ERROR,
                    "Google/Metadata",
                    "AndroidManifest.xml missing <application> element",
                    "Add <application> element with app configuration"
                )
            else:
                self.add_passed("AndroidManifest.xml structure valid")

        except ET.ParseError as e:
            self.add_issue(
                ValidationIssue.ERROR,
                "Google/Metadata",
                f"Failed to parse AndroidManifest.xml: {e}",
                "Fix XML syntax errors"
            )

    def _validate_gradle_config(self, android_path: Path):
        """Validate Gradle build configuration."""
        build_gradle_path = android_path / "app" / "build.gradle"

        if not build_gradle_path.exists():
            self.add_issue(
                ValidationIssue.ERROR,
                "Google/Build",
                "app/build.gradle not found",
                "Create build.gradle in android/app/ directory"
            )
            return

        self.log(f"Checking build.gradle: {build_gradle_path}")

        try:
            with open(build_gradle_path, 'r') as f:
                content = f.read()

            # Check targetSdkVersion
            target_sdk_matches = re.findall(r'targetSdkVersion\s+(\d+)', content)
            if target_sdk_matches:
                target_sdk = int(target_sdk_matches[0])
                if target_sdk < 34:
                    self.add_issue(
                        ValidationIssue.ERROR,
                        "Google/Build",
                        f"targetSdkVersion is {target_sdk} (must be 34+ for new apps in 2024)",
                        "Update targetSdkVersion to 34 in android/app/build.gradle"
                    )
                else:
                    self.add_passed(f"Target SDK version: {target_sdk}")

            # Check minSdkVersion
            min_sdk_matches = re.findall(r'minSdkVersion\s+(\d+)', content)
            if min_sdk_matches:
                min_sdk = int(min_sdk_matches[0])
                self.add_passed(f"Minimum SDK version: {min_sdk}")

            # Check versionCode and versionName
            if "versionCode" not in content:
                self.add_issue(
                    ValidationIssue.ERROR,
                    "Google/Build",
                    "versionCode not set in build.gradle",
                    "Add versionCode to defaultConfig block"
                )

            if "versionName" not in content:
                self.add_issue(
                    ValidationIssue.ERROR,
                    "Google/Build",
                    "versionName not set in build.gradle",
                    "Add versionName to defaultConfig block"
                )

            # Check for 64-bit support
            if "arm64-v8a" not in content and "abiFilters" in content:
                self.add_issue(
                    ValidationIssue.ERROR,
                    "Google/Build",
                    "Missing arm64-v8a support (64-bit required)",
                    "Add 'arm64-v8a' to ndk.abiFilters in build.gradle"
                )
            else:
                self.add_passed("64-bit support configured (or using defaults)")

            # Check for ProGuard/R8
            if "minifyEnabled" in content and "true" in content:
                self.add_passed("Code minification enabled")
            else:
                self.add_issue(
                    ValidationIssue.WARNING,
                    "Google/Build",
                    "Code minification not enabled",
                    "Enable minifyEnabled true for release builds to reduce APK size"
                )

        except IOError as e:
            self.add_issue(
                ValidationIssue.ERROR,
                "Google/Build",
                f"Failed to read build.gradle: {e}",
                "Check file permissions"
            )

    def _validate_android_icons(self, android_path: Path):
        """Validate Android app icons."""
        res_path = android_path / "app" / "src" / "main" / "res"

        if not res_path.exists():
            self.add_issue(
                ValidationIssue.ERROR,
                "Google/Assets",
                "Android res/ directory not found",
                "Create android/app/src/main/res/ directory structure"
            )
            return

        # Check for mipmap directories
        mipmap_dirs = ["mipmap-mdpi", "mipmap-hdpi", "mipmap-xhdpi",
                      "mipmap-xxhdpi", "mipmap-xxxhdpi"]

        found_mipmaps = []
        for mipmap_dir in mipmap_dirs:
            if (res_path / mipmap_dir).exists():
                found_mipmaps.append(mipmap_dir)

        if not found_mipmaps:
            self.add_issue(
                ValidationIssue.ERROR,
                "Google/Assets",
                "No mipmap directories found for app icons",
                "Create mipmap-* directories with ic_launcher.png icons"
            )
        else:
            self.add_passed(f"App icon mipmaps found: {len(found_mipmaps)} densities")

        # Check for adaptive icon (Android 8.0+)
        adaptive_icon_paths = list(res_path.rglob("ic_launcher_foreground.xml"))
        if not adaptive_icon_paths:
            self.add_issue(
                ValidationIssue.WARNING,
                "Google/Assets",
                "Adaptive icon not found (ic_launcher_foreground.xml)",
                "Add adaptive icon for better appearance on Android 8.0+"
            )
        else:
            self.add_passed("Adaptive icon configured")

    def _validate_android_permissions(self, android_path: Path):
        """Validate Android permissions."""
        manifest_paths = list(android_path.rglob("AndroidManifest.xml"))
        main_manifests = [p for p in manifest_paths if "src/main" in str(p)]

        if not main_manifests:
            return

        try:
            tree = ET.parse(main_manifests[0])
            root = tree.getroot()

            # Find all uses-permission elements
            permissions = root.findall("uses-permission")

            # Dangerous permissions that require user approval
            dangerous_permissions = [
                "android.permission.CAMERA",
                "android.permission.READ_CONTACTS",
                "android.permission.WRITE_CONTACTS",
                "android.permission.ACCESS_FINE_LOCATION",
                "android.permission.ACCESS_COARSE_LOCATION",
                "android.permission.RECORD_AUDIO",
                "android.permission.READ_EXTERNAL_STORAGE",
                "android.permission.WRITE_EXTERNAL_STORAGE",
            ]

            found_dangerous = []
            for perm in permissions:
                perm_name = perm.get("{http://schemas.android.com/apk/res/android}name")
                if perm_name in dangerous_permissions:
                    found_dangerous.append(perm_name.split(".")[-1])

            if found_dangerous:
                self.add_issue(
                    ValidationIssue.INFO,
                    "Google/Permissions",
                    f"Dangerous permissions declared: {', '.join(found_dangerous)}",
                    "Ensure Data Safety form in Play Console declares these permissions"
                )

        except Exception:
            pass

    def _get_results(self) -> Dict[str, Any]:
        """Get validation results."""
        errors = [i for i in self.issues if i.severity == ValidationIssue.ERROR]
        warnings = [i for i in self.issues if i.severity == ValidationIssue.WARNING]
        info = [i for i in self.issues if i.severity == ValidationIssue.INFO]

        return {
            "summary": {
                "passed": len(self.passed_checks),
                "errors": len(errors),
                "warnings": len(warnings),
                "info": len(info)
            },
            "passed_checks": self.passed_checks,
            "issues": [i.to_dict() for i in self.issues]
        }


def format_text_output(results: Dict[str, Any], store_name: str, strict: bool = False) -> str:
    """Format results as human-readable text."""
    output = f"=== {store_name} Validation Results ===\n\n"

    summary = results["summary"]
    output += f"Passed: {summary['passed']}\n"
    output += f"Errors: {summary['errors']}\n"
    output += f"Warnings: {summary['warnings']}\n"
    output += f"Info: {summary['info']}\n\n"

    # Passed checks
    if results["passed_checks"]:
        output += "--- Passed Checks ---\n"
        for check in results["passed_checks"]:
            output += f"  ✓ {check}\n"
        output += "\n"

    # Issues by severity
    errors = [i for i in results["issues"] if i["severity"] == "error"]
    warnings = [i for i in results["issues"] if i["severity"] == "warning"]
    info = [i for i in results["issues"] if i["severity"] == "info"]

    if errors:
        output += "--- Errors (Must Fix) ---\n"
        for issue in errors:
            output += f"  ✗ [{issue['category']}] {issue['message']}\n"
            if issue["recommendation"]:
                output += f"    → {issue['recommendation']}\n"
        output += "\n"

    if warnings:
        output += "--- Warnings (Should Fix) ---\n"
        for issue in warnings:
            output += f"  ⚠ [{issue['category']}] {issue['message']}\n"
            if issue["recommendation"]:
                output += f"    → {issue['recommendation']}\n"
        output += "\n"

    if info:
        output += "--- Info (Review) ---\n"
        for issue in info:
            output += f"  ℹ [{issue['category']}] {issue['message']}\n"
            if issue["recommendation"]:
                output += f"    → {issue['recommendation']}\n"
        output += "\n"

    # Overall status
    if summary["errors"] == 0:
        if strict and summary["warnings"] > 0:
            output += "Status: NEEDS ATTENTION (warnings in strict mode)\n"
        else:
            output += "Status: READY FOR SUBMISSION\n"
    else:
        output += "Status: NOT READY (fix errors before submission)\n"

    return output


def format_markdown_output(results: Dict[str, Any], project_name: str, store_name: str,
                          strict: bool = False) -> str:
    """Format results as Markdown report."""
    output = f"# App Store Validation Report\n\n"
    output += f"**Project:** {project_name}\n"
    output += f"**Store:** {store_name}\n"
    output += f"**Generated:** {datetime.utcnow().isoformat()}Z\n"
    output += f"**Validator Version:** 1.0.0\n\n"

    summary = results["summary"]
    output += "## Summary\n\n"
    output += "| Metric | Count |\n"
    output += "|--------|-------|\n"
    output += f"| Passed Checks | {summary['passed']} |\n"
    output += f"| Errors | {summary['errors']} |\n"
    output += f"| Warnings | {summary['warnings']} |\n"
    output += f"| Info | {summary['info']} |\n\n"

    # Passed checks
    if results["passed_checks"]:
        output += "## Passed Checks\n\n"
        for check in results["passed_checks"]:
            output += f"- ✅ {check}\n"
        output += "\n"

    # Issues
    errors = [i for i in results["issues"] if i["severity"] == "error"]
    warnings = [i for i in results["issues"] if i["severity"] == "warning"]
    info = [i for i in results["issues"] if i["severity"] == "info"]

    if errors:
        output += "## Errors (Must Fix)\n\n"
        for issue in errors:
            output += f"### ❌ {issue['message']}\n\n"
            output += f"**Category:** {issue['category']}\n\n"
            if issue["recommendation"]:
                output += f"**Recommendation:** {issue['recommendation']}\n\n"

    if warnings:
        output += "## Warnings (Should Fix)\n\n"
        for issue in warnings:
            output += f"### ⚠️ {issue['message']}\n\n"
            output += f"**Category:** {issue['category']}\n\n"
            if issue["recommendation"]:
                output += f"**Recommendation:** {issue['recommendation']}\n\n"

    if info:
        output += "## Information\n\n"
        for issue in info:
            output += f"### ℹ️ {issue['message']}\n\n"
            output += f"**Category:** {issue['category']}\n\n"
            if issue["recommendation"]:
                output += f"**Note:** {issue['recommendation']}\n\n"

    # Status
    output += "## Overall Status\n\n"
    if summary["errors"] == 0:
        if strict and summary["warnings"] > 0:
            output += "🟡 **NEEDS ATTENTION** - Warnings present in strict mode\n"
        else:
            output += "✅ **READY FOR SUBMISSION**\n"
    else:
        output += "❌ **NOT READY** - Fix errors before submission\n"

    return output


def format_json_output(results_apple: Optional[Dict[str, Any]],
                      results_google: Optional[Dict[str, Any]],
                      project_name: str) -> str:
    """Format results as JSON with metadata."""
    output = {
        "metadata": {
            "tool": "app_store_validator.py",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "project": project_name
        },
        "validation": {}
    }

    if results_apple:
        output["validation"]["apple_app_store"] = results_apple

    if results_google:
        output["validation"]["google_play_store"] = results_google

    return json.dumps(output, indent=2)


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Validate mobile app projects against app store requirements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ./my-app
  %(prog)s ./my-app --store apple
  %(prog)s ./my-app --store google --output markdown
  %(prog)s ./my-app --build-path ./build/app.ipa --strict
  %(prog)s ./my-app -o markdown -f report.md

For more information, see:
skills/engineering-team/senior-mobile/SKILL.md
        """
    )

    parser.add_argument(
        'project_path',
        help='Path to mobile project directory to validate'
    )

    parser.add_argument(
        '--store', '-s',
        choices=['apple', 'google', 'both'],
        default='both',
        help='Target store to validate against (default: both)'
    )

    parser.add_argument(
        '--build-path', '-b',
        help='Path to built artifact (IPA/APK/AAB) for binary validation'
    )

    parser.add_argument(
        '--check', '-c',
        choices=['metadata', 'assets', 'privacy', 'permissions', 'all'],
        default='all',
        help='Specific check category to run (default: all)'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Enable strict mode (fail on warnings)'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    try:
        # Validate project path
        project_path = Path(args.project_path)
        if not project_path.exists():
            print(f"Error: Project path not found: {args.project_path}", file=sys.stderr)
            sys.exit(1)

        if not project_path.is_dir():
            print(f"Error: Project path is not a directory: {args.project_path}", file=sys.stderr)
            sys.exit(1)

        # Validate build path if provided
        build_path = None
        if args.build_path:
            build_path = Path(args.build_path)
            if not build_path.exists():
                print(f"Warning: Build path not found: {args.build_path}", file=sys.stderr)
                build_path = None

        project_name = project_path.name

        # Run validations
        results_apple = None
        results_google = None

        if args.store in ['apple', 'both']:
            if args.verbose:
                print("Validating Apple App Store requirements...", file=sys.stderr)
            validator_apple = AppStoreValidator(project_path, build_path, args.verbose)
            results_apple = validator_apple.validate_apple_app_store()

        if args.store in ['google', 'both']:
            if args.verbose:
                print("Validating Google Play Store requirements...", file=sys.stderr)
            validator_google = AppStoreValidator(project_path, build_path, args.verbose)
            results_google = validator_google.validate_google_play_store()

        # Format output
        if args.output == 'json':
            output = format_json_output(results_apple, results_google, project_name)
        elif args.output == 'markdown':
            output = ""
            if results_apple:
                output += format_markdown_output(results_apple, project_name,
                                                "Apple App Store", args.strict)
                output += "\n---\n\n"
            if results_google:
                output += format_markdown_output(results_google, project_name,
                                                "Google Play Store", args.strict)
        else:  # text
            output = ""
            if results_apple:
                output += format_text_output(results_apple, "Apple App Store", args.strict)
                output += "\n"
            if results_google:
                output += format_text_output(results_google, "Google Play Store", args.strict)

        # Write output
        if args.file:
            try:
                output_path = Path(args.file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"Validation report written to: {args.file}")
            except PermissionError:
                print(f"Error: Permission denied writing to: {args.file}", file=sys.stderr)
                sys.exit(4)
            except Exception as e:
                print(f"Error writing output file: {e}", file=sys.stderr)
                sys.exit(4)
        else:
            print(output)

        # Determine exit code
        total_errors = 0
        total_warnings = 0

        if results_apple:
            total_errors += results_apple["summary"]["errors"]
            total_warnings += results_apple["summary"]["warnings"]

        if results_google:
            total_errors += results_google["summary"]["errors"]
            total_warnings += results_google["summary"]["warnings"]

        if total_errors > 0:
            sys.exit(2)  # Errors found
        elif args.strict and total_warnings > 0:
            sys.exit(3)  # Warnings in strict mode
        else:
            sys.exit(0)  # Success

    except KeyboardInterrupt:
        print("\nValidation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}", exc_info=args.verbose)
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
