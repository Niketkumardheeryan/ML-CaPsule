import unittest
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crime_analytics import CrimeDataAnalyzer, HotspotDetector, RiskScorer, generate_automated_insights

class TestCrimeAnalytics(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        csv_path = os.path.join(os.path.dirname(__file__), "crime_dataset.csv")
        cls.df = pd.read_csv(csv_path)

    def test_dataset_loaded(self):
        self.assertFalse(self.df.empty, "Dataset should not be empty.")
        self.assertIn("incident_id", self.df.columns)
        self.assertIn("latitude", self.df.columns)
        self.assertIn("longitude", self.df.columns)
        self.assertIn("severity_score", self.df.columns)

    def test_kpi_summary(self):
        analyzer = CrimeDataAnalyzer(self.df)
        kpis = analyzer.get_summary_kpis()
        self.assertGreater(kpis["total_incidents"], 0)
        self.assertGreaterEqual(kpis["avg_severity"], 0)
        self.assertGreaterEqual(kpis["solved_rate_pct"], 0)

    def test_time_series_trends(self):
        analyzer = CrimeDataAnalyzer(self.df)
        monthly = analyzer.get_time_series_trends(freq="ME")
        self.assertFalse(monthly.empty)
        self.assertIn("total_incidents", monthly.columns)

    def test_mom_yoy_growth(self):
        analyzer = CrimeDataAnalyzer(self.df)
        growth_df = analyzer.get_mom_yoy_comparison()
        self.assertIn("MoM_Growth_%", growth_df.columns)
        self.assertIn("YoY_Growth_%", growth_df.columns)

    def test_hotspot_detector(self):
        detector = HotspotDetector(self.df)
        hotspots = detector.get_district_hotspots()
        self.assertFalse(hotspots.empty)
        self.assertIn("center_lat", hotspots.columns)
        self.assertIn("incident_count", hotspots.columns)

    def test_risk_scorer(self):
        scorer = RiskScorer(self.df)
        risk_df = scorer.calculate_district_risk_scores()
        self.assertFalse(risk_df.empty)
        self.assertIn("risk_score", risk_df.columns)
        self.assertIn("risk_level", risk_df.columns)
        self.assertTrue((risk_df["risk_score"] >= 0).all() and (risk_df["risk_score"] <= 100).all())

    def test_automated_insights(self):
        insights = generate_automated_insights(self.df)
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)

if __name__ == "__main__":
    unittest.main()
