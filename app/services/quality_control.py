from typing import Dict, Tuple
import os
import shutil
from datetime import datetime

from config import Config

class QualityControlService:
    """Main service for image quality control and validation."""
    
    def __init__(self, config):
        """
        Initialize with either Config class instance or Flask config object
        
        Args:
            config: Config class instance or Flask config object
        """
        self.config = config
        
        # Handle both Config class and Flask config object
        if hasattr(config, 'PROCESSED_FOLDER'):
            # Config class instance
            self.processed_folder = config.PROCESSED_FOLDER
            self.rejected_folder = config.REJECTED_FOLDER
            self.yolo_model_path = config.YOLO_MODEL_PATH
            self.blur_threshold = config.BLUR_THRESHOLD
            self.min_brightness = config.MIN_BRIGHTNESS
            self.max_brightness = config.MAX_BRIGHTNESS
            self.min_resolution_width = config.MIN_RESOLUTION_WIDTH
            self.min_resolution_height = config.MIN_RESOLUTION_HEIGHT
            self.city_boundaries = config.CITY_BOUNDARIES
        else:
            # Flask config object (dictionary-like)
            self.processed_folder = config.get('PROCESSED_FOLDER', 'storage/processed')
            self.rejected_folder = config.get('REJECTED_FOLDER', 'storage/rejected')
            self.yolo_model_path = config.get('YOLO_MODEL_PATH', 'models/yolov8n.pt')
            self.blur_threshold = config.get('BLUR_THRESHOLD', 100.0)
            self.min_brightness = config.get('MIN_BRIGHTNESS', 30)
            self.max_brightness = config.get('MAX_BRIGHTNESS', 220)
            self.min_resolution_width = config.get('MIN_RESOLUTION_WIDTH', 800)
            self.min_resolution_height = config.get('MIN_RESOLUTION_HEIGHT', 600)
            self.city_boundaries = config.get('CITY_BOUNDARIES', {
                'min_lat': 40.4774,
                'max_lat': 40.9176,
                'min_lon': -74.2591,
                'max_lon': -73.7004
            })
        
        self.object_detector = None
        self._initialize_object_detector()
    
    def _initialize_object_detector(self):
        """Initialize object detector if model exists."""
        try:
            if os.path.exists(self.yolo_model_path):
                from app.utils.object_detection import ObjectDetector
                self.object_detector = ObjectDetector(self.yolo_model_path)
        except Exception as e:
            print(f"Warning: Object detector initialization failed: {e}")
    
    def validate_image(self, image_path: str) -> Dict:
        """
        Perform comprehensive image quality validation.

        Args:
            image_path: Path to the uploaded image

        Returns:
            Dictionary with complete validation results
        """
        validation_start = datetime.now()

        try:
            # Initialize results structure
            results = {
                "timestamp": validation_start.isoformat(),
                "image_path": image_path,
                "overall_status": "pending",
                "issues": [],
                "warnings": [],
                "validations": {
                    "blur_detection": None,
                    "brightness_validation": None,
                    "resolution_check": None,
                    "metadata_extraction": None,
                    "object_detection": None
                },
                "metrics": {},
                "recommendations": []
            }

            # 1. Blur Detection
            try:
                from app.utils.blur_detection import BlurDetector
                blur_score, is_blurry = BlurDetector.calculate_blur_score(
                    image_path, self.blur_threshold
                )
                results["validations"]["blur_detection"] = BlurDetector.get_blur_details(
                    blur_score, self.blur_threshold
                )
                
                if is_blurry:
                    results["issues"].append({
                        "type": "blur",
                        "severity": "high",
                        "message": f"Image is too blurry (score: {blur_score:.2f})"
                    })
                    results["recommendations"].append(
                        "Take a new photo with better focus and stable camera"
                    )
                
            except Exception as e:
                results["validations"]["blur_detection"] = {"error": str(e)}
                results["warnings"].append(f"Blur detection failed: {str(e)}")
            
            # 2. Brightness Validation
            try:
                from app.utils.brightness_validation import BrightnessValidator
                brightness_analysis = BrightnessValidator.analyze_brightness(
                    image_path, self.min_brightness, self.max_brightness
                )
                results["validations"]["brightness_validation"] = brightness_analysis
                
                if brightness_analysis["has_brightness_issues"]:
                    severity = "high" if brightness_analysis["is_too_dark"] or brightness_analysis["is_too_bright"] else "medium"
                    results["issues"].append({
                        "type": "brightness",
                        "severity": severity,
                        "message": "Image has brightness/exposure issues"
                    })
                    results["recommendations"].append(
                        "Adjust lighting conditions or use flash for better exposure"
                    )
                
            except Exception as e:
                results["validations"]["brightness_validation"] = {"error": str(e)}
                results["warnings"].append(f"Brightness validation failed: {str(e)}")
            
            # 3. Resolution Check
            try:
                from app.utils.resolution_check import ResolutionChecker
                resolution_analysis = ResolutionChecker.analyze_resolution(
                    image_path, self.min_resolution_width, self.min_resolution_height
                )
                results["validations"]["resolution_check"] = resolution_analysis
                
                if not resolution_analysis["meets_min_resolution"]:
                    results["issues"].append({
                        "type": "resolution",
                        "severity": "high",
                        "message": f"Image resolution too low: {resolution_analysis['width']}x{resolution_analysis['height']}"
                    })
                    results["recommendations"].append(
                        "Take photo with higher resolution camera or zoom in"
                    )
                
            except Exception as e:
                results["validations"]["resolution_check"] = {"error": str(e)}
                results["warnings"].append(f"Resolution check failed: {str(e)}")
            
            # 4. Exposure Check
            try:
                from app.utils.exposure_check import ExposureChecker
                exposure_analysis = ExposureChecker.analyze_exposure(image_path)
                results["validations"]["exposure_check"] = exposure_analysis
                
                if not exposure_analysis["has_good_exposure"]:
                    severity = "high" if exposure_analysis["is_underexposed"] or exposure_analysis["is_overexposed"] else "medium"
                    results["issues"].append({
                        "type": "exposure",
                        "severity": severity,
                        "message": f"Poor exposure quality: {exposure_analysis['exposure_quality']}"
                    })
                    
                    # Add specific recommendations
                    for rec in exposure_analysis["recommendations"]:
                        if rec != "Exposure looks good":
                            results["recommendations"].append(rec)
                
            except Exception as e:
                results["validations"]["exposure_check"] = {"error": str(e)}
                results["warnings"].append(f"Exposure check failed: {str(e)}")
            
            # 5. Metadata Extraction
            try:
                from app.utils.metadata_extraction import MetadataExtractor
                metadata = MetadataExtractor.extract_metadata(image_path)
                results["validations"]["metadata_extraction"] = metadata
                
                # Check GPS location if available
                if metadata.get("gps_data"):
                    location_validation = MetadataExtractor.validate_location(
                        metadata["gps_data"], self.city_boundaries
                    )
                    if not location_validation["within_boundaries"]:
                        results["warnings"].append({
                            "type": "location",
                            "message": location_validation["reason"]
                        })
                
            except Exception as e:
                results["validations"]["metadata_extraction"] = {"error": str(e)}
                results["warnings"].append(f"Metadata extraction failed: {str(e)}")            # 6. Object Detection (if available)
            if self.object_detector:
                try:
                    detection_results = self.object_detector.detect_objects(image_path)
                    results["validations"]["object_detection"] = detection_results

                    if not detection_results["has_civic_content"]:
                        results["warnings"].append({
                            "type": "civic_content",
                            "message": "No civic-related objects detected in image"
                        })

                except Exception as e:
                    results["validations"]["object_detection"] = {"error": str(e)}
                    results["warnings"].append(f"Object detection failed: {str(e)}")
            else:
                results["validations"]["object_detection"] = {
                    "message": "Object detection not available - model not loaded"
                }

            # Calculate overall metrics
            results["metrics"] = self._calculate_metrics(results)

            # Determine overall status
            results["overall_status"] = self._determine_overall_status(results)

            # Add processing time
            processing_time = (datetime.now() - validation_start).total_seconds()
            results["processing_time_seconds"] = round(processing_time, 3)

            # Handle image based on status
            self._handle_image_result(image_path, results)

            return results

        except Exception as e:
            return {
                "timestamp": validation_start.isoformat(),
                "image_path": image_path,
                "overall_status": "error",
                "error": f"Validation failed: {str(e)}",
                "issues": [{
                    "type": "validation_error",
                    "severity": "critical",
                    "message": str(e)
                }],
                "warnings": [],
                "recommendations": ["Please try uploading the image again"],
                "processing_time_seconds": (datetime.now() - validation_start).total_seconds()
            }
    
    def _calculate_metrics(self, results: Dict) -> Dict:
        """Calculate overall quality metrics."""
        metrics = {
            "total_issues": len(results["issues"]),
            "total_warnings": len(results["warnings"]),
            "validations_completed": 0,
            "validations_failed": 0,
            "quality_scores": {}
        }
        
        # Count successful validations
        for validation_type, validation_result in results["validations"].items():
            if validation_result and not validation_result.get("error"):
                metrics["validations_completed"] += 1
            else:
                metrics["validations_failed"] += 1
        
        # Calculate overall quality score
        quality_scores = list(metrics["quality_scores"].values())
        if quality_scores:
            metrics["overall_quality_score"] = round(sum(quality_scores) / len(quality_scores), 3)
        else:
            metrics["overall_quality_score"] = 0.0
        
        return metrics
    
    def _determine_overall_status(self, results: Dict) -> str:
        """Determine overall validation status."""
        if results["metrics"]["total_issues"] == 0:
            if results["metrics"]["total_warnings"] == 0:
                return "excellent"
            elif results["metrics"]["total_warnings"] <= 2:
                return "good"
            else:
                return "acceptable"
        else:
            high_severity_issues = sum(1 for issue in results["issues"] 
                                     if issue.get("severity") == "high")
            if high_severity_issues > 0:
                return "rejected"
            else:
                return "needs_improvement"
    
    def _handle_image_result(self, image_path: str, results: Dict):
        """Move image to appropriate folder based on validation results."""
        try:
            filename = os.path.basename(image_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{timestamp}_{filename}"
            
            if results["overall_status"] in ["excellent", "good", "acceptable"]:
                # Move to processed folder
                target_dir = self.processed_folder
                destination = os.path.join(target_dir, new_filename)
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(image_path, destination)
                results["processed_path"] = destination
            else:
                # Move to rejected folder for analysis
                target_dir = self.rejected_folder
                destination = os.path.join(target_dir, new_filename)
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(image_path, destination)
                results["rejected_path"] = destination
                
        except Exception as e:
            results["warnings"].append(f"Failed to move image file: {str(e)}")

    def get_validation_summary(self) -> Dict:
        """Get summary statistics of validation results."""
        try:
            processed_count = len(os.listdir(self.processed_folder)) if os.path.exists(self.processed_folder) else 0
            rejected_count = len(os.listdir(self.rejected_folder)) if os.path.exists(self.rejected_folder) else 0
            total_count = processed_count + rejected_count
            
            acceptance_rate = (processed_count / total_count * 100) if total_count > 0 else 0
            
            return {
                "total_processed": processed_count,
                "total_rejected": rejected_count,
                "total_images": total_count,
                "acceptance_rate": round(acceptance_rate, 2),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to generate summary: {str(e)}"}

    def validate_image_with_new_rules(self, filepath):
        """
        Comprehensive image validation using updated validation rules.
        
        Returns detailed validation results in the new format.
        """
        results = {
            'overall_status': 'pending',
            'overall_score': 0,
            'issues_found': 0,
            'checks': {
                'blur': None,
                'brightness': None,
                'resolution': None,
                'exposure': None,
                'metadata': None
            },
            'recommendations': []
        }
        
        import time
        start_time = time.time()
        
        try:
            # Load image for processing
            import cv2
            image = cv2.imread(filepath)
            if image is None:
                raise ValueError("Could not load image file")
            
            # 1. Blur Detection with new rules
            try:
                from app.utils.blur_detection import BlurDetector
                from config import Config
                config = Config()
                blur_score, is_blurry = BlurDetector.calculate_blur_score(filepath, config.VALIDATION_RULES['blur']['min_score'])
                blur_result = BlurDetector.get_blur_details(blur_score, config.VALIDATION_RULES['blur']['min_score'])
                
                status = "pass" if blur_result.get('meets_requirements', False) else "fail"
                results['checks']['blur'] = {
                    'status': status,
                    'score': blur_result.get('blur_score', 0),
                    'threshold': config.VALIDATION_RULES['blur']['min_score'],
                    'reason': 'Image sharpness is acceptable' if status == 'pass' else 'Image is too blurry for quality standards'
                }
                
                if status == "fail":
                    results['issues_found'] += 1
                    results['recommendations'].append('Take a clearer photo with better focus')
                    
            except Exception as e:
                results['checks']['blur'] = {
                    'status': 'fail',
                    'score': 0,
                    'threshold': 150,
                    'reason': f'Blur detection failed: {str(e)}'
                }
                results['issues_found'] += 1
            
            # 2. Brightness Validation with new rules
            try:
                from app.utils.brightness_validation import BrightnessValidator
                from config import Config
                config = Config()
                brightness_result = BrightnessValidator.analyze_brightness(
                    filepath, 
                    config.VALIDATION_RULES['brightness']['range'][0],
                    config.VALIDATION_RULES['brightness']['range'][1]
                )
                
                status = "pass" if brightness_result.get('meets_requirements', False) else "fail"
                results['checks']['brightness'] = {
                    'status': status,
                    'mean_brightness': brightness_result.get('mean_brightness', 0),
                    'range': config.VALIDATION_RULES['brightness']['range'],
                    'reason': 'Brightness is within the acceptable range' if status == 'pass' else 'Brightness is outside the acceptable range'
                }
                
                if status == "fail":
                    results['issues_found'] += 1
                    results['recommendations'].append('Take photo in better lighting conditions')
                    
            except Exception as e:
                results['checks']['brightness'] = {
                    'status': 'fail',
                    'mean_brightness': 0,
                    'range': [90, 180],
                    'reason': f'Brightness validation failed: {str(e)}'
                }
                results['issues_found'] += 1
            
            # 3. Resolution Check with new rules
            try:
                from app.utils.resolution_check import ResolutionChecker
                from config import Config
                config = Config()
                resolution_result = ResolutionChecker.analyze_resolution(
                    filepath,
                    config.VALIDATION_RULES['resolution']['min_width'],
                    config.VALIDATION_RULES['resolution']['min_height']
                )
                
                status = "pass" if resolution_result.get('meets_requirements', False) else "fail"
                results['checks']['resolution'] = {
                    'status': status,
                    'width': resolution_result.get('width', 0),
                    'height': resolution_result.get('height', 0),
                    'megapixels': resolution_result.get('megapixels', 0),
                    'min_required': f"{config.VALIDATION_RULES['resolution']['min_width']}x{config.VALIDATION_RULES['resolution']['min_height']}, ≥{config.VALIDATION_RULES['resolution']['min_megapixels']} MP",
                    'reason': 'Resolution meets the minimum requirements' if status == 'pass' else 'Resolution below minimum required size'
                }
                
                if status == "fail":
                    results['issues_found'] += 1
                    results['recommendations'].append('Use higher resolution camera setting')
                    
            except Exception as e:
                results['checks']['resolution'] = {
                    'status': 'fail',
                    'width': 0,
                    'height': 0,
                    'megapixels': 0,
                    'min_required': "1024x1024, ≥1 MP",
                    'reason': f'Resolution check failed: {str(e)}'
                }
                results['issues_found'] += 1
            
            # 4. Exposure Check with new rules
            try:
                from app.utils.exposure_check import ExposureChecker
                from config import Config
                config = Config()
                exposure_result = ExposureChecker.analyze_exposure(filepath)
                
                status = "pass" if exposure_result.get('meets_requirements', False) else "fail"
                results['checks']['exposure'] = {
                    'status': status,
                    'dynamic_range': exposure_result.get('dynamic_range', 0),
                    'threshold': config.VALIDATION_RULES['exposure']['min_score'],
                    'reason': 'Exposure and dynamic range are excellent' if status == 'pass' else 'Exposure quality below acceptable standards'
                }
                
                if status == "fail":
                    results['issues_found'] += 1
                    
                # Add specific recommendations from the exposure checker
                exposure_recommendations = exposure_result.get('recommendations', [])
                for rec in exposure_recommendations:
                    if rec not in results['recommendations'] and 'Exposure looks good' not in rec:
                        results['recommendations'].append(rec)
                    
            except Exception as e:
                results['checks']['exposure'] = {
                    'status': 'fail',
                    'dynamic_range': 0,
                    'threshold': 150,
                    'reason': f'Exposure check failed: {str(e)}'
                }
                results['issues_found'] += 1
            
            # 5. Metadata Extraction with new rules
            try:
                from app.utils.metadata_extraction import MetadataExtractor
                from config import Config
                config = Config()
                metadata_result = MetadataExtractor.extract_metadata(filepath)
                
                # Extract validation info if available
                validation_info = metadata_result.get('validation', {})
                completeness = validation_info.get('completeness_percentage', 0)
                meets_requirements = completeness >= config.VALIDATION_RULES['metadata']['min_completeness_percentage']
                
                # Find missing fields
                all_fields = set(config.VALIDATION_RULES['metadata']['required_fields'])
                extracted_fields = set()
                
                # Check what fields we actually have
                basic_info = metadata_result.get('basic_info', {})
                camera_settings = metadata_result.get('camera_settings', {})
                
                if basic_info.get('timestamp'):
                    extracted_fields.add('timestamp')
                if basic_info.get('camera_make') or basic_info.get('camera_model'):
                    extracted_fields.add('camera_make_model')
                if basic_info.get('orientation'):
                    extracted_fields.add('orientation')
                if camera_settings.get('iso'):
                    extracted_fields.add('iso')
                if camera_settings.get('shutter_speed'):
                    extracted_fields.add('shutter_speed')
                if camera_settings.get('aperture'):
                    extracted_fields.add('aperture')
                
                missing_fields = list(all_fields - extracted_fields)
                
                status = "pass" if meets_requirements else "fail"
                results['checks']['metadata'] = {
                    'status': status,
                    'completeness': completeness,
                    'required_min': config.VALIDATION_RULES['metadata']['min_completeness_percentage'],
                    'missing_fields': missing_fields,
                    'reason': 'Sufficient metadata extracted' if status == 'pass' else 'Insufficient metadata extracted'
                }
                
                if status == "fail":
                    results['issues_found'] += 1
                    results['recommendations'].append('Ensure camera metadata is enabled')
                    
            except Exception as e:
                results['checks']['metadata'] = {
                    'status': 'fail',
                    'completeness': 0,
                    'required_min': 30,
                    'missing_fields': config.VALIDATION_RULES['metadata']['required_fields'],
                    'reason': f'Metadata extraction failed: {str(e)}'
                }
                results['issues_found'] += 1
            
            # Calculate overall status and score
            self._calculate_overall_status_new_format(results)
            
            return results
            
        except Exception as e:
            results['issues_found'] += 1
            results['overall_status'] = 'fail'
            results['overall_score'] = 0
            return results

    def _calculate_overall_status_new_format(self, results):
        """Calculate overall status and score based on validation results in new format."""
        checks = results['checks']
        
        # Weight different checks by importance for civic photos
        check_weights = {
            'blur': 25,      # Very important - blurry photos are unusable
            'resolution': 25, # Important - need readable details
            'brightness': 20, # Important but more tolerance
            'exposure': 15,   # Less critical - can be adjusted
            'metadata': 15    # Nice to have but not critical for civic use
        }
        
        total_weighted_score = 0
        total_weight = 0
        
        for check_name, check_result in checks.items():
            if check_result is not None:
                weight = check_weights.get(check_name, 10)
                if check_result.get('status') == 'pass':
                    score = 100
                else:
                    # Partial credit based on how close to passing
                    score = self._calculate_partial_score(check_name, check_result)
                
                total_weighted_score += score * weight
                total_weight += weight
        
        # Calculate overall score (0-100)
        if total_weight > 0:
            results['overall_score'] = round(total_weighted_score / total_weight, 1)
        else:
            results['overall_score'] = 0
        
        # More flexible overall status - pass if score >= 65
        if results['overall_score'] >= 65:
            results['overall_status'] = 'pass'
        else:
            results['overall_status'] = 'fail'
    
    def _calculate_partial_score(self, check_name, check_result):
        """Calculate partial score for failed checks."""
        if check_name == 'blur':
            score = check_result.get('score', 0)
            threshold = check_result.get('threshold', 100)
            # Give partial credit up to threshold
            return min(80, (score / threshold) * 80) if score > 0 else 0
            
        elif check_name == 'brightness':
            brightness = check_result.get('mean_brightness', 0)
            range_min, range_max = check_result.get('range', [50, 220])
            # Give partial credit if close to acceptable range
            if brightness < range_min:
                distance = range_min - brightness
                return max(30, 80 - (distance / 50) * 50)
            elif brightness > range_max:
                distance = brightness - range_max
                return max(30, 80 - (distance / 50) * 50)
            return 70  # Close to range
            
        elif check_name == 'resolution':
            megapixels = check_result.get('megapixels', 0)
            # Give partial credit based on megapixels
            if megapixels >= 0.3:  # At least VGA quality
                return min(80, (megapixels / 0.5) * 80)
            return 20
            
        elif check_name == 'exposure':
            dynamic_range = check_result.get('dynamic_range', 0)
            threshold = check_result.get('threshold', 100)
            # Give partial credit
            return min(70, (dynamic_range / threshold) * 70) if dynamic_range > 0 else 30
            
        elif check_name == 'metadata':
            completeness = check_result.get('completeness', 0)
            # Give partial credit for any metadata
            return min(60, completeness * 2)  # Scale to 60 max
            
        return 20  # Default partial score

    def handle_validated_image(self, filepath, validation_results):
        """Move image to appropriate folder based on new validation results."""
        try:
            import os
            import shutil
            import uuid
            from datetime import datetime
            
            filename = os.path.basename(filepath)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            new_filename = f"{timestamp}_{unique_id}_{filename}"
            
            # Use new scoring system - pass images with score >= 65
            if validation_results['overall_status'] == 'pass':
                # Move to processed folder
                target_dir = self.processed_folder
                destination = os.path.join(target_dir, new_filename)
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(filepath, destination)
                validation_results['processed_path'] = destination
            else:
                # Move to rejected folder for analysis
                target_dir = self.rejected_folder
                destination = os.path.join(target_dir, new_filename)
                os.makedirs(target_dir, exist_ok=True)
                shutil.move(filepath, destination)
                validation_results['rejected_path'] = destination
                
        except Exception as e:
            # If moving fails, just log it - don't break the validation
            validation_results['file_handling_error'] = str(e)