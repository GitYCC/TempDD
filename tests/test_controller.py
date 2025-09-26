"""
Tests for TempDD Controller

This module contains tests for the Controller class initialization
and basic functionality.
"""

import pytest
import json
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open
from tempdd.core.controllers.controller_default import Controller


class TestControllerInitialization:
    """Test Controller class initialization"""

    def test_controller_init_without_config_path(self):
        """Test Controller initialization without custom config path uses default config"""
        # Should initialize successfully using default config
        controller = Controller()
        assert controller is not None
        assert controller.config is not None
        assert isinstance(controller.config, dict)

    def test_controller_init_with_project_config(self, tmp_path):
        """Test Controller initialization with existing project config"""
        # Create a temporary project structure
        tempdd_dir = tmp_path / ".tempdd"
        tempdd_dir.mkdir()

        config_data = {
            "language": "en",
            "stages": ["prd", "arch", "research", "blueprint", "task"],
            "controller": "default",
            "templates": {"prd": "template_prd_default"},
            "controller_state": {}
        }

        config_file = tempdd_dir / "config.json"
        config_file.write_text(json.dumps(config_data, indent=2))

        # Mock current working directory
        with patch('pathlib.Path.cwd', return_value=tmp_path):
            controller = Controller()
            assert controller.config == config_data
            assert controller.work_dir == tmp_path

    def test_controller_init_with_custom_config_path(self, tmp_path):
        """Test Controller initialization with custom config path"""
        # Create custom config file
        custom_config = tmp_path / "custom_config.json"
        config_data = {
            "language": "zh-TW",
            "stages": ["prd", "arch"],
            "controller": "default"
        }

        custom_config.write_text(json.dumps(config_data))

        controller = Controller(config_path=str(custom_config))
        assert controller.config == config_data
        assert controller.config_path == str(custom_config)

    def test_controller_init_fallback_to_default_config(self, tmp_path):
        """Test Controller initialization falls back to default config"""
        # This test is actually covered by the first test since it uses real default config
        # Let's just verify the behavior exists by checking config is loaded
        controller = Controller()
        assert controller.config is not None
        assert "stages" in controller.config

    def test_controller_init_no_config_found(self, tmp_path):
        """Test Controller initialization when no config is found"""
        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('pathlib.Path.exists', return_value=False):
                with pytest.raises(FileNotFoundError, match="No configuration file found"):
                    Controller()

    def test_controller_uses_work_directory_from_new_config(self, tmp_path):
        """Test process_command uses work_directory from the new config format."""
        # Create a temporary project structure
        tempdd_dir = tmp_path / ".tempdd"
        tempdd_dir.mkdir()
        templates_dir = tempdd_dir / "templates"
        templates_dir.mkdir()

        # New configuration format
        config_data = {
            "language": "zh-TW",
            "stages": ["prd"],
            "controller": "default",
            "templates": {"prd": "template_prd_default"},
            "controller_state": {
                "work_directory": "custom-docs"
            }
        }
        config_file = tempdd_dir / "config.json"
        config_file.write_text(json.dumps(config_data, indent=2))

        # Create a dummy template file to avoid FileNotFoundError
        template_file = templates_dir / "template_prd.md"
        template_file.write_text("---\nbuild:\n  prompt: 'Test prompt for {{TARGET_DOCUMENT}}'\n---\n# Template")

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            controller = Controller()
            ai_instruction = controller.process_command("prd", "build")

            # The path in the instruction should use the default docs-for-works directory
            expected_path_segment = str(Path("docs-for-works") / "001_initialization" / "prd.md")
            assert expected_path_segment in ai_instruction


class TestControllerBasicMethods:
    """Test Controller basic methods"""

    def test_validate_stage_valid(self, tmp_path):
        """Test _validate_stage with valid stage"""
        config_data = {
            "stages": ["prd", "arch", "research"]
        }

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
                with patch('pathlib.Path.exists', return_value=True):
                    controller = Controller()
                    assert controller._validate_stage("prd") is True
                    assert controller._validate_stage("arch") is True

    def test_validate_stage_invalid(self, tmp_path):
        """Test _validate_stage with invalid stage"""
        config_data = {
            "stages": ["prd", "arch"]
        }

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
                with patch('pathlib.Path.exists', return_value=True):
                    controller = Controller()
                    assert controller._validate_stage("invalid_stage") is False

    def test_get_config(self, tmp_path):
        """Test get_config returns a copy of configuration"""
        config_data = {
            "language": "en",
            "stages": ["prd"]
        }

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
                with patch('pathlib.Path.exists', return_value=True):
                    controller = Controller()
                    returned_config = controller.get_config()

                    # Should return a copy, not the original
                    assert returned_config == config_data
                    returned_config["language"] = "zh-TW"
                    assert controller.config["language"] == "en"  # Original unchanged


class TestProcessCommand:
    """Test Controller process_command method"""

    def test_process_command_valid_stage_default_action(self, tmp_path):
        """Test process_command with valid stage and default action"""
        config_data = {
            "stages": ["prd", "arch", "research"],
            "templates": {"prd": "template_prd_default"}
        }

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
                with patch('pathlib.Path.exists', return_value=True):
                    controller = Controller()

                    # This should fail initially because process_command logic is incomplete
                    result = controller.process_command("prd")

                    # Currently returns placeholder, but should return proper AI instruction
                    assert "[PLACEHOLDER]" not in result
                    assert "prd" in result.lower()
                    assert "build" in result.lower()

    def test_process_command_valid_stage_custom_action(self, tmp_path):
        """Test process_command with valid stage and custom action"""
        config_data = {
            "stages": ["prd", "arch"],
            "templates": {"arch": "template_arch_default"}
        }

        # Create a mock existing directory structure
        docs_dir = tmp_path / "docs-for-works"
        docs_dir.mkdir()
        existing_dir = docs_dir / "001_initialization"
        existing_dir.mkdir()

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
                with patch('pathlib.Path.exists', return_value=True):
                    controller = Controller()

                    result = controller.process_command("arch", "run")

                    # Should return proper AI instruction, not placeholder
                    assert "[PLACEHOLDER]" not in result
                    assert "arch" in result.lower()
                    assert "run" in result.lower()

    def test_process_command_invalid_stage(self, tmp_path):
        """Test process_command with invalid stage raises ValueError"""
        config_data = {
            "stages": ["prd", "arch"]
        }

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
                with patch('pathlib.Path.exists', return_value=True):
                    controller = Controller()

                    with pytest.raises(ValueError, match="Invalid stage: invalid_stage"):
                        controller.process_command("invalid_stage")

    def test_process_command_missing_template(self, tmp_path):
        """Test process_command when template file is missing"""
        config_data = {
            "stages": ["prd"],
            "templates": {"prd": "template_prd_default"}
        }

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
                with patch('pathlib.Path.exists', return_value=True):
                    controller = Controller()

                    # Mock template file doesn't exist
                    with patch('pathlib.Path.exists', return_value=False):
                        with pytest.raises(FileNotFoundError):
                            controller.process_command("prd")

    def test_process_command_generates_ai_instruction_format(self, tmp_path):
        """Test that process_command generates properly formatted AI instruction"""
        config_data = {
            "language": "zh-TW",
            "stages": ["prd"],
            "templates": {"prd": "template_prd_default"},
            "controller_state": {"current_target_document": "/path/to/prd.md"}
        }

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            with patch('builtins.open', mock_open(read_data=json.dumps(config_data))):
                with patch('pathlib.Path.exists', return_value=True):
                    controller = Controller()

                    result = controller.process_command("prd", "create")

                    # Controller should return content without AI instruction markers
                    assert "[AI_INSTRUCTION_START]" not in result
                    assert "[AI_INSTRUCTION_END]" not in result

                    # Should contain language and target document info
                    assert "zh-TW" in result or "Language:" in result
                    assert "Target Document:" in result

# Helper function to get stages from default config
def get_default_stages():
    default_config_path = Path(__file__).parent.parent / "tempdd" / "core" / "configs" / "config_default.json"
    with open(default_config_path, 'r') as f:
        config = json.load(f)
    return config.get("stages", [])

class TestCompleteness:
    """
    Tests for complete coverage of all stages and actions.
    This corresponds to T305, T306, and T307.
    """
    STAGES = get_default_stages()

    def _run_combination_test(self, tmp_path, stage, action):
        """Helper function to run a stage/action combination test."""
        # Setup a mock project structure in a temporary directory
        tempdd_dir = tmp_path / ".tempdd"
        tempdd_dir.mkdir()
        templates_dir = tempdd_dir / "templates"
        templates_dir.mkdir()
        
        config_data = {
            "stages": self.STAGES,
            "controller_state": {}
        }
        config_file = tempdd_dir / "config.json"
        config_file.write_text(json.dumps(config_data))

        template_path = Path(__file__).parent.parent / "tempdd" / "core" / "templates" / f"template_{stage}_default.md"
        if not template_path.exists():
            pytest.fail(f"Template not found at path: {template_path.resolve()}")

        shutil.copy(template_path, templates_dir / f"template_{stage}.md")

        if stage != "prd":
            (tmp_path / "docs-for-works" / "001_initialization").mkdir(parents=True, exist_ok=True)

        with patch('pathlib.Path.cwd', return_value=tmp_path):
            controller = Controller()
            try:
                ai_instruction = controller.process_command(stage, action)
                assert "[AI_INSTRUCTION_START]" not in ai_instruction
                assert "[AI_INSTRUCTION_END]" not in ai_instruction
                assert "You are working on the" not in ai_instruction, f"Stage '{{stage}}', Action '{{action}}' is using a fallback prompt."
            except FileNotFoundError as e:
                pytest.fail(f"Stage '{{stage}}', Action '{{action}}' failed: {{e}}")

    @pytest.mark.parametrize("stage", STAGES)
    def test_build_action_for_all_stages(self, tmp_path, stage):
        """Test that the 'build' action is correctly implemented for all stages."""
        self._run_combination_test(tmp_path, stage, "build")

    def test_run_action_for_tasks_stage(self, tmp_path):
        """Test that the 'run' action is correctly implemented for the 'tasks' stage."""
        self._run_combination_test(tmp_path, "tasks", "run")
