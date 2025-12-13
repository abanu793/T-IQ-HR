import os
from faker import Faker
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random

fake = Faker()

OUTPUT_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images\fake"
NUM_RESUMES = 500  # 🔥 increase here (500 or 1000)

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


def create_fake_resume(path, idx):
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


for i in range(51, 51 + NUM_RESUMES):
    pdf_path = os.path.join(OUTPUT_DIR, f"FAKE_{i}.pdf")
    create_fake_resume(pdf_path, i)

print(f"[OK] Generated {NUM_RESUMES} fake resume PDFs.")
