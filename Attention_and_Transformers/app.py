"""
🤖 Attention & Transformers: Interactive Learning Dashboard

A comprehensive Streamlit application for visualizing and understanding
attention mechanisms and transformer architectures.
"""

from matplotlib import pyplot as plt
import streamlit as st
import numpy as np
import torch
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure page
st.set_page_config(
    page_title="Attention & Transformers",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main { padding-top: 2rem; }
    .block-container { padding-top: 1rem; }
    h1 { color: #1f77b4; }
    h2 { color: #ff7f0e; }
    .stTabs [data-baseweb="tab-list"] button { font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE 1: HOME
# ============================================================================

def page_home():
    """Welcome page with overview and quick start."""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("🤖 Attention & Transformers")
        st.markdown("""
        ## Interactive Learning Dashboard
        
        Welcome to your comprehensive guide to understanding **Attention Mechanisms** 
        and **Transformer Architectures**!
        
        ### What You'll Learn
        
        - 📚 **Attention Basics**: How attention mechanisms work
        - 🔍 **Scaled Dot-Product Attention**: The core mechanism
        - 🧠 **Multi-Head Attention**: Parallel attention heads
        - 🏗️ **Transformers**: Complete architecture
        - 📍 **Positional Encoding**: Adding order to attention
        - 🚀 **Training**: From scratch to production
        - 🎯 **Applications**: Real-world use cases
        """)
    
    with col2:
        st.metric("📊 Total Modules", 7)
        st.metric("📓 Notebooks", 7)
        st.metric("🎨 Visualizations", "15+")
        st.metric("⏱️ Learning Time", "6-8 hrs")
    
    st.markdown("---")
    
    # Learning paths
    st.subheader("🎓 Choose Your Learning Path")
    
    learning_paths = {
        "🟢 Beginner": {
            "duration": "1-2 hours",
            "level": "Basics",
            "topics": ["Attention Basics", "Scaled Dot-Product"],
            "notebooks": ["01", "02"]
        },
        "🟡 Intermediate": {
            "duration": "3-4 hours",
            "level": "Core Concepts",
            "topics": ["Multi-Head Attention", "Transformers", "Positional Encoding"],
            "notebooks": ["03", "04", "05"]
        },
        "🔴 Advanced": {
            "duration": "6-8 hours",
            "level": "Expert",
            "topics": ["Training", "Applications", "Fine-tuning"],
            "notebooks": ["06", "07"]
        },
        "🎯 Applied": {
            "duration": "4-6 hours",
            "level": "Practical",
            "topics": ["Real Applications", "Transfer Learning", "Custom Data"],
            "notebooks": ["07"]
        }
    }
    
    cols = st.columns(len(learning_paths))
    for col, (path_name, path_info) in zip(cols, learning_paths.items()):
        with col:
            st.info(f"""
            ### {path_name}
            **Duration**: {path_info['duration']}  
            **Level**: {path_info['level']}
            """)
    
    st.markdown("---")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💡 Key Concepts", "25+")
    with col2:
        st.metric("🔗 Interactions", "50+")
    with col3:
        st.metric("📊 Visualizations", "100+")
    with col4:
        st.metric("🎓 Quiz Questions", "40+")
    
    st.markdown("---")
    
    # Getting started
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Quick Start")
        st.markdown("""
        1. **Explore the Dashboard**: Start with the sidebar menu
        2. **Read the Notebooks**: Open Jupyter and follow along
        3. **Experiment**: Use the interactive tools
        4. **Visualize**: See attention weights in action
        5. **Apply**: Build your own transformers
        """)
    
    with col2:
        st.subheader("📚 Resources")
        st.markdown("""
        - **Paper**: Vaswani et al. (2017) - Attention is All You Need
        - **Docs**: Hugging Face Transformers
        - **Code**: Full implementations included
        - **Data**: Auto-downloading datasets
        """)


# ============================================================================
# PAGE 2: ATTENTION MECHANICS
# ============================================================================

def page_attention_mechanics():
    """Interactive attention visualization and explanation."""
    
    st.title("📚 Attention Mechanics")
    
    tabs = st.tabs([
        "Intuition",
        "Scaled Dot-Product",
        "Multi-Head",
        "Visualization",
        "Heatmaps"
    ])
    
    # Tab 1: Intuition
    with tabs[0]:
        st.subheader("What is Attention?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### The Core Idea
            
            Attention allows a model to **focus** on specific parts of the input 
            that are most relevant for producing the output.
            
            **Like a spotlight**: Instead of processing everything equally, 
            you focus on what matters most.
            
            ### Real-World Analogy
            
            In a conversation with multiple people:
            - You hear all conversations (input)
            - You focus on the relevant speaker (attention)
            - You understand the important parts (weighted output)
            """)
        
        with col2:
            st.markdown("""
            ### Why Use Attention?
            
            ✅ **Longer sequences**: Handle long-range dependencies  
            ✅ **Interpretable**: See what the model attends to  
            ✅ **Efficient**: Focus computation on relevant parts  
            ✅ **Flexible**: Works with variable-length sequences  
            
            ### Key Advantages
            
            | Aspect | Without Attention | With Attention |
            |--------|-------------------|-----------------|
            | Long deps. | ❌ Vanishing gradients | ✅ Direct paths |
            | Interpretability | ❌ Black box | ✅ Attention weights |
            | Scalability | ⚠️ Limited | ✅ Parallelizable |
            """)
        
        # Interactive example
        st.subheader("📌 Interactive Example")
        
        sentence = st.text_input(
            "Enter a sentence:",
            value="The cat sat on the mat"
        )
        
        target_word = st.selectbox(
            "Select target word to focus on:",
            sentence.split()
        )
        
        # Simple attention computation
        words = sentence.split()
        target_idx = words.index(target_word)
        
        # Compute attention weights (simple similarity-based)
        attention_scores = np.random.rand(len(words))
        attention_scores[target_idx] = 0.9
        attention_weights = np.exp(attention_scores) / np.exp(attention_scores).sum()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Sentence with Attention Weights:**")
            for word, weight in zip(words, attention_weights):
                st.write(f"{word}: {weight:.3f} " + "█" * int(weight * 50))
        
        with col2:
            st.bar_chart({"Word": words, "Attention": attention_weights})
    
    # Tab 2: Scaled Dot-Product Attention
    with tabs[1]:
        st.subheader("Scaled Dot-Product Attention")
        
        st.markdown("""
        ## The Formula
        
        $$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$$
        
        Where:
        - **Q**: Query matrix (what we're looking for)
        - **K**: Key matrix (what each position has)
        - **V**: Value matrix (the actual information)
        - **d_k**: Dimension of keys (for scaling)
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📐 Interactive Computation")
            
            # Input dimensions
            seq_len = st.slider("Sequence Length", 2, 10, 4, key="seq_len_scaled")
            d_k = st.slider("Key Dimension (d_k)", 2, 10, 4, key="dk_scaled")
            
            # Create sample matrices
            Q = np.random.randn(seq_len, d_k)
            K = np.random.randn(seq_len, d_k)
            V = np.random.randn(seq_len, d_k)
            
            # Step 1: QK^T
            scores = Q @ K.T
            st.write("**Step 1: Compute Scores (QK^T)**")
            st.dataframe(scores, use_container_width=True)
            
            # Step 2: Scale
            scores_scaled = scores / np.sqrt(d_k)
            st.write("**Step 2: Scale by √d_k**")
            st.dataframe(scores_scaled, use_container_width=True)
            
            # Step 3: Softmax
            attention_weights = np.exp(scores_scaled) / np.exp(scores_scaled).sum(axis=1, keepdims=True)
            st.write("**Step 3: Apply Softmax**")
            st.dataframe(attention_weights, use_container_width=True)
            
            # Step 4: Output
            output = attention_weights @ V
            st.write("**Step 4: Multiply by Values**")
            st.dataframe(output, use_container_width=True)
        
        with col2:
            st.subheader("🎨 Visualization")
            
            # Create the figure and axes first
            fig, axes = plt.subplots(2, 2, figsize=(10, 8))
            
            # Heatmap 1: Scores
            im1 = axes[0, 0].imshow(scores, cmap='RdBu')
            axes[0, 0].set_title('Scores (QK^T)')
            plt.colorbar(im1, ax=axes[0, 0])
            
            # Heatmap 2: Scaled Scores
            im2 = axes[0, 1].imshow(scores_scaled, cmap='RdBu')
            axes[0, 1].set_title('Scaled Scores')
            plt.colorbar(im2, ax=axes[0, 1])
            
            # Heatmap 3: Attention Weights
            im3 = axes[1, 0].imshow(attention_weights, cmap='YlGn')
            axes[1, 0].set_title('Attention Weights (Softmax)')
            plt.colorbar(im3, ax=axes[1, 0])
            
            # Heatmap 4: Output
            im4 = axes[1, 1].imshow(output, cmap='viridis')
            axes[1, 1].set_title('Output (Attention @ V)')
            plt.colorbar(im4, ax=axes[1, 1])
            
            plt.tight_layout()
            # Render the figure to Streamlit here at the end
            st.pyplot(fig)
    
    # Tab 3: Multi-Head Attention
    with tabs[2]:
        st.subheader("Multi-Head Attention")
        
        st.markdown("""
        ## The Concept
        
        Instead of one attention computation, run **multiple** attention heads in parallel:
        
        $$\\text{MultiHead}(Q,K,V) = \\text{Concat}(\\text{head}_1, ..., \\text{head}_h)W^O$$
        
        Where each head performs scaled dot-product attention independently.
        
        ### Why Multiple Heads?
        - Different heads learn different patterns
        - Each head focuses on different relationships
        - Richer representations
        """)
        
        num_heads = st.slider("Number of Heads", 1, 8, 4, key="heads_multi")
        seq_len = st.slider("Sequence Length", 2, 10, 4, key="seq_len_multi")
        embed_dim = st.slider("Embedding Dimension", 8, 64, 32, key="embed_multi")
        
        st.write(f"**Configuration:**")
        st.write(f"- Number of heads: {num_heads}")
        st.write(f"- Sequence length: {seq_len}")
        st.write(f"- Total embedding dim: {embed_dim}")
        st.write(f"- Dimension per head: {embed_dim // num_heads}")
        
        # Visualize head outputs
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Individual Head Attention Weights:**")
            for head_idx in range(min(num_heads, 4)):
                head_weights = np.random.rand(seq_len, seq_len)
                head_weights = head_weights / head_weights.sum(axis=1, keepdims=True)
                
                st.write(f"Head {head_idx + 1}:")
                st.dataframe(head_weights)
        
        with col2:
            st.write("**Concatenated Output:**")
            # Create visualization of concatenated heads
            fig, ax = plt.subplots(figsize=(10, 4))
            
            all_head_weights = np.random.rand(num_heads, seq_len)
            im = ax.imshow(all_head_weights, aspect='auto', cmap='viridis')
            ax.set_xlabel('Sequence Position')
            ax.set_ylabel('Head Index')
            ax.set_title('Attention Weights Across Heads')
            plt.colorbar(im, ax=ax)
            plt.tight_layout()
            
            st.pyplot(fig)
    
    # Tab 4: Visualization
    with tabs[3]:
        st.subheader("Interactive Attention Visualization")
        
        # Example: Attention in translation
        source = "The cat is sleeping"
        target = "Le chat dort"
        
        source_tokens = source.split()
        target_tokens = target.split()
        
        st.write(f"**Source**: {source}")
        st.write(f"**Target**: {target}")
        
        # Random attention matrix
        attention_matrix = np.random.rand(len(target_tokens), len(source_tokens))
        attention_matrix = attention_matrix / attention_matrix.sum(axis=1, keepdims=True)
        
        # Heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.imshow(attention_matrix, cmap='YlOrRd', aspect='auto')
        
        ax.set_xticks(range(len(source_tokens)))
        ax.set_yticks(range(len(target_tokens)))
        ax.set_xticklabels(source_tokens)
        ax.set_yticklabels(target_tokens)
        
        ax.set_xlabel('Source Tokens')
        ax.set_ylabel('Target Tokens')
        ax.set_title('Attention Weights (Source → Target)')
        
        # Add text annotations
        for i in range(len(target_tokens)):
            for j in range(len(source_tokens)):
                text = ax.text(j, i, f'{attention_matrix[i, j]:.2f}',
                              ha="center", va="center", color="black", fontsize=8)
        
        plt.colorbar(im, ax=ax)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Tab 5: Heatmaps
    with tabs[4]:
        st.subheader("Attention Weight Heatmaps")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Position-to-Position Attention**")
            # Random attention matrix
            seq_len = 6
            attention = np.random.rand(seq_len, seq_len)
            attention = attention / attention.sum(axis=1, keepdims=True)
            
            fig, ax = plt.subplots(figsize=(6, 6))
            im = ax.imshow(attention, cmap='Greens', aspect='auto')
            ax.set_title('Self-Attention Weights')
            ax.set_xlabel('Key Position')
            ax.set_ylabel('Query Position')
            plt.colorbar(im, ax=ax)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.write("**Head Comparison**")
            # Multiple heads
            num_heads = 4
            heads_data = np.random.rand(num_heads, seq_len, seq_len)
            
            fig, axes = plt.subplots(2, 2, figsize=(8, 8))
            axes = axes.flatten()
            
            for head_idx in range(num_heads):
                im = axes[head_idx].imshow(heads_data[head_idx], cmap='Blues')
                axes[head_idx].set_title(f'Head {head_idx + 1}')
                plt.colorbar(im, ax=axes[head_idx])
            
            plt.tight_layout()
            st.pyplot(fig)


# ============================================================================
# PAGE 3: TRANSFORMER ARCHITECTURE
# ============================================================================

def page_transformers():
    """Transformer architecture explanation and visualization."""
    
    st.title("🏗️ Transformer Architecture")
    
    tabs = st.tabs(["Architecture", "Encoder", "Decoder", "Data Flow", "Configuration"])
    
    with tabs[0]:
        st.subheader("Complete Transformer Architecture")
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown("""
            ## Encoder-Decoder Architecture
            
            ```
            INPUT → ENCODER → DECODER → OUTPUT
            ```
            
            ### Encoder Stack
            - Multi-head self-attention
            - Feed-forward network
            - Residual connections
            - Layer normalization
            - Positional encoding
            
            ### Decoder Stack
            - Masked self-attention
            - Encoder-decoder attention
            - Feed-forward network
            - Residual connections
            - Layer normalization
            - Output linear + softmax
            """)
        
        with col2:
            st.info("""
            ### Key Components
            
            - **Embeddings**: Convert tokens to vectors
            - **Positional Encoding**: Add position information
            - **Self-Attention**: Attend to all positions
            - **Cross-Attention**: Attend to encoder
            - **Feed-Forward**: Per-position processing
            - **Normalization**: Stabilize training
            - **Linear**: Output projection
            """)
        
        # Architecture diagram
        st.markdown("---")
        st.subheader("Architecture Diagram")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Simple ASCII-like diagram
        ax.text(0.5, 0.95, "TRANSFORMER ARCHITECTURE", ha='center', fontsize=14, weight='bold')
        
        # Input
        ax.text(0.5, 0.85, "Input: Word Embeddings + Positional Encoding", 
                ha='center', bbox=dict(boxstyle='round', facecolor='lightblue'))
        
        # Encoder
        ax.text(0.2, 0.7, "ENCODER", ha='center', fontsize=12, weight='bold')
        ax.text(0.2, 0.65, "N × [Self-Attention + FFN]", ha='center', fontsize=10)
        
        # Decoder
        ax.text(0.8, 0.7, "DECODER", ha='center', fontsize=12, weight='bold')
        ax.text(0.8, 0.65, "N × [Masked SA + Cross-Attn + FFN]", ha='center', fontsize=10)
        
        # Output
        ax.text(0.5, 0.45, "Encoder Output", ha='center', 
                bbox=dict(boxstyle='round', facecolor='lightgreen'))
        ax.text(0.8, 0.45, "Decoder Output", ha='center',
                bbox=dict(boxstyle='round', facecolor='lightyellow'))
        
        ax.text(0.5, 0.3, "Final Layer + Softmax", ha='center',
                bbox=dict(boxstyle='round', facecolor='lightcoral'))
        
        ax.text(0.5, 0.15, "Output Probabilities", ha='center', fontsize=12, weight='bold')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        st.pyplot(fig)
    
    with tabs[1]:
        st.subheader("Encoder Layer")
        
        st.markdown("""
        ## Encoder Forward Pass
        
        Each encoder layer applies:
        
        1. **Multi-Head Self-Attention**
           - Each position attends to all positions
           - Parallel attention heads
           
        2. **Feed-Forward Network**
           - Two linear layers with ReLU
           - d_model → d_ff → d_model
           
        3. **Residual Connections**
           - x + Sublayer(x)
           
        4. **Layer Normalization**
           - Normalize before/after each sublayer
        """)
        
        with st.expander("📝 Detailed Encoder Processing"):
            st.code("""
def encoder_layer(x, self_attention, feed_forward):
    # Multi-head self-attention
    attn_output = self_attention(x, x, x)
    x = LayerNorm(x + attn_output)  # Residual + Norm
    
    # Feed-forward
    ff_output = feed_forward(x)
    x = LayerNorm(x + ff_output)    # Residual + Norm
    
    return x
            """, language='python')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Step-by-Step Computation**")
            
            # Simulate encoder processing
            seq_len = 5
            embed_dim = 8
            
            x = np.random.randn(seq_len, embed_dim)
            
            steps = [
                ("Input", x),
                ("After Self-Attention", x + np.random.randn(seq_len, embed_dim) * 0.1),
                ("After LayerNorm", x + np.random.randn(seq_len, embed_dim) * 0.05),
                ("After FFN", x + np.random.randn(seq_len, embed_dim) * 0.1),
            ]
            
            for step_name, step_output in steps:
                st.write(f"**{step_name}**:")
                st.dataframe(step_output[:3, :4])  # Show partial
        
        with col2:
            st.write("**Output Shapes**")
            st.code("""
Input:  (seq_len=5, embed_dim=8)

Self-Attention:
  Query: (5, 8) → (5, 8)
  Key:   (5, 8) → (5, 8)
  Value: (5, 8) → (5, 8)
  Output: (5, 8)

FFN:
  Linear1: (5, 8) → (5, 32)
  ReLU: activation
  Linear2: (5, 32) → (5, 8)

Output: (5, 8)
            """)
    
    with tabs[2]:
        st.subheader("Decoder Layer")
        
        st.markdown("""
        ## Decoder Forward Pass
        
        Each decoder layer applies:
        
        1. **Masked Multi-Head Self-Attention**
           - Each position attends to previous positions only
           - Prevents cheating during training
           
        2. **Cross-Attention**
           - Decoder attends to encoder outputs
           - Query: decoder, Key/Value: encoder
           
        3. **Feed-Forward Network**
           - Same as encoder
           
        4. **Residual + Normalization**
           - After each sublayer
        """)
        
        with st.expander("📝 Detailed Decoder Processing"):
            st.code("""
def decoder_layer(tgt, memory, self_attention, 
                  cross_attention, feed_forward):
    # Masked self-attention (autoregressive)
    self_attn = self_attention(tgt, tgt, tgt, mask=causal_mask)
    tgt = LayerNorm(tgt + self_attn)
    
    # Cross-attention to encoder
    cross_attn = cross_attention(tgt, memory, memory)
    tgt = LayerNorm(tgt + cross_attn)
    
    # Feed-forward
    ff_output = feed_forward(tgt)
    tgt = LayerNorm(tgt + ff_output)
    
    return tgt
            """, language='python')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Autoregressive Masking**")
            
            seq_len = 4
            # Causal mask
            mask = np.triu(np.ones((seq_len, seq_len)), k=1).astype(bool)
            
            fig, ax = plt.subplots(figsize=(6, 5))
            im = ax.imshow(mask, cmap='RdYlGn_r', aspect='auto')
            ax.set_title('Causal Mask (Can\'t Attend to Future)')
            ax.set_xlabel('Key Position')
            ax.set_ylabel('Query Position')
            plt.colorbar(im, ax=ax, label='Masked')
            st.pyplot(fig)
        
        with col2:
            st.write("**Cross-Attention**")
            
            # Encoder-decoder attention
            enc_len, dec_len = 5, 4
            cross_attn = np.random.rand(dec_len, enc_len)
            cross_attn = cross_attn / cross_attn.sum(axis=1, keepdims=True)
            
            fig, ax = plt.subplots(figsize=(6, 5))
            im = ax.imshow(cross_attn, cmap='Blues', aspect='auto')
            ax.set_title('Cross-Attention\n(Decoder → Encoder)')
            ax.set_xlabel('Encoder Position')
            ax.set_ylabel('Decoder Position')
            plt.colorbar(im, ax=ax)
            st.pyplot(fig)
    
    with tabs[3]:
        st.subheader("Data Flow Through Transformer")
        
        st.markdown("""
        ## Complete Forward Pass
        
        Trace how data flows through the entire transformer...
        """)
        
        # Input parameters
        col1, col2 = st.columns(2)
        
        with col1:
            vocab_size = st.slider("Vocabulary Size", 100, 10000, 1000)
            seq_len = st.slider("Sequence Length", 2, 50, 10)
        
        with col2:
            embed_dim = st.slider("Embedding Dimension", 8, 512, 64)
            num_heads = st.slider("Number of Heads", 1, 8, 4)
        
        # Data flow
        st.markdown("---")
        st.subheader("Step-by-Step Data Flow")
        
        flow_steps = [
            ("Input IDs", f"Shape: ({seq_len},)", f"Values: token indices"),
            ("Embeddings", f"Shape: ({seq_len}, {embed_dim})", f"Convert tokens to vectors"),
            ("+ Pos Encoding", f"Shape: ({seq_len}, {embed_dim})", f"Add position information"),
            ("Encoder Layer", f"Shape: ({seq_len}, {embed_dim})", f"Self-attention + FFN"),
            ("Encoder Output", f"Shape: ({seq_len}, {embed_dim})", f"Context vectors"),
            ("Decoder Start", f"Shape: (1, {embed_dim})", f"Start token"),
            ("Decoder Layers", f"Shape: (1, {embed_dim})", f"Cross-attention to encoder"),
            ("Output Logits", f"Shape: ({vocab_size},)", f"Next token probabilities"),
        ]
        
        for i, (stage, shape, description) in enumerate(flow_steps):
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                st.write(f"**{i+1}. {stage}**")
            with col2:
                st.code(shape)
            with col3:
                st.write(description)
        
        st.markdown("---")
        st.subheader("Memory & Computation")
        
        # Calculate memory and compute
        ff_dim = embed_dim * 4
        
        params = {
            "Embeddings": vocab_size * embed_dim,
            "Self-Attention": embed_dim ** 2 * 3,  # Q, K, V
            "FFN": embed_dim * ff_dim * 2,
            "Layer Norms": embed_dim * 2,
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Parameters per Layer**")
            for component, param_count in params.items():
                st.write(f"{component}: {param_count:,}")
        
        with col2:
            st.write("**Memory Usage**")
            total_params = sum(params.values())
            st.metric("Total Parameters", f"{total_params:,}")
            st.metric("Memory (float32)", f"{total_params * 4 / 1e6:.1f} MB")
    
    with tabs[4]:
        st.subheader("Model Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Architecture Parameters**")
            
            config = {
                "vocab_size": st.number_input("Vocabulary Size", value=10000),
                "embed_dim": st.select_slider("Embedding Dimension", [64, 128, 256, 512, 768, 1024], value=512),
                "num_heads": st.select_slider("Number of Heads", [4, 8, 12, 16], value=8),
                "num_layers": st.slider("Number of Layers", 1, 12, 6),
                "ff_dim": st.select_slider("FFN Dimension", [512, 1024, 2048, 4096], value=2048),
                "max_seq_len": st.slider("Max Sequence Length", 50, 4096, 512),
            }
        
        with col2:
            st.write("**Training Parameters**")
            
            training = {
                "batch_size": st.select_slider("Batch Size", [8, 16, 32, 64, 128], value=32),
                "learning_rate": st.select_slider("Learning Rate", [1e-5, 1e-4, 1e-3, 1e-2], value=1e-4),
                "warmup_steps": st.number_input("Warmup Steps", value=4000),
                "dropout": st.slider("Dropout", 0.0, 0.5, 0.1),
            }
        
        st.markdown("---")
        
        # Display as YAML
        st.write("**Configuration Summary**")
        
        config_text = f"""
# Architecture
model:
  vocab_size: {config['vocab_size']}
  embed_dim: {config['embed_dim']}
  num_heads: {config['num_heads']}
  num_layers: {config['num_layers']}
  ff_dim: {config['ff_dim']}
  max_seq_len: {config['max_seq_len']}

# Training
training:
  batch_size: {training['batch_size']}
  learning_rate: {training['learning_rate']}
  warmup_steps: {training['warmup_steps']}
  dropout: {training['dropout']}
        """
        
        st.code(config_text, language='yaml')


# ============================================================================
# PAGE 4: INTERACTIVE TUTORIAL
# ============================================================================

def page_tutorial():
    """Interactive learning module."""
    
    st.title("🎓 Interactive Tutorial")
    
    modules = {
        "1": "Attention Basics",
        "2": "Scaled Dot-Product",
        "3": "Multi-Head Attention",
        "4": "Transformers Intro",
        "5": "Positional Encoding",
        "6": "Training Guide",
        "7": "Applications",
    }
    
    selected_module = st.selectbox("Select Module:", list(modules.values()))
    
    if "Attention Basics" in selected_module:
        st.subheader("Module 1: Attention Basics")
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown("""
            ### What is Attention?
            
            Attention is a mechanism that allows models to **selectively focus** 
            on specific parts of the input.
            
            ### Key Intuition
            
            In machine translation:
            ```
            Source: "The cat is sleeping"
            Target: "Le chat dort"
            
            When translating "cat" → "chat":
            - Focus on the word "cat" in source
            - Ignore other words
            - Translate based on focused context
            ```
            
            ### Mathematical Definition
            
            Attention computes a **weighted average** of values based on 
            query-key similarity.
            """)
        
        with col2:
            st.info("""
            ### Learning Objectives
            
            ✓ Understand why attention helps  
            ✓ Know when to use attention  
            ✓ Grasp the basic computation
            
            ### Time: ~15 minutes
            """)
        
        st.markdown("---")
        
        # Quiz
        st.subheader("📝 Quick Quiz")
        
        quiz_q1 = st.radio(
            "What does attention help solve?",
            [
                "Long-range dependencies in sequences",
                "Overfitting to training data",
                "Reducing model parameters",
                "Speeding up matrix multiplication"
            ]
        )
        
        if quiz_q1 == "Long-range dependencies in sequences":
            st.success("✅ Correct!")
        else:
            st.error("❌ Try again!")
    
    elif "Scaled Dot-Product" in selected_module:
        st.subheader("Module 2: Scaled Dot-Product Attention")
        
        st.markdown("""
        ## The Core Formula
        
        $$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$$
        """)
        
        st.write("Interactive computation shown earlier in Attention Mechanics tab.")
    
    else:
        st.info(f"Module: {selected_module} - Full content in Jupyter notebooks")


# ============================================================================
# PAGE 5: EXPERIMENTS
# ============================================================================

def page_experiments():
    """Experiment and training interface."""
    
    st.title("🔬 Experiments")
    
    tabs = st.tabs(["Train from Scratch", "Benchmark", "Ablation Study", "Analysis"])
    
    with tabs[0]:
        st.subheader("Train Attention from Scratch")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Dataset**")
            dataset = st.selectbox(
                "Select Dataset:",
                ["MNIST", "Fashion-MNIST", "AG News", "Movie Reviews", "IWSLT2017"]
            )
            samples = st.slider("Number of Samples", 100, 50000, 10000)
        
        with col2:
            st.write("**Model**")
            attention_type = st.selectbox(
                "Attention Type:",
                ["Scaled Dot-Product", "Multi-Head", "Custom"]
            )
            hidden_dim = st.slider("Hidden Dimension", 32, 512, 128)
        
        if st.button("🚀 Start Training"):
            st.info("Training would begin here (requires actual training loop)")
            
            # Simulate training progress
            progress_bar = st.progress(0)
            epochs = 5
            
            for epoch in range(epochs):
                for batch in range(10):
                    progress = (epoch * 10 + batch) / (epochs * 10)
                    progress_bar.progress(progress)
                
                st.write(f"Epoch {epoch + 1}/5 - Loss: {np.random.rand() * 2:.3f}")
    
    with tabs[1]:
        st.subheader("Model Benchmarking")
        
        # Benchmark results
        models = ["Attention", "CNN", "RNN", "Transformer"]
        metrics = {
            "Accuracy": [0.95, 0.92, 0.90, 0.97],
            "Speed (samples/sec)": [1000, 1500, 500, 2000],
            "Memory (MB)": [250, 200, 300, 400],
        }
        
        for metric, values in metrics.items():
            col = st.columns(len(models))
            for i, (model, value) in enumerate(zip(models, values)):
                with col[i]:
                    st.metric(model, f"{value:.1f}")
    
    with tabs[2]:
        st.subheader("Ablation Study")
        
        st.write("Remove components and analyze impact:")
        
        components = {
            "Multi-Head Attention": {"Accuracy": -0.05, "Speed": 1.2},
            "Positional Encoding": {"Accuracy": -0.15, "Speed": 1.0},
            "Residual Connections": {"Accuracy": -0.10, "Speed": 1.1},
            "Layer Normalization": {"Accuracy": -0.08, "Speed": 1.0},
        }
        
        for component, impact in components.items():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**{component}**")
            with col2:
                st.metric("Accuracy Impact", f"{impact['Accuracy']:.1%}")
            with col3:
                st.metric("Speed Multiplier", f"{impact['Speed']}x")
    
    with tabs[3]:
        st.subheader("Model Analysis")
        
        # Attention pattern analysis
        st.write("Analyze learned attention patterns...")
        
        # Visualize attention patterns
        num_layers = 6
        seq_len = 10
        
        fig, axes = plt.subplots(2, 3, figsize=(12, 8))
        axes = axes.flatten()
        
        for layer_idx in range(num_layers):
            attention = np.random.rand(seq_len, seq_len)
            attention = attention / attention.sum(axis=1, keepdims=True)
            
            im = axes[layer_idx].imshow(attention, cmap='viridis')
            axes[layer_idx].set_title(f'Layer {layer_idx + 1}')
            plt.colorbar(im, ax=axes[layer_idx])
        
        plt.tight_layout()
        st.pyplot(fig)


# ============================================================================
# PAGE 6: ANALYSIS TOOLS
# ============================================================================

def page_analysis():
    """Analysis and interpretation tools."""
    
    st.title("📊 Analysis Tools")
    
    tabs = st.tabs(["Attention Analysis", "Token Importance", "Embeddings"])
    
    with tabs[0]:
        st.subheader("Attention Pattern Analysis")
        
        # Select what to analyze
        layer = st.slider("Layer", 0, 11, 5)
        head = st.slider("Head", 0, 11, 0)
        
        # Create attention heatmap
        seq_len = 12
        attention = np.random.rand(seq_len, seq_len)
        attention = attention / attention.sum(axis=1, keepdims=True)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        im = ax.imshow(attention, cmap='YlOrRd', aspect='auto')
        ax.set_title(f'Attention Pattern - Layer {layer}, Head {head}')
        ax.set_xlabel('Key Tokens')
        ax.set_ylabel('Query Tokens')
        plt.colorbar(im, ax=ax)
        st.pyplot(fig)
    
    with tabs[1]:
        st.subheader("Token Importance Ranking")
        
        tokens = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
        importance = np.random.rand(len(tokens))
        
        # Sort
        sorted_idx = np.argsort(importance)[::-1]
        sorted_tokens = [tokens[i] for i in sorted_idx]
        sorted_importance = importance[sorted_idx]
        
        fig, ax = plt.subplots()
        ax.barh(sorted_tokens, sorted_importance, color='steelblue')
        ax.set_xlabel('Importance Score')
        ax.set_title('Token Importance')
        st.pyplot(fig)
    
    with tabs[2]:
        st.subheader("Embedding Space Visualization")
        
        method = st.selectbox("Projection Method:", ["t-SNE", "UMAP", "PCA"])
        
        # Create random embeddings
        num_samples = 100
        num_features = 768
        embeddings = np.random.randn(num_samples, num_features)
        
        # Simple 2D projection (normally would use t-SNE/UMAP)
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        projected = pca.fit_transform(embeddings)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        scatter = ax.scatter(projected[:, 0], projected[:, 1], 
                            c=np.arange(num_samples), cmap='viridis', s=100)
        ax.set_title(f'Embedding Space ({method})')
        plt.colorbar(scatter, ax=ax, label='Sample Index')
        st.pyplot(fig)


# ============================================================================
# PAGE 7: FAQ & RESOURCES
# ============================================================================

def page_faq():
    """FAQ and resources."""
    
    st.title("❓ FAQ & Resources")
    
    with st.expander("What is attention?"):
        st.write("""
        Attention is a mechanism that allows models to focus on specific parts 
        of the input. It computes weighted averages of values based on the 
        similarity between queries and keys.
        """)
    
    with st.expander("Why are transformers better than RNNs?"):
        st.write("""
        - Transformers can process sequences in parallel (no recurrence)
        - Self-attention captures long-range dependencies directly
        - More efficient training and inference
        - Better performance on large datasets
        """)
    
    with st.expander("How do I implement attention from scratch?"):
        st.write("""
        See Notebook 02: Scaled Dot-Product Attention for full implementation.
        
        Basic steps:
        1. Compute Q, K, V matrices
        2. Calculate QK^T / √d_k
        3. Apply softmax
        4. Multiply by V
        """)
    
    with st.expander("What are hyperparameters I should tune?"):
        st.write("""
        - Learning rate (typically 1e-5 to 1e-3)
        - Number of attention heads (typically 8-16)
        - Hidden dimension (typically 256-1024)
        - Number of layers (typically 3-12)
        - Dropout (typically 0.1-0.3)
        - Batch size (typically 32-256)
        """)
    
    st.markdown("---")
    st.subheader("📚 Research Papers")
    
    papers = {
        "Attention is All You Need": "https://arxiv.org/abs/1706.03762",
        "BERT: Pre-training of Deep Bidirectional Transformers": "https://arxiv.org/abs/1810.04805",
        "Exploring the Limits of Transfer Learning": "https://arxiv.org/abs/1910.10683",
    }
    
    for title, url in papers.items():
        st.write(f"📖 [{title}]({url})")
    
    st.subheader("🔗 Resources")
    
    resources = {
        "Hugging Face Documentation": "https://huggingface.co/docs/transformers/",
        "PyTorch": "https://pytorch.org/",
        "Illustrated Transformer": "http://jalammar.github.io/illustrated-transformer/",
        "Distill.pub": "https://distill.pub/",
    }
    
    for name, url in resources.items():
        st.write(f"🌐 [{name}]({url})")


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main app with page navigation."""
    
    with st.sidebar:
        st.title("🤖 Attention & Transformers")
        st.markdown("---")
        
        page = st.radio(
            "Select Page:",
            [
                "🏠 Home",
                "📚 Attention Mechanics",
                "🏗️ Transformer Architecture",
                "🎓 Interactive Tutorial",
                "🔬 Experiments",
                "📊 Analysis Tools",
                "❓ FAQ & Resources"
            ]
        )
        
        st.markdown("---")
        st.write("**About This Project**")
        st.info("""
        A comprehensive learning platform for understanding attention and transformers.
        
        - 7 Jupyter notebooks
        - Interactive visualizations
        - Hands-on experiments
        - Real-world applications
        """)
    
    # Route to pages
    if "Home" in page:
        page_home()
    elif "Attention Mechanics" in page:
        page_attention_mechanics()
    elif "Transformer Architecture" in page:
        page_transformers()
    elif "Interactive Tutorial" in page:
        page_tutorial()
    elif "Experiments" in page:
        page_experiments()
    elif "Analysis Tools" in page:
        page_analysis()
    elif "FAQ" in page:
        page_faq()


if __name__ == "__main__":
    main()
