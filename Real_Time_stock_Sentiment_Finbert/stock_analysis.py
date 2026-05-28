"""
Real-Time Stock Market Sentiment Analysis using FinBERT and live news.

Run:
    python stock_analysis.py
"""

import os
import warnings
from datetime import datetime, timedelta

import feedparser
import matplotlib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import seaborn as sns
import torch
import yfinance as yf
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from plotly.subplots import make_subplots
from textblob import TextBlob
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud


matplotlib.use("Agg")
warnings.filterwarnings("ignore")

load_dotenv()

# Runtime configuration lives at the top so the batch script can be adjusted
# without touching the analysis logic below.
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_NEWSAPI_KEY_HERE")
TICKERS = ["AAPL", "TSLA", "INFY", "GOOGL", "MSFT"]
DAYS_BACK = 7
FINBERT_MODEL = "ProsusAI/finbert"
LABEL_MAP = {"positive": 1, "neutral": 0, "negative": -1}


# News Collection
def fetch_news_newsapi(ticker: str, api_key: str, days_back: int = 7) -> pd.DataFrame:
    """Fetch financial news headlines for a ticker using NewsAPI."""
    if not api_key or api_key == "YOUR_NEWSAPI_KEY_HERE":
        print(f"  [SKIP] No NewsAPI key set. Using RSS fallback for {ticker}.")
        return pd.DataFrame()

    # NewsAPI accepts an ISO date string for the lower bound of the search window.
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    url = (
        "https://newsapi.org/v2/everything"
        f"?q={ticker}&from={from_date}&sortBy=publishedAt"
        f"&language=en&apiKey={api_key}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        # Normalize the API response into the same columns used by the RSS fallback.
        records = [
            {
                "ticker": ticker,
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "publishedAt": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", ""),
            }
            for article in articles
            if article.get("title")
        ]
        df = pd.DataFrame(records)
        print(f"  [NewsAPI] {ticker}: {len(df)} articles fetched.")
        return df
    except Exception as exc:
        print(f"  [ERROR] NewsAPI failed for {ticker}: {exc}")
        return pd.DataFrame()


def fetch_news_rss(ticker: str) -> pd.DataFrame:
    """Fetch financial news via Yahoo Finance RSS feed."""
    # Yahoo's RSS endpoint gives this project a no-key backup source of headlines.
    rss_url = (
        "https://feeds.finance.yahoo.com/rss/2.0/headline"
        f"?s={ticker}&region=US&lang=en-US"
    )

    try:
        feed = feedparser.parse(rss_url)
        records = [
            {
                "ticker": ticker,
                "title": entry.get("title", ""),
                "description": entry.get("summary", ""),
                "publishedAt": entry.get("published", ""),
                "source": "Yahoo Finance RSS",
            }
            for entry in feed.entries
            if entry.get("title")
        ]
        df = pd.DataFrame(records)
        print(f"  [RSS] {ticker}: {len(df)} articles fetched.")
        return df
    except Exception as exc:
        print(f"  [ERROR] RSS failed for {ticker}: {exc}")
        return pd.DataFrame()


def fetch_all_news(tickers: list[str], api_key: str, days_back: int = 7) -> pd.DataFrame:
    """Fetch news from NewsAPI first, then fall back to Yahoo RSS per ticker."""
    all_dfs = []

    for ticker in tickers:
        print(f"\nFetching news for {ticker}...")

        # Prefer NewsAPI when a key is available; RSS keeps the script usable without one.
        df = fetch_news_newsapi(ticker, api_key, days_back)
        if df.empty:
            df = fetch_news_rss(ticker)
        if not df.empty:
            all_dfs.append(df)

    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)

        # The same headline can appear from multiple sources, so title is a practical
        # duplicate key for this reporting workflow.
        combined.drop_duplicates(subset=["title"], inplace=True)
        print(f"\nTotal unique headlines collected: {len(combined)}")
        return combined

    print("\nNo news fetched from NewsAPI or RSS.")
    return pd.DataFrame()


# Sentiment Inference
def prepare_news(news_df: pd.DataFrame) -> pd.DataFrame:
    """Add a combined text field used by the sentiment models."""
    news_df = news_df.copy()

    # Sentiment models work best with the headline and short article summary together.
    news_df["text"] = (
        news_df["title"].fillna("") + ". " + news_df["description"].fillna("")
    ).str.strip(". ")
    return news_df


def load_finbert_pipeline():
    """Load the finance-specific Transformer model used for headline sentiment."""
    print("\nLoading FinBERT model. This may take a minute on first run...")
    tokenizer = AutoTokenizer.from_pretrained(FINBERT_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(FINBERT_MODEL)

    # Use CUDA automatically when available; otherwise the Hugging Face pipeline runs on CPU.
    finbert = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,
        truncation=True,
        max_length=512,
    )
    print("FinBERT model loaded successfully.")
    return finbert


def run_finbert(texts: list[str], finbert) -> list[dict]:
    """Run FinBERT inference on a list of texts."""
    results = []
    for text in texts:
        try:
            # Keep each input within the model's maximum token window.
            output = finbert(str(text)[:512])[0]
            results.append(
                {
                    "finbert_label": output["label"],
                    "finbert_score": round(output["score"], 4),
                }
            )
        except Exception:
            # A single malformed headline should not stop the full ticker analysis.
            results.append({"finbert_label": "neutral", "finbert_score": 0.5})
    return results


def add_finbert_sentiment(news_df: pd.DataFrame) -> pd.DataFrame:
    """Attach FinBERT labels and confidence scores to each headline."""
    finbert = load_finbert_pipeline()
    finbert_results = run_finbert(news_df["text"].tolist(), finbert)
    finbert_df = pd.DataFrame(finbert_results)
    news_df = pd.concat([news_df.reset_index(drop=True), finbert_df], axis=1)

    print(f"\nFinBERT inference complete on {len(news_df)} headlines.")
    print(news_df[["ticker", "title", "finbert_label", "finbert_score"]].head(8))
    return news_df


def textblob_sentiment(text: str) -> str:
    """Classify text with TextBlob polarity thresholds."""
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.05:
        return "positive"
    if polarity < -0.05:
        return "negative"
    return "neutral"


def vader_sentiment(text: str, vader: SentimentIntensityAnalyzer) -> str:
    """Classify text with VADER compound-score thresholds."""
    score = vader.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "positive"
    if score <= -0.05:
        return "negative"
    return "neutral"


def add_baseline_sentiment(news_df: pd.DataFrame) -> pd.DataFrame:
    """Run lightweight baseline models for comparison with FinBERT."""
    vader = SentimentIntensityAnalyzer()
    news_df = news_df.copy()
    news_df["textblob_label"] = news_df["text"].apply(textblob_sentiment)
    news_df["vader_label"] = news_df["text"].apply(lambda text: vader_sentiment(text, vader))

    print("TextBlob and VADER inference complete.")
    print(news_df[["ticker", "finbert_label", "textblob_label", "vader_label"]].head(8))
    return news_df


def build_sentiment_summary(news_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate per-headline sentiment into ticker-level summary metrics."""
    # Map labels to numeric values so each model can be averaged per ticker.
    news_df["finbert_score_num"] = news_df["finbert_label"].map(LABEL_MAP)
    news_df["textblob_score_num"] = news_df["textblob_label"].map(LABEL_MAP)
    news_df["vader_score_num"] = news_df["vader_label"].map(LABEL_MAP)

    summary = (
        news_df.groupby("ticker")
        .agg(
            total_articles=("title", "count"),
            finbert_positive=("finbert_label", lambda values: (values == "positive").sum()),
            finbert_neutral=("finbert_label", lambda values: (values == "neutral").sum()),
            finbert_negative=("finbert_label", lambda values: (values == "negative").sum()),
            finbert_avg_score=("finbert_score_num", "mean"),
            textblob_avg_score=("textblob_score_num", "mean"),
            vader_avg_score=("vader_score_num", "mean"),
        )
        .reset_index()
    )

    summary["finbert_dominant"] = (
        summary[["finbert_positive", "finbert_neutral", "finbert_negative"]]
        .idxmax(axis=1)
        .str.replace("finbert_", "")
    )

    print("\nSentiment Summary per Ticker:")
    print(summary.to_string(index=False))
    return summary


# Market Data
def fetch_stock_prices(tickers: list[str], days_back: int = 30) -> pd.DataFrame:
    """Fetch OHLCV data from Yahoo Finance for given tickers."""
    end = datetime.now()
    start = end - timedelta(days=days_back)
    all_prices = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start, end=end, progress=False)
            if df.empty:
                continue

            # yfinance can return MultiIndex columns depending on version and request shape.
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df = df[["Close", "Volume"]].copy()
            df.columns = ["close", "volume"]
            df["ticker"] = ticker
            df["date"] = df.index

            # Daily percent change is printed for context and can support later analysis.
            df["pct_change"] = df["close"].pct_change() * 100
            all_prices.append(df.reset_index(drop=True))
            print(f"  {ticker}: {len(df)} trading days fetched.")
        except Exception as exc:
            print(f"  [ERROR] {ticker}: {exc}")

    return pd.concat(all_prices, ignore_index=True) if all_prices else pd.DataFrame()


# Report Artifacts
def save_sentiment_distribution(sentiment_summary: pd.DataFrame) -> None:
    """Save a grouped bar chart of positive, neutral, and negative headlines."""
    fig = go.Figure()
    colors = {
        "finbert_positive": "#2ecc71",
        "finbert_neutral": "#95a5a6",
        "finbert_negative": "#e74c3c",
    }
    labels = {
        "finbert_positive": "Positive",
        "finbert_neutral": "Neutral",
        "finbert_negative": "Negative",
    }

    for column, color in colors.items():
        # Each sentiment category becomes one grouped bar series per ticker.
        fig.add_trace(
            go.Bar(
                name=labels[column],
                x=sentiment_summary["ticker"],
                y=sentiment_summary[column],
                marker_color=color,
            )
        )

    fig.update_layout(
        title="FinBERT Sentiment Distribution by Stock Ticker",
        xaxis_title="Ticker",
        yaxis_title="Number of Headlines",
        barmode="group",
        template="plotly_white",
        legend_title="Sentiment",
        font=dict(size=13),
    )
    fig.write_html("sentiment_distribution.html")
    print("Chart saved: sentiment_distribution.html")


def save_model_comparison(sentiment_summary: pd.DataFrame) -> None:
    """Save average sentiment score comparison across FinBERT and baselines."""
    fig = go.Figure()
    model_cols = {
        "finbert_avg_score": ("FinBERT", "#3498db"),
        "textblob_avg_score": ("TextBlob", "#e67e22"),
        "vader_avg_score": ("VADER", "#9b59b6"),
    }

    for column, (name, color) in model_cols.items():
        fig.add_trace(
            go.Bar(
                name=name,
                x=sentiment_summary["ticker"],
                y=sentiment_summary[column],
                marker_color=color,
            )
        )

    fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.4)
    fig.update_layout(
        title="Model Comparison: Average Sentiment Score per Ticker",
        xaxis_title="Ticker",
        yaxis_title="Average Sentiment Score (-1 = Negative, +1 = Positive)",
        barmode="group",
        template="plotly_white",
        legend_title="Model",
        font=dict(size=13),
    )
    fig.write_html("model_comparison.html")
    print("Chart saved: model_comparison.html")


def save_price_vs_sentiment(price_df: pd.DataFrame, news_df: pd.DataFrame) -> None:
    """Save one price-vs-sentiment chart for each ticker with available data."""
    if price_df.empty:
        print("Skipping price vs sentiment chart because no price data is available.")
        return

    for ticker in TICKERS:
        ticker_prices = price_df[price_df["ticker"] == ticker].copy()
        ticker_news = news_df[news_df["ticker"] == ticker].copy()

        if ticker_prices.empty or ticker_news.empty:
            continue

        # Convert article timestamps to calendar dates so headlines can be averaged by day.
        ticker_news["date_only"] = pd.to_datetime(
            ticker_news["publishedAt"], errors="coerce"
        ).dt.date
        daily_sentiment = (
            ticker_news.groupby("date_only")["finbert_score_num"].mean().reset_index()
        )
        daily_sentiment.columns = ["date", "sentiment"]
        daily_sentiment["date"] = pd.to_datetime(daily_sentiment["date"])
        ticker_prices["date"] = pd.to_datetime(ticker_prices["date"])

        # Plot price and sentiment on separate y-axes because they use different scales.
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(
                x=ticker_prices["date"],
                y=ticker_prices["close"],
                name="Stock Price (USD)",
                line=dict(color="#2c3e50", width=2),
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Bar(
                x=daily_sentiment["date"],
                y=daily_sentiment["sentiment"],
                name="FinBERT Sentiment",
                marker_color=[
                    "#2ecc71" if value > 0 else "#e74c3c" if value < 0 else "#95a5a6"
                    for value in daily_sentiment["sentiment"]
                ],
                opacity=0.6,
            ),
            secondary_y=True,
        )
        fig.update_layout(
            title=f"{ticker}: Stock Price vs Daily News Sentiment (FinBERT)",
            template="plotly_white",
            font=dict(size=12),
        )
        fig.update_yaxes(title_text="Stock Price (USD)", secondary_y=False)
        fig.update_yaxes(title_text="Sentiment Score", secondary_y=True)
        output_file = f"{ticker}_price_vs_sentiment.html"
        fig.write_html(output_file)
        print(f"Chart saved: {output_file}")


def save_wordcloud(news_df: pd.DataFrame) -> None:
    """Save word clouds for the positive and negative FinBERT headline groups."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Word clouds make recurring terms visible within each sentiment bucket.
    for ax, label, color, title in zip(
        axes,
        ["positive", "negative"],
        ["Greens", "Reds"],
        ["Positive Headlines Word Cloud", "Negative Headlines Word Cloud"],
    ):
        subset = news_df[news_df["finbert_label"] == label]["text"]
        if subset.empty:
            ax.set_title(f"No {label} headlines found")
            ax.axis("off")
            continue

        text = " ".join(subset.tolist())
        wordcloud = WordCloud(
            width=700,
            height=400,
            background_color="white",
            colormap=color,
            max_words=80,
        ).generate(text)
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.axis("off")

    plt.tight_layout()
    plt.savefig("wordcloud_sentiment.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Chart saved: wordcloud_sentiment.png")


def save_confidence_heatmap(news_df: pd.DataFrame) -> None:
    """Save a heatmap of average FinBERT confidence by ticker and label."""
    # Pivot the long headline table into a ticker-by-label grid for Seaborn.
    pivot = news_df.pivot_table(
        index="finbert_label",
        columns="ticker",
        values="finbert_score",
        aggfunc="mean",
    )

    plt.figure(figsize=(10, 4))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        linewidths=0.5,
        cbar_kws={"label": "Avg Confidence Score"},
    )
    plt.title("FinBERT Average Confidence Score by Sentiment and Ticker", fontsize=13)
    plt.xlabel("Ticker")
    plt.ylabel("Sentiment")
    plt.tight_layout()
    plt.savefig("finbert_confidence_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Chart saved: finbert_confidence_heatmap.png")


# Console Reports
def print_model_report(news_df: pd.DataFrame) -> None:
    """Print model agreement and label-distribution diagnostics."""
    print("\n" + "=" * 60)
    print("MODEL COMPARISON REPORT")
    print("=" * 60)

    agreement_df = news_df[
        ["ticker", "title", "finbert_label", "textblob_label", "vader_label"]
    ].copy()

    # Agreement metrics show how often finance-specific FinBERT matches generic baselines.
    agreement_df["finbert_vs_textblob"] = (
        agreement_df["finbert_label"] == agreement_df["textblob_label"]
    )
    agreement_df["finbert_vs_vader"] = (
        agreement_df["finbert_label"] == agreement_df["vader_label"]
    )
    agreement_df["all_agree"] = (
        agreement_df["finbert_vs_textblob"] & agreement_df["finbert_vs_vader"]
    )

    total = len(agreement_df)
    print(f"\nTotal headlines analyzed      : {total}")
    print(
        "FinBERT vs TextBlob agreement : "
        f"{agreement_df['finbert_vs_textblob'].sum()} / {total} "
        f"({agreement_df['finbert_vs_textblob'].mean() * 100:.1f}%)"
    )
    print(
        "FinBERT vs VADER agreement    : "
        f"{agreement_df['finbert_vs_vader'].sum()} / {total} "
        f"({agreement_df['finbert_vs_vader'].mean() * 100:.1f}%)"
    )
    print(
        "All three models agree        : "
        f"{agreement_df['all_agree'].sum()} / {total} "
        f"({agreement_df['all_agree'].mean() * 100:.1f}%)"
    )

    print("\nFinBERT Label Distribution:")
    print(news_df["finbert_label"].value_counts().to_string())
    print("\nTextBlob Label Distribution:")
    print(news_df["textblob_label"].value_counts().to_string())
    print("\nVADER Label Distribution:")
    print(news_df["vader_label"].value_counts().to_string())

    print("\nKey Insight:")
    print(
        "FinBERT is specifically trained on financial text. It can better classify "
        "financial language like guidance raised, headwinds, and margin compression "
        "than generic models such as TextBlob and VADER."
    )


def print_final_summary(sentiment_summary: pd.DataFrame) -> None:
    """Print the compact ticker-level result table shown at the end of the run."""
    print("\n" + "=" * 60)
    print("FINAL SENTIMENT SUMMARY")
    print("=" * 60)

    summary_display = sentiment_summary[
        [
            "ticker",
            "total_articles",
            "finbert_dominant",
            "finbert_avg_score",
            "textblob_avg_score",
            "vader_avg_score",
        ]
    ].copy()

    # Rename internal column names into labels that are easier to read in the terminal.
    summary_display.columns = [
        "Ticker",
        "Articles",
        "FinBERT Dominant",
        "FinBERT Score",
        "TextBlob Score",
        "VADER Score",
    ]

    summary_display["FinBERT Score"] = summary_display["FinBERT Score"].round(3)
    summary_display["TextBlob Score"] = summary_display["TextBlob Score"].round(3)
    summary_display["VADER Score"] = summary_display["VADER Score"].round(3)

    print(summary_display.to_string(index=False))


# Orchestration
def main() -> None:
    """Run the full data collection, sentiment analysis, and reporting pipeline."""
    print("All libraries loaded successfully.")
    print(f"PyTorch version : {torch.__version__}")
    print(f"Device          : {'GPU (CUDA)' if torch.cuda.is_available() else 'CPU'}")
    print("Configuration loaded.")
    print(f"Tickers selected : {TICKERS}")
    print(f"Analysis window  : Last {DAYS_BACK} days")

    news_df = fetch_all_news(TICKERS, NEWS_API_KEY, DAYS_BACK)
    if news_df.empty:
        print("No headlines available. Add a valid NEWS_API_KEY in .env or check RSS/network access.")
        return

    # Every later model and report uses this prepared text column.
    news_df = prepare_news(news_df)

    print(f"\nFinal dataset shape: {news_df.shape}")
    print(news_df[["ticker", "title", "publishedAt"]].head(5))

    news_df = add_finbert_sentiment(news_df)
    news_df = add_baseline_sentiment(news_df)
    sentiment_summary = build_sentiment_summary(news_df)

    print("\nFetching stock price data...")
    price_df = fetch_stock_prices(TICKERS, days_back=30)
    if not price_df.empty:
        print(f"\nPrice data shape: {price_df.shape}")
        print(price_df[["ticker", "date", "close", "pct_change"]].tail(10))
    else:
        print("Could not fetch price data. Skipping price correlation.")

    # Save tabular outputs before charting so results are preserved even if a plot fails later.
    news_df.to_csv("news_sentiment_results.csv", index=False)
    sentiment_summary.to_csv("sentiment_summary.csv", index=False)
    print("Data saved: news_sentiment_results.csv")
    print("Data saved: sentiment_summary.csv")

    save_sentiment_distribution(sentiment_summary)
    save_model_comparison(sentiment_summary)
    save_price_vs_sentiment(price_df, news_df)
    save_wordcloud(news_df)
    save_confidence_heatmap(news_df)
    print_model_report(news_df)
    print_final_summary(sentiment_summary)

    print("\nAll outputs saved. Project complete.")
    print("Run app.py separately for the Streamlit dashboard.")


if __name__ == "__main__":
    main()
