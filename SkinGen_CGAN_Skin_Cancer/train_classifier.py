import time

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from models import Classifier, pick_device


def train(images, labels, n_classes, epochs=15, batch_size=128, lr=1e-3,
          device=None, seed=42, verbose=True):
    torch.manual_seed(seed)
    device = device or pick_device()

    model = Classifier(n_classes).to(device)
    optimiser = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    loader = DataLoader(TensorDataset(images, labels), batch_size=batch_size, shuffle=True)

    history = []
    started = time.perf_counter()

    for epoch in range(1, epochs + 1):
        model.train()
        running, correct, seen = 0.0, 0, 0

        for batch, target in loader:
            batch = batch.to(device)
            target = target.to(device)

            optimiser.zero_grad()
            output = model(batch)
            loss = criterion(output, target)
            loss.backward()
            optimiser.step()

            running += loss.item() * len(batch)
            correct += (output.argmax(1) == target).sum().item()
            seen += len(batch)

        history.append({"epoch": epoch, "loss": running / seen, "accuracy": correct / seen})
        if verbose and (epoch % 5 == 0 or epoch == 1):
            print(f"  epoch {epoch:>2}/{epochs}  loss {history[-1]['loss']:.3f}  "
                  f"acc {history[-1]['accuracy']:.3f}  "
                  f"[{time.perf_counter() - started:.0f}s]", flush=True)

    return model, history


@torch.no_grad()
def predict(model, images, device=None, batch_size=256):
    device = device or pick_device()
    model.eval()
    outputs = []

    for start in range(0, len(images), batch_size):
        chunk = images[start:start + batch_size].to(device)
        outputs.append(model(chunk).argmax(1).cpu())

    return torch.cat(outputs)


def repeat(train_images, train_labels, test_images, test_labels, n_classes,
           seeds=(42, 43, 44), device=None, **kwargs):
    """Train the classifier once per seed and average the metrics over the runs.

    The test set is only 629 images, so a single seed moves accuracy by a couple of points on
    its own. Averaging over seeds is what makes a difference between arms worth reading.
    """
    runs, first_model = [], None
    for seed in seeds:
        model, _ = train(train_images, train_labels, n_classes=n_classes, seed=seed,
                         device=device, **kwargs)
        first_model = first_model or model
        runs.append(evaluate(model, test_images, test_labels, n_classes, device=device))

    per_class = {}
    for label in range(n_classes):
        averages = {metric: sum(run["per_class"][label][metric] for run in runs) / len(runs)
                    for metric in ("recall", "precision", "f1")}
        averages["support"] = runs[0]["per_class"][label]["support"]
        per_class[label] = averages

    averaged = {
        "accuracy": sum(run["accuracy"] for run in runs) / len(runs),
        "macro_f1": sum(run["macro_f1"] for run in runs) / len(runs),
        "per_class": per_class,
        "predictions": runs[0]["predictions"],
        "model": first_model,
        "runs": runs,
        "seeds": list(seeds),
    }
    averaged["accuracy_spread"] = (min(run["accuracy"] for run in runs),
                                   max(run["accuracy"] for run in runs))
    return averaged


def evaluate(model, images, labels, n_classes, device=None):
    predictions = predict(model, images, device=device)
    accuracy = (predictions == labels).float().mean().item()

    per_class = {}
    f1_scores = []

    for label in range(n_classes):
        actual = labels == label
        predicted = predictions == label
        true_positive = (actual & predicted).sum().item()
        recall = true_positive / max(1, actual.sum().item())
        precision = true_positive / max(1, predicted.sum().item())
        f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
        per_class[label] = {"recall": recall, "precision": precision, "f1": f1,
                            "support": int(actual.sum().item())}
        f1_scores.append(f1)

    return {
        "accuracy": accuracy,
        "macro_f1": sum(f1_scores) / len(f1_scores),
        "per_class": per_class,
        "predictions": predictions,
    }
