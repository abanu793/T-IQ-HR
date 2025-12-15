from resume_assistant.resume_parser import extract_resume_text
from resume_assistant.resume_scorer import calculate_fit_score
from llm.openai_client import call_llm


def analyze_resume(pdf_file, jd_text):
    """
    Analyze a candidate's resume against a Job Description (JD) using GPT-3.5-turbo.
    Returns:
        fit_score: numeric fit score
        analysis: GPT analysis text
        is_real_gpt: boolean flag, True if GPT API succeeded, False if dummy fallback
    """
    # 1️⃣ Extract resume text
    resume_text = extract_resume_text(pdf_file)

    # 2️⃣ Calculate fit score
    fit_score = calculate_fit_score(resume_text, jd_text)

    # 3️⃣ Prepare enhanced GPT prompt for full HR analysis
    prompt = f"""
You are an expert HR assistant. Analyze the candidate's resume below:

Resume:
{resume_text}

Job Description:
{jd_text}

Tasks:
1. Provide a concise candidate summary.
2. List strengths and relevant skills.
3. Identify weaknesses or gaps.
4. Suggest 3–5 interview questions tailored to this candidate.
5. Give a hiring recommendation (Hire / Consider / Reject).
6. Validate or comment on the calculated fit score: {fit_score}%.

Be clear, structured, and professional.
"""

    # 4️⃣ Call GPT (returns analysis text + boolean flag if real GPT)
    analysis, is_real_gpt = call_llm(prompt)

    # 5️⃣ Return 3 values
    return fit_score, analysis, is_real_gpt
