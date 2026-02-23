# Transcriptor Blueprint: Whisper-Powered Audio-to-Text System

## Overview
Transcriptor is a robust, production-ready system for converting various audio formats (ogg, mp3, mpeg, etc.) into high-quality text using OpenAI's Whisper `large-v3` model. The system is designed with a TDD-first approach, providing a CLI for developers, an API for integration, and an SPA for end-users.

## Architecture
- **Core Engine:** Python-based module wrapping the `openai-whisper` library.
- **CLI:** Command-line interface built with `Typer` or `Click`.
- **API:** RESTful API built with `FastAPI`.
- **SPA:** React (TypeScript) frontend for web-based interaction.
- **CI/CD:** GitHub Actions for automated testing and deployment.

## Technical Specifications
- **Whisper Model:** `large-v3` (Highest quality available).
- **Supported Formats:** `.ogg`, `.mp3`, `.wav`, `.mpeg`, `.m4a`.
- **Primary Dependencies:**
  - `openai-whisper`: Transcription engine.
  - `ffmpeg`: Audio processing.
  - `fastapi` & `uvicorn`: API layer.
  - `typer`: CLI layer.
  - `pytest`: Testing framework.

## TDD Roadmap

### Phase 1: CI/CD & Harness (The "Safe" Foundation)
- [ ] Initialize Git repository and Python environment.
- [ ] Configure `pytest` and `black`/`isort` for linting.
- [ ] Set up GitHub Actions workflow for automated testing on push.
- [ ] **Test:** Ensure CI fails on broken code and passes on empty tests.

### Phase 2: Core Engine Development
- [ ] **Test:** Validate audio file existence and format.
- [ ] **Test:** Mock Whisper to verify transcription pipeline logic.
- [ ] **Implementation:** Integrate `openai-whisper` with `large-v3`.
- [ ] **Test:** Verify output formats (Text, JSON, SRT).

### Phase 3: CLI Implementation
- [ ] **Test:** CLI command `transcribe <path>` returns expected status codes.
- [ ] **Implementation:** Build CLI using `Typer`.
- [ ] **Test:** Batch processing of files in `/targets`.

### Phase 4: API Layer
- [ ] **Test:** Endpoint `POST /transcribe` accepts multipart file uploads.
- [ ] **Implementation:** FastAPI endpoints for single and batch transcription.
- [ ] **Test:** Asynchronous processing for large files.

### Phase 5: Single Page Application (SPA)
- [ ] **Test:** UI components render correctly (Upload, Progress, Results).
- [ ] **Implementation:** React/TypeScript SPA with Vanilla CSS.
- [ ] **Implementation:** Integration with the FastAPI backend.

## Deployment Commands (Quick Start)

### Development Setup
```bash
# Install system dependencies (FFmpeg is required for Whisper)
sudo apt update && sudo apt install ffmpeg -y

# Setup Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the CLI
```bash
python -m transcriptor.cli transcribe targets/some_audio.ogg --model large-v3
```

### Launching the API
```bash
uvicorn transcriptor.api:app --reload --port 8000
```

### Launching the SPA
```bash
cd frontend && npm install && npm run dev
```

## Maintenance & Safety
- **Secrets:** Use `.env` for any API keys (though Whisper runs locally by default).
- **Validation:** Every feature must have a corresponding test in `tests/` before implementation.
- **Resource Management:** `large-v3` requires significant VRAM; implement checks for available hardware.
