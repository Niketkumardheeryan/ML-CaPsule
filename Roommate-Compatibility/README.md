# AI Roommate Compatibility Predictor 🏠🤖

An AI-powered roommate matching system that predicts compatibility between two students using engineered behavioral features and a Deep Learning regression model.

Built with:

* PyTorch
* Streamlit
* Scikit-learn
* Feature Engineering
* Interactive UI/UX

---

# 🚀 Features

✅ Predicts roommate compatibility score (0–100)

✅ Deep Learning based compatibility prediction

✅ Advanced behavioral feature engineering

✅ Interactive modern Streamlit UI

✅ Dynamic compatibility analysis

✅ Conflict & similarity detection

✅ Compatibility insights and recommendations

✅ Real-time inference pipeline

✅ Beautiful animated glassmorphism UI

---

# 🧠 ML Pipeline

The system works using:

```text
Raw User Inputs
→ Feature Engineering
→ Top Feature Selection
→ Standard Scaling
→ Deep Learning Model
→ Compatibility Score
→ Detailed Analysis
```

---

# 📊 Engineered Features

The project uses:

* Difference Features
* Similarity Features
* Interaction Features

Examples:

* cleanliness_diff
* social_energy_diff
* academic_goal_similarity
* gamer_vs_light_sleeper
* extrovert_vs_introvert_conflict
* messy_vs_clean_conflict

---

# 🏗️ Model Architecture

PyTorch MLP Regression Network:

```python
Linear(input_size, 128)
ReLU()

Linear(128 , 64)
ReLU()

Linear(64 , 32)
ReLU()

Linear(32, 1)
```

The model predicts:

```text
Compatibility Score → 0–100
```

---

# 🖥️ UI Highlights

* Light blue premium theme
* Glassmorphism cards
* Animated transitions
* Dynamic compatibility reports
* Interactive member switching
* Visual compatibility analysis
* Risk & positive factor detection

---

# 📂 Project Structure

```text
roommate-compatability/
│
├── app.py
├── calculations.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── best_model.pth
│   ├── top_features.pkl
│   └── scaler.pkl
│
├── dataset/
│   └── dataset.csv
│
├── notebooks/
│   └── experimentation.ipynb
│
├── utils/
│   ├── inference.py
│   └── preprocessing.py
│
├── assets/
│   └── screenshots/
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <your-repo-link>
cd roommate-compatability
```

Create virtual environment:

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Linux/Mac

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

If Streamlit command fails:

```bash
python -m streamlit run app.py
```

---

# 📦 Requirements

Main libraries used:

```text
streamlit
torch
pandas
numpy
scikit-learn
joblib
plotly
```

---

# 📈 Compatibility Score Labels

| Score Range | Compatibility |
| ----------- | ------------- |
| 0–20        | Very Poor     |
| 21–40       | Poor          |
| 41–60       | Moderate      |
| 61–80       | Good          |
| 81–100      | Excellent     |

---

# 🧪 Dataset

The dataset was synthetically generated using:

* engineered compatibility formulas
* weighted behavioral relationships
* realistic roommate interaction patterns
* controlled randomness/noise

Dataset includes:

* 30 engineered features
* compatibility scores
* compatibility labels

---

# 🔥 Future Improvements

* SHAP explainability
* Real survey-based dataset
* Authentication system
* Multi-roommate matching
* Cloud deployment
* Recommendation engine
* Chat-based roommate assistant

---

---

# 🌐 Deployment

Recommended platforms:

* Streamlit Cloud
* HuggingFace Spaces
* Render
* Railway

---

# 👨‍💻 Author

Varshith

---

# ⭐ If You Like This Project

Give the repository a star ⭐ and share feedback!
