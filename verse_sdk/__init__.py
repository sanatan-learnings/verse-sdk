"""
Verse Content SDK

A Python SDK for generating rich multimedia content for verse-based texts.
"""

__version__ = "0.26.1"

# Note: Import only what exists to avoid circular imports
# from .embeddings import EmbeddingGenerator
# from .audio import AudioGenerator
from .utils import file_utils, yaml_parser

__all__ = [
    # "EmbeddingGenerator",
    # "AudioGenerator",
    "yaml_parser",
    "file_utils",
]
