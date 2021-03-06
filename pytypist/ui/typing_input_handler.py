from collections import namedtuple
from PyQt5 import QtCore
from .ui_settings import config
from .signals import thread_pool
from .. import db


TypingError = namedtuple(
    "TypingError",
    "lesson_name char_entered char_target"
)


class SaveTypingErrorsTask(QtCore.QRunnable):
    def __init__(self, typing_error):
        super().__init__()
        if not isinstance(typing_error, TypingError):
            raise TypeError("Expected instance of TypingError.")
        self._typing_error = typing_error

    def run(self):
        db.populate_typing_error(self._typing_error)


class TypingInputHandler:
    hit_color = config.get("typing_widget", "hit_color")
    miss_color = config.get("typing_widget", "miss_color")

    def refresh(self, lesson_name=None, target_text=None):
        self.lesson_name = lesson_name
        self.hits = self.miss = 0
        self.accuracy = 0
        self.entered_text = ""
        self.target_text = target_text
        self.char_comparison_list = []
        self.finished = False
        if target_text is not None:
            self.display_text = '<span style="color:{}">{}</span>'.format(
                self.hit_color, self.target_text
            )
        else:
            self.display_text = ""

    def process_key_press(self, event):
        target_text = self.target_text
        if target_text is None:
            return
        event_key = event.key()

        if event_key == QtCore.Qt.Key_Backspace:
            if len(self.entered_text) > 0:
                self.entered_text = self.entered_text[:-1]
                self.char_comparison_list = self.char_comparison_list[:-1]
        else:
            char_entered = event.text()
            if len(char_entered) == 0:
                return
            self.entered_text += char_entered
            len_entered = len(self.entered_text)
            char_target = target_text[len_entered-1]
            if char_entered == char_target:
                color = self.hit_color
                self.hits += 1
            else:
                color = self.miss_color
                self.miss += 1
                # update our records for this typing error
                typing_error = TypingError(
                    self.lesson_name, char_entered, char_target
                )
                task = SaveTypingErrorsTask(typing_error)
                thread_pool.start(task)
                # replace red (incorrect) spaces with red asterix
                if char_target == " ":
                    char_target = "*"
            char_text = '<span style="color:{}">{}</span>'.format(
                color, char_target
            )

            self.accuracy = int(self.hits / (self.hits + self.miss) * 100)
            self.char_comparison_list.append(char_text)

        entered_text = "".join(self.char_comparison_list)
        remaining_text = target_text[len(self.entered_text):]
        self.display_text = entered_text + remaining_text
        if len(self.entered_text) >= len(target_text):
            self.finished = True
