"""
Docling Serve SDK

A Python SDK for interacting with Docling Serve API using Pydantic models.
"""

from .client import DoclingClient, DoclingError, DoclingAPIError, DoclingTimeoutError
from .models import (
    # Core models
    ConvertDocumentsRequest,
    ConvertDocumentsRequestOptions,
    ConvertDocumentResponse,
    PresignedUrlConvertDocumentResponse,
    HealthCheckResponse,
    TaskStatusResponse,
    ChunkDocumentResponse,
    
    # Source models
    FileSourceRequest,
    HttpSourceRequest,
    S3SourceRequest,
    
    # Target models
    InBodyTarget,
    ZipTarget,
    S3Target,
    PutTarget,
    
    # Chunker options
    HierarchicalChunkerOptions,
    HybridChunkerOptions,
    
    # Enums
    InputFormat,
    OutputFormat,
    ImageRefMode,
    OCREngine,
    PdfBackend,
    TableMode,
    Pipeline,
    
    # Type aliases
    SourceRequest,
    TargetRequest,
)

__version__ = "1.2.0"
__all__ = [
    "DoclingClient",
    "DoclingError",
    "DoclingAPIError", 
    "DoclingTimeoutError",
    "ConvertDocumentsRequest",
    "ConvertDocumentsRequestOptions",
    "ConvertDocumentResponse",
    "PresignedUrlConvertDocumentResponse",
    "HealthCheckResponse",
    "TaskStatusResponse",
    "ChunkDocumentResponse",
    "FileSourceRequest",
    "HttpSourceRequest",
    "S3SourceRequest",
    "InBodyTarget",
    "ZipTarget",
    "S3Target",
    "PutTarget",
    "HierarchicalChunkerOptions",
    "HybridChunkerOptions",
    "InputFormat",
    "OutputFormat",
    "ImageRefMode",
    "OCREngine",
    "PdfBackend",
    "TableMode",
    "Pipeline",
    "SourceRequest",
    "TargetRequest",
]