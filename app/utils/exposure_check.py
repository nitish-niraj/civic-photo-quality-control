import cv2
import numpy as np
from typing import Dict, Tuple

class ExposureChecker:
    """Checks image exposure and lighting conditions."""
    
    @staticmethod
    def analyze_exposure(image_path: str) -> Dict:
        """
        Analyze image exposure using histogram analysis.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with exposure analysis results
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert to different color spaces for analysis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Calculate histogram
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist = hist.flatten()
            total_pixels = hist.sum()
            
            # Analyze exposure zones
            shadows = np.sum(hist[:85]) / total_pixels      # 0-85: shadows
            midtones = np.sum(hist[85:170]) / total_pixels  # 85-170: midtones  
            highlights = np.sum(hist[170:]) / total_pixels  # 170-255: highlights
            
            # Calculate exposure metrics
            mean_luminance = np.mean(gray)
            std_luminance = np.std(gray)
            
            # Detect clipping
            shadow_clipping = hist[0] / total_pixels
            highlight_clipping = hist[255] / total_pixels
            
            # Calculate dynamic range
            dynamic_range = ExposureChecker._calculate_dynamic_range(hist)
            
            # Analyze exposure quality
            exposure_quality = ExposureChecker._assess_exposure_quality(
                shadows, midtones, highlights, shadow_clipping, highlight_clipping
            )
            
            # Apply new validation rules
            meets_min_score = dynamic_range >= 150
            is_acceptable_range = 120 <= dynamic_range <= 150
            
            # Check clipping against new rules (max 1%)
            clipping_percentage = max(shadow_clipping, highlight_clipping) * 100
            has_excessive_clipping = clipping_percentage > 1.0
            
            # Determine quality level
            if dynamic_range >= 150 and not has_excessive_clipping:
                quality_level = "excellent"
            elif dynamic_range >= 120 and clipping_percentage <= 1.0:
                quality_level = "acceptable"
            else:
                quality_level = "poor"
            
            meets_requirements = meets_min_score or is_acceptable_range
            
            return {
                "mean_luminance": round(mean_luminance, 2),
                "std_luminance": round(std_luminance, 2),
                "shadows_ratio": round(shadows, 3),
                "midtones_ratio": round(midtones, 3),
                "highlights_ratio": round(highlights, 3),
                "shadow_clipping": round(shadow_clipping, 4),
                "highlight_clipping": round(highlight_clipping, 4),
                "dynamic_range": round(dynamic_range, 2),
                "exposure_quality": exposure_quality,
                "quality_level": quality_level,
                "is_underexposed": shadows > 0.6,
                "is_overexposed": highlights > 0.4,
                "has_clipping": shadow_clipping > 0.01 or highlight_clipping > 0.01,
                "has_excessive_clipping": has_excessive_clipping,
                "clipping_percentage": round(clipping_percentage, 2),
                "meets_min_score": meets_min_score,
                "is_acceptable_range": is_acceptable_range,
                "meets_requirements": meets_requirements,
                "has_good_exposure": meets_requirements and not has_excessive_clipping,
                "validation_rules": {
                    "min_score": 150,
                    "acceptable_range": [120, 150],
                    "max_clipping_percentage": 1.0
                },
                "recommendations": ExposureChecker._get_exposure_recommendations(
                    shadows, highlights, shadow_clipping, highlight_clipping
                )
            }
            
        except Exception as e:
            raise Exception(f"Exposure analysis failed: {str(e)}")
    
    @staticmethod
    def _calculate_dynamic_range(hist: np.ndarray) -> float:
        """Calculate the dynamic range of the image."""
        # Find the range of values that contain 99% of the data
        cumsum = np.cumsum(hist)
        total = cumsum[-1]
        
        # Find 0.5% and 99.5% percentiles
        low_idx = np.where(cumsum >= total * 0.005)[0][0]
        high_idx = np.where(cumsum >= total * 0.995)[0][0]
        
        return high_idx - low_idx
    
    @staticmethod
    def _assess_exposure_quality(shadows: float, midtones: float, highlights: float, 
                               shadow_clip: float, highlight_clip: float) -> str:
        """Assess overall exposure quality."""
        # Ideal distribution: good midtones, some shadows/highlights, no clipping
        if shadow_clip > 0.02 or highlight_clip > 0.02:
            return "poor"  # Significant clipping
        
        if shadows > 0.7:
            return "underexposed"
        
        if highlights > 0.5:
            return "overexposed"
        
        # Good exposure has balanced distribution
        if 0.3 <= midtones <= 0.7 and shadows < 0.5 and highlights < 0.4:
            return "excellent"
        elif 0.2 <= midtones <= 0.8 and shadows < 0.6 and highlights < 0.45:
            return "good"
        else:
            return "fair"
    
    @staticmethod
    def _get_exposure_recommendations(shadows: float, highlights: float,
                                    shadow_clip: float, highlight_clip: float) -> list:
        """Get recommendations for improving exposure."""
        recommendations = []
        
        if shadow_clip > 0.02:
            recommendations.append("Increase exposure or use fill flash to recover shadow details")
        
        if highlight_clip > 0.02:
            recommendations.append("Decrease exposure or use graduated filter to recover highlights")
        
        if shadows > 0.6:
            recommendations.append("Image is underexposed - increase brightness or use flash")
        
        if highlights > 0.4:
            recommendations.append("Image is overexposed - reduce brightness or avoid direct sunlight")
        
        if not recommendations:
            recommendations.append("Exposure looks good")
        
        return recommendations