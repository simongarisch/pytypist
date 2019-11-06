from PyQt5 import QtCore
from pytypist.ui.lessons_widget import LessonsWidget
from pytypist.ui.signals import signals


def test_lessons_widget(qtbot):
    widget = LessonsWidget(None)
    qtbot.addWidget(widget)

    section_selected = lesson_selected = None

    @QtCore.pyqtSlot(str)
    def on_lesson_select(name):
        nonlocal lesson_selected
        lesson_selected = name

    @QtCore.pyqtSlot(str)
    def on_section_select(name):
        nonlocal section_selected
        section_selected = name

    signals.lesson_selected.connect(on_lesson_select)
    signals.section_selected.connect(on_section_select)

    item = widget.topLevelItem(0)
    widget.itemClicked.emit(item, 0)

    assert section_selected == "The Home Row"
    assert lesson_selected is None

    section_selected = lesson_selected = None

    item = widget.topLevelItem(0).child(0)
    widget.itemClicked.emit(item, 0)

    assert section_selected is None
    assert lesson_selected == "Keys 'asdf'"
