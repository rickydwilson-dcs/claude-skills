#!/usr/bin/env python3
"""
Project Architect
Analyzes project structure and detects architecture patterns.
Supports MVC, Clean Architecture, Hexagonal, Layered, and Microservices patterns.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict


# Architecture pattern definitions
ARCHITECTURE_PATTERNS = {
    'mvc': {
        'name': 'Model-View-Controller (MVC)',
        'description': 'Separates application into Model (data), View (UI), and Controller (logic)',
        'indicators': {
            'directories': ['models', 'views', 'controllers', 'model', 'view', 'controller'],
            'files': ['*Controller.*', '*Model.*', '*View.*'],
            'strong_signals': ['controllers/', 'views/', 'models/'],
        },
        'confidence_weight': 1.0,
    },
    'clean': {
        'name': 'Clean Architecture',
        'description': 'Dependency rule: outer layers depend on inner layers (entities, use cases, adapters, frameworks)',
        'indicators': {
            'directories': ['entities', 'use_cases', 'usecases', 'adapters', 'interfaces', 'infrastructure',
                          'domain', 'application', 'presentation'],
            'files': ['*UseCase.*', '*Entity.*', '*Repository.*', '*Interactor.*'],
            'strong_signals': ['domain/', 'application/', 'infrastructure/', 'use_cases/'],
        },
        'confidence_weight': 1.2,
    },
    'hexagonal': {
        'name': 'Hexagonal Architecture (Ports & Adapters)',
        'description': 'Core business logic isolated from external concerns via ports and adapters',
        'indicators': {
            'directories': ['ports', 'adapters', 'core', 'domain', 'application', 'inbound', 'outbound'],
            'files': ['*Port.*', '*Adapter.*', '*Gateway.*'],
            'strong_signals': ['ports/', 'adapters/', 'inbound/', 'outbound/'],
        },
        'confidence_weight': 1.3,
    },
    'layered': {
        'name': 'Layered Architecture (N-Tier)',
        'description': 'Traditional layers: presentation, business logic, data access',
        'indicators': {
            'directories': ['presentation', 'business', 'data', 'dal', 'bll', 'services', 'repositories',
                          'api', 'service', 'repository', 'dao'],
            'files': ['*Service.*', '*Repository.*', '*DAO.*'],
            'strong_signals': ['services/', 'repositories/', 'dal/', 'bll/'],
        },
        'confidence_weight': 0.8,
    },
    'microservices': {
        'name': 'Microservices Architecture',
        'description': 'Independent, loosely coupled services with their own data stores',
        'indicators': {
            'directories': ['services', 'microservices', 'api-gateway', 'gateway'],
            'files': ['docker-compose.*', 'Dockerfile', '*.service.*', 'k8s/', 'kubernetes/'],
            'strong_signals': ['services/*/', 'microservices/*/', 'docker-compose.yml'],
        },
        'confidence_weight': 1.1,
    },
    'modular_monolith': {
        'name': 'Modular Monolith',
        'description': 'Monolithic application with well-defined module boundaries',
        'indicators': {
            'directories': ['modules', 'features', 'packages', 'apps'],
            'files': ['module.json', 'feature.json'],
            'strong_signals': ['modules/*/', 'features/*/'],
        },
        'confidence_weight': 0.9,
    },
    'component_based': {
        'name': 'Component-Based Architecture',
        'description': 'UI organized around reusable components (common in React, Vue, Angular)',
        'indicators': {
            'directories': ['components', 'containers', 'pages', 'layouts', 'hooks', 'context'],
            'files': ['*.component.*', '*.tsx', '*.jsx', '*.vue'],
            'strong_signals': ['components/', 'containers/', 'pages/'],
        },
        'confidence_weight': 0.9,
    },
}


class StructureAnalyzer:
    """Analyzes project directory structure"""

    def __init__(self, root_path: Path, verbose: bool = False):
        self.root_path = root_path
        self.verbose = verbose
        self.structure: Dict = {}
        self.directories: Set[str] = set()
        self.files: Set[str] = set()
        self.file_extensions: Dict[str, int] = defaultdict(int)

    def analyze(self) -> Dict:
        """Analyze the project structure"""
        self._scan_directory(self.root_path)

        return {
            'total_directories': len(self.directories),
            'total_files': len(self.files),
            'file_extensions': dict(self.file_extensions),
            'directories': list(self.directories),
            'structure': self.structure,
        }

    def _scan_directory(self, path: Path, depth: int = 0, max_depth: int = 5) -> Dict:
        """Recursively scan directory structure"""
        if depth > max_depth:
            return {}

        # Skip common non-source directories
        skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'env', 'dist',
                    'build', '.next', 'coverage', '.idea', '.vscode', 'target'}

        result = {'type': 'directory', 'children': {}}

        try:
            for item in path.iterdir():
                if item.name.startswith('.') and item.name not in ['.env', '.env.example']:
                    continue

                if item.is_dir():
                    if item.name in skip_dirs:
                        continue

                    rel_path = str(item.relative_to(self.root_path))
                    self.directories.add(rel_path)

                    if self.verbose and depth < 2:
                        print(f"  Scanning: {rel_path}/", file=sys.stderr)

                    result['children'][item.name] = self._scan_directory(item, depth + 1, max_depth)
                else:
                    rel_path = str(item.relative_to(self.root_path))
                    self.files.add(rel_path)

                    # Track file extensions
                    ext = item.suffix.lower()
                    if ext:
                        self.file_extensions[ext] += 1

                    result['children'][item.name] = {'type': 'file', 'extension': ext}

        except PermissionError:
            pass

        return result


class PatternDetector:
    """Detects architecture patterns in a project"""

    def __init__(self, directories: Set[str], files: Set[str], verbose: bool = False):
        self.directories = directories
        self.files = files
        self.verbose = verbose

    def detect(self) -> List[Dict]:
        """Detect all matching architecture patterns"""
        matches = []

        for pattern_id, pattern_def in ARCHITECTURE_PATTERNS.items():
            score, evidence = self._calculate_pattern_score(pattern_def)

            if score > 0:
                confidence = self._calculate_confidence(score, pattern_def['confidence_weight'])
                matches.append({
                    'pattern': pattern_id,
                    'name': pattern_def['name'],
                    'description': pattern_def['description'],
                    'score': score,
                    'confidence': confidence,
                    'confidence_level': self._confidence_level(confidence),
                    'evidence': evidence,
                })

        # Sort by confidence descending
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        return matches

    def _calculate_pattern_score(self, pattern_def: Dict) -> Tuple[int, List[str]]:
        """Calculate match score for a pattern"""
        score = 0
        evidence = []

        indicators = pattern_def['indicators']

        # Check directories
        dir_names = {d.split('/')[-1].lower() for d in self.directories}
        for indicator_dir in indicators.get('directories', []):
            if indicator_dir.lower() in dir_names:
                score += 1
                evidence.append(f"Directory match: {indicator_dir}/")

        # Check for strong signals (path patterns)
        for signal in indicators.get('strong_signals', []):
            signal_pattern = signal.rstrip('/').lower()
            for directory in self.directories:
                if signal_pattern in directory.lower():
                    score += 2
                    evidence.append(f"Strong signal: {directory}")
                    break

        # Check file patterns
        for file_pattern in indicators.get('files', []):
            # Convert glob-like pattern to regex
            regex_pattern = file_pattern.replace('.', r'\.').replace('*', '.*')
            try:
                pattern = re.compile(regex_pattern, re.IGNORECASE)
                for file in self.files:
                    file_name = file.split('/')[-1]
                    if pattern.match(file_name):
                        score += 0.5
                        if len(evidence) < 10:  # Limit evidence entries
                            evidence.append(f"File match: {file_name}")
                        break
            except re.error:
                pass

        return score, evidence

    def _calculate_confidence(self, score: int, weight: float) -> float:
        """Calculate confidence percentage"""
        # Normalize score to 0-100 range
        raw_confidence = min(score * 15 * weight, 100)
        return round(raw_confidence, 1)

    def _confidence_level(self, confidence: float) -> str:
        """Convert confidence to human-readable level"""
        if confidence >= 80:
            return 'HIGH'
        elif confidence >= 50:
            return 'MEDIUM'
        elif confidence >= 25:
            return 'LOW'
        else:
            return 'VERY_LOW'


class LayerViolationDetector:
    """Detects potential layer violations in the architecture"""

    # Layer dependencies (what each layer should NOT depend on)
    LAYER_RULES = {
        'domain': {'presentation', 'ui', 'views', 'controllers', 'infrastructure', 'frameworks'},
        'entities': {'presentation', 'ui', 'views', 'controllers', 'infrastructure', 'adapters'},
        'use_cases': {'presentation', 'ui', 'views', 'controllers', 'infrastructure'},
        'core': {'presentation', 'ui', 'views', 'controllers', 'infrastructure', 'adapters'},
        'models': {'views', 'controllers', 'presentation'},
    }

    def __init__(self, root_path: Path, verbose: bool = False):
        self.root_path = root_path
        self.verbose = verbose

    def detect(self) -> List[Dict]:
        """Detect layer violations by analyzing imports"""
        violations = []

        # Scan Python files for import violations
        for py_file in self.root_path.glob('**/*.py'):
            if self._should_skip(py_file):
                continue

            file_layer = self._get_layer(py_file)
            if not file_layer:
                continue

            forbidden = self.LAYER_RULES.get(file_layer, set())
            if not forbidden:
                continue

            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                imports = self._extract_imports(content)

                for imp in imports:
                    imp_lower = imp.lower()
                    for forbidden_layer in forbidden:
                        if forbidden_layer in imp_lower:
                            violations.append({
                                'file': str(py_file.relative_to(self.root_path)),
                                'layer': file_layer,
                                'violation': f"Imports from forbidden layer: {imp}",
                                'forbidden_layer': forbidden_layer,
                                'severity': 'medium',
                            })
                            break

            except Exception as e:
                if self.verbose:
                    print(f"  Warning: Could not analyze {py_file}: {e}", file=sys.stderr)

        return violations

    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'env',
                    'dist', 'build', 'test', 'tests', '__tests__'}
        return any(part in skip_dirs for part in file_path.parts)

    def _get_layer(self, file_path: Path) -> Optional[str]:
        """Determine which layer a file belongs to"""
        path_parts = [p.lower() for p in file_path.parts]

        for layer in self.LAYER_RULES.keys():
            if layer in path_parts:
                return layer

        return None

    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from Python code"""
        imports = []
        import_pattern = re.compile(r'^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))', re.MULTILINE)

        for match in import_pattern.finditer(content):
            imp = match.group(1) or match.group(2)
            if imp:
                imports.append(imp)

        return imports


class ProjectArchitect:
    """Main class for project architecture analysis"""

    def __init__(self, target_path: str, verbose: bool = False):
        self.target_path = Path(target_path)
        self.verbose = verbose
        self.results: Dict = {}

    def run(self) -> Dict:
        """Execute the main functionality"""
        if self.verbose:
            print(f"Analyzing project architecture: {self.target_path}", file=sys.stderr)

        self.validate_target()
        self.analyze_structure()
        self.detect_patterns()
        self.detect_violations()
        self.generate_assessment()

        return self.results

    def validate_target(self):
        """Validate the target path exists"""
        if not self.target_path.exists():
            raise ValueError(f"Target path does not exist: {self.target_path}")

        if not self.target_path.is_dir():
            raise ValueError(f"Target must be a directory: {self.target_path}")

    def analyze_structure(self):
        """Analyze the project structure"""
        analyzer = StructureAnalyzer(self.target_path, self.verbose)
        structure = analyzer.analyze()

        self.results['structure'] = {
            'total_directories': structure['total_directories'],
            'total_files': structure['total_files'],
            'file_extensions': structure['file_extensions'],
            'top_level_directories': [
                d for d in structure['directories'] if '/' not in d
            ],
        }

        self._directories = set(structure['directories'])
        self._files = set(analyzer.files)

        if self.verbose:
            print(f"  Found {structure['total_directories']} directories, "
                  f"{structure['total_files']} files", file=sys.stderr)

    def detect_patterns(self):
        """Detect architecture patterns"""
        detector = PatternDetector(self._directories, self._files, self.verbose)
        patterns = detector.detect()

        self.results['patterns'] = patterns
        self.results['primary_pattern'] = patterns[0] if patterns else None

        if self.verbose and patterns:
            print(f"  Primary pattern: {patterns[0]['name']} "
                  f"({patterns[0]['confidence']}% confidence)", file=sys.stderr)

    def detect_violations(self):
        """Detect architecture violations"""
        detector = LayerViolationDetector(self.target_path, self.verbose)
        violations = detector.detect()

        self.results['violations'] = violations
        self.results['violation_count'] = len(violations)

        if self.verbose:
            print(f"  Found {len(violations)} potential violations", file=sys.stderr)

    def generate_assessment(self):
        """Generate overall architecture assessment"""
        primary = self.results.get('primary_pattern')
        violations = self.results.get('violation_count', 0)

        # Calculate health score
        health_score = 100

        # Deduct for no clear pattern
        if not primary or primary['confidence'] < 30:
            health_score -= 30
            pattern_clarity = 'unclear'
        elif primary['confidence'] < 50:
            health_score -= 15
            pattern_clarity = 'emerging'
        elif primary['confidence'] < 70:
            health_score -= 5
            pattern_clarity = 'moderate'
        else:
            pattern_clarity = 'clear'

        # Deduct for violations
        if violations > 10:
            health_score -= 30
        elif violations > 5:
            health_score -= 20
        elif violations > 0:
            health_score -= 10

        health_score = max(0, health_score)

        # Determine overall rating
        if health_score >= 80:
            rating = 'EXCELLENT'
        elif health_score >= 60:
            rating = 'GOOD'
        elif health_score >= 40:
            rating = 'FAIR'
        else:
            rating = 'NEEDS_IMPROVEMENT'

        self.results['assessment'] = {
            'health_score': health_score,
            'rating': rating,
            'pattern_clarity': pattern_clarity,
            'recommendations': self._generate_recommendations(primary, violations, pattern_clarity),
        }

    def _generate_recommendations(self, primary: Optional[Dict], violations: int,
                                  pattern_clarity: str) -> List[str]:
        """Generate architecture recommendations"""
        recommendations = []

        if pattern_clarity in ('unclear', 'emerging'):
            recommendations.append(
                "Consider adopting a clear architecture pattern to improve maintainability"
            )

        if violations > 5:
            recommendations.append(
                f"Address {violations} layer violations to maintain architectural integrity"
            )

        if primary:
            if primary['pattern'] == 'mvc':
                recommendations.append(
                    "Ensure controllers remain thin and delegate business logic to services"
                )
            elif primary['pattern'] in ('clean', 'hexagonal'):
                recommendations.append(
                    "Verify that domain layer has no dependencies on infrastructure"
                )
            elif primary['pattern'] == 'layered':
                recommendations.append(
                    "Consider introducing interfaces between layers for better testability"
                )
            elif primary['pattern'] == 'component_based':
                recommendations.append(
                    "Extract shared logic into custom hooks or utility modules"
                )

        if not recommendations:
            recommendations.append("Architecture appears well-structured. Continue following current patterns.")

        return recommendations


def format_text_output(results: Dict) -> str:
    """Format results as human-readable text"""
    lines = ["=" * 60]
    lines.append("PROJECT ARCHITECTURE ANALYSIS")
    lines.append("=" * 60)

    # Structure summary
    structure = results.get('structure', {})
    lines.append(f"\nProject Structure:")
    lines.append(f"  Directories: {structure.get('total_directories', 0)}")
    lines.append(f"  Files: {structure.get('total_files', 0)}")

    top_dirs = structure.get('top_level_directories', [])
    if top_dirs:
        lines.append(f"\n  Top-Level Directories:")
        for d in sorted(top_dirs)[:15]:
            lines.append(f"    - {d}/")
        if len(top_dirs) > 15:
            lines.append(f"    ... and {len(top_dirs) - 15} more")

    # File extensions
    extensions = structure.get('file_extensions', {})
    if extensions:
        top_ext = sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]
        lines.append(f"\n  Top File Types:")
        for ext, count in top_ext:
            lines.append(f"    {ext}: {count} files")

    # Architecture patterns
    lines.append(f"\n{'=' * 60}")
    lines.append("DETECTED ARCHITECTURE PATTERNS")
    lines.append("=" * 60)

    patterns = results.get('patterns', [])
    if patterns:
        for i, pattern in enumerate(patterns[:5], 1):
            lines.append(f"\n{i}. {pattern['name']}")
            lines.append(f"   Confidence: {pattern['confidence']}% ({pattern['confidence_level']})")
            lines.append(f"   Description: {pattern['description']}")

            if pattern.get('evidence'):
                lines.append(f"   Evidence:")
                for evidence in pattern['evidence'][:5]:
                    lines.append(f"     - {evidence}")
    else:
        lines.append("\nNo clear architecture pattern detected.")

    # Violations
    violations = results.get('violations', [])
    if violations:
        lines.append(f"\n{'=' * 60}")
        lines.append(f"POTENTIAL VIOLATIONS ({len(violations)} found)")
        lines.append("=" * 60)

        for v in violations[:10]:
            lines.append(f"\n  [{v['severity'].upper()}] {v['file']}")
            lines.append(f"    Layer: {v['layer']}")
            lines.append(f"    Issue: {v['violation']}")

        if len(violations) > 10:
            lines.append(f"\n  ... and {len(violations) - 10} more violations")

    # Assessment
    assessment = results.get('assessment', {})
    lines.append(f"\n{'=' * 60}")
    lines.append("ARCHITECTURE ASSESSMENT")
    lines.append("=" * 60)

    lines.append(f"\n  Health Score: {assessment.get('health_score', 0)}/100")
    lines.append(f"  Rating: {assessment.get('rating', 'N/A')}")
    lines.append(f"  Pattern Clarity: {assessment.get('pattern_clarity', 'N/A')}")

    recommendations = assessment.get('recommendations', [])
    if recommendations:
        lines.append(f"\n  Recommendations:")
        for rec in recommendations:
            lines.append(f"    - {rec}")

    return '\n'.join(lines)


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="Analyze project structure and detect architecture patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input ./my-project
  %(prog)s --input ./src --output json
  %(prog)s --input ./project -o json --file analysis.json
  %(prog)s --input ./project -v

Detected Architecture Patterns:
  - MVC (Model-View-Controller)
  - Clean Architecture
  - Hexagonal Architecture (Ports & Adapters)
  - Layered Architecture (N-Tier)
  - Microservices
  - Modular Monolith
  - Component-Based (React/Vue/Angular)

Analysis includes:
  - Directory structure analysis
  - Architecture pattern detection with confidence scores
  - Layer violation detection
  - Health assessment and recommendations

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Project directory to analyze'
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
        architect = ProjectArchitect(
            args.target,
            verbose=args.verbose
        )

        results = architect.run()

        if args.output == 'json':
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
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
