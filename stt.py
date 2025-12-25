


from config import USE_WHISPER


# -------------------------------
# Whisper enabled
# -------------------------------
if USE_WHISPER:
    import whisper

    _model = None

    def get_model():
        global _model
        if _model is None:
            _model = whisper.load_model("tiny")
        return _model

    def speech_to_text(audio_path: str) -> str:
        model = get_model()
        result = model.transcribe(audio_path)
        return result["text"]


# -------------------------------
# Whisper disabled
# -------------------------------
else:
    print("Whisper disabled, using browser STT")

    def speech_to_text(audio_path: str) -> str:
        print("Whisper disabled, using browser STT")
        result = model.transcribe(file_path)
        return result["text"]

