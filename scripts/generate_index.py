#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {'.git', '.github', 'docs', 'website', 'assets', '__pycache__', '.vscode'}

TECH_KEYWORDS = {
    'TensorFlow': ['tensorflow', 'keras'],
    'PyTorch': ['pytorch', 'torch'],
    'scikit-learn': ['scikit-learn', 'sklearn'],
    'OpenCV': ['opencv'],
    'Transformers': ['transformers', 'huggingface'],
    'XGBoost': ['xgboost'],
    'LightGBM': ['lightgbm'],
    'Pandas': ['pandas'],
    'NumPy': ['numpy'],
    'NLP': ['nlp', 'natural language', 'tokenize', 'spacy'],
    'Audio': ['audio', 'wav', 'mfcc'],
}

CATEGORY_KEYWORDS = {
    'Computer Vision': ['vision', 'image', 'opencv', 'mask', 'segmentation', 'yolo', 'cnn'],
    'NLP': ['nlp', 'language', 'text', 'token', 'transformer'],
    'Time Series': ['time series', 'forecast', 'forecasting'],
    'Reinforcement Learning': ['reinforce', 'reinforcement', 'agent'],
    'Audio': ['audio', 'speech', 'wav', 'mfcc'],
}

DIFFICULTY_KEYWORDS = {
    'Beginner': ['beginner', 'easy', 'basic'],
    'Intermediate': ['intermediate', 'medium'],
    'Advanced': ['advanced', 'hard', 'difficult'],
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8', errors='ignore').lower()
    except Exception:
        return ''


def detect_tags(text: str, mapping: dict):
    found = set()
    for tag, keys in mapping.items():
        for k in keys:
            if k in text:
                found.add(tag)
                break
    return sorted(found)


def detect_difficulty(text: str):
    for level, keys in DIFFICULTY_KEYWORDS.items():
        for k in keys:
            if k in text:
                return level
    return 'Unknown'


def build_index():
    projects = []
    for entry in sorted(os.listdir(ROOT)):
        if entry in EXCLUDE:
            continue
        path = ROOT / entry
        if not path.is_dir():
            continue

        # Try to find README / requirements
        readme = None
        for candidate in ('README.md', 'Readme.md', 'readme.md'):
            cand = path / candidate
            if cand.exists():
                readme = cand
                break

        req_exists = any((path / name).exists() for name in ('requirements.txt', 'environment.yml', 'requirements_dev.txt'))

        readme_text = read_text(readme) if readme else ''
        folder_name = entry
        display_name = folder_name.replace('_', ' ').replace('-', ' ').strip()

        tech = detect_tags(' '.join([readme_text, folder_name.lower()]), TECH_KEYWORDS)
        categories = detect_tags(' '.join([readme_text, folder_name.lower()]), CATEGORY_KEYWORDS)
        category = categories[0] if categories else 'Other'
        difficulty = detect_difficulty(readme_text)

        projects.append({
            'name': display_name,
            'folder': folder_name,
            'category': category,
            'difficulty': difficulty,
            'tech': tech,
            'hasRequirements': req_exists,
            'hasReadme': bool(readme),
        })

    # write to docs/projects.json and projects.json at repo root
    out_docs = ROOT / 'docs' / 'projects.json'
    out_root = ROOT / 'projects.json'
    out_docs.parent.mkdir(parents=True, exist_ok=True)
    with out_docs.open('w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
    with out_root.open('w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

    print(f'Wrote {len(projects)} projects to {out_docs} and {out_root}')


if __name__ == '__main__':
    build_index()
