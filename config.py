import os

STT_MODE = os.getenv("STT_MODE", "browser").lower()

USE_WHISPER = STT_MODE == "whisper"
