#!/usr/bin/env python3
"""
Test Suite Generator
Generate comprehensive test suites from source code analysis with unit tests,
integration test stubs, and edge case coverage.

Features:
- Source code analysis (function/method extraction)
- Parameter and return type inference
- Happy path test generation
- Error condition and edge case tests
- Boundary value test generation
- Framework-specific output (Jest, Vitest, Pytest, Mocha)
- Mock generation support
"""

import argparse
import ast
import csv
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Parameter:
    """Represents a function parameter"""
    name: str
    type_hint: str = 'any'
    default_value: Optional[str] = None
    is_optional: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class FunctionInfo:
    """Information about a function/method"""
    name: str
    parameters: List[Parameter] = field(default_factory=list)
    return_type: str = 'any'
    is_async: bool = False
    is_method: bool = False
    class_name: Optional[str] = None
    docstring: Optional[str] = None
    line_number: int = 0
    complexity: int = 1
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'parameters': [p.to_dict() for p in self.parameters],
            'return_type': self.return_type,
            'is_async': self.is_async,
            'is_method': self.is_method,
            'class_name': self.class_name,
            'docstring': self.docstring,
            'line_number': self.line_number,
            'complexity': self.complexity,
            'dependencies': self.dependencies,
        }


@dataclass
class TestCase:
    """Generated test case"""
    name: str
    function_name: str
    category: str  # happy_path, error, boundary, edge_case
    description: str
    setup: List[str] = field(default_factory=list)
    input_values: Dict[str, Any] = field(default_factory=dict)
    expected: str = ''
    assertions: List[str] = field(default_factory=list)
    mocks: List[str] = field(default_factory=list)
    priority: str = 'medium'  # high, medium, low

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class TestSuite:
    """Collection of tests for a file/module"""
    source_file: str
    framework: str
    functions_analyzed: int = 0
    test_cases: List[TestCase] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    setup_code: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'source_file': self.source_file,
            'framework': self.framework,
            'functions_analyzed': self.functions_analyzed,
            'test_cases': [tc.to_dict() for tc in self.test_cases],
            'imports': self.imports,
            'setup_code': self.setup_code,
        }


class SourceAnalyzer:
    """Analyze source code to extract function information"""

    # Common type patterns for inference
    TYPE_PATTERNS = {
        'id': 'string',
        'name': 'string',
        'email': 'string',
        'url': 'string',
        'path': 'string',
        'count': 'number',
        'index': 'number',
        'size': 'number',
        'length': 'number',
        'amount': 'number',
        'price': 'number',
        'total': 'number',
        'is_': 'boolean',
        'has_': 'boolean',
        'can_': 'boolean',
        'should_': 'boolean',
        'enabled': 'boolean',
        'disabled': 'boolean',
        'active': 'boolean',
        'items': 'array',
        'list': 'array',
        'data': 'object',
        'config': 'object',
        'options': 'object',
        'settings': 'object',
        'callback': 'function',
        'handler': 'function',
        'fn': 'function',
    }

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def analyze_file(self, filepath: Path) -> List[FunctionInfo]:
        """Analyze a source file and extract function information"""
        content = filepath.read_text()
        ext = filepath.suffix.lower()

        if ext == '.py':
            return self._analyze_python(content)
        elif ext in ('.ts', '.tsx', '.js', '.jsx'):
            return self._analyze_typescript(content)
        else:
            if self.verbose:
                print(f"Unsupported file type: {ext}")
            return []

    def _analyze_python(self, content: str) -> List[FunctionInfo]:
        """Analyze Python source code"""
        functions = []

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            if self.verbose:
                print(f"Python syntax error: {e}")
            return functions

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_info = self._extract_python_function(node)
                functions.append(func_info)

        return functions

    def _extract_python_function(self, node) -> FunctionInfo:
        """Extract function information from Python AST node"""
        parameters = []

        for arg in node.args.args:
            param_name = arg.arg
            type_hint = 'any'

            if arg.annotation:
                type_hint = self._get_annotation_string(arg.annotation)

            if type_hint == 'any':
                type_hint = self._infer_type_from_name(param_name)

            parameters.append(Parameter(
                name=param_name,
                type_hint=type_hint,
            ))

        # Handle defaults
        defaults = node.args.defaults
        num_defaults = len(defaults)
        num_params = len(parameters)

        for i, default in enumerate(defaults):
            param_index = num_params - num_defaults + i
            if param_index >= 0:
                parameters[param_index].is_optional = True
                parameters[param_index].default_value = self._get_default_string(default)

        # Return type
        return_type = 'any'
        if node.returns:
            return_type = self._get_annotation_string(node.returns)

        # Docstring
        docstring = ast.get_docstring(node)

        # Calculate complexity (simplified)
        complexity = self._calculate_complexity(node)

        # Extract dependencies
        dependencies = self._extract_dependencies(node)

        return FunctionInfo(
            name=node.name,
            parameters=parameters,
            return_type=return_type,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            is_method=parameters and parameters[0].name == 'self',
            docstring=docstring,
            line_number=node.lineno,
            complexity=complexity,
            dependencies=dependencies,
        )

    def _get_annotation_string(self, annotation) -> str:
        """Convert AST annotation to string"""
        if isinstance(annotation, ast.Name):
            return annotation.id.lower()
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value).lower()
        elif isinstance(annotation, ast.Subscript):
            return 'any'  # Complex type
        return 'any'

    def _get_default_string(self, default) -> str:
        """Convert AST default value to string"""
        if isinstance(default, ast.Constant):
            return repr(default.value)
        elif isinstance(default, ast.Name):
            return default.id
        elif isinstance(default, ast.List):
            return '[]'
        elif isinstance(default, ast.Dict):
            return '{}'
        return 'None'

    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity (simplified)"""
        complexity = 1

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _extract_dependencies(self, node) -> List[str]:
        """Extract function dependencies (called functions)"""
        dependencies = []

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    dependencies.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    dependencies.append(child.func.attr)

        return list(set(dependencies))

    def _analyze_typescript(self, content: str) -> List[FunctionInfo]:
        """Analyze TypeScript/JavaScript source code using regex"""
        functions = []

        # Function patterns
        patterns = [
            # Regular function
            r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)(?:\s*:\s*([^{]+))?\s*\{',
            # Arrow function with explicit type
            r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(([^)]*)\)(?:\s*:\s*([^=]+))?\s*=>',
            # Class method
            r'(?:async\s+)?(\w+)\s*\(([^)]*)\)(?:\s*:\s*([^{]+))?\s*\{',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                name = match.group(1)
                params_str = match.group(2)
                return_type = match.group(3).strip() if match.group(3) else 'any'

                # Skip constructor
                if name == 'constructor':
                    continue

                parameters = self._parse_ts_parameters(params_str)
                is_async = 'async' in content[max(0, match.start() - 20):match.start()]

                # Get line number
                line_number = content[:match.start()].count('\n') + 1

                functions.append(FunctionInfo(
                    name=name,
                    parameters=parameters,
                    return_type=return_type.lower() if return_type else 'any',
                    is_async=is_async,
                    line_number=line_number,
                ))

        return functions

    def _parse_ts_parameters(self, params_str: str) -> List[Parameter]:
        """Parse TypeScript/JavaScript parameter string"""
        parameters = []

        if not params_str.strip():
            return parameters

        # Split by comma, handling nested types
        depth = 0
        current = ''
        parts = []

        for char in params_str:
            if char in '<([':
                depth += 1
            elif char in '>)]':
                depth -= 1
            elif char == ',' and depth == 0:
                parts.append(current.strip())
                current = ''
                continue
            current += char

        if current.strip():
            parts.append(current.strip())

        for part in parts:
            # Parse name: type = default
            match = re.match(r'(\w+)(?:\s*:\s*([^=]+))?(?:\s*=\s*(.+))?', part.strip())
            if match:
                name = match.group(1)
                type_hint = match.group(2).strip() if match.group(2) else 'any'
                default = match.group(3)

                if type_hint == 'any':
                    type_hint = self._infer_type_from_name(name)

                parameters.append(Parameter(
                    name=name,
                    type_hint=type_hint.lower(),
                    default_value=default,
                    is_optional=default is not None or '?' in part,
                ))

        return parameters

    def _infer_type_from_name(self, name: str) -> str:
        """Infer type from parameter name"""
        name_lower = name.lower()

        for pattern, type_name in self.TYPE_PATTERNS.items():
            if pattern in name_lower or name_lower.startswith(pattern):
                return type_name

        return 'any'


class TestGenerator:
    """Generate test cases from function information"""

    # Boundary values by type
    BOUNDARY_VALUES = {
        'string': ['', 'a', 'test', 'a' * 1000, 'special!@#$%', '  spaces  ', None],
        'number': [0, 1, -1, 0.5, -0.5, float('inf'), None],
        'int': [0, 1, -1, 2147483647, -2147483648, None],
        'boolean': [True, False, None],
        'array': [[], [1], [1, 2, 3], None],
        'object': [{}, {'key': 'value'}, None],
        'any': [None, '', 0, [], {}],
    }

    # Error scenarios by type
    ERROR_SCENARIOS = {
        'string': [
            ('null_input', None, 'should handle null string'),
            ('undefined_input', 'undefined', 'should handle undefined'),
            ('numeric_input', 123, 'should handle numeric input'),
        ],
        'number': [
            ('nan_input', 'NaN', 'should handle NaN'),
            ('string_input', '"not a number"', 'should handle string input'),
            ('null_input', None, 'should handle null'),
        ],
        'array': [
            ('null_input', None, 'should handle null array'),
            ('non_array', '{}', 'should handle non-array input'),
        ],
    }

    def __init__(self, framework: str = 'jest', with_mocks: bool = False, verbose: bool = False):
        self.framework = framework
        self.with_mocks = with_mocks
        self.verbose = verbose

    def generate_tests(self, functions: List[FunctionInfo], source_file: str) -> TestSuite:
        """Generate test suite for a list of functions"""
        suite = TestSuite(
            source_file=source_file,
            framework=self.framework,
            functions_analyzed=len(functions),
        )

        # Generate imports based on framework
        suite.imports = self._generate_imports(source_file)

        for func in functions:
            # Skip private functions and special methods
            if func.name.startswith('_') and not func.name.startswith('__'):
                continue

            # Generate test cases
            test_cases = self._generate_function_tests(func)
            suite.test_cases.extend(test_cases)

        return suite

    def _generate_imports(self, source_file: str) -> List[str]:
        """Generate import statements for test file"""
        module_name = Path(source_file).stem

        if self.framework == 'jest':
            return [
                f"import {{ /* functions */ }} from './{module_name}';",
            ]
        elif self.framework == 'vitest':
            return [
                "import { describe, it, expect, vi } from 'vitest';",
                f"import {{ /* functions */ }} from './{module_name}';",
            ]
        elif self.framework == 'pytest':
            return [
                "import pytest",
                f"from {module_name} import *",
            ]
        elif self.framework == 'mocha':
            return [
                "const { expect } = require('chai');",
                f"const {{ /* functions */ }} = require('./{module_name}');",
            ]

        return []

    def _generate_function_tests(self, func: FunctionInfo) -> List[TestCase]:
        """Generate test cases for a single function"""
        test_cases = []

        # 1. Happy path test
        test_cases.append(self._generate_happy_path_test(func))

        # 2. Error handling tests
        test_cases.extend(self._generate_error_tests(func))

        # 3. Boundary value tests
        test_cases.extend(self._generate_boundary_tests(func))

        # 4. Edge case tests
        test_cases.extend(self._generate_edge_case_tests(func))

        return test_cases

    def _generate_happy_path_test(self, func: FunctionInfo) -> TestCase:
        """Generate happy path test"""
        input_values = {}
        for param in func.parameters:
            if param.name == 'self':
                continue
            input_values[param.name] = self._get_valid_value(param.type_hint)

        return TestCase(
            name=f"should return expected result for valid input",
            function_name=func.name,
            category='happy_path',
            description=f"Test {func.name} with valid inputs",
            input_values=input_values,
            expected=f"expected {func.return_type} result",
            assertions=[
                self._generate_assertion(func.return_type, 'toBeDefined'),
            ],
            priority='high',
        )

    def _generate_error_tests(self, func: FunctionInfo) -> List[TestCase]:
        """Generate error handling tests"""
        test_cases = []

        for param in func.parameters:
            if param.name == 'self':
                continue

            # Test null/undefined handling
            test_cases.append(TestCase(
                name=f"should handle null {param.name}",
                function_name=func.name,
                category='error',
                description=f"Test {func.name} with null {param.name}",
                input_values={**{p.name: self._get_valid_value(p.type_hint)
                               for p in func.parameters if p.name != 'self'},
                             param.name: None},
                expected='error or default behavior',
                assertions=[
                    self._generate_assertion('error', 'toThrow'),
                ],
                priority='high',
            ))

            # Test invalid type handling
            invalid_value = self._get_invalid_value(param.type_hint)
            if invalid_value is not None:
                test_cases.append(TestCase(
                    name=f"should handle invalid type for {param.name}",
                    function_name=func.name,
                    category='error',
                    description=f"Test {func.name} with invalid type for {param.name}",
                    input_values={**{p.name: self._get_valid_value(p.type_hint)
                                   for p in func.parameters if p.name != 'self'},
                                 param.name: invalid_value},
                    expected='error or type coercion',
                    assertions=[
                        self._generate_assertion('error', 'toThrow'),
                    ],
                    priority='medium',
                ))

        return test_cases

    def _generate_boundary_tests(self, func: FunctionInfo) -> List[TestCase]:
        """Generate boundary value tests"""
        test_cases = []

        for param in func.parameters:
            if param.name == 'self':
                continue

            type_hint = param.type_hint.lower()
            boundaries = self._get_boundary_values(type_hint)

            for boundary_name, boundary_value in boundaries:
                other_values = {p.name: self._get_valid_value(p.type_hint)
                              for p in func.parameters if p.name not in ('self', param.name)}

                test_cases.append(TestCase(
                    name=f"should handle {boundary_name} for {param.name}",
                    function_name=func.name,
                    category='boundary',
                    description=f"Test {func.name} with {boundary_name} value for {param.name}",
                    input_values={**other_values, param.name: boundary_value},
                    expected='valid result or handled error',
                    assertions=[
                        self._generate_assertion(func.return_type, 'toBeDefined'),
                    ],
                    priority='medium',
                ))

        return test_cases[:5]  # Limit boundary tests

    def _generate_edge_case_tests(self, func: FunctionInfo) -> List[TestCase]:
        """Generate edge case tests"""
        test_cases = []

        # Test with all optional parameters missing
        required_params = [p for p in func.parameters if not p.is_optional and p.name != 'self']
        optional_params = [p for p in func.parameters if p.is_optional]

        if optional_params:
            test_cases.append(TestCase(
                name="should work with only required parameters",
                function_name=func.name,
                category='edge_case',
                description=f"Test {func.name} with only required parameters",
                input_values={p.name: self._get_valid_value(p.type_hint) for p in required_params},
                expected='valid result',
                assertions=[
                    self._generate_assertion(func.return_type, 'toBeDefined'),
                ],
                priority='medium',
            ))

        # Test async behavior
        if func.is_async:
            test_cases.append(TestCase(
                name="should resolve async operation",
                function_name=func.name,
                category='edge_case',
                description=f"Test {func.name} async resolution",
                input_values={p.name: self._get_valid_value(p.type_hint)
                             for p in func.parameters if p.name != 'self'},
                expected='resolved promise',
                assertions=[
                    'await expect(result).resolves.toBeDefined()',
                ],
                priority='high',
            ))

            test_cases.append(TestCase(
                name="should handle async rejection",
                function_name=func.name,
                category='edge_case',
                description=f"Test {func.name} async rejection handling",
                input_values={},
                expected='rejected promise with error',
                assertions=[
                    'await expect(result).rejects.toThrow()',
                ],
                priority='medium',
            ))

        # High complexity functions need more tests
        if func.complexity > 5:
            test_cases.append(TestCase(
                name="should handle complex branching",
                function_name=func.name,
                category='edge_case',
                description=f"Test {func.name} complex code paths (complexity: {func.complexity})",
                input_values={p.name: self._get_valid_value(p.type_hint)
                             for p in func.parameters if p.name != 'self'},
                expected='test all branches',
                assertions=[
                    '// TODO: Add assertions for each code branch',
                ],
                priority='high',
            ))

        return test_cases

    def _get_valid_value(self, type_hint: str) -> Any:
        """Get a valid value for a type"""
        type_lower = type_hint.lower()

        if 'string' in type_lower or type_lower == 'str':
            return 'test_value'
        elif 'number' in type_lower or 'int' in type_lower or 'float' in type_lower:
            return 42
        elif 'bool' in type_lower:
            return True
        elif 'array' in type_lower or 'list' in type_lower:
            return [1, 2, 3]
        elif 'object' in type_lower or 'dict' in type_lower:
            return {'key': 'value'}

        return 'test_input'

    def _get_invalid_value(self, type_hint: str) -> Any:
        """Get an invalid value for a type"""
        type_lower = type_hint.lower()

        if 'string' in type_lower or type_lower == 'str':
            return 123  # number instead of string
        elif 'number' in type_lower or 'int' in type_lower:
            return 'not_a_number'
        elif 'bool' in type_lower:
            return 'not_a_boolean'
        elif 'array' in type_lower or 'list' in type_lower:
            return {}  # object instead of array

        return None

    def _get_boundary_values(self, type_hint: str) -> List[Tuple[str, Any]]:
        """Get boundary values for testing"""
        boundaries = []

        if 'string' in type_hint or type_hint == 'str':
            boundaries = [
                ('empty_string', ''),
                ('single_char', 'a'),
                ('long_string', 'a' * 1000),
                ('special_chars', '!@#$%^&*()'),
                ('whitespace', '   '),
            ]
        elif 'number' in type_hint or 'int' in type_hint:
            boundaries = [
                ('zero', 0),
                ('positive_one', 1),
                ('negative_one', -1),
                ('max_safe_int', 9007199254740991),
                ('min_safe_int', -9007199254740991),
            ]
        elif 'array' in type_hint or 'list' in type_hint:
            boundaries = [
                ('empty_array', []),
                ('single_item', [1]),
                ('many_items', list(range(100))),
            ]

        return boundaries

    def _generate_assertion(self, return_type: str, assertion_type: str) -> str:
        """Generate assertion based on type and framework"""
        if self.framework == 'pytest':
            if assertion_type == 'toBeDefined':
                return 'assert result is not None'
            elif assertion_type == 'toThrow':
                return 'pytest.raises(Exception)'
            return f'assert result'
        else:
            # Jest/Vitest/Mocha style
            return f'expect(result).{assertion_type}()'


class TestSuiteGenerator:
    """Main class for test suite generation"""

    def __init__(self, target_path: str, verbose: bool = False,
                 framework: str = 'jest', recursive: bool = False,
                 with_mocks: bool = False, output_dir: Optional[str] = None):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("TestSuiteGenerator initialized")

        self.target_path = Path(target_path)
        self.verbose = verbose
        self.framework = framework
        self.recursive = recursive
        self.with_mocks = with_mocks
        self.output_dir = Path(output_dir) if output_dir else None

        self.analyzer = SourceAnalyzer(verbose=verbose)
        self.generator = TestGenerator(framework=framework, with_mocks=with_mocks, verbose=verbose)

        self.results = {
            'status': 'success',
            'target': str(target_path),
            'framework': framework,
            'files_analyzed': 0,
            'functions_found': 0,
            'tests_generated': 0,
            'test_suites': [],
            'generated_files': [],
            'recommendations': [],
        }

    def run(self) -> Dict:
        """Execute test suite generation"""
        logger.debug("Starting test suite generation run")
        print(f"Running TestSuiteGenerator...")
        print(f"Target: {self.target_path}")
        print(f"Framework: {self.framework}")

        try:
            # Find source files
            source_files = self._find_source_files()
            if not source_files:
                logger.warning(f"No source files found in {self.target_path}")
                raise ValueError(f"No source files found in {self.target_path}")

            print(f"Found {len(source_files)} source files")

            # Process each file
            for filepath in source_files:
                self._process_file(filepath)

            self._generate_recommendations()
            self._generate_report()

            print("Completed successfully!")
            return self.results

        except Exception as e:
            logger.error(f"Error during test suite generation: {e}")
            print(f"Error: {e}")
            self.results['status'] = 'error'
            self.results['error'] = str(e)
            if self.verbose:
                import traceback
                traceback.print_exc()
            return self.results

    def _find_source_files(self) -> List[Path]:
        """Find source files to analyze"""
        extensions = {'.py', '.ts', '.tsx', '.js', '.jsx'}
        exclude_patterns = {'test', 'spec', '__pycache__', 'node_modules', 'dist', 'build', '.d.ts'}

        files = []

        if self.target_path.is_file():
            if self.target_path.suffix in extensions:
                files.append(self.target_path)
        else:
            pattern = '**/*' if self.recursive else '*'
            for ext in extensions:
                for filepath in self.target_path.glob(f'{pattern}{ext}'):
                    # Skip test files and excluded patterns
                    if any(p in str(filepath).lower() for p in exclude_patterns):
                        continue
                    files.append(filepath)

        return files

    def _process_file(self, filepath: Path):
        """Process a single source file"""
        if self.verbose:
            print(f"Analyzing: {filepath}")

        # Analyze source
        functions = self.analyzer.analyze_file(filepath)
        if not functions:
            if self.verbose:
                print(f"  No functions found")
            return

        self.results['files_analyzed'] += 1
        self.results['functions_found'] += len(functions)

        if self.verbose:
            print(f"  Found {len(functions)} functions")

        # Generate tests
        suite = self.generator.generate_tests(functions, str(filepath))
        self.results['tests_generated'] += len(suite.test_cases)
        self.results['test_suites'].append(suite.to_dict())

        # Write test file if output directory specified
        if self.output_dir:
            self._write_test_file(suite, filepath)

    def _write_test_file(self, suite: TestSuite, source_path: Path):
        """Write generated tests to file"""
        # Determine test file path
        rel_path = source_path.relative_to(self.target_path) if self.target_path.is_dir() else source_path.name
        test_filename = self._get_test_filename(rel_path)
        test_path = self.output_dir / test_filename

        # Create directory if needed
        test_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate test file content
        content = self._generate_test_file_content(suite)

        test_path.write_text(content)
        self.results['generated_files'].append(str(test_path))

        if self.verbose:
            print(f"  Generated: {test_path}")

    def _get_test_filename(self, source_path: Path) -> str:
        """Generate test file name based on framework"""
        stem = source_path.stem
        suffix = source_path.suffix

        if self.framework in ('jest', 'vitest'):
            return f"{stem}.test{suffix}"
        elif self.framework == 'mocha':
            return f"{stem}.spec{suffix}"
        elif self.framework == 'pytest':
            return f"test_{stem}.py"

        return f"{stem}.test{suffix}"

    def _generate_test_file_content(self, suite: TestSuite) -> str:
        """Generate test file content"""
        lines = []

        # Imports
        for imp in suite.imports:
            lines.append(imp)
        lines.append('')

        # Group tests by function
        tests_by_function: Dict[str, List[TestCase]] = {}
        for tc in suite.test_cases:
            if tc.function_name not in tests_by_function:
                tests_by_function[tc.function_name] = []
            tests_by_function[tc.function_name].append(tc)

        # Generate test blocks
        if self.framework == 'pytest':
            lines.extend(self._generate_pytest_content(tests_by_function))
        else:
            lines.extend(self._generate_jest_content(tests_by_function))

        return '\n'.join(lines)

    def _generate_jest_content(self, tests_by_function: Dict[str, List[TestCase]]) -> List[str]:
        """Generate Jest/Vitest/Mocha style test content"""
        lines = []

        for func_name, test_cases in tests_by_function.items():
            lines.append(f"describe('{func_name}', () => {{")

            for tc in test_cases:
                lines.append(f"  it('{tc.name}', {'async ' if 'await' in str(tc.assertions) else ''}() => {{")
                lines.append(f"    // {tc.description}")
                lines.append(f"    // Category: {tc.category}")
                lines.append('')

                # Arrange
                lines.append('    // Arrange')
                if tc.input_values:
                    for param, value in tc.input_values.items():
                        lines.append(f"    const {param} = {json.dumps(value)};")
                lines.append('')

                # Act
                lines.append('    // Act')
                params_str = ', '.join(tc.input_values.keys()) if tc.input_values else ''
                if tc.category == 'error':
                    lines.append(f"    const action = () => {func_name}({params_str});")
                else:
                    lines.append(f"    const result = {func_name}({params_str});")
                lines.append('')

                # Assert
                lines.append('    // Assert')
                for assertion in tc.assertions:
                    lines.append(f"    {assertion};")

                lines.append('  });')
                lines.append('')

            lines.append('});')
            lines.append('')

        return lines

    def _generate_pytest_content(self, tests_by_function: Dict[str, List[TestCase]]) -> List[str]:
        """Generate Pytest style test content"""
        lines = []

        for func_name, test_cases in tests_by_function.items():
            lines.append(f"class Test{func_name.title().replace('_', '')}:")

            for tc in test_cases:
                test_name = tc.name.lower().replace(' ', '_').replace("'", '')
                lines.append(f"    def test_{test_name}(self):")
                lines.append(f"        '''")
                lines.append(f"        {tc.description}")
                lines.append(f"        Category: {tc.category}")
                lines.append(f"        '''")

                # Arrange
                lines.append('        # Arrange')
                if tc.input_values:
                    for param, value in tc.input_values.items():
                        lines.append(f"        {param} = {repr(value)}")
                lines.append('')

                # Act
                lines.append('        # Act')
                if tc.category == 'error':
                    lines.append(f"        with pytest.raises(Exception):")
                    params_str = ', '.join(tc.input_values.keys()) if tc.input_values else ''
                    lines.append(f"            {func_name}({params_str})")
                else:
                    params_str = ', '.join(tc.input_values.keys()) if tc.input_values else ''
                    lines.append(f"        result = {func_name}({params_str})")
                    lines.append('')

                    # Assert
                    lines.append('        # Assert')
                    for assertion in tc.assertions:
                        lines.append(f"        {assertion}")

                lines.append('')

            lines.append('')

        return lines

    def _generate_recommendations(self):
        """Generate recommendations for test coverage"""
        recommendations = []

        # Check if any files were analyzed
        if self.results['files_analyzed'] == 0:
            recommendations.append({
                'type': 'warning',
                'message': 'No source files were analyzed - check file paths and extensions',
            })

        # Check functions per file ratio
        if self.results['files_analyzed'] > 0:
            ratio = self.results['functions_found'] / self.results['files_analyzed']
            if ratio < 2:
                recommendations.append({
                    'type': 'info',
                    'message': 'Low function count per file - consider checking file patterns',
                })

        # Test coverage recommendations
        if self.results['tests_generated'] > 0:
            tests_per_function = self.results['tests_generated'] / max(1, self.results['functions_found'])
            recommendations.append({
                'type': 'info',
                'message': f'Generated ~{tests_per_function:.1f} tests per function',
            })

        # Framework-specific recommendations
        if self.framework == 'jest':
            recommendations.append({
                'type': 'tip',
                'message': 'Run tests with: npm test or jest --coverage',
            })
        elif self.framework == 'pytest':
            recommendations.append({
                'type': 'tip',
                'message': 'Run tests with: pytest -v --cov=.',
            })
        elif self.framework == 'vitest':
            recommendations.append({
                'type': 'tip',
                'message': 'Run tests with: npx vitest run --coverage',
            })

        self.results['recommendations'] = recommendations

    def _generate_report(self):
        """Generate and display the report"""
        print("\n" + "=" * 60)
        print("TEST SUITE GENERATOR REPORT")
        print("=" * 60)

        print(f"\nFramework: {self.framework}")
        print(f"Files analyzed: {self.results['files_analyzed']}")
        print(f"Functions found: {self.results['functions_found']}")
        print(f"Tests generated: {self.results['tests_generated']}")

        if self.results['generated_files']:
            print(f"\nGenerated Files ({len(self.results['generated_files'])}):")
            for filepath in self.results['generated_files'][:10]:
                print(f"   {filepath}")
            if len(self.results['generated_files']) > 10:
                print(f"   ... and {len(self.results['generated_files']) - 10} more")

        # Test categories breakdown
        categories = {}
        for suite in self.results['test_suites']:
            for tc in suite.get('test_cases', []):
                cat = tc.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1

        if categories:
            print(f"\nTest Categories:")
            for cat, count in sorted(categories.items()):
                print(f"   {cat}: {count}")

        # Recommendations
        if self.results['recommendations']:
            print(f"\nRecommendations:")
            for rec in self.results['recommendations']:
                print(f"   [{rec['type'].upper()}] {rec['message']}")

        print("\n" + "=" * 60)


def format_csv_output(results: Dict) -> str:
    """Format results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['function_name', 'test_name', 'category', 'priority'])

    for suite in results.get('test_suites', []):
        for tc in suite.get('test_cases', []):
            writer.writerow([
                tc.get('function_name', ''),
                tc.get('name', ''),
                tc.get('category', ''),
                tc.get('priority', ''),
            ])

    return output.getvalue()


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="TestSuiteGenerator - Generate comprehensive test suites from source code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input src/auth.ts --framework jest
  %(prog)s --input src/ --framework pytest --recursive
  %(prog)s --input . --framework vitest --output tests/
  %(prog)s --input lib/ --framework jest --with-mocks -v

Supported Frameworks:
  jest    - Jest (JavaScript/TypeScript)
  vitest  - Vitest (JavaScript/TypeScript)
  pytest  - Pytest (Python)
  mocha   - Mocha (JavaScript/TypeScript)

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Source file or directory to analyze'
    )

    parser.add_argument(
        '--framework', '-F',
        choices=['jest', 'vitest', 'pytest', 'mocha'],
        default='jest',
        help='Test framework to generate tests for (default: jest)'
    )

    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Recursively analyze subdirectories'
    )

    parser.add_argument(
        '--with-mocks',
        action='store_true',
        help='Generate mock setup for dependencies'
    )

    parser.add_argument(
        '--output', '-O',
        dest='output_dir',
        help='Output directory for generated test files'
    )

    parser.add_argument(
        '--format', '-o',
        choices=['text', 'json', 'csv'],
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

    generator = TestSuiteGenerator(
        args.target,
        verbose=args.verbose,
        framework=args.framework,
        recursive=args.recursive,
        with_mocks=args.with_mocks,
        output_dir=args.output_dir,
    )

    results = generator.run()

    # Format output
    if args.format == 'csv':
        output = format_csv_output(results)
    elif args.format == 'json':
        output = json.dumps(results, indent=2, default=str)
    else:
        output = json.dumps(results, indent=2, default=str)

    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Results written to {args.file}")
    elif args.format != 'text':
        print(output)

    # Exit code
    sys.exit(0 if results.get('status') == 'success' else 1)


if __name__ == '__main__':
    main()
