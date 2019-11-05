from PyQt5 import QtGui, QtCore
from pytypist.lessons import Lesson
from pytypist.ui.typing_widget import TypingWidget, TypingState


def test_typing_widget(qtbot):
    widget = TypingWidget(None)
    qtbot.addWidget(widget)

    # we start with no text in the widget
    assert widget.toPlainText() == ""

    # check our starting conditions
    lesson_name = "Keys 'asdf'"
    lesson = Lesson.get_lesson_by_name(lesson_name)
    target_text = lesson.content

    widget.set_target_text(lesson_name)
    assert widget.toPlainText() == target_text
    assert widget.entered_text == ""
    assert widget.typing_state is TypingState.UNSTARTED

    # send keys to the widget
    widget.start_typing()
    chars = ["a", "s", "d", "f", " "]
    keys = [
        QtCore.Qt.Key_A,
        QtCore.Qt.Key_S,
        QtCore.Qt.Key_D,
        QtCore.Qt.Key_F,
        QtCore.Qt.Key_Space,
    ]
    for key, char in zip(keys, chars):
        event = QtGui.QKeyEvent(
            QtCore.QEvent.KeyPress,
            key,
            QtCore.Qt.NoModifier,
            char
        )
        widget.keyPressEvent(event)

    # entered text should be walled off in a span
    html = widget.toHtml()
    section = '<span style=" color:#008000;">asdf </span>asdf asdf '
    assert section in html

    assert widget.typing_state is TypingState.TYPING
    remaining_text = target_text[len(chars):]

    # put in some wrong text
    key = QtCore.Qt.Key_Z
    char = "z"
    event = QtGui.QKeyEvent(
        QtCore.QEvent.KeyPress,
        key,
        QtCore.Qt.NoModifier,
        char
    )
    [widget.keyPressEvent(event) for _ in remaining_text]

    html = widget.toHtml()
    section = """
        <span style=" color:#008000;">asdf </span>
        <span style=" color:#ff0000;">asdf*asdf*asdf*aaaa*
            ssss*dddd*ffff*asdf*asdf*adsf*asdf*aa*ss*dd*ff*
            aa*ss*dd*ff*asdf*asdf*asdf*asdf*afsd*afsd*afsd*
            afsd*ffff*dddd*ssss*aaaa*aaaa*ssss*dddd*ffff*
            afs*afs*afd*afd*afs*saf*sass*safd*afds*saddf*
            saf*sad*sass*asdf*asdf*asdf*asdf
        </span>
    """
    section = section.replace("\n", "")
    section = section.replace(" ", "")
    html = html.replace(" ", "")
    assert section in html
