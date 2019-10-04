import os
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from .signals import signals


def get_presentation_index(section):
    """ Get the index.html file associate with a presentation. """
    name = str(name).lower().replace(" ", "_")
    dire_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "presentations",
        name
    )

    # check for index.html in the root directory
    file_path = os.path.join(dire_path, "slides.html")
    if os.path.isfile(file_path):
        return file_path

    # also check in 'site_folder'
    file_path = os.path.join(dire_path, "site_folder", "slides.html")
    if os.path.isfile(file_path):
        return file_path

    raise PresentationNotFound("Cannot find slides.html.")


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
