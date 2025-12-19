"""Data models used across the application (DTOs and simple value objects)."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    """Represents a document ready to be indexed.

    Attributes:
        title: Human-friendly document title.
        content: Full textual content extracted from the source file.
        path: Original file system path or logical identifier.
        metadata: Arbitrary key/value metadata associated with the document.
    """

    title: str
    content: str
    path: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """Result returned by a search operation.

    Fields are minimal: title, path, score and an optional snippet to be
    displayed in the UI.
    """

    title: str
    path: str
    score: float
    snippet: str = ""


@dataclass
class ExpandedQuery:
    """Representation of a user query after NLP enrichment.

    The object contains the original text (for debugging or display)
    and a list of expanded terms produced by the NLP pipeline.
    """

    original_text: str
    expanded_terms: list[str]

    def to_boolean_query(self) -> str:
        """Create a boolean search string from `expanded_terms`.

        The method sanitizes the expanded terms and joins them using the
        logical `OR` operator, wrapping each term in double quotes to
        favour phrase/term matching depending on the backend.

        Returns:
            A string suitable to pass to the search backend, or the
            original text if there are no valid expanded terms.
        """
        clean_terms = [t.replace('"', "") for t in self.expanded_terms if t.strip()]

        if not clean_terms:
            return self.original_text

        return " OR ".join(f'"{term}"' for term in clean_terms)
