"""Whoosh writer implementation.

This module contains a small adapter that writes `Document` objects
to a Whoosh index using the provided `WhooshAdapter`.
"""

from src.core.interfaces import IIndexWriter
from src.core.models import Document
from src.infrastructure.search_engine.adapter import WhooshAdapter

###CAMBIAR DEBUG A LOGGIN


class WhooshWriter(IIndexWriter):
    """Writer that persists documents into a Whoosh index.

    The writer maintains a Whoosh writer instance and provides
    `add_documents` and `commit` operations required by the
    `IIndexWriter` contract.
    """

    def __init__(self, adapter: WhooshAdapter):
        self.adapter = adapter
        self.ix = adapter.get_index()
        self._writer = self.ix.writer()

    def add_documents(self, docs: list[Document]) -> None:
        """Add multiple documents to the index buffer.

        Args:
            docs: List of `Document` instances to be indexed.
        """
        for doc in docs:
            try:
                self._writer.add_document(
                    title=doc.title, content=doc.content, path=doc.path
                )
            except Exception as e:
                print(f"Error indexando {doc.title}: {e}")

    def commit(self) -> None:
        """Commit pending documents to disk and reset the writer.

        If an error occurs during commit the writer will attempt to
        cancel the pending transaction.
        """
        try:
            self._writer.commit()
            self._writer = self.ix.writer()
        except Exception as e:
            print(f"Error en commit: {e}")
            self._writer.cancel()
