from PyQt5 import QtCore


class Signals(QtCore.QObject):
    lesson_selected = QtCore.pyqtSignal(str)
