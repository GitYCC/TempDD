"""Init command implementation."""

from pathlib import Path
import json
import shutil
import logging
import glob
from tempdd.utils import load_config as load_existing_config, process_template

COLOR_GRAY = '\033[90m'
COLOR_YELLOW = '\033[93m'
COLOR_END = '\033[0m'


def get_core_path() -> Path:
    """Get the core directory path."""
    return Path(__file__).parent.parent / "core"


def get_tools_path() -> Path:
    """Get the integrations directory path."""
    return Path(__file__).parent.parent / "integrations"


def get_available_configs() -> list[tuple[str, dict]]:
    """Get available configuration files with their metadata."""
    configs_dir = get_core_path() / "configs"
    config_files = []

    for config_file in configs_dir.glob("config_*.json"):
        config_name = config_file.stem.replace("config_", "")
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            config_files.append((config_name, config_data))
        except (json.JSONDecodeError, FileNotFoundError):
            continue

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
    platforms = [
        ("claudecode", "Claude Code"),
        ("geminicli", "Gemini CLI"),
    ]

    print("\nSelect target platform:")
    for i, (key, name) in enumerate(platforms, 1):
        print(COLOR_GRAY + f"{i}. {name}" + COLOR_END)

    while True:
        try:
            if len(platforms) == 1:
                choice = input(f"Enter choice (1, default: 1): ").strip()
            else:
                choice = input(f"Enter choice (1-{len(platforms)}, default: 1): ").strip()
            if not choice:
                return platforms[0][0]  # Default to Claude Code

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
    if config_path:
        if '/' in config_path:
            # It's a file path - must have .json extension
            if not config_path.endswith('.json'):
                raise ValueError(f"Config file path must have .json extension: {config_path}")
            config_file = Path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
        elif config_path.endswith('.json'):
            # It's a .json file in current directory
            config_file = Path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
        else:
            # Use as config name from configs directory
            config_file = get_core_path() / "configs" / f"config_{config_path}.json"
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {config_file}")
    else:
        # Use default config
        config_file = get_core_path() / "configs" / "config_default.json"
        if not config_file.exists():
            raise FileNotFoundError(f"Default config file not found: {config_file}")

    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_directory_structure(base_path: Path, force: bool = False) -> None:
    """Create the basic TempDD directory structure."""
    directories = [
        ".claude/commands",
        ".tempdd/templates",
    ]

    logger = logging.getLogger(__name__)
    for dir_path in directories:
        full_path = base_path / dir_path
        if full_path.exists() and not force:
            logger.info(f"Directory {dir_path} already exists, skipping...")
            continue
        full_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")



def create_tool_integration(base_path: Path, tool: str = "claudecode", force: bool = False) -> None:
    """Create tool integration files."""
    commands_path = base_path / ".claude" / "commands"

    # Get the source command file from tools directory
    tools_path = get_tools_path() / tool / "commands"
    source_file = tools_path / "tempdd.md"

    logger = logging.getLogger(__name__)
    if not source_file.exists():
        logger.warning(f"Tool integration not found for '{tool}': {source_file}")
        return

    target_file = commands_path / "tempdd.md"
    if target_file.exists() and not force:
        logger.info(f"{tool.title()} integration already exists, skipping...")
        return

    shutil.copy2(source_file, target_file)
    logger.info(f"Created {tool} integration: .claude/commands/tempdd.md")


def copy_templates_from_config(base_path: Path, config: dict, force: bool = False) -> None:
    """Copy template files based on configuration with new naming convention."""
    target_dir = base_path / ".tempdd" / "templates"
    source_dir = get_core_path() / "templates"

    logger = logging.getLogger(__name__)
    logger.info("Creating templates from configuration...")

    # Get templates from config
    templates = config.get("templates", {})

    for stage, template_name in templates.items():
        source_file = source_dir / f"{template_name}.md"
        target_file = target_dir / f"template_{stage}.md"

        # Skip if target exists and force is False
        if target_file.exists() and not force:
            logger.info(f"Template template_{stage}.md already exists, skipping...")
            continue

        # Skip if source doesn't exist
        if not source_file.exists():
            logger.warning(f"Source template not found: {source_file}")
            continue

        # Copy template content directly
        content = source_file.read_text(encoding='utf-8')
        target_file.write_text(content, encoding='utf-8')
        logger.info(f"Created template: .tempdd/templates/template_{stage}.md")


def init_command(force: bool = False, tool: str = None, language: str = None, config_path: str = None, interactive: bool = True) -> int:
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
        tool = "claudecode"
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

        # 2. Create basic directory structure
        create_directory_structure(current_path, force)

        # 3. Write config to ./.tempdd/config.json
        target_config_path = current_path / ".tempdd" / "config.json"
        if target_config_path.exists() and not force:
            logger.info(f"Config file already exists at {target_config_path}, skipping...")
        else:
            with open(target_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logger.info(f"Created config file: .tempdd/config.json")

        # 4. Copy templates with new naming convention (template_{stage}.md)
        copy_templates_from_config(current_path, config, force)

        # 5. Create tool integration
        create_tool_integration(current_path, tool, force)

        print(COLOR_YELLOW + "\nTempDD project initialized successfully!" + COLOR_END)
        print(COLOR_YELLOW + "Next steps:" + COLOR_END)
        if tool == 'claudecode':
            print(COLOR_YELLOW + "1. Execute `claude` to start Claude Code" + COLOR_END)
            print(COLOR_YELLOW + "2. Use '/tempdd help' command in Claude Code to learn how to use the current flow." + COLOR_END)
        print("")
        return 0

    except Exception as e:
        logger.error(f"Failed to initialize project: {e}")
        return 1