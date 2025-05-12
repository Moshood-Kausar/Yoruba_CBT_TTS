import streamlit as st
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForTextToWaveform
import soundfile as sf
import os

# Load Yoruba TTS model
@st.cache_resource
def load_tts_model():
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-yor")
    model = AutoModelForTextToWaveform.from_pretrained("facebook/mms-tts-yor")
    return tokenizer, model

tokenizer, model = load_tts_model()

# Load questions from local CSV file
@st.cache_data
def load_questions():
    return pd.read_csv("questions.csv")

questions_df = load_questions()

# Yoruba numbers for question count
yoruba_numbers = [
    "Kìnní", "Kẹta", "Kẹrin", "Karùn-ún", "Kẹfà",
    "Kẹfà", "Keje", "Kejo", "Kẹsàn-án", "Kẹwàá"
]

# Generate TTS audio
def generate_audio(text, filename="generated.wav"):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    output_np = output.squeeze().cpu().numpy()
    sf.write(filename, output_np, samplerate=16000)
    return filename

# Streamlit app
st.title("📣 Yoruba CBT TTS App")
st.subheader("Practice WAEC Yoruba Questions with Voice")

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

question_index = st.session_state.question_index
total_questions = len(questions_df)

if question_index < total_questions:
    selected_question = questions_df.iloc[question_index]
    yoruba_num = yoruba_numbers[question_index] if question_index < len(yoruba_numbers) else f"#{question_index + 1}"

    # Construct TTS script
    question_text = (
        f"Ibéèrè {yoruba_num}: {selected_question['question']}... "
        f"A... , {selected_question['option_a']}... "
        f"B... , {selected_question['option_b']}... "
        f"C... , {selected_question['option_c']}... "
        f"D... , {selected_question['option_d']}."
    )

    # Generate and play TTS audio
    audio_path = generate_audio(question_text)
    st.audio(audio_path, format="audio/wav")

    # Display text version
st.markdown(f"### Ibéèrè {yoruba_num}")
st.write(selected_question["question"])

# Prepare options with text from CSV
option_texts = {
    "A": selected_question["option_a"],
    "B": selected_question["option_b"],
    "C": selected_question["option_c"],
    "D": selected_question["option_d"],
}

# Combine label and option text
formatted_options = [
    f"{key}. {value}" for key, value in option_texts.items()
]

# Show radio buttons using labels only (but capture key as answer)
user_choice_label = st.radio("Yan idahun rẹ:", formatted_options, key=f"q_{question_index}")
user_choice = user_choice_label.split(".")[0]  # Extract A/B/C/D

if st.button("Tẹsiwaju si Ibéèrè Tó Kàn"):
        st.session_state.question_index += 1
        os.remove(audio_path)
else:
    st.success("O pari gbogbo awọn ibeere naa! 👏")
    st.balloons()
