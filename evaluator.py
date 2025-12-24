import google.generativeai as genai
from pathlib import Path

import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

print("Gemini key loaded:", bool(os.getenv("GEMINI_API_KEY")))

evaluation_prompt = Path("prompts/evaluation.txt").read_text()

def evaluate(question, answer):
    prompt = evaluation_prompt.format(
        question=question,
        answer=answer
    )
    response = model.generate_content(prompt)
    return response.text
