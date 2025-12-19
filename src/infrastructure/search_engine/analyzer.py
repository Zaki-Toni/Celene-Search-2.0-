"""Custom Whoosh analyzer integrating NLTK lemmatization.

Provides a lightweight lemmatizer filter that can be composed with
Whoosh tokenizers and filters to produce normalized tokens for
indexing and searching.
"""

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from whoosh.analysis import Filter, RegexTokenizer, LowercaseFilter, StopFilter, Token
from typing import Iterator, Any, cast


class NLTKLemmatizerFilter(Filter):
    """Whoosh-compatible filter that applies NLTK lemmatization.

    The filter reads token text, lemmatizes using a conservative noun
    POS tag and mutates the token text in place.
    """

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def __call__(self, tokens: Iterator[Token]) -> Iterator[Token]:
        """Yield tokens after applying lemmatization.

        Args:
            tokens: An iterator of Whoosh `Token` objects.

        Yields:
            Tokens with `.text` possibly replaced by their lemma form.
        """
        for token in tokens:
            # Casteamos el token a 'Any' para que Pylance nos deje acceder a .text
            t = cast(Any, token)

            lemma = self.lemmatizer.lemmatize(t.text, pos=wordnet.NOUN)

            if lemma != t.text:
                t.text = lemma

            yield t


def NLTKAnalyzer(stopwords_lang: str = 'english'):
    """Build a Whoosh analyzer pipeline that includes lemmatization.

    Args:
        stopwords_lang: Language code for the stopwords filter.

    Returns:
        A Whoosh analyzer composed of a tokenizer, lowercase and stopword
        filters, and the custom NLTK lemmatizer.
    """
    return (
        RegexTokenizer()
        | LowercaseFilter()
        | StopFilter(lang=stopwords_lang)
        | NLTKLemmatizerFilter()
    )