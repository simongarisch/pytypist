from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from .signals import signals
from ..lessons import Section


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

    def load(self, file_path):
        url = QtCore.QUrl().fromLocalFile(file_path)
        self.browser.load(url)
        signals.status_update.emit("Ready.")

    @QtCore.pyqtSlot(str)
    def section_selected(self, section_name):
        section = Section.get_section_by_name(section_name)
        if not isinstance(section, Section):
            raise TypeError("Expected Section instance.")
        file_path = section.collect_slides()
        self.load(file_path)
