@echo off
REM Production startup script for Civic Quality Control App (Windows)
REM This script sets up and starts the production environment

echo 🚀 Starting Civic Quality Control - Production Setup
echo =================================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please update Docker Desktop.
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist storage\temp mkdir storage\temp
if not exist storage\processed mkdir storage\processed
if not exist storage\rejected mkdir storage\rejected
if not exist logs mkdir logs
if not exist nginx\ssl mkdir nginx\ssl

REM Set environment variables if not already set
if not defined SECRET_KEY (
    echo 🔐 Generating secret key...
    set SECRET_KEY=change-this-in-production-windows
)

REM Build and start the application
echo 🏗️  Building and starting the application...
docker-compose up --build -d

REM Wait for the application to start
echo ⏳ Waiting for application to start...
timeout /t 30 /nobreak >nul

REM Test the application
echo 🧪 Testing the application...
python test_production.py --quick

REM Show status
echo.
echo 📊 Container Status:
docker-compose ps

echo.
echo 🎉 Production deployment completed!
echo =================================================
echo 📱 Mobile Interface: http://localhost/api/mobile
echo 🔍 Health Check: http://localhost/api/health
echo 📊 API Documentation: http://localhost/api/summary
echo.
echo 📋 Management Commands:
echo   Stop:    docker-compose down
echo   Logs:    docker-compose logs -f
echo   Restart: docker-compose restart
echo   Test:    python test_production.py
echo.
echo ⚠️  For production use:
echo   1. Configure HTTPS with SSL certificates
echo   2. Set a secure SECRET_KEY environment variable
echo   3. Configure domain-specific CORS settings
echo   4. Set up monitoring and log aggregation

pause