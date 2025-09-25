from flask import Blueprint, request, jsonify, current_app, render_template, send_from_directory
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from app.services.quality_control import QualityControlService
from app.utils.response_formatter import ResponseFormatter

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload_bp.route('/upload', methods=['POST'])
def upload_image():
    """Upload and validate image endpoint."""
    try:
        # Check if file is in request
        if 'image' not in request.files:
            return ResponseFormatter.error("No image file provided", 400)
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return ResponseFormatter.error("No file selected", 400)
        
        # Check file type
        if not allowed_file(file.filename):
            return ResponseFormatter.error(
                f"File type not allowed. Allowed types: {', '.join(current_app.config['ALLOWED_EXTENSIONS'])}",
                400
            )
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(filepath)
        
        # Initialize quality control service
        qc_service = QualityControlService(current_app.config)
        
        # Validate image
        validation_results = qc_service.validate_image(filepath)
        
        # Format response
        return ResponseFormatter.success(
            data=validation_results,
            message="Image validation completed"
        )
        
    except RequestEntityTooLarge:
        return ResponseFormatter.error("File too large", 413)
    except Exception as e:
        return ResponseFormatter.error(f"Upload failed: {str(e)}", 500)

@upload_bp.route('/validate-url', methods=['POST'])
def validate_image_url():
    """Validate image from URL endpoint."""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return ResponseFormatter.error("No URL provided", 400)
        
        url = data['url']
        
        # Download image from URL (implement this as needed)
        # For now, return not implemented
        return ResponseFormatter.error("URL validation not yet implemented", 501)
        
    except Exception as e:
        return ResponseFormatter.error(f"URL validation failed: {str(e)}", 500)

@upload_bp.route('/summary', methods=['GET'])
def get_validation_summary():
    """Get validation statistics summary."""
    try:
        qc_service = QualityControlService(current_app.config)
        summary = qc_service.get_validation_summary()
        
        return ResponseFormatter.success(
            data=summary,
            message="Validation summary retrieved"
        )
        
    except Exception as e:
        return ResponseFormatter.error(f"Failed to get summary: {str(e)}", 500)

@upload_bp.route('/mobile', methods=['GET'])
def mobile_interface():
    """Serve mobile-friendly upload interface."""
    return render_template('mobile_upload.html')

@upload_bp.route('/validate', methods=['POST'])
def validate_image_api():
    """
    Comprehensive image validation API endpoint.
    Returns detailed JSON results with all quality checks.
    """
    try:
        # Check if file is in request
        if 'image' not in request.files:
            return ResponseFormatter.error("No image file provided", 400)
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return ResponseFormatter.error("No file selected", 400)
        
        # Check file type
        if not allowed_file(file.filename):
            return ResponseFormatter.error(
                f"File type not allowed. Allowed types: {', '.join(current_app.config['ALLOWED_EXTENSIONS'])}",
                400
            )
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(filepath)
        
        # Initialize quality control service
        qc_service = QualityControlService(current_app.config)
        
        # Validate image with new rules
        validation_results = qc_service.validate_image_with_new_rules(filepath)
        
        # Move image based on validation results
        qc_service.handle_validated_image(filepath, validation_results)
        
        # Format response in the new structure
        response_data = {
            "summary": {
                "overall_status": validation_results['overall_status'],
                "overall_score": validation_results['overall_score'],
                "issues_found": validation_results['issues_found'],
                "recommendations": validation_results['recommendations']
            },
            "checks": validation_results['checks']
        }
        
        return ResponseFormatter.success(
            data=response_data,
            message="Image validation completed"
        )
        
    except RequestEntityTooLarge:
        return ResponseFormatter.error("File too large", 413)
    except Exception as e:
        return ResponseFormatter.error(f"Validation failed: {str(e)}", 500)

@upload_bp.route('/validation-rules', methods=['GET'])
def get_validation_rules():
    """Get current validation rules."""
    from config import Config
    config = Config()
    
    return ResponseFormatter.success(
        data=config.VALIDATION_RULES,
        message="Current validation rules"
    )

@upload_bp.route('/test-api', methods=['GET'])
def test_api_endpoint():
    """Test API endpoint with sample data."""
    test_results = {
        "api_version": "2.0",
        "timestamp": "2025-09-25T11:00:00Z",
        "validation_rules_applied": {
            "blur": "variance_of_laplacian >= 100 (mobile-friendly)",
            "brightness": "mean_pixel_intensity 50-220 (expanded range)",
            "resolution": "min 800x600, >= 0.5MP (mobile-friendly)",
            "exposure": "dynamic_range >= 100, clipping <= 2%",
            "metadata": "6 required fields, >= 15% completeness",
            "overall": "weighted scoring system, pass at >= 65% overall score"
        },
        "endpoints": {
            "POST /api/validate": "Main validation endpoint",
            "POST /api/upload": "Legacy upload endpoint", 
            "GET /api/validation-rules": "Get current validation rules",
            "GET /api/test-api": "This test endpoint",
            "GET /api/health": "Health check",
            "GET /api/summary": "Processing statistics"
        },
        "example_response_structure": {
            "success": True,
            "message": "Image validation completed",
            "data": {
                "summary": {
                    "overall_status": "pass|fail",
                    "overall_score": 80.0,
                    "issues_found": 1,
                    "recommendations": [
                        "Use higher resolution camera setting",
                        "Ensure camera metadata is enabled"
                    ]
                },
                "checks": {
                    "blur": {
                        "status": "pass|fail",
                        "score": 253.96,
                        "threshold": 150,
                        "reason": "Image sharpness is acceptable"
                    },
                    "brightness": {
                        "status": "pass|fail",
                        "mean_brightness": 128.94,
                        "range": [90, 180],
                        "reason": "Brightness is within the acceptable range"
                    },
                    "exposure": {
                        "status": "pass|fail",
                        "dynamic_range": 254,
                        "threshold": 150,
                        "reason": "Exposure and dynamic range are excellent"
                    },
                    "resolution": {
                        "status": "pass|fail",
                        "width": 1184,
                        "height": 864,
                        "megapixels": 1.02,
                        "min_required": "1024x1024, ≥1 MP",
                        "reason": "Resolution below minimum required size"
                    },
                    "metadata": {
                        "status": "pass|fail",
                        "completeness": 33.3,
                        "required_min": 30,
                        "missing_fields": ["timestamp", "camera_make_model", "orientation", "iso", "shutter_speed", "aperture"],
                        "reason": "Sufficient metadata extracted"
                    }
                }
            }
        }
    }
    
    return ResponseFormatter.success(
        data=test_results,
        message="API test information and example response structure"
    )

@upload_bp.route('/summary', methods=['GET'])
def get_processing_summary():
    """Get processing statistics and summary."""
    try:
        qc_service = QualityControlService(current_app.config)
        summary = qc_service.get_validation_summary()
        
        return ResponseFormatter.success(
            data=summary,
            message="Processing summary retrieved"
        )
        
    except Exception as e:
        return ResponseFormatter.error(f"Failed to get summary: {str(e)}", 500)

@upload_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return ResponseFormatter.success(
        data={
            "status": "healthy", 
            "service": "civic-quality-control",
            "api_version": "2.0",
            "validation_rules": "updated"
        },
        message="Service is running with updated validation rules"
    )
