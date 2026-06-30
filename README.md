# AI Resume Analyzer & Job Recommendation System

An AI-powered application that analyzes resumes using NLP and Machine Learning to
extract skills, predict suitable job roles, recommend jobs, calculate resume scores,
and identify skill gaps.

## 🚀 Features
- Resume parsing (PDF & DOCX)
- NLP-based text preprocessing
- Skill extraction using keyword & phrase matching
- Job role prediction using ML (TF-IDF + Logistic Regression)
- Content-based job recommendation using cosine similarity
- Resume scoring system
- Skill gap analysis
- Interactive Streamlit dashboard

## 🛠 Tech Stack
- Python
- Streamlit
- spaCy, NLTK
- scikit-learn
- pandas, numpy


## ▶️ How to Run
```bash
git clone <repo-url>
cd resume_analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python ml/train_model.py
streamlit run app.py

```


## 🚀 Production Run
For a production-style local or container deployment:

1. Keep `en_core_web_sm` installed in the runtime image or environment.
2. Set `MAX_FILE_SIZE_MB`, `LOG_LEVEL`, or `ENABLE_FILE_LOGGING` as needed.
3. Run the app behind a process manager or Docker container using `streamlit run app.py`.

### Docker
```bash
docker build -t resume-analyzer .
docker run -p 8501:8501 resume-analyzer
```

The bundled Streamlit configuration disables browser usage stats, runs headless, and sets the upload limit to match the app.

