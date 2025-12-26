from gtts import gTTS
import uuid
from pathlib import Path

AUDIO_DIR = Path("static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def text_to_speech(text: str) -> str:
    filename = f"{uuid.uuid4()}.mp3"
    file_path = AUDIO_DIR / filename

    tts = gTTS(text=text, lang="en")
    tts.save(str(file_path))  # ✅ MUST be string path

    return f"/static/audio/{filename}"
