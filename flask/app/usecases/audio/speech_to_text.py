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
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio) #asynchronous
    response = operation.result(timeout=10000)

    print('berhasil selesai')
    print(response)
    for result in response.results:
        transcript += result.alternatives[0].transcript
    
    return transcript