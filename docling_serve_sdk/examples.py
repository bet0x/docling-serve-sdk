"""
Examples for using the Docling Serve SDK.

This module contains practical examples of how to use the Docling Serve SDK
for document conversion and processing.
"""

from pathlib import Path
from docling_serve_sdk import (
    DoclingClient, 
    ConvertDocumentsRequestOptions,
    InputFormat,
    OutputFormat,
    ImageRefMode,
    OCREngine,
    PdfBackend,
    TableMode,
    Pipeline
)


def basic_conversion_example():
    """Basic document conversion example."""
    print("=== Basic Document Conversion ===")
    
    # Create client
    client = DoclingClient(base_url="http://localhost:5001")
    
    # Check health
    health = client.health_check()
    print(f"Service status: {health.status}")
    
    # Convert a document
    result = client.convert_file("document.pdf")
    print(f"Conversion status: {result.status}")
    print(f"Processing time: {result.processing_time:.2f}s")
    print(f"Content preview: {result.document['md_content'][:200]}...")


def custom_options_example():
    """Example with custom conversion options."""
    print("\n=== Custom Options Example ===")
    
    # Create client
    client = DoclingClient(base_url="http://localhost:5001")
    
    # Create custom options
    options = ConvertDocumentsRequestOptions(
        from_formats=[InputFormat.PDF, InputFormat.DOCX],
        to_formats=[OutputFormat.MD, OutputFormat.HTML],
        image_export_mode=ImageRefMode.EMBEDDED,
        do_ocr=True,
        ocr_engine=OCREngine.EASYOCR,
        pdf_backend=PdfBackend.DLPARSE_V4,
        table_mode=TableMode.ACCURATE,
        pipeline=Pipeline.STANDARD,
        include_images=True,
        images_scale=2.0
    )
    
    # Convert with custom options
    result = client.convert_file("document.pdf", options=options)
    print(f"Conversion status: {result.status}")
    print(f"Processing time: {result.processing_time:.2f}s")
    print(f"Filename: {result.document['filename']}")


def error_handling_example():
    """Example of error handling."""
    print("\n=== Error Handling Example ===")
    
    from docling_serve_sdk import DoclingError, DoclingAPIError
    
    client = DoclingClient(base_url="http://localhost:5001")
    
    try:
        # Try to convert a non-existent file
        result = client.convert_file("non_existent_file.pdf")
    except DoclingError as e:
        print(f"Docling error: {e}")
    except DoclingAPIError as e:
        print(f"API error: {e}")
        print(f"Status code: {e.status_code}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def async_example():
    """Example of async usage."""
    print("\n=== Async Example ===")
    
    import asyncio
    
    async def async_conversion():
        client = DoclingClient(base_url="http://localhost:5001")
        
        # Check health
        health = await client.health_check_async()
        print(f"Service status: {health.status}")
        
        # Convert document
        result = await client.convert_file_async("document.pdf")
        print(f"Conversion status: {result.status}")
        print(f"Processing time: {result.processing_time:.2f}s")
    
    # Run async example
    asyncio.run(async_conversion())


def batch_processing_example():
    """Example of batch processing multiple documents."""
    print("\n=== Batch Processing Example ===")
    
    client = DoclingClient(base_url="http://localhost:5001")
    
    # List of documents to process
    documents = [
        "document1.pdf",
        "document2.docx", 
        "document3.html"
    ]
    
    results = []
    for doc in documents:
        try:
            print(f"Processing {doc}...")
            result = client.convert_file(doc)
            results.append({
                "filename": doc,
                "status": result.status,
                "processing_time": result.processing_time,
                "content_length": len(result.document.get('md_content', ''))
            })
            print(f"  ✅ Success: {result.processing_time:.2f}s")
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            results.append({
                "filename": doc,
                "status": "failed",
                "error": str(e)
            })
    
    # Summary
    print(f"\nBatch processing complete:")
    print(f"Total documents: {len(documents)}")
    print(f"Successful: {len([r for r in results if r['status'] == 'success'])}")
    print(f"Failed: {len([r for r in results if r['status'] == 'failed'])}")


if __name__ == "__main__":
    """Run all examples."""
    print("Docling Serve SDK Examples")
    print("=" * 50)
    
    try:
        basic_conversion_example()
        custom_options_example()
        error_handling_example()
        async_example()
        batch_processing_example()
    except Exception as e:
        print(f"Example failed: {e}")
        print("Make sure Docling Serve is running on http://localhost:5001")