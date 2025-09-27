"""
Setup configuration for Docling Serve SDK.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docling-serve-sdk",
    version="1.0.0",
    author="RAG MCP Team",
    author_email="team@example.com",
    description="A Python SDK for interacting with Docling Serve API using Pydantic models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/docling-serve-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "docling-sdk=docling_serve_sdk.cli:main",
        ],
    },
    keywords="docling document processing ocr pdf conversion chunking",
    project_urls={
        "Bug Reports": "https://github.com/your-org/docling-serve-sdk/issues",
        "Source": "https://github.com/your-org/docling-serve-sdk",
        "Documentation": "https://github.com/your-org/docling-serve-sdk#readme",
    },
)
