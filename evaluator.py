import google.generativeai as genai
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

print("Gemini key loaded:", bool(os.getenv("GEMINI_API_KEY")))


BASE_DIR = Path(__file__).resolve().parent
print("BASE_DIR:", BASE_DIR)
print("Files in BASE_DIR:", list(BASE_DIR.iterdir()))
print("Prompts exists:", (BASE_DIR / "prompts").exists())
evaluation_prompt_path = BASE_DIR / "prompts" / "evaluation.txt"

PROMPTS_DIR = BASE_DIR / "prompts"

DEFAULT_EVALUATION_PROMPT = """
Evaluate the candidate answer.
Point out missing concepts.
Suggest improvements.
"""

evaluation_prompt_path = PROMPTS_DIR / "evaluation.txt"

if evaluation_prompt_path.exists():
    evaluation_prompt = evaluation_prompt_path.read_text()
else:
    print("⚠️ evaluation.txt not found, using default prompt")
    evaluation_prompt = DEFAULT_EVALUATION_PROMPT

def evaluate(question, answer):
    prompt = evaluation_prompt.format(
        question=question,
        answer=answer
    )
    response = model.generate_content(prompt)
    return response.text
