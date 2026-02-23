from typer.testing import CliRunner
from transcriptor.cli import app
from unittest.mock import patch, MagicMock
import os

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout

@patch("transcriptor.engine.TranscriptorEngine.transcribe")
def test_cli_transcribe_success(mock_transcribe):
    mock_transcribe.return_value = {"text": "Transcribed text from CLI"}
    
    # Create a dummy file
    with open("cli_test.ogg", "w") as f:
        f.write("dummy")
    
    try:
        # Note: Added --no-api or equivalent if needed, but transcribe defaults to api=True
        # Let's pass --api/--no-api if the CLI supports it
        result = runner.invoke(app, ["transcribe", "cli_test.ogg", "--model", "tiny", "--no-api"])
        assert result.exit_code == 0
        assert "Transcribed text from CLI" in result.stdout
    finally:
        if os.path.exists("cli_test.ogg"):
            os.remove("cli_test.ogg")

def test_cli_transcribe_file_not_found():
    result = runner.invoke(app, ["transcribe", "missing.ogg"])
    assert result.exit_code != 0
    # Combine stdout and stderr for the check
    output = result.stdout + (getattr(result, "stderr", "") or "")
    assert "not found" in output.lower()
