import os
from PyQt5 import QtWidgets, QtGui, QtCore
from .ui_settings import config


class StatsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

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

        start_btn = self.start_btn = QtWidgets.QPushButton("Start")
        pause_btn = self.pause_btn = QtWidgets.QPushButton("Pause")

        countdown_lcd.display(0)
        wpm_lcd.display(0)

        hbox = QtWidgets.QHBoxLayout()
        [hbox.addWidget(w) for w in [countdown_lbl, countdown_lcd]]
        [hbox.addWidget(w) for w in [timer_lbl, timer_lcd]]
        [hbox.addWidget(w) for w in [wpm_lbl, wpm_lcd]]
        hbox.addStretch()
        hbox.addWidget(start_btn)
        hbox.addWidget(pause_btn)
        self.setLayout(hbox)
