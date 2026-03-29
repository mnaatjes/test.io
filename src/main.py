import os
import sys
from pathlib import Path

# Add src to the path so we can import 'tio'
sys.path.append(str(Path(__file__).parent))

from tio.cli import run_cli

def main():
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
