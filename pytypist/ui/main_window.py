import os
from PyQt5 import QtWidgets, QtGui, QtCore
from .typing_widget import TypingWidget
from .lessons_widget import LessonsWidget
from .ui_settings import config


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_style()
        self.setup_ui()
        self.show()

    def setup_style(self):
        dire_name = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(
            dire_name, "style_sheets", "elegant-dark.qss"
        )
        with open(file_name, "r") as target_file:
            self.setStyleSheet(target_file.read())

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

        # create the widgets
        left_frame = QtWidgets.QFrame()
        right_frame = QtWidgets.QFrame()
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        splitter.addWidget(left_frame)
        splitter.addWidget(right_frame)
        splitter.setSizes([25, 75])

        lessons_widget = self.lessons_widget = LessonsWidget(left_frame)
        typing_widget = self.typing_widget = TypingWidget(right_frame)
        left_vbox = QtWidgets.QVBoxLayout()
        left_vbox.addWidget(lessons_widget)
        left_frame.setLayout(left_vbox)

        right_vbox = QtWidgets.QVBoxLayout()
        right_vbox.addWidget(typing_widget)
        right_frame.setLayout(right_vbox)

        self.setCentralWidget(splitter)
