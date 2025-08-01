import sys
import math
import time
from PyQt5.QtCore import Qt, QTimer, QTime, QPoint, QDateTime
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QLabel, QPushButton, QTimeEdit, QHBoxLayout
)
import pytz
from datetime import datetime


# -------- ساعت آنالوگ --------
class AnalogClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 300)
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        current_time = QTime.currentTime()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # پس‌زمینه
        painter.setBrush(QBrush(QColor(230, 230, 250)))
        painter.drawEllipse(-100, -100, 200, 200)

        # ساعت
        painter.setPen(QPen(Qt.black, 6))
        painter.save()
        painter.rotate(30.0 * ((current_time.hour() + current_time.minute() / 60.0)))
        painter.drawLine(0, 0, 0, -50)
        painter.restore()

        # دقیقه
        painter.setPen(QPen(Qt.blue, 4))
        painter.save()
        painter.rotate(6.0 * (current_time.minute() + current_time.second() / 60.0))
        painter.drawLine(0, 0, 0, -70)
        painter.restore()

        # ثانیه
        painter.setPen(QPen(Qt.red, 2))
        painter.save()
        painter.rotate(6.0 * current_time.second())
        painter.drawLine(0, 0, 0, -90)
        painter.restore()


# -------- کرنومتر --------
class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.start_time = None
        self.running = False
        self.elapsed = 0

        layout = QVBoxLayout()
        self.label = QLabel("00:00:00")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px")
        layout.addWidget(self.label)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle)
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.reset_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)

    def toggle(self):
        if self.running:
            self.running = False
            self.timer.stop()
            self.start_btn.setText("Start")
            self.elapsed += time.time() - self.start_time
        else:
            self.running = True
            self.start_time = time.time()
            self.timer.start(100)
            self.start_btn.setText("Pause")

    def reset(self):
        self.running = False
        self.timer.stop()
        self.elapsed = 0
        self.label.setText("00:00:00")
        self.start_btn.setText("Start")

    def update_display(self):
        total = self.elapsed
        if self.running:
            total += time.time() - self.start_time
        h = int(total // 3600)
        m = int((total % 3600) // 60)
        s = int(total % 60)
        self.label.setText(f"{h:02d}:{m:02d}:{s:02d}")


# -------- تایمر --------
class TimerTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        layout.addWidget(self.time_edit)

        self.label = QLabel("00:00:00")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px")
        layout.addWidget(self.label)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_timer)
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_timer)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.reset_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_seconds = 0

    def start_timer(self):
        selected_time = self.time_edit.time()
        self.remaining_seconds = selected_time.hour() * 3600 + selected_time.minute() * 60 + selected_time.second()
        if self.remaining_seconds > 0:
            self.timer.start(1000)
            self.update_timer()

    def reset_timer(self):
        self.timer.stop()
        self.remaining_seconds = 0
        self.label.setText("00:00:00")

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            h = self.remaining_seconds // 3600
            m = (self.remaining_seconds % 3600) // 60
            s = self.remaining_seconds % 60
            self.label.setText(f"{h:02d}:{m:02d}:{s:02d}")
        else:
            self.timer.stop()
            self.label.setText("Time's up!")


# -------- ساعت جهانی --------
class WorldClock(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px")
        self.layout.addWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.setLayout(self.layout)

    def update_time(self):
        timezones = ["Asia/Tehran", "Europe/London", "America/New_York", "Asia/Tokyo"]
        text = ""
        for tz_name in timezones:
            tz = pytz.timezone(tz_name)
            dt = datetime.now(tz)
            text += f"{tz_name}: {dt.strftime('%H:%M:%S')}<br>"
        self.label.setText(text)


# -------- اپلیکیشن اصلی --------
class ClockApp(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ساعت چندکاره با PyQt5")
        self.resize(400, 400)

        self.addTab(AnalogClock(), "ساعت آنالوگ")
        self.addTab(TimerTab(), "تایمر")
        self.addTab(Stopwatch(), "کرنومتر")
        self.addTab(WorldClock(), "ساعت جهانی")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClockApp()
    window.show()
    sys.exit(app.exec_())
