"""Main CLI entry point for TempDD."""

import argparse
import json
import logging
import sys
from pathlib import Path

from . import __version__
from tempdd.handlers.init import init_command
from tempdd.handlers.ai import ai_command


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
        """
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"TempDD {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new TempDD project"
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Force initialization even if files already exist"
    )
    init_parser.add_argument(
        "--tool",
        default="claudecode",
        help="Target tool for integration (default: claude-code)"
    )
    init_parser.add_argument(
        "--language",
        default="en",
        help="Language setting (default: en)"
    )
    init_parser.add_argument(
        "--config",
        help="Path to configuration file (default: uses built-in default_config.json)"
    )

    # AI command (replaces preprocess and agent)
    ai_parser = subparsers.add_parser(
        "ai",
        help="Process stage with specified action"
    )
    ai_parser.add_argument(
        "stage_action",
        help="Stage and action in format 'stage action' (e.g., 'prd build', 'arch continue')"
    )

    return parser


def _get_logging_level_from_config() -> int:
    """Get logging level from configuration."""
    try:
        # Try to load project config first
        config_file = Path.cwd() / ".tempdd" / "config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            # Fallback to default config
            default_config_path = Path(__file__).parent / "core" / "default_config.json"
            with open(default_config_path, 'r', encoding='utf-8') as f:
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
        format='%(levelname)s: %(message)s',
        handlers=[logging.StreamHandler()]
    )

    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    try:
        if args.command == "init":
            return init_command(
                force=getattr(args, 'force', False),
                tool=getattr(args, 'tool', 'claudecode'),
                language=getattr(args, 'language', 'en'),
                config_path=getattr(args, 'config', None)
            )
        elif args.command == "ai":
            return ai_command(args.stage_action)
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
