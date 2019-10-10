from PyQt5 import QtWidgets, QtGui
from .signals import signals
from .ui_settings import config
from ..lessons import Lesson, Sections


class LessonsWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        font_name = config.get("lessons_widget", "font_name")
        font_size = config.getint("lessons_widget", "font_size")
        font = QtGui.QFont(font_name, font_size, QtGui.QFont.Monospace)
        font.setWeight(QtGui.QFont.Light)
        self.setFont(font)

        headers = QtWidgets.QTreeWidgetItem(["Lessons"])
        self.setHeaderItem(headers)
        sections = Sections()

        for section_name in sections:
            section = sections[section_name]
            section_root = QtWidgets.QTreeWidgetItem(self, [section_name])
            for lesson_name in section:
                QtWidgets.QTreeWidgetItem(section_root, [lesson_name])

        self.section_names = list(sections)
        self.lesson_names = Lesson.list_names()
        self.itemClicked.connect(self.on_clicked)

    def on_clicked(self, item, column):
        text = item.text(column)
        if text in self.lesson_names:
            # lesson clicked, so start lesson
            signals.lesson_selected.emit(text)
        if text in self.section_names:
            # section clicked, so start presentation
            signals.section_selected.emit(text)
