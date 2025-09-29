"""
TempDD Unified Controller

Unified controller for handling all TempDD workflow configurations.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any, Optional

from tempdd.utils import process_template
from tempdd.template_parser import (
    parse_template,
    get_action_prompt,
    process_template_variables,
)
from tempdd.file_manager import FileManager


class Controller:
    """
    Unified TempDD Controller

    Handles workflow configurations with YAML-based config files and unified template processing.
    """

    # Constants
    DEFAULT_DOCS_DIR = "docs-for-works"
    DIR_NAME_PATTERN = r"^\d{3}_"
    INITIALIZATION_SUFFIX = "initialization"
    FEATURE_SUFFIX = "feature"

    # AI Instruction Templates
    FALLBACK_INSTRUCTION_TEMPLATE = """You are working on the {stage} stage with {action} action.

Language: {language}
Target Document: {target_document}

Please proceed with the {action} operation for {stage} stage.
Follow the guidelines and update the target document accordingly."""

    SYSTEM_PROMPT_TEMPLATE = """
**Global Rules**:
**RULE1:** You MUST use "{language}" as your preferred language for following conversation and documentation. However, use English for code (including comments) and web search queries.
"""

    HELP_CONTENT_TEMPLATE = """{system_prompt}

== TempDD Workflow ==

**Language:** {language}
**Available Stages:** {stages}

**How to run this workflow?**
{help_content}
"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the controller

        Args:
            config_path: Optional custom configuration file path
        """
        self.config_path = config_path
        self.work_dir = Path.cwd()
        self.config = self._load_config()
        self._docs_dir: Optional[Path] = None

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration file"""
        if self.config_path:
            config_file = Path(self.config_path)
        else:
            # Only load from project workflow config - no fallback
            workflow_config = self.work_dir / ".tempdd" / "workflow" / "config.yaml"
            if not workflow_config.exists():
                raise FileNotFoundError(
                    f"Workflow configuration not found: {workflow_config}. "
                    f"Please run 'tempdd init' to set up the project workflow properly."
                )
            config_file = workflow_config

        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def process_command(self, stage: str, action: str = "build") -> str:
        """
        Process command and return AI instruction

        Args:
            stage: Stage name (prd, arch, research, blueprint, task)
            action: Action type (build, run, etc.)

        Returns:
            AI execution instruction string

        Raises:
            ValueError: When stage or action is invalid
        """
        # Validate stage
        stages = self.config.get("stages", [])
        if stage not in stages:
            raise ValueError(f"Invalid stage '{stage}'. Available stages: {', '.join(stages)}")

        # Get stage configuration
        define_section = self.config.get("define", {})
        stage_config = define_section.get(stage)
        if not stage_config:
            raise ValueError(f"No configuration found for stage '{stage}'")

        # Load template
        template_name = stage_config.get("template")
        if not template_name:
            raise ValueError(f"No template specified for stage '{stage}'")

        # Only use workflow configuration - no fallback to core
        workflow_template_path = self.work_dir / ".tempdd" / "workflow" / "templates" / f"{stage}.md"
        if not workflow_template_path.exists():
            raise FileNotFoundError(
                f"Workflow template not found: {workflow_template_path}. "
                f"Please run 'tempdd init' to set up the project workflow properly."
            )

        template_path = workflow_template_path

        # Parse template and get action prompt
        template_data, template_content = parse_template(str(template_path))

        action_prompt = get_action_prompt(template_data, action)
        if not action_prompt:
            # Use fallback instruction
            return self._generate_fallback_instruction(stage, action)

        # Get target document path
        docs_dir = self._get_docs_dir()
        target_document = self._get_target_document_path(docs_dir, stage)

        # Process template variables
        input_symbols = stage_config.get("input_symbols", []) or []
        symbol_values = self._resolve_symbols(input_symbols, docs_dir)

        # Add TARGET_DOCUMENT symbol
        symbol_values["TARGET_DOCUMENT"] = str(target_document)

        # Process the prompt with symbols and add system prompt
        processed_prompt = self._create_template_based_instruction(
            action_prompt, symbol_values, str(target_document), stage, action
        )

        # Save target document if action is build
        if action == "build":
            self._save_target_document(str(target_document), template_content, target_document.parent)

        return processed_prompt

    def get_help_content(self) -> str:
        """
        Generate help content for the current configuration

        Returns:
            Formatted help content string
        """
        language = self.config.get("language", "en")
        stages = self.config.get("stages", [])
        stages_text = ", ".join(stages)

        # Get help content from config
        help_content = self.config.get("help", "")

        # Generate system prompt
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(language=language)

        return self.HELP_CONTENT_TEMPLATE.format(
            system_prompt=system_prompt,
            language=language,
            stages=stages_text,
            help_content=help_content
        )

    def _generate_fallback_instruction(self, stage: str, action: str) -> str:
        """Generate fallback instruction when template action is not found"""
        language = self.config.get("language", "en")
        docs_dir = self._get_docs_dir()
        target_document = self._get_target_document_path(docs_dir, stage)

        return self.FALLBACK_INSTRUCTION_TEMPLATE.format(
            stage=stage,
            action=action,
            language=language,
            target_document=target_document
        )

    def _create_template_based_instruction(
        self,
        action_prompt: str,
        symbol_values: Dict[str, str],
        target_document: str,
        stage: str,
        action: str
    ) -> str:
        """Create AI instruction content using template-defined prompt with system prompt"""
        language = self.config.get("language", "en")
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(language=language)

        # Process the action prompt with symbols
        processed_action_prompt = process_template_variables(action_prompt, symbol_values)

        # Combine system prompt and action prompt
        return f"{system_prompt}\n\n===\n\n{processed_action_prompt}"

    def _get_docs_dir(self) -> Path:
        """Get or create docs directory"""
        if self._docs_dir is not None:
            return self._docs_dir

        docs_dir = self.work_dir / self.DEFAULT_DOCS_DIR
        docs_dir.mkdir(exist_ok=True)
        self._docs_dir = docs_dir
        return docs_dir

    def _get_target_document_path(self, docs_dir: Path, stage: str) -> Path:
        """Get target document path for a stage"""
        target_dir = self._get_target_directory(docs_dir, stage)
        return target_dir / f"{stage}.md"

    def _get_target_directory(self, docs_dir: Path, stage: str) -> Path:
        """Get or create target directory for the stage"""
        if stage == "prd":
            return self._create_prd_directory(docs_dir)
        else:
            return self._get_latest_directory(docs_dir)

    def _create_prd_directory(self, docs_dir: Path) -> Path:
        """Create a new directory for PRD stage"""
        existing_dirs = self._get_existing_numbered_dirs(docs_dir)
        index = len(existing_dirs) + 1
        index_str = f"{index:03d}"

        if not existing_dirs:
            folder_name = f"{index_str}_{self.INITIALIZATION_SUFFIX}"
        else:
            folder_name = f"{index_str}_{self.FEATURE_SUFFIX}"

        target_dir = docs_dir / folder_name
        target_dir.mkdir(exist_ok=True)
        return target_dir

    def _get_latest_directory(self, docs_dir: Path) -> Path:
        """Get the most recent numbered directory"""
        existing_dirs = sorted(
            self._get_existing_numbered_dirs(docs_dir), key=lambda d: d.name
        )

        if not existing_dirs:
            raise FileNotFoundError(
                "No existing directories found. Please run 'prd' stage first."
            )

        return existing_dirs[-1]

    def _get_existing_numbered_dirs(self, docs_dir: Path) -> list[Path]:
        """Get all existing numbered directories"""
        return [
            d
            for d in docs_dir.iterdir()
            if d.is_dir() and re.match(self.DIR_NAME_PATTERN, d.name)
        ]

    def _resolve_symbols(self, symbols: list, docs_dir: Path) -> Dict[str, str]:
        """Resolve symbol values from previous stage outputs"""
        symbol_values = {}

        for symbol in symbols:
            if symbol.startswith("PATH_"):
                # Extract stage name from symbol (e.g., PATH_PRD -> prd)
                stage_name = symbol.replace("PATH_", "").lower()
                stage_file = docs_dir / f"{stage_name}.md"
                symbol_values[symbol] = str(stage_file)
            else:
                # Handle other symbol types if needed
                symbol_values[symbol] = str(docs_dir / f"{symbol.lower()}.md")

        return symbol_values

    def _save_target_document(self, target_document: str, template_content: str, target_dir: Path) -> None:
        """Save the target document with processed template content"""
        target_content = self._fill_in_template_content(template_content, target_dir)
        with open(target_document, "w", encoding="utf-8") as f:
            f.write(target_content)

    def _fill_in_template_content(self, template_content: str, target_dir: Path) -> str:
        """Fill in template content with context variables"""
        context = {
            "PATH_PRD": str(target_dir / "prd.md"),
            "PATH_ARCH": str(target_dir / "arch.md"),
            "PATH_RESEARCH": str(target_dir / "research.md"),
            "PATH_BLUEPRINT": str(target_dir / "blueprint.md"),
        }
        processed_content = process_template(template_content, context)
        return processed_content