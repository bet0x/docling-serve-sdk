#!/usr/bin/env python3
"""
Test integration of new features with DoclingClient.

This script tests that the new classes work correctly with the actual client.
"""

import sys
from pathlib import Path
import base64

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from docling_serve_sdk import (
    DoclingClient, DoclingError,
    ConvertDocumentsRequest, ConvertDocumentsRequestOptions,
    FileSourceRequest, HttpSourceRequest,
    ZipTarget, S3Target,
    HierarchicalChunkerOptions, HybridChunkerOptions,
    InputFormat, OutputFormat
)


def test_client_with_new_models():
    """Test that the client can work with the new models."""
    print("Testing Client Integration with New Models...")
    
    client = DoclingClient(base_url="http://localhost:5001")
    
    try:
        # Test health check first
        health = client.health_check()
        print(f"✅ Health check: {health.status}")
        
        # Create a test document
        test_content = """# Integration Test Document

This document tests the integration of new models with the DoclingClient.

## Features to Test

1. FileSourceRequest with base64 content
2. ConvertDocumentsRequest with custom options
3. Different target types
4. Chunker options

## Conclusion

If you can read this, the integration is working!
"""
        
        test_file = Path("integration_test.md")
        test_file.write_text(test_content, encoding='utf-8')
        
        try:
            # Test 1: Basic conversion with existing method (should still work)
            print("\n--- Test 1: Basic conversion (existing method) ---")
            result = client.convert_file(test_file)
            print(f"✅ Basic conversion: {result.status}")
            print(f"   Processing time: {result.processing_time:.2f}s")
            
            # Test 2: Create FileSourceRequest manually
            print("\n--- Test 2: FileSourceRequest creation ---")
            with open(test_file, 'rb') as f:
                file_content = f.read()
                base64_content = base64.b64encode(file_content).decode('utf-8')
            
            file_source = FileSourceRequest(
                base64_string=base64_content,
                filename=test_file.name
            )
            print(f"✅ FileSourceRequest created: {file_source.filename}")
            print(f"   Base64 length: {len(file_source.base64_string)} characters")
            
            # Test 3: Create ConvertDocumentsRequest
            print("\n--- Test 3: ConvertDocumentsRequest creation ---")
            options = ConvertDocumentsRequestOptions(
                from_formats=[InputFormat.MD],
                to_formats=[OutputFormat.HTML],
                do_ocr=False,
                include_images=False
            )
            
            request = ConvertDocumentsRequest(
                sources=[file_source],
                options=options,
                target=ZipTarget()
            )
            print(f"✅ ConvertDocumentsRequest created")
            print(f"   Sources: {len(request.sources)}")
            print(f"   Target: {request.target.kind}")
            print(f"   Input formats: {[fmt.value for fmt in request.options.from_formats]}")
            print(f"   Output formats: {[fmt.value for fmt in request.options.to_formats]}")
            
            # Test 4: Test chunker options
            print("\n--- Test 4: Chunker Options ---")
            hierarchical = HierarchicalChunkerOptions(
                max_chunk_size=1000,
                min_chunk_size=100,
                overlap=50
            )
            hybrid = HybridChunkerOptions(
                max_chunk_size=800,
                min_chunk_size=80,
                overlap=40,
                semantic_threshold=0.7
            )
            print(f"✅ HierarchicalChunkerOptions: max={hierarchical.max_chunk_size}")
            print(f"✅ HybridChunkerOptions: threshold={hybrid.semantic_threshold}")
            
            # Test 5: Test different targets
            print("\n--- Test 5: Different Targets ---")
            targets = [ZipTarget(), S3Target()]
            for target in targets:
                print(f"✅ {target.__class__.__name__}: {target.kind}")
            
            print("\n🎉 All integration tests passed!")
            return True
            
        finally:
            # Clean up
            if test_file.exists():
                test_file.unlink()
                
    except DoclingError as e:
        print(f"❌ Docling error: {e}")
        return False
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def test_model_serialization():
    """Test that models can be serialized/deserialized correctly."""
    print("\nTesting Model Serialization...")
    
    try:
        # Create a complex request
        file_source = FileSourceRequest(
            base64_string=base64.b64encode(b"test content").decode(),
            filename="test.pdf"
        )
        
        http_source = HttpSourceRequest(
            url="https://example.com/doc.pdf",
            headers={"Authorization": "Bearer token123"}
        )
        
        options = ConvertDocumentsRequestOptions(
            from_formats=[InputFormat.PDF, InputFormat.DOCX],
            to_formats=[OutputFormat.MD],
            do_ocr=True,
            include_images=True
        )
        
        request = ConvertDocumentsRequest(
            sources=[file_source, http_source],
            options=options,
            target=S3Target()
        )
        
        # Test serialization to dict
        request_dict = request.model_dump()
        print(f"✅ Serialized to dict: {len(request_dict)} top-level keys")
        
        # Test serialization to JSON
        request_json = request.model_dump_json()
        print(f"✅ Serialized to JSON: {len(request_json)} characters")
        
        # Test deserialization from dict
        request_from_dict = ConvertDocumentsRequest.model_validate(request_dict)
        print(f"✅ Deserialized from dict: {len(request_from_dict.sources)} sources")
        
        # Test deserialization from JSON
        request_from_json = ConvertDocumentsRequest.model_validate_json(request_json)
        print(f"✅ Deserialized from JSON: {request_from_json.target.kind}")
        
        print("🎉 Model serialization tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Serialization test failed: {e}")
        return False


def main():
    """Run integration tests."""
    print("Docling Serve SDK v1.1.0 - Client Integration Test Suite")
    print("=" * 70)
    
    tests = [
        test_client_with_new_models,
        test_model_serialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 70)
    print(f"Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        return 0
    else:
        print("❌ Some integration tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
