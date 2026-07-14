"""
neutralizer_model.py
A lightweight sequence model that learns to map accented MFCC features
toward native-accent MFCC features (accent neutralization).
"""

import torch
import torch.nn as nn


class AccentNeutralizer(nn.Module):
    def __init__(self, n_mfcc=13, hidden_dim=128, num_layers=2):
        super().__init__()
        self.n_mfcc = n_mfcc

        self.encoder = nn.LSTM(
            input_size=n_mfcc,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.2 if num_layers > 1 else 0.0
        )

        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, n_mfcc)
        )

    def forward(self, x):
        encoded, _ = self.encoder(x)
        output = self.decoder(encoded)
        return x + output


if __name__ == "__main__":
    model = AccentNeutralizer()
    dummy_input = torch.randn(4, 100, 13)
    output = model(dummy_input)
    print("Input shape:", dummy_input.shape)
    print("Output shape:", output.shape)
    num_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {num_params:,}")
