#!/usr/bin/env python3
"""
Test All Python Tools - CLI Compliance Testing

Tests that all Python scripts in the skills/ directory respond correctly
to the --help flag, ensuring CLI compliance across all automation tools.

Usage:
    python3 scripts/test_all_python_tools.py              # Test all tools
    python3 scripts/test_all_python_tools.py --sample 10  # Random sample
    python3 scripts/test_all_python_tools.py --json       # JSON output
    python3 scripts/test_all_python_tools.py --verbose    # Detailed output

Exit Codes:
    0 - All tools passed
    1 - Some tools failed
    2 - No tools found
"""

import argparse
import json
import os
import random
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def find_python_tools(base_path: str = "skills") -> List[Path]:
    """Find all Python scripts in the skills directory."""
    tools = []
    base = Path(base_path)

    if not base.exists():
        return tools

    for py_file in base.rglob("*.py"):
        # Skip __pycache__ and test files
        if "__pycache__" in str(py_file) or py_file.name.startswith("test_"):
            continue

        # Check if it's a CLI tool (has shebang or argparse)
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read(2000)  # Read first 2000 chars
                if 'argparse' in content or '#!/usr/bin/env python' in content or '#!/usr/bin/python' in content:
                    tools.append(py_file)
        except (IOError, UnicodeDecodeError):
            continue

    return sorted(tools)


def test_tool_help(tool_path: Path, timeout: int = 10) -> Tuple[bool, str]:
    """Test if a Python tool responds correctly to --help."""
    try:
        result = subprocess.run(
            [sys.executable, str(tool_path), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:
            # Check if output looks like help text
            output = result.stdout.lower()
            if 'usage' in output or 'help' in output or 'option' in output:
                return True, "OK"
            else:
                return True, "OK (minimal output)"
        else:
            error = result.stderr[:200] if result.stderr else "No error message"
            return False, f"Exit code {result.returncode}: {error}"

    except subprocess.TimeoutExpired:
        return False, "Timeout (>10s)"
    except Exception as e:
        return False, str(e)[:100]


def run_tests(tools: List[Path], verbose: bool = False) -> Dict:
    """Run --help tests on all tools."""
    results = {
        "total": len(tools),
        "passed": 0,
        "failed": 0,
        "tools": []
    }

    for i, tool in enumerate(tools, 1):
        relative_path = str(tool)
        passed, message = test_tool_help(tool)

        tool_result = {
            "path": relative_path,
            "passed": passed,
            "message": message
        }
        results["tools"].append(tool_result)

        if passed:
            results["passed"] += 1
            if verbose:
                print(f"✓ [{i}/{len(tools)}] {relative_path}")
        else:
            results["failed"] += 1
            if verbose:
                print(f"✗ [{i}/{len(tools)}] {relative_path}")
                print(f"  Error: {message}")

    return results


def print_summary(results: Dict, verbose: bool = False):
    """Print human-readable summary."""
    print("\n" + "=" * 60)
    print("Python Tools --help Test Results")
    print("=" * 60)
    print(f"Total tools:  {results['total']}")
    print(f"Passed:       {results['passed']}")
    print(f"Failed:       {results['failed']}")

    if results['total'] > 0:
        pass_rate = (results['passed'] / results['total']) * 100
        print(f"Pass rate:    {pass_rate:.1f}%")

    if results['failed'] > 0:
        print("\nFailed tools:")
        for tool in results['tools']:
            if not tool['passed']:
                print(f"  ✗ {tool['path']}")
                print(f"    {tool['message']}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Test all Python tools for CLI compliance (--help support)"
    )
    parser.add_argument(
        "--sample", "-s",
        type=int,
        metavar="N",
        help="Test random sample of N tools instead of all"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed progress"
    )
    parser.add_argument(
        "--path", "-p",
        default="skills",
        help="Base path to search for Python tools (default: skills)"
    )

    args = parser.parse_args()

    # Find all tools
    tools = find_python_tools(args.path)

    if not tools:
        print("No Python tools found!", file=sys.stderr)
        sys.exit(2)

    if args.verbose:
        print(f"Found {len(tools)} Python tools")

    # Sample if requested
    if args.sample and args.sample < len(tools):
        tools = random.sample(tools, args.sample)
        if args.verbose:
            print(f"Testing random sample of {len(tools)} tools")

    # Run tests
    results = run_tests(tools, verbose=args.verbose)

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_summary(results, verbose=args.verbose)

    # Exit with appropriate code
    if results['failed'] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
