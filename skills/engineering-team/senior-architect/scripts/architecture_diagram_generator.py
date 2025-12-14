#!/usr/bin/env python3
"""
Architecture Diagram Generator
Generates Mermaid and PlantUML diagrams from code analysis.
Supports component diagrams, dependency graphs, and class diagrams.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict


class CodeAnalyzer:
    """Analyzes source code files to extract architectural information"""

    PYTHON_IMPORT_PATTERNS = [
        re.compile(r'^import\s+([\w.]+)'),
        re.compile(r'^from\s+([\w.]+)\s+import'),
    ]

    TYPESCRIPT_IMPORT_PATTERNS = [
        re.compile(r"^import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]"),
        re.compile(r"^import\s+['\"]([^'\"]+)['\"]"),
        re.compile(r"require\(['\"]([^'\"]+)['\"]\)"),
    ]

    PYTHON_CLASS_PATTERN = re.compile(r'^class\s+(\w+)(?:\(([^)]*)\))?:')
    TYPESCRIPT_CLASS_PATTERN = re.compile(r'^(?:export\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?')

    def __init__(self, root_path: Path, verbose: bool = False):
        self.root_path = root_path
        self.verbose = verbose
        self.modules: Dict[str, Dict] = {}
        self.classes: Dict[str, Dict] = {}
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)

    def analyze(self) -> Dict:
        """Analyze all supported files in the directory"""
        if self.root_path.is_file():
            self._analyze_file(self.root_path)
        else:
            for pattern in ['**/*.py', '**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx']:
                for file_path in self.root_path.glob(pattern):
                    if self._should_skip(file_path):
                        continue
                    self._analyze_file(file_path)

        return {
            'modules': self.modules,
            'classes': self.classes,
            'dependencies': {k: list(v) for k, v in self.dependencies.items()},
        }

    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'env',
                     'dist', 'build', '.next', 'coverage'}
        return any(part in skip_dirs for part in file_path.parts)

    def _analyze_file(self, file_path: Path) -> None:
        """Analyze a single file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            if self.verbose:
                print(f"  Warning: Could not read {file_path}: {e}", file=sys.stderr)
            return

        rel_path = str(file_path.relative_to(self.root_path) if self.root_path.is_dir() else file_path.name)
        module_name = self._get_module_name(file_path)

        self.modules[module_name] = {
            'path': rel_path,
            'type': self._get_file_type(file_path),
            'imports': [],
            'classes': [],
            'functions': [],
        }

        lines = content.split('\n')

        for line in lines:
            line = line.strip()

            # Extract imports
            imports = self._extract_imports(line, file_path)
            for imp in imports:
                self.modules[module_name]['imports'].append(imp)
                self.dependencies[module_name].add(imp)

            # Extract classes
            class_info = self._extract_class(line, file_path)
            if class_info:
                class_name, parent, interfaces = class_info
                full_class_name = f"{module_name}.{class_name}"
                self.classes[full_class_name] = {
                    'name': class_name,
                    'module': module_name,
                    'parent': parent,
                    'interfaces': interfaces,
                }
                self.modules[module_name]['classes'].append(class_name)

        if self.verbose:
            print(f"  Analyzed: {rel_path} - {len(self.modules[module_name]['imports'])} imports, "
                  f"{len(self.modules[module_name]['classes'])} classes")

    def _get_module_name(self, file_path: Path) -> str:
        """Convert file path to module name"""
        if self.root_path.is_file():
            return file_path.stem
        rel = file_path.relative_to(self.root_path)
        parts = list(rel.parts)
        if parts[-1].endswith(('.py', '.ts', '.tsx', '.js', '.jsx')):
            parts[-1] = Path(parts[-1]).stem
        return '.'.join(parts)

    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type"""
        suffix = file_path.suffix.lower()
        return {
            '.py': 'python',
            '.ts': 'typescript',
            '.tsx': 'typescript-react',
            '.js': 'javascript',
            '.jsx': 'javascript-react',
        }.get(suffix, 'unknown')

    def _extract_imports(self, line: str, file_path: Path) -> List[str]:
        """Extract import statements from a line"""
        imports = []
        suffix = file_path.suffix.lower()

        if suffix == '.py':
            for pattern in self.PYTHON_IMPORT_PATTERNS:
                match = pattern.match(line)
                if match:
                    imports.append(match.group(1).split('.')[0])
        elif suffix in ('.ts', '.tsx', '.js', '.jsx'):
            for pattern in self.TYPESCRIPT_IMPORT_PATTERNS:
                match = pattern.search(line)
                if match:
                    import_path = match.group(1)
                    # Convert path to module name
                    if import_path.startswith('.'):
                        imports.append(f"local:{import_path}")
                    else:
                        imports.append(import_path.split('/')[0])

        return imports

    def _extract_class(self, line: str, file_path: Path) -> Optional[Tuple[str, Optional[str], List[str]]]:
        """Extract class definition from a line"""
        suffix = file_path.suffix.lower()

        if suffix == '.py':
            match = self.PYTHON_CLASS_PATTERN.match(line)
            if match:
                class_name = match.group(1)
                parents = match.group(2)
                parent = parents.split(',')[0].strip() if parents else None
                return (class_name, parent, [])
        elif suffix in ('.ts', '.tsx', '.js', '.jsx'):
            match = self.TYPESCRIPT_CLASS_PATTERN.match(line)
            if match:
                class_name = match.group(1)
                parent = match.group(2)
                interfaces = [i.strip() for i in (match.group(3) or '').split(',')] if match.group(3) else []
                return (class_name, parent, interfaces)

        return None


class MermaidGenerator:
    """Generates Mermaid diagram syntax"""

    @staticmethod
    def component_diagram(modules: Dict, dependencies: Dict, title: str = "Component Diagram") -> str:
        """Generate a Mermaid component diagram"""
        lines = [
            "```mermaid",
            f"graph TB",
            f"    subgraph {title.replace(' ', '_')}",
        ]

        # Group modules by directory
        groups: Dict[str, List[str]] = defaultdict(list)
        for module_name, info in modules.items():
            path_parts = info.get('path', module_name).split('/')
            if len(path_parts) > 1:
                group = path_parts[0]
            else:
                group = 'root'
            groups[group].append(module_name)

        # Add subgraphs for each group
        for group_name, group_modules in groups.items():
            safe_group = group_name.replace('-', '_').replace('.', '_')
            lines.append(f"        subgraph {safe_group}")
            for module in group_modules:
                safe_module = module.replace('.', '_').replace('-', '_')
                lines.append(f"            {safe_module}[{module}]")
            lines.append("        end")

        lines.append("    end")

        # Add dependencies
        for source, targets in dependencies.items():
            safe_source = source.replace('.', '_').replace('-', '_')
            for target in targets:
                if target.startswith('local:'):
                    continue  # Skip local relative imports
                safe_target = target.replace('.', '_').replace('-', '_')
                if target in modules:
                    lines.append(f"    {safe_source} --> {safe_target}")

        lines.append("```")
        return '\n'.join(lines)

    @staticmethod
    def dependency_graph(dependencies: Dict, title: str = "Dependency Graph") -> str:
        """Generate a Mermaid dependency flowchart"""
        lines = [
            "```mermaid",
            f"flowchart LR",
        ]

        # Collect all external dependencies
        external_deps: Set[str] = set()
        internal_modules: Set[str] = set(dependencies.keys())

        for source, targets in dependencies.items():
            for target in targets:
                if target.startswith('local:'):
                    continue
                if target not in internal_modules:
                    external_deps.add(target)

        # Add external dependencies subgraph
        if external_deps:
            lines.append("    subgraph External_Dependencies")
            for dep in sorted(external_deps):
                safe_dep = dep.replace('.', '_').replace('-', '_').replace('@', '_')
                lines.append(f"        {safe_dep}[({dep})]")
            lines.append("    end")

        # Add internal modules subgraph
        if internal_modules:
            lines.append("    subgraph Internal_Modules")
            for module in sorted(internal_modules):
                safe_module = module.replace('.', '_').replace('-', '_')
                lines.append(f"        {safe_module}[{module}]")
            lines.append("    end")

        # Add edges
        for source, targets in dependencies.items():
            safe_source = source.replace('.', '_').replace('-', '_')
            for target in targets:
                if target.startswith('local:'):
                    continue
                safe_target = target.replace('.', '_').replace('-', '_').replace('@', '_')
                lines.append(f"    {safe_source} --> {safe_target}")

        lines.append("```")
        return '\n'.join(lines)

    @staticmethod
    def class_diagram(classes: Dict, title: str = "Class Diagram") -> str:
        """Generate a Mermaid class diagram"""
        lines = [
            "```mermaid",
            "classDiagram",
        ]

        # Add classes
        for full_name, info in classes.items():
            class_name = info['name']
            lines.append(f"    class {class_name}")

            # Add inheritance
            if info.get('parent'):
                lines.append(f"    {info['parent']} <|-- {class_name}")

            # Add interface implementations
            for interface in info.get('interfaces', []):
                if interface:
                    lines.append(f"    {interface} <|.. {class_name}")

        lines.append("```")
        return '\n'.join(lines)


class PlantUMLGenerator:
    """Generates PlantUML diagram syntax"""

    @staticmethod
    def component_diagram(modules: Dict, dependencies: Dict, title: str = "Component Diagram") -> str:
        """Generate a PlantUML component diagram"""
        lines = [
            "@startuml",
            f"title {title}",
            "",
        ]

        # Group modules by directory
        groups: Dict[str, List[str]] = defaultdict(list)
        for module_name, info in modules.items():
            path_parts = info.get('path', module_name).split('/')
            if len(path_parts) > 1:
                group = path_parts[0]
            else:
                group = 'root'
            groups[group].append(module_name)

        # Add packages for each group
        for group_name, group_modules in groups.items():
            lines.append(f'package "{group_name}" {{')
            for module in group_modules:
                lines.append(f'    component "{module}" as {module.replace(".", "_")}')
            lines.append("}")

        lines.append("")

        # Add dependencies
        for source, targets in dependencies.items():
            safe_source = source.replace('.', '_')
            for target in targets:
                if target.startswith('local:') or target not in modules:
                    continue
                safe_target = target.replace('.', '_')
                lines.append(f"{safe_source} --> {safe_target}")

        lines.append("")
        lines.append("@enduml")
        return '\n'.join(lines)

    @staticmethod
    def class_diagram(classes: Dict, title: str = "Class Diagram") -> str:
        """Generate a PlantUML class diagram"""
        lines = [
            "@startuml",
            f"title {title}",
            "",
        ]

        # Add classes
        for full_name, info in classes.items():
            class_name = info['name']
            lines.append(f"class {class_name}")

        lines.append("")

        # Add relationships
        for full_name, info in classes.items():
            class_name = info['name']

            if info.get('parent'):
                lines.append(f"{info['parent']} <|-- {class_name}")

            for interface in info.get('interfaces', []):
                if interface:
                    lines.append(f"{interface} <|.. {class_name}")

        lines.append("")
        lines.append("@enduml")
        return '\n'.join(lines)


class ArchitectureDiagramGenerator:
    """Main class for generating architecture diagrams from code analysis"""

    def __init__(self, target_path: str, verbose: bool = False, diagram_format: str = 'mermaid'):
        self.target_path = Path(target_path)
        self.verbose = verbose
        self.diagram_format = diagram_format
        self.results: Dict = {}
        self.analysis: Dict = {}

    def run(self) -> Dict:
        """Execute the main functionality"""
        if self.verbose:
            print(f"Analyzing: {self.target_path}", file=sys.stderr)

        self.validate_target()
        self.analyze()
        self.generate_diagrams()

        if self.verbose:
            print(f"Generated {len(self.results.get('diagrams', {}))} diagrams", file=sys.stderr)

        return self.results

    def validate_target(self):
        """Validate the target path exists and is accessible"""
        if not self.target_path.exists():
            raise ValueError(f"Target path does not exist: {self.target_path}")

    def analyze(self):
        """Perform code analysis"""
        analyzer = CodeAnalyzer(self.target_path, self.verbose)
        self.analysis = analyzer.analyze()

        self.results['status'] = 'success'
        self.results['target'] = str(self.target_path)
        self.results['statistics'] = {
            'modules_analyzed': len(self.analysis['modules']),
            'classes_found': len(self.analysis['classes']),
            'total_dependencies': sum(len(deps) for deps in self.analysis['dependencies'].values()),
        }

    def generate_diagrams(self):
        """Generate diagrams based on analysis"""
        self.results['diagrams'] = {}

        modules = self.analysis['modules']
        dependencies = self.analysis['dependencies']
        classes = self.analysis['classes']

        if self.diagram_format in ('mermaid', 'all'):
            self.results['diagrams']['mermaid'] = {
                'component': MermaidGenerator.component_diagram(modules, dependencies),
                'dependency': MermaidGenerator.dependency_graph(dependencies),
            }
            if classes:
                self.results['diagrams']['mermaid']['class'] = MermaidGenerator.class_diagram(classes)

        if self.diagram_format in ('plantuml', 'all'):
            self.results['diagrams']['plantuml'] = {
                'component': PlantUMLGenerator.component_diagram(modules, dependencies),
            }
            if classes:
                self.results['diagrams']['plantuml']['class'] = PlantUMLGenerator.class_diagram(classes)

        self.results['analysis'] = {
            'modules': list(modules.keys()),
            'classes': list(classes.keys()),
            'external_dependencies': list(set(
                dep for deps in dependencies.values()
                for dep in deps
                if not dep.startswith('local:') and dep not in modules
            )),
        }


def format_text_output(results: Dict) -> str:
    """Format results as human-readable text"""
    lines = ["=" * 60]
    lines.append("ARCHITECTURE DIAGRAM GENERATOR RESULTS")
    lines.append("=" * 60)

    stats = results.get('statistics', {})
    lines.append(f"\nTarget: {results.get('target')}")
    lines.append(f"Status: {results.get('status')}")
    lines.append(f"\nStatistics:")
    lines.append(f"  Modules Analyzed: {stats.get('modules_analyzed', 0)}")
    lines.append(f"  Classes Found: {stats.get('classes_found', 0)}")
    lines.append(f"  Total Dependencies: {stats.get('total_dependencies', 0)}")

    analysis = results.get('analysis', {})
    if analysis.get('external_dependencies'):
        lines.append(f"\nExternal Dependencies ({len(analysis['external_dependencies'])}):")
        for dep in sorted(analysis['external_dependencies'])[:20]:
            lines.append(f"  - {dep}")
        if len(analysis['external_dependencies']) > 20:
            lines.append(f"  ... and {len(analysis['external_dependencies']) - 20} more")

    diagrams = results.get('diagrams', {})
    for format_name, format_diagrams in diagrams.items():
        lines.append(f"\n{'=' * 60}")
        lines.append(f"{format_name.upper()} DIAGRAMS")
        lines.append("=" * 60)

        for diagram_type, diagram_content in format_diagrams.items():
            lines.append(f"\n--- {diagram_type.upper()} DIAGRAM ---\n")
            lines.append(diagram_content)

    return '\n'.join(lines)


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="Generate architecture diagrams (Mermaid/PlantUML) from source code analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input ./src
  %(prog)s --input ./src --format mermaid
  %(prog)s --input ./src --format plantuml --output json
  %(prog)s --input ./src --format all -o json --file diagrams.json
  %(prog)s --input ./src -v

Supported file types: Python (.py), TypeScript (.ts, .tsx), JavaScript (.js, .jsx)

Diagram types generated:
  - Component Diagram: Shows module/package structure
  - Dependency Graph: Shows module dependencies (internal and external)
  - Class Diagram: Shows class hierarchy and relationships

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Source directory or file to analyze'
    )

    parser.add_argument(
        '--format', '-F',
        choices=['mermaid', 'plantuml', 'all'],
        default='mermaid',
        help='Diagram format to generate (default: mermaid)'
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
        generator = ArchitectureDiagramGenerator(
            args.target,
            verbose=args.verbose,
            diagram_format=args.format
        )

        results = generator.run()

        if args.output == 'json':
            output = json.dumps(results, indent=2)
        else:
            output = format_text_output(results)

        if args.file:
            with open(args.file, 'w') as f:
                f.write(output)
            print(f"Results written to {args.file}")
        else:
            print(output)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
