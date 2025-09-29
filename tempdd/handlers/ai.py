"""AI command implementation."""

import sys
import logging
from pathlib import Path
from tempdd.controller import Controller


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
    Load the unified Controller.

    Args:
        config_path: Optional path to configuration file

    Returns:
        Controller instance

    Raises:
        FileNotFoundError: When configuration file is not found
    """
    return Controller(config_path)


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
