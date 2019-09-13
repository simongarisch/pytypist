from PyQt5 import QtWidgets, QtCore, QtGui
from .signals import signals
from .ui_settings import config
from ..lessons import Lessons


class TypingWidget(QtWidgets.QTextEdit):
    def __init__(self, parent):
        super().__init__("", parent)
        self.lessons = Lessons()
        self.set_font()
        self.connect_signals()
        self.create_timers()
        self.set_disabled()
        self.refresh()

    def set_font(self):
        font_name = config.get("typing_widget", "font_name")
        font_size = config.getint("typing_widget", "font_size")
        font = QtGui.QFont(font_name, font_size, QtGui.QFont.Monospace)
        self.setFont(font)

    def connect_signals(self):
        signals.lesson_selected.connect(self.set_target_text)
        signals.start_countdown.connect(self.start_countdown)
        signals.disable_typing.connect(lambda: self.set_disabled(True))

    def create_timers(self):
        self.countdown_timer = QtCore.QTimer()
        self.typing_timer = QtCore.QTimer()

    def start_countdown(self):
        self.enable_typing_in = 3  # seconds
        signals.update_countdown.emit(self.enable_typing_in)
        self.countdown_timer.stop()
        self.countdown_timer.setInterval(1000)
        self.countdown_timer.timeout.connect(self.countdown)
        self.countdown_timer.start()

    def countdown(self):
        self.enable_typing_in -= 1
        signals.update_countdown.emit(self.enable_typing_in)
        if self.enable_typing_in <= 0:
            self.countdown_timer.stop()
            self.setDisabled(False)

    @QtCore.pyqtSlot(bool)
    def set_disabled(self, disabled=True):
        self.setDisabled(disabled)

    def refresh(self):
        self.countdown_timer.stop()
        self.typing_timer.stop()
        self.finished = False
        self.entered_text = ""
        self.target_text = None

    @QtCore.pyqtSlot(str)
    def set_target_text(self, lesson_name):
        self.refresh()
        self.target_text = self.lessons.get_lesson_content(lesson_name)
        self.update_display()

    def keyPressEvent(self, event):
        if self.finished or self.target_text is None:
            return
        if event.key() == QtCore.Qt.Key_Backspace:
            if len(self.entered_text) > 0:
                self.entered_text = self.entered_text[:-1]
        else:
            text = event.text()
            self.entered_text += text
        self.update_display()

    def update_display(self):
        entered_text = self.entered_text
        target_text = self.target_text

        len_entered = len(entered_text)
        len_target = len(target_text)
        if len_entered >= len_target:
            self.finished = True

        display_text = ""
        for char_entered, char_target in zip(entered_text, target_text):
            color = "green"
            if char_entered != char_target:
                color = "red"
                # replace red (incorrect) spaces with red asterix
                if char_target == " ":
                    char_target = "*"
            display_text += '<span style="color:{}">{}</span>'.format(
                color, char_target
            )
        display_text += target_text[len_entered:]
        self.setText(display_text)

        cursor = self.textCursor()
        cursor.setPosition(len_entered, QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)
