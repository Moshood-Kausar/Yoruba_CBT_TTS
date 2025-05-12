import os
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-yor"
headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content  # raw audio (MP3 format)

def get_audio_from_text(text):
    audio_data = query({"inputs": text})
    return audio_data
