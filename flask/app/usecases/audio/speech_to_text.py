from google.cloud import speech
import io
import os
from flask import jsonify

def speech_to_text(filename):
    print(filename)
    print('berhasil masuk')

    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= './gcp/key.json'
    client = speech.SpeechClient()

    transcript = '*'

    with io.open(filename, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        sample_rate_hertz=22050,
    )

    response = client.recognize(request={"config": config, "audio": audio})

    print('berhasil selesai')
    print(response)
    for result in response.results:
        transcript += result.alternatives[0].transcript
    
    return transcript