"""
Consensus Engine & Voting Mechanisms for Tiny-Council.
Includes Borda Count, Weighted Scoring, Delphi Iterative Convergence,
Agreement Index, Shannon Disagreement Entropy, and Convergence Delta metrics.
"""

from enum import Enum
import math
from typing import Dict, List, Any, Tuple, Optional


class ConsensusMode(Enum):
    WEIGHTED_SCORING = "weighted_scoring"
    BORDA_COUNT = "borda_count"
    DELPHI_METHOD = "delphi_method"


class ConsensusEngine:
    """
    Computes voting outcomes and consensus metrics across agent evaluations.
    """

    @staticmethod
    def calculate_agreement_index(confidences: List[float], weights: Optional[List[float]] = None) -> float:
        """
        Calculates normalized Agreement Index A in [0.0, 1.0].
        High agreement index indicates consensus around high confidence scores.
        Formula: A = 1 - (2 * Weighted_Std_Dev)
        """
        if not confidences:
            return 0.0
        if len(confidences) == 1:
            return 1.0

        if weights is None or len(weights) != len(confidences):
            weights = [1.0] * len(confidences)

        total_weight = sum(weights)
        if total_weight == 0:
            return 0.0

        mean = sum(c * w for c, w in zip(confidences, weights)) / total_weight
        variance = sum(w * ((c - mean) ** 2) for c, w in zip(confidences, weights)) / total_weight
        std_dev = math.sqrt(variance)

        # Scale std_dev (max possible std dev for range [0,1] is 0.5)
        agreement = 1.0 - (2.0 * std_dev)
        return max(0.0, min(1.0, float(agreement)))

    @staticmethod
    def calculate_disagreement_entropy(probabilities: List[float]) -> float:
        """
        Calculates Shannon Entropy H(D) of decision option distribution.
        H(D) = - sum(p * log2(p))
        Low entropy indicates high consensus on a single decision path.
        """
        entropy = 0.0
        total_p = sum(probabilities)
        if total_p == 0:
            return 0.0

        for p in probabilities:
            norm_p = p / total_p
            if norm_p > 0:
                entropy -= norm_p * math.log2(norm_p)
        return float(entropy)

    @staticmethod
    def calculate_convergence_delta(round_confidences: List[List[float]]) -> float:
        """
        Calculates rate of change in mean confidence / agreement between debate rounds.
        Convergence Delta = Agreement(Round_N) - Agreement(Round_N-1)
        """
        if len(round_confidences) < 2:
            return 0.0

        prev_agreement = ConsensusEngine.calculate_agreement_index(round_confidences[-2])
        curr_agreement = ConsensusEngine.calculate_agreement_index(round_confidences[-1])
        return curr_agreement - prev_agreement

    @staticmethod
    def compute_weighted_scoring(agent_evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Computes weighted score based on agent confidence and assigned weight.
        """
        if not agent_evaluations:
            return {"weighted_score": 0.0, "agreement_index": 0.0}

        total_weighted_conf = 0.0
        total_weight = 0.0
        confidences = []
        weights = []

        for eval_item in agent_evaluations:
            w = eval_item.get("weight", 1.0)
            c = eval_item.get("confidence", 0.8)
            confidences.append(c)
            weights.append(w)
            total_weighted_conf += c * w
            total_weight += w

        weighted_mean = total_weighted_conf / total_weight if total_weight > 0 else 0.0
        agreement = ConsensusEngine.calculate_agreement_index(confidences, weights)

        return {
            "weighted_score": round(weighted_mean, 4),
            "agreement_index": round(agreement, 4),
            "agent_count": len(agent_evaluations),
        }

    @staticmethod
    def compute_borda_count(
        options: List[str], agent_rankings: List[List[str]], agent_weights: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Computes Borda Count voting across ranked options.
        Points awarded per position: (N_options - rank_position) * agent_weight
        """
        if not options or not agent_rankings:
            return {"rankings": [], "scores": {}}

        n_options = len(options)
        if agent_weights is None or len(agent_weights) != len(agent_rankings):
            agent_weights = [1.0] * len(agent_rankings)

        scores = {opt: 0.0 for opt in options}

        for ranking, w in zip(agent_rankings, agent_weights):
            for rank_idx, opt in enumerate(ranking):
                if opt in scores:
                    pts = (n_options - rank_idx) * w
                    scores[opt] += pts

        sorted_options = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return {
            "winner": sorted_options[0][0] if sorted_options else None,
            "ranked_outcomes": sorted_options,
            "scores": {k: round(v, 2) for k, v in scores.items()},
        }

    @staticmethod
    def compute_delphi_convergence(
        round_history: List[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Analyzes multi-round Delphi convergence trajectories.
        """
        agreements = []
        confidences_by_round = []

        for r_idx, round_evals in enumerate(round_history):
            confs = [e.get("confidence", 0.8) for e in round_evals]
            wts = [e.get("weight", 1.0) for e in round_evals]
            agreements.append(ConsensusEngine.calculate_agreement_index(confs, wts))
            confidences_by_round.append(confs)

        deltas = []
        for i in range(1, len(agreements)):
            deltas.append(round(agreements[i] - agreements[i - 1], 4))

        final_conf = confidences_by_round[-1] if confidences_by_round else []
        entropy = ConsensusEngine.calculate_disagreement_entropy(final_conf)

        return {
            "rounds_executed": len(round_history),
            "agreement_per_round": [round(a, 4) for a in agreements],
            "convergence_deltas": deltas,
            "final_agreement_index": round(agreements[-1], 4) if agreements else 0.0,
            "disagreement_entropy": round(entropy, 4),
            "is_converged": deltas[-1] >= 0 if deltas else True,
        }


# Convenience classes for direct API access
class BordaCount:
    @staticmethod
    def evaluate(options: List[str], rankings: List[List[str]], weights: Optional[List[float]] = None):
        return ConsensusEngine.compute_borda_count(options, rankings, weights)


class WeightedScoring:
    @staticmethod
    def evaluate(agent_evaluations: List[Dict[str, Any]]):
        return ConsensusEngine.compute_weighted_scoring(agent_evaluations)


class DelphiMethod:
    @staticmethod
    def evaluate(round_history: List[List[Dict[str, Any]]]):
        return ConsensusEngine.compute_delphi_convergence(round_history)

if __name__ == "__main__":
    score_res = ConsensusEngine.compute_weighted_scoring([{"confidence": 0.85, "weight": 1.2}])
    print(f"[Self-Test] Consensus Score: {score_res['weighted_score']} | Agreement: {score_res['agreement_index']}")
