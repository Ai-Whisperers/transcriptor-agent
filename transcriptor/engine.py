import os
import whisper
import torch
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class TranscriptorEngine:
    # Priority list as requested
    # 1. openai API, 2. groq API, 3. local large-v3, 4. local large, 5. local medium, 6. local base
    
    def __init__(self):
        self._local_models = {}
        self._openai_client = None
        self._groq_client = None
        
        # Initialize clients if keys exist
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self._openai_client = OpenAI(api_key=openai_key)
            
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            self._groq_client = Groq(api_key=groq_key)

    def transcribe(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        # Cascade 1: OpenAI API
        if self._openai_client:
            try:
                if os.path.getsize(file_path) / (1024 * 1024) < 25:
                    with open(file_path, "rb") as f:
                        transcription = self._openai_client.audio.transcriptions.create(
                            model="whisper-1", 
                            file=f
                        )
                    return {
                        "text": transcription.text,
                        "metadata": {"provider": "OpenAI API", "model": "whisper-1"}
                    }
                else:
                    print(f"⚠️ WARNING: File too large for OpenAI API. Falling back to Groq/Local...")
            except Exception as e:
                print(f"⚠️ WARNING: OpenAI API failed: {e}. Falling back to Groq...")

        # Cascade 2: Groq API
        if self._groq_client:
            try:
                # Groq 25MB check
                if os.path.getsize(file_path) / (1024 * 1024) < 25:
                    with open(file_path, "rb") as f:
                        transcription = self._groq_client.audio.transcriptions.create(
                            model="whisper-large-v3", 
                            file=f
                        )
                    return {
                        "text": transcription.text,
                        "metadata": {"provider": "Groq API", "model": "whisper-large-v3"}
                    }
                else:
                    print(f"⚠️ WARNING: File too large for Groq. Falling back to Local...")
            except Exception as e:
                print(f"⚠️ WARNING: Groq API failed (possibly rate limit): {e}. Falling back to Local...")

        # Cascade 3-6: Local Models
        local_priority = [
            ("large-v3", "Highest"),
            ("large", "High"),
            ("medium", "Medium"),
            ("base", "Low")
        ]

        for model_name, level_name in local_priority:
            try:
                print(f"🔄 Attempting Local {level_name} model ({model_name})...")
                result = self._transcribe_local(file_path, model_name)
                return {
                    "text": result["text"],
                    "metadata": {"provider": "Local", "model": model_name, "tier": level_name}
                }
            except torch.cuda.OutOfMemoryError:
                print(f"⚠️ WARNING: Out of VRAM for {model_name}. Falling back to next tier...")
                # Clear cache
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                continue
            except Exception as e:
                print(f"⚠️ WARNING: Local {model_name} failed: {e}. Falling back...")
                continue

        raise RuntimeError("CRITICAL: All transcription providers and local models failed.")

    def _transcribe_local(self, file_path: str, model_name: str):
        if model_name not in self._local_models:
            self._local_models[model_name] = whisper.load_model(model_name)
        return self._local_models[model_name].transcribe(file_path)
