from PyQt5 import QtWidgets


class LessonsWidget(QtWidgets.QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        lessons = [
            "lesson 1",
            "lesson 2"
        ]
        for lesson in lessons:
            self.addItem(lesson)
    