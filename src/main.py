#!/usr/bin/env python3
"""
PDF to Markdown Converter CLI
Converts PDF files to Markdown using Gemini AI.
"""

import argparse
import os
import sys
from pathlib import Path

from .config import Config
from .logger import setup_logger, PDFToMarkdownError
from .gemini_client import GeminiClient
from .pdf_splitter import PDFSplitter
from .output_handler import OutputHandler

def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF files to Markdown using Gemini AI"
    )
    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file to convert"
    )
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory for Markdown files (default: output)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Maximum tokens per section (default: 100000)"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        help="DPI for PDF to image conversion (default: 300)"
    )

    args = parser.parse_args()

    try:
        # Load configuration
        config = Config()

        # Override config with command line args
        if args.output_dir:
            config.output_dir = args.output_dir
        if args.max_tokens:
            config.max_tokens_per_section = args.max_tokens
        if args.dpi:
            config.image_dpi = args.dpi

        # Setup logging
        logger = setup_logger(config)
        logger.info("Starting PDF to Markdown conversion")

        # Validate input
        pdf_path = Path(args.pdf_path)
        if not pdf_path.exists():
            raise PDFToMarkdownError(f"PDF file not found: {pdf_path}")

        # Initialize components
        gemini_client = GeminiClient(config.gemini_api_key)
        splitter = PDFSplitter(gemini_client, config.max_tokens_per_section)
        output_handler = OutputHandler(config.output_dir)

        # Process PDF
        base_name = pdf_path.stem
        logger.info(f"Processing PDF: {pdf_path}")

        if splitter.should_split_pdf(str(pdf_path)):
            logger.info("PDF will be split into multiple sections")
            sections = splitter.split_pdf_into_sections(str(pdf_path))

            markdown_contents = []
            for i, (images, start_page, end_page) in enumerate(sections):
                logger.info(f"Processing section {i+1}: pages {start_page+1}-{end_page+1}")
                content = gemini_client.generate_markdown_from_images(images)
                markdown_contents.append(content)

            saved_files = output_handler.process_sections(sections, base_name, markdown_contents)
        else:
            logger.info("Processing PDF as single document")
            from .pdf_processor import convert_pdf_to_images
            images = convert_pdf_to_images(str(pdf_path), config.image_dpi)
            content = gemini_client.generate_markdown_from_images(images)

            filename = f"{base_name}.md"
            saved_file = output_handler.save_markdown(content, filename)
            saved_files = [saved_file]

        logger.info("Conversion completed successfully")
        print(f"Generated {len(saved_files)} Markdown file(s):")
        for file_path in saved_files:
            print(f"  - {file_path}")

    except PDFToMarkdownError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()