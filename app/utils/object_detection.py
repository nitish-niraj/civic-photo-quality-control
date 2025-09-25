from ultralytics import YOLO
import cv2
import numpy as np
from typing import Dict, List, Tuple
import os

class ObjectDetector:
    """Handles object detection using YOLO models."""
    
    def __init__(self, model_path: str = "models/yolov8n.pt"):
        """Initialize YOLO model."""
        self.model_path = model_path
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load YOLO model."""
        try:
            if os.path.exists(self.model_path):
                self.model = YOLO(self.model_path)
            else:
                # Download model if not exists
                self.model = YOLO("yolov8n.pt")
                # Save to models directory
                os.makedirs("models", exist_ok=True)
                self.model.export(format="onnx")  # Optional: export to different format
        except Exception as e:
            raise Exception(f"Failed to load YOLO model: {str(e)}")
    
    def detect_objects(self, image_path: str, confidence_threshold: float = 0.5) -> Dict:
        """
        Detect objects in image using YOLO.
        
        Args:
            image_path: Path to the image file
            confidence_threshold: Minimum confidence for detections
            
        Returns:
            Dictionary with detection results
        """
        try:
            if self.model is None:
                raise Exception("YOLO model not loaded")
            
            # Run inference
            results = self.model(image_path, conf=confidence_threshold)
            
            # Process results
            detections = []
            civic_objects = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get detection details
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        class_name = self.model.names[class_id]
                        bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                        
                        detection = {
                            "class_name": class_name,
                            "confidence": round(confidence, 3),
                            "bbox": [round(coord, 2) for coord in bbox],
                            "area": (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                        }
                        detections.append(detection)
                        
                        # Check for civic-related objects
                        if self._is_civic_object(class_name):
                            civic_objects.append(detection)
            
            return {
                "total_detections": len(detections),
                "all_detections": detections,
                "civic_objects": civic_objects,
                "civic_object_count": len(civic_objects),
                "has_civic_content": len(civic_objects) > 0,
                "summary": self._generate_detection_summary(detections)
            }
            
        except Exception as e:
            return {
                "error": f"Object detection failed: {str(e)}",
                "total_detections": 0,
                "all_detections": [],
                "civic_objects": [],
                "civic_object_count": 0,
                "has_civic_content": False
            }
    
    def _is_civic_object(self, class_name: str) -> bool:
        """Check if detected object is civic-related."""
        civic_classes = [
            "car", "truck", "bus", "motorcycle", "bicycle",
            "traffic light", "stop sign", "bench", "fire hydrant",
            "street sign", "pothole", "trash can", "dumpster"
        ]
        return class_name.lower() in [c.lower() for c in civic_classes]
    
    def _generate_detection_summary(self, detections: List[Dict]) -> Dict:
        """Generate summary of detections."""
        if not detections:
            return {"message": "No objects detected"}
        
        # Count objects by class
        class_counts = {}
        for detection in detections:
            class_name = detection["class_name"]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        # Find most confident detection
        most_confident = max(detections, key=lambda x: x["confidence"])
        
        return {
            "unique_classes": len(class_counts),
            "class_counts": class_counts,
            "most_confident_detection": {
                "class": most_confident["class_name"],
                "confidence": most_confident["confidence"]
            },
            "avg_confidence": round(
                sum(d["confidence"] for d in detections) / len(detections), 3
            )
        }

    def detect_specific_civic_issues(self, image_path: str) -> Dict:
        """
        Detect specific civic issues (future enhancement).
        This would use a fine-tuned model for pothole, overflowing bins, etc.
        """
        # Placeholder for future implementation
        return {
            "potholes": [],
            "overflowing_bins": [],
            "broken_streetlights": [],
            "graffiti": [],
            "message": "Specific civic issue detection not yet implemented"
        }
