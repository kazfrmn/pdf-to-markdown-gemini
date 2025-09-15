import os
import google.generativeai as genai
from PIL import Image
from typing import List

class GeminiClient:
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini client.

        Args:
            api_key: Gemini API key. If None, uses GOOGLE_API_KEY env var.
        """
        if api_key is None:
            api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("Gemini API key not provided. Set GOOGLE_API_KEY environment variable.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Using 1.5-flash as 2.0 may not be available yet

    def generate_markdown_from_images(self, images: List[Image.Image]) -> str:
        """
        Generate Markdown from a list of images using Gemini.

        Args:
            images: List of PIL Image objects

        Returns:
            Markdown string
        """
        if not images:
            return ""

        # Combine images into a single prompt
        prompt = """Convert the content of these images to Markdown format.
        Preserve the structure, headings, lists, tables, and formatting as much as possible.
        Use appropriate Markdown syntax for text formatting."""

        # For multiple images, we need to upload them as files
        image_parts = []
        for img in images:
            image_parts.append(img)

        try:
            response = self.model.generate_content([prompt] + image_parts)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Failed to generate Markdown from images: {str(e)}")

    def estimate_token_count(self, images: List[Image.Image]) -> int:
        """
        Estimate token count for a list of images.
        This is a rough estimate based on image dimensions.

        Args:
            images: List of PIL Image objects

        Returns:
            Estimated token count
        """
        total_pixels = 0
        for img in images:
            width, height = img.size
            total_pixels += width * height

        # Rough estimate: 1 token per ~100 pixels (this is approximate)
        estimated_tokens = total_pixels // 100
        return max(estimated_tokens, 1)  # At least 1 token