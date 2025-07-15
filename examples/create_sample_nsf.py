"""
Script to create a sample NSF file for testing the converter.

This creates a mock NSF file with basic structure for demonstration purposes.
"""

import struct
from pathlib import Path


def create_sample_nsf(output_path: Path) -> None:
    """Create a sample NSF file for testing."""
    
    # Create basic NSF file structure
    with open(output_path, 'wb') as f:
        # Write NSF file header
        f.write(b'\x1a\x00')  # Signature
        f.write(struct.pack('<H', 43))  # Version
        f.write(struct.pack('<H', 128))  # Info buffer size
        f.write(struct.pack('<H', 1))   # Class ID
        f.write(b'\x00' * 12)  # Padding
        
        # Write database header (simplified)
        db_header = b'Sample Notes Database' + b'\x00' * 107
        f.write(db_header)
        
        # Write some sample notes (very simplified)
        for i in range(5):
            # Note header
            f.write(struct.pack('<H', 1024))  # Note class (design note)
            f.write(b'\x00' * 2)  # Padding
            f.write(struct.pack('<L', 64))    # Note length
            f.write(b'\x00' * 8)  # More padding
            
            # Note data (simplified)
            note_data = f'Sample note {i+1} data'.encode('utf-8')
            note_data += b'\x00' * (64 - len(note_data))
            f.write(note_data)
        
        # Write some document notes
        for i in range(3):
            # Document note header
            f.write(struct.pack('<H', 512))   # Note class (document)
            f.write(b'\x00' * 2)  # Padding
            f.write(struct.pack('<L', 64))    # Note length
            f.write(b'\x00' * 8)  # More padding
            
            # Document data
            doc_data = f'Document {i+1} content'.encode('utf-8')
            doc_data += b'\x00' * (64 - len(doc_data))
            f.write(doc_data)


if __name__ == '__main__':
    # Create examples directory
    examples_dir = Path(__file__).parent
    examples_dir.mkdir(exist_ok=True)
    
    # Create sample NSF file
    sample_nsf = examples_dir / 'sample.nsf'
    create_sample_nsf(sample_nsf)
    
    print(f"Created sample NSF file: {sample_nsf}")
    print(f"File size: {sample_nsf.stat().st_size} bytes")

