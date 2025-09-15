import os
from pdf2image import convert_from_path
from PIL import Image
import tempfile

def convert_pdf_to_images(pdf_path: str, dpi: int = 300) -> list[Image.Image]:
    """
    Convert PDF pages to PIL Images.

    Args:
        pdf_path: Path to the PDF file
        dpi: DPI for image conversion (higher = better quality)

    Returns:
        List of PIL Image objects, one per page
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        # Get the directory of this script and construct poppler path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        poppler_path = os.path.join(project_root, 'poppler', 'poppler-24.02.0', 'Library', 'bin')

        images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
        return images
    except Exception as e:
        raise RuntimeError(f"Failed to convert PDF to images: {str(e)}")

def get_pdf_page_count(pdf_path: str) -> int:
    """
    Get the number of pages in a PDF.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Number of pages
    """
    images = convert_pdf_to_images(pdf_path, dpi=72)  # Low DPI for count only
    return len(images)