"""Abstract interfaces used across the application.

This module declares small ABCs that decouple the application logic
from concrete implementations (index readers/writers, NLP
components and file extractors). Implementers should follow these
contracts to ensure compatibility with the higher-level services.
"""

import abc
from typing import Any

from src.core.models import Document, ExpandedQuery, SearchResult


class IIndexWriter(abc.ABC):
    """Contract for index writers.

    Implementations must provide a way to add documents and persist
    the pending changes.
    """

    @abc.abstractmethod
    def add_documents(self, docs: list[Document]) -> None:
        """Add multiple documents to the pending write set.

        Implementations should accept a list of `Document` instances
        and stage them for persistence. No return value is expected.
        """

    @abc.abstractmethod
    def commit(self) -> None:
        """Persist all staged documents to permanent storage.

        This method should ensure that previously added documents are
        durably written, raising on unrecoverable errors.
        """


class IIndexReader(abc.ABC):
    """Contract for index readers used to perform searches."""

    @abc.abstractmethod
    def search(self, query: ExpandedQuery) -> list[SearchResult]:
        """Execute a search against the index.

        Args:
            query: An `ExpandedQuery` produced by the NLP pipeline.

        Returns:
            A list of `SearchResult` objects matching the query.
        """


class INLPComponent(abc.ABC):
    """Contract for NLP pipeline components.

    Each component implements a small `process` method that receives
    and returns data. The concrete types depend on the component
    (e.g. str -> list[str], list[str] -> list[Tuple[str,str]], etc.).
    """

    @abc.abstractmethod
    def process(self, data: Any) -> Any:
        """Process the provided data and return the transformed result."""


class BaseExtractor(abc.ABC):
    """Contract for file extractors that return plain text."""

    @abc.abstractmethod
    def get_text(self, file_path: str) -> str | None:
        """Extract textual content from ``file_path``.

        Args:
            file_path: File system path to the input file.

        Returns:
            The extracted text as a string, or ``None`` if extraction
            failed or the file format is unsupported.
        """
