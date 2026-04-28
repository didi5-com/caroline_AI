import pvporcupine
import sounddevice as sd
import numpy as np


class WakeWordDetector:
    def __init__(self, keyword="computer"):
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
                pass

        return True
