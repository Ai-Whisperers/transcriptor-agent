import pytest
from fastapi.testclient import TestClient
from transcriptor.api import app
from unittest.mock import patch, MagicMock
import io

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Transcriptor API" in response.json()["message"]

@patch("transcriptor.engine.TranscriptorEngine.transcribe")
def test_api_transcribe_success(mock_transcribe):
    mock_transcribe.return_value = {"text": "API transcription result"}
    
    # Mocking a file upload
    file_content = b"fake audio data"
    files = {"file": ("test.ogg", file_content, "audio/ogg")}
    
    response = client.post("/transcribe?model=tiny&use_api=false", files=files)
    
    assert response.status_code == 200
    assert response.json()["text"] == "API transcription result"

def test_api_transcribe_no_file():
    response = client.post("/transcribe")
    assert response.status_code == 422 # Validation error for missing file
