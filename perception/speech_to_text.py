import speech_recognition as sr


class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        with self.microphone as source:
            print("🎙️ Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"🧠 You said: {text}")
            return text

        except sr.UnknownValueError:
            return "I couldn't understand audio"

        except sr.RequestError:
            return "Speech service error"
