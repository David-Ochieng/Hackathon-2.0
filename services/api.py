import os
import requests
from config import Config

HEADERS = {"Authorization": f"Bearer {Config.HF_API_TOKEN}"}

def analyze_emotion(text: str, model: str = None, timeout: int = 15):
    model = model or Config.HF_MODEL
    url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs": text}
    try:
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}
