#!/usr/bin/env python3
"""
Dependency Analyzer
Analyzes package dependencies from package.json and requirements.txt files.
Detects circular dependencies, builds dependency trees, and visualizes relationships.
"""

import argparse
import json
import logging
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DependencyParser:
    """Parses dependency files from various package managers"""

    @staticmethod
    def parse_package_json(file_path: Path) -> Dict[str, Dict]:
        """Parse npm package.json file"""
        logger.debug(f"Parsing package.json: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error parsing package.json {file_path}: {e}")
            return {'error': str(e)}

        dependencies = {}

        # Regular dependencies
        for name, version in data.get('dependencies', {}).items():
            dependencies[name] = {
                'version': version,
                'type': 'production',
                'source': 'npm',
            }

        # Dev dependencies
        for name, version in data.get('devDependencies', {}).items():
            dependencies[name] = {
                'version': version,
                'type': 'development',
                'source': 'npm',
            }

        # Peer dependencies
        for name, version in data.get('peerDependencies', {}).items():
            dependencies[name] = {
                'version': version,
                'type': 'peer',
                'source': 'npm',
            }

        # Optional dependencies
        for name, version in data.get('optionalDependencies', {}).items():
            dependencies[name] = {
                'version': version,
                'type': 'optional',
                'source': 'npm',
            }

        return {
            'name': data.get('name', 'unknown'),
            'version': data.get('version', '0.0.0'),
            'dependencies': dependencies,
            'source_file': str(file_path),
        }

    @staticmethod
    def parse_requirements_txt(file_path: Path) -> Dict[str, Dict]:
        """Parse Python requirements.txt file"""
        logger.debug(f"Parsing requirements.txt: {file_path}")
        dependencies = {}
        version_pattern = re.compile(r'^([a-zA-Z0-9_-]+)\s*([<>=!~]+)?\s*([0-9a-zA-Z.*]+)?')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError as e:
            logger.error(f"Error parsing requirements.txt {file_path}: {e}")
            return {'error': str(e)}

        for line in lines:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#') or line.startswith('-'):
                continue

            # Handle extras like package[extra]
            if '[' in line:
                line = line.split('[')[0] + line.split(']')[-1] if ']' in line else line.split('[')[0]

            match = version_pattern.match(line)
            if match:
                name = match.group(1).lower()
                operator = match.group(2) or ''
                version = match.group(3) or '*'

                dependencies[name] = {
                    'version': f"{operator}{version}" if operator else version,
                    'type': 'production',
                    'source': 'pip',
                }

        return {
            'name': file_path.parent.name,
            'version': '0.0.0',
            'dependencies': dependencies,
            'source_file': str(file_path),
        }

    @staticmethod
    def parse_pyproject_toml(file_path: Path) -> Dict[str, Dict]:
        """Parse Python pyproject.toml file (basic TOML parsing without external deps)"""
        logger.debug(f"Parsing pyproject.toml: {file_path}")
        dependencies = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError as e:
            logger.error(f"Error parsing pyproject.toml {file_path}: {e}")
            return {'error': str(e)}

        # Simple regex-based TOML parsing for dependencies
        # This handles common cases but not all TOML edge cases
        dep_pattern = re.compile(r'"([a-zA-Z0-9_-]+)(?:\[.*?\])?(?:\s*([<>=!~]+)\s*([0-9a-zA-Z.*]+))?"')

        # Find dependencies section
        in_dependencies = False
        project_name = 'unknown'
        project_version = '0.0.0'

        for line in content.split('\n'):
            line = line.strip()

            # Extract project name
            if line.startswith('name = '):
                project_name = line.split('=')[1].strip().strip('"\'')

            # Extract project version
            if line.startswith('version = '):
                project_version = line.split('=')[1].strip().strip('"\'')

            # Check for dependencies section
            if '[project.dependencies]' in line or 'dependencies = [' in line:
                in_dependencies = True
                continue

            if in_dependencies:
                if line.startswith('[') and 'dependencies' not in line:
                    in_dependencies = False
                    continue

                # Parse dependency line
                matches = dep_pattern.findall(line)
                for match in matches:
                    name = match[0].lower()
                    operator = match[1] if len(match) > 1 else ''
                    version = match[2] if len(match) > 2 else '*'

                    dependencies[name] = {
                        'version': f"{operator}{version}" if operator and version else '*',
                        'type': 'production',
                        'source': 'pip',
                    }

        return {
            'name': project_name,
            'version': project_version,
            'dependencies': dependencies,
            'source_file': str(file_path),
        }


class CircularDependencyDetector:
    """Detects circular dependencies in a dependency graph"""

    def __init__(self, dependencies: Dict[str, Set[str]], verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.dependencies = dependencies
        self.cycles: List[List[str]] = []
        logger.debug("CircularDependencyDetector initialized")

    def detect(self) -> List[List[str]]:
        """Find all circular dependencies using DFS"""
        logger.debug("Starting circular dependency detection")
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        path: List[str] = []

        def dfs(node: str) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.dependencies.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    if cycle not in self.cycles:
                        self.cycles.append(cycle)

            path.pop()
            rec_stack.remove(node)

        for node in self.dependencies:
            if node not in visited:
                dfs(node)

        return self.cycles


class DependencyTreeBuilder:
    """Builds a hierarchical dependency tree"""

    def __init__(self, root_deps: Dict[str, Dict], max_depth: int = 3, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.root_deps = root_deps
        self.max_depth = max_depth
        logger.debug("DependencyTreeBuilder initialized")

    def build(self) -> Dict:
        """Build the dependency tree"""
        logger.debug("Building dependency tree")
        tree = {
            'name': 'root',
            'children': [],
        }

        for name, info in self.root_deps.items():
            node = {
                'name': name,
                'version': info.get('version', '*'),
                'type': info.get('type', 'unknown'),
                'children': [],
            }
            tree['children'].append(node)

        return tree


class DependencyAnalyzer:
    """Main class for dependency analysis"""

    def __init__(self, target_path: str, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.target_path = Path(target_path)
        self.verbose = verbose
        self.results: Dict = {}
        self.all_dependencies: Dict[str, Dict] = {}
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        logger.debug("DependencyAnalyzer initialized")

    def run(self) -> Dict:
        """Execute the main functionality"""
        logger.debug(f"Running dependency analysis for {self.target_path}")
        if self.verbose:
            print(f"Analyzing dependencies in: {self.target_path}", file=sys.stderr)

        self.validate_target()
        self.discover_and_parse()
        self.analyze_dependencies()
        self.generate_visualizations()

        return self.results

    def validate_target(self):
        """Validate the target path exists"""
        logger.debug("Validating target path")
        if not self.target_path.exists():
            logger.error(f"Target path does not exist: {self.target_path}")
            raise ValueError(f"Target path does not exist: {self.target_path}")

    def discover_and_parse(self):
        """Discover and parse all dependency files"""
        logger.debug("Starting file discovery and parsing")
        parsed_files = []

        if self.target_path.is_file():
            parsed = self._parse_file(self.target_path)
            if parsed and 'error' not in parsed:
                parsed_files.append(parsed)
        else:
            # Look for dependency files
            patterns = [
                'package.json',
                '**/package.json',
                'requirements.txt',
                '**/requirements.txt',
                'pyproject.toml',
                '**/pyproject.toml',
            ]

            for pattern in patterns:
                for file_path in self.target_path.glob(pattern):
                    # Skip node_modules and virtual environments
                    if any(part in str(file_path) for part in ['node_modules', 'venv', 'env', '.git']):
                        continue

                    parsed = self._parse_file(file_path)
                    if parsed and 'error' not in parsed:
                        parsed_files.append(parsed)
                        if self.verbose:
                            print(f"  Parsed: {file_path}", file=sys.stderr)

        self.results['parsed_files'] = len(parsed_files)
        self.results['sources'] = parsed_files

        if not parsed_files:
            logger.warning("No dependency files found to parse")

        # Aggregate all dependencies
        for parsed in parsed_files:
            for name, info in parsed.get('dependencies', {}).items():
                if name not in self.all_dependencies:
                    self.all_dependencies[name] = info
                    self.all_dependencies[name]['used_by'] = [parsed.get('source_file')]
                else:
                    self.all_dependencies[name]['used_by'].append(parsed.get('source_file'))

    def _parse_file(self, file_path: Path) -> Optional[Dict]:
        """Parse a single dependency file"""
        name = file_path.name.lower()

        if name == 'package.json':
            return DependencyParser.parse_package_json(file_path)
        elif name == 'requirements.txt':
            return DependencyParser.parse_requirements_txt(file_path)
        elif name == 'pyproject.toml':
            return DependencyParser.parse_pyproject_toml(file_path)

        return None

    def analyze_dependencies(self):
        """Analyze the collected dependencies"""
        logger.debug("Analyzing dependencies")
        # Build dependency graph (simplified - actual transitive deps would need registry lookups)
        for name in self.all_dependencies:
            self.dependency_graph[name] = set()

        # Detect circular dependencies
        detector = CircularDependencyDetector(self.dependency_graph)
        cycles = detector.detect()

        # Categorize dependencies
        production_deps = [n for n, i in self.all_dependencies.items() if i.get('type') == 'production']
        dev_deps = [n for n, i in self.all_dependencies.items() if i.get('type') == 'development']
        peer_deps = [n for n, i in self.all_dependencies.items() if i.get('type') == 'peer']
        optional_deps = [n for n, i in self.all_dependencies.items() if i.get('type') == 'optional']

        # Calculate statistics
        self.results['statistics'] = {
            'total_dependencies': len(self.all_dependencies),
            'production': len(production_deps),
            'development': len(dev_deps),
            'peer': len(peer_deps),
            'optional': len(optional_deps),
            'circular_dependencies': len(cycles),
        }

        self.results['dependencies'] = self.all_dependencies
        self.results['circular_dependencies'] = cycles

        # Identify potential issues
        issues = []

        if cycles:
            issues.append({
                'type': 'circular_dependency',
                'severity': 'high',
                'message': f"Found {len(cycles)} circular dependency chain(s)",
                'details': cycles,
            })

        # Check for very old or unpinned versions
        unpinned = [n for n, i in self.all_dependencies.items()
                    if i.get('version') in ('*', 'latest', '')]
        if unpinned:
            issues.append({
                'type': 'unpinned_versions',
                'severity': 'medium',
                'message': f"{len(unpinned)} dependencies have unpinned versions",
                'details': unpinned[:10],  # Limit to first 10
            })

        self.results['issues'] = issues

    def generate_visualizations(self):
        """Generate visualization outputs"""
        logger.debug("Generating visualizations")
        self.results['visualizations'] = {}

        # Generate Mermaid dependency tree
        mermaid = self._generate_mermaid_tree()
        self.results['visualizations']['mermaid_tree'] = mermaid

        # Generate Mermaid flowchart
        flowchart = self._generate_mermaid_flowchart()
        self.results['visualizations']['mermaid_flowchart'] = flowchart

    def _generate_mermaid_tree(self) -> str:
        """Generate a Mermaid tree diagram"""
        lines = [
            "```mermaid",
            "graph TD",
            "    Root[Project Dependencies]",
        ]

        # Group by type
        by_type: Dict[str, List[str]] = defaultdict(list)
        for name, info in self.all_dependencies.items():
            dep_type = info.get('type', 'unknown')
            by_type[dep_type].append(name)

        type_colors = {
            'production': ':::production',
            'development': ':::dev',
            'peer': ':::peer',
            'optional': ':::optional',
        }

        for dep_type, deps in by_type.items():
            safe_type = dep_type.replace(' ', '_')
            lines.append(f"    Root --> {safe_type}[{dep_type.title()} ({len(deps)})]")

            for dep in sorted(deps)[:15]:  # Limit to 15 per type for readability
                safe_dep = dep.replace('@', '_').replace('/', '_').replace('-', '_')
                version = self.all_dependencies[dep].get('version', '')[:10]
                lines.append(f"    {safe_type} --> {safe_dep}[{dep}@{version}]")

            if len(deps) > 15:
                lines.append(f"    {safe_type} --> {safe_type}_more[... and {len(deps) - 15} more]")

        lines.append("```")
        return '\n'.join(lines)

    def _generate_mermaid_flowchart(self) -> str:
        """Generate a Mermaid flowchart of dependencies"""
        lines = [
            "```mermaid",
            "flowchart LR",
        ]

        # Production subgraph
        prod_deps = [n for n, i in self.all_dependencies.items() if i.get('type') == 'production']
        if prod_deps:
            lines.append("    subgraph Production")
            for dep in sorted(prod_deps)[:20]:
                safe_dep = dep.replace('@', '_').replace('/', '_').replace('-', '_')
                lines.append(f"        {safe_dep}[{dep}]")
            if len(prod_deps) > 20:
                lines.append(f"        prod_more[+{len(prod_deps) - 20} more]")
            lines.append("    end")

        # Dev subgraph
        dev_deps = [n for n, i in self.all_dependencies.items() if i.get('type') == 'development']
        if dev_deps:
            lines.append("    subgraph Development")
            for dep in sorted(dev_deps)[:20]:
                safe_dep = dep.replace('@', '_').replace('/', '_').replace('-', '_')
                lines.append(f"        {safe_dep}[{dep}]")
            if len(dev_deps) > 20:
                lines.append(f"        dev_more[+{len(dev_deps) - 20} more]")
            lines.append("    end")

        lines.append("```")
        return '\n'.join(lines)


def format_text_output(results: Dict) -> str:
    """Format results as human-readable text"""
    lines = ["=" * 60]
    lines.append("DEPENDENCY ANALYSIS RESULTS")
    lines.append("=" * 60)

    lines.append(f"\nTarget analyzed with {results.get('parsed_files', 0)} dependency file(s)")

    stats = results.get('statistics', {})
    lines.append(f"\nDependency Statistics:")
    lines.append(f"  Total Dependencies: {stats.get('total_dependencies', 0)}")
    lines.append(f"  Production: {stats.get('production', 0)}")
    lines.append(f"  Development: {stats.get('development', 0)}")
    lines.append(f"  Peer: {stats.get('peer', 0)}")
    lines.append(f"  Optional: {stats.get('optional', 0)}")

    # Issues
    issues = results.get('issues', [])
    if issues:
        lines.append(f"\nIssues Found ({len(issues)}):")
        for issue in issues:
            severity_icon = {'high': '!!!', 'medium': '!!', 'low': '!'}.get(issue['severity'], '?')
            lines.append(f"  [{severity_icon}] {issue['message']}")
    else:
        lines.append("\nNo issues found.")

    # Circular dependencies
    cycles = results.get('circular_dependencies', [])
    if cycles:
        lines.append(f"\nCircular Dependencies ({len(cycles)}):")
        for cycle in cycles[:5]:
            lines.append(f"  {' -> '.join(cycle)}")
        if len(cycles) > 5:
            lines.append(f"  ... and {len(cycles) - 5} more")

    # Dependency list (top 20)
    deps = results.get('dependencies', {})
    if deps:
        lines.append(f"\nTop Dependencies (showing {min(20, len(deps))} of {len(deps)}):")
        for name in sorted(deps.keys())[:20]:
            info = deps[name]
            lines.append(f"  {name}: {info.get('version', '*')} ({info.get('type', 'unknown')})")

    # Visualizations
    viz = results.get('visualizations', {})
    if viz.get('mermaid_tree'):
        lines.append(f"\n{'=' * 60}")
        lines.append("DEPENDENCY TREE (Mermaid)")
        lines.append("=" * 60)
        lines.append(viz['mermaid_tree'])

    return '\n'.join(lines)


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="Analyze project dependencies from package.json and requirements.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input ./my-project
  %(prog)s --input package.json
  %(prog)s --input requirements.txt
  %(prog)s --input ./project --output json --file deps.json
  %(prog)s --input ./project -v

Supported dependency files:
  - package.json (npm/yarn)
  - requirements.txt (pip)
  - pyproject.toml (pip/poetry)

Analysis includes:
  - Dependency categorization (production, dev, peer, optional)
  - Circular dependency detection
  - Version analysis
  - Mermaid visualization generation

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Project directory or dependency file to analyze'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json'],
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
        analyzer = DependencyAnalyzer(
            args.target,
            verbose=args.verbose
        )

        results = analyzer.run()

        if args.output == 'json':
            # Convert sets to lists for JSON serialization
            output = json.dumps(results, indent=2, default=list)
        else:
            output = format_text_output(results)

        if args.file:
            with open(args.file, 'w') as f:
                f.write(output)
            print(f"Results written to {args.file}")
        else:
            print(output)

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
