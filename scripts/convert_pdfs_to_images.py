import os
import pandas as pd
from pdf2image import convert_from_path

# -----------------------
# CONFIGURATION
# -----------------------
RAW_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\raw\resumes"
OUTPUT_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images"
CSV_PATH = os.path.join(OUTPUT_DIR, "resume_images_labels.csv")

POPPLER_PATH = r"C:\Users\abanu\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

# -----------------------
# PREPARE OUTPUT DIRS
# -----------------------
REAL_DIR = os.path.join(OUTPUT_DIR, "real")
FAKE_DIR = os.path.join(OUTPUT_DIR, "fake")

os.makedirs(REAL_DIR, exist_ok=True)
os.makedirs(FAKE_DIR, exist_ok=True)


# -----------------------
# PDF → IMAGE FUNCTION
# -----------------------
def convert_pdf(pdf_path, label):
    try:
        images = convert_from_path(pdf_path, dpi=200, poppler_path=POPPLER_PATH)
    except Exception as e:
        print(f"[ERROR] {pdf_path}: {e}")
        return []

    records = []
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    out_dir = REAL_DIR if label == "real" else FAKE_DIR

    for i, img in enumerate(images):
        img_name = f"{base}_page_{i+1}.png"
        img_path = os.path.join(out_dir, img_name)
        img.save(img_path, "PNG")

        records.append({"image_path": img_path, "label": label})

    print(f"[OK] {pdf_path} → {len(images)} images")
    return records


# -----------------------
# PROCESS ALL PDFs
# -----------------------
all_rows = []

for root, _, files in os.walk(RAW_DIR):
    for file in files:
        if not file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(root, file)

        # ✅ LABEL LOGIC (FINAL & SAFE)
        label = "fake" if "fake" in root.lower() or "fake" in file.lower() else "real"

        all_rows.extend(convert_pdf(pdf_path, label))

# -----------------------
# SAVE CSV
# -----------------------
if not all_rows:
    raise RuntimeError("❌ No images generated. Check paths.")

df = pd.DataFrame(all_rows)
df.to_csv(CSV_PATH, index=False)

print("\n✅ DATASET READY")
print(df["label"].value_counts())
print(f"\nCSV saved at: {CSV_PATH}")
