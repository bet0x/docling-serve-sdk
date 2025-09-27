# Docling Serve SDK

A comprehensive Python SDK for interacting with Docling Serve API using Pydantic models. This SDK provides type-safe, async/sync support for document conversion, chunking, and processing.

[![PyPI version](https://badge.fury.io/py/docling-serve-sdk.svg)](https://badge.fury.io/py/docling-serve-sdk)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Author:** [Alberto Ferrer](https://www.barrahome.org)  
**Email:** albertof@barrahome.org  
**Repository:** [https://github.com/bet0x/docling-serve-sdk](https://github.com/bet0x/docling-serve-sdk)  
**PyPI:** [https://pypi.org/project/docling-serve-sdk/](https://pypi.org/project/docling-serve-sdk/)

## Features

- ✅ **Document Conversion**: PDF, DOCX, PPTX, HTML, images, and more
- ✅ **Multiple Source Types**: Local files, HTTP URLs, S3 storage
- ✅ **Flexible Output**: In-body, ZIP, S3, PUT targets
- ✅ **OCR Processing**: Multiple engines (EasyOCR, Tesseract, etc.)
- ✅ **Table Extraction**: Structure analysis and cell matching
- ✅ **Image Handling**: Processing, scaling, and embedding
- ✅ **Chunking**: Hierarchical and hybrid document chunking
- ✅ **Async/Sync Support**: Both synchronous and asynchronous operations
- ✅ **Type Safety**: Full Pydantic model validation
- ✅ **Error Handling**: Comprehensive exception handling
- ✅ **Production Ready**: Connection pooling, retries, timeouts

## Installation

### From PyPI (Recommended)

```bash
pip install docling-serve-sdk
```

### From Source

```bash
# Clone the repository
git clone https://github.com/bet0x/docling-serve-sdk.git
cd docling-serve-sdk

# Install with pip
pip install -e .

# Or with uv
uv pip install -e .
```

### Requirements

- Python 3.8+
- httpx >= 0.24.0
- pydantic >= 2.0.0

## Quick Start

```python
from docling_serve_sdk import DoclingClient

# Create client
client = DoclingClient(base_url="http://localhost:5001")

# Check health
health = client.health_check()
print(f"Status: {health.status}")

# Convert document
result = client.convert_file("document.pdf")
print(f"Content: {result.document['md_content']}")
```

## Documentation

📖 **[Complete Usage Guide](USAGE.md)** - Comprehensive examples and advanced usage patterns

## Examples

### Basic Conversion

```python
from docling_serve_sdk import DoclingClient

client = DoclingClient(base_url="http://localhost:5001")
result = client.convert_file("document.pdf")

print(f"Status: {result.status}")
print(f"Processing time: {result.processing_time:.2f}s")
print(f"Content: {result.document['md_content']}")
```

### Advanced Usage with Multiple Sources

```python
from docling_serve_sdk import (
    DoclingClient, ConvertDocumentsRequest, ConvertDocumentsRequestOptions,
    FileSourceRequest, HttpSourceRequest, ZipTarget,
    InputFormat, OutputFormat
)
import base64

# Create file source
with open("document.pdf", "rb") as f:
    content = base64.b64encode(f.read()).decode('utf-8')

file_source = FileSourceRequest(base64_string=content, filename="document.pdf")
http_source = HttpSourceRequest(url="https://example.com/doc.pdf")

# Create request with multiple sources
request = ConvertDocumentsRequest(
    sources=[file_source, http_source],
    options=ConvertDocumentsRequestOptions(
        from_formats=[InputFormat.PDF, InputFormat.DOCX],
        to_formats=[OutputFormat.MD, OutputFormat.HTML],
        do_ocr=True,
        include_images=True
    ),
    target=ZipTarget()
)
```

### Async Usage

```python
import asyncio
from docling_serve_sdk import DoclingClient

async def convert_document():
    client = DoclingClient(base_url="http://localhost:5001")
    
    # Check health
    health = await client.health_check_async()
    print(f"Status: {health.status}")
    
    # Convert document
    result = await client.convert_file_async("document.pdf")
    print(f"Content: {result.document['md_content']}")

# Run async function
asyncio.run(convert_document())
```

### Error Handling

```python
from docling_serve_sdk import DoclingClient, DoclingError, DoclingAPIError

client = DoclingClient(base_url="http://localhost:5001")

try:
    result = client.convert_file("document.pdf")
    print(f"Success: {result.status}")
except DoclingError as e:
    print(f"Docling error: {e}")
except DoclingAPIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Configuration Options

### ConvertDocumentsRequestOptions

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `from_formats` | List[InputFormat] | All formats | Input formats to accept |
| `to_formats` | List[OutputFormat] | `[MD]` | Output formats to generate |
| `image_export_mode` | ImageRefMode | `EMBEDDED` | How to handle images |
| `do_ocr` | bool | `True` | Enable OCR processing |
| `force_ocr` | bool | `False` | Force OCR over existing text |
| `ocr_engine` | OCREngine | `EASYOCR` | OCR engine to use |
| `pdf_backend` | PdfBackend | `DLPARSE_V4` | PDF processing backend |
| `table_mode` | TableMode | `ACCURATE` | Table processing mode |
| `include_images` | bool | `True` | Include images in output |
| `images_scale` | float | `2.0` | Image scale factor |

### Supported Formats

**Input Formats:**
- PDF, DOCX, PPTX, HTML, MD, CSV, XLSX
- Images (PNG, JPG, etc.)
- XML (USPTO, JATS)
- Audio files

**Output Formats:**
- Markdown (MD)
- HTML
- JSON
- Text
- DocTags

## API Reference

### Core Classes

- **`DoclingClient`**: Main client for API interactions
- **`ConvertDocumentsRequest`**: Request model for document conversion
- **`ConvertDocumentsRequestOptions`**: Configuration options
- **`ConvertDocumentResponse`**: Response model for conversions

### Source Types

- **`FileSourceRequest`**: Local files (base64 encoded)
- **`HttpSourceRequest`**: HTTP/HTTPS URLs
- **`S3SourceRequest`**: S3-compatible storage

### Target Types

- **`InBodyTarget`**: Return in response body (default)
- **`ZipTarget`**: Return as ZIP file
- **`S3Target`**: Upload to S3
- **`PutTarget`**: Upload via PUT request

### Chunking

- **`HierarchicalChunkerOptions`**: Hierarchical document chunking
- **`HybridChunkerOptions`**: Hybrid semantic chunking

## Testing

```bash
# Run basic tests
uv run python test_sdk.py

# Run new features tests
uv run python test_new_features.py

# Run integration tests
uv run python test_client_integration.py

# Or with pytest
pytest test_*.py
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions:

- 📖 **Documentation**: [Complete Usage Guide](USAGE.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/bet0x/docling-serve-sdk/issues)
- 📦 **PyPI**: [docling-serve-sdk](https://pypi.org/project/docling-serve-sdk/)
- 🔗 **Docling Serve**: [Official Documentation](https://github.com/docling-project/docling-serve)

## Changelog

### v1.1.0 (Latest)
- ✅ Added complete API model coverage
- ✅ Added multiple source types (File, HTTP, S3)
- ✅ Added multiple target types (InBody, ZIP, S3, PUT)
- ✅ Added chunking options (Hierarchical, Hybrid)
- ✅ Added comprehensive error handling
- ✅ Added async/sync support
- ✅ Added complete documentation

### v1.0.0
- ✅ Initial release
- ✅ Basic document conversion
- ✅ Health check functionality
- ✅ Custom options support