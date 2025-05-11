
# tts.py
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/tts_transformer-yor-eng-ft-lyr"
HF_TOKEN = "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" 

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_audio(text: str):
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    return response.content
