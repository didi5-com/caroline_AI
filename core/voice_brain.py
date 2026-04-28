from core.brain import Brain
from perception.speech_to_text import SpeechToText
from perception.text_to_speech import TextToSpeech


class VoiceBrain:
    def __init__(self):
        self.brain = Brain()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()

    def run(self):
        print("🚀 Caroline Voice AI Started")

        while True:
            # 1. Listen
            user_input = self.stt.listen()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "stop", "quit"]:
                self.tts.speak("Goodbye.")
                break

            # 2. Process brain
            response = self.brain.process(user_id="voice_user", message=user_input)

            # 3. Speak response
            self.tts.speak(response)
