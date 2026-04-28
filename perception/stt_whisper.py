import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel


class WhisperSTT:
    def __init__(self):
        self.model = WhisperModel("base", compute_type="int8")

    def record_audio(self, duration=5, samplerate=16000):
        print("🎙️ Recording...")
        audio = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype=np.float32,
        )
        sd.wait()
        return np.squeeze(audio)

    def transcribe(self, audio):
        segments, _ = self.model.transcribe(audio)
        text = " ".join([seg.text for seg in segments])
        print(f"🧠 Whisper heard: {text}")
        return text
