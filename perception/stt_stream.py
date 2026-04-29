from __future__ import annotations

import numpy as np

try:
    import sounddevice as sd
    from faster_whisper import WhisperModel

    STT_AVAILABLE = True
except Exception:
    sd = None
    WhisperModel = None
    STT_AVAILABLE = False


class StreamingWhisper:
    def __init__(self):
        self.sample_rate = 16000
        self.model = None
        if STT_AVAILABLE and WhisperModel is not None:
            try:
                self.model = WhisperModel("base", compute_type="int8")
            except Exception:
                self.model = None

    def record_chunk(self, duration=3):
        if sd is None:
            return np.array([], dtype=np.float32)

        try:
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.float32,
            )
            sd.wait()
            return np.squeeze(audio)
        except Exception:
            return np.array([], dtype=np.float32)

    def transcribe(self, audio):
        if self.model is None or audio is None or len(audio) == 0:
            return ""

        try:
            segments, _ = self.model.transcribe(audio)
            return " ".join([s.text for s in segments]).strip()
        except Exception:
            return ""
