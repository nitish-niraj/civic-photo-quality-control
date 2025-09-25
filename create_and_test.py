#!/usr/bin/env python3
"""
Create a test image and demonstrate the full API
"""

from PIL import Image
import os
import requests
import json

def create_test_image():
    """Create a test image for API testing"""
    
    # Create a simple test image
    width, height = 1200, 800
    image = Image.new('RGB', (width, height), color='lightblue')
    
    # Add some simple content
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(image)
    
    # Draw some basic shapes
    draw.rectangle([100, 100, 300, 200], fill='red')
    draw.ellipse([400, 200, 600, 400], fill='green')
    draw.polygon([(700, 100), (800, 200), (900, 100)], fill='yellow')
    
    # Add text
    try:
        font = ImageFont.load_default()
        draw.text((50, 50), "Test Image for Civic Quality Control", fill='black', font=font)
        draw.text((50, 700), f"Resolution: {width}x{height}", fill='black', font=font)
    except:
        draw.text((50, 50), "Test Image for Civic Quality Control", fill='black')
        draw.text((50, 700), f"Resolution: {width}x{height}", fill='black')
    
    # Save the image
    test_image_path = 'test_image.jpg'
    image.save(test_image_path, 'JPEG', quality=85)
    
    print(f"✅ Created test image: {test_image_path}")
    print(f"📏 Resolution: {width}x{height}")
    print(f"📁 File size: {os.path.getsize(test_image_path)} bytes")
    
    return test_image_path

def test_api_with_image(image_path):
    """Test the API with the created image"""
    
    url = "http://localhost:5000/api/upload"
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(url, files=files)
            
        print(f"\n🌐 API Response:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful!")
            print(f"📊 Status: {result['data']['overall_status']}")
            print(f"⏱️ Processing time: {result['data']['processing_time_seconds']}s")
            
            # Pretty print the full response
            print(f"\n📋 Full Response:")
            print(json.dumps(result, indent=2))
            
        else:
            print(f"❌ Upload failed!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("📸 Testing Civic Quality Control API with Real Image")
    print("=" * 60)
    
    # Test with the user's actual image
    user_image_path = r"e:\niraj\IMG_20190410_101022.jpg"
    
    # Check if the image exists
    if os.path.exists(user_image_path):
        print(f"✅ Found image: {user_image_path}")
        print(f"📁 File size: {os.path.getsize(user_image_path)} bytes")
        
        # Test the API with the real image
        test_api_with_image(user_image_path)
    else:
        print(f"❌ Image not found: {user_image_path}")
        print("📝 Creating a test image instead...")
        
        # Fallback: Create test image
        image_path = create_test_image()
        test_api_with_image(image_path)
        
        print(f"\n🧹 Cleaning up...")
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"✅ Removed temporary test image")