# ======================================================
# train_resume_text_model.py
# ======================================================

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

# -----------------------
# CONFIG
# -----------------------
DATA_PATH = r"C:\Users\abanu\Documents\t_iq_hr\data\processed\resume_text_dataset.csv"
MODEL_DIR = r"C:\Users\abanu\Documents\t_iq_hr\models"

MODEL_PATH = f"{MODEL_DIR}\\resume_text_classifier.pkl"
VECT_PATH = f"{MODEL_DIR}\\resume_text_vectorizer.pkl"

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv(DATA_PATH)

df = df.dropna()
df["label"] = df["label"].map({"real": 0, "fake": 1})

X = df["text"]
y = df["label"]

# -----------------------
# SPLIT DATA
# -----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# -----------------------
# VECTORIZATION
# -----------------------
vectorizer = TfidfVectorizer(
    max_features=50000, ngram_range=(1, 2), stop_words="english", min_df=3
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------
# MODEL
# -----------------------
model = LogisticRegression(max_iter=1000, class_weight="balanced", n_jobs=-1)

model.fit(X_train_vec, y_train)

# -----------------------
# EVALUATION
# -----------------------
y_pred = model.predict(X_test_vec)
y_prob = model.predict_proba(X_test_vec)[:, 1]

print("\n CLASSIFICATION REPORT\n")
print(classification_report(y_test, y_pred, target_names=["REAL", "FAKE"]))

print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# -----------------------
# SAVE MODEL
# -----------------------
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECT_PATH)

print("\n MODEL SAVED")
print("Model:", MODEL_PATH)
print("Vectorizer:", VECT_PATH)
