import requests

OLLAMA_URL = "http://ollama:11434/api/embeddings"

def generate_embedding(text: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    data = response.json()

    return data["embedding"]