from flask import jsonify
from typing import Dict, Any, Optional
import json
import numpy as np

class ResponseFormatter:
    """Standardized API response formatter."""
    
    @staticmethod
    def _make_json_serializable(obj):
        """Convert non-serializable objects to JSON-serializable format."""
        if isinstance(obj, dict):
            return {key: ResponseFormatter._make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [ResponseFormatter._make_json_serializable(item) for item in obj]
        elif isinstance(obj, bytes):
            # Convert bytes to base64 string or length info
            return f"<bytes: {len(obj)} bytes>"
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32, np.float16)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif hasattr(obj, '__dict__'):
            return ResponseFormatter._make_json_serializable(obj.__dict__)
        else:
            return obj
    
    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = 200):
        """Format successful response."""
        # Make data JSON serializable
        if data is not None:
            data = ResponseFormatter._make_json_serializable(data)
            
        response = {
            "success": True,
            "message": message,
            "data": data,
            "error": None
        }
        return jsonify(response), status_code
    
    @staticmethod
    def error(message: str, status_code: int = 400, error_details: Optional[Dict] = None):
        """Format error response."""
        response = {
            "success": False,
            "message": message,
            "data": None,
            "error": error_details or {"code": status_code, "message": message}
        }
        return jsonify(response), status_code
    
    @staticmethod
    def validation_response(validation_results: Dict):
        """Format validation-specific response."""
        status_code = 200
        
        # Determine HTTP status based on validation results
        if validation_results.get("overall_status") == "error":
            status_code = 500
        elif validation_results.get("overall_status") == "rejected":
            status_code = 422  # Unprocessable Entity
        
        message_map = {
            "excellent": "Image passed all quality checks",
            "good": "Image passed with minor warnings",
            "acceptable": "Image acceptable with some issues",
            "needs_improvement": "Image needs improvement",
            "rejected": "Image rejected due to quality issues",
            "error": "Validation failed due to processing error"
        }
        
        overall_status = validation_results.get("overall_status", "unknown")
        message = message_map.get(overall_status, "Validation completed")
        
        return ResponseFormatter.success(
            data=validation_results,
            message=message,
            status_code=status_code
        )