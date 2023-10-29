from app import app
import os
from flask import jsonify
import uuid

AUDIO_DIRECTORY="../../../.data/audio"
app.config["AUDIO_DIRECTORY"] = AUDIO_DIRECTORY

class AudioUseCase():

    def __ensure_audio_dir(self):
        audio_dir = app.config["AUDIO_DIRECTORY"]
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

    def __save_to_dir(self, file):
        self.__ensure_audio_dir()
        allowed_extensions = {"mp3", "wav", "ogg"}
        if not file.filename.rsplit(".", 1)[1].lower() in allowed_extensions:
            return "Invalid file format", 400
        
        unique_filename = str(uuid.uuid4())
        file.save(os.path.join(app.config['AUDIO_DIRECTORY'], unique_filename))
        return unique_filename, 200

    def process_audio(self, file):
        # save audio into directory
        result, status_code = self.__save_to_dir(file)

        if not status_code == 200:
            return jsonify({"error": result}), status_code
        
        return jsonify({"filename": result}), status_code
        


    