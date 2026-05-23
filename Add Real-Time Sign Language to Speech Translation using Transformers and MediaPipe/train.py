"""
train.py
--------
Transformer-based sign language recognition training pipeline.

Architecture:
  - Positional encoding + multi-head self-attention over landmark sequences
  - CLS token pooling → classification head (alphabet / word level)
  - Mixed-precision training, LR scheduling, early stopping
"""

import os
import json
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, Tuple

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.cuda.amp import GradScaler, autocast

from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

from preprocessing import FEATURE_DIM, load_label_encoder, build_label_encoder, save_label_encoder


# ── Dataset ───────────────────────────────────────────────────────────────────

class SignLandmarkDataset(Dataset):
    """
    Loads pre-extracted landmark CSVs.

    Supports both single-frame (63 features) and sequence data
    (sequence_length × 63 features).
    """

    def __init__(self, csv_path: str, label_to_idx: dict,
                 sequence_length: Optional[int] = None):
        df = pd.read_csv(csv_path)
        feature_cols = [c for c in df.columns if c.startswith("f")]
        self.X = torch.tensor(df[feature_cols].values, dtype=torch.float32)
        self.y = torch.tensor(
            [label_to_idx[l] for l in df["label"]], dtype=torch.long
        )
        self.sequence_length = sequence_length

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        x = self.X[idx]
        # Reshape into (seq_len, feature_dim) if sequence_length provided
        if self.sequence_length:
            x = x.reshape(self.sequence_length, -1)
        return x, self.y[idx]


# ── Model components ──────────────────────────────────────────────────────────

class PositionalEncoding(nn.Module):
    """Standard sinusoidal positional encoding."""

    def __init__(self, d_model: int, max_len: int = 512, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(max_len).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))  # (1, max_len, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, seq_len, d_model)
        x = x + self.pe[:, : x.size(1)]
        return self.dropout(x)


class SignLanguageTransformer(nn.Module):
    """
    Transformer encoder for sign language recognition.

    Input:  (B, seq_len, feature_dim)  — sequence of landmark frames
            OR (B, feature_dim)        — single frame (auto-unsqueezed)
    Output: (B, num_classes)           — class logits
    """

    def __init__(
        self,
        feature_dim: int = FEATURE_DIM,
        num_classes: int = 29,
        d_model: int = 128,
        nhead: int = 8,
        num_layers: int = 4,
        dim_feedforward: int = 512,
        dropout: float = 0.1,
        max_seq_len: int = 64,
    ):
        super().__init__()

        # Input projection
        self.input_proj = nn.Linear(feature_dim, d_model)

        # CLS token (learnable)
        self.cls_token = nn.Parameter(torch.randn(1, 1, d_model))

        # Positional encoding
        self.pos_enc = PositionalEncoding(d_model, max_len=max_seq_len + 1, dropout=dropout)

        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
            norm_first=True,          # Pre-LN for stability
        )
        self.transformer = nn.TransformerEncoder(
            encoder_layer, num_layers=num_layers,
            norm=nn.LayerNorm(d_model)
        )

        # Classification head
        self.classifier = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_model // 2, num_classes),
        )

        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(1)                          # (B, 1, F)

        B = x.size(0)
        x = self.input_proj(x)                          # (B, T, d_model)

        cls = self.cls_token.expand(B, -1, -1)          # (B, 1, d_model)
        x   = torch.cat([cls, x], dim=1)                # (B, T+1, d_model)
        x   = self.pos_enc(x)

        x   = self.transformer(x)                       # (B, T+1, d_model)
        cls_out = x[:, 0]                               # CLS representation
        return self.classifier(cls_out)


# ── Training utilities ────────────────────────────────────────────────────────

class EarlyStopping:
    def __init__(self, patience: int = 10, min_delta: float = 1e-4):
        self.patience  = patience
        self.min_delta = min_delta
        self.counter   = 0
        self.best_loss = float("inf")

    def __call__(self, val_loss: float) -> bool:
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter   = 0
        else:
            self.counter += 1
        return self.counter >= self.patience


def train_one_epoch(
    model, loader, optimizer, criterion, scaler, device
) -> Tuple[float, float]:
    model.train()
    total_loss, correct, total = 0.0, 0, 0

    for x, y in loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()

        with autocast():
            logits = model(x)
            loss   = criterion(logits, y)

        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()

        total_loss += loss.item() * x.size(0)
        correct    += (logits.argmax(1) == y).sum().item()
        total      += x.size(0)

    return total_loss / total, correct / total


@torch.no_grad()
def evaluate(model, loader, criterion, device) -> Tuple[float, float]:
    model.eval()
    total_loss, correct, total = 0.0, 0, 0

    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss   = criterion(logits, y)

        total_loss += loss.item() * x.size(0)
        correct    += (logits.argmax(1) == y).sum().item()
        total      += x.size(0)

    return total_loss / total, correct / total


def save_checkpoint(model, optimizer, epoch: int, val_loss: float, path: str):
    torch.save({
        "epoch":           epoch,
        "model_state":     model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
        "val_loss":        val_loss,
    }, path)


def plot_history(history: dict, output_dir: str):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, key in zip(axes, ["loss", "acc"]):
        ax.plot(history[f"train_{key}"], label="train")
        ax.plot(history[f"val_{key}"],   label="val")
        ax.set_title(key.capitalize())
        ax.legend()
        ax.set_xlabel("Epoch")
    plt.tight_layout()
    path = os.path.join(output_dir, "training_history.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Training plot saved → {path}")


# ── Main training loop ────────────────────────────────────────────────────────

def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # ── Label encoding ──
    df = pd.read_csv(args.data)
    l2i, i2l = build_label_encoder(df["label"].tolist())
    save_label_encoder(l2i, os.path.join(args.model_dir, "label_encoder.json"))
    num_classes = len(l2i)
    print(f"Classes ({num_classes}): {list(l2i.keys())}")

    # ── Dataset splits ──
    full_ds = SignLandmarkDataset(args.data, l2i, sequence_length=args.seq_len)
    n_val   = int(len(full_ds) * args.val_split)
    n_train = len(full_ds) - n_val
    train_ds, val_ds = random_split(full_ds, [n_train, n_val])

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True,
                              num_workers=2, pin_memory=True)
    val_loader   = DataLoader(val_ds,   batch_size=args.batch_size, shuffle=False,
                              num_workers=2, pin_memory=True)

    # ── Model ──
    model = SignLanguageTransformer(
        feature_dim=FEATURE_DIM,
        num_classes=num_classes,
        d_model=args.d_model,
        nhead=args.nhead,
        num_layers=args.num_layers,
        dim_feedforward=args.d_model * 4,
        dropout=args.dropout,
    ).to(device)
    print(f"Parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")

    # ── Optimiser & schedule ──
    optimizer = AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-6)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    scaler    = GradScaler()
    stopper   = EarlyStopping(patience=args.patience)

    history    = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
    best_val   = float("inf")
    model_path = os.path.join(args.model_dir, "best_model.pt")

    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_one_epoch(model, train_loader, optimizer,
                                          criterion, scaler, device)
        va_loss, va_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step()

        history["train_loss"].append(tr_loss)
        history["val_loss"].append(va_loss)
        history["train_acc"].append(tr_acc)
        history["val_acc"].append(va_acc)

        print(f"Epoch {epoch:03d} | "
              f"train loss {tr_loss:.4f} acc {tr_acc:.4f} | "
              f"val loss {va_loss:.4f} acc {va_acc:.4f}")

        if va_loss < best_val:
            best_val = va_loss
            save_checkpoint(model, optimizer, epoch, va_loss, model_path)
            print(f"  ✓ New best — checkpoint saved")

        if stopper(va_loss):
            print(f"Early stopping at epoch {epoch}")
            break

    plot_history(history, args.model_dir)
    with open(os.path.join(args.model_dir, "history.json"), "w") as f:
        json.dump(history, f)
    print("Training complete.")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train sign language Transformer")
    parser.add_argument("--data",       default="dataset/features.csv")
    parser.add_argument("--model_dir",  default="models/")
    parser.add_argument("--epochs",     type=int,   default=100)
    parser.add_argument("--batch_size", type=int,   default=64)
    parser.add_argument("--lr",         type=float, default=1e-3)
    parser.add_argument("--d_model",    type=int,   default=128)
    parser.add_argument("--nhead",      type=int,   default=8)
    parser.add_argument("--num_layers", type=int,   default=4)
    parser.add_argument("--dropout",    type=float, default=0.1)
    parser.add_argument("--seq_len",    type=int,   default=None,
                        help="Sequence length for temporal modelling (None = single-frame)")
    parser.add_argument("--val_split",  type=float, default=0.2)
    parser.add_argument("--patience",   type=int,   default=10)
    args = parser.parse_args()

    os.makedirs(args.model_dir, exist_ok=True)
    train(args)
