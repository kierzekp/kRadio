from common import ApplicationConfig
from gui_threading import GUIThreadingManager

from PySide2.QtGui import QColor, QFontDatabase, QPalette
from PySide2.QtWidgets import QDial, QGridLayout, QLabel, QMainWindow, QPushButton, QStyle, QHBoxLayout, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, config: ApplicationConfig, gui_threading_manager: GUIThreadingManager) -> None:
        super().__init__()
        self.config = config
        self.gtm = gui_threading_manager

        self.setCentralWidget(self._initialize_contents())

        self.show()

    def _initialize_contents(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout()
        
        self.led_screen = LEDScreen(self.config, self.gtm)
        layout.addWidget(self.led_screen)

        self.control_panel = ControlPanel(self.config)
        layout.addWidget(self.control_panel)

        container.setLayout(layout)
        return container


class LEDScreen(QLabel):
    def __init__(self, config: ApplicationConfig, gui_threading_manager: GUIThreadingManager) -> None:
        super().__init__()
        self.config = config
        self.gtm = gui_threading_manager

        self._initialize_widget()
        self.gtm.register_led_screen(self)
        
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
        self.playing = False
        self.playback_button.clicked.connect(self.change_button_symbol)

        layout.addWidget(self.playback_button)

        self.setLayout(layout)

    def change_button_symbol(self):
        style = self.playback_button.style()
        play_icon = style.standardIcon(QStyle.SP_MediaPlay)
        stop_icon = style.standardIcon(QStyle.SP_MediaStop)

        print(self.playing)

        if not self.playing:
            self.playback_button.setIcon(stop_icon)
            self.playing = True
        else:
            self.playback_button.setIcon(play_icon)
            self.playing = False
        self.playback_button.update()
