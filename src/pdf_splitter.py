from typing import List, Tuple
from PIL import Image
from .gemini_client import GeminiClient
from .pdf_processor import convert_pdf_to_images

class PDFSplitter:
    def __init__(self, gemini_client: GeminiClient, max_tokens_per_section: int = 100000):
        """
        Initialize PDF splitter.

        Args:
            gemini_client: Configured Gemini client
            max_tokens_per_section: Maximum tokens per section
        """
        self.gemini_client = gemini_client
        self.max_tokens_per_section = max_tokens_per_section

    def split_pdf_into_sections(self, pdf_path: str) -> List[Tuple[List[Image.Image], int, int]]:
        """
        Split PDF into sections based on token limits.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of tuples: (images, start_page, end_page)
        """
        images = convert_pdf_to_images(pdf_path)
        if not images:
            return []

        sections = []
        current_section_images = []
        current_tokens = 0
        start_page = 0

        for i, img in enumerate(images):
            img_tokens = self.gemini_client.estimate_token_count([img])

            if current_tokens + img_tokens > self.max_tokens_per_section and current_section_images:
                # Save current section
                sections.append((current_section_images, start_page, i - 1))
                # Start new section
                current_section_images = [img]
                current_tokens = img_tokens
                start_page = i
            else:
                current_section_images.append(img)
                current_tokens += img_tokens

        # Add the last section
        if current_section_images:
            sections.append((current_section_images, start_page, len(images) - 1))

        return sections

    def should_split_pdf(self, pdf_path: str) -> bool:
        """
        Determine if PDF should be split based on total token count.

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if PDF should be split
        """
        images = convert_pdf_to_images(pdf_path, dpi=72)  # Low DPI for estimation
        total_tokens = self.gemini_client.estimate_token_count(images)
        return total_tokens > self.max_tokens_per_section