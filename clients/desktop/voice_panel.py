from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QVBoxLayout


class VoicePanel(QWidget):
    def __init__(self, on_talk_clicked):
        super().__init__()
        layout = QVBoxLayout()

        self.status = QLabel("Status: Idle")
        self.voice_btn = QPushButton("🎙️ Talk to Caroline")
        self.voice_btn.clicked.connect(on_talk_clicked)

        layout.addWidget(self.status)
        layout.addWidget(self.voice_btn)
        self.setLayout(layout)

    def set_status(self, text: str) -> None:
        self.status.setText(f"Status: {text}")
