"""Web routes (Flask Blueprint) for the simple search application.

This module defines the `main` blueprint and wires lightweight
dependency instances used by the views. It intentionally performs
module-level initialization for the demonstration web app; in larger
projects this wiring should be moved to a factory or an IoC container.

Provided routes
    /       -> Home page with search form
    /search -> Performs a query and renders results
"""

import os
from flask import Blueprint, render_template, request

from src.infrastructure.fs.loader import FileDocumentLoader
from src.infrastructure.search_engine.adapter import WhooshAdapter
from src.infrastructure.search_engine.reader import WhooshReader
from src.domain_nlp.pipeline import NLPPipeline
from src.services.search_service import SearchService

# Definimos el Blueprint (agrupación de rutas)
main_bp = Blueprint('main', __name__)

# --- CONFIGURACIÓN E INYECCIÓN DE DEPENDENCIAS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX_DIR = os.path.join(BASE_DIR, 'data', 'index_storage')

# Instanciamos las dependencias (demo wiring)
adapter = WhooshAdapter(INDEX_DIR)
reader = WhooshReader(adapter)
nlp = NLPPipeline()

# Inyectamos todo en el servicio
search_service = SearchService(reader, nlp)


@main_bp.route('/')
def home():
    """Render the search homepage.

    Returns:
        A rendered template for the index page (HTML string).
    """
    return render_template('index.html')


@main_bp.route('/search')
def search():
    """Handle a GET search request and render results.

    The view reads the `q` query parameter, delegates the search to
    `search_service` and passes the results to the `results.html`
    template.

    Returns:
        A rendered HTML template. If no query is provided, the index
        page is returned.
    """
    query = request.args.get('q', '')
    
    if not query:
        return render_template('index.html')
    
    results = search_service.execute_search(query)

    return render_template('results.html', query=query, results=results)