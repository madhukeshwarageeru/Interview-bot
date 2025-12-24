import google.generativeai as genai
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

print("Gemini key loaded:", bool(os.getenv("GEMINI_API_KEY")))

BASE_DIR = Path(__file__).resolve().parent

evaluation_prompt_path = BASE_DIR / "prompts" / "evaluation.txt"

if not evaluation_prompt_path.exists():
    raise RuntimeError(
        f"Missing file: {evaluation_prompt_path}. "
        "Ensure prompts/evaluation.txt exists and is committed."
    )
evaluation_prompt = evaluation_prompt_path.read_text()


def evaluate(question, answer):
    prompt = evaluation_prompt.format(
        question=question,
        answer=answer
    )
    response = model.generate_content(prompt)
    return response.text
