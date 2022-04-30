from audio import AudioPlayer
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
    audio_player = AudioPlayer()
    audio_player.set_media("https://stream.rcs.revma.com/an1ugyygzk8uv")

    register_included_fonts()

    window = MainWindow(config, gui_threading_manager, audio_player)
    window.setWindowTitle("kRadio")
    window.show()

    gui_threading_manager.add_led_screen_task_to_queue("100", 2)
    gui_threading_manager.add_led_screen_task_to_queue("200", 2)
    gui_threading_manager.add_led_screen_task_to_queue("300", 2)
    gui_threading_manager.add_led_screen_task_to_queue("end of test")

    app.exec_()

    gui_threading_manager.kill_running_threads()