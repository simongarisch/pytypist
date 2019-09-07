import os
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class PresentationError(Exception):
    """ Base exception relating to presentations. """


class PresentationNotFound(PresentationError):
    """ Unable to find index.html. """


def get_presentation_index(name="example"):
    dire_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "presentations",
        name
    )

    # check for index.html in the root directory
    file_path = os.path.join(dire_path, "index.html")
    if os.path.isfile(file_path):
        return file_path

    # also check in 'site_folder'
    file_path = os.path.join(dire_path, "site_folder", "index.html")
    if os.path.isfile(file_path):
        return file_path

    raise PresentationNotFound("Cannot find index.html.")


class PresentationWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.browser)

    def load(self, name):
        index_path = get_presentation_index(name)
        self.browser.load(QtCore.QUrl().fromLocalFile(index_path))
