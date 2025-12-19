"""Search service layer.

This module defines a thin application service that orchestrates the
query flow: it expands the raw user query using the NLP pipeline and
delegates the actual search to an index reader implementation.
"""

from src.core.interfaces import IIndexReader
from src.core.models import SearchResult
from src.domain_nlp.pipeline import NLPPipeline


class SearchService:
    """Coordinate query processing and index lookup.

    The service is intentionally simple and acts as an anti-corruption
    layer between web views and lower-level components.
    """

    def __init__(self, reader: IIndexReader, nlp: NLPPipeline):
        """Create a SearchService.

        Args:
            reader: An object implementing `IIndexReader` used to run
                searches against the persisted index.
            nlp: An `NLPPipeline` instance used to process and expand
                raw user input.
        """
        self.reader = reader
        self.nlp = nlp

    def execute_search(self, raw_query: str) -> list[SearchResult]:
        """Process a raw query string and return search results.

        The method performs minimal validation, uses the NLP pipeline to
        expand or normalise the input, and forwards the resulting query
        object to the configured reader.

        Args:
            raw_query: The raw user input string from the UI.

        Returns:
            A list of `SearchResult` instances (may be empty).
        """
        if not raw_query.strip():
            return []

        # 1. Expandir la consulta con NLP (Sinónimos, correcciones, etc.)
        expanded_query = self.nlp.process(raw_query)
        
        # Debugging info: keep prints for development; replace with
        # proper logging in production.
        print(f"DEBUG - Original: '{expanded_query.original_text}'")
        print(f"DEBUG - Expandida: {expanded_query.to_boolean_query()}")

        # 2. Ejecutar la búsqueda en el índice
        results = self.reader.search(expanded_query)

        return results