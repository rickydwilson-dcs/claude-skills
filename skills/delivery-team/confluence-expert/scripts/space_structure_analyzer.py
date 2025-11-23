#!/usr/bin/env python3
"""
Space Structure Analyzer - Confluence Documentation Analysis Tool

Analyzes Confluence space documentation structure, identifies gaps, suggests improvements,
and validates against documentation best practices.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class SpaceStructureAnalyzer:
    """Analyzes Confluence space structure and documentation patterns"""

    def __init__(self, space_path: str, verbose: bool = False):
        self.space_path = Path(space_path)
        self.verbose = verbose
        self.results = {
            'analyzed_at': datetime.now().isoformat(),
            'space_path': str(space_path),
            'pages_count': 0,
            'structure_score': 0,
            'issues': [],
            'recommendations': []
        }

    def run(self) -> Dict:
        """Execute the space structure analysis"""
        if self.verbose:
            print(f"🔍 Analyzing Confluence Space Structure...")
            print(f"📁 Path: {self.space_path}")

        try:
            self.validate_path()
            self.analyze_structure()
            self.check_best_practices()
            self.generate_recommendations()
            self.calculate_score()

            if self.verbose:
                self.print_report()

            return self.results

        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)

    def validate_path(self):
        """Validate the space path exists"""
        if not self.space_path.exists():
            raise ValueError(f"Path does not exist: {self.space_path}")

        if not self.space_path.is_dir():
            raise ValueError(f"Path must be a directory: {self.space_path}")

        if self.verbose:
            print(f"✓ Path validated")

    def analyze_structure(self):
        """Analyze the documentation structure"""
        md_files = list(self.space_path.rglob('*.md'))
        self.results['pages_count'] = len(md_files)

        # Check for standard documentation patterns
        required_pages = ['README.md', 'OVERVIEW.md', 'INDEX.md']
        found_pages = [f.name for f in md_files]

        missing = [page for page in required_pages if page not in found_pages]
        if missing:
            self.results['issues'].append({
                'type': 'missing_core_pages',
                'severity': 'medium',
                'message': f"Missing core pages: {', '.join(missing)}"
            })

        # Check directory depth
        max_depth = max([len(f.relative_to(self.space_path).parts) for f in md_files]) if md_files else 0
        if max_depth > 4:
            self.results['issues'].append({
                'type': 'excessive_nesting',
                'severity': 'low',
                'message': f"Directory nesting too deep ({max_depth} levels). Consider flattening."
            })

        if self.verbose:
            print(f"✓ Found {len(md_files)} documentation pages")

    def check_best_practices(self):
        """Check against Confluence best practices"""
        # Check for navigation structure
        has_index = any(f.name.lower() in ['index.md', 'toc.md', 'contents.md']
                       for f in self.space_path.rglob('*.md'))

        if not has_index:
            self.results['issues'].append({
                'type': 'missing_navigation',
                'severity': 'high',
                'message': "No navigation/index page found. Users may have difficulty finding content."
            })

        # Check for templates directory
        has_templates = (self.space_path / 'templates').exists()
        if not has_templates:
            self.results['recommendations'].append(
                "Create a templates/ directory for reusable page templates"
            )

        # Check for assets organization
        has_assets = (self.space_path / 'assets').exists()
        if not has_assets:
            self.results['recommendations'].append(
                "Create an assets/ directory for images and attachments"
            )

    def generate_recommendations(self):
        """Generate improvement recommendations"""
        if self.results['pages_count'] == 0:
            self.results['recommendations'].append(
                "Initialize space with core pages: Overview, Getting Started, FAQ"
            )
        elif self.results['pages_count'] < 5:
            self.results['recommendations'].append(
                "Expand documentation coverage. Recommended minimum: 10-15 pages"
            )

        # Recommend space organization
        self.results['recommendations'].extend([
            "Follow standard structure: Home > Category > Subcategory > Page",
            "Use consistent naming conventions (lowercase-with-hyphens or Title Case)",
            "Create page hierarchies that mirror team mental models",
            "Add breadcrumb navigation for deep page trees"
        ])

    def calculate_score(self):
        """Calculate overall structure health score"""
        score = 100

        # Deduct for issues
        for issue in self.results['issues']:
            if issue['severity'] == 'high':
                score -= 20
            elif issue['severity'] == 'medium':
                score -= 10
            elif issue['severity'] == 'low':
                score -= 5

        # Bonus for page count
        if self.results['pages_count'] >= 10:
            score += 10
        elif self.results['pages_count'] >= 5:
            score += 5

        self.results['structure_score'] = max(0, min(100, score))

    def print_report(self):
        """Print human-readable report"""
        print("\n" + "="*60)
        print("CONFLUENCE SPACE STRUCTURE ANALYSIS")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  Pages Found: {self.results['pages_count']}")
        print(f"  Structure Score: {self.results['structure_score']}/100")

        if self.results['issues']:
            print(f"\n⚠️  Issues Found ({len(self.results['issues'])}):")
            for i, issue in enumerate(self.results['issues'], 1):
                print(f"  {i}. [{issue['severity'].upper()}] {issue['message']}")
        else:
            print("\n✅ No structural issues found!")

        if self.results['recommendations']:
            print(f"\n💡 Recommendations ({len(self.results['recommendations'])}):")
            for i, rec in enumerate(self.results['recommendations'], 1):
                print(f"  {i}. {rec}")

        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Confluence space documentation structure and best practices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze current directory
  %(prog)s .

  # Analyze specific space with verbose output
  %(prog)s /path/to/confluence/space -v

  # Output as JSON
  %(prog)s ./docs --json
        """
    )

    parser.add_argument(
        'space_path',
        help='Path to Confluence space documentation directory'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)'
    )

    args = parser.parse_args()

    analyzer = SpaceStructureAnalyzer(args.space_path, verbose=args.verbose)
    results = analyzer.run()

    if args.json:
        output = json.dumps(results, indent=2)
        if args.output:
            Path(args.output).write_text(output)
            print(f"✅ Results written to {args.output}")
        else:
            print(output)

if __name__ == "__main__":
    main()
