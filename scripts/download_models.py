#!/usr/bin/env python3
"""
Script to download YOLO models.
"""

import os
import urllib.request
from pathlib import Path

def download_yolo_model():
    """Download YOLOv8 nano model if not exists."""
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "yolov8n.pt"
    
    if model_path.exists():
        print(f"Model already exists at {model_path}")
        return
    
    # YOLOv8n URL (example, replace with actual)
    url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
    
    print(f"Downloading YOLOv8n model to {model_path}...")
    try:
        urllib.request.urlretrieve(url, model_path)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download model: {e}")

if __name__ == "__main__":
    download_yolo_model()