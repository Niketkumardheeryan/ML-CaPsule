# Real-Time Stock Market Sentiment Analysis using FinBERT & Live News API

## Overview

This project analyzes real-time financial news headlines to predict short-term stock
sentiment using FinBERT — a BERT model specifically fine-tuned on financial text such
as earnings call transcripts, analyst reports, and 10-K filings.

Unlike traditional stock prediction projects that rely solely on historical price data
(LSTM, ARIMA), this project takes an NLP-first approach — understanding what the market
is saying about a stock before looking at what the price is doing.

---

## Features

- Live news ingestion via NewsAPI or Yahoo Finance RSS (no API key needed for RSS)
- FinBERT sentiment classification: Positive, Neutral, Negative
- Baseline model comparison: FinBERT vs TextBlob vs VADER
- Stock price vs sentiment correlation charts using Plotly
- Word clouds for positive and negative headline clusters
- FinBERT confidence heatmap by ticker and sentiment
- Interactive Streamlit dashboard with live ticker input
- Downloadable CSV of all results

---

## Project Structure

```
Real_Time_Stock_Sentiment_FinBERT/
|
|-- stock_analysis.py      # Full batch analysis script
|-- app.py                 # Streamlit interactive dashboard
|-- requirements.txt       # All dependencies
|-- README.md              # This file
```

---

## Setup Instructions

### Step 1: Clone the repository
```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd ML-CaPsule/Real_Time_Stock_Sentiment_FinBERT
```

### Step 2: Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: (Optional) Set your NewsAPI key
Get a free key at https://newsapi.org/register and set it as an environment variable:
```bash
export NEWS_API_KEY=your_key_here       # Linux / macOS
set NEWS_API_KEY=your_key_here          # Windows CMD
```
If no key is provided, the project automatically falls back to Yahoo Finance RSS feeds
for the batch analysis script.

---

## Running the Project

### Option A: Run the full analysis script
```bash
python stock_analysis.py
```
This runs all 16 analysis cells end to end and saves charts as HTML and PNG files.

### Option B: Launch the Streamlit dashboard
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

---

## Models Used

| Model   | Type                          | Best For                          |
|---------|-------------------------------|-----------------------------------|
| FinBERT | BERT fine-tuned on finance    | Financial news, earnings reports  |
| TextBlob| Rule-based NLP                | General English text              |
| VADER   | Rule-based, lexicon-based     | Social media, short text          |

FinBERT (ProsusAI/finbert) significantly outperforms generic sentiment models on
financial language. Words like "headwinds", "guidance raised", "margin compression",
and "beat estimates" are correctly understood by FinBERT but often misclassified
by TextBlob and VADER.

---

## Sample Results

```
Ticker  | Articles | Dominant Sentiment | FinBERT Score | TextBlob Score | VADER Score
--------|----------|-------------------|---------------|----------------|------------
AAPL     |    3     | Negative          |    -0.333     |    -0.167      |   -0.333
TSLA     |    3     | Neutral           |    -0.333     |    -0.333      |   -0.667
INFY     |    2     | Neutral           |     0.000     |     0.500      |    0.000
GOOGL    |    2     | Neutral           |    -0.500     |     0.000      |   -0.500
MSFT     |    2     | Positive          |     1.000     |     0.500      |    0.500
```

---

## Output Files

After running stock_analysis.py, the following files are generated:

- sentiment_distribution.html     — Bar chart of positive/neutral/negative per ticker
- model_comparison.html           — FinBERT vs TextBlob vs VADER score comparison
- AAPL_price_vs_sentiment.html    — Price overlaid with daily sentiment (per ticker)
- wordcloud_sentiment.png         — Word clouds for positive vs negative headlines
- finbert_confidence_heatmap.png  — Heatmap of model confidence scores

---

## Tech Stack

| Component       | Technology                              |
|-----------------|-----------------------------------------|
| NLP Model       | FinBERT (ProsusAI/finbert via HuggingFace) |
| Baselines       | TextBlob, VADER                         |
| News Source     | NewsAPI, Yahoo Finance RSS              |
| Stock Data      | yfinance                                |
| Charts          | Plotly, Matplotlib, Seaborn             |
| Dashboard       | Streamlit                               |
| Data Processing | Pandas, NumPy                           |

---

## Contributor

Submitted as part of GSSoC 2026 contribution to ML-CaPsule.
Issue: #1651
