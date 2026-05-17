import requests

def ask_llm(prompt):
    url = "http://ollama:11434/api/generate"

    payload = {
        "model": "qwen2.5-coder:7b",
        "prompt": prompt,
        "stream": False   # IMPORTANT FIX
    }

    response = requests.post(url, json=payload)

    return response.json()["response"]