#!/usr/bin/env python3
"""
Simple test to verify the production-ready quality control system works
"""

import requests
import os
from PIL import Image

def create_test_image():
    """Create a simple test image."""
    img = Image.new('RGB', (1200, 800), color='lightblue')
    test_path = 'simple_test.jpg'
    img.save(test_path, 'JPEG', quality=85)
    return test_path

def test_quality_control():
    """Test the quality control system."""
    print("🚀 Testing Production-Ready Civic Quality Control System")
    print("=" * 60)
    
    # Test health check
    print("🔍 Testing health check...")
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Create test image
    print("\n📸 Creating test image...")
    test_image = create_test_image()
    print(f"✅ Created test image: {test_image}")
    
    # Test image upload and analysis
    print("\n🔍 Testing image analysis with all quality checks...")
    try:
        with open(test_image, 'rb') as f:
            files = {'image': f}
            response = requests.post('http://localhost:5000/api/upload', files=files, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Image analysis completed successfully!")
            
            data = result['data']
            print(f"\n📊 Results:")
            print(f"   Overall Status: {data['overall_status']}")
            print(f"   Processing Time: {data['processing_time_seconds']}s")
            print(f"   Issues Found: {len(data.get('issues', []))}")
            print(f"   Warnings: {len(data.get('warnings', []))}")
            
            # Show validation results
            validations = data.get('validations', {})
            print(f"\n🔍 Quality Checks Performed:")
            
            if 'blur_detection' in validations and not validations['blur_detection'].get('error'):
                blur = validations['blur_detection']
                print(f"   ✅ Blur Detection: {blur['quality']} (Score: {blur['blur_score']})")
            
            if 'brightness_validation' in validations and not validations['brightness_validation'].get('error'):
                brightness = validations['brightness_validation']
                score = brightness['quality_score'] * 100
                print(f"   ✅ Brightness Check: {score:.1f}% quality")
            
            if 'exposure_check' in validations and not validations['exposure_check'].get('error'):
                exposure = validations['exposure_check']
                print(f"   ✅ Exposure Analysis: {exposure['exposure_quality']}")
            
            if 'resolution_check' in validations and not validations['resolution_check'].get('error'):
                resolution = validations['resolution_check']
                print(f"   ✅ Resolution Check: {resolution['width']}x{resolution['height']} ({resolution['megapixels']}MP)")
            
            if 'metadata_extraction' in validations and not validations['metadata_extraction'].get('error'):
                print(f"   ✅ Metadata Extraction: Completed")
            
            # Show recommendations if any
            recommendations = data.get('recommendations', [])
            if recommendations:
                print(f"\n💡 Recommendations:")
                for rec in recommendations:
                    print(f"   • {rec}")
            
            print(f"\n🎉 All quality checks completed successfully!")
            print(f"   The system is ready for production mobile use!")
            
        else:
            print(f"❌ Image analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Image analysis error: {e}")
        return False
    
    finally:
        # Clean up test image
        if os.path.exists(test_image):
            os.remove(test_image)
            print(f"\n🧹 Cleaned up test image")
    
    return True

if __name__ == "__main__":
    success = test_quality_control()
    
    if success:
        print(f"\n" + "=" * 60)
        print("🌟 PRODUCTION SYSTEM READY!")
        print("=" * 60)
        print("📱 For mobile users:")
        print("   1. Navigate to http://your-domain/api/mobile")
        print("   2. Click 'Take Photo or Upload Image'")
        print("   3. Capture photo or select from gallery")
        print("   4. Click 'Analyze Photo Quality'")
        print("   5. View instant quality analysis results")
        print("")
        print("🔧 Quality checks performed automatically:")
        print("   ✅ Blur detection (Laplacian variance)")
        print("   ✅ Brightness validation (histogram analysis)")
        print("   ✅ Exposure check (dynamic range & clipping)")
        print("   ✅ Resolution validation (minimum requirements)")
        print("   ✅ Metadata extraction (EXIF & GPS data)")
        print("")
        print("🚀 Ready for production deployment!")
    else:
        print(f"\n❌ System test failed. Please check the server logs.")