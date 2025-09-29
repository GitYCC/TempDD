"""Main CLI entry point for TempDD."""

import argparse
import json
import logging
import sys

from . import __version__
from tempdd.handlers.init import init_command
from tempdd.handlers.ai import ai_command
from tempdd.handlers.help import help_command
from tempdd.file_manager import FileManager


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="tempdd",
        description="Template-Driven Development CLI framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tempdd init                    # Initialize a new TempDD project
  tempdd ai "prd build"          # Build PRD document
  tempdd ai "arch continue"      # Continue architecture document
  tempdd ai "task run"           # Run task document
        """,
    )

    parser.add_argument("--version", action="version", version=f"TempDD {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new TempDD project")
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Force initialization even if files already exist",
    )
    init_parser.add_argument(
        "--workflow",
        help="Path to workflow directory (e.g., customized/workflow_example). If contains config.yaml, will copy entire workflow without interactive mode.",
    )

    # AI command (replaces preprocess and agent)
    ai_parser = subparsers.add_parser("ai", help="Process stage with specified action")
    ai_parser.add_argument(
        "stage_action",
        help="Stage and action in format 'stage action' (e.g., 'prd build', 'arch continue')",
    )

    # Help command
    help_parser = subparsers.add_parser(
        "help", help="Show help information about TempDD workflow"
    )

    return parser


def _get_logging_level_from_config() -> int:
    """Get logging level from configuration."""
    try:
        file_manager = FileManager()

        # Try to load project config first
        project_config_path = file_manager.get_project_config_path()
        if project_config_path.exists():
            with open(project_config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            # Fallback to default config
            default_config_path = file_manager.get_default_config_path()
            with open(default_config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

        level_str = config.get("logging_level", "WARNING").upper()
        return getattr(logging, level_str, logging.WARNING)
    except (FileNotFoundError, json.JSONDecodeError, AttributeError):
        # If anything fails, default to WARNING
        return logging.WARNING


def main() -> int:
    """Main CLI entry point."""
    # Configure logging for CLI from configuration
    logging_level = _get_logging_level_from_config()
    logging.basicConfig(
        level=logging_level,
        format="%(levelname)s: %(message)s",
        handlers=[logging.StreamHandler()],
    )

    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    try:
        if args.command == "init":
            return init_command(
                force=getattr(args, "force", False),
                workflow_path=getattr(args, "workflow", None),
            )
        elif args.command == "ai":
            return ai_command(args.stage_action)
        elif args.command == "help":
            return help_command()
        else:
            logger = logging.getLogger(__name__)
            logger.error(f"Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        logger = logging.getLogger(__name__)
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
