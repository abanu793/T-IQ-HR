# T-IQ HR — Intelligent Talent Insights & Qualification System

T-IQ HR is an AI-powered talent analytics platform designed to help organizations evaluate candidates, optimize hiring decisions, and automate HR workflows.  
This project includes modules for **resume parsing**, **job–candidate matching**, **skill extraction**, and **ML-based prediction models**.

---

## 🚀 Project Overview

The goal of **T-IQ HR** is to build an end-to-end intelligence system that supports:

### 🔹 1. Resume Understanding  
- Automatic resume parsing  
- Extraction of skills, education, experience  
- Classification of candidate profile

### 🔹 2. Job Description Analysis  
- JD parsing  
- Skill matching  
- Role suitability scoring

### 🔹 3. ML-Based Candidate Scoring  
- Machine learning classification models  
- Predictive score based on candidate–job fit  
- ROC-AUC, F1-Score and confusion matrix analysis

### 🔹 4. HR Decision Dashboard *(upcoming)*  
- Streamlit UI for HR teams  
- Visualization of scores & metrics  
- Candidate ranking dashboard  

---

## 📁 Project Structure (current / planned)

t-iq-hr/
├─ data/
│ ├─ raw/
│ ├─ processed/
├─ models/
│ ├─ logistic_regression.pkl
│ ├─ scaler.pkl
│ ├─ vectorizers/
├─ notebooks/
│ ├─ 01_data_cleaning.ipynb
│ ├─ 02_feature_engineering.ipynb
│ ├─ 03_model_training.ipynb
│ └─ 04_evaluation.ipynb
├─ utils/
│ ├─ preprocessing.py
│ ├─ feature_extraction.py
│ ├─ model_utils.py
│ └─ file_loader.py
├─ app/ # Streamlit app (to be added)
│ └─ app.py # (Coming soon)
├─ requirements.txt
├─ README.md
└─ .gitignore


---

## 🧠 ML Models Used (so far)

### ✔ Logistic Regression (balanced)  
- Used for classification  
- Good performance on imbalanced data  

### ✔ Scalers  
- StandardScaler  
- MinMaxScaler *(depending on notebook)*  

Future models: **XGBoost, RandomForest, BERT-based resume ranking, embeddings**.

---

## 🛠 Setup Instructions (for developers)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/abanu793/t-iq-hr.git
cd t-iq-hr

python -m venv .venv
.\.venv\Scripts\Activate.ps1     # Windows
# or
source .venv/bin/activate        # Mac/Linux
pip install -r requirements.txt
📞 Contact

Author: Asma Banu
GitHub: @abanu793