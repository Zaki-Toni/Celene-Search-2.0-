import os
import shutil
"""Whoosh adapter: manage index creation and access.

This component encapsulates the Whoosh index schema, directory
creation and simple lifecycle operations such as creating or resetting
the index directory.
"""

import os
import shutil
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import Index, create_in, exists_in, open_dir
from src.infrastructure.search_engine.analyzer import NLTKAnalyzer


class WhooshAdapter:
    """Adapter that manages the Whoosh index instance and schema.

    Args:
        index_dir: Filesystem path where the Whoosh index files are stored.
    """

    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        # Definimos el esquema de la base de datos:
        # - title: Texto indexable y almacenado.
        # - content: Texto indexable y almacenado. Analizador Estándar.
        # - path: ID único, almacenado pero no analizado.
        self.schema = Schema(
            title=TEXT(stored=True),
            content=TEXT(stored=True, analyzer=NLTKAnalyzer(stopwords_lang='english')),
            path=ID(stored=True, unique=True),
        )

    def get_index(self) -> Index:
        """Return a Whoosh Index object, creating it if necessary.

        The method ensures the directory exists and returns a ready-to-use
        Index instance.
        """
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)
            return create_in(self.index_dir, self.schema)

        if exists_in(self.index_dir):
            return open_dir(self.index_dir)
        else:
            return create_in(self.index_dir, self.schema)

    def reset_index(self):
        """Remove the index directory and create a fresh index.

        Useful for tests or re-indexing from scratch.
        """
        if os.path.exists(self.index_dir):
            shutil.rmtree(self.index_dir)
        os.makedirs(self.index_dir)
        create_in(self.index_dir, self.schema)
