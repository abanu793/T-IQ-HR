import os
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

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
# LOAD ALL IMAGES (recursive)
# -----------------------
image_files = []
for root, dirs, files in os.walk(IMAGES_DIR):
    for f in files:
        if f.lower().endswith((".png", ".jpg", ".jpeg")):
            image_files.append(os.path.join(root, f))

if len(image_files) == 0:
    raise ValueError(f"No images found in folder: {IMAGES_DIR}")

print(f"[INFO] Found {len(image_files)} images to predict.")

# -----------------------
# PREDICT
# -----------------------
results = []

for img_path in image_files:
    img = load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array, verbose=0)[0][0]
    label = "real" if pred >= 0.5 else "fake"

    results.append({"image_path": img_path, "prediction": label, "score": float(pred)})

# -----------------------
# SAVE RESULTS
# -----------------------
df_results = pd.DataFrame(results)
df_results.to_csv(OUTPUT_CSV, index=False)
print(f"[INFO] Predictions saved to: {OUTPUT_CSV}")
print(df_results.head())
