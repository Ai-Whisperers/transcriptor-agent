# 🎙️ Transcriptor

Transcriptor is a production-ready, TDD-built audio transcription system. It leverages OpenAI's **Whisper large-v3** model to provide industry-leading accuracy across multiple file formats including `.ogg`, `.mp3`, and `.mpeg`.

## 🌟 Key Features
- **Flexible Interfaces:** Use the CLI for automation, the API for integration, or the SPA for a friendly UI.
- **TDD Native:** 100% test coverage of core logic, CLI commands, and API endpoints.
- **Whisper Integration:** Supports all Whisper models from `tiny` to `large-v3`.
- **Modern UI:** Built with React + TypeScript + Vite with a focus on UX.
- **CI/CD Ready:** Pre-configured GitHub Actions for automated testing.

## 🛠️ Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js & npm
- FFmpeg installed on your system:
  ```bash
  sudo apt update && sudo apt install ffmpeg -y
  ```

### 2. Backend Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Usage

#### CLI
```bash
python -m transcriptor.cli transcribe "path/to/audio.ogg" --model large-v3
```

#### API
```bash
uvicorn transcriptor.api:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📂 Documentation
- [Architecture Details](./docs/ARCHITECTURE.md)
- [Testing & TDD Guide](./docs/TESTING.md)
- [Project Blueprint](./BLUEPRINT.md)

## 🧪 Testing
Run the automated test suite:
```bash
./venv/bin/pytest
```

## 📜 License
MIT
