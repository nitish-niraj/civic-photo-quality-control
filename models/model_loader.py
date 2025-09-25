import torch
from ultralytics import YOLO

def load_yolo_model(model_path='models/yolov8n.pt'):
    """
    Load YOLOv8 model for object detection.
    
    Args:
        model_path (str): Path to the YOLO model file
        
    Returns:
        YOLO: Loaded YOLO model
    """
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load YOLO model: {e}")

# Global model instance
yolo_model = None

def get_yolo_model():
    """
    Get the global YOLO model instance, loading it if necessary.
    
    Returns:
        YOLO: The YOLO model instance
    """
    global yolo_model
    if yolo_model is None:
        yolo_model = load_yolo_model()
    return yolo_model