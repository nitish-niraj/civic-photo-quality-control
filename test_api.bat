@echo off
echo Testing Image Upload API
echo ========================

echo.
echo 1. Testing Health Endpoint...
curl -s http://localhost:5000/api/health

echo.
echo.
echo 2. Testing Image Upload...
curl -X POST -F "image=@C:\Users\kumar\OneDrive\Pictures\IMG_20220629_174412.jpg" http://localhost:5000/api/upload

echo.
echo.
echo 3. Testing Summary Endpoint...
curl -s http://localhost:5000/api/summary

echo.
echo.
echo Test completed!
pause