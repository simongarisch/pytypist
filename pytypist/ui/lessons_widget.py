from PyQt5 import QtWidgets
from ..lessons import get_lessons


class LessonsWidget(QtWidgets.QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        lessons = self.lessons = get_lessons()
        for lesson in lessons:
            self.addItem(str(lesson))
