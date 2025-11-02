"""
Civic Photo Quality Control API - Configuration
================================================
Centralized configuration for the application with mobile-optimized validation rules.

Key Features:
- Weighted scoring system with 65% pass threshold
- Mobile-friendly validation thresholds
- Environment-based configuration (development/production)
- Comprehensive validation rules for 5 quality checks

Author: Civic Quality Control Team
Version: 2.0
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
load_dotenv()


class Config:
    """Base configuration class with default settings."""
    
    # ===================================================================
    # FLASK CORE CONFIGURATION
    # ===================================================================
    
    # Secret key for session management and CSRF protection
    # IMPORTANT: Change this in production!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Maximum file upload size (16MB default, supports large mobile photos)
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    
    # ===================================================================
    # STORAGE CONFIGURATION
    # ===================================================================
    
    # Directory paths for image storage
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'storage/temp')  # Temporary upload storage
    PROCESSED_FOLDER = 'storage/processed'  # Accepted images (passed validation)
    REJECTED_FOLDER = 'storage/rejected'  # Rejected images (failed validation)
    
    # ===================================================================
    # BASIC IMAGE QUALITY THRESHOLDS (Mobile-Optimized)
    # ===================================================================
    
    # Blur detection threshold (Laplacian variance)
    # Lower = more lenient, Higher = stricter
    # Mobile-optimized: 100 (down from 150)
    BLUR_THRESHOLD = float(os.environ.get('BLUR_THRESHOLD', 100.0))
    
    # Brightness range (pixel intensity: 0-255)
    # Wider range accommodates varied mobile lighting conditions
    # Mobile-optimized: 50-220 (expanded from 90-180)
    MIN_BRIGHTNESS = int(os.environ.get('MIN_BRIGHTNESS', 50))
    MAX_BRIGHTNESS = int(os.environ.get('MAX_BRIGHTNESS', 220))
    
    # Resolution requirements (pixels)
    # Mobile-optimized: 800x600 (down from 1024x1024)
    # Supports landscape and portrait orientations
    MIN_RESOLUTION_WIDTH = int(os.environ.get('MIN_RESOLUTION_WIDTH', 800))
    MIN_RESOLUTION_HEIGHT = int(os.environ.get('MIN_RESOLUTION_HEIGHT', 600))
    
    # ===================================================================
    # COMPREHENSIVE VALIDATION RULES (Mobile-Optimized v2.0)
    # ===================================================================
    # These rules implement a weighted scoring system with partial credit
    # Pass threshold: 65% overall score required
    # Acceptance rate target: 35-40% for quality mobile photos
    # ===================================================================
    
    VALIDATION_RULES = {
        # -----------------------------------------------------------
        # 1. BLUR DETECTION (25% weight in overall score)
        # -----------------------------------------------------------
        # Uses Laplacian variance to measure image sharpness
        # Higher variance = sharper image
        "blur": {
            "metric": "variance_of_laplacian",  # Algorithm used
            "min_score": 100,  # Minimum acceptable score (mobile-optimized: down from 150)
            "levels": {
                "excellent": 300,  # Very sharp, professional quality
                "acceptable": 100,  # Adequate sharpness for documentation
                "poor": 0  # Blurry, unacceptable
            }
        },
        
        # -----------------------------------------------------------
        # 2. BRIGHTNESS VALIDATION (20% weight in overall score)
        # -----------------------------------------------------------
        # Analyzes pixel intensity distribution (0-255 scale)
        # Ensures image is neither too dark nor too bright
        "brightness": {
            "metric": "mean_pixel_intensity",  # Average brightness measurement
            "range": [50, 220],  # Acceptable range (mobile-optimized: 50-220 vs 90-180)
            "quality_score_min": 60  # Minimum quality percentage required (down from 70%)
        },
        
        # -----------------------------------------------------------
        # 3. RESOLUTION CHECK (25% weight in overall score)
        # -----------------------------------------------------------
        # Verifies image has sufficient resolution for documentation
        # Accepts both landscape and portrait orientations
        "resolution": {
            "min_width": 800,  # Minimum width pixels (down from 1024)
            "min_height": 600,  # Minimum height pixels (down from 1024)
            "min_megapixels": 0.5,  # Minimum total pixels (down from 1MP)
            "recommended_megapixels": 2  # Recommended for optimal quality
        },
        
        # -----------------------------------------------------------
        # 4. EXPOSURE ANALYSIS (15% weight in overall score)
        # -----------------------------------------------------------
        # Checks dynamic range and pixel clipping
        # Ensures image has good contrast and detail
        "exposure": {
            "metric": "dynamic_range",  # Difference between darkest and brightest pixels
            "min_score": 100,  # Minimum dynamic range (down from 150)
            "acceptable_range": [80, 150],  # Acceptable dynamic range bounds
            "check_clipping": {
                "max_percentage": 2  # Maximum % of clipped (pure white/black) pixels (up from 1%)
            }
        },
        
        # -----------------------------------------------------------
        # 5. METADATA EXTRACTION (15% weight in overall score)
        # -----------------------------------------------------------
        # Extracts and validates EXIF data from image
        # Many mobile photos lack complete metadata, so requirement is minimal
        "metadata": {
            "required_fields": [
                "timestamp",  # When photo was taken
                "camera_make_model",  # Device information
                "orientation",  # Image orientation
                "iso",  # Camera ISO setting
                "shutter_speed",  # Exposure time
                "aperture"  # Lens aperture
            ],
            "min_completeness_percentage": 15  # Only 15% required (down from 30%)
            # Allows acceptance of photos with minimal metadata
        }
    }
    
    # ===================================================================
    # FILE TYPE CONFIGURATION
    # ===================================================================
    
    # Allowed image file extensions for upload
    # Supports common mobile photo formats including HEIC (iOS)
    ALLOWED_EXTENSIONS = set(os.environ.get('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,bmp,tiff').split(','))


# ===================================================================
# ENVIRONMENT-SPECIFIC CONFIGURATIONS
# ===================================================================

class DevelopmentConfig(Config):
    """Development environment configuration with debug mode enabled."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration with debug mode disabled."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration with deterministic behaviour."""
    DEBUG = False
    TESTING = True
    # Use in-memory friendly limits to keep tests fast
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 8 * 1024 * 1024))


# Configuration dictionary for easy access
# Usage: config[os.getenv('FLASK_ENV', 'default')]
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig  # Default to development if not specified
}