# Internship Scam Detection

A full-stack machine learning application designed to detect fraudulent or spam internship postings. This project uses a trained supervised learning model (Decision Tree) served via a Flask backend, with a responsive web interface for users to analyze job descriptions and requirements.

## Project Structure

```text
Internship Scam Detection/
├── data/
│   └── internship_scam_data.csv       # Raw dataset used for training
├── models/
│   ├── model.pkl                      # Trained machine learning classifier
│   └── pipeline.pkl                   # Data preprocessing pipeline (ColumnTransformer/Imputer)
├── notebooks/
│   ├── internship_scam_detection.ipynb # Jupyter notebook for EDA and model training
│   └── README.md                      # Notes specific to the modeling process
├── static/
│   └── styles.css                     # Custom CSS for the web frontend
├── templates/
│   └── index.html                     # Main HTML interface
├── .gitignore                         # Specifies files for Git to ignore (e.g., venv, __pycache__)
├── app.py                             # Flask backend server and API routes
├── README.md                          # Project documentation
└── requirements.txt                   # Python dependencies (Flask, scikit-learn, pandas, etc.)

```

## 🚀 Installation & Setup

To run this project locally, follow these steps:

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd "Internship Scam Detection"
```

**2. Create a virtual environment**
A virtual environment keeps your project dependencies isolated.

```bash
python -m venv venv
```

**3. Activate the virtual environment**

* On macOS/Linux:
```bash
source venv/bin/activate
```


* On Windows:
```bash
venv\Scripts\activate
```



**4. Install dependencies**

```bash
pip install -r requirements.txt
```

## 💻 Usage

Once your environment is activated and dependencies are installed, start the Flask server:

```bash
flask run
```

Open your web browser and navigate to `http://127.0.0.1:5000` to view the application. Enter the details of an internship posting, and the ML pipeline will analyze the inputs and return a confidence score indicating the likelihood of it being a scam.

## 🧠 Model Methodology (`notebooks/internship_scam_detection.ipynb`)

The machine learning core of this application was built and optimized using `scikit-learn` in a Jupyter Notebook. The notebook walks through the entire lifecycle from raw data to a deployed model.

**1. Data Preprocessing (The Pipeline)**
To handle incoming web data cleanly, a `ColumnTransformer` pipeline was built:
* **Imputation:** Missing numerical values (like `stipend`) are automatically filled with 0s using a `SimpleImputer`.
* **Scaling & Encoding:** Numerical data is normalized using `StandardScaler`, while categorical text (like `work_mode` or `company_size`) is transformed into a machine-readable format using `OneHotEncoder`.
* **Feature Selection:** High-cardinality fields (like `company_name` and `location`) were dropped to prevent the model from overfitting on highly unique text strings.

**2. Model Training & Optimization**
* **Algorithm:** The core engine is a `DecisionTreeClassifier`. 
* **Hyperparameter Tuning:** Instead of guessing the best settings, `GridSearchCV` was used to systematically test multiple combinations of parameters (`max_depth`, `min_samples_split`, `criterion`) to find the most mathematically optimal tree.

**3. Performance Metrics**
The final optimized model achieved the following results on the isolated test set:
* **Overall Accuracy:** 70%
* **Scam Precision:** 74% (When it flags a scam, it is correct 74% of the time)
* **Scam Recall:** 63% (It successfully catches 63% of all actual scams)

## 🛠️ Technologies Used

* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
* **Backend:** Python, Flask, Flask-CORS
* **Machine Learning:** scikit-learn, pandas, joblib

---

> Created by Naina Bhatnagar

> [Connect on linkedin](https://www.linkedin.com/in/nainabhatnagar/) <br>[Connect on github](https://github.com/naina-bhatnagar)

---