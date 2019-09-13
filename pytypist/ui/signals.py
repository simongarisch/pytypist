from PyQt5 import QtCore


class Signals(QtCore.QObject):
    lesson_selected = QtCore.pyqtSignal(str)
    section_selected = QtCore.pyqtSignal(str)
    status_update = QtCore.pyqtSignal(str)


signals = Signals()
