from PyQt5 import QtCore


class Signals(QtCore.QObject):

    lesson_selected = QtCore.pyqtSignal(str)
    section_selected = QtCore.pyqtSignal(str)
    status_update = QtCore.pyqtSignal(str)

    start_countdown = QtCore.pyqtSignal()
    update_countdown = QtCore.pyqtSignal(int)
    enable_typing = QtCore.pyqtSignal()
    disable_typing = QtCore.pyqtSignal()


signals = Signals()
