# Transformer-Based Headline Generator

## Overview

This project implements an AI-powered headline generation system using transformer-based NLP models from HuggingFace.

The application accepts long-form article text and generates concise headline-style summaries using a pretrained BART sequence-to-sequence transformer model.

The project is designed with a modular backend architecture and exposes a REST API using Flask for easy integration into content management systems, publishing workflows, and NLP pipelines.

---

## Features

- Transformer-based headline generation
- HuggingFace model integration
- REST API using Flask
- Modular inference pipeline
- JSON request/response support
- Input validation and error handling
- Lightweight local deployment setup

---

## Tech Stack

- Python
- Flask
- HuggingFace Transformers
- PyTorch
- BART Large CNN

---

## Project Structure

``` id="q5jlwm"
Headline_Generator_Transformer/
│
├── app.py
├── inference.py
├── requirements.txt
├── README.md
├── sample_input.txt
└── .gitignore


## Installataion

```bash
pip install -r requirements.txt