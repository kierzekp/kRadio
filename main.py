from common import ApplicationConfig
from gui import MainWindow
from gui_threading import GUIThreadingManager

from PySide2.QtCore import QThreadPool
from PySide2.QtGui import QFontDatabase
from PySide2.QtWidgets import QApplication


def register_included_fonts() -> None:
    QFontDatabase.addApplicationFont("res/digital-7 (mono).ttf")


if __name__ == "__main__":
    app = QApplication([])
    config = ApplicationConfig()
    thread_pool = QThreadPool()
    gui_threading_manager = GUIThreadingManager(thread_pool)

    register_included_fonts()

    window = MainWindow(config, gui_threading_manager)
    window.setWindowTitle("kRadio")
    window.show()

    gui_threading_manager.set_current_led_screen_task("1234567890test")

    app.exec_()

    gui_threading_manager.stop_current_led_screen_task()