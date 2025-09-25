"""AI command implementation."""

import sys
import json
import importlib
from pathlib import Path


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
    work_dir = Path.cwd()

    if config_path:
        config_file = Path(config_path)
    else:
        config_file = work_dir / ".tempdd" / "config.json"

    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        # Fallback to default config
        default_config_path = Path(__file__).parent.parent / "core" / "default_config.json"
        if default_config_path.exists():
            with open(default_config_path, 'r', encoding='utf-8') as f:
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
            print(f"Error: Invalid command format. Expected 'stage action', got: '{command_str}'", file=sys.stderr)
            print("Examples: 'prd build', 'arch run'", file=sys.stderr)
            return 1

        stage, action = parts

        # Load controller and process command
        controller = _load_controller()
        ai_instruction = controller.process_command(stage, action)

        # Output the AI instruction
        print(ai_instruction)
        return 0

    except FileNotFoundError as e:
        print(f"Error: A required file was not found. Please check your configuration and templates.\nDetails: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: Invalid value or configuration provided.\nDetails: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return 1
