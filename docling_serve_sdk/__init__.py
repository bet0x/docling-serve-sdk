"""
Docling Serve SDK

A Python SDK for interacting with Docling Serve API using Pydantic models.
"""

from .client import DoclingClient, DoclingError, DoclingAPIError, DoclingTimeoutError
from .models import (
    # Core models
    ConvertDocumentsRequestOptions,
    ConvertDocumentResponse,
    HealthCheckResponse,
    
    # Enums
    InputFormat,
    OutputFormat,
    ImageRefMode,
    OCREngine,
    PdfBackend,
    TableMode,
    Pipeline,
    
    # Target models
    InBodyTarget,
    TargetRequest,
)

__version__ = "1.0.0"
__all__ = [
    "DoclingClient",
    "DoclingError",
    "DoclingAPIError", 
    "DoclingTimeoutError",
    "ConvertDocumentsRequestOptions",
    "ConvertDocumentResponse",
    "HealthCheckResponse",
    "InputFormat",
    "OutputFormat",
    "ImageRefMode",
    "OCREngine",
    "PdfBackend",
    "TableMode",
    "Pipeline",
    "InBodyTarget",
    "TargetRequest",
]