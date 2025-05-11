# app.py
import streamlit as st
import tempfile
from tts import generate_audio

# Sample WAEC-style Yoruba question
question_data = {
    "question": "Ta ni akọrin Yoruba to gbajumo ju ni ọdun 1980?",
    "options": ["Ayinde Barrister", "Fela Kuti", "K1 De Ultimate", "Sunny Ade"],
    "answer": "Ayinde Barrister"
}

st.set_page_config(page_title="Yoruba CBT TTS", layout="centered")
st.title("📚 Yoruba CBT Exam (TTS Enabled)")
st.markdown("**Ẹ jọwọ, tẹtisi ibeere naa ki o yan idahun to pe.**")

# Generate audio from question text
with st.spinner("🔊 N ṣiṣẹ lori ọrọ sisọ..."):
    audio = generate_audio(question_data["question"])
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        tmpfile.write(audio)
        st.audio(tmpfile.name, format="audio/wav")

# Show question and options
user_answer = st.radio("Yan idahun rẹ:", question_data["options"])

if st.button("Firanṣẹ"):
    if user_answer == question_data["answer"]:
        st.success("O dahun ni deede ✅")
    else:
        st.error(f"Idahun naa ko tọ ❌. Idahun to pe ni: {question_data['answer']}")
