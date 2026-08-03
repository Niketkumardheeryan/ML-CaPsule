"""
Core Attention Mechanisms

Implementation of various attention mechanisms from scratch.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Optional, Tuple


class ScaledDotProductAttention(nn.Module):
    """
    Scaled Dot-Product Attention
    
    Formula:
        Attention(Q, K, V) = softmax(QK^T / √d_k)V
    
    Args:
        d_k: Dimension of keys (for scaling)
        dropout: Dropout probability
    """
    
    def __init__(self, d_k: int, dropout: float = 0.1):
        super().__init__()
        self.d_k = d_k
        self.dropout = nn.Dropout(dropout)
    
    def forward(
        self,
        query: torch.Tensor,      # (batch, seq_len, d_k)
        key: torch.Tensor,        # (batch, seq_len, d_k)
        value: torch.Tensor,      # (batch, seq_len, d_v)
        mask: Optional[torch.Tensor] = None  # (batch, 1, seq_len, seq_len)
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Apply scaled dot-product attention.
        
        Args:
            query: Query matrix (batch, seq_len, d_k)
            key: Key matrix (batch, seq_len, d_k)
            value: Value matrix (batch, seq_len, d_v)
            mask: Optional mask for positions to ignore
        
        Returns:
            output: Attention output (batch, seq_len, d_v)
            weights: Attention weights (batch, seq_len, seq_len)
        """
        # Step 1: Compute scores = QK^T
        scores = torch.matmul(query, key.transpose(-2, -1))  # (batch, seq_len, seq_len)
        
        # Step 2: Scale by √d_k
        scores = scores / np.sqrt(self.d_k)
        
        # Step 3: Apply mask if provided (set masked positions to -inf)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        # Step 4: Apply softmax to get weights
        weights = F.softmax(scores, dim=-1)
        weights = self.dropout(weights)
        
        # Step 5: Apply weights to values
        output = torch.matmul(weights, value)  # (batch, seq_len, d_v)
        
        return output, weights


class MultiHeadAttention(nn.Module):
    """
    Multi-Head Attention
    
    Multiple attention heads computed in parallel, then concatenated.
    
    Formula:
        MultiHead(Q,K,V) = Concat(head_1, ..., head_h)W^O
        where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
    
    Args:
        d_model: Model dimension
        num_heads: Number of attention heads
        dropout: Dropout probability
    """
    
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Linear projections for Q, K, V
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        
        # Output projection
        self.W_o = nn.Linear(d_model, d_model)
        
        # Scaled dot-product attention
        self.attention = ScaledDotProductAttention(self.d_k, dropout)
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Apply multi-head attention.
        
        Args:
            query: (batch, seq_len, d_model)
            key: (batch, seq_len, d_model)
            value: (batch, seq_len, d_model)
            mask: Optional mask
        
        Returns:
            output: (batch, seq_len, d_model)
            weights: (batch, num_heads, seq_len, seq_len)
        """
        batch_size = query.size(0)
        
        # Step 1: Apply linear projections
        Q = self.W_q(query)  # (batch, seq_len, d_model)
        K = self.W_k(key)
        V = self.W_v(value)
        
        # Step 2: Reshape for multi-head attention
        # (batch, seq_len, d_model) → (batch, seq_len, num_heads, d_k)
        Q = Q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        # (batch, num_heads, seq_len, d_k)
        K = K.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # Step 3: Apply attention for each head
        attn_output, attn_weights = self.attention(Q, K, V, mask)
        # attn_output: (batch, num_heads, seq_len, d_k)
        # attn_weights: (batch, num_heads, seq_len, seq_len)
        
        # Step 4: Concatenate heads
        attn_output = attn_output.transpose(1, 2).contiguous()
        # (batch, seq_len, num_heads, d_k)
        attn_output = attn_output.view(batch_size, -1, self.d_model)
        # (batch, seq_len, d_model)
        
        # Step 5: Apply output projection
        output = self.W_o(attn_output)
        
        return output, attn_weights


class AdditiveAttention(nn.Module):
    """
    Additive Attention (Bahdanau Attention)
    
    More computationally efficient than dot-product for some cases.
    
    Formula:
        score(s, h) = v^T tanh(W[s, h])
        where s = current state, h = encoder hidden state
    
    Args:
        hidden_dim: Dimension of hidden states
        dropout: Dropout probability
    """
    
    def __init__(self, hidden_dim: int, dropout: float = 0.1):
        super().__init__()
        
        self.hidden_dim = hidden_dim
        
        # Scoring function: tanh(W[q, k])
        self.W = nn.Linear(2 * hidden_dim, hidden_dim)
        self.v = nn.Parameter(torch.randn(hidden_dim))
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(
        self,
        query: torch.Tensor,       # (batch, hidden_dim)
        keys: torch.Tensor,        # (batch, seq_len, hidden_dim)
        values: torch.Tensor,      # (batch, seq_len, hidden_dim)
        mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Apply additive attention.
        
        Args:
            query: (batch, hidden_dim)
            keys: (batch, seq_len, hidden_dim)
            values: (batch, seq_len, hidden_dim)
            mask: Optional mask
        
        Returns:
            output: (batch, hidden_dim)
            weights: (batch, seq_len)
        """
        seq_len = keys.size(1)
        
        # Expand query to match sequence length
        query_expanded = query.unsqueeze(1).expand(-1, seq_len, -1)
        # (batch, seq_len, hidden_dim)
        
        # Concatenate query and keys
        combined = torch.cat([query_expanded, keys], dim=2)
        # (batch, seq_len, 2 * hidden_dim)
        
        # Compute scores
        scores = torch.tanh(self.W(combined))  # (batch, seq_len, hidden_dim)
        scores = torch.matmul(scores, self.v)  # (batch, seq_len)
        
        # Apply mask if provided
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        # Apply softmax
        weights = F.softmax(scores, dim=1)  # (batch, seq_len)
        weights = self.dropout(weights)
        
        # Apply weights to values
        weights_expanded = weights.unsqueeze(1)  # (batch, 1, seq_len)
        output = torch.matmul(weights_expanded, values).squeeze(1)
        # (batch, hidden_dim)
        
        return output, weights


class MultiQueryAttention(nn.Module):
    """
    Multi-Query Attention
    
    Like multi-head attention, but with shared keys and values
    across heads for efficiency.
    
    Args:
        d_model: Model dimension
        num_heads: Number of query heads
        dropout: Dropout probability
    """
    
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Per-head query projections
        self.W_q = nn.Linear(d_model, d_model)
        
        # Shared key/value projections
        self.W_k = nn.Linear(d_model, self.d_k)
        self.W_v = nn.Linear(d_model, self.d_k)
        
        # Output projection
        self.W_o = nn.Linear(d_model, d_model)
        
        self.attention = ScaledDotProductAttention(self.d_k, dropout)
    
    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Apply multi-query attention."""
        batch_size = query.size(0)
        
        # Project queries to (batch, seq_len, num_heads, d_k)
        Q = self.W_q(query)
        Q = Q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # Project keys and values (shared)
        K = self.W_k(key)  # (batch, seq_len, d_k)
        K = K.unsqueeze(1)  # (batch, 1, seq_len, d_k)
        
        V = self.W_v(value)
        V = V.unsqueeze(1)  # (batch, 1, seq_len, d_k)
        
        # Apply attention
        attn_output, attn_weights = self.attention(Q, K, V, mask)
        
        # Concatenate and project
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.view(batch_size, -1, self.d_model)
        output = self.W_o(attn_output)
        
        return output, attn_weights


def create_causal_mask(seq_len: int, device: torch.device) -> torch.Tensor:
    """
    Create a causal mask to prevent attending to future positions.
    
    Args:
        seq_len: Sequence length
        device: Device to create tensor on
    
    Returns:
        Causal mask (1, 1, seq_len, seq_len)
    """
    mask = torch.tril(torch.ones(seq_len, seq_len, device=device))
    return mask.unsqueeze(0).unsqueeze(0)


def create_padding_mask(
    lengths: torch.Tensor,
    max_len: int,
    device: torch.device
) -> torch.Tensor:
    """
    Create a mask for padding positions.
    
    Args:
        lengths: Actual lengths of sequences (batch,)
        max_len: Maximum length
        device: Device to create tensor on
    
    Returns:
        Padding mask (batch, 1, 1, max_len)
    """
    batch_size = lengths.size(0)
    mask = torch.arange(max_len, device=device).unsqueeze(0) < lengths.unsqueeze(1)
    return mask.unsqueeze(1).unsqueeze(1)
