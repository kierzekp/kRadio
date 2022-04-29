from time import sleep

from common import ApplicationConfig

from PySide2.QtCore import QRunnable, Slot
from PySide2.QtGui import QColor, QFontDatabase, QPalette
from PySide2.QtWidgets import QDial, QLabel, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, config: ApplicationConfig) -> None:
        super().__init__()
        self.config = config
        self.setCentralWidget(self._initialize_contents())

        self.show()

    def _initialize_contents(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout()
        
        self.led_screen = LEDScreen(self.config)
        layout.addWidget(self.led_screen)

        self.control_panel = ControlPanel()
        layout.addWidget(self.control_panel)

        container.setLayout(layout)
        return container


class LEDScreen(QLabel):
    def __init__(self, config: ApplicationConfig) -> None:
        super().__init__()
        self.config = config

        self._initialize_widget()

        scroll_task = LEDScreenScrollTask(self, "TESTING")
        self.config.registered_runnables["led"] = scroll_task
        
    def _initialize_widget(self) -> None:
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("black"))
        palette.setColor(QPalette.WindowText, QColor("yellow"))

        self.setAutoFillBackground(True)
        self.setPalette(palette)

        font_db = QFontDatabase()
        font = font_db.font("Digital-7 Mono", "mono", 64)
        self.setFont(font)

        self.setText(self.get_empty_string_for_led_width())

    def get_empty_string_for_led_width(self) -> str:
        string = ""
        for i in range(0, self.config.led_screen_width):
            string += " "
        return string


class LEDScreenScrollTask(QRunnable):
    def __init__(self, led_screen: LEDScreen, text_to_scroll: str) -> None:
        super().__init__()

        self.time_between_updates = 0.5
        self.led_screen = led_screen
        self.text_to_scroll = text_to_scroll
        self.text_to_display = text_to_scroll

        self.current_text_offset = 0

        self.is_killed = False

    @Slot()
    def run(self):
        while True:
            if self.is_killed:
                return

            self.scroll_text()
            sleep(self.time_between_updates)

    def scroll_text(self) -> None:
        led_length = self.led_screen.config.led_screen_width
        text_length = len(self.text_to_scroll)

        if self.current_text_offset >= 0 and self.current_text_offset <= text_length:
            self.text_to_display.strip()
            if self.current_text_offset != 0:
                self.text_to_display = self.text_to_display[1:]
        else:
            if self.current_text_offset > text_length:
                self.current_text_offset = (-1) * led_length
            self.text_to_display = self.led_screen.get_empty_string_for_led_width()[:abs(self.current_text_offset)-1] + self.text_to_scroll

        if len(self.text_to_display) > led_length:
            self.text_to_display = self.text_to_display[:led_length]
        
        self.current_text_offset += 1
        self.led_screen.setText(self.text_to_display)
        self.led_screen.update()

    def kill(self) -> None:
        self.is_killed = True


class ControlPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._initialize_widget()


    def _initialize_widget(self) -> None:
        layout = QHBoxLayout()

        self.preset_chooser = QWidget() # placeholder
        layout.addWidget(self.preset_chooser)

        self.dial = QDial()
        self.dial.setRange(0, 100)
        self.dial.setSingleStep(1)
        layout.addWidget(self.dial)

        self.setLayout(layout)