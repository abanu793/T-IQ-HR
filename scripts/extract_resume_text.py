import os
import pdfplumber
import pandas as pd

RAW_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\raw\resumes"
OUT_CSV = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_text_dataset.csv"

records = []

for label in ["real", "fake"]:
    folder = os.path.join(RAW_DIR, label)
    if not os.path.exists(folder):
        continue

    for file in os.listdir(folder):
        if not file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(folder, file)

        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except:
            continue

        if len(text.strip()) < 200:
            continue

        records.append({"file_name": file, "text": text, "label": label})

df = pd.DataFrame(records)
df.to_csv(OUT_CSV, index=False)

print("Text dataset created")
print(df["label"].value_counts())
