import nltk
from nltk.corpus import wordnet, stopwords
from typing import Any, List, Tuple, cast
from src.core.interfaces import INLPComponent

### Añadir un mecanismo de verificación en tiempo de ejecución

# Tokenizador 
class TokenizerComponent(INLPComponent):
    """Divide el texto en palabras individuales."""
    
    def process(self, text: str) -> list[str]:
        return nltk.word_tokenize(text.lower())

# Filtro de Stopwords
class StopwordFilter(INLPComponent):
    """Elimina palabras vacías."""
    
    def __init__(self, language: str = 'spanish'):
        self.stop_words = set(stopwords.words(language))

    def process(self, tokens: list[str]) -> list[str]:
        return [w for w in tokens if w not in self.stop_words and w.isalnum()]

# Etiquetador Gramatical
class POSTagger(INLPComponent):
    """Identifica sustantivos, verbos, etc."""
    
    def process(self, tokens: list[str]) -> list[Tuple[str, str]]:
        return nltk.pos_tag(tokens)

# Expansor de WordNet
class WordNetExpander(INLPComponent):
    """Busca sinónimos en WordNet."""

    def _get_wordnet_pos(self, treebank_tag: str) -> str | None:
        if treebank_tag.startswith('J'): return wordnet.ADJ
        elif treebank_tag.startswith('V'): return wordnet.VERB
        elif treebank_tag.startswith('N'): return wordnet.NOUN
        elif treebank_tag.startswith('R'): return wordnet.ADV
        else: return None

    def process(self, tagged_tokens: list[Tuple[str, str]]) -> list[str]:
        expanded_terms: set[str] = set()
        
        for word, tag in tagged_tokens:
            expanded_terms.add(word)
            
            wn_tag = self._get_wordnet_pos(tag)
            
            # Intento Principal: Buscar respetando la categoría gramatical detectada
            synsets = wordnet.synsets(word, pos=wn_tag, lang='spa')
            
            # Plan B: 
            # Si la búsqueda estricta no trajo nada (quizás el POS tagger se equivocó),
            # buscamos la palabra en CUALQUIER categoría (verbo, sustantivo, adj...)
            if not synsets:
                synsets = wordnet.synsets(word, lang='spa')

            for syn in synsets:
                # Casteamos a Any para evitar error de Pylance
                syn_obj = cast(Any, syn)
                for lemma in syn_obj.lemmas('spa'):
                    clean_lemma = lemma.name().replace('_', ' ')
                    expanded_terms.add(clean_lemma)
        
        return list(expanded_terms)