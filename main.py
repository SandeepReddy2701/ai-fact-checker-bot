from __future__ import annotations
import sys
from src.ui.cli import main

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python main.py <claim to fact-check>")
        sys.exit(1)
    main()
