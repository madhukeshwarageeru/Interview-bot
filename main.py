from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import shutil
import uuid

from interviewer import get_question
from stt import speech_to_text
from evaluator import evaluate
from decision import decide
from tts import text_to_speech

from config import USE_WHISPER
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

current_question = None
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
print("🚀 App started successfully (Whisper lazy-loaded)")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html") as f:
        return f.read()


current_question = get_question()

@app.get("/question")
def question():
    global current_question
    audio_path = text_to_speech(current_question)
    current_question = question
    return {
        "question": current_question,
        "audio_url": f"/audio/{audio_path.split('/')[-1]}"
    }


@app.post("/answer")
async def answer(
    text: str = Form(None),
    audio: UploadFile = None
    

    if not current_question:
        return JSONResponse(
            status_code=400,
            content={"error": "No active question"}
        )
):
    if USE_WHISPER:
        if not audio:
            return {"error": "Audio required"}

        path = f"/tmp/{audio.filename}"
        with open(path, "wb") as f:
            f.write(await audio.read())

        from stt import transcribe_audio
        text = transcribe_audio(path)

    if not text:
        return {"error": "No answer text"}

    return evaluate(current_question,text)
    
@app.get("/config")
def config():
    return {"stt_mode": STT_MODE}

@app.get("/audio/{filename}")
def get_audio(filename: str):
    return FileResponse(f"/tmp/{filename}", media_type="audio/mpeg")
