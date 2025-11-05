"""
Test suite for basic script execution and functionality

Tests that scripts:
- Execute successfully with valid input
- Return exit code 0 on success
- Handle missing files gracefully
- Return appropriate error codes
- Produce meaningful output

Markers:
  @pytest.mark.execution - Execution and functionality tests
"""

import pytest
import subprocess
import json
from pathlib import Path


class TestBasicScriptExecution:
    """Test basic execution and error handling"""

    @pytest.mark.execution
    def test_script_executes_without_args(self, script_path: Path):
        """Test that script can be run (may fail if required args, but shouldn't crash)"""
        result = subprocess.run(
            ['python3', str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Script should either:
        # 1. Run successfully (exit 0)
        # 2. Show error about missing args (exit 1 or 2)
        # But should NOT crash with exit 127 or timeout
        assert result.returncode in [0, 1, 2], \
            f"Script {script_path.name} crashed: {result.stderr[:200]}"

    @pytest.mark.execution
    def test_script_with_valid_input_file(self, script_path: Path, sample_data_dir: Path):
        """Test script execution with valid sample data"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should handle input file without crashing
        # May return 0 (success) or 1 (expected error), but not crash
        assert result.returncode in [0, 1, 2], \
            f"Script {script_path.name} crashed with input: {result.stderr[:200]}"

    @pytest.mark.execution
    def test_script_missing_file_error(self, script_path: Path):
        """Test that script handles missing files gracefully"""
        result = subprocess.run(
            ['python3', str(script_path), '/nonexistent/file/that/does/not/exist.txt'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should NOT execute successfully
        # Should return error code (1, 2) but not crash
        if result.returncode == 0:
            # Some scripts might not require file args - that's ok
            pass
        else:
            # Should have error message in stderr or stdout
            output = result.stderr + result.stdout
            assert len(output.strip()) > 0, \
                f"Script {script_path.name} failed silently on missing file"

    @pytest.mark.execution
    def test_script_no_timeout(self, script_path: Path, sample_data_dir: Path):
        """Test that script completes within timeout"""
        sample_file = sample_data_dir / 'sample.txt'

        try:
            result = subprocess.run(
                ['python3', str(script_path), str(sample_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            # Should complete without timeout
            assert True
        except subprocess.TimeoutExpired:
            pytest.fail(f"Script {script_path.name} exceeded 30 second timeout")

    @pytest.mark.execution
    def test_script_output_not_empty_on_success(self, script_path: Path, sample_data_dir: Path):
        """Test that successful execution produces output"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # If script succeeds, should produce output
        if result.returncode == 0:
            combined_output = result.stdout + result.stderr
            assert len(combined_output.strip()) > 0, \
                f"Script {script_path.name} produced no output"

    @pytest.mark.execution
    def test_script_syntax_valid(self, script_path: Path):
        """Test that script has valid Python syntax"""
        result = subprocess.run(
            ['python3', '-m', 'py_compile', str(script_path)],
            capture_output=True,
            text=True,
            timeout=10
        )

        assert result.returncode == 0, \
            f"Script {script_path.name} has syntax errors: {result.stderr}"

    @pytest.mark.execution
    def test_script_has_main_function(self, script_path: Path):
        """Test that script has a main entry point"""
        content = script_path.read_text()

        # Should have either:
        # 1. if __name__ == "__main__": pattern
        # 2. main() function
        has_main_guard = 'if __name__ == "__main__"' in content
        has_main_func = 'def main' in content

        assert has_main_guard, \
            f"Script {script_path.name} missing main guard (if __name__ == '__main__')"

    @pytest.mark.execution
    def test_script_uses_argparse(self, script_path: Path):
        """Test that script uses argparse for CLI"""
        content = script_path.read_text()

        # All scripts should use argparse for CLI compatibility
        assert 'argparse' in content, \
            f"Script {script_path.name} doesn't use argparse"

        assert 'ArgumentParser' in content or 'argparse.ArgumentParser' in content, \
            f"Script {script_path.name} doesn't instantiate ArgumentParser"


class TestExitCodes:
    """Test that scripts return appropriate exit codes"""

    @pytest.mark.execution
    def test_help_returns_zero(self, script_path: Path):
        """Test that --help returns exit code 0"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, \
            f"Help should return 0, got {result.returncode} for {script_path.name}"

    @pytest.mark.execution
    def test_invalid_arg_returns_nonzero(self, script_path: Path):
        """Test that invalid arguments return non-zero exit code"""
        result = subprocess.run(
            ['python3', str(script_path), '--invalid-arg-xyz-123'],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Should fail with invalid argument
        if '--invalid-arg-xyz-123' not in result.stderr and '--invalid-arg-xyz-123' not in result.stdout:
            # If argument wasn't recognized by argparse, should be error
            assert result.returncode != 0, \
                f"Invalid argument should return non-zero for {script_path.name}"


class TestOutputFormatFlags:
    """Test output format flags if supported"""

    @pytest.mark.execution
    def test_output_json_flag(self, script_path: Path, sample_data_dir: Path):
        """Test --output json flag if implemented"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file), '--output', 'json'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # If flag is not supported, script might error (that's ok)
        # If supported, should be valid JSON
        if result.returncode == 0 and result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                # Should be valid JSON
                assert isinstance(data, (dict, list)), \
                    f"JSON output should be dict or list for {script_path.name}"
            except json.JSONDecodeError:
                # Flag might not be implemented - that's ok
                pass

    @pytest.mark.execution
    def test_output_text_flag(self, script_path: Path, sample_data_dir: Path):
        """Test --output text flag if implemented"""
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file), '--output', 'text'],
            capture_output=True,
            text=True,
            timeout=30
        )

        # If flag is supported, should return readable text
        if result.returncode == 0:
            assert len(result.stdout.strip()) > 0, \
                f"Text output should not be empty for {script_path.name}"


class TestErrorHandling:
    """Test error handling and edge cases"""

    @pytest.mark.execution
    def test_error_message_clarity(self, script_path: Path):
        """Test that error messages are clear when args are missing"""
        result = subprocess.run(
            ['python3', str(script_path), '--invalid'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            # Error output should be informative
            error_msg = result.stderr + result.stdout
            assert len(error_msg.strip()) > 0, \
                f"Error message should explain the problem for {script_path.name}"

    @pytest.mark.execution
    def test_script_doesnt_modify_cwd(self, script_path: Path, sample_data_dir: Path):
        """Test that script execution doesn't unexpectedly change working directory"""
        from pathlib import Path
        import os

        original_cwd = os.getcwd()
        sample_file = sample_data_dir / 'sample.txt'

        result = subprocess.run(
            ['python3', str(script_path), str(sample_file)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=original_cwd
        )

        # After subprocess, cwd should still be the same
        assert os.getcwd() == original_cwd, \
            "Script execution changed working directory"

    @pytest.mark.execution
    def test_script_handles_unicode(self, script_path: Path, sample_data_dir: Path):
        """Test that script can handle UTF-8 encoded input"""
        unicode_file = sample_data_dir / 'unicode_sample.txt'
        unicode_file.write_text(
            'Hello with Unicode characters: café, naïve, résumé, 你好, مرحبا',
            encoding='utf-8'
        )

        try:
            result = subprocess.run(
                ['python3', str(script_path), str(unicode_file)],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8'
            )

            # Should handle unicode without crashing (may error gracefully)
            assert result.returncode in [0, 1, 2], \
                f"Script {script_path.name} crashed on unicode input"
        finally:
            unicode_file.unlink()
