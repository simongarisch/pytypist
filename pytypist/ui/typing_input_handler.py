from PyQt5 import QtCore
from .ui_settings import config


class TypingInputHandler:
    chars_per_word = config.getint("typing_widget", "chars_per_word")
    hit_color = config.get("typing_widget", "hit_color")
    miss_color = config.get("typing_widget", "miss_color")

    def __init__(self, target_text=None):
        self.hits = self.miss = 0
        self.entered_text = ""
        self.target_text = target_text
        self.char_comparison_list = []  # with green for hit, red for miss
        self.display_text = '<span style="color:{}">{}</span>'.format(
            self.hit_color, self.target_text
        )

    def process_key_press(self, event):
        event_key = event.key()
         
        if event_key == QtCore.Qt.Key_Backspace:
            if len(self.entered_text) > 0:
                self.entered_text = self.entered_text[:-1]
                self.char_comparison_list = self.char_comparison_list[:-1]
        else:
            char_entered = event.text()
            self.entered_text += char_entered
            len_entered = len(self.entered_text)
            char_target = target_text[len_entered-1]
            if char_entered == char_target:
                color = self.hit_color
                self.hits += 1
            else:
                color = self.miss_color
                self.miss += 1
                # replace red (incorrect) spaces with red asterix
                if char_target == " ":
                    char_target = "*"
            char_text = '<span style="color:{}">{}</span>'.format(
                color, char_target
            )

            self.char_comparison_list.append(char_text)
