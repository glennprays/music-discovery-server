from flask import Flask
# from app.blueprints.root import bp as root_bp
from app.blueprints.root import bp as root_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(root_bp)
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

    return app
