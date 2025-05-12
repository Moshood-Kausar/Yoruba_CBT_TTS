import requests
import os

# Set your Hugging Face token here if not using environment variables
HF_TOKEN = "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"  # Replace with your actual token if needed

API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-yor"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    print("Status Code:", response.status_code)
    print("Content-Type:", response.headers.get("content-type", ""))

    if response.status_code == 200 and "audio" in response.headers.get("content-type", ""):
        with open("yoruba_test.mp3", "wb") as f:
            f.write(response.content)
        print("✅ Audio saved to yoruba_test.mp3")
    else:
        print("❌ ERROR: Not valid audio")
        print("Response text:", response.text)

if __name__ == "__main__":
    yoruba_text = "Báwo ni o ṣe wà?"
    query(yoruba_text)
