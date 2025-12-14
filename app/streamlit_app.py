import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

st.set_page_config(page_title="Resume Authenticity Dashboard", layout="wide")
st.title("📝 Resume Authenticity Dashboard")

# -----------------------
# DB CONNECTION
# -----------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aira",  # 🔑 update
    database="t_iq_hr",
)
df = pd.read_sql(
    "SELECT r.file_name, r.file_path, p.fake_probability, p.predicted_label, p.model_version, p.predicted_at FROM predictions p JOIN resumes r ON p.resume_id = r.resume_id",
    conn,
)
conn.close()

# -----------------------
# FIX LOGIC
# -----------------------
FAKE_PROB_THRESHOLD = 0.5  # page-level
FAKE_PAGE_RATIO = 0.5  # resume-level

df["real_probability"] = 1 - df["fake_probability"]
df["is_fake_page"] = df["fake_probability"] >= FAKE_PROB_THRESHOLD

# -----------------------
# RESUME SUMMARY
# -----------------------
summary = (
    df.groupby("file_name")
    .agg(
        total_pages=("file_name", "count"),
        fake_pages=("is_fake_page", "sum"),
        max_fake_prob=("fake_probability", "max"),
    )
    .reset_index()
)

summary["is_fake_resume"] = (
    summary["fake_pages"] / summary["total_pages"] >= FAKE_PAGE_RATIO
)

st.subheader("Resume Summary")
st.dataframe(summary)

# -----------------------
# SELECT RESUME
# -----------------------
selected_resume = st.selectbox("Select Resume", summary["file_name"].tolist())

if selected_resume:
    resume_pages = df[df["file_name"] == selected_resume].copy()
    st.subheader(f"Page-level details: {selected_resume}")
    st.dataframe(resume_pages[["file_name", "predicted_label", "fake_probability"]])

    final_row = summary[summary["file_name"] == selected_resume].iloc[0]
    st.markdown(
        f"**Resume-level verdict:** {'🚨 FAKE' if final_row['is_fake_resume'] else '✅ REAL'}"
    )
    st.markdown(f"**Max fake probability:** {final_row['max_fake_prob']:.2f}")
    st.markdown(
        f"**Total pages:** {final_row['total_pages']}, Fake pages: {final_row['fake_pages']}"
    )
