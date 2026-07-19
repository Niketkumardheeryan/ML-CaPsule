# 🧠 Prompt Engineering — Advanced Techniques

> **ReAct Prompting · Negative Prompting · Interactive Playground**  
> Built for GSSoC 2026 — ML-CaPsule

---

## Overview

This notebook covers **2 advanced prompt engineering techniques** not commonly found in beginner resources, along with an **interactive playground** to practice all 7 techniques live using the Groq API (free, no credit card required).

Prompt Engineering is the skill of designing effective inputs to get the best possible outputs from AI language models — one of the **most in-demand AI skills in 2026**.

---

## Techniques Covered

| # | Technique | Level | Real World Use Case |
|---|-----------|-------|---------------------|
| 1 | **ReAct Prompting** | Advanced | AI Agents, DevOps, Medical AI, Business Planning |
| 2 | **Negative Prompting** | Intermediate | Content Moderation, EdTech, Corporate AI, Code Review |
| 3 | **Interactive Playground** | All Levels | Practice all 7 techniques live with real API calls |

---

## Notebook Structure

```
Prompt_Engineering_Techniques/
├── Prompt_Engineering_Advanced.ipynb   ← Main notebook
└── README.md                           ← This file
```

---

## ReAct Prompting

**ReAct = Reasoning + Acting**

The model alternates between Thought → Action → Observation loops — the foundation of modern AI agents.

### Real World Examples included:
- **Medical Symptom Analysis** — AI health assistant reasoning
- **Production Incident Investigation** — DevOps root cause analysis
- **Startup Growth Strategy** — Business planning agent
- **ML Model Selection** — AutoML decision making

```
Question
   ↓
Thought 1 → Action 1 → Observation 1
   ↓
Thought 2 → Action 2 → Observation 2
   ↓
Final Answer
```

---

## Negative Prompting

Explicitly telling the model what to **avoid** — giving you precise control over outputs.

### Real World Examples included:
- **News Summarization** — Unbiased, no speculation
- **Kids Educational Content** — No jargon, age-appropriate
- **Corporate Product Description** — No competitor mentions
- **AI Code Review** — Security focus only, no style suggestions

```
Without: "Explain AI"  →  Generic, long, any style
With:    "Explain AI.
          Do NOT use jargon.
          Do NOT exceed 3 sentences."  →  Precise, controlled
```

---

## Interactive Playground

A live widget supporting **all 7 prompt engineering techniques**:

| Feature | Details |
|---------|---------|
| Techniques | Zero-Shot, Few-Shot, Chain-of-Thought, Role-Based, Structured Output, ReAct, Negative |
| Load Examples | One-click example prompts for each technique |
| Live API calls | Real responses from LLaMA3 via Groq |
| Temperature control | Slider from 0.0 (precise) to 1.0 (creative) |
| Role input | Custom system messages for Role-Based technique |
| Negative rules | Line-by-line rule entry for Negative technique |
| Output stats | Word count + character count per response |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.8+** | Core language |
| **Groq API** | Free LLM inference (LLaMA3) |
| **ipywidgets** | Interactive playground UI |
| **Matplotlib** | Technique comparison charts |
| **Pandas** | Summary tables |

---

## Setup

### Step 1 — Install dependencies
```bash
pip install groq matplotlib pandas ipywidgets
```

### Step 2 — Get free Groq API key
1. Go to → [https://console.groq.com](https://console.groq.com)
2. Sign up (free, no credit card)
3. Click **API Keys → Create API Key**
4. Copy your key

### Step 3 — Run the notebook
```bash
jupyter notebook Prompt_Engineering_Advanced.ipynb
```

Enter your API key when prompted (uses `getpass` — never stored or hardcoded).

---

## Visualizations

The notebook includes 3 charts:

1. **Response Length Control** — Shows how negative prompting reduces verbosity
2. **Complete Technique Comparison** — Quality, difficulty, and real-world value for all 7 techniques
3. **When to Use Which Technique** — Visual decision guide

---

## Quick Reference

```
Zero-Shot    → Ask directly. No examples needed.
Few-Shot     → Give 2-3 examples first, then ask.
Chain-of-Thought → Add "think step by step".
Role-Based   → "You are a [expert]..." in system message.
Structured   → "Respond ONLY in JSON format: {...}"
ReAct        → Thought → Action → Observation loop.
Negative     → "Do NOT use jargon. Do NOT exceed 3 lines."
```

### Temperature Guide
| Task | Temperature |
|------|------------|
| Classification, JSON | 0.0 |
| Reasoning, math | 0.0 – 0.2 |
| Technical writing | 0.3 – 0.5 |
| Conversations | 0.5 – 0.7 |
| Creative writing | 0.7 – 1.0 |

---

## Further Reading

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Chain-of-Thought Paper (Wei et al. 2022)](https://arxiv.org/abs/2201.11903)
- [ReAct Paper (Yao et al. 2022)](https://arxiv.org/abs/2210.03629)
- [Groq API Docs](https://console.groq.com/docs)

---

## Author

**Komal Pandey** — GSSoC 2026 Contributor  
ML-CaPsule | [GitHub](https://github.com/Komal-11k)

---

*If you found this helpful, give ML-CaPsule a star!*