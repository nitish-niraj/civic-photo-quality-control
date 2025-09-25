import cv2
import numpy as np
from typing import Tuple

class BlurDetector:
    """Detects image blur using Laplacian variance method."""
    
    @staticmethod
    def calculate_blur_score(image_path: str, threshold: float = 100.0) -> Tuple[float, bool]:
        """
        Calculate blur score using Laplacian variance.
        
        Args:
            image_path: Path to the image file
            threshold: Blur threshold (lower = more blurry)
            
        Returns:
            Tuple of (blur_score, is_blurry)
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate Laplacian variance
            blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            is_blurry = blur_score < threshold
            
            return blur_score, is_blurry
            
        except Exception as e:
            raise Exception(f"Blur detection failed: {str(e)}")
    
    @staticmethod
    def get_blur_details(blur_score: float, threshold: float) -> dict:
        """Get detailed blur analysis using new validation rules."""
        # New validation levels
        if blur_score >= 300:
            quality = "Excellent"
            quality_level = "excellent"
        elif blur_score >= 150:
            quality = "Acceptable"
            quality_level = "acceptable"
        else:
            quality = "Poor"
            quality_level = "poor"
            
        return {
            "blur_score": round(blur_score, 2),
            "threshold": threshold,
            "is_blurry": blur_score < threshold,
            "quality": quality,
            "quality_level": quality_level,
            "confidence": min(blur_score / threshold, 2.0),
            "meets_requirements": blur_score >= threshold,
            "validation_rule": "variance_of_laplacian"
        }
