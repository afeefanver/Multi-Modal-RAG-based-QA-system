# src/ingestion/__init__.py
"""
Document ingestion module
Handles PDF parsing, table extraction, and image processing
"""

from .pdf_processor import MultiModalPDFProcessor

__all__ = ['MultiModalPDFProcessor']
