#!/usr/bin/env python3
"""
Test suite for Docling Serve SDK.

This script tests the basic functionality of the Docling Serve SDK.
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from docling_serve_sdk import DoclingClient, DoclingError
from docling_serve_sdk.models import ConvertDocumentsRequestOptions, OutputFormat, InputFormat


def test_health_check():
    """Test health check endpoint."""
    print("Testing health check...")
    
    client = DoclingClient(base_url="http://localhost:5001")
    
    try:
        health = client.health_check()
        print(f"✅ Health check passed: {health.status}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_basic_conversion():
    """Test basic document conversion."""
    print("Testing basic conversion...")
    
    client = DoclingClient(base_url="http://localhost:5001")
    
    # Create a simple test document
    test_content = """# Test Document

This is a test document for the Docling Serve SDK.

## Features

- Document conversion
- OCR processing
- Table extraction
- Image handling

## Conclusion

The SDK is working correctly!
"""
    
    test_file = Path("test_document.md")
    test_file.write_text(test_content, encoding='utf-8')
    
    try:
        # Test conversion
        result = client.convert_file(test_file)
        print(f"✅ Conversion successful: {result.status}")
        print(f"   Processing time: {result.processing_time:.2f}s")
        print(f"   Content length: {len(result.document['md_content'])} characters")
        print(f"   Filename: {result.document['filename']}")
        
        # Clean up
        test_file.unlink()
        return True
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        # Clean up
        if test_file.exists():
            test_file.unlink()
        return False


def test_custom_options():
    """Test conversion with custom options."""
    print("Testing custom options...")
    
    client = DoclingClient(base_url="http://localhost:5001")
    
    # Create custom options
    options = ConvertDocumentsRequestOptions(
        from_formats=[InputFormat.MD],
        to_formats=[OutputFormat.HTML],
        do_ocr=False,
        include_images=False
    )
    
    # Create test document
    test_content = "# Custom Options Test\n\nThis tests custom conversion options."
    test_file = Path("test_options.md")
    test_file.write_text(test_content, encoding='utf-8')
    
    try:
        result = client.convert_file(test_file, options=options)
        print(f"✅ Custom options test successful: {result.status}")
        print(f"   Processing time: {result.processing_time:.2f}s")
        print(f"   Filename: {result.document['filename']}")
        
        # Clean up
        test_file.unlink()
        return True
        
    except Exception as e:
        print(f"❌ Custom options test failed: {e}")
        # Clean up
        if test_file.exists():
            test_file.unlink()
        return False


def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")
    
    client = DoclingClient(base_url="http://localhost:5001")
    
    try:
        # Try to convert a non-existent file
        result = client.convert_file("non_existent_file.pdf")
        print("❌ Error handling test failed: Should have raised an exception")
        return False
        
    except DoclingError as e:
        print(f"✅ Error handling test passed: {e}")
        return True
    except Exception as e:
        print(f"❌ Unexpected error type: {e}")
        return False


def main():
    """Run all tests."""
    print("Docling Serve SDK Test Suite")
    print("=" * 40)
    
    tests = [
        test_health_check,
        test_basic_conversion,
        test_custom_options,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())