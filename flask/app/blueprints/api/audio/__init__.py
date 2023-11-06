from flask import Blueprint, request, jsonify
from app.usecases.audio import AudioUseCase

bp = Blueprint("audio", __name__, url_prefix="/audio")

audio_uc = AudioUseCase()

@bp.route("/", methods=["POST"])
def process_audio():
    print(request.files, 'masuk')
    if "audio" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["audio"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    return audio_uc.process_audio(file)