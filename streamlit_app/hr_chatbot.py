import sys
import os
import re
import streamlit as st

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from resume_assistant.resume_agent import analyze_resume
from resume_assistant.resume_parser import extract_resume_text

st.set_page_config(page_title="GPT-Powered HR Assistant", layout="wide")
st.title("GPT-Powered HR Assistant")
st.write("Upload a candidate resume (PDF) and paste the Job Description (JD) below.")

jd_text = st.text_area("Paste Job Description", height=200)
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Analyze Resume"):
    if not resume_file or not jd_text.strip():
        st.warning("Please upload a resume and provide a job description.")
    else:
        with st.spinner("Analyzing resume with GPT..."):
            try:
                fit_score, analysis, is_real_gpt = analyze_resume(resume_file, jd_text)
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                fit_score, analysis, is_real_gpt = None, None, False

        if fit_score is not None:
            # Badge for GPT response
            if is_real_gpt:
                st.success("Real GPT-3.5-turbo response")
            else:
                st.info("🛈 Demo Mode: Dummy GPT response active")

            st.subheader(f"Candidate Fit Score: {fit_score}%")
            st.markdown("---")

            # Structured display of analysis
            sections = [
                "Candidate Summary",
                "Strengths",
                "Weaknesses / Skill Gaps",
                "Suggested Interview Questions",
                "Hiring Recommendation",
                "Fit Score",
            ]

            for section in sections:
                st.markdown(f"### {section}")
                # Try to extract section text from GPT/dummy response
                pattern = rf"{section}[:\n]+(.*?)(?=\n[A-Z][a-z]+|\Z)"
                match = re.search(pattern, analysis, re.DOTALL)
                if match:
                    st.markdown(match.group(1).strip())
                else:
                    # Fallback: show full analysis if section not found
                    st.markdown(analysis)

            st.markdown("---")

            with st.expander("Preview Resume Text"):
                text = extract_resume_text(resume_file)
                st.text_area("Resume Text", text, height=300)

st.caption("T-IQ HR | GPT-3.5-turbo | Resume Assistant | Demo Mode supported")
