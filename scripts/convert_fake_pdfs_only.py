import os
import pandas as pd
from pdf2image import convert_from_path

# ==========================
# PATHS (LOCKED TO FAKE ONLY)
# ==========================
FAKE_PDF_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images\fake"
CSV_PATH = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images\resume_images_labels.csv"

# Safety check
assert "fake" in FAKE_PDF_DIR.lower(), "❌ Path is not a fake directory!"

# Load existing CSV
df = pd.read_csv(CSV_PATH)

new_rows = []

for pdf in os.listdir(FAKE_PDF_DIR):
    if not pdf.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(FAKE_PDF_DIR, pdf)
    base = os.path.splitext(pdf)[0]

    try:
        pages = convert_from_path(pdf_path, dpi=200)
        for i, page in enumerate(pages):
            img_name = f"{base}_page{i+1}.png"
            img_path = os.path.join(FAKE_PDF_DIR, img_name)
            page.save(img_path, "PNG")

            new_rows.append({"image_path": img_path, "label": "fake"})

        print(f"[OK] {pdf} → {len(pages)} images")

    except Exception as e:
        print(f"[ERROR] {pdf}: {e}")

# Append only fake rows
if new_rows:
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    print(f"\n✅ Added {len(new_rows)} FAKE images to CSV")
else:
    print("\n⚠️ No fake images added")
