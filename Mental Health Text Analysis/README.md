# Mental Health Text Analysis

This project analyzes Reddit mental health text and predicts four mental health risk categories:

- Depression
- Anxiety
- Stress
- Burnout

The project is beginner-friendly and uses a CPU-friendly machine learning pipeline: TF-IDF text features plus one Logistic Regression classifier per label. It also includes LIME explainability so users can see which words contributed most to a prediction.

## Dataset Used

This project is designed for the **Reddit Mental Health Dataset from Kaggle**.

Place the downloaded dataset CSV inside the `data/` folder, for example:

```text
Mental Health Text Analysis/
  data/
    reddit_mental_health.csv
```

The notebook tries to automatically find a CSV file in common locations such as `data/`, the project root, or Kaggle's `/kaggle/input/` directory.

## Project Files

```text
Mental Health Text Analysis/
  mental_health_analysis.ipynb
  app.py
  README.md
  requirements.txt
```

## How To Run

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Open the notebook:

```bash
jupyter notebook mental_health_analysis.ipynb
```

3. Run all notebook cells from top to bottom.

4. The notebook saves trained model files inside:

```text
models/
```

5. Start the Gradio app:

```bash
python app.py
```

6. Open the local URL printed in the terminal.

## How To Check The Project Before Creating A Pull Request

Run these checks locally:

```bash
pip install -r requirements.txt
jupyter notebook mental_health_analysis.ipynb
```

Inside the notebook:

- Run every cell from top to bottom.
- Confirm the EDA charts are displayed.
- Confirm F1 score and AUC-ROC values are printed.
- Confirm the `models/` folder contains the saved `.joblib` files.

Then run:

```bash
python app.py
```

Enter a sample text in the Gradio UI and confirm it returns risk scores for Depression, Anxiety, Stress, and Burnout.

## Sample Output Screenshot

Add your screenshot here after running the Gradio app:

```text
assets/sample_output_screenshot.png
```

Suggested screenshot content:

- A sample Reddit-style text input
- Risk scores for Depression, Anxiety, Stress, and Burnout
- Severity labels: Low, Medium, or High

## Requirements

Main libraries used:

- pandas
- numpy
- scikit-learn
- nltk
- lime
- gradio
- matplotlib
- seaborn
- joblib

## Important Note

This project is for educational and research purposes only. It is **not** a medical diagnosis tool. Mental health predictions from text should always be interpreted carefully and should never replace support from qualified professionals.
