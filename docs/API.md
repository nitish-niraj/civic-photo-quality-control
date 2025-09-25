# API Documentation

## Endpoints

### POST /check_quality

Upload an image for quality control assessment.

**Request:**
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
  "status": "PASS|FAIL",
  "checks": {
    "blur": {
      "value": 150.5,
      "status": "OK"
    },
    "brightness": {
      "value": 128.0,
      "status": "OK"
    },
    "resolution": {
      "value": "1920x1080",
      "status": "OK"
    }
  },
  "metadata": {
    "format": "JPEG",
    "size": [1920, 1080],
    "mode": "RGB"
  },
  "objects": []
}
```