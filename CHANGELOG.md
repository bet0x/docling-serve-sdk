# Changelog

All notable changes to the Docling Serve SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-09-28

### Fixed
- **ImageRefMode Enum**: Fixed `REFERENCE` value from `"reference"` to `"referenced"` to match docling-serve API expectations
  - This resolves the 422 validation error when using `ImageRefMode.REFERENCE`
  - The SDK now correctly sends `"referenced"` as expected by the docling-serve API
  - Fixes issue where `image_export_mode=ImageRefMode.REFERENCE` would fail with validation error

### Technical Details
- Updated `ImageRefMode.REFERENCE` enum value in `models.py`
- Ensures compatibility with docling-serve API validation requirements
- Maintains backward compatibility for other enum values

## [1.2.0] - 2025-09-27

### Added
- **Initial Release**: Complete Python SDK for Docling Serve API
- **Type Safety**: Full Pydantic model support with type hints
- **Async/Sync Support**: Both synchronous and asynchronous client methods
- **Comprehensive API Coverage**: Support for all docling-serve endpoints
- **Error Handling**: Robust error handling with custom exception types
- **Documentation**: Complete API documentation and usage examples

### Features
- Document conversion (file and URL sources)
- Chunking operations (hybrid and hierarchical)
- Task status monitoring and WebSocket support
- Health checks and system status
- Configurable timeouts and retry logic
- Support for all input/output formats
- Image processing options
- OCR configuration
- Table processing modes
