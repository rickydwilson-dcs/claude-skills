#!/usr/bin/env python3
"""
Code Quality Analyzer for Legacy Codebases

Measures code quality metrics including complexity, duplication, maintainability,
and documentation coverage using Python's AST module.

Features:
- Cyclomatic complexity calculation per function
- Token-based code duplication detection
- Function length and parameter count analysis
- Nesting depth measurement
- Documentation coverage assessment
- Test coverage estimation
- Overall quality scoring with letter grades

Usage:
    python code_quality_analyzer.py --input /path/to/code
    python code_quality_analyzer.py -i ./src --output json --file report.json
    python code_quality_analyzer.py -i ./src --threshold-complexity 15 --verbose
"""

from collections import defaultdict
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Optional
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

@dataclass
class ComplexityResult:
    """Function complexity measurement"""
    function_name: str
    file_path: str
    line_number: int
    complexity: int
    parameters: int
    length: int
    has_docstring: bool
    max_nesting: int


@dataclass
class DuplicationBlock:
    """Code duplication detection result"""
    content: str
    occurrences: int
    file_locations: List[Dict[str, Any]]
    line_count: int


@dataclass
class CodeSmell:
    """Code smell detection result"""
    type: str
    severity: str  # high, medium, low
    file_path: str
    line_number: int
    function_name: str
    description: str
    metric_value: Any


@dataclass
class QualityMetrics:
    """Overall quality metrics"""
    total_files: int = 0
    total_lines: int = 0
    total_functions: int = 0
    average_complexity: float = 0.0
    max_complexity: int = 0
    average_function_length: float = 0.0
    average_parameters: float = 0.0
    documentation_coverage: float = 0.0
    test_coverage_estimate: float = 0.0
    duplication_percentage: float = 0.0


@dataclass
class QualityScore:
    """Quality scoring breakdown"""
    overall: float = 0.0
    complexity_score: float = 0.0
    duplication_score: float = 0.0
    documentation_score: float = 0.0
    maintainability_score: float = 0.0
    grade: str = "F"


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    quality_score: QualityScore
    metrics: QualityMetrics
    complexity_results: List[ComplexityResult] = field(default_factory=list)
    duplicate_blocks: List[DuplicationBlock] = field(default_factory=list)
    code_smells: List[CodeSmell] = field(default_factory=list)
    high_complexity_functions: List[Dict[str, Any]] = field(default_factory=list)


class ComplexityCalculator(ast.NodeVisitor):
    """Calculate cyclomatic complexity using AST"""

    def __init__(self):
        self.complexity = 1
        self.max_nesting = 0
        self.current_nesting = 0

    def visit_If(self, node):
        self.complexity += 1
        self._visit_with_nesting(node)

    def visit_For(self, node):
        self.complexity += 1
        self._visit_with_nesting(node)

    def visit_While(self, node):
        self.complexity += 1
        self._visit_with_nesting(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self._visit_with_nesting(node)

    def visit_With(self, node):
        self.complexity += 1
        self._visit_with_nesting(node)

    def visit_Assert(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        # Count 'and'/'or' operators
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        # Ternary operator
        self.complexity += 1
        self.generic_visit(node)

    def _visit_with_nesting(self, node):
        """Track nesting depth"""
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1


class FunctionAnalyzer(ast.NodeVisitor):
    """Analyze functions in Python source code"""

    def __init__(self, file_path: str, source_lines: List[str]):
        self.file_path = file_path
        self.source_lines = source_lines
        self.results: List[ComplexityResult] = []

    def visit_FunctionDef(self, node):
        self._analyze_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._analyze_function(node)
        self.generic_visit(node)

    def _analyze_function(self, node):
        """Analyze a single function"""
        # Calculate complexity
        calculator = ComplexityCalculator()
        calculator.visit(node)

        # Get function details
        function_name = node.name
        line_number = node.lineno

        # Count parameters
        parameters = len(node.args.args) + len(node.args.posonlyargs) + len(node.args.kwonlyargs)
        if node.args.vararg:
            parameters += 1
        if node.args.kwarg:
            parameters += 1

        # Calculate function length
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else line_number
        length = end_line - line_number + 1

        # Check for docstring
        has_docstring = (
            isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.body[0].value.value, str)
        ) if node.body else False

        result = ComplexityResult(
            function_name=function_name,
            file_path=self.file_path,
            line_number=line_number,
            complexity=calculator.complexity,
            parameters=parameters,
            length=length,
            has_docstring=has_docstring,
            max_nesting=calculator.max_nesting
        )

        self.results.append(result)


class CodeQualityAnalyzer:
    """Main analyzer for code quality metrics"""

    def __init__(self, input_path: str, threshold_complexity: int = 10,
                 threshold_duplication: int = 5, verbose: bool = False):
        self.input_path = Path(input_path)
        self.threshold_complexity = threshold_complexity
        self.threshold_duplication = threshold_duplication
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("CodeQualityAnalyzer initialized")

        self.complexity_results: List[ComplexityResult] = []
        self.code_smells: List[CodeSmell] = []
        self.metrics = QualityMetrics()

        # For duplication detection
        self.line_hashes: Dict[int, List[Tuple[str, int]]] = defaultdict(list)
        self.duplicate_blocks: List[DuplicationBlock] = []

    def analyze(self) -> AnalysisResult:
        """Run complete code quality analysis"""
        if self.verbose:
            print(f"Analyzing code in: {self.input_path}")

        # Collect all Python files
        python_files = self._find_python_files()
        test_files = [f for f in python_files if self._is_test_file(f)]
        source_files = [f for f in python_files if not self._is_test_file(f)]

        if self.verbose:
            print(f"Found {len(python_files)} Python files ({len(source_files)} source, {len(test_files)} test)")

        # Analyze each file
        total_lines = 0
        for file_path in python_files:
            if self.verbose:
                print(f"  Analyzing: {file_path}")

            file_lines = self._analyze_file(file_path)
            total_lines += file_lines

        # Calculate metrics
        self.metrics.total_files = len(source_files)
        self.metrics.total_lines = total_lines
        self.metrics.total_functions = len(self.complexity_results)

        if self.complexity_results:
            complexities = [r.complexity for r in self.complexity_results]
            self.metrics.average_complexity = sum(complexities) / len(complexities)
            self.metrics.max_complexity = max(complexities)

            lengths = [r.length for r in self.complexity_results]
            self.metrics.average_function_length = sum(lengths) / len(lengths)

            params = [r.parameters for r in self.complexity_results]
            self.metrics.average_parameters = sum(params) / len(params)

            documented = sum(1 for r in self.complexity_results if r.has_docstring)
            self.metrics.documentation_coverage = (documented / len(self.complexity_results)) * 100

        # Test coverage estimate
        if source_files:
            self.metrics.test_coverage_estimate = (len(test_files) / len(source_files)) * 100

        # Detect duplication
        self._detect_duplication()

        # Calculate quality score
        quality_score = self._calculate_quality_score()

        # Find high complexity functions
        high_complexity = [
            {
                "function": r.function_name,
                "file": r.file_path,
                "line": r.line_number,
                "complexity": r.complexity
            }
            for r in sorted(self.complexity_results, key=lambda x: x.complexity, reverse=True)[:10]
        ]

        return AnalysisResult(
            quality_score=quality_score,
            metrics=self.metrics,
            complexity_results=self.complexity_results,
            duplicate_blocks=self.duplicate_blocks,
            code_smells=self.code_smells,
            high_complexity_functions=high_complexity
        )

    def _find_python_files(self) -> List[str]:
        """Find all Python files in input path"""
        python_files = []

        if self.input_path.is_file():
            if self.input_path.suffix == '.py':
                python_files.append(str(self.input_path))
        else:
            for root, _, files in os.walk(self.input_path):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))

        return python_files

    def _is_test_file(self, file_path: str) -> bool:
        """Check if file is a test file"""
        file_name = os.path.basename(file_path)
        return (
            file_name.startswith('test_') or
            file_name.endswith('_test.py') or
            'test' in Path(file_path).parts
        )

    def _analyze_file(self, file_path: str) -> int:
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()

            # Parse AST
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                if self.verbose:
                    print(f"    Warning: Syntax error in {file_path}: {e}")
                return len(lines)

            # Analyze functions
            analyzer = FunctionAnalyzer(file_path, lines)
            analyzer.visit(tree)
            self.complexity_results.extend(analyzer.results)

            # Detect code smells
            self._detect_code_smells(analyzer.results)

            # Store line hashes for duplication detection
            self._hash_lines(file_path, lines)

            return len(lines)

        except Exception as e:
            if self.verbose:
                print(f"    Error analyzing {file_path}: {e}")
            return 0

    def _hash_lines(self, file_path: str, lines: List[str]):
        """Hash lines for duplication detection"""
        for i, line in enumerate(lines, 1):
            # Normalize: strip whitespace and ignore comments/empty lines
            normalized = line.strip()
            if normalized and not normalized.startswith('#'):
                line_hash = hash(normalized)
                self.line_hashes[line_hash].append((file_path, i))

    def _detect_duplication(self):
        """Detect duplicate code blocks"""
        # Find lines that appear multiple times
        duplicates = {
            h: locations for h, locations in self.line_hashes.items()
            if len(locations) >= self.threshold_duplication
        }

        if not duplicates:
            self.metrics.duplication_percentage = 0.0
            return

        # Group into blocks
        for line_hash, locations in duplicates.items():
            # Get the actual line content from first occurrence
            file_path, line_num = locations[0]
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    content = lines[line_num - 1].strip() if line_num <= len(lines) else "Unknown"
            except Exception:
                content = "Unknown"

            block = DuplicationBlock(
                content=content,
                occurrences=len(locations),
                file_locations=[
                    {"file": loc[0], "line": loc[1]} for loc in locations
                ],
                line_count=1
            )
            self.duplicate_blocks.append(block)

        # Calculate duplication percentage
        total_lines = self.metrics.total_lines
        duplicate_lines = sum(block.occurrences for block in self.duplicate_blocks)
        self.metrics.duplication_percentage = (duplicate_lines / total_lines * 100) if total_lines > 0 else 0.0

    def _detect_code_smells(self, results: List[ComplexityResult]):
        """Detect code smells from complexity results"""
        for result in results:
            # High complexity
            if result.complexity > self.threshold_complexity:
                self.code_smells.append(CodeSmell(
                    type="high_complexity",
                    severity="high" if result.complexity > self.threshold_complexity * 2 else "medium",
                    file_path=result.file_path,
                    line_number=result.line_number,
                    function_name=result.function_name,
                    description=f"Function has cyclomatic complexity of {result.complexity}",
                    metric_value=result.complexity
                ))

            # Long function
            if result.length > 50:
                self.code_smells.append(CodeSmell(
                    type="long_function",
                    severity="medium" if result.length < 100 else "high",
                    file_path=result.file_path,
                    line_number=result.line_number,
                    function_name=result.function_name,
                    description=f"Function is {result.length} lines long",
                    metric_value=result.length
                ))

            # Too many parameters
            if result.parameters > 5:
                self.code_smells.append(CodeSmell(
                    type="too_many_parameters",
                    severity="medium",
                    file_path=result.file_path,
                    line_number=result.line_number,
                    function_name=result.function_name,
                    description=f"Function has {result.parameters} parameters",
                    metric_value=result.parameters
                ))

            # Deep nesting
            if result.max_nesting > 4:
                self.code_smells.append(CodeSmell(
                    type="deep_nesting",
                    severity="high" if result.max_nesting > 6 else "medium",
                    file_path=result.file_path,
                    line_number=result.line_number,
                    function_name=result.function_name,
                    description=f"Function has nesting depth of {result.max_nesting}",
                    metric_value=result.max_nesting
                ))

            # Missing docstring
            if not result.has_docstring:
                self.code_smells.append(CodeSmell(
                    type="missing_docstring",
                    severity="low",
                    file_path=result.file_path,
                    line_number=result.line_number,
                    function_name=result.function_name,
                    description="Function missing docstring",
                    metric_value=False
                ))

    def _calculate_quality_score(self) -> QualityScore:
        """Calculate overall quality score"""
        # Complexity score (0-100)
        # Lower complexity is better
        if self.metrics.average_complexity <= 5:
            complexity_score = 100
        elif self.metrics.average_complexity <= 10:
            complexity_score = 80
        elif self.metrics.average_complexity <= 15:
            complexity_score = 60
        elif self.metrics.average_complexity <= 20:
            complexity_score = 40
        else:
            complexity_score = max(0, 40 - (self.metrics.average_complexity - 20) * 2)

        # Duplication score (0-100)
        # Lower duplication is better
        if self.metrics.duplication_percentage <= 5:
            duplication_score = 100
        elif self.metrics.duplication_percentage <= 10:
            duplication_score = 80
        elif self.metrics.duplication_percentage <= 15:
            duplication_score = 60
        else:
            duplication_score = max(0, 60 - (self.metrics.duplication_percentage - 15) * 3)

        # Documentation score (0-100)
        documentation_score = self.metrics.documentation_coverage

        # Maintainability score (0-100)
        # Based on function length and parameters
        length_score = 100 if self.metrics.average_function_length <= 30 else max(0, 100 - (self.metrics.average_function_length - 30))
        param_score = 100 if self.metrics.average_parameters <= 3 else max(0, 100 - (self.metrics.average_parameters - 3) * 20)
        maintainability_score = (length_score + param_score) / 2

        # Overall score (weighted average)
        overall = (
            complexity_score * 0.30 +
            duplication_score * 0.25 +
            documentation_score * 0.20 +
            maintainability_score * 0.25
        )

        # Assign grade
        if overall >= 90:
            grade = "A"
        elif overall >= 80:
            grade = "B"
        elif overall >= 70:
            grade = "C"
        elif overall >= 60:
            grade = "D"
        else:
            grade = "F"

        return QualityScore(
            overall=round(overall, 2),
            complexity_score=round(complexity_score, 2),
            duplication_score=round(duplication_score, 2),
            documentation_score=round(documentation_score, 2),
            maintainability_score=round(maintainability_score, 2),
            grade=grade
        )


class OutputFormatter:
    """Format analysis results in various formats"""

    @staticmethod
    def format_text(result: AnalysisResult, verbose: bool = False) -> str:
        """Format results as human-readable text"""
        lines = []
        lines.append("=" * 80)
        lines.append("CODE QUALITY ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Quality Score
        lines.append("QUALITY SCORE")
        lines.append("-" * 80)
        lines.append(f"Overall Score: {result.quality_score.overall}/100 (Grade: {result.quality_score.grade})")
        lines.append(f"  - Complexity Score:      {result.quality_score.complexity_score}/100")
        lines.append(f"  - Duplication Score:     {result.quality_score.duplication_score}/100")
        lines.append(f"  - Documentation Score:   {result.quality_score.documentation_score}/100")
        lines.append(f"  - Maintainability Score: {result.quality_score.maintainability_score}/100")
        lines.append("")

        # Metrics
        lines.append("METRICS")
        lines.append("-" * 80)
        lines.append(f"Total Files:              {result.metrics.total_files}")
        lines.append(f"Total Lines:              {result.metrics.total_lines}")
        lines.append(f"Total Functions:          {result.metrics.total_functions}")
        lines.append(f"Average Complexity:       {result.metrics.average_complexity:.2f}")
        lines.append(f"Max Complexity:           {result.metrics.max_complexity}")
        lines.append(f"Average Function Length:  {result.metrics.average_function_length:.2f} lines")
        lines.append(f"Average Parameters:       {result.metrics.average_parameters:.2f}")
        lines.append(f"Documentation Coverage:   {result.metrics.documentation_coverage:.2f}%")
        lines.append(f"Test Coverage Estimate:   {result.metrics.test_coverage_estimate:.2f}%")
        lines.append(f"Code Duplication:         {result.metrics.duplication_percentage:.2f}%")
        lines.append("")

        # High Complexity Functions
        if result.high_complexity_functions:
            lines.append("HIGH COMPLEXITY FUNCTIONS (Top 10)")
            lines.append("-" * 80)
            for func in result.high_complexity_functions[:10]:
                lines.append(f"  {func['function']} (complexity: {func['complexity']})")
                lines.append(f"    {func['file']}:{func['line']}")
            lines.append("")

        # Code Smells Summary
        if result.code_smells:
            smell_counts = defaultdict(int)
            for smell in result.code_smells:
                smell_counts[smell.type] += 1

            lines.append("CODE SMELLS SUMMARY")
            lines.append("-" * 80)
            lines.append(f"Total Code Smells: {len(result.code_smells)}")
            for smell_type, count in sorted(smell_counts.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"  - {smell_type.replace('_', ' ').title()}: {count}")
            lines.append("")

            if verbose:
                lines.append("CODE SMELLS DETAIL")
                lines.append("-" * 80)
                for smell in sorted(result.code_smells, key=lambda x: (x.severity, x.type)):
                    lines.append(f"[{smell.severity.upper()}] {smell.type.replace('_', ' ').title()}")
                    lines.append(f"  Function: {smell.function_name}")
                    lines.append(f"  Location: {smell.file_path}:{smell.line_number}")
                    lines.append(f"  {smell.description}")
                    lines.append("")

        # Duplication
        if result.duplicate_blocks:
            lines.append(f"CODE DUPLICATION ({len(result.duplicate_blocks)} blocks)")
            lines.append("-" * 80)
            for i, block in enumerate(result.duplicate_blocks[:5], 1):
                lines.append(f"Block {i}: {block.occurrences} occurrences")
                if verbose:
                    for loc in block.file_locations[:3]:
                        lines.append(f"  - {loc['file']}:{loc['line']}")
                    if len(block.file_locations) > 3:
                        lines.append(f"  ... and {len(block.file_locations) - 3} more")
            if len(result.duplicate_blocks) > 5:
                lines.append(f"... and {len(result.duplicate_blocks) - 5} more duplicate blocks")
            lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)

    @staticmethod
    def format_json(result: AnalysisResult) -> str:
        """Format results as JSON"""
        data = {
            "quality_score": asdict(result.quality_score),
            "metrics": asdict(result.metrics),
            "high_complexity_functions": result.high_complexity_functions,
            "code_smells": [asdict(smell) for smell in result.code_smells],
            "duplicate_blocks": [asdict(block) for block in result.duplicate_blocks]
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def format_csv(result: AnalysisResult) -> str:
        """Format results as CSV (per-function metrics)"""
        lines = []
        lines.append("file,function,line,complexity,parameters,length,has_docstring,max_nesting")

        for func in result.complexity_results:
            lines.append(
                f"{func.file_path},{func.function_name},{func.line_number},"
                f"{func.complexity},{func.parameters},{func.length},"
                f"{func.has_docstring},{func.max_nesting}"
            )

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze code quality metrics for legacy codebases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze directory with default settings
  python code_quality_analyzer.py --input ./src

  # Generate JSON report
  python code_quality_analyzer.py -i ./src --output json --file report.json

  # Custom thresholds with verbose output
  python code_quality_analyzer.py -i ./src --threshold-complexity 15 --verbose

  # Generate CSV of function metrics
  python code_quality_analyzer.py -i ./src --output csv --file metrics.csv
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input file or directory to analyze'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Output file path (prints to stdout if not specified)'
    )

    parser.add_argument(
        '--threshold-complexity',
        type=int,
        default=10,
        help='Complexity threshold for flagging functions (default: 10)'
    )

    parser.add_argument(
        '--threshold-duplication',
        type=int,
        default=5,
        help='Minimum occurrences to flag duplication (default: 5)'
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

    # Validate input path
    if not os.path.exists(args.input):
        print(f"Error: Input path does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Run analysis
    try:
        analyzer = CodeQualityAnalyzer(
            input_path=args.input,
            threshold_complexity=args.threshold_complexity,
            threshold_duplication=args.threshold_duplication,
            verbose=args.verbose
        )

        result = analyzer.analyze()

        # Format output
        if args.output == 'text':
            output = OutputFormatter.format_text(result, verbose=args.verbose)
        elif args.output == 'json':
            output = OutputFormatter.format_json(result)
        elif args.output == 'csv':
            output = OutputFormatter.format_csv(result)
        else:
            output = OutputFormatter.format_text(result)

        # Write output
        if args.file:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(output)
            if args.verbose:
                print(f"\nReport written to: {args.file}")
        else:
            print(output)

        # Exit with appropriate code based on quality grade
        grade_exit_codes = {'A': 0, 'B': 0, 'C': 1, 'D': 1, 'F': 2}
        sys.exit(grade_exit_codes.get(result.quality_score.grade, 0))

    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
