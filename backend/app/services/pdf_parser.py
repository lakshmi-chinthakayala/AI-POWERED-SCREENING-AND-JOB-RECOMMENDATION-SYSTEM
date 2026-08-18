"""
PDF Document Processing Service.
Uses PyMuPDF (fitz) to extract raw text content from vector PDF resumes.
Falls back to OCR if PDF contains scanned image pages.
"""

import fitz  # PyMuPDF
from backend.app.services.ocr_service import extract_text_with_ocr

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from PDF file bytes.
    If text yield is very low (< 50 chars), attempts OCR fallback.
    """
    extracted_text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            extracted_text += page.get_text() + "\n"
        doc.close()
    except Exception as e:
        print(f"[PDF Parser Error] {e}")

    # Fallback to OCR if PDF appears to be a scanned image
    if len(extracted_text.strip()) < 50:
        ocr_text = extract_text_with_ocr(file_bytes, file_type="pdf")
        if len(ocr_text.strip()) > len(extracted_text.strip()):
            extracted_text = ocr_text

    return extracted_text.strip()
