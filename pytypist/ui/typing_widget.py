from PyQt5 import QtWidgets, QtCore, QtGui
from .signals import signals
from .ui_settings import config
from ..lessons import Lessons


class TypingWidget(QtWidgets.QTextEdit):
    def __init__(self, parent):
        super().__init__("", parent)
        self.lessons = Lessons()
        signals.lesson_selected.connect(self.set_target_text)
        font = QtGui.QFont()
        font.setPointSize(config.getint("typing_widget", "font_size"))
        self.setFont(font)
        self.refresh()

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
            display_text += '<span style="color:{}">{}</span>'.format(
                color, char_target
            )
        display_text += target_text[len_entered:]
        self.setText(display_text)

        cursor = self.textCursor()
        cursor.setPosition(len_entered, QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)
