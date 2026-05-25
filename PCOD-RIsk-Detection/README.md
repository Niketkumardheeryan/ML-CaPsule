# PCOS Detection System 🌸

AI-powered healthcare dashboard for predicting **PCOS (Polycystic Ovary Syndrome)** risk using **Machine Learning**, **XGBoost**, **SHAP Explainability**, and **Streamlit**.

This project provides:
- PCOS risk prediction
- Prediction confidence score
- SHAP-based AI explainability
- Personalized healthcare guidance dashboard
- Modern healthcare UI design

---

# 🚀 Features

## ✅ AI-Based PCOS Prediction
Predicts the likelihood of PCOS using clinical parameters.

## 📊 SHAP Explainability
Shows which features influenced the prediction most.

## 🌸 Modern Healthcare Dashboard
Clean pink-themed responsive Streamlit interface.

## 🧠 Personalized Guidance
Displays different recommendations based on:
- High PCOS risk
- Low PCOS risk

## 📋 Multi-Page Streamlit App
Includes:
- Home Prediction Page
- Dashboard Page

---

# 🛠️ Tech Stack

- Python
- Streamlit
- XGBoost
- SHAP
- NumPy
- Joblib
- Matplotlib

---

# 📂 Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── models/
│   └── pcos_grid_model.pkl
│
└── README.md
```

---

# 📈 Machine Learning Model

The model was trained using:
- XGBoost Classifier
- Hyperparameter tuning
- Cross-validation

### Features Used

```text
Follicle No. (R)
Follicle No. (L)
Skin darkening (Y/N)
Weight gain(Y/N)
hair growth(Y/N)
AMH(ng/mL)
Cycle(R/I)
LH(mIU/mL)
FSH/LH
Cycle length(days)
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone <your-repository-link>
cd <repository-folder>
```

---

## 2. Create Virtual Environment (Optional but Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run The Application

Start Streamlit app:

```bash
streamlit run app.py
```

After running, Streamlit will automatically open the application in your browser.

Usually at:

```text
http://localhost:8501
```

---

# 🖥️ What You Will See

## 🏠 Home Page

The Home page contains:
- PCOS prediction form
- Clinical parameter inputs
- Prediction button

### User Inputs
The user enters:
- Follicle counts
- Hormonal values
- Menstrual cycle information
- Symptoms like:
  - hair growth
  - skin darkening
  - weight gain

### Prediction Result
After clicking:

```text
🔍 Check PCOS Risk
```

The system displays:
- PCOS Risk Status
- Confidence Score
- SHAP Explainability Graph

---

# 🧠 SHAP Explainability

The app uses SHAP (SHapley Additive exPlanations) to explain:
- which features increased PCOS risk
- which features decreased PCOS risk

This improves:
- model transparency
- interpretability
- healthcare AI trustworthiness

---

# 📊 Dashboard Page

The Dashboard page provides:
- Personalized healthcare guidance
- Lifestyle recommendations
- Medical recommendations
- Preventive care suggestions

Different recommendations are shown based on:
- High PCOS Risk
- Low PCOS Risk

---

# 🌸 UI Highlights

- Soft pink medical theme
- Modern dashboard layout
- Responsive design
- Sidebar navigation
- Professional healthcare styling

---

# 📌 Example Prediction Output

## High Risk

```text
⚠️ High PCOS Risk Detected
Confidence Score: 89.64%
```

## Low Risk

```text
✅ Low PCOS Risk
Confidence Score: 87.42%
```

---

# ⚠️ Medical Disclaimer

This project is for:
- educational purposes
- machine learning demonstration
- portfolio showcase

It is NOT:
- a medical diagnosis system
- a replacement for professional healthcare consultation

Always consult a qualified healthcare professional for medical advice.

---

# 📷 Future Improvements

Planned upgrades:
- PDF report generation
- ROC-AUC visualization
- Feature importance dashboard
- User authentication
- Cloud deployment
- Mobile optimization
- Database integration

---

# 👨‍💻 Author

Developed as an AI/ML healthcare portfolio project using:
- XGBoost
- Streamlit
- SHAP Explainability
- Python

🌸 AI for Women's Healthcare