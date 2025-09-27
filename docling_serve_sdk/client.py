"""
Docling Serve HTTP Client - Fixed Version

This module provides a client for interacting with the Docling Serve API.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional, Union, BinaryIO
from pathlib import Path
import httpx
from httpx import Response, RequestError, HTTPStatusError

from .models import (
    ConvertDocumentResponse,
    HealthCheckResponse,
    InBodyTarget,
    ConvertDocumentsRequestOptions,
    TargetRequest,
)


class DoclingError(Exception):
    """Base exception for Docling SDK errors."""
    pass


class DoclingAPIError(DoclingError):
    """Exception raised for API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class DoclingTimeoutError(DoclingError):
    """Exception raised for timeout errors."""
    pass


class DoclingClient:
    """
    Client for interacting with Docling Serve API.
    
    This client provides both synchronous and asynchronous methods for
    document conversion, chunking, and other Docling operations.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:5001",
        api_key: Optional[str] = None,
        timeout: float = 300.0,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize the Docling client.
        
        Args:
            base_url: Base URL of the Docling Serve instance
            api_key: API key for authentication (if required)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # HTTP client configuration
        self._headers = {
            "User-Agent": "docling-serve-sdk/1.0.0",
        }
        
        if self.api_key:
            self._headers["Authorization"] = f"Bearer {self.api_key}"
    
    def _get_headers(self, content_type: Optional[str] = None) -> Dict[str, str]:
        """Get headers for requests."""
        headers = self._headers.copy()
        if content_type:
            headers["Content-Type"] = content_type
        return headers
    
    def _handle_response(self, response: Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions."""
        try:
            response.raise_for_status()
            return response.json()
        except HTTPStatusError as e:
            try:
                error_data = e.response.json()
                message = error_data.get("detail", str(e))
            except:
                message = str(e)
            raise DoclingAPIError(
                message=message,
                status_code=e.response.status_code,
                response=error_data if 'error_data' in locals() else None
            )
        except json.JSONDecodeError:
            raise DoclingAPIError(f"Invalid JSON response: {response.text}")
    
    # Health Check
    def health_check(self) -> HealthCheckResponse:
        """Check the health of the Docling Serve instance."""
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(
                f"{self.base_url}/health",
                headers=self._get_headers()
            )
            data = self._handle_response(response)
            return HealthCheckResponse(**data)
    
    async def health_check_async(self) -> HealthCheckResponse:
        """Check the health of the Docling Serve instance (async)."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/health",
                headers=self._get_headers()
            )
            data = self._handle_response(response)
            return HealthCheckResponse(**data)
    
    # Document Conversion
    def convert_file(
        self,
        file_path: Union[str, Path, BinaryIO],
        options: Optional[ConvertDocumentsRequestOptions] = None,
        target: Optional[TargetRequest] = None
    ) -> ConvertDocumentResponse:
        """
        Convert a document file.
        
        Args:
            file_path: Path to the file or file-like object
            options: Conversion options
            target: Output target configuration
            
        Returns:
            ConvertDocumentResponse with converted document
        """
        if options is None:
            options = ConvertDocumentsRequestOptions()
        if target is None:
            target = InBodyTarget()
        
        # Prepare file data
        if isinstance(file_path, (str, Path)):
            file_path = Path(file_path)
            if not file_path.exists():
                raise DoclingError(f"File not found: {file_path}")
            
            with open(file_path, 'rb') as f:
                files = {"files": (file_path.name, f, "application/octet-stream")}
                data = {
                    "target_type": target.kind,
                    "from_formats": [fmt.value for fmt in options.from_formats],
                    "to_formats": [fmt.value for fmt in options.to_formats],
                    "image_export_mode": options.image_export_mode.value,
                    "do_ocr": options.do_ocr,
                    "force_ocr": options.force_ocr,
                    "ocr_engine": options.ocr_engine.value,
                    "pdf_backend": options.pdf_backend.value,
                    "table_mode": options.table_mode.value,
                    "table_cell_matching": options.table_cell_matching,
                    "pipeline": options.pipeline.value,
                    "page_range": options.page_range,
                    "document_timeout": options.document_timeout,
                    "abort_on_error": options.abort_on_error,
                    "do_table_structure": options.do_table_structure,
                    "include_images": options.include_images,
                    "images_scale": options.images_scale,
                    "md_page_break_placeholder": options.md_page_break_placeholder,
                    "do_code_enrichment": options.do_code_enrichment,
                    "do_formula_enrichment": options.do_formula_enrichment,
                    "do_picture_classification": options.do_picture_classification,
                    "do_picture_description": options.do_picture_description,
                    "picture_description_area_threshold": options.picture_description_area_threshold
                }
                
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(
                        f"{self.base_url}/v1/convert/file",
                        files=files,
                        data=data,
                        headers=self._get_headers(content_type=None)  # Let httpx set multipart
                    )
                    response_data = self._handle_response(response)
                    return ConvertDocumentResponse(**response_data)
        else:
            # File-like object
            files = {"files": ("document", file_path, "application/octet-stream")}
            data = {
                "target_type": target.kind,
                "from_formats": [fmt.value for fmt in options.from_formats],
                "to_formats": [fmt.value for fmt in options.to_formats],
                "image_export_mode": options.image_export_mode.value,
                "do_ocr": options.do_ocr,
                "force_ocr": options.force_ocr,
                "ocr_engine": options.ocr_engine.value,
                "pdf_backend": options.pdf_backend.value,
                "table_mode": options.table_mode.value,
                "table_cell_matching": options.table_cell_matching,
                "pipeline": options.pipeline.value,
                "page_range": options.page_range,
                "document_timeout": options.document_timeout,
                "abort_on_error": options.abort_on_error,
                "do_table_structure": options.do_table_structure,
                "include_images": options.include_images,
                "images_scale": options.images_scale,
                "md_page_break_placeholder": options.md_page_break_placeholder,
                "do_code_enrichment": options.do_code_enrichment,
                "do_formula_enrichment": options.do_formula_enrichment,
                "do_picture_classification": options.do_picture_classification,
                "do_picture_description": options.do_picture_description,
                "picture_description_area_threshold": options.picture_description_area_threshold
            }
            
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/v1/convert/file",
                    files=files,
                    data=data,
                    headers=self._get_headers(content_type=None)
                )
                response_data = self._handle_response(response)
                return ConvertDocumentResponse(**response_data)
    
    async def convert_file_async(
        self,
        file_path: Union[str, Path, BinaryIO],
        options: Optional[ConvertDocumentsRequestOptions] = None,
        target: Optional[TargetRequest] = None
    ) -> ConvertDocumentResponse:
        """Convert a document file (async)."""
        if options is None:
            options = ConvertDocumentsRequestOptions()
        if target is None:
            target = InBodyTarget()
        
        # Prepare file data
        if isinstance(file_path, (str, Path)):
            file_path = Path(file_path)
            if not file_path.exists():
                raise DoclingError(f"File not found: {file_path}")
            
            with open(file_path, 'rb') as f:
                files = {"files": (file_path.name, f, "application/octet-stream")}
                data = {
                    "target_type": target.kind,
                    "from_formats": [fmt.value for fmt in options.from_formats],
                    "to_formats": [fmt.value for fmt in options.to_formats],
                    "image_export_mode": options.image_export_mode.value,
                    "do_ocr": options.do_ocr,
                    "force_ocr": options.force_ocr,
                    "ocr_engine": options.ocr_engine.value,
                    "pdf_backend": options.pdf_backend.value,
                    "table_mode": options.table_mode.value,
                    "table_cell_matching": options.table_cell_matching,
                    "pipeline": options.pipeline.value,
                    "page_range": options.page_range,
                    "document_timeout": options.document_timeout,
                    "abort_on_error": options.abort_on_error,
                    "do_table_structure": options.do_table_structure,
                    "include_images": options.include_images,
                    "images_scale": options.images_scale,
                    "md_page_break_placeholder": options.md_page_break_placeholder,
                    "do_code_enrichment": options.do_code_enrichment,
                    "do_formula_enrichment": options.do_formula_enrichment,
                    "do_picture_classification": options.do_picture_classification,
                    "do_picture_description": options.do_picture_description,
                    "picture_description_area_threshold": options.picture_description_area_threshold
                }
                
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/v1/convert/file",
                        files=files,
                        data=data,
                        headers=self._get_headers(content_type=None)
                    )
                    response_data = self._handle_response(response)
                    return ConvertDocumentResponse(**response_data)
        else:
            # File-like object
            files = {"files": ("document", file_path, "application/octet-stream")}
            data = {
                "target_type": target.kind,
                "from_formats": [fmt.value for fmt in options.from_formats],
                "to_formats": [fmt.value for fmt in options.to_formats],
                "image_export_mode": options.image_export_mode.value,
                "do_ocr": options.do_ocr,
                "force_ocr": options.force_ocr,
                "ocr_engine": options.ocr_engine.value,
                "pdf_backend": options.pdf_backend.value,
                "table_mode": options.table_mode.value,
                "table_cell_matching": options.table_cell_matching,
                "pipeline": options.pipeline.value,
                "page_range": options.page_range,
                "document_timeout": options.document_timeout,
                "abort_on_error": options.abort_on_error,
                "do_table_structure": options.do_table_structure,
                "include_images": options.include_images,
                "images_scale": options.images_scale,
                "md_page_break_placeholder": options.md_page_break_placeholder,
                "do_code_enrichment": options.do_code_enrichment,
                "do_formula_enrichment": options.do_formula_enrichment,
                "do_picture_classification": options.do_picture_classification,
                "do_picture_description": options.do_picture_description,
                "picture_description_area_threshold": options.picture_description_area_threshold
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/convert/file",
                    files=files,
                    data=data,
                    headers=self._get_headers(content_type=None)
                )
                response_data = self._handle_response(response)
                return ConvertDocumentResponse(**response_data)
