import whisper

_model = None

def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("tiny")
    return _model

def speech_to_text(audio_path):
    model = get_model()
    result = model.transcribe(audio_path)
    return result["text"]
