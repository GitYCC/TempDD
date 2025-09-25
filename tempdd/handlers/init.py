"""Init command implementation."""

from pathlib import Path
import json
import shutil
from tempdd.utils import load_config as load_existing_config, process_template


def get_core_path() -> Path:
    """Get the core directory path."""
    return Path(__file__).parent.parent / "core"


def get_tools_path() -> Path:
    """Get the integrations directory path."""
    return Path(__file__).parent.parent / "integrations"


def load_default_or_custom_config(config_path: str = None) -> dict:
    """Load configuration file, using default if not specified."""
    if config_path:
        # Use specified config file
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
    else:
        # Use default config
        config_file = get_core_path() / "default_config.json"
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

    for dir_path in directories:
        full_path = base_path / dir_path
        if full_path.exists() and not force:
            print(f"Directory {dir_path} already exists, skipping...")
            continue
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")



def create_tool_integration(base_path: Path, tool: str = "claudecode", force: bool = False) -> None:
    """Create tool integration files."""
    commands_path = base_path / ".claude" / "commands"

    # Get the source command file from tools directory
    tools_path = get_tools_path() / tool / "commands"
    source_file = tools_path / "tempdd.md"

    if not source_file.exists():
        print(f"Warning: Tool integration not found for '{tool}': {source_file}")
        return

    target_file = commands_path / "tempdd.md"
    if target_file.exists() and not force:
        print(f"{tool.title()} integration already exists, skipping...")
        return

    shutil.copy2(source_file, target_file)
    print(f"Created {tool} integration: .claude/commands/tempdd.md")


def copy_templates_from_config(base_path: Path, config: dict, force: bool = False) -> None:
    """Copy template files based on configuration with new naming convention."""
    target_dir = base_path / ".tempdd" / "templates"
    source_dir = get_core_path() / "templates"

    print("Creating templates from configuration...")

    # Get templates from config
    templates = config.get("templates", {})

    for stage, template_name in templates.items():
        source_file = source_dir / f"{template_name}.md"
        target_file = target_dir / f"template_{stage}.md"

        # Skip if target exists and force is False
        if target_file.exists() and not force:
            print(f"Template template_{stage}.md already exists, skipping...")
            continue

        # Skip if source doesn't exist
        if not source_file.exists():
            print(f"Warning: Source template not found: {source_file}")
            continue

        # Copy template content directly
        content = source_file.read_text(encoding='utf-8')
        target_file.write_text(content, encoding='utf-8')
        print(f"Created template: .tempdd/templates/template_{stage}.md")


def init_command(force: bool = False, tool: str = "claudecode", language: str = "en", config_path: str = None) -> int:
    """Initialize a new TempDD project."""
    current_path = Path.cwd()

    print(f"Initializing TempDD project in: {current_path}")
    print(f"Using tool: {tool}")
    print(f"Language: {language}")
    if config_path:
        print(f"Config file: {config_path}")
    else:
        print("Using default configuration")

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
            print(f"Config file already exists at {target_config_path}, skipping...")
        else:
            with open(target_config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"Created config file: .tempdd/config.json")

        # 4. Copy templates with new naming convention (template_{stage}.md)
        copy_templates_from_config(current_path, config, force)

        # 5. Create tool integration
        create_tool_integration(current_path, tool, force)

        print("\n✓ TempDD project initialized successfully!")
        print("\nNext steps:")
        print("1. Customize templates in .tempdd/templates/")
        print("2. Use '/tempdd' command in Claude Code for integration")

        return 0

    except Exception as e:
        print(f"Failed to initialize project: {e}")
        return 1