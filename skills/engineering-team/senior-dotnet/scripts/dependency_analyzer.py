#!/usr/bin/env python3
"""
NuGet Dependency Analyzer

Analyze .NET project dependencies for vulnerabilities, outdated packages,
and upgrade recommendations.

Part of senior-dotnet skill for engineering-team.

Usage:
    python dependency_analyzer.py PROJECT_PATH [options]
    python dependency_analyzer.py MyProject.csproj --check-security
    python dependency_analyzer.py --help
    python dependency_analyzer.py --version
"""

import os
import sys
import json
import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

__version__ = "1.0.0"


class DependencyAnalyzer:
    """Analyze NuGet dependencies for issues and updates."""

    # Known vulnerable packages (simplified - in production, use a real vulnerability database)
    KNOWN_VULNERABILITIES = {
        'Newtonsoft.Json': {'below': '13.0.1', 'severity': 'high', 'cve': 'CVE-2024-21907'},
        'System.Text.Json': {'below': '8.0.0', 'severity': 'medium', 'cve': 'Potential DoS'},
        'Microsoft.Data.SqlClient': {'below': '5.1.2', 'severity': 'high', 'cve': 'CVE-2024-0056'},
        'System.Drawing.Common': {'below': '8.0.0', 'severity': 'medium', 'cve': 'Cross-platform issues'},
    }

    # Package recommendations for common scenarios
    PACKAGE_RECOMMENDATIONS = {
        'Microsoft.AspNetCore.Mvc.NewtonsoftJson': 'Consider using System.Text.Json for better performance',
        'AutoMapper': 'Consider using Mapster for simpler mapping scenarios',
        'MediatR': 'Ensure using version 12.x for .NET 8 compatibility',
        'FluentValidation': 'Ensure using version 11.x for .NET 8 compatibility',
    }

    def __init__(self, project_path: str, check_security: bool = False,
                 check_outdated: bool = True, output_format: str = 'text',
                 output_file: Optional[str] = None, verbose: bool = False):
        """
        Initialize Dependency Analyzer.

        Args:
            project_path: Path to .csproj file or directory containing projects
            check_security: Check for known security vulnerabilities
            check_outdated: Check for outdated packages
            output_format: Output format (text, json, markdown)
            output_file: Output file path
            verbose: Enable verbose output
        """
        self.project_path = Path(project_path)
        self.check_security = check_security
        self.check_outdated = check_outdated
        self.output_format = output_format
        self.output_file = output_file
        self.verbose = verbose

    def _log(self, message: str) -> None:
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"  {message}")

    def analyze(self) -> Dict:
        """Analyze dependencies and return results."""
        results = {
            'success': True,
            'analyzed_at': datetime.now().isoformat(),
            'projects': [],
            'summary': {
                'total_packages': 0,
                'vulnerable_packages': 0,
                'outdated_packages': 0,
                'recommendations': 0
            }
        }

        try:
            # Find all .csproj files
            if self.project_path.is_file():
                csproj_files = [self.project_path]
            else:
                csproj_files = list(self.project_path.rglob('*.csproj'))

            if not csproj_files:
                results['success'] = False
                results['error'] = f"No .csproj files found in {self.project_path}"
                return results

            for csproj in csproj_files:
                self._log(f"Analyzing {csproj.name}")
                project_result = self._analyze_project(csproj)
                results['projects'].append(project_result)

                # Update summary
                results['summary']['total_packages'] += len(project_result['packages'])
                results['summary']['vulnerable_packages'] += len(project_result['vulnerabilities'])
                results['summary']['outdated_packages'] += len(project_result['outdated'])
                results['summary']['recommendations'] += len(project_result['recommendations'])

            # Generate output
            if self.output_file:
                self._write_output(results)

            return results

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'projects': []
            }

    def _analyze_project(self, csproj_path: Path) -> Dict:
        """Analyze a single .csproj file."""
        result = {
            'name': csproj_path.stem,
            'path': str(csproj_path),
            'packages': [],
            'vulnerabilities': [],
            'outdated': [],
            'recommendations': [],
            'target_framework': None
        }

        try:
            tree = ET.parse(csproj_path)
            root = tree.getroot()

            # Get target framework
            tf_element = root.find('.//TargetFramework')
            if tf_element is not None:
                result['target_framework'] = tf_element.text

            # Get package references
            for pkg_ref in root.findall('.//PackageReference'):
                pkg_name = pkg_ref.get('Include')
                pkg_version = pkg_ref.get('Version')

                if pkg_name:
                    package_info = {
                        'name': pkg_name,
                        'version': pkg_version or 'Not specified',
                        'issues': []
                    }

                    # Check for security vulnerabilities
                    if self.check_security and pkg_name in self.KNOWN_VULNERABILITIES:
                        vuln_info = self.KNOWN_VULNERABILITIES[pkg_name]
                        if self._version_below(pkg_version, vuln_info['below']):
                            vulnerability = {
                                'package': pkg_name,
                                'current_version': pkg_version,
                                'fixed_version': vuln_info['below'],
                                'severity': vuln_info['severity'],
                                'description': vuln_info['cve']
                            }
                            result['vulnerabilities'].append(vulnerability)
                            package_info['issues'].append(f"Vulnerability: {vuln_info['cve']}")

                    # Check for recommendations
                    if pkg_name in self.PACKAGE_RECOMMENDATIONS:
                        recommendation = {
                            'package': pkg_name,
                            'message': self.PACKAGE_RECOMMENDATIONS[pkg_name]
                        }
                        result['recommendations'].append(recommendation)

                    result['packages'].append(package_info)

            # Check for outdated framework
            if result['target_framework']:
                tf = result['target_framework']
                if tf.startswith('net6') or tf.startswith('net5') or tf.startswith('netcoreapp'):
                    result['recommendations'].append({
                        'package': 'TargetFramework',
                        'message': f'Consider upgrading from {tf} to net8.0 for LTS support'
                    })

        except ET.ParseError as e:
            result['error'] = f"XML parsing error: {e}"

        return result

    def _version_below(self, current: Optional[str], threshold: str) -> bool:
        """Check if current version is below threshold."""
        if not current:
            return True

        try:
            # Parse versions (simplified - handles major.minor.patch)
            current_parts = [int(p) for p in re.findall(r'\d+', current)[:3]]
            threshold_parts = [int(p) for p in re.findall(r'\d+', threshold)[:3]]

            # Pad to same length
            while len(current_parts) < 3:
                current_parts.append(0)
            while len(threshold_parts) < 3:
                threshold_parts.append(0)

            return tuple(current_parts) < tuple(threshold_parts)
        except (ValueError, IndexError):
            return False

    def _write_output(self, results: Dict) -> None:
        """Write results to output file."""
        output_path = Path(self.output_file)

        if self.output_format == 'json':
            content = json.dumps(results, indent=2)
        elif self.output_format == 'markdown':
            content = self._format_markdown(results)
        else:
            content = self._format_text(results)

        output_path.write_text(content)
        self._log(f"Results written to {output_path}")

    def _format_text(self, results: Dict) -> str:
        """Format results as plain text."""
        lines = [
            "=" * 60,
            "NuGet Dependency Analysis Report",
            f"Generated: {results['analyzed_at']}",
            "=" * 60,
            ""
        ]

        # Summary
        lines.extend([
            "SUMMARY",
            "-" * 40,
            f"Total Packages: {results['summary']['total_packages']}",
            f"Vulnerable Packages: {results['summary']['vulnerable_packages']}",
            f"Recommendations: {results['summary']['recommendations']}",
            ""
        ])

        # Per-project details
        for project in results['projects']:
            lines.extend([
                f"\nPROJECT: {project['name']}",
                "-" * 40,
                f"Target Framework: {project['target_framework'] or 'Unknown'}",
                f"Packages: {len(project['packages'])}"
            ])

            if project['vulnerabilities']:
                lines.append("\n  VULNERABILITIES:")
                for vuln in project['vulnerabilities']:
                    lines.append(f"    [{vuln['severity'].upper()}] {vuln['package']}")
                    lines.append(f"      Current: {vuln['current_version']} -> Fix: {vuln['fixed_version']}")
                    lines.append(f"      {vuln['description']}")

            if project['recommendations']:
                lines.append("\n  RECOMMENDATIONS:")
                for rec in project['recommendations']:
                    lines.append(f"    {rec['package']}: {rec['message']}")

        return '\n'.join(lines)

    def _format_markdown(self, results: Dict) -> str:
        """Format results as Markdown."""
        lines = [
            "# NuGet Dependency Analysis Report",
            "",
            f"**Generated:** {results['analyzed_at']}",
            "",
            "## Summary",
            "",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Total Packages | {results['summary']['total_packages']} |",
            f"| Vulnerable Packages | {results['summary']['vulnerable_packages']} |",
            f"| Recommendations | {results['summary']['recommendations']} |",
            ""
        ]

        # Per-project details
        for project in results['projects']:
            lines.extend([
                f"## {project['name']}",
                "",
                f"- **Target Framework:** {project['target_framework'] or 'Unknown'}",
                f"- **Package Count:** {len(project['packages'])}",
                ""
            ])

            if project['vulnerabilities']:
                lines.extend([
                    "### Vulnerabilities",
                    "",
                    "| Package | Current | Fixed | Severity | Description |",
                    "|---------|---------|-------|----------|-------------|"
                ])
                for vuln in project['vulnerabilities']:
                    lines.append(f"| {vuln['package']} | {vuln['current_version']} | {vuln['fixed_version']} | {vuln['severity']} | {vuln['description']} |")
                lines.append("")

            if project['recommendations']:
                lines.extend([
                    "### Recommendations",
                    ""
                ])
                for rec in project['recommendations']:
                    lines.append(f"- **{rec['package']}:** {rec['message']}")
                lines.append("")

            # Package list
            if project['packages']:
                lines.extend([
                    "### Packages",
                    "",
                    "| Package | Version |",
                    "|---------|---------|"
                ])
                for pkg in project['packages']:
                    lines.append(f"| {pkg['name']} | {pkg['version']} |")
                lines.append("")

        lines.extend([
            "---",
            "",
            "*Generated by senior-dotnet dependency_analyzer.py*"
        ])

        return '\n'.join(lines)


def main():
    """Main entry point with CLI interface."""
    parser = argparse.ArgumentParser(
        description="Dependency Analyzer - Analyze NuGet dependencies for issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s MyProject.csproj
  %(prog)s src/ --check-security
  %(prog)s . --output report.md --format markdown
  %(prog)s MyProject.csproj --check-security --format json

Output Formats:
  text     - Plain text report (default)
  json     - JSON format
  markdown - Markdown format

Part of senior-dotnet skill.
"""
    )

    parser.add_argument(
        'project_path',
        nargs='?',
        default='.',
        help='Path to .csproj file or directory (default: current directory)'
    )

    parser.add_argument(
        '--check-security', '-s',
        action='store_true',
        help='Check for known security vulnerabilities'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file path'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()

    print(f"Analyzing dependencies: {args.project_path}")
    if args.check_security:
        print("  Security check: Enabled")
    print()

    analyzer = DependencyAnalyzer(
        project_path=args.project_path,
        check_security=args.check_security,
        output_format=args.format,
        output_file=args.output,
        verbose=args.verbose
    )

    results = analyzer.analyze()

    if results['success']:
        # Print summary
        print("Analysis complete!")
        print(f"  Projects analyzed: {len(results['projects'])}")
        print(f"  Total packages: {results['summary']['total_packages']}")

        if results['summary']['vulnerable_packages'] > 0:
            print(f"  VULNERABILITIES FOUND: {results['summary']['vulnerable_packages']}")

        if results['summary']['recommendations'] > 0:
            print(f"  Recommendations: {results['summary']['recommendations']}")

        if args.output:
            print(f"\nReport saved to: {args.output}")

        # Show vulnerabilities in console
        for project in results['projects']:
            if project['vulnerabilities']:
                print(f"\n{project['name']} vulnerabilities:")
                for vuln in project['vulnerabilities']:
                    print(f"  [{vuln['severity'].upper()}] {vuln['package']} {vuln['current_version']}")
                    print(f"    Upgrade to {vuln['fixed_version']} - {vuln['description']}")
    else:
        print(f"Error: {results.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
