@echo off
REM Civic Quality Control API Test Script
REM Tests all API endpoints with curl commands

echo.
echo ========================================
echo   Civic Quality Control API Testing
echo ========================================
echo.

set API_BASE=http://localhost:5000/api

echo Testing if server is running...
curl -s %API_BASE%/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Server not running! Please start the server first:
    echo    python app.py
    echo    Or: python production.py
    pause
    exit /b 1
)

echo ✅ Server is running!
echo.

REM Test 1: Health Check
echo ==================== Health Check ====================
curl -X GET %API_BASE%/health
echo.
echo.

REM Test 2: Validation Rules
echo ================= Validation Rules ===================
curl -X GET %API_BASE%/validation-rules
echo.
echo.

REM Test 3: API Information
echo ================== API Information ===================
curl -X GET %API_BASE%/test-api
echo.
echo.

REM Test 4: Processing Summary
echo ================= Processing Summary ==================
curl -X GET %API_BASE%/summary
echo.
echo.

REM Test 5: Image Validation (if test image exists)
echo ================= Image Validation ====================
if exist "storage\temp\7db56d0e-ff94-49ca-b61a-5f33469fe4af_IMG_20220629_174412.jpg" (
    echo Testing with existing image...
    curl -X POST -F "image=@storage\temp\7db56d0e-ff94-49ca-b61a-5f33469fe4af_IMG_20220629_174412.jpg" %API_BASE%/validate
) else (
    echo ⚠️ No test image found in storage\temp\
    echo Please add an image to test validation endpoint
)
echo.
echo.

echo ================================================
echo                 API Test Complete
echo ================================================
echo.
echo 💡 Manual Testing Commands:
echo    Health: curl %API_BASE%/health
echo    Rules:  curl %API_BASE%/validation-rules
echo    Upload: curl -X POST -F "image=@your_image.jpg" %API_BASE%/validate
echo    Summary: curl %API_BASE%/summary
echo.
pause