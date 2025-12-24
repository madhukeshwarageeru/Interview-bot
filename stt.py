from config import USE_WHISPER

if USE_WHISPER:
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

if not USE_WHISPER:
     print("Whisper disabled, using browser STT")
    def transcribe_audio(file_path: str) -> str:
        result = model.transcribe(file_path)
        return result["text"]

