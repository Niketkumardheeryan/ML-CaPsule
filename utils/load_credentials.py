"""
ML-CaPsule Centralized Credential Loading Utility
==================================================
This module provides standardized, secure access to environment variables,
secrets, and API keys across notebooks and scripts in the ML-CaPsule repository.

Usage in notebooks / scripts:
-----------------------------
    from utils.load_credentials import get_credential

    api_key = get_credential("GEMINI_API_KEY", required=True)
"""

import os
import sys
from typing import Optional, Dict, Union, List

# Attempt to load .env file automatically using python-dotenv if installed
try:
    from dotenv import load_dotenv, find_dotenv
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        # Fallback to root directory .env relative to this file
        root_dotenv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        if os.path.exists(root_dotenv):
            load_dotenv(root_dotenv)
except ImportError:
    # python-dotenv is optional; fallback gracefully to os.environ
    pass


def get_credential(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Retrieve an API key or credential by environment variable name.

    Search order:
    1. Operating System Environment (`os.environ`) / `.env` file
    2. Google Colab User Data (`google.colab.userdata`) if running in Colab
    3. Provided `default` fallback value

    Parameters
    ----------
    key : str
        The name of the environment variable (e.g. 'OPENAI_API_KEY', 'ROBOFLOW_API_KEY').
    default : str, optional
        Default value to return if the key is not set and required is False.
    required : bool, optional
        If True, raises a ValueError when the key is missing instead of returning None.

    Returns
    -------
    str or None
        The requested credential value if present.

    Raises
    ------
    ValueError
        If required is True and the key is not found in environment, Colab secrets, or default.
    """
    val = os.environ.get(key)
    if val:
        return val

    # Check Google Colab Secrets panel if running in Colab environment
    if "google.colab" in sys.modules or os.environ.get("COLAB_RELEASE_TAG"):
        try:
            from google.colab import userdata  # type: ignore
            colab_val = userdata.get(key)
            if colab_val:
                return colab_val
        except Exception:
            pass

    if default is not None:
        return default

    if required:
        raise ValueError(
            f"\n[CRITICAL SECURITY ERROR] Required environment variable '{key}' is missing!\n"
            f"Please set '{key}' in your environment or inside a root '.env' file.\n"
            f"Refer to '.env.example' in the repository root for required environment variable names.\n"
            f"Do NOT hardcode your API keys directly into source code or notebooks."
        )

    return None


def load_credentials(keys: List[str], required: bool = True) -> Dict[str, Optional[str]]:
    """
    Load multiple credentials at once.

    Parameters
    ----------
    keys : List[str]
        List of environment variable names to load.
    required : bool, optional
        If True, raises an error if any of the keys are missing.

    Returns
    -------
    Dict[str, Optional[str]]
        Dictionary mapping each key name to its loaded value.
    """
    credentials = {}
    for key in keys:
        credentials[key] = get_credential(key, required=required)
    return credentials
