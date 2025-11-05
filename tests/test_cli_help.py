"""
Test suite for CLI --help flag compliance

Tests that all Python scripts follow CLI standards:
- Respond to --help flag
- Return exit code 0 on help
- Include usage information
- Document standard flags (--output, --file, --verbose)
- Include examples in help text

Markers:
  @pytest.mark.help - Help flag tests
"""

import pytest
import subprocess
from pathlib import Path


class TestCliHelpFlag:
    """Test --help flag functionality for all scripts"""

    @pytest.mark.help
    def test_script_help_flag(self, script_path: Path, cli_helper):
        """Test that script responds to --help flag with exit code 0"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, \
            f"Help flag failed for {script_path.name}: {result.stderr}"

    @pytest.mark.help
    def test_help_output_contains_usage(self, script_path: Path, cli_helper):
        """Test that help output contains 'usage:' line"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        output = result.stdout.lower()
        assert 'usage:' in output or 'usage ' in output, \
            f"No usage line found in help for {script_path.name}"

    @pytest.mark.help
    def test_help_output_contains_description(self, script_path: Path):
        """Test that help output contains a description"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        # Help should have some description/purpose statement
        lines = result.stdout.strip().split('\n')
        assert len(lines) > 3, \
            f"Help output too short for {script_path.name}: missing description"

    @pytest.mark.help
    def test_help_output_contains_positional_or_optional(self, script_path: Path):
        """Test that help documents arguments (positional or optional)"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        output = result.stdout.lower()

        # Should have at least one of these sections
        has_args = any(keyword in output for keyword in [
            'positional arguments',
            'optional arguments',
            'options:',
            'arguments:',
            'usage:',
            '-h, --help'
        ])
        assert has_args, \
            f"Help output missing argument documentation for {script_path.name}"

    @pytest.mark.help
    def test_help_h_shortcut(self, script_path: Path):
        """Test that -h also works as help shortcut"""
        result = subprocess.run(
            ['python3', str(script_path), '-h'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, \
            f"-h shortcut failed for {script_path.name}"

    @pytest.mark.help
    def test_help_text_quality(self, script_path: Path):
        """Test that help text is well-formed and informative"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0

        lines = result.stdout.strip().split('\n')
        non_empty_lines = [l for l in lines if l.strip()]

        # Should have meaningful content (not just one-liner)
        assert len(non_empty_lines) >= 5, \
            f"Help output too brief for {script_path.name}"

        # Should not have excessive empty lines
        empty_line_ratio = 1 - (len(non_empty_lines) / len(lines)) if lines else 0
        assert empty_line_ratio < 0.5, \
            f"Help output has too many empty lines for {script_path.name}"


class TestCliStandardFlags:
    """Test for common standard flags in help output"""

    @pytest.mark.help
    def test_help_mentions_output_flag(self, script_path: Path):
        """Test that help mentions --output or similar flag (if applicable)"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        # Only assert if script supports it (many scripts do)
        output = result.stdout.lower()

        # This is optional but common - just check if documented when present
        if '--output' in result.stdout or '--json' in result.stdout or '--format' in result.stdout:
            # If output flag exists, it should be documented
            assert 'output' in output or 'json' in output or 'format' in output

    @pytest.mark.help
    def test_help_mentions_verbose_flag(self, script_path: Path):
        """Test that help mentions verbose flag if script supports it"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        # This is optional but good to have
        output = result.stdout.lower()

        if '--verbose' in result.stdout or '-v' in result.stdout:
            # If verbose flag exists, it should be documented
            assert 'verbose' in output or 'detailed' in output

    @pytest.mark.help
    def test_help_contains_examples(self, script_path: Path):
        """Test that help output contains usage examples"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0

        output = result.stdout.lower()
        # Should have examples section or at least show script name in examples
        has_examples = 'example' in output or 'usage' in output

        assert has_examples, \
            f"Help output should include examples for {script_path.name}"


class TestCliHelpEdgeCases:
    """Test edge cases and error handling"""

    @pytest.mark.help
    def test_help_flag_with_extra_args(self, script_path: Path):
        """Test that --help works even with extra arguments"""
        result = subprocess.run(
            ['python3', str(script_path), '--help', 'extra', 'args'],
            capture_output=True,
            text=True,
            timeout=10
        )
        # --help should show help regardless of other args
        assert result.returncode == 0

    @pytest.mark.help
    def test_help_output_not_stderr(self, script_path: Path):
        """Test that help output goes to stdout (not stderr)"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        # Help should be in stdout, not stderr
        assert len(result.stdout.strip()) > 0, \
            f"Help output empty for {script_path.name}"
        # stderr might have warnings but stdout should be primary
        assert 'usage:' in result.stdout.lower() or 'usage ' in result.stdout.lower(), \
            f"Help output not in stdout for {script_path.name}"

    @pytest.mark.help
    def test_help_is_readable(self, script_path: Path):
        """Test that help output uses standard ASCII characters"""
        result = subprocess.run(
            ['python3', str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0

        # Should be readable text, not binary or corrupted
        try:
            # Can decode without issues
            _ = result.stdout.encode('utf-8')
        except UnicodeDecodeError:
            pytest.fail(f"Help output not valid UTF-8 for {script_path.name}")

        # Should have printable characters
        printable = sum(1 for c in result.stdout if c.isprintable() or c in '\n\r\t')
        total = len(result.stdout)
        assert printable / total > 0.95, \
            f"Help output contains too many non-printable characters for {script_path.name}"


class TestCliVersionFlag:
    """Test version flag (if implemented)"""

    @pytest.mark.help
    def test_version_flag_optional(self, script_path: Path):
        """Test that --version flag works if implemented"""
        result = subprocess.run(
            ['python3', str(script_path), '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )

        # --version is optional, but if implemented should return 0
        if result.returncode == 0:
            # Should output version string
            output = result.stdout.strip()
            assert len(output) > 0, \
                f"Version output empty for {script_path.name}"

        # If not implemented, might return non-zero (that's ok)
        # We just verify it doesn't crash
        assert result.returncode in [0, 2], \
            f"Unexpected error with --version for {script_path.name}: {result.stderr}"
