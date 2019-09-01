import os
from PyQt5 import QtWidgets, QtGui
from .typing_widget import TypingWidget
from .lessons_widget import LessonsWidget
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

        # create the widgets
        frame = QtWidgets.QFrame()
        lessons_widget = self.lessons_widget = LessonsWidget(frame)
        typing_widget = self.typing_widget = TypingWidget(frame)

        # set the size policy
        # https://www.riverbankcomputing.com/static/Docs/PyQt4/qsizepolicy.html#Policy-enum
        lessons_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )

        # set layout
        hbox = QtWidgets.QHBoxLayout(frame)
        hbox.addWidget(lessons_widget)
        hbox.addWidget(typing_widget)
        self.setCentralWidget(frame)
