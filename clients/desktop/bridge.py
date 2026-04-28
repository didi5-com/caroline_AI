from core.voice_engine import VoiceEngine


class BrainBridge:
    def __init__(self):
        self.voice_engine = VoiceEngine()
        self.voice_engine.buffer.start_stream()

    def listen(self):
        # For UI mode: direct STT (no wake-word loop).
        audio = self.voice_engine.buffer.get_audio_chunk()

        if audio is None:
            return "No input detected"

        text = self.voice_engine.stt.transcribe(audio)
        return text

    def send_to_brain(self, message):
        response = self.voice_engine.brain.process(user_id="desktop_user", message=message)
        return response
