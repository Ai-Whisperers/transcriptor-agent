# Transcriptor Architecture

## System Overview
Transcriptor is a multi-interface application designed to provide high-quality audio-to-text conversion using OpenAI's Whisper model.

## Components

### 1. Core Engine (`transcriptor/engine.py`)
- Wraps the `openai-whisper` library.
- Implements lazy loading of models to optimize memory/GPU usage.
- Handles file system validation and error management.
- Standardizes output formats.

### 2. CLI Interface (`transcriptor/cli.py`)
- Built with `Typer`.
- Provides commands for `version` and `transcribe`.
- Supports model selection via flags (e.g., `--model large-v3`).

### 3. API Layer (`transcriptor/api.py`)
- Powered by `FastAPI`.
- RESTful endpoint `POST /transcribe` for multipart file uploads.
- Uses temporary file handling for secure processing.

### 4. SPA Frontend (`frontend/`)
- Developed with React, TypeScript, and Vite.
- Proxy-aware configuration to communicate with the FastAPI backend.
- Features a modern, responsive UI with progress feedback.

## Data Flow
1. **Input:** Audio file (ogg, mp3, mpeg) provided via CLI, API, or UI.
2. **Validation:** System checks for file existence and format compatibility.
3. **Processing:** Whisper model (default `large-v3`) processes audio through FFmpeg.
4. **Output:** Plain text transcription returned to the requester.
