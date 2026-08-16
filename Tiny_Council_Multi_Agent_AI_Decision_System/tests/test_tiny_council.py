"""
Unit Tests for Tiny-Council Multi-Agent AI Decision System.
"""

import os
import tempfile
import sys
import unittest
from pathlib import Path

# Add project directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tiny_council.agent import (
    AnalystAgent,
    CriticAgent,
    StrategistAgent,
    EthicsAgent,
    SynthesizerAgent,
    CustomAgent,
)
from tiny_council.consensus import (
    ConsensusEngine,
    BordaCount,
    WeightedScoring,
    DelphiMethod,
    ConsensusMode,
)
from tiny_council.llm_backend import HeuristicRuleEngine, APIBackend
from tiny_council.orchestrator import CouncilOrchestrator, DecisionContext
from tiny_council.utils import export_report_markdown, export_report_json, plot_consensus_trajectory
from tiny_council.cli import main as cli_main


class TestTinyCouncilAgentSystem(unittest.TestCase):
    def setUp(self):
        self.backend = HeuristicRuleEngine()

    def test_agent_evaluations(self):
        analyst = AnalystAgent(backend=self.backend)
        critic = CriticAgent(backend=self.backend)
        topic = "Should we migrate from monolithic to microservices architecture?"

        eval_analyst = analyst.evaluate_topic(topic)
        self.assertEqual(eval_analyst["role"], "Analyst")
        self.assertGreaterEqual(eval_analyst["confidence"], 0.0)
        self.assertLessEqual(eval_analyst["confidence"], 1.0)
        self.assertIn("Analyst", eval_analyst["response"])

        eval_critic = critic.evaluate_topic(topic)
        self.assertEqual(eval_critic["role"], "Critic")
        self.assertIn("Critic", eval_critic["response"])

    def test_custom_agent(self):
        custom = CustomAgent(
            name="Security Specialist",
            role="Security Auditor",
            persona_description="Audits threat models and zero-trust paradigms.",
            weight=1.5,
            backend=self.backend,
        )
        res = custom.evaluate_topic("Implement JWT authentication.")
        self.assertEqual(res["agent_name"], "Security Specialist")
        self.assertEqual(res["role"], "Security Auditor")
        self.assertEqual(res["weight"], 1.5)

    def test_consensus_metrics(self):
        confidences = [0.8, 0.82, 0.85, 0.79]
        weights = [1.0, 1.2, 1.1, 1.0]

        agr = ConsensusEngine.calculate_agreement_index(confidences, weights)
        self.assertGreater(agr, 0.85)

        entropy = ConsensusEngine.calculate_disagreement_entropy([0.25, 0.25, 0.25, 0.25])
        self.assertAlmostEqual(entropy, 2.0, places=2)

        weighted_res = ConsensusEngine.compute_weighted_scoring([
            {"confidence": 0.9, "weight": 1.0},
            {"confidence": 0.8, "weight": 2.0},
        ])
        self.assertAlmostEqual(weighted_res["weighted_score"], 0.8333, places=3)

    def test_borda_count_voting(self):
        options = ["Option A", "Option B", "Option C"]
        rankings = [
            ["Option A", "Option B", "Option C"],
            ["Option A", "Option C", "Option B"],
            ["Option B", "Option A", "Option C"],
        ]
        res = BordaCount.evaluate(options, rankings)
        self.assertEqual(res["winner"], "Option A")
        self.assertIn("Option A", res["scores"])

    def test_orchestrator_run_council(self):
        orchestrator = CouncilOrchestrator(backend=self.backend)
        topic = "Should we adopt Rust for low-latency backend services?"

        ctx = orchestrator.run_council(topic=topic, rounds=2, mode=ConsensusMode.DELPHI_METHOD)

        self.assertIsInstance(ctx, DecisionContext)
        self.assertEqual(len(ctx.initial_proposals), 4)
        self.assertEqual(len(ctx.refined_proposals), 4)
        self.assertGreater(len(ctx.executive_resolution), 20)
        self.assertIn("final_agreement_index", ctx.consensus_summary)

    def test_report_export_and_plot(self):
        orchestrator = CouncilOrchestrator(backend=self.backend)
        ctx = orchestrator.run_council(topic="Adopt AI Code Assistant", rounds=1)

        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = os.path.join(tmpdir, "report.md")
            json_path = os.path.join(tmpdir, "report.json")
            plot_path = os.path.join(tmpdir, "chart.png")

            export_report_markdown(ctx, md_path)
            export_report_json(ctx, json_path)
            saved_plot = plot_consensus_trajectory(ctx, plot_path)

            self.assertTrue(os.path.exists(md_path))
            self.assertTrue(os.path.exists(json_path))
            if saved_plot:
                self.assertTrue(os.path.exists(plot_path))

    def test_cli_execution(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = os.path.join(tmpdir, "cli_report.md")
            json_path = os.path.join(tmpdir, "cli_report.json")

            args = [
                "--prompt", "CLI test prompt for multi-agent evaluation.",
                "--rounds", "1",
                "--output-md", md_path,
                "--output-json", json_path,
            ]
            cli_main(args)

            self.assertTrue(os.path.exists(md_path))
            self.assertTrue(os.path.exists(json_path))


if __name__ == "__main__":
    unittest.main()
