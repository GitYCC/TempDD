
"""
TempDD Controller

Handles command processing, document management, and AI instruction generation.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional

from tempdd.utils import process_template
from tempdd.template_parser import parse_template, get_action_prompt, process_template_variables


class Controller:
    """
    TempDD Controller

    Responsible for:
    1. Configuration management
    2. Command processing and dispatching
    3. Document management
    4. AI instruction generation
    """

    # Constants
    DEFAULT_DOCS_DIR = "docs-for-works"
    DIR_NAME_PATTERN = r'^\d{3}_'
    INITIALIZATION_SUFFIX = "initialization"
    FEATURE_SUFFIX = "feature"

    # AI Instruction Templates
    FALLBACK_INSTRUCTION_TEMPLATE = """You are working on the {stage} stage with {action} action.

Language: {language}
Target Document: {target_document}

Please proceed with the {action} operation for {stage} stage.
Follow the guidelines and update the target document accordingly."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the controller

        Args:
            config_path: Optional custom configuration file path
        """
        self.config_path = config_path
        self.work_dir = Path.cwd()
        self.config = self._load_config()
        self._controller_state = self.config.get("controller_state", {})
        self._docs_dir: Optional[Path] = None

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration file"""
        # First try to load project config
        if self.config_path:
            config_file = Path(self.config_path)
        else:
            config_file = self.work_dir / ".tempdd" / "config.json"

        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        # Fallback to default config
        default_config_path = Path(__file__).parent.parent / "default_config.json"
        if default_config_path.exists():
            with open(default_config_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        raise FileNotFoundError("No configuration file found")

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
            FileNotFoundError: When template file does not exist
        """
        self._validate_stage_or_raise(stage)

        docs_dir = self._get_docs_directory()
        target_dir = self._get_target_directory(docs_dir, stage)
        target_document = str(target_dir / f"{stage}.md")

        template_path = self._get_template_path(stage)
        metadata, template_content = self._parse_template(template_path, stage)
        action_prompt = get_action_prompt(metadata, action)

        language_str = self.config.get("language", "en").upper()
        ai_instruction = self._generate_ai_instruction(stage, action, language_str, target_document, action_prompt)

        if action == 'build':
            self._save_target_document(target_document, template_content, target_dir)

        return ai_instruction

    def _validate_stage_or_raise(self, stage: str) -> None:
        """Validate stage or raise ValueError"""
        if not self._validate_stage(stage):
            raise ValueError(f"Invalid stage: {stage}")

    def _get_docs_directory(self) -> Path:
        """Get or create the docs directory"""
        if self._docs_dir is not None:
            return self._docs_dir

        docs_dir_str = self._controller_state.get("docs_dir")
        if docs_dir_str:
            self._docs_dir = Path(docs_dir_str)
        else:
            self._docs_dir = self.work_dir / self.DEFAULT_DOCS_DIR
            self._docs_dir.mkdir(exist_ok=True)
            self.update_controller_state(docs_dir=str(self._docs_dir))

        return self._docs_dir

    def _get_target_directory(self, docs_dir: Path, stage: str) -> Path:
        """Get or create target directory for the stage"""
        if stage == 'prd':
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
            self._get_existing_numbered_dirs(docs_dir),
            key=lambda d: d.name
        )

        if not existing_dirs:
            raise FileNotFoundError("No existing directories found. Please run 'prd' stage first.")

        return existing_dirs[-1]

    def _get_existing_numbered_dirs(self, docs_dir: Path) -> list[Path]:
        """Get all existing numbered directories"""
        return [
            d for d in docs_dir.iterdir()
            if d.is_dir() and re.match(self.DIR_NAME_PATTERN, d.name)
        ]

    def _get_template_path(self, stage: str) -> Path:
        """Get template file path for the stage"""
        template_path = self.work_dir / ".tempdd" / "templates" / f"template_{stage}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found for stage: {stage}")
        return template_path

    def _parse_template(self, template_path: Path, stage: str):
        """Parse template file and return metadata and content"""
        try:
            return parse_template(str(template_path))
        except (FileNotFoundError, ValueError) as e:
            raise FileNotFoundError(f"Failed to parse template for stage {stage}: {e}")

    def _save_target_document(self, target_document: str, template_content: str, target_dir: Path) -> None:
        """Save the target document with processed template content"""
        target_content = self._fill_in_template_content(template_content, target_dir)
        with open(target_document, 'w', encoding='utf-8') as f:
            f.write(target_content)

    def _fill_in_template_content(self, template_content, target_dir):
        context = {
            'PATH_PRD': str(target_dir / "prd.md"),
            'PATH_ARCH': str(target_dir / "arch.md"),
            'PATH_RESEARCH': str(target_dir / "research.md"),
            'PATH_BLUEPRINT': str(target_dir / "blueprint.md"),
        }
        processed_content = process_template(template_content, context)
        return processed_content

    def _template_exists(self, stage: str) -> bool:
        """Check if template exists for the given stage"""
        template_path = self.work_dir / ".tempdd" / "templates" / f"template_{stage}.md"
        return template_path.exists()

    def _generate_ai_instruction(self, stage: str, action: str, language: str, target_document: str, action_prompt: str = None) -> str:
        """Generate AI instruction string with template-based prompt"""
        if action_prompt:
            return self._create_template_based_instruction(action_prompt, language, target_document, stage, action)
        else:
            return self._create_fallback_instruction(stage, action, language, target_document)

    def _create_template_based_instruction(self, action_prompt: str, language: str, target_document: str, stage: str, action: str, system_prompt: str=None) -> str:
        """Create AI instruction content using template-defined prompt"""
        variables = {
            'TARGET_DOCUMENT': target_document,
            'STAGE': stage,
            'ACTION': action
        }

        if system_prompt is None:
            system_prompt = f"""
**Constitution**:
**RULE1:** You MUST use "{language}" as your preferred language for following conversation and documentation. However, use English for code (including comments) and web search queries.  
"""

        return process_template_variables(f'{system_prompt}\n\n===\n\n{action_prompt}', variables)

    def _create_fallback_instruction(self, stage: str, action: str, language: str, target_document: str) -> str:
        """Create fallback AI instruction content when no template prompt is available"""
        return self.FALLBACK_INSTRUCTION_TEMPLATE.format(
            stage=stage,
            action=action,
            language=language,
            target_document=target_document
        )

    def _validate_stage(self, stage: str) -> bool:
        """Validate if stage is valid"""
        stages = self.config.get("stages", [])
        return stage in stages

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config.copy()

    def update_controller_state(self, **kwargs) -> None:
        """Update controller state"""
        self._controller_state.update(kwargs)
        self.config["controller_state"] = self._controller_state
        self._save_config()

    def _save_config(self) -> None:
        """Save configuration to file"""
        config_file = self.work_dir / ".tempdd" / "config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
