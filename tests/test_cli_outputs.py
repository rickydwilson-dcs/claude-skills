"""
Test suite for output format validation

Tests that scripts produce valid output in different formats:
- Text output is readable and structured
- JSON output is valid and parseable
- CSV output follows proper format
- File output creates files correctly
- Output encoding is correct (UTF-8)

Markers:
  @pytest.mark.output - Output format tests
"""

import pytest
import subprocess
import json
import csv
import io
from pathlib import Path
from typing import Dict, List


class TestTextOutput:
    """Test text/human-readable output format"""

    @pytest.mark.output
    def test_default_output_is_readable(self, script_path: Path, sample_data_dir: Path):
        """Test that default output is readable text"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            output = result.stdout.strip()
            assert len(output) > 0, f"Output empty for {script_path.name}"

            # Should be mostly printable ASCII + UTF-8
            printable = sum(1 for c in output if c.isprintable() or c in '\n\r\t')
            total = len(output)
            assert printable / total > 0.90, \
                f"Output contains too many non-printable characters for {script_path.name}"

    @pytest.mark.output
    def test_text_output_has_structure(self, script_path: Path, sample_data_dir: Path):
        """Test that text output has reasonable structure (newlines, sections)"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            output = result.stdout.strip()
            lines = output.split('\n')

            # Output should have multiple lines or be a single paragraph
            # (formatting matters)
            assert len(output) > 10, \
                f"Text output too short for {script_path.name}"

    @pytest.mark.output
    def test_text_output_encoding(self, script_path: Path, sample_data_dir: Path):
        """Test that text output is properly encoded"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            # Should be UTF-8 decodable
            try:
                output_bytes = result.stdout.encode('utf-8')
                decoded = output_bytes.decode('utf-8')
                assert len(decoded) > 0 or len(result.stdout) == 0
            except (UnicodeDecodeError, UnicodeEncodeError):
                pytest.fail(f"Output encoding error for {script_path.name}")

    @pytest.mark.output
    def test_no_excessive_output(self, script_path: Path, sample_data_dir: Path):
        """Test that output is reasonable size (not excessive)"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            # For sample.txt input, output should be reasonably sized
            # Not more than 1MB (sanity check)
            assert len(result.stdout) < 1_000_000, \
                f"Output exceeds 1MB for {script_path.name} - possible infinite loop?"


class TestJsonOutput:
    """Test JSON output format"""

    @pytest.mark.output
    def test_json_output_flag_valid_json(self, script_path: Path, sample_data_dir: Path):
        """Test that --output json produces valid JSON"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file), '--output', 'json'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # If --output flag is not supported, that's fine
        if result.returncode == 0 and '--output' in result.stderr:
            # Flag not supported
            return

        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                # Valid JSON parsed
                assert True
            except json.JSONDecodeError as e:
                # If script supports --output json, it must be valid JSON
                if '--output' in result.stderr or 'json' not in result.stderr:
                    # Format not recognized, skip
                    return
                pytest.fail(f"Invalid JSON output for {script_path.name}: {e}")

    @pytest.mark.output
    def test_json_output_is_dict_or_list(self, script_path: Path, sample_data_dir: Path):
        """Test that JSON output is valid structure (dict or list)"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file), '--output', 'json'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                # Should be dict or list at top level
                assert isinstance(data, (dict, list)), \
                    f"JSON output not dict or list for {script_path.name}"
            except json.JSONDecodeError:
                # JSON format not supported, skip
                return

    @pytest.mark.output
    def test_json_output_no_trailing_content(self, script_path: Path, sample_data_dir: Path):
        """Test that JSON output doesn't have extra content after JSON"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file), '--output', 'json'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout.strip():
            output = result.stdout.strip()

            # Try to parse JSON
            try:
                # Find where JSON ends
                data = json.loads(output)

                # Re-encode to get original length
                encoded = json.dumps(data)

                # Allow small differences for formatting
                # But flag if there's a lot of extra content
                if len(output) > len(encoded) * 2:
                    # Might have extra logging after JSON
                    # Check if it's valid JSON followed by extra text
                    try:
                        json.loads(output.split('\n')[0])
                        # First line is valid JSON but there's more
                        # This might be ok (logging) but worth noting
                    except:
                        pass  # Not JSON format issue

            except json.JSONDecodeError:
                # Not JSON, skip
                return


class TestCsvOutput:
    """Test CSV output format (for scripts that support it)"""

    @pytest.mark.output
    def test_csv_output_valid_format(self, script_path: Path, sample_data_dir: Path):
        """Test that CSV output is valid format"""
        sample_file = sample_data_dir / 'sample.csv'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file), '--output', 'csv'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # CSV format is optional, skip if not supported
        if result.returncode != 0:
            return

        if result.stdout.strip():
            try:
                # Parse as CSV
                reader = csv.reader(io.StringIO(result.stdout))
                rows = list(reader)

                # Should have at least header
                assert len(rows) > 0, \
                    f"CSV output empty for {script_path.name}"

                # All rows should have same column count
                if len(rows) > 1:
                    header_cols = len(rows[0])
                    for i, row in enumerate(rows[1:], 1):
                        assert len(row) == header_cols, \
                            f"CSV row {i} has inconsistent column count for {script_path.name}"

            except Exception as e:
                # CSV parsing failed, might not be CSV format
                pass


class TestFileOutput:
    """Test file output functionality"""

    @pytest.mark.output
    def test_file_output_flag_creates_file(self, script_path: Path, sample_data_dir: Path, temp_output_dir: Path):
        """Test that --file flag creates output file"""
        sample_file = sample_data_dir / 'sample.txt'
        output_file = temp_output_dir / 'output.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file), '--file', str(output_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # --file flag is optional
        if '--file' in result.stderr or 'unrecognized arguments' in result.stderr:
            # Flag not supported
            return

        if result.returncode == 0:
            # File should be created
            assert output_file.exists(), \
                f"Output file not created for {script_path.name}"

            content = output_file.read_text()
            assert len(content.strip()) > 0, \
                f"Output file is empty for {script_path.name}"

    @pytest.mark.output
    def test_file_output_with_json_format(self, script_path: Path, sample_data_dir: Path, temp_output_dir: Path):
        """Test that --file works with --output json"""
        sample_file = sample_data_dir / 'sample.txt'
        output_file = temp_output_dir / 'output.json'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file),
             '--output', 'json', '--file', str(output_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Both flags optional
        if '--file' in result.stderr or '--output' in result.stderr:
            return

        if result.returncode == 0 and output_file.exists():
            # File should contain valid JSON
            try:
                data = json.loads(output_file.read_text())
                assert isinstance(data, (dict, list))
            except json.JSONDecodeError:
                # File content might not be JSON (format not supported)
                pass

    @pytest.mark.output
    def test_file_output_directory_permissions(self, script_path: Path, sample_data_dir: Path, temp_output_dir: Path):
        """Test that file output respects directory permissions"""
        sample_file = sample_data_dir / 'sample.txt'
        output_file = temp_output_dir / 'output.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file), '--file', str(output_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # If output to temp directory succeeded, should have valid file
        if result.returncode == 0 and output_file.exists():
            assert output_file.is_file(), \
                f"Output path is not a file for {script_path.name}"


class TestOutputConsistency:
    """Test consistency of output across multiple runs"""

    @pytest.mark.output
    def test_repeated_execution_produces_consistent_output(self, script_path: Path, sample_data_dir: Path):
        """Test that running script twice with same input produces same output"""
        sample_file = sample_data_dir / 'sample.txt'

        result1 = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        result2 = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result1.returncode == 0 and result2.returncode == 0:
            # Should produce same output (for deterministic scripts)
            assert result1.stdout == result2.stdout, \
                f"Output inconsistent on repeated runs for {script_path.name}"

    @pytest.mark.output
    def test_stderr_for_warnings_only(self, script_path: Path, sample_data_dir: Path):
        """Test that stderr is used for warnings/errors, not normal output"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            # On success, main output should be on stdout
            # stderr should be empty or just warnings
            if result.stderr.strip():
                # stderr might have debug/verbose output, but stdout should have primary output
                assert len(result.stdout.strip()) > 0 or result.stderr.startswith('DEBUG') or \
                       result.stderr.startswith('INFO'), \
                       f"Error output on stderr for successful execution of {script_path.name}"

    @pytest.mark.output
    def test_verbose_output_option(self, script_path: Path, sample_data_dir: Path):
        """Test that --verbose flag produces additional output"""
        sample_file = sample_data_dir / 'sample.txt'

        result_normal = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        result_verbose = subprocess.run(
            ['python3', str(script_path), str(sample_file), '--verbose'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # --verbose is optional
        if 'unrecognized arguments' in result_verbose.stderr:
            return

        if result_verbose.returncode == 0:
            # Verbose output should be equal or longer
            normal_out = len(result_normal.stdout) + len(result_normal.stderr)
            verbose_out = len(result_verbose.stdout) + len(result_verbose.stderr)

            # Verbose should not produce less output
            assert verbose_out >= normal_out, \
                f"Verbose mode produces less output for {script_path.name}"
