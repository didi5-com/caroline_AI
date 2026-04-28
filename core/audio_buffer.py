import queue
import sounddevice as sd
import numpy as np


class AudioBuffer:
    def __init__(self, samplerate=16000):
        self.samplerate = samplerate
        self.buffer = queue.Queue()

    def callback(self, indata, frames, time, status):
        _ = (frames, time, status)
        self.buffer.put(indata.copy())

    def start_stream(self):
        print("🎙️ Audio stream started...")

        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=1,
            dtype="float32",
            callback=self.callback,
        )
        self.stream.start()

    def get_audio_chunk(self):
        chunks = []

        while not self.buffer.empty():
            chunks.append(self.buffer.get())

        if not chunks:
            return None

        return np.concatenate(chunks, axis=0)
