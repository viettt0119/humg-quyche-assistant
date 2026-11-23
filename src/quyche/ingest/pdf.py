"""Trích text từ PDF.

Đây là bản tối giản dùng pypdf. Ở tuần 1 bạn sẽ so sánh với pymupdf và OCR
(thí nghiệm E1 trong EXPERIMENTS.md) rồi quyết định giữ cách nào.
"""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from quyche.schemas import Document

# Trung bình ít hơn ngần này ký tự mỗi trang thì nhiều khả năng là PDF scan (ảnh), cần OCR.
SCANNED_CHARS_PER_PAGE = 50


def load_document(path: Path) -> Document:
    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return Document(doc_id=path.stem.lower(), source_path=str(path), pages=pages)


def looks_scanned(doc: Document) -> bool:
    if not doc.pages:
        return True
    total = sum(len(p.strip()) for p in doc.pages)
    return total / len(doc.pages) < SCANNED_CHARS_PER_PAGE
