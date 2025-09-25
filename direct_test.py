#!/usr/bin/env python3
"""
Direct test of the QualityControlService with the user's image
"""

import os
import sys
sys.path.append('.')

from app.services.quality_control import QualityControlService
from config import Config

def test_image_directly(image_path):
    """Test image quality control directly without the web server"""

    print(f"Testing image: {image_path}")
    print("=" * 60)

    # Check if image exists
    if not os.path.exists(image_path):
        print(f"❌ ERROR: Image file not found: {image_path}")
        return

    try:
        # Create config instance
        config = Config()

        # Initialize quality control service
        qc_service = QualityControlService(config)

        # Validate image
        print("🔍 Analyzing image quality...")
        validation_result = qc_service.validate_image(image_path)

        print("✅ SUCCESS!")
        print("=" * 50)

        # Print overall status
        print(f"📊 Overall Status: {validation_result['overall_status']}")
        print(f"⏱️  Processing Time: {validation_result['processing_time_seconds']} seconds")

        # Print issues
        issues = validation_result.get('issues', [])
        if issues:
            print(f"\n❌ Issues Found ({len(issues)}):")
            for issue in issues:
                print(f"  • {issue['type']}: {issue['message']} (Severity: {issue['severity']})")
        else:
            print("\n✅ No Issues Found!")

        # Print warnings
        warnings = validation_result.get('warnings', [])
        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"  • {warning}")

        # Print recommendations
        recommendations = validation_result.get('recommendations', [])
        if recommendations:
            print(f"\n💡 Recommendations:")
            for rec in recommendations:
                print(f"  • {rec}")

        # Print validation details
        validations = validation_result.get('validations', {})
        print(f"\n🔍 Validation Results:")
        for validation_type, validation_result_detail in validations.items():
            if validation_result_detail and not validation_result_detail.get('error'):
                print(f"  ✅ {validation_type}: OK")
            else:
                print(f"  ❌ {validation_type}: Failed")

        # Print metrics
        metrics = validation_result.get('metrics', {})
        if metrics:
            print(f"\n📈 Metrics:")
            for key, value in metrics.items():
                print(f"  • {key}: {value}")

        # Print file paths if available
        if 'processed_path' in validation_result:
            print(f"\n📁 Processed Path: {validation_result['processed_path']}")
        if 'rejected_path' in validation_result:
            print(f"\n📁 Rejected Path: {validation_result['rejected_path']}")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with the user's image
    image_path = r"C:\Users\kumar\OneDrive\Pictures\IMG_20220629_174412.jpg"
    test_image_directly(image_path)