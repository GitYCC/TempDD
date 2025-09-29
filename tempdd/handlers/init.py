"""Init command implementation."""

from pathlib import Path
import json
import yaml
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

    for config_file in configs_dir.glob("config_*.yaml"):
        config_name = config_file.stem.replace("config_", "")
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)
            config_files.append((config_name, config_data))
        except (yaml.YAMLError, FileNotFoundError):
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


def update_config_template_paths(config: dict) -> dict:
    """Update config template paths to point to local templates directory."""
    import copy
    updated_config = copy.deepcopy(config)

    if "define" in updated_config:
        for stage_name, stage_config in updated_config["define"].items():
            if "template" in stage_config:
                # Update template path to point to local templates
                updated_config["define"][stage_name]["template"] = f"templates/{stage_name}.md"

    return updated_config


def copy_workflow_templates(file_manager: FileManager, config: dict, templates_dir: Path, force: bool) -> None:
    """Copy templates from core templates to workflow templates directory."""
    logger = logging.getLogger(__name__)
    define_section = config.get("define", {})

    for stage_name, stage_config in define_section.items():
        template_name = stage_config.get("template")
        if not template_name:
            continue

        # Source template path (from core templates)
        source_template = file_manager.get_core_path() / "templates" / f"{template_name}.md"

        # Target template path (stage name)
        target_template = templates_dir / f"{stage_name}.md"

        if not source_template.exists():
            logger.warning(f"Template not found: {source_template}")
            continue

        if target_template.exists() and not force:
            logger.info(f"Template already exists: {target_template}, skipping...")
            continue

        # Copy template content
        with open(source_template, "r", encoding="utf-8") as src:
            template_content = src.read()

        with open(target_template, "w", encoding="utf-8") as dst:
            dst.write(template_content)

        logger.info(f"Copied template: {stage_name}.md")


def show_success_summary(config_type: str, config_path: str, tool: str, language: str, config: dict) -> None:
    """Show success summary with configuration details and next steps."""
    # Get stages from config
    stages = config.get("stages", [])
    stages_text = ", ".join(stages) if stages else "None"

    # Determine configuration display text
    if config_type == "workflow":
        config_display = "Customized configuration located in .tempdd/workflow/"
    else:
        config_display = config_path

    if HAS_RICH and console:
        console.print("\n[bold green]✓ TempDD project initialized successfully![/bold green]")

        # Show configuration summary
        from rich.panel import Panel

        config_summary = f"Configuration: [cyan]{config_display}[/cyan]\nPlatform: [cyan]{tool}[/cyan]\nLanguage: [cyan]{language}[/cyan]\nStages: [cyan]{stages_text}[/cyan]"
        summary_panel = Panel(
            config_summary,
            title="[bold]Project Configuration[/bold]",
            border_style="blue",
            padding=(1, 2)
        )
        console.print(summary_panel)

        # Create next steps panel
        steps_lines = _get_next_steps_for_tool(tool)
        if steps_lines:
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
        print(f"Configuration: {config_display}")
        print(f"Platform: {tool}")
        print(f"Language: {language}")
        print(f"Stages: {stages_text}")

        print(COLOR_YELLOW + "\nNext steps:" + COLOR_END)
        _print_next_steps_for_tool(tool)


def _get_next_steps_for_tool(tool: str) -> list[str]:
    """Get next steps instructions for a specific tool (Rich format)."""
    file_manager = FileManager()
    integration_config = file_manager.INTEGRATION_CONFIGS.get(tool)
    if not integration_config:
        return []

    steps_lines = ["1. Use [cyan]tempdd help[/cyan] to learn how to use the current flow first."]

    if tool == "claude":
        steps_lines.extend([
            "2. Execute [cyan]claude[/cyan] to start Claude Code",
            "3. Use [cyan]/tempdd-go <stage> <action>[/cyan] to start running the workflow"
        ])
    elif tool == "gemini":
        steps_lines.extend([
            "2. Execute [cyan]gemini[/cyan] to start Gemini CLI",
            "3. Use [cyan]/tempdd-go <stage> <action>[/cyan] to start running the workflow"
        ])
    elif tool == "cursor":
        steps_lines.extend([
            "2. Execute [cyan]cursor .[/cyan] to start Cursor",
            "3. Use [cyan]/tempdd-go <stage> <action>[/cyan] to start running the workflow"
        ])
    elif tool == "copilot":
        steps_lines.extend([
            "2. Open project in your IDE with GitHub Copilot installed",
            "3. Use [cyan]#tempdd-go <stage> <action>[/cyan] to start running the workflow"
        ])

    return steps_lines


def _print_next_steps_for_tool(tool: str) -> None:
    """Print next steps instructions for a specific tool (plain text format)."""
    file_manager = FileManager()
    integration_config = file_manager.INTEGRATION_CONFIGS.get(tool)
    if not integration_config:
        return

    if tool == "claude":
        print(COLOR_YELLOW + "1. Execute `claude` to start Claude Code" + COLOR_END)
        print(COLOR_YELLOW + "2. Use '/tempdd-go help' command in Claude Code to learn how to use the current flow." + COLOR_END)
    elif tool == "gemini":
        print(COLOR_YELLOW + "1. Execute `gemini` to start Gemini CLI" + COLOR_END)
        print(COLOR_YELLOW + "2. Use '/tempdd-go help' command in Gemini CLI to learn how to use the current flow." + COLOR_END)
    elif tool == "cursor":
        print(COLOR_YELLOW + "1. Execute `cursor .` to start Cursor" + COLOR_END)
        print(COLOR_YELLOW + "2. Use 'Ctrl+K' then '/tempdd-go help' to learn how to use the current flow." + COLOR_END)
    elif tool == "copilot":
        print(COLOR_YELLOW + "1. Open project in your IDE with GitHub Copilot installed" + COLOR_END)
        print(COLOR_YELLOW + "2. Use '#tempdd-go help' in your prompt to learn how to use the current flow." + COLOR_END)


def copy_workflow_directory(source_workflow_path: str, target_workflow_dir: Path, force: bool = False) -> bool:
    """Copy entire workflow directory from source to target."""
    import shutil
    logger = logging.getLogger(__name__)

    source_path = Path(source_workflow_path)
    if not source_path.exists():
        raise FileNotFoundError(f"Workflow path not found: {source_workflow_path}")

    if not source_path.is_dir():
        raise ValueError(f"Workflow path is not a directory: {source_workflow_path}")

    # Check if source contains config.yaml
    config_file = source_path / "config.yaml"
    if not config_file.exists():
        raise FileNotFoundError(f"config.yaml not found in workflow directory: {source_workflow_path}")

    # Check if target already exists
    if target_workflow_dir.exists():
        if not force:
            return False  # Don't copy, target already exists
        else:
            shutil.rmtree(target_workflow_dir)
            logger.info(f"Removed existing workflow directory: {target_workflow_dir}")

    # Copy the entire directory
    shutil.copytree(source_path, target_workflow_dir)
    logger.info(f"Copied workflow from {source_workflow_path} to {target_workflow_dir}")

    return True


def load_default_or_custom_config(config_path: str = None) -> dict:
    """Load configuration file, using default if not specified."""
    file_manager = FileManager()

    if config_path:
        if "/" in config_path:
            # It's a file path - must have .yaml extension
            if not config_path.endswith(".yaml"):
                raise ValueError(
                    f"Config file path must have .yaml extension: {config_path}"
                )
            config_file = Path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
        elif config_path.endswith(".yaml"):
            # It's a .yaml file in current directory
            config_file = Path(config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {config_path}")
        else:
            # Use as config name from configs directory
            config_file = file_manager.get_core_path() / "configs" / f"config_{config_path}.yaml"
            if not config_file.exists():
                raise FileNotFoundError(f"Config file not found: {config_file}")
    else:
        # Use default config
        config_file = file_manager.get_core_path() / "configs" / "config_default.yaml"
        if not config_file.exists():
            raise FileNotFoundError(f"Default config file not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def init_command(
    force: bool = False,
    workflow_path: str = None,
    interactive: bool = True,
) -> int:
    """Initialize a new TempDD project."""
    logger = logging.getLogger(__name__)
    current_path = Path.cwd()

    # Show banner if interactive
    if interactive:
        show_banner()

    logger.info(f"Initializing TempDD project in: {current_path}")

    # Check if workflow_path is provided (direct workflow copy mode)
    if workflow_path:
        return init_with_workflow_copy(current_path, workflow_path, force)

    # Interactive mode - existing logic with tool and language prompts
    return init_with_interactive_mode(current_path, force)


def init_with_workflow_copy(current_path: Path, workflow_path: str, force: bool) -> int:
    """Initialize project by copying an existing workflow directory."""
    logger = logging.getLogger(__name__)
    target_workflow_dir = current_path / ".tempdd" / "workflow"

    try:
        # Copy workflow directory
        copied = copy_workflow_directory(workflow_path, target_workflow_dir, force)
        if not copied:
            logger.error(f"Workflow already exists at {target_workflow_dir}. Use --force to overwrite.")
            return 1

        # Create .tempdd directory
        tempdd_dir = current_path / ".tempdd"
        tempdd_dir.mkdir(exist_ok=True)

        # Load config from copied workflow to get language
        config_path = target_workflow_dir / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Get language from workflow config
        language = config.get("language", "en")

        # Interactive tool selection
        tool = prompt_platform_selection()
        if tool is None:  # User cancelled
            return 1

        logger.info(f"Using tool: {tool}")
        logger.info(f"Language: {language} (from workflow)")

        # Create tool integration
        file_manager = FileManager(current_path)
        file_manager.copy_integration_file(tool, force)

        # Show complete configuration summary using shared function
        show_success_summary("workflow", "", tool, language, config)

        return 0

    except Exception as e:
        logger.error(f"Failed to initialize project with workflow: {e}")
        return 1


def init_with_interactive_mode(current_path: Path, force: bool) -> int:
    """Initialize project with interactive mode (existing logic)."""
    logger = logging.getLogger(__name__)
    interactive = True  # This is always interactive mode

    # Check if project is already initialized
    if is_project_initialized(current_path):
        if force:
            # Force flag provided, proceed without asking
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

            should_continue = ask_user_confirmation(message, default=False)
            if not should_continue:
                if HAS_RICH and console:
                    console.print("[blue]Initialization cancelled.[/blue]")
                else:
                    print("Initialization cancelled.")
                return 0

    # Interactive prompts for config, tool, and language selection
    config_path = prompt_config_selection()
    if config_path is None:  # User cancelled
        return 1

    tool = prompt_platform_selection()
    if tool is None:  # User cancelled
        return 1

    language = prompt_language_input()
    if language is None:  # User cancelled
        return 1

    logger.info(f"Using tool: {tool}")
    logger.info(f"Language: {language}")
    logger.info(f"Config: {config_path}")

    try:
        # 1. Load configuration first
        config = load_default_or_custom_config(config_path)

        # 2. Create basic directory structure and initialize project
        file_manager = FileManager(current_path)
        file_manager.create_directory_structure(tool, force)

        # 3. Create workflow directory structure
        workflow_dir = current_path / ".tempdd" / "workflow"
        templates_dir = workflow_dir / "templates"

        workflow_dir.mkdir(exist_ok=True)
        templates_dir.mkdir(exist_ok=True)
        logger.info(f"Created workflow directory structure")

        # 4. Copy templates to ./.tempdd/workflow/templates/ with stage names first
        copy_workflow_templates(file_manager, config, templates_dir, force)

        # 5. Update config template paths to point to local templates and write config
        updated_config = update_config_template_paths(config)
        # Update language setting from user selection
        updated_config["language"] = language
        workflow_config_path = workflow_dir / "config.yaml"
        if workflow_config_path.exists() and not force:
            logger.info(
                f"Workflow config already exists at {workflow_config_path}, skipping..."
            )
        else:
            with open(workflow_config_path, "w", encoding="utf-8") as f:
                yaml.dump(updated_config, f, default_flow_style=False, indent=2, allow_unicode=True, sort_keys=False)
            logger.info(f"Created workflow config: .tempdd/workflow/config.yaml")

        # 6. Create tool integration
        file_manager.copy_integration_file(tool, force)

        # Show success message using shared function
        show_success_summary("config", config_path, tool, language, updated_config)
        return 0

    except Exception as e:
        logger.error(f"Failed to initialize project: {e}")
        return 1
