from PyQt5 import QtWidgets, QtGui
from .signals import signals
from .ui_settings import config
from ..lessons import Lessons


class LessonsWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        font = QtGui.QFont()
        font.setPointSize(config.getint("lessons_widget", "font_size"))
        self.setFont(font)

        headers = QtWidgets.QTreeWidgetItem(["Lessons"])
        self.setHeaderItem(headers)
        lessons = self.lessons = Lessons()
        sections = lessons.sections

        for section in sections.keys():
            section_root = QtWidgets.QTreeWidgetItem(self, [section])
            for lesson in sections[section].keys():
                lesson_item = QtWidgets.QTreeWidgetItem(section_root, [lesson])

        self.lesson_names = [str(lesson) for lesson in lessons.lessons]
        self.itemClicked.connect(self.on_clicked)

    def on_clicked(self, item, column):
        text = item.text(column)
        if text in self.lesson_names:  # we haven't clicked on a section
            signals.lesson_selected.emit(text)
