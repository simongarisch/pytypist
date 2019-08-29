import os
from PyQt5 import QtWidgets, QtGui
from .typing_widget import TypingWidget
from .ui_settings import config


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setWindowTitle(
            config.get("main_window", "title")
        )

        self.resize(
            config.getint("main_window", "width"),
            config.getint("main_window", "height")
        )

        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            config.get("main_window", "icon")
        )
        self.setWindowIcon(QtGui.QIcon(icon_path))

        typing_widget = self.typing_widget = TypingWidget(self)
        self.setCentralWidget(typing_widget)
