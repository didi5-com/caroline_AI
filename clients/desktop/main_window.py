import sys

from clients.desktop.bridge import BrainBridge

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

    from clients.desktop.chat_panel import ChatPanel
    from clients.desktop.logs_panel import LogsPanel
    from clients.desktop.voice_panel import VoicePanel

    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False


if PYQT_AVAILABLE:

    class CarolineUI(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Caroline AI - Neural Interface")
            self.setGeometry(200, 200, 900, 600)

            self.bridge = BrainBridge()

            self.init_ui()
            self.apply_jarvis_theme()

        def init_ui(self):
            central = QWidget()
            layout = QVBoxLayout()

            self.voice_panel = VoicePanel(self.handle_voice)
            self.chat_display = ChatPanel()
            self.logs_panel = LogsPanel()

            layout.addWidget(self.voice_panel)
            layout.addWidget(self.chat_display)
            layout.addWidget(self.logs_panel)

            central.setLayout(layout)
            self.setCentralWidget(central)

        def apply_jarvis_theme(self) -> None:
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #0b0f1a;
                    color: #00ffcc;
                }
                QTextEdit {
                    background-color: #0f172a;
                    color: #00ffcc;
                    border: 1px solid #1e293b;
                    font-family: Consolas;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #1e293b;
                    color: #00ffcc;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover { background-color: #334155; }
                QLabel { color: #38bdf8; }
                """
            )

        def handle_voice(self):
            self.voice_panel.set_status("Listening...")
            self.logs_panel.log("[voice] Capturing audio chunk")

            user_text = self.bridge.listen()
            self.chat_display.add_user_message(user_text)

            self.logs_panel.log("[brain] Processing desktop message")
            response = self.bridge.send_to_brain(user_text)
            self.chat_display.add_ai_message(response)

            self.voice_panel.set_status("Idle")


else:
    import tkinter as tk
    from tkinter.scrolledtext import ScrolledText

    class CarolineUI:
        """Tk fallback UI when PyQt6 is unavailable."""

        def __init__(self):
            self.bridge = BrainBridge()
            self.root = tk.Tk()
            self.root.title("Caroline AI - Neural Interface (Tk Fallback)")
            self.root.geometry("900x600")
            self.root.configure(bg="#0b0f1a")

            self.status = tk.Label(self.root, text="Status: Idle", fg="#38bdf8", bg="#0b0f1a")
            self.status.pack(fill="x", padx=10, pady=10)

            self.chat = ScrolledText(self.root, bg="#0f172a", fg="#00ffcc")
            self.chat.pack(fill="both", expand=True, padx=10, pady=10)

            self.button = tk.Button(self.root, text="🎙️ Talk to Caroline", command=self.handle_voice)
            self.button.pack(padx=10, pady=10)

        def handle_voice(self):
            self.status.config(text="Status: Listening...")
            user_text = self.bridge.listen()
            self.chat.insert("end", f"You: {user_text}\n")
            response = self.bridge.send_to_brain(user_text)
            self.chat.insert("end", f"Caroline: {response}\n")
            self.status.config(text="Status: Idle")

        def show(self):
            self.root.mainloop()


if __name__ == "__main__":
    if PYQT_AVAILABLE:
        app = QApplication(sys.argv)
        window = CarolineUI()
        window.show()
        sys.exit(app.exec())
    else:
        ui = CarolineUI()
        ui.show()
