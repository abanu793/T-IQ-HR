def resume_analysis_prompt(resume_text, jd_text, fit_score):
    return f"""
You are an expert HR assistant. Analyze the candidate's resume below:

Resume:
{resume_text}

Job Description:
{jd_text}

Tasks:
1. Provide a concise candidate summary.
2. List key strengths and relevant skills.
3. Identify weaknesses or skill gaps.
4. Suggest 3–5 interview questions tailored to this candidate.
5. Give a hiring recommendation (Hire / Consider / Reject).
6. Comment on the pre-calculated fit score: {fit_score}% — validate or explain.

Be structured, clear, and professional in your response.
"""
