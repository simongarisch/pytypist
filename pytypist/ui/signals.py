from PyQt5 import QtCore


class Signals(QtCore.QObject):

    lesson_selected = QtCore.pyqtSignal(str)
    section_selected = QtCore.pyqtSignal(str)
    status_update = QtCore.pyqtSignal(str)

    start_countdown = QtCore.pyqtSignal()
    update_countdown = QtCore.pyqtSignal(int)
    update_typing_time = QtCore.pyqtSignal(int)
    update_wpm = QtCore.pyqtSignal(int)
    update_accuracy = QtCore.pyqtSignal(int)

    enable_typing = QtCore.pyqtSignal()
    disable_typing = QtCore.pyqtSignal()

    update_database_lessons_stats = QtCore.pyqtSignal(str)


signals = Signals()

thread_pool = QtCore.QThreadPool()
