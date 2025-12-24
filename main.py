from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import uuid

from interviewer import get_question
from stt import speech_to_text
from evaluator import evaluate
from decision import decide
from tts import text_to_speech

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


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
    audio_path = text_to_speech(current_question)
    return {
        "question": current_question,
        "audio_url": f"/audio/{audio_path.split('/')[-1]}"
    }

@app.post("/answer")
def answer(audio: UploadFile = File(...)):
    filename = f"/tmp/{uuid.uuid4()}.wav"
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    text = speech_to_text(filename)
    evaluation = evaluate(current_question, text)

    score_line = [l for l in evaluation.splitlines() if l.startswith("Score:")][0]
    score = int(score_line.split(":")[1].strip())

    action = decide(score)

    spoken_feedback = f"Your result is {action}. {evaluation}"
    feedback_audio = text_to_speech(spoken_feedback)

    return {
        "transcribed_answer": text,
        "evaluation": evaluation,
        "decision": action,
        "audio_url": f"/audio/{feedback_audio.split('/')[-1]}"
    }

@app.get("/audio/{filename}")
def get_audio(filename: str):
    return FileResponse(f"/tmp/{filename}", media_type="audio/mpeg")
