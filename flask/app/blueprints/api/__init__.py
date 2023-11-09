from flask import Blueprint
from .music import bp as music_bp

bp = Blueprint("api", __name__, url_prefix="/api")

bp.register_blueprint(music_bp)

@bp.route("/")
def index():
    return "Music Discovery API"