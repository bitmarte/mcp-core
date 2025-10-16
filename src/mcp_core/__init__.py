# mcp_core/__init__.py
from .core import CoreAPI  # spostiamo la definizione CoreAPI in core.py
from .loader import load_tools

# Istanza globale già pronta per i tool
from .core import core_api

__all__ = ["core_api", "load_tools"]
