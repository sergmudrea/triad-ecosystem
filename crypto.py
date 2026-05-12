# src/utils/crypto.py

"""Encryption utilities for Meta-Memory."""

import os
from cryptography.fernet import Fernet


def generate_key() -> str:
    """Generate a new Fernet encryption key."""
    return Fernet.generate_key().decode()


def encrypt(data: bytes, key: str) -> bytes:
    """Encrypt data using Fernet symmetric encryption."""
    f = Fernet(key.encode() if isinstance(key, str) else key)
    return f.encrypt(data)


def decrypt(data: bytes, key: str) -> bytes:
    """Decrypt data using Fernet symmetric encryption."""
    f = Fernet(key.encode() if isinstance(key, str) else key)
    return f.decrypt(data)
