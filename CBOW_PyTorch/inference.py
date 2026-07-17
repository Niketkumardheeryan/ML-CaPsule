import os
import json
import argparse
import torch
import torch.nn.functional as F

from dataset import preprocess_text
from cbow import CBOWModel

def load_inference_model(model_dir: str, device: torch.device):
    """
    Loads the trained model weights and configuration metadata.
    
    Args:
        model_dir (str): Directory containing the weights and metadata.
        device (torch.device): Device to load the model to.
        
    Returns:
        Tuple[CBOWModel, dict]: The loaded model and metadata dictionary.
    """
    metadata_path = os.path.join(model_dir, "metadata.json")
    model_path = os.path.join(model_dir, "cbow_model.pt")
    
    if not os.path.exists(metadata_path) or not os.path.exists(model_path):
        raise FileNotFoundError(f"Model or metadata not found in '{model_dir}'. Run train.py first.")
        
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
        
    # Standardize dictionary keys (JSON keys are stored as strings)
    metadata["ix_to_word"] = {int(k): v for k, v in metadata["ix_to_word"].items()}
    
    # Initialize model
    model = CBOWModel(vocab_size=metadata["vocab_size"], embedding_dim=metadata["embed_dim"])
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    
    return model, metadata

def predict_missing_word(context_words: str, model: CBOWModel, metadata: dict, device: torch.device, top_k: int = 3):
    """
    Predicts the target word based on context words.
    
    Args:
        context_words (str): Space-separated context words.
        model (CBOWModel): Trained PyTorch CBOW model.
        metadata (dict): Vocabulary and parameter metadata.
        device (torch.device): CPU or GPU device.
        top_k (int): Number of top predictions to return.
    """
    word_to_ix = metadata["word_to_ix"]
    ix_to_word = metadata["ix_to_word"]
    window_size = metadata["window_size"]
    expected_len = 2 * window_size
    
    # Clean input text
    tokens = preprocess_text(context_words)
    
    if not tokens:
        print("Error: No words entered or all words were removed by preprocessing.")
        return
        
    # Check vocabulary matches
    indices = []
    oov_words = []
    for word in tokens:
        if word in word_to_ix:
            indices.append(word_to_ix[word])
        else:
            oov_words.append(word)
            
    if oov_words:
        print(f"Warning: Words {oov_words} are out of vocabulary (OOV) and were ignored.")
        
    if len(indices) == 0:
        print("Error: None of the entered words exist in the model's vocabulary.")
        return
        
    # Validate context size
    if len(indices) != expected_len:
        print(f"Warning: Model expects exactly {expected_len} context words (window_size={window_size}). "
              f"You provided {len(indices)} valid words. Adjusting input size...")
        if len(indices) > expected_len:
            # Truncate to middle context words or first context words
            indices = indices[:expected_len]
        else:
            # Pad with the most common word or first word to match dimension
            pad_ix = indices[0]
            indices += [pad_ix] * (expected_len - len(indices))
            
    print(f"Active context tokens: {[ix_to_word[idx] for idx in indices]}")
    
    # Run forward pass
    context_tensor = torch.tensor([indices], dtype=torch.long).to(device) # shape [1, expected_len]
    with torch.no_grad():
        logits = model(context_tensor) # shape [1, vocab_size]
        probabilities = F.softmax(logits, dim=1).squeeze(0) # shape [vocab_size]
        
    # Retrieve top predictions
    top_probs, top_indices = torch.topk(probabilities, k=min(top_k, len(probabilities)))
    
    print("\n--- Predictions ---")
    for i, (prob, idx_tensor) in enumerate(zip(top_probs, top_indices)):
        idx = idx_tensor.item()
        word = ix_to_word[idx]
        is_top = "(Best Predict)" if i == 0 else ""
        print(f"Rank {i+1}: {word:<15} Prob: {prob.item():.4f} {is_top}")
    print("-------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Inference script for Continuous Bag-of-Words (CBOW)")
    parser.add_argument("--model_dir", type=str, default="saved_model", help="Directory where model and vocab are saved")
    parser.add_argument("--context", type=str, default="", help="Space-separated context words to predict the target")
    parser.add_argument("--top_k", type=int, default=3, help="Number of top predictions to display")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive command line loop")
    
    args = parser.parse_args()
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load model and configurations
    # If running from repository root, try prepending the project path
    model_dir = args.model_dir
    if not os.path.exists(model_dir):
        alt_path = os.path.join("CBOW_PyTorch", model_dir)
        if os.path.exists(alt_path):
            model_dir = alt_path
            
    try:
        model, metadata = load_inference_model(model_dir, device)
        print(f"Model successfully loaded from '{model_dir}'")
        print(f"Model Vocabulary Size: {metadata['vocab_size']}")
        print(f"Expected Context Words: {2 * metadata['window_size']} words (window_size={metadata['window_size']})")
    except FileNotFoundError as e:
        print(e)
        return
        
    # Handle single prediction or run interactive loop
    if args.context:
        print(f"\nContext entered: '{args.context}'")
        predict_missing_word(args.context, model, metadata, device, top_k=args.top_k)
    elif args.interactive or not args.context:
        print("\n--- Interactive CBOW Inference Mode ---")
        print(f"Type {2 * metadata['window_size']} context words surrounding the target word to predict.")
        print("Example: 'popular architecture training embeddings' to predict 'model'")
        print("Type 'exit' or 'quit' to close the program.\n")
        
        while True:
            try:
                user_input = input("Enter context words: ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    print("Exiting interactive inference. Goodbye!")
                    break
                if not user_input:
                    continue
                predict_missing_word(user_input, model, metadata, device, top_k=args.top_k)
            except KeyboardInterrupt:
                print("\nExiting interactive inference. Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
