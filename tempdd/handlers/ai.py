"""AI command implementation."""

import sys
import json
import importlib
import logging
from pathlib import Path
from tempdd.file_manager import FileManager


# AI Instruction Templates
AI_INSTRUCTION_START = "[AI_INSTRUCTION_START]"
AI_INSTRUCTION_END = "[AI_INSTRUCTION_END]"


def format_ai_instruction(content: str) -> str:
    """Format content as AI instruction with start/end markers."""
    return f"""{AI_INSTRUCTION_START}
{content}
{AI_INSTRUCTION_END}"""


def _load_controller(config_path: str = None):
    """
    Dynamically load Controller from configuration.

    Args:
        config_path: Optional path to configuration file

    Returns:
        Controller instance

    Raises:
        FileNotFoundError: When configuration file is not found
        ImportError: When controller module cannot be imported
    """
    file_manager = FileManager()

    if config_path:
        config_file = Path(config_path)
    else:
        config_file = file_manager.get_project_config_path()

    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        # Fallback to default config
        default_config_path = (
            Path(__file__).parent.parent / "core" / "configs" / "config_default.json"
        )
        if default_config_path.exists():
            with open(default_config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            raise FileNotFoundError("No configuration file found")

    # Get controller name from config
    controller_name = config.get("controller", "controller_default")

    # Dynamically import the controller
    module_path = f"tempdd.core.controllers.{controller_name}"
    try:
        controller_module = importlib.import_module(module_path)
        Controller = controller_module.Controller
        return Controller(config_path)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Failed to import controller '{controller_name}': {e}")


def ai_command(command_str: str) -> int:
    """
    Handle AI command with stage and action.

    Args:
        command_str: Command string in format "stage action" (e.g., "prd build")

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Parse command string "stage action"
        parts = command_str.strip().split()
        if len(parts) != 2:
            logger = logging.getLogger(__name__)
            logger.error(
                f"Invalid command format. Expected 'stage action', got: '{command_str}'"
            )
            logger.info("Examples: 'prd build', 'arch run'")
            return 1

        stage, action = parts

        # Load controller and process command
        controller = _load_controller()
        instruction_content = controller.process_command(stage, action)

        # Format the instruction with AI markers
        ai_instruction = format_ai_instruction(instruction_content)

        # Output the AI instruction
        print(ai_instruction)  # This should remain as print for CLI output
        return 0

    except FileNotFoundError as e:
        logger = logging.getLogger(__name__)
        logger.error(
            f"A required file was not found. Please check your configuration and templates.\nDetails: {e}"
        )
        return 1
    except ValueError as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Invalid value or configuration provided.\nDetails: {e}")
        return 1
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"An unexpected error occurred: {e}")
        return 1
