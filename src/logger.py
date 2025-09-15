import logging
import sys
from .config import Config

def setup_logger(config: Config) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        config: Configuration object

    Returns:
        Configured logger
    """
    logger = logging.getLogger('pdf_to_md')
    logger.setLevel(getattr(logging, config.log_level.upper(), logging.INFO))

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logger.level)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger

class PDFToMarkdownError(Exception):
    """Base exception for PDF to Markdown conversion errors."""
    pass

class PDFProcessingError(PDFToMarkdownError):
    """Error during PDF processing."""
    pass

class GeminiAPIError(PDFToMarkdownError):
    """Error during Gemini API interaction."""
    pass

class ConfigurationError(PDFToMarkdownError):
    """Error in configuration."""
    pass