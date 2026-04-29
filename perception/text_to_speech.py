import pyttsx3


class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)

    def speak(self, text: str):
        print(f"🤖 Caroline: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
