import pandas as pd
import numpy as np

class CrimeDataAnalyzer:
    """Core analytical module for crime data aggregation, trend decomposition, and statistics."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        if "timestamp" in self.df.columns:
            self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
            self.df["year_month"] = self.df["timestamp"].dt.to_period("M").astype(str)

    def get_summary_kpis(self):
        total_incidents = len(self.df)
        avg_severity = round(self.df["severity_score"].mean(), 2) if "severity_score" in self.df.columns else 0
        avg_response_time = round(self.df["response_time_min"].mean(), 1) if "response_time_min" in self.df.columns else 0
        top_crime = self.df["crime_type"].mode()[0] if not self.df.empty else "N/A"
        solved_rate = round((self.df["status"] == "Solved").mean() * 100, 1) if "status" in self.df.columns else 0
        
        return {
            "total_incidents": total_incidents,
            "avg_severity": avg_severity,
            "avg_response_time_min": avg_response_time,
            "top_crime_type": top_crime,
            "solved_rate_pct": solved_rate
        }

    def get_time_series_trends(self, freq="ME"):
        """Calculate crime counts over time by specified frequency ('ME' for Month End, 'YE' for Year End)."""
        df_ts = self.df.set_index("timestamp").resample(freq).agg(
            total_incidents=("incident_id", "count"),
            avg_severity=("severity_score", "mean")
        ).reset_index()
        df_ts["avg_severity"] = df_ts["avg_severity"].round(2)
        return df_ts

    def get_mom_yoy_comparison(self):
        """Calculate Month-over-Month (MoM) and Year-over-Year (YoY) crime rate changes."""
        monthly = self.df.groupby("year_month").agg(
            incident_count=("incident_id", "count"),
            avg_severity=("severity_score", "mean")
        ).reset_index()
        
        monthly["MoM_Growth_%"] = monthly["incident_count"].pct_change() * 100
        monthly["MoM_Growth_%"] = monthly["MoM_Growth_%"].round(2)
        
        # YoY change: calculate comparison with 12 months prior
        monthly["YoY_Growth_%"] = monthly["incident_count"].pct_change(12) * 100
        monthly["YoY_Growth_%"] = monthly["YoY_Growth_%"].round(2)
        
        return monthly

    def get_category_distribution(self):
        """Distribution and frequency breakdown of crime types."""
        dist = self.df.groupby("crime_type").agg(
            count=("incident_id", "count"),
            avg_severity=("severity_score", "mean"),
            avg_response_time=("response_time_min", "mean")
        ).reset_index()
        
        dist["percentage"] = round((dist["count"] / len(self.df)) * 100, 2)
        dist["avg_severity"] = dist["avg_severity"].round(2)
        dist["avg_response_time"] = dist["avg_response_time"].round(1)
        return dist.sort_values("count", ascending=False)

    def get_hourly_day_heatmap_data(self):
        """Cross-tabulation of day of week vs hour for heatmap visualization."""
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        pivot = pd.crosstab(self.df["day_of_week"], self.df["hour"])
        pivot = pivot.reindex(days_order)
        return pivot


class HotspotDetector:
    """Identification of crime hotspots using spatial aggregation and risk clustering."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def get_district_hotspots(self):
        """Aggregate crime volume, severity, and risk scores by district."""
        hotspots = self.df.groupby("district").agg(
            incident_count=("incident_id", "count"),
            avg_severity=("severity_score", "mean"),
            center_lat=("latitude", "mean"),
            center_lon=("longitude", "mean")
        ).reset_index()
        
        hotspots["avg_severity"] = hotspots["avg_severity"].round(2)
        hotspots["center_lat"] = hotspots["center_lat"].round(4)
        hotspots["center_lon"] = hotspots["center_lon"].round(4)
        return hotspots.sort_values("incident_count", ascending=False)


class RiskScorer:
    """Generates composite risk scores (0 - 100 scale) for locations based on volume, severity, and recency."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        if "timestamp" in self.df.columns:
            self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])

    def calculate_district_risk_scores(self, recency_weight=0.3, volume_weight=0.4, severity_weight=0.3):
        """
        Calculate composite risk score per district.
        Formulation: Risk = w_vol * Norm(Volume) + w_sev * Norm(AvgSeverity) + w_rec * Norm(RecentIncidents)
        """
        max_date = self.df["timestamp"].max()
        recent_threshold = max_date - pd.Timedelta(days=90)
        
        agg = self.df.groupby("district").agg(
            total_incidents=("incident_id", "count"),
            avg_severity=("severity_score", "mean"),
            recent_incidents=("timestamp", lambda x: (x >= recent_threshold).sum())
        ).reset_index()
        
        # Min-Max Normalization helper
        def norm(series):
            min_val = series.min()
            max_val = series.max()
            if max_val == min_val:
                return pd.Series(0.5, index=series.index)
            return (series - min_val) / (max_val - min_val)
            
        agg["norm_vol"] = norm(agg["total_incidents"])
        agg["norm_sev"] = norm(agg["avg_severity"])
        agg["norm_rec"] = norm(agg["recent_incidents"])
        
        # Weighted raw risk score (0 to 1)
        raw_risk = (
            volume_weight * agg["norm_vol"] +
            severity_weight * agg["norm_sev"] +
            recency_weight * agg["norm_rec"]
        )
        
        # Scale to 0 - 100
        agg["risk_score"] = (raw_risk * 100).round(1)
        
        def assign_risk_category(score):
            if score >= 75:
                return "Critical"
            elif score >= 50:
                return "High"
            elif score >= 25:
                return "Medium"
            else:
                return "Low"
                
        agg["risk_level"] = agg["risk_score"].apply(assign_risk_category)
        
        return agg[["district", "total_incidents", "avg_severity", "recent_incidents", "risk_score", "risk_level"]].sort_values("risk_score", ascending=False)


def generate_automated_insights(df: pd.DataFrame) -> list:
    """Generate rule-based statistical observations and insights from the crime dataset."""
    analyzer = CrimeDataAnalyzer(df)
    kpis = analyzer.get_summary_kpis()
    cat_dist = analyzer.get_category_distribution()
    hotspots = HotspotDetector(df).get_district_hotspots()
    scorer = RiskScorer(df).calculate_district_risk_scores()
    
    insights = []
    
    # 1. Primary Crime Insight
    top_cat = cat_dist.iloc[0]
    insights.append(f"**Dominant Crime Category**: '{top_cat['crime_type']}' is the most frequent crime category, accounting for **{top_cat['percentage']}%** of all incidents ({top_cat['count']} records).")
    
    # 2. Hotspot & Highest Risk Area
    top_risk = scorer.iloc[0]
    insights.append(f"**Highest Risk Hotspot**: District **{top_risk['district']}** exhibits the highest risk score of **{top_risk['risk_score']}/100** ({top_risk['risk_level']} Level) with {top_risk['total_incidents']} recorded incidents.")
    
    # 3. Peak Crime Hours
    df_temp = df.copy()
    df_temp["timestamp"] = pd.to_datetime(df_temp["timestamp"])
    peak_hour = df_temp["timestamp"].dt.hour.mode()[0]
    insights.append(f"**Temporal Peak**: The highest density of crimes occurs during peak hour **{peak_hour}:00 - {peak_hour+1}:00**, indicating heightened night-time activity.")
    
    # 4. Solution & Case Resolution Rate
    insights.append(f"**Case Resolution Status**: The overall case clearance rate stands at **{kpis['solved_rate_pct']}%**, with an average emergency response time of **{kpis['avg_response_time_min']} minutes**.")
    
    return insights
