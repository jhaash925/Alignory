import shutil
import subprocess
import tempfile

import docx
import pdfplumber


def word_count(text):
    return len((text or "").split())


def _ocr_pdf_page(page):
    if not shutil.which("tesseract"):
        return "", "tesseract_unavailable"

    try:
        image = page.to_image(resolution=180).original

        with tempfile.NamedTemporaryFile(suffix=".png") as image_file:
            image.save(image_file.name)
            result = subprocess.run(
                ["tesseract", image_file.name, "stdout", "--psm", "6"],
                check=False,
                capture_output=True,
                text=True,
                timeout=20,
            )

        if result.returncode != 0:
            return "", "ocr_failed"

        return result.stdout.strip(), "ocr"

    except subprocess.TimeoutExpired:
        return "", "ocr_timeout"
    except Exception:
        return "", "ocr_failed"


def extract_text_from_pdf(file):
    text_parts = []
    page_diagnostics = []

    with pdfplumber.open(file) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = (page.extract_text() or "").strip()
            direct_words = word_count(page_text)
            extraction_method = "direct"
            ocr_text = ""
            ocr_status = "not_needed"

            if direct_words < 8:
                ocr_text, ocr_status = _ocr_pdf_page(page)

                if word_count(ocr_text) > direct_words:
                    page_text = ocr_text
                    extraction_method = "ocr"

            if page_text:
                text_parts.append(page_text)

            page_diagnostics.append(
                {
                    "page": page_number,
                    "method": extraction_method,
                    "direct_words": direct_words,
                    "ocr_words": word_count(ocr_text),
                    "ocr_status": ocr_status,
                }
            )

    text = "\n".join(text_parts)
    diagnostics = {
        "file_type": "pdf",
        "pages": len(page_diagnostics),
        "method": "ocr_fallback" if any(item["method"] == "ocr" for item in page_diagnostics) else "direct",
        "ocr_available": bool(shutil.which("tesseract")),
        "text_words": word_count(text),
        "pages_with_ocr": sum(1 for item in page_diagnostics if item["method"] == "ocr"),
        "page_diagnostics": page_diagnostics,
    }

    return text, diagnostics


def extract_text_from_docx(file):
    document = docx.Document(file)
    text = "\n".join([para.text for para in document.paragraphs])
    return text, {
        "file_type": "docx",
        "method": "direct",
        "text_words": word_count(text),
    }
