from flask import Flask, render_template
import os


def create_app(config_name: str = 'default') -> Flask:
    """Application factory that wires configuration, blueprints, and assets."""
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )

    # Load configuration class by name with graceful fallback to default.
    from config import config as config_map
    config_class = config_map.get(config_name, config_map['default'])
    app.config.from_object(config_class)

    # Enable CORS when the optional dependency is available.
    try:
        from flask_cors import CORS  # type: ignore
        CORS(app)
    except ImportError:
        print("Warning: Flask-CORS not installed, CORS disabled")

    # Ensure required storage directories exist so uploads succeed at runtime.
    directories = [
        app.config['UPLOAD_FOLDER'],
        app.config.get('PROCESSED_FOLDER', 'storage/processed'),
        app.config.get('REJECTED_FOLDER', 'storage/rejected')
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            open(gitkeep_path, 'a').close()

    # Register API blueprint.
    from app.routes.upload import upload_bp
    app.register_blueprint(upload_bp, url_prefix='/api')

    @app.route('/')
    def index():
        """Serve the main quality control interface."""
        return render_template('index.html')

    return app
