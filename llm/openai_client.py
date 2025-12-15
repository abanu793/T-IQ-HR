import os
import random
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI

    OPENAI_INSTALLED = True
except ImportError:
    OPENAI_INSTALLED = False

OPENAI_AVAILABLE = False
client = None

if OPENAI_INSTALLED:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
        OPENAI_AVAILABLE = True


# Predefined lists for smarter dummy generation
DUMMY_NAMES = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Lee", "Charlie Kim"]
DUMMY_SKILLS = [
    "Python",
    "Excel",
    "SQL",
    "Machine Learning",
    "Data Analysis",
    "Communication",
    "Leadership",
]


def generate_dummy_response(fit_score=None):
    name = random.choice(DUMMY_NAMES)
    years_exp = random.randint(2, 8)
    skills = random.sample(DUMMY_SKILLS, 3)
    gaps = random.sample([s for s in DUMMY_SKILLS if s not in skills], 2)
    recommendation = random.choice(["Hire", "Consider", "Reject"])
    fit_score_val = fit_score if fit_score else round(random.uniform(65, 90), 2)

    response = f"""
Candidate Summary: {name}, {years_exp} years of experience, skilled in {', '.join(skills)}.
Strengths: {', '.join(skills)}.
Weaknesses / Skill Gaps: {', '.join(gaps)}.
Suggested Interview Questions:
1. How would you apply {skills[0]} in a real project?
2. Can you describe a challenge you faced using {skills[1]}?
3. How do you improve your {skills[2]} skills?
Hiring Recommendation: {recommendation}.
Fit Score: {fit_score_val}%.
"""
    return response.strip()


def call_llm(prompt: str) -> (str, bool):
    if not OPENAI_AVAILABLE or client is None:
        # Smarter dummy response
        return generate_dummy_response(), False

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional HR recruiter."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content, True
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Fallback to smarter dummy
        return generate_dummy_response(), False
