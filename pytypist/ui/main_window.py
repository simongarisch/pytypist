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
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        left_frame = QtWidgets.QFrame(splitter)
        right_frame = QtWidgets.QFrame(splitter)

        splitter.addWidget(left_frame)
        splitter.addWidget(right_frame)
        splitter.setSizes([25, 75])

        lessons_widget = self.lessons_widget = LessonsWidget(left_frame)
        typing_widget = self.typing_widget = TypingWidget(right_frame)

        """
        # set the size policy
        # https://www.riverbankcomputing.com/static/Docs/PyQt4/qsizepolicy.html#Policy-enum
        for frame in [left_frame, right_frame]:
            frame.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding
            )

        lessons_widget.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.Expanding
        )
        """
        # set layout
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        #left_frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        splitter.addWidget(left_frame)
        splitter.addWidget(right_frame)
        splitter.setSizes([25, 75])
        #hbox = QtWidgets.QHBoxLayout(frame)
        #hbox.addWidget(lessons_widget)
        #hbox.addWidget(typing_widget)
        #self.setCentralWidget(frame)
        self.setCentralWidget(splitter)
