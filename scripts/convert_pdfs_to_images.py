from pdf2image import convert_from_path
import os
import pandas as pd

# ---------------------------
# CONFIGURATION
# ---------------------------
PDF_ROOT = r"C:\Users\abanu\Documents\t_iq_hr\data\raw\resumes\data\data"
OUTPUT_ROOT = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images"
REAL_FOLDER = os.path.join(OUTPUT_ROOT, "real")
FAKE_FOLDER = os.path.join(OUTPUT_ROOT, "fake")

os.makedirs(REAL_FOLDER, exist_ok=True)
os.makedirs(FAKE_FOLDER, exist_ok=True)

# Poppler path
POPPLER_PATH = r"C:\Users\abanu\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"


# ---------------------------
# FUNCTION TO CONVERT PDFs
# ---------------------------
def convert_pdfs(folder_path, output_folder, label="real"):
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(subdir, file)
                try:
                    pages = convert_from_path(
                        pdf_path, dpi=200, poppler_path=POPPLER_PATH
                    )
                    for i, page in enumerate(pages):
                        output_file = os.path.join(
                            output_folder, f"{file[:-4]}_page_{i+1}.png"
                        )
                        page.save(output_file, "PNG")
                    print(f"[OK] Converted {pdf_path} -> {len(pages)} images")
                except Exception as e:
                    print(f"[ERROR] {pdf_path}: {e}")


# ---------------------------
# PROCESS ALL SUBFOLDERS
# ---------------------------
convert_pdfs(PDF_ROOT, REAL_FOLDER, label="real")

# ---------------------------
# CREATE CSV FILE
# ---------------------------
data = []
for folder, label in [(REAL_FOLDER, "real"), (FAKE_FOLDER, "fake")]:
    for img_file in os.listdir(folder):
        if img_file.lower().endswith(".png"):
            data.append({"image_path": os.path.join(folder, img_file), "label": label})

df = pd.DataFrame(data)
csv_path = os.path.join(OUTPUT_ROOT, "resume_images_labels.csv")
df.to_csv(csv_path, index=False)
print(f"\nDataset CSV created: {csv_path}")
print(df.head())
