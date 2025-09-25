# Civic Quality Control API Documentation

**Version**: 2.0  
**Base URL**: `http://localhost:5000/api` (development) | `http://your-domain.com/api` (production)  
**Content-Type**: `application/json`

## 📋 API Overview

The Civic Quality Control API provides comprehensive image validation services optimized for mobile photography. It uses a weighted scoring system with partial credit to achieve realistic acceptance rates for civic documentation.

### Key Features
- **Weighted Validation**: 5-component analysis with intelligent scoring
- **Mobile-Optimized**: Thresholds designed for smartphone cameras  
- **High Performance**: <2 second processing time per image
- **Comprehensive Feedback**: Detailed validation results and recommendations

---

## 🔍 Endpoints

### 1. Health Check

**Endpoint**: `GET /api/health`  
**Purpose**: System status and configuration verification

**Response:**
```json
{
  "success": true,
  "data": {
    "service": "civic-quality-control",
    "status": "healthy",
    "api_version": "2.0",
    "validation_rules": "updated"
  },
  "message": "Service is running with updated validation rules",
  "error": null
}
```

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

### 2. Image Validation (Primary Endpoint)

**Endpoint**: `POST /api/validate`  
**Purpose**: Comprehensive image quality validation with weighted scoring

**Request:**
```bash
Content-Type: multipart/form-data
Body: image=@your_image.jpg
```

**Response Structure:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "overall_status": "PASS|FAIL",
      "overall_score": 85.2,
      "total_issues": 1,
      "image_id": "20250925_143021_abc123_image.jpg"
    },
    "checks": {
      "blur": {
        "status": "PASS|FAIL",
        "score": 95.0,
        "weight": 25,
        "message": "Image sharpness is excellent",
        "details": {
          "variance": 245.6,
          "threshold": 100,
          "quality_level": "excellent"
        }
      },
      "resolution": {
        "status": "PASS|FAIL",
        "score": 100.0,
        "weight": 25,
        "message": "Resolution exceeds requirements",
        "details": {
          "width": 1920,
          "height": 1080,
          "megapixels": 2.07,
          "min_required": 0.5
        }
      },
      "brightness": {
        "status": "PASS|FAIL",
        "score": 80.0,
        "weight": 20,
        "message": "Brightness is within acceptable range",
        "details": {
          "mean_intensity": 142.3,
          "range": [50, 220],
          "quality_percentage": 75
        }
      },
      "exposure": {
        "status": "PASS|FAIL",
        "score": 90.0,
        "weight": 15,
        "message": "Exposure and dynamic range are good",
        "details": {
          "dynamic_range": 128,
          "clipping_percentage": 0.5,
          "max_clipping_allowed": 2
        }
      },
      "metadata": {
        "status": "PASS|FAIL",  
        "score": 60.0,
        "weight": 15,
        "message": "Sufficient metadata extracted",
        "details": {
          "completeness": 45,
          "required": 15,
          "extracted_fields": ["timestamp", "camera_make_model", "iso"]
        }
      }
    },
    "recommendations": [
      "Consider reducing brightness slightly for optimal quality",
      "Image is suitable for civic documentation"
    ]
  },
  "message": "Image validation completed successfully",
  "error": null
}
```

**Scoring System:**
- **Overall Score**: Weighted average of all validation checks
- **Pass Threshold**: 65% overall score required
- **Component Weights**:
  - Blur Detection: 25%
  - Resolution Check: 25%
  - Brightness Validation: 20%
  - Exposure Analysis: 15%
  - Metadata Extraction: 15%

**Example:**
```bash
curl -X POST -F 'image=@test_photo.jpg' http://localhost:5000/api/validate
```

---

### 3. Processing Statistics

**Endpoint**: `GET /api/summary`  
**Purpose**: System performance metrics and acceptance rates

**Response:**
```json
{
  "success": true,
  "data": {
    "total_processed": 156,
    "accepted": 61,
    "rejected": 95,
    "acceptance_rate": 39.1,
    "processing_stats": {
      "avg_processing_time": 1.8,
      "last_24_hours": {
        "processed": 23,
        "accepted": 9,
        "acceptance_rate": 39.1
      }
    },
    "common_rejection_reasons": [
      "blur: 45%",
      "resolution: 23%", 
      "brightness: 18%",
      "exposure: 8%",
      "metadata: 6%"
    ]
  },
  "message": "Processing statistics retrieved",
  "error": null
}
```

**Example:**
```bash
curl http://localhost:5000/api/summary
```

---

### 4. Validation Rules

**Endpoint**: `GET /api/validation-rules`  
**Purpose**: Current validation thresholds and requirements

**Response:**
```json
{
  "success": true,
  "data": {
    "blur": {
      "min_score": 100,
      "metric": "variance_of_laplacian",
      "levels": {
        "poor": 0,
        "acceptable": 100,
        "excellent": 300
      }
    },
    "brightness": {
      "range": [50, 220],
      "metric": "mean_pixel_intensity",
      "quality_score_min": 60
    },
    "resolution": {
      "min_width": 800,
      "min_height": 600,
      "min_megapixels": 0.5,
      "recommended_megapixels": 2
    },
    "exposure": {
      "min_score": 100,
      "metric": "dynamic_range",
      "acceptable_range": [80, 150],
      "check_clipping": {
        "max_percentage": 2
      }
    },
    "metadata": {
      "min_completeness_percentage": 15,
      "required_fields": [
        "timestamp",
        "camera_make_model", 
        "orientation",
        "iso",
        "shutter_speed",
        "aperture"
      ]
    }
  },
  "message": "Current validation rules",
  "error": null
}
```

**Example:**
```bash
curl http://localhost:5000/api/validation-rules
```

---

### 5. API Information

**Endpoint**: `GET /api/test-api`  
**Purpose**: API capabilities and endpoint documentation

**Response:**
```json
{
  "success": true,
  "data": {
    "api_version": "2.0",
    "endpoints": {
      "GET /api/health": "Health check",
      "POST /api/validate": "Main validation endpoint", 
      "GET /api/summary": "Processing statistics",
      "GET /api/validation-rules": "Get current validation rules",
      "GET /api/test-api": "This test endpoint",
      "POST /api/upload": "Legacy upload endpoint"
    },
    "features": [
      "Mobile-optimized validation",
      "Weighted scoring system",
      "Partial credit evaluation",
      "Real-time processing",
      "Comprehensive feedback"
    ]
  },
  "message": "API information retrieved",
  "error": null
}
```

---

### 6. Legacy Upload (Deprecated)

**Endpoint**: `POST /api/upload`  
**Purpose**: Legacy endpoint for backward compatibility  
**Status**: ⚠️ **Deprecated** - Use `/api/validate` instead

---

## 📊 Validation Components

### Blur Detection (25% Weight)
- **Method**: Laplacian variance analysis
- **Threshold**: 100 (mobile-optimized)
- **Levels**: Poor (0-99), Acceptable (100-299), Excellent (300+)

### Resolution Check (25% Weight)  
- **Minimum**: 800×600 pixels (0.5 megapixels)
- **Recommended**: 2+ megapixels
- **Mobile-Friendly**: Optimized for smartphone cameras

### Brightness Validation (20% Weight)
- **Range**: 50-220 pixel intensity
- **Method**: Histogram analysis
- **Quality Threshold**: 60% minimum

### Exposure Analysis (15% Weight)
- **Dynamic Range**: 80-150 acceptable
- **Clipping Check**: Max 2% clipped pixels
- **Method**: Pixel value distribution analysis

### Metadata Extraction (15% Weight)
- **Required Completeness**: 15% (mobile-friendly)
- **Key Fields**: Timestamp, camera info, settings
- **EXIF Analysis**: Automatic extraction and validation

---

## 🚨 Error Handling

### Standard Error Response
```json
{
  "success": false,
  "data": null,
  "message": "Error description",
  "error": {
    "code": "ERROR_CODE",
    "details": "Detailed error information"
  }
}
```

### Common Error Codes
- `INVALID_IMAGE`: Image format not supported or corrupted
- `FILE_TOO_LARGE`: Image exceeds size limit (32MB)
- `PROCESSING_ERROR`: Internal validation error
- `MISSING_IMAGE`: No image provided in request
- `SERVER_ERROR`: Internal server error

---

## 🔧 Usage Examples

### JavaScript/Fetch
```javascript
const formData = new FormData();
formData.append('image', imageFile);

fetch('/api/validate', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Validation result:', data);
  if (data.success && data.data.summary.overall_status === 'PASS') {
    console.log('Image accepted with score:', data.data.summary.overall_score);
  }
});
```

### Python/Requests
```python
import requests

with open('image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/api/validate', files=files)
    
result = response.json()
if result['success'] and result['data']['summary']['overall_status'] == 'PASS':
    print(f"Image accepted with score: {result['data']['summary']['overall_score']}")
```

### cURL Examples
```bash
# Validate image
curl -X POST -F 'image=@photo.jpg' http://localhost:5000/api/validate

# Check system health
curl http://localhost:5000/api/health

# Get processing statistics  
curl http://localhost:5000/api/summary

# View validation rules
curl http://localhost:5000/api/validation-rules
```

---

## 📈 Performance Characteristics

- **Processing Time**: <2 seconds per image
- **Concurrent Requests**: Supports multiple simultaneous validations
- **Memory Usage**: Optimized for mobile image sizes
- **Acceptance Rate**: 35-40% for quality mobile photos
- **Supported Formats**: JPG, JPEG, PNG, HEIC, WebP
- **Maximum File Size**: 32MB

---

## 🔒 Security Considerations

- **File Type Validation**: Only image formats accepted
- **Size Limits**: 32MB maximum file size
- **Input Sanitization**: All uploads validated and sanitized
- **Temporary Storage**: Images automatically cleaned up
- **No Data Persistence**: Original images not permanently stored

---

**Documentation Version**: 2.0  
**API Version**: 2.0  
**Last Updated**: September 25, 2025