import torch
import torch.nn as nn

class CBOWModel(nn.Module):
    """
    Continuous Bag-of-Words (CBOW) Model implemented in PyTorch.
    
    The architecture consists of:
    1. An embedding layer to map word indices to dense vectors.
    2. A mean pooling step that averages context embeddings.
    3. A linear output projection layer to compute vocab logits.
    """
    def __init__(self, vocab_size: int, embedding_dim: int):
        """
        Initializes the CBOW model layers.
        
        Args:
            vocab_size (int): Size of the vocabulary.
            embedding_dim (int): Dimensionality of the dense word embeddings.
        """
        super(CBOWModel, self).__init__()
        
        # Word embedding lookup table
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        
        # Fully connected layer projecting average embedding to vocabulary logits
        self.linear = nn.Linear(embedding_dim, vocab_size)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """
        Defines the forward computation of the model.
        
        Args:
            inputs (torch.Tensor): Context tensor of shape [batch_size, context_size].
            
        Returns:
            torch.Tensor: Logits tensor of shape [batch_size, vocab_size].
        """
        # Lookup embeddings: [batch_size, context_size] -> [batch_size, context_size, embedding_dim]
        embeds = self.embeddings(inputs)
        
        # Average the embeddings of context words: -> [batch_size, embedding_dim]
        mean_embeds = torch.mean(embeds, dim=1)
        
        # Project to vocabulary space logits: -> [batch_size, vocab_size]
        logits = self.linear(mean_embeds)
        
        return logits
