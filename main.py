from common import ApplicationConfig
from gui import MainWindow

from PySide2.QtCore import QThreadPool
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

    thread_pool = QThreadPool()
    
    for runnable in config.registered_runnables.values():
        thread_pool.start(runnable)

    app.exec_()

    for runnable in config.registered_runnables.values():
        runnable.kill()