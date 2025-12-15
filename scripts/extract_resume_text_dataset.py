# ===============================================
# extract_resume_text_dataset.py (FAST + CACHED)
# ===============================================

import os
import pytesseract
from pdf2image import convert_from_path
import pandas as pd

# -----------------------
# CONFIGURATION
# -----------------------
RAW_DIR_REAL = r"C:\Users\abanu\Documents\t_iq_hr\data\raw\resumes\data\data"
RAW_DIR_FAKE = r"C:\Users\abanu\Documents\t_iq_hr\data\raw\resumes\fake"

POPPLER_PATH = r"C:\Users\abanu\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

OUTPUT_CSV = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_text_dataset.csv"
PROCESSED_LOG = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\processed_pdfs.txt"

MIN_TEXT_LEN = 50
DPI = 200  # speed boost (300 is overkill)

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# -----------------------
# LOAD PROCESSED FILES
# -----------------------
processed_files = set()
if os.path.exists(PROCESSED_LOG):
    with open(PROCESSED_LOG, "r", encoding="utf-8") as f:
        processed_files = set(line.strip() for line in f.readlines())

print(f"🔁 Already processed PDFs: {len(processed_files)}")

# -----------------------
# LOAD EXISTING CSV (resume-safe)
# -----------------------
if os.path.exists(OUTPUT_CSV):
    df_existing = pd.read_csv(OUTPUT_CSV)
    data = df_existing.to_dict("records")
    print(f" Loaded existing records: {len(data)}")
else:
    data = []


# -----------------------
# OCR FUNCTION
# -----------------------
def extract_text_from_pdf(pdf_path):
    texts = []
    try:
        images = convert_from_path(pdf_path, dpi=DPI, poppler_path=POPPLER_PATH)
        for img in images:
            text = pytesseract.image_to_string(img)
            texts.append(text)
    except Exception as e:
        print(f"[ERROR] {pdf_path}: {e}")
    return "\n".join(texts)


# -----------------------
# MAIN LOOP
# -----------------------
def process_folder(label, folder):
    global data

    if not os.path.exists(folder):
        print(f"[WARNING] Folder not found: {folder}")
        return

    for root, _, files in os.walk(folder):
        for file in files:
            if not file.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(root, file)

            if pdf_path in processed_files:
                continue  # skip already done

            print(f" OCR → {file}")

            text = extract_text_from_pdf(pdf_path)

            if len(text.strip()) >= MIN_TEXT_LEN:
                data.append({"file_name": file, "text": text, "label": label})

                # SAVE IMMEDIATELY
                pd.DataFrame(data).to_csv(OUTPUT_CSV, index=False)

            # LOG PROCESSED FILE
            with open(PROCESSED_LOG, "a", encoding="utf-8") as f:
                f.write(pdf_path + "\n")

            processed_files.add(pdf_path)


# -----------------------
# RUN
# -----------------------
process_folder("real", RAW_DIR_REAL)
process_folder("fake", RAW_DIR_FAKE)

print("\n EXTRACTION COMPLETE")
df = pd.DataFrame(data)
print(df["label"].value_counts())
print(f" Saved at: {OUTPUT_CSV}")
