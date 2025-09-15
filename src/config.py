import os
from dotenv import dotenv_values
from pathlib import Path

class Config:
    def __init__(self):
        # Load .env file from project root
        project_root = Path(__file__).parent.parent
        env_file = project_root / '.env'

        # Load values from .env file directly (prioritize over system env)
        env_values = {}
        if env_file.exists():
            env_values = dotenv_values(env_file)

        # API Configuration - prioritize .env file over system environment
        self.gemini_api_key = env_values.get('GOOGLE_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not self.gemini_api_key or self.gemini_api_key == 'your_api_key_here':
            raise ValueError("GOOGLE_API_KEY not set in .env file. Please update the .env file with your actual API key.")

        # Processing Configuration
        self.max_tokens_per_section = int(env_values.get('MAX_TOKENS_PER_SECTION') or os.getenv('MAX_TOKENS_PER_SECTION', '100000'))
        self.image_dpi = int(env_values.get('IMAGE_DPI') or os.getenv('IMAGE_DPI', '300'))

        # Output Configuration
        self.output_dir = env_values.get('OUTPUT_DIR') or os.getenv('OUTPUT_DIR', 'output')

        # Logging Configuration
        self.log_level = env_values.get('LOG_LEVEL') or os.getenv('LOG_LEVEL', 'INFO')

    def __str__(self):
        return f"Config(max_tokens={self.max_tokens_per_section}, dpi={self.image_dpi}, output_dir={self.output_dir})"