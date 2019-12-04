import os
from PyQt5 import QtWidgets, QtGui, QtCore
from .stats_widget import StatsWidget
from .typing_widget import TypingWidget
from .lessons_widget import LessonsWidget
from .presentation_widget import PresentationWidget
from .ui_settings import config
from .signals import signals
from ..lessons import Sections


class MainWindow(QtWidgets.QMainWindow):
    _sections = Sections()

    def __init__(self):
        super().__init__()
        self.setup_style()
        self.setup_ui()
        self.showMaximized()

    def setup_style(self):
        dire_name = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(
            dire_name, "style_sheets", "elegant-dark.qss"
        )
        with open(file_name, "r") as target_file:
            self.setStyleSheet(target_file.read())

    def setup_ui(self):
        font_name = config.get("main_window", "font_name")
        font = QtGui.QFont(font_name)
        self.setFont(font)

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
        splitter.setSizes([35, 65])

        lessons_widget = self.lessons_widget = LessonsWidget(left_frame)
        stats_widget = self.stats_widget = StatsWidget(right_frame)
        typing_widget = self.typing_widget = TypingWidget(right_frame)
        self.presentation_widget = PresentationWidget(right_frame)
        presentation_widget = self.presentation_widget
        left_vbox = QtWidgets.QVBoxLayout()
        left_vbox.addWidget(lessons_widget)
        left_frame.setLayout(left_vbox)

        right_vbox = QtWidgets.QVBoxLayout()
        right_vbox.addWidget(stats_widget)
        right_vbox.addWidget(typing_widget)
        right_vbox.addWidget(presentation_widget)
        stats_widget.hide()
        typing_widget.hide()
        right_frame.setLayout(right_vbox)

        self.setCentralWidget(splitter)

        # show a statusbar
        statusbar = self.statusbar = self.statusBar()
        statusbar.showMessage("Ready.")

        # connect the signals
        signals.lesson_selected.connect(self.lesson_selected)
        signals.section_selected.connect(self.section_selected)
        signals.status_update.connect(self.show_status_update)

    @QtCore.pyqtSlot(str)
    def show_status_update(self, message):
        self.statusbar.showMessage(message)

    @QtCore.pyqtSlot(str)
    def lesson_selected(self, *args):
        self.presentation_widget.hide()
        self.stats_widget.show()
        self.typing_widget.show()

    @QtCore.pyqtSlot(str)
    def section_selected(self, *args):
        self.presentation_widget.show()
        self.stats_widget.hide()
        self.typing_widget.hide()
