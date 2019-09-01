from PyQt5 import QtWidgets
from ..lessons import Lessons


class LessonsWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        headers = QtWidgets.QTreeWidgetItem(["Lessons"])
        self.setHeaderItem(headers)
        lessons = self.lessons = Lessons()

        for section in lessons.sections.keys():
            section_root = QtWidgets.QTreeWidgetItem(self, [section])
            for lesson in lessons.sections[section]:
                lesson_item = QtWidgets.QTreeWidgetItem(section_root, [str(lesson)])
