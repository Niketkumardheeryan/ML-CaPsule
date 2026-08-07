"""
CLI Interface for Tiny-Council.
"""

import argparse
import sys
from typing import Optional, List
from pathlib import Path

# Support direct script execution as well as module import
try:
    from .orchestrator import CouncilOrchestrator
    from .consensus import ConsensusMode
    from .utils import export_report_markdown, export_report_json, plot_consensus_trajectory
    from .llm_backend import HeuristicRuleEngine, APIBackend
except ImportError:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from tiny_council.orchestrator import CouncilOrchestrator
    from tiny_council.consensus import ConsensusMode
    from tiny_council.utils import export_report_markdown, export_report_json, plot_consensus_trajectory
    from tiny_council.llm_backend import HeuristicRuleEngine, APIBackend


def main(args_list: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        description="Tiny-Council: Multi-Agent AI Decision System CLI"
    )
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        required=False,
        default="Should we adopt a microservices architecture for our high-scale e-commerce platform?",
        help="Decision topic or question to evaluate.",
    )
    parser.add_argument(
        "--rounds", "-r",
        type=int,
        default=2,
        help="Number of deliberation rounds (default: 2).",
    )
    parser.add_argument(
        "--mode", "-m",
        type=str,
        choices=["delphi", "weighted", "borda"],
        default="delphi",
        help="Consensus mode algorithm (delphi, weighted, borda).",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="OpenAI API key (if omitted, uses built-in local heuristic engine).",
    )
    parser.add_argument(
        "--output-md",
        type=str,
        default=None,
        help="File path to save Markdown decision report.",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default=None,
        help="File path to save JSON decision trace.",
    )
    parser.add_argument(
        "--output-plot",
        type=str,
        default=None,
        help="File path to save consensus plot image.",
    )

    args = parser.parse_args(args_list)

    print("=" * 60)
    print("TINY-COUNCIL: Multi-Agent AI Decision System")
    print("=" * 60)
    print(f"Topic: {args.prompt}")
    print(f"Rounds: {args.rounds}")
    print(f"Mode: {args.mode}")

    backend = APIBackend(api_key=args.api_key) if args.api_key else HeuristicRuleEngine()
    print(f"Engine: {'External API' if args.api_key else 'Standalone Heuristic Rule Engine'}")
    print("-" * 60)

    mode_enum = ConsensusMode.DELPHI_METHOD
    if args.mode == "weighted":
        mode_enum = ConsensusMode.WEIGHTED_SCORING
    elif args.mode == "borda":
        mode_enum = ConsensusMode.BORDA_COUNT

    orchestrator = CouncilOrchestrator(backend=backend)

    print("\n[...] Convening AI Council members...")
    context = orchestrator.run_council(
        topic=args.prompt,
        rounds=args.rounds,
        mode=mode_enum,
    )

    print("\n[OK] Deliberation Completed in {:.2f}s".format(context.get_duration()))
    print(f"Agreement Index: {context.consensus_summary.get('final_agreement_index')}")
    print(f"Disagreement Entropy: {context.consensus_summary.get('disagreement_entropy')}")
    print("\n" + "=" * 60)
    print("EXECUTIVE SYNTHESIS & RESOLUTION")
    print("=" * 60)
    print(context.executive_resolution)
    print("=" * 60)

    if args.output_md:
        export_report_markdown(context, args.output_md)
        print(f"[REPORT] Saved Markdown report to: {args.output_md}")

    if args.output_json:
        export_report_json(context, args.output_json)
        print(f"[DATA] Saved JSON report to: {args.output_json}")

    if args.output_plot:
        saved_path = plot_consensus_trajectory(context, args.output_plot)
        if saved_path:
            print(f"[CHART] Saved consensus chart to: {saved_path}")

if __name__ == "__main__":
    main()
