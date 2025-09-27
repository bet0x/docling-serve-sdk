# Docling Serve SDK

A Python SDK for interacting with Docling Serve API using Pydantic models.

**Author:** [Alberto Ferrer](https://www.barrahome.org)  
**Email:** albertof@barrahome.org  
**Repository:** [https://github.com/bet0x/docling-serve-sdk](https://github.com/bet0x/docling-serve-sdk)

## Features

- ✅ Document conversion (PDF, DOCX, HTML, images, etc.)
- ✅ OCR processing with multiple engines
- ✅ Table extraction and structure analysis
- ✅ Image handling and processing
- ✅ Async/sync support
- ✅ Type-safe with Pydantic models
- ✅ Comprehensive error handling

## Installation

```bash
# Clone or download the SDK
cd docling_serve_sdk

# Install with uv
uv pip install -e .

# Or with pip
pip install -e .
```

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

### Custom Options

```python
from docling_serve_sdk import (
    DoclingClient, 
    ConvertDocumentsRequestOptions,
    InputFormat,
    OutputFormat,
    ImageRefMode,
    OCREngine
)

# Create custom options
options = ConvertDocumentsRequestOptions(
    from_formats=[InputFormat.PDF, InputFormat.DOCX],
    to_formats=[OutputFormat.MD, OutputFormat.HTML],
    image_export_mode=ImageRefMode.EMBEDDED,
    do_ocr=True,
    ocr_engine=OCREngine.EASYOCR,
    include_images=True,
    images_scale=2.0
)

# Convert with options
client = DoclingClient(base_url="http://localhost:5001")
result = client.convert_file("document.pdf", options=options)
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

## Testing

```bash
# Run tests
uv run python test_sdk.py

# Or with pytest
pytest test_sdk.py
```

## Requirements

- Python 3.8+
- httpx
- pydantic

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
- Check the [Docling Serve documentation](https://github.com/docling-project/docling-serve)
- Open an issue in this repository