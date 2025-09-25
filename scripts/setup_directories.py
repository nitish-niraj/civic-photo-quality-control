#!/usr/bin/env python3
"""
Script to set up project directories.
"""

import os
from pathlib import Path

def setup_directories():
    """Create all necessary directories."""
    dirs = [
        "storage/temp",
        "storage/processed", 
        "storage/rejected",
        "tests/sample_images/blurry",
        "tests/sample_images/dark",
        "tests/sample_images/low_res",
        "tests/sample_images/good",
        "docs"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")

if __name__ == "__main__":
    setup_directories()