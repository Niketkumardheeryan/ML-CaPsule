"""
Utilities for Tiny-Council: Report Exporting & Consensus Trajectory Visualization.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
try:
    from .orchestrator import DecisionContext
except ImportError:
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from tiny_council.orchestrator import DecisionContext


def export_report_markdown(ctx: DecisionContext, filepath: Optional[str] = None) -> str:
    """Generate Markdown report for decision context."""
    lines = []
    lines.append(f"# Tiny-Council Decision Report")
    lines.append(f"**Topic**: {ctx.topic}")
    lines.append(f"**Duration**: {ctx.get_duration()} seconds")
    lines.append(f"**Agreement Index**: {ctx.consensus_summary.get('final_agreement_index', 0.0)}")
    lines.append(f"**Disagreement Entropy**: {ctx.consensus_summary.get('disagreement_entropy', 0.0)}")
    lines.append("\n---\n")

    lines.append("## Executive Synthesis")
    lines.append(ctx.executive_resolution)
    lines.append("\n---\n")

    lines.append("## Agent Final Standpoints")
    for prop in ctx.refined_proposals:
        lines.append(f"### {prop['agent_name']} ({prop['role']})")
        lines.append(f"- **Weight**: {prop['weight']} | **Confidence**: {prop['confidence']}")
        lines.append(f"\n{prop.get('refined_response', prop.get('response', ''))}\n")

    lines.append("## Deliberation History & Metrics")
    delphi = ctx.consensus_summary.get("delphi_metrics", {})
    lines.append(f"- **Total Rounds**: {delphi.get('rounds_executed', 0)}")
    lines.append(f"- **Agreement Per Round**: {delphi.get('agreement_per_round', [])}")
    lines.append(f"- **Convergence Deltas**: {delphi.get('convergence_deltas', [])}")

    content = "\n".join(lines)

    if filepath:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return content


def export_report_json(ctx: DecisionContext, filepath: Optional[str] = None) -> str:
    """Generate JSON representation of decision context."""
    data = {
        "topic": ctx.topic,
        "metadata": ctx.metadata,
        "duration_seconds": ctx.get_duration(),
        "consensus_summary": ctx.consensus_summary,
        "executive_resolution": ctx.executive_resolution,
        "initial_proposals": ctx.initial_proposals,
        "refined_proposals": ctx.refined_proposals,
        "round_history": ctx.round_history,
    }
    content = json.dumps(data, indent=2)

    if filepath:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return content


def plot_consensus_trajectory(ctx: DecisionContext, save_path: Optional[str] = None):
    """
    Plot consensus metrics (Agreement Index & Confidence Distributions) across rounds.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend
        import matplotlib.pyplot as plt

        delphi = ctx.consensus_summary.get("delphi_metrics", {})
        agreements = delphi.get("agreement_per_round", [])
        rounds = list(range(1, len(agreements) + 1))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Agreement Trajectory
        ax1.plot(rounds, agreements, marker="o", color="#2563eb", linewidth=2.5, markersize=8)
        ax1.set_title("Consensus Agreement Index Over Rounds", fontsize=12, fontweight="bold")
        ax1.set_xlabel("Deliberation Round", fontsize=10)
        ax1.set_ylabel("Agreement Index (0.0 - 1.0)", fontsize=10)
        ax1.set_ylim(0.0, 1.05)
        ax1.grid(True, linestyle="--", alpha=0.6)

        # Agent Confidence Bar Chart
        agent_names = [p["agent_name"] for p in ctx.refined_proposals]
        confidences = [p["confidence"] for p in ctx.refined_proposals]
        colors = ["#3b82f6", "#ef4444", "#10b981", "#8b5cf6", "#f59e0b"]

        ax2.bar(agent_names, confidences, color=colors[: len(agent_names)], alpha=0.85, edgecolor="black")
        ax2.set_title("Agent Confidence Scores", fontsize=12, fontweight="bold")
        ax2.set_xlabel("Agent Role", fontsize=10)
        ax2.set_ylabel("Confidence Score", fontsize=10)
        ax2.set_ylim(0.0, 1.05)
        ax2.grid(axis="y", linestyle="--", alpha=0.6)

        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300)
            plt.close(fig)
            return save_path
        else:
            plt.show()
            plt.close(fig)
            return None
    except Exception as e:
        print(f"Warning: Visualization plot skipped due to environment constraint ({e}).")
        return None

if __name__ == "__main__":
    try:
        from .orchestrator import CouncilOrchestrator
    except ImportError:
        import sys
        from pathlib import Path
        PROJECT_ROOT = Path(__file__).resolve().parents[1]
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.insert(0, str(PROJECT_ROOT))
        from tiny_council.orchestrator import CouncilOrchestrator

    orch = CouncilOrchestrator()
    ctx = orch.run_council("Utils self-test topic", rounds=1)
    md_str = export_report_markdown(ctx)
    print(f"[Self-Test] Utils generated markdown report ({len(md_str)} chars).")
