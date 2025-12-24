import random

QUESTIONS = [
    "Explain how you would solve the Two Sum problem and its time complexity.",
    "Difference between IEnumerable and IList in C# with example.",
    "Design a URL shortener system at high level.",
    "How would you design an LRU Cache?",
    "Explain async vs parallel programming in C#."
]

def get_question():
    return random.choice(QUESTIONS)
