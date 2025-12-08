"""
Setup script for downloading the LinkedIn job postings database.
Downloads the pre-built SQLite database from GitHub Releases.

Usage:
    python scripts/setup_data.py
"""

import os
import sys
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "linkedin_jobs.db"

# GitHub Release URL for the database
DB_URL = "https://github.com/cole-nielson/job-market-insights/releases/download/v1.0.0/linkedin_jobs.db"


def download_database():
    """Download the database from GitHub Releases."""
    print(f"Downloading database from GitHub...")
    print(f"URL: {DB_URL}")
    print(f"Destination: {DB_PATH}")

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # Download with progress indicator
        def report_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100, downloaded * 100 / total_size)
                mb_downloaded = downloaded / (1024 * 1024)
                mb_total = total_size / (1024 * 1024)
                print(f"\rProgress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end="", flush=True)

        urllib.request.urlretrieve(DB_URL, DB_PATH, reporthook=report_progress)
        print("\nDownload complete!")
        return True

    except Exception as e:
        print(f"\nERROR downloading database: {e}")
        return False


def main():
    """Main setup function."""
    print("=" * 50)
    print("LinkedIn Job Postings - Database Setup")
    print("=" * 50)

    # Check if database already exists
    if DB_PATH.exists():
        size_mb = DB_PATH.stat().st_size / (1024 * 1024)
        print(f"\nDatabase already exists: {DB_PATH}")
        print(f"Size: {size_mb:.1f} MB")
        print("Skipping download.")
        return 0

    # Download database
    if not download_database():
        return 1

    # Verify download
    if DB_PATH.exists():
        size_mb = DB_PATH.stat().st_size / (1024 * 1024)
        print(f"\nDatabase ready: {DB_PATH}")
        print(f"Size: {size_mb:.1f} MB")
    else:
        print("ERROR: Database file not found after download")
        return 1

    print("\n" + "=" * 50)
    print("Setup complete!")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
