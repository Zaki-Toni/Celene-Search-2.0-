"""Utilities to load documents from the filesystem into Document objects.

`FileDocumentLoader` scans a directory and uses the extractor
strategies from :mod:`src.infrastructure.fs.extractors` to convert
supported files into `Document` instances.

The loader is intentionally simple: it ignores subdirectories and
unsupported file extensions and returns a list of processed
documents.
"""

import os

from src.core.interfaces import BaseExtractor
from src.core.models import Document

####DEBEMOS USAR LOGGIN EN LUGAR DE PRINT

from src.infrastructure.fs.extractors import (
    DocxExtractor,
    HTMLExtractor,
    PDFExtractor,
    TextExtractor,
)


class FileDocumentLoader:
    """Scan a source folder and convert supported files into Documents.

    Attributes:
        source_dir: Path to the directory that will be scanned.
        _extractors: Mapping of file extension to extractor instance.
    """

    def __init__(self, source_dir: str):
        self.source_dir = source_dir

        # Mapeo: Extensión -> Estrategia de extracción
        # Usamos tipado moderno dict[str, BaseExtractor]
        self._extractors: dict[str, BaseExtractor] = {
            ".txt": TextExtractor(),
            ".pdf": PDFExtractor(),
            ".docx": DocxExtractor(),
            ".html": HTMLExtractor(),
            ".htm": HTMLExtractor(),
        }

    def load_all(self) -> list[Document]:
        """Scan the `source_dir` and return a list of `Document` objects.

        The loader will iterate files at the top level of `source_dir`,
        select an extractor based on file extension and build a
        `Document` for each file that yields content.

        Returns:
            A list of `Document` instances. If the directory does not
            exist or no supported files are found an empty list is
            returned.
        """
        if not os.path.exists(self.source_dir):
            print(f"Advertencia: El directorio {self.source_dir} no existe.")
            return []

        documents: list[Document] = []

        print(f"Escaneando directorio: {self.source_dir} ...")

        for filename in os.listdir(self.source_dir):
            file_path = os.path.join(self.source_dir, filename)

            # Saltamos carpetas, solo archivos
            if not os.path.isfile(file_path):
                continue

            # Obtener extensión (ej: '.pdf') en minúsculas
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

            # Verificar si tenemos un extractor para esa extensión
            if ext in self._extractors:
                extractor = self._extractors[ext]

                # Usamos el extractor
                content = extractor.get_text(file_path)

                if content:
                    doc = Document(
                        title=filename,
                        content=content,
                        path=file_path,
                        metadata={"type": ext},
                    )
                    documents.append(doc)
                    print(f"✅ Cargado: {filename}")
                else:
                    print(f"⚠️  Archivo vacío o corrupto: {filename}")
            else:
                # Cositas para hacer luego
                # Avisar de archivos ignorados
                # print(f"Ignorando formato no soportado: {filename}")
                pass

        return documents
