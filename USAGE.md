# Docling Serve SDK - Usage Guide

This guide provides comprehensive examples of how to use the Docling Serve SDK v1.1.0.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Source Types](#source-types)
- [Target Types](#target-types)
- [Chunking](#chunking)
- [Async Operations](#async-operations)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Installation

```bash
pip install docling-serve-sdk
```

## Quick Start

```python
from docling_serve_sdk import DoclingClient

# Create client
client = DoclingClient(base_url="http://localhost:5001")

# Check health
health = client.health_check()
print(f"Status: {health.status}")

# Convert a document
result = client.convert_file("document.pdf")
print(f"Content: {result.document['md_content']}")
```

## Basic Usage

### Health Check

```python
from docling_serve_sdk import DoclingClient

client = DoclingClient(base_url="http://localhost:5001")

# Synchronous health check
health = client.health_check()
print(f"Health: {health.status}")

# Asynchronous health check
import asyncio
async def check_health():
    health = await client.health_check_async()
    print(f"Health: {health.status}")

asyncio.run(check_health())
```

### Document Conversion

```python
from docling_serve_sdk import DoclingClient, ConvertDocumentsRequestOptions, InputFormat, OutputFormat

client = DoclingClient(base_url="http://localhost:5001")

# Basic conversion
result = client.convert_file("document.pdf")
print(f"Status: {result.status}")
print(f"Processing time: {result.processing_time:.2f}s")
print(f"Content: {result.document['md_content']}")

# Conversion with custom options
options = ConvertDocumentsRequestOptions(
    from_formats=[InputFormat.PDF, InputFormat.DOCX],
    to_formats=[OutputFormat.MD, OutputFormat.HTML],
    do_ocr=True,
    include_images=True,
    images_scale=2.0
)

result = client.convert_file("document.pdf", options=options)
```

## Advanced Features

### Using ConvertDocumentsRequest

```python
from docling_serve_sdk import (
    DoclingClient, ConvertDocumentsRequest, ConvertDocumentsRequestOptions,
    FileSourceRequest, HttpSourceRequest, S3SourceRequest,
    ZipTarget, S3Target, PutTarget,
    InputFormat, OutputFormat
)
import base64

client = DoclingClient(base_url="http://localhost:5001")

# Create file source from local file
with open("document.pdf", "rb") as f:
    file_content = f.read()
    base64_content = base64.b64encode(file_content).decode('utf-8')

file_source = FileSourceRequest(
    base64_string=base64_content,
    filename="document.pdf"
)

# Create HTTP source
http_source = HttpSourceRequest(
    url="https://example.com/document.pdf",
    headers={"User-Agent": "DoclingSDK/1.1.0"}
)

# Create S3 source
s3_source = S3SourceRequest(
    endpoint="s3.amazonaws.com",
    access_key="your-access-key",
    secret_key="your-secret-key",
    bucket="your-bucket",
    key_prefix="documents/"
)

# Create custom options
options = ConvertDocumentsRequestOptions(
    from_formats=[InputFormat.PDF, InputFormat.DOCX, InputFormat.PPTX],
    to_formats=[OutputFormat.MD, OutputFormat.HTML],
    do_ocr=True,
    force_ocr=False,
    include_images=True,
    images_scale=1.5,
    do_table_structure=True
)

# Create request with multiple sources
request = ConvertDocumentsRequest(
    sources=[file_source, http_source, s3_source],
    options=options,
    target=ZipTarget()  # Output as ZIP file
)

# Note: The actual API call would depend on your client implementation
# This shows the structure of the request
```

## Source Types

### FileSourceRequest

For local files converted to base64:

```python
from docling_serve_sdk import FileSourceRequest
import base64

# Read file and encode to base64
with open("document.pdf", "rb") as f:
    file_content = f.read()
    base64_content = base64.b64encode(file_content).decode('utf-8')

file_source = FileSourceRequest(
    base64_string=base64_content,
    filename="document.pdf"
)
```

### HttpSourceRequest

For documents accessible via HTTP/HTTPS:

```python
from docling_serve_sdk import HttpSourceRequest

# Basic HTTP source
http_source = HttpSourceRequest(
    url="https://example.com/document.pdf"
)

# HTTP source with custom headers
http_source = HttpSourceRequest(
    url="https://api.example.com/documents/123",
    headers={
        "Authorization": "Bearer your-token",
        "User-Agent": "DoclingSDK/1.1.0",
        "Accept": "application/pdf"
    }
)
```

### S3SourceRequest

For documents stored in S3-compatible storage:

```python
from docling_serve_sdk import S3SourceRequest

# AWS S3
s3_source = S3SourceRequest(
    endpoint="s3.amazonaws.com",
    access_key="your-access-key",
    secret_key="your-secret-key",
    bucket="your-bucket",
    key_prefix="documents/",
    verify_ssl=True
)

# MinIO or other S3-compatible storage
s3_source = S3SourceRequest(
    endpoint="minio.example.com:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    bucket="documents",
    verify_ssl=False
)
```

## Target Types

### InBodyTarget (Default)

Returns the converted document in the response body:

```python
from docling_serve_sdk import InBodyTarget

target = InBodyTarget()  # Default target
```

### ZipTarget

Returns the converted documents as a ZIP file:

```python
from docling_serve_sdk import ZipTarget

target = ZipTarget()
```

### S3Target

Uploads converted documents to S3:

```python
from docling_serve_sdk import S3Target

target = S3Target()
```

### PutTarget

Uploads converted documents via PUT request:

```python
from docling_serve_sdk import PutTarget

target = PutTarget()
```

## Chunking

### Hierarchical Chunking

```python
from docling_serve_sdk import HierarchicalChunkerOptions

chunker_options = HierarchicalChunkerOptions(
    max_chunk_size=2000,    # Maximum characters per chunk
    min_chunk_size=200,     # Minimum characters per chunk
    overlap=100             # Overlap between chunks
)
```

### Hybrid Chunking

```python
from docling_serve_sdk import HybridChunkerOptions

chunker_options = HybridChunkerOptions(
    max_chunk_size=1500,        # Maximum characters per chunk
    min_chunk_size=150,         # Minimum characters per chunk
    overlap=75,                 # Overlap between chunks
    semantic_threshold=0.8      # Semantic similarity threshold
)
```

## Async Operations

```python
import asyncio
from docling_serve_sdk import DoclingClient

async def async_conversion():
    client = DoclingClient(base_url="http://localhost:5001")
    
    # Async health check
    health = await client.health_check_async()
    print(f"Health: {health.status}")
    
    # Async document conversion
    result = await client.convert_file_async("document.pdf")
    print(f"Content: {result.document['md_content']}")

# Run async function
asyncio.run(async_conversion())
```

## Error Handling

```python
from docling_serve_sdk import DoclingClient, DoclingError, DoclingAPIError, DoclingTimeoutError

client = DoclingClient(base_url="http://localhost:5001")

try:
    result = client.convert_file("document.pdf")
    print(f"Success: {result.status}")
    
except DoclingError as e:
    print(f"Docling error: {e}")
    
except DoclingAPIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Response: {e.response}")
    
except DoclingTimeoutError as e:
    print(f"Timeout error: {e}")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

### 1. Connection Management

```python
from docling_serve_sdk import DoclingClient

# Use connection pooling for multiple requests
client = DoclingClient(
    base_url="http://localhost:5001",
    timeout=300.0,        # 5 minutes timeout
    max_retries=3,        # Retry failed requests
    retry_delay=1.0       # Delay between retries
)
```

### 2. File Handling

```python
import base64
from pathlib import Path
from docling_serve_sdk import FileSourceRequest

def create_file_source(file_path: str) -> FileSourceRequest:
    """Create FileSourceRequest from file path."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, 'rb') as f:
        file_content = f.read()
        base64_content = base64.b64encode(file_content).decode('utf-8')
    
    return FileSourceRequest(
        base64_string=base64_content,
        filename=path.name
    )

# Usage
file_source = create_file_source("document.pdf")
```

### 3. Batch Processing

```python
from docling_serve_sdk import DoclingClient, ConvertDocumentsRequest, FileSourceRequest
import base64
from pathlib import Path

def process_multiple_documents(file_paths: list[str]):
    """Process multiple documents in a single request."""
    client = DoclingClient(base_url="http://localhost:5001")
    
    sources = []
    for file_path in file_paths:
        path = Path(file_path)
        with open(path, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        
        sources.append(FileSourceRequest(
            base64_string=content,
            filename=path.name
        ))
    
    # Create request with multiple sources
    request = ConvertDocumentsRequest(sources=sources)
    
    # Process all documents
    # Note: Actual implementation depends on your client methods
    return request

# Usage
documents = ["doc1.pdf", "doc2.docx", "doc3.pptx"]
request = process_multiple_documents(documents)
```

### 4. Configuration Management

```python
from docling_serve_sdk import ConvertDocumentsRequestOptions, InputFormat, OutputFormat, OCREngine, PdfBackend

def create_production_options() -> ConvertDocumentsRequestOptions:
    """Create optimized options for production use."""
    return ConvertDocumentsRequestOptions(
        from_formats=[
            InputFormat.PDF, InputFormat.DOCX, InputFormat.PPTX,
            InputFormat.HTML, InputFormat.MD, InputFormat.CSV,
            InputFormat.XLSX
        ],
        to_formats=[OutputFormat.MD, OutputFormat.HTML],
        do_ocr=True,
        force_ocr=False,
        ocr_engine=OCREngine.EASYOCR,
        pdf_backend=PdfBackend.DLPARSE_V4,
        include_images=True,
        images_scale=1.5,
        do_table_structure=True,
        document_timeout=600.0,  # 10 minutes
        abort_on_error=False
    )

# Usage
options = create_production_options()
```

### 5. Error Recovery

```python
from docling_serve_sdk import DoclingClient, DoclingAPIError
import time

def convert_with_retry(client: DoclingClient, file_path: str, max_retries: int = 3):
    """Convert document with automatic retry on failure."""
    for attempt in range(max_retries):
        try:
            result = client.convert_file(file_path)
            return result
            
        except DoclingAPIError as e:
            if e.status_code == 429:  # Rate limited
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                continue
            else:
                raise  # Re-raise non-rate-limit errors
                
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Last attempt, re-raise the error
            print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            time.sleep(1)
    
    raise Exception(f"Failed after {max_retries} attempts")

# Usage
client = DoclingClient(base_url="http://localhost:5001")
result = convert_with_retry(client, "document.pdf")
```

## Complete Example

Here's a complete example that demonstrates most features:

```python
import asyncio
import base64
from pathlib import Path
from docling_serve_sdk import (
    DoclingClient, ConvertDocumentsRequest, ConvertDocumentsRequestOptions,
    FileSourceRequest, HttpSourceRequest, ZipTarget,
    InputFormat, OutputFormat, OCREngine, PdfBackend,
    DoclingError, DoclingAPIError
)

async def complete_example():
    """Complete example demonstrating SDK features."""
    
    # Initialize client
    client = DoclingClient(
        base_url="http://localhost:5001",
        timeout=300.0,
        max_retries=3
    )
    
    try:
        # Health check
        health = await client.health_check_async()
        print(f"✅ Health: {health.status}")
        
        # Create file source
        with open("document.pdf", "rb") as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        
        file_source = FileSourceRequest(
            base64_string=content,
            filename="document.pdf"
        )
        
        # Create HTTP source
        http_source = HttpSourceRequest(
            url="https://example.com/sample.pdf",
            headers={"User-Agent": "DoclingSDK/1.1.0"}
        )
        
        # Create options
        options = ConvertDocumentsRequestOptions(
            from_formats=[InputFormat.PDF, InputFormat.DOCX],
            to_formats=[OutputFormat.MD, OutputFormat.HTML],
            do_ocr=True,
            ocr_engine=OCREngine.EASYOCR,
            pdf_backend=PdfBackend.DLPARSE_V4,
            include_images=True,
            images_scale=2.0,
            do_table_structure=True
        )
        
        # Create request
        request = ConvertDocumentsRequest(
            sources=[file_source, http_source],
            options=options,
            target=ZipTarget()
        )
        
        print(f"✅ Created request with {len(request.sources)} sources")
        print(f"✅ Target: {request.target.kind}")
        print(f"✅ Input formats: {[fmt.value for fmt in request.options.from_formats]}")
        print(f"✅ Output formats: {[fmt.value for fmt in request.options.to_formats]}")
        
        # Convert document (using existing method for demonstration)
        result = await client.convert_file_async("document.pdf", options=options)
        print(f"✅ Conversion successful: {result.status}")
        print(f"✅ Processing time: {result.processing_time:.2f}s")
        print(f"✅ Content length: {len(result.document.get('md_content', ''))} characters")
        
    except DoclingAPIError as e:
        print(f"❌ API Error: {e}")
        print(f"   Status code: {e.status_code}")
        
    except DoclingError as e:
        print(f"❌ Docling Error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

# Run the example
if __name__ == "__main__":
    asyncio.run(complete_example())
```

## Support

For more information and support:

- **Documentation**: [GitHub Repository](https://github.com/bet0x/docling-serve-sdk)
- **Issues**: [GitHub Issues](https://github.com/bet0x/docling-serve-sdk/issues)
- **PyPI**: [docling-serve-sdk](https://pypi.org/project/docling-serve-sdk/)

## License

MIT License - see LICENSE file for details.
