from time import sleep

from common import ApplicationConfig

from PySide2.QtCore import QRunnable, Slot
from PySide2.QtGui import QColor, QFontDatabase, QPalette
from PySide2.QtWidgets import QDial, QGridLayout, QLabel, QMainWindow, QPushButton, QStyle, QHBoxLayout, QVBoxLayout, QWidget

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

        self.control_panel = ControlPanel(self.config)
        layout.addWidget(self.control_panel)

        container.setLayout(layout)
        return container


class LEDScreen(QLabel):
    def __init__(self, config: ApplicationConfig) -> None:
        super().__init__()
        self.config = config

        self._initialize_widget()

        scroll_task = LEDScreenScrollTask(self, "kradio - internet radio music player")
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

class ControlPanel(QWidget):
    def __init__(self, config: ApplicationConfig) -> None:
        super().__init__()
        self.config = config
        self._initialize_widget()


    def _initialize_widget(self) -> None:
        layout = QHBoxLayout()

        self.preset_chooser = PresetChooser(self.config)
        layout.addWidget(self.preset_chooser)

        self.playback_controls = PlaybackControls()
        layout.addWidget(self.playback_controls)

        self.setLayout(layout)


class PresetChooser(QWidget):
    def __init__(self, config: ApplicationConfig) -> None:
        super().__init__()
        self.config = config

        self.presets = ["1", "2", "3", "4", "5", "6"]

        self._initialize_widget()

    def _initialize_widget(self) -> None:
        layout = QGridLayout()

        first_row_length = int(len(self.presets) // 2)

        for index in range(0, first_row_length):
            preset = self.presets[index]
            preset_button = QPushButton()
            preset_button.setText(str(index))

            layout.addWidget(preset_button, 0, index)

        for index in range(first_row_length, len(self.presets)):
            preset = self.presets[index]
            preset_button = QPushButton()
            preset_button.setText(str(index))

            layout.addWidget(preset_button, 1, index-first_row_length)

        self.setLayout(layout)


class PlaybackControls(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._initialize_widget()

    def _initialize_widget(self) -> None:
        layout = QVBoxLayout()

        self.dial = QDial()
        self.dial.setRange(0, 100)
        self.dial.setSingleStep(1)
        layout.addWidget(self.dial)

        self.playback_button = QPushButton()
        button_style = self.playback_button.style()
        icon = button_style.standardIcon(QStyle.SP_MediaPlay)
        self.playback_button.setIcon(icon)
        layout.addWidget(self.playback_button)

        self.setLayout(layout)


class LEDScreenScrollTask(QRunnable):
    def __init__(self, led_screen: LEDScreen, text_to_scroll: str, duration: int = -1) -> None:
        super().__init__()

        self.duration = duration

        self.time_between_updates = 0.5
        self.led_screen = led_screen
        self.text_to_scroll = text_to_scroll
        self.text_to_display = text_to_scroll

        self.current_text_offset = 0

        self.is_killed = False

    @Slot()
    def run(self):
        if self.duration <= 0:
            while True:
                if self.is_killed:
                    return
                self.single_loop()

        else:
            times_to_cycle = int(self.duration / self.time_between_updates)

            for i in range(0, times_to_cycle):
                if self.is_killed:
                    return
                self.single_loop()
    
    def single_loop(self):
        self.scroll_text()
        sleep(self.time_between_updates)

    def scroll_text(self) -> None:
        led_length = self.led_screen.config.led_screen_width
        text_length = len(self.text_to_scroll)

        if self.current_text_offset >= 0 and self.current_text_offset <= text_length:
            self.text_to_display.strip()
            if self.current_text_offset != 0:
                self.text_to_display = self.text_to_scroll[self.current_text_offset:]
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