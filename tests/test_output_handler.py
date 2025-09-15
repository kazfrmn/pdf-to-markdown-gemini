import unittest
import tempfile
import os
from pathlib import Path
from src.output_handler import OutputHandler

class TestOutputHandler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.handler = OutputHandler(self.temp_dir)

    def tearDown(self):
        # Clean up temp directory
        for file in Path(self.temp_dir).glob("*"):
            file.unlink()
        Path(self.temp_dir).rmdir()

    def test_generate_markdown_filename_single_page(self):
        filename = self.handler.generate_markdown_filename("document", 0, 0)
        self.assertEqual(filename, "document_page_1.md")

    def test_generate_markdown_filename_multiple_pages(self):
        filename = self.handler.generate_markdown_filename("document", 0, 4)
        self.assertEqual(filename, "document_pages_1-5.md")

    def test_save_markdown(self):
        content = "# Test Header\n\nThis is a test."
        filename = "test.md"
        filepath = self.handler.save_markdown(content, filename)

        self.assertTrue(os.path.exists(filepath))
        with open(filepath, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), content)

if __name__ == '__main__':
    unittest.main()