# src/llm.py
import ollama

def call_llm(prompt, model="llama3"):
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0},
    )
    return response["message"]["content"]