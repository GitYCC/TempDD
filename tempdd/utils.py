"""Common utilities for TempDD handlers."""

import json
from pathlib import Path
from typing import Tuple


def load_config() -> dict:
    """Load the TempDD configuration file."""
    config_path = Path.cwd() / ".tempdd" / "config.json"

    if not config_path.exists():
        raise FileNotFoundError(f"TempDD configuration not found: {config_path}. Please run 'tempdd init' first.")

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_stage(stage: str, config: dict) -> Tuple[bool, str]:
    """
    Validate if a stage exists in the configuration.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Check if stage exists in stages list or flow configuration
    stages = config.get("stages", [])
    flow = config.get("flow", {})

    if stage in stages or stage in flow:
        return True, ""
    else:
        return False, f"Stage '{stage}' not found in configuration"




def process_template(template_content: str, context: dict) -> str:
    """Process template with context variables."""
    processed_content = template_content

    # Replace template variables
    for key, value in context.items():
        placeholder = f"{{{{{key}}}}}"
        processed_content = processed_content.replace(placeholder, str(value))

    return processed_content