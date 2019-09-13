from PyQt5 import QtWidgets, QtCore, QtGui
from .signals import signals
from .ui_settings import config
from ..lessons import Lessons


class TypingWidget(QtWidgets.QTextEdit):
    def __init__(self, parent):
        super().__init__("", parent)
        self.lessons = Lessons()
        self.refresh()
        self.set_font()
        self.connect_signals()
        self.create_timers()
        self.set_read_only()

    def set_font(self):
        font_name = config.get("typing_widget", "font_name")
        font_size = config.getint("typing_widget", "font_size")
        font = QtGui.QFont(font_name, font_size, QtGui.QFont.Monospace)
        self.setFont(font)

    def connect_signals(self):
        signals.lesson_selected.connect(self.set_target_text)
        signals.enable_typing.connect(lambda: self.set_read_only(False))
        signals.disable_typing.connect(lambda: self.set_read_only(True))

    def create_timers(self):
        self.countdown_timer = QtCore.QTimer()
        self.typing_timer = QtCore.QTimer()

    @QtCore.pyqtSlot(bool)
    def set_read_only(self, read_only=True):
        self.setDisabled(read_only)

    def refresh(self):
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
