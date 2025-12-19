"""High-level service that orchestrates ingestion and indexing."""

from src.core.interfaces import IIndexWriter
from src.infrastructure.fs.loader import FileDocumentLoader


class IndexingService:
    """Service responsible for loading documents and writing them to the index."""

    def __init__(self, writer: IIndexWriter, loader: FileDocumentLoader):
        self.writer = writer
        self.loader = loader

    def run_indexing(self) -> int:
        """Execute a full ingestion and indexing process.

        Returns:
            The number of documents that were indexed.
        """
        # 1. Cargar documentos
        print("Cargando documentos del disco...")
        docs = self.loader.load_all()

        if not docs:
            print("No se encontraron documentos.")
            return 0

        # 2. Guardar en índice
        print(f"Indexando {len(docs)} archivos...")
        self.writer.add_documents(docs)

        # 3. Confirmar cambios
        self.writer.commit()
        print("Cambios guardados correctamente.")

        return len(docs)