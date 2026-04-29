from __future__ import annotations

import time

from core.audio_buffer import AudioBuffer
from core.brain import Brain
from perception.stt_stream import StreamingWhisper
from perception.text_to_speech import TextToSpeech
from perception.wake_word import WakeWordDetector


class VoiceEngine:
    def __init__(self):
        self.brain = Brain()
        self.tts = TextToSpeech()
        self.stt = StreamingWhisper()
        self.wake = WakeWordDetector()

        self.buffer = AudioBuffer()

    def run(self):
        print("🧠 Caroline Advanced Voice Engine Started")

        try:
            self.buffer.start_stream()
        except Exception as exc:  # noqa: BLE001
            print(f"[voice] audio stream unavailable: {exc}")

        while True:
            try:
                self.wake.listen()
                self.tts.speak("Yes?")

                start_time = time.time()
                collected_audio = []
                while time.time() - start_time < 6:
                    chunk = self.buffer.get_audio_chunk()
                    if chunk is not None:
                        collected_audio.append(chunk)

                if not collected_audio:
                    continue

                text = self.stt.transcribe(collected_audio[-1])
                if not text:
                    continue

                if "stop" in text.lower():
                    self.tts.speak("Going idle.")
                    continue

                response = self.brain.process(user_id="voice_user", message=text)
                self.tts.speak(response)
            except Exception as exc:  # noqa: BLE001
                print(f"[voice] loop error: {exc}")
                time.sleep(0.3)
        self.buffer.start_stream()

        while True:
            # 🔥 1. Wake word detection
            self.wake.listen()

            self.tts.speak("Yes?")

            # 🔁 2. Active listening window
            start_time = time.time()
            collected_audio = []

            while time.time() - start_time < 6:  # 6-second command window
                chunk = self.buffer.get_audio_chunk()

                if chunk is not None:
                    collected_audio.append(chunk)

            if not collected_audio:
                continue

            audio = collected_audio[-1]

            # ⚡ 3. Speech to text
            text = self.stt.transcribe(audio)

            print(f"🧠 Heard: {text}")

            if not text:
                continue

            if "stop" in text.lower():
                self.tts.speak("Going idle.")
                continue

            # 🧠 4. Brain processing
            response = self.brain.process(user_id="voice_user", message=text)

            # 🗣️ 5. Speak response
            self.tts.speak(response)
