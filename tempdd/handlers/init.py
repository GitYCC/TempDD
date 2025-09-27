"""Init command implementation."""

from pathlib import Path
import json
import logging
from tempdd.utils import load_config as load_existing_config, process_template
from tempdd.file_manager import FileManager

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

    print("\nSelect a configuration:")
    for i, (name, config_data) in enumerate(configs, 1):
        description = config_data.get("description", "No description available")
        print(COLOR_GRAY + f"{i}. {name} ({description})" + COLOR_END)

    while True:
        try:
            if len(configs) == 1:
                choice = input(f"Enter choice (1): ").strip()
            else:
                choice = input(f"Enter choice (1-{len(configs)}): ").strip()
            if not choice:
                return configs[0][0]  # Default to first option

            choice_num = int(choice)
            if 1 <= choice_num <= len(configs):
                return configs[choice_num - 1][0]
            else:
                print(f"Please enter a number between 1 and {len(configs)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None


def prompt_platform_selection() -> str:
    """Interactive prompt for platform selection."""
    file_manager = FileManager()
    available_tools = file_manager.list_available_integrations()

    if not available_tools:
        print("No integration tools available.")
        return None

    platforms = [
        (tool, file_manager.INTEGRATION_CONFIGS[tool].name) for tool in available_tools
    ]

    print("\nSelect target platform:")
    for i, (key, name) in enumerate(platforms, 1):
        print(COLOR_GRAY + f"{i}. {name}" + COLOR_END)

    while True:
        try:
            if len(platforms) == 1:
                choice = input(f"Enter choice (1, default: 1): ").strip()
            else:
                choice = input(
                    f"Enter choice (1-{len(platforms)}, default: 1): "
                ).strip()
            if not choice:
                return platforms[0][0]  # Default to first available

            choice_num = int(choice)
            if 1 <= choice_num <= len(platforms):
                return platforms[choice_num - 1][0]
            else:
                print(f"Please enter a number between 1 and {len(platforms)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None


def prompt_language_input() -> str:
    """Interactive prompt for language selection."""
    print("\nEnter preferred language (default: en):")
    print(COLOR_GRAY + "Examples: en, zh-TW, zh-CN, ja, ko, etc." + COLOR_END)

    try:
        language = input("Language: ").strip()
        return language if language else "en"
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return None


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

    logger.info(f"Initializing TempDD project in: {current_path}")

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

        print(COLOR_YELLOW + "\nTempDD project initialized successfully!" + COLOR_END)
        print(COLOR_YELLOW + "Next steps:" + COLOR_END)

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
        print("")
        return 0

    except Exception as e:
        logger.error(f"Failed to initialize project: {e}")
        return 1
