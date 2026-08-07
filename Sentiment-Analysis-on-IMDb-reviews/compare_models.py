"""Compare the sentiment analysers on labelled IMDb reviews.

Downloads a sample of the IMDb test split, runs every analyser in sentiment.py
over the same reviews and reports how often each agrees with the true label.

    python compare_models.py --sample 200
"""

import argparse
import time

from sentiment import ANALYSERS

LABELS = {0: "Negative", 1: "Positive"}
IMDB_DATASET = "stanfordnlp/imdb"


def load_reviews(sample_size, seed=42):
    from datasets import load_dataset

    dataset = load_dataset(IMDB_DATASET, split="test").shuffle(seed=seed)
    rows = dataset.select(range(sample_size))
    return list(rows["text"]), [LABELS[label] for label in rows["label"]]


def evaluate(name, analyse, reviews, truths):
    predictions = []
    started = time.perf_counter()
    for review in reviews:
        predictions.append(analyse(review))
    elapsed = time.perf_counter() - started

    correct = sum(p == t for p, t in zip(predictions, truths))
    neutral = predictions.count("Neutral")
    return {
        "name": name,
        "accuracy": correct / len(truths),
        "neutral": neutral,
        "seconds": elapsed,
        "predictions": predictions,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--examples", type=int, default=3)
    args = parser.parse_args()

    reviews, truths = load_reviews(args.sample, args.seed)
    print(f"{len(reviews)} IMDb test reviews "
          f"({truths.count('Positive')} positive / {truths.count('Negative')} negative)\n")

    results = [evaluate(name, fn, reviews, truths) for name, fn in ANALYSERS.items()]

    print(f"{'model':<26} {'accuracy':>9} {'neutral':>9} {'seconds':>9}")
    print("-" * 56)
    for result in results:
        print(f"{result['name']:<26} {result['accuracy']:>8.1%} "
              f"{result['neutral']:>9} {result['seconds']:>9.1f}")

    baseline = results[-1]
    others = results[:-1]
    print(f"\nReviews {baseline['name']} gets right and the others do not:\n")

    shown = 0
    for index, truth in enumerate(truths):
        if shown >= args.examples:
            break
        if baseline["predictions"][index] != truth:
            continue
        if all(other["predictions"][index] == truth for other in others):
            continue

        snippet = " ".join(reviews[index].split())[:220]
        print(f"  true: {truth}")
        for result in results:
            print(f"    {result['name']:<26} {result['predictions'][index]}")
        print(f"    \"{snippet}...\"\n")
        shown += 1


if __name__ == "__main__":
    main()
