from __future__ import annotations

import time

try:
    import numpy as np
    import pvporcupine
    import sounddevice as sd

    WAKE_AVAILABLE = True
except Exception:
    np = None
    pvporcupine = None
    sd = None
    WAKE_AVAILABLE = False
import pvporcupine
import sounddevice as sd
import numpy as np


class WakeWordDetector:
    def __init__(self, keyword="computer"):
        self.keyword = keyword
        self.porcupine = None
        self.sample_rate = 16000
        if WAKE_AVAILABLE and pvporcupine is not None:
            try:
                self.porcupine = pvporcupine.create(keywords=[keyword])
                self.sample_rate = self.porcupine.sample_rate
            except Exception:
                self.porcupine = None

    def listen(self):
        if self.porcupine is None or sd is None or np is None:
            time.sleep(0.2)
            return True  # fallback: don't block system when wake engine unavailable

        def callback(indata, frames, time_info, status):
            _ = (frames, time_info, status)
            pcm = np.frombuffer(indata, dtype=np.int16)
            result = self.porcupine.process(pcm)
            if result >= 0:
                self.triggered = True

        self.triggered = False
        self.porcupine = pvporcupine.create(keywords=[keyword])
        self.sample_rate = self.porcupine.sample_rate

    def listen(self):
        print("👂 Listening for wake word...")

        def callback(indata, frames, time, status):
            _ = (frames, time, status)
            pcm = np.frombuffer(indata, dtype=np.int16)
            result = self.porcupine.process(pcm)

            if result >= 0:
                print("🔥 Wake word detected!")
                self.triggered = True

        self.triggered = False

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            callback=callback,
        ):
            while not self.triggered:
                time.sleep(0.01)
                pass

        return True
