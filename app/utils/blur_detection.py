import cv2
import numpy as np
from typing import Optional, Tuple, Union


def blur_score(image: Optional[Union[str, bytes, np.ndarray]]) -> float:
    """Return Laplacian variance for backward-compatible API calls.

    Accepts either a path to an image on disk or an in-memory numpy array.
    When the input is ``None`` or invalid, ``0.0`` is returned so legacy
    callers can treat the output as a failed blur computation.
    """
    if image is None:
        return 0.0

    try:
        if isinstance(image, (str, bytes)):
            frame = cv2.imread(image)
        else:
            frame = np.asarray(image)

        if frame is None or frame.size == 0:
            return 0.0

        if frame.ndim == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        return float(cv2.Laplacian(gray, cv2.CV_64F).var())
    except Exception:
        return 0.0

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
