from gtts import gTTS
import uuid
import os

def text_to_speech(text: str) -> str:
    filename = f"/tmp/{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(filename)
    return filename
