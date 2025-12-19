"""Extractors for different file formats.

This module implements small, pluggable extractor strategies that
convert files on disk into plain text. Each extractor implements the
`BaseExtractor` interface and provides a `get_text(file_path)` method
that returns the extracted text or `None` on failure.

Note: extractors currently use simple exception handling and `print`
statements for diagnostics; in production code a proper logger should
be used instead.
"""

from bs4 import BeautifulSoup
from docx import Document as DocxReader
from pypdf import PdfReader

####DEBEMOS MEJORARA LOS EXTRACTORES PARA QUE USEN LOGGIN EN LUGAR DE PRINT

# Importamos la interfaz que deben cumplir
from src.core.interfaces import BaseExtractor


class TextExtractor(BaseExtractor):
    """Extractor for plain text files (.txt).

    The implementation reads the file using UTF-8 and returns the raw
    content as a string. Binary or non-text files will typically cause
    the extractor to return ``None``.
    """

    def get_text(self, file_path: str) -> str | None:
        """Read a text file and return its contents.

        Args:
            file_path: Path to the file to read.

        Returns:
            The file content as a string, or ``None`` if an error occurs.
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            print(f"Error leyendo TXT {file_path}: {e}")
            return None


class PDFExtractor(BaseExtractor):
    """Extractor for PDF files using ``pypdf``.

    Pages are extracted and concatenated using newline separators.
    """

    def get_text(self, file_path: str) -> str | None:
        """Extract text from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            A single string with text from all pages, or ``None`` if an
            error occurs during parsing.
        """
        try:
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_parts.append(extracted)
            return "\n".join(text_parts)
        except Exception as e:
            print(f"Error leyendo PDF {file_path}: {e}")
            return None


class DocxExtractor(BaseExtractor):
    """Extractor for Microsoft Word documents (.docx)."""

    def get_text(self, file_path: str) -> str | None:
        """Extract and concatenate paragraph text from a DOCX file.

        Args:
            file_path: Path to the .docx file.

        Returns:
            A string with the joined paragraphs, or ``None`` on error.
        """
        try:
            doc = DocxReader(file_path)
            # Unimos los párrafos con saltos de línea
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"Error leyendo DOCX {file_path}: {e}")
            return None


class HTMLExtractor(BaseExtractor):
    """Extractor for HTML files using BeautifulSoup to strip tags."""

    def get_text(self, file_path: str) -> str | None:
        """Open an HTML file and return visible text.

        Args:
            file_path: Path to the HTML file.

        Returns:
            The visible text extracted from the document, or ``None`` on
            failure.
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f, "html.parser")
                # get_text con separator=' ' evita que palabras pegadas de dif etiquetas se unan
                return soup.get_text(separator=" ")
        except Exception as e:
            print(f"Error leyendo HTML {file_path}: {e}")
            return None
