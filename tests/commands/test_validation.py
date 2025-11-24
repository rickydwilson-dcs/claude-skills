#!/usr/bin/env python3
"""
Unit tests for command validation

Tests all 8 validation checks against various command fixtures.
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from validate_all_commands import CommandValidator, CommandMetadata


class TestCommandMetadata(unittest.TestCase):
    """Test YAML frontmatter parsing"""

    def setUp(self):
        self.fixtures_dir = Path(__file__).parent / 'fixtures'
        self.repo_root = Path(__file__).parent.parent.parent

    def test_parse_valid_frontmatter(self):
        """Test parsing valid YAML frontmatter"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        self.assertEqual(metadata.metadata['name'], 'review.code-pr')
        self.assertEqual(metadata.metadata['category'], 'review')
        self.assertEqual(metadata.metadata['pattern'], 'multi-phase')
        self.assertIn('version', metadata.metadata)

    def test_filename_extraction(self):
        """Test filename is correctly extracted"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        self.assertEqual(metadata.filename, 'review.code-pr')

    def test_content_extraction(self):
        """Test markdown content is correctly extracted"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        self.assertIn('## Usage', metadata.content)
        self.assertIn('## Examples', metadata.content)


class TestValidationChecks(unittest.TestCase):
    """Test all 8 validation checks"""

    def setUp(self):
        self.fixtures_dir = Path(__file__).parent / 'fixtures'
        self.repo_root = Path(__file__).parent.parent.parent
        self.validator = CommandValidator(self.repo_root, verbose=True)

    def test_check_1_valid_name_format(self):
        """Test Check 1: Valid name format"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_name_format(metadata)
        self.assertTrue(valid, f"Name format check failed: {msg}")

    def test_check_1_invalid_name_format(self):
        """Test Check 1: Invalid name format"""
        cmd_file = self.fixtures_dir / 'invalid_name_format.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_name_format(metadata)
        self.assertFalse(valid, "Should reject invalid name format")

    def test_check_2_valid_yaml_frontmatter(self):
        """Test Check 2: Valid YAML frontmatter"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_yaml_frontmatter(metadata)
        self.assertTrue(valid, f"Frontmatter check failed: {msg}")

    def test_check_3_description_length_valid(self):
        """Test Check 3: Valid description length"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_description_length(metadata)
        self.assertTrue(valid, f"Description length check failed: {msg}")

    def test_check_3_description_length_invalid(self):
        """Test Check 3: Invalid description length (too long)"""
        cmd_file = self.fixtures_dir / 'invalid_description_length.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_description_length(metadata)
        self.assertFalse(valid, "Should reject description > 150 chars")

    def test_check_4_pattern_validity_invalid(self):
        """Test Check 4: Invalid pattern type"""
        cmd_file = self.fixtures_dir / 'invalid_pattern.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_pattern_validity(metadata)
        self.assertFalse(valid, "Should reject invalid pattern type")

    def test_check_4_pattern_validity_simple(self):
        """Test Check 4: Valid simple pattern"""
        cmd_file = self.fixtures_dir / 'update.docs-readme.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_pattern_validity(metadata)
        self.assertTrue(valid, f"Simple pattern check failed: {msg}")

    def test_check_4_pattern_validity_agent_style(self):
        """Test Check 4: Valid agent-style pattern"""
        cmd_file = self.fixtures_dir / 'review.architecture-design.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_pattern_validity(metadata)
        self.assertTrue(valid, f"Agent-style pattern check failed: {msg}")

    def test_check_5_category_validity(self):
        """Test Check 5: Category validity"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_category_validity(metadata)
        self.assertTrue(valid, f"Category check failed: {msg}")

    def test_check_6_content_completeness(self):
        """Test Check 6: Content completeness"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_content_completeness(metadata)
        self.assertTrue(valid, f"Content completeness check failed: {msg}")

    def test_check_7_markdown_structure(self):
        """Test Check 7: Markdown structure"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_markdown_structure(metadata)
        self.assertTrue(valid, f"Markdown structure check failed: {msg}")

    def test_check_8_integration_references(self):
        """Test Check 8: Integration references"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        metadata = CommandMetadata(cmd_file)

        valid, msg = self.validator._check_integration_references(metadata)
        self.assertTrue(valid, f"Integration references check failed: {msg}")


class TestFullValidation(unittest.TestCase):
    """Test full validation against fixture commands"""

    def setUp(self):
        self.fixtures_dir = Path(__file__).parent / 'fixtures'
        self.repo_root = Path(__file__).parent.parent.parent
        self.validator = CommandValidator(self.repo_root, verbose=True)

    def test_valid_command_passes_all_checks(self):
        """Test that review.code-pr.md passes all validation"""
        cmd_file = self.fixtures_dir / 'review.code-pr.md'
        is_valid, errors = self.validator.validate_command(cmd_file)

        self.assertTrue(is_valid, f"Valid command failed: {errors}")

    def test_simple_pattern_passes_all_checks(self):
        """Test that update.docs-readme.md passes all validation"""
        cmd_file = self.fixtures_dir / 'update.docs-readme.md'
        is_valid, errors = self.validator.validate_command(cmd_file)

        self.assertTrue(is_valid, f"Simple pattern command failed: {errors}")

    def test_agent_style_pattern_passes_all_checks(self):
        """Test that review.architecture-design.md passes all validation"""
        cmd_file = self.fixtures_dir / 'review.architecture-design.md'
        is_valid, errors = self.validator.validate_command(cmd_file)

        self.assertTrue(is_valid, f"Agent-style pattern command failed: {errors}")

    def test_invalid_name_format_fails(self):
        """Test that invalid_name_format.md fails validation"""
        cmd_file = self.fixtures_dir / 'invalid_name_format.md'
        is_valid, errors = self.validator.validate_command(cmd_file)

        self.assertFalse(is_valid, "Invalid name format should fail validation")
        self.assertTrue(any('Check 1' in str(e) for e in errors), "Should fail Check 1")

    def test_invalid_description_length_fails(self):
        """Test that invalid_description_length.md fails validation"""
        cmd_file = self.fixtures_dir / 'invalid_description_length.md'
        is_valid, errors = self.validator.validate_command(cmd_file)

        self.assertFalse(is_valid, "Long description should fail validation")
        self.assertTrue(any('Check 3' in str(e) for e in errors), "Should fail Check 3")

    def test_invalid_pattern_fails(self):
        """Test that invalid_pattern.md fails validation"""
        cmd_file = self.fixtures_dir / 'invalid_pattern.md'
        is_valid, errors = self.validator.validate_command(cmd_file)

        self.assertFalse(is_valid, "Invalid pattern should fail validation")
        self.assertTrue(any('Check 4' in str(e) for e in errors), "Should fail Check 4")


if __name__ == '__main__':
    unittest.main()
