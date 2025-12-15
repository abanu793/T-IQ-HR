import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import mysql.connector

# -----------------------
# CONFIGURATION
# -----------------------
MODEL_PATH = r"C:\Users\abanu\Documents\t_iq_hr\models\resume_cnn_test.h5"
IMG_HEIGHT, IMG_WIDTH = 128, 128

IMAGES_DIR = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_images"
OUTPUT_CSV = (
    r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_cnn_predictions.csv"
)

# -----------------------
# LOAD MODEL
# -----------------------
model = load_model(MODEL_PATH)
print("[INFO] Model loaded.")

# -----------------------
# LOAD ALL IMAGES
# -----------------------
image_files = []
for root, _, files in os.walk(IMAGES_DIR):
    for f in files:
        if f.lower().endswith((".png", ".jpg", ".jpeg")):
            image_files.append(os.path.join(root, f))

if not image_files:
    raise ValueError("No images found")

print(f"[INFO] Found {len(image_files)} images to predict.")

# -----------------------
# RUN PREDICTIONS
# -----------------------
results = []

for img_path in image_files:
    img = load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    score = float(model.predict(img_array, verbose=0)[0][0])
    label = "real" if score >= 0.5 else "fake"

    results.append(
        {
            "file_name": os.path.basename(img_path),
            "file_path": img_path,
            "prediction": label,
            "score": score,
        }
    )

# -----------------------
# SAVE CSV
# -----------------------
df_results = pd.DataFrame(results)
df_results.to_csv(OUTPUT_CSV, index=False)

print(f"[INFO] Predictions saved to: {OUTPUT_CSV}")
print(df_results.head())

# ===============================
# SAVE TO MYSQL (FINAL & CORRECT)
# ===============================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aira",
    database="t_iq_hr",
)

cursor = conn.cursor()

insert_resume_sql = """
INSERT INTO resumes (file_name, file_path)
VALUES (%s, %s)
"""

insert_prediction_sql = """
INSERT INTO predictions
(resume_id, fake_probability, predicted_label, model_version)
VALUES (%s, %s, %s, %s)
"""

for _, row in df_results.iterrows():

    # 1️.Insert resume
    cursor.execute(
        insert_resume_sql,
        (row["file_name"], row["file_path"]),
    )
    resume_id = cursor.lastrowid

    # 2️.Insert prediction
    cursor.execute(
        insert_prediction_sql,
        (
            resume_id,
            row["score"],
            row["prediction"],
            "v1_cnn",
        ),
    )

conn.commit()
cursor.close()
conn.close()

print("All resumes & predictions inserted successfully")
