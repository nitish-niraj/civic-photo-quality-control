#!/usr/bin/env python3
"""
API Test Script for Civic Quality Control App
Demonstrates how to test the updated validation API endpoints.
"""

import requests
import json
import os
import sys
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:5000/api"
TEST_IMAGE_PATH = "storage/temp/7db56d0e-ff94-49ca-b61a-5f33469fe4af_IMG_20220629_174412.jpg"

def test_health_endpoint():
    """Test the health check endpoint."""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_validation_rules_endpoint():
    """Test the validation rules endpoint."""
    print("\n🔍 Testing Validation Rules Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/validation-rules")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            rules = response.json()
            print("✅ Validation Rules Retrieved:")
            print(json.dumps(rules, indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Validation rules test failed: {e}")
        return False

def test_api_info_endpoint():
    """Test the API information endpoint."""
    print("\n🔍 Testing API Information Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/test-api")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            info = response.json()
            print("✅ API Information Retrieved:")
            print(f"API Version: {info['data']['api_version']}")
            print(f"Available Endpoints: {len(info['data']['endpoints'])}")
            print("\nEndpoints:")
            for endpoint, description in info['data']['endpoints'].items():
                print(f"  {endpoint}: {description}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API info test failed: {e}")
        return False

def test_image_validation_endpoint():
    """Test the main image validation endpoint."""
    print("\n🔍 Testing Image Validation Endpoint...")
    
    # Check if test image exists
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"❌ Test image not found: {TEST_IMAGE_PATH}")
        print("Please ensure you have an image in the storage/temp folder or update TEST_IMAGE_PATH")
        return False
    
    try:
        # Prepare file for upload
        with open(TEST_IMAGE_PATH, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{API_BASE_URL}/validate", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Image Validation Completed!")
            
            # Extract key information
            data = result['data']
            summary = data['summary']
            checks = data['checks']
            
            print(f"\n📊 Overall Status: {summary['overall_status'].upper()}")
            print(f"📊 Overall Score: {summary['overall_score']}")
            print(f"📊 Issues Found: {summary['issues_found']}")
            
            # Show validation results
            print("\n📋 Validation Results:")
            for check_type, check_result in checks.items():
                if check_result:
                    status = "✅ PASS" if check_result.get('status') == 'pass' else "❌ FAIL"
                    reason = check_result.get('reason', 'unknown')
                    print(f"  {check_type}: {status} - {reason}")
            
            # Show recommendations if any
            if summary['recommendations']:
                print(f"\n💡 Recommendations ({len(summary['recommendations'])}):")
                for rec in summary['recommendations']:
                    print(f"  - {rec}")
                    
        else:
            print(f"❌ Validation failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Image validation test failed: {e}")
        return False

def test_summary_endpoint():
    """Test the processing summary endpoint."""
    print("\n🔍 Testing Summary Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/summary")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            summary = response.json()
            print("✅ Processing Summary Retrieved:")
            data = summary['data']
            print(f"  Total Images Processed: {data.get('total_images', 0)}")
            print(f"  Accepted Images: {data.get('total_processed', 0)}")
            print(f"  Rejected Images: {data.get('total_rejected', 0)}")
            print(f"  Acceptance Rate: {data.get('acceptance_rate', 0)}%")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Summary test failed: {e}")
        return False

def main():
    """Run all API tests."""
    print("🚀 Starting Civic Quality Control API Tests")
    print("=" * 50)
    
    # Check if server is running
    try:
        requests.get(API_BASE_URL, timeout=5)
    except requests.exceptions.ConnectionError:
        print("❌ Server not running! Please start the server first:")
        print("   python app.py")
        print("   Or: python production.py")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Health Check", test_health_endpoint),
        ("Validation Rules", test_validation_rules_endpoint),
        ("API Information", test_api_info_endpoint),
        ("Image Validation", test_image_validation_endpoint),
        ("Processing Summary", test_summary_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    # Final results
    print("\n" + "="*50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\n💡 API Usage Examples:")
    print(f"  Health Check: curl {API_BASE_URL}/health")
    print(f"  Get Rules: curl {API_BASE_URL}/validation-rules")
    print(f"  Validate Image: curl -X POST -F 'image=@your_image.jpg' {API_BASE_URL}/validate")
    print(f"  Get Summary: curl {API_BASE_URL}/summary")

if __name__ == "__main__":
    main()