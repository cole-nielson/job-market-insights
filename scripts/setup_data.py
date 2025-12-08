"""
Setup script for downloading and preparing the LinkedIn job postings database.
Used during deployment to fetch data from Kaggle.

Requirements:
- KAGGLE_USERNAME and KAGGLE_KEY environment variables must be set
- Or ~/.kaggle/kaggle.json must exist

Usage:
    python scripts/setup_data.py
"""

import os
import sys
import subprocess
import zipfile
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "linkedin_jobs.db"
KAGGLE_DATASET = "arshkon/linkedin-job-postings"


def check_kaggle_auth():
    """Verify Kaggle authentication is available."""
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"

    if kaggle_json.exists():
        return True

    if os.getenv("KAGGLE_USERNAME") and os.getenv("KAGGLE_KEY"):
        return True

    print("ERROR: Kaggle authentication not found.")
    print("Either set KAGGLE_USERNAME and KAGGLE_KEY environment variables,")
    print("or create ~/.kaggle/kaggle.json with your credentials.")
    return False


def download_dataset():
    """Download the LinkedIn job postings dataset from Kaggle."""
    print(f"Downloading dataset from Kaggle: {KAGGLE_DATASET}")

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Download using kaggle CLI
    result = subprocess.run(
        ["kaggle", "datasets", "download", "-d", KAGGLE_DATASET, "-p", str(DATA_DIR)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"ERROR downloading dataset: {result.stderr}")
        return False

    print("Download complete.")
    return True


def extract_dataset():
    """Extract the downloaded zip file."""
    zip_path = DATA_DIR / "linkedin-job-postings.zip"

    if not zip_path.exists():
        print(f"ERROR: Zip file not found at {zip_path}")
        return False

    print("Extracting dataset...")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)

    # Remove zip file to save space
    zip_path.unlink()
    print("Extraction complete.")
    return True


def create_database():
    """Run the database creation script."""
    print("Creating SQLite database...")

    create_script = Path(__file__).parent / "create_database.py"

    result = subprocess.run(
        [sys.executable, str(create_script)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"ERROR creating database: {result.stderr}")
        print(result.stdout)
        return False

    print(result.stdout)
    return True


def main():
    """Main setup function."""
    print("=" * 50)
    print("LinkedIn Job Postings - Data Setup")
    print("=" * 50)

    # Check if database already exists
    if DB_PATH.exists():
        size_mb = DB_PATH.stat().st_size / (1024 * 1024)
        print(f"\nDatabase already exists: {DB_PATH}")
        print(f"Size: {size_mb:.1f} MB")
        print("Skipping setup.")
        return 0

    # Check Kaggle auth
    if not check_kaggle_auth():
        return 1

    # Download dataset
    if not download_dataset():
        return 1

    # Extract dataset
    if not extract_dataset():
        return 1

    # Create database
    if not create_database():
        return 1

    print("\n" + "=" * 50)
    print("Setup complete!")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
