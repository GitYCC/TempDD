"""Help command handler for TempDD."""

import logging
import json
from pathlib import Path


def help_command() -> int:
    """
    Handle help command

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    logger = logging.getLogger(__name__)

    try:
        # Try to load configuration to get controller type
        work_dir = Path.cwd()
        config_file = work_dir / ".tempdd" / "config.json"

        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            # Fallback to default config
            default_config_path = Path(__file__).parent.parent / "core" / "configs" / "config_default.json"
            with open(default_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

        # Get controller type and dynamically import
        controller_type = config.get("controller", "controller_default")

        try:
            if controller_type == "controller_default":
                from tempdd.core.controllers.controller_default import Controller
            else:
                # Handle other controller types if needed
                from tempdd.core.controllers.controller_default import Controller

            controller = Controller()
            help_content = controller.get_help_content()
            print(help_content)
            return 0
        except ImportError:
            logger.error(f"Controller '{controller_type}' not found")
            return 1

    except Exception as e:
        logger.error(f"Failed to get help content: {e}")
        return 1