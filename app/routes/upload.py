from flask import Blueprint, current_app, render_template, request, jsonify
import os
import uuid
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from app.services.quality_control import QualityControlService
from app.utils.response_formatter import ResponseFormatter
from app.api_spec import OPENAPI_SPEC


upload_bp = Blueprint('upload', __name__)


class UploadError(Exception):
    """Exception raised when an upload request is invalid."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.status_code = status_code


def allowed_file(filename: str) -> bool:
    """Return True when the provided filename has an allowed extension."""
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in current_app.config['ALLOWED_EXTENSIONS']


def _extract_upload() -> FileStorage:
    """Pull the uploaded file from the request or raise UploadError."""
    if 'image' not in request.files:
        raise UploadError("No image file provided", status_code=400)

    file_storage = request.files['image']
    if not isinstance(file_storage, FileStorage) or file_storage.filename == '':
        raise UploadError("No file selected", status_code=400)

    if not allowed_file(file_storage.filename):
        allowed = ', '.join(sorted(current_app.config['ALLOWED_EXTENSIONS']))
        raise UploadError(f"File type not allowed. Allowed types: {allowed}")

    return file_storage


def _store_upload(file_storage: FileStorage) -> str:
    """Persist the uploaded file to the configured upload directory."""
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)

    filename = secure_filename(file_storage.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    filepath = os.path.join(upload_dir, unique_filename)
    file_storage.save(filepath)
    return filepath


@upload_bp.route('/validate', methods=['POST'])
def validate_image_api():
    """Validate an uploaded image and return the consolidated scoring payload."""
    try:
        file_storage = _extract_upload()
        filepath = _store_upload(file_storage)

        qc_service = QualityControlService(current_app.config)
        validation_results = qc_service.validate_image_with_new_rules(filepath)
        qc_service.handle_validated_image(filepath, validation_results)

        response_data = {
            "summary": {
                "overall_status": validation_results.get('overall_status'),
                "overall_score": validation_results.get('overall_score'),
                "issues_found": validation_results.get('issues_found'),
                "recommendations": validation_results.get('recommendations', []),
            },
            "checks": validation_results.get('checks', {}),
        }

        return ResponseFormatter.success(
            data=response_data,
            message="Image validation completed"
        )

    except UploadError as exc:
        return ResponseFormatter.error(str(exc), exc.status_code)
    except RequestEntityTooLarge:
        return ResponseFormatter.error("File too large", 413)
    except Exception as exc:  # pragma: no cover - defensive safeguard
        return ResponseFormatter.error(f"Validation failed: {exc}", 500)


@upload_bp.route('/validation-rules', methods=['GET'])
def get_validation_rules():
    """Expose the active validation rules for clients and documentation."""
    from config import Config
    config = Config()
    return ResponseFormatter.success(
        data=config.VALIDATION_RULES,
        message="Current validation rules"
    )





@upload_bp.route('/summary', methods=['GET'])
def get_processing_summary():
    """Return aggregate validation statistics for observability dashboards."""
    try:
        qc_service = QualityControlService(current_app.config)
        summary = qc_service.get_validation_summary()
        return ResponseFormatter.success(
            data=summary,
            message="Processing summary retrieved"
        )
    except Exception as exc:  # pragma: no cover - defensive safeguard
        return ResponseFormatter.error(f"Failed to get summary: {exc}", 500)


@upload_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint for load balancers and monitors."""
    return ResponseFormatter.success(
        data={
            "status": "healthy",
            "service": "photoguard",
            "api_version": "3.0.0",
            "validation_rules": "updated"
        },
        message="Service is running"
    )


@upload_bp.route('/openapi.json', methods=['GET'])
def get_openapi_spec():
    """Return the OpenAPI 3.1 specification in JSON format."""
    return jsonify(OPENAPI_SPEC)


@upload_bp.route('/docs', methods=['GET'])
def swagger_ui():
    """Serve the Swagger UI documentation page."""
    return render_template('swagger.html')


@upload_bp.route('/redoc', methods=['GET'])
def redoc_ui():
    """Serve the ReDoc documentation page."""
    return render_template('redoc.html')
