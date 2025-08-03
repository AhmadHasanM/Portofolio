# 🧠 Lead Scoring Prediction Tool
A machine learning-powered lead scoring application built as part of the Caprae Capital AI Readiness Pre-Screening Challenge.

This tool evaluates the potential quality of a lead based on key company attributes such as revenue, growth rate, employee count, industry, and location. It helps sales teams prioritize which companies to target for higher conversion rates.

---

## 🚀 Project Overview

- Goal: Predict whether a company lead is "high-value" based on historical data
- Model: Random Forest Classifier (scikit-learn)
- Interface: Streamlit app for simple interactive use
- Deployment: Streamlit Cloud

---

## 🧩 Features

✅ Cleaned company dataset  
✅ Preprocessing (encoding, normalization, label creation)  
✅ Lead classification model with >90% accuracy  
✅ Interactive Streamlit interface with user inputs  
✅ Confidence score with prediction  
✅ Ready-to-deploy via GitHub + Streamlit Cloud  

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| Python | Core programming language |
| Pandas | Data preprocessing |
| Scikit-learn | Machine learning model |
| Joblib | Model serialization |
| Streamlit | Web app interface |
| GitHub | Version control & deployment base |

---

## 📊 Dataset Features

- **Industri**: Categorical (encoded)
- **Revenue (USD millions)**: Numeric
- **Revenue growth (%)**: Numeric
- **Employees**: Numeric
- **State**: Location code
- **Converted**: Label (1 = valuable lead, 0 = not valuable)

---

## ⚙️ How to Run Locally

1. **Clone the repository**

bash
git clone https://github.com/yourusername/lead-scoring-app.git
cd lead-scoring-app

2. **Install dependencies**
pip install -r requirements.txt

3. **Run the Streamlit app**
streamlit run app.py

📎 Demo Links
🔗 App: https://yourname-lead-scoring-app.streamlit.app
