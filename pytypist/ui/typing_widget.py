from PyQt5 import QtWidgets, QtCore, QtGui


class TypingWidget(QtWidgets.QTextEdit):
    def __init__(self, parent):
        super().__init__("", parent)

    def set_target_text(self, text):
        self.finished = False
        self.text_entered = ""
        self.text_target = text
        self.update_display()

    def keyPressEvent(self, event):
        if self.finished:
            return
        if event.key() == QtCore.Qt.Key_Backspace:
            if len(self.text_entered) > 0:
                self.text_entered = self.text_entered[:-1]
        else:
            text = event.text()
            self.text_entered += text
        self.update_display()

    def update_display(self):
        text_entered = self.text_entered
        text_target = self.text_target

        len_entered = len(text_entered)
        len_target = len(text_target)
        if len_entered >= len_target:
            self.finished = True

        display_text = ""
        for char_entered, char_target in zip(text_entered, text_target):
            color = "green"
            if char_entered != char_target:
                color = "red"
            display_text += '<span style="color:{}">{}</span>'.format(
                color, char_target
            )
        display_text += text_target[len_entered:]
        self.setText(display_text)

        cursor = self.textCursor()
        cursor.setPosition(len_entered, QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = QtWidgets.QMainWindow()

    typing_widget = TypingWidget(win)
    typing_widget.set_target_text("This is the text to enter!")
    win.setCentralWidget(typing_widget)
    win.show()
    app.exec_()
