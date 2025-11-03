"""
WSGI Entry Point for PhotoGuard API
====================================
Production entry point for running the application with WSGI servers like Gunicorn.
"""

import os
from app import create_app

# Create Flask application instance
# Use production config for Hugging Face Spaces deployment
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    # This is for debugging only
    app.run(host='0.0.0.0', port=7860)
