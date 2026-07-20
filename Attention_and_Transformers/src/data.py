"""
Data Loading Utilities

Load datasets from torch.hub and kagglehub for attention/transformer training.
"""

import torch
import torchvision
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, List
import os

# Set data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


class DatasetLoader:
    """Unified interface for loading datasets."""
    
    @staticmethod
    def load_mnist(
        split: str = "train",
        samples: Optional[int] = None,
        batch_size: int = 32
    ) -> DataLoader:
        """
        Load MNIST dataset.
        
        Args:
            split: 'train' or 'test'
            samples: Number of samples to load (None = all)
            batch_size: Batch size for DataLoader
        
        Returns:
            DataLoader
        """
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        is_train = split == "train"
        dataset = datasets.MNIST(
            root=DATA_DIR / "mnist",
            train=is_train,
            download=True,
            transform=transform
        )
        
        if samples:
            indices = np.random.choice(len(dataset), samples, replace=False)
            dataset = torch.utils.data.Subset(dataset, indices)
        
        return DataLoader(dataset, batch_size=batch_size, shuffle=is_train)
    
    @staticmethod
    def load_fashion_mnist(
        split: str = "train",
        samples: Optional[int] = None,
        batch_size: int = 32
    ) -> DataLoader:
        """
        Load Fashion-MNIST dataset.
        
        Args:
            split: 'train' or 'test'
            samples: Number of samples to load
            batch_size: Batch size
        
        Returns:
            DataLoader
        """
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.2859,), (0.3530,))
        ])
        
        is_train = split == "train"
        dataset = datasets.FashionMNIST(
            root=DATA_DIR / "fashion_mnist",
            train=is_train,
            download=True,
            transform=transform
        )
        
        if samples:
            indices = np.random.choice(len(dataset), samples, replace=False)
            dataset = torch.utils.data.Subset(dataset, indices)
        
        return DataLoader(dataset, batch_size=batch_size, shuffle=is_train)
    
    @staticmethod
    def load_cifar10(
        split: str = "train",
        samples: Optional[int] = None,
        batch_size: int = 32
    ) -> DataLoader:
        """
        Load CIFAR-10 dataset.
        
        Args:
            split: 'train' or 'test'
            samples: Number of samples to load
            batch_size: Batch size
        
        Returns:
            DataLoader
        """
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                (0.4914, 0.4822, 0.4465),
                (0.2023, 0.1994, 0.2010)
            )
        ])
        
        is_train = split == "train"
        dataset = datasets.CIFAR10(
            root=DATA_DIR / "cifar10",
            train=is_train,
            download=True,
            transform=transform
        )
        
        if samples:
            indices = np.random.choice(len(dataset), samples, replace=False)
            dataset = torch.utils.data.Subset(dataset, indices)
        
        return DataLoader(dataset, batch_size=batch_size, shuffle=is_train)
    
    @staticmethod
    def load_synthetic_sequence_data(
        seq_len: int = 50,
        vocab_size: int = 100,
        num_samples: int = 1000,
        batch_size: int = 32
    ) -> DataLoader:
        """
        Create synthetic sequence data for attention mechanism training.
        
        Args:
            seq_len: Sequence length
            vocab_size: Vocabulary size
            num_samples: Number of samples
            batch_size: Batch size
        
        Returns:
            DataLoader
        """
        # Random sequences
        sequences = torch.randint(0, vocab_size, (num_samples, seq_len))
        targets = torch.randint(0, vocab_size, (num_samples, 1))
        
        dataset = TensorDataset(sequences, targets)
        return DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    @staticmethod
    def load_copy_task(
        seq_len: int = 10,
        num_samples: int = 10000,
        batch_size: int = 32
    ) -> Tuple[DataLoader, DataLoader]:
        """
        Create copy task dataset (attention benchmark).
        
        Task: Model must copy input sequence to output.
        
        Args:
            seq_len: Sequence length
            num_samples: Number of samples
            batch_size: Batch size
        
        Returns:
            train_loader, test_loader
        """
        # Create sequences
        vocab_size = 10
        
        def create_copy_data(num_samples):
            inputs = torch.randint(1, vocab_size, (num_samples, seq_len))
            targets = inputs.clone()
            return TensorDataset(inputs, targets)
        
        train_data = create_copy_data(int(0.8 * num_samples))
        test_data = create_copy_data(int(0.2 * num_samples))
        
        train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)
        
        return train_loader, test_loader
    
    @staticmethod
    def load_addition_task(
        seq_len: int = 10,
        num_samples: int = 10000,
        batch_size: int = 32
    ) -> Tuple[DataLoader, DataLoader]:
        """
        Create addition task dataset (attention benchmark).
        
        Task: Model must add two numbers at specific positions.
        
        Args:
            seq_len: Sequence length
            num_samples: Number of samples
            batch_size: Batch size
        
        Returns:
            train_loader, test_loader
        """
        def create_addition_data(num_samples):
            inputs = torch.zeros(num_samples, seq_len)
            targets = torch.zeros(num_samples, 1)
            
            for i in range(num_samples):
                # Random positions for two numbers
                pos1, pos2 = np.random.choice(seq_len, 2, replace=False)
                num1 = np.random.randint(1, 10)
                num2 = np.random.randint(1, 10)
                
                inputs[i, pos1] = num1
                inputs[i, pos2] = num2
                targets[i] = num1 + num2
            
            return TensorDataset(inputs, targets)
        
        train_data = create_addition_data(int(0.8 * num_samples))
        test_data = create_addition_data(int(0.2 * num_samples))
        
        train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)
        
        return train_loader, test_loader


# Convenience functions
def get_mnist(split="train", samples=None):
    """Load MNIST."""
    return DatasetLoader.load_mnist(split, samples)


def get_fashion_mnist(split="train", samples=None):
    """Load Fashion-MNIST."""
    return DatasetLoader.load_fashion_mnist(split, samples)


def get_cifar10(split="train", samples=None):
    """Load CIFAR-10."""
    return DatasetLoader.load_cifar10(split, samples)


def get_synthetic_data(**kwargs):
    """Load synthetic sequence data."""
    return DatasetLoader.load_synthetic_sequence_data(**kwargs)


def get_copy_task(**kwargs):
    """Load copy task."""
    return DatasetLoader.load_copy_task(**kwargs)


def get_addition_task(**kwargs):
    """Load addition task."""
    return DatasetLoader.load_addition_task(**kwargs)


if __name__ == "__main__":
    # Test data loading
    print("Testing data loaders...")
    
    # MNIST
    print("\n1. Loading MNIST...")
    train_loader = get_mnist("train", samples=1000)
    print(f"   ✓ MNIST train loader: {len(train_loader)} batches")
    
    for batch_idx, (images, labels) in enumerate(train_loader):
        print(f"   Batch {batch_idx}: images {images.shape}, labels {labels.shape}")
        if batch_idx == 0:
            break
    
    # Fashion-MNIST
    print("\n2. Loading Fashion-MNIST...")
    train_loader = get_fashion_mnist("train", samples=1000)
    print(f"   ✓ Fashion-MNIST train loader: {len(train_loader)} batches")
    
    # Synthetic
    print("\n3. Creating Synthetic Data...")
    train_loader = get_synthetic_data(num_samples=1000)
    print(f"   ✓ Synthetic data: {len(train_loader)} batches")
    
    # Copy task
    print("\n4. Creating Copy Task...")
    train_loader, test_loader = get_copy_task(num_samples=5000)
    print(f"   ✓ Copy task: {len(train_loader)} train, {len(test_loader)} test")
    
    # Addition task
    print("\n5. Creating Addition Task...")
    train_loader, test_loader = get_addition_task(num_samples=5000)
    print(f"   ✓ Addition task: {len(train_loader)} train, {len(test_loader)} test")
    
    print("\n✅ All data loaders working!")
