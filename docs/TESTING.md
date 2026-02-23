# Testing Strategy & TDD

## Overview
Transcriptor is built with a TDD (Test-Driven Development) first approach, ensuring that every feature is validated before and after implementation.

## Test Suites
- **Core Engine Tests (`tests/test_engine.py`):**
  - Initialization checks.
  - File existence validation.
  - Mocked transcription logic.
- **CLI Tests (`tests/test_cli.py`):**
  - Command existence and help flags.
  - Model selection handling.
  - Output verification.
- **API Tests (`tests/test_api.py`):**
  - Endpoint reachability.
  - Multipart file upload handling.
  - JSON response validation.

## Running Tests
Ensure you have the virtual environment activated:
```bash
source venv/bin/activate
pytest
```

## Continuous Integration
A GitHub Actions workflow (`.github/workflows/ci.yml`) is configured to:
1. Set up a Python 3.10 environment.
2. Install system-level FFmpeg.
3. Install project dependencies.
4. Run the full test suite on every push.
