T-IQ HR — Intelligent Talent Insights & Qualification System

T-IQ HR is an AI-powered HR intelligence platform designed to analyze resumes, detect authenticity, extract skills, and support smarter hiring decisions.

The system combines computer vision (CNNs), machine learning, database-backed pipelines, and interactive dashboards to deliver end-to-end talent insights.

🚀 Key Features
✅ Resume Authenticity Detection (CNN)

Converts resumes (PDF → images)

Classifies resumes as Real vs Fake

Trained using:

Real resumes dataset

Synthetic fake resumes generated using Faker

Image-based deep learning using TensorFlow / Keras

✅ Resume Image Processing Pipeline

Recursive PDF ingestion

Page-level image extraction using Poppler

Label generation & dataset balancing

CSV-based training metadata

✅ Machine Learning & Deep Learning

CNN-based binary classifier

Classical ML baselines (Logistic Regression, etc.)

Metrics tracked:

Accuracy

ROC-AUC

Validation loss

✅ Database Integration (MySQL)

Normalized schema:

resumes

predictions

Foreign-key enforced consistency

Model versioning per prediction

✅ Streamlit HR Dashboard

Resume selection & filtering

Page-level predictions

Resume-level authenticity decision

Confidence score visualization

📁 Project Structure
t-iq-hr/
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   │   └── resumes/
│   │       ├── real/
│   │       └── fake/
│   ├── processed/
│   │   └── resume_images/
│   │       ├── real/
│   │       ├── fake/
│   │       └── resume_images_labels.csv
│
├── models/
│   ├── resume_cnn_v1.h5
│   ├── resume_cnn_v2.keras
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_Attrition_Model.ipynb
│   ├── 04_performance_model.ipynb
│   ├── 05_Jobs_Analysis_and_Predictions.ipynb
│   ├── 06_Resume_Parsing.ipynb
│   ├── 07_Attrition_Prediction_Inference.ipynb
│   ├── 08_Performance_Prediction_Inference.ipynb
│   ├── 09_Integrated_HR_Dashboard.ipynb
│   ├── 10_HR_Insights_and_Recommendations.ipynb
│   └── 11_Resume_CNN_Analysis.ipynb
│
├── scripts/
│   ├── convert_pdfs_to_images.py
│   ├── generate_fake_resumes.py
│   ├── train_resume_cnn.py
│   └── resume_cnn_inference.py
│
├── requirements.txt
├── README.md
└── .gitignore


📓 Notebooks Overview (Actual Implementation)

This project is supported by 11 well-structured Jupyter notebooks, covering the full HR analytics and AI pipeline — from EDA to deep learning and decision insights.

🧪 Exploratory & Data Preparation
Notebook	Purpose
01_EDA.ipynb	Exploratory Data Analysis on HR & resume datasets
02_Data_Cleaning.ipynb	Data cleaning, preprocessing, missing values handling
📉 HR Analytics & Classical ML
Notebook	Purpose
03_Attrition_Model.ipynb	Employee attrition prediction model
04_performance_model.ipynb	Employee performance prediction
05_Jobs_Analysis_and_Predictions.ipynb	Job role analysis & hiring trends
📄 Resume Intelligence
Notebook	Purpose
06_Resume_Parsing.ipynb	Resume text extraction & NLP-based parsing
11_Resume_CNN_Analysis.ipynb	CNN-based resume authenticity detection
🔍 Model Inference & Integration
Notebook	Purpose
07_Attrition_Prediction_Inference.ipynb	Attrition model inference
08_Performance_Prediction_Inference.ipynb	Performance model inference
09_Integrated_HR_Dashboard.ipynb	Combined analytics for HR decision-making
10_HR_Insights_and_Recommendations.ipynb	Actionable HR insights & recommendations

📌 These notebooks serve as:

Experiment logs

Model justification

Research documentation

📊 Dataset Summary
Class	Count
Real resume images	~4,800
Fake resume images	~1,200
Total	~6,000+

✔ Multi-page resumes supported
✔ Balanced using synthetic data

🧠 Model Training Highlights

Framework: TensorFlow / Keras

Input: 128 × 128 × 3

Loss: Binary Crossentropy

Optimizer: Adam

Primary metric: ROC-AUC

Accuracy is threshold-dependent.
ROC-AUC is used for real-world decision quality.

🛠 Setup Instructions
1️⃣ Clone repository
git clone https://github.com/abanu793/t-iq-hr.git
cd t-iq-hr

2️⃣ Create virtual environment
python -m venv env
env\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Install Poppler (Windows)

Download Poppler

Add poppler/Library/bin to system PATH

Verify:

pdftoppm -h

▶️ Running the Pipeline
python scripts/convert_pdfs_to_images.py
python scripts/generate_fake_resumes.py
python scripts/train_resume_cnn.py
python scripts/resume_cnn_inference.py
streamlit run app/streamlit_app.py

🔮 Roadmap

🔲 Multimodal (image + text) resume model

🔲 Job–resume matching engine

🔲 Skill gap analysis

🔲 Candidate ranking

🔲 Admin analytics dashboard

🔲 Model monitoring & drift detection

👩‍💻 Author

Asma Banu
AI / ML Engineer
GitHub: https://github.com/abanu793