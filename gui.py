from common import ApplicationConfig

from PySide2.QtGui import QColor, QFont, QFontDatabase, QPalette
from PySide2.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget

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
        
    def _initialize_widget(self) -> None:
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("black"))
        palette.setColor(QPalette.Text, QColor("yellow"))

        self.setAutoFillBackground(True)
        self.setPalette(palette)

        font_db = QFontDatabase()
        font = font_db.font("Digital-7 Mono", "mono", 64)
        self.setFont(font)

        init_string = ""
        for i in range(0, self.config.led_screen_width):
            init_string += " "
        self.setText(init_string)


class ControlPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()