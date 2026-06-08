"""Download Steam games dataset from Kaggle."""

import subprocess
import sys
import zipfile
from pathlib import Path

DATASET = "fronkongames/steam-games-dataset"
DATA_DIR = Path(__file__).parent


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading Kaggle dataset: {DATASET}")
    print("Requires ~/.kaggle/kaggle.json with valid API credentials.")

    result = subprocess.run(
        ["kaggle", "datasets", "download", "-d", DATASET, "-p", str(DATA_DIR)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)

    zip_path = DATA_DIR / "steam-games-dataset.zip"
    if zip_path.exists():
        print(f"Extracting {zip_path.name} …")
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(DATA_DIR)
        zip_path.unlink()
        print("Extracted.")

    print("Files ready in data/:")
    for p in sorted(DATA_DIR.glob("*.csv")):
        size_mb = p.stat().st_size / 1_048_576
        print(f"  {p.name}  ({size_mb:.0f} MB)")


if __name__ == "__main__":
    main()
