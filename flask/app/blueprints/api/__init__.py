from flask import Blueprint
from .audio import bp as audio_bp

bp = Blueprint("api", __name__, url_prefix="/api")

bp.register_blueprint(audio_bp)

@bp.route("/")
def index():
    return "Music Discovery API"