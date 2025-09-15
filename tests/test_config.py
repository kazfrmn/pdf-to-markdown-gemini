import unittest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch
from src.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        # Store original working directory
        self.original_cwd = os.getcwd()

    def tearDown(self):
        # Restore original working directory
        os.chdir(self.original_cwd)

    def test_config_with_env_file(self):
        # Create temporary directory with .env file
        with tempfile.TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / '.env'
            env_file.write_text("""GOOGLE_API_KEY=test_key
MAX_TOKENS_PER_SECTION=50000
IMAGE_DPI=150
OUTPUT_DIR=custom_output
LOG_LEVEL=DEBUG
""")

            # Change to temp directory
            os.chdir(temp_dir)

            config = Config()
            self.assertEqual(config.gemini_api_key, 'test_key')
            self.assertEqual(config.max_tokens_per_section, 50000)
            self.assertEqual(config.image_dpi, 150)
            self.assertEqual(config.output_dir, 'custom_output')
            self.assertEqual(config.log_level, 'DEBUG')

    def test_config_defaults(self):
        # Create temporary directory with minimal .env file
        with tempfile.TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / '.env'
            env_file.write_text("GOOGLE_API_KEY=test_key\n")

            # Change to temp directory
            os.chdir(temp_dir)

            config = Config()
            self.assertEqual(config.gemini_api_key, 'test_key')
            self.assertEqual(config.max_tokens_per_section, 100000)
            self.assertEqual(config.image_dpi, 300)
            self.assertEqual(config.output_dir, 'output')
            self.assertEqual(config.log_level, 'INFO')

    def test_config_missing_api_key(self):
        # Create temporary directory without .env file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory (no .env file)
            os.chdir(temp_dir)

            with self.assertRaises(ValueError):
                Config()

    def test_config_placeholder_api_key(self):
        # Create temporary directory with placeholder API key
        with tempfile.TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / '.env'
            env_file.write_text("GOOGLE_API_KEY=your_api_key_here\n")

            # Change to temp directory
            os.chdir(temp_dir)

            with self.assertRaises(ValueError):
                Config()

if __name__ == '__main__':
    unittest.main()