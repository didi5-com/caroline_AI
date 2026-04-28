import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel


class StreamingWhisper:
    def __init__(self):
        self.model = WhisperModel("base", compute_type="int8")
        self.sample_rate = 16000

    def record_chunk(self, duration=3):
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
        )
        sd.wait()
        return np.squeeze(audio)

    def transcribe(self, audio):
        segments, _ = self.model.transcribe(audio)
        return " ".join([s.text for s in segments])
