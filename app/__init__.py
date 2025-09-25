from flask import Flask
import os

def create_app(config_name='default'):
    # Set template and static folders relative to project root
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')

    # Load configuration
    from config import config
    app.config.from_object(config[config_name])

    # Enable CORS if available
    try:
        from flask_cors import CORS
        CORS(app)
    except ImportError:
        print("Warning: Flask-CORS not installed, CORS disabled")

    # Create necessary directories
    directories = [
        app.config['UPLOAD_FOLDER'],
        'storage/processed',
        'storage/rejected',
        'models'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Create .gitkeep files
        gitkeep_path = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            open(gitkeep_path, 'a').close()

    # Register blueprints
    from app.routes.upload import upload_bp
    app.register_blueprint(upload_bp, url_prefix='/api')

    return app
