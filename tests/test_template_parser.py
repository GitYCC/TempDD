"""
Tests for TempDD Template Parser

This module contains tests for the Template Parser's YAML frontmatter parsing,
action-specific prompt extraction, and template variable processing.
"""

import pytest
from pathlib import Path
from tempdd.template_parser import (
    parse_template,
    get_action_prompt,
    process_template_variables,
    validate_template_metadata
)


class TestTemplateConversion:
    """Test template conversion to new format"""

    def test_prd_template_has_new_format_frontmatter(self):
        """Test that PRD template has been converted to new format"""
        template_path = Path(__file__).parent.parent / "tempdd" / "core" / "templates" / "template_prd_default.md"

        if not template_path.exists():
            pytest.skip("PRD template does not exist yet")

        # Parse the template
        metadata, content = parse_template(str(template_path))

        # Should have the new action-based structure
        assert "build" in metadata

        # Each action should have a prompt
        assert "prompt" in metadata["build"]

        # Content should still contain the original template
        assert "Product Requirements Document" in content
        assert "Basic Information" in content


class TestYAMLFrontmatterParsing:
    """Test YAML frontmatter parsing functionality"""

    def test_parse_template_with_valid_frontmatter(self, tmp_path):
        """Test parsing template with valid YAML frontmatter"""
        template_content = """---
build:
  prompt: |
    You are a Product Manager working on building a PRD.
    Language: {{LANGUAGE}}
    Target Document: {{TARGET_DOCUMENT}}

    Ask the stakeholder what they want to build today.
run:
  prompt: |
    Review and validate the PRD document.
    Check completeness of {{TARGET_DOCUMENT}}.
---

# Product Requirements Document

This is the template content for PRD.
"""

        template_file = tmp_path / "test_template.md"
        template_file.write_text(template_content)

        # This should parse correctly and extract metadata
        metadata, content = parse_template(str(template_file))

        # Test metadata structure
        assert isinstance(metadata, dict)
        assert "build" in metadata
        assert "run" in metadata

        # Test build action
        assert "prompt" in metadata["build"]
        assert "You are a Product Manager" in metadata["build"]["prompt"]
        assert "{{LANGUAGE}}" in metadata["build"]["prompt"]

        # Test run action
        assert "prompt" in metadata["run"]
        assert "Review and validate" in metadata["run"]["prompt"]

        # Test content separation
        assert "# Product Requirements Document" in content
        assert "This is the template content" in content
        assert "---" not in content  # Frontmatter should be removed

    def test_parse_template_without_frontmatter(self, tmp_path):
        """Test parsing template without YAML frontmatter"""
        template_content = """# Simple Template

This template has no frontmatter.
Just plain markdown content.
"""

        template_file = tmp_path / "simple_template.md"
        template_file.write_text(template_content)

        metadata, content = parse_template(str(template_file))

        # Should return empty metadata and full content
        assert metadata == {}
        assert content == template_content

    def test_parse_template_with_invalid_yaml(self, tmp_path):
        """Test parsing template with malformed YAML frontmatter"""
        template_content = """---
build:
  prompt: |
    Valid prompt here
continue
  prompt: |  # Missing colon - invalid YAML
    Continue prompt
---

# Template Content
"""

        template_file = tmp_path / "invalid_yaml.md"
        template_file.write_text(template_content)

        # Should raise ValueError for invalid YAML
        with pytest.raises(ValueError, match="Invalid YAML frontmatter"):
            parse_template(str(template_file))

    def test_parse_template_file_not_found(self):
        """Test parsing non-existent template file"""
        with pytest.raises(FileNotFoundError, match="Template file not found"):
            parse_template("/nonexistent/path/template.md")

    def test_parse_template_with_incomplete_frontmatter(self, tmp_path):
        """Test parsing template with incomplete frontmatter markers"""
        template_content = """---
build:
  prompt: |
    Some content here
# Missing closing ---

# Template Content
"""

        template_file = tmp_path / "incomplete.md"
        template_file.write_text(template_content)

        # Current implementation will try to parse even incomplete frontmatter
        # The YAML parser will treat everything after first --- as YAML until it finds another ---
        # Since there's no closing ---, it parses the entire content as YAML
        metadata, content = parse_template(str(template_file))

        # Should parse the YAML part successfully
        assert "build" in metadata
        assert "prompt" in metadata["build"]
        assert "Some content here" in metadata["build"]["prompt"]


class TestActionPromptExtraction:
    """Test action-specific prompt extraction"""

    def test_get_action_prompt_valid_action(self):
        """Test extracting prompt for valid action"""
        metadata = {
            "build": {
                "prompt": "Build a new document according to requirements."
            },
            "run": {
                "prompt": "Run validation on existing document."
            }
        }

        build_prompt = get_action_prompt(metadata, "build")
        assert build_prompt == "Build a new document according to requirements."

        run_prompt = get_action_prompt(metadata, "run")
        assert run_prompt == "Run validation on existing document."

    def test_get_action_prompt_invalid_action(self):
        """Test extracting prompt for non-existent action"""
        metadata = {
            "build": {
                "prompt": "Build prompt"
            }
        }

        result = get_action_prompt(metadata, "nonexistent")
        assert result is None

    def test_get_action_prompt_malformed_metadata(self):
        """Test extracting prompt from malformed metadata"""
        # Test with non-dict metadata
        assert get_action_prompt("not a dict", "build") is None

        # Test with action that's not a dict
        metadata = {
            "build": "not a dict"
        }
        assert get_action_prompt(metadata, "build") is None

        # Test with action dict missing prompt
        metadata = {
            "build": {
                "description": "Some description"
                # Missing 'prompt' key
            }
        }
        assert get_action_prompt(metadata, "build") is None

    def test_get_action_prompt_empty_metadata(self):
        """Test extracting prompt from empty metadata"""
        assert get_action_prompt({}, "build") is None
        assert get_action_prompt(None, "build") is None


class TestTemplateVariableProcessing:
    """Test template variable replacement functionality"""

    def test_process_template_variables_basic(self):
        """Test basic variable replacement"""
        template = "Hello {{NAME}}, your language is {{LANGUAGE}}."
        variables = {
            "NAME": "World",
            "LANGUAGE": "English"
        }

        result = process_template_variables(template, variables)
        assert result == "Hello World, your language is English."

    def test_process_template_variables_multiple_occurrences(self):
        """Test replacing multiple occurrences of same variable"""
        template = "{{GREETING}} {{NAME}}! How are you {{NAME}}?"
        variables = {
            "GREETING": "Hello",
            "NAME": "Alice"
        }

        result = process_template_variables(template, variables)
        assert result == "Hello Alice! How are you Alice?"

    def test_process_template_variables_no_variables(self):
        """Test processing template with no variables"""
        template = "This is a plain text template."
        variables = {}

        result = process_template_variables(template, variables)
        assert result == template

    def test_process_template_variables_unused_variables(self):
        """Test processing with unused variables"""
        template = "Hello {{NAME}}!"
        variables = {
            "NAME": "World",
            "UNUSED": "This won't be used"
        }

        result = process_template_variables(template, variables)
        assert result == "Hello World!"

    def test_process_template_variables_missing_variables(self):
        """Test processing with missing variables (should leave placeholders)"""
        template = "Hello {{NAME}}, your age is {{AGE}}."
        variables = {
            "NAME": "Alice"
            # Missing AGE variable
        }

        result = process_template_variables(template, variables)
        assert result == "Hello Alice, your age is {{AGE}}."

    def test_process_template_variables_missing_variables_with_logging(self, caplog):
        """Test that missing variables are logged as warnings"""
        template = "Hello {{NAME}}, your age is {{AGE}}, location {{LOCATION}}."
        variables = {
            "NAME": "Alice"
            # Missing AGE and LOCATION variables
        }

        with caplog.at_level("WARNING"):
            result = process_template_variables(template, variables)

        assert result == "Hello Alice, your age is {{AGE}}, location {{LOCATION}}."

        # Check that warnings were logged for missing variables
        warning_messages = [record.message for record in caplog.records if record.levelname == "WARNING"]
        assert len(warning_messages) == 2
        assert any("AGE" in msg for msg in warning_messages)
        assert any("LOCATION" in msg for msg in warning_messages)

    def test_process_template_variables_complex_content(self):
        """Test processing template with complex content and multiple variables"""
        template = """You are a {{ROLE}} working on {{STAGE}} stage.

Language: {{LANGUAGE}}
Target Document: {{TARGET_DOCUMENT}}

Instructions:
1. Review the current {{TARGET_DOCUMENT}}
2. Use {{LANGUAGE}} language for communication
3. Complete the {{STAGE}} requirements

Action: {{ACTION}}"""

        variables = {
            "ROLE": "Product Manager",
            "STAGE": "PRD",
            "LANGUAGE": "English",
            "TARGET_DOCUMENT": "/docs/prd.md",
            "ACTION": "build"
        }

        result = process_template_variables(template, variables)

        assert "Product Manager" in result
        assert "PRD stage" in result
        assert "English" in result
        assert "/docs/prd.md" in result
        assert "build" in result
        assert "{{" not in result  # No placeholders should remain


class TestTemplateMetadataValidation:
    """Test template metadata validation"""

    def test_validate_template_metadata_valid(self):
        """Test validating valid metadata"""
        valid_metadata = {
            "build": {
                "prompt": "Build something"
            },
            "run": {
                "prompt": "Run something"
            }
        }

        assert validate_template_metadata(valid_metadata) is True

    def test_validate_template_metadata_empty(self):
        """Test validating empty metadata (should be valid)"""
        assert validate_template_metadata({}) is True

    def test_validate_template_metadata_invalid_structure(self):
        """Test validating invalid metadata structures"""
        # Non-dict metadata
        assert validate_template_metadata("not a dict") is False

        # Action without prompt
        invalid_metadata = {
            "build": {
                "description": "Some description"
                # Missing prompt
            }
        }
        assert validate_template_metadata(invalid_metadata) is False

        # Action that's not a dict
        invalid_metadata = {
            "build": "not a dict"
        }
        assert validate_template_metadata(invalid_metadata) is False

    def test_validate_template_metadata_partial_valid(self):
        """Test validating metadata with mix of valid and invalid actions"""
        mixed_metadata = {
            "build": {
                "prompt": "Valid build prompt"
            },
            "invalid_action": {
                "description": "No prompt field"
            }
        }

        # Should be valid if at least one action is properly structured
        assert validate_template_metadata(mixed_metadata) is True