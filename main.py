import sys
from PyQt5 import QtWidgets
import pytypist


def main():
    app = QtWidgets.QApplication(sys.argv)
    pytypist.ui.MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
