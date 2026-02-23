import pytest
import os
from unittest.mock import patch, MagicMock
from transcriptor.engine import TranscriptorEngine

def test_engine_init_no_keys():
    with patch.dict(os.environ, {}, clear=True):
        engine = TranscriptorEngine()
        assert engine._openai_client is None
        assert engine._groq_client is None

@patch("whisper.load_model")
def test_transcribe_local_fallback_chain(mock_load_model):
    # Mocking local model transcribe
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"text": "Local text"}
    mock_load_model.return_value = mock_model
    
    # Ensure no API keys to force local path
    with patch.dict(os.environ, {}, clear=True):
        engine = TranscriptorEngine()
        
        # Create dummy file
        with open("test_chain.ogg", "w") as f:
            f.write("data")
            
        try:
            result = engine.transcribe("test_chain.ogg")
            # Should have reached 'large-v3' (first local in chain)
            assert result["metadata"]["model"] == "large-v3"
            assert result["metadata"]["provider"] == "Local"
        finally:
            if os.path.exists("test_chain.ogg"):
                os.remove("test_chain.ogg")

@patch("transcriptor.engine.OpenAI")
def test_transcribe_openai_priority(mock_openai_class):
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    mock_client.audio.transcriptions.create.return_value = MagicMock(text="OpenAI text")
    
    with patch.dict(os.environ, {"OPENAI_API_KEY": "fake"}):
        engine = TranscriptorEngine()
        engine._openai_client = mock_client
        
        with open("test_oa.ogg", "w") as f:
            f.write("data")
            
        try:
            result = engine.transcribe("test_oa.ogg")
            assert result["metadata"]["provider"] == "OpenAI API"
            assert result["text"] == "OpenAI text"
        finally:
            if os.path.exists("test_oa.ogg"):
                os.remove("test_oa.ogg")
