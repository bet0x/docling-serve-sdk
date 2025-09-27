#!/usr/bin/env python3
"""
Test suite for new features in Docling Serve SDK v1.1.0.

This script tests the newly added classes and functionality.
"""

import sys
from pathlib import Path
import base64

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from docling_serve_sdk import (
    DoclingClient, DoclingError,
    ConvertDocumentsRequest, ConvertDocumentsRequestOptions,
    FileSourceRequest, HttpSourceRequest, S3SourceRequest,
    ZipTarget, S3Target, PutTarget,
    TaskStatusResponse, PresignedUrlConvertDocumentResponse,
    HierarchicalChunkerOptions, HybridChunkerOptions,
    InputFormat, OutputFormat
)


def test_file_source_request():
    """Test FileSourceRequest functionality."""
    print("Testing FileSourceRequest...")
    
    # Create a test file
    test_content = "# Test Document\n\nThis is a test for FileSourceRequest."
    test_file = Path("test_file_source.md")
    test_file.write_text(test_content, encoding='utf-8')
    
    try:
        # Read file and encode to base64
        with open(test_file, 'rb') as f:
            file_content = f.read()
            base64_content = base64.b64encode(file_content).decode('utf-8')
        
        # Create FileSourceRequest
        file_source = FileSourceRequest(
            base64_string=base64_content,
            filename=test_file.name
        )
        
        # Create ConvertDocumentsRequest
        request = ConvertDocumentsRequest(sources=[file_source])
        
        print(f"✅ FileSourceRequest created: {file_source.filename}")
        print(f"✅ ConvertDocumentsRequest created with {len(request.sources)} sources")
        
        return True
        
    except Exception as e:
        print(f"❌ FileSourceRequest test failed: {e}")
        return False
    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()


def test_http_source_request():
    """Test HttpSourceRequest functionality."""
    print("Testing HttpSourceRequest...")
    
    try:
        # Create HttpSourceRequest
        http_source = HttpSourceRequest(
            url="https://example.com/document.pdf",
            headers={"User-Agent": "DoclingSDK/1.1.0"}
        )
        
        # Create ConvertDocumentsRequest
        request = ConvertDocumentsRequest(sources=[http_source])
        
        print(f"✅ HttpSourceRequest created: {http_source.url}")
        print(f"✅ Headers: {http_source.headers}")
        
        return True
        
    except Exception as e:
        print(f"❌ HttpSourceRequest test failed: {e}")
        return False


def test_s3_source_request():
    """Test S3SourceRequest functionality."""
    print("Testing S3SourceRequest...")
    
    try:
        # Create S3SourceRequest
        s3_source = S3SourceRequest(
            endpoint="s3.amazonaws.com",
            access_key="test-access-key",
            secret_key="test-secret-key",
            bucket="test-bucket",
            key_prefix="documents/",
            verify_ssl=True
        )
        
        # Create ConvertDocumentsRequest
        request = ConvertDocumentsRequest(sources=[s3_source])
        
        print(f"✅ S3SourceRequest created: {s3_source.bucket}")
        print(f"✅ Endpoint: {s3_source.endpoint}")
        print(f"✅ Key prefix: {s3_source.key_prefix}")
        
        return True
        
    except Exception as e:
        print(f"❌ S3SourceRequest test failed: {e}")
        return False


def test_target_models():
    """Test different target models."""
    print("Testing Target Models...")
    
    try:
        # Test ZipTarget
        zip_target = ZipTarget()
        print(f"✅ ZipTarget: {zip_target.kind}")
        
        # Test S3Target
        s3_target = S3Target()
        print(f"✅ S3Target: {s3_target.kind}")
        
        # Test PutTarget
        put_target = PutTarget()
        print(f"✅ PutTarget: {put_target.kind}")
        
        return True
        
    except Exception as e:
        print(f"❌ Target models test failed: {e}")
        return False


def test_chunker_options():
    """Test chunker options."""
    print("Testing Chunker Options...")
    
    try:
        # Test HierarchicalChunkerOptions
        hierarchical = HierarchicalChunkerOptions(
            max_chunk_size=2000,
            min_chunk_size=200,
            overlap=100
        )
        print(f"✅ HierarchicalChunkerOptions: max={hierarchical.max_chunk_size}, min={hierarchical.min_chunk_size}")
        
        # Test HybridChunkerOptions
        hybrid = HybridChunkerOptions(
            max_chunk_size=1500,
            min_chunk_size=150,
            overlap=75,
            semantic_threshold=0.8
        )
        print(f"✅ HybridChunkerOptions: threshold={hybrid.semantic_threshold}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chunker options test failed: {e}")
        return False


def test_response_models():
    """Test response models."""
    print("Testing Response Models...")
    
    try:
        # Test TaskStatusResponse
        task_status = TaskStatusResponse(
            task_id="test-task-123",
            task_type="convert",
            task_status="completed",
            task_position=1,
            task_meta={"processing_time": 2.5}
        )
        print(f"✅ TaskStatusResponse: {task_status.task_id} - {task_status.task_status}")
        
        # Test PresignedUrlConvertDocumentResponse
        presigned_response = PresignedUrlConvertDocumentResponse(
            processing_time=3.2,
            num_converted=5,
            num_succeeded=4,
            num_failed=1
        )
        print(f"✅ PresignedUrlConvertDocumentResponse: {presigned_response.num_succeeded}/{presigned_response.num_converted} succeeded")
        
        return True
        
    except Exception as e:
        print(f"❌ Response models test failed: {e}")
        return False


def test_complex_convert_request():
    """Test a complex ConvertDocumentsRequest with multiple sources and custom options."""
    print("Testing Complex ConvertDocumentsRequest...")
    
    try:
        # Create multiple sources
        file_source = FileSourceRequest(
            base64_string=base64.b64encode(b"test content").decode(),
            filename="test1.pdf"
        )
        
        http_source = HttpSourceRequest(
            url="https://example.com/doc.pdf"
        )
        
        # Create custom options
        options = ConvertDocumentsRequestOptions(
            from_formats=[InputFormat.PDF, InputFormat.DOCX],
            to_formats=[OutputFormat.MD, OutputFormat.HTML],
            do_ocr=True,
            include_images=True,
            images_scale=1.5
        )
        
        # Create request with multiple sources
        request = ConvertDocumentsRequest(
            sources=[file_source, http_source],
            options=options,
            target=ZipTarget()
        )
        
        print(f"✅ Complex request created with {len(request.sources)} sources")
        print(f"✅ Custom options: {len(request.options.from_formats)} input formats, {len(request.options.to_formats)} output formats")
        print(f"✅ Target: {request.target.kind}")
        
        return True
        
    except Exception as e:
        print(f"❌ Complex ConvertDocumentsRequest test failed: {e}")
        return False


def main():
    """Run all new feature tests."""
    print("Docling Serve SDK v1.1.0 - New Features Test Suite")
    print("=" * 60)
    
    tests = [
        test_file_source_request,
        test_http_source_request,
        test_s3_source_request,
        test_target_models,
        test_chunker_options,
        test_response_models,
        test_complex_convert_request
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            print()
    
    print("=" * 60)
    print(f"New Features Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All new features work correctly!")
        return 0
    else:
        print("❌ Some new features have issues!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
