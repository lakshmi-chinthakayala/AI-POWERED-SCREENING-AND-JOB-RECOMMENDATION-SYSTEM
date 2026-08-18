"""
OCR Processing Service.
Integrates pytesseract and PyMuPDF image rendering for scanned image resumes.
Gracefully handles environments where Tesseract OCR engine binaries are not installed.
"""

import io
import fitz
try:
    import pytesseract
    from PIL import Image
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False

def extract_text_with_ocr(file_bytes: bytes, file_type: str = "pdf") -> str:
    """
    Performs OCR image extraction if Tesseract is available.
    """
    if not HAS_PYTESSERACT:
        print("[OCR Service] Pytesseract/Pillow library not loaded.")
        return ""

    ocr_text = ""
    try:
        if file_type == "pdf":
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                pix = page.get_pixmap(dpi=150)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_text += pytesseract.image_to_string(img) + "\n"
            doc.close()
        else:
            img = Image.open(io.BytesIO(file_bytes))
            ocr_text = pytesseract.image_to_string(img)
    except Exception as e:
        print(f"[OCR Extraction Warning] {e}. Ensure Tesseract binary is installed and added to PATH.")
        
    return ocr_text.strip()
