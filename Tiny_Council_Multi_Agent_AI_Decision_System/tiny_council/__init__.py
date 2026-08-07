"""
Tiny-Council: Multi-Agent AI Decision System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A modular framework where specialized AI agents collaborate, critique, refine,
and synthesize consensus decisions through structured reasoning and voting mechanisms.
"""

from .agent import BaseAgent, AnalystAgent, CriticAgent, StrategistAgent, EthicsAgent, SynthesizerAgent, CustomAgent
from .consensus import ConsensusEngine, ConsensusMode, BordaCount, WeightedScoring, DelphiMethod
from .llm_backend import BaseLLMBackend, HeuristicRuleEngine, APIBackend
from .orchestrator import CouncilOrchestrator, DecisionContext
from .utils import export_report_markdown, export_report_json, plot_consensus_trajectory

__version__ = "1.0.0"

__all__ = [
    "BaseAgent",
    "AnalystAgent",
    "CriticAgent",
    "StrategistAgent",
    "EthicsAgent",
    "SynthesizerAgent",
    "CustomAgent",
    "ConsensusEngine",
    "ConsensusMode",
    "BordaCount",
    "WeightedScoring",
    "DelphiMethod",
    "BaseLLMBackend",
    "HeuristicRuleEngine",
    "APIBackend",
    "CouncilOrchestrator",
    "DecisionContext",
    "export_report_markdown",
    "export_report_json",
    "plot_consensus_trajectory",
]
