"""
Visualization Utilities

Helper functions for visualizing attention mechanisms and transformer behavior.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import seaborn as sns
from typing import List, Optional, Tuple
import torch


def plot_attention_heatmap(
    attention_weights: np.ndarray,
    tokens: List[str],
    title: str = "Attention Weights",
    figsize: Tuple[int, int] = (10, 8),
    cmap: str = "YlOrRd",
    save_path: Optional[str] = None
) -> None:
    """
    Plot attention weights as a heatmap.
    
    Args:
        attention_weights: (seq_len, seq_len) array
        tokens: List of token strings
        title: Plot title
        figsize: Figure size
        cmap: Colormap
        save_path: Path to save figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot heatmap
    im = ax.imshow(attention_weights, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    
    # Set labels
    ax.set_xticks(range(len(tokens)))
    ax.set_yticks(range(len(tokens)))
    ax.set_xticklabels(tokens, rotation=45, ha='right')
    ax.set_yticklabels(tokens)
    
    ax.set_xlabel('Keys (What we look at)', fontsize=12)
    ax.set_ylabel('Queries (Who is looking)', fontsize=12)
    ax.set_title(title, fontsize=14, weight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Attention Weight', fontsize=11)
    
    # Add text annotations
    for i in range(len(tokens)):
        for j in range(len(tokens)):
            text = ax.text(j, i, f'{attention_weights[i, j]:.2f}',
                          ha="center", va="center", 
                          color="white" if attention_weights[i, j] > 0.5 else "black",
                          fontsize=9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()


def plot_multi_head_attention(
    attention_weights: List[np.ndarray],
    tokens: List[str],
    num_heads: int = 4,
    figsize: Tuple[int, int] = (14, 10),
    save_path: Optional[str] = None
) -> None:
    """
    Plot multiple attention heads.
    
    Args:
        attention_weights: List of (seq_len, seq_len) arrays
        tokens: List of tokens
        num_heads: Number of heads to plot
        figsize: Figure size
        save_path: Path to save figure
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    axes = axes.flatten()
    
    for head_idx in range(min(num_heads, 4)):
        ax = axes[head_idx]
        
        weights = attention_weights[head_idx]
        
        im = ax.imshow(weights, cmap='viridis', aspect='auto', vmin=0, vmax=1)
        
        ax.set_xticks(range(len(tokens)))
        ax.set_yticks(range(len(tokens)))
        ax.set_xticklabels(tokens, rotation=45, ha='right')
        ax.set_yticklabels(tokens)
        
        ax.set_title(f'Head {head_idx + 1}', fontsize=12, weight='bold')
        
        plt.colorbar(im, ax=ax)
    
    plt.suptitle('Multi-Head Attention Weights', fontsize=14, weight='bold', y=1.00)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()


def plot_attention_flow(
    source_tokens: List[str],
    target_tokens: List[str],
    attention_matrix: np.ndarray,
    title: str = "Attention Flow",
    figsize: Tuple[int, int] = (12, 8),
    save_path: Optional[str] = None
) -> None:
    """
    Plot attention flow diagram (e.g., for translation).
    
    Args:
        source_tokens: Source language tokens
        target_tokens: Target language tokens
        attention_matrix: (len(target), len(source)) array
        title: Plot title
        figsize: Figure size
        save_path: Path to save figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot heatmap
    im = ax.imshow(attention_matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)
    
    # Set labels
    ax.set_xticks(range(len(source_tokens)))
    ax.set_yticks(range(len(target_tokens)))
    ax.set_xticklabels(source_tokens, fontsize=12)
    ax.set_yticklabels(target_tokens, fontsize=12)
    
    ax.set_xlabel('Source Tokens', fontsize=12, weight='bold')
    ax.set_ylabel('Target Tokens', fontsize=12, weight='bold')
    ax.set_title(title, fontsize=14, weight='bold')
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Attention Weight', fontsize=11)
    
    # Annotations
    for i in range(len(target_tokens)):
        for j in range(len(source_tokens)):
            text = ax.text(j, i, f'{attention_matrix[i, j]:.2f}',
                          ha="center", va="center",
                          color="white" if attention_matrix[i, j] > 0.5 else "black",
                          fontsize=10, weight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()


def plot_token_importance(
    tokens: List[str],
    importance_scores: np.ndarray,
    title: str = "Token Importance",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> None:
    """
    Plot token importance as a bar chart.
    
    Args:
        tokens: List of tokens
        importance_scores: Importance score for each token
        title: Plot title
        figsize: Figure size
        save_path: Path to save figure
    """
    # Sort by importance
    sorted_idx = np.argsort(importance_scores)[::-1]
    sorted_tokens = [tokens[i] for i in sorted_idx]
    sorted_scores = importance_scores[sorted_idx]
    
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = plt.cm.RdYlGn(sorted_scores / sorted_scores.max())
    bars = ax.barh(sorted_tokens, sorted_scores, color=colors)
    
    ax.set_xlabel('Importance Score', fontsize=12, weight='bold')
    ax.set_title(title, fontsize=14, weight='bold')
    ax.set_xlim(0, max(sorted_scores) * 1.1)
    
    # Add value labels
    for i, (token, score) in enumerate(zip(sorted_tokens, sorted_scores)):
        ax.text(score, i, f' {score:.3f}', va='center', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()


def plot_embeddings_2d(
    embeddings: np.ndarray,
    labels: Optional[np.ndarray] = None,
    method: str = 'pca',
    title: str = "Embedding Space",
    figsize: Tuple[int, int] = (10, 8),
    save_path: Optional[str] = None
) -> None:
    """
    Plot embeddings in 2D space.
    
    Args:
        embeddings: (num_samples, embedding_dim) array
        labels: Optional labels for coloring
        method: 'pca', 'tsne', or 'umap'
        title: Plot title
        figsize: Figure size
        save_path: Path to save figure
    """
    # Reduce to 2D
    if method == 'pca':
        from sklearn.decomposition import PCA
        reducer = PCA(n_components=2)
        embeddings_2d = reducer.fit_transform(embeddings)
    elif method == 'tsne':
        from sklearn.manifold import TSNE
        reducer = TSNE(n_components=2, random_state=42)
        embeddings_2d = reducer.fit_transform(embeddings)
    elif method == 'umap':
        try:
            import umap
            reducer = umap.UMAP(n_components=2, random_state=42)
            embeddings_2d = reducer.fit_transform(embeddings)
        except ImportError:
            print("UMAP not installed, using PCA instead")
            from sklearn.decomposition import PCA
            reducer = PCA(n_components=2)
            embeddings_2d = reducer.fit_transform(embeddings)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    fig, ax = plt.subplots(figsize=figsize)
    
    if labels is not None:
        scatter = ax.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1],
                            c=labels, cmap='tab10', s=50, alpha=0.6)
        plt.colorbar(scatter, ax=ax, label='Label')
    else:
        scatter = ax.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1],
                            c=np.arange(len(embeddings)), cmap='viridis',
                            s=50, alpha=0.6)
        plt.colorbar(scatter, ax=ax, label='Sample Index')
    
    ax.set_xlabel(f'{method.upper()} Component 1', fontsize=12, weight='bold')
    ax.set_ylabel(f'{method.upper()} Component 2', fontsize=12, weight='bold')
    ax.set_title(title, fontsize=14, weight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()


def plot_transformer_architecture() -> None:
    """Plot simplified transformer architecture diagram."""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Hide axes
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'TRANSFORMER ARCHITECTURE', fontsize=16, weight='bold',
            ha='center', va='top')
    
    # Input
    rect = patches.FancyBboxPatch((3.5, 8.5), 3, 0.6, 
                                  boxstyle="round,pad=0.1", 
                                  edgecolor='black', facecolor='lightblue')
    ax.add_patch(rect)
    ax.text(5, 8.8, 'Input: Token + Position Embeddings', ha='center', va='center')
    
    # Encoder
    rect = patches.FancyBboxPatch((0.5, 6), 3.5, 1.5,
                                  boxstyle="round,pad=0.1",
                                  edgecolor='blue', facecolor='lightblue', linewidth=2)
    ax.add_patch(rect)
    ax.text(2.25, 7.2, 'ENCODER', fontsize=12, weight='bold', ha='center')
    ax.text(2.25, 6.8, 'N Layers:', fontsize=10, ha='center')
    ax.text(2.25, 6.4, '• Self-Attention', fontsize=9, ha='center')
    ax.text(2.25, 6.1, '• Feed-Forward', fontsize=9, ha='center')
    
    # Decoder
    rect = patches.FancyBboxPatch((6, 6), 3.5, 1.5,
                                  boxstyle="round,pad=0.1",
                                  edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(rect)
    ax.text(7.75, 7.2, 'DECODER', fontsize=12, weight='bold', ha='center')
    ax.text(7.75, 6.8, 'N Layers:', fontsize=10, ha='center')
    ax.text(7.75, 6.4, '• Masked Self-Attn', fontsize=9, ha='center')
    ax.text(7.75, 6.1, '• Cross-Attention', fontsize=9, ha='center')
    
    # Arrows
    arrow = FancyArrowPatch((5, 8.5), (2.25, 7.5),
                          arrowstyle='->', mutation_scale=20, lw=2)
    ax.add_patch(arrow)
    
    arrow = FancyArrowPatch((5, 8.5), (7.75, 7.5),
                          arrowstyle='->', mutation_scale=20, lw=2)
    ax.add_patch(arrow)
    
    # Output
    rect = patches.FancyBboxPatch((3.5, 4.5), 3, 0.6,
                                  boxstyle="round,pad=0.1",
                                  edgecolor='black', facecolor='lightyellow')
    ax.add_patch(rect)
    ax.text(5, 4.8, 'Output: Probability Distribution', ha='center', va='center')
    
    arrow = FancyArrowPatch((2.25, 6), (5, 5.1),
                          arrowstyle='->', mutation_scale=20, lw=2, linestyle='dashed')
    ax.add_patch(arrow)
    
    arrow = FancyArrowPatch((7.75, 6), (5, 5.1),
                          arrowstyle='->', mutation_scale=20, lw=2)
    ax.add_patch(arrow)
    
    # Key concepts
    ax.text(5, 3.5, 'Key Components:', fontsize=12, weight='bold', ha='center')
    ax.text(5, 3, '✓ Self-Attention: Each position attends to all positions',
           fontsize=10, ha='center', style='italic')
    ax.text(5, 2.5, '✓ Cross-Attention: Decoder attends to encoder',
           fontsize=10, ha='center', style='italic')
    ax.text(5, 2, '✓ Feed-Forward: Fully connected layers',
           fontsize=10, ha='center', style='italic')
    ax.text(5, 1.5, '✓ Positional Encoding: Add sequence order information',
           fontsize=10, ha='center', style='italic')
    
    plt.tight_layout()
    plt.show()


def plot_attention_scores_distribution(
    scores: np.ndarray,
    title: str = "Attention Scores Distribution",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> None:
    """
    Plot distribution of attention scores.
    
    Args:
        scores: Attention scores array
        title: Plot title
        figsize: Figure size
        save_path: Path to save figure
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Histogram
    axes[0].hist(scores.flatten(), bins=50, alpha=0.7, color='steelblue', edgecolor='black')
    axes[0].set_xlabel('Attention Weight', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].set_title('Distribution of Attention Weights', fontsize=12, weight='bold')
    axes[0].axvline(scores.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {scores.mean():.3f}')
    axes[0].legend()
    
    # Box plot by position
    axes[1].boxplot([scores[i, :] for i in range(min(scores.shape[0], 10))],
                    labels=[f'Pos {i}' for i in range(min(scores.shape[0], 10))])
    axes[1].set_ylabel('Attention Weight', fontsize=12)
    axes[1].set_title('Attention Weights by Position', fontsize=12, weight='bold')
    axes[1].set_ylim(0, 1)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    plt.show()
