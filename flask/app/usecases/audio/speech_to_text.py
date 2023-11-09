import speech_recognition as sr

def speech_to_text(filename):
    recognizer = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    
    try:
    # Use the Google Web Speech API recognizer
        text = recognizer.recognize_google(audio, with_confidence=True)
        # print("Google Web Speech API recognized: " + text)
        print(text)
        return text
    except sr.UnknownValueError:
        return "Google Web Speech API could not understand the audio"
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return (f"Could not request results from Google Web Speech API; {e}")