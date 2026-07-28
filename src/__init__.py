"""HYDRO GPT package and Streamlit deployment entry point."""
import sys
from pathlib import Path

# Add project root and src directory to sys.path
ROOT = Path(__file__).resolve().parent.parent
SRC = Path(__file__).resolve().parent

for p in (str(ROOT), str(SRC)):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    from src.app import main
except ImportError:
    from app import main

# Automatically invoke main when Streamlit executes this module
main()
