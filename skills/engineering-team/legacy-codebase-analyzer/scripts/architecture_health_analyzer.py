#!/usr/bin/env python3
"""
Architecture Health Analyzer

Analyzes architectural patterns, coupling, cohesion, and structural health of codebases.
Detects circular dependencies, god modules, layer violations, and calculates coupling metrics.

Usage:
    python architecture_health_analyzer.py --input /path/to/codebase
    python architecture_health_analyzer.py -i /path/to/codebase --output json --diagram
    python architecture_health_analyzer.py -i . --file report.json --verbose
"""

from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import argparse
import ast
import json
import logging
import os
import sys


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LayerType(Enum):
    """Application layer types"""
    PRESENTATION = "presentation"
    BUSINESS = "business"
    DATA = "data"
    UTILITY = "utility"
    UNKNOWN = "unknown"


@dataclass
class ModuleInfo:
    """Information about a single module"""
    path: str
    name: str
    lines: int
    functions: int
    classes: int
    imports: List[str] = field(default_factory=list)
    layer: LayerType = LayerType.UNKNOWN

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['layer'] = self.layer.value
        return data


@dataclass
class CouplingMetrics:
    """Coupling metrics for a module"""
    module: str
    afferent_coupling: int  # Ca - incoming dependencies
    efferent_coupling: int  # Ce - outgoing dependencies
    instability: float      # I = Ce / (Ca + Ce)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class CircularDependency:
    """Circular dependency chain"""
    cycle: List[str]
    severity: str  # "high", "medium", "low"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class AntiPattern:
    """Detected architectural anti-pattern"""
    type: str
    module: str
    description: str
    severity: str  # "critical", "high", "medium", "low"
    metrics: Dict[str, any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class LayerViolation:
    """Layer dependency violation"""
    from_module: str
    from_layer: str
    to_module: str
    to_layer: str
    violation_type: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class DependencyGraph:
    """Module dependency graph"""
    nodes: List[str]
    edges: Dict[str, List[str]]  # module -> list of dependencies
    edge_count: int

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'nodes': self.nodes,
            'edges': self.edges,
            'edge_count': self.edge_count
        }


@dataclass
class ArchitectureAnalysis:
    """Complete architecture analysis results"""
    summary: Dict[str, any]
    dependency_graph: DependencyGraph
    circular_dependencies: List[CircularDependency]
    coupling_metrics: List[CouplingMetrics]
    anti_patterns: List[AntiPattern]
    layer_analysis: Dict[str, any]
    layer_violations: List[LayerViolation]
    mermaid_diagram: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'summary': self.summary,
            'dependency_graph': self.dependency_graph.to_dict(),
            'circular_dependencies': [cd.to_dict() for cd in self.circular_dependencies],
            'coupling_metrics': [cm.to_dict() for cm in self.coupling_metrics],
            'anti_patterns': [ap.to_dict() for ap in self.anti_patterns],
            'layer_analysis': self.layer_analysis,
            'layer_violations': [lv.to_dict() for lv in self.layer_violations],
            'mermaid_diagram': self.mermaid_diagram
        }


class PythonImportExtractor(ast.NodeVisitor):
    """Extract imports from Python AST"""

    def __init__(self):
        self.imports: List[str] = []
        self.functions: int = 0
        self.classes: int = 0

    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statement"""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from-import statement"""
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition"""
        self.functions += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition"""
        self.functions += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition"""
        self.classes += 1
        self.generic_visit(node)


class ArchitectureHealthAnalyzer:
    """Analyze codebase architecture and structural health"""

    def __init__(self, root_path: Path, verbose: bool = False):
        self.root_path = root_path.resolve()
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("ArchitectureHealthAnalyzer initialized")
        self.modules: Dict[str, ModuleInfo] = {}
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)

        # Layer detection patterns
        self.layer_patterns = {
            LayerType.PRESENTATION: [
                'views', 'controllers', 'handlers', 'routes', 'api',
                'endpoints', 'templates', 'ui', 'web', 'rest'
            ],
            LayerType.BUSINESS: [
                'services', 'business', 'domain', 'logic', 'core',
                'use_cases', 'usecases', 'application'
            ],
            LayerType.DATA: [
                'models', 'repositories', 'dao', 'database', 'db',
                'persistence', 'storage', 'entities', 'orm'
            ],
            LayerType.UTILITY: [
                'utils', 'helpers', 'common', 'shared', 'lib',
                'utilities', 'tools'
            ]
        }

    def log(self, message: str) -> None:
        """Log message if verbose mode enabled"""
        if self.verbose:
            print(f"[INFO] {message}", file=sys.stderr)

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the codebase"""
        python_files = []

        for path in self.root_path.rglob("*.py"):
            # Skip virtual environments and common directories
            skip_dirs = {'venv', 'env', '.venv', 'node_modules', '.git', '__pycache__', 'build', 'dist'}
            if any(skip_dir in path.parts for skip_dir in skip_dirs):
                continue

            if path.is_file():
                python_files.append(path)

        return python_files

    def extract_module_info(self, file_path: Path) -> Optional[ModuleInfo]:
        """Extract module information from a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = len(content.splitlines())

            # Parse AST
            try:
                tree = ast.parse(content, filename=str(file_path))
                extractor = PythonImportExtractor()
                extractor.visit(tree)

                # Get module path relative to root
                rel_path = file_path.relative_to(self.root_path)
                module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')

                # Filter imports to only include project modules
                project_imports = self._filter_project_imports(extractor.imports)

                # Detect layer
                layer = self._detect_layer(str(rel_path))

                return ModuleInfo(
                    path=str(rel_path),
                    name=module_name,
                    lines=lines,
                    functions=extractor.functions,
                    classes=extractor.classes,
                    imports=project_imports,
                    layer=layer
                )
            except SyntaxError as e:
                self.log(f"Syntax error in {file_path}: {e}")
                return None

        except Exception as e:
            self.log(f"Error processing {file_path}: {e}")
            return None

    def _filter_project_imports(self, imports: List[str]) -> List[str]:
        """Filter imports to only include project modules"""
        # Filter out standard library and third-party imports
        stdlib_prefixes = {
            'os', 'sys', 'json', 'math', 'datetime', 're', 'collections',
            'itertools', 'functools', 'typing', 'pathlib', 'argparse',
            'logging', 'unittest', 'pytest', 'http', 'urllib', 'email',
            'xml', 'html', 'sqlite3', 'csv', 'random', 'pickle', 'copy'
        }

        third_party_prefixes = {
            'django', 'flask', 'fastapi', 'requests', 'numpy', 'pandas',
            'sqlalchemy', 'pytest', 'click', 'pydantic', 'redis', 'celery'
        }

        filtered = []
        for imp in imports:
            base = imp.split('.')[0]
            if base not in stdlib_prefixes and base not in third_party_prefixes:
                filtered.append(imp)

        return filtered

    def _detect_layer(self, path: str) -> LayerType:
        """Detect application layer based on path patterns"""
        path_lower = path.lower()

        for layer, patterns in self.layer_patterns.items():
            if any(pattern in path_lower for pattern in patterns):
                return layer

        return LayerType.UNKNOWN

    def build_dependency_graph(self) -> DependencyGraph:
        """Build module dependency graph"""
        self.log("Building dependency graph...")

        nodes = list(self.modules.keys())
        edges: Dict[str, List[str]] = defaultdict(list)
        edge_count = 0

        for module_name, module_info in self.modules.items():
            for import_name in module_info.imports:
                # Try to resolve import to actual module
                resolved = self._resolve_import(import_name, module_name)
                if resolved and resolved in self.modules:
                    self.dependency_graph[module_name].add(resolved)
                    edges[module_name].append(resolved)
                    edge_count += 1

        return DependencyGraph(
            nodes=nodes,
            edges=dict(edges),
            edge_count=edge_count
        )

    def _resolve_import(self, import_name: str, from_module: str) -> Optional[str]:
        """Resolve import name to actual module"""
        # Try exact match first
        if import_name in self.modules:
            return import_name

        # Try partial matches (handle package imports)
        for module_name in self.modules.keys():
            if module_name.startswith(import_name):
                return module_name
            if import_name.startswith(module_name):
                return module_name

        return None

    def detect_circular_dependencies(self) -> List[CircularDependency]:
        """Detect circular dependencies using DFS"""
        self.log("Detecting circular dependencies...")

        cycles = []
        visited = set()
        rec_stack = []

        def dfs(node: str) -> None:
            """Depth-first search for cycles"""
            visited.add(node)
            rec_stack.append(node)

            for neighbor in self.dependency_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = rec_stack.index(neighbor)
                    cycle = rec_stack[cycle_start:] + [neighbor]

                    # Determine severity based on cycle length
                    if len(cycle) == 2:
                        severity = "high"
                    elif len(cycle) <= 4:
                        severity = "medium"
                    else:
                        severity = "low"

                    cycles.append(CircularDependency(
                        cycle=cycle,
                        severity=severity
                    ))

            rec_stack.pop()

        for node in self.dependency_graph.keys():
            if node not in visited:
                dfs(node)

        # Remove duplicates (same cycle detected from different entry points)
        unique_cycles = []
        seen_cycles = set()

        for cycle_obj in cycles:
            # Normalize cycle (rotate to start with smallest element)
            cycle = cycle_obj.cycle
            min_idx = cycle.index(min(cycle[:-1]))  # Exclude last element (duplicate)
            normalized = tuple(cycle[min_idx:-1] + cycle[:min_idx] + [cycle[min_idx]])

            if normalized not in seen_cycles:
                seen_cycles.add(normalized)
                unique_cycles.append(cycle_obj)

        return unique_cycles

    def calculate_coupling_metrics(self) -> List[CouplingMetrics]:
        """Calculate coupling metrics for all modules"""
        self.log("Calculating coupling metrics...")

        # Calculate afferent coupling (incoming dependencies)
        afferent = defaultdict(int)
        for source, targets in self.dependency_graph.items():
            for target in targets:
                afferent[target] += 1

        # Calculate efferent coupling (outgoing dependencies)
        efferent = {module: len(deps) for module, deps in self.dependency_graph.items()}

        # Calculate instability metric: I = Ce / (Ca + Ce)
        metrics = []
        for module in self.modules.keys():
            ca = afferent.get(module, 0)
            ce = efferent.get(module, 0)

            if ca + ce > 0:
                instability = ce / (ca + ce)
            else:
                instability = 0.0

            metrics.append(CouplingMetrics(
                module=module,
                afferent_coupling=ca,
                efferent_coupling=ce,
                instability=instability
            ))

        return metrics

    def detect_anti_patterns(self, coupling_metrics: List[CouplingMetrics]) -> List[AntiPattern]:
        """Detect architectural anti-patterns"""
        self.log("Detecting anti-patterns...")

        anti_patterns = []

        # Create coupling lookup
        coupling_map = {cm.module: cm for cm in coupling_metrics}

        for module_name, module_info in self.modules.items():
            # God modules (large modules with many responsibilities)
            if module_info.lines > 1000 or module_info.functions > 20:
                anti_patterns.append(AntiPattern(
                    type="god_module",
                    module=module_name,
                    description=f"Large module with {module_info.lines} lines and {module_info.functions} functions",
                    severity="high" if module_info.lines > 2000 else "medium",
                    metrics={
                        'lines': module_info.lines,
                        'functions': module_info.functions,
                        'classes': module_info.classes
                    }
                ))

            # Dead code (no incoming dependencies)
            coupling = coupling_map.get(module_name)
            if coupling and coupling.afferent_coupling == 0 and coupling.efferent_coupling > 0:
                anti_patterns.append(AntiPattern(
                    type="dead_code",
                    module=module_name,
                    description="Module has no incoming dependencies (possibly unused)",
                    severity="low",
                    metrics={
                        'afferent_coupling': coupling.afferent_coupling,
                        'efferent_coupling': coupling.efferent_coupling
                    }
                ))

            # Feature envy (high outgoing coupling)
            if coupling and coupling.efferent_coupling > 10:
                anti_patterns.append(AntiPattern(
                    type="feature_envy",
                    module=module_name,
                    description=f"Module depends on {coupling.efferent_coupling} other modules",
                    severity="medium",
                    metrics={
                        'efferent_coupling': coupling.efferent_coupling,
                        'instability': coupling.instability
                    }
                ))

            # Unstable dependencies (high instability with many dependents)
            if coupling and coupling.instability > 0.8 and coupling.afferent_coupling > 5:
                anti_patterns.append(AntiPattern(
                    type="unstable_dependencies",
                    module=module_name,
                    description=f"Highly unstable module ({coupling.instability:.2f}) with many dependents",
                    severity="high",
                    metrics={
                        'instability': coupling.instability,
                        'afferent_coupling': coupling.afferent_coupling
                    }
                ))

        return anti_patterns

    def analyze_layers(self) -> Tuple[Dict[str, any], List[LayerViolation]]:
        """Analyze layer architecture and detect violations"""
        self.log("Analyzing layers...")

        # Count modules per layer
        layer_counts = defaultdict(int)
        for module_info in self.modules.values():
            layer_counts[module_info.layer.value] += 1

        # Detect layer violations
        violations = []

        # Layer dependency rules (allowed dependencies)
        allowed_deps = {
            LayerType.PRESENTATION: {LayerType.BUSINESS, LayerType.UTILITY},
            LayerType.BUSINESS: {LayerType.DATA, LayerType.UTILITY},
            LayerType.DATA: {LayerType.UTILITY},
            LayerType.UTILITY: set()
        }

        for module_name, module_info in self.modules.items():
            from_layer = module_info.layer

            for dep_name in self.dependency_graph.get(module_name, []):
                if dep_name in self.modules:
                    to_layer = self.modules[dep_name].layer

                    # Skip if same layer or unknown layer
                    if from_layer == to_layer or from_layer == LayerType.UNKNOWN or to_layer == LayerType.UNKNOWN:
                        continue

                    # Check if dependency is allowed
                    if to_layer not in allowed_deps.get(from_layer, set()):
                        violation_type = self._classify_violation(from_layer, to_layer)
                        violations.append(LayerViolation(
                            from_module=module_name,
                            from_layer=from_layer.value,
                            to_module=dep_name,
                            to_layer=to_layer.value,
                            violation_type=violation_type
                        ))

        layer_analysis = {
            'layer_distribution': dict(layer_counts),
            'total_modules': len(self.modules),
            'violations_count': len(violations)
        }

        return layer_analysis, violations

    def _classify_violation(self, from_layer: LayerType, to_layer: LayerType) -> str:
        """Classify type of layer violation"""
        # Data layer should not depend on business or presentation
        if from_layer == LayerType.DATA and to_layer in {LayerType.BUSINESS, LayerType.PRESENTATION}:
            return "upward_dependency"

        # Business layer should not depend on presentation
        if from_layer == LayerType.BUSINESS and to_layer == LayerType.PRESENTATION:
            return "upward_dependency"

        # Presentation layer should not depend on data directly
        if from_layer == LayerType.PRESENTATION and to_layer == LayerType.DATA:
            return "layer_skip"

        return "invalid_dependency"

    def generate_mermaid_diagram(self, max_nodes: int = 20) -> str:
        """Generate Mermaid dependency diagram"""
        self.log("Generating Mermaid diagram...")

        # Limit nodes for readability
        nodes = list(self.dependency_graph.keys())[:max_nodes]

        lines = ["graph TD"]

        # Add nodes with layer colors
        layer_colors = {
            LayerType.PRESENTATION: "#e1f5ff",
            LayerType.BUSINESS: "#fff3e0",
            LayerType.DATA: "#f3e5f5",
            LayerType.UTILITY: "#e8f5e9",
            LayerType.UNKNOWN: "#f5f5f5"
        }

        for node in nodes:
            if node in self.modules:
                module_info = self.modules[node]
                color = layer_colors.get(module_info.layer, "#f5f5f5")
                # Simplify node name for diagram
                simple_name = node.split('.')[-1]
                lines.append(f'    {node.replace(".", "_")}["{simple_name}"]')
                lines.append(f'    style {node.replace(".", "_")} fill:{color}')

        # Add edges
        for source in nodes:
            for target in self.dependency_graph.get(source, []):
                if target in nodes:
                    lines.append(f'    {source.replace(".", "_")} --> {target.replace(".", "_")}')

        return "\n".join(lines)

    def calculate_health_score(self, analysis: ArchitectureAnalysis) -> float:
        """Calculate overall architecture health score (0-100)"""
        score = 100.0

        # Circular dependencies penalty
        if analysis.circular_dependencies:
            high_severity = sum(1 for cd in analysis.circular_dependencies if cd.severity == "high")
            medium_severity = sum(1 for cd in analysis.circular_dependencies if cd.severity == "medium")
            score -= (high_severity * 10) + (medium_severity * 5)

        # Anti-patterns penalty
        critical_ap = sum(1 for ap in analysis.anti_patterns if ap.severity == "critical")
        high_ap = sum(1 for ap in analysis.anti_patterns if ap.severity == "high")
        medium_ap = sum(1 for ap in analysis.anti_patterns if ap.severity == "medium")
        score -= (critical_ap * 15) + (high_ap * 10) + (medium_ap * 5)

        # Layer violations penalty
        score -= len(analysis.layer_violations) * 3

        # High instability penalty
        high_instability = sum(1 for cm in analysis.coupling_metrics if cm.instability > 0.9)
        score -= high_instability * 2

        return max(0.0, min(100.0, score))

    def analyze(self, generate_diagram: bool = False) -> ArchitectureAnalysis:
        """Run complete architecture analysis"""
        self.log(f"Starting architecture analysis of {self.root_path}")

        # Find and process all Python files
        python_files = self.find_python_files()
        self.log(f"Found {len(python_files)} Python files")

        for file_path in python_files:
            module_info = self.extract_module_info(file_path)
            if module_info:
                self.modules[module_info.name] = module_info

        self.log(f"Processed {len(self.modules)} modules")

        # Build dependency graph
        dependency_graph = self.build_dependency_graph()

        # Detect circular dependencies
        circular_deps = self.detect_circular_dependencies()

        # Calculate coupling metrics
        coupling_metrics = self.calculate_coupling_metrics()

        # Detect anti-patterns
        anti_patterns = self.detect_anti_patterns(coupling_metrics)

        # Analyze layers
        layer_analysis, layer_violations = self.analyze_layers()

        # Generate Mermaid diagram if requested
        mermaid_diagram = None
        if generate_diagram:
            mermaid_diagram = self.generate_mermaid_diagram()

        # Create analysis result
        analysis = ArchitectureAnalysis(
            summary={
                'total_modules': len(self.modules),
                'total_dependencies': dependency_graph.edge_count,
                'circular_dependencies_count': len(circular_deps),
                'anti_patterns_count': len(anti_patterns),
                'layer_violations_count': len(layer_violations),
                'health_score': 0.0  # Calculated below
            },
            dependency_graph=dependency_graph,
            circular_dependencies=circular_deps,
            coupling_metrics=coupling_metrics,
            anti_patterns=anti_patterns,
            layer_analysis=layer_analysis,
            layer_violations=layer_violations,
            mermaid_diagram=mermaid_diagram
        )

        # Calculate health score
        analysis.summary['health_score'] = self.calculate_health_score(analysis)

        return analysis


def format_text_output(analysis: ArchitectureAnalysis) -> str:
    """Format analysis results as human-readable text"""
    lines = []

    lines.append("=" * 80)
    lines.append("ARCHITECTURE HEALTH ANALYSIS REPORT")
    lines.append("=" * 80)
    lines.append("")

    # Summary
    lines.append("SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Total Modules:              {analysis.summary['total_modules']}")
    lines.append(f"Total Dependencies:         {analysis.summary['total_dependencies']}")
    lines.append(f"Circular Dependencies:      {analysis.summary['circular_dependencies_count']}")
    lines.append(f"Anti-Patterns Detected:     {analysis.summary['anti_patterns_count']}")
    lines.append(f"Layer Violations:           {analysis.summary['layer_violations_count']}")
    lines.append(f"Architecture Health Score:  {analysis.summary['health_score']:.1f}/100")
    lines.append("")

    # Health rating
    score = analysis.summary['health_score']
    if score >= 90:
        rating = "EXCELLENT"
    elif score >= 75:
        rating = "GOOD"
    elif score >= 60:
        rating = "FAIR"
    elif score >= 40:
        rating = "POOR"
    else:
        rating = "CRITICAL"
    lines.append(f"Overall Health:             {rating}")
    lines.append("")

    # Circular Dependencies
    if analysis.circular_dependencies:
        lines.append("CIRCULAR DEPENDENCIES")
        lines.append("-" * 80)
        for i, cd in enumerate(analysis.circular_dependencies[:10], 1):
            lines.append(f"{i}. Severity: {cd.severity.upper()}")
            lines.append(f"   Cycle: {' -> '.join(cd.cycle)}")
            lines.append("")
        if len(analysis.circular_dependencies) > 10:
            lines.append(f"... and {len(analysis.circular_dependencies) - 10} more")
            lines.append("")

    # Anti-Patterns (top 10)
    if analysis.anti_patterns:
        lines.append("ANTI-PATTERNS (Top 10)")
        lines.append("-" * 80)
        sorted_ap = sorted(analysis.anti_patterns, key=lambda x: x.severity, reverse=True)
        for i, ap in enumerate(sorted_ap[:10], 1):
            lines.append(f"{i}. {ap.type.upper()} - Severity: {ap.severity.upper()}")
            lines.append(f"   Module: {ap.module}")
            lines.append(f"   Description: {ap.description}")
            if ap.metrics:
                metrics_str = ", ".join(f"{k}={v}" for k, v in ap.metrics.items())
                lines.append(f"   Metrics: {metrics_str}")
            lines.append("")

    # Coupling Metrics (top 10 most coupled)
    lines.append("COUPLING METRICS (Top 10 Most Coupled)")
    lines.append("-" * 80)
    sorted_coupling = sorted(analysis.coupling_metrics,
                            key=lambda x: x.afferent_coupling + x.efferent_coupling,
                            reverse=True)
    for i, cm in enumerate(sorted_coupling[:10], 1):
        lines.append(f"{i}. {cm.module}")
        lines.append(f"   Afferent (Ca):  {cm.afferent_coupling} (incoming dependencies)")
        lines.append(f"   Efferent (Ce):  {cm.efferent_coupling} (outgoing dependencies)")
        lines.append(f"   Instability (I): {cm.instability:.3f}")
        lines.append("")

    # Layer Analysis
    lines.append("LAYER ANALYSIS")
    lines.append("-" * 80)
    lines.append("Layer Distribution:")
    for layer, count in analysis.layer_analysis['layer_distribution'].items():
        percentage = (count / analysis.layer_analysis['total_modules']) * 100
        lines.append(f"  {layer:15} {count:4} modules ({percentage:5.1f}%)")
    lines.append("")

    # Layer Violations
    if analysis.layer_violations:
        lines.append("LAYER VIOLATIONS (Top 10)")
        lines.append("-" * 80)
        for i, lv in enumerate(analysis.layer_violations[:10], 1):
            lines.append(f"{i}. {lv.violation_type.upper()}")
            lines.append(f"   From: {lv.from_module} ({lv.from_layer})")
            lines.append(f"   To:   {lv.to_module} ({lv.to_layer})")
            lines.append("")
        if len(analysis.layer_violations) > 10:
            lines.append(f"... and {len(analysis.layer_violations) - 10} more violations")
            lines.append("")

    # Mermaid Diagram
    if analysis.mermaid_diagram:
        lines.append("DEPENDENCY DIAGRAM (Mermaid)")
        lines.append("-" * 80)
        lines.append(analysis.mermaid_diagram)
        lines.append("")

    lines.append("=" * 80)
    lines.append("END OF REPORT")
    lines.append("=" * 80)

    return "\n".join(lines)


def format_csv_output(analysis: ArchitectureAnalysis) -> str:
    """Format coupling metrics as CSV"""
    lines = []
    lines.append("module,afferent_coupling,efferent_coupling,instability,layer")

    # Get layer for each module
    module_layers = {}
    for node in analysis.dependency_graph.nodes:
        # Extract layer from analysis if available
        module_layers[node] = "unknown"

    for cm in analysis.coupling_metrics:
        layer = module_layers.get(cm.module, "unknown")
        lines.append(f"{cm.module},{cm.afferent_coupling},{cm.efferent_coupling},{cm.instability:.3f},{layer}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze architectural patterns, coupling, and structural health",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input /path/to/codebase
  %(prog)s -i /path/to/codebase --output json --diagram
  %(prog)s -i . --file report.json --verbose
  %(prog)s -i src/ --output csv --file metrics.csv

Output Formats:
  text - Human-readable report with architecture health score
  json - Structured JSON with all metrics and findings
  csv  - CSV export of coupling metrics
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input directory path to analyze'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Save output to file instead of stdout'
    )

    parser.add_argument(
        '--diagram',
        action='store_true',
        help='Generate Mermaid dependency diagram'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Validate input path
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not input_path.is_dir():
        print(f"Error: Input path is not a directory: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Run analysis
    try:
        analyzer = ArchitectureHealthAnalyzer(input_path, verbose=args.verbose)
        analysis = analyzer.analyze(generate_diagram=args.diagram)

        # Format output
        if args.output == 'json':
            output = json.dumps(analysis.to_dict(), indent=2)
        elif args.output == 'csv':
            output = format_csv_output(analysis)
        else:  # text
            output = format_text_output(analysis)

        # Write output
        if args.file:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Analysis written to {args.file}", file=sys.stderr)
        else:
            print(output)

        # Exit with non-zero if health score is poor
        if analysis.summary['health_score'] < 60:
            sys.exit(1)

    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
