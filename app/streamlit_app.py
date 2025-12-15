# ======================================================
# streamlit_app.py
# ======================================================

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import joblib
import pdfplumber
from db.db_ops import insert_resume, insert_prediction

# -----------------------
# CONFIG
# -----------------------
MODEL_PATH = r"C:\Users\abanu\Documents\t_iq_hr\models\resume_text_classifier.pkl"
VECT_PATH = r"C:\Users\abanu\Documents\t_iq_hr\models\resume_text_vectorizer.pkl"

UPLOAD_DIR = r"C:\Users\abanu\Documents\t_iq_hr\uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="T-IQ HR Resume Authenticity", layout="centered")


# -----------------------
# LOAD MODEL
# -----------------------
@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECT_PATH)
    return model, vectorizer


model, vectorizer = load_model()


# -----------------------
# TEXT EXTRACTION
# -----------------------
def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")
    return text.strip()


# -----------------------
# PREDICTION
# -----------------------
def predict_resume(text):
    vec = vectorizer.transform([text])
    prob_fake = model.predict_proba(vec)[0][1]
    label = "fake" if prob_fake >= 0.5 else "real"
    confidence = prob_fake if label == "fake" else (1 - prob_fake)
    return label, confidence, prob_fake


# -----------------------
# UI
# -----------------------
st.title("T-IQ HR — Resume Authenticity Detector")
st.write("Upload a resume PDF to check whether it is **Real or Fake**")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    # Save PDF
    saved_pdf_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(saved_pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Extracting text & analyzing..."):
        text = extract_text_from_pdf(saved_pdf_path)

    if len(text) < 100:
        st.warning("⚠️ Not enough readable text found in resume.")
    else:
        label, confidence, fake_prob = predict_resume(text)

        # -----------------------
        # SAVE TO DATABASE
        # -----------------------
        resume_id = insert_resume(
            file_name=uploaded_file.name, file_path=saved_pdf_path
        )

        insert_prediction(
            resume_id=resume_id,
            fake_prob=float(fake_prob),
            label=label,
            model_version="v1_text",
        )

        # -----------------------
        # DISPLAY RESULT
        # -----------------------
        st.subheader("Prediction Result")

        if label == "fake":
            st.error("🚨 **FAKE RESUME DETECTED**")
        else:
            st.success("✅ **REAL RESUME**")

        st.metric("Confidence", f"{confidence * 100:.2f}%")
        st.caption(f"Raw fake probability: {fake_prob:.4f}")

        with st.expander("Extracted Resume Text"):
            st.text_area("Text", text, height=300)

st.markdown("---")
st.caption("T-IQ HR | Text-Based ML | MySQL Integrated | Production-Ready")
