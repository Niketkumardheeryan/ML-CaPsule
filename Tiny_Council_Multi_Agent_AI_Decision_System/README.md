# 🏛️ Tiny-Council: Multi-Agent AI Decision System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Architecture: Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-green.svg)](#system-architecture)
[![Consensus: Delphi%20%2B%20Borda](https://img.shields.io/badge/Consensus-Delphi%20%2B%20Borda-orange.svg)](#consensus-mechanisms)

**Tiny-Council** is an open-source, multi-agent AI decision-making framework designed to aggregate, critique, refine, and synthesize complex decisions across specialized AI personas. By combining mathematical voting models (Borda Count, Weighted Scoring, Delphi Iterative Convergence) with structured peer-review cycles, Tiny-Council eliminates single-prompt bias and produces audit-ready executive resolutions.

---

## 🌟 Key Features

1. **Multi-Agent Deliberation Architecture**:
   - Structured 4-phase decision cycle: **Initial Assessment -> Peer Critique -> Position Refinement -> Executive Synthesis**.
   - Modular event flow with full execution telemetry and duration metrics.

2. **Role-Based AI Agent Hierarchy**:
   - **Analyst Agent (`AnalystAgent`)**: Empirical metric evaluation, risk modeling, and technical feasibility.
   - **Critic Agent (`CriticAgent`)**: Devil's advocate, vulnerability analysis, and edge-case identification.
   - **Strategist Agent (`StrategistAgent`)**: Strategic alignment, modular trade-offs, and long-term scalability.
   - **Ethics Agent (`EthicsAgent`)**: Algorithmic bias, compliance, safety guardrails, and human impact.
   - **Synthesizer Agent (`SynthesizerAgent`)**: Council chair formulating unified executive resolutions.
   - **Custom Agents (`CustomAgent`)**: Dynamic creation of domain-specific experts on demand.

3. **Mathematical Consensus & Voting Algorithms**:
   - **Agreement Index ($A \in [0, 1]$)**: Pairwise confidence alignment score.
   - **Disagreement Entropy ($H(D)$)**: Shannon entropy measuring variance across decision options.
   - **Convergence Delta ($\Delta C$)**: Rate of agreement acceleration between debate rounds.
   - **Borda Count Voting**: Rank-order voting algorithm for Pareto-optimal option selection.
   - **Weighted Scoring**: Multi-agent confidence weighting based on domain expertise.

4. **Zero-Dependency Local & API Backends**:
   - **`HeuristicRuleEngine` (Default)**: Standalone, offline rule-based reasoning engine requiring zero external API keys.
   - **`APIBackend`**: Pluggable connectors for OpenAI GPT-4/3.5, Anthropic Claude, or local Ollama endpoints.

5. **Exportable Audit Trails & Visualizations**:
   - Export full decision traces into **Markdown reports**, **JSON audit logs**, and **matplotlib consensus charts**.

---

## 📐 System Architecture

```mermaid
graph TD
    User([User Prompt / Decision Question]) --> Orchestrator[Council Orchestrator]

    subgraph Agent Council
        A1[Analyst Agent]
        A2[Critic Agent]
        A3[Strategist Agent]
        A4[Ethics Agent]
        A5[Custom Agents...]
    end

    Orchestrator -->|Phase 1: Proposals| Agent Council
    Agent Council -->|Phase 2: Peer Critique| PeerReview[Cross-Critique Matrix]
    PeerReview -->|Phase 3: Refinement| Agent Council
    Agent Council -->|Phase 4: Standpoints & Confidences| Consensus[Consensus Engine]

    subgraph Consensus Metrics & Voting
        Consensus --> M1[Agreement Index A]
        Consensus --> M2[Disagreement Entropy H]
        Consensus --> M3[Borda Count / Delphi]
    end

    Consensus --> Synthesizer[Synthesizer Chair]
    Synthesizer --> ExecutiveResolution[Executive Resolution & Report]
```

---

## 🧮 Mathematical Consensus Formulas

### 1. Agreement Index ($A$)
$$A = \max\left(0, 1 - 2 \cdot \sqrt{\frac{\sum_{i=1}^N w_i (c_i - \bar{c})^2}{\sum_{i=1}^N w_i}}\right)$$
Where $c_i$ is agent confidence, $w_i$ is agent weight, and $\bar{c}$ is the weighted mean confidence.

### 2. Disagreement Entropy ($H(D)$)
$$H(D) = -\sum_{j=1}^M p_j \log_2(p_j)$$
Where $p_j$ is the normalized probability assigned to option $j$.

### 3. Convergence Delta ($\Delta C$)
$$\Delta C_k = A_k - A_{k-1}$$
Measures consensus acceleration between round $k-1$ and round $k$.

---

## 📁 Repository Structure

```
Tiny_Council_Multi_Agent_AI_Decision_System/
├── README.md                           # Comprehensive documentation
├── requirements.txt                    # Project dependencies
├── app.py                              # Main CLI entry point
├── Tiny_Council_Demo.ipynb             # Interactive Jupyter Notebook demo
├── tiny_council/                       # Core python package
│   ├── __init__.py                     # Exports & package version
│   ├── agent.py                        # Role-based agent implementations
│   ├── consensus.py                    # Voting algorithms & math metrics
│   ├── llm_backend.py                  # Heuristic engine & API backend
│   ├── orchestrator.py                 # Multi-phase decision orchestrator
│   ├── cli.py                          # Command Line Interface runner
│   └── utils.py                        # Report exporters & plotting tools
└── tests/
    └── test_tiny_council.py            # Unit test suite
```

---

## 🚀 Quickstart & Installation

### 1. Requirements
Ensure Python 3.8+ is installed.

```bash
pip install -r requirements.txt
```

### 2. Run via Command Line Interface (CLI)

Run out-of-the-box using the built-in offline reasoning engine:

```bash
python app.py --prompt "Should we adopt a microservices architecture for our e-commerce platform?" --rounds 2 --mode delphi
```

Export Markdown, JSON reports, and consensus charts:

```bash
python app.py \
  --prompt "Should we implement automated model retraining on cloud edge nodes?" \
  --rounds 2 \
  --output-md report.md \
  --output-json report.json \
  --output-plot consensus_chart.png
```

---

## 💻 Python API Usage

```python
from tiny_council import (
    CouncilOrchestrator,
    ConsensusMode,
    CustomAgent,
    export_report_markdown,
)

# 1. Initialize Orchestrator
orchestrator = CouncilOrchestrator()

# 2. Add custom domain expert
security_agent = CustomAgent(
    name="CISO Auditor",
    role="Security Specialist",
    persona_description="Audits zero-trust networking, data encryption, and vulnerability vectors.",
    weight=1.3,
)
orchestrator.add_agent(security_agent)

# 3. Execute Council Deliberation
context = orchestrator.run_council(
    topic="Should we deploy LLM agents for customer healthcare triage?",
    rounds=2,
    mode=ConsensusMode.DELPHI_METHOD,
)

# 4. Access Outputs
print("Executive Resolution:")
print(context.executive_resolution)
print("Agreement Index:", context.consensus_summary["final_agreement_index"])

# 5. Export Report
export_report_markdown(context, "healthcare_ai_resolution.md")
```

---

## 🧪 Running Unit Tests

Run the unit test suite to verify agent logic, consensus calculations, orchestrator flow, and CLI execution:

```bash
python tests/test_tiny_council.py
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
