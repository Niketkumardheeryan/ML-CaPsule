import os


def _load_dotenv() -> None:
    try:
        from dotenv import find_dotenv, load_dotenv
    except ImportError:
        return

    load_dotenv(find_dotenv())


_load_dotenv()
def load_credential(key_name: str) -> str:
    """
    Safely retrieves a credential from environment variables or Google Colab userdata.
    Raises a descriptive KeyError if the credential is missing.
    """

    value = os.environ.get(key_name)
    if value:
        return value
    try:
        from google.colab import userdata
        value = userdata.get(key_name)
        if value:
            return value
    except ImportError:
        pass

    
    raise KeyError(
        f"🚨 Missing credential: '{key_name}'. "
        f"Please add it to your local .env file or your environment variables."
    )