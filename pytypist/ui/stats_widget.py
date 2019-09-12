import os
from PyQt5 import QtWidgets, QtGui, QtCore


class StatsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        countdown_lbl = QtWidgets.QLabel("Countdown", self)
        countdown_lcd = self.countdown_lcd = QtWidgets.QLCDNumber(self)
        wpm_lbl = QtWidgets.QLabel("WPM", self)
        wpm_lcd = self.wpm_lcd = QtWidgets.QLCDNumber(self)

        countdown_lcd.display(0)
        wpm_lcd.display(0)

        hbox = QtWidgets.QHBoxLayout()
        [hbox.addWidget(w) for w in [countdown_lbl, countdown_lcd]]
        hbox.addStretch()
        [hbox.addWidget(w) for w in [wpm_lbl, wpm_lcd]]
        self.setLayout(hbox)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = StatsWidget()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
