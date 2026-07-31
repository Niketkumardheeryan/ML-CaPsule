"""Voice & CLI driven system virtual assistant.

The package is intentionally split into small, independently testable modules:

``config``        runtime settings resolved from environment variables
``speech``        text-to-speech and speech-to-text with graceful fallbacks
``knowledge``     Wikipedia / Google / YouTube lookups
``live_data``     weather and news headlines from keyless public endpoints
``system_tools``  clipboard, screenshots, battery telemetry, power controls
``commands``      regex based intent router
``core``          the assistant object that wires everything together
``cli``           argument parsing and the interactive loops
"""

from .config import AssistantConfig, load_config
from .core import VirtualAssistant

__all__ = ["AssistantConfig", "load_config", "VirtualAssistant", "__version__"]

__version__ = "1.0.0"
