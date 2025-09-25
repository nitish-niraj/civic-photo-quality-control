from .blur_detection import BlurDetector
from .brightness_validation import BrightnessValidator
from .resolution_check import ResolutionChecker
from .metadata_extraction import MetadataExtractor
from .object_detection import ObjectDetector

class ImageValidator:
    """Combined image validation class for legacy compatibility."""
    
    def __init__(self, blur_threshold=100, brightness_min=40, brightness_max=220, min_width=800, min_height=600):
        self.blur_threshold = blur_threshold
        self.brightness_min = brightness_min
        self.brightness_max = brightness_max
        self.min_width = min_width
        self.min_height = min_height
    
    def validate_image(self, image_path: str) -> dict:
        """
        Validate image and return comprehensive results.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Validation results
        """
        results = {
            "blur": None,
            "brightness": None,
            "resolution": None,
            "metadata": None,
            "objects": None,
            "overall_status": "UNKNOWN"
        }
        
        try:
            # Blur detection
            blur_score, is_blurry = BlurDetector.calculate_blur_score(image_path, self.blur_threshold)
            results["blur"] = BlurDetector.get_blur_details(blur_score, self.blur_threshold)
            
            # Brightness validation
            results["brightness"] = BrightnessValidator.analyze_brightness(
                image_path, self.brightness_min, self.brightness_max
            )
            
            # Resolution check
            results["resolution"] = ResolutionChecker.analyze_resolution(
                image_path, self.min_width, self.min_height
            )
            
            # Metadata extraction
            results["metadata"] = MetadataExtractor.extract_metadata(image_path)
            
            # Object detection (if available)
            try:
                detector = ObjectDetector()
                results["objects"] = detector.detect_objects(image_path)
            except:
                results["objects"] = {"error": "Object detection not available"}
            
            # Determine overall status
            issues = []
            if results["blur"]["is_blurry"]:
                issues.append("blurry")
            if results["brightness"]["has_brightness_issues"]:
                issues.append("brightness")
            if not results["resolution"]["meets_min_resolution"]:
                issues.append("resolution")
            
            results["overall_status"] = "PASS" if not issues else "FAIL"
            results["issues"] = issues
            
        except Exception as e:
            results["error"] = str(e)
            results["overall_status"] = "ERROR"
        
        return results