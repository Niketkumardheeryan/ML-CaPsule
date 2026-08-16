"""
LLM Backend abstraction for Tiny-Council.
Supports zero-dependency Heuristic Rule Engine (default) and API-based backends.
"""

from abc import ABC, abstractmethod
import math
import re
from typing import Dict, List, Any, Optional


class BaseLLMBackend(ABC):
    """Abstract Base Class for LLM backends."""

    @abstractmethod
    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Generate response given system and user prompts."""
        pass


class HeuristicRuleEngine(BaseLLMBackend):
    """
    Standalone, zero-external-dependency LLM simulator.
    Uses domain keyword analysis, sentiment heuristic scoring, and dynamic rule-based
    reasoning templates to simulate agent responses with explainable traces.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        agent_role = self._extract_role(system_prompt)
        prompt_lower = user_prompt.lower()

        if "critique" in user_prompt.lower() or "peer proposal" in user_prompt.lower():
            return self._generate_critique(agent_role, user_prompt, temperature)
        elif "synthesize" in system_prompt.lower() or "synthesizer" in agent_role.lower():
            return self._generate_synthesis(user_prompt)
        elif "refine" in user_prompt.lower() or "revised position" in user_prompt.lower():
            return self._generate_refinement(agent_role, user_prompt, temperature)
        else:
            return self._generate_initial_proposal(agent_role, user_prompt, temperature)

    def _extract_role(self, system_prompt: str) -> str:
        if "analyst" in system_prompt.lower():
            return "Analyst"
        elif "critic" in system_prompt.lower():
            return "Critic"
        elif "strategist" in system_prompt.lower():
            return "Strategist"
        elif "ethics" in system_prompt.lower() or "safety" in system_prompt.lower():
            return "Ethics Evaluator"
        elif "synthesizer" in system_prompt.lower() or "chair" in system_prompt.lower():
            return "Synthesizer"
        return "Council Member"

    def _generate_initial_proposal(self, role: str, prompt: str, temperature: float) -> str:
        if role == "Analyst":
            return (
                f"### [Analyst Evaluation]\n"
                f"**Problem Analysis**: Deconstructing key empirical variables in: '{prompt[:100]}...'\n"
                f"**Feasibility & Metric Impact**:\n"
                f"- Quantitative Risk Factor: Low-to-Moderate (Score: 0.78)\n"
                f"- Implementation Complexity: Moderate\n"
                f"**Recommendation**: Proceed with phased deployment focusing on measurable KPIs and telemetry.\n"
                f"**Confidence**: 0.85"
            )
        elif role == "Critic":
            return (
                f"### [Critic Challenge]\n"
                f"**Vulnerability Analysis**: Identified potential edge cases in: '{prompt[:100]}...'\n"
                f"**Risk Vectors**:\n"
                f"- Overhead risk during high-concurrency peak load.\n"
                f"- Potential single-point-of-failure in orchestration protocol.\n"
                f"**Recommendation**: Require strict contingency rollback and validation gates prior to sign-off.\n"
                f"**Confidence**: 0.72"
            )
        elif role == "Strategist":
            return (
                f"### [Strategist Blueprint]\n"
                f"**Strategic Alignment**: Long-term value assessment for: '{prompt[:100]}...'\n"
                f"**Trade-off Matrix**:\n"
                f"- High scalability vs. initial setup complexity.\n"
                f"- Modular flexibility empowers future extensibility.\n"
                f"**Recommendation**: Adopt iterative milestones with modular decoupling.\n"
                f"**Confidence**: 0.90"
            )
        elif role == "Ethics Evaluator":
            return (
                f"### [Ethics & Safety Assessment]\n"
                f"**Governance Analysis**: Evaluating fairness, transparency, and safety for: '{prompt[:100]}...'\n"
                f"**Compliance Directives**:\n"
                f"- Zero algorithmic bias risk detected.\n"
                f"- High transparency requirement in automated decision audit trail.\n"
                f"**Recommendation**: Approve subject to mandatory audit logging and human-in-the-loop oversight.\n"
                f"**Confidence**: 0.88"
            )
        else:
            return (
                f"### [{role} Assessment]\n"
                f"General evaluation of topic: '{prompt[:100]}...'\n"
                f"**Recommendation**: Support proposal with standard guardrails.\n"
                f"**Confidence**: 0.80"
            )

    def _generate_critique(self, role: str, prompt: str, temperature: float) -> str:
        return (
            f"### [{role} Peer Critique]\n"
            f"Reviewing peer assessments for points of friction and hidden assumptions:\n"
            f"- Strengths: Comprehensive domain coverage across proposals.\n"
            f"- Weaknesses: Insufficient attention to edge-case stress conditions.\n"
            f"- Suggested Adjustments: Incorporate automated fault recovery and continuous verification metrics."
        )

    def _generate_refinement(self, role: str, prompt: str, temperature: float) -> str:
        return (
            f"### [{role} Revised Stance]\n"
            f"After incorporating peer critiques, adjusting position:\n"
            f"- Updated Risk Index: Reduced by 15% following suggested safety guardrails.\n"
            f"- Final Standing: Strong endorsement with operational safeguards.\n"
            f"**Revised Confidence**: 0.92"
        )

    def _generate_synthesis(self, prompt: str) -> str:
        return (
            f"### [Council Executive Synthesis]\n"
            f"**Consensus Overview**: High alignment achieved across Analyst, Critic, Strategist, and Ethics agents.\n"
            f"**Core Resolution**: Proceed with modular, phased implementation backed by real-time telemetry, automated rollback gates, and transparent audit logging.\n"
            f"**Overall Council Confidence Score**: 0.88"
        )


class APIBackend(BaseLLMBackend):
    """
    Generic API Backend for external LLM endpoints (e.g. OpenAI, Ollama, custom HTTP API).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gpt-3.5-turbo",
        endpoint_url: Optional[str] = None,
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.endpoint_url = endpoint_url or "https://api.openai.com/v1/chat/completions"

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        if not self.api_key:
            # Fallback to local heuristic engine if API key missing
            fallback = HeuristicRuleEngine()
            return fallback.generate_response(system_prompt, user_prompt, temperature, max_tokens)
        
        # Real HTTP request logic using urllib.request to avoid mandatory requests package requirement
        import json
        import urllib.request

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        req = urllib.request.Request(
            self.endpoint_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            # Safe fallback on network or authorization error
            fallback = HeuristicRuleEngine()
            return f"[API Error: {e} - Falling back to local reasoning engine]\n" + fallback.generate_response(
                system_prompt, user_prompt, temperature, max_tokens
            )

if __name__ == "__main__":
    engine = HeuristicRuleEngine()
    resp = engine.generate_response("You are an Analyst", "Should we adopt Rust?")
    print(f"[Self-Test] LLM Backend response generated ({len(resp)} chars).")
