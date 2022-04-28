from common import ApplicationConfig
from gui import MainWindow

from PySide2.QtGui import QFontDatabase
from PySide2.QtWidgets import QApplication


def register_included_fonts() -> None:
    QFontDatabase.addApplicationFont("res/digital-7 (mono).ttf")


if __name__ == "__main__":
    app = QApplication([])
    config = ApplicationConfig()

    register_included_fonts()

    window = MainWindow(config)
    window.show()
    app.exec_()