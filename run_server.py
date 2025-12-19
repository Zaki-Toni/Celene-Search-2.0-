"""Small script to run the demo Flask application.

This module uses the application factory from :mod:`src.web` to create
and run a development server. It is intended for local testing only.
"""

from src.web import create_app

app = create_app()


if __name__ == '__main__':
    """Start the Flask development server on port 5000."""
    print("🚀 Servidor iniciado en http://localhost:5000")
    app.run(debug=True, port=5000)