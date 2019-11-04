from PyQt5 import QtWidgets, QtCore, QtGui
from enum import Enum
from .signals import signals
from .ui_settings import config
from ..lessons import Lesson


class TypingState(Enum):
    UNSTARTED = 1
    TYPING = 2
    FINISHED = 3


class TypingWidget(QtWidgets.QTextEdit):
    def __init__(self, parent):
        super().__init__("", parent)
        self.typing_state = TypingState.UNSTARTED
        self.chars_per_word = config.getint("typing_widget", "chars_per_word")
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
        if self.enable_typing_in <= 0:
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

    def start_typing(self):
        if self.typing_state != TypingState.FINISHED:
            self.countdown_timer.stop()
            self.set_disabled(False)
            signals.status_update.emit("Start typing...")
            self.typing_state = TypingState.TYPING
        else:
            self.set_disabled(True)
            signals.status_update.emit("Finished exercise...")

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

    @QtCore.pyqtSlot(bool)
    def set_disabled(self, disabled=True):
        self.setDisabled(disabled)
        if disabled:
            self.typing_timer.stop()
            if self.typing_state is TypingState.TYPING:
                signals.status_update.emit("Paused...")
        else:
            self.typing_timer.start()
            self.setFocus()

    def refresh(self):
        self.enable_typing_in = config.getint("typing_widget", "countdown")
        self.countdown_timer.stop()
        self.typing_timer.stop()

        self.typing_time = 0
        self.wpm = 0
        self.accuracy = 0
        signals.update_countdown.emit(self.enable_typing_in)
        signals.update_typing_time.emit(self.typing_time)
        signals.update_wpm.emit(self.wpm)
        signals.update_accuracy.emit(self.accuracy)

        self.typing_state = TypingState.UNSTARTED
        self.entered_text = ""
        self.target_text = None

    @QtCore.pyqtSlot(str)
    def set_target_text(self, lesson_name):
        self.refresh()
        lesson = Lesson.get_lesson_by_name(lesson_name)
        self.target_text = lesson.content
        self.update_display()
        signals.status_update.emit("Ready.")
        self.setDisabled(True)

    def keyPressEvent(self, event):
        if self.typing_state is TypingState.FINISHED \
                or self.target_text is None:
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

        if self.typing_state == TypingState.UNSTARTED \
                or len(entered_text) == 0:
            display_text = '<span style="color:{}">{}</span>'.format(
                "green", self.target_text
            )
            self.setText(display_text)
            return

        display_text = ""
        greens, reds = 0, 0
        for char_entered, char_target in zip(entered_text, target_text):
            if char_entered == char_target:
                color = "green"
                greens += 1
            else:
                color = "red"
                reds += 1
                # replace red (incorrect) spaces with red asterix
                if char_target == " ":
                    char_target = "*"

            display_text += '<span style="color:{}">{}</span>'.format(
                color, char_target
            )

        if len_entered > 0:
            self.accuracy = int(greens / (greens + reds) * 100)

        display_text += target_text[len_entered:]
        self.setText(display_text)

        cursor = self.textCursor()
        cursor.setPosition(len_entered, QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

        scrollbar = self.verticalScrollBar()
        scroll_value = scrollbar.value()
        current_position = scrollbar.sliderPosition()
        scrollbar_increment = 200
        if current_position > 0:
            scrollbar.setSliderPosition(scrollbar.sliderPosition() + scrollbar_increment)

        """
        current_row = self.textCursor().blockNumber() + 1  # not much love there...

        scrollbar = self.verticalScrollBar()
        target_vertical_scroll = min(scrollbar.maximum(), current_row + 4)
        self.verticalScrollBar().setValue(target_vertical_scroll)
        print(current_row, scrollbar.maximum(), target_vertical_scroll)

        block = cursor.block()
        print(block.firstLineNumber(), block.length(), block.lineCount(), block.position(), cursor.positionInBlock())
        """

        if len_entered >= len_target:
            self.typing_state = TypingState.FINISHED
            self.typing_timer.stop()
            self.set_disabled(True)
            signals.status_update.emit("Finished exercise...")
            return
