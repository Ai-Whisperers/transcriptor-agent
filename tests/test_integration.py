import os
import pytest
from typer.testing import CliRunner
from transcriptor.cli import app
from unittest.mock import patch, MagicMock

runner = CliRunner()

def test_full_batch_flow_mocked(tmp_path):
    # Setup temporary directories
    target_dir = tmp_path / "targets"
    output_dir = tmp_path / "outputs"
    target_dir.mkdir()
    output_dir.mkdir()
    
    # Create dummy audio files
    (target_dir / "audio1.mp3").write_text("dummy")
    (target_dir / "audio2.m4a").write_text("dummy")
    
    # Mock the engine to avoid real transcription/API calls
    with patch("transcriptor.engine.TranscriptorEngine.transcribe") as mock_transcribe:
        mock_transcribe.return_value = {"text": "Transcribed text"}
        
        # Run batch command
        result = runner.invoke(app, [
            "batch", 
            "--directory", str(target_dir), 
            "--output-dir", str(output_dir),
            "--no-api",
            "--model", "tiny"
        ])
        
        assert result.exit_code == 0
        assert "Found 2 files" in result.stdout
        
        # Verify output files exist
        assert os.path.exists(output_dir / "audio1.txt")
        assert os.path.exists(output_dir / "audio2.txt")
        assert (output_dir / "audio1.txt").read_text() == "Transcribed text"
