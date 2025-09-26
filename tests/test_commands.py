"""Simple end-to-end tests for TempDD commands."""
import subprocess
import os
from pathlib import Path
import tempfile
import shutil
from tempdd.handlers.ai import format_ai_instruction


def test_cli_help():
    """Test CLI help command."""
    result = subprocess.run(
        ["python", "-m", "tempdd.cli", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "tempdd" in result.stdout


def test_cli_version():
    """Test CLI version command."""
    result = subprocess.run(
        ["python", "-m", "tempdd.cli", "--version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_init_command():
    """Test init command creates project structure."""
    temp_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()

    try:
        os.chdir(temp_dir)

        result = subprocess.run(
            ["python", "-m", "tempdd.cli", "init", "--force"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert Path(".tempdd").exists()
        assert Path(".claude").exists()
        assert Path(".tempdd/config.json").exists()

    finally:
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_ai_instruction_formatting():
    """Test that AI instruction formatting works correctly."""
    content = "This is test content for AI instruction"

    formatted = format_ai_instruction(content)

    assert "[AI_INSTRUCTION_START]" in formatted
    assert "[AI_INSTRUCTION_END]" in formatted
    assert content in formatted

    # Ensure the content is properly wrapped
    lines = formatted.split('\n')
    assert lines[0] == "[AI_INSTRUCTION_START]"
    assert lines[-1] == "[AI_INSTRUCTION_END]"


def test_ai_command_format():
    """Test AI command with valid stage action format."""
    result = subprocess.run(
        ["python", "-m", "tempdd.cli", "ai", "prd build"],
        capture_output=True,
        text=True
    )
    # Should handle missing config gracefully
    assert result.returncode in [0, 1]


def test_ai_command_invalid_format():
    """Test AI command with invalid format should fail."""
    result = subprocess.run(
        ["python", "-m", "tempdd.cli", "ai", "prd"],  # Missing action
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert "Invalid command format" in result.stderr


def test_ai_command_with_project():
    """Test AI command in initialized project."""
    temp_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()

    try:
        os.chdir(temp_dir)

        # Initialize project first
        subprocess.run(
            ["python", "-m", "tempdd.cli", "init", "--force"],
            capture_output=True
        )

        # Run AI command
        result = subprocess.run(
            ["python", "-m", "tempdd.cli", "ai", "prd build"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "[AI_INSTRUCTION_START]" in result.stdout
        assert "[AI_INSTRUCTION_END]" in result.stdout

    finally:
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_ai_instruction_formatting():
    """Test that AI instruction formatting works correctly."""
    content = "This is test content for AI instruction"

    formatted = format_ai_instruction(content)

    assert "[AI_INSTRUCTION_START]" in formatted
    assert "[AI_INSTRUCTION_END]" in formatted
    assert content in formatted

    # Ensure the content is properly wrapped
    lines = formatted.split('\n')
    assert lines[0] == "[AI_INSTRUCTION_START]"
    assert lines[-1] == "[AI_INSTRUCTION_END]"


def test_old_commands_removed():
    """Test that old preprocess and agent commands are no longer available."""
    # Test preprocess command should fail
    result = subprocess.run(
        ["python", "-m", "tempdd.cli", "preprocess", "prd"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0

    # Test agent command should fail
    result = subprocess.run(
        ["python", "-m", "tempdd.cli", "agent", "prd"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0

def test_e2e_ai_command_generates_correct_path():
    """
    End-to-end test to ensure 'tempdd ai' command generates AI instructions
    with the correct document path based on the new directory logic.
    """
    temp_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()

    try:
        os.chdir(temp_dir)

        # 1. Initialize project
        subprocess.run(
            ["python", "-m", "tempdd.cli", "init", "--force"],
            check=True,
            capture_output=True
        )

        # 2. Run the 'ai' command
        result = subprocess.run(
            ["python", "-m", "tempdd.cli", "ai", "prd build"],
            capture_output=True,
            text=True,
            check=True
        )

        # 3. Assert the output contains the correct path
        assert "[AI_INSTRUCTION_START]" in result.stdout
        # The path should be constructed using the default logic
        expected_path = Path("docs-for-works") / "001_initialization" / "prd.md"
        assert str(expected_path) in result.stdout

    finally:
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_ai_instruction_formatting():
    """Test that AI instruction formatting works correctly."""
    content = "This is test content for AI instruction"

    formatted = format_ai_instruction(content)

    assert "[AI_INSTRUCTION_START]" in formatted
    assert "[AI_INSTRUCTION_END]" in formatted
    assert content in formatted

    # Ensure the content is properly wrapped
    lines = formatted.split('\n')
    assert lines[0] == "[AI_INSTRUCTION_START]"
    assert lines[-1] == "[AI_INSTRUCTION_END]"