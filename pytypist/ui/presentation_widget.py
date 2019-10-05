import os
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from .signals import signals


class PresentationWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.browser = browser = QtWebEngineWidgets.QWebEngineView()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(browser)
        self.setLayout(vbox)
        signals.section_selected.connect(self.section_selected)

    def load(self, name):
        index_path = get_presentation_index(name)
        url = QtCore.QUrl().fromLocalFile(index_path)
        self.browser.load(url)

    @QtCore.pyqtSlot(str)
    def section_selected(self, section):
        self.load(section)
