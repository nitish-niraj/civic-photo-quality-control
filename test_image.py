#!/usr/bin/env python3
"""
Test script for the Civic Quality Control API
"""

import requests
import json

def test_image_upload(image_path):
    """Test image upload to the quality control API"""

    url = "http://localhost:5000/api/upload"

    try:
        # Open the image file
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            response = requests.post(url, files=files)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS!")
            print("=" * 50)

            # Print overall status
            print(f"📊 Overall Status: {result['data']['overall_status']}")
            print(f"⏱️  Processing Time: {result['data']['processing_time_seconds']} seconds")

            # Print issues
            issues = result['data'].get('issues', [])
            if issues:
                print(f"\n❌ Issues Found ({len(issues)}):")
                for issue in issues:
                    print(f"  • {issue['type']}: {issue['message']} (Severity: {issue['severity']})")
            else:
                print("\n✅ No Issues Found!")

            # Print warnings
            warnings = result['data'].get('warnings', [])
            if warnings:
                print(f"\n⚠️  Warnings ({len(warnings)}):")
                for warning in warnings:
                    print(f"  • {warning}")

            # Print recommendations
            recommendations = result['data'].get('recommendations', [])
            if recommendations:
                print(f"\n💡 Recommendations:")
                for rec in recommendations:
                    print(f"  • {rec}")

            # Print validation details
            validations = result['data'].get('validations', {})
            print(f"\n🔍 Validation Results:")
            for validation_type, validation_result in validations.items():
                if validation_result and not validation_result.get('error'):
                    print(f"  ✅ {validation_type}: OK")
                else:
                    print(f"  ❌ {validation_type}: Failed")

            # Print metrics
            metrics = result['data'].get('metrics', {})
            if metrics:
                print(f"\n📈 Metrics:")
                for key, value in metrics.items():
                    print(f"  • {key}: {value}")

        else:
            print(f"❌ ERROR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error Message: {error_data.get('message', 'Unknown error')}")
            except:
                print(f"Response: {response.text}")

    except FileNotFoundError:
        print(f"❌ ERROR: Image file not found: {image_path}")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Flask server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    # Test with the user's image
    image_path = r"C:\Users\kumar\OneDrive\Pictures\IMG_20220629_174412.jpg"
    print(f"Testing image: {image_path}")
    print("=" * 60)
    test_image_upload(image_path)