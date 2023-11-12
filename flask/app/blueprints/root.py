from flask import Blueprint
from .api import bp as api_bp

bp = Blueprint("root", __name__)

bp.register_blueprint(api_bp)

@bp.route("/")
def index():
    return "Music Discovery"