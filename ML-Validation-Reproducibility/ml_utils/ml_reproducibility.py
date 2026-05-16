import random
import numpy as np

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def get_environment_info():
    return {
        "numpy_version": np.__version__,
        "random_seed": 42
    }