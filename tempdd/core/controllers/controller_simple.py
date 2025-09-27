"""
TempDD Simple Controller

Handles command processing for the simplified workflow with reduced stages.
"""

from typing import Optional

from tempdd.core.controllers.base import BaseController


class Controller(BaseController):
    """
    TempDD Simple Controller

    Handles a simplified workflow including only core stages:
    PRD, Blueprint, and Tasks (without Architecture and Research stages)
    """

    HELP_CONTENT_TEMPLATE = """{system_prompt}

== TempDD Simple Workflow ==

Language: {language}
Available Stages: {stages}

Simplified Workflow:
1. PRD (Product Requirements Document)
   - Use '/tempdd-go prd build' to create product requirements

2. Blueprint Document
   - Use '/tempdd-go blueprint build' to create implementation blueprint

3. Tasks Document & Implementation
   - Use '/tempdd-go tasks build' to break down implementation tasks
   - Use '/tempdd-go tasks run' to implement the planned tasks

Stage Actions:
  build - Create/build the document for the stage
  run   - Execute the implementation (for tasks stage)

This simplified workflow focuses on the essential stages for faster development cycles.
"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the simple controller

        Args:
            config_path: Optional custom configuration file path
        """
        super().__init__(config_path)

    def get_help_content(self) -> str:
        """Generate help content for TempDD simple workflow in Claude Code"""
        stages = self.config.get("stages", [])
        language = self.config.get("language", "en").upper()
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(language=language)

        return self.HELP_CONTENT_TEMPLATE.format(
            system_prompt=system_prompt, language=language, stages=", ".join(stages)
        )