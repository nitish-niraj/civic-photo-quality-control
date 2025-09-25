# Civic Quality Control API

A production-ready mobile photo validation system for civic documentation with intelligent quality control and comprehensive API endpoints.

## 🚀 Key Features

- **📱 Mobile-Optimized**: Designed specifically for mobile photography with realistic validation thresholds
- **⚖️ Weighted Scoring System**: Intelligent partial credit system with 65% pass threshold
- **🎯 High Acceptance Rate**: Optimized to achieve 35-40% acceptance rate for quality mobile photos
- **📊 Comprehensive API**: Full REST API with health checks, validation, and statistics
- **⚡ Real-time Processing**: Instant image validation with detailed feedback
- **🔍 Multi-layer Validation**: Blur, brightness, resolution, exposure, and metadata analysis

## 📊 Performance Metrics

- **Acceptance Rate**: 35-40% (optimized for mobile photography)
- **Processing Speed**: < 2 seconds per image
- **Supported Formats**: JPG, JPEG, PNG, HEIC, WebP
- **Mobile-Friendly**: Works seamlessly with smartphone cameras

## 🏗️ System Architecture

### Core Validation Pipeline

1. **Blur Detection** (25% weight) - Laplacian variance analysis
2. **Resolution Check** (25% weight) - Minimum 800×600 pixels, 0.5MP
3. **Brightness Validation** (20% weight) - Range 50-220 pixel intensity
4. **Exposure Analysis** (15% weight) - Dynamic range and clipping detection
5. **Metadata Extraction** (15% weight) - EXIF data analysis (15% completeness required)

### Weighted Scoring System

- **Pass Threshold**: 65% overall score
- **Partial Credit**: Failed checks don't automatically reject images
- **Quality Levels**: Poor (0-40%), Fair (40-65%), Good (65-85%), Excellent (85%+)

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8+
python --version

# Install dependencies
pip install -r requirements.txt
```

### Setup & Run

```bash
# Setup directories and download models
python scripts/setup_directories.py
python scripts/download_models.py

# Start development server
python app.py

# Access mobile interface
# http://localhost:5000/mobile_upload.html
```

## 📱 API Endpoints

### Core Endpoints

#### 1. Health Check
```bash
GET /api/health
```
Returns system status and validation rule version.

#### 2. Image Validation (Primary)
```bash
POST /api/validate
Content-Type: multipart/form-data
Body: image=@your_photo.jpg
```

**Response Format:**
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
        "status": "PASS",
        "score": 95.0,
        "message": "Image sharpness is excellent",
        "details": { "variance": 245.6, "threshold": 100 }
      },
      "resolution": {
        "status": "PASS", 
        "score": 100.0,
        "message": "Resolution exceeds requirements",
        "details": { "width": 1920, "height": 1080, "megapixels": 2.07 }
      },
      "brightness": {
        "status": "PASS",
        "score": 80.0,
        "message": "Brightness is within acceptable range",
        "details": { "mean_intensity": 142.3, "range": [50, 220] }
      },
      "exposure": {
        "status": "PASS",
        "score": 90.0,
        "message": "Exposure and dynamic range are good",
        "details": { "dynamic_range": 128, "clipping_percentage": 0.5 }
      },
      "metadata": {
        "status": "PASS",
        "score": 60.0,
        "message": "Sufficient metadata extracted", 
        "details": { "completeness": 45, "required": 15 }
      }
    },
    "recommendations": [
      "Consider reducing brightness slightly for optimal quality"
    ]
  },
  "message": "Image validation completed successfully"
}
```

#### 3. Processing Statistics
```bash
GET /api/summary
```
Returns acceptance rates and processing statistics.

#### 4. Validation Rules
```bash
GET /api/validation-rules
```
Returns current validation thresholds and requirements.

### Testing Endpoints

#### 5. API Information  
```bash
GET /api/test-api
```

#### 6. Legacy Upload (Deprecated)
```bash
POST /api/upload
```

## 🏗️ Production Deployment

### Docker Deployment (Recommended)

```bash
# Build production image
docker build -t civic-quality-app .

# Run with Docker Compose
docker-compose up -d

# Access production app
# http://localhost:8000
```

### Manual Deployment

```bash
# Install production dependencies
pip install -r requirements.txt gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 production:app

# Or use production script
chmod +x start_production.sh
./start_production.sh
```

## ⚙️ Configuration

### Environment Variables

```bash
# Core settings
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
MAX_CONTENT_LENGTH=33554432  # 32MB

# File storage
UPLOAD_FOLDER=storage/temp
PROCESSED_FOLDER=storage/processed  
REJECTED_FOLDER=storage/rejected

# Validation thresholds (mobile-optimized)
BLUR_THRESHOLD=100
MIN_BRIGHTNESS=50
MAX_BRIGHTNESS=220
MIN_RESOLUTION_WIDTH=800
MIN_RESOLUTION_HEIGHT=600
MIN_MEGAPIXELS=0.5
METADATA_COMPLETENESS=15
```

### Validation Rules (Mobile-Optimized)

```python
VALIDATION_RULES = {
    "blur": {
        "min_score": 100,           # Laplacian variance threshold
        "levels": {
            "poor": 0,
            "acceptable": 100,
            "excellent": 300
        }
    },
    "brightness": {
        "range": [50, 220],         # Pixel intensity range
        "quality_score_min": 60     # Minimum quality percentage
    },
    "resolution": {
        "min_width": 800,           # Minimum width in pixels  
        "min_height": 600,          # Minimum height in pixels
        "min_megapixels": 0.5,      # Minimum megapixels
        "recommended_megapixels": 2
    },
    "exposure": {
        "min_score": 100,           # Dynamic range threshold
        "acceptable_range": [80, 150],
        "check_clipping": {
            "max_percentage": 2     # Maximum clipped pixels %
        }
    },
    "metadata": {
        "min_completeness_percentage": 15,  # Only 15% required
        "required_fields": [
            "timestamp", "camera_make_model", "orientation",
            "iso", "shutter_speed", "aperture"
        ]
    }
}
```

## 📁 Project Structure

```
civic_quality_app/
├── app.py                      # Development server
├── production.py               # Production WSGI app
├── config.py                   # Configuration & validation rules
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container definition
│
├── app/                        # Application package
│   ├── routes/
│   │   └── upload.py          # API route handlers
│   ├── services/
│   │   └── quality_control.py # Core validation logic
│   └── utils/                 # Validation utilities
│       ├── blur_detection.py
│       ├── brightness_validation.py
│       ├── exposure_check.py
│       ├── resolution_check.py
│       ├── metadata_extraction.py
│       └── object_detection.py
│
├── storage/                    # File storage
│   ├── temp/                  # Temporary uploads
│   ├── processed/             # Accepted images
│   └── rejected/              # Rejected images
│
├── templates/
│   └── mobile_upload.html     # Mobile web interface
│
├── tests/                     # Test suites
├── docs/                      # Documentation
├── scripts/                   # Setup scripts
└── logs/                      # Application logs
```

## 🧪 Testing

### Comprehensive API Testing

```bash
# Run full API test suite
python api_test.py

# Test specific endpoints
curl http://localhost:5000/api/health
curl -X POST -F 'image=@test.jpg' http://localhost:5000/api/validate
curl http://localhost:5000/api/summary
```

### Unit Testing

```bash
# Run validation tests
python -m pytest tests/

# Test specific components
python test_blur_detection.py
python test_brightness_validation.py
```

## 📊 Monitoring & Analytics

### Processing Statistics

- **Total Images Processed**: Track via `/api/summary`
- **Acceptance Rate**: Current rate ~35-40%
- **Common Rejection Reasons**: Available in logs and statistics
- **Processing Performance**: Response time monitoring

### Log Analysis

```bash
# Check application logs
tail -f logs/app.log

# Monitor processing stats
curl http://localhost:5000/api/summary | jq '.data'
```

## 🔧 Troubleshooting

### Common Issues

1. **Low Acceptance Rate**
   - Check if validation rules are too strict
   - Review mobile photo quality expectations
   - Adjust thresholds in `config.py`

2. **Performance Issues**
   - Monitor memory usage for large images
   - Consider image resizing for very large uploads
   - Check model loading performance

3. **Deployment Issues**
   - Verify all dependencies installed
   - Check file permissions for storage directories
   - Ensure models are downloaded correctly

### Support

For issues and improvements:
1. Check logs in `logs/` directory
2. Test individual validation components
3. Review configuration in `config.py`
4. Use API testing tools for debugging

## 📈 Performance Optimization

### Current Optimizations

- **Mobile-Friendly Rules**: Relaxed thresholds for mobile photography
- **Weighted Scoring**: Intelligent partial credit system
- **Efficient Processing**: Optimized validation pipeline
- **Smart Caching**: Model loading optimization

### Future Enhancements

- [ ] Real-time processing optimization
- [ ] Advanced object detection integration
- [ ] GPS metadata validation
- [ ] Batch processing capabilities
- [ ] API rate limiting
- [ ] Enhanced mobile UI

---

**Version**: 2.0  
**Last Updated**: September 25, 2025  
**Production Status**: ✅ Ready for deployment