"""File manager for TempDD integrations and templates."""

import shutil
import logging
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class IntegrationConfig:
    """Configuration for AI tool integrations."""

    name: str
    tool_dir: str
    commands_dir: str
    file_name: str
    file_extension: str


class FileManager:
    """Manages files for TempDD integrations and templates."""

    # Integration configurations for different AI tools
    INTEGRATION_CONFIGS = {
        "claude": IntegrationConfig(
            name="Claude Code",
            tool_dir=".claude",
            commands_dir="commands",
            file_name="tempdd",
            file_extension=".md",
        ),
        "gemini": IntegrationConfig(
            name="Gemini CLI",
            tool_dir=".gemini",
            commands_dir="commands",
            file_name="tempdd",
            file_extension=".toml",
        ),
        "cursor": IntegrationConfig(
            name="Cursor",
            tool_dir=".cursor",
            commands_dir="commands",
            file_name="tempdd",
            file_extension=".md",
        ),
        "copilot": IntegrationConfig(
            name="GitHub Copilot",
            tool_dir=".github",
            commands_dir="prompts",
            file_name="tempdd.prompt",
            file_extension=".md",
        ),
    }

    def __init__(self, base_path: Optional[Path] = None):
        """Initialize FileManager with base path."""
        self.base_path = base_path or Path.cwd()
        self.logger = logging.getLogger(__name__)

    def get_core_path(self) -> Path:
        """Get the core directory path."""
        return Path(__file__).parent / "core"

    def get_integrations_path(self) -> Path:
        """Get the integrations directory path."""
        return Path(__file__).parent / "integrations"

    def create_directory_structure(self, tool: str, force: bool = False) -> None:
        """Create directory structure for specified tool."""
        # Create basic template directory
        templates_dir = self.base_path / ".tempdd" / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        # Create tool-specific directory
        if tool in self.INTEGRATION_CONFIGS:
            config = self.INTEGRATION_CONFIGS[tool]
            tool_dir = self.base_path / config.tool_dir / config.commands_dir
            tool_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.logger.warning(f"Unknown tool: {tool}")

    def get_integration_file_path(self, tool: str) -> Optional[Path]:
        """Get the integration file path for a specific tool."""
        if tool not in self.INTEGRATION_CONFIGS:
            return None

        config = self.INTEGRATION_CONFIGS[tool]
        return (
            self.base_path
            / config.tool_dir
            / config.commands_dir
            / f"{config.file_name}{config.file_extension}"
        )

    def get_source_integration_path(self, tool: str) -> Optional[Path]:
        """Get the source integration file path from the integrations directory."""
        if tool not in self.INTEGRATION_CONFIGS:
            return None

        config = self.INTEGRATION_CONFIGS[tool]
        return (
            self.get_integrations_path()
            / tool
            / config.tool_dir
            / config.commands_dir
            / f"{config.file_name}{config.file_extension}"
        )

    def copy_integration_file(self, tool: str, force: bool = False) -> bool:
        """Copy integration file from source to target location."""
        if tool not in self.INTEGRATION_CONFIGS:
            self.logger.error(f"Unsupported tool: {tool}")
            return False

        source_path = self.get_source_integration_path(tool)
        target_path = self.get_integration_file_path(tool)

        if not source_path or not source_path.exists():
            self.logger.warning(
                f"Source integration file not found for '{tool}': {source_path}"
            )
            return False

        if target_path.exists() and not force:
            self.logger.info(
                f"{self.INTEGRATION_CONFIGS[tool].name} integration already exists, skipping..."
            )
            return False

        # Create target directory and copy file
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        self.logger.info(
            f"Created {self.INTEGRATION_CONFIGS[tool].name} integration: {target_path.relative_to(self.base_path)}"
        )
        return True

    def list_available_integrations(self) -> List[str]:
        """List all available integration tools."""
        return [
            tool
            for tool in self.INTEGRATION_CONFIGS.keys()
            if (source_path := self.get_source_integration_path(tool))
            and source_path.exists()
        ]

    def list_installed_integrations(self) -> List[str]:
        """List all installed integration tools."""
        return [
            tool
            for tool in self.INTEGRATION_CONFIGS.keys()
            if (file_path := self.get_integration_file_path(tool))
            and file_path.exists()
        ]

    def get_template_path(self, stage: str) -> Path:
        """Get the template file path for a specific stage."""
        return self.base_path / ".tempdd" / "templates" / f"template_{stage}.md"

    def get_project_config_path(self) -> Path:
        """Get the project configuration file path."""
        return self.base_path / ".tempdd" / "config.json"

    def get_default_config_path(self) -> Path:
        """Get the default configuration file path."""
        return self.get_core_path() / "configs" / "config_default.json"

    def get_config_path(self, config_name: str) -> Path:
        """Get configuration file path by name."""
        return (
            self.get_default_config_path()
            if config_name == "default"
            else self.get_core_path() / "configs" / f"config_{config_name}.json"
        )

    def copy_template_from_core(
        self, stage: str, template_name: str, force: bool = False
    ) -> bool:
        """Copy template from core to project templates directory."""
        source_file = self.get_core_path() / "templates" / f"{template_name}.md"
        target_file = self.get_template_path(stage)

        if target_file.exists() and not force:
            self.logger.info(
                f"Template template_{stage}.md already exists, skipping..."
            )
            return False

        if not source_file.exists():
            self.logger.warning(f"Source template not found: {source_file}")
            return False

        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
        self.logger.info(f"Created template: .tempdd/templates/template_{stage}.md")
        return True

    def copy_templates_from_config(self, config: dict, force: bool = False) -> None:
        """Copy template files based on configuration."""
        self.logger.info("Creating templates from configuration...")

        templates = config.get("templates", {})
        for stage, template_name in templates.items():
            self.copy_template_from_core(stage, template_name, force)
