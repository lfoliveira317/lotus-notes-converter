"""
Exception classes for the Lotus Notes to React converter.
"""


class LotusConverterError(Exception):
    """Base exception for all converter errors."""
    pass


class NSFParseError(LotusConverterError):
    """Raised when NSF file parsing fails."""
    pass


class UnsupportedNSFVersion(NSFParseError):
    """Raised when NSF file version is not supported."""
    pass


class InvalidNSFFile(NSFParseError):
    """Raised when NSF file is invalid or corrupted."""
    pass


class ReactGenerationError(LotusConverterError):
    """Raised when React code generation fails."""
    pass


class TemplateError(ReactGenerationError):
    """Raised when template processing fails."""
    pass


class ValidationError(LotusConverterError):
    """Raised when data validation fails."""
    pass


class ConversionError(LotusConverterError):
    """Raised when conversion process fails."""
    pass

