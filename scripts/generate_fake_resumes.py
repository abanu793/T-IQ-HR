import os
from faker import Faker
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random

fake = Faker()

# CORRECT LOCATION (RAW PDFs)
OUTPUT_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\raw\resumes\fake"

NUM_RESUMES = 1200  # RECOMMENDED

os.makedirs(OUTPUT_DIR, exist_ok=True)

SKILLS = [
    "Python",
    "Java",
    "SQL",
    "Machine Learning",
    "Excel",
    "Data Analysis",
    "Deep Learning",
    "NLP",
    "TensorFlow",
    "Communication",
    "Leadership",
]


def create_fake_resume(path):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, fake.name())
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, fake.email())
    y -= 20
    c.drawString(50, y, fake.phone_number())
    y -= 30

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Summary")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(50, y, fake.text(max_nb_chars=120))
    y -= 40

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Skills")
    y -= 20
    c.setFont("Helvetica", 11)
    skills = ", ".join(random.sample(SKILLS, k=5))
    c.drawString(50, y, skills)
    y -= 40

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Experience")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(50, y, fake.job())
    y -= 20
    c.drawString(50, y, fake.company())

    c.showPage()
    c.save()


for i in range(1, NUM_RESUMES + 1):
    pdf_path = os.path.join(OUTPUT_DIR, f"FAKE_{i}.pdf")
    create_fake_resume(pdf_path)

print(f"[✅] Generated {NUM_RESUMES} fake resume PDFs")
