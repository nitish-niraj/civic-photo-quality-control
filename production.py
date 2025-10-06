#!/usr/bin/env python3
"""
Civic Photo Quality Control API - Production WSGI Application
==============================================================
Production-ready entry point for deployment with Gunicorn or similar WSGI servers.

Usage:
    gunicorn --bind 0.0.0.0:8000 --workers 4 production:app

Features:
- Automatic directory structure setup
- Production logging configuration
- Model initialization
- Environment validation

Author: Civic Quality Control Team
Version: 2.0
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to Python path for proper module imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app
from config import Config


def setup_logging():
    """
    Configure production-grade logging.
    
    Logs are written to both console (stdout) and log file (logs/app.log).
    Log format includes timestamp, logger name, level, and message.
    """
    logging.basicConfig(
        level=logging.INFO,  # INFO level for production (change to DEBUG for troubleshooting)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),  # Console output
            # File output (only if logs directory exists)
            logging.FileHandler('logs/app.log') if os.path.exists('logs') else logging.StreamHandler()
        ]
    )


def ensure_directories():
    """
    Create all required directory structures if they don't exist.
    
    Directories created:
    - storage/temp: Temporary upload storage
    - storage/processed: Accepted/validated images
    - storage/rejected: Rejected images for analysis
    - models: Machine learning model storage
    - logs: Application log files
    """
    directories = [
        'storage/temp',
        'storage/processed',
        'storage/rejected',
        'models',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logging.info(f"Ensured directory exists: {directory}")

        
def download_models():
    """
    Download YOLOv8 object detection model if not already present.
    
    The model is used for optional civic object detection feature.
    Downloads from Ultralytics repository on first run.
    """
    model_path = Path('models/yolov8n.pt')
    if not model_path.exists():
        try:
            from ultralytics import YOLO
            logging.info("YOLO model not found. Downloading...")
            model = YOLO('yolov8n.pt')  # Downloads YOLOv8n (nano) model
            logging.info("YOLO model download completed successfully.")
        except Exception as e:
            logging.warning(f"Failed to download YOLO model: {e}")
            logging.info("Object detection feature will be disabled.")


def create_production_app():
    """
    Create and configure the production Flask application.
    
    Steps performed:
    1. Setup logging configuration
    2. Ensure directory structure exists
    3. Download required models (if missing)
    4. Create Flask app with production configuration
    5. Validate critical configuration settings
    
    Returns:
        Flask application instance configured for production
    """
    # Step 1: Configure logging
    setup_logging()
    logging.info("=" * 60)
    logging.info("Civic Photo Quality Control API - Production Startup")
    logging.info("=" * 60)
    
    # Step 2: Setup directories
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