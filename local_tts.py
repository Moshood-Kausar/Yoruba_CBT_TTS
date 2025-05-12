from transformers import AutoProcessor, BarkModel
from transformers import AutoModelForSpeechSeq2Seq, AutoTokenizer, pipeline
import torch
import soundfile as sf

# Load the model and processor
model_id = "facebook/mms-tts-yor"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Input Yoruba text
text = "Báwo ni o ṣe wà?"

# Preprocess and run model
inputs = processor(text=text, return_tensors="pt").to(device)
with torch.no_grad():
    speech = model.generate(**inputs)

# Decode and save audio
audio_array = processor.batch_decode(speech, skip_special_tokens=True)[0]
audio = processor.decode(speech[0])
sf.write("yoruba_output.wav", audio_array, 16000)

print("✅ Audio saved to yoruba_output.wav")
