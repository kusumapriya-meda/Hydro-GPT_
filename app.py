import sys
from pathlib import Path

# Ensure root and src paths are in sys.path
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

for p in (str(ROOT), str(SRC)):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from src.app import main

if __name__ == "__main__":
    main()
