#!/usr/bin/env python3
"""
Production startup script for Civic Quality Control App
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app
from config import Config

def setup_logging():
    """Setup production logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/app.log') if os.path.exists('logs') else logging.StreamHandler()
        ]
    )

def ensure_directories():
    """Ensure all required directories exist."""
    directories = [
        'storage/temp',
        'storage/processed',
        'storage/rejected',
        'models',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
def download_models():
    """Download required models if not present."""
    model_path = Path('models/yolov8n.pt')
    if not model_path.exists():
        try:
            from ultralytics import YOLO
            print("Downloading YOLO model...")
            model = YOLO('yolov8n.pt')
            print("Model download completed.")
        except Exception as e:
            print(f"Warning: Failed to download YOLO model: {e}")

def create_production_app():
    """Create and configure production Flask app."""
    setup_logging()
    ensure_directories()
    download_models()
    
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    
    # Create Flask app with production config
    app = create_app('production')
    
    # Configure for production
    app.config.update({
        'MAX_CONTENT_LENGTH': 32 * 1024 * 1024,  # 32MB for mobile photos
        'UPLOAD_FOLDER': 'storage/temp',
        'PROCESSED_FOLDER': 'storage/processed',
        'REJECTED_FOLDER': 'storage/rejected',
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'production-secret-key-change-me'),
        'BLUR_THRESHOLD': 80.0,  # More lenient for mobile
        'MIN_BRIGHTNESS': 25,
        'MAX_BRIGHTNESS': 235,
        'MIN_RESOLUTION_WIDTH': 720,
        'MIN_RESOLUTION_HEIGHT': 480,
    })
    
    logging.info("Civic Quality Control App started in production mode")
    logging.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logging.info(f"Max file size: {app.config['MAX_CONTENT_LENGTH']} bytes")
    
    return app

# Create the app instance for WSGI servers (gunicorn, uwsgi, etc.)
app = create_production_app()

if __name__ == '__main__':
    # Development server (not recommended for production)
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        debug=False
    )