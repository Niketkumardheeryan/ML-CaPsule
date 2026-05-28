"""
Real-Time Stock Market Sentiment Dashboard
Run with: streamlit run app.py
"""

import warnings
import feedparser
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

# Page Config and Global Controls
st.set_page_config(
    page_title="Stock Sentiment Analyzer",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Real-Time Stock Market Sentiment Analysis")
st.markdown("Powered by **FinBERT** — a BERT model fine-tuned on financial text")
st.markdown("---")

# Sidebar Controls
st.sidebar.header("Configuration")

tickers_input = st.sidebar.text_input(
    "Stock Tickers (comma-separated)",
    value="AAPL, TSLA, INFY, GOOGL, MSFT",
)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

model_choice = st.sidebar.selectbox(
    "Sentiment Model",
    ["FinBERT (Recommended)", "TextBlob", "VADER", "All Three"],
)

run_btn = st.sidebar.button("Analyze Now", type="primary", use_container_width=True)

# Helper Functions
LABEL_MAP = {"positive": 1, "neutral": 0, "negative": -1}
SENTIMENT_COLORS = {"positive": "#2ecc71", "neutral": "#95a5a6", "negative": "#e74c3c"}


@st.cache_resource(show_spinner="Loading FinBERT model...")
def load_finbert():
    """Load FinBERT once per Streamlit session and reuse it across reruns."""
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    return pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,
        truncation=True,
        max_length=512,
    )


def fetch_rss(ticker):
    """Fetch Yahoo Finance RSS headlines for one ticker."""
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    try:
        feed = feedparser.parse(url)
        return [
            {"ticker": ticker, "title": e.get("title", ""),
             "description": e.get("summary", ""), "publishedAt": e.get("published", ""), "source": "Yahoo Finance"}
            for e in feed.entries if e.get("title")
        ]
    except Exception:
        return []


def get_sentiment_textblob(text):
    """Return a coarse TextBlob sentiment label from polarity."""
    p = TextBlob(text).sentiment.polarity
    return "positive" if p > 0.05 else "negative" if p < -0.05 else "neutral"


def get_sentiment_vader(text, analyzer):
    """Return a VADER sentiment label from the compound score."""
    score = analyzer.polarity_scores(text)["compound"]
    return "positive" if score >= 0.05 else "negative" if score <= -0.05 else "neutral"


# Main Analysis
if run_btn:
    # 1. Load live Yahoo Finance RSS headlines for the selected tickers.
    with st.spinner("Fetching news headlines..."):
        records = []
        for ticker in tickers:
            records.extend(fetch_rss(ticker))
        news_df = pd.DataFrame(records)

        if news_df.empty:
            st.error("No live news data available. Please check the tickers or try again later.")
            st.stop()

        news_df["text"] = (
            news_df["title"].fillna("") + ". " + news_df["description"].fillna("")
        ).str.strip(". ")
        news_df = news_df[news_df["ticker"].isin(tickers)].reset_index(drop=True)

    st.success(f"Loaded {len(news_df)} headlines across {news_df['ticker'].nunique()} tickers.")

    # 2. Run the selected sentiment model(s). FinBERT is cached because loading
    # the Transformer is the slowest step in the dashboard.
    with st.spinner("Running sentiment analysis..."):
        if model_choice in ["FinBERT (Recommended)", "All Three"]:
            finbert = load_finbert()
            fb_results = []
            for text in news_df["text"].tolist():
                try:
                    out = finbert(text[:512])[0]
                    fb_results.append({"finbert_label": out["label"], "finbert_score": round(out["score"], 4)})
                except Exception:
                    fb_results.append({"finbert_label": "neutral", "finbert_score": 0.5})
            fb_df = pd.DataFrame(fb_results)
            news_df = pd.concat([news_df.reset_index(drop=True), fb_df], axis=1)

        if model_choice in ["TextBlob", "All Three"]:
            news_df["textblob_label"] = news_df["text"].apply(get_sentiment_textblob)

        if model_choice in ["VADER", "All Three"]:
            vader = SentimentIntensityAnalyzer()
            news_df["vader_label"] = news_df["text"].apply(lambda x: get_sentiment_vader(x, vader))

    # 3. Normalize whichever model was selected into one primary label column
    # so downstream charts can use the same aggregation code.
    primary_label = (
        "finbert_label" if "finbert_label" in news_df.columns
        else "textblob_label" if "textblob_label" in news_df.columns
        else "vader_label"
    )
    news_df["primary_label"] = news_df[primary_label]
    news_df["primary_score_num"] = news_df["primary_label"].map(LABEL_MAP)

    # Section 1 — Sentiment Summary Cards

    st.markdown("## Sentiment Overview")

    summary = (
        news_df.groupby("ticker")
        .agg(
            articles=("title", "count"),
            positive=("primary_label", lambda x: (x == "positive").sum()),
            neutral=("primary_label", lambda x: (x == "neutral").sum()),
            negative=("primary_label", lambda x: (x == "negative").sum()),
            avg_score=("primary_score_num", "mean"),
        )
        .reset_index()
    )
    summary["dominant"] = summary[["positive", "neutral", "negative"]].idxmax(axis=1)
    summary["confidence"] = (
        summary[["positive", "neutral", "negative"]].max(axis=1) / summary["articles"] * 100
    ).round(1)

    cols = st.columns(len(summary))
    for col, (_, row) in zip(cols, summary.iterrows()):
        label = row["dominant"]
        color = SENTIMENT_COLORS[label]
        col.markdown(
            f"""
            <div style='background:{color}22; border-left:5px solid {color};
                        padding:12px; border-radius:8px; text-align:center;'>
                <h2 style='margin:0;color:{color};'>{row['ticker']}</h2>
                <p style='margin:4px 0;font-size:18px;font-weight:bold;'>{label.upper()}</p>
                <p style='margin:0;font-size:13px;'>
                    {int(row['articles'])} articles<br>
                    Score: {row['avg_score']:.2f}<br>
                    Confidence: {row['confidence']}%
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Section 2 — Sentiment Distribution Chart
    st.markdown("## Sentiment Distribution by Ticker")

    fig1 = go.Figure()
    for sentiment, color in SENTIMENT_COLORS.items():
        fig1.add_trace(go.Bar(
            name=sentiment.capitalize(),
            x=summary["ticker"],
            y=summary[sentiment],
            marker_color=color,
        ))
    fig1.update_layout(
        barmode="group", template="plotly_white",
        yaxis_title="Number of Headlines",
        xaxis_title="Ticker",
        legend_title="Sentiment",
        height=400,
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Section 3 — Model Comparison (if All Three selected)
    if model_choice == "All Three":
        st.markdown("## Model Comparison: FinBERT vs TextBlob vs VADER")

        comp_data = []
        for ticker in tickers:
            sub = news_df[news_df["ticker"] == ticker]
            comp_data.append({
                "ticker": ticker,
                "FinBERT": sub["finbert_label"].map(LABEL_MAP).mean() if "finbert_label" in sub else 0,
                "TextBlob": sub["textblob_label"].map(LABEL_MAP).mean() if "textblob_label" in sub else 0,
                "VADER": sub["vader_label"].map(LABEL_MAP).mean() if "vader_label" in sub else 0,
            })
        comp_df = pd.DataFrame(comp_data)

        fig2 = go.Figure()
        model_colors = {"FinBERT": "#3498db", "TextBlob": "#e67e22", "VADER": "#9b59b6"}
        for model, color in model_colors.items():
            fig2.add_trace(go.Bar(
                name=model, x=comp_df["ticker"], y=comp_df[model], marker_color=color
            ))
        fig2.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.3)
        fig2.update_layout(
            barmode="group", template="plotly_white",
            yaxis_title="Avg Sentiment Score (-1 to +1)",
            height=400,
        )
        st.plotly_chart(fig2, use_container_width=True)

        agreement = (news_df["finbert_label"] == news_df["vader_label"]).mean() * 100
        st.info(
            f"FinBERT and VADER agree on **{agreement:.1f}%** of headlines. "
            "FinBERT's financial domain training makes it more accurate on earnings reports, "
            "analyst commentary, and market jargon."
        )

    # Section 4 — Stock Price Data
    st.markdown("## Stock Price (Last 30 Days)")

    try:
        with st.spinner("Fetching price data..."):
            selected_ticker = st.selectbox("Select ticker for price chart", tickers)
            price_df = yf.download(
                selected_ticker,
                start=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                end=datetime.now().strftime("%Y-%m-%d"),
                progress=False,
            )

        if not price_df.empty:
            price_df = price_df[["Close"]].reset_index()
            price_df.columns = ["Date", "Close"]

            ticker_sentiment = news_df[news_df["ticker"] == selected_ticker]["primary_score_num"].mean()
            sentiment_label = "Positive" if ticker_sentiment > 0 else "Negative" if ticker_sentiment < 0 else "Neutral"
            sentiment_color = SENTIMENT_COLORS[sentiment_label.lower()]

            fig3 = make_subplots(specs=[[{"secondary_y": True}]])
            fig3.add_trace(
                go.Scatter(
                    x=price_df["Date"], y=price_df["Close"],
                    name="Stock Price", line=dict(color="#2c3e50", width=2)
                ),
                secondary_y=False,
            )
            fig3.add_hline(
                y=price_df["Close"].mean(),
                line_dash="dot", line_color=sentiment_color,
                annotation_text=f"News Sentiment: {sentiment_label} ({ticker_sentiment:.2f})",
                annotation_position="top left",
            )
            fig3.update_layout(
                title=f"{selected_ticker} — 30-Day Price with Sentiment Overlay",
                template="plotly_white", height=400,
            )
            fig3.update_yaxes(title_text="Price (USD)", secondary_y=False)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("Could not fetch price data for this ticker.")
    except Exception as e:
        st.warning(f"Price data unavailable: {e}")

    # Section 5 — Raw Headlines Table
    st.markdown("## Raw Headlines with Sentiment Labels")

    display_cols = ["ticker", "title", "source", "primary_label"]
    if "finbert_score" in news_df.columns:
        display_cols.append("finbert_score")

    st.dataframe(
        news_df[display_cols].rename(columns={
            "ticker": "Ticker", "title": "Headline",
            "source": "Source", "primary_label": "Sentiment",
            "finbert_score": "Confidence",
        }),
        use_container_width=True,
        height=400,
    )
    # Section 6 — Download Results
    st.markdown("---")
    csv = news_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="sentiment_results.csv",
        mime="text/csv",
    )

else:
    st.info("Configure your settings in the sidebar and click **Analyze Now** to begin.")
    st.markdown("""
    **What this tool does:**
    - Fetches live financial news headlines for your chosen tickers
    - Runs FinBERT (finance-specific BERT) to classify sentiment as Positive, Neutral, or Negative
    - Compares FinBERT against TextBlob and VADER baselines
    - Overlays sentiment scores on real stock price charts
    - Exports results as a downloadable CSV
    """)
