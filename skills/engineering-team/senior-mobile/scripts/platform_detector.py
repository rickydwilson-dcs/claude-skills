#!/usr/bin/env python3
"""
Module: platform_detector.py
Description: Analyze mobile projects to detect platform capabilities, dependencies, and configuration.

Detects project type (React Native, Flutter, Expo, Native iOS/Android), analyzes platform
configurations, identifies capabilities, and provides actionable recommendations for mobile
development projects.

Usage:
    python platform_detector.py /path/to/project
    python platform_detector.py /path/to/project --check ios
    python platform_detector.py /path/to/project --depth deep -o json
    python platform_detector.py /path/to/project -o json -f report.json

Author: Claude Skills - Senior Mobile
Version: 1.0.0
Last Updated: 2025-12-13
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone


class PlatformDetector:
    """Analyzes mobile projects for platform capabilities and configuration."""

    def __init__(self, project_path: str, depth: str = "standard"):
        """
        Initialize the detector.

        Args:
            project_path: Path to the mobile project
            depth: Analysis depth (quick, standard, deep)
        """
        self.project_path = Path(project_path).resolve()
        self.depth = depth
        self.results = {
            "project_type": None,
            "framework_version": None,
            "platforms": {},
            "shared_code_percentage": 0,
            "native_modules": [],
            "dependencies": {"total": 0, "outdated": 0, "vulnerable": 0},
            "recommendations": []
        }

    def detect(self, check_types: List[str] = None) -> Dict[str, Any]:
        """
        Run detection analysis.

        Args:
            check_types: List of checks to run (ios, android, dependencies, config, all)

        Returns:
            Detection results dictionary
        """
        if check_types is None or "all" in check_types:
            check_types = ["ios", "android", "dependencies", "config"]

        # Detect project type first
        self._detect_project_type()

        # Run requested checks
        if "ios" in check_types:
            self._analyze_ios()

        if "android" in check_types:
            self._analyze_android()

        if "dependencies" in check_types:
            self._analyze_dependencies()

        if "config" in check_types:
            self._analyze_configuration()

        # Calculate shared code percentage
        self._calculate_shared_code()

        # Generate recommendations
        self._generate_recommendations()

        return self.results

    def _detect_project_type(self):
        """Detect the type of mobile project."""
        # Check for React Native
        package_json = self.project_path / "package.json"
        if package_json.exists():
            package_data = self._read_json(package_json)
            if package_data:
                deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}

                if "expo" in deps or (self.project_path / "app.json").exists():
                    self.results["project_type"] = "expo"
                    self.results["framework_version"] = deps.get("expo", "unknown")
                elif "react-native" in deps:
                    self.results["project_type"] = "react-native"
                    self.results["framework_version"] = deps.get("react-native", "unknown")

        # Check for Flutter
        pubspec = self.project_path / "pubspec.yaml"
        if pubspec.exists():
            self.results["project_type"] = "flutter"
            version = self._extract_flutter_version(pubspec)
            if version:
                self.results["framework_version"] = version

        # Check for Native iOS
        if not self.results["project_type"]:
            if list(self.project_path.glob("*.xcodeproj")) or list(self.project_path.glob("*.xcworkspace")):
                self.results["project_type"] = "native-ios"

        # Check for Native Android
        if not self.results["project_type"]:
            if (self.project_path / "app" / "build.gradle").exists() or (self.project_path / "build.gradle").exists():
                self.results["project_type"] = "native-android"

        if not self.results["project_type"]:
            self.results["project_type"] = "unknown"

    def _analyze_ios(self):
        """Analyze iOS platform configuration."""
        ios_config = {
            "status": "not_configured",
            "min_version": None,
            "swift_version": None,
            "language_ratio": {},
            "capabilities": [],
            "signing": None,
            "package_manager": None,
            "issues": []
        }

        # Look for iOS directory
        ios_paths = [
            self.project_path / "ios",
            self.project_path / "app" / "ios",
            self.project_path
        ]

        ios_dir = None
        for path in ios_paths:
            if path.exists() and (list(path.glob("*.xcodeproj")) or list(path.glob("*.xcworkspace"))):
                ios_dir = path
                break

        if not ios_dir:
            self.results["platforms"]["ios"] = ios_config
            return

        ios_config["status"] = "configured"

        # Analyze Info.plist
        info_plist = self._find_file(ios_dir, "Info.plist")
        if info_plist:
            ios_config["capabilities"].extend(self._extract_ios_capabilities(info_plist))
        else:
            ios_config["issues"].append("Info.plist not found")

        # Check for Podfile (CocoaPods)
        if (ios_dir / "Podfile").exists():
            ios_config["package_manager"] = "cocoapods"
            min_version = self._extract_ios_min_version(ios_dir / "Podfile")
            if min_version:
                ios_config["min_version"] = min_version

        # Check for Package.swift (SPM)
        if (ios_dir / "Package.swift").exists():
            ios_config["package_manager"] = "spm"

        # Analyze Swift/Objective-C ratio
        if self.depth in ["standard", "deep"]:
            ios_config["language_ratio"] = self._calculate_language_ratio(ios_dir, [".swift", ".m", ".mm"])

        # Check signing configuration
        pbxproj = self._find_file(ios_dir, "project.pbxproj")
        if pbxproj:
            signing = self._extract_signing_config(pbxproj)
            ios_config["signing"] = signing
            if not signing or signing == "manual-missing":
                ios_config["issues"].append("Signing configuration incomplete")

        self.results["platforms"]["ios"] = ios_config

    def _analyze_android(self):
        """Analyze Android platform configuration."""
        android_config = {
            "status": "not_configured",
            "min_sdk": None,
            "target_sdk": None,
            "compile_sdk": None,
            "kotlin_version": None,
            "language_ratio": {},
            "signing": None,
            "issues": []
        }

        # Look for Android directory
        android_paths = [
            self.project_path / "android",
            self.project_path / "app" / "android",
            self.project_path
        ]

        android_dir = None
        for path in android_paths:
            if path.exists() and ((path / "app" / "build.gradle").exists() or (path / "build.gradle").exists()):
                android_dir = path
                break

        if not android_dir:
            self.results["platforms"]["android"] = android_config
            return

        android_config["status"] = "configured"

        # Analyze build.gradle
        build_gradle = android_dir / "app" / "build.gradle"
        if not build_gradle.exists():
            build_gradle = android_dir / "build.gradle"

        if build_gradle.exists():
            gradle_data = self._parse_build_gradle(build_gradle)
            android_config.update(gradle_data)

        # Check AndroidManifest.xml
        manifest = self._find_file(android_dir, "AndroidManifest.xml")
        if not manifest:
            android_config["issues"].append("AndroidManifest.xml not found")

        # Analyze Kotlin/Java ratio
        if self.depth in ["standard", "deep"]:
            android_config["language_ratio"] = self._calculate_language_ratio(android_dir, [".kt", ".java"])

        # Check signing configuration
        signing = self._check_android_signing(android_dir)
        android_config["signing"] = signing
        if signing == "missing-release-key":
            android_config["issues"].append("Missing release signing configuration")

        self.results["platforms"]["android"] = android_config

    def _analyze_dependencies(self):
        """Analyze project dependencies."""
        if self.results["project_type"] in ["react-native", "expo"]:
            self._analyze_npm_dependencies()
        elif self.results["project_type"] == "flutter":
            self._analyze_flutter_dependencies()

    def _analyze_npm_dependencies(self):
        """Analyze npm dependencies for React Native/Expo."""
        package_json = self.project_path / "package.json"
        if not package_json.exists():
            return

        package_data = self._read_json(package_json)
        if not package_data:
            return

        deps = package_data.get("dependencies", {})
        dev_deps = package_data.get("devDependencies", {})
        all_deps = {**deps, **dev_deps}

        self.results["dependencies"]["total"] = len(all_deps)

        # Identify native modules
        native_modules = []
        for dep_name in all_deps.keys():
            if (self._is_native_module(dep_name) and
                dep_name not in ["react", "react-native", "expo"]):
                native_modules.append(dep_name)

        self.results["native_modules"] = sorted(native_modules)

        # Check for outdated dependencies (basic heuristic)
        if self.depth == "deep":
            self.results["dependencies"]["outdated"] = self._count_outdated_deps(all_deps)

    def _analyze_flutter_dependencies(self):
        """Analyze Flutter dependencies."""
        pubspec = self.project_path / "pubspec.yaml"
        if not pubspec.exists():
            return

        content = pubspec.read_text(encoding="utf-8")

        # Simple dependency counting
        deps = re.findall(r'^\s{2}[\w_]+:', content, re.MULTILINE)
        self.results["dependencies"]["total"] = len(deps)

        # Identify plugin dependencies
        plugins = []
        for match in re.finditer(r'^\s{2}([\w_]+):', content, re.MULTILINE):
            dep_name = match.group(1)
            if dep_name not in ["flutter", "cupertino_icons"]:
                plugins.append(dep_name)

        self.results["native_modules"] = sorted(plugins)

    def _analyze_configuration(self):
        """Analyze overall project configuration."""
        # This is a placeholder for additional configuration checks
        pass

    def _calculate_shared_code(self):
        """Calculate the percentage of shared vs platform-specific code."""
        if self.depth == "quick":
            self.results["shared_code_percentage"] = 0
            return

        total_files = 0
        platform_specific = 0

        for root, dirs, files in os.walk(self.project_path):
            # Skip node_modules, build directories, etc.
            dirs[:] = [d for d in dirs if d not in ["node_modules", "build", "Pods", ".git", "android", "ios"]]

            for file in files:
                if file.endswith((".js", ".jsx", ".ts", ".tsx", ".dart")):
                    total_files += 1

                    # Check for platform-specific files
                    if any(p in file for p in [".ios.", ".android.", ".native."]):
                        platform_specific += 1

        if total_files > 0:
            shared_percentage = int(((total_files - platform_specific) / total_files) * 100)
            self.results["shared_code_percentage"] = shared_percentage
        else:
            self.results["shared_code_percentage"] = 0

    def _generate_recommendations(self):
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        # iOS recommendations
        if "ios" in self.results["platforms"]:
            ios_config = self.results["platforms"]["ios"]
            if ios_config["issues"]:
                for issue in ios_config["issues"]:
                    recommendations.append(f"iOS: {issue}")

        # Android recommendations
        if "android" in self.results["platforms"]:
            android_config = self.results["platforms"]["android"]
            if android_config["issues"]:
                for issue in android_config["issues"]:
                    recommendations.append(f"Android: {issue}")

        # Dependency recommendations
        if self.results["dependencies"]["outdated"] > 0:
            recommendations.append(
                f"Update {self.results['dependencies']['outdated']} outdated dependencies"
            )

        # Native module recommendations
        if len(self.results["native_modules"]) > 10:
            recommendations.append(
                f"Consider reviewing {len(self.results['native_modules'])} native modules for potential consolidation"
            )

        self.results["recommendations"] = recommendations

    # Helper methods

    def _read_json(self, file_path: Path) -> Optional[Dict]:
        """Read and parse JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def _find_file(self, directory: Path, filename: str) -> Optional[Path]:
        """Find a file recursively in directory."""
        for root, dirs, files in os.walk(directory):
            # Skip common build directories
            dirs[:] = [d for d in dirs if d not in ["node_modules", "build", "Pods", ".git"]]

            if filename in files:
                return Path(root) / filename
        return None

    def _extract_flutter_version(self, pubspec_path: Path) -> Optional[str]:
        """Extract Flutter SDK version from pubspec.yaml."""
        try:
            content = pubspec_path.read_text(encoding='utf-8')
            match = re.search(r'sdk:\s*["\']>=?([\d.]+)', content)
            return match.group(1) if match else None
        except IOError:
            return None

    def _extract_ios_capabilities(self, info_plist_path: Path) -> List[str]:
        """Extract iOS capabilities from Info.plist."""
        capabilities = []
        try:
            content = info_plist_path.read_text(encoding='utf-8')

            # Look for common capability keys
            capability_keys = {
                "NSLocationWhenInUseUsageDescription": "location",
                "NSCameraUsageDescription": "camera",
                "NSPhotoLibraryUsageDescription": "photo-library",
                "NSMicrophoneUsageDescription": "microphone",
                "NSContactsUsageDescription": "contacts",
                "UIBackgroundModes": "background-modes"
            }

            for key, capability in capability_keys.items():
                if key in content:
                    capabilities.append(capability)

        except IOError:
            pass

        return capabilities

    def _extract_ios_min_version(self, podfile_path: Path) -> Optional[str]:
        """Extract iOS minimum version from Podfile."""
        try:
            content = podfile_path.read_text(encoding='utf-8')
            match = re.search(r"platform\s+:ios,\s*['\"]([0-9.]+)['\"]", content)
            return match.group(1) if match else None
        except IOError:
            return None

    def _extract_signing_config(self, pbxproj_path: Path) -> Optional[str]:
        """Extract signing configuration from project.pbxproj."""
        try:
            content = pbxproj_path.read_text(encoding='utf-8')

            if "CODE_SIGN_STYLE = Automatic" in content:
                return "automatic"
            elif "CODE_SIGN_STYLE = Manual" in content:
                return "manual"
            elif "CODE_SIGN_IDENTITY" in content:
                return "configured"
            else:
                return "manual-missing"
        except IOError:
            return None

    def _parse_build_gradle(self, gradle_path: Path) -> Dict[str, Any]:
        """Parse Android build.gradle file."""
        config = {
            "min_sdk": None,
            "target_sdk": None,
            "compile_sdk": None,
            "kotlin_version": None
        }

        try:
            content = gradle_path.read_text(encoding='utf-8')

            # Extract SDK versions
            min_sdk_match = re.search(r'minSdkVersion\s+(\d+)', content)
            if min_sdk_match:
                config["min_sdk"] = int(min_sdk_match.group(1))

            target_sdk_match = re.search(r'targetSdkVersion\s+(\d+)', content)
            if target_sdk_match:
                config["target_sdk"] = int(target_sdk_match.group(1))

            compile_sdk_match = re.search(r'compileSdkVersion\s+(\d+)', content)
            if compile_sdk_match:
                config["compile_sdk"] = int(compile_sdk_match.group(1))

            # Extract Kotlin version
            kotlin_match = re.search(r'kotlin[_-]version\s*=\s*["\']([^"\']+)["\']', content)
            if kotlin_match:
                config["kotlin_version"] = kotlin_match.group(1)

        except IOError:
            pass

        return config

    def _check_android_signing(self, android_dir: Path) -> str:
        """Check Android signing configuration."""
        gradle_file = android_dir / "app" / "build.gradle"
        if not gradle_file.exists():
            return "not-configured"

        try:
            content = gradle_file.read_text(encoding='utf-8')

            if "signingConfigs" in content and "release" in content:
                return "configured"
            else:
                return "missing-release-key"
        except IOError:
            return "not-configured"

    def _calculate_language_ratio(self, directory: Path, extensions: List[str]) -> Dict[str, int]:
        """Calculate the ratio of different language files."""
        counts = {ext.lstrip('.'): 0 for ext in extensions}
        total = 0

        for root, dirs, files in os.walk(directory):
            # Skip build directories
            dirs[:] = [d for d in dirs if d not in ["node_modules", "build", "Pods", ".git", "DerivedData"]]

            for file in files:
                for ext in extensions:
                    if file.endswith(ext):
                        counts[ext.lstrip('.')] += 1
                        total += 1

        # Convert to percentages
        if total > 0:
            return {lang: int((count / total) * 100) for lang, count in counts.items() if count > 0}
        else:
            return {}

    def _is_native_module(self, dep_name: str) -> bool:
        """Check if a dependency is likely a native module."""
        native_indicators = [
            "react-native-",
            "@react-native",
            "expo-",
            "@expo/",
            "native"
        ]
        return any(indicator in dep_name for indicator in native_indicators)

    def _count_outdated_deps(self, dependencies: Dict[str, str]) -> int:
        """
        Count potentially outdated dependencies.
        This is a basic heuristic - in production, you'd use npm outdated or similar.
        """
        outdated = 0
        for version in dependencies.values():
            # Very simple heuristic: versions with ^ or ~ might be outdated
            if version.startswith(("^", "~")):
                outdated += 1
        return min(outdated, len(dependencies) // 10)  # Cap at 10% for estimate


def format_text_output(results: Dict[str, Any], verbose: bool = False) -> str:
    """
    Format results as human-readable text.

    Args:
        results: Detection results dictionary
        verbose: Include detailed information if True

    Returns:
        Formatted text output
    """
    output = ["=" * 60]
    output.append("Mobile Platform Detection Report")
    output.append("=" * 60)
    output.append("")

    # Project type
    output.append(f"Project Type: {results['project_type']}")
    if results['framework_version']:
        output.append(f"Framework Version: {results['framework_version']}")
    output.append("")

    # iOS platform
    if "ios" in results["platforms"]:
        ios = results["platforms"]["ios"]
        output.append("iOS Configuration")
        output.append("-" * 40)
        output.append(f"  Status: {ios['status']}")
        if ios['min_version']:
            output.append(f"  Minimum Version: {ios['min_version']}")
        if ios['package_manager']:
            output.append(f"  Package Manager: {ios['package_manager']}")
        if ios['signing']:
            output.append(f"  Signing: {ios['signing']}")
        if ios['capabilities']:
            output.append(f"  Capabilities: {', '.join(ios['capabilities'])}")
        if ios['language_ratio']:
            output.append(f"  Languages: {ios['language_ratio']}")
        if ios['issues']:
            output.append(f"  Issues: {len(ios['issues'])}")
            if verbose:
                for issue in ios['issues']:
                    output.append(f"    - {issue}")
        output.append("")

    # Android platform
    if "android" in results["platforms"]:
        android = results["platforms"]["android"]
        output.append("Android Configuration")
        output.append("-" * 40)
        output.append(f"  Status: {android['status']}")
        if android['min_sdk']:
            output.append(f"  Min SDK: {android['min_sdk']}")
        if android['target_sdk']:
            output.append(f"  Target SDK: {android['target_sdk']}")
        if android['compile_sdk']:
            output.append(f"  Compile SDK: {android['compile_sdk']}")
        if android['signing']:
            output.append(f"  Signing: {android['signing']}")
        if android['language_ratio']:
            output.append(f"  Languages: {android['language_ratio']}")
        if android['issues']:
            output.append(f"  Issues: {len(android['issues'])}")
            if verbose:
                for issue in android['issues']:
                    output.append(f"    - {issue}")
        output.append("")

    # Dependencies
    output.append("Dependencies")
    output.append("-" * 40)
    output.append(f"  Total: {results['dependencies']['total']}")
    if results['dependencies']['outdated'] > 0:
        output.append(f"  Outdated: {results['dependencies']['outdated']}")
    if results['dependencies']['vulnerable'] > 0:
        output.append(f"  Vulnerable: {results['dependencies']['vulnerable']}")
    output.append("")

    # Native modules
    if results['native_modules']:
        output.append(f"Native Modules: {len(results['native_modules'])}")
        if verbose:
            for module in results['native_modules'][:10]:  # Show first 10
                output.append(f"  - {module}")
            if len(results['native_modules']) > 10:
                output.append(f"  ... and {len(results['native_modules']) - 10} more")
        output.append("")

    # Shared code
    if results['shared_code_percentage'] > 0:
        output.append(f"Shared Code: {results['shared_code_percentage']}%")
        output.append("")

    # Recommendations
    if results['recommendations']:
        output.append("Recommendations")
        output.append("-" * 40)
        for rec in results['recommendations']:
            output.append(f"  • {rec}")
        output.append("")

    return "\n".join(output)


def format_json_output(results: Dict[str, Any], project_path: str) -> str:
    """
    Format results as JSON with metadata.

    Args:
        results: Detection results dictionary
        project_path: Path to the analyzed project

    Returns:
        JSON-formatted string
    """
    output = {
        "metadata": {
            "tool": "platform_detector.py",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "project_path": str(Path(project_path).resolve())
        },
        **results
    }

    return json.dumps(output, indent=2)


def format_csv_output(results: Dict[str, Any]) -> str:
    """
    Format results as CSV.

    Args:
        results: Detection results dictionary

    Returns:
        CSV-formatted string
    """
    lines = ["Category,Key,Value"]

    # Project info
    lines.append(f"Project,Type,{results['project_type']}")
    lines.append(f"Project,Framework Version,{results.get('framework_version', 'N/A')}")

    # iOS
    if "ios" in results["platforms"]:
        ios = results["platforms"]["ios"]
        lines.append(f"iOS,Status,{ios['status']}")
        lines.append(f"iOS,Min Version,{ios.get('min_version', 'N/A')}")
        lines.append(f"iOS,Signing,{ios.get('signing', 'N/A')}")
        lines.append(f"iOS,Issues,{len(ios['issues'])}")

    # Android
    if "android" in results["platforms"]:
        android = results["platforms"]["android"]
        lines.append(f"Android,Status,{android['status']}")
        lines.append(f"Android,Min SDK,{android.get('min_sdk', 'N/A')}")
        lines.append(f"Android,Target SDK,{android.get('target_sdk', 'N/A')}")
        lines.append(f"Android,Issues,{len(android['issues'])}")

    # Dependencies
    lines.append(f"Dependencies,Total,{results['dependencies']['total']}")
    lines.append(f"Dependencies,Outdated,{results['dependencies']['outdated']}")
    lines.append(f"Dependencies,Native Modules,{len(results['native_modules'])}")

    # Shared code
    lines.append(f"Code,Shared Percentage,{results['shared_code_percentage']}")

    return "\n".join(lines)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze mobile projects to detect platform capabilities and configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze entire project
  python platform_detector.py /path/to/project

  # Check only iOS configuration
  python platform_detector.py /path/to/project --check ios

  # Deep analysis with JSON output
  python platform_detector.py /path/to/project --depth deep -o json

  # Save report to file
  python platform_detector.py /path/to/project -o json -f report.json

  # Verbose text output
  python platform_detector.py /path/to/project -v
        """
    )

    parser.add_argument(
        "project_path",
        help="Path to the mobile project to analyze"
    )

    parser.add_argument(
        "--check", "-c",
        nargs="+",
        choices=["ios", "android", "dependencies", "config", "all"],
        default=["all"],
        help="Specific checks to run (default: all)"
    )

    parser.add_argument(
        "--depth",
        choices=["quick", "standard", "deep"],
        default="standard",
        help="Analysis depth (default: standard)"
    )

    parser.add_argument(
        "--output", "-o",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--file", "-f",
        help="Write output to file"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    # Validate project path
    if not Path(args.project_path).exists():
        print(f"Error: Project path does not exist: {args.project_path}", file=sys.stderr)
        sys.exit(1)

    try:
        # Run detection
        detector = PlatformDetector(args.project_path, depth=args.depth)
        results = detector.detect(check_types=args.check)

        # Format output
        if args.output == "json":
            output = format_json_output(results, args.project_path)
        elif args.output == "csv":
            output = format_csv_output(results)
        else:  # text
            output = format_text_output(results, verbose=args.verbose)

        # Write output
        if args.file:
            Path(args.file).write_text(output, encoding='utf-8')
            print(f"Report saved to: {args.file}")
        else:
            print(output)

        # Exit with appropriate code
        has_issues = any(
            platform.get("issues", [])
            for platform in results["platforms"].values()
        )
        sys.exit(1 if has_issues else 0)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
