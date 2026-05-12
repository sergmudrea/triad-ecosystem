# src/__main__.py

"""Allow running as module: python -m triad"""

import sys
from src.orchestrator import main

if __name__ == "__main__":
    sys.exit(main())
