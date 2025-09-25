import cv2
import numpy as np
from typing import Tuple, Dict

class BrightnessValidator:
    """Validates image brightness and exposure."""
    
    @staticmethod
    def analyze_brightness(image_path: str, min_brightness: int = 90, 
                          max_brightness: int = 180) -> Dict:
        """
        Analyze image brightness and exposure.
        
        Args:
            image_path: Path to the image file
            min_brightness: Minimum acceptable mean brightness
            max_brightness: Maximum acceptable mean brightness
            
        Returns:
            Dictionary with brightness analysis results
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate statistics
            mean_brightness = np.mean(gray)
            std_brightness = np.std(gray)
            
            # Calculate histogram
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist = hist.flatten()
            
            # Analyze exposure
            dark_pixels = np.sum(hist[:50]) / hist.sum()  # Very dark pixels
            bright_pixels = np.sum(hist[200:]) / hist.sum()  # Very bright pixels
            
            # Determine issues
            is_too_dark = mean_brightness < min_brightness
            is_too_bright = mean_brightness > max_brightness
            is_overexposed = bright_pixels > 0.1  # >10% very bright pixels
            is_underexposed = dark_pixels > 0.3   # >30% very dark pixels
            
            # Overall assessment
            has_brightness_issues = is_too_dark or is_too_bright or is_overexposed or is_underexposed
            
            # Calculate quality score percentage
            quality_score = BrightnessValidator._calculate_quality_score(
                mean_brightness, std_brightness, dark_pixels, bright_pixels
            )
            quality_score_percentage = quality_score * 100
            
            # Determine quality level based on new rules
            meets_requirements = (min_brightness <= mean_brightness <= max_brightness and 
                                quality_score_percentage >= 60)  # Updated to match new config
            
            quality_level = "excellent" if quality_score_percentage >= 80 else \
                           "acceptable" if quality_score_percentage >= 60 else "poor"
            
            return {
                "mean_brightness": round(mean_brightness, 2),
                "std_brightness": round(std_brightness, 2),
                "dark_pixels_ratio": round(dark_pixels, 3),
                "bright_pixels_ratio": round(bright_pixels, 3),
                "is_too_dark": is_too_dark,
                "is_too_bright": is_too_bright,
                "is_overexposed": is_overexposed,
                "is_underexposed": is_underexposed,
                "has_brightness_issues": has_brightness_issues,
                "quality_score": round(quality_score, 3),
                "quality_score_percentage": round(quality_score_percentage, 1),
                "quality_level": quality_level,
                "meets_requirements": meets_requirements,
                "validation_rule": "mean_pixel_intensity",
                "acceptable_range": [min_brightness, max_brightness]
            }
            
        except Exception as e:
            raise Exception(f"Brightness analysis failed: {str(e)}")
    
    @staticmethod
    def _calculate_quality_score(mean_brightness: float, std_brightness: float,
                               dark_ratio: float, bright_ratio: float) -> float:
        """Calculate overall brightness quality score (0-1)."""
        # Ideal brightness range
        brightness_score = 1.0 - abs(mean_brightness - 128) / 128
        
        # Good contrast (standard deviation)
        contrast_score = min(std_brightness / 64, 1.0)
        
        # Penalize extreme ratios
        exposure_penalty = max(dark_ratio - 0.1, 0) + max(bright_ratio - 0.05, 0)
        
        quality_score = (brightness_score + contrast_score) / 2 - exposure_penalty
        return max(0, min(1, quality_score))
