---
title: PhotoGuard API
emoji: 🛡️
colorFrom: gray
colorTo: gray
sdk: docker
pinned: false
license: mit
---

# PhotoGuard API 🛡️

Professional image quality validation system with automated blur detection, brightness analysis, resolution checking, exposure verification, and metadata extraction.

## 🚀 Key Features

- **🎨 Modern UI**: Clean monochrome interface with black/white/gray theme
- **📚 Interactive Documentation**: Complete Swagger UI and ReDoc API documentation
- **📱 Mobile-Optimized**: Realistic validation thresholds for mobile photography
- **⚖️ Weighted Scoring System**: Intelligent partial credit with 65% pass threshold
- **🎯 High Acceptance Rate**: 35-40% acceptance rate for quality images
- **📊 Comprehensive API**: RESTful API with OpenAPI 3.1 specification
- **⚡ Real-time Processing**: Instant validation with detailed feedback
- **🔍 Multi-layer Validation**: 5 automated quality checks

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

- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/nitish-niraj/civic-photo-quality-control.git
cd civic-photo-quality-control

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
# Start development server (auto-creates storage directories)
python app.py

# Access the application
# Web UI: http://localhost:5000
# Swagger UI: http://localhost:5000/api/docs
# ReDoc: http://localhost:5000/api/redoc
```

## 📚 API Documentation

### Interactive Documentation

PhotoGuard provides comprehensive API documentation through multiple interfaces:

| Documentation | URL | Description |
|--------------|-----|-------------|
| **Swagger UI** | `/api/docs` | Interactive testing interface with live API execution |
| **ReDoc** | `/api/redoc` | Clean, comprehensive API reference with schemas |
| **OpenAPI Spec** | `/api/openapi.json` | Complete OpenAPI 3.1 specification (JSON) |

**Local URLs:**
- Swagger UI: http://localhost:5000/api/docs
- ReDoc: http://localhost:5000/api/redoc
- OpenAPI: http://localhost:5000/api/openapi.json

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



## 🏗️ Production Deployment

### Docker Deployment

```bash
# Build production image
docker build -t photoguard-api .

# Run container
docker run -d -p 5000:5000 --name photoguard photoguard-api

# Access production app
# http://localhost:5000
```

### Deployment to Hugging Face Spaces

PhotoGuard can be deployed to **Hugging Face Spaces** (not Models) as it's a web application with UI and API endpoints.

#### Step 1: Create a Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - **Space name**: `photoguard-api` (or your preferred name)
   - **SDK**: Docker
   - **Space hardware**: CPU basic (free tier works fine)

#### Step 2: Prepare Your Repository

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/photoguard-api
cd photoguard-api

# Copy PhotoGuard files
cp -r /path/to/civic_quality_app/* .
```

#### Step 3: Create README.md for Spaces

Add this header to your README.md:

```markdown
---
title: PhotoGuard API
emoji: 🛡️
colorFrom: black
colorTo: gray
sdk: docker
pinned: false
---
```

#### Step 4: Deploy

```bash
# Add all files
git add .

# Commit changes
git commit -m "Deploy PhotoGuard API to Hugging Face Spaces"

# Push to Hugging Face
git push
```

#### Environment Variables (Optional)

If you need to set environment variables in your Space:
1. Go to Space Settings → Variables and secrets
2. Add variables like:
   - `SECRET_KEY`: Your Flask secret key
   - `MAX_CONTENT_LENGTH`: Maximum upload size

#### Access Your Deployed API

Once deployed, your Space will be available at:
- **UI**: `https://huggingface.co/spaces/YOUR_USERNAME/photoguard-api`
- **API**: `https://YOUR_USERNAME-photoguard-api.hf.space/api/validate`
- **Swagger**: `https://YOUR_USERNAME-photoguard-api.hf.space/api/docs`
- **ReDoc**: `https://YOUR_USERNAME-photoguard-api.hf.space/api/redoc`

### Manual Server Deployment

```bash
# Install production dependencies
pip install -r requirements.txt gunicorn

# Run with Gunicorn (production WSGI server)
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
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
├── app.py                          # Flask application entry point
├── config.py                       # Configuration & validation rules
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker container definition
├── .dockerignore                   # Docker ignore patterns
├── .gitignore                      # Git ignore patterns
│
├── app/                            # Core application package
│   ├── __init__.py                # App factory
│   ├── api_spec.py                # OpenAPI 3.1 specification
│   ├── routes/
│   │   └── upload.py              # API endpoints & documentation routes
│   ├── services/
│   │   └── quality_control.py     # Validation orchestration
│   └── utils/                     # Validation utilities
│       ├── blur_detection.py      # Laplacian variance analysis
│       ├── brightness_validation.py # Pixel intensity check
│       ├── exposure_check.py      # Dynamic range analysis
│       ├── resolution_check.py    # Dimension validation
│       ├── metadata_extraction.py # EXIF data extraction
│       └── response_formatter.py  # API response formatting
│
├── templates/                      # HTML templates
│   ├── index.html                 # Main UI (monochrome theme)
│   ├── swagger.html               # Swagger UI documentation
│   └── redoc.html                 # ReDoc API reference
│
├── storage/                        # Auto-created storage directories
│   ├── temp/                      # Temporary uploads
│   ├── processed/                 # Accepted images
│   └── rejected/                  # Failed images
│
└── tests/                         # Test suite
    ├── conftest.py                # Test configuration
    ├── test_api_endpoints.py      # API tests
    ├── test_blur_detection.py     # Blur detection tests
    └── sample_images/             # Test images
        ├── blurry/
        ├── dark/
        ├── good/
        └── low_res/
```

## 🧪 Testing

### API Testing

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Validate an image
curl -X POST -F 'image=@test.jpg' http://localhost:5000/api/validate

# Get validation rules
curl http://localhost:5000/api/validation-rules

# Get processing statistics
curl http://localhost:5000/api/summary
```

### Unit Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
pytest tests/test_blur_detection.py
pytest tests/test_api_endpoints.py

# Run with verbose output
pytest -v tests/
```

## 📊 Monitoring & Analytics

### Processing Statistics

Track validation metrics through the `/api/summary` endpoint:

```bash
# Get processing statistics
curl http://localhost:5000/api/summary

# Pretty print with jq
curl http://localhost:5000/api/summary | jq '.data'
```

**Available Metrics:**
- Total images processed
- Pass/fail counts
- Acceptance rate (~35-40%)
- Average quality scores
- Common rejection reasons

## 🔧 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/Mac

# Use a different port
export FLASK_RUN_PORT=8000
python app.py
```

**2. Storage Directory Errors**
- Storage directories are auto-created on startup
- Ensure write permissions in the application directory

**3. Image Upload Fails**
- Check file size (max 16MB by default)
- Verify file format (jpg, jpeg, png, bmp, tiff)
- Check `MAX_CONTENT_LENGTH` in config.py

**4. Low Acceptance Rate**
- Review validation thresholds in `config.py`
- Current system targets 35-40% acceptance for quality images
- Adjust `VALIDATION_RULES` if needed

**5. API Documentation Not Loading**
- Ensure Flask server is running
- Check browser console for errors
- Try accessing OpenAPI spec directly: `/api/openapi.json`

### Getting Help

- **Issues**: https://github.com/nitish-niraj/civic-photo-quality-control/issues
- **API Docs**: Use `/api/docs` for interactive testing
- **Logs**: Check Flask console output for errors

## 🎨 UI Features

### Modern Interface

- **Monochrome Theme**: Professional black/white/gray color scheme
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Drag & Drop Upload**: Easy file upload with visual feedback
- **Real-time Results**: Instant validation feedback with detailed scores
- **Interactive Documentation**: Built-in Swagger UI and ReDoc access

### Navigation Sections

1. **Home**: Upload and validate images
2. **How It Works**: 3-step validation process explanation
3. **API Docs**: Interactive API documentation access

## 📈 Technical Highlights

### Performance

- **Processing Speed**: < 2 seconds per image
- **Supported Formats**: JPG, JPEG, PNG, BMP, TIFF
- **Max Upload Size**: 16MB (configurable)
- **Concurrent Requests**: Supported via WSGI server

### Validation Accuracy

- **Blur Detection**: Laplacian variance (min: 100)
- **Brightness Range**: 50-220 pixel intensity
- **Resolution**: Min 800×600 pixels, 0.5MP
- **Exposure**: Dynamic range ≥100, clipping ≤2%
- **Metadata**: 15% completeness minimum

### API Specifications

- **Protocol**: REST API over HTTP
- **Format**: JSON request/response
- **Documentation**: OpenAPI 3.1
- **Authentication**: None (add as needed)
- **CORS**: Configurable

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available for use and modification.

## 🔗 Links

- **GitHub**: https://github.com/nitish-niraj/civic-photo-quality-control
- **Issues**: https://github.com/nitish-niraj/civic-photo-quality-control/issues

---

**Version**: 3.0.0  
**Last Updated**: November 3, 2025  
**Status**: ✅ Production Ready  
**Deployment**: Docker, Hugging Face Spaces, Manual Server