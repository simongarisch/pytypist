import os
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from .signals import signals
from ..lessons import Section, Sections


class PresentationWidget(QtWidgets.QWidget):
    _sections = Sections()

    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.browser = browser = QtWebEngineWidgets.QWebEngineView()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(browser)
        self.setLayout(vbox)
        signals.section_selected.connect(self.section_selected)

    def load(self, file_path):
        url = QtCore.QUrl().fromLocalFile(file_path)
        self.browser.load(url)

    @QtCore.pyqtSlot(str)
    def section_selected(self, section_name):
        section = self._sections[section_name]
        if not isinstance(section, Section):
            raise TypeError("Expected Section instance.")
        file_path = section.collect_slides()
        self.load(file_path)
