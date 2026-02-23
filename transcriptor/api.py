from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from transcriptor.engine import TranscriptorEngine
import os
import shutil
import tempfile

app = FastAPI(title="Transcriptor API")

@app.get("/")
async def root():
    return {"message": "Welcome to Transcriptor API"}

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    model: str = Query("large-v3", description="Whisper model for local use"),
    use_api: bool = Query(True, description="Use API"),
    provider: str = Query("openai", description="API provider: openai or groq")
):
    # Handle the 'local' option from frontend
    actual_use_api = use_api
    if provider == "local":
        actual_use_api = False

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        engine = TranscriptorEngine(model_name=model, use_api=actual_use_api, provider=provider)
        result = engine.transcribe(tmp_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
