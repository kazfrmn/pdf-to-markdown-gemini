# PDF to Markdown Converter

A Python program that converts PDF files to Markdown format using Google's Gemini AI. The program can handle large PDFs by automatically splitting them into sections when they exceed token limits.

## Features

- Convert PDF pages to images and process with Gemini AI
- Automatic splitting of large PDFs based on token limits
- Configurable output with page range naming
- Command-line interface
- Environment-based configuration
- Comprehensive error handling and logging

## Requirements

- Python 3.8+
- Poppler (for PDF processing)
- A Google Gemini API key

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment configuration:
   ```bash
   cp .env.example .env
   # Edit .env and add your actual Gemini API key
   ```

3. Install Poppler (required for PDF processing):
   - **Windows**: Download from [poppler releases](https://blog.alivate.com.au/poppler-windows/) and add to PATH
   - **macOS**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils`

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your actual Gemini API key:
   ```env
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   MAX_TOKENS_PER_SECTION=100000
   IMAGE_DPI=300
   OUTPUT_DIR=output
   LOG_LEVEL=INFO
   ```

**Important:** Never commit your actual `.env` file to version control. The `.env.example` file is tracked and contains placeholder values.

Alternatively, you can set environment variables directly in your system.

## Usage

### Basic Usage

```bash
python -m src.main path/to/your/document.pdf
```

### Advanced Usage

```bash
python -m src.main path/to/document.pdf \
  --output-dir ./markdown_output \
  --max-tokens 50000 \
  --dpi 150
```

### Options

- `pdf_path`: Path to the PDF file (required)
- `-o, --output-dir`: Output directory for Markdown files (default: output)
- `--max-tokens`: Maximum tokens per section (default: 100000)
- `--dpi`: DPI for PDF to image conversion (default: 300)

## Output

- For small PDFs: Single `document.md` file
- For large PDFs: Multiple files like `document_pages_1-10.md`, `document_pages_11-20.md`

## How It Works

1. Converts PDF pages to high-quality images
2. Estimates token count for Gemini API limits
3. Splits large documents into sections if needed
4. Sends images to Gemini AI for Markdown conversion
5. Saves results with descriptive filenames

## Error Handling

The program includes comprehensive error handling for:
- Missing or invalid PDF files
- Gemini API errors
- Configuration issues
- File system errors

## Testing

Run unit tests:

```bash
python -m unittest discover tests/
```

## Dependencies

- `google-generativeai`: Gemini AI integration
- `pdf2image`: PDF to image conversion
- `Pillow`: Image processing
- `python-dotenv`: Environment configuration

## License

This project is open source. Please check individual dependency licenses.