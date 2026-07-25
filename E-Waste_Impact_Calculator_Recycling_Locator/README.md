# E-Waste Impact Calculator & Recycling Locator

An interactive, Machine Learning-powered tool that calculates the environmental footprint of electronic devices and helps users find local authorized recycling centers using geospatial mapping.

## Features

- **Impact Calculator:** Uses a Random Forest ML model trained on synthetic device lifespans, category baselines, and condition variables to predict:
  - **CO₂ Lifecycle Footprint** (in kg CO₂ equivalent)
  - **Toxic Material Score** (0 to 100 indicator based on toxic metals present)
  - **Recyclability Score** (0 to 100% potential index)
- **Interactive Recycler Locator:** Helps users locate authorized disposal centers using the Haversine distance algorithm, showing results in a localized table and a dynamic map (built via Streamlit's `st.map`).
- **Educational Dashboard:** Provides actionable guides (data sanitization, battery removal), toxic compound insights, and impact statistics.

## Project Structure

```text
E-Waste_Impact_Calculator_Recycling_Locator/
├── train_model.py     # Data generation & Random Forest model training script
├── app.py             # Streamlit web application
├── dataset.csv        # Generated synthetic dataset (created after training)
├── e_waste_model.pkl  # Trained Random Forest model bundle (created after training)
├── requirements.txt   # Local dependencies
└── README.md          # Project documentation
```

## Dataset

The synthetic dataset containing device configurations along with calculated carbon footprint, toxicity score, and recyclability index is saved at:
- **Local path:** `E-Waste_Impact_Calculator_Recycling_Locator/dataset.csv`
- **Remote Dataset Link:** [dataset.csv](https://raw.githubusercontent.com/Rakshak05/ML-CaPsule/issue-%232028/E-Waste_Impact_Calculator_Recycling_Locator/dataset.csv) (This remote RAW link is loaded dynamically inside `train_model.py`).



## Setup & Installation

1. Navigate to the project directory:
   ```bash
   cd E-Waste_Impact_Calculator_Recycling_Locator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Train the Machine Learning model:
   ```bash
   python train_model.py
   ```

4. Run the Streamlit dashboard:
   ```bash
   streamlit run app.py
   ```
