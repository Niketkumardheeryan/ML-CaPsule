"""
Council Orchestrator for Tiny-Council.
Manages multi-round agent deliberation phases, consensus synthesis, and audit trail generation.
"""

import time
from typing import Dict, List, Any, Optional
try:
    from .agent import BaseAgent, AnalystAgent, CriticAgent, StrategistAgent, EthicsAgent, SynthesizerAgent
    from .consensus import ConsensusEngine, ConsensusMode
    from .llm_backend import BaseLLMBackend, HeuristicRuleEngine
except ImportError:
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from tiny_council.agent import BaseAgent, AnalystAgent, CriticAgent, StrategistAgent, EthicsAgent, SynthesizerAgent
    from tiny_council.consensus import ConsensusEngine, ConsensusMode
    from tiny_council.llm_backend import BaseLLMBackend, HeuristicRuleEngine


class DecisionContext:
    """Encapsulates the decision context and output artifacts."""

    def __init__(self, topic: str, metadata: Optional[Dict[str, Any]] = None):
        self.topic = topic
        self.metadata = metadata or {}
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.initial_proposals: List[Dict[str, Any]] = []
        self.peer_critiques: List[Dict[str, Any]] = []
        self.refined_proposals: List[Dict[str, Any]] = []
        self.round_history: List[List[Dict[str, Any]]] = []
        self.consensus_summary: Dict[str, Any] = {}
        self.executive_resolution: str = ""

    def complete(self):
        self.end_time = time.time()

    def get_duration(self) -> float:
        if self.end_time:
            return round(self.end_time - self.start_time, 2)
        return round(time.time() - self.start_time, 2)


class CouncilOrchestrator:
    """
    Modular Orchestrator managing multi-agent deliberation rounds and consensus generation.
    """

    def __init__(
        self,
        agents: Optional[List[BaseAgent]] = None,
        synthesizer: Optional[SynthesizerAgent] = None,
        backend: Optional[BaseLLMBackend] = None,
    ):
        self.backend = backend or HeuristicRuleEngine()
        self.agents = agents or self._default_council_agents()
        self.synthesizer = synthesizer or SynthesizerAgent(backend=self.backend)

    def _default_council_agents(self) -> List[BaseAgent]:
        """Instantiate default balanced council (Analyst, Critic, Strategist, Ethics)."""
        return [
            AnalystAgent(backend=self.backend),
            CriticAgent(backend=self.backend),
            StrategistAgent(backend=self.backend),
            EthicsAgent(backend=self.backend),
        ]

    def add_agent(self, agent: BaseAgent):
        """Add custom agent to the council."""
        self.agents.append(agent)

    def run_council(
        self,
        topic: str,
        rounds: int = 2,
        mode: ConsensusMode = ConsensusMode.DELPHI_METHOD,
        context_metadata: Optional[Dict[str, Any]] = None,
    ) -> DecisionContext:
        """
        Execute full multi-agent decision cycle.

        Phases:
        - Phase 1: Independent Initial Proposals
        - Phase 2: Peer Critiques
        - Phase 3: Position Refinements (Iterated for specified rounds)
        - Phase 4: Consensus Evaluation & Executive Synthesis
        """
        ctx = DecisionContext(topic=topic, metadata=context_metadata)

        # Phase 1: Independent Initial Assessments
        initial_evals = []
        for agent in self.agents:
            eval_res = agent.evaluate_topic(topic, context=context_metadata)
            initial_evals.append(eval_res)
        ctx.initial_proposals = initial_evals
        ctx.round_history.append(initial_evals)

        current_evals = initial_evals

        # Phase 2 & 3: Multi-Round Deliberation (Critique -> Refine)
        for r in range(rounds):
            # Peer Critique
            critiques = []
            for agent in self.agents:
                crit_res = agent.critique_peers(topic, current_evals)
                critiques.append(crit_res)
            ctx.peer_critiques.extend(critiques)

            # Refinement
            refined_evals = []
            for agent, prev_eval in zip(self.agents, current_evals):
                ref_res = agent.refine_position(
                    topic=topic,
                    initial_response=prev_eval.get("response") or prev_eval.get("refined_response", ""),
                    critiques=critiques,
                )
                refined_evals.append(ref_res)

            ctx.round_history.append(refined_evals)
            current_evals = refined_evals

        ctx.refined_proposals = current_evals

        # Phase 4: Consensus Evaluation & Final Executive Synthesis
        weighted_scoring = ConsensusEngine.compute_weighted_scoring(current_evals)
        delphi_metrics = ConsensusEngine.compute_delphi_convergence(ctx.round_history)

        ctx.consensus_summary = {
            "mode": mode.value,
            "weighted_scoring": weighted_scoring,
            "delphi_metrics": delphi_metrics,
            "final_agreement_index": delphi_metrics["final_agreement_index"],
            "disagreement_entropy": delphi_metrics["disagreement_entropy"],
        }

        # Synthesizer Chair creates executive resolution
        sys_prompt = self.synthesizer.get_system_prompt()
        proposals_text = "\n\n".join(
            [f"--- Agent {p['agent_name']} ({p['role']}) ---\n{p.get('refined_response') or p.get('response')}" for p in current_evals]
        )
        user_prompt = (
            f"Topic: '{topic}'\n"
            f"Consensus Agreement Index: {delphi_metrics['final_agreement_index']}\n"
            f"Agent Refined Standpoints:\n{proposals_text}\n"
            f"Draft the definitive executive council decision and action plan."
        )

        ctx.executive_resolution = self.synthesizer.backend.generate_response(
            sys_prompt, user_prompt, temperature=self.synthesizer.temperature
        )

        ctx.complete()
        return ctx

if __name__ == "__main__":
    orch = CouncilOrchestrator()
    res_ctx = orch.run_council("Should we adopt serverless computing?", rounds=1)
    print(f"[Self-Test] Orchestrator executed in {res_ctx.get_duration()}s | Resolution length: {len(res_ctx.executive_resolution)} chars.")
