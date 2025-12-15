# ===============================================
# extract_resume_text_ocr.py (FIXED + WINDOWS SAFE)
# ===============================================

import os
import pytesseract
import pandas as pd
from pdf2image import convert_from_path

# -----------------------
# CONFIG
# -----------------------
REAL_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\raw\resumes\data\data"
FAKE_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\raw\resumes\fake"

POPPLER_PATH = r"C:\Users\abanu\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"
OUTPUT_CSV = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_text_dataset.csv"

# Uncomment ONLY if tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -----------------------
# OCR FUNCTION
# -----------------------
def extract_text_from_pdf(pdf_path):
    text_parts = []
    try:
        images = convert_from_path(
            pdf_path,
            dpi=200,  # faster than 300, good enough for resumes
            poppler_path=POPPLER_PATH,
        )
        for img in images:
            txt = pytesseract.image_to_string(img)
            text_parts.append(txt)
    except Exception as e:
        print(f"[ERROR] {pdf_path} → {e}")

    return "\n".join(text_parts)


# -----------------------
# MAIN PIPELINE
# -----------------------
def main():
    data = []

    for label, folder in [("real", REAL_DIR), ("fake", FAKE_DIR)]:
        if not os.path.exists(folder):
            print(f"[WARNING] Folder not found: {folder}")
            continue

        print(f"\n Scanning {label.upper()} resumes from: {folder}")

        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    print(f"[INFO] OCR → {file}")

                    text = extract_text_from_pdf(pdf_path)

                    if len(text.strip()) > 50:
                        data.append({"file_name": file, "text": text, "label": label})

    if not data:
        print("\n[WARNING] No text extracted.")
        return

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_CSV, index=False)

    print("\n OCR TEXT DATASET CREATED SUCCESSFULLY")
    print(df["label"].value_counts())
    print(f" Saved at: {OUTPUT_CSV}")


# -----------------------
# WINDOWS ENTRY POINT
# -----------------------
if __name__ == "__main__":
    main()
