from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/")
def index():
    return "Music Discovery API"