import os

STT_MODE = os.getenv("STT_MODE")

USE_WHISPER = STT_MODE == 1   # whisper
