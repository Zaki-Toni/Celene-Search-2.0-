"""Reader implementation that executes queries against a Whoosh index.

This module exposes a `WhooshReader` that converts an
:class:`ExpandedQuery` into a Whoosh-parsable boolean query and
returns a list of `SearchResult` objects suitable for UI rendering.
"""

from typing import cast, Any
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh.highlight import ContextFragmenter

from src.core.interfaces import IIndexReader
from src.core.models import SearchResult, ExpandedQuery
from src.infrastructure.search_engine.adapter import WhooshAdapter


class WhooshReader(IIndexReader):
    """IIndexReader implementation using Whoosh."""

    def __init__(self, adapter: WhooshAdapter):
        self.adapter = adapter
        self.ix = adapter.get_index()

    def search(self, query: ExpandedQuery) -> list[SearchResult]:
        """Execute a search for the given expanded query.

        The method builds a boolean query string from the
        :class:`ExpandedQuery`, parses it against both `title` and
        `content` fields and returns a list of `SearchResult` values
        containing a highlighted snippet and a safe numeric score.
        """
        results_list: list[SearchResult] = []

        query_str = query.to_boolean_query()

        with self.ix.searcher() as searcher:
            # Search both title and content fields
            parser = MultifieldParser(["title", "content"], self.ix.schema, group=OrGroup)  # type: ignore

            try:
                parsed_query = parser.parse(query_str)

                hits = searcher.search(parsed_query, limit=20)

                # Configure snippet highlighting
                hits.fragmenter = ContextFragmenter(maxchars=200, surround=40)

                for hit in hits:
                    # Try to obtain a highlighted snippet, fall back to raw content
                    snippet = hit.highlights("content") or cast(str, hit.get("content", ""))[:200]

                    # Safe score handling
                    raw_score = hit.score
                    safe_score: float = float(raw_score) if raw_score is not None else 0.0

                    result = SearchResult(
                        title=cast(str, hit.get("title", "Sin título")),
                        path=cast(str, hit.get("path", "")),
                        score=safe_score,
                        snippet=snippet,
                    )
                    results_list.append(result)

            except Exception as e:
                print(f"Error durante la búsqueda: {e}")
                return []

        return results_list