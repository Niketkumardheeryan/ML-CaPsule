"""
Batter vs Bowler Analytics Module
===================================
Predicts dismissal probability and provides matchup statistics
between batters and bowlers using historical IPL ball-by-ball data.

Author: Contribution to ML-CaPsule / IPL Cricket Match Win Prediction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, confusion_matrix,
    roc_auc_score, roc_curve, classification_report
)
import lightgbm as lgb
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────
# 1. DATA LOADING & PREPROCESSING
# ─────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load ball-by-ball IPL dataset.

    Expected columns (standard Cricsheet format):
        match_id, inning, batting_team, bowling_team, over, ball,
        batter, bowler, non_striker, batsman_runs, extra_runs,
        total_runs, extras_type, is_wicket, player_dismissed,
        dismissal_kind, fielder
    """
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    # derive is_wicket from player_dismissed column
    if "is_wicket" not in df.columns:
        df["is_wicket"] = df["player_dismissed"].apply(
            lambda x: 0 if (pd.isna(x) or str(x).strip() in ["nan", "", "None"]) else 1
        )
    df["is_wicket"] = df["is_wicket"].astype(int)
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and derive helper columns."""
    df = df.copy()

    # Ensure numeric types
    for col in ["batsman_runs", "total_runs", "is_wicket"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Ball number within over (1-6)
    if "ball" in df.columns:
        df["ball_in_over"] = df["ball"].apply(lambda x: round((x % 1) * 10) if x % 1 != 0 else x)

    # Phase of innings
    df["phase"] = pd.cut(
        df["over"],
        bins=[-1, 5, 15, 20],
        labels=["powerplay", "middle", "death"]
    )

    return df


# ─────────────────────────────────────────────
# 2. MATCHUP STATISTICS
# ─────────────────────────────────────────────

def get_matchup_stats(df: pd.DataFrame, batter: str, bowler: str) -> dict:
    """
    Compute head-to-head statistics for a batter vs bowler pair.

    Returns
    -------
    dict with keys: balls_faced, runs_scored, dismissals,
                    strike_rate, dismissal_rate, avg_runs_per_dismissal,
                    dot_ball_pct, boundary_count
    """
    matchup = df[(df["batsman"] == batter) & (df["bowler"] == bowler)].copy()

    if matchup.empty:
        return {"error": f"No historical data found for {batter} vs {bowler}"}

    balls_faced    = len(matchup)
    runs_scored    = int(matchup["batsman_runs"].sum())
    dismissals     = int(matchup["is_wicket"].sum())
    strike_rate    = round((runs_scored / balls_faced) * 100, 2) if balls_faced else 0
    dismissal_rate = round(dismissals / balls_faced, 4) if balls_faced else 0
    avg_runs       = round(runs_scored / dismissals, 2) if dismissals else float("inf")
    dot_ball_pct   = round(
        (matchup["batsman_runs"] == 0).sum() / balls_faced * 100, 2
    ) if balls_faced else 0
    boundaries     = int(matchup[matchup["batsman_runs"].isin([4, 6])].shape[0])

    return {
        "batsman":              batter,
        "bowler":              bowler,
        "balls_faced":         balls_faced,
        "runs_scored":         runs_scored,
        "dismissals":          dismissals,
        "strike_rate":         strike_rate,
        "dismissal_rate":      dismissal_rate,
        "avg_runs_per_wicket": avg_runs,
        "dot_ball_pct":        dot_ball_pct,
        "boundary_count":      boundaries,
    }


def top_matchups(df: pd.DataFrame, min_balls: int = 12) -> pd.DataFrame:
    """
    Return all batter-bowler pairs with at least `min_balls` deliveries,
    sorted by dismissal rate descending.
    """
    grouped = (
        df.groupby(["batsman", "bowler"])
        .agg(
            balls_faced=("batsman_runs", "count"),
            runs_scored=("batsman_runs", "sum"),
            dismissals=("is_wicket", "sum"),
        )
        .reset_index()
    )
    grouped = grouped[grouped["balls_faced"] >= min_balls].copy()
    grouped["strike_rate"]    = (grouped["runs_scored"] / grouped["balls_faced"] * 100).round(2)
    grouped["dismissal_rate"] = (grouped["dismissals"] / grouped["balls_faced"]).round(4)
    return grouped.sort_values("dismissal_rate", ascending=False)


# ─────────────────────────────────────────────
# 3. FEATURE ENGINEERING FOR ML MODEL
# ─────────────────────────────────────────────

def build_features(df: pd.DataFrame, min_balls: int = 6) -> pd.DataFrame:
    """
    Build a ball-level feature matrix for dismissal prediction.

    Features
    --------
    - batter_career_sr       : batter's overall career strike rate
    - batter_career_avg      : batter's career average vs all bowlers
    - bowler_career_econ     : bowler's economy rate
    - bowler_career_wkt_rate : bowler's wickets per ball
    - h2h_sr                 : batter's SR against this specific bowler
    - h2h_dismissal_rate     : historical dismissal rate in this matchup
    - h2h_balls              : balls faced by batter against bowler (proxy for sample size)
    - over                   : over number (1-20)
    - phase_encoded          : powerplay=0, middle=1, death=2
    - target (label)         : is_wicket
    """
    # -- Batter career stats (on full df, before filtering)
    batter_stats = (
        df.groupby("batsman")
        .agg(
            batter_career_balls=("batsman_runs", "count"),
            batter_career_runs=("batsman_runs", "sum"),
            batter_career_wkts=("is_wicket", "sum"),
        )
        .reset_index()
    )
    batter_stats["batter_career_sr"]  = (
        batter_stats["batter_career_runs"] / batter_stats["batter_career_balls"] * 100
    ).round(2)
    batter_stats["batter_career_avg"] = (
        batter_stats["batter_career_runs"] / batter_stats["batter_career_wkts"].replace(0, np.nan)
    ).fillna(50).round(2)

    # -- Bowler career stats
    bowler_stats = (
        df.groupby("bowler")
        .agg(
            bowler_career_balls=("batsman_runs", "count"),
            bowler_career_runs=("batsman_runs", "sum"),
            bowler_career_wkts=("is_wicket", "sum"),
        )
        .reset_index()
    )
    bowler_stats["bowler_career_econ"]     = (
        bowler_stats["bowler_career_runs"] / (bowler_stats["bowler_career_balls"] / 6)
    ).round(2)
    bowler_stats["bowler_career_wkt_rate"] = (
        bowler_stats["bowler_career_wkts"] / bowler_stats["bowler_career_balls"]
    ).round(4)

    # -- Head-to-head stats
    h2h = (
        df.groupby(["batsman", "bowler"])
        .agg(
            h2h_balls=("batsman_runs", "count"),
            h2h_runs=("batsman_runs", "sum"),
            h2h_wickets=("is_wicket", "sum"),
        )
        .reset_index()
    )
    h2h = h2h[h2h["h2h_balls"] >= min_balls]
    h2h["h2h_sr"]             = (h2h["h2h_runs"] / h2h["h2h_balls"] * 100).round(2)
    h2h["h2h_dismissal_rate"] = (h2h["h2h_wickets"] / h2h["h2h_balls"]).round(4)

    # -- Merge into ball-level data
    feat = df.merge(batter_stats[["batsman", "batter_career_sr", "batter_career_avg"]],
                    on="batsman", how="left")
    feat = feat.merge(
        bowler_stats[["bowler", "bowler_career_econ", "bowler_career_wkt_rate"]],
        on="bowler", how="left"
    )
    feat = feat.merge(h2h[["batsman", "bowler", "h2h_sr", "h2h_dismissal_rate", "h2h_balls"]],
                      on=["batsman", "bowler"], how="inner")   # keep only pairs with enough data

    # Phase encoding
    phase_map = {"powerplay": 0, "middle": 1, "death": 2}
    feat["phase_encoded"] = feat["phase"].map(phase_map).fillna(1)

    feature_cols = [
        "batter_career_sr", "batter_career_avg",
        "bowler_career_econ", "bowler_career_wkt_rate",
        "h2h_sr", "h2h_dismissal_rate", "h2h_balls",
        "over", "phase_encoded",
    ]
    label_col = "is_wicket"

    clean = feat[feature_cols + [label_col]].dropna()
    return clean


# ─────────────────────────────────────────────
# 4. MODEL TRAINING
# ─────────────────────────────────────────────

def train_dismissal_model(features_df: pd.DataFrame):
    """
    Train a LightGBM classifier to predict dismissal probability.

    Returns
    -------
    model    : trained LGBMClassifier
    X_test   : test feature matrix
    y_test   : test labels
    y_pred   : predicted labels
    y_proba  : predicted probabilities (class=1)
    """
    feature_cols = [c for c in features_df.columns if c != "is_wicket"]
    X = features_df[feature_cols]
    y = features_df["is_wicket"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = lgb.LGBMClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        num_leaves=31,
        min_child_samples=20,
        class_weight="balanced",
        random_state=42,
        verbose=-1,
    )
    model.fit(X_train, y_train)

    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("=" * 50)
    print("Dismissal Probability Model — Evaluation")
    print("=" * 50)
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC  : {roc_auc_score(y_test, y_proba):.4f}")
    print()
    print(classification_report(y_test, y_pred, target_names=["Not Out", "Dismissed"]))

    return model, X_test, y_test, y_pred, y_proba


def predict_dismissal_probability(
    model,
    batter: str,
    bowler: str,
    df: pd.DataFrame,
    over: int = 10,
    phase: str = "middle",
) -> float:
    """
    Predict dismissal probability for a specific batter-bowler pair.

    Parameters
    ----------
    model  : trained LGBMClassifier
    batter : batter name (as in dataset)
    bowler : bowler name
    df     : full ball-by-ball DataFrame
    over   : over number (1-20)
    phase  : 'powerplay', 'middle', or 'death'

    Returns
    -------
    dismissal probability (float, 0–1)
    """
    stats = get_matchup_stats(df, batter, bowler)
    if "error" in stats:
        raise ValueError(stats["error"])

    batter_rows = df[df["batsman"] == batter]
    bowler_rows = df[df["bowler"] == bowler]

    batter_sr  = (batter_rows["batsman_runs"].sum() / len(batter_rows) * 100) if len(batter_rows) else 120
    batter_avg = (
        batter_rows["batsman_runs"].sum() / batter_rows["is_wicket"].sum()
        if batter_rows["is_wicket"].sum() > 0 else 30
    )
    bowler_econ     = (bowler_rows["batsman_runs"].sum() / (len(bowler_rows) / 6)) if len(bowler_rows) else 8
    bowler_wkt_rate = (bowler_rows["is_wicket"].sum() / len(bowler_rows)) if len(bowler_rows) else 0.05
    phase_map       = {"powerplay": 0, "middle": 1, "death": 2}

    X_input = pd.DataFrame([{
        "batter_career_sr":         batter_sr,
        "batter_career_avg":        batter_avg,
        "bowler_career_econ":       bowler_econ,
        "bowler_career_wkt_rate":   bowler_wkt_rate,
        "h2h_sr":                   stats["strike_rate"],
        "h2h_dismissal_rate":       stats["dismissal_rate"],
        "h2h_balls":                stats["balls_faced"],
        "over":                     over,
        "phase_encoded":            phase_map.get(phase, 1),
    }])

    prob = model.predict_proba(X_input)[0][1]
    return round(prob, 4)


# ─────────────────────────────────────────────
# 5. VISUALIZATIONS
# ─────────────────────────────────────────────

def plot_matchup_summary(stats: dict, save_path: str = "matchup_summary.png") -> None:
    """Bar chart of key matchup statistics."""
    if "error" in stats:
        print(stats["error"])
        return

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle(
        f"{stats['batsman']}  vs  {stats['bowler']}",
        fontsize=16, fontweight="bold", y=1.02
    )

    # Runs & Balls
    axes[0].bar(["Runs Scored", "Balls Faced"],
                [stats["runs_scored"], stats["balls_faced"]],
                color=["#1f77b4", "#ff7f0e"])
    axes[0].set_title("Runs & Balls")
    axes[0].set_ylabel("Count")

    # Strike Rate vs Dot Ball %
    axes[1].bar(["Strike Rate", "Dot Ball %"],
                [stats["strike_rate"], stats["dot_ball_pct"]],
                color=["#2ca02c", "#d62728"])
    axes[1].set_title("Scoring Patterns")
    axes[1].set_ylabel("Percentage")

    # Dismissal Rate
    axes[2].bar(["Dismissal Rate"],
                [stats["dismissal_rate"] * 100],
                color=["#9467bd"])
    axes[2].set_ylim(0, 30)
    axes[2].set_title("Dismissal Rate (%)")
    axes[2].set_ylabel("Rate per 100 balls")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✓ Matchup summary saved → {save_path}")


def plot_confusion_matrix(y_test, y_pred, save_path: str = "confusion_matrix.png") -> None:
    """Styled confusion matrix."""
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=["Not Out", "Dismissed"],
        yticklabels=["Not Out", "Dismissed"],
    )
    plt.title("Confusion Matrix — Dismissal Prediction", fontsize=13)
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✓ Confusion matrix saved → {save_path}")


def plot_roc_curve(y_test, y_proba, save_path: str = "roc_curve.png") -> None:
    """ROC curve for the dismissal model."""
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc          = roc_auc_score(y_test, y_proba)

    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, color="#1f77b4", lw=2, label=f"AUC = {auc:.4f}")
    plt.plot([0, 1], [0, 1], "k--", lw=1)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve — Dismissal Probability Model")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✓ ROC curve saved → {save_path}")


def plot_feature_importance(model, feature_names: list, save_path: str = "feature_importance.png") -> None:
    """Horizontal bar chart of LGBM feature importances."""
    imp = pd.Series(model.feature_importances_, index=feature_names).sort_values()
    plt.figure(figsize=(8, 5))
    imp.plot(kind="barh", color="#ff7f0e")
    plt.title("Feature Importance — Dismissal Prediction Model")
    plt.xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✓ Feature importance saved → {save_path}")


def plot_top_bowler_threats(df: pd.DataFrame, batter: str, top_n: int = 8,
                             save_path: str = "top_threats.png") -> None:
    """Show which bowlers have the highest dismissal rate vs a given batter."""
    batter_df = df[df["batsman"] == batter]
    threat = (
        batter_df.groupby("bowler")
        .agg(balls=("batsman_runs", "count"), wickets=("is_wicket", "sum"))
        .query("balls >= 6")
        .assign(dismissal_rate=lambda x: x["wickets"] / x["balls"] * 100)
        .sort_values("dismissal_rate", ascending=False)
        .head(top_n)
        .reset_index()
    )

    plt.figure(figsize=(10, 5))
    bars = plt.barh(threat["bowler"], threat["dismissal_rate"], color="#d62728")
    plt.xlabel("Dismissal Rate (%)")
    plt.title(f"Biggest Bowling Threats to {batter}", fontsize=13)
    plt.gca().invert_yaxis()
    for bar, val in zip(bars, threat["dismissal_rate"]):
        plt.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}%", va="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"✓ Top threats chart saved → {save_path}")


# ─────────────────────────────────────────────
# 6. MAIN PIPELINE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # ── Load data ──────────────────────────────
    DATA_PATH = "deliveries.csv"   # replace with your dataset path
    print(f"Loading data from '{DATA_PATH}' …")
    df_raw = load_data(DATA_PATH)
    df     = preprocess(df_raw)
    print(f"Dataset loaded: {df.shape[0]:,} deliveries\n")

    # ── Matchup stats example ──────────────────
    BATTER = "V Kohli"
    BOWLER = "SL Malinga"
    stats  = get_matchup_stats(df, BATTER, BOWLER)
    print("Head-to-Head Stats:")
    for k, v in stats.items():
        print(f"  {k:<28}: {v}")
    print()

    plot_matchup_summary(stats)
    plot_top_bowler_threats(df, BATTER)

    # ── Top matchups table ─────────────────────
    print("\nTop 10 High-Dismissal Matchups (min 12 balls):")
    top = top_matchups(df)
    print(top.head(10).to_string(index=False))

    # ── ML Model ──────────────────────────────
    print("\nBuilding features for ML model …")
    feat_df = build_features(df)
    print(f"Feature matrix: {feat_df.shape[0]:,} samples\n")

    model, X_test, y_test, y_pred, y_proba = train_dismissal_model(feat_df)

    plot_confusion_matrix(y_test, y_pred)
    plot_roc_curve(y_test, y_proba)
    plot_feature_importance(model, X_test.columns.tolist())

    # ── Single prediction ─────────────────────
    try:
        prob = predict_dismissal_probability(model, BATTER, BOWLER, df, over=15, phase="middle")
        print(f"\nDismissal probability ({BATTER} vs {BOWLER}, over 15): {prob:.2%}")
    except ValueError as e:
        print(f"Prediction skipped: {e}")
