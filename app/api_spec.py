"""
PhotoGuard API - OpenAPI 3.1 Specification
===========================================
Complete API specification for PhotoGuard image quality validation system.
"""

OPENAPI_SPEC = {
    "openapi": "3.1.0",
    "info": {
        "title": "PhotoGuard API",
        "version": "3.0.0",
        "description": "Professional image quality validation system with automated blur detection, brightness analysis, resolution checking, exposure verification, and metadata extraction",
        "contact": {
            "name": "PhotoGuard API Support"
        }
    },
    "servers": [
        {
            "url": "/api",
            "description": "API Server"
        }
    ],
    "tags": [
        {
            "name": "Image Validation",
            "description": "Core image quality validation endpoints"
        },
        {
            "name": "System Information",
            "description": "System status and configuration endpoints"
        }
    ],
    "paths": {
        "/validate": {
            "post": {
                "tags": ["Image Validation"],
                "summary": "Validate Image Quality",
                "description": "Upload an image and receive comprehensive quality validation results including blur detection, brightness analysis, resolution check, exposure verification, and metadata extraction",
                "operationId": "validate_image",
                "requestBody": {
                    "required": True,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/ImageUpload"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Validation completed successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ValidationResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request - Invalid file or missing parameters",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "413": {
                        "description": "File too large - Maximum 16MB",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/validation-rules": {
            "get": {
                "tags": ["System Information"],
                "summary": "Get Validation Rules",
                "description": "Retrieve the current validation rules and thresholds used by the system",
                "operationId": "get_validation_rules",
                "responses": {
                    "200": {
                        "description": "Validation rules retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ValidationRulesResponse"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/summary": {
            "get": {
                "tags": ["System Information"],
                "summary": "Get Processing Summary",
                "description": "Retrieve aggregate validation statistics including total images processed, pass/fail counts, and average scores",
                "operationId": "get_summary",
                "responses": {
                    "200": {
                        "description": "Processing summary retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/SummaryResponse"
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ErrorResponse"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/health": {
            "get": {
                "tags": ["System Information"],
                "summary": "Health Check",
                "description": "Check if the API service is running and healthy",
                "operationId": "health_check",
                "responses": {
                    "200": {
                        "description": "Service is healthy",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HealthResponse"
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "ImageUpload": {
                "type": "object",
                "required": ["image"],
                "properties": {
                    "image": {
                        "type": "string",
                        "format": "binary",
                        "description": "Image file to validate (jpg, jpeg, png, bmp, tiff). Maximum size: 16MB"
                    }
                }
            },
            "ValidationResponse": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Whether the request was processed successfully",
                        "example": True
                    },
                    "message": {
                        "type": "string",
                        "description": "Response message",
                        "example": "Image validation completed"
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "object",
                                "properties": {
                                    "overall_status": {
                                        "type": "string",
                                        "enum": ["pass", "fail"],
                                        "description": "Overall validation result"
                                    },
                                    "overall_score": {
                                        "type": "number",
                                        "format": "float",
                                        "description": "Overall weighted quality score (0-100)",
                                        "example": 78.5
                                    },
                                    "issues_found": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "List of quality issues detected"
                                    },
                                    "recommendations": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "Recommendations for improving image quality"
                                    }
                                }
                            },
                            "checks": {
                                "type": "object",
                                "properties": {
                                    "blur": {
                                        "$ref": "#/components/schemas/BlurCheck"
                                    },
                                    "brightness": {
                                        "$ref": "#/components/schemas/BrightnessCheck"
                                    },
                                    "resolution": {
                                        "$ref": "#/components/schemas/ResolutionCheck"
                                    },
                                    "exposure": {
                                        "$ref": "#/components/schemas/ExposureCheck"
                                    },
                                    "metadata": {
                                        "$ref": "#/components/schemas/MetadataCheck"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "BlurCheck": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pass", "fail"],
                        "description": "Blur check result"
                    },
                    "score": {
                        "type": "number",
                        "format": "float",
                        "description": "Laplacian variance score (higher = sharper)",
                        "example": 245.8
                    },
                    "threshold": {
                        "type": "number",
                        "format": "float",
                        "description": "Minimum acceptable blur score",
                        "example": 100.0
                    },
                    "quality_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Quality score as percentage (0-100)",
                        "example": 85.5
                    }
                }
            },
            "BrightnessCheck": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pass", "fail"],
                        "description": "Brightness check result"
                    },
                    "mean_brightness": {
                        "type": "number",
                        "format": "float",
                        "description": "Mean pixel intensity (0-255)",
                        "example": 145.3
                    },
                    "acceptable_range": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        },
                        "description": "Acceptable brightness range",
                        "example": [50, 220]
                    },
                    "quality_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Quality score as percentage (0-100)",
                        "example": 92.0
                    }
                }
            },
            "ResolutionCheck": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pass", "fail"],
                        "description": "Resolution check result"
                    },
                    "width": {
                        "type": "integer",
                        "description": "Image width in pixels",
                        "example": 1920
                    },
                    "height": {
                        "type": "integer",
                        "description": "Image height in pixels",
                        "example": 1080
                    },
                    "megapixels": {
                        "type": "number",
                        "format": "float",
                        "description": "Total megapixels",
                        "example": 2.07
                    },
                    "quality_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Quality score as percentage (0-100)",
                        "example": 100.0
                    }
                }
            },
            "ExposureCheck": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pass", "fail"],
                        "description": "Exposure check result"
                    },
                    "dynamic_range": {
                        "type": "number",
                        "format": "float",
                        "description": "Dynamic range (difference between max and min pixel values)",
                        "example": 185.5
                    },
                    "clipping_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Percentage of clipped pixels (pure white or black)",
                        "example": 0.5
                    },
                    "quality_percentage": {
                        "type": "number",
                        "format": "float",
                        "description": "Quality score as percentage (0-100)",
                        "example": 88.0
                    }
                }
            },
            "MetadataCheck": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["pass", "fail"],
                        "description": "Metadata check result"
                    },
                    "completeness": {
                        "type": "number",
                        "format": "float",
                        "description": "Metadata completeness percentage",
                        "example": 66.7
                    },
                    "fields_found": {
                        "type": "integer",
                        "description": "Number of metadata fields found",
                        "example": 4
                    },
                    "fields_required": {
                        "type": "integer",
                        "description": "Total number of expected metadata fields",
                        "example": 6
                    },
                    "extracted_data": {
                        "type": "object",
                        "description": "Extracted EXIF metadata",
                        "properties": {
                            "timestamp": {
                                "type": "string",
                                "description": "Image capture timestamp"
                            },
                            "camera_make_model": {
                                "type": "string",
                                "description": "Camera make and model"
                            },
                            "gps": {
                                "type": "object",
                                "properties": {
                                    "latitude": {
                                        "type": "number",
                                        "format": "float"
                                    },
                                    "longitude": {
                                        "type": "number",
                                        "format": "float"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "ValidationRulesResponse": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "example": True
                    },
                    "message": {
                        "type": "string",
                        "example": "Current validation rules"
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "blur": {
                                "type": "object",
                                "description": "Blur detection rules (25% weight)"
                            },
                            "brightness": {
                                "type": "object",
                                "description": "Brightness validation rules (20% weight)"
                            },
                            "resolution": {
                                "type": "object",
                                "description": "Resolution check rules (25% weight)"
                            },
                            "exposure": {
                                "type": "object",
                                "description": "Exposure analysis rules (15% weight)"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Metadata extraction rules (15% weight)"
                            }
                        }
                    }
                }
            },
            "SummaryResponse": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "example": True
                    },
                    "message": {
                        "type": "string",
                        "example": "Processing summary retrieved"
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "total_processed": {
                                "type": "integer",
                                "description": "Total number of images processed",
                                "example": 150
                            },
                            "passed": {
                                "type": "integer",
                                "description": "Number of images that passed validation",
                                "example": 98
                            },
                            "failed": {
                                "type": "integer",
                                "description": "Number of images that failed validation",
                                "example": 52
                            },
                            "average_score": {
                                "type": "number",
                                "format": "float",
                                "description": "Average quality score across all processed images",
                                "example": 72.5
                            }
                        }
                    }
                }
            },
            "HealthResponse": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "example": True
                    },
                    "message": {
                        "type": "string",
                        "example": "Service is running"
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "example": "healthy"
                            },
                            "service": {
                                "type": "string",
                                "example": "photoguard"
                            },
                            "api_version": {
                                "type": "string",
                                "example": "3.0.0"
                            }
                        }
                    }
                }
            },
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "example": False
                    },
                    "message": {
                        "type": "string",
                        "description": "Error description",
                        "example": "File type not allowed"
                    }
                }
            }
        }
    }
}
