import os
import torch
import streamlit as st
import pandas as pd
import soundfile as sf
import streamlit.components.v1 as components
from transformers import AutoTokenizer, AutoModelForTextToWaveform
import soundfile as sf
import os
import streamlit.components.v1 as components


# Setup generated audio folder
AUDIO_DIR = "generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


# Load Yoruba TTS model
@st.cache_resource
def load_tts_model():
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-yor")
    model = AutoModelForTextToWaveform.from_pretrained("facebook/mms-tts-yor")
    return tokenizer, model

tokenizer, model = load_tts_model()


# Load questions
@st.cache_data
def load_questions():
    return pd.read_csv("questions.csv")

questions_df = load_questions()

# Yoruba ordinal labels
yoruba_numbers = [
    "Kínní", "Kejì", "Kẹta", "Kẹrin", "Karùn-ún",
    "Kẹfà", "Keje", "Kejo", "Kẹsàn-án", "Kẹwàá"
]


# Audio generator
def generate_audio(text, filename="generated.wav"):
    file_path = os.path.join(AUDIO_DIR, filename)
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    output_np = output.squeeze().cpu().numpy()
    sf.write(file_path, output_np, samplerate=16000)
    return file_path


# Streamlit UI
st.title("Yoruba CBT TTS App")
st.subheader("Practice WAEC Yoruba Questions with Voice")

# Track question index
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

question_index = st.session_state.question_index
total_questions = len(questions_df)

# Clean up old audio
for f in os.listdir(AUDIO_DIR):
    file_path = os.path.join(AUDIO_DIR, f)
    if os.path.isfile(file_path):
        os.remove(file_path)

# Display current question
if question_index < total_questions:
    selected_question = questions_df.iloc[question_index]
    yoruba_label = yoruba_numbers[question_index] if question_index < len(yoruba_numbers) else f"#{question_index + 1}"

    # Prepare question text
    question_text = (
        f"Ibéèrè {yoruba_label}: {selected_question['question']}... "
        f"A..., {selected_question['option_a']}... "
        f"B..., {selected_question['option_b']}... "
        f"C..., {selected_question['option_c']}... "
        f"D..., {selected_question['option_d']}."
    )

    # Generate audio
    audio_filename = f"question_{question_index + 1}.wav"
    audio_path = generate_audio(question_text, filename=audio_filename)
    st.audio(audio_path, format="audio/wav")

    # Display text and options
    st.markdown(f"### Ibéèrè {yoruba_label}")
    st.write(selected_question["question"])

    option_texts = {
        "A": selected_question["option_a"],
        "B": selected_question["option_b"],
        "C": selected_question["option_c"],
        "D": selected_question["option_d"],
    }
    formatted_options = [f"{key}. {value}" for key, value in option_texts.items()]
    user_choice_label = st.radio("Yan idahun rẹ:", formatted_options, key=f"q_{question_index}")
    user_choice = user_choice_label.split(".")[0]

    # Navigation
    if st.button("Tẹsiwaju si Ibéèrè Tó Kàn"):
        st.session_state.question_index += 1
        # Remove current audio after moving forward
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # Optional: enable right-arrow key to continue
        components.html(
        """
        <script>
            document.addEventListener("keydown", function(event) {
                if (event.key === "ArrowRight") {
                    const btns = window.parent.document.querySelectorAll('button');
                    for (let btn of btns) {
                        if (btn.innerText.includes("Tẹsiwaju")) {
                            btn.click();
                            break;
                        }
                    }
                }
            });
        </script>
        """,
        height=0,
        )

    # Progress indicator
    st.markdown(
        f"<p style='text-align: center; font-weight: bold;'>🔢 {question_index + 1}/{total_questions}</p>",
        unsafe_allow_html=True
    )

else:
    st.success("O ti pari gbogbo awọn ibeere naa! 👏")
    st.balloons()
