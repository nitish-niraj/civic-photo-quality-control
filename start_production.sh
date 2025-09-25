#!/bin/bash

# Production startup script for Civic Quality Control App
# This script sets up and starts the production environment

set -e

echo "🚀 Starting Civic Quality Control - Production Setup"
echo "================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p storage/temp storage/processed storage/rejected logs nginx/ssl

# Set environment variables
export SECRET_KEY=${SECRET_KEY:-$(openssl rand -hex 32)}
echo "🔐 Secret key configured"

# Build and start the application
echo "🏗️  Building and starting the application..."
docker-compose up --build -d

# Wait for the application to start
echo "⏳ Waiting for application to start..."
sleep 30

# Test the application
echo "🧪 Testing the application..."
python test_production.py --quick

# Show status
echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "🎉 Production deployment completed!"
echo "================================================="
echo "📱 Mobile Interface: http://localhost/api/mobile"
echo "🔍 Health Check: http://localhost/api/health"
echo "📊 API Documentation: http://localhost/api/summary"
echo ""
echo "📋 Management Commands:"
echo "  Stop:    docker-compose down"
echo "  Logs:    docker-compose logs -f"
echo "  Restart: docker-compose restart"
echo "  Test:    python test_production.py"
echo ""
echo "⚠️  For production use:"
echo "  1. Configure HTTPS with SSL certificates"
echo "  2. Set a secure SECRET_KEY environment variable"
echo "  3. Configure domain-specific CORS settings"
echo "  4. Set up monitoring and log aggregation"