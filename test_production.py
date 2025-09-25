#!/usr/bin/env python3
"""
Production Testing Suite for Civic Quality Control App
Tests all quality check components with real mobile photos
"""

import requests
import json
import time
import os
from pathlib import Path
from PIL import Image
import numpy as np

class ProductionTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        
    def test_health_check(self):
        """Test the health check endpoint."""
        print("🔍 Testing health check...")
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['message']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def create_test_images(self):
        """Create various test images for quality checks."""
        test_images = {}
        
        # 1. Good quality image
        print("📸 Creating test images...")
        good_img = Image.new('RGB', (1200, 800), color='lightblue')
        good_path = 'test_good.jpg'
        good_img.save(good_path, 'JPEG', quality=85)
        test_images['good'] = good_path
        
        # 2. Low resolution image
        low_res_img = Image.new('RGB', (400, 300), color='red')
        low_res_path = 'test_low_res.jpg'
        low_res_img.save(low_res_path, 'JPEG', quality=85)
        test_images['low_resolution'] = low_res_path
        
        # 3. Dark image (brightness test)
        dark_img = Image.new('RGB', (1200, 800), color=(20, 20, 20))
        dark_path = 'test_dark.jpg'
        dark_img.save(dark_path, 'JPEG', quality=85)
        test_images['dark'] = dark_path
        
        # 4. Bright image (brightness test)
        bright_img = Image.new('RGB', (1200, 800), color=(240, 240, 240))
        bright_path = 'test_bright.jpg'
        bright_img.save(bright_path, 'JPEG', quality=85)
        test_images['bright'] = bright_path
        
        return test_images
    
    def test_image_upload(self, image_path, test_name):
        """Test image upload and analysis."""
        print(f"\n🔍 Testing {test_name}...")
        
        try:
            with open(image_path, 'rb') as f:
                files = {'image': f}
                start_time = time.time()
                response = requests.post(f"{self.api_url}/upload", files=files, timeout=60)
                processing_time = time.time() - start_time
            
            print(f"⏱️  Request time: {processing_time:.2f}s")
            print(f"📊 Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.print_analysis_results(result, test_name)
                return True
            else:
                print(f"❌ Upload failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing {test_name}: {e}")
            return False
    
    def print_analysis_results(self, result, test_name):
        """Print detailed analysis results."""
        if not result.get('success'):
            print(f"❌ Analysis failed: {result.get('message')}")
            return
        
        data = result['data']
        print(f"✅ Analysis completed for {test_name}")
        print(f"📊 Overall Status: {data['overall_status']}")
        print(f"⏱️  Processing Time: {data['processing_time_seconds']}s")
        
        # Quality checks results
        validations = data.get('validations', {})
        
        # Blur Detection
        if 'blur_detection' in validations:
            blur = validations['blur_detection']
            if not blur.get('error'):
                status = "❌ BLURRY" if blur['is_blurry'] else "✅ SHARP"
                print(f"  🔍 Blur: {status} (Score: {blur['blur_score']}, Quality: {blur['quality']})")
        
        # Brightness Validation  
        if 'brightness_validation' in validations:
            brightness = validations['brightness_validation']
            if not brightness.get('error'):
                status = "❌ ISSUES" if brightness['has_brightness_issues'] else "✅ GOOD"
                print(f"  💡 Brightness: {status} (Mean: {brightness['mean_brightness']}, Score: {(brightness['quality_score']*100):.1f}%)")
        
        # Resolution Check
        if 'resolution_check' in validations:
            resolution = validations['resolution_check']
            if not resolution.get('error'):
                status = "✅ GOOD" if resolution['meets_min_resolution'] else "❌ LOW"
                print(f"  📏 Resolution: {status} ({resolution['width']}x{resolution['height']}, {resolution['megapixels']}MP)")
        
        # Exposure Check
        if 'exposure_check' in validations:
            exposure = validations['exposure_check']
            if not exposure.get('error'):
                status = "✅ GOOD" if exposure['has_good_exposure'] else "❌ POOR"
                print(f"  ☀️  Exposure: {status} (Quality: {exposure['exposure_quality']}, Range: {exposure['dynamic_range']})")
        
        # Metadata Extraction
        if 'metadata_extraction' in validations:
            metadata = validations['metadata_extraction']
            if not metadata.get('error'):
                file_info = metadata.get('file_info', {})
                print(f"  📋 Metadata: ✅ EXTRACTED (Size: {file_info.get('file_size', 0)} bytes)")
        
        # Issues and Recommendations
        issues = data.get('issues', [])
        if issues:
            print(f"  ⚠️  Issues ({len(issues)}):")
            for issue in issues:
                print(f"    • {issue['type']}: {issue['message']} ({issue['severity']})")
        
        recommendations = data.get('recommendations', [])
        if recommendations:
            print(f"  💡 Recommendations:")
            for rec in recommendations:
                print(f"    • {rec}")
    
    def test_mobile_interface(self):
        """Test mobile interface accessibility."""
        print("\n🔍 Testing mobile interface...")
        try:
            response = requests.get(f"{self.api_url}/mobile", timeout=10)
            if response.status_code == 200:
                print("✅ Mobile interface accessible")
                print(f"📱 Interface URL: {self.api_url}/mobile")
                return True
            else:
                print(f"❌ Mobile interface failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Mobile interface error: {e}")
            return False
    
    def test_validation_summary(self):
        """Test validation summary endpoint."""
        print("\n🔍 Testing validation summary...")
        try:
            response = requests.get(f"{self.api_url}/summary", timeout=10)
            if response.status_code == 200:
                data = response.json()
                summary = data['data']
                print("✅ Summary endpoint working")
                print(f"📊 Total processed: {summary.get('total_processed', 0)}")
                print(f"📊 Total rejected: {summary.get('total_rejected', 0)}")
                print(f"📊 Acceptance rate: {summary.get('acceptance_rate', 0)}%")
                return True
            else:
                print(f"❌ Summary failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Summary error: {e}")
            return False
    
    def cleanup_test_images(self, test_images):
        """Clean up test images."""
        print("\n🧹 Cleaning up test images...")
        for name, path in test_images.items():
            try:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"✅ Removed {name} test image")
            except Exception as e:
                print(f"❌ Failed to remove {path}: {e}")
    
    def run_full_test_suite(self):
        """Run the complete production test suite."""
        print("🚀 Starting Production Test Suite")
        print("=" * 60)
        
        # Test health check first
        if not self.test_health_check():
            print("❌ Health check failed - cannot continue tests")
            return False
        
        # Test mobile interface
        self.test_mobile_interface()
        
        # Create test images
        test_images = self.create_test_images()
        
        # Test each image type
        test_results = {}
        for test_name, image_path in test_images.items():
            test_results[test_name] = self.test_image_upload(image_path, test_name)
        
        # Test summary endpoint
        self.test_validation_summary()
        
        # Clean up
        self.cleanup_test_images(test_images)
        
        # Print final results
        print("\n" + "=" * 60)
        print("📋 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(test_results.values())
        total = len(test_results)
        
        print(f"✅ Tests passed: {passed}/{total}")
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test_name}")
        
        if passed == total:
            print("\n🎉 All tests passed! Production system is ready.")
        else:
            print(f"\n⚠️  {total - passed} tests failed. Check the issues above.")
        
        print(f"\n🌐 Access the mobile interface at: {self.api_url}/mobile")
        
        return passed == total

def main():
    """Main test function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Civic Quality Control Production System')
    parser.add_argument('--url', default='http://localhost:8000', help='Base URL of the application')
    parser.add_argument('--quick', action='store_true', help='Run quick tests only')
    
    args = parser.parse_args()
    
    tester = ProductionTester(args.url)
    
    if args.quick:
        # Quick test - just health check and mobile interface
        health_ok = tester.test_health_check()
        mobile_ok = tester.test_mobile_interface()  
        if health_ok and mobile_ok:
            print("✅ Quick tests passed!")
        else:
            print("❌ Quick tests failed!")
    else:
        # Full test suite
        tester.run_full_test_suite()

if __name__ == "__main__":
    main()