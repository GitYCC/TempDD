"""Init command implementation."""

from pathlib import Path
import json
import logging
import sys
from tempdd.utils import load_config as load_existing_config, process_template
from tempdd.file_manager import FileManager
from .ui_helpers import (
    select_with_arrows,
    check_tool_installed,
    fallback_number_selection,
    show_banner,
    is_project_initialized,
    ask_user_confirmation,
    HAS_READCHAR,
    HAS_RICH,
    console
)

COLOR_GRAY = "\033[90m"
COLOR_YELLOW = "\033[93m"
COLOR_END = "\033[0m"


def get_available_configs() -> list[tuple[str, dict]]:
    """Get available configuration files with their metadata."""
    file_manager = FileManager()
    configs_dir = file_manager.get_core_path() / "configs"
    config_files = []

    for config_file in configs_dir.glob("config_*.json"):
        config_name = config_file.stem.replace("config_", "")
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            config_files.append((config_name, config_data))
        except (json.JSONDecodeError, FileNotFoundError):
            continue

    # Sort configs to put "default" first
    config_files.sort(key=lambda x: (x[0] != "default", x[0]))

    return config_files


def prompt_config_selection() -> str:
    """Interactive prompt for config selection."""
    configs = get_available_configs()

    if not configs:
        print("No configuration files found, using default.")
        return "default"

    # Build options dictionary
    config_options = {}
    for name, config_data in configs:
        description = config_data.get("description", "No description available")
        config_options[name] = description

    # Check if interactive mode is supported
    if not sys.stdin.isatty() or not HAS_READCHAR:
        # Non-interactive mode or no readchar: use fallback
        return fallback_number_selection(config_options, "Select a configuration:", "default")

    # Interactive mode: use arrow keys
    try:
        selected = select_with_arrows(config_options, "Select a configuration:", "default")
        return selected if selected else configs[0][0]  # Default to first option
    except ImportError:
        # readchar not available, fallback to number selection
        return fallback_number_selection(config_options, "Select a configuration:", "default")


def prompt_platform_selection() -> str:
    """Interactive prompt for platform selection."""
    file_manager = FileManager()
    available_tools = file_manager.list_available_integrations()

    if not available_tools:
        print("No integration tools available.")
        return None

    # Build options dictionary with tool detection status
    platform_options = {}
    for tool in available_tools:
        name = file_manager.INTEGRATION_CONFIGS[tool].name
        # Check if tool is installed
        is_installed = check_tool_installed(tool)
        status = "✓ installed" if is_installed else "○ not detected"
        platform_options[tool] = f"{name} ({status})"

    # Check if interactive mode is supported
    if not sys.stdin.isatty() or not HAS_READCHAR:
        # Non-interactive mode or no readchar: use fallback
        return fallback_number_selection(platform_options, "Select target AI tool:", available_tools[0])

    # Interactive mode: use arrow keys
    try:
        selected = select_with_arrows(platform_options, "Select target AI tool:", available_tools[0])
        return selected if selected else available_tools[0]  # Default to first option
    except ImportError:
        # readchar not available, fallback to number selection
        return fallback_number_selection(platform_options, "Select target AI tool:", available_tools[0])


def prompt_language_input() -> str:
    """Interactive prompt for language selection."""
    language_options = {
        "en": "English",
        "zh-TW": "繁體中文",
        "zh-CN": "简体中文",
        "ja": "日本語",
        "ko": "한국어",
        "custom": "Enter custom language code"
    }

    # Check if interactive mode is supported
    if not sys.stdin.isatty() or not HAS_READCHAR:
        # Non-interactive mode or no readchar: use simple input
        print("\nEnter preferred language (default: en):")
        print(COLOR_GRAY + "Examples: en, zh-TW, zh-CN, ja, ko, etc." + COLOR_END)
        try:
            language = input("Language: ").strip()
            return language if language else "en"
        except KeyboardInterrupt:
            print("\n\033[91mUser interrupted.\033[0m")
            sys.exit(0)

    # Interactive mode: use arrow keys
    try:
        selected = select_with_arrows(language_options, "Enter preferred language:", "en")

        if selected == "custom":
            try:
                language = input("Language code: ").strip()
                return language if language else "en"
            except KeyboardInterrupt:
                sys.exit(0)

        return selected if selected else "en"
    except ImportError:
        # readchar not available, fallback to simple input
        return fallback_number_selection(language_options, "Enter preferred language:", "en")


def load_default_or_custom_config(config_path: str = None) -> dict:
    """Load configuration file, using default if not specified."""
    file_manager = FileManager()

    if config_path:
        if "/" in config_path:
            # It's a file path - must have .json extension
            if not config_path.endswith(".json"):
                raise ValueError(
                    f"Config file path must have .json extension: {config_path}"
                )
            config_file = Path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
        elif config_path.endswith(".json"):
            # It's a .json file in current directory
            config_file = Path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
        else:
            # Use as config name from configs directory
            config_file = file_manager.get_config_path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {config_file}")
    else:
        # Use default config
        config_file = file_manager.get_default_config_path()
        if not config_file.exists():
            raise FileNotFoundError(f"Default config file not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def init_command(
    force: bool = False,
    tool: str = None,
    language: str = None,
    config_path: str = None,
    interactive: bool = True,
) -> int:
    """Initialize a new TempDD project."""
    logger = logging.getLogger(__name__)
    current_path = Path.cwd()

    # Show banner if interactive
    if interactive:
        show_banner()

    logger.info(f"Initializing TempDD project in: {current_path}")

    # Check if project is already initialized
    if is_project_initialized(current_path):
        if force:
            # Force flag provided, proceed without asking
            if interactive:
                if HAS_RICH and console:
                    console.print("[yellow]⚠ Project already initialized. Force flag provided, proceeding...[/yellow]")
                else:
                    print("Warning: Project already initialized. Force flag provided, proceeding...")
        else:
            # Ask user for confirmation
            message = (
                "This directory appears to already contain a TempDD project.\n"
                "Continuing will overwrite existing configuration and templates.\n\n"
                "Do you want to continue and reinitialize the project?"
            )

            if interactive:
                should_continue = ask_user_confirmation(message, default=False)
                if not should_continue:
                    if HAS_RICH and console:
                        console.print("[blue]Initialization cancelled.[/blue]")
                    else:
                        print("Initialization cancelled.")
                    return 0
                else:
                    # User confirmed, continue with normal flow
                    pass
            else:
                # Non-interactive mode: don't proceed without force flag
                logger.error("Project already initialized. Use --force to reinitialize.")
                return 1

    # Interactive prompts if parameters not provided
    if interactive:
        if config_path is None:
            config_path = prompt_config_selection()
            if config_path is None:  # User cancelled
                return 1

        if tool is None:
            tool = prompt_platform_selection()
            if tool is None:  # User cancelled
                return 1

        if language is None:
            language = prompt_language_input()
            if language is None:  # User cancelled
                return 1

    # Set defaults if still None
    if config_path is None:
        config_path = "default"
    if tool is None:
        tool = "claude"
    if language is None:
        language = "en"

    logger.info(f"Using tool: {tool}")
    logger.info(f"Language: {language}")
    logger.info(f"Config: {config_path}")

    try:
        # 1. Load configuration first
        config = load_default_or_custom_config(config_path)

        # Override language if specified
        if language:
            config["language"] = language

        # 2. Create basic directory structure and initialize project
        file_manager = FileManager(current_path)
        file_manager.create_directory_structure(tool, force)

        # 3. Write config to ./.tempdd/config.json
        target_config_path = file_manager.get_project_config_path()
        if target_config_path.exists() and not force:
            logger.info(
                f"Config file already exists at {target_config_path}, skipping..."
            )
        else:
            with open(target_config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logger.info(f"Created config file: .tempdd/config.json")

        # 4. Copy templates with new naming convention (template_{stage}.md)
        file_manager.copy_templates_from_config(config, force)

        # 5. Create tool integration
        file_manager.copy_integration_file(tool, force)

        # Show success message with Rich styling
        if HAS_RICH and console:
            console.print("\n[bold green]✓ TempDD project initialized successfully![/bold green]")

            # Show configuration summary
            from rich.panel import Panel

            # Get stages from config
            stages = config.get("stages", [])
            stages_text = ", ".join(stages) if stages else "None"

            config_summary = f"Configuration: [cyan]{config_path}[/cyan]\nPlatform: [cyan]{tool}[/cyan]\nLanguage: [cyan]{language}[/cyan]\nStages: [cyan]{stages_text}[/cyan]"
            summary_panel = Panel(
                config_summary,
                title="[bold]Project Configuration[/bold]",
                border_style="blue",
                padding=(1, 2)
            )
            console.print(summary_panel)

            # Create next steps panel
            steps_lines = []
            file_manager = FileManager()
            config = file_manager.INTEGRATION_CONFIGS.get(tool)
            if config:
                if tool == "claude":
                    steps_lines.extend([
                        "1. Execute [cyan]claude[/cyan] to start Claude Code",
                        "2. Use [cyan]/tempdd-go help[/cyan] command in Claude Code to learn how to use the current flow."
                    ])
                elif tool == "gemini":
                    steps_lines.extend([
                        "1. Execute [cyan]gemini[/cyan] to start Gemini CLI",
                        "2. Use [cyan]/tempdd-go help[/cyan] command in Gemini CLI to learn how to use the current flow."
                    ])
                elif tool == "cursor":
                    steps_lines.extend([
                        "1. Execute [cyan]cursor .[/cyan] to start Cursor",
                        "2. Use [cyan]Ctrl+K[/cyan] then [cyan]/tempdd-go help[/cyan] to learn how to use the current flow."
                    ])
                elif tool == "copilot":
                    steps_lines.extend([
                        "1. Open project in your IDE with GitHub Copilot installed",
                        "2. Use [cyan]#tempdd-go help[/cyan] in your prompt to learn how to use the current flow."
                    ])

            if steps_lines:
                from rich.panel import Panel
                steps_panel = Panel(
                    "\n".join(steps_lines),
                    title="[bold]Next Steps[/bold]",
                    border_style="green",
                    padding=(1, 2)
                )
                console.print(steps_panel)
        else:
            # Fallback without Rich
            print(COLOR_YELLOW + "\nTempDD project initialized successfully!" + COLOR_END)
            print(f"Configuration: {config_path}")
            print(f"Platform: {tool}")
            print(f"Language: {language}")

            # Get stages from config
            stages = config.get("stages", [])
            stages_text = ", ".join(stages) if stages else "None"
            print(f"Stages: {stages_text}")

            print(COLOR_YELLOW + "\nNext steps:" + COLOR_END)

            file_manager = FileManager()
            config = file_manager.INTEGRATION_CONFIGS.get(tool)
            if config:
                if tool == "claude":
                    print(
                        COLOR_YELLOW
                        + "1. Execute `claude` to start Claude Code"
                        + COLOR_END
                    )
                    print(
                        COLOR_YELLOW
                        + "2. Use '/tempdd-go help' command in Claude Code to learn how to use the current flow."
                        + COLOR_END
                    )
                elif tool == "gemini":
                    print(
                        COLOR_YELLOW + "1. Execute `gemini` to start Gemini CLI" + COLOR_END
                    )
                    print(
                        COLOR_YELLOW
                        + "2. Use '/tempdd-go help' command in Gemini CLI to learn how to use the current flow."
                        + COLOR_END
                    )
                elif tool == "cursor":
                    print(
                        COLOR_YELLOW + "1. Execute `cursor .` to start Cursor" + COLOR_END
                    )
                    print(
                        COLOR_YELLOW
                        + "2. Use 'Ctrl+K' then '/tempdd-go help' to learn how to use the current flow."
                        + COLOR_END
                    )
                elif tool == "copilot":
                    print(
                        COLOR_YELLOW
                        + "1. Open project in your IDE with GitHub Copilot installed"
                        + COLOR_END
                    )
                    print(
                        COLOR_YELLOW
                        + "2. Use '#tempdd-go help' in your prompt to learn how to use the current flow."
                        + COLOR_END
                    )
        return 0

    except Exception as e:
        logger.error(f"Failed to initialize project: {e}")
        return 1
