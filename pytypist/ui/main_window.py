from PyQt5 import QtWidgets
from .typing_widget import TypingWidget
from .ui_settings import config


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
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

        typing_widget = self.typing_widget = TypingWidget(self)
        self.setCentralWidget(typing_widget)
