import speech_recognition as sr

def to_text(filename):
    recognizer = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    
    try:
    # Use the Google Web Speech API recognizer
        text = recognizer.recognize_google(audio)
        print("Google Web Speech API recognized: " + text)
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")