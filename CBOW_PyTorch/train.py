import os
import json
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from dataset import preprocess_text, build_vocab, generate_context_target_pairs, CBOWDataset
from cbow import CBOWModel

def main():
    parser = argparse.ArgumentParser(description="Train Continuous Bag-of-Words (CBOW) Word Embeddings in PyTorch")
    parser.add_argument("--corpus", type=str, default="sample_corpus.txt", help="Path to raw text corpus file")
    parser.add_argument("--window_size", type=int, default=2, help="Context window size (C)")
    parser.add_argument("--embed_dim", type=int, default=50, help="Embedding dimension size")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=0.005, help="Learning rate")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training")
    parser.add_argument("--model_dir", type=str, default="saved_model", help="Directory to save model checkpoints and vocab metadata")
    
    args = parser.parse_args()
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 1. Read and preprocess text corpus
    if not os.path.exists(args.corpus):
        # If running from repository root, try prepending the project path
        alt_path = os.path.join("CBOW_PyTorch", args.corpus)
        if os.path.exists(alt_path):
            args.corpus = alt_path
        else:
            raise FileNotFoundError(f"Corpus file not found: {args.corpus}")
            
    print(f"Reading corpus from: {args.corpus}")
    with open(args.corpus, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    tokens = preprocess_text(raw_text)
    print(f"Tokenized corpus: {len(tokens)} total tokens.")
    
    # 2. Build vocabularies
    word_to_ix, ix_to_word = build_vocab(tokens)
    vocab_size = len(word_to_ix)
    print(f"Vocabulary size: {vocab_size} unique words.")
    
    if vocab_size == 0:
        print("Error: Vocabulary is empty. Please check the content of your corpus.")
        return
        
    # 3. Generate context-target training pairs
    pairs = generate_context_target_pairs(tokens, window_size=args.window_size)
    print(f"Generated {len(pairs)} context-target training pairs.")
    
    if len(pairs) == 0:
        print("Error: No training pairs generated. Please verify text size and context window size.")
        return
        
    # 4. Create Dataset and DataLoader
    dataset = CBOWDataset(pairs, word_to_ix)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
    
    # 5. Initialize Model, Loss Function, and Optimizer
    model = CBOWModel(vocab_size=vocab_size, embedding_dim=args.embed_dim).to(device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    
    # 6. Training Loop
    print("\nStarting training...")
    model.train()
    for epoch in range(1, args.epochs + 1):
        total_loss = 0.0
        for context_batch, target_batch in dataloader:
            # Move data to the selected device
            context_batch = context_batch.to(device)
            target_batch = target_batch.to(device)
            
            # Step 1: Zero the gradients
            optimizer.zero_grad()
            
            # Step 2: Forward pass
            logits = model(context_batch)
            
            # Step 3: Compute loss
            loss = loss_function(logits, target_batch)
            
            # Step 4: Backward pass & optimize
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item() * len(target_batch)
            
        epoch_loss = total_loss / len(dataset)
        if epoch == 1 or epoch % 10 == 0 or epoch == args.epochs:
            print(f"Epoch {epoch:03d}/{args.epochs:03d} - Loss: {epoch_loss:.4f}")
            
    print("Training completed.\n")
    
    # 7. Save Model Weights and Vocabulary
    os.makedirs(args.model_dir, exist_ok=True)
    
    # Save PyTorch model state dict
    model_path = os.path.join(args.model_dir, "cbow_model.pt")
    torch.save(model.state_dict(), model_path)
    print(f"Model state dict saved to {model_path}")
    
    # Save vocabulary dictionary and configurations for inference
    metadata = {
        "word_to_ix": word_to_ix,
        "ix_to_word": {int(k): v for k, v in ix_to_word.items()}, # Ensure integer keys are saved nicely
        "window_size": args.window_size,
        "embed_dim": args.embed_dim,
        "vocab_size": vocab_size
    }
    metadata_path = os.path.join(args.model_dir, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"Vocabulary and configuration metadata saved to {metadata_path}")

if __name__ == "__main__":
    main()
