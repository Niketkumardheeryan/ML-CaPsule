import matplotlib.pyplot as plt
import numpy as np
import torch

from data import CLASSES, SHORT_NAMES


def to_display(images):
    return images.mul(0.5).add(0.5).clamp(0, 1).permute(0, 2, 3, 1).numpy()


def plot_class_distribution(counts, save_path=None):
    names = list(counts)
    values = [counts[name] for name in names]
    order = np.argsort(values)[::-1]

    figure, axis = plt.subplots(figsize=(8, 4))
    bars = axis.bar([names[i] for i in order], [values[i] for i in order], color="#4c72b0")
    for index, value in enumerate([values[i] for i in order]):
        axis.text(index, value, str(value), ha="center", va="bottom", fontsize=9)

    axis.set_ylabel("images")
    axis.set_title("HAM10000 subset by lesion type")
    axis.spines[["top", "right"]].set_visible(False)
    bars[-1].set_color("#c44e52")
    bars[-2].set_color("#c44e52")

    figure.tight_layout()
    if save_path:
        figure.savefig(save_path, dpi=120, bbox_inches="tight")
    return figure


def plot_samples(images, labels, title, save_path=None, per_class=6):
    grid = {}
    for image, label in zip(images, labels.tolist()):
        grid.setdefault(label, [])
        if len(grid[label]) < per_class:
            grid[label].append(image)

    order = sorted(grid)
    figure, axes = plt.subplots(len(order), per_class,
                                figsize=(per_class * 1.3, len(order) * 1.45))
    axes = np.atleast_2d(axes)
    shown = to_display(torch.stack([img for label in order for img in grid[label]]))

    position = 0
    for row, label in enumerate(order):
        for column in range(per_class):
            axis = axes[row, column]
            if column < len(grid[label]):
                axis.imshow(shown[position])
                position += 1
            axis.set_xticks([])
            axis.set_yticks([])
            if column == 0:
                axis.set_ylabel(SHORT_NAMES[CLASSES[label]], rotation=0,
                                ha="right", va="center", fontsize=9)

    figure.suptitle(title, fontsize=11)
    figure.tight_layout(rect=(0, 0, 1, 1 - 0.35 / figure.get_figheight()))
    if save_path:
        figure.savefig(save_path, dpi=120, bbox_inches="tight")
    return figure


def plot_gan_losses(history, real_diversity=None, save_path=None):
    """Losses on the left, sample diversity on the right.

    Both panels are needed: the losses can sit in a healthy equilibrium while the generator
    emits one image per class, and only the right-hand panel shows that.
    """
    epochs = [row["epoch"] for row in history]
    measured = [row for row in history if row.get("diversity") is not None]
    has_diversity = bool(measured)
    figure, axes = plt.subplots(1, 2 if has_diversity else 1,
                                figsize=(11 if has_diversity else 8, 4))
    axes = np.atleast_1d(axes)

    axes[0].plot(epochs, [row["d_loss"] for row in history], label="discriminator")
    axes[0].plot(epochs, [row["g_loss"] for row in history], label="generator")
    axes[0].set_xlabel("epoch")
    axes[0].set_ylabel("loss")
    axes[0].set_title("CGAN training losses")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    if has_diversity:
        axes[1].plot([row["epoch"] for row in measured],
                     [row["diversity"] for row in measured],
                     color="#4c72b0", marker="o", markersize=3, label="generated")
        if real_diversity:
            axes[1].axhline(real_diversity, color="#c44e52", linestyle="--",
                            label=f"real images ({real_diversity:.3f})")
        axes[1].set_xlabel("epoch")
        axes[1].set_ylabel("within-class pixel std")
        axes[1].set_title("Sample diversity")
        axes[1].set_ylim(bottom=0)
        axes[1].legend()
        axes[1].grid(alpha=0.3)

    figure.tight_layout()
    if save_path:
        figure.savefig(save_path, dpi=120, bbox_inches="tight")
    return figure


ARM_COLOURS = {"real only": "#8c8c8c", "real + flips": "#dd8452", "real + CGAN": "#4c72b0"}


def plot_recall_comparison(arms, rare, save_path=None):
    """Grouped per-class recall. `arms` maps an arm name to an evaluate() result."""
    names = [SHORT_NAMES[name] for name in CLASSES]
    positions = np.arange(len(names))
    width = 0.8 / len(arms)

    figure, axis = plt.subplots(figsize=(9, 4.5))
    for index, (arm, result) in enumerate(arms.items()):
        offset = (index - (len(arms) - 1) / 2) * width
        axis.bar(positions + offset,
                 [result["per_class"][i]["recall"] for i in range(len(names))],
                 width, label=arm, color=ARM_COLOURS.get(arm))

    axis.set_xticks(positions, names)
    axis.set_ylabel("recall")
    axis.set_ylim(0, 1)
    axis.set_title("Per-class recall on the held-out test set")
    axis.legend()
    axis.grid(axis="y", alpha=0.3)

    for index, name in enumerate(names):
        if name in rare:
            axis.get_xticklabels()[index].set_color("#c44e52")
            axis.get_xticklabels()[index].set_fontweight("bold")

    figure.tight_layout()
    if save_path:
        figure.savefig(save_path, dpi=120, bbox_inches="tight")
    return figure


def plot_confusion_matrices(arms, labels, save_path=None):
    """One row-normalised confusion matrix per arm, on the same colour scale."""
    names = [SHORT_NAMES[name] for name in CLASSES]
    figure, axes = plt.subplots(1, len(arms), figsize=(4.2 * len(arms), 4.4))
    axes = np.atleast_1d(axes)

    for axis, (arm, result) in zip(axes, arms.items()):
        matrix = np.zeros((len(names), len(names)))
        for actual, predicted in zip(labels.tolist(), result["predictions"].tolist()):
            matrix[actual, predicted] += 1
        matrix = matrix / np.clip(matrix.sum(axis=1, keepdims=True), 1, None)

        axis.imshow(matrix, cmap="Blues", vmin=0, vmax=1)
        axis.set_xticks(range(len(names)), names, rotation=45, ha="right", fontsize=8)
        axis.set_yticks(range(len(names)), names, fontsize=8)
        axis.set_title(arm, fontsize=10)
        axis.set_xlabel("predicted", fontsize=9)
        if axis is axes[0]:
            axis.set_ylabel("actual", fontsize=9)

        for row in range(len(names)):
            for column in range(len(names)):
                value = matrix[row, column]
                if value >= 0.01:
                    axis.text(column, row, f"{value:.2f}".lstrip("0"), ha="center",
                              va="center", fontsize=7,
                              color="white" if value > 0.5 else "#333333")

    figure.tight_layout()
    if save_path:
        figure.savefig(save_path, dpi=120, bbox_inches="tight")
    return figure
