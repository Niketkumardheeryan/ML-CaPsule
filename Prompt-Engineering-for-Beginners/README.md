# Prompt Engineering for Beginners

A beginner-friendly, hands-on Jupyter notebook covering the 5 most essential Prompt Engineering techniques — with real working code, free APIs, and zero math prerequisites.

---

## What is Prompt Engineering?

Prompt Engineering is the skill of crafting inputs to AI language models (LLMs) that produce accurate, consistent, and useful outputs. It's one of the most in-demand AI skills in 2025–2026 and requires no model training — just learning how to communicate with AI effectively.

---

## Techniques Covered

| # | Technique | What You'll Learn |
|---|-----------|-------------------|
| 1 | **Zero-Shot Prompting** | Ask the model directly without examples; use constraints to improve output quality |
| 2 | **Few-Shot Prompting** | Provide example input-output pairs to teach the model a custom format or schema |
| 3 | **Chain-of-Thought Prompting** | Force the model to reason step by step — dramatically improves accuracy on logic and math |
| 4 | **Role-Based Prompting** | Assign a persona using the system message to control tone, expertise, and style |
| 5 | **Structured Output Prompting** | Get JSON, Markdown tables, or other machine-readable formats — essential for production AI |

---

## API Used

**Groq API (Free Tier)**
- No credit card required
- Access to Llama 3.1 8B — fast and capable
- Sign up at [https://console.groq.com](https://console.groq.com)

---

## Prerequisites

- Basic Python knowledge (variables, functions, strings)
- A free Groq account (takes 2 minutes to set up)
- No ML background required

---

## Setup

```bash
pip install groq
```

Then open the notebook and follow the setup cell to enter your API key securely.

---

## What's Inside

The notebook is structured so each technique:
1. Explains the concept clearly in plain English
2. Shows a bad prompt vs a good prompt (where applicable)
3. Provides 2–3 working code examples with increasing complexity
4. Ends with a summary table and key takeaway
5. Includes an experiment cell for you to try your own prompts

A final section combines all 5 techniques into a single real-world example (AI-powered resume screener).

---

## Sample Output

**Few-Shot Extraction:**
```
Input: "Satya Nadella, Microsoft's CEO, unveiled the company's latest AI roadmap."
Output: Satya Nadella | CEO | Microsoft
```

**Structured JSON Extraction from a job posting:**
```json
{
  "job_title": "Machine Learning Engineer",
  "company": "TechCorp",
  "location": "Bangalore",
  "experience_required_years": 3,
  "required_skills": ["PyTorch", "TensorFlow"],
  "salary_range_lpa": {"min": 18, "max": 25}
}
```

---

## Notebook Structure

```
Prompt_Engineering_for_Beginners.ipynb
├── Setup (install groq, initialize client, helper functions)
├── Technique 1: Zero-Shot Prompting
│   ├── Bad vs Good prompt comparison
│   ├── Sentiment classification example
│   └── Experiment cell
├── Technique 2: Few-Shot Prompting
│   ├── Custom label classification
│   ├── Entity extraction
│   ├── Style transfer
│   └── Zero-shot vs few-shot comparison
├── Technique 3: Chain-of-Thought Prompting
│   ├── Zero-shot CoT (math problem)
│   ├── Few-shot CoT with structured reasoning
│   ├── Logic puzzle
│   └── Code debugging with CoT
├── Technique 4: Role-Based Prompting
│   ├── Same question, 3 different expert roles
│   └── Building a customer support bot persona
├── Technique 5: Structured Output Prompting
│   ├── JSON extraction from job posting
│   ├── Markdown table generation
│   └── JSON array generation (flashcards)
├── Combined Example: All 5 techniques — AI resume screener
└── Cheat Sheet & Next Steps
```

---

## Contributing

This notebook was contributed as part of **GSSoC 2026** to ML-CaPsule.

If you find an issue or want to add more techniques, feel free to open an issue or submit a PR.

---

## License

This project is licensed under the MIT License — see the [LICENSE](../../LICENSE) file for details.
