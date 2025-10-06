"""
Civic Photo Quality Control API - Development Server
=====================================================
Entry point for running the application in development mode.
For production deployment, use production.py with Gunicorn or similar WSGI server.

Author: Civic Quality Control Team
Version: 2.0
"""

from app import create_app
import os

# Create Flask application instance with environment-specific configuration
# Defaults to 'default' (development) if FLASK_ENV is not set
app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    # Run development server
    # WARNING: This is for development only - use Gunicorn for production
    app.run(
        debug=app.config.get('DEBUG', False),  # Enable debug mode for development
        host='0.0.0.0',  # Listen on all network interfaces
        port=int(os.environ.get('PORT', 5000))  # Default port 5000, configurable via environment
    )
