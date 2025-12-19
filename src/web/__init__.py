"""Flask application factory for the demo search web app.

This module implements a simple `create_app()` factory to produce a
Flask instance configured with the blueprint defined in
`src.web.routes`. Using a factory enables easier testing and avoids
module-level side-effects when importing the package.
"""

from flask import Flask


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        A configured `Flask` application instance with the main
        blueprint registered.
    """
    app = Flask(__name__)

    # Importamos y registramos las rutas (el controlador)
    from src.web.routes import main_bp
    app.register_blueprint(main_bp)

    return app