# src/utils/hashing.py

"""Hashing utilities for deduplication."""

import hashlib
import json
from typing import Any


def calculate_checksum(data: Any) -> str:
    """
    Calculate SHA-256 checksum of data for deduplication.

    Args:
        data: Any JSON-serializable data structure

    Returns:
        Hexadecimal SHA-256 hash string
    """
    serialized = json.dumps(data, default=str, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()
