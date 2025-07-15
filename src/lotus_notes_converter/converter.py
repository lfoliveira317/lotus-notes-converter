"""
Main Converter Module

This module orchestrates the entire conversion process from NSF parsing
to React application generation.
"""

import logging
from pathlib import Path
from typing import Optional

from .models import ApplicationModel
from .parser import NSFParser
from .generator import ReactGenerator
from .exceptions import ConversionError


logger = logging.getLogger(__name__)


class NotesConverter:
    """Main converter class that orchestrates the conversion process."""
    
    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize the converter."""
        self.parser = NSFParser()
        self.generator = ReactGenerator(template_dir)
    
    def convert(self, nsf_file: Path, output_dir: Path) -> ApplicationModel:
        """Convert a Lotus Notes NSF file to a React application."""
        logger.info(f"Starting conversion of {nsf_file} to {output_dir}")
        
        try:
            # Validate inputs
            self._validate_inputs(nsf_file, output_dir)
            
            # Parse NSF file
            logger.info("Parsing NSF file...")
            app_model = self.parser.parse_file(nsf_file)
            
            # Generate React application
            logger.info("Generating React application...")
            self.generator.generate_react_app(app_model, output_dir)
            
            logger.info("Conversion completed successfully")
            return app_model
            
        except Exception as e:
            raise ConversionError(f"Conversion failed: {e}")
    
    def _validate_inputs(self, nsf_file: Path, output_dir: Path) -> None:
        """Validate input parameters."""
        if not nsf_file.exists():
            raise ConversionError(f"NSF file not found: {nsf_file}")
        
        if not nsf_file.is_file():
            raise ConversionError(f"NSF path is not a file: {nsf_file}")
        
        if output_dir.exists() and not output_dir.is_dir():
            raise ConversionError(f"Output path exists but is not a directory: {output_dir}")
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

