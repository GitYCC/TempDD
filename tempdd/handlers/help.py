"""Help command handler for TempDD."""

import logging
from tempdd.controller import Controller


def help_command() -> int:
    """
    Handle help command

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    logger = logging.getLogger(__name__)

    try:
        controller = Controller()
        help_content = controller.get_help_content()
        print(help_content)
        return 0

    except Exception as e:
        logger.error(f"Failed to get help content: {e}")
        return 1
