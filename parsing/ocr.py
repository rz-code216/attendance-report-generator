import os
from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image

# Tesseract location: env variable if set, else the default Windows install path.
# In Docker/Linux it is found automatically.
_DEFAULT_WINDOWS_TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if os.environ.get("TESSERACT_CMD"):
    pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_CMD"]
elif _DEFAULT_WINDOWS_TESSERACT.exists():
    pytesseract.pytesseract.tesseract_cmd = str(_DEFAULT_WINDOWS_TESSERACT)

OCR_LANG = os.environ.get("OCR_LANG", "eng")


def list_pdfs(folder: Path) -> list[Path]:
    return sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() == ".pdf"
    )


def pdf_to_images(pdf_path: Path) -> list[Image.Image]:
    images = []
    with pymupdf.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap(dpi=400)
            images.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    return images


def image_to_text(image: Image.Image, psm: int = 6) -> str:
    """Run OCR on one image and return the raw text."""
    gray = image.convert("L")   # grayscale removes color noise
    return pytesseract.image_to_string(gray, lang=OCR_LANG, config=f"--psm {psm}")


def ocr_pdf(pdf_path: Path, psm: int = 6) -> str:
    """Full OCR for one PDF: PDF -> images -> text (all pages joined)."""
    images = pdf_to_images(pdf_path)
    return "\n".join(image_to_text(img, psm) for img in images)