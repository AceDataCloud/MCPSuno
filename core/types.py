"""Type definitions for Suno MCP server."""

from typing import Literal

# Suno model versions
SunoModel = Literal[
    "chirp-v3",
    "chirp-v3-5",
    "chirp-v4",
    "chirp-v4-5",
    "chirp-v4-5-plus",
    "chirp-v5",
]

# Vocal gender options (v4.5+ only)
VocalGender = Literal["", "f", "m"]

# Default model
DEFAULT_MODEL: SunoModel = "chirp-v4-5"
