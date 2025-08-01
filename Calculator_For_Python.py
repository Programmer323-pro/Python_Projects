import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout)
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advhnced Calculator- PyQt5")
        self.setFixedSize(350, 400)
        self._create_ui()

    def _create_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # نمایشگر
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")
        self.layout.addWidget(self.display)

        # دکمه‌ها
        buttons = {
            '7': (0, 0), '8': (0, 1), '9': (0, 2), '/': (0, 3),
            '4': (1, 0), '5': (1, 1), '6': (1, 2), '*': (1, 3),
            '1': (2, 0), '2': (2, 1), '3': (2, 2), '-': (2, 3),
            '0': (3, 0), '.': (3, 1), '^': (3, 2), '+': (3, 3),
            '(': (4, 0), ')': (4, 1), '√': (4, 2), '=': (4, 3),
            'C': (5, 0, 1, 4)
        }

        grid = QGridLayout()
        self.layout.addLayout(grid)

        for btn_text, pos in buttons.items():
            button = QPushButton(btn_text)
            button.setStyleSheet("font-size: 18px; padding: 15px;")
            if len(pos) == 2:
                grid.addWidget(button, pos[0], pos[1])
            else:
                grid.addWidget(button, *pos)
            button.clicked.connect(self._on_button_click)

    def _on_button_click(self):
        sender = self.sender().text()

        if sender == "=":
            self._calculate_result()
        elif sender == "C":
            self.display.clear()
        elif sender == "√":
            self.display.insert("**0.5")
        elif sender == "^":
            self.display.insert("**")
        else:
            self.display.insert(sender)

    def _calculate_result(self):
        try:
            expression = self.display.text()
            result = eval(expression)
            self.display.setText(str(result))
        except Exception:
            self.display.setText("Error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
