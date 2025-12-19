"""NLP components: tokenizer, stopword filter, POS tagger and expander.

The module provides small components that implement the
`INLPComponent` interface and are composed by the `NLPPipeline`.

Note: Components rely on NLTK data (tokenizers, stopwords and WordNet).
Make sure the required corpora are installed in the environment.
"""

import nltk
from nltk.corpus import wordnet, stopwords
from typing import Any, List, Tuple, cast
from src.core.interfaces import INLPComponent

### Añadir un mecanismo de verificación en tiempo de ejecución


# Tokenizador
class TokenizerComponent(INLPComponent):
    """Split text into tokens using NLTK's tokenizer.

    The component lower-cases the input before tokenization.
    """

    def process(self, text: str) -> list[str]:
        """Tokenize and normalize the input string.

        Args:
            text: The raw input string to tokenize.

        Returns:
            A list of lowercase token strings.
        """
        return nltk.word_tokenize(text.lower())


# Filtro de Stopwords
class StopwordFilter(INLPComponent):
    """Remove language-specific stopwords from a token list."""

    def __init__(self, language: str = 'english'):
        self.stop_words = set(stopwords.words(language))

    def process(self, tokens: list[str]) -> list[str]:
        """Filter out tokens that are stopwords or non-alphanumeric.

        Returns a reduced list of tokens suitable for further processing.
        """
        return [w for w in tokens if w not in self.stop_words and w.isalnum()]


# Etiquetador Gramatical
class POSTagger(INLPComponent):
    """Part-of-speech tagger using NLTK's `pos_tag`.

    The component receives a list of tokens and returns a list of
    `(token, tag)` tuples.
    """

    def process(self, tokens: list[str]) -> list[Tuple[str, str]]:
        """Tag the provided tokens with POS labels.

        Args:
            tokens: List of token strings.

        Returns:
            A list of `(token, pos_tag)` tuples as produced by NLTK.
        """
        return nltk.pos_tag(tokens)


# Expansor de WordNet
class WordNetExpander(INLPComponent):
    """Expand tokens using WordNet synonyms.

    The expander attempts to respect POS tags when looking up synsets
    and falls back to a more general lookup if needed.
    """

    def _get_wordnet_pos(self, treebank_tag: str) -> str | None:
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    def process(self, tagged_tokens: list[Tuple[str, str]]) -> list[str]:
        """Return a list of expanded terms given POS-tagged tokens.

        For each token the method includes the original word and any
        synonyms found in WordNet, normalising lemma names by replacing
        underscores with spaces.
        """
        expanded_terms: set[str] = set()

        for word, tag in tagged_tokens:
            expanded_terms.add(word)

            wn_tag = self._get_wordnet_pos(tag)

            # Intento Principal: Buscar respetando la categoría gramatical detectada
            synsets = wordnet.synsets(word, pos=wn_tag)

            # Plan B:
            # Si la búsqueda estricta no trajo nada (quizás el POS tagger se equivocó),
            # buscamos la palabra en CUALQUIER categoría (verbo, sustantivo, adj...)
            if not synsets and wn_tag is None:
                synsets = wordnet.synsets(word)

            for syn in synsets:
                # Casteamos a Any para evitar error de Pylance
                syn_obj = cast(Any, syn)
                for lemma in syn_obj.lemmas():
                    clean_lemma = lemma.name().replace('_', ' ')
                    expanded_terms.add(clean_lemma)

        return list(expanded_terms)