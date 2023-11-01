# from google.cloud import speech
# import io
# from flask import jsonify

# def speech_to_text(filename):
#     print(filename)
#     print('berhasil masuk')
#     client = speech.SpeechClient.from_service_account_file("./gcp/key.json")

#     with open(filename, "rb") as f:
#         data = f.read()

#     audio_file = speech.RecognitionAudio(content=data)

#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=44100,
#         language_code='en-US'
#     )

#     response = client.recognize(
#         config=config,
#         audio=audio_file
#     )

#     print('berhasil selesai')
#     print(response)
#     for result in response.results:
#         print(f"Transcript: {result.alternatives[0].transcript}")
#     return "success"