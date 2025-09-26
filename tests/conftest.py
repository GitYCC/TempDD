"""Test configuration and fixtures."""
import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for testing TempDD projects."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_config():
    """Sample TempDD configuration for testing."""
    return {
        "language": "en",
        "stages": ["prd", "arch"],
        "flow": {
            "prd": {
                "template": "prd_template",
                "agent": "prd_agent",
                "preprocess": "preprocess_default"
            },
            "arch": {
                "template": "arch_template",
                "agent": "arch_agent",
                "preprocess": "preprocess_default"
            }
        },
        "current_target_document": None
    }