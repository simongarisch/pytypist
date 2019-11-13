from collections import namedtuple
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
from .ui_settings import config
from .signals import signals
from .. import db


LessonStats = namedtuple("LessonStats", "lesson_name date_time seconds_elapsed wpm accuracy")


class StatsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def fetch_stats(self, lesson_name):
        return LessonStats(
            lesson_name,
            datetime.now(),
            self.timer_lcd.intValue(),
            self.wpm_lcd.intValue(),
            self.accuracy_lcd.intValue(),
        )

    def setup_ui(self):
        font_name = config.get("stats_widget", "font_name")
        font_size = config.getint("stats_widget", "font_size")
        font = QtGui.QFont(font_name, font_size)
        self.setFont(font)

        countdown_lbl = QtWidgets.QLabel("  Countdown", self)
        countdown_lcd = self.countdown_lcd = QtWidgets.QLCDNumber(self)

        timer_lbl = QtWidgets.QLabel("  Timer", self)
        timer_lcd = self.timer_lcd = QtWidgets.QLCDNumber(self)

        wpm_lbl = QtWidgets.QLabel("  WPM", self)
        wpm_lcd = self.wpm_lcd = QtWidgets.QLCDNumber(self)

        accuracy_lbl = QtWidgets.QLabel("  Accuracy", self)
        accuracy_lcd = self.accuracy_lcd = QtWidgets.QLCDNumber(self)

        start_btn = self.start_btn = QtWidgets.QPushButton("Start")
        pause_btn = self.pause_btn = QtWidgets.QPushButton("Pause")

        start_btn.clicked.connect(self.start_clicked)
        pause_btn.clicked.connect(self.pause_clicked)

        countdown_lcd.display(3)

        hbox = QtWidgets.QHBoxLayout()
        [hbox.addWidget(w) for w in [countdown_lbl, countdown_lcd]]
        [hbox.addWidget(w) for w in [timer_lbl, timer_lcd]]
        [hbox.addWidget(w) for w in [wpm_lbl, wpm_lcd]]
        [hbox.addWidget(w) for w in [accuracy_lbl, accuracy_lcd]]
        hbox.addStretch()
        hbox.addWidget(start_btn)
        hbox.addWidget(pause_btn)
        self.setLayout(hbox)

        # connect signals
        signals.update_countdown.connect(self.update_countdown)
        signals.update_typing_time.connect(self.update_typing_time)
        signals.update_wpm.connect(self.update_wpm)
        signals.update_accuracy.connect(self.update_accuracy)
        signals.update_database_lessons_stats.connect(
            self.update_database_lessons_stats
        )

    @QtCore.pyqtSlot(int)
    def update_countdown(self, number):
        self.countdown_lcd.display(number)

    @QtCore.pyqtSlot(int)
    def update_typing_time(self, number):
        self.timer_lcd.display(number)

    @QtCore.pyqtSlot(int)
    def update_wpm(self, number):
        self.wpm_lcd.display(number)

    @QtCore.pyqtSlot(int)
    def update_accuracy(self, number):
        self.accuracy_lcd.display(number)

    @QtCore.pyqtSlot(str)
    def update_database_lessons_stats(self, lesson_name):
        stats = self.fetch_stats(lesson_name)
        db.populate_lessons_stats(stats)

    def start_clicked(self):
        signals.start_countdown.emit()

    def pause_clicked(self):
        signals.disable_typing.emit()
