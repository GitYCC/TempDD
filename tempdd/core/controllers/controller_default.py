
"""
TempDD Controller

Handles command processing, document management, and AI instruction generation.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional

from tempdd.utils import process_template
from tempdd.template_parser import parse_template, get_action_prompt


class Controller:
    """
    TempDD Controller

    Responsible for:
    1. Configuration management
    2. Command processing and dispatching
    3. Document management
    4. AI instruction generation
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
        self._controller_state = self.config.get("controller_state", {})

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
            action: Action type (build, continue, run, etc.)

        Returns:
            AI execution instruction string

        Raises:
            ValueError: When stage or action is invalid
            FileNotFoundError: When template file does not exist
        """
        # Validate stage
        if not self._validate_stage(stage):
            raise ValueError(f"Invalid stage: {stage}")

        # 1. Get work directory from controller state
        docs_dir = Path(self._controller_state["docs_dir"]) if 'docs_dir' in self._controller_state else None
        if docs_dir is None:
            docs_dir = self.work_dir / "docs-for-works"
            docs_dir.mkdir(exist_ok=True)
            self.update_controller_state(docs_dir=str(docs_dir))

        # 2. Implement directory creation/selection logic
        if stage == 'prd':
            existing_dirs = [
                d for d in docs_dir.iterdir()
                if d.is_dir() and re.match(r'^\d{3}_', d.name)
            ]
            index = len(existing_dirs) + 1
            index_str = f"{index:03d}"

            if not existing_dirs:
                folder_name = f"{index_str}_initialization"
            else:
                folder_name = f"{index_str}_feature"

            target_dir = docs_dir / folder_name
            target_dir.mkdir(exist_ok=True)
        else:
            # For other stages, use the most recent directory
            existing_dirs = sorted([
                d for d in docs_dir.iterdir()
                if d.is_dir() and re.match(r'^\d{3}_', d.name)
            ], key=lambda d: d.name)

            if not existing_dirs:
                raise FileNotFoundError("No existing directories found. Please run 'prd' stage first.")

            target_dir = existing_dirs[-1]

        # 3. Define target file path
        target_document = str(target_dir / f"{stage}.md")

        # 4. Get template path and parse it
        template_path = self.work_dir / ".tempdd" / "templates" / f"template_{stage}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found for stage: {stage}")

        # 5. Parse template to get action-specific prompt
        try:
            metadata, template_content = parse_template(str(template_path))
            action_prompt = get_action_prompt(metadata, action)
        except (FileNotFoundError, ValueError) as e:
            raise FileNotFoundError(f"Failed to parse template for stage {stage}: {e}")
        
        # 6. Generate AI instruction
        language_str = self.config.get("language", "en").upper()
        ai_instruction = self._generate_ai_instruction(stage, action, language_str, target_document, action_prompt)

        # 7. Save target document
        if action == 'build':
            target_content = self._fill_in_template_content(template_content, target_dir, language_str)

            with open(target_document, 'w', encoding='utf-8') as f:
                f.write(target_content)

        return ai_instruction

    def _fill_in_template_content(self, template_content, target_dir, language):
        context = {
            'PATH_PRD': str(target_dir / "prd.md"),
            'PATH_ARCH': str(target_dir / "arch.md"),
            'PATH_RESEARCH': str(target_dir / "research.md"),
            'PATH_BLUEPRINT': str(target_dir / "blueprint.md"),
            'LANGUAGE': language,
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
            # Use template-defined prompt with variable substitution
            from tempdd.template_parser import process_template_variables

            variables = {
                'LANGUAGE': language,
                'TARGET_DOCUMENT': target_document,
                'STAGE': stage,
                'ACTION': action
            }

            processed_prompt = process_template_variables(action_prompt, variables)

            return \
f"""[AI_INSTRUCTION_START]
{processed_prompt}
[AI_INSTRUCTION_END]"""
        else:
            # Fallback to simple format when no template prompt is available
            return \
f"""[AI_INSTRUCTION_START]
You are working on the {stage} stage with {action} action.

Language: {language}
Target Document: {target_document}

Please proceed with the {action} operation for {stage} stage.
Follow the guidelines and update the target document accordingly.
[AI_INSTRUCTION_END]"""

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
