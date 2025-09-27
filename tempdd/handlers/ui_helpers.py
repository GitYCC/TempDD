"""UI helper functions for interactive terminal interfaces."""

import sys
import shutil
from pathlib import Path

# Check if required packages are available
try:
    import readchar
    HAS_READCHAR = True
except ImportError:
    HAS_READCHAR = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.live import Live
    from rich.align import Align
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

console = Console() if HAS_RICH else None


# TempDD ASCII Art Banner
BANNER = """

████████╗███████╗███╗   ███╗██████╗ ██████╗ ██████╗
╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██╔══██╗██╔══██╗
   ██║   █████╗  ██╔████╔██║██████╔╝██║  ██║██║  ██║
   ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║  ██║██║  ██║
   ██║   ███████╗██║ ╚═╝ ██║██║     ██████╔╝██████╔╝
   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚═════╝ ╚═════╝
"""

TAGLINE = "Template-Driven Development Framework for AI-Augmented Coding"


def show_banner():
    """Display the TempDD ASCII art banner with Rich styling"""
    if HAS_RICH and console:
        # Create gradient effect with different colors
        banner_lines = BANNER.split('\n')
        colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

        styled_banner = Text()
        for i, line in enumerate(banner_lines):
            color = colors[i % len(colors)]
            styled_banner.append(line + "\n", style=color)

        console.print(Align.center(styled_banner))
        console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
        console.print()
    else:
        # Basic banner without Rich
        print(BANNER)
        print(f"{TAGLINE}")
        print()


def select_with_arrows(options: dict, prompt: str, default_key: str = None) -> str:
    """Interactive selection using arrow keys with Rich styling

    Args:
        options: Dictionary of {key: description} format options
        prompt: Prompt text to display
        default_key: Default option key

    Returns:
        Selected option key, or None if cancelled
    """
    if not HAS_READCHAR:
        raise ImportError("readchar package is required for interactive selection")

    if not HAS_RICH:
        # Fallback to basic implementation if Rich not available
        return _basic_select_with_arrows(options, prompt, default_key)

    option_keys = list(options.keys())
    if not option_keys:
        return None

    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    def create_selection_panel():
        """Create Rich selection panel"""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        # Handle multi-line prompts
        prompt_lines = prompt.split('\n')
        title_line = prompt_lines[0]

        # Add prompt message lines (except first line which becomes title)
        if len(prompt_lines) > 1:
            table.add_row("", "")
            for line in prompt_lines[1:]:
                if line.strip():  # Skip empty lines
                    table.add_row("", f"[white]{line}[/white]")
            table.add_row("", "")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")

        return Panel(
            table,
            title=f"[bold]{title_line}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )

    selected_key = None

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = readchar.readkey()
                    if key == readchar.key.UP:
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == readchar.key.DOWN:
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == readchar.key.ENTER:
                        selected_key = option_keys[selected_index]
                        break
                    elif key == readchar.key.ESC:
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        selected_key = None
                        break
                    elif key == readchar.key.CTRL_C:
                        raise KeyboardInterrupt

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[red]User interrupted[/red]")
                    sys.exit(0)

    run_selection_loop()
    return selected_key


def _basic_select_with_arrows(options: dict, prompt: str, default_key: str = None) -> str:
    """Basic arrow selection without Rich styling (fallback)"""
    option_keys = list(options.keys())
    if not option_keys:
        return None

    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    def render_menu():
        """Render the basic selection menu"""
        print(f"\n{prompt}")
        for i, key in enumerate(option_keys):
            marker = "▶" if i == selected_index else " "
            print(f"{marker} {key}: {options[key]}")
        print("\n↑/↓: Navigate, Enter: Select, Esc: Cancel")

    while True:
        # Clear screen and re-render
        print("\033[2J\033[H", end="")  # Clear screen
        render_menu()

        try:
            key = readchar.readkey()

            # Handle arrow keys
            if key == readchar.key.UP:
                selected_index = (selected_index - 1) % len(option_keys)
            elif key == readchar.key.DOWN:
                selected_index = (selected_index + 1) % len(option_keys)
            elif key == readchar.key.ENTER:
                return option_keys[selected_index]
            elif key == readchar.key.ESC:
                return None
            elif key == readchar.key.CTRL_C:
                raise KeyboardInterrupt

        except KeyboardInterrupt:
            print("\n\n\033[91mUser interrupted.\033[0m")
            sys.exit(0)


def is_project_initialized(project_path: Path) -> bool:
    """Check if TempDD project is already initialized

    Args:
        project_path: Path to check for initialization

    Returns:
        True if project is already initialized, False otherwise
    """
    tempdd_dir = project_path / ".tempdd"
    config_file = tempdd_dir / "config.json"

    return tempdd_dir.exists() and config_file.exists()


def ask_user_confirmation(message: str, default: bool = False) -> bool:
    """Ask user for confirmation using arrow key selection

    Args:
        message: Confirmation message to display
        default: Default response if user just presses Enter

    Returns:
        True if user confirms, False otherwise
    """
    # Create options for Yes/No selection
    if default:
        options = {"yes": "Continue and reinitialize", "no": "Cancel operation"}
        default_key = "yes"
    else:
        options = {"no": "Cancel operation", "yes": "Continue and reinitialize"}
        default_key = "no"

    # Use the existing selection UI with separate title and message
    selected = select_with_arrows(options, f"Confirmation Required\n\n{message}", default_key)

    if selected is None:  # User cancelled (Esc or Ctrl+C)
        return False

    return selected == "yes"


def check_tool_installed(tool: str) -> bool:
    """Check if a tool is installed

    Args:
        tool: Tool name to check

    Returns:
        True if tool is installed, False otherwise
    """
    # Special handling for Claude Code installation path
    if tool == "claude":
        claude_local_path = Path.home() / ".claude" / "local" / "claude"
        if claude_local_path.exists() and claude_local_path.is_file():
            return True

    # General tool check
    return shutil.which(tool) is not None


def fallback_number_selection(options: dict, prompt: str, default_key: str = None) -> str:
    """Fallback number selection mode with Rich styling (when readchar is not available)

    Args:
        options: Dictionary of {key: description} format options
        prompt: Prompt text to display
        default_key: Default option key

    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if not option_keys:
        return None

    if HAS_RICH and console:
        # Create Rich styled fallback menu
        table = Table.grid(padding=(0, 1))
        table.add_column(style="cyan", justify="left", width=4)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys, 1):
            marker = " [green](default)[/green]" if key == default_key else ""
            table.add_row(f"{i}.", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]{marker}")

        panel = Panel(
            table,
            title=f"[bold]{prompt}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )
        console.print(panel)

        instructions = "[dim]Enter choice number (press Enter for default):[/dim]"
        console.print(instructions)
    else:
        # Basic fallback without Rich
        print(f"\n{prompt}")
        for i, key in enumerate(option_keys, 1):
            marker = " (default)" if key == default_key else ""
            print(f"{i}. {key}: {options[key]}{marker}")

    while True:
        try:
            if len(option_keys) == 1:
                choice = input("Choice (1): ").strip()
            else:
                choice = input(f"Choice (1-{len(option_keys)}): ").strip()

            if not choice:
                # If default_key exists, return it; otherwise return first option
                return default_key if default_key in option_keys else option_keys[0]

            choice_num = int(choice)
            if 1 <= choice_num <= len(option_keys):
                return option_keys[choice_num - 1]
            else:
                if HAS_RICH and console:
                    console.print(f"[red]Please enter a number between 1 and {len(option_keys)}[/red]")
                else:
                    print(f"Please enter a number between 1 and {len(option_keys)}")

        except ValueError:
            if HAS_RICH and console:
                console.print("[red]Please enter a valid number[/red]")
            else:
                print("Please enter a valid number")
        except KeyboardInterrupt:
            if HAS_RICH and console:
                console.print("\n[red]User interrupted.[/red]")
            else:
                print("\n\033[91mUser interrupted.\033[0m")
            sys.exit(0)