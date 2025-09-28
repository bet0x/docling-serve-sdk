"""
Pydantic models for Docling Serve API.

This module contains the essential Pydantic models for the Docling Serve API.
"""

from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


# Enums
class InputFormat(str, Enum):
    """Input format enumeration."""
    DOCX = "docx"
    PPTX = "pptx"
    HTML = "html"
    IMAGE = "image"
    PDF = "pdf"
    ASCIIDOC = "asciidoc"
    MD = "md"
    CSV = "csv"
    XLSX = "xlsx"
    XML_USPTO = "xml_uspto"
    XML_JATS = "xml_jats"
    METS_GBS = "mets_gbs"
    JSON_DOCLING = "json_docling"
    AUDIO = "audio"


class OutputFormat(str, Enum):
    """Output format enumeration."""
    MD = "md"
    JSON = "json"
    HTML = "html"
    HTML_SPLIT_PAGE = "html_split_page"
    TEXT = "text"
    DOCTAGS = "doctags"


class ImageRefMode(str, Enum):
    """Image reference mode enumeration."""
    EMBEDDED = "embedded"
    REFERENCE = "referenced"
    PLACEHOLDER = "placeholder"


class OCREngine(str, Enum):
    """OCR engine enumeration."""
    EASYOCR = "easyocr"
    OCRMAC = "ocrmac"
    RAPIDOCR = "rapidocr"
    TESSEROCR = "tesserocr"
    TESSERACT = "tesseract"


class PdfBackend(str, Enum):
    """PDF backend enumeration."""
    PYPDFIUM2 = "pypdfium2"
    DLPARSE_V1 = "dlparse_v1"
    DLPARSE_V2 = "dlparse_v2"
    DLPARSE_V4 = "dlparse_v4"


class TableMode(str, Enum):
    """Table mode enumeration."""
    FAST = "fast"
    ACCURATE = "accurate"


class Pipeline(str, Enum):
    """Processing pipeline enumeration."""
    STANDARD = "standard"
    VLM = "vlm"


# Core Models
class HealthCheckResponse(BaseModel):
    """Health check response model."""
    model_config = ConfigDict(extra="forbid")
    
    status: str = Field(..., description="Health status")


class ConvertDocumentsRequestOptions(BaseModel):
    """Convert documents request options."""
    model_config = ConfigDict(extra="forbid")
    
    from_formats: List[InputFormat] = Field(
        default=[
            InputFormat.DOCX, InputFormat.PPTX, InputFormat.HTML, InputFormat.IMAGE,
            InputFormat.PDF, InputFormat.ASCIIDOC, InputFormat.MD, InputFormat.CSV,
            InputFormat.XLSX, InputFormat.XML_USPTO, InputFormat.XML_JATS,
            InputFormat.METS_GBS, InputFormat.JSON_DOCLING, InputFormat.AUDIO
        ],
        description="Input format(s) to convert from"
    )
    to_formats: List[OutputFormat] = Field(
        default=[OutputFormat.MD],
        description="Output format(s) to convert to"
    )
    image_export_mode: ImageRefMode = Field(
        default=ImageRefMode.EMBEDDED,
        description="Image export mode"
    )
    do_ocr: bool = Field(default=True, description="Enable OCR processing")
    force_ocr: bool = Field(default=False, description="Force OCR over existing text")
    ocr_engine: OCREngine = Field(default=OCREngine.EASYOCR, description="OCR engine to use")
    pdf_backend: PdfBackend = Field(default=PdfBackend.DLPARSE_V4, description="PDF backend")
    table_mode: TableMode = Field(default=TableMode.ACCURATE, description="Table processing mode")
    table_cell_matching: bool = Field(default=True, description="Enable table cell matching")
    pipeline: Pipeline = Field(default=Pipeline.STANDARD, description="Processing pipeline")
    page_range: List[int] = Field(default=[1, 9223372036854775807], description="Page range to process")
    document_timeout: float = Field(default=604800.0, description="Document timeout in seconds")
    abort_on_error: bool = Field(default=False, description="Abort on error")
    do_table_structure: bool = Field(default=True, description="Extract table structure")
    include_images: bool = Field(default=True, description="Include images in output")
    images_scale: float = Field(default=2.0, description="Image scale factor")
    md_page_break_placeholder: str = Field(default="", description="Page break placeholder")
    do_code_enrichment: bool = Field(default=False, description="Enable code enrichment")
    do_formula_enrichment: bool = Field(default=False, description="Enable formula enrichment")
    do_picture_classification: bool = Field(default=False, description="Enable picture classification")
    do_picture_description: bool = Field(default=False, description="Enable picture description")
    picture_description_area_threshold: float = Field(default=0.05, description="Picture description threshold")


class InBodyTarget(BaseModel):
    """In-body target model."""
    model_config = ConfigDict(extra="forbid")
    
    kind: Literal["inbody"] = Field(default="inbody", description="Target kind")


# Response Models
class ConvertDocumentResponse(BaseModel):
    """Convert document response model."""
    model_config = ConfigDict(extra="forbid")
    
    document: Dict[str, Any] = Field(..., description="Converted document data")
    status: str = Field(..., description="Conversion status")
    processing_time: float = Field(..., description="Processing time in seconds")
    errors: List[str] = Field(default_factory=list, description="Processing errors")
    timings: Dict[str, Any] = Field(default_factory=dict, description="Processing timings")


# Source Request Models
class FileSourceRequest(BaseModel):
    """File source request model."""
    model_config = ConfigDict(extra="forbid")
    
    base64_string: str = Field(..., description="Content of the file serialized in base64")
    filename: str = Field(..., description="Filename of the uploaded document")
    kind: Literal["file"] = Field(default="file", description="Source kind")


class HttpSourceRequest(BaseModel):
    """HTTP source request model."""
    model_config = ConfigDict(extra="forbid")
    
    url: str = Field(..., description="HTTP url to process")
    headers: Dict[str, Any] = Field(default_factory=dict, description="Additional headers")
    kind: Literal["http"] = Field(default="http", description="Source kind")


class S3SourceRequest(BaseModel):
    """S3 source request model."""
    model_config = ConfigDict(extra="forbid")
    
    endpoint: str = Field(..., description="S3 service endpoint")
    access_key: str = Field(..., description="S3 access key")
    secret_key: str = Field(..., description="S3 secret key")
    bucket: str = Field(..., description="S3 bucket name")
    key_prefix: str = Field(default="", description="Prefix for object keys")
    verify_ssl: bool = Field(default=True, description="Verify SSL")
    kind: Literal["s3"] = Field(default="s3", description="Source kind")


# Target Models
class ZipTarget(BaseModel):
    """Zip target model."""
    model_config = ConfigDict(extra="forbid")
    
    kind: Literal["zip"] = Field(default="zip", description="Target kind")


class S3Target(BaseModel):
    """S3 target model."""
    model_config = ConfigDict(extra="forbid")
    
    kind: Literal["s3"] = Field(default="s3", description="Target kind")


class PutTarget(BaseModel):
    """Put target model."""
    model_config = ConfigDict(extra="forbid")
    
    kind: Literal["put"] = Field(default="put", description="Target kind")


# Request Models
class ConvertDocumentsRequest(BaseModel):
    """Convert documents request model."""
    model_config = ConfigDict(extra="forbid")
    
    sources: List[Union[FileSourceRequest, HttpSourceRequest, S3SourceRequest]] = Field(
        ..., description="List of document sources"
    )
    options: ConvertDocumentsRequestOptions = Field(
        default_factory=ConvertDocumentsRequestOptions,
        description="Conversion options"
    )
    target: Union[InBodyTarget, ZipTarget, S3Target, PutTarget] = Field(
        default_factory=InBodyTarget,
        description="Output target"
    )


# Response Models
class PresignedUrlConvertDocumentResponse(BaseModel):
    """Presigned URL convert document response model."""
    model_config = ConfigDict(extra="forbid")
    
    processing_time: float = Field(..., description="Processing time in seconds")
    num_converted: int = Field(..., description="Number of documents converted")
    num_succeeded: int = Field(..., description="Number of successful conversions")
    num_failed: int = Field(..., description="Number of failed conversions")


class TaskStatusResponse(BaseModel):
    """Task status response model."""
    model_config = ConfigDict(extra="forbid")
    
    task_id: str = Field(..., description="Task ID")
    task_type: str = Field(..., description="Task type")
    task_status: str = Field(..., description="Task status")
    task_position: Optional[int] = Field(None, description="Task position in queue")
    task_meta: Optional[Dict[str, Any]] = Field(None, description="Task metadata")


class ChunkDocumentResponse(BaseModel):
    """Chunk document response model."""
    model_config = ConfigDict(extra="forbid")
    
    document: Dict[str, Any] = Field(..., description="Chunked document data")
    status: str = Field(..., description="Chunking status")
    processing_time: float = Field(..., description="Processing time in seconds")


# Chunker Options
class HierarchicalChunkerOptions(BaseModel):
    """Hierarchical chunker options model."""
    model_config = ConfigDict(extra="forbid")
    
    max_chunk_size: int = Field(default=1000, description="Maximum chunk size")
    min_chunk_size: int = Field(default=100, description="Minimum chunk size")
    overlap: int = Field(default=50, description="Overlap between chunks")


class HybridChunkerOptions(BaseModel):
    """Hybrid chunker options model."""
    model_config = ConfigDict(extra="forbid")
    
    max_chunk_size: int = Field(default=1000, description="Maximum chunk size")
    min_chunk_size: int = Field(default=100, description="Minimum chunk size")
    overlap: int = Field(default=50, description="Overlap between chunks")
    semantic_threshold: float = Field(default=0.7, description="Semantic similarity threshold")


# Type aliases for convenience
SourceRequest = Union[FileSourceRequest, HttpSourceRequest, S3SourceRequest]
TargetRequest = Union[InBodyTarget, ZipTarget, S3Target, PutTarget]
