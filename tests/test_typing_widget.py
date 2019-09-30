"""
from PyQt5 import QtWidgets, QtCore, QtGui
from pytypist.ui.typing_widget import TypingWidget


def test_typing_widget(qtbot):
    win = QtWidgets.QMainWindow()
    widget = TypingWidget(win)
    [qtbot.addWidget(w) for w in [win, widget]]

    # we start with no text in the widget
    assert widget.toPlainText() == ""

    # check our starting conditions
    target_text = "some target text"
    widget.set_target_text(target_text)
    assert widget.toPlainText() == target_text
    assert widget.entered_text == ""
    assert widget.finished is False

    # send keys to the widget
    keys = [QtCore.Qt.Key_S, QtCore.Qt.Key_O, QtCore.Qt.Key_X, QtCore.Qt.Key_E]
    for key in keys:
        QtCore.QCoreApplication.sendEvent(
            widget,
            QtGui.QKeyEvent(QtCore.QEvent.KeyPress, key, QtCore.Qt.NoModifier),
        )

    text = widget.toHtml()
"""
