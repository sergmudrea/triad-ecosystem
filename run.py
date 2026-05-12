#!/usr/bin/env python3
# run.py

"""Main entry point for TRIAD Ecosystem."""

import sys
import asyncio
from src.orchestrator import main

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
