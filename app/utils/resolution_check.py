import cv2
from PIL import Image
import os
from typing import Dict, Tuple

class ResolutionChecker:
    """Checks image resolution and quality metrics."""
    
    @staticmethod
    def analyze_resolution(image_path: str, min_width: int = 1024, 
                          min_height: int = 1024) -> Dict:
        """
        Analyze image resolution and quality.
        
        Args:
            image_path: Path to the image file
            min_width: Minimum acceptable width
            min_height: Minimum acceptable height
            
        Returns:
            Dictionary with resolution analysis results
        """
        try:
            # Get file size
            file_size = os.path.getsize(image_path)
            
            # Use PIL for accurate dimensions
            with Image.open(image_path) as img:
                width, height = img.size
                format_name = img.format
                mode = img.mode
            
            # Calculate metrics
            total_pixels = width * height
            megapixels = total_pixels / 1_000_000
            aspect_ratio = width / height
            
            # Quality assessments based on new validation rules
            meets_min_resolution = width >= min_width and height >= min_height
            meets_min_megapixels = megapixels >= 1.0
            is_recommended_quality = megapixels >= 2.0
            is_high_resolution = width >= 1920 and height >= 1080
            
            # Determine quality level
            if megapixels >= 2.0:
                quality_level = "excellent"
            elif megapixels >= 1.0:
                quality_level = "acceptable"
            else:
                quality_level = "poor"
            
            # Overall validation
            meets_requirements = meets_min_resolution and meets_min_megapixels
            
            # Estimate compression quality (rough)
            bytes_per_pixel = file_size / total_pixels
            estimated_quality = ResolutionChecker._estimate_jpeg_quality(
                bytes_per_pixel, format_name
            )
            
            return {
                "width": width,
                "height": height,
                "total_pixels": total_pixels,
                "megapixels": round(megapixels, 2),
                "aspect_ratio": round(aspect_ratio, 2),
                "file_size_bytes": file_size,
                "file_size_mb": round(file_size / (1024*1024), 2),
                "format": format_name,
                "color_mode": mode,
                "meets_min_resolution": meets_min_resolution,
                "meets_min_megapixels": meets_min_megapixels,
                "is_recommended_quality": is_recommended_quality,
                "is_high_resolution": is_high_resolution,
                "quality_level": quality_level,
                "meets_requirements": meets_requirements,
                "bytes_per_pixel": round(bytes_per_pixel, 2),
                "estimated_quality": estimated_quality,
                "quality_tier": ResolutionChecker._get_quality_tier(width, height),
                "validation_rules": {
                    "min_width": min_width,
                    "min_height": min_height,
                    "min_megapixels": 1.0,
                    "recommended_megapixels": 2.0
                }
            }
            
        except Exception as e:
            raise Exception(f"Resolution analysis failed: {str(e)}")
    
    @staticmethod
    def _estimate_jpeg_quality(bytes_per_pixel: float, format_name: str) -> str:
        """Estimate JPEG compression quality."""
        if format_name != 'JPEG':
            return "N/A (not JPEG)"
        
        if bytes_per_pixel > 3:
            return "High (minimal compression)"
        elif bytes_per_pixel > 1.5:
            return "Good"
        elif bytes_per_pixel > 0.8:
            return "Fair"
        else:
            return "Low (high compression)"
    
    @staticmethod
    def _get_quality_tier(width: int, height: int) -> str:
        """Get quality tier based on resolution."""
        total_pixels = width * height
        
        if total_pixels >= 8_000_000:  # 4K+
            return "Ultra High"
        elif total_pixels >= 2_000_000:  # Full HD+
            return "High"
        elif total_pixels >= 1_000_000:  # HD+
            return "Medium"
        elif total_pixels >= 500_000:   # SD+
            return "Low"
        else:
            return "Very Low"
