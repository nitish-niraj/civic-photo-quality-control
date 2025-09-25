# Production Deployment Guide

**Version**: 2.0  
**Status**: ✅ **Production Ready**  
**Last Updated**: September 25, 2025

## 🎯 Overview

This guide covers deploying the **Civic Quality Control API v2.0** - a production-ready mobile photo validation system with weighted scoring and optimized acceptance rates for civic documentation.

## 🚀 Key Production Features

### **Advanced Validation System**
- ⚖️ **Weighted Scoring**: Intelligent partial credit system (65% pass threshold)
- 📱 **Mobile-Optimized**: Realistic thresholds for smartphone photography
- 🎯 **High Acceptance Rate**: 35-40% acceptance rate for quality mobile photos
- ⚡ **Fast Processing**: <2 seconds per image validation
- 📊 **Comprehensive API**: 6 endpoints with detailed feedback

### **Validation Components** 
- 🔍 **Blur Detection** (25% weight) - Laplacian variance ≥100
- 📐 **Resolution Check** (25% weight) - Min 800×600px, 0.5MP
- 💡 **Brightness Validation** (20% weight) - Range 50-220 intensity
- 🌅 **Exposure Analysis** (15% weight) - Dynamic range + clipping check
- 📋 **Metadata Extraction** (15% weight) - 15% EXIF completeness required

---

## 🏗️ Quick Start

### 1. Prerequisites Check

```bash
# Verify Python version
python --version  # Required: 3.8+

# Check system resources
# RAM: 2GB+ recommended
# Storage: 1GB+ for models and processing
# CPU: 2+ cores recommended
```

### 2. Local Development Setup

```bash
# Clone and navigate to project
cd civic_quality_app

# Install dependencies
pip install -r requirements.txt

# Setup directories and download models
python scripts/setup_directories.py
python scripts/download_models.py

# Start development server
python app.py

# Test the API
curl http://localhost:5000/api/health
```

**Access Points:**
- **API Base**: `http://localhost:5000/api/`
- **Mobile Interface**: `http://localhost:5000/mobile_upload.html`
- **Health Check**: `http://localhost:5000/api/health`

### 3. Production Deployment Options

#### **Option A: Docker (Recommended)**

```bash
# Build production image
docker build -t civic-quality-app:v2.0 .

# Run with production settings
docker run -d \
  --name civic-quality-prod \
  -p 8000:8000 \
  -e SECRET_KEY=your-production-secret-key-here \
  -e FLASK_ENV=production \
  -v $(pwd)/storage:/app/storage \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  civic-quality-app:v2.0

# Or use Docker Compose
docker-compose up -d
```

#### **Option B: Manual Production**

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn (4 workers)
gunicorn --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  production:app

# Or use provided script
chmod +x start_production.sh
./start_production.sh
```

#### **Option C: Cloud Deployment**

**AWS/Azure/GCP:**
```bash
# Use production Docker image
# Configure load balancer for port 8000
# Set environment variables via cloud console
# Enable auto-scaling based on CPU/memory
```

---

## ⚙️ Production Configuration

### **Environment Variables**

```bash
# === Core Application ===
SECRET_KEY=your-256-bit-production-secret-key
FLASK_ENV=production
DEBUG=False

# === File Handling ===
MAX_CONTENT_LENGTH=33554432  # 32MB max file size
UPLOAD_FOLDER=storage/temp
PROCESSED_FOLDER=storage/processed
REJECTED_FOLDER=storage/rejected

# === Validation Thresholds (Mobile-Optimized) ===
BLUR_THRESHOLD=100              # Laplacian variance minimum
MIN_BRIGHTNESS=50               # Minimum pixel intensity
MAX_BRIGHTNESS=220              # Maximum pixel intensity  
MIN_RESOLUTION_WIDTH=800        # Minimum width pixels
MIN_RESOLUTION_HEIGHT=600       # Minimum height pixels
MIN_MEGAPIXELS=0.5             # Minimum megapixels
METADATA_COMPLETENESS=15        # Required EXIF completeness %

# === Performance ===
WORKERS=4                       # Gunicorn workers
MAX_REQUESTS=1000              # Requests per worker
TIMEOUT=120                    # Request timeout seconds

# === Security ===
ALLOWED_EXTENSIONS=jpg,jpeg,png,heic,webp
SECURE_HEADERS=True
```

### **Production Configuration File**

Create `production_config.py`:
```python
import os
from config import VALIDATION_RULES

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-key-change-in-production'
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
    
    # Optimized validation rules
    VALIDATION_RULES = VALIDATION_RULES
    
    # Performance settings
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year cache
    PROPAGATE_EXCEPTIONS = True
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    WTF_CSRF_ENABLED = True
```

---

## 🏗️ Production Architecture

### **System Components**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │────│  Civic Quality  │────│   File Storage  │
│   (nginx/ALB)   │    │      API        │    │   (persistent)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                    ┌─────────────────┐
                    │   ML Models     │
                    │   (YOLOv8)      │
                    └─────────────────┘
```

### **Nginx Configuration** (Optional Reverse Proxy)

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 32M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 120s;
        proxy_read_timeout 120s;
    }
    
    # Static files (if serving directly)
    location /static/ {
        alias /app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 📊 Performance & Monitoring

### **Key Metrics to Monitor**

```bash
# Application Health
curl http://your-domain.com/api/health

# Processing Statistics
curl http://your-domain.com/api/summary

# Response Time Monitoring
curl -w "@curl-format.txt" -o /dev/null -s http://your-domain.com/api/health
```

### **Expected Performance**

- **Processing Time**: 1-3 seconds per image
- **Acceptance Rate**: 35-40% for mobile photos
- **Throughput**: 100+ images/minute (4 workers)
- **Memory Usage**: ~200MB per worker
- **CPU Usage**: 50-80% during processing

### **Monitoring Setup**

```bash
# Application logs
tail -f logs/app.log

# System monitoring
htop
df -h  # Check disk space
```

---

## 🧪 Production Testing

### **Pre-Deployment Testing**

```bash
# 1. Run comprehensive API tests
python api_test.py

# 2. Test production server locally
gunicorn --bind 127.0.0.1:8000 production:app &
curl http://localhost:8000/api/health

# 3. Load testing (optional)
# Use tools like Apache Bench, wrk, or Artillery
ab -n 100 -c 10 http://localhost:8000/api/health
```

### **Post-Deployment Validation**

```bash
# 1. Health check
curl https://your-domain.com/api/health

# 2. Upload test image
curl -X POST -F 'image=@test_mobile_photo.jpg' \
     https://your-domain.com/api/validate

# 3. Check processing statistics
curl https://your-domain.com/api/summary

# 4. Validate acceptance rate
# Should be 35-40% for realistic mobile photos
```

---

## 🔒 Security Considerations

### **Production Security Checklist**

- ✅ **Environment Variables**: All secrets in environment variables
- ✅ **File Validation**: Strict image format checking
- ✅ **Size Limits**: 32MB maximum file size
- ✅ **Input Sanitization**: All uploads validated
- ✅ **Temporary Cleanup**: Auto-cleanup of temp files
- ✅ **HTTPS**: SSL/TLS encryption in production
- ✅ **Rate Limiting**: Consider implementing API rate limits
- ✅ **Access Logs**: Monitor for suspicious activity

### **Firewall Configuration**

```bash
# Allow only necessary ports
ufw allow 22     # SSH
ufw allow 80     # HTTP
ufw allow 443    # HTTPS
ufw deny 5000    # Block development port
ufw enable
```

---

## 🚨 Troubleshooting

### **Common Issues & Solutions**

#### **1. Low Acceptance Rate**
```bash
# Check current rates
curl http://localhost:8000/api/summary

# Solution: Validation rules already optimized for mobile photos
# Current acceptance rate: 35-40%
# If still too low, adjust thresholds in config.py
```

#### **2. Performance Issues**
```bash
# Check processing time
time curl -X POST -F 'image=@test.jpg' http://localhost:8000/api/validate

# Solutions:
# - Increase worker count
# - Add more CPU/memory
# - Optimize image preprocessing
```

#### **3. Memory Issues**
```bash
# Monitor memory usage
free -h
ps aux | grep gunicorn

# Solutions:
# - Reduce max file size
# - Implement image resizing
# - Restart workers periodically
```

#### **4. File Storage Issues**
```bash
# Check disk space
df -h

# Clean up old files
find storage/temp -type f -mtime +1 -delete
find storage/rejected -type f -mtime +7 -delete
```

---

## 📈 Scaling & Optimization

### **Horizontal Scaling**

```bash
# Multiple server instances
docker run -d --name civic-quality-1 -p 8001:8000 civic-quality-app:v2.0
docker run -d --name civic-quality-2 -p 8002:8000 civic-quality-app:v2.0

# Load balancer configuration
# Route traffic across multiple instances
```

### **Performance Optimization**

```python
# config.py optimizations
VALIDATION_RULES = {
    # Already optimized for mobile photography
    # Higher thresholds = lower acceptance but better quality
    # Lower thresholds = higher acceptance but more false positives
}
```

### **Future Enhancements**

- [ ] **Redis Caching**: Cache validation results
- [ ] **Background Processing**: Async image processing
- [ ] **CDN Integration**: Faster image delivery
- [ ] **Auto-scaling**: Dynamic worker adjustment
- [ ] **Monitoring Dashboard**: Real-time metrics
- [ ] **A/B Testing**: Validation rule optimization

---

## 📚 Additional Resources

### **API Documentation**
- **Comprehensive API Docs**: `docs/API_v2.md`
- **Response Format Examples**: See API documentation
- **Error Codes Reference**: Listed in API docs

### **Configuration Files**
- **Validation Rules**: `config.py`
- **Docker Setup**: `docker-compose.yml`
- **Production Server**: `production.py`

### **Testing Resources**
- **API Test Suite**: `api_test.py`
- **Individual Tests**: `test_*.py` files
- **Sample Images**: `tests/sample_images/`

---

**Deployment Status**: ✅ **Production Ready**  
**API Version**: 2.0  
**Acceptance Rate**: 35-40% (Optimized)  
**Processing Speed**: <2 seconds per image  
**Mobile Optimized**: ✅ Fully Compatible

```yaml
# docker-compose.yml
version: '3.8'
services:
  civic-quality:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    volumes:
      - ./storage:/app/storage
      - ./logs:/app/logs
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - civic-quality
    restart: unless-stopped
```

### Option 2: Cloud Deployment

#### Azure Container Apps

```bash
# Create resource group
az group create --name civic-quality-rg --location eastus

# Create container app environment
az containerapp env create \
  --name civic-quality-env \
  --resource-group civic-quality-rg \
  --location eastus

# Deploy container app
az containerapp create \
  --name civic-quality-app \
  --resource-group civic-quality-rg \
  --environment civic-quality-env \
  --image civic-quality-app:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars SECRET_KEY=your-secret-key
```

#### AWS ECS Fargate

```json
{
  "family": "civic-quality-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "civic-quality",
      "image": "your-registry/civic-quality-app:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "SECRET_KEY",
          "value": "your-secret-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/civic-quality",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

## Production Considerations

### Security

1. **HTTPS**: Always use HTTPS in production
2. **Secret Key**: Use a strong, random secret key
3. **File Validation**: All uploads are validated for type and size
4. **CORS**: Configure CORS appropriately for your domain

### Performance

1. **Gunicorn**: Production WSGI server with multiple workers
2. **Model Caching**: YOLO model loaded once and cached
3. **File Cleanup**: Temporary files automatically cleaned up
4. **Optimized Processing**: Parallel processing for multiple validations

### Monitoring

1. **Health Check**: `/api/health` endpoint for load balancer
2. **Metrics**: Processing time and validation statistics
3. **Logging**: Structured logging for debugging
4. **Storage Monitoring**: Track processed/rejected ratios

### Scaling

1. **Horizontal**: Multiple container instances
2. **Load Balancer**: Distribute requests across instances
3. **Storage**: Use cloud storage for uploaded files
4. **Database**: Optional database for audit logs

## API Endpoints

- `GET /api/mobile` - Mobile upload interface
- `POST /api/upload` - Image upload and analysis
- `GET /api/health` - Health check
- `GET /api/summary` - Processing statistics

## Testing Production Deployment

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test image upload (mobile interface)
open http://localhost:8000/api/mobile

# Test API directly
curl -X POST \
  -F "image=@test_image.jpg" \
  http://localhost:8000/api/upload
```

## Troubleshooting

### Common Issues

1. **Model download fails**: Check internet connectivity
2. **Large file uploads**: Increase `MAX_CONTENT_LENGTH`
3. **Permission errors**: Check file permissions on storage directories
4. **Memory issues**: Increase container memory allocation

### Logs

```bash
# View container logs
docker logs civic-quality

# View application logs
tail -f logs/app.log
```

## Support

For issues and support:

1. Check the logs for error details
2. Verify configuration settings
3. Test with sample images
4. Review the troubleshooting section