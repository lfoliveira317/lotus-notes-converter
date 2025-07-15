"""
Lotus Notes to React Converter

A comprehensive tool for converting Lotus Notes applications to modern React applications.
"""

__version__ = "1.0.0"
__author__ = "Manus AI"
__email__ = "manus@example.com"

from .models import ApplicationModel, FormModel, ViewModel, DocumentModel
from .parser import NSFParser
from .generator import ReactGenerator
from .converter import NotesConverter

__all__ = [
    "ApplicationModel",
    "FormModel", 
    "ViewModel",
    "DocumentModel",
    "NSFParser",
    "ReactGenerator",
    "NotesConverter",
]

