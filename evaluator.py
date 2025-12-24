import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-pro")

evaluation_prompt = Path("prompts/evaluation.txt").read_text()

def evaluate(question, answer):
    prompt = evaluation_prompt.format(
        question=question,
        answer=answer
    )
    response = model.generate_content(prompt)
    return response.text
