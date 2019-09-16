from PyQt5 import QtWidgets, QtCore, QtGui
from .signals import signals
from .ui_settings import config
from ..lessons import Lessons


class TypingWidget(QtWidgets.QTextEdit):
    def __init__(self, parent):
        super().__init__("", parent)
        self.finished = True
        self.chars_per_word = config.getint("typing_widget", "chars_per_word")
        self.lessons = Lessons()
        self.set_font()
        self.create_timers()
        self.connect_signals()
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
        self.countdown_timer.timeout.connect(self.countdown)
        signals.disable_typing.connect(lambda: self.set_disabled(True))
        stats_methods = [
            self.show_typing_time,
            self.show_wpm,
            self.show_accuracy
        ]
        for method in stats_methods:
            self.typing_timer.timeout.connect(method)

    def create_timers(self):
        self.countdown_timer = QtCore.QTimer()
        self.typing_timer = QtCore.QTimer()
        self.countdown_timer.setInterval(1000)
        self.typing_timer.setInterval(1000)

    def start_countdown(self):
        if self.enable_typing_in <=0:
            self.start_typing()
            return

        self.enable_typing_in = config.getint("typing_widget", "countdown")
        signals.update_countdown.emit(self.enable_typing_in)
        self.countdown_timer.start()

    def countdown(self):
        self.enable_typing_in -= 1
        signals.update_countdown.emit(self.enable_typing_in)
        if self.enable_typing_in <= 0:
            self.start_typing()

    def show_typing_time(self):
        self.typing_time += 1
        signals.update_typing_time.emit(self.typing_time)

    def show_wpm(self):
        words_typed = len(self.entered_text) / self.chars_per_word
        minutes_passed = (self.typing_time / 60)
        self.wpm = int(words_typed / minutes_passed)
        signals.update_wpm.emit(self.wpm)

    def show_accuracy(self):
        signals.update_accuracy.emit(self.accuracy)

    def start_typing(self):
        if not self.finished:
            self.countdown_timer.stop()
            self.set_disabled(False)
            signals.status_update.emit("Start typing...")
        else:
            self.set_disabled(True)
            signals.status_update.emit("Finished exercise...")

    @QtCore.pyqtSlot(bool)
    def set_disabled(self, disabled=True):
        self.setDisabled(disabled)
        if disabled:
            self.typing_timer.stop()
            if self.finished is False:
                signals.status_update.emit("Paused...")
        else:
            self.typing_timer.start()
            self.setFocus()

    def refresh(self):
        self.enable_typing_in = config.getint("typing_widget", "countdown")
        self.typing_time = 0
        self.wpm = 0
        self.accuracy = 0
        signals.update_countdown.emit(self.enable_typing_in)
        signals.update_typing_time.emit(self.typing_time)
        signals.update_wpm.emit(self.wpm)
        signals.update_accuracy.emit(self.accuracy)
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
            self.typing_timer.stop()
            self.set_disabled(True)
            signals.status_update.emit("Finished exercise...")

        display_text = ""
        greens, reds = 0, 0
        for char_entered, char_target in zip(entered_text, target_text):
            color = "green"
            greens += 1
            if char_entered != char_target:
                color = "red"
                reds += 1
                # replace red (incorrect) spaces with red asterix
                if char_target == " ":
                    char_target = "*"
            display_text += '<span style="color:{}">{}</span>'.format(
                color, char_target
            )
        if len_entered > 0:
            self.accuracy = int(greens / (greens + reds)  * 100)
        display_text += target_text[len_entered:]
        self.setText(display_text)

        cursor = self.textCursor()
        cursor.setPosition(len_entered, QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)
