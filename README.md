# Yoruba CBT TTS App

This repository contains the Streamlit app and code used as the artifact for the paper: “Evaluating Yoruba Text-to-Speech Systems for Accessible Computer-Based Testing in Visually Impaired Learners.” It uses the facebook/mms-tts-yor model to read Yoruba CBT questions and options aloud for accessible practice.

🔗 **Live App:**
[https://yoruba-cbt-tts.streamlit.app/](https://yoruba-cbt-tts.streamlit.app/)

## Features

* Yoruba Text-to-Speech using `facebook/mms-tts-yor`
* Reads full CBT questions and options aloud (10)
* Interactive multiple-choice interface
* No Hugging Face token required (uses public model locally)


## Model Used

* **Model:** `facebook/mms-tts-yor`
* Loaded locally using Hugging Face `transformers`
* Works without API calls or authentication

## Project Structure

```
Yoruba_CBT_TTS/
│
├── app.py
├── questions.csv
├── generated_audio/
├── requirements.txt
└── README.md
```

* `app.py` → Main Streamlit application
* `questions.csv` → WAEC-style Yoruba questions
* `generated_audio/` → Stores generated audio files during runtime


##  Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Moshood-Kausar/Yoruba_CBT_TTS.git
cd Yoruba_CBT_TTS
```

### 2. Create and activate virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

##  Requirements

Make sure `requirements.txt` includes:

```
streamlit
torch
transformers
pandas
soundfile
```

---

## Deployment

This app is deployed on **Streamlit Cloud** and works without any API keys or tokens because the model is public and downloaded locally by the `transformers` library.


## License

This project is open-source and available for educational and research purposes.
