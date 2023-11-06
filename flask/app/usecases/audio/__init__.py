# from app import app
import os
from flask import jsonify
import uuid
import librosa
from librosa.effects import preemphasis
import soundfile as sf
import numpy as np 
from .speech_to_text import speech_to_text
from .speech import to_text

import librosa
from scipy import signal

from pydub import AudioSegment
from pydub.playback import play

AUDIO_RAW_DIRECTORY="./.data/audio/raw"
AUDIO_CLEANED_DIRECTORY="./.data/audio/cleaned"
AUDIO_BACKGROUND_DIRECTORY="./.data/audio/background"

class AudioUseCase():

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
        print(file, 'done')
        
        original_filename = file.filename
        filename, file_extension = os.path.splitext(original_filename)
        file_extension = file_extension.lstrip('.')  

        if file_extension.lower() not in allowed_extensions:
            return "Invalid file format", 400

        unique_filename = str(uuid.uuid4()) + '.' + file_extension
        file.save(os.path.join(AUDIO_RAW_DIRECTORY, unique_filename))
        return unique_filename, 200
    
    def __equalization(self, audio_data, fs):
        # Apply equalization by boosting mid-frequency range (500 Hz - 2 kHz)
        low = 100
        high = 2000
        b, a = signal.butter(6, [low / (fs / 2), high / (fs / 2)], 'band')
        equalized_audio = signal.filtfilt(b, a, audio_data)

        return equalized_audio
    
    def __dynamic_range_compression(self, audio_data):
        # Apply dynamic range compression (adjust parameters as needed)
        compressed_audio = audio_data  # You can modify this part based on your compression settings

        return compressed_audio
    
    def __voice_separator(self, filename, raw_path, output_foreground, output_background):
        print(filename)
        y, sr = librosa.load(os.path.join(raw_path, filename))

        S_full, phase = librosa.magphase(librosa.stft(y))
        idx = slice(*librosa.time_to_frames([90, 110], sr=sr))
        S_filter = librosa.decompose.nn_filter(S_full, aggregate=np.median, metric='cosine', width=int(librosa.time_to_frames(2, sr=sr)))
        S_filter = np.minimum(S_full, S_filter)
        margin_i, margin_v = 3, 1
        power = 3

        mask_i = librosa.util.softmask(S_filter, margin_i * (S_full - S_filter), power=power)
        mask_v = librosa.util.softmask(S_full - S_filter, margin_v * S_filter, power=power)

        S_foreground = mask_v * S_full
        S_background = mask_i * S_full

        y_foreground = librosa.istft(S_foreground * phase)
        y_background = librosa.istft(S_background * phase)

        output_foreground = os.path.join(output_foreground, filename)
        output_background = os.path.join(output_background, filename)
        sf.write(output_foreground, y_foreground, sr)
        sf.write(output_background, y_background, sr)

        return output_foreground

    def clean_audio(self, filename, voice_boost=20, instrument_attenuation=300):
        # Load the audio file
        audio = AudioSegment.from_file(filename)

        # Split the audio into separate tracks (voice and instruments)
        voice = audio
        instruments = audio

        # Boost the voice and attenuate the instruments
        voice = voice + voice_boost  # Increase this value to boost the voice
        # instruments = instruments - instrument_attenuation  # Increase this value to attenuate the instruments

        # Combine the voice and attenuated instruments
        result = voice.overlay(instruments)

        # Export the result to an output file
        # output = os.path.join(output_path, filename)
        result.export(filename, format="wav")

        return filename


    def process_audio(self, file):
        # save audio into directory
        print("sebelum")
        result, status_code = self.__save_to_dir(file)
        print("saved")

        if not status_code == 200:
            return jsonify({"error": result}), status_code
        
        filename = self.__voice_separator(result, AUDIO_RAW_DIRECTORY, AUDIO_CLEANED_DIRECTORY, AUDIO_BACKGROUND_DIRECTORY)
        filename = self.clean_audio(filename)
        # response = speech_to_text(filename)
        to_text(filename)
        return jsonify({"filename": result, "response": "response"}), status_code
    