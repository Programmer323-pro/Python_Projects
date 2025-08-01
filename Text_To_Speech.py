import sys
import pyttsx3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont


class TextToSpeechApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("(Text to Speech)")
        self.setGeometry(100, 100, 500, 300)

        self.engine = pyttsx3.init()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Enter Your Text")
        label.setFont(QFont("Arial", 12))
        layout.addWidget(label)

        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Tahoma", 12))
        layout.addWidget(self.text_edit)

        self.speak_button = QPushButton("🔊 Play Sound")
        self.speak_button.setFont(QFont("Arial", 12))
        self.speak_button.clicked.connect(self.text_to_speech)
        layout.addWidget(self.speak_button)

        self.setLayout(layout)

    def text_to_speech(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "هشدار", "لطفاً یک متن وارد کنید!")
            return

        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"مشکل در تبدیل به صدا:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec_())
