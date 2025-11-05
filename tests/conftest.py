"""
Pytest configuration and fixtures for Claude Skills test suite

Provides:
- Script discovery fixtures
- Sample data paths
- Common test utilities
- Parametrization for all scripts
"""

import pytest
import subprocess
import json
import tempfile
from pathlib import Path
from typing import List, Generator


def discover_scripts(domain_dirs: List[str] = None) -> List[Path]:
    """
    Discover all Python CLI scripts in skills directories.

    Args:
        domain_dirs: Optional list of domain directories to search.
                     If None, searches all standard domains.

    Returns:
        List of Path objects pointing to Python scripts
    """
    base_path = Path(__file__).parent.parent

    if domain_dirs is None:
        domain_dirs = [
            'marketing-skill',
            'product-team',
            'engineering-team',
            'c-level-advisor',
            'ra-qm-team'
        ]

    scripts = []
    for domain in domain_dirs:
        domain_path = base_path / domain
        if domain_path.exists():
            # Find all .py files in scripts/ directories
            for script in domain_path.glob('**/scripts/*.py'):
                # Skip __init__.py and example.py (templates)
                if script.name not in ('__init__.py', 'example.py'):
                    scripts.append(script)

    return sorted(scripts)


@pytest.fixture(scope='session')
def base_path() -> Path:
    """Return the base path of the claude-skills repository"""
    return Path(__file__).parent.parent


@pytest.fixture(scope='session')
def all_scripts() -> List[Path]:
    """Return all discovered Python CLI scripts"""
    return discover_scripts()


@pytest.fixture(scope='session')
def sample_data_dir(base_path: Path) -> Path:
    """Return path to sample data directory, creating if needed"""
    sample_dir = base_path / 'tests' / 'sample_data'
    sample_dir.mkdir(exist_ok=True)
    return sample_dir


@pytest.fixture(scope='session', autouse=True)
def setup_sample_data(sample_data_dir: Path) -> None:
    """Create sample data files for testing"""

    # Create sample text file
    text_file = sample_data_dir / 'sample.txt'
    if not text_file.exists():
        text_file.write_text(
            "This is sample content for testing. "
            "It contains multiple sentences. "
            "The brand voice is professional yet friendly. "
            "We believe in clear communication. "
            "This text demonstrates readability analysis. "
            "The content structure is important. "
            "Sentence variety matters for engagement."
        )

    # Create sample CSV file
    csv_file = sample_data_dir / 'sample.csv'
    if not csv_file.exists():
        csv_file.write_text(
            "category,value,description\n"
            "test1,100,First test value\n"
            "test2,200,Second test value\n"
            "test3,150,Third test value\n"
        )

    # Create sample JSON file
    json_file = sample_data_dir / 'sample.json'
    if not json_file.exists():
        json_file.write_text(json.dumps({
            'data': [
                {'id': 1, 'value': 'test1'},
                {'id': 2, 'value': 'test2'}
            ]
        }, indent=2))

    # Create sample markdown file
    md_file = sample_data_dir / 'sample.md'
    if not md_file.exists():
        md_file.write_text("""# Sample Article

## Introduction

This is a sample article for testing SEO optimization.

## Main Content

The main content goes here with multiple paragraphs. This is the second paragraph. It contains important information about the topic.

## Conclusion

The conclusion summarizes the key points discussed in the article.
""")


@pytest.fixture
def temp_output_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test output files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def run_script(script_path: Path, *args, **kwargs) -> subprocess.CompletedProcess:
    """
    Run a Python script as a CLI tool.

    Args:
        script_path: Path to the Python script
        *args: Positional arguments to pass to the script
        **kwargs: Additional keyword arguments for subprocess.run()
                  Common: timeout, env, cwd

    Returns:
        CompletedProcess object with returncode, stdout, stderr
    """
    cmd = ['python3', str(script_path)] + list(args)

    # Set defaults for subprocess
    defaults = {
        'capture_output': True,
        'text': True,
        'timeout': 30
    }
    defaults.update(kwargs)

    return subprocess.run(cmd, **defaults)


@pytest.fixture
def run_script_fixture(request):
    """Fixture to run scripts with cleanup"""
    def _run(script_path: Path, *args, **kwargs):
        return run_script(script_path, *args, **kwargs)
    return _run


# Parametrization helpers
def pytest_generate_tests(metafunc):
    """
    Pytest hook to parametrize tests with all discovered scripts.

    Tests can use the 'script_path' parameter to automatically
    receive all scripts one at a time.
    """
    if 'script_path' in metafunc.fixturenames:
        scripts = discover_scripts()
        script_ids = [s.parent.parent.name + '/' + s.parent.parent.parent.name + '/' + s.name
                      for s in scripts]
        metafunc.parametrize('script_path', scripts, ids=script_ids)

    if 'script_with_text' in metafunc.fixturenames:
        scripts = discover_scripts()
        script_ids = [s.stem for s in scripts]
        metafunc.parametrize('script_with_text',
                            [(s, 'tests/sample_data/sample.txt') for s in scripts],
                            ids=script_ids)

    if 'script_with_json' in metafunc.fixturenames:
        scripts = discover_scripts()
        script_ids = [s.stem for s in scripts]
        metafunc.parametrize('script_with_json',
                            [(s, 'tests/sample_data/sample.json') for s in scripts],
                            ids=script_ids)


# Test utilities
class CLITestHelper:
    """Helper class for common CLI testing operations"""

    @staticmethod
    def assert_help_output(result: subprocess.CompletedProcess, script_name: str) -> None:
        """Assert that --help output is valid and informative"""
        assert result.returncode == 0, f"Help failed for {script_name}: {result.stderr}"
        output = result.stdout.lower()
        assert 'usage:' in output, f"No usage found in help for {script_name}"
        assert script_name.lower() in output or 'positional' in output, \
            f"Help output doesn't mention script purpose for {script_name}"

    @staticmethod
    def assert_json_output(result: subprocess.CompletedProcess) -> dict:
        """Assert that output is valid JSON and return parsed data"""
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        try:
            data = json.loads(result.stdout)
            return data
        except json.JSONDecodeError as e:
            pytest.fail(f"Output is not valid JSON: {e}\nGot: {result.stdout[:200]}")

    @staticmethod
    def assert_text_output(result: subprocess.CompletedProcess) -> str:
        """Assert that output is non-empty text"""
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert len(result.stdout.strip()) > 0, "Output is empty"
        return result.stdout

    @staticmethod
    def assert_csv_output(result: subprocess.CompletedProcess) -> List[str]:
        """Assert that output is valid CSV format"""
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        lines = result.stdout.strip().split('\n')
        assert len(lines) > 0, "CSV output is empty"

        # Check header
        header = lines[0].split(',')
        assert len(header) > 0, "CSV header is empty"

        # Check data rows have consistent column count
        for i, line in enumerate(lines[1:], 1):
            cols = line.split(',')
            assert len(cols) == len(header), \
                f"Row {i} has {len(cols)} columns, expected {len(header)}"

        return lines


@pytest.fixture
def cli_helper():
    """Fixture providing CLI testing utilities"""
    return CLITestHelper()
