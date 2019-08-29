import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets


class PresentationWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.browser)
    
    @staticmethod
    def get_presentation_index(name="example"):
        dire_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(
            dire_path, "presentations", name, "index.html"
        )
        return file_path

    def load(self, name):
        index_path = get_presentation_index(name)
        self.browser.load(QtCore.QUrl().fromLocalFile(index_path))
