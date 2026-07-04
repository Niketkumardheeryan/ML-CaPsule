import logging
import sys
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ml_capsule.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class MLCapsuleError(Exception):
    """Base exception class for ML-CaPsule"""
    pass

class DataValidationError(MLCapsuleError):
    """Raised when data validation fails"""
    pass

class ModelError(MLCapsuleError):
    """Raised when model operations fail"""
    pass

def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MLCapsuleError as e:
            logging.error(f"ML-CaPsule error in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise MLCapsuleError(f"Function {func.__name__} failed: {str(e)}")
    return wrapper 