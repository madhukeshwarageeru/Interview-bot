import google.generativeai as genai
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

print("Gemini key loaded:", bool(os.getenv("GEMINI_API_KEY")))

evaluation_prompt_path= Path(__file__).parent / "prompts" / "evaluation.txt"
evaluation_prompt = evaluation_prompt_path.read_text()


def evaluate(question, answer):
    prompt = evaluation_prompt.format(
        question=question,
        answer=answer
    )
    response = model.generate_content(prompt)
    return response.text
