"""Natural Language Processing pipeline orchestration.

This module composes small, focused NLP components into a simple
pipeline that converts a raw query string into an :class:`ExpandedQuery`.
The pipeline is intentionally linear and easy to extend by adding or
replacing components.
"""

from src.core.models import ExpandedQuery
from src.domain_nlp.components import (
    TokenizerComponent,
    StopwordFilter,
    POSTagger,
    WordNetExpander,
)


class NLPPipeline:
    """Pipeline that tokenizes, filters, tags and expands queries."""

    def __init__(self):
        # Inicializamos los pasos del pipeline en orden estricto
        self.tokenizer = TokenizerComponent()
        self.sw_filter = StopwordFilter(language='english')
        self.tagger = POSTagger()
        self.expander = WordNetExpander()

    def process(self, raw_query: str) -> ExpandedQuery:
        """Process a raw query string through the NLP pipeline.

        Steps performed:
            1. Tokenization
            2. Stopword filtering
            3. POS tagging
            4. Lexical expansion (synonyms)

        Args:
            raw_query: The user-provided query string.

        Returns:
            An :class:`ExpandedQuery` instance containing the original
            text and the list of expanded terms.
        """
        # 1. Tokenizar: "El coche veloz" -> ["el", "coche", "veloz"]
        tokens = self.tokenizer.process(raw_query)

        # 2. Filtrar: ["el", "coche", "veloz"] -> ["coche", "veloz"]
        clean_tokens = self.sw_filter.process(tokens)

        # 3. Etiquetar: ["coche", "veloz"] -> [("coche", "NN"), ("veloz", "ADJ")]
        tagged_tokens = self.tagger.process(clean_tokens)

        # 4. Expandir: -> ["coche", "auto", "carro", "veloz", "rápido"...]
        expanded_terms = self.expander.process(tagged_tokens)

        # 5. Empaquetar en el DTO
        return ExpandedQuery(
            original_text=raw_query,
            expanded_terms=expanded_terms,
        )