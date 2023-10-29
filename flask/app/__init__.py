from flask import Flask
from app.blueprints.root import bp as root_bp

app = Flask(__name__)
app.register_blueprint(root_bp)
