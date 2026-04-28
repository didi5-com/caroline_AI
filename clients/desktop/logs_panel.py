from PyQt6.QtWidgets import QTextEdit


class LogsPanel(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setPlaceholderText("Brain + tool logs...")

    def log(self, message: str) -> None:
        self.append(message)
