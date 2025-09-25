"""Main CLI entry point for TempDD."""

import argparse
import sys

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


def main() -> int:
    """Main CLI entry point."""
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
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
