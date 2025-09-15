import os
from typing import List, Tuple
from PIL import Image

class OutputHandler:
    def __init__(self, output_dir: str = "output"):
        """
        Initialize output handler.

        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_markdown_filename(self, base_name: str, start_page: int, end_page: int) -> str:
        """
        Generate filename for Markdown output.

        Args:
            base_name: Base name from PDF file
            start_page: Starting page number (0-based)
            end_page: Ending page number (0-based)

        Returns:
            Filename string
        """
        if start_page == end_page:
            page_str = f"page_{start_page + 1}"
        else:
            page_str = f"pages_{start_page + 1}-{end_page + 1}"

        return f"{base_name}_{page_str}.md"

    def save_markdown(self, content: str, filename: str) -> str:
        """
        Save Markdown content to file.

        Args:
            content: Markdown content
            filename: Output filename

        Returns:
            Full path to saved file
        """
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    def process_sections(self, sections: List[Tuple[List[Image.Image], int, int]],
                        base_name: str, markdown_contents: List[str]) -> List[str]:
        """
        Process sections and save corresponding Markdown files.

        Args:
            sections: List of (images, start_page, end_page) tuples
            base_name: Base name for output files
            markdown_contents: List of Markdown strings corresponding to sections

        Returns:
            List of saved file paths
        """
        saved_files = []

        for i, ((images, start_page, end_page), content) in enumerate(zip(sections, markdown_contents)):
            filename = self.generate_markdown_filename(base_name, start_page, end_page)
            filepath = self.save_markdown(content, filename)
            saved_files.append(filepath)

        return saved_files