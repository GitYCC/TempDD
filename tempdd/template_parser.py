"""
Template Parser for TempDD

Handles parsing of template files with YAML frontmatter containing action-specific prompts.
Supports the new simplified format where actions (build, continue, run) directly contain prompt fields.
"""

import yaml
import re
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


def parse_template(template_path: str) -> Tuple[Dict[str, Any], str]:
    """
    Parse template file with YAML frontmatter

    Expected format:
    ---
    build:
      prompt: |
        Build instructions...
    continue:
      prompt: |
        Continue instructions...
    run:
      prompt: |
        Run instructions...
    ---

    # Template Content
    ...

    Args:
        template_path: Path to the template file

    Returns:
        Tuple[Dict[str, Any], str]: (metadata, template_content)

    Raises:
        FileNotFoundError: When template file does not exist
        ValueError: When template format is invalid
    """
    template_file = Path(template_path)

    if not template_file.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if content starts with YAML frontmatter
    if not content.startswith('---\n'):
        # No frontmatter, return empty metadata
        return {}, content

    # Split frontmatter and content
    try:
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            # Invalid frontmatter format
            return {}, content

        frontmatter_raw = parts[1]
        template_content = parts[2]

        # Parse YAML frontmatter
        metadata = yaml.safe_load(frontmatter_raw) or {}

        return metadata, template_content

    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter in template {template_path}: {e}")


def get_action_prompt(metadata: Dict[str, Any], action: str) -> Optional[str]:
    """
    Extract prompt for specific action from metadata

    Args:
        metadata: Parsed template metadata
        action: Action name (build, continue, run, etc.)

    Returns:
        Optional[str]: Action-specific prompt or None if not found
    """
    if not isinstance(metadata, dict):
        return None

    action_data = metadata.get(action, {})
    if isinstance(action_data, dict):
        return action_data.get('prompt')

    return None


def process_template_variables(content: str, variables: Dict[str, str]) -> str:
    """
    Replace template variables in content

    Variables are in the format {{VARIABLE_NAME}}

    Args:
        content: Content with template variables
        variables: Dictionary mapping variable names to values

    Returns:
        str: Content with variables replaced
    """
    processed_content = content

    for var_name, var_value in variables.items():
        placeholder = f"{{{{{var_name}}}}}"
        processed_content = processed_content.replace(placeholder, str(var_value))

    # Check for remaining unreplaced variables and log warnings
    remaining_vars = re.findall(r'\{\{([^}]+)\}\}', processed_content)
    if remaining_vars:
        logger = logging.getLogger(__name__)
        for var in remaining_vars:
            logger.warning(f"Template variable '{{{{%s}}}}' was not replaced. Variable not found in provided variables.", var)

    return processed_content


def validate_template_metadata(metadata: Dict[str, Any]) -> bool:
    """
    Validate template metadata structure

    Args:
        metadata: Parsed template metadata

    Returns:
        bool: True if metadata is valid, False otherwise
    """
    if not isinstance(metadata, dict):
        return False

    # Check if at least one valid action exists
    valid_actions = ['build', 'continue', 'run']

    for action in valid_actions:
        if action in metadata:
            action_data = metadata[action]
            if isinstance(action_data, dict) and 'prompt' in action_data:
                return True

    return len(metadata) == 0  # Empty metadata is also valid