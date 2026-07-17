import re
from typing import List, Tuple, Dict
import torch
from torch.utils.data import Dataset

def preprocess_text(text: str) -> List[str]:
    """
    Cleans and tokenizes raw input text.
    
    Converts text to lowercase, removes punctuation (keeping alphanumeric
    characters and whitespace), and splits into individual word tokens.
    
    Args:
        text (str): Raw input string.
        
    Returns:
        List[str]: List of tokenized words.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation, keeping alphanumeric characters and spaces
    # Replacing hyphens/newlines with space before punctuation removal to avoid joining words
    text = re.sub(r'[\r\n\t\-]', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Tokenize by splitting on any whitespace sequence
    tokens = text.split()
    return tokens

def build_vocab(tokens: List[str]) -> Tuple[Dict[str, int], Dict[int, str]]:
    """
    Builds word-to-index and index-to-word mappings from a list of tokens.
    
    Args:
        tokens (List[str]): List of all tokens in the corpus.
        
    Returns:
        Tuple[Dict[str, int], Dict[int, str]]: 
            - word_to_ix: Mapping from word strings to integer indices.
            - ix_to_word: Mapping from integer indices to word strings.
    """
    unique_tokens = sorted(list(set(tokens)))
    word_to_ix = {word: i for i, word in enumerate(unique_tokens)}
    ix_to_word = {i: word for i, word in enumerate(unique_tokens)}
    return word_to_ix, ix_to_word

def generate_context_target_pairs(tokens: List[str], window_size: int = 2) -> List[Tuple[List[str], str]]:
    """
    Generates training pairs for the CBOW model using a sliding window.
    
    For a given word at index i, context words are those within window_size to the
    left and right, excluding the target word itself. Boundary words that do not
    have enough left or right context are skipped to maintain a constant context length.
    
    Args:
        tokens (List[str]): List of tokenized words.
        window_size (int): Context window size on each side of the target word.
        
    Returns:
        List[Tuple[List[str], str]]: A list of (context_words, target_word) tuples.
    """
    pairs = []
    # If the tokens are too few to form a context, return empty
    if len(tokens) <= 2 * window_size:
        return pairs
        
    for i in range(window_size, len(tokens) - window_size):
        context = tokens[i - window_size : i] + tokens[i + 1 : i + 1 + window_size]
        target = tokens[i]
        pairs.append((context, target))
    return pairs

class CBOWDataset(Dataset):
    """
    Custom PyTorch Dataset for the Continuous Bag-of-Words (CBOW) model.
    """
    def __init__(self, pairs: List[Tuple[List[str], str]], word_to_ix: Dict[str, int]):
        """
        Initializes the dataset with context-target word pairs and vocab index mapping.
        
        Args:
            pairs (List[Tuple[List[str], str]]): List of (context_words, target_word) tuples.
            word_to_ix (Dict[str, int]): Word to index mapping dictionary.
        """
        self.pairs = pairs
        self.word_to_ix = word_to_ix

    def __len__(self) -> int:
        """
        Returns the total number of training samples.
        """
        return len(self.pairs)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Retrieves the idx-th training sample as index tensors.
        
        Args:
            idx (int): Index of the sample.
            
        Returns:
            Tuple[torch.Tensor, torch.Tensor]: 
                - context_tensor: torch.LongTensor of shape [2 * window_size]
                - target_tensor: torch.tensor (scalar long) containing target index
        """
        context_words, target_word = self.pairs[idx]
        
        # Map words to indices
        context_indices = [self.word_to_ix[w] for w in context_words]
        target_index = self.word_to_ix[target_word]
        
        # Convert to tensors
        context_tensor = torch.tensor(context_indices, dtype=torch.long)
        target_tensor = torch.tensor(target_index, dtype=torch.long)
        
        return context_tensor, target_tensor
