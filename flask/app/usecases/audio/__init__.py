# from app import app
import os
from flask import jsonify
import uuid
import librosa
import soundfile as sf
import numpy as np
from .speech_to_text import speech_to_text

import librosa
from pydub import AudioSegment
import ffmpeg

from moviepy.editor import VideoFileClip

from .youtube_music import search_music

AUDIO_RAW_DIRECTORY = "./.data/audio/raw"
AUDIO_CLEANED_DIRECTORY = "./.data/audio/cleaned"
AUDIO_BACKGROUND_DIRECTORY = "./.data/audio/background"


class AudioUseCase:
    def __ensure_audio_dir(self):
        if not os.path.exists(AUDIO_RAW_DIRECTORY):
            os.makedirs(AUDIO_RAW_DIRECTORY)
        if not os.path.exists(AUDIO_CLEANED_DIRECTORY):
            os.makedirs(AUDIO_CLEANED_DIRECTORY)
        if not os.path.exists(AUDIO_BACKGROUND_DIRECTORY):
            os.makedirs(AUDIO_BACKGROUND_DIRECTORY)

    def __save_to_dir(self, file):
        print(file)
        self.__ensure_audio_dir()
        allowed_extensions = {"wav"}
        print(file, "done")

        original_filename = file.filename
        filename, file_extension = os.path.splitext(original_filename)
        file_extension = file_extension.lstrip(".")

        if file_extension.lower() in allowed_extensions:
            unique_filename = str(uuid.uuid4()) + "." + file_extension
            file.save(os.path.join(AUDIO_RAW_DIRECTORY, unique_filename))
            return unique_filename, 200
        elif file_extension.lower() == "webm":
            try:
                unique_filename = str(uuid.uuid4()) + ".webm"
                file_path = os.path.join(AUDIO_RAW_DIRECTORY, unique_filename)
                file.save(file_path)

                
                wav_filename = str(uuid.uuid4()) + ".wav"
                wav_output_path = os.path.join(AUDIO_RAW_DIRECTORY, wav_filename)
                sampling_rate = 256000
                ffmpeg.input(file_path).output(wav_output_path).run(
                    overwrite_output=True
                )

                return wav_filename, 200

            except Exception as e:
                print(f"Conversion failed: {str(e)}")
                return (f"Conversion failed: {str(e)}"), 400

        else:
            return "Invalid file format", 400

    def __voice_separator(self, filename, output_foreground, output_background):
        print(filename)
        y, sr = librosa.load(filename)

        S_full, phase = librosa.magphase(librosa.stft(y))
        idx = slice(*librosa.time_to_frames([90, 110], sr=sr))
        S_filter = librosa.decompose.nn_filter(
            S_full,
            aggregate=np.median,
            metric="cosine",
            width=int(librosa.time_to_frames(2, sr=sr)),
        )
        S_filter = np.minimum(S_full, S_filter)
        margin_i, margin_v = 3, 4
        power = 3

        mask_i = librosa.util.softmask(
            S_filter, margin_i * (S_full - S_filter), power=power
        )
        mask_v = librosa.util.softmask(
            S_full - S_filter, margin_v * S_filter, power=power
        )

        S_foreground = mask_v * S_full
        S_background = mask_i * S_full

        y_foreground = librosa.istft(S_foreground * phase)
        y_background = librosa.istft(S_background * phase)

        sf.write(output_foreground, y_foreground, sr)
        sf.write(output_background, y_background, sr)

        return output_foreground

    def __enhance_audio(self, filename, voice_boost=10):
        audio = AudioSegment.from_file(filename)

        voice = audio + voice_boost

        voice.export(filename, format="wav")

        return filename

    def process_audio(self, file):
        result, status_code = self.__save_to_dir(file)

        print("berhasil====")

        if not status_code == 200:
            return jsonify({"error": result}), status_code
        
        filename = self.__voice_separator(
            os.path.join(AUDIO_RAW_DIRECTORY, result),
            os.path.join(AUDIO_CLEANED_DIRECTORY, result),
            os.path.join(AUDIO_BACKGROUND_DIRECTORY, result),
        )
        filename = self.__enhance_audio(filename)
        text, confidence = speech_to_text(filename)
        if confidence is None:
            return jsonify({"error": text}), 404

        search_result = search_music(text)[0]
        return (
            jsonify(
                {"filename": result, "lyrics": text, "search_result": search_result}
            ),
            status_code,
        )
