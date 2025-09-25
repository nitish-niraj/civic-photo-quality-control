import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # Storage Configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'storage/temp')
    PROCESSED_FOLDER = 'storage/processed'
    REJECTED_FOLDER = 'storage/rejected'
    
    # Image Quality Thresholds - Updated validation rules (more lenient for mobile)
    BLUR_THRESHOLD = float(os.environ.get('BLUR_THRESHOLD', 100.0))  # Reduced for mobile photos
    MIN_BRIGHTNESS = int(os.environ.get('MIN_BRIGHTNESS', 50))  # More lenient range
    MAX_BRIGHTNESS = int(os.environ.get('MAX_BRIGHTNESS', 220))  # More lenient range
    MIN_RESOLUTION_WIDTH = int(os.environ.get('MIN_RESOLUTION_WIDTH', 800))  # Reduced for mobile
    MIN_RESOLUTION_HEIGHT = int(os.environ.get('MIN_RESOLUTION_HEIGHT', 600))  # Reduced for mobile
    
    # Advanced validation rules
    VALIDATION_RULES = {
        "blur": {
            "metric": "variance_of_laplacian",
            "min_score": 100,  # Reduced from 150 - more lenient for mobile photos
            "levels": {
                "excellent": 300,
                "acceptable": 100,  # Reduced from 150
                "poor": 0
            }
        },
        "brightness": {
            "metric": "mean_pixel_intensity",
            "range": [50, 220],  # Expanded from [90, 180] - more realistic for mobile
            "quality_score_min": 60  # Reduced from 70
        },
        "resolution": {
            "min_width": 800,  # Reduced from 1024 - accept smaller mobile photos
            "min_height": 600,  # Reduced from 1024 - accept landscape orientation
            "min_megapixels": 0.5,  # Reduced from 1 - more realistic for mobile
            "recommended_megapixels": 2
        },
        "exposure": {
            "metric": "dynamic_range",
            "min_score": 100,  # Reduced from 150 - more lenient
            "acceptable_range": [80, 150],  # Expanded lower bound
            "check_clipping": {
                "max_percentage": 2  # Increased from 1% - more tolerant
            }
        },
        "metadata": {
            "required_fields": [
                "timestamp",
                "camera_make_model",
                "orientation",
                "iso",
                "shutter_speed",
                "aperture"
            ],
            "min_completeness_percentage": 15  # Reduced from 30 - many mobile photos lack metadata
        }
    }
    
    # Model Configuration
    YOLO_MODEL_PATH = os.environ.get('YOLO_MODEL_PATH', 'models/yolov8n.pt')
    
    # File Type Configuration
    ALLOWED_EXTENSIONS = set(os.environ.get('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,bmp,tiff').split(','))
    
    # Geographic Boundaries (example for a city)
    CITY_BOUNDARIES = {
        'min_lat': 40.4774,
        'max_lat': 40.9176,
        'min_lon': -74.2591,
        'max_lon': -73.7004
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}